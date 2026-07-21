"""No-object message and transition audit for aligned-history v2."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from .freeze_inputs import REWRITE_BASE, SHARED_ANCHOR
from .git_objects import git_object_id, parse_raw_commit, render_raw_commit
from .manifest import validate_input_manifest
from .message import parse_message, render_message
from .repository import GitRepository
from .remediation import validate_remediation_transitions
from .tree_transition import parse_raw_transition


FORBIDDEN_FINAL_KEYS = (
    b"Previous-Rewrite-Commit:",
    b"Legacy-DeckShell-Target:",
    b"Legacy-DeckShell-Commit:",
    b"Source-Ref:",
    b"Absorbed-DeckShell-Commit:",
    b"Derived-From-Commit:",
    b"Superseded-Source-Commit:",
    b"Excluded-Source-Commit:",
)


def audit_rendered_message(message_input: dict[str, Any]) -> dict[str, Any]:
    """Render, parse, and re-render a message byte-for-byte."""

    schema = str(message_input.get("schema"))
    rendered = render_message(message_input)
    parsed = parse_message(rendered, schema)
    rerendered = render_message(parsed)
    if rendered != rerendered:
        raise ValueError(f"message round-trip drift for schema {schema}")
    forbidden = [key.decode("ascii") for key in FORBIDDEN_FINAL_KEYS if key in rendered]
    if forbidden:
        raise ValueError(f"rendered message contains retired key: {forbidden}")
    return {
        "schema": schema,
        "rendered_message_sha256": hashlib.sha256(rendered).hexdigest(),
        "rendered_message_size": len(rendered),
        "round_trip_equal": True,
    }


def run_sequential_dry_run(
    repo_path: Path,
    manifest: dict[str, Any],
    remediation_ledger: dict[str, Any],
) -> dict[str, Any]:
    """Audit all messages/transitions and precompute the unchanged-tree prefix."""

    validate_input_manifest(manifest)
    validate_remediation_transitions(manifest, remediation_ledger)
    repo = GitRepository(repo_path)
    previous_projected = REWRITE_BASE
    records: list[dict[str, Any]] = []
    representatives: dict[str, dict[str, Any]] = {}
    prefix: list[dict[str, Any]] = []
    for entry in manifest["entries"]:
        index = int(entry["ordered_index"])
        commit = str(entry["expected_v1_commit"])
        raw_payload = repo.cat_file("commit", commit)
        raw = parse_raw_commit(raw_payload)
        if raw.parent != entry["expected_v1_parent"] or raw.tree != entry["expected_v1_tree"]:
            raise ValueError(f"raw commit identity drift at {index}")
        transition = repo.raw_transition(raw.parent, commit)
        transition_hash = hashlib.sha256(transition).hexdigest()
        if transition_hash != entry["expected_v1_delta_sha256"]:
            raise ValueError(f"tree transition hash drift at {index}")
        changed_paths = [change.path for change in parse_raw_transition(transition)]
        if changed_paths != entry["expected_v1_changed_paths"]:
            raise ValueError(f"tree transition path drift at {index}")
        record: dict[str, Any] = {
            "ordered_index": index,
            "expected_v1_commit": commit,
            "tree_transition": entry["tree_transition"],
            "v1_delta_sha256": transition_hash,
            "changed_paths": changed_paths,
        }
        if index == 1:
            if commit != SHARED_ANCHOR or git_object_id("commit", raw_payload) != commit:
                raise ValueError("corrected-v1 anchor raw object drift")
            if raw.parent != REWRITE_BASE:
                raise ValueError("corrected-v1 anchor parent drift")
        message_audit = audit_rendered_message(entry["message_inputs"])
        record.update(message_audit)
        if index <= 315:
            rendered = render_message(entry["message_inputs"])
            projected = render_raw_commit(
                raw,
                tree=entry["expected_v1_tree"],
                parent=previous_projected,
                message=rendered,
            )
            if index == 1 and projected.object_id == commit:
                raise ValueError("v2 rebuilt anchor reused the corrected-v1 object")
            record["projected_commit"] = projected.object_id
            record["projected_parent"] = previous_projected
            previous_projected = projected.object_id
        if entry["message_schema"] == "treeland":
            prefix.append(
                {
                    "ordered_index": index,
                    "normalized_treeland_commit": entry["message_inputs"]["source_commit"],
                    "projected_v2_target": record.get("projected_commit"),
                    "classification": entry["message_inputs"]["classification"],
                    "action": entry["message_inputs"]["action"],
                }
            )
        label = _representative_label(entry)
        if label and label not in representatives:
            representatives[label] = record
        records.append(record)
    _verify_dry_run_counts(records, prefix, representatives)
    return {
        "schema_version": 2,
        "workflow_mode": "commit-aligned-history-rewrite-v2",
        "outcome": "pass",
        "input_manifest_sha256": manifest["canonical_payload_sha256"],
        "entry_count": len(records),
        "rendered_count": len(records),
        "rebuilt_anchor_count": sum(
            record["tree_transition"] == "replay-rebuilt-anchor"
            for record in records
        ),
        "ordinary_transition_count": sum(
            record["tree_transition"] == "replay-v1-delta" for record in records
        ),
        "dependency_proven_transition_count": sum(
            record["tree_transition"]
            == "replay-dependency-proven-v1-delta"
            for record in records
        ),
        "remediated_transition_count": sum(
            record["tree_transition"] == "replay-remediated-v1-delta"
            for record in records
        ),
        "regeneration_plan_count": sum(
            record["tree_transition"] == "regenerate" for record in records
        ),
        "projected_prefix_end_index": 315,
        "projected_prefix_head": records[314]["projected_commit"],
        "treeland_target_projection_candidate": prefix,
        "representatives": representatives,
        "records": records,
    }


def _representative_label(entry: dict[str, Any]) -> str | None:
    message = entry["message_inputs"]
    if message.get("source_commit") == "fd7baaa323c4c23cf021c29704cf1bb3c89dc244":
        return "fd7baaa3-adapted-omitted"
    if entry["target_kind"] == "treeland-other" and message.get("action") == "applied":
        return "other-applied"
    if entry["target_kind"] == "treeland-mixed" and message.get("action") == "adapted":
        return "mixed-adapted"
    if entry["target_kind"] == "treeland-dependency-only":
        return "dependency-only"
    if entry["target_kind"] == "waylib-local":
        return "waylib-local"
    if entry["ordered_index"] == 307:
        return "adaptation-composite"
    return None


def _verify_dry_run_counts(
    records: list[dict[str, Any]],
    prefix: list[dict[str, Any]],
    representatives: dict[str, dict[str, Any]],
) -> None:
    if len(records) != 330 or len(prefix) != 298:
        raise ValueError("dry-run count gate failed")
    if any(item["projected_v2_target"] is None for item in prefix):
        raise ValueError("Treeland target prefix was not fully projected")
    expected = {
        "other-applied",
        "mixed-adapted",
        "dependency-only",
        "fd7baaa3-adapted-omitted",
        "waylib-local",
        "adaptation-composite",
    }
    if set(representatives) != expected:
        raise ValueError(f"representative proof set mismatch: {set(representatives)}")
