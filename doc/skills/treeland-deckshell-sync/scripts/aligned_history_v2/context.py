"""Filesystem inputs for one aligned-history v2 execution."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InputPaths:
    """Explicit repositories, frozen evidence, and generated-output roots."""

    workspace: Path
    atomic_root: Path
    repo: Path
    target_worktree: Path
    waylib_repo: Path
    protocol_repo: Path
    v1_manifest: Path
    v1_source_mapping: Path
    v1_rewrite_mapping: Path
    v1_object_result: Path
    v1_applied_verification: Path
    v1_product_manifest: Path
    v1_atomic_mapping: Path
    v1_history_contract: Path
    task8_evidence: Path
    task9_evidence: Path
    refs_before: Path
    build_environment: Path
    protocol_ledger: Path
    dependency_set: Path
    dependency_bundle: Path
    runtime_observations: Path
    protocol_lock: Path
    anchor_provenance: Path
    legacy_v2_candidate: Path
    legacy_v2_manifest: Path
    legacy_v2_mapping: Path
    bootstrap_transition_map: Path
    anchor_generation: Path
    input_lock: Path
    remediation_ledger: Path
    master_product_manifest: Path
    product_overlay_rules: Path
    adaptation_manifest: Path
    legacy_inventory: Path
    equivalence_evidence: Path
    waylib_sync_record: Path
    waylib_mapping_gate: Path
    plan: Path
    bundle_root: Path
    output_directory: Path
