"""Trace source trailers through the waylib-shared target history."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

from .adaptations import ADAPTATION_KINDS
from .git_ops import changed_paths
from .git_ops import commit_changes, resolve_commit, run_git, stable_unique
from .patches import source_metadata
from .schema import CHILD_ACTIONS, CHILD_ROOTS, LANE_ACTIONS, WLROOTS_ROOT, child_inventory_entries


TRAILER = re.compile(r"(?m)^Treeland-Commit: ([0-9a-f]{40})$")
CLASSIFICATION = re.compile(
    r"(?m)^\[treeland-unified-sync\] classification: (waylib-only|dual)$"
)
ACTION = re.compile(
    r"(?m)^\[treeland-unified-sync\] action: (applied|adapted|empty|gitlink-only)$"
)
DROP_BLOCK = re.compile(
    r"(?m)^\[treeland-unified-sync\] drop files:$\n((?:- [^\n]*\n?)+)"
)
NOTES_BLOCK = re.compile(
    r"(?m)^\[treeland-unified-sync\] adaptation notes:$\n((?:- [^\n]*\n?)+)"
)
ADAPTATION_BLOCK = re.compile(
    r"(?m)^\[treeland-unified-sync\] adaptation paths:$\n((?:- [^\n]*\n?)+)"
)
PARENT_ASSOCIATION = "[treeland-unified-sync] parent association: manifest-only"


def _target_commits(
    repo: Path, base: str, head: str
) -> Tuple[str, str, List[str], List[str]]:
    base_sha = resolve_commit(repo, base)
    head_sha = resolve_commit(repo, head)
    run_git(repo, "merge-base", "--is-ancestor", base_sha, head_sha)
    commits = str(run_git(repo, "rev-list", "--reverse", f"{base_sha}..{head_sha}")).split()
    merges = str(run_git(repo, "rev-list", "--merges", f"{base_sha}..{head_sha}")).split()
    return base_sha, head_sha, commits, merges


def _single_match(pattern: re.Pattern, message: str, label: str) -> Tuple[Optional[str], List[str]]:
    matches = pattern.findall(message)
    if len(matches) != 1:
        return None, [f"{label} must appear exactly once"]
    return str(matches[0]), []


def _within_child(path: str) -> bool:
    return path in {".gitmodules", "CMakeLists.txt", WLROOTS_ROOT} or any(path == root or path.startswith(f"{root}/") for root in CHILD_ROOTS)


def _message_block(
    pattern: re.Pattern, message: str, label: str
) -> Tuple[List[str], List[str]]:
    matches = pattern.findall(message)
    if len(matches) != 1:
        return [], [f"{label} must appear exactly once"]
    values = [line[2:].strip() for line in matches[0].splitlines()]
    if values == ["none"]:
        return [], []
    if not values or any(not value for value in values):
        return [], [f"{label} must contain non-empty bullet values"]
    return values, []


def _original_block(message: str) -> str:
    lines = message.rstrip("\n").splitlines() or ["(empty message)"]
    return "\n".join(f"    {line}" for line in lines)


def _adaptation_paths(message: str) -> Tuple[List[Dict[str, str]], List[str]]:
    values, errors = _message_block(
        ADAPTATION_BLOCK, message, "adaptation paths marker"
    )
    if errors or not values:
        return [], errors
    paths: List[Dict[str, str]] = []
    for value in values:
        kind, separator, path = value.partition(": ")
        if not separator or kind not in ADAPTATION_KINDS or not path:
            errors.append(f"invalid adaptation path marker: {value}")
            continue
        paths.append({"kind": kind, "path": path})
    return paths, errors


def _source_identity_errors(
    source_repo: Path,
    target_repo: Path,
    source_sha: str,
    target_sha: str,
    message: str,
) -> List[str]:
    source = source_metadata(source_repo, source_sha)
    target = source_metadata(target_repo, target_sha)
    errors: List[str] = []
    if (target["author"], target["email"], target["date"]) != (
        source["author"], source["email"], source["date"]
    ):
        errors.append(f"child author identity/date mismatch for {source_sha}")
    expected = f"Original treeland commit:\n{_original_block(source['message'])}\n"
    if expected not in message or target["subject"] != source["subject"]:
        errors.append(f"child original message differs from source for {source_sha}")
    return errors


def _trace_commit(
    repo: Path, sha: str, source_repo: Optional[Path], lane: str = "child"
) -> Dict[str, Any]:
    message = str(run_git(repo, "show", "-s", "--format=%B", sha)).rstrip("\n")
    source, errors = _single_match(TRAILER, message, "Treeland-Commit trailer")
    classification, more = _single_match(CLASSIFICATION, message, "classification marker")
    errors.extend(more)
    action, more = _single_match(ACTION, message, "action marker")
    errors.extend(more)
    content_action, more = _single_match(re.compile(r"(?m)^\[treeland-unified-sync\] content action: (applied|adapted|empty|not-applicable)$"), message, "content action")
    errors.extend(more)
    recorded_lane, more = _single_match(re.compile(r"(?m)^\[treeland-unified-sync\] lane: (child|wlroots)$"), message, "lane")
    errors.extend(more)
    if recorded_lane != lane:
        errors.append("commit lane differs from requested repository role")
    nested_text, more = _single_match(re.compile(r"(?m)^\[treeland-unified-sync\] nested gitlink: (.+)$"), message, "nested gitlink")
    errors.extend(more)
    try:
        nested = json.loads(nested_text) if nested_text else None
    except ValueError:
        nested = None
        errors.append("invalid nested gitlink JSON in commit message")
    if lane == "wlroots" and nested is not None:
        errors.append("wlroots source commit cannot carry a nested child gitlink")
    drop_paths, more = _message_block(DROP_BLOCK, message, "drop files marker")
    errors.extend(more)
    notes, more = _message_block(NOTES_BLOCK, message, "adaptation notes marker")
    errors.extend(more)
    adaptation_paths, more = _adaptation_paths(message)
    errors.extend(more)
    if message.count("Original treeland commit:\n") != 1:
        errors.append("Original treeland commit marker must appear exactly once")
    association_lines = [
        line for line in message.splitlines()
        if line.startswith("[treeland-unified-sync] parent")
    ]
    if association_lines != [PARENT_ASSOCIATION]:
        errors.append("child parent association must be manifest-only exactly once")
    if source_repo is not None and source:
        errors.extend(_source_identity_errors(source_repo, repo, source, sha, message))
    paths: List[str] = []
    for change in commit_changes(repo, sha):
        paths.extend(changed_paths(change))
    invalid = stable_unique([path for path in paths if lane == "child" and not _within_child(path)])
    errors.extend(f"path boundary violation in {sha}: {path}" for path in invalid)
    return {
        "target_commit": sha,
        "source_commit": source,
        "classification": classification,
        "action": action,
        "content_action": content_action,
        "nested_gitlink": nested,
        "drop_paths": drop_paths,
        "adaptation_notes": notes or ["none"],
        "adaptation_paths": adaptation_paths,
        "changed_paths": stable_unique(paths),
        "blocked_reasons": errors,
    }


def _mapping_errors(
    traces: List[Mapping[str, Any]], expected: List[Mapping[str, Any]], lane: str = "child"
) -> List[str]:
    errors: List[str] = []
    actual_sources = [item.get("source_commit") for item in traces]
    expected_sources = [item.get("source_commit") for item in expected]
    duplicates = stable_unique(
        [sha for sha in actual_sources if sha and actual_sources.count(sha) > 1]
    )
    errors.extend(f"duplicate source mapping: {sha}" for sha in duplicates)
    if actual_sources != expected_sources:
        errors.append(
            "source order mismatch: expected "
            f"{expected_sources}, got {actual_sources}"
        )
    expected_by_sha = {item["source_commit"]: item for item in expected}
    for item in traces:
        source = item.get("source_commit")
        inventory = expected_by_sha.get(source)
        if inventory and item.get("classification") != inventory.get("classification"):
            errors.append(f"classification mismatch for source {source}")
        if item.get("action") not in (CHILD_ACTIONS if lane == "child" else LANE_ACTIONS):
            errors.append(f"invalid child action for target {item.get('target_commit')}")
    return errors


def build_waylib_traces(
    repo: Path,
    base: str,
    head: str,
    inventory: Mapping[str, Any],
    source_repo: Optional[Path] = None,
    lane: str = "child",
) -> Dict[str, Any]:
    """Build deterministic child history traces and mapping diagnostics."""

    if lane not in {"child", "wlroots"}:
        raise ValueError("unsupported file lane")
    base_sha, head_sha, targets, merges = _target_commits(repo, base, head)
    entries = [_trace_commit(repo, sha, source_repo, lane) for sha in targets]
    expected = child_inventory_entries(inventory) if lane == "child" else [item for item in inventory["commits"] if item["wlroots"]["included"]]
    blockers = [reason for entry in entries for reason in entry["blocked_reasons"]]
    blockers.extend(f"target range contains merge commit: {sha}" for sha in merges)
    blockers.extend(_mapping_errors(entries, expected, lane))
    if source_repo is None:
        blockers.append("source repo is required for child identity verification")
    blockers = stable_unique(blockers)
    return {
        "schema_version": 2,
        "kind": f"treeland-unified-{'waylib' if lane == 'child' else 'wlroots'}-traces",
        "target_range": {"base": base_sha, "head": head_sha},
        "expected_source_commits": [item["source_commit"] for item in expected],
        "source_identity_verified": source_repo is not None,
        "entries": entries,
        "blocked_reasons": blockers,
        "outcome": "blocked" if blockers else "pass",
    }
