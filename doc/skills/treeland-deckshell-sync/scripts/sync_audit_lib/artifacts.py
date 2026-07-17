"""Evidence artifact reference validation."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path, PurePosixPath
from typing import Any


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_artifact_reference(root: Path, path: Path) -> dict[str, Any]:
    """Build one immutable relative artifact record for a regular file."""

    resolved_root = root.resolve()
    resolved_path = path.resolve(strict=False)
    if resolved_path != resolved_root and resolved_root not in resolved_path.parents:
        raise ValueError(f"artifact is outside evidence root: {path}")
    findings = _regular_file_findings(path, "artifact", str(path))
    if findings:
        raise ValueError(findings[0])
    return {
        "path": path.relative_to(root).as_posix(),
        "size": path.stat().st_size,
        "sha256": _sha256_file(path),
    }


def _relative_artifact_path(
    root: Path, value: Any, field: str, source: str
) -> tuple[Path | None, list[str]]:
    if not isinstance(value, dict):
        return None, [f"strict artifact reference must be an object: {field}: {source}"]
    relative = value.get("path")
    if not isinstance(relative, str) or not relative:
        return None, [f"missing artifact path: {field}: {source}"]
    candidate = PurePosixPath(relative)
    if candidate.is_absolute() or ".." in candidate.parts or "." in candidate.parts:
        return None, [f"path escapes evidence root: {field}: {relative}"]
    path = root.joinpath(*candidate.parts)
    resolved_root = root.resolve()
    try:
        resolved_path = path.resolve(strict=False)
    except OSError:
        return None, [f"invalid artifact path: {field}: {relative}"]
    if resolved_path != resolved_root and resolved_root not in resolved_path.parents:
        return None, [f"path escapes evidence root: {field}: {relative}"]
    return path, []


def _regular_file_findings(path: Path, field: str, source: str) -> list[str]:
    try:
        info = os.lstat(path)
    except OSError:
        return [f"artifact missing: {field}: {source}: {path}"]
    if not stat.S_ISREG(info.st_mode) or path.is_symlink():
        return [f"artifact must be a regular file: {field}: {source}: {path}"]
    return []


def verify_strict_artifact(
    root: Path | None, value: Any, field: str, source: str
) -> list[str]:
    """Verify one strict relative artifact record and its immutable metadata."""

    if root is None:
        return [f"strict evidence root is required: {field}: {source}"]
    path, findings = _relative_artifact_path(root, value, field, source)
    if path is None:
        return findings
    findings.extend(_regular_file_findings(path, field, source))
    if findings:
        return findings

    expected_size = value.get("size")
    if type(expected_size) is not int or expected_size < 0:
        findings.append(f"invalid artifact size: {field}: {source}")
    elif path.stat().st_size != expected_size:
        findings.append(f"size mismatch: {field}: {source}")

    expected_sha = value.get("sha256")
    if not isinstance(expected_sha, str) or len(expected_sha) != 64:
        findings.append(f"invalid artifact sha256: {field}: {source}")
    elif _sha256_file(path) != expected_sha.lower():
        findings.append(f"sha256 mismatch: {field}: {source}")
    return findings


def verify_legacy_artifact(value: Any, field: str, source: str) -> list[str]:
    """Verify one legacy absolute artifact path without claiming immutability."""

    if not isinstance(value, str) or not value:
        return [f"missing evidence field {field} for {source}"]
    path = Path(value)
    if not path.is_absolute():
        return [f"evidence path must be absolute: {field}: {value}"]
    if not path.is_file() or path.stat().st_size == 0:
        return [f"evidence artifact missing or empty: {field}: {value}"]
    return []
