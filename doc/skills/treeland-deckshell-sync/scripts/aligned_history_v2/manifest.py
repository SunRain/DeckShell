"""Input-manifest validation for commit-aligned-history-rewrite-v2."""

from __future__ import annotations

import re
from typing import Any

from .artifacts import canonical_bytes
from .remediation import REMEDIATED_INDICES


SHA1_PATTERN = re.compile(r"[0-9a-f]{40}\Z")
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
OUTPUT_ONLY_FIELDS = {
    "new_commit",
    "new_tree",
    "new_parent",
    "actual_v2_changed_paths",
    "inherited_overlay_paths",
    "rendered_message_sha256",
    "raw_commit_sha256",
    "verification",
}
REQUIRED_ENTRY_FIELDS = {
    "ordered_index",
    "target_kind",
    "expected_v1_commit",
    "expected_v1_parent",
    "expected_v1_tree",
    "expected_v2_parent",
    "message_schema",
    "expected_v1_changed_paths",
    "authorized_v2_delta_paths",
    "tree_transition",
    "remediation_proof",
    "gitlink_before",
    "gitlink_after",
    "source_objects",
    "message_inputs",
    "message_inputs_sha256",
    "regeneration_job",
    "test_action",
    "post_assertions",
}
TRANSITIONS = {
    "replay-rebuilt-anchor",
    "replay-v1-delta",
    "replay-dependency-proven-v1-delta",
    "replay-remediated-v1-delta",
    "regenerate",
}


def validate_input_manifest(
    manifest: dict[str, Any], *, expected_count: int = 330
) -> dict[str, int]:
    """Validate the immutable input-only boundary and return type counts."""

    if manifest.get("schema_version") != 2:
        raise ValueError("input manifest schema_version must be 2")
    if manifest.get("workflow_mode") != "commit-aligned-history-rewrite-v2":
        raise ValueError("input manifest workflow_mode mismatch")
    if manifest.get("status") not in {"candidate", "frozen-input-ready-for-v2-dry-run"}:
        raise ValueError("input manifest status is invalid")
    entries = manifest.get("entries")
    if not isinstance(entries, list) or len(entries) != expected_count:
        actual = len(entries) if isinstance(entries, list) else None
        raise ValueError(f"input manifest entry count mismatch: {actual}")
    counts: dict[str, int] = {}
    regenerate_indices: list[int] = []
    remediated_indices: list[int] = []
    transition_counts: dict[str, int] = {}
    for position, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            raise ValueError(f"input manifest entry {position} is not an object")
        output_fields = sorted(OUTPUT_ONLY_FIELDS & set(entry))
        if output_fields:
            raise ValueError(
                f"entry {position} contains output-only field: {', '.join(output_fields)}"
            )
        missing = sorted(REQUIRED_ENTRY_FIELDS - set(entry))
        if missing:
            raise ValueError(f"entry {position} lacks fields: {', '.join(missing)}")
        if entry["ordered_index"] != position:
            raise ValueError(f"entry order mismatch at {position}")
        for key in ("expected_v1_commit", "expected_v1_parent", "expected_v1_tree"):
            _require_sha(entry[key], f"entry {position} {key}")
        transition = entry["tree_transition"]
        if transition not in TRANSITIONS:
            raise ValueError(f"entry {position} has invalid tree transition")
        if position == 1 and transition != "replay-rebuilt-anchor":
            raise ValueError("first entry must replay the rebuilt anchor")
        if position > 1 and transition == "replay-rebuilt-anchor":
            raise ValueError("only the first entry may replay the rebuilt anchor")
        if transition == "regenerate":
            regenerate_indices.append(position)
            if not isinstance(entry["regeneration_job"], dict):
                raise ValueError(f"entry {position} lacks regeneration job")
        elif entry["regeneration_job"] is not None:
            raise ValueError(f"entry {position} unexpectedly has a regeneration job")
        if transition == "replay-remediated-v1-delta":
            remediated_indices.append(position)
            if not isinstance(entry["remediation_proof"], dict):
                raise ValueError(f"entry {position} lacks remediation proof")
        elif entry["remediation_proof"] is not None:
            raise ValueError(f"entry {position} unexpectedly has remediation proof")
        transition_counts[transition] = transition_counts.get(transition, 0) + 1
        for key in ("expected_v1_changed_paths", "authorized_v2_delta_paths", "post_assertions"):
            if not isinstance(entry[key], list) or len(entry[key]) != len(set(entry[key])):
                raise ValueError(f"entry {position} has invalid {key}")
        message_hash = entry["message_inputs_sha256"]
        if SHA256_PATTERN.fullmatch(str(message_hash)) is None:
            raise ValueError(f"entry {position} has invalid message input hash")
        expected_message_hash = _sha256(canonical_bytes(entry["message_inputs"]))
        if message_hash != expected_message_hash:
            raise ValueError(f"entry {position} message input hash mismatch")
        kind = str(entry["target_kind"])
        counts[kind] = counts.get(kind, 0) + 1
    if expected_count == 330 and regenerate_indices != [316, 329, 330]:
        raise ValueError(f"regeneration indices mismatch: {regenerate_indices}")
    if expected_count == 330:
        _validate_correction_contract(
            manifest, transition_counts, remediated_indices
        )
    return counts


