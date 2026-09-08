"""Shared schema constants and strict inventory validation."""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, Mapping

from .git_ops import read_json, sha256_bytes


INVENTORY_KIND = "treeland-deckshell-waylib-unified-inventory"
CHILD_ROOTS = ("qwlroots", "waylib", "wlroots")
WLROOTS_ROOT = "3rdparty/wlroots"
WAYLIB_EVIDENCE_KIND = "treeland-unified-waylib-evidence"
CLASSIFICATIONS = {
    "deckshell-only",
    "waylib-only",
    "dual",
    "unowned-skip",
    "blocked",
}
CHILD_CLASSIFICATIONS = {"waylib-only", "dual"}
LANE_ACTIONS = {"applied", "adapted", "empty"}
CHILD_ACTIONS = LANE_ACTIONS | {"gitlink-only"}
PARENT_ACTIONS = LANE_ACTIONS | {"gitlink-only", "not-applicable"}
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
CHANGE_STATUS = re.compile(r"^[A-Z][0-9]{0,3}$")
PATH_CATEGORIES = {"mapped", "root-owned", "excluded", "review-only", "unknown"}


def is_full_sha(value: Any) -> bool:
    """Return whether a value is a lowercase full object identifier."""

    return isinstance(value, str) and bool(FULL_SHA.fullmatch(value))


def _range_errors(range_data: Mapping[str, Any]) -> List[str]:
    errors: List[str] = []
    for field in ("base", "head", "source_tip"):
        if not is_full_sha(range_data.get(field)):
            errors.append(f"inventory range.{field} must be a full SHA")
    ordered = range_data.get("ordered_source_commits")
    if not isinstance(ordered, list):
        return errors + ["inventory ordered_source_commits must be an array"]
    if not all(is_full_sha(value) for value in ordered):
        errors.append("inventory ordered_source_commits must contain full SHAs")
    elif len(ordered) != len(set(ordered)):
        errors.append("inventory ordered_source_commits contains duplicates")
    encoded = "".join(f"{value}\n" for value in ordered).encode("ascii", errors="replace")
    if range_data.get("ordered_sha256") != sha256_bytes(encoded):
        errors.append("inventory range.ordered_sha256 does not match commit order")
    merges = range_data.get("merge_commits")
    if not isinstance(merges, list) or not all(is_full_sha(value) for value in merges):
        errors.append("inventory range.merge_commits must contain full SHAs")
    elif not set(merges).issubset(set(ordered)):
        errors.append("inventory merge_commits must be contained in the source range")
    if ordered and range_data.get("head") != ordered[-1]:
        errors.append("inventory range.head must be the final ordered source commit")
    if not ordered and range_data.get("base") != range_data.get("head"):
        errors.append("empty inventory range requires base and head to be equal")
    return errors


def _policy_errors(policy: Any) -> List[str]:
    if not isinstance(policy, dict):
        return ["inventory path_policy must be an object"]
    errors: List[str] = []
    if not isinstance(policy.get("path"), str) or not policy.get("path"):
        errors.append("inventory path_policy.path must be non-empty")
    if not isinstance(policy.get("sha256"), str) or not SHA256.fullmatch(policy["sha256"]):
        errors.append("inventory path_policy.sha256 must be a SHA-256 digest")
    return errors


def _valid_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\0" in value or value.startswith("/"):
        return False
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        return False
    return ".." not in PurePosixPath(value).parts


def _path_array_errors(value: Any, label: str) -> List[str]:
    if not isinstance(value, list) or not all(_valid_path(path) for path in value):
        return [f"{label} must be a relative path array"]
    if len(value) != len(set(value)):
        return [f"{label} contains duplicates"]
    return []


def _side_errors(side: Any, label: str) -> List[str]:
    if side is None:
        return []
    if not isinstance(side, dict):
        return [f"{label} must be an object or null"]
    errors: List[str] = []
    if not _valid_path(side.get("source")):
        errors.append(f"{label}.source must be a relative path")
    category = side.get("category")
    if category not in PATH_CATEGORIES:
        errors.append(f"{label}.category is invalid")
    target = side.get("target")
    expects_target = category in {"mapped", "root-owned", "review-only"}
    if expects_target and not _valid_path(target):
        errors.append(f"{label}.target must be a relative path")
    if not expects_target and target is not None:
        errors.append(f"{label}.target must be null for {category}")
    if side.get("policy_key") is not None and not isinstance(side.get("policy_key"), str):
        errors.append(f"{label}.policy_key must be a string or null")
    return errors


