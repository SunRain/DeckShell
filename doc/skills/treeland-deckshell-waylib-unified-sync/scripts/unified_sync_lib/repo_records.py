"""按仓记录生成入口与不覆盖已有内容的写入边界。"""

from __future__ import annotations

import re
from pathlib import Path

from .git_ops import read_json, run_git
from .record_context import RecordContext, relative_name, require
from .record_git import check_history
from .record_initialization import initialization_node
from .record_render import render_documents
from .record_replay import replay_metadata, replay_rows


def collect_records(context: RecordContext, inputs: dict) -> tuple:
    """组合有序节点，不引入另一个同步/审批状态机。"""
    descriptors = inputs.get("nodes")
    require(isinstance(descriptors, list) and bool(descriptors), "缺少有序 nodes 输入")
    require(all(isinstance(v, dict) for v in descriptors), "nodes 条目必须为对象")
    require(len(descriptors) == len({v["name"] for v in descriptors}), "节点名称重复")
    nodes, rows = [], {lane: [] for lane in context.repos}
    for descriptor in descriptors:
        require(bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", descriptor["name"])), "节点名称无效")
        kind = descriptor.get("kind")
        if kind == "replay":
            node = replay_metadata(context, descriptor)
            source_order = str(run_git(context.source, "rev-list", "--reverse",
                                       f"{node['source_base']}..{node['source_head']}")).split()
            require(source_order == node["inventory"]["range"]["ordered_source_commits"], "来源区间覆盖不完整")
            current = replay_rows(context, node)
        elif kind == "initialization":
            node, current = initialization_node(context, descriptor)
        else:
            raise ValueError(f"未知节点类型：{kind}")
        if nodes:
            require(nodes[-1]["source_head"] == node["source_base"], "来源节点不连续")
        node["previous_runs"] = []
        for prior in descriptor.get("previous_runs", []):
            require(prior.get("kind") == "replay", "previous_runs 只接受原普通节点报告")
            previous = replay_metadata(context, prior)
            require((previous["source_base"], previous["source_head"]) == (node["source_base"], node["source_head"]),
                    "先前尝试的来源范围不匹配当前节点")
            node["previous_runs"].append(previous)
        nodes.append(node)
        for lane in rows:
            rows[lane].extend(current[lane])
    check_history(context, nodes, rows)
    return nodes, rows


def _no_symlinks(repo: Path, relative: str) -> Path:
    current = repo
    for part in Path(relative_name(relative)).parts:
        current = current / part
        require(not current.is_symlink(), f"输出路径包含符号链接：{current}")
    require(current.resolve().is_relative_to(repo), "输出路径越界")
    return current


def _preflight_output(context, documents):
    for (lane, relative), content in documents.items():
        prefix = ("doc" if lane == "parent" else "docs") + f"/treeland-sync/{context.batch}/"
        require(lane in ("parent", "child") and relative.startswith(prefix), "输出不在 P/C 批次目录")
        path = _no_symlinks(context.repos[lane], relative)
        if path.exists():
            require(path.is_file() and path.read_bytes() == content.encode("utf-8"), f"已有内容冲突：{path}")
    for lane in ("parent", "child"):
        prefix = ("doc" if lane == "parent" else "docs") + f"/treeland-sync/{context.batch}"
        directory = _no_symlinks(context.repos[lane], prefix)
        if not directory.exists():
            continue
        require(directory.is_dir(), f"输出目录冲突：{directory}")
        for path in directory.rglob("*"):
            require(not path.is_symlink(), f"批次目录内存在符号链接：{path}")
            if path.is_file():
                relative = path.relative_to(context.repos[lane]).as_posix()
                require((lane, relative) in documents, f"批次目录存在手写或其他输入的文件：{path}")


def generate_records(context: RecordContext, nodes_file: Path) -> dict:
    """验证并实际生成 P/C 记录；不暂存、提交、更新 refs 或覆盖文件。"""
    nodes, rows = collect_records(context, read_json(nodes_file))
    documents = render_documents(context, nodes, rows)
    _preflight_output(context, documents)
    for (lane, relative), content in sorted(documents.items()):
        path = _no_symlinks(context.repos[lane], relative)
        encoded = content.encode("utf-8")
        if path.exists():
            require(path.read_bytes() == encoded, f"生成期间内容发生变化：{path}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path = _no_symlinks(context.repos[lane], relative)
        with path.open("xb") as stream:
            stream.write(encoded)
    return {lane: {"records": len(rows[lane]),
                   "files": sum(role == lane for role, _ in documents),
                   "adaptations": sum(row["action"] == "adapted" for row in rows[lane])}
            for lane in ("parent", "child")}
