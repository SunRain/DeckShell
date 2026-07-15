"""Target commit and evidence verification."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import Policy, match_path, parse_name_status_z, run_git


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


def _artifact_finding(entry: dict[str, Any], field: str) -> str | None:
    value = entry.get(field)
    if not isinstance(value, str) or not value:
        return f"missing evidence field {field} for {entry.get('source_commit')}"
    path = Path(value)
    if not path.is_absolute():
        return f"evidence path must be absolute: {field}: {value}"
    if not path.is_file() or path.stat().st_size == 0:
        return f"evidence artifact missing or empty: {field}: {value}"
    return None


def _actual_target_paths(repo: Path, target: str) -> tuple[list[str], bool]:
    parent_line = str(run_git(repo, "rev-list", "--parents", "-n", "1", target)).strip()
    if len(parent_line.split()) != 2:
        return [], False
    raw = run_git(
        repo,
        "diff-tree",
        "--no-commit-id",
        "--name-status",
        "-r",
        "--find-renames",
        "--find-copies",
        "-z",
        f"{target}^",
        target,
        text=False,
    )
    changes = parse_name_status_z(bytes(raw))
    paths = [
        path
        for change in changes
        for path in (change.old_path, change.new_path)
        if path
    ]
    return list(dict.fromkeys(paths)), True


def _verify_action_evidence(
    entry: dict[str, Any], actual_paths: list[str], expected_paths: set[str]
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
    findings.extend(
        filter(None, (_artifact_finding(entry, field) for field in required))
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
) -> list[str]:
    source, target = mapping["source_commit"], mapping["target_commit"]
    actual_paths, single_parent = _actual_target_paths(repo, target)
    if not single_parent:
        return [f"target commit is not a single-parent commit: {target}"]

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
    findings.extend(_verify_action_evidence(pair_evidence[0], actual_paths, expected_paths))
    return findings


def verify_sync(
    repo: Path,
    policy: Policy,
    inventory: dict[str, Any],
    traces: dict[str, Any],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    """Verify target commits, target paths, trace order, and action evidence."""

    findings: list[str] = []
    expected_sources = [
        item["source_commit"]
        for item in inventory.get("commits", [])
        if item["classification"] not in {"dependency-only", "blocked"}
    ]
    trace_complete = (
        traces.get("state") == "already-synced"
        and traces.get("mapped_source_commits") == expected_sources
    )
    if not trace_complete:
        findings.append("trace audit does not contain the complete ordered source mapping")
    findings.extend(traces.get("blocked_reasons", []))

    inventory_by_source = {
        item["source_commit"]: item for item in inventory.get("commits", [])
    }
    evidence_by_pair: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for item in evidence.get("entries", []):
        evidence_by_pair.setdefault(
            (item.get("source_commit"), item.get("target_commit")), []
        ).append(item)

    for mapping in traces.get("mappings", []):
        findings.extend(
            _verify_mapping(
                repo,
                policy,
                inventory,
                inventory_by_source,
                evidence_by_pair,
                mapping,
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
        "schema_version": 1,
        "outcome": "blocked" if findings else "pass",
        "verified_mappings": len(traces.get("mappings", [])),
        "findings": findings,
    }
