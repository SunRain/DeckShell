"""Tests for aligned-history v2 input artifact boundaries."""

from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aligned_history_v2.artifacts import canonical_payload_sha256
from aligned_history_v2.input_messages import build_treeland_message_input
from aligned_history_v2.manifest import validate_input_manifest
from aligned_history_v2.message import render_message


def entry(index: int, transition: str) -> dict[str, object]:
    return {
        "ordered_index": index,
        "target_kind": "deckshell-tool-passthrough" if index == 1 else "treeland-other",
        "expected_v1_commit": str(index) * 40,
        "expected_v1_parent": str(index - 1) * 40,
        "expected_v1_tree": "a" * 40,
        "expected_v2_parent": "rewrite-base" if index == 1 else f"entry:{index - 1}",
        "message_schema": "passthrough" if index == 1 else "treeland",
        "expected_v1_changed_paths": [],
        "authorized_v2_delta_paths": [],
        "tree_transition": transition,
        "remediation_proof": None,
        "gitlink_before": None,
        "gitlink_after": None,
        "source_objects": {},
        "message_inputs": {},
        "message_inputs_sha256": hashlib.sha256(b"{}\n").hexdigest(),
        "regeneration_job": None,
        "test_action": "static-check",
        "post_assertions": [],
    }


class AlignedHistoryV2ManifestTests(unittest.TestCase):
    def test_first_entry_replays_rebuilt_anchor_and_dependency_type_is_valid(self) -> None:
        manifest = {
            "schema_version": 2,
            "workflow_mode": "commit-aligned-history-rewrite-v2",
            "status": "candidate",
            "entries": [
                entry(1, "replay-rebuilt-anchor"),
                entry(2, "replay-dependency-proven-v1-delta"),
            ],
        }

        counts = validate_input_manifest(manifest, expected_count=2)

        self.assertEqual(counts["deckshell-tool-passthrough"], 1)
        self.assertEqual(counts["treeland-other"], 1)

    def test_input_manifest_rejects_preview_output_fields(self) -> None:
        manifest = {
            "schema_version": 2,
            "workflow_mode": "commit-aligned-history-rewrite-v2",
            "status": "candidate",
            "entries": [
                entry(1, "replay-rebuilt-anchor"),
                entry(2, "replay-v1-delta"),
            ],
        }
        manifest["entries"][1]["new_commit"] = "f" * 40

        with self.assertRaisesRegex(ValueError, "output-only field"):
            validate_input_manifest(manifest, expected_count=2)

    def test_canonical_payload_hash_ignores_only_its_self_description(self) -> None:
        payload = {"value": 1, "canonical_payload_sha256": "0" * 64}

        first = canonical_payload_sha256(payload)
        payload["canonical_payload_sha256"] = "f" * 64

        self.assertEqual(canonical_payload_sha256(payload), first)
        payload["value"] = 2
        self.assertNotEqual(canonical_payload_sha256(payload), first)

    def test_legacy_treeland_message_is_upgraded_without_copying_old_target_identity(self) -> None:
        source = "1" * 40
        legacy_message = (
            "fix: mapped change\n\n"
            f"(cherry picked from commit {source})\n\n"
            "[treeland-sync] classification: mixed\n"
            "[treeland-sync] action: applied\n"
            "[treeland-sync] drop files:\n- waylib/a.cpp\n"
            "[treeland-sync] path mapping:\n- src/a.cpp -> compositor/src/a.cpp\n"
            "[treeland-sync] adaptation paths:\n- none\n"
            "[treeland-sync] adaptation notes:\n- none\n\n"
            f"Treeland-Commit: {source}\n"
        )
        v1_entry = {
            "target_kind": "treeland-mixed",
            "normalized_treeland_commit": source,
            "legacy_treeland_commit": "2" * 40,
            "treeland_patch_id": "3" * 40,
            "legacy_deckshell_target": "4" * 40,
            "waylib_target": "5" * 40,
            "metadata": {"message": legacy_message},
        }

        message_input = build_treeland_message_input(v1_entry, [])
        rendered = render_message(message_input)

        self.assertIn(b"Treeland-Remote: treeland\n", rendered)
        self.assertIn(b"Legacy-Treeland-Commit: " + b"2" * 40, rendered)
        self.assertNotIn(b"Legacy-DeckShell", rendered)

    def test_dependency_only_message_lists_every_source_path(self) -> None:
        source = "6" * 40
        v1_entry = {
            "target_kind": "treeland-dependency-only",
            "normalized_treeland_commit": source,
            "legacy_treeland_commit": None,
            "treeland_patch_id": None,
            "legacy_deckshell_target": None,
            "waylib_target": "7" * 40,
            "metadata": {"message": "fix: dependency only\n"},
        }
        changed_paths = ["qwlroots/CMakeLists.txt", "waylib/src/example.cpp"]

        message_input = build_treeland_message_input(v1_entry, changed_paths)

        self.assertEqual(message_input["drop_files"], changed_paths)
        self.assertEqual(message_input["path_mapping"], ["none"])
        self.assertEqual(message_input["adaptation_paths"], ["none"])
        self.assertIn("7" * 40, message_input["adaptation_notes"][0])


if __name__ == "__main__":
    unittest.main()
