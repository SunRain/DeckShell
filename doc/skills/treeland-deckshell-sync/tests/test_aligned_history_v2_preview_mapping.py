"""Tests for complete aligned-history v2 output mapping gates."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aligned_history_v2.preview_mapping import finalize_output_mapping


class AlignedHistoryV2PreviewMappingTests(unittest.TestCase):
    def test_mapping_requires_linear_chain_and_equal_replayed_deltas(self) -> None:
        manifest, records = self._fixture()

        mapping = finalize_output_mapping(
            manifest,
            records,
            treeland_prefix_sha256="a" * 64,
            tool_bundle_sha256="b" * 64,
            product_manifest_sha256="c" * 64,
            final_gitlink="d" * 40,
        )

        self.assertEqual(mapping["entry_count"], 330)
        self.assertEqual(mapping["head"], records[-1]["new_commit"])
        self.assertEqual(mapping["counts"]["rebuilt_anchor"], 1)
        self.assertEqual(mapping["counts"]["ordinary_transitions"], 186)
        self.assertEqual(mapping["counts"]["dependency_proven_transitions"], 129)
        self.assertEqual(mapping["counts"]["remediated_transitions"], 11)
        self.assertEqual(mapping["counts"]["regeneration_transitions"], 3)

        records[100]["v2_delta_sha256"] = "e" * 64
        with self.assertRaisesRegex(ValueError, "replayed transition delta drift"):
            finalize_output_mapping(
                manifest,
                records,
                treeland_prefix_sha256="a" * 64,
                tool_bundle_sha256="b" * 64,
                product_manifest_sha256="c" * 64,
                final_gitlink="d" * 40,
            )

    @staticmethod
    def _fixture() -> tuple[dict[str, object], list[dict[str, object]]]:
        entries = []
        records = []
        previous_new = f"{900:040x}"
        remediated = {133, 146, 148, 159, 174, 180, 194, 231, 233, 278, 284}
        regeneration = {316, 329, 330}
        dependency = set(
            index
            for index in range(2, 331)
            if index not in remediated | regeneration
        )
        dependency = set(sorted(dependency)[:129])
        for index in range(1, 331):
            old = f"{index:040x}"
            new = f"{index + 1000:040x}"
            transition = (
                "replay-rebuilt-anchor"
                if index == 1
                else "regenerate"
                if index in regeneration
                else "replay-remediated-v1-delta"
                if index in remediated
                else "replay-dependency-proven-v1-delta"
                if index in dependency
                else "replay-v1-delta"
            )
            entries.append(
                {
                    "ordered_index": index,
                    "expected_v1_commit": old,
                    "tree_transition": transition,
                }
            )
            records.append(
                {
                    "ordered_index": index,
                    "expected_v1_commit": old,
                    "new_commit": new,
                    "new_parent": previous_new,
                    "new_tree": f"{index + 2000:040x}",
                    "v1_delta_sha256": "1" * 64,
                    "v2_delta_sha256": "2" * 64
                    if transition == "regenerate"
                    else "1" * 64,
                    "actual_v2_changed_paths": [],
                    "inherited_overlay_paths": [],
                    "verification": "pass",
                }
            )
            previous_new = new
        manifest = {
            "canonical_payload_sha256": "f" * 64,
            "frozen_inputs": {"rewrite_base": f"{900:040x}"},
            "entries": entries,
        }
        return manifest, records


if __name__ == "__main__":
    unittest.main()
