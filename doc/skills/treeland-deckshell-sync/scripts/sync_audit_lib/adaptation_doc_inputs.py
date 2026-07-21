"""Validate adaptation document inputs against Git and commit metadata."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from .adaptation import parse_commit_adaptation_fields
from .common import run_git
from .target import inspect_target_commit


SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
DIGEST_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def read_json(path: Path) -> tuple[dict[str, Any], str]:
    """Read one JSON object and return it with its byte-level SHA-256."""

    data = path.read_bytes()
    payload = json.loads(data.decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return payload, hashlib.sha256(data).hexdigest()


def validate_inputs(
    repo: Path,
    manifest: dict[str, Any],
    mapping: dict[str, Any],
    base: str,
    head: str,
) -> list[dict[str, Any]]:
    """Validate top-level contracts and return the manifest entry list."""

    if manifest.get("schema_version") != 2:
        raise ValueError("adaptation manifest schema_version must be 2")
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        raise ValueError("adaptation manifest entries must be a list")
    _validate_manifest_counts(manifest, entries)
    rows = mapping.get("mappings")
    if not isinstance(rows, list):
        raise ValueError("mapping mappings must be a list")
    if mapping.get("count") != len(rows):
        raise ValueError("mapping count does not match mappings")
    if len(rows) != len(entries):
        raise ValueError("mapping count does not match manifest entries")
    plan_digest = mapping.get("plan_digest_sha256")
    if not isinstance(plan_digest, str) or not DIGEST_PATTERN.fullmatch(plan_digest):
        raise ValueError("mapping plan_digest_sha256 must be 64 lowercase hex digits")
    required_sha({"base": base}, "base")
    required_sha({"head": head}, "head")
    try:
        run_git(repo, "merge-base", "--is-ancestor", base, head)
    except subprocess.CalledProcessError as error:
        raise ValueError("base is not an ancestor of head") from error
    return entries


def mapping_by_legacy(mapping: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Index mapping rows by unique legacy target SHA."""

    result: dict[str, dict[str, Any]] = {}
    rows = mapping.get("mappings")
    if not isinstance(rows, list):
        raise ValueError("mapping mappings must be a list")
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("mapping row must be an object")
        legacy = required_sha(row, "legacy_target_commit")
        required_sha(row, "rewritten_target_commit")
        required_sha(row, "source_commit")
        if legacy in result:
            raise ValueError(f"duplicate legacy target mapping: {legacy}")
        result[legacy] = row
    return result


def required_sha(payload: Any, field: str) -> str:
    """Read one required lowercase full Git SHA from an object."""

    if not isinstance(payload, dict):
        raise ValueError(f"missing object for {field}")
    value = payload.get(field)
    if not isinstance(value, str) or not SHA_PATTERN.fullmatch(value):
        raise ValueError(f"invalid {field}: {value!r}")
    return value


def verify_target_in_range(repo: Path, base: str, head: str, target: str) -> None:
    """Require one rewritten target inside the left-open requested range."""

    if target == base:
        raise ValueError(f"rewritten target equals excluded base: {target}")
    try:
        run_git(repo, "merge-base", "--is-ancestor", base, target)
        run_git(repo, "merge-base", "--is-ancestor", target, head)
    except subprocess.CalledProcessError as error:
        raise ValueError(f"rewritten target is outside requested range: {target}") from error


def verify_commit_message(
    repo: Path,
    target: str,
    source: str,
    classification: str,
    paths: list[dict[str, Any]],
    notes: str,
) -> None:
    """Require target message fields to match the reviewed manifest."""

    message_paths, message_notes, findings = parse_commit_adaptation_fields(
        repo, target, source, strict=True
    )
    simple_paths = [
        {"kind": item.get("kind"), "path": item.get("path")} for item in paths
    ]
    if message_paths != simple_paths:
        findings.append(f"commit adaptation paths differ from manifest for {source}")
    expected_notes = [line.strip() for line in notes.splitlines() if line.strip()]
    if message_notes != expected_notes:
        findings.append(f"commit adaptation notes differ from manifest for {source}")
    body = str(run_git(repo, "show", "-s", "--format=%B", target))
    if _single_message_value(body, "classification") != classification:
        findings.append(f"classification mismatch for {source}")
    if _single_message_value(body, "action") != "adapted":
        findings.append(f"action mismatch for {source}")
    trailers = re.findall(r"^Treeland-Commit: ([0-9a-f]{40})$", body, re.MULTILINE)
    if trailers != [source]:
        findings.append(f"Treeland-Commit mismatch for {source}")
    if findings:
        raise ValueError("; ".join(findings))


