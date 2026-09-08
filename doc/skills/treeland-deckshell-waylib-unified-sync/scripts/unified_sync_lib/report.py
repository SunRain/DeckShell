"""Truthful unified synchronization report assembly."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

from .git_ops import canonical_json_sha256, stable_unique
from .schema import inventory_errors
from .materialization import recursive_materialization_errors
from .validation_gates import contract_binding_errors, validation_errors


GATE_KINDS = {
    "deckshell_verify": "treeland-unified-parent-verify",
    "waylib_verify": "treeland-unified-waylib-verify",
    "gitlink_verify": "treeland-unified-gitlink-verify",
    "protocol_tracking": "treeland-unified-protocol-candidates",
    "contract_audit": "waylib-install-contract-audit",
    "child_materialization": "treeland-unified-child-materialization",
    "wlroots_verify": "treeland-unified-wlroots-verify",
    "nested_gitlink_verify": "treeland-unified-nested-gitlink-verify",
}


def _escape(value: Any) -> str:
    return str(value if value is not None else "-").replace("|", "\\|").replace("\n", " ")


def _gate_identity_errors(
    gates: Mapping[str, Any], manifest: Mapping[str, Any]
) -> List[str]:
    identity = manifest.get("identity")
    identity = identity if isinstance(identity, dict) else {}
    expected_ranges = {
        "deckshell_verify": {
            "base": identity.get("parent_base"),
            "head": manifest.get("final_parent_head"),
        },
        "waylib_verify": {
            "base": identity.get("child_base"),
            "head": manifest.get("final_child_head"),
        },
    }
    r = identity.get("wlroots")
    expected_ranges["wlroots_verify"] = {"base": r.get("base"), "head": manifest.get("final_wlroots_head")} if isinstance(r, dict) else None
    errors = [
        f"{name} target range differs from the manifest"
        for name, expected in expected_ranges.items()
        if not isinstance(gates.get(name), dict)
        or gates[name].get("target_range") != expected
    ]
    gitlink = gates.get("gitlink_verify")
    expected_gitlink = {
        "parent_base": identity.get("parent_base"),
        "child_base": identity.get("child_base"),
        "final_parent_head": manifest.get("final_parent_head"),
        "final_child_head": manifest.get("final_child_head"),
    }
    if not isinstance(gitlink, dict) or any(
        gitlink.get(name) != value for name, value in expected_gitlink.items()
    ):
        errors.append("gitlink_verify heads differ from the manifest")
    nested = gates.get("nested_gitlink_verify", {})
    if not isinstance(nested, dict) or nested.get("final_child_head") != manifest.get("final_child_head") or nested.get("final_wlroots_head") != manifest.get("final_wlroots_head"):
        errors.append("nested gitlink heads differ from the manifest")
    for name in ("wlroots_verify", "nested_gitlink_verify"):
        gate = gates.get(name, {})
        if not isinstance(gate, dict) or gate.get("status") != ("verified" if r is not None else "not-applicable"):
            errors.append(f"{name} applicability differs from the manifest")
    return errors


def _gate_errors(
    gates: Mapping[str, Any],
    inventory: Mapping[str, Any],
    manifest: Mapping[str, Any],
) -> List[str]:
    errors: List[str] = []
    inventory_digest = canonical_json_sha256(inventory)
    manifest_digest = canonical_json_sha256(manifest)
    for name, kind in GATE_KINDS.items():
        gate = gates.get(name)
        if not isinstance(gate, dict):
            errors.append(f"required gate is missing: {name}")
            continue
        if gate.get("schema_version") != 2 or gate.get("kind") != kind:
            errors.append(f"gate schema/kind mismatch: {name}")
        if gate.get("outcome") != "pass":
            errors.append(f"gate did not pass: {name}={gate.get('outcome')}")
        if gate.get("blocked_reasons") != []:
            errors.append(f"passing gate contains blocked reasons: {name}")
        if gate.get("errors"):
            errors.append(f"passing gate contains execution errors: {name}")
    protocol = gates.get("protocol_tracking")
    if isinstance(protocol, dict) and protocol.get("advisory") is not True:
        errors.append("protocol tracking must explicitly declare advisory=true")
    if isinstance(protocol, dict) and (protocol.get("parent_context_used") is not True
                                      or protocol.get("manifest_sha256") != manifest_digest):
        errors.append("protocol tracking must bind manifest and actual parent context")
    for name in ("deckshell_verify", "waylib_verify", "protocol_tracking", "wlroots_verify", "nested_gitlink_verify"):
        gate = gates.get(name)
        if isinstance(gate, dict) and gate.get("inventory_sha256") != inventory_digest:
            errors.append(f"gate does not bind inventory: {name}")
    for name in ("deckshell_verify", "gitlink_verify", "wlroots_verify", "nested_gitlink_verify"):
        gate = gates.get(name)
        if isinstance(gate, dict) and gate.get("manifest_sha256") != manifest_digest:
            errors.append(f"gate does not bind manifest: {name}")
    errors.extend(_gate_identity_errors(gates, manifest))
    return errors


def _mapping_errors(
    inventory: Mapping[str, Any], manifest: Mapping[str, Any]
) -> List[str]:
    errors = inventory_errors(inventory)
    if inventory.get("outcome") != "pass":
        errors.append("inventory outcome must be pass")
    if manifest.get("schema_version") != 2 or manifest.get("kind") != "treeland-unified-sync-manifest":
        errors.append("manifest schema or kind is invalid")
    if manifest.get("outcome") != "pass":
        errors.append("manifest outcome must be pass")
    inventory_entries = inventory.get("commits")
    manifest_entries = manifest.get("entries")
    if not isinstance(inventory_entries, list):
        inventory_entries = []
    if not isinstance(manifest_entries, list):
        errors.append("manifest entries must be an array")
        manifest_entries = []
    expected = [
        item.get("source_commit") if isinstance(item, dict) else None
        for item in inventory_entries
    ]
    actual = [
        item.get("source_commit") if isinstance(item, dict) else None
        for item in manifest_entries
    ]
    if expected != actual:
        errors.append("manifest source order differs from inventory")
    identity = manifest.get("identity", {})
    if "wlroots" not in identity:
        errors.append("manifest is missing the explicit wlroots identity slot")
    for source, node in zip(inventory_entries, manifest_entries):
        if isinstance(source, dict) and isinstance(node, dict):
            r = node.get("wlroots")
            if not isinstance(r, dict) or bool(r.get("commit")) != bool(source.get("wlroots", {}).get("included")):
                errors.append("wlroots manifest inclusion differs from source inventory")
            if node.get("classification") != source.get("classification"):
                errors.append("manifest classification differs from source inventory")
    return errors


def _mapping_row(item, protocol):
    parent, child, r = [item.get(lane) or {} for lane in ("parent", "child", "wlroots")]
    link, nested = item.get("gitlink") or {}, item.get("nested_gitlink") or {}
    notes = stable_unique(note for lane in (r, child, parent)
                          for note in lane.get("adaptation_notes", []) if note != "none")
    candidates = ", ".join(row.get("commit", "") for row in protocol.get("candidates", [])) or "-"
    values = (
        item.get("source_commit"), item.get("classification"), r.get("commit"), r.get("action"),
        child.get("commit"), child.get("action"), child.get("content_action", child.get("action")),
        f"{nested.get('from') or '-'} → {nested.get('to') or '-'}",
        parent.get("commit"), parent.get("action"), f"{link.get('from') or '-'} → {link.get('to') or '-'}",
        protocol.get("match_status", "not-triggered"), candidates, "; ".join(notes) or "none",
    )
    return "| " + " | ".join(_escape(value) for value in values) + " |"


def _mapping_table(manifest: Mapping[str, Any], protocol: Any) -> List[str]:
    lines = [
        "| Treeland | 分类 | wlroots | R action | waylib-shared | C action | C 普通内容 | C→R gitlink | DeckShell | P action | P→C gitlink | 协议状态 | 协议候选 | 说明 |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    entries = protocol.get("entries", []) if isinstance(protocol, dict) else []
    protocols = {row.get("source_commit"): row for row in entries if isinstance(row, dict)}
    for item in manifest.get("entries", []):
        if isinstance(item, dict):
            lines.append(_mapping_row(item, protocols.get(item.get("source_commit"), {})))
    return lines


def _gate_table(gates: Mapping[str, Any]) -> List[str]:
    lines = ["| 门禁 | 结果 |", "|---|---|"]
    for name in GATE_KINDS:
        gate = gates.get(name)
        outcome = str(gate.get("outcome", "unknown")).upper() if isinstance(gate, dict) else "MISSING"
        lines.append(f"| `{name}` | {outcome} |")
    return lines


def _validation_status(entry: Mapping[str, Any]) -> str:
    if entry.get("outcome") == "not-applicable":
        return "NOT_APPLICABLE（来源子树不存在且 R0 为空树；未执行）"
    if entry.get("outcome") == "no-tests":
        total = entry.get("tests", {}).get("total", "?")
        return f"NO_TESTS（total={total}）"
    if entry.get("category") == "test" and entry.get("outcome") == "pass":
        tests = entry.get("tests", {})
        return f"PASS（{tests.get('passed')}/{tests.get('total')}）"
    return str(entry.get("outcome", "unknown")).upper()


def _validation_table(validations: Mapping[str, Any]) -> List[str]:
    lines = ["| 验证 | 类别 | 结果 | exit |", "|---|---|---|---|"]
    for entry in validations.get("entries", []):
        if not isinstance(entry, dict):
            continue
        lines.append(
            f"| `{_escape(entry.get('id'))}` | {_escape(entry.get('category'))} | "
            f"{_validation_status(entry)} | {_escape(entry.get('exit_code'))} |"
        )
    return lines


def _protocol_table(protocol: Any) -> List[str]:
    lines = ["| Treeland | advisory 状态 | 候选 |", "|---|---|---|"]
    entries = protocol.get("entries", []) if isinstance(protocol, dict) else []
    entries = entries if isinstance(entries, list) else []
    if not entries:
        lines.append("| - | no-protocol-touch | - |")
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        raw_candidates = entry.get("candidates", [])
        candidates_data = raw_candidates if isinstance(raw_candidates, list) else []
        candidates = ", ".join(
            f"{item.get('commit', '')[:12]} ({item.get('similarity')})"
            for item in candidates_data
            if isinstance(item, dict)
        ) or "-"
        lines.append(
            f"| {str(entry.get('source_commit', ''))[:12]} | "
            f"{_escape(entry.get('match_status'))} | {_escape(candidates)} |"
        )
    return lines


def _markdown(
    inventory: Mapping[str, Any],
    manifest: Mapping[str, Any],
    gates: Mapping[str, Any],
    validations: Mapping[str, Any],
    blockers: Sequence[str],
) -> str:
    outcome = "PASS" if not blockers else "BLOCKED"
    range_data = inventory.get("range", {})
    range_data = range_data if isinstance(range_data, dict) else {}
    lines = [
        "# Treeland → DeckShell + waylib-shared + wlroots 统一同步报告",
        "",
        "## 结论",
        "",
        f"- 总体结果：**{outcome}**",
        f"- 来源区间：`({range_data.get('base')}..{range_data.get('head')}]`",
        f"- DeckShell candidate：`{manifest.get('final_parent_head', 'unknown')}`",
        f"- waylib-shared candidate：`{manifest.get('final_child_head', 'unknown')}`",
        f"- wlroots candidate：`{manifest.get('final_wlroots_head') or 'not-applicable'}`",
        "- 构建验收仅覆盖本段终点对应的候选及必需基线；普通中间提交不要求构建，本报告不证明区间内其他 tag 已通过。",
        "- 远程 push：同步工具未执行；本报告不把外部状态冒充为证据。",
        "",
        "## 统一映射",
        "",
        *_mapping_table(manifest, gates.get("protocol_tracking")),
        "",
        "## 结构化门禁",
        "",
        *_gate_table(gates),
        "",
        "## 构建与测试证据",
        "",
        *_validation_table(validations),
        "",
        "## 协议候选（仅 advisory）",
        "",
        *_protocol_table(gates.get("protocol_tracking")),
        "",
        "## 阻断项",
        "",
    ]
    lines.extend(f"- {item}" for item in blockers)
    if not blockers:
        lines.append("- 无。")
    return "\n".join(lines) + "\n"


def build_sync_report(
    inventory: Mapping[str, Any],
    manifest: Mapping[str, Any],
    gates: Mapping[str, Any],
    validations: Mapping[str, Any],
    artifact_root: Path,
) -> Dict[str, Any]:
    """Build a report whose PASS state is derived only from supplied evidence."""

    blockers = _mapping_errors(inventory, manifest)
    blockers.extend(_gate_errors(gates, inventory, manifest))
    blockers.extend(validation_errors(validations, artifact_root, manifest, gates))
    blockers.extend(contract_binding_errors(gates, validations, manifest, artifact_root))
    audit = gates.get("contract_audit") or {}
    blockers.extend(recursive_materialization_errors(
        gates.get("child_materialization"), manifest, audit.get("source_roots", {}).get("before"),
    ))
    blockers = stable_unique(blockers)
    source_range = inventory.get("range")
    source_range = source_range if isinstance(source_range, dict) else {}
    return {
        "schema_version": 2,
        "kind": "treeland-unified-sync-report",
        "outcome": "blocked" if blockers else "pass",
        "build_scope": {"kind": "range-head-only", "source_head": source_range.get("head")},
        "final_parent_head": manifest.get("final_parent_head"),
        "final_child_head": manifest.get("final_child_head"),
        "final_wlroots_head": manifest.get("final_wlroots_head"),
        "replay_identity": manifest.get("identity"),
        "inventory_sha256": canonical_json_sha256(inventory),
        "manifest_sha256": canonical_json_sha256(manifest),
        "gate_sha256": {
            name: canonical_json_sha256(gate)
            for name, gate in gates.items()
            if isinstance(gate, dict)
        },
        "validations_sha256": canonical_json_sha256(validations),
        "blocked_reasons": blockers,
        "markdown": _markdown(inventory, manifest, gates, validations, blockers),
    }
