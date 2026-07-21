"""Compare two independent object previews at canonical artifact boundaries."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from .artifacts import canonical_bytes, read_hashed_json, with_canonical_hash


def compare_previews(first_directory: Path, second_directory: Path) -> dict[str, Any]:
    """Require byte-equivalent payloads and prove A/B object isolation."""

    first = _read_preview(first_directory.resolve())
    second = _read_preview(second_directory.resolve())
    for key, label in (
        ("prefix", "Treeland prefix"),
        ("mapping", "mapping"),
        ("inventory", "object inventory"),
    ):
        if canonical_bytes(first[key]) != canonical_bytes(second[key]):
            raise ValueError(f"preview {label} payloads differ")
    _verify_isolation(first["evidence"], second["evidence"])
    atomic = first["evidence"].get("compile_atomic_verification")
    if not isinstance(atomic, dict) or atomic.get("outcome") != "pass":
        raise ValueError("preview compile-atomic evidence is not passing")
    if canonical_bytes(atomic) != canonical_bytes(
        second["evidence"].get("compile_atomic_verification")
    ):
        raise ValueError("preview compile-atomic evidence differs")
    mapping = first["mapping"]
    for preview in (first, second):
        evidence = preview["evidence"]
        if evidence.get("outcome") != "pass":
            raise ValueError("preview evidence is not passing")
        if evidence.get("head") != mapping["head"]:
            raise ValueError("preview evidence head differs from mapping")
        if evidence.get("head_tree") != mapping["head_tree"]:
            raise ValueError("preview evidence head tree differs from mapping")
    return with_canonical_hash(
        {
            "schema_version": 2,
            "workflow_mode": "commit-aligned-history-rewrite-v2",
            "outcome": "pass",
            "independent_previews": 2,
            "head": mapping["head"],
            "head_tree": mapping["head_tree"],
            "treeland_prefix_sha256": first["prefix"]["canonical_payload_sha256"],
            "mapping_sha256": mapping["canonical_payload_sha256"],
            "object_inventory_sha256": first["inventory"][
                "canonical_payload_sha256"
            ],
            "objects_identical": True,
            "mapping_bytes_identical": True,
            "head_tree_identical": True,
            "compile_atomic_verification_sha256": hashlib.sha256(
                canonical_bytes(atomic)
            ).hexdigest(),
        }
    )


def _read_preview(directory: Path) -> dict[str, dict[str, Any]]:
    return {
        "prefix": read_hashed_json(directory / "treeland-target-prefix.v2.json"),
        "mapping": read_hashed_json(directory / "rewrite-target-mapping.v2.json"),
        "inventory": read_hashed_json(directory / "object-inventory.v2.json"),
        "evidence": read_hashed_json(directory / "preview-evidence.v2.json"),
    }


def _verify_isolation(first: dict[str, Any], second: dict[str, Any]) -> None:
    if first.get("preview_name") != "A" or second.get("preview_name") != "B":
        raise ValueError("preview evidence must be ordered A then B")
    first_isolation = first.get("isolation", {})
    second_isolation = second.get("isolation", {})
    first_objects = Path(first_isolation.get("writable_object_directory", "")).resolve()
    second_objects = Path(second_isolation.get("writable_object_directory", "")).resolve()
    alternate_a = Path(first_isolation.get("read_only_alternate", "")).resolve()
    alternate_b = Path(second_isolation.get("read_only_alternate", "")).resolve()
    if first_objects == second_objects or first_objects.is_relative_to(second_objects) or second_objects.is_relative_to(first_objects):
        raise ValueError("preview writable object directories are not independent")
    if alternate_a != alternate_b:
        raise ValueError("preview source alternates differ")
    for isolation, objects in (
        (first_isolation, first_objects),
        (second_isolation, second_objects),
    ):
        if objects == alternate_a or objects.is_relative_to(alternate_a) or alternate_a.is_relative_to(objects):
            raise ValueError("preview writable objects overlap the source alternate")
        if isolation.get("alternate_count") != 1:
            raise ValueError("preview does not use exactly one alternate")
        if isolation.get("other_preview_is_alternate") is not False:
            raise ValueError("one preview reads the other preview")
        if isolation.get("formal_object_writes") != 0:
            raise ValueError("preview evidence reports formal object writes")
