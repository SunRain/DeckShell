"""协议配套、本地修复与节点间修复的原证据和 Git 历史记录。"""

from __future__ import annotations

import json

from .artifacts import read_verified_artifact
from .git_ops import read_json, run_git
from .local_fixes import local_fix_errors
from .protocol_update import companion_lane_errors
from .record_context import LINKS, require
from .record_git import changed, entries, parent_of, target_message


def _row(context, node, lane, kind, record, notes, evidence):
    repo, head, base = context.repos[lane], record["head"], record["base"]
    require(parent_of(repo, head) == base, "特殊提交不是一个相邻线性提交")
    paths = changed(repo, base, head)
    require(sorted(paths) == sorted(record["paths"]), "特殊提交路径与 Git 不符")
    require(context.target(lane, head) == head, "特殊提交尚不支持历史改写，不能隐式替换身份")
    require(not any(line.startswith("Treeland-Commit:") for line in target_message(repo, head)),
            "特殊提交不能冒充普通 Treeland 来源")
    transition = None
    if lane in LINKS:
        path, lower = LINKS[lane]
        before, after = entries(repo, base).get(path), entries(repo, head).get(path)
        if before != after:
            require(after is not None and after.startswith("160000 commit "), "特殊提交依赖类型错误")
            target = after.split()[-1]
            run_git(context.repos[lower], "cat-file", "-e", target + "^{commit}")
            transition = {"status": "updated", "from": before.split()[-1] if before else None, "to": target}
    return {"kind": kind, "lane": lane, "node": node["name"], "node_path": node["path"],
            "source": None, "old": head, "target": head, "base": base,
            "subject": str(run_git(repo, "show", "-s", "--format=%s", head)).strip(),
            "classification": kind, "action": kind, "content_action": kind,
            "paths": paths, "actual_paths": paths, "drop_paths": [], "structural_paths": [],
            "notes": notes, "evidence_locations": evidence, "transition": transition,
            "adaptation_paths": [], "equivalence": None, "related": {}}


def special_rows(context, node):
    """复用 companion/local-fix 校验，不把专属提交塞入普通来源计数。"""
    manifest = node["manifest"]
    root = context.node_root(node["path"])
    result = {lane: [] for lane in context.repos}
    update = manifest.get("protocol_update")
    if update is not None:
        link = entries(context.repos["parent"], update["parent"]["head"]).get(LINKS["parent"][0])
        require(link == "160000 commit " + update["child"]["head"], "协议配套 P 未引用同轮 C 候选")
        for lane in ("child", "parent"):
            errors = companion_lane_errors(context.repos[lane], update, lane, root)
            require(not errors, "; ".join(errors))
            record = update[lane]
            if record["base"] == record["head"]:
                continue
            selection = update["inspection"]["protocol"]
            decision = manifest["identity"]["protocol_update"].get(lane, {})
            notes = ["协议来源 " + selection["head"] + ":" + selection["head_path"],
                     "配对实现来源 " + update["inspection"]["implementation"]["head"],
                     decision.get("reason") or "按原协议配对更新受控快照/配对元数据及依赖引用；不计为普通来源回放。"]
            result[lane].append(_row(context, node, lane, "protocol-companion", record, notes,
                                     ["manifest.json#protocol_update", record["target_diff"]["path"]]))
    fix = manifest.get("local_fix")
    if fix is not None:
        errors = local_fix_errors(manifest, root)
        require(not errors, "; ".join(errors))
        approval = json.loads(read_verified_artifact(fix["approval"], root, "local approval")[1])
        for lane in ("child", "parent"):
            result[lane].append(_row(context, node, lane, "local-fix", fix[lane],
                                     [fix["reason"], approval["authorization"]],
                                     [fix["approval"]["path"], fix[lane]["target_diff"]["path"]]))
    return result


def bridge_rows(context, previous, node, descriptors):
    """仅按显式原接受凭据解释节点间差异；未知间隙依旧拒绝。"""
    result = {lane: [] for lane in context.repos}
    seen = set()
    for descriptor in descriptors:
        lane = descriptor["lane"]
        require(previous is not None and lane in context.repos and lane not in seen, "节点间修复归属重复或无前节点")
        seen.add(lane)
        path = context.node_root(descriptor["path"])
        receipt = read_json(path)
        require(isinstance(receipt.get("kind"), str)
                and receipt["kind"].startswith("treeland-")
                and receipt["kind"].endswith("structural-repair-closeout")
                and receipt.get("schema_version") == 1, "不支持的节点间接受凭据")
        require(receipt.get("authorization", "").strip() and receipt.get("changes"), "节点间修复缺少原授权/说明")
        base, head = receipt["expected_old"], receipt["new_head"]
        require(base == previous["heads"][lane] and head == node["bases"][lane], "节点间修复端点错配")
        require(receipt.get("source_range") == "none; local structural repair only", "节点间修复冒充来源映射")
        logs = [receipt[key] for key in receipt if key.startswith("verified_") and key != "verified_worktree"]
        require(logs and all(context.node_root(log).is_file() for log in logs), "节点间修复缺少原验证日志")
        repo = context.repos[lane]
        paths = changed(repo, base, head)
        if lane in LINKS:
            link = LINKS[lane][0]
            require(entries(repo, base).get(link) == entries(repo, head).get(link), "结构修复不允许隐含依赖变化")
        record = {"base": base, "head": head, "paths": paths}
        bridge = {"name": previous["name"] + " → " + node["name"], "path": ""}
        result[lane].append(_row(context, bridge, lane, "structural-repair", record,
                                 [receipt["authorization"], *receipt["changes"], receipt.get("notes", "")],
                                 [descriptor["path"], *logs]))
    for lane in context.repos:
        if previous is not None and previous["heads"].get(lane) != node["bases"].get(lane):
            require(bool(result[lane]), f"{lane} 节点不连续，缺少原接受的独立修复")
    return result
