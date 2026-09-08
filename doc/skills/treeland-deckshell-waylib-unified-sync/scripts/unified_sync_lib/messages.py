"""Commit message generation without cross-repository SHA cycles."""

from __future__ import annotations

import json

from typing import Any, List, Mapping, Optional, Sequence


PREFIX = "[treeland-unified-sync]"


def _bullets(values: Sequence[str]) -> str:
    normalized = [value for value in values if value]
    return "\n".join(f"- {value}" for value in (normalized or ["none"]))


def _original(message: str) -> str:
    lines = message.rstrip("\n").splitlines() or ["(empty message)"]
    return "\n".join(f"    {line}" for line in lines)


def _adaptation_paths(paths: Sequence[Mapping[str, Any]]) -> str:
    return _bullets([f"{item['kind']}: {item['path']}" for item in paths])


def child_message(
    subject: str,
    original: str,
    source_sha: str,
    classification: str,
    action: str,
    drop_paths: Sequence[str],
    adaptation_paths: Sequence[Mapping[str, Any]],
    notes: Sequence[str],
    run_id: str,
    refs_doc: str,
    *,
    lane: str = "child",
    content_action: Optional[str] = None,
    nested_gitlink: Optional[Mapping[str, Any]] = None,
) -> str:
    """Build a child message that never references a future parent SHA."""

    return (
        f"{subject}\n\n"
        f"Original treeland commit:\n{_original(original)}\n\n"
        f"{PREFIX} classification: {classification}\n"
        f"{PREFIX} action: {action}\n"
        f"{PREFIX} lane: {lane}\n"
        f"{PREFIX} content action: {content_action or action}\n"
        f"{PREFIX} nested gitlink: {json.dumps(nested_gitlink, sort_keys=True, ensure_ascii=True)}\n"
        f"{PREFIX} drop files:\n{_bullets(drop_paths)}\n"
        f"{PREFIX} adaptation paths:\n{_adaptation_paths(adaptation_paths)}\n"
        f"{PREFIX} adaptation notes:\n{_bullets(notes)}\n"
        f"{PREFIX} parent association: manifest-only\n"
        f"{PREFIX} run-id: {run_id}\n\n"
        f"Refs: {refs_doc}\n"
        f"Treeland-Commit: {source_sha}\n"
    )


def parent_message(
    subject: str,
    original: str,
    source_sha: str,
    classification: str,
    action: str,
    drop_paths: Sequence[str],
    path_mappings: Sequence[str],
    adaptation_paths: Sequence[Mapping[str, Any]],
    notes: Sequence[str],
    child_sha: Optional[str],
    run_id: str,
    refs_doc: str,
) -> str:
    """Build a parent message with an already-existing child SHA."""

    child_lines: List[str]
    if child_sha:
        child_lines = [f"commit: {child_sha}", "action: synced", "gitlink: updated"]
    else:
        child_lines = ["action: not-applicable", "gitlink: unchanged"]
    return (
        f"{subject}\n\n"
        f"Original treeland commit:\n{_original(original)}\n\n"
        f"{PREFIX} classification: {classification}\n"
        f"{PREFIX} action: {action}\n"
        f"{PREFIX} drop files:\n{_bullets(drop_paths)}\n"
        f"{PREFIX} path mapping:\n{_bullets(path_mappings)}\n"
        f"{PREFIX} adaptation paths:\n{_adaptation_paths(adaptation_paths)}\n"
        f"{PREFIX} adaptation notes:\n{_bullets(notes)}\n"
        f"{PREFIX} waylib-shared sync:\n{_bullets(child_lines)}\n"
        f"{PREFIX} run-id: {run_id}\n\n"
        f"Refs: {refs_doc}\n"
        f"Treeland-Commit: {source_sha}\n"
    )
