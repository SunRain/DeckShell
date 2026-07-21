"""Tests for commit-aligned-history-rewrite-v2 message contracts."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aligned_history_v2.message import parse_message, render_message


class AlignedHistoryV2MessageTests(unittest.TestCase):
    def test_treeland_message_round_trips_with_fixed_source_identity(self) -> None:
        source = "a" * 40
        message_input = {
            "schema": "treeland",
            "subject_body": "fix: keep the compositor contract\n\nDetailed source body.\n",
            "source_commit": source,
            "classification": "mixed",
            "action": "adapted",
            "drop_files": ["waylib/src/example.cpp"],
            "path_mapping": ["src/example.cpp -> compositor/src/example.cpp"],
            "adaptation_paths": ["modified: compositor/src/example.cpp"],
            "adaptation_notes": ["Use the DeckShell-owned lifecycle."],
            "legacy_treeland_commit": "b" * 40,
            "treeland_patch_id": "c" * 40,
            "waylib_commit": "d" * 40,
        }

        rendered = render_message(message_input)
        parsed = parse_message(rendered, "treeland")

        self.assertEqual(render_message(parsed), rendered)
        self.assertEqual(rendered.count(b"(cherry picked from commit "), 1)
        self.assertIn(b"Treeland-Remote: treeland\n", rendered)
        self.assertIn(b"Treeland-Remote-Branch: master\n", rendered)
        self.assertIn(
            b"Treeland-Tracking-Ref: refs/remotes/treeland/master\n", rendered
        )
        self.assertTrue(rendered.endswith(("WaylibShared-Commit: " + "d" * 40 + "\n").encode()))

    def test_waylib_local_message_round_trips_without_treeland_identity(self) -> None:
        message_input = {
            "schema": "waylib",
            "subject_body": "fix: preserve the dependency checkpoint\n",
            "classification": "dependency-structure",
            "action": "local-gitlink",
            "waylib_commit": "e" * 40,
            "absorbed_waylib_commit": "f" * 40,
        }

        rendered = render_message(message_input)
        parsed = parse_message(rendered, "waylib")

        self.assertEqual(render_message(parsed), rendered)
        self.assertNotIn(b"cherry picked", rendered)
        self.assertNotIn(b"Treeland-", rendered)

    def test_adaptation_message_round_trips_without_legacy_source_trailers(self) -> None:
        message_input = {
            "schema": "adaptation",
            "subject_body": "docs(sync): regenerate v2 adaptation records\n",
            "classification": "regenerate",
            "action": "regenerate",
            "paths": ["doc/treeland-sync/adaptations/"],
            "notes": ["Render records from the frozen Treeland target prefix."],
            "derivation": "regenerate",
        }

        rendered = render_message(message_input)
        parsed = parse_message(rendered, "adaptation")

        self.assertEqual(render_message(parsed), rendered)
        self.assertNotIn(b"cherry picked", rendered)
        self.assertNotIn(b"Legacy-DeckShell", rendered)
        self.assertTrue(rendered.endswith(b"Derivation: regenerate\n"))


if __name__ == "__main__":
    unittest.main()
