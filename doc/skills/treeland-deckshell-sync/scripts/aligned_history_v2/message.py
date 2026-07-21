"""Canonical message rendering and parsing for aligned-history v2."""

from __future__ import annotations

import re
from typing import Any

from .adaptation_message import parse_adaptation_message, render_adaptation_message
from .waylib_message import parse_waylib_message, render_waylib_message


SHA1_PATTERN = re.compile(r"[0-9a-f]{40}\Z")
TREELAND_CLASSIFICATIONS = {"other", "mixed", "dependency-only"}
TREELAND_ACTIONS = {
    "applied",
    "adapted",
    "empty",
    "dependency-gitlink",
}
LIST_FIELDS = (
    ("drop_files", "[treeland-sync] drop files:"),
    ("path_mapping", "[treeland-sync] path mapping:"),
    ("adaptation_paths", "[treeland-sync] adaptation paths:"),
    ("adaptation_notes", "[treeland-sync] adaptation notes:"),
)


def render_message(message_input: dict[str, Any]) -> bytes:
    """Render one canonical v2 message from validated structured input."""

    if message_input.get("schema") == "adaptation":
        return render_adaptation_message(message_input)
    if message_input.get("schema") == "waylib":
        return render_waylib_message(message_input)
    if message_input.get("schema") != "treeland":
        raise ValueError("unsupported message schema")
    _validate_treeland_input(message_input)
    source = str(message_input["source_commit"])
    subject_body = _subject_body(message_input["subject_body"])
    lines = [subject_body.rstrip("\n"), "", f"(cherry picked from commit {source})", ""]
    lines.extend(
        [
            f"[treeland-sync] classification: {message_input['classification']}",
            f"[treeland-sync] action: {message_input['action']}",
        ]
    )
    for key, header in LIST_FIELDS:
        lines.append(header)
        lines.extend(f"- {value}" for value in message_input[key])
    lines.extend(
        [
            "",
            "Treeland-Remote: treeland",
            "Treeland-Remote-Branch: master",
            "Treeland-Tracking-Ref: refs/remotes/treeland/master",
            f"Treeland-Commit: {source}",
        ]
    )
    for key, trailer in (
        ("legacy_treeland_commit", "Legacy-Treeland-Commit"),
        ("treeland_patch_id", "Treeland-Patch-ID"),
        ("waylib_commit", "WaylibShared-Commit"),
    ):
        value = message_input.get(key)
        if value is not None:
            lines.append(f"{trailer}: {value}")
    return ("\n".join(lines) + "\n").encode("utf-8")


def parse_message(message: bytes, schema: str) -> dict[str, Any]:
    """Parse a canonical message and reject duplicates or order drift."""

    if schema == "adaptation":
        return parse_adaptation_message(message)
    if schema == "waylib":
        return parse_waylib_message(message)
    if schema != "treeland":
        raise ValueError("unsupported message schema")
    text = _decode_message(message)
    lines = text.splitlines()
    cherry_indices = [
        index
        for index, line in enumerate(lines)
        if line.startswith("(cherry picked from commit ")
    ]
    if len(cherry_indices) != 1:
        raise ValueError("expected exactly one cherry-pick line")
    cherry_index = cherry_indices[0]
    if cherry_index < 2 or lines[cherry_index - 1] or lines[cherry_index + 1]:
        raise ValueError("cherry-pick line spacing is not canonical")
    match = re.fullmatch(r"\(cherry picked from commit ([0-9a-f]{40})\)", lines[cherry_index])
    if match is None:
        raise ValueError("invalid cherry-pick source")
    result: dict[str, Any] = {
        "schema": "treeland",
        "subject_body": "\n".join(lines[: cherry_index - 1]) + "\n",
        "source_commit": match.group(1),
    }
    cursor = cherry_index + 2
    cursor = _parse_value_line(lines, cursor, result, "classification", "[treeland-sync] classification: ")
    cursor = _parse_value_line(lines, cursor, result, "action", "[treeland-sync] action: ")
    for key, header in LIST_FIELDS:
        cursor = _parse_list(lines, cursor, result, key, header)
    if cursor >= len(lines) or lines[cursor]:
        raise ValueError("missing separator before source trailers")
    cursor += 1
    fixed_trailers = (
        ("Treeland-Remote: ", "treeland"),
        ("Treeland-Remote-Branch: ", "master"),
        ("Treeland-Tracking-Ref: ", "refs/remotes/treeland/master"),
        ("Treeland-Commit: ", result["source_commit"]),
    )
    for prefix, expected in fixed_trailers:
        cursor = _expect_line(lines, cursor, prefix + expected)
    optional = (
        ("Legacy-Treeland-Commit: ", "legacy_treeland_commit"),
        ("Treeland-Patch-ID: ", "treeland_patch_id"),
        ("WaylibShared-Commit: ", "waylib_commit"),
    )
    for prefix, key in optional:
        if cursor < len(lines) and lines[cursor].startswith(prefix):
            result[key] = lines[cursor][len(prefix) :]
            cursor += 1
    if cursor != len(lines):
        raise ValueError(f"unexpected message line: {lines[cursor]!r}")
    _validate_treeland_input(result)
    return result


