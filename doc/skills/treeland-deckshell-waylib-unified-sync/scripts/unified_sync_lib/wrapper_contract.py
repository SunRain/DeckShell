"""新增 wrapper 产物的精确批准，不放宽已有 Waylib 公共合同。"""

from __future__ import annotations

from typing import Any, Mapping


def installed_addition_errors(before: Mapping[str, Any], after: Mapping[str, Any], drift: Mapping[str, Any], approval: Any):
    """只允许保持全部旧值的新增项，逐快照绑定并精确列出所有差异。"""

    expected = {"before_snapshot_sha256": before.get("snapshot_sha256"),
                "after_snapshot_sha256": after.get("snapshot_sha256"), "drift": drift,
                "review_state": "approved"}
    if not isinstance(approval, dict) or any(approval.get(key) != value for key, value in expected.items()):
        return ["wrapper installation approval does not bind exact snapshots and additions"]
    if not isinstance(approval.get("reason"), str) or not approval["reason"].strip():
        return ["wrapper installation approval requires a substantive review reason"]
    errors = []
    for field, change in drift.items():
        if field in {"public_namespaces", "source_public_namespaces"}:
            errors.append("wrapper approval cannot change public namespaces")
        elif "removed" in change:
            if change["removed"]:
                errors.append(f"wrapper approval cannot remove existing {field}")
            if field.startswith("source_"):
                wrapper = after.get("source_contract", {}).get("wrapper_contract") or {}
                if not set(change["added"]).issubset(wrapper.get(field[len("source_"):], [])):
                    errors.append(f"approved additions must originate in wrapper: {field}")
        elif field in {"exported_target_properties", "pkg_config"}:
            left, right = change["before"], change["after"]
            if any(right.get(key) != value for key, value in left.items()):
                errors.append(f"wrapper approval cannot change existing {field}")
        else:
            errors.append(f"unsupported wrapper installation drift: {field}")
    new_paths = set(after.get("installed_paths", [])) - set(before.get("installed_paths", []))
    if approval.get("installed_paths") != sorted(new_paths):
        errors.append("wrapper approval must enumerate every new installed path")
    if any("wlroots" not in path.lower() and "/wlr/" not in path.lower() for path in new_paths):
        errors.append("new installed paths must belong to wlroots")
    return errors
