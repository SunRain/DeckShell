"""Post-hoc DeckShell parent lane verification."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple

from .adaptations import adaptation_semantic_errors, lane_target_paths
from .artifacts import artifact_errors
from .contract_migration import migration_paths
from .git_ops import changed_paths
from .git_ops import (
    canonical_json_sha256,
    commit_changes,
    resolve_commit,
    run_git,
    stable_unique,
)
from .patches import source_metadata
from .parent_documents import parent_document_errors, parent_evidence_content_errors
from .replay_types import GITLINK_PATH
from .schema import CHILD_CLASSIFICATIONS, inventory_errors, is_full_sha


TRAILER = re.compile(r"(?m)^Treeland-Commit: ([0-9a-f]{40})$")
CLASSIFICATION = re.compile(
    r"(?m)^\[treeland-unified-sync\] classification: "
    r"(deckshell-only|waylib-only|dual)$"
)
ACTION = re.compile(
    r"(?m)^\[treeland-unified-sync\] action: "
    r"(applied|adapted|empty|gitlink-only)$"
)
DROP_BLOCK = re.compile(
    r"(?m)^\[treeland-unified-sync\] drop files:$\n((?:- [^\n]*\n?)+)"
)
NOTES_BLOCK = re.compile(
    r"(?m)^\[treeland-unified-sync\] adaptation notes:$\n((?:- [^\n]*\n?)+)"
)
MAPPING_BLOCK = re.compile(
    r"(?m)^\[treeland-unified-sync\] path mapping:$\n((?:- [^\n]*\n?)+)"
)
ADAPTATION_BLOCK = re.compile(
    r"(?m)^\[treeland-unified-sync\] adaptation paths:$\n((?:- [^\n]*\n?)+)"
)


def _single(pattern: re.Pattern, message: str, label: str) -> tuple:
    matches = pattern.findall(message)
    return (matches[0], []) if len(matches) == 1 else (None, [f"{label} must appear exactly once"])


def _block(pattern: re.Pattern, message: str, label: str) -> tuple:
    matches = pattern.findall(message)
    if len(matches) != 1:
        return [], [f"{label} must appear exactly once"]
    values = [line[2:].strip() for line in matches[0].splitlines()]
    return ([] if values == ["none"] else values), []


def _adaptation_markers(message: str) -> tuple:
    values, errors = _block(ADAPTATION_BLOCK, message, "adaptation paths marker")
    markers: List[Dict[str, str]] = []
    for value in values:
        kind, separator, path = value.partition(": ")
        if not separator or not path:
            errors.append(f"invalid adaptation path marker: {value}")
            continue
        markers.append({"kind": kind, "path": path})
    return markers, errors


def _paths(repo: Path, commit: str) -> List[str]:
    values: List[str] = []
    for change in commit_changes(repo, commit):
        values.extend(changed_paths(change))
    return stable_unique(values)


def _path_mappings(item: Mapping[str, Any]) -> List[str]:
    values: List[str] = []
    for change in item.get("changes", []):
        sides = (change.get("new"),) if str(change.get("status", "")).startswith("C") else (
            change.get("old"),
            change.get("new"),
        )
        for side in sides:
            if side and side.get("category") in {"mapped", "root-owned"}:
                values.append(f"{side['source']} -> {side['target']}")
    return stable_unique(values)


def _original_block(message: str) -> str:
    lines = message.rstrip("\n").splitlines() or ["(empty message)"]
    return "\n".join(f"    {line}" for line in lines)


def _message_errors(
    source_repo: Path,
    parent_repo: Path,
    item: Mapping[str, Any],
    manifest_entry: Mapping[str, Any],
    evidence_entry: Mapping[str, Any],
) -> List[str]:
    source_sha = item["source_commit"]
    target_sha = manifest_entry.get("parent", {}).get("commit")
    message = str(run_git(parent_repo, "show", "-s", "--format=%B", target_sha)).rstrip("\n")
    trailer, errors = _single(TRAILER, message, "Treeland-Commit trailer")
    classification, more = _single(CLASSIFICATION, message, "classification marker")
    errors.extend(more)
    action, more = _single(ACTION, message, "action marker")
    errors.extend(more)
    drops, more = _block(DROP_BLOCK, message, "drop files marker")
    errors.extend(more)
    notes, more = _block(NOTES_BLOCK, message, "adaptation notes marker")
    errors.extend(more)
    mappings, more = _block(MAPPING_BLOCK, message, "path mapping marker")
    errors.extend(more)
    adaptation_markers, more = _adaptation_markers(message)
    errors.extend(more)
    if trailer != source_sha or classification != item["classification"]:
        errors.append(f"parent message source/classification mismatch for {source_sha}")
    if action != manifest_entry.get("parent", {}).get("action"):
        errors.append(f"parent message action mismatch for {source_sha}")
    if drops != item["deckshell"]["drop_paths"]:
        errors.append(f"parent message drop paths mismatch for {source_sha}")
    expected_notes = evidence_entry.get("adaptation_notes", [])
    if notes != ([] if expected_notes == ["none"] else expected_notes):
        errors.append(f"parent message adaptation notes mismatch for {source_sha}")
    if mappings != _path_mappings(item):
        errors.append(f"parent message path mapping mismatch for {source_sha}")
    expected_adaptations = [
        {"kind": value.get("kind"), "path": value.get("path")}
        for value in evidence_entry.get("adaptation_paths", [])
        if isinstance(value, dict)
    ]
    if adaptation_markers != expected_adaptations:
        errors.append(f"parent message adaptation paths mismatch for {source_sha}")
    child = manifest_entry.get("child")
    if not isinstance(child, dict):
        errors.append(f"parent manifest child lane is invalid for {source_sha}")
        child = {}
    child_sha = child.get("commit")
    if child_sha and str(child_sha) not in message:
        errors.append(f"parent message omits child commit for {source_sha}")
    if message.count("Original treeland commit:\n") != 1:
        errors.append("Original treeland commit marker must appear exactly once")
    source = source_metadata(source_repo, source_sha)
    expected_original = f"Original treeland commit:\n{_original_block(source['message'])}\n"
    target_subject = str(
        run_git(parent_repo, "show", "-s", "--format=%s", str(target_sha))
    ).rstrip("\n")
    if expected_original not in message or target_subject != source["subject"]:
        errors.append(f"parent original message differs from source for {source_sha}")
    errors.extend(_author_errors(source_repo, parent_repo, source_sha, str(target_sha)))
    return errors


def _author_errors(
    source_repo: Path, parent_repo: Path, source_sha: str, target_sha: str
) -> List[str]:
    source = source_metadata(source_repo, source_sha)
    raw = str(run_git(parent_repo, "show", "-s", "--format=%an%x00%ae%x00%aI", target_sha)).rstrip("\n")
    author, email, date = raw.split("\0")
    if (author, email, date) != (source["author"], source["email"], source["date"]):
        return [f"parent author identity/date mismatch for {source_sha}"]
    return []


def _action_path_errors(
    item: Mapping[str, Any], manifest_entry: Mapping[str, Any], actual: Sequence[str],
    structural_paths: Sequence[str] = (),
) -> List[str]:
    source = item["source_commit"]
    action = manifest_entry.get("parent", {}).get("action")
    classification = item["classification"]
    allowed_content = set(item["deckshell"]["target_paths"]) | set(structural_paths)
    allowed = set(allowed_content)
    if classification in CHILD_CLASSIFICATIONS:
        allowed.add(GITLINK_PATH)
    actual_set = set(actual)
    errors = [
        f"target path expansion for {source}: {path}"
        for path in sorted(actual_set - allowed)
    ]
    content = actual_set - {GITLINK_PATH}
    if action == "applied" and content != allowed_content:
        errors.append(f"applied parent paths differ from inventory for {source}")
    if action == "adapted" and not content:
        errors.append(f"adapted parent commit has no content path for {source}")
    if action == "empty" and content:
        errors.append(f"empty parent commit has content paths for {source}")
    if action == "gitlink-only" and actual != [GITLINK_PATH]:
        errors.append(f"gitlink-only parent purity violation for {source}")
    if classification == "waylib-only" and action != "gitlink-only":
        errors.append(f"waylib-only parent action mismatch for {source}")
    return errors


def _evidence_identity_errors(item, manifest_entry, evidence):
    source = item["source_commit"]
    parent = manifest_entry.get("parent", {})
    errors = []
    expected = (source, parent.get("commit"), item["classification"], parent.get("action"))
    actual = (
        evidence.get("source_commit"), evidence.get("target_commit"),
        evidence.get("classification"), evidence.get("action"),
    )
    if expected != actual:
        errors.append(f"parent evidence identity mismatch for {source}")
    if evidence.get("drop_paths") != item["deckshell"]["drop_paths"]:
        errors.append(f"parent evidence drop paths mismatch for {source}")
    if evidence.get("target_paths") != item["deckshell"]["target_paths"]:
        errors.append(f"parent evidence target paths mismatch for {source}")
    return errors


def _evidence_errors(
    source_repo: Path,
    parent_repo: Path,
    item: Mapping[str, Any],
    manifest_entry: Mapping[str, Any],
    evidence: Mapping[str, Any],
    artifact_root: Path,
) -> List[str]:
    source = item["source_commit"]
    parent = manifest_entry.get("parent", {})
    errors: List[str] = []
    errors.extend(_evidence_identity_errors(item, manifest_entry, evidence))
    artifacts = evidence.get("artifacts", {})
    if not isinstance(artifacts, dict):
        return errors + [f"parent artifacts must be an object for {source}"]
    extra, more = migration_paths(artifacts, artifact_root, source, "parent")
    errors.extend(more)
    if "contract_migration" in artifacts and parent.get("action") != "adapted":
        errors.append("parent public migration requires an adapted action")
    required = ["target_diff"]
    if item["deckshell"]["included"]:
        required.extend(["mapped_source_patch", "root_source_patch"])
    if parent.get("action") == "adapted":
        required.append("adaptation_patch")
        notes = evidence.get("adaptation_notes", [])
        if not any(isinstance(note, str) and note.lower() != "none" for note in notes):
            errors.append(f"adapted parent evidence requires notes for {source}")
        errors.extend(
            adaptation_semantic_errors(
                parent_repo,
                str(parent.get("commit")),
                evidence.get("adaptation_paths"),
                lane_target_paths(item, "parent") + extra,
                _paths(parent_repo, str(parent.get("commit"))),
                artifact_root,
                f"parent {source}",
            )
        )
    elif evidence.get("adaptation_paths") not in (None, []):
        errors.append(f"non-adapted parent evidence has adaptation_paths for {source}")
    if parent.get("action") == "empty":
        errors.extend(
            artifact_errors(
                evidence.get("equivalence_proof"), artifact_root, f"{source}/equivalence_proof",
            )
        )
    for name in required:
        errors.extend(artifact_errors(artifacts.get(name), artifact_root, f"{source}/{name}"))
    errors.extend(
        parent_evidence_content_errors(
            source_repo, parent_repo, item, parent, artifacts, artifact_root
        )
    )
    return errors


def _entry_verification_errors(
    source_repo: Path,
    parent_repo: Path,
    expected: Sequence[Mapping[str, Any]],
    mapped_entries: Sequence[Mapping[str, Any]],
    evidence_entries: Sequence[Any],
    artifact_root: Path,
) -> List[str]:
    errors: List[str] = []
    for index, item in enumerate(expected):
        if index >= len(mapped_entries) or index >= len(evidence_entries):
            continue
        mapped = mapped_entries[index]
        proof = evidence_entries[index]
        if not isinstance(proof, dict):
            errors.append(f"parent evidence entry[{index}] must be an object")
            continue
        if mapped.get("source_commit") != item["source_commit"]:
            errors.append(f"parent source order mismatch at index {index}")
            continue
        parent = mapped.get("parent")
        if not isinstance(parent, dict) or not is_full_sha(parent.get("commit")):
            errors.append(f"parent manifest lane is invalid at index {index}")
            continue
        actual_paths = _paths(parent_repo, parent["commit"])
        extra, more = migration_paths(proof.get("artifacts", {}), artifact_root, item["source_commit"], "parent")
        errors.extend(more)
        errors.extend(_action_path_errors(item, mapped, actual_paths, extra))
        errors.extend(
            _evidence_errors(
                source_repo, parent_repo, item, mapped, proof, artifact_root
            )
        )
        errors.extend(_message_errors(source_repo, parent_repo, item, mapped, proof))
    return errors


def _mapping_verification_errors(
    source_repo: Path,
    parent_repo: Path,
    base_sha: str,
    head_sha: str,
    inventory: Mapping[str, Any],
    manifest: Mapping[str, Any],
    evidence: Mapping[str, Any],
    artifact_root: Path,
) -> Tuple[List[str], int]:
    errors: List[str] = []
    expected = [
        item
        for item in inventory.get("commits", [])
        if isinstance(item, dict) and item.get("classification") != "unowned-skip"
    ]
    raw_manifest = manifest.get("entries", [])
    raw_manifest = raw_manifest if isinstance(raw_manifest, list) else []
    if any(not isinstance(item, dict) for item in raw_manifest):
        errors.append("manifest entry must be an object")
    mapped_entries = [
        item
        for item in raw_manifest
        if isinstance(item, dict) and item.get("classification") != "unowned-skip"
    ]
    raw_evidence = evidence.get("entries", [])
    evidence_entries = raw_evidence if isinstance(raw_evidence, list) else []
    target_commits = str(
        run_git(parent_repo, "rev-list", "--reverse", f"{base_sha}..{head_sha}")
    ).split()
    mapped_commits = [
        item["parent"].get("commit")
        if isinstance(item.get("parent"), dict)
        else None
        for item in mapped_entries
    ]
    if target_commits != mapped_commits:
        errors.append("parent history differs from manifest order")
    if len(expected) != len(mapped_entries) or len(expected) != len(evidence_entries):
        errors.append("parent inventory/manifest/evidence counts differ")
    errors.extend(
        _entry_verification_errors(
            source_repo,
            parent_repo,
            expected,
            mapped_entries,
            evidence_entries,
            artifact_root,
        )
    )
    return errors, len(expected)


def verify_parent_sync(
    source_repo: Path,
    parent_repo: Path,
    parent_base: str,
    parent_head: str,
    inventory: Mapping[str, Any],
    manifest: Mapping[str, Any],
    evidence: Mapping[str, Any],
    artifact_root: Path,
) -> Dict[str, Any]:
    """Verify parent order, target-path authority, messages, and artifacts."""

    base_sha = resolve_commit(parent_repo, parent_base)
    head_sha = resolve_commit(parent_repo, parent_head)
    blockers = inventory_errors(inventory)
    blockers.extend(parent_document_errors(inventory, manifest, evidence, head_sha))
    mapping_errors, verified_entries = _mapping_verification_errors(
        source_repo,
        parent_repo,
        base_sha,
        head_sha,
        inventory,
        manifest,
        evidence,
        artifact_root,
    )
    blockers.extend(mapping_errors)
    blockers = stable_unique(blockers)
    return {
        "schema_version": 2,
        "kind": "treeland-unified-parent-verify",
        "target_range": {"base": base_sha, "head": head_sha},
        "inventory_sha256": canonical_json_sha256(inventory),
        "manifest_sha256": canonical_json_sha256(manifest),
        "evidence_sha256": canonical_json_sha256(evidence),
        "verified_entries": verified_entries,
        "blocked_reasons": blockers,
        "outcome": "blocked" if blockers else "pass",
    }
