"""Fail-closed tests for corrected-v2 remediation transitions."""

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

from aligned_history_v2.artifacts import canonical_bytes
from aligned_history_v2.remediation import (
    REMEDIATED_INDICES,
    validate_remediation_ledger,
    validate_remediation_transitions,
)


def _ledger() -> dict[str, object]:
    targets = [
        {
            "target_index": index,
            "source_commit": f"{position:040x}",
            "legacy_target_commit": f"{position + 20:040x}",
            "waylib_gitlink": f"{position + 40:040x}",
            "component_ids": [f"component-{position}"],
            "paths": [f"compositor/path-{position}.cpp"],
        }
        for position, index in enumerate(REMEDIATED_INDICES, 1)
    ]
    ledger: dict[str, object] = {
        "schema_version": 2,
        "components": [
            {"component_id": target["component_ids"][0]} for target in targets
        ],
        "targets": targets,
    }
    ledger["canonical_sha256"] = hashlib.sha256(
        canonical_bytes(ledger)
    ).hexdigest()
    return ledger


def _manifest(ledger: dict[str, object]) -> dict[str, object]:
    targets = {
        target["target_index"]: target for target in ledger["targets"]
    }
    excluded = {1, 316, 329, 330, *REMEDIATED_INDICES}
    dependency_indices = set(
        index for index in range(2, 331) if index not in excluded
    )
    dependency_indices = set(sorted(dependency_indices)[:129])
    entries = []
    for index in range(1, 331):
        transition = "replay-v1-delta"
        proof = None
        if index == 1:
            transition = "replay-rebuilt-anchor"
        elif index in {316, 329, 330}:
            transition = "regenerate"
        elif index in REMEDIATED_INDICES:
            transition = "replay-remediated-v1-delta"
            target = targets[index]
            proof = {
                "ledger_sha256": ledger["canonical_sha256"],
                "target_index": index,
                "source_commit": target["source_commit"],
                "legacy_target_commit": target["legacy_target_commit"],
                "waylib_gitlink": target["waylib_gitlink"],
                "component_ids": target["component_ids"],
                "paths": target["paths"],
            }
        elif index in dependency_indices:
            transition = "replay-dependency-proven-v1-delta"
        entries.append(
            {
                "ordered_index": index,
                "tree_transition": transition,
                "remediation_proof": proof,
            }
        )
    return {"entries": entries}


class AlignedHistoryV2RemediationTests(unittest.TestCase):
    def test_ledger_component_tampering_is_rejected(self) -> None:
        ledger = _ledger()
        ledger["components"][0]["component_id"] = "tampered"

        with self.assertRaisesRegex(ValueError, "canonical hash drift"):
            validate_remediation_ledger(ledger)

    def test_remediated_component_ids_must_match_ledger(self) -> None:
        ledger = _ledger()
        manifest = _manifest(ledger)
        manifest["entries"][REMEDIATED_INDICES[0] - 1][
            "remediation_proof"
        ]["component_ids"] = ["wrong-component"]

        with self.assertRaisesRegex(ValueError, "component IDs"):
            validate_remediation_transitions(manifest, ledger)

    def test_transition_distribution_is_exactly_1_186_129_11_3(self) -> None:
        ledger = _ledger()
        manifest = _manifest(ledger)
        manifest["entries"][200]["tree_transition"] = "regenerate"

        with self.assertRaisesRegex(ValueError, "transition distribution"):
            validate_remediation_transitions(manifest, ledger)

    def test_remediated_indices_are_not_interchangeable(self) -> None:
        ledger = _ledger()
        manifest = _manifest(ledger)
        first = REMEDIATED_INDICES[0]
        manifest["entries"][first - 1]["tree_transition"] = "replay-v1-delta"
        manifest["entries"][199][
            "tree_transition"
        ] = "replay-remediated-v1-delta"

        with self.assertRaisesRegex(ValueError, "remediated indices"):
            validate_remediation_transitions(manifest, ledger)

    def test_canonical_ledger_round_trip_passes(self) -> None:
        ledger = _ledger()
        result = validate_remediation_ledger(
            json.loads(json.dumps(ledger))
        )

        self.assertEqual(result["target_count"], 11)
        self.assertEqual(result["component_count"], 11)


if __name__ == "__main__":
    unittest.main()