def _validate_correction_contract(
    manifest: dict[str, Any],
    transition_counts: dict[str, int],
    remediated_indices: list[int],
) -> None:
    expected_counts = {
        "replay-rebuilt-anchor": 1,
        "replay-v1-delta": 186,
        "replay-dependency-proven-v1-delta": 129,
        "replay-remediated-v1-delta": 11,
        "regenerate": 3,
    }
    if transition_counts != expected_counts:
        raise ValueError(f"transition distribution mismatch: {transition_counts}")
    if tuple(remediated_indices) != REMEDIATED_INDICES:
        raise ValueError(f"remediated indices mismatch: {remediated_indices}")
    contract = manifest.get("remediation_contract")
    if not isinstance(contract, dict):
        raise ValueError("input manifest lacks remediation contract")
    if contract.get("target_indices") != list(REMEDIATED_INDICES):
        raise ValueError("remediation contract indices drift")
    if contract.get("target_count") != len(REMEDIATED_INDICES):
        raise ValueError("remediation contract count drift")
    frozen = manifest.get("frozen_inputs")
    if not isinstance(frozen, dict):
        raise ValueError("input manifest lacks frozen inputs")
    if contract.get("ledger_sha256") != frozen.get("remediation_ledger_sha256"):
        raise ValueError("remediation contract ledger binding drift")
    _validate_dependency_classification(manifest, frozen)
    oracle = manifest.get("product_oracle_contract")
    if not isinstance(oracle, dict):
        raise ValueError("input manifest lacks product oracle contract")
    expected_oracle = {
        "master_commit": frozen.get("master_commit"),
        "master_tree": frozen.get("master_tree"),
        "overlay_rules_sha256": frozen.get("overlay_rules_sha256"),
        "master_product_manifest_sha256": frozen.get(
            "master_product_manifest_sha256"
        ),
    }
    if oracle != expected_oracle:
        raise ValueError("product oracle contract binding drift")


def _validate_dependency_classification(
    manifest: dict[str, Any], frozen: dict[str, Any]
) -> None:
    expected = frozen.get("dependency_sensitive_indices")
    if not isinstance(expected, list) or len(expected) != 129:
        raise ValueError("frozen dependency-sensitive index set drift")
    actual = [
        entry["ordered_index"]
        for entry in manifest["entries"]
        if entry["tree_transition"]
        == "replay-dependency-proven-v1-delta"
    ]
    if actual != expected:
        raise ValueError("v2 dependency-sensitive classification drift")
    contract = manifest.get("compile_atomic_contract")
    if not isinstance(contract, dict):
        raise ValueError("input manifest lacks compile-atomic contract")
    expected_binding = {
        "protocol_ledger_sha256": frozen.get("protocol_ledger_sha256"),
        "dependency_set_sha256": frozen.get("dependency_set_sha256"),
        "dependency_bundle_sha256": frozen.get("dependency_bundle_sha256"),
        "dependency_sensitive_indices": expected,
    }
    if contract != expected_binding:
        raise ValueError("compile-atomic contract binding drift")


def _sha256(payload: bytes) -> str:
    import hashlib

    return hashlib.sha256(payload).hexdigest()


def _require_sha(value: Any, label: str) -> None:
    if not isinstance(value, str) or SHA1_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{label} must be a full lowercase SHA-1")