def _validate_treeland_input(value: dict[str, Any]) -> None:
    _require_sha(value.get("source_commit"), "source_commit")
    classification = value.get("classification")
    action = value.get("action")
    if classification not in TREELAND_CLASSIFICATIONS:
        raise ValueError(f"invalid Treeland classification: {classification}")
    if action not in TREELAND_ACTIONS:
        raise ValueError(f"invalid Treeland action: {action}")
    if (classification == "dependency-only") != (action == "dependency-gitlink"):
        raise ValueError("dependency-only must use dependency-gitlink")
    for key, _ in LIST_FIELDS:
        _validate_list(value.get(key), key)
    paths = value["adaptation_paths"]
    notes = value["adaptation_notes"]
    if action == "adapted" and (paths == ["none"] or notes == ["none"]):
        raise ValueError("adapted message requires paths and notes")
    if action in {"applied", "dependency-gitlink"} and paths != ["none"]:
        raise ValueError(f"{action} message must use no adaptation paths")
    legacy = value.get("legacy_treeland_commit")
    patch_id = value.get("treeland_patch_id")
    if (legacy is None) != (patch_id is None):
        raise ValueError("legacy Treeland commit and patch ID must be paired")
    for key in ("legacy_treeland_commit", "treeland_patch_id", "waylib_commit"):
        if value.get(key) is not None:
            _require_sha(value[key], key)
    if classification in {"mixed", "dependency-only"} and value.get("waylib_commit") is None:
        raise ValueError(f"{classification} message requires WaylibShared-Commit")


def _subject_body(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("subject_body must be non-empty text")
    if "\r" in value or not value.endswith("\n") or value.endswith("\n\n"):
        raise ValueError("subject_body must end with exactly one LF")
    return value


def _validate_list(value: Any, label: str) -> None:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{label} must be a non-empty string list")
    if "none" in value and value != ["none"]:
        raise ValueError(f"none must be the only {label} item")
    if any("\n" in item or "\r" in item for item in value):
        raise ValueError(f"{label} items must be single-line")


def _require_sha(value: Any, label: str) -> None:
    if not isinstance(value, str) or SHA1_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{label} must be a full lowercase SHA-1")


def _decode_message(message: bytes) -> str:
    if b"\r" in message or not message.endswith(b"\n") or message.endswith(b"\n\n"):
        raise ValueError("message must end with exactly one LF and contain no CR")
    try:
        return message.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("message is not UTF-8") from error


def _parse_value_line(
    lines: list[str], cursor: int, result: dict[str, Any], key: str, prefix: str
) -> int:
    if cursor >= len(lines) or not lines[cursor].startswith(prefix):
        raise ValueError(f"missing {key}")
    result[key] = lines[cursor][len(prefix) :]
    return cursor + 1


def _parse_list(
    lines: list[str], cursor: int, result: dict[str, Any], key: str, header: str
) -> int:
    cursor = _expect_line(lines, cursor, header)
    values: list[str] = []
    while cursor < len(lines) and lines[cursor].startswith("- "):
        values.append(lines[cursor][2:])
        cursor += 1
    result[key] = values
    return cursor


def _expect_line(lines: list[str], cursor: int, expected: str) -> int:
    if cursor >= len(lines) or lines[cursor] != expected:
        actual = None if cursor >= len(lines) else lines[cursor]
        raise ValueError(f"expected {expected!r}, got {actual!r}")
    return cursor + 1
