"""Target commit and evidence verification."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .adaptation import verify_adaptation_fields
from .artifacts import verify_legacy_artifact, verify_strict_artifact
from .common import Policy, match_path
from .target import inspect_target_commit


def _target_roots(
    policy: Policy, inventory: dict[str, Any]
) -> tuple[dict[str, str], dict[str, str]]:
    directories: dict[str, str] = {}
    files: dict[str, str] = {}
    for section_name in ("mapped", "root_owned"):
        section = policy.get(section_name, {})
        directories.update(
            {str(value): str(value) for value in section.get("directories", {}).values()}
        )
        files.update({str(value): str(value) for value in section.get("files", {}).values()})
    approved = set(inventory.get("approved_review", []))
    review = policy.get("review_only", {})
    directories.update(
        {
            str(target): str(target)
            for source, target in review.get("directories", {}).items()
            if source in approved
        }
    )
    files.update(
        {
            str(target): str(target)
            for source, target in review.get("files", {}).items()
            if source in approved
        }
    )
    return directories, files


def classify_target_path(path: str, policy: Policy, inventory: dict[str, Any]) -> str:
    """Classify a target commit path against approved DeckShell destinations."""

    excluded = policy.get("excluded", {})
    for root in excluded.get("directories", []):
        if path == root or path.startswith(f"{root}/"):
            return "excluded"
    if path in set(excluded.get("files", [])):
        return "excluded"
    directories, files = _target_roots(policy, inventory)
    return "allowed" if match_path(path, directories, files) else "unknown"


def _verify_action_evidence(
    entry: dict[str, Any],
    actual_paths: list[str],
    expected_paths: set[str],
    strict: bool,
    evidence_root: Path | None,
) -> list[str]:
    findings: list[str] = []
    source = entry.get("source_commit")
    action = entry.get("action")
    if action not in {"applied", "adapted", "empty"}:
        return [f"invalid action for {source}: {action}"]
    required = ["mapped_patch", "commit_diff", "path_audit"]
    if action in {"applied", "adapted"}:
        required.append("staged_diff")
    if action == "adapted":
        required.append("difference_report")
        notes = entry.get("adaptation_notes")
        if not isinstance(notes, str) or not notes.strip():
            findings.append(f"missing adaptation_notes for {source}")
    if action == "empty":
        required.append("equivalence_proof")
    for field in required:
        if strict:
            findings.extend(
                verify_strict_artifact(
                    evidence_root, entry.get(field), field, str(source)
                )
            )
        else:
            findings.extend(
                verify_legacy_artifact(entry.get(field), field, str(source))
            )
    if action == "applied" and set(actual_paths) != expected_paths:
        findings.append(f"applied target paths differ from inventory: {source}")
    if action == "empty" and actual_paths:
        findings.append(f"empty action produced target paths: {source}")
    return findings


def _verify_mapping(
    repo: Path,
    policy: Policy,
    inventory: dict[str, Any],
    inventory_by_source: dict[str, dict[str, Any]],
    evidence_by_pair: dict[tuple[str, str], list[dict[str, Any]]],
    mapping: dict[str, Any],
    evidence_schema_version: int,
    required_evidence_schema: int | None,
    evidence_root: Path | None,
) -> list[str]:
    source, target = mapping["source_commit"], mapping["target_commit"]
    target_changes = inspect_target_commit(repo, target)
    if not target_changes["single_parent"]:
        return [f"target commit is not a single-parent commit: {target}"]
    actual_paths = target_changes["all_paths"]
    actual_statuses = target_changes["statuses"]
    parent = target_changes["parent"]

    findings = []
    for path in actual_paths:
        category = classify_target_path(path, policy, inventory)
        if category != "allowed":
            findings.append(f"target path is {category}: {target}: {path}")
    pair_evidence = evidence_by_pair.get((source, target), [])
    if len(pair_evidence) != 1:
        findings.append(f"expected exactly one evidence entry: {source} -> {target}")
        return findings
    expected_paths = set(inventory_by_source.get(source, {}).get("target_paths", []))
    evidence_entry = pair_evidence[0]
    findings.extend(
        _verify_action_evidence(
            evidence_entry,
            actual_paths,
            expected_paths,
            required_evidence_schema == 2,
            evidence_root,
        )
    )
    if evidence_schema_version == 2:
        findings.extend(
            verify_adaptation_fields(
                repo,
                target,
                evidence_entry,
                actual_paths,
                expected_paths,
                actual_statuses=actual_statuses,
                parent=parent,
                strict=required_evidence_schema == 2,
                evidence_root=evidence_root,
            )
        )
    return findings


def _evidence_schema_version(evidence: dict[str, Any]) -> tuple[int, list[str]]:
    version = evidence.get("schema_version", 1)
    if type(version) is int and version in {1, 2}:
        return version, []
    return 1, [f"unsupported evidence schema_version: {version}"]


def _trace_findings(
    inventory: dict[str, Any], traces: dict[str, Any]
) -> list[str]:
    expected_sources = [
        item["source_commit"]
        for item in inventory.get("commits", [])
        if item["classification"] not in {"dependency-only", "blocked"}
    ]
    complete = (
        traces.get("state") == "already-synced"
        and traces.get("mapped_source_commits") == expected_sources
    )
    findings = [] if complete else [
        "trace audit does not contain the complete ordered source mapping"
    ]
    return findings + traces.get("blocked_reasons", [])


def _index_evidence(
    evidence: dict[str, Any],
) -> dict[tuple[str, str], list[dict[str, Any]]]:
    indexed: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for item in evidence.get("entries", []):
        indexed.setdefault(
            (item.get("source_commit"), item.get("target_commit")), []
        ).append(item)
    return indexed


def verify_sync(
    repo: Path,
    policy: Policy,
    inventory: dict[str, Any],
    traces: dict[str, Any],
    evidence: dict[str, Any],
    required_evidence_schema: int | None = None,
    evidence_root: Path | None = None,
) -> dict[str, Any]:
    """Verify target commits, target paths, trace order, and action evidence."""

    evidence_schema_version, findings = _evidence_schema_version(evidence)
    if (
        required_evidence_schema is not None
        and evidence_schema_version != required_evidence_schema
    ):
        findings.append(
            "strict evidence schema "
            f"{required_evidence_schema} required; got {evidence_schema_version}"
        )
    findings.extend(_trace_findings(inventory, traces))
    inventory_by_source = {
        item["source_commit"]: item for item in inventory.get("commits", [])
    }
    evidence_by_pair = _index_evidence(evidence)
    for mapping in traces.get("mappings", []):
        findings.extend(
            _verify_mapping(
                repo,
                policy,
                inventory,
                inventory_by_source,
                evidence_by_pair,
                mapping,
                evidence_schema_version,
                required_evidence_schema,
                evidence_root,
            )
        )

    expected_pairs = {
        (item["source_commit"], item["target_commit"]) for item in traces.get("mappings", [])
    }
    extra_pairs = set(evidence_by_pair).difference(expected_pairs)
    if extra_pairs:
        findings.append(f"evidence contains unmapped pairs: {sorted(extra_pairs)}")
    findings = list(dict.fromkeys(findings))
    return {
        "schema_version": 2,
        "report_schema_version": 2,
        "evidence_schema_version": evidence_schema_version,
        "strict_evidence_schema_required": required_evidence_schema,
        "outcome": "blocked" if findings else "pass",
        "verified_mappings": len(traces.get("mappings", [])),
        "findings": findings,
    }
