"""Canonical adaptation message schema for aligned-history v2."""

from __future__ import annotations

import re
from typing import Any


SHA1_PATTERN = re.compile(r"[0-9a-f]{40}\Z")
CLASSIFICATIONS = {"preserve-tail", "paired-dependency-fix", "regenerate"}
DERIVATIONS = {"patch-equivalent", "selective-composite", "regenerate"}


def render_adaptation_message(value: dict[str, Any]) -> bytes:
    """Render one preserve, paired, or regenerated adaptation message."""

    _validate(value)
    lines = [
        str(value["subject_body"]).rstrip("\n"),
        "",
        f"[adaptation-rewrite] classification: {value['classification']}",
        f"[adaptation-rewrite] action: {value['action']}",
        "[adaptation-rewrite] paths:",
    ]
    lines.extend(f"- {item}" for item in value["paths"])
    lines.append("[adaptation-rewrite] notes:")
    lines.extend(f"- {item}" for item in value["notes"])
    lines.extend(["", f"Derivation: {value['derivation']}"])
    if value.get("waylib_commit") is not None:
        lines.append(f"WaylibShared-Commit: {value['waylib_commit']}")
    return ("\n".join(lines) + "\n").encode("utf-8")


def parse_adaptation_message(message: bytes) -> dict[str, Any]:
    """Parse and validate one canonical adaptation message."""

    text = _decode(message)
    lines = text.splitlines()
    indices = [
        index
        for index, line in enumerate(lines)
        if line.startswith("[adaptation-rewrite] classification: ")
    ]
    if len(indices) != 1:
        raise ValueError("expected exactly one adaptation classification")
    index = indices[0]
    if index < 2 or lines[index - 1]:
        raise ValueError("adaptation message spacing is not canonical")
    classification = lines[index].partition(": ")[2]
    result: dict[str, Any] = {
        "schema": "adaptation",
        "subject_body": "\n".join(lines[: index - 1]) + "\n",
        "classification": classification,
    }
    cursor = index + 1
    cursor = _parse_value(
        lines, cursor, result, "action", "[adaptation-rewrite] action: "
    )
    cursor = _parse_list(lines, cursor, result, "paths", "[adaptation-rewrite] paths:")
    cursor = _parse_list(lines, cursor, result, "notes", "[adaptation-rewrite] notes:")
    if cursor >= len(lines) or lines[cursor]:
        raise ValueError("missing separator before adaptation trailers")
    cursor += 1
    cursor = _parse_value(lines, cursor, result, "derivation", "Derivation: ")
    if cursor < len(lines) and lines[cursor].startswith("WaylibShared-Commit: "):
        cursor = _parse_value(
            lines, cursor, result, "waylib_commit", "WaylibShared-Commit: "
        )
    if cursor != len(lines):
        raise ValueError(f"unexpected adaptation message line: {lines[cursor]!r}")
    _validate(result)
    return result


def _validate(value: dict[str, Any]) -> None:
    subject = value.get("subject_body")
    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("adaptation subject_body must be non-empty")
    if "\r" in subject or not subject.endswith("\n") or subject.endswith("\n\n"):
        raise ValueError("adaptation subject_body must end with exactly one LF")
    classification = value.get("classification")
    if classification not in CLASSIFICATIONS or value.get("action") != classification:
        raise ValueError("adaptation classification and action must match")
    derivation = value.get("derivation")
    if derivation not in DERIVATIONS:
        raise ValueError(f"invalid adaptation derivation: {derivation}")
    if classification == "preserve-tail" and derivation != "patch-equivalent":
        raise ValueError("preserve-tail must be patch-equivalent")
    if classification == "paired-dependency-fix" and derivation != "patch-equivalent":
        raise ValueError("paired dependency fix must be patch-equivalent")
    for key in ("paths", "notes"):
        items = value.get(key)
        if not isinstance(items, list) or not items:
            raise ValueError(f"adaptation {key} must be a non-empty list")
        if any(not isinstance(item, str) or not item or "\n" in item or "\r" in item for item in items):
            raise ValueError(f"adaptation {key} items must be non-empty single lines")
    waylib = value.get("waylib_commit")
    if classification == "paired-dependency-fix":
        _require_sha(waylib, "waylib_commit")
    elif waylib is not None:
        raise ValueError("WaylibShared-Commit only applies to paired dependency fix")


def _decode(message: bytes) -> str:
    if b"\r" in message or not message.endswith(b"\n") or message.endswith(b"\n\n"):
        raise ValueError("adaptation message must end with exactly one LF")
    try:
        return message.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("adaptation message is not UTF-8") from error


def _parse_value(
    lines: list[str], cursor: int, result: dict[str, Any], key: str, prefix: str
) -> int:
    if cursor >= len(lines) or not lines[cursor].startswith(prefix):
        raise ValueError(f"missing adaptation {key}")
    result[key] = lines[cursor][len(prefix) :]
    return cursor + 1


def _parse_list(
    lines: list[str], cursor: int, result: dict[str, Any], key: str, header: str
) -> int:
    if cursor >= len(lines) or lines[cursor] != header:
        raise ValueError(f"missing adaptation {key}")
    cursor += 1
    values: list[str] = []
    while cursor < len(lines) and lines[cursor].startswith("- "):
        values.append(lines[cursor][2:])
        cursor += 1
    result[key] = values
    return cursor


def _require_sha(value: Any, label: str) -> None:
    if not isinstance(value, str) or SHA1_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{label} must be a full lowercase SHA-1")
