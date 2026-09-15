"""同步记录只消费已有证据与实际 Git 对象，不产生新验收结论。"""

from __future__ import annotations

from .artifacts import read_verified_artifact
from .git_ops import canonical_json_sha256, read_json, run_git
from .patches import commit_diff, source_patch
from .record_context import LINKS, RecordContext, relative_name, require
from .record_git import changed, check_pair, check_transition, parent_of, target_message

EVIDENCE = {
    "parent": ("parent-evidence.json", "treeland-unified-parent-evidence", "deckshell_verify"),
    "child": ("waylib-evidence.json", "treeland-unified-waylib-evidence", "waylib_verify"),
    "wlroots": ("wlroots-evidence.json", "treeland-unified-wlroots-evidence", "wlroots_verify"),
}


def load_lane_evidence(root, lane, gate, expected, inactive=False):
    """lane 证据必须完整对应 manifest，且绑定原 verifier 的摘要。"""
    filename, kind, _ = EVIDENCE[lane]
    path = root / filename
    if inactive:
        require(lane == "wlroots" and not expected and gate.get("status") == "not-applicable"
                and gate.get("target_range") is None, "不适用的 R gate 与节点身份冲突")
        if not path.exists():
            return {}
    payload = read_json(path)
    require(payload.get("kind") == kind and payload.get("schema_version") == 2, f"{lane} evidence 类型错误")
    if not inactive:
        require(gate.get("evidence_sha256") == canonical_json_sha256(payload), f"{lane} evidence 与原验证不一致")
    records = payload.get("entries")
    require(isinstance(records, list), f"{lane} evidence entries 缺失")
    require([v["source_commit"] for v in records] == expected, f"{lane} evidence 来源集合/顺序不完整")
    return {v["source_commit"]: v for v in records}


def _paths(item, lane):
    if lane == "parent":
        return item["deckshell"]["target_paths"], item["deckshell"]["drop_paths"]
    if lane == "child":
        return item["waylib_shared"]["source_paths"], item["waylib_shared"]["drop_paths"]
    return item["wlroots"]["target_paths"], item["wlroots"]["drop_paths"]


def _source_artifacts(context, root, item, lane, evidence):
    artifacts = evidence["artifacts"]
    source = item["source_commit"]
    if lane == "parent":
        fields = [("mapped_source_patch", item["deckshell"]["mapped_source_paths"]),
                  ("root_source_patch", item["deckshell"]["root_source_paths"])]
        if evidence["action"] == "gitlink-only":
            fields = [(key, paths) for key, paths in fields if key in artifacts]
    else:
        fields = [("source_patch", item["wlroots" if lane == "wlroots" else "waylib_shared"]["source_paths"])]
    for key, paths in fields:
        _, actual = read_verified_artifact(artifacts.get(key), root, f"{source}/{lane}/{key}")
        expected = source_patch(context.source, source, paths, "3rdparty/wlroots" if lane == "wlroots" else None)
        require(actual == expected, f"{lane} 来源补丁不匹配 Git 对象：{source}")


def _adaptation(evidence, root, content_action):
    paths = evidence.get("adaptation_paths", [])
    if content_action == "adapted":
        require(bool(paths) and bool(evidence.get("adaptation_notes")), "adapted 缺少逐路径理由")
        require("adaptation_patch" in evidence["artifacts"], "adapted 缺少目标相对补丁")
    for item in paths:
        relative_name(item["path"])
        require(item.get("kind") in ("modified", "materialized", "omitted"), "适配路径 kind 错误")
        require(item.get("review_state") == "approved" and bool(item.get("reason", "").strip()),
                "逐路径审核说明缺失")
        read_verified_artifact(item.get("proof"), root, f"{item['path']} proof")
    require(len(paths) == len({p["path"] for p in paths}), "重复的适配路径")
    if content_action == "empty":
        _, content = read_verified_artifact(evidence.get("equivalence_proof"), root, "empty equivalence proof")
        return content.decode("utf-8")
    return None


