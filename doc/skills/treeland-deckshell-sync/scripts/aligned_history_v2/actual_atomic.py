"""Git-object-backed compile-atomic verification for v2 history."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .artifacts import canonical_bytes
from .atomic_bindings import (
    is_ancestor,
    verify_gitlink_bindings,
    verify_protocol_bindings,
    verify_protocol_source_policy,
    verify_remediation_bindings,
    verify_waylib_bindings,
)
from .atomic_bundle_bindings import verify_bundle_materialization
from .atomic_contract import validate_atomic_replay_contract
from .atomic_rebuild import read_sidecar_json, rebuild_atomic_ledgers
from .context import InputPaths
from .product_oracle import (
    build_product_entries,
    path_is_excluded,
    project_master_product_entries,
    validate_master_manifest,
    validate_overlay_rules,
)
from .repository import GitRepository
from .tree_transition import parse_raw_transition


def projected_transition_sha256(
    repo: GitRepository,
    parent: str,
    commit: str,
    rules: dict[str, Any],
) -> str:
    """Hash one raw transition after removing only approved overlay paths."""

    projection = [
        {
            "old_mode": change.old_mode,
            "new_mode": change.new_mode,
            "old_object": change.old_object,
            "new_object": change.new_object,
            "status": change.status,
            "path": change.path,
        }
        for change in parse_raw_transition(repo.raw_transition(parent, commit))
        if not path_is_excluded(change.path, rules)
    ]
    return hashlib.sha256(canonical_bytes(projection)).hexdigest()


def verify_compile_atomic_history(
    paths: InputPaths,
    repo: GitRepository,
    manifest: dict[str, Any],
    v2_records: list[dict[str, Any]],
) -> dict[str, Any]:
    """Rebuild every authority and bind it to actual v1/v2 objects."""

    if len(manifest.get("entries", ())) != 330 or len(v2_records) != 330:
        raise ValueError("compile-atomic verification requires 330 history nodes")
    rebuilt = rebuild_atomic_ledgers(paths, repo)
    v1_mapping = read_sidecar_json(paths.v1_atomic_mapping, "artifact_sha256")
    v1_records = v1_mapping.get("records", ())
    if len(v1_records) != 330:
        raise ValueError("corrected-v1 atomic mapping requires 330 records")
    rules = read_sidecar_json(paths.product_overlay_rules, "artifact_sha256")
    master = read_sidecar_json(paths.master_product_manifest, "artifact_sha256")
    validate_overlay_rules(
        rules,
        expected_artifact_sha256=manifest["frozen_inputs"]["overlay_rules_sha256"],
    )
    validate_master_manifest(
        master,
        rules,
        expected_artifact_sha256=manifest["frozen_inputs"][
            "master_product_manifest_sha256"
        ],
    )
    replay_pairs = _replay_pairs(
        repo, manifest["entries"], list(v1_records), v2_records, rules
    )
    _verify_candidate_classification(manifest, rebuilt["dependency"])
    product = _product_contract(repo, manifest, v2_records, master, rules)
    v2_by_index = {
        int(record["ordered_index"]): record for record in v2_records
    }
    protocol_repo = GitRepository(paths.protocol_repo)
    contract = {
        "replay_pairs": replay_pairs,
        "nodes": [
            {
                "owner_index": index,
                "files": {},
                "generated_signatures": {},
                "consumed_signatures": {},
                "bundle_members": [],
            }
            for index in range(1, 331)
        ],
        "protocol": {
            "ledger": rebuilt["protocol"],
            "source_components": rebuilt["protocol_source_components"],
            "ancestry_order": [
                item["commit"] for item in rebuilt["protocol_lock"]["history"]
            ],
            "valid_owner_indexes": list(range(1, 331)),
            "is_ancestor": lambda older, newer: is_ancestor(
                protocol_repo, older, newer
            ),
            "read_blob": lambda object_id: protocol_repo.cat_file(
                "blob", object_id
            ),
        },
        "dependency_set": {
            "ledger": rebuilt["dependency"],
            "ordinary_candidates": _ordinary_candidates(
                rebuilt["legacy_manifest"]
            ),
            "remediation_targets": rebuilt["dependency"][
                "remediation_target_indices"
            ],
            "carry_forward_entry_ids": rebuilt["dependency"][
                "carry_forward_entry_ids"
            ],
            "protocol_components": rebuilt["protocol"]["components"],
        },
        "dependency_bundle": {
            "ledger": rebuilt["bundle"],
            "expected_components": rebuilt["rebuilt_bundle"]["components"],
            "valid_owner_indexes": list(range(1, 331)),
            "is_ancestor": lambda older, newer: is_ancestor(
                repo,
                str(v2_by_index[older]["new_commit"]),
                str(v2_by_index[newer]["new_commit"]),
            ),
        },
        "product": product,
    }
    structural = validate_atomic_replay_contract(contract)
    bindings = {
        "v1_protocol": verify_protocol_bindings(
            repo, list(v1_records), rebuilt["protocol"]
        ),
        "v2_protocol": verify_protocol_bindings(
            repo, v2_records, rebuilt["protocol"]
        ),
        "v2_gitlinks": verify_gitlink_bindings(
            repo, v2_records, manifest["entries"]
        ),
        "v2_waylib": verify_waylib_bindings(
            repo,
            GitRepository(paths.waylib_repo),
            v2_records,
            rebuilt["bundle"],
        ),
        "v2_bundles": verify_bundle_materialization(
            repo,
            v2_records,
            rebuilt["bundle"],
            rebuilt["protocol"],
            v1_records=list(v1_records),
        ),
        "v2_protocol_source": verify_protocol_source_policy(repo, v2_records),
        "v2_remediation": verify_remediation_bindings(
            repo,
            list(v1_records),
            v2_records,
            rebuilt["remediation"],
            rebuilt["bundle"],
        ),
    }
    return {
        "schema_version": 1,
        "kind": "corrected-v2-independent-compile-atomic-verification",
        "outcome": "pass",
        **structural,
        "replay_pair_count": 330,
        "replay_pairs_sha256": hashlib.sha256(
            canonical_bytes(replay_pairs)
        ).hexdigest(),
        "dependency_sensitive_count": len(
            rebuilt["dependency"]["dependency_sensitive_indices"]
        ),
        "bundle_count": rebuilt["bundle"]["bundle_count"],
        "protocol_recomputed_sha256": rebuilt["protocol_recomputed_sha256"],
        "dependency_recomputed_sha256": rebuilt[
            "dependency_recomputed_sha256"
        ],
        "bundle_recomputed_sha256": rebuilt["bundle_recomputed_sha256"],
        "product_entry_count": len(product["master_entries"]),
        "product_entries_sha256": product["master_entries_sha256"],
        "bindings": bindings,
    }


def _replay_pairs(
    repo: GitRepository,
    entries: list[dict[str, Any]],
    v1_records: list[dict[str, Any]],
    v2_records: list[dict[str, Any]],
    rules: dict[str, Any],
) -> list[dict[str, Any]]:
    pairs = []
    for entry, v1, v2 in zip(entries, v1_records, v2_records, strict=True):
        index = int(entry["ordered_index"])
        if (
            int(v1["ordered_index"]) != index
            or int(v2["ordered_index"]) != index
            or v1["commit"] != entry["expected_v1_commit"]
            or v2["expected_v1_commit"] != entry["expected_v1_commit"]
        ):
            raise ValueError(f"v1/v2 replay identity drift at {index}")
        v1_raw = repo.raw_transition(str(v1["parent"]), str(v1["commit"]))
        v2_raw = repo.raw_transition(str(v2["new_parent"]), str(v2["new_commit"]))
        v1_raw_hash = hashlib.sha256(v1_raw).hexdigest()
        v2_raw_hash = hashlib.sha256(v2_raw).hexdigest()
        if v1_raw_hash != entry["expected_v1_delta_sha256"]:
            raise ValueError(f"corrected-v1 raw transition drift at {index}")
        if (
            v1_raw_hash != v2["v1_delta_sha256"]
            or v2_raw_hash != v2["v2_delta_sha256"]
        ):
            raise ValueError(f"v2 mapping transition hash drift at {index}")
        if entry["tree_transition"] != "regenerate" and v1_raw != v2_raw:
            raise ValueError(f"replayed raw transition differs at {index}")
        v1_product = projected_transition_sha256(
            repo, str(v1["parent"]), str(v1["commit"]), rules
        )
        v2_product = projected_transition_sha256(
            repo, str(v2["new_parent"]), str(v2["new_commit"]), rules
        )
        pairs.append(
            {
                "ordered_index": index,
                "transition_type": entry["tree_transition"],
                "source_delta_sha256": v1_product,
                "v1_delta_sha256": v1_product,
                "v2_delta_sha256": v2_product,
            }
        )
    return pairs


def _verify_candidate_classification(
    manifest: dict[str, Any], dependency: dict[str, Any]
) -> None:
    actual = [
        int(entry["ordered_index"])
        for entry in manifest["entries"]
        if entry["tree_transition"] == "replay-dependency-proven-v1-delta"
    ]
    expected = list(dependency["dependency_sensitive_indices"])
    declared = manifest["compile_atomic_contract"][
        "dependency_sensitive_indices"
    ]
    if actual != expected or declared != expected or len(actual) != 129:
        raise ValueError("candidate dependency-sensitive classification drift")


def _product_contract(
    repo: GitRepository,
    manifest: dict[str, Any],
    v2_records: list[dict[str, Any]],
    master: dict[str, Any],
    rules: dict[str, Any],
) -> dict[str, Any]:
    projected, _ = project_master_product_entries(repo, master["entries"])
    v1 = build_product_entries(
        repo, manifest["frozen_inputs"]["v1_head_tree"], rules
    )
    v2 = build_product_entries(repo, v2_records[-1]["new_tree"], rules)
    return {
        "master_entries": projected,
        "v1_entries": v1,
        "v2_entries": v2,
        "master_entries_sha256": _compact_sha256(projected),
    }


def _ordinary_candidates(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        entry
        for entry in manifest["entries"]
        if entry["ordered_index"] != 1
        and entry.get("tree_transition") != "regenerate"
        and entry.get("remediation_proof") is None
    ]


def _compact_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
