"""读取普通节点及原验收结果；生成记录不执行或取代验收。"""

from __future__ import annotations

from .artifacts import read_verified_artifact
from .git_ops import canonical_json_sha256, read_json, run_git
from .record_context import RecordContext, check_identity, require
from .record_evidence import EVIDENCE, build_row, load_lane_evidence
from .schema import load_inventory
from .record_reports import accepted_report, check_closeout, check_accepted_results, exception_record, original_report

GATES = {
    "deckshell_verify": "deckshell-verify.json", "waylib_verify": "waylib-verify.json",
    "wlroots_verify": "wlroots-verify.json", "gitlink_verify": "gitlink-verify.json",
    "nested_gitlink_verify": "nested-gitlink-verify.json", "protocol_tracking": "protocol-candidates.json",
    "contract_audit": "waylib-contract-audit.json", "child_materialization": "child-materialization.json",
}


PAIRING_GATE = {"protocol_pairing": "protocol-pairing.json"}


def _gates(root, report, manifest):
    expected = dict(GATES)
    if (manifest.get("protocol_update") is not None or manifest["identity"].get("protocol_update") is not None
            or report.get("protocol_pairing") is not None
            or "protocol_pairing" in report.get("gate_sha256", {})):
        expected.update(PAIRING_GATE)
    require(set(report.get("gate_sha256", {})) == set(expected), "原报告缺少 gate 绑定")
    gates = {}
    for key, filename in expected.items():
        gates[key] = read_json(root / filename)
        require(report["gate_sha256"][key] == canonical_json_sha256(gates[key]), f"原 gate 失配：{key}")
    return gates


def validations(root, payload):
    """保留真实状态与历史 attempts，并验证已执行项的原日志。"""
    require(payload.get("kind") == "treeland-unified-command-validations", "验证记录类型错误")
    records = payload.get("entries")
    require(isinstance(records, list), "缺少验证 entries")
    for record in records + payload.get("previous_attempts", []):
        outcome = record.get("outcome")
        require(outcome in ("pass", "fail", "blocked", "no-tests", "not-applicable", "unverified", "not-run"),
                f"验证状态缺失或未知：{record.get('id')}")
        if record.get("log") is not None:
            read_verified_artifact(record["log"], root, f"validation {record['id']}")
        else:
            require(outcome in ("unverified", "not-run"), f"已执行验证缺少原始日志：{record['id']}")
        if outcome in ("pass", "no-tests"):
            require(record.get("exit_code") == 0, "成功状态与退出码冲突")
        if outcome == "no-tests":
            require(record.get("tests", {}).get("total") == 0, "NO_TESTS 与测试数量冲突")
    return records


def replay_metadata(context: RecordContext, descriptor: dict) -> dict:
    """加载原报告的精确候选和状态，拒绝替换旧 SHA 后的假验收。"""
    root = context.node_root(descriptor["path"])
    inventory = load_inventory(root / "inventory.json")
    manifest = read_json(root / "manifest.json")
    report, report_path, closeout = accepted_report(root, descriptor.get("report"))
    validation = read_json(root / "validations.json")
    require(manifest.get("kind") == "treeland-unified-sync-manifest" and manifest.get("schema_version") == 2,
            "manifest 类型错误")
    require(manifest.get("outcome") == "pass", "只记录已完成回放；缺项 manifest 不能冒充完整历史")
    require(report.get("kind") == "treeland-unified-sync-report", "原节点报告类型错误")
    identity = manifest["identity"]
    check_identity(context, identity)
    require(identity.get("inventory_sha256") == canonical_json_sha256(inventory), "manifest/inventory 错配")
    require(report.get("replay_identity") == identity, "报告候选身份被替换")
    for key, value in (("inventory", inventory), ("manifest", manifest), ("validations", validation)):
        require(report.get(key + "_sha256") == canonical_json_sha256(value), f"原报告 {key} 绑定失配")
    require(report.get("build_scope") == {"kind": "range-head-only", "source_head": inventory["range"]["head"]},
            "原节点验收范围错配")
    gates = _gates(root, report, manifest)
    check_closeout(closeout, manifest)
    exception = exception_record(context, descriptor, root, report, inventory, manifest, validation, closeout)
    check_accepted_results(closeout, gates, validation, exception)
    heads = {lane: manifest.get(f"final_{lane}_head") for lane in context.repos}
    require(all(report.get(f"final_{lane}_head") == head for lane, head in heads.items()), "原报告终点失配")
    bases = {"parent": identity["parent_base"], "child": identity["child_base"],
             "wlroots": identity["wlroots"]["base"] if identity.get("wlroots") else None}
    return {"name": descriptor["name"], "kind": "replay", "path": descriptor["path"],
            "source_base": inventory["range"]["base"], "source_head": inventory["range"]["head"],
            "bases": bases, "heads": heads, "inventory": inventory, "manifest": manifest, "report": report,
            "gates": gates, "validations": validations(root, validation),
            "previous_attempts": validation.get("previous_attempts", []), "status": report.get("outcome", "unverified"),
            "report_path": report_path, "closeout": closeout, "exception": exception,
            "original_report": original_report(root, report_path, report)}


def replay_rows(context: RecordContext, node: dict) -> dict:
    """从统一 inventory 的实际 lane 归属展开本仓记录。"""
    inventory, manifest = node["inventory"], node["manifest"]
    ordered = inventory["range"]["ordered_source_commits"]
    require([v["source_commit"] for v in manifest["entries"]] == ordered, "manifest 来源顺序不完整")
    rows, evidences = {lane: [] for lane in context.repos}, {}
    root = context.node_root(node["path"])
    for lane in context.repos:
        expected = [e["source_commit"] for e in manifest["entries"] if e[lane].get("commit")]
        evidences[lane] = load_lane_evidence(root, lane, node["gates"][EVIDENCE[lane][2]], expected,
                                             inactive=lane == "wlroots" and node["bases"][lane] is None)
    for item, entry in zip(inventory["commits"], manifest["entries"]):
        require(item["classification"] == entry["classification"], "manifest 归属不符")
        subject = str(run_git(context.source, "show", "-s", "--format=%s", item["source_commit"])).rstrip("\n")
        require(subject == item["subject"], "inventory 来源主题与 Git 对象不符")
        ownership = {"parent": item["deckshell"]["included"] or item["waylib_shared"]["included"],
                     "child": item["waylib_shared"]["included"], "wlroots": item["wlroots"]["included"]}
        for lane in context.repos:
            require(bool(entry[lane].get("commit")) == ownership[lane], f"{lane} 归属/目标缺失")
            if ownership[lane]:
                rows[lane].append(build_row(context, node, item, entry, lane,
                                           evidences[lane][item["source_commit"]]))
        require(not ownership["wlroots"] or "wlroots" in context.repos, "遗漏 R lane")
    return rows
