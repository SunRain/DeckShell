"""Schema-v2 adaptation field parsing and verification."""

from __future__ import annotations

import subprocess
from pathlib import Path, PurePosixPath
from typing import Any

from .artifacts import verify_strict_artifact
from .common import run_git


ADAPTATION_KINDS = {"modified", "omitted", "materialized"}
KIND_ORDER = {"omitted": 0, "materialized": 1, "modified": 2}


def _commit_list_field(body: str, field: str, source: str) -> tuple[list[str], list[str]]:
    header = f"[treeland-sync] {field}:"
    lines = body.splitlines()
    positions = [index for index, line in enumerate(lines) if line.strip() == header]
    if not positions:
        return [], [f"missing commit {field} field for {source}"]
    if len(positions) > 1:
        return [], [f"duplicate commit {field} field for {source}"]

    values: list[str] = []
    findings: list[str] = []
    for line in lines[positions[0] + 1 :]:
        stripped = line.strip()
        if stripped.startswith("[treeland-sync] ") or stripped.startswith(
            "Treeland-Commit:"
        ):
            break
        if not stripped:
            continue
        if not stripped.startswith("- "):
            findings.append(f"malformed commit {field} item for {source}: {stripped}")
            continue
        values.append(stripped[2:].strip())
    if not values:
        findings.append(f"empty commit {field} field for {source}")
    return values, findings


def _valid_repo_path(path: str) -> bool:
    candidate = PurePosixPath(path)
    return bool(path) and not candidate.is_absolute() and ".." not in candidate.parts


def _evidence_paths(entry: dict[str, Any], source: str) -> tuple[list[dict[str, str]], list[str]]:
    raw = entry.get("adaptation_paths", [])
    if raw is None:
        raw = []
    if not isinstance(raw, list):
        return [], [f"adaptation_paths must be a list for {source}"]

    paths: list[dict[str, str]] = []
    findings: list[str] = []
    seen: set[tuple[str, str]] = set()
    seen_paths: set[str] = set()
    for item in raw:
        if not isinstance(item, dict):
            findings.append(f"invalid adaptation path entry for {source}: {item!r}")
            continue
        kind, path = item.get("kind"), item.get("path")
        if kind not in ADAPTATION_KINDS:
            findings.append(f"invalid kind for {source}: {kind}")
            continue
        if not isinstance(path, str) or not _valid_repo_path(path):
            findings.append(f"invalid adaptation path for {source}: {path}")
            continue
        pair = (kind, path)
        if pair in seen or path in seen_paths:
            findings.append(f"duplicate adaptation path for {source}: {kind}: {path}")
            continue
        seen.add(pair)
        seen_paths.add(path)
        paths.append(dict(item))
    return paths, findings


def _message_paths(items: list[str], source: str) -> tuple[list[dict[str, str]], list[str]]:
    if items == ["none"]:
        return [], []
    if "none" in items:
        return [], [f"commit adaptation paths mixes none with paths for {source}"]

    paths = []
    findings = []
    for item in items:
        kind, separator, path = item.partition(": ")
        if not separator:
            findings.append(f"malformed commit adaptation path for {source}: {item}")
            continue
        paths.append({"kind": kind, "path": path})
    return paths, findings


def _notes(value: Any) -> list[str]:
    if not isinstance(value, str):
        return []
    return [line.strip() for line in value.splitlines() if line.strip()]


def _verify_path_semantics(
    source: str,
    paths: list[dict[str, str]],
    actual_paths: set[str],
    expected_paths: set[str],
) -> list[str]:
    findings = []
    known_paths = actual_paths | expected_paths
    for item in paths:
        kind, path = item["kind"], item["path"]
        if path not in known_paths:
            findings.append(
                "adaptation path is outside inventory and target commit: "
                f"{source}: {path}"
            )
        if kind in {"modified", "materialized"} and path not in actual_paths:
            findings.append(
                f"{kind} adaptation path is not in target commit: {source}: {path}"
            )
        if kind == "omitted" and path not in expected_paths:
            findings.append(
                "omitted adaptation path is not expected by inventory: "
                f"{source}: {path}"
            )
        if kind == "omitted" and path in actual_paths:
            findings.append(
                "omitted adaptation path is present in target commit: "
                f"{source}: {path}"
            )
    return findings


def _parent_path_exists(repo: Path, parent: str, path: str) -> bool:
    try:
        run_git(repo, "cat-file", "-e", f"{parent}:{path}")
    except subprocess.CalledProcessError:
        return False
    return True


