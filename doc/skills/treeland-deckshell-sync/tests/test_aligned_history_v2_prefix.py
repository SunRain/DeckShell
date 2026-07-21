"""Tests for the sealed index-303 Treeland target prefix."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aligned_history_v2.prefix import seal_treeland_prefix


class AlignedHistoryV2PrefixTests(unittest.TestCase):
    def test_prefix_contains_only_final_treeland_identity_and_v2_targets(self) -> None:
        indices = [index for index in range(2, 304) if index not in {13, 31, 77, 201}]
        classifications = ["other"] * 233 + ["mixed"] * 29 + ["dependency-only"] * 36
        entries = []
        targets = {}
        for sequence, (index, classification) in enumerate(
            zip(indices, classifications, strict=True), 1
        ):
            source = f"{sequence:040x}"
            target = f"{sequence + 500:040x}"
            entries.append(
                {
                    "ordered_index": index,
                    "target_kind": f"treeland-{classification}",
                    "message_schema": "treeland",
                    "message_inputs": {
                        "schema": "treeland",
                        "source_commit": source,
                        "subject_body": f"subject {sequence}\n",
                        "classification": classification,
                        "action": (
                            "dependency-gitlink"
                            if classification == "dependency-only"
                            else "applied"
                        ),
                    },
                    "source_objects": {
                        "normalized_treeland_commit": source,
                        "legacy_deckshell_target": "f" * 40,
                    },
                }
            )
            targets[index] = target

        prefix = seal_treeland_prefix(entries, targets)

        self.assertEqual(prefix["sealed_at_ordered_index"], 303)
        self.assertEqual(prefix["entry_count"], 298)
        self.assertEqual(prefix["entries"][0]["treeland_remote"], "treeland")
        self.assertEqual(
            prefix["entries"][0]["treeland_tracking_ref"],
            "refs/remotes/treeland/master",
        )
        serialized = str(prefix)
        self.assertNotIn("legacy_deckshell_target", serialized)
        self.assertNotIn("expected_v1_commit", serialized)


if __name__ == "__main__":
    unittest.main()