def validate_path_metadata(
    repo: Path, target: str, path_entry: dict[str, Any]
) -> None:
    """Validate reviewed path semantics against the rewritten target tree."""

    kind = str(path_entry.get("kind"))
    path = str(path_entry.get("path"))
    if path_entry.get("review_state") != "approved":
        raise ValueError(f"review_state is not approved: {target}: {path}")
    proof = path_entry.get("proof")
    if not isinstance(proof, list) or not proof:
        raise ValueError(f"adaptation path lacks proof: {target}: {path}")
    inspection = inspect_target_commit(repo, target)
    if not inspection["single_parent"]:
        raise ValueError(f"adaptation target must have one parent: {target}")
    parent = str(inspection["parent"])
    parent_exists = _tree_path_exists(repo, parent, path)
    if path_entry.get("parent_exists") is not parent_exists:
        label = "exists" if path_entry.get("parent_exists") else "is absent"
        raise ValueError(f"{kind} parent path {label} contrary to Git: {target}: {path}")
    actual_status = str(inspection["statuses"].get(path, ""))
    expected_status = "omitted" if kind == "omitted" else actual_status
    if path_entry.get("target_status") != expected_status:
        raise ValueError(f"target_status mismatch: {target}: {path}")
    if kind == "materialized" and parent_exists:
        raise ValueError(f"materialized parent path exists: {target}: {path}")
    if kind == "materialized" and actual_status != "A":
        raise ValueError(f"materialized target status is not A: {target}: {path}")


def source_path_for_target(entry: dict[str, Any], target_path: str) -> str:
    """Resolve one target path to exactly one source path from manifest changes."""

    matches: set[str] = set()
    changes = entry.get("source_changes")
    if not isinstance(changes, list):
        raise ValueError(f"source_changes must be a list for {target_path}")
    for change in changes:
        if not isinstance(change, dict):
            continue
        for side in (change.get("old"), change.get("new")):
            if not isinstance(side, dict) or side.get("target") != target_path:
                continue
            source = side.get("source")
            if isinstance(source, str) and source:
                matches.add(source)
    if len(matches) != 1:
        raise ValueError(
            f"target path must map to exactly one source path: {target_path}: {sorted(matches)}"
        )
    return matches.pop()


def _validate_manifest_counts(
    manifest: dict[str, Any], entries: list[dict[str, Any]]
) -> None:
    counts = manifest.get("counts")
    if not isinstance(counts, dict):
        raise ValueError("adaptation manifest counts must be an object")
    declared_total = counts.get("total", counts.get("entries"))
    if declared_total != len(entries):
        raise ValueError(
            f"manifest total count mismatch: declared {declared_total}, got {len(entries)}"
        )
    actual_adapted = sum(entry.get("action") == "adapted" for entry in entries)
    if counts.get("adapted") != actual_adapted:
        raise ValueError(
            "manifest adapted count mismatch: "
            f"declared {counts.get('adapted')}, got {actual_adapted}"
        )


def _single_message_value(body: str, field: str) -> str:
    pattern = rf"^\[treeland-sync\] {re.escape(field)}: (.+)$"
    values = re.findall(pattern, body, re.MULTILINE)
    if len(values) != 1:
        raise ValueError(f"commit must contain exactly one {field} field")
    return values[0].strip()


def _tree_path_exists(repo: Path, treeish: str, path: str) -> bool:
    try:
        run_git(repo, "cat-file", "-e", f"{treeish}:{path}")
    except subprocess.CalledProcessError:
        return False
    return True
