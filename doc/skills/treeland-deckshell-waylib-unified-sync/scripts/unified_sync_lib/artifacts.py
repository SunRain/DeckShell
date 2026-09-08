"""Content-addressed persistent artifact helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple

from .git_ops import atomic_write_bytes, sha256_bytes, sha256_file


def resolve_artifact_path(root: Path, relative: str) -> Path:
    """Resolve one relative artifact path without permitting root escape."""

    raw = Path(relative)
    if raw.is_absolute() or ".." in raw.parts:
        raise ValueError(f"artifact path escapes root: {relative}")
    resolved_root = root.resolve()
    resolved = (resolved_root / raw).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as error:
        raise ValueError(f"artifact path escapes root: {relative}") from error
    return resolved


def artifact_record(relative: str, content: bytes) -> Dict[str, Any]:
    """Build a content-addressed record for bytes."""

    return {
        "path": relative,
        "size": len(content),
        "sha256": sha256_bytes(content),
    }


def write_artifact(root: Path, relative: str, content: bytes) -> Dict[str, Any]:
    """Atomically write an artifact and return its integrity record."""

    path = resolve_artifact_path(root, relative)
    atomic_write_bytes(path, content)
    return artifact_record(relative, content)


def artifact_errors(record: Any, root: Path, label: str) -> List[str]:
    """Return path, size, and digest violations for an artifact record."""

    if not isinstance(record, dict):
        return [f"{label} must be an artifact object"]
    relative = record.get("path")
    if not isinstance(relative, str) or not relative:
        return [f"{label}.path must be a non-empty relative path"]
    try:
        path = resolve_artifact_path(root, relative)
    except ValueError as error:
        return [f"{label}: {error}"]
    if not path.is_file():
        return [f"{label} is missing: {relative}"]
    errors: List[str] = []
    if record.get("size") != path.stat().st_size:
        errors.append(f"{label} size mismatch: {relative}")
    if record.get("sha256") != sha256_file(path):
        errors.append(f"{label} sha256 mismatch: {relative}")
    return errors


def read_verified_artifact(
    record: Mapping[str, Any], root: Path, label: str
) -> Tuple[Path, bytes]:
    """Read an artifact only after its integrity record passes."""

    errors = artifact_errors(record, root, label)
    if errors:
        raise ValueError("; ".join(errors))
    path = resolve_artifact_path(root, str(record["path"]))
    return path, path.read_bytes()
