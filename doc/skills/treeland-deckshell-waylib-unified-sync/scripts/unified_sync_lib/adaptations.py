"""Structured, reviewed per-path evidence for adapted replay decisions."""

from __future__ import annotations

from pathlib import Path
from typing import Any, List, Mapping, Sequence

from .artifacts import artifact_errors
from .patches import tree_entry


ADAPTATION_KINDS = {"modified", "omitted", "materialized"}
ADAPTATION_FIELDS = {"path", "kind", "reason", "proof", "review_state"}


def lane_target_paths(item: Mapping[str, Any], lane: str) -> List[str]:
    """Return the inventory-authorized target paths for one replay lane."""

    if lane == "child":
        return list(item.get("waylib_shared", {}).get("source_paths", []))
    if lane == "parent":
        return list(item.get("deckshell", {}).get("target_paths", []))
    if lane == "wlroots":
        return list(item.get("wlroots", {}).get("target_paths", []))
    raise ValueError(f"unsupported adaptation lane: {lane}")


def _single_line(value: Any) -> bool:
    return (
        isinstance(value, str)
        and bool(value.strip())
        and not any(ord(character) < 32 or ord(character) == 127 for character in value)
    )


def adaptation_path_errors(
    paths: Any,
    expected_paths: Sequence[str],
    artifact_root: Path,
    label: str,
) -> List[str]:
    """Validate durable adapted-decision coverage before target mutation."""

    if not isinstance(paths, list) or not paths:
        return [f"{label} adaptation_paths must be a non-empty array"]
    errors: List[str] = []
    actual_paths: List[str] = []
    for index, entry in enumerate(paths):
        entry_label = f"{label} adaptation_paths[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{entry_label} must be an object")
            continue
        errors.extend(
            f"{entry_label} has unsupported field: {name}"
            for name in entry
            if name not in ADAPTATION_FIELDS
        )
        path = entry.get("path")
        if not _single_line(path):
            errors.append(f"{entry_label}.path must be a safe relative path")
        else:
            actual_paths.append(path)
        if not isinstance(entry.get("kind"), str) or entry["kind"] not in ADAPTATION_KINDS:
            errors.append(f"{entry_label}.kind is invalid")
        if not _single_line(entry.get("reason")):
            errors.append(f"{entry_label}.reason must be a non-empty single-line value")
        if entry.get("review_state") != "approved":
            errors.append(f"{entry_label}.review_state must be approved")
        errors.extend(artifact_errors(entry.get("proof"), artifact_root, f"{entry_label}.proof"))
    if actual_paths != list(expected_paths):
        errors.append(f"{label} adaptation_paths must cover inventory target paths in order")
    if len(actual_paths) != len(set(actual_paths)):
        errors.append(f"{label} adaptation_paths contains duplicate paths")
    return errors


def adaptation_semantic_errors(
    repo: Path,
    target_commit: str,
    paths: Any,
    expected_paths: Sequence[str],
    actual_paths: Sequence[str],
    artifact_root: Path,
    label: str,
) -> List[str]:
    """Verify path dispositions against the committed target-tree transition."""

    errors = adaptation_path_errors(paths, expected_paths, artifact_root, label)
    if not isinstance(paths, list):
        return errors
    actual = set(actual_paths)
    for entry in paths:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            continue
        path = entry["path"]
        if path not in expected_paths:
            continue
        kind = entry.get("kind")
        existed_before = tree_entry(repo, f"{target_commit}^", path) is not None
        if kind == "omitted" and path in actual:
            errors.append(f"{label} omitted adaptation path appears in target diff: {path}")
        elif kind == "modified" and (path not in actual or not existed_before):
            errors.append(f"{label} modified adaptation path has invalid target state: {path}")
        elif kind == "materialized" and (path not in actual or existed_before):
            errors.append(f"{label} materialized adaptation path has invalid target state: {path}")
    return errors