def _change_errors(changes: Any, label: str) -> List[str]:
    if not isinstance(changes, list):
        return [f"{label}.changes must be an array"]
    errors: List[str] = []
    for index, change in enumerate(changes):
        item_label = f"{label}.changes[{index}]"
        if not isinstance(change, dict):
            errors.append(f"{item_label} must be an object")
            continue
        status = change.get("status")
        if not isinstance(status, str) or not CHANGE_STATUS.fullmatch(status):
            errors.append(f"{item_label}.status is invalid")
        errors.extend(_side_errors(change.get("old"), f"{item_label}.old"))
        errors.extend(_side_errors(change.get("new"), f"{item_label}.new"))
        if change.get("old") is None and change.get("new") is None:
            errors.append(f"{item_label} must contain an old or new side")
        for name in ("child_old", "child_new", "wlroots_old", "wlroots_new"):
            if not isinstance(change.get(name), bool):
                errors.append(f"{item_label}.{name} must be boolean")
    return errors


def _lane_errors(item: Mapping[str, Any], label: str) -> List[str]:
    errors: List[str] = []
    parent = item.get("deckshell")
    child = item.get("waylib_shared")
    wlroots = item.get("wlroots")
    if not isinstance(parent, dict):
        errors.append(f"{label}.deckshell must be an object")
        parent = {}
    if not isinstance(child, dict):
        errors.append(f"{label}.waylib_shared must be an object")
        child = {}
    if not isinstance(wlroots, dict):
        errors.append(f"{label}.wlroots must be an object")
        wlroots = {}
    for lane, field_names in (
        (parent, ("mapped_source_paths", "root_source_paths", "target_paths", "drop_paths")),
        (child, ("source_paths", "drop_paths")),
        (wlroots, ("source_paths", "target_paths", "drop_paths")),
    ):
        for field in field_names:
            errors.extend(_path_array_errors(lane.get(field), f"{label}.{field}"))
    for name, lane in (("deckshell", parent), ("waylib_shared", child), ("wlroots", wlroots)):
        if not isinstance(lane.get("included"), bool):
            errors.append(f"{label}.{name}.included must be boolean")
    child_paths = child.get("source_paths", [])
    if isinstance(child_paths, list) and any(
        not any(path.startswith(root + "/") for root in CHILD_ROOTS)
        for path in child_paths
        if isinstance(path, str)
    ):
        errors.append(f"{label}.waylib_shared.source_paths leaves child roots")
    rpaths = wlroots.get("source_paths", [])
    if isinstance(rpaths, list) and all(isinstance(path, str) for path in rpaths):
        if any(not path.startswith(WLROOTS_ROOT + "/") for path in rpaths):
            errors.append(f"{label}.wlroots.source_paths leaves wlroots root")
        elif wlroots.get("target_paths") != [path[len(WLROOTS_ROOT) + 1:] for path in rpaths]:
            errors.append(f"{label}.wlroots target projection is invalid")
        if wlroots.get("included") is not bool(rpaths):
            errors.append(f"{label}.wlroots inclusion disagrees with source paths")
        if child.get("included") is not bool(child_paths or rpaths):
            errors.append(f"{label}.child inclusion must include wlroots dependency changes")
    classification = item.get("classification")
    if classification != "blocked":
        expected_parent = classification in {"deckshell-only", "dual"}
        expected_child = classification in CHILD_CLASSIFICATIONS
        if parent.get("included") is not expected_parent:
            errors.append(f"{label} parent inclusion disagrees with classification")
        if child.get("included") is not expected_child:
            errors.append(f"{label} child inclusion disagrees with classification")
    return errors


