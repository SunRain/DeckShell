"""Import verified preview A loose objects into the formal Git object database."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

from .actual_atomic import verify_compile_atomic_history
from .artifacts import (
    canonical_bytes,
    read_hashed_json,
    with_canonical_hash,
)
from .context import InputPaths
from .freeze_inputs import collect_frozen_inputs
from .manifest import validate_input_manifest
from .object_inventory import inventory_loose_objects
from .preview_compare import compare_previews
from .preview_verification import verify_final_tree
from .repository import GitRepository


MIGRATION_REF_PATTERN = re.compile(
    r"refs/heads/migration/"
    r"commit-aligned-history-corrected-v2-[0-9A-Za-z._-]+\Z"
)
ZERO_OBJECT = "0" * 40


def import_verified_objects(
    formal_repo: GitRepository,
    first_object_directory: Path,
    second_object_directory: Path,
    first_inventory: dict[str, Any],
    second_inventory: dict[str, Any],
) -> dict[str, int]:
    """Copy exact A loose bytes after independently verifying A/B inventories."""

    first_root = first_object_directory.resolve()
    second_root = second_object_directory.resolve()
    if first_root == second_root:
        raise ValueError("preview object directories must be distinct")
    actual_first = inventory_loose_objects(first_root)
    actual_second = inventory_loose_objects(second_root)
    if canonical_bytes(first_inventory) != canonical_bytes(actual_first):
        raise ValueError("preview A object inventory changed after verification")
    if canonical_bytes(second_inventory) != canonical_bytes(actual_second):
        raise ValueError("preview B object inventory changed after verification")
    if canonical_bytes(actual_first) != canonical_bytes(actual_second):
        raise ValueError("preview object inventories differ")
    formal_root = formal_repo.object_directory()
    imported = existing = 0
    for record in actual_first["objects"]:
        source = first_root / record["object_id"][:2] / record["object_id"][2:]
        destination = formal_root / record["object_id"][:2] / record["object_id"][2:]
        if _import_one(source, destination):
            imported += 1
        else:
            existing += 1
        _verify_formal_object(formal_repo, record)
    return {
        "verified_object_count": len(actual_first["objects"]),
        "imported_object_count": imported,
        "preexisting_object_count": existing,
    }


def create_migration_ref(repo: GitRepository, ref: str, head: str) -> str:
    """Create the temporary v2 migration ref with expected-absent CAS."""

    if MIGRATION_REF_PATTERN.fullmatch(ref) is None:
        raise ValueError(f"invalid v2 migration ref: {ref}")
    if repo.run("cat-file", "-t", head).decode().strip() != "commit":
        raise ValueError("v2 migration head is not a commit")
    existing = repo.run("for-each-ref", "--format=%(objectname)", ref).decode().strip()
    if existing:
        raise ValueError(f"v2 migration ref already exists: {ref}: {existing}")
    repo.run("update-ref", ref, head, ZERO_OBJECT)
    actual = repo.run("rev-parse", "--verify", ref).decode().strip()
    if actual != head:
        raise ValueError(f"v2 migration ref verification failed: {actual}")
    return ref


def run_formal_import(
    paths: InputPaths,
    manifest: dict[str, Any],
    *,
    preview_a_directory: Path,
    preview_b_directory: Path,
    dual_verification_path: Path,
    migration_ref: str,
) -> dict[str, Any]:
    """Reverify both previews, import A, and create the temporary v2 ref."""

    validate_input_manifest(manifest)
    if collect_frozen_inputs(paths) != manifest.get("frozen_inputs"):
        raise ValueError("formal import frozen inputs differ from the manifest")
    dual = read_hashed_json(dual_verification_path.resolve())
    current_dual = compare_previews(
        preview_a_directory.resolve(), preview_b_directory.resolve()
    )
    if canonical_bytes(dual) != canonical_bytes(current_dual):
        raise ValueError("dual-preview verification drift before formal import")
    first = _read_import_preview(preview_a_directory.resolve())
    second = _read_import_preview(preview_b_directory.resolve())
    mapping = first["mapping"]
    if canonical_bytes(mapping) != canonical_bytes(second["mapping"]):
        raise ValueError("preview mappings differ before formal import")
    if canonical_bytes(first["prefix"]) != canonical_bytes(second["prefix"]):
        raise ValueError("preview Treeland prefixes differ before formal import")
    formal = GitRepository(paths.repo)
    refs_before = _snapshot_refs(formal)
    if migration_ref in refs_before:
        raise ValueError(f"v2 migration ref already exists: {migration_ref}")
    import_summary = import_verified_objects(
        formal,
        Path(first["evidence"]["isolation"]["writable_object_directory"]),
        Path(second["evidence"]["isolation"]["writable_object_directory"]),
        first["inventory"],
        second["inventory"],
    )
    _verify_formal_head(formal, manifest, mapping)
    final_verification = verify_final_tree(
        paths,
        formal,
        manifest=manifest,
        v1_tree=manifest["frozen_inputs"]["v1_head_tree"],
        v2_tree=mapping["head_tree"],
        treeland_prefix=first["prefix"],
        expected_gitlink=manifest["frozen_inputs"]["final_gitlink"],
        expected_tool_bundle_sha256=manifest["frozen_inputs"][
            "tool_bundle_sha256"
        ],
    )
    compile_atomic = verify_compile_atomic_history(
        paths, formal, manifest, mapping["entries"]
    )
    for preview in (first, second):
        reported = preview["evidence"].get("compile_atomic_verification")
        if canonical_bytes(reported) != canonical_bytes(compile_atomic):
            raise ValueError(
                "preview compile-atomic evidence drift before formal import"
            )
    create_migration_ref(formal, migration_ref, mapping["head"])
    refs_after = _snapshot_refs(formal)
    expected_refs = dict(refs_before)
    expected_refs[migration_ref] = mapping["head"]
    if refs_after != expected_refs:
        raise ValueError("formal import changed refs outside the v2 migration ref")
    return with_canonical_hash(
        {
            "schema_version": 2,
            "workflow_mode": "commit-aligned-history-rewrite-v2",
            "outcome": "pass",
            "input_manifest_sha256": manifest["canonical_payload_sha256"],
            "dual_preview_sha256": dual["canonical_payload_sha256"],
            "mapping_sha256": mapping["canonical_payload_sha256"],
            "object_inventory_sha256": first["inventory"][
                "canonical_payload_sha256"
            ],
            "head": mapping["head"],
            "head_tree": mapping["head_tree"],
            "migration_ref": migration_ref,
            "refs_unchanged_except_migration": True,
            "formal_final_verification": final_verification,
            "formal_compile_atomic_verification": compile_atomic,
            **import_summary,
        }
    )


def _read_import_preview(directory: Path) -> dict[str, dict[str, Any]]:
    return {
        "mapping": read_hashed_json(directory / "rewrite-target-mapping.v2.json"),
        "inventory": read_hashed_json(directory / "object-inventory.v2.json"),
        "evidence": read_hashed_json(directory / "preview-evidence.v2.json"),
        "prefix": read_hashed_json(directory / "treeland-target-prefix.v2.json"),
    }


def _snapshot_refs(repo: GitRepository) -> dict[str, str]:
    payload = repo.run("for-each-ref", "--format=%(refname)%00%(objectname)")
    result = {}
    for line in payload.decode().splitlines():
        ref, separator, object_id = line.partition("\0")
        if not separator or not ref or not object_id:
            raise ValueError("invalid Git ref snapshot record")
        result[ref] = object_id
    return result


def _verify_formal_head(
    repo: GitRepository, manifest: dict[str, Any], mapping: dict[str, Any]
) -> None:
    head = mapping["head"]
    if repo.run("cat-file", "-t", head).decode().strip() != "commit":
        raise ValueError("formal v2 head is not a commit")
    if repo.tree_id(head) != mapping["head_tree"]:
        raise ValueError("formal v2 head tree differs from preview mapping")
    base = manifest["frozen_inputs"]["rewrite_base"]
    if int(repo.run("rev-list", "--count", f"{base}..{head}")) != 330:
        raise ValueError("formal v2 successor count drift")
    repo.run("fsck", "--strict", "--no-reflogs", "--no-dangling", head)


def _import_one(source: Path, destination: Path) -> bool:
    if destination.exists():
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".aligned-history-v2-", dir=destination.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as output, source.open("rb") as input_file:
            shutil.copyfileobj(input_file, output)
            output.flush()
            os.fsync(output.fileno())
        try:
            os.link(temporary, destination)
            return True
        except FileExistsError:
            return False
    finally:
        temporary.unlink(missing_ok=True)


def _verify_formal_object(repo: GitRepository, record: dict[str, Any]) -> None:
    object_id = record["object_id"]
    kind = repo.run("cat-file", "-t", object_id).decode().strip()
    payload = repo.cat_file(kind, object_id)
    if kind != record["kind"] or len(payload) != record["size"]:
        raise ValueError(f"formal object type or size drift: {object_id}")
    if hashlib.sha256(payload).hexdigest() != record["payload_sha256"]:
        raise ValueError(f"formal object payload drift: {object_id}")