def _strict_path_findings(
    repo: Path,
    parent: str,
    source: str,
    paths: list[dict[str, Any]],
    actual_statuses: dict[str, str],
    evidence_root: Path | None,
) -> list[str]:
    findings = []
    canonical = sorted(
        paths,
        key=lambda item: (KIND_ORDER[item["kind"]], item["path"].encode("utf-8")),
    )
    if paths != canonical:
        findings.append(f"adaptation paths are not in canonical order for {source}")
    for index, item in enumerate(paths):
        kind, path = item["kind"], item["path"]
        actual_status = actual_statuses.get(path, "")[:1]
        declared_status = item.get("target_status")
        expected_status = "omitted" if kind == "omitted" else actual_status
        if declared_status != expected_status:
            findings.append(f"target_status mismatch for {source}: {path}")
        source_status = item.get("source_status")
        if not isinstance(source_status, str) or source_status[:1] not in "AMDRC":
            findings.append(f"invalid source_status for {source}: {path}")

        parent_exists = _parent_path_exists(repo, parent, path)
        if item.get("parent_exists") is not parent_exists:
            findings.append(f"parent_exists mismatch for {source}: {path}")
        proof = item.get("proof")
        if not isinstance(proof, list) or not proof:
            findings.append(f"missing proof for {source}: {path}")
        else:
            for proof_index, artifact in enumerate(proof):
                field = f"adaptation_paths[{index}].proof[{proof_index}]"
                findings.extend(
                    verify_strict_artifact(evidence_root, artifact, field, source)
                )
        if item.get("review_state") != "approved":
            findings.append(f"review_state is not approved for {source}: {path}")
        if kind == "materialized" and actual_status != "A":
            findings.append(f"materialized target status is not A: {source}: {path}")
        if kind == "materialized" and parent_exists:
            findings.append(f"materialized parent path exists: {source}: {path}")
    return findings


def _evidence_contract(
    entry: dict[str, Any], source: str, action: Any
) -> tuple[list[dict[str, str]], list[str], list[str]]:
    paths, findings = _evidence_paths(entry, source)
    notes = _notes(entry.get("adaptation_notes"))
    if action == "adapted":
        if not paths:
            findings.append(f"missing adaptation_paths for {source}")
        if not notes or notes == ["none"]:
            findings.append(f"missing adaptation_notes for {source}")
        return paths, notes, findings

    if paths:
        findings.append(f"{action} action has adaptation_paths for {source}")
    if notes and notes != ["none"]:
        findings.append(f"{action} action has adaptation_notes for {source}")
    return paths, ["none"], findings


def _message_contract(
    repo: Path, target: str, source: str, strict: bool
) -> tuple[list[dict[str, str]], list[str], list[str]]:
    body = str(run_git(repo, "show", "-s", "--format=%B", target))
    path_items, path_findings = _commit_list_field(body, "adaptation paths", source)
    note_items, note_findings = _commit_list_field(body, "adaptation notes", source)
    paths, message_path_findings = _message_paths(path_items, source)
    findings = path_findings + note_findings + message_path_findings
    if strict:
        path_header = "[treeland-sync] adaptation paths:"
        note_header = "[treeland-sync] adaptation notes:"
        if body.find(path_header) > body.find(note_header):
            findings.append(f"adaptation fields are out of order for {source}")
    return paths, note_items, findings


def verify_adaptation_fields(
    repo: Path,
    target: str,
    entry: dict[str, Any],
    actual_paths: list[str],
    expected_paths: set[str],
    *,
    actual_statuses: dict[str, str] | None = None,
    parent: str = "",
    strict: bool = False,
    evidence_root: Path | None = None,
) -> list[str]:
    """Verify schema-v2 evidence and its canonical commit-message fields."""

    source = str(entry.get("source_commit"))
    action = entry.get("action")
    evidence_paths, evidence_notes, findings = _evidence_contract(
        entry, source, action
    )
    findings.extend(
        _verify_path_semantics(
            source, evidence_paths, set(actual_paths), expected_paths
        )
    )
    if strict:
        findings.extend(
            _strict_path_findings(
                repo,
                parent,
                source,
                evidence_paths,
                actual_statuses or {},
                evidence_root,
            )
        )
    message_paths, message_notes, message_findings = _message_contract(
        repo, target, source, strict
    )
    findings.extend(message_findings)
    canonical_evidence_paths = [
        {"kind": item["kind"], "path": item["path"]} for item in evidence_paths
    ]
    if message_paths != canonical_evidence_paths:
        findings.append(f"commit adaptation paths differ from evidence for {source}")
    if message_notes != evidence_notes:
        findings.append(f"commit adaptation notes differ from evidence for {source}")
    return findings