def inventory_errors(payload: Mapping[str, Any]) -> List[str]:
    """Return all structural errors in a unified inventory."""

    errors: List[str] = []
    if payload.get("schema_version") != 2:
        errors.append("inventory schema_version must be 2")
    if payload.get("kind") != INVENTORY_KIND:
        errors.append(f"inventory kind must be {INVENTORY_KIND}")
    if not isinstance(payload.get("source_repo"), str) or not payload.get("source_repo"):
        errors.append("inventory source_repo must be non-empty")
    commits = payload.get("commits")
    range_data = payload.get("range")
    if not isinstance(commits, list):
        errors.append("inventory commits must be an array")
        commits = []
    if not isinstance(range_data, dict):
        errors.append("inventory range must be an object")
        range_data = {}
    errors.extend(_range_errors(range_data))
    errors.extend(_policy_errors(payload.get("path_policy")))
    ordered = range_data.get("ordered_source_commits", [])
    if not isinstance(ordered, list):
        ordered = []
    errors.extend(_inventory_commit_errors(commits))
    actual = [item.get("source_commit") for item in commits if isinstance(item, dict)]
    if ordered != actual:
        errors.append("inventory commit order differs from ordered_source_commits")
    outcome = payload.get("outcome")
    if outcome not in {"pass", "blocked"}:
        errors.append("inventory outcome must be pass or blocked")
    blocked_reasons = payload.get("blocked_reasons")
    if not isinstance(blocked_reasons, list) or not all(
        isinstance(reason, str) for reason in blocked_reasons
    ):
        errors.append("inventory blocked_reasons must be a string array")
    elif outcome == "pass" and blocked_reasons:
        errors.append("passing inventory must not contain blocked_reasons")
    elif outcome == "blocked" and not blocked_reasons:
        errors.append("blocked inventory must contain blocked_reasons")
    if outcome == "pass" and any(
        isinstance(item, dict) and item.get("classification") == "blocked"
        for item in commits
    ):
        errors.append("passing inventory must not contain blocked commits")
    errors.extend(_inventory_scope_errors(payload, commits))
    return errors



def _inventory_scope_errors(payload, commits):
    errors = []
    approvals = payload.get("approved_review")
    if not isinstance(approvals, list) or not all(isinstance(item, str) for item in approvals):
        errors.append("inventory approved_review must be a string array")
    if payload.get("child_owned_roots") != list(CHILD_ROOTS):
        errors.append("inventory child_owned_roots is invalid")
    if payload.get("wlroots_owned_root") != WLROOTS_ROOT:
        errors.append("inventory wlroots_owned_root is invalid")
    counts = payload.get("counts")
    expected_counts = {
        name: sum(
            isinstance(item, dict) and item.get("classification") == name
            for item in commits
        )
        for name in CLASSIFICATIONS
    }
    if counts != expected_counts:
        errors.append("inventory counts do not match commit classifications")
    return errors


def _inventory_commit_errors(commits: List[Any]) -> List[str]:
    errors: List[str] = []
    for index, item in enumerate(commits):
        label = f"inventory commit[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue
        sha = item.get("source_commit")
        classification = item.get("classification")
        if not is_full_sha(sha):
            errors.append(f"{label} source_commit must be a full SHA")
        if not isinstance(item.get("subject"), str):
            errors.append(f"{label} subject must be a string")
        if classification not in CLASSIFICATIONS:
            errors.append(f"{label} has unsupported classification: {classification}")
        errors.extend(_change_errors(item.get("changes"), label))
        errors.extend(_lane_errors(item, label))
        errors.extend(
            _path_array_errors(item.get("protocol_source_paths"), f"{label}.protocol_source_paths")
        )
        errors.extend(
            _path_array_errors(item.get("protocol_target_paths"), f"{label}.protocol_target_paths")
        )
        reasons = item.get("blocked_reasons")
        if not isinstance(reasons, list) or not all(isinstance(reason, str) for reason in reasons):
            errors.append(f"{label}.blocked_reasons must be a string array")
        elif classification == "blocked" and not reasons:
            errors.append(f"{label} blocked classification requires reasons")
        elif classification != "blocked" and reasons:
            errors.append(f"{label} non-blocked classification has blocked reasons")
    return errors


def load_inventory(path: Path) -> Dict[str, Any]:
    """Load an inventory and reject malformed or blocked input."""

    payload = read_json(path)
    errors = inventory_errors(payload)
    if payload.get("outcome") != "pass":
        errors.append("inventory outcome is not pass")
    if errors:
        raise ValueError("; ".join(errors))
    return payload


def child_inventory_entries(payload: Mapping[str, Any]) -> List[Mapping[str, Any]]:
    """Return child-owned entries in frozen source order."""

    return [
        item
        for item in payload.get("commits", [])
        if isinstance(item, dict) and item.get("classification") in CHILD_CLASSIFICATIONS
    ]
