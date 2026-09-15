"""从 Git 对象核对记录归属、历史映射与逐路径增量。"""

from __future__ import annotations

import difflib
from functools import lru_cache
from pathlib import Path

from .git_ops import run_git
from .record_context import LINKS, RecordContext, require


@lru_cache(maxsize=128)
def entries(repo: Path, revision: str) -> dict:
    """返回全部叶子项，模式/类型与 blob 身份均参与比较。"""
    raw = run_git(repo, "ls-tree", "-r", "-z", revision, text=False)
    return {row.split(b"\t", 1)[1].decode("utf-8"): row.split(b"\t", 1)[0].decode("ascii")
            for row in raw.split(b"\0") if row}


def parent_of(repo: Path, sha: str) -> str:
    """仅接受有一个直接父提交的目标记录。"""
    parents = str(run_git(repo, "show", "-s", "--format=%P", sha)).split()
    require(len(parents) == 1, f"目标不是线性提交：{sha}")
    return parents[0]


def changed(repo: Path, old: str, new: str) -> list:
    """读取真实改变的路径，包括类型/模式变化和删除。"""
    raw = run_git(repo, "diff", "--name-only", "--no-renames", "-z", old, new, text=False)
    return [value.decode("utf-8") for value in raw.split(b"\0") if value]


def target_message(repo: Path, sha: str) -> list:
    """读取原始提交消息，不运行 format/cleanup。"""
    raw = run_git(repo, "cat-file", "commit", sha, text=False)
    return raw.split(b"\n\n", 1)[1].decode("utf-8").splitlines()


def check_pair(context: RecordContext, lane: str, old: str, source: str, initialization=False) -> str:
    """验证目标来源不变及允许的 gitlink 派生差异。"""
    repo, new = context.repos[lane], context.target(lane, old)
    trailer = "Treeland-Initialization" if initialization else "Treeland-Commit"
    for sha in dict.fromkeys((old, new)):
        values = [line for line in target_message(repo, sha) if line.startswith(trailer + ":")]
        require(values == [f"{trailer}: {source}"], f"{lane} 来源与目标错配：{sha}")
    if new == old:
        return new
    require(parent_of(repo, new) == context.target(lane, parent_of(repo, old)), f"{lane} 映射拓扑错误")
    before, after = entries(repo, old), entries(repo, new).copy()
    require(before.keys() == after.keys(), f"{lane} 历史映射改变了路径集合")
    if lane in LINKS:
        path, lower = LINKS[lane]
        if path in before:
            mode, kind, target = before[path].split()
            require((mode, kind) == ("160000", "commit"), f"{lane} 依赖不是 gitlink")
            expected = context.target(lower, target)
            require(after[path] == f"160000 commit {expected}", f"{lane} 旧新 gitlink 错配")
            after[path] = before[path]
    require(after == before, f"{lane} 历史映射混入普通文件变化")
    return new


def check_transition(context: RecordContext, lane: str, old: str, transition: dict) -> None:
    """依赖前后 SHA 必须同时与旧树和新树匹配。"""
    if transition is None:
        return
    path, lower = LINKS[lane]
    require(lower in context.repos, f"{lane} 缺少依赖仓库 {lower}")
    repo = context.repos[lane]
    for revision, key in ((parent_of(repo, old), "from"), (old, "to")):
        entry = entries(repo, revision).get(path)
        value = entry.split()[-1] if entry else None
        require(value == transition.get(key), f"{lane} 依赖 {key} 与原 Git 树不符")
        mapped_revision = context.target(lane, revision)
        actual = entries(repo, mapped_revision).get(path)
        expected = context.target(lower, value)
        require((actual.split()[-1] if actual else None) == expected, f"{lane} 新依赖 {key} 不符")
        if expected:
            run_git(context.repos[lower], "cat-file", "-e", f"{expected}^{{commit}}")


def check_history(context: RecordContext, nodes: list, rows: dict) -> None:
    """验证所有本仓记录完整覆盖连续历史，不漏掉空提交或初始化。"""
    for lane, repo in context.repos.items():
        active = [node for node in nodes if node["bases"].get(lane) is not None]
        require(bool(active) or not rows[lane], f"{lane} 缺少基线")
        if not active:
            continue
        base, head = active[0]["bases"][lane], active[-1]["heads"][lane]
        for previous, following in zip(active, active[1:]):
            require(previous["heads"][lane] == following["bases"][lane], f"{lane} 节点不连续")
        expected = str(run_git(repo, "rev-list", "--reverse", f"{base}..{head}")).split()
        require(expected == [row["old"] for row in rows[lane]], f"{lane} 本仓记录未完整覆盖历史")
        if lane in context.history:
            info = context.history[lane]
            require((info["base"], info["old_head"]) == (base, head), f"{lane} 映射范围错配")
            require(list(info["mapping"]) == expected, f"{lane} 映射遗漏或多出提交")
            new = str(run_git(repo, "rev-list", "--reverse", f"{base}..{info['new_head']}")).split()
            require(new == [context.target(lane, sha) for sha in expected], f"{lane} 新区间不匹配")


def source_paths(item: dict, lane: str, path: str) -> list:
    """由 inventory 实际映射找来源路径，不从主题推断。"""
    if lane == "parent":
        result = [side["source"] for change in item["changes"] for side in (change["old"], change["new"])
                  if side and side.get("target") == path]
    elif lane == "child":
        result = [path] if path in item["waylib_shared"]["source_paths"] else []
    else:
        result = [f"3rdparty/wlroots/{path}"] if path in item["wlroots"]["target_paths"] else []
    return list(dict.fromkeys(result))


def _increment(repo: Path, before: str, after: str, paths: list) -> str:
    if not paths:
        return ""
    raw = str(run_git(repo, "diff", "--no-ext-diff", "--no-textconv", "--no-renames",
                      "--unified=0", before, after, "--", *paths))
    lines = raw.splitlines(keepends=True)
    return "".join(line for line in lines if not line.startswith(("diff --git ", "index ", "--- ", "+++ ")))


def path_comparison(context: RecordContext, row: dict, path: str) -> dict:
    """对比来源增量与本仓增量，保留比较端点，绝不冒充纯适配补丁。"""
    sources = source_paths(row["item"], row["lane"], path)
    source, old = row["source"], row["old"]
    repo = context.repos[row["lane"]]
    source_before, target_before = parent_of(context.source, source), parent_of(repo, old)
    upstream = _increment(context.source, source_before, source, sources)
    local = _increment(repo, target_before, old, [path])
    comparison = "".join(difflib.unified_diff(upstream.splitlines(keepends=True), local.splitlines(keepends=True),
                                            fromfile="来源的本次增量", tofile="本仓的本次增量"))
    source_trees = (entries(context.source, source_before), entries(context.source, source))
    target_trees = (entries(repo, target_before), entries(repo, old))
    return {"sources": sources, "source_before": source_before, "target_before": target_before,
            "source_entries": [{"path": value, "before": source_trees[0].get(value),
                                "after": source_trees[1].get(value)} for value in sources],
            "target_entries": [tree.get(path) for tree in target_trees], "comparison": comparison}
