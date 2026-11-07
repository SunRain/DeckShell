"""Portable public plan references; runtime filesystem paths remain separate."""

from pathlib import PurePosixPath, PureWindowsPath


def relative_reference(value: str) -> str:
    """Require a canonical workspace-relative reference without resolving it."""
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError("refs-doc must be a non-empty relative reference")
    path = PurePosixPath(value)
    if (path.is_absolute() or PureWindowsPath(value).drive or "\\" in value
            or ":" in value or value.startswith("~") or ".." in path.parts
            or str(path) != value or value == "."
            or any(ord(c) < 32 or ord(c) == 127 for c in value)):
        raise ValueError("refs-doc must be a canonical workspace-relative reference")
    return value
