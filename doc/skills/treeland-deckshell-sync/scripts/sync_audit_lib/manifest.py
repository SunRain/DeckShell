"""Candidate and approved adaptation manifest generation."""

from __future__ import annotations

import copy
import hashlib
import subprocess
from pathlib import Path
from typing import Any

from .artifacts import build_artifact_reference
from .common import run_git
from .patch_delta import compare_patch_sections, parse_patch_sections
from .target import inspect_target_commit


KIND_ORDER = {"omitted": 0, "materialized": 1, "modified": 2}
PROOF_FIELDS = ("difference_report", "path_audit", "commit_diff")


def _index_unique(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    indexed = {}
    for item in items:
        value = item.get(key)
        if not isinstance(value, str) or not value:
            raise ValueError(f"missing {key}")
        if value in indexed:
            raise ValueError(f"duplicate {key}: {value}")
        indexed[value] = item
    return indexed


def _source_statuses(inventory_entry: dict[str, Any]) -> dict[str, str]:
    statuses = {}
    for change in inventory_entry.get("changes", []):
        status = str(change.get("status", ""))[:1]
        for side in (change.get("old"), change.get("new")):
            if isinstance(side, dict) and isinstance(side.get("target"), str):
                statuses[side["target"]] = status
    return statuses


def _parent_exists(repo: Path, parent: str, path: str) -> bool:
    try:
        run_git(repo, "cat-file", "-e", f"{parent}:{path}")
    except subprocess.CalledProcessError:
        return False
    return True


def _proof_references(
    evidence_root: Path,
    source: str,
    legacy_entry: dict[str, Any],
) -> list[dict[str, Any]]:
    references = []
    for field in PROOF_FIELDS:
        legacy_path = legacy_entry.get(field)
        if not isinstance(legacy_path, str) or not legacy_path:
            continue
        path = evidence_root / "source" / "adapted" / source / Path(legacy_path).name
        if path.is_file():
            references.append(build_artifact_reference(evidence_root, path))
    if not references:
        raise ValueError(f"adapted entry has no persistent proof: {source}")
    return references


def _persistent_artifact(
    evidence_root: Path, source: str, legacy_entry: dict[str, Any], field: str
) -> Path | None:
    legacy_path = legacy_entry.get(field)
    if not isinstance(legacy_path, str) or not legacy_path:
        return None
    path = evidence_root / "source" / "adapted" / source / Path(legacy_path).name
    return path if path.is_file() else None


def _source_target_map(inventory_entry: dict[str, Any]) -> dict[str, str]:
    mapping = {}
    for change in inventory_entry.get("changes", []):
        status = str(change.get("status", ""))[:1]
        preferred = change.get("old") if status == "D" else change.get("new")
        if isinstance(preferred, dict):
            source, target = preferred.get("source"), preferred.get("target")
            if isinstance(source, str) and isinstance(target, str):
                mapping[source] = target
    return mapping


def _delta_comparisons(
    evidence_root: Path,
    source: str,
    inventory_entry: dict[str, Any],
    legacy_entry: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    filtered = _persistent_artifact(
        evidence_root, source, legacy_entry, "mapped_patch"
    )
    commit_diff = _persistent_artifact(
        evidence_root, source, legacy_entry, "commit_diff"
    )
    if filtered is None or commit_diff is None:
        return {}
    return compare_patch_sections(
        parse_patch_sections(filtered.read_text(encoding="utf-8", errors="replace")),
        parse_patch_sections(commit_diff.read_text(encoding="utf-8", errors="replace")),
        _source_target_map(inventory_entry),
    )


def _message_sha256(repo: Path, target: str) -> str:
    message = str(run_git(repo, "show", "-s", "--format=%B", target))
    return hashlib.sha256(message.encode("utf-8")).hexdigest()


def _candidate_paths(
    repo: Path,
    source: str,
    inventory_entry: dict[str, Any],
    target_changes: dict[str, Any],
    proof: list[dict[str, Any]],
    comparisons: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    statuses = _source_statuses(inventory_entry)
    actual = {item["path"]: item for item in target_changes["canonical_changes"]}
    expected = set(inventory_entry.get("target_paths", []))
    observations = []
    for path in sorted(expected.difference(target_changes["all_paths"])):
        observations.append(
            {
                "suggested_kind": "omitted",
                "path": path,
                "target_status": "omitted",
                "source_status": statuses.get(path, ""),
                "parent_exists": _parent_exists(repo, target_changes["parent"], path),
                "proof": proof,
                "delta_equivalent": False,
                "review_state": "candidate",
            }
        )
    for path, change in actual.items():
        target_status = str(change["status"])[:1]
        parent_exists = _parent_exists(repo, target_changes["parent"], path)
        source_status = statuses.get(path, target_status)
        suggested = (
            "materialized"
            if target_status == "A" and source_status != "A" and not parent_exists
            else "modified"
        )
        comparison = comparisons.get(path, {})
        observations.append(
            {
                "suggested_kind": suggested,
                "path": path,
                "target_status": target_status,
                "source_status": source_status,
                "parent_exists": parent_exists,
                "proof": proof,
                "delta_comparison": comparison,
                "delta_equivalent": bool(comparison.get("delta_equivalent")),
                "review_state": "candidate",
            }
        )
    candidates = [
        item
        for item in observations
        if item["target_status"] == "omitted" or not item["delta_equivalent"]
    ]
    return observations, candidates


def _candidate_entry(
    repo: Path,
    ordinal: int,
    inventory_entry: dict[str, Any],
    mapping: dict[str, Any],
    legacy_entry: dict[str, Any],
    evidence_root: Path,
) -> dict[str, Any]:
    source = mapping["source_commit"]
    target = mapping["target_commit"]
    action = legacy_entry.get("action")
    target_changes = inspect_target_commit(repo, target)
    if not target_changes["single_parent"]:
        raise ValueError(f"target is not single parent: {target}")
    entry = {
        "ordinal": ordinal,
        "source_commit": source,
        "legacy_target_commit": target,
        "classification": inventory_entry.get("classification"),
        "action": action,
        "expected_paths": inventory_entry.get("target_paths", []),
        "actual_changes": target_changes["canonical_changes"],
        "source_changes": inventory_entry.get("changes", []),
        "legacy_message_sha256": _message_sha256(repo, target),
        "legacy_adaptation_notes": legacy_entry.get("adaptation_notes", "none"),
    }
    if action == "adapted":
        proof = _proof_references(evidence_root, source, legacy_entry)
        comparisons = _delta_comparisons(
            evidence_root, source, inventory_entry, legacy_entry
        )
        entry["delta_comparisons"] = comparisons
        observations, candidates = _candidate_paths(
            repo, source, inventory_entry, target_changes, proof, comparisons
        )
        entry["path_observations"] = observations
        entry["adaptation_candidates"] = candidates
    return entry


def build_candidate_manifest(
    *,
    repo: Path,
    inventory: dict[str, Any],
    traces: dict[str, Any],
    legacy_evidence: dict[str, Any],
    evidence_root: Path,
    migration_id: str,
) -> dict[str, Any]:
    """Build objective candidates without approving semantic adaptation paths."""

    inventory_entries = [
        item
        for item in inventory.get("commits", [])
        if item.get("classification") not in {"dependency-only", "blocked"}
    ]
    mappings = traces.get("mappings", [])
    if len(inventory_entries) != len(mappings):
        raise ValueError("inventory and trace mapping count differ")
    by_source = _index_unique(inventory_entries, "source_commit")
    evidence_by_source = _index_unique(legacy_evidence.get("entries", []), "source_commit")
    entries = []
    for ordinal, mapping in enumerate(mappings, 1):
        source = mapping["source_commit"]
        entries.append(
            _candidate_entry(
                repo,
                ordinal,
                by_source[source],
                mapping,
                evidence_by_source[source],
                evidence_root,
            )
        )
    counts = {
        "total": len(entries),
        "applied": sum(item["action"] == "applied" for item in entries),
        "adapted": sum(item["action"] == "adapted" for item in entries),
        "empty": sum(item["action"] == "empty" for item in entries),
    }
    return {
        "schema_version": 2,
        "migration_id": migration_id,
        "legacy_range": {
            "base_exclusive": inventory.get("range_base"),
            "head_inclusive": inventory.get("range_head"),
            "count": len(entries),
        },
        "counts": counts,
        "entries": entries,
    }


def _final_paths(
    candidate: dict[str, Any], review: dict[str, Any]
) -> list[dict[str, Any]]:
    observations = {item["path"]: item for item in candidate["path_observations"]}
    paths = []
    for requested in review.get("adaptation_paths", []):
        path, kind = requested.get("path"), requested.get("kind")
        if path not in observations:
            raise ValueError(f"review path is not a candidate: {candidate['source_commit']}: {path}")
        observation = observations[path]
        if kind not in KIND_ORDER:
            raise ValueError(f"invalid review kind: {kind}")
        if observation["target_status"] == "omitted" and kind != "omitted":
            raise ValueError(f"omitted candidate changed kind: {path}")
        if kind == "materialized" and (
            observation["target_status"] != "A" or observation["parent_exists"]
        ):
            raise ValueError(f"invalid materialized review: {path}")
        approved = {
            "kind": kind,
            "path": path,
            "target_status": observation["target_status"],
            "source_status": observation["source_status"],
            "parent_exists": observation["parent_exists"],
            "proof": observation["proof"],
            "review_state": "approved",
        }
        basis = requested.get("review_basis")
        justification = requested.get("justification")
        if isinstance(basis, str) and basis:
            approved["review_basis"] = basis
        if isinstance(justification, str) and justification.strip():
            approved["justification"] = justification.strip()
        if observation.get("delta_equivalent"):
            if (
                basis != "persistent-contract"
                or not isinstance(justification, str)
                or not justification.strip()
            ):
                raise ValueError(f"persistent-contract justification required: {path}")
        paths.append(approved)
    if not paths:
        raise ValueError(f"adapted review has no paths: {candidate['source_commit']}")
    return sorted(paths, key=lambda item: (KIND_ORDER[item["kind"]], item["path"].encode("utf-8")))


def finalize_manifest(
    candidate_manifest: dict[str, Any], reviews: dict[str, Any]
) -> dict[str, Any]:
    """Apply explicit human/agent reviews and produce the canonical manifest."""

    review_by_source = _index_unique(reviews.get("entries", []), "source_commit")
    entries = []
    consumed = set()
    for candidate in candidate_manifest.get("entries", []):
        entry = copy.deepcopy(candidate)
        entry.pop("adaptation_candidates", None)
        entry.pop("path_observations", None)
        if entry["action"] == "adapted":
            source = entry["source_commit"]
            review = review_by_source.get(source)
            if review is None:
                raise ValueError(f"missing adapted review: {source}")
            notes = review.get("adaptation_notes")
            if not isinstance(notes, str) or not notes.strip() or notes.strip() == "none":
                raise ValueError(f"invalid adapted notes: {source}")
            entry["adaptation_paths"] = _final_paths(candidate, review)
            entry["adaptation_notes"] = notes.strip()
            entry["reviewed_by"] = review.get("reviewed_by")
            entry["reviewed_at"] = review.get("reviewed_at")
            consumed.add(source)
        else:
            entry["adaptation_paths"] = []
            entry["adaptation_notes"] = "none"
        entries.append(entry)
    extras = set(review_by_source).difference(consumed)
    if extras:
        raise ValueError(f"reviews contain non-adapted or unknown sources: {sorted(extras)}")
    return {
        **{key: value for key, value in candidate_manifest.items() if key != "entries"},
        "entries": entries,
    }
