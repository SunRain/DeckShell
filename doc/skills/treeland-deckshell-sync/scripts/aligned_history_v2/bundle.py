"""Freeze the repo-local v2 tool bundle used by both previews."""

from __future__ import annotations

import hashlib
from pathlib import Path

from .repository import GitRepository


GENERATED_EVIDENCE_NAMES = {"red-v2-atomic-contract.xml"}


def bundle_files(root: Path, repo_prefix: str) -> dict[str, bytes]:
    """Return every regular bundle file under its repository-relative path."""

    result: dict[str, bytes] = {}
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().encode("utf-8")):
        if not path.is_file() or path.is_symlink():
            continue
        if (
            "__pycache__" in path.parts
            or ".pytest_cache" in path.parts
            or path.suffix == ".pyc"
            or path.name in GENERATED_EVIDENCE_NAMES
        ):
            continue
        relative = path.relative_to(root).as_posix()
        result[f"{repo_prefix}/{relative}"] = path.read_bytes()
    if not result:
        raise ValueError("v2 tool bundle contains no regular files")
    return result


def bundle_sha256(files: dict[str, bytes]) -> str:
    """Hash ordered path and byte pairs for a complete tool bundle."""

    digest = hashlib.sha256()
    for path, content in sorted(files.items(), key=lambda item: item[0].encode("utf-8")):
        digest.update(path.encode("utf-8") + b"\0" + content)
    return digest.hexdigest()


def bundle_overlay(
    repo: GitRepository,
    parent_revision: str,
    files: dict[str, bytes],
    repo_prefix: str,
) -> dict[str, bytes | None]:
    """Calculate the exact overlay that makes the tree equal the frozen bundle."""

    raw = repo.run("ls-tree", "-r", "-z", parent_revision, "--", repo_prefix)
    tracked = _parse_tree_files(raw)
    overlay: dict[str, bytes | None] = {}
    managed_tracked = set(tracked)
    for path in sorted(
        managed_tracked - set(files), key=lambda value: value.encode("utf-8")
    ):
        overlay[path] = None
    for path, content in files.items():
        current = tracked.get(path)
        if current is None or repo.cat_file("blob", current[1]) != content:
            overlay[path] = content
        elif current[0] != "100644":
            raise ValueError(f"tool bundle path has unsupported tracked mode: {path}")
    return overlay


def _parse_tree_files(payload: bytes) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for record in payload.rstrip(b"\0").split(b"\0") if payload else []:
        metadata, separator, path_bytes = record.partition(b"\t")
        if not separator:
            raise ValueError("invalid ls-tree record")
        mode, kind, object_id = metadata.decode("ascii").split(" ")
        if kind != "blob":
            raise ValueError(f"tool bundle contains non-blob entry: {path_bytes!r}")
        path = path_bytes.decode("utf-8")
        result[path] = (mode, object_id)
    return result
