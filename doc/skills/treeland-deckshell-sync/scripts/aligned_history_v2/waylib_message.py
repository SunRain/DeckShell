"""Canonical WaylibShared message schema for aligned-history v2."""

from __future__ import annotations

import re
from typing import Any


SHA1_PATTERN = re.compile(r"[0-9a-f]{40}\Z")
CLASSIFICATIONS = {
    "dependency-structure",
    "dependency-metadata",
    "dependency-checkpoint",
    "dependency-gate",
    "dependency-convergence",
}


def render_waylib_message(value: dict[str, Any]) -> bytes:
    """Render a local or convergence WaylibShared gitlink message."""

    _validate(value)
    subject_body = str(value["subject_body"]).rstrip("\n")
    lines = [
        subject_body,
        "",
        f"[waylib-sync] classification: {value['classification']}",
        "[waylib-sync] action: local-gitlink",
        "",
        f"WaylibShared-Commit: {value['waylib_commit']}",
    ]
    absorbed = value.get("absorbed_waylib_commit")
    if absorbed is not None:
        lines.append(f"Absorbed-WaylibShared-Commit: {absorbed}")
    return ("\n".join(lines) + "\n").encode("utf-8")


def parse_waylib_message(message: bytes) -> dict[str, Any]:
    """Parse and validate one canonical WaylibShared message."""

    text = _decode(message)
    lines = text.splitlines()
    classification_indices = [
        index
        for index, line in enumerate(lines)
        if line.startswith("[waylib-sync] classification: ")
    ]
    if len(classification_indices) != 1:
        raise ValueError("expected exactly one waylib classification")
    index = classification_indices[0]
    if index < 2 or lines[index - 1]:
        raise ValueError("waylib message spacing is not canonical")
    result: dict[str, Any] = {
        "schema": "waylib",
        "subject_body": "\n".join(lines[: index - 1]) + "\n",
        "classification": lines[index].partition(": ")[2],
        "action": "local-gitlink",
    }
    expected_action = "[waylib-sync] action: local-gitlink"
    if index + 2 >= len(lines) or lines[index + 1] != expected_action or lines[index + 2]:
        raise ValueError("waylib action block is not canonical")
    cursor = index + 3
    cursor = _parse_sha_trailer(
        lines, cursor, result, "WaylibShared-Commit: ", "waylib_commit"
    )
    if cursor < len(lines) and lines[cursor].startswith("Absorbed-WaylibShared-Commit: "):
        cursor = _parse_sha_trailer(
            lines,
            cursor,
            result,
            "Absorbed-WaylibShared-Commit: ",
            "absorbed_waylib_commit",
        )
    if cursor != len(lines):
        raise ValueError(f"unexpected waylib message line: {lines[cursor]!r}")
    _validate(result)
    return result


def _validate(value: dict[str, Any]) -> None:
    subject = value.get("subject_body")
    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("WaylibShared subject_body must be non-empty")
    if "\r" in subject or not subject.endswith("\n") or subject.endswith("\n\n"):
        raise ValueError("WaylibShared subject_body must end with exactly one LF")
    classification = value.get("classification")
    if classification not in CLASSIFICATIONS:
        raise ValueError(f"invalid WaylibShared classification: {classification}")
    if value.get("action") != "local-gitlink":
        raise ValueError("WaylibShared action must be local-gitlink")
    _require_sha(value.get("waylib_commit"), "waylib_commit")
    absorbed = value.get("absorbed_waylib_commit")
    if absorbed is not None:
        _require_sha(absorbed, "absorbed_waylib_commit")
        if classification != "dependency-structure":
            raise ValueError("absorbed WaylibShared parent requires dependency-structure")


def _decode(message: bytes) -> str:
    if b"\r" in message or not message.endswith(b"\n") or message.endswith(b"\n\n"):
        raise ValueError("WaylibShared message must end with exactly one LF")
    try:
        return message.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("WaylibShared message is not UTF-8") from error


def _parse_sha_trailer(
    lines: list[str], cursor: int, result: dict[str, Any], prefix: str, key: str
) -> int:
    if cursor >= len(lines) or not lines[cursor].startswith(prefix):
        raise ValueError(f"missing {prefix.rstrip()}")
    result[key] = lines[cursor][len(prefix) :]
    return cursor + 1


def _require_sha(value: Any, label: str) -> None:
    if not isinstance(value, str) or SHA1_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{label} must be a full lowercase SHA-1")
