"""Fail-closed tests for the independent v2 compile-atomic trust boundary."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aligned_history_v2.atomic_contract import validate_atomic_replay_contract
from aligned_history_v2.atomic_verifiers.protocol_policy import assign_protocol_owner


def _canonical_sha256(value: object) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _product_entry(object_id: str) -> dict[str, str]:
    return {
        "mode": "100644",
        "kind": "blob",
        "object_id": object_id,
        "path": "compositor/src/seat/helper.cpp",
    }


def _protocol_component() -> dict[str, object]:
    return {
        "protocol_component_id": "protocol:one",
        "source_commit": "a" * 40,
        "source_path": "xml/example.xml",
        "target_path": "protocols/compositor/xml/example.xml",
        "owner_index": 2,
        "consumer_paths": ["compositor/src/example.cpp"],
        "generated_signatures": ["request:ready"],
        "local_overlay_components": [],
        "after_blob": "b" * 40,
        "result_blob": "b" * 40,
    }


def _dependency_component() -> dict[str, object]:
    return {
        "component_id": "dependency:one",
        "kind": "definition",
        "owner_index": 2,
        "target_owner_index": 2,
        "source_indices": [2],
        "payload": {"path": "compositor/src/example.cpp"},
        "bundle_id": "bundle:one",
    }


def _valid_contract() -> dict[str, object]:
    protocol = _protocol_component()
    dependency = _dependency_component()
    product = [_product_entry("c" * 40)]
    return {
        "replay_pairs": [
            {
                "ordered_index": 1,
                "transition_type": "replay-rebuilt-anchor",
                "source_delta_sha256": "1" * 64,
                "v1_delta_sha256": "1" * 64,
                "v2_delta_sha256": "1" * 64,
            },
            {
                "ordered_index": 2,
                "transition_type": "replay-dependency-proven-v1-delta",
                "source_delta_sha256": "2" * 64,
                "v1_delta_sha256": "2" * 64,
                "v2_delta_sha256": "2" * 64,
            },
        ],
        "nodes": [
            {
                "owner_index": 1,
                "files": {"CMakeLists.txt": "project(Example)\n"},
                "generated_signatures": {},
                "consumed_signatures": {},
                "bundle_members": [],
            },
            {
                "owner_index": 2,
                "files": {"CMakeLists.txt": "project(Example)\n"},
                "generated_signatures": {"example": ["request:ready"]},
                "consumed_signatures": {"example": ["request:ready"]},
                "bundle_members": [{"kind": "definition", "owner_index": 2}],
            },
        ],
        "protocol": {
            "ledger": {
                "components": [copy.deepcopy(protocol)],
                "fixed_mappings": {},
                "convergence_owner_index": 2,
            },
            "source_components": [protocol],
            "ancestry_order": ["a" * 40],
            "valid_owner_indexes": [1, 2],
        },
        "dependency_set": {
            "ledger": {
                "ordinary_classifications": [
                    {
                        "ordered_index": 2,
                        "entry_id": "entry:two",
                        "classification": "independent",
                        "edge_ids": [],
                        "reason_kinds": [],
                        "gitlink_before": "d" * 40,
                        "gitlink_after": "d" * 40,
                    }
                ],
                "dependency_sensitive_indices": [],
                "synthesis_audit": [],
                "graph": {"edges": []},
            },
            "ordinary_candidates": [
                {
                    "ordered_index": 2,
                    "entry_id": "entry:two",
                    "gitlink_before": "d" * 40,
                    "gitlink_after": "d" * 40,
                }
            ],
            "remediation_targets": [],
            "carry_forward_entry_ids": [],
            "protocol_components": [],
        },
        "dependency_bundle": {
            "ledger": {
                "components": [copy.deepcopy(dependency)],
                "bundles": [
                    {
                        "bundle_id": "bundle:one",
                        "owner_index": 2,
                        "component_ids": ["dependency:one"],
                        "forbidden_early_members": [
                            {
                                "component_id": "dependency:one",
                                "before_owner_index": 2,
                            }
                        ],
                        "preconditions": [
                            {
                                "kind": "definition",
                                "component_ids": ["dependency:one"],
                            }
                        ],
                        "proof_nodes": [2],
                    }
                ],
            },
            "expected_components": [dependency],
            "valid_owner_indexes": [1, 2],
        },
        "product": {
            "master_entries": product,
            "v1_entries": copy.deepcopy(product),
            "v2_entries": copy.deepcopy(product),
            "master_entries_sha256": _canonical_sha256(product),
        },
    }


class AlignedHistoryV2AtomicContractTests(unittest.TestCase):
    def test_independent_policy_owns_wine_state_at_first_consumer(self) -> None:
        owner = assign_protocol_owner(
            "1a55a4fc7ae13285e7b6f809720c02c1b1175f88",
            "xml/treeland-wine-window-state-unstable-v1.xml",
            anchor_absorbed=False,
        )

        self.assertEqual(owner.owner_index, 81)

    def test_v1_and_v2_identically_wrong_replay_is_rejected(self) -> None:
        contract = _valid_contract()
        pair = contract["replay_pairs"][1]
        pair["v1_delta_sha256"] = "9" * 64
        pair["v2_delta_sha256"] = "9" * 64

        with self.assertRaisesRegex(ValueError, "shared v1/v2 replay drift"):
            validate_atomic_replay_contract(contract)

    def test_protocol_ledger_tampering_is_rejected(self) -> None:
        contract = _valid_contract()
        component = contract["protocol"]["ledger"]["components"][0]
        component["result_blob"] = "e" * 40

        with self.assertRaisesRegex(ValueError, "protocol transition ledger"):
            validate_atomic_replay_contract(contract)

    def test_component_specific_protocol_owner_drift_is_rejected(self) -> None:
        contract = _valid_contract()
        component = contract["protocol"]["ledger"]["components"][0]
        contract["protocol"]["ledger"]["fixed_component_mappings"] = [
            {
                "source_commit": component["source_commit"],
                "source_path": component["source_path"],
                "owner_index": 1,
            }
        ]

        with self.assertRaisesRegex(ValueError, "protocol transition ledger"):
            validate_atomic_replay_contract(contract)

    def test_dependency_bundle_missing_member_is_rejected(self) -> None:
        contract = _valid_contract()
        contract["dependency_bundle"]["ledger"]["components"] = []

        with self.assertRaisesRegex(ValueError, "dependency bundle ledger"):
            validate_atomic_replay_contract(contract)

    def test_dependency_sensitive_classification_drift_is_rejected(self) -> None:
        contract = _valid_contract()
        row = contract["dependency_set"]["ledger"]["ordinary_classifications"][0]
        row["classification"] = "dependency-sensitive"

        with self.assertRaisesRegex(ValueError, "dependency-sensitive set"):
            validate_atomic_replay_contract(contract)

    def test_anchor_external_protocol_lookup_is_rejected(self) -> None:
        contract = _valid_contract()
        contract["nodes"][0]["files"]["CMakeLists.txt"] = (
            "find_package(TreelandProtocols REQUIRED)\n"
        )

        with self.assertRaisesRegex(ValueError, "external protocol lookup"):
            validate_atomic_replay_contract(contract)

    def test_xml_signature_misalignment_is_rejected(self) -> None:
        contract = _valid_contract()
        contract["nodes"][1]["consumed_signatures"]["example"] = [
            "request:not-generated"
        ]

        with self.assertRaisesRegex(ValueError, "generated signature mismatch"):
            validate_atomic_replay_contract(contract)

    def test_master_oracle_drift_is_rejected_before_three_way_compare(self) -> None:
        contract = _valid_contract()
        contract["product"]["master_entries_sha256"] = "f" * 64

        with self.assertRaisesRegex(ValueError, "master oracle drift"):
            validate_atomic_replay_contract(contract)

    def test_valid_contract_returns_independently_recomputed_counts(self) -> None:
        report = validate_atomic_replay_contract(_valid_contract())

        self.assertEqual(report["replay_pair_count"], 2)
        self.assertEqual(report["node_count"], 2)
        self.assertEqual(report["protocol_component_count"], 1)
        self.assertEqual(report["dependency_component_count"], 1)


if __name__ == "__main__":
    unittest.main()
