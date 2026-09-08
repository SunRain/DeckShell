"""Waylib lane evidence integrity and semantic verification."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from .adaptations import adaptation_semantic_errors, lane_target_paths
from .artifacts import artifact_errors, read_verified_artifact
from .contracts import source_contract_audit_errors
from .git_ops import canonical_json_sha256, resolve_commit, stable_unique
from .patches import commit_diff, source_patch
from .wlroots import nested_transition, updater_guard_errors, wlroots_source_audit
from .projections import adapted_content_projection_errors, content_projection_errors
from .schema import (
    LANE_ACTIONS,
    CHILD_ACTIONS,
    WLROOTS_ROOT,
    WAYLIB_EVIDENCE_KIND,
    child_inventory_entries,
    inventory_errors,
    is_full_sha,
)


def _content_errors(
    record: Any, root: Path, label: str, expected: bytes
) -> List[str]:
    errors = artifact_errors(record, root, label)
    if errors:
        return errors
    _path, content = read_verified_artifact(record, root, label)
    return [] if content == expected else [f"{label} content differs from Git objects"]


def _child_contract_errors(
    record: Any, root: Path, repo: Path, target: str
) -> List[str]:
    label = "child source contract audit"
    errors = artifact_errors(record, root, label)
    if errors:
        return errors
    try:
        _path, content = read_verified_artifact(record, root, label)
        audit = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as error:
        return [f"{label} is invalid JSON: {error}"]
    return source_contract_audit_errors(repo, f"{target}^", target, audit)


def _entry_artifact_errors(entry, expected, source_repo, target_repo, root, lane="child"):
    errors: List[str] = []
    action = entry.get("content_action", entry.get("action"))
    artifacts = entry.get("artifacts")
    if not isinstance(artifacts, dict):
        return ["entry artifacts must be an object"]
    source_sha, target_sha = str(entry.get("source_commit")), str(entry.get("target_commit"))
    lane_data = expected["waylib_shared" if lane == "child" else "wlroots"]
    patch = source_patch(source_repo, source_sha, lane_data["source_paths"], WLROOTS_ROOT if lane == "wlroots" else None)
    errors.extend(_content_errors(artifacts.get("source_patch"), root, "artifacts.source_patch", patch))
    if is_full_sha(target_sha):
        errors.extend(_content_errors(artifacts.get("target_diff"), root, "artifacts.target_diff", commit_diff(target_repo, target_sha)))
        if lane == "child":
            errors.extend(updater_guard_errors(source_repo, source_sha, target_repo, target_sha, f"{target_sha}^"))
            errors.extend(_child_contract_errors(artifacts.get("source_contract_audit"), root, target_repo, target_sha))
            audit_record = artifacts.get("source_contract_audit")
            if not artifact_errors(audit_record, root, "audit"):
                _, raw = read_verified_artifact(audit_record, root, "audit")
                audit = json.loads(raw.decode("utf-8"))
                approval = audit.get("approved_additions")
                if approval is not None:
                    errors.extend(artifact_errors(artifacts.get("contract_additions"), root, "contract additions"))
                    if not artifact_errors(artifacts.get("contract_additions"), root, "contract additions"):
                        _, raw_approval = read_verified_artifact(artifacts["contract_additions"], root, "contract additions")
                        if json.loads(raw_approval.decode("utf-8")) != approval:
                            errors.append("contract additions differ from the approved artifact")
        else:
            records = {**artifacts, "equivalence_proof": entry.get("equivalence_proof")}
            audit = wlroots_source_audit(source_repo, target_repo, expected, target_sha, action, entry.get("adaptation_paths", []), records, root)
            errors.extend(audit["blocked_reasons"])
            record = artifacts.get("source_audit")
            errors.extend(artifact_errors(record, root, "wlroots source audit"))
            if not artifact_errors(record, root, "wlroots source audit"):
                _, raw = read_verified_artifact(record, root, "wlroots source audit")
                if json.loads(raw.decode("utf-8")) != audit:
                    errors.append("wlroots source audit differs from Git objects")
        if action == "applied":
            errors.extend(content_projection_errors(target_repo, target_sha, lane_target_paths(expected, lane), [(patch, None)], f"{lane} {source_sha}"))
        if action == "adapted" and lane == "child":
            structural = entry.get("structural_paths", [])
            paths = lane_target_paths(expected, lane) + (structural if structural == ["CMakeLists.txt"] else [])
            errors.extend(adapted_content_projection_errors(target_repo, target_sha, paths, artifacts.get("adaptation_patch"), root, f"{lane} {source_sha}"))
    if action == "empty":
        errors.extend(artifact_errors(entry.get("equivalence_proof"), root, "equivalence_proof"))
    return errors


def _derived_child_paths(entry, trace, repo, target, lane):
    errors = []
    derived = set()
    nested = entry.get("nested_gitlink")
    if nested != trace.get("nested_gitlink"):
        errors.append("nested gitlink differs from commit message")
    if nested is not None:
        if lane != "child" or not isinstance(nested, dict) or not is_full_sha(nested.get("to")) or not isinstance(nested.get("url"), str):
            errors.append("invalid nested gitlink metadata")
        else:
            try:
                value = nested_transition(repo, f"{target}^", target, nested["to"], nested["url"])
                if value != nested:
                    errors.append("nested gitlink transition differs from Git objects")
                if value["status"] != "unchanged":
                    derived.add(WLROOTS_ROOT)
                if value["status"] == "registered":
                    derived.add(".gitmodules")
            except (ValueError, RuntimeError) as error:
                errors.append(str(error))
    return derived, errors


def _entry_semantic_errors(entry, expected, trace, repo, artifact_root, lane="child"):
    source, target = entry.get("source_commit"), entry.get("target_commit")
    action = entry.get("action")
    content_action = entry.get("content_action", action)
    lane_data = expected["waylib_shared" if lane == "child" else "wlroots"]
    errors: List[str] = []
    if entry.get("classification") != expected.get("classification"):
        errors.append(f"evidence classification mismatch for {source}")
    if target != trace.get("target_commit") or action != trace.get("action") or content_action != trace.get("content_action"):
        errors.append(f"evidence differs from target trace for {source}")
    if entry.get("drop_paths") != lane_data["drop_paths"] or entry.get("drop_paths") != trace.get("drop_paths"):
        errors.append(f"evidence drop_paths differ from inventory/message for {source}")
    notes = entry.get("adaptation_notes")
    if notes != trace.get("adaptation_notes"):
        errors.append("adaptation notes differ from commit message")
    if action == "adapted" and (not isinstance(notes, list) or not any(isinstance(note, str) and note.strip().lower() != "none" for note in notes)):
        errors.append("adapted action requires substantive adaptation notes")
    actual = set(trace.get("changed_paths", []))
    nested = entry.get("nested_gitlink")
    derived, nested_errors = _derived_child_paths(entry, trace, repo, target, lane)
    errors.extend(nested_errors)
    extra = entry.get("structural_paths", [])
    if extra and (lane != "child" or nested is None or extra != ["CMakeLists.txt"] or content_action != "adapted"):
        errors.append("unauthorized child structural paths")
        extra = []
    paths = lane_target_paths(expected, lane) + (extra if isinstance(extra, list) else [])
    content = actual - derived
    unexpected = sorted(content - set(paths))
    errors.extend(f"{lane} path expansion for {source}: {path}" for path in unexpected)
    if not derived.issubset(actual):
        errors.append("derived gitlink/registration changes are missing")
    if content_action == "applied" and content != set(paths):
        errors.append(f"applied {lane} paths differ from inventory for {source}")
    if content_action == "adapted" and not content:
        errors.append(f"adapted action target has no content changes: {target}")
    if content_action in {"empty", "not-applicable"} and content:
        errors.append(f"empty action target contains changes: {target}")
    if content_action == "not-applicable" and (lane != "child" or paths or not derived):
        errors.append("not-applicable content action requires a derived-only child change")
    expected_action = "adapted" if ".gitmodules" in derived else "gitlink-only" if derived and not content else content_action
    if action != expected_action:
        errors.append("overall action differs from ordinary content and gitlink changes")
    adaptations = entry.get("adaptation_paths", [])
    if content_action == "adapted" and is_full_sha(target):
        errors.extend(adaptation_semantic_errors(repo, target, adaptations, paths, list(content), artifact_root, f"{lane} {source}"))
    elif adaptations not in (None, []):
        errors.append("non-adapted content has adaptation_paths")
    if isinstance(adaptations, list):
        markers = [{"kind": item.get("kind"), "path": item.get("path")} for item in adaptations if isinstance(item, dict)]
        if markers != trace.get("adaptation_paths", []):
            errors.append("adaptation paths differ from commit message")
    return errors


def _evidence_shape_errors(evidence: Mapping[str, Any], lane: str = "child") -> List[str]:
    errors: List[str] = []
    if evidence.get("schema_version") != 2:
        errors.append("waylib evidence schema_version must be 2")
    if evidence.get("kind") != (WAYLIB_EVIDENCE_KIND if lane == "child" else "treeland-unified-wlroots-evidence"):
        errors.append(f"waylib evidence kind must be {WAYLIB_EVIDENCE_KIND}")
    if not isinstance(evidence.get("entries"), list):
        errors.append("waylib evidence entries must be an array")
    return errors


def _trace_shape_errors(traces: Mapping[str, Any], lane: str = "child") -> List[str]:
    errors: List[str] = []
    if traces.get("schema_version") != 2:
        errors.append("waylib traces schema_version must be 2")
    if traces.get("kind") != f"treeland-unified-{'waylib' if lane == 'child' else 'wlroots'}-traces":
        errors.append("waylib traces kind is invalid")
    if traces.get("source_identity_verified") is not True:
        errors.append("waylib traces lack source identity verification")
    if not isinstance(traces.get("entries"), list):
        errors.append("waylib traces entries must be an array")
    return errors


def _mapping_entry_errors(
    entries: List[Any],
    expected: List[Mapping[str, Any]],
    trace_entries: List[Any],
    repo: Path,
    source_repo: Optional[Path],
    artifact_root: Path,
    lane: str = "child",
) -> List[str]:
    errors: List[str] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"evidence entry[{index}] must be an object")
            continue
        if index >= len(expected) or index >= len(trace_entries):
            continue
        trace = trace_entries[index]
        if not isinstance(trace, dict):
            errors.append(f"trace entry[{index}] must be an object")
            continue
        source = entry.get("source_commit")
        if source != expected[index].get("source_commit"):
            errors.append(f"evidence source order mismatch at index {index}")
        if entry.get("action") not in (CHILD_ACTIONS if lane == "child" else LANE_ACTIONS):
            errors.append(f"unsupported evidence action for {source}")
        errors.extend(
            _entry_semantic_errors(entry, expected[index], trace, repo, artifact_root, lane)
        )
        if source_repo is not None:
            errors.extend(
                _entry_artifact_errors(
                    entry, expected[index], source_repo, repo, artifact_root, lane
                )
            )
    return errors


def verify_waylib_sync(
    repo: Path,
    base: str,
    head: str,
    inventory: Mapping[str, Any],
    traces: Mapping[str, Any],
    evidence: Mapping[str, Any],
    artifact_root: Path,
    source_repo: Optional[Path] = None,
    lane: str = "child",
) -> Dict[str, Any]:
    """Verify child mapping, action semantics, paths, and artifact digests."""

    if lane not in {"child", "wlroots"}:
        raise ValueError("unsupported file lane")
    base_sha = resolve_commit(repo, base)
    head_sha = resolve_commit(repo, head)
    blockers = inventory_errors(inventory)
    if inventory.get("outcome") != "pass":
        blockers.append("inventory outcome must be pass")
    blockers.extend(_evidence_shape_errors(evidence, lane))
    blockers.extend(_trace_shape_errors(traces, lane))
    if source_repo is not None:
        from .traces import build_waylib_traces
        if traces != build_waylib_traces(repo, base_sha, head_sha, inventory, source_repo, lane):
            blockers.append("traces differ from immutable Git history")
    if source_repo is None:
        blockers.append("source repo is required for source-patch verification")
    if traces.get("outcome") != "pass":
        blockers.extend(traces.get("blocked_reasons", []))
    trace_range = traces.get("target_range", {})
    if trace_range != {"base": base_sha, "head": head_sha}:
        blockers.append("traces target_range differs from requested target range")
    expected = child_inventory_entries(inventory) if lane == "child" else [item for item in inventory["commits"] if item["wlroots"]["included"]]
    entries = evidence.get("entries", []) if isinstance(evidence.get("entries"), list) else []
    trace_entries = traces.get("entries", []) if isinstance(traces.get("entries"), list) else []
    if len(entries) != len(expected):
        blockers.append(f"evidence count mismatch: expected {len(expected)}, got {len(entries)}")
    blockers.extend(
        _mapping_entry_errors(
            entries, expected, trace_entries, repo, source_repo, artifact_root, lane
        )
    )
    blockers = stable_unique(blockers)
    return {
        "schema_version": 2,
        "kind": f"treeland-unified-{'waylib' if lane == 'child' else 'wlroots'}-verify",
        "target_range": {"base": base_sha, "head": head_sha},
        "inventory_sha256": canonical_json_sha256(inventory),
        "traces_sha256": canonical_json_sha256(traces),
        "evidence_sha256": canonical_json_sha256(evidence),
        "verified_entries": len(entries),
        "blocked_reasons": blockers,
        "outcome": "blocked" if blockers else "pass",
    }
