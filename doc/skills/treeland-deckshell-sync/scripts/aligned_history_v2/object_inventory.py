"""Inventory and verify loose objects written by one isolated preview."""

from __future__ import annotations

import hashlib
import re
import zlib
from collections import Counter
from pathlib import Path

from .artifacts import with_canonical_hash
from .git_objects import git_object_id


OBJECT_DIR_PATTERN = re.compile(r"[0-9a-f]{2}\Z")
OBJECT_FILE_PATTERN = re.compile(r"[0-9a-f]{38}\Z")
ALLOWED_KINDS = {"blob", "tree", "commit"}


def inventory_loose_objects(object_directory: Path) -> dict[str, object]:
    """Verify every loose object and return a canonical content inventory."""

    root = object_directory.resolve()
    if not root.is_dir():
        raise ValueError(f"preview object directory does not exist: {root}")
    pack = root / "pack"
    if pack.exists() and any(pack.iterdir()):
        raise ValueError("preview object directory contains packed objects")
    objects = []
    for directory in sorted(root.iterdir(), key=lambda path: path.name):
        if not directory.is_dir() or OBJECT_DIR_PATTERN.fullmatch(directory.name) is None:
            continue
        for path in sorted(directory.iterdir(), key=lambda item: item.name):
            if path.is_symlink() or OBJECT_FILE_PATTERN.fullmatch(path.name) is None:
                raise ValueError(f"invalid loose object path: {path}")
            objects.append(_inspect_object(path, directory.name + path.name))
    counts = Counter(item["kind"] for item in objects)
    return with_canonical_hash(
        {
            "schema_version": 2,
            "object_count": len(objects),
            "counts_by_type": dict(sorted(counts.items())),
            "objects": objects,
        }
    )


def _inspect_object(path: Path, object_id: str) -> dict[str, object]:
    try:
        raw = zlib.decompress(path.read_bytes())
    except zlib.error as error:
        raise ValueError(f"invalid compressed loose object: {object_id}") from error
    header, separator, payload = raw.partition(b"\0")
    if not separator:
        raise ValueError(f"loose object lacks header terminator: {object_id}")
    kind_bytes, space, size_bytes = header.partition(b" ")
    if not space:
        raise ValueError(f"loose object has invalid header: {object_id}")
    try:
        kind = kind_bytes.decode("ascii")
        size = int(size_bytes.decode("ascii"))
    except (UnicodeDecodeError, ValueError) as error:
        raise ValueError(f"loose object has invalid header: {object_id}") from error
    if kind not in ALLOWED_KINDS or size != len(payload):
        raise ValueError(f"loose object type or size mismatch: {object_id}")
    if git_object_id(kind, payload) != object_id:
        raise ValueError(f"loose object ID mismatch: {object_id}")
    return {
        "object_id": object_id,
        "kind": kind,
        "size": size,
        "payload_sha256": hashlib.sha256(payload).hexdigest(),
    }