def _content_check(context, root, item, lane, result, evidence):
    source, old = item["source_commit"], result["commit"]
    require(evidence.get("target_commit") == old and evidence.get("source_commit") == source,
            f"{lane} evidence 目标错配")
    for key in ("action", "adaptation_notes", "adaptation_paths"):
        require(evidence.get(key) == result.get(key), f"{lane} manifest/evidence {key} 不一致")
    require(evidence.get("classification") == item["classification"], f"{lane} 归属错配")
    paths, drops = _paths(item, lane)
    require(evidence.get("drop_paths") == drops, f"{lane} 排除路径错配")
    artifacts = evidence.get("artifacts")
    require(isinstance(artifacts, dict) and "target_diff" in artifacts, f"{lane} 关键证据缺失")
    for name, record in artifacts.items():
        read_verified_artifact(record, root, f"{source}/{lane}/{name}")
    _, actual = read_verified_artifact(artifacts["target_diff"], root, f"{lane} target_diff")
    require(actual == commit_diff(context.repos[lane], old), f"{lane} 目标差异与 Git 对象不符")
    _source_artifacts(context, root, item, lane, evidence)
    content_action = evidence.get("content_action", evidence["action"])
    if lane == "child":
        require(content_action == result.get("content_action"), f"{lane} content_action 不一致")
    elif lane == "wlroots":
        require(content_action == result["action"], "R 不存在独立于 action 的依赖 content_action")
    proof = _adaptation(evidence, root, content_action)
    return paths, drops, content_action, proof


def build_row(context: RecordContext, node: dict, item: dict, entry: dict, lane: str, evidence: dict) -> dict:
    """生成一个本仓事实行；纯 gitlink 不继承下游源码适配。"""
    result, source = entry[lane], item["source_commit"]
    root = context.node_root(node["path"])
    paths, drops, content_action, proof = _content_check(context, root, item, lane, result, evidence)
    old = result["commit"]
    new = check_pair(context, lane, old, source)
    action = evidence["action"]
    require(action in ("applied", "adapted", "empty", "gitlink-only"), f"未知 action：{action}")
    for sha in dict.fromkeys((old, new)):
        message = target_message(context.repos[lane], sha)
        require(message.count(f"[treeland-unified-sync] action: {action}") == 1, f"{lane} 消息 action 错配")
    transition = entry.get("gitlink" if lane == "parent" else "nested_gitlink") if lane in LINKS else None
    if lane in LINKS:
        check_transition(context, lane, old, transition)
        require(evidence.get("gitlink" if lane == "parent" else "nested_gitlink") == transition,
                f"{lane} evidence 依赖与 manifest 不一致")
    actual_paths = changed(context.repos[lane], parent_of(context.repos[lane], old), old)
    structural = evidence.get("structural_paths", [])
    allowed = set(paths + structural + [p["path"] for p in evidence.get("adaptation_paths", [])])
    if lane in LINKS:
        allowed.add(LINKS[lane][0])
        if transition and transition.get("status") == "registered":
            allowed.add(".gitmodules")
    require(set(actual_paths) <= allowed, f"{lane} 实际差异超出证据路径")
    if action == "gitlink-only":
        require(not paths and set(actual_paths) <= {LINKS[lane][0]}, "纯 gitlink 混入源码变化")
    return {"kind": "replay", "lane": lane, "node": node["name"], "node_path": node["path"],
            "source": source, "old": old, "target": new, "subject": item["subject"],
            "classification": item["classification"], "action": action, "content_action": content_action,
            "paths": paths, "actual_paths": actual_paths, "structural_paths": structural, "drop_paths": drops,
            "notes": evidence["adaptation_notes"], "adaptation_paths": evidence["adaptation_paths"],
            "equivalence": proof, "transition": transition, "item": item, "evidence": evidence,
            "related": {role: context.target(role, entry[role].get("commit")) for role in entry
                        if role in context.repos}}
