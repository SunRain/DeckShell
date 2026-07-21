"""Parse canonical `git diff-tree --raw -z --no-renames` transitions."""

from __future__ import annotations

import re
from dataclasses import dataclass


OBJECT_PATTERN = re.compile(rb"[0-9a-f]{40}\Z")
MODE_PATTERN = re.compile(rb"[0-7]{6}\Z")
ALLOWED_STATUSES = {"A", "D", "M", "T"}


@dataclass(frozen=True)
class TreeChange:
    """One exact index update from an old mode/object to a new one."""

    old_mode: str
    new_mode: str
    old_object: str
    new_object: str
    status: str
    path: str


def parse_raw_transition(payload: bytes) -> tuple[TreeChange, ...]:
    """Parse a no-rename raw transition without losing path boundaries."""

    if not payload:
        return ()
    if not payload.endswith(b"\0"):
        raise ValueError("raw tree transition must end with NUL")
    fields = payload[:-1].split(b"\0")
    if len(fields) % 2:
        raise ValueError("raw tree transition has an incomplete record")
    changes: list[TreeChange] = []
    seen_paths: set[str] = set()
    for index in range(0, len(fields), 2):
        metadata, path_bytes = fields[index], fields[index + 1]
        parts = metadata.split(b" ")
        if len(parts) != 5 or not parts[0].startswith(b":"):
            raise ValueError(f"invalid raw transition metadata: {metadata!r}")
        old_mode = parts[0][1:]
        new_mode, old_object, new_object, status_bytes = parts[1:]
        if MODE_PATTERN.fullmatch(old_mode) is None or MODE_PATTERN.fullmatch(new_mode) is None:
            raise ValueError("raw transition contains an invalid mode")
        if OBJECT_PATTERN.fullmatch(old_object) is None or OBJECT_PATTERN.fullmatch(new_object) is None:
            raise ValueError("raw transition contains an invalid object ID")
        status = status_bytes.decode("ascii")
        if status not in ALLOWED_STATUSES:
            raise ValueError(f"raw transition contains unsupported status: {status}")
        try:
            path = path_bytes.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("raw transition path is not UTF-8") from error
        if not path or path.startswith("/") or "\0" in path:
            raise ValueError(f"invalid raw transition path: {path!r}")
        if path in seen_paths:
            raise ValueError(f"duplicate raw transition path: {path}")
        seen_paths.add(path)
        changes.append(
            TreeChange(
                old_mode=old_mode.decode("ascii"),
                new_mode=new_mode.decode("ascii"),
                old_object=old_object.decode("ascii"),
                new_object=new_object.decode("ascii"),
                status=status,
                path=path,
            )
        )
    return tuple(changes)
