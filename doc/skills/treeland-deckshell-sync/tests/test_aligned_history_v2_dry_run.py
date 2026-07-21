"""Tests for the aligned-history v2 no-object dry run."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aligned_history_v2.dry_run import audit_rendered_message


class AlignedHistoryV2DryRunTests(unittest.TestCase):
    def test_message_audit_proves_byte_stable_round_trip(self) -> None:
        message_input = {
            "schema": "waylib",
            "subject_body": "fix: converge dependency\n",
            "classification": "dependency-convergence",
            "action": "local-gitlink",
            "waylib_commit": "a" * 40,
        }

        audit = audit_rendered_message(message_input)

        self.assertEqual(audit["schema"], "waylib")
        self.assertEqual(len(audit["rendered_message_sha256"]), 64)
        self.assertTrue(audit["round_trip_equal"])


if __name__ == "__main__":
    unittest.main()
