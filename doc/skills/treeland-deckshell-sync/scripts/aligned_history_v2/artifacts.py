"""Canonical JSON hashing and sidecar-backed artifact writes."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any


SELF_HASH_FIELD = "canonical_payload_sha256"


def canonical_bytes(payload: Any) -> bytes:
    """Serialize JSON using stable UTF-8 key and separator rules."""

    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return (encoded + "\n").encode("utf-8")


def canonical_payload_sha256(payload: dict[str, Any]) -> str:
    """Hash a payload while excluding only its self-description field."""

    unhashed = copy.deepcopy(payload)
    unhashed.pop(SELF_HASH_FIELD, None)
    return hashlib.sha256(canonical_bytes(unhashed)).hexdigest()


def with_canonical_hash(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a deep copy carrying its canonical payload hash."""

    result = copy.deepcopy(payload)
    result[SELF_HASH_FIELD] = canonical_payload_sha256(result)
    return result


def write_hashed_json(path: Path, payload: dict[str, Any]) -> dict[str, str]:
    """Write pretty JSON and a non-recursive full-file SHA-256 sidecar."""

    hashed = with_canonical_hash(payload)
    serialized = (
        json.dumps(hashed, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(serialized)
    file_hash = hashlib.sha256(serialized).hexdigest()
    sidecar = path.with_name(path.name + ".sha256")
    sidecar.write_text(f"{file_hash}  {path.name}\n", encoding="ascii", newline="\n")
    return {
        "canonical_payload_sha256": hashed[SELF_HASH_FIELD],
        "file_sha256": file_hash,
        "sidecar": str(sidecar),
    }


def read_hashed_json(path: Path) -> dict[str, Any]:
    """Read a JSON artifact and verify its canonical and sidecar hashes."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    expected = payload.get(SELF_HASH_FIELD)
    if expected != canonical_payload_sha256(payload):
        raise ValueError(f"canonical payload hash mismatch: {path}")
    sidecar = path.with_name(path.name + ".sha256")
    parts = sidecar.read_text(encoding="ascii").strip().split()
    if len(parts) != 2 or parts[1] != path.name:
        raise ValueError(f"invalid SHA-256 sidecar: {sidecar}")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if parts[0] != actual:
        raise ValueError(f"file SHA-256 mismatch: {path}")
    return payload
