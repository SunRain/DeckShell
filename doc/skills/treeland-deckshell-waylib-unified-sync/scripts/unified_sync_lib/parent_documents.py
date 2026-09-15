"""Document-level validation for DeckShell parent verification."""

from __future__ import annotations

from pathlib import Path
from typing import Any, List, Mapping

from .artifacts import artifact_errors, read_verified_artifact
from .contract_migration import migration_paths
from .git_ops import canonical_json_sha256
from .patches import commit_diff, source_patch
from .projections import adapted_content_projection_errors, content_projection_errors
from .schema import is_full_sha


def parent_document_errors(
    inventory: Mapping[str, Any],
    manifest: Mapping[str, Any],
    evidence: Mapping[str, Any],
    parent_head: str,
) -> List[str]:
    """Validate parent verifier input schemas and frozen identity."""

    errors: List[str] = []
    if inventory.get("outcome") != "pass":
        errors.append("inventory outcome must be pass")
    if manifest.get("schema_version") != 2:
        errors.append("manifest schema_version must be 2")
    if manifest.get("kind") != "treeland-unified-sync-manifest":
        errors.append("manifest kind is invalid")
    if manifest.get("outcome") != "pass":
        errors.append("manifest outcome must be pass")
    if manifest.get("final_parent_head") != parent_head:
        errors.append("manifest final parent head differs from requested head")
    identity = manifest.get("identity")
    inventory_digest = canonical_json_sha256(inventory)
    if not isinstance(identity, dict) or identity.get("inventory_sha256") != inventory_digest:
        errors.append("manifest identity does not bind the inventory")
    if evidence.get("schema_version") != 2:
        errors.append("parent evidence schema_version must be 2")
    if evidence.get("kind") != "treeland-unified-parent-evidence":
        errors.append("parent evidence kind is invalid")
    if not isinstance(evidence.get("entries"), list):
        errors.append("parent evidence entries must be an array")
    return errors


def _artifact_content_errors(
    record: Any,
    root: Path,
    label: str,
    expected: bytes,
) -> List[str]:
    errors = artifact_errors(record, root, label)
    if errors:
        return errors
    _path, actual = read_verified_artifact(record, root, label)
    return [] if actual == expected else [f"{label} content differs from Git objects"]


def parent_evidence_content_errors(
    source_repo: Path,
    parent_repo: Path,
    item: Mapping[str, Any],
    parent: Mapping[str, Any],
    artifacts: Mapping[str, Any],
    artifact_root: Path,
) -> List[str]:
    """从 Git 对象重建工件，并核对来源或获批适配补丁的内容投影。"""

    source = item["source_commit"]
    target = parent.get("commit")
    errors: List[str] = []
    if is_full_sha(target):
        errors.extend(
            _artifact_content_errors(
                artifacts.get("target_diff"), artifact_root, f"{source}/target_diff",
                commit_diff(parent_repo, str(target)),
            )
        )
    for name, paths in (
        ("mapped_source_patch", item["deckshell"]["mapped_source_paths"]),
        ("root_source_patch", item["deckshell"]["root_source_paths"]),
    ):
        if name in artifacts:
            expected = source_patch(source_repo, source, paths)
            errors.extend(
                _artifact_content_errors(
                    artifacts.get(name), artifact_root, f"{source}/{name}", expected
                )
            )
    if parent.get("action") == "applied" and is_full_sha(target):
        mapped_paths = item["deckshell"]["mapped_source_paths"]
        root_paths = item["deckshell"]["root_source_paths"]
        operations = [
            (source_patch(source_repo, source, mapped_paths), "compositor"),
            (source_patch(source_repo, source, root_paths), None),
        ]
        errors.extend(
            content_projection_errors(
                parent_repo,
                str(target),
                item["deckshell"]["target_paths"],
                operations,
                f"parent {source}",
            )
        )
    if parent.get("action") == "adapted" and is_full_sha(target):
        extra, more = migration_paths(artifacts, artifact_root, source, "parent")
        errors.extend(more)
        errors.extend(adapted_content_projection_errors(
            parent_repo, str(target), item["deckshell"]["target_paths"] + extra,
            artifacts.get("adaptation_patch"), artifact_root, f"parent {source}",
        ))
    return errors
