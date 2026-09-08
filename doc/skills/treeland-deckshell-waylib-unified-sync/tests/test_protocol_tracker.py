from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from unified_sync_lib.inventory import build_unified_inventory
from unified_sync_lib.git_ops import canonical_json_sha256
from unified_sync_lib.policy import load_policy
from unified_sync_lib.protocols import (
    build_parent_protocol_context,
    track_protocol_candidates,
)
from protocol_tracker import main as protocol_main

from support import commit_files, init_repo, write_policy


class ProtocolTrackerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.source = init_repo(self.root / "source")
        self.protocols = init_repo(self.root / "protocols")
        self.source_base = commit_files(
            self.source,
            {"README.local": "base\n"},
            "base",
            timestamp="2026-01-10T00:00:00+00:00",
        )
        self.protocol_base = commit_files(
            self.protocols,
            {"README": "base\n"},
            "base",
            timestamp="2026-01-01T00:00:00+00:00",
        )
        policy_path = write_policy(self.root / "policy.md")
        self.policy_path = policy_path
        self.policy = load_policy(policy_path)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def inventory(self, content: str = "<protocol name=\"demo\"/>\n"):
        source_sha = commit_files(
            self.source,
            {"protocols/compositor/xml/demo.xml": content},
            "protocol update",
            timestamp="2026-01-10T00:00:00+00:00",
        )
        inventory = build_unified_inventory(
            self.source,
            self.source_base,
            source_sha,
            self.policy,
            self.policy_path,
            set(),
        )
        return source_sha, inventory

    def track(self, inventory, head: str, threshold: float = 0.9):
        return track_protocol_candidates(
            self.source,
            inventory,
            self.protocols,
            head,
            threshold=threshold,
            days_before=30,
            days_after=7,
        )

    def test_reports_no_candidate_without_blocking_content_sync(self) -> None:
        _source_sha, inventory = self.inventory()
        head = commit_files(
            self.protocols,
            {"xml/unrelated.xml": "entirely different words\n"},
            "unrelated",
            timestamp="2026-01-09T00:00:00+00:00",
        )

        result = self.track(inventory, head)

        self.assertEqual(result["outcome"], "pass")
        self.assertTrue(result["advisory"])
        self.assertEqual(result["entries"][0]["match_status"], "no-candidate")
        self.assertEqual(result["entries"][0]["candidates"], [])

    def test_pure_xml_rename_is_not_comparable_even_at_zero_threshold(self):
        content = '<protocol name="unchanged"/>\n'
        base = commit_files(self.source, {"protocols/old.xml": content}, "source XML baseline")
        head = commit_files(self.source, {"protocols/old.xml": None, "protocols/new.xml": content}, "source rename")
        commit_files(self.protocols, {"xml/old.xml": content}, "protocol XML baseline")
        protocol_head = commit_files(self.protocols, {"xml/old.xml": None, "xml/new.xml": content}, "protocol rename")
        inventory = build_unified_inventory(self.source, base, head, self.policy, self.policy_path, set())
        result = self.track(inventory, protocol_head, threshold=0.0)
        self.assertEqual(result["outcome"], "pass")
        entry = result["entries"][0]
        self.assertEqual(entry["match_status"], "not-comparable")
        self.assertEqual(entry["candidates"], [])
        self.assertTrue(entry["not_comparable"])
        self.assertTrue(all(row["similarity"] is None for row in entry["not_comparable"]))

    def test_reports_one_candidate_without_claiming_confirmation(self) -> None:
        source_sha, inventory = self.inventory()
        candidate = commit_files(
            self.protocols,
            {"xml/demo.xml": "<protocol name=\"demo\"/>\n"},
            "matching protocol",
            timestamp="2026-01-10T01:00:00+00:00",
        )

        result = self.track(inventory, candidate)

        entry = result["entries"][0]
        self.assertEqual(entry["source_commit"], source_sha)
        self.assertEqual(entry["match_status"], "single-candidate")
        self.assertEqual(entry["candidates"][0]["commit"], candidate)
        self.assertNotIn("confirmed_commit", entry)

    def test_tracks_root_owned_treeland_protocol_in_current_category_layout(self) -> None:
        content = "<protocol name=\"keyboard_state\"/>\n"
        source_sha = commit_files(
            self.source,
            {"protocols/kde-keystate.xml": content},
            "source protocol",
            timestamp="2026-01-10T00:00:00+00:00",
        )
        inventory = build_unified_inventory(
            self.source,
            self.source_base,
            source_sha,
            self.policy,
            self.policy_path,
            set(),
        )
        candidate = commit_files(
            self.protocols,
            {"dde/treeland-keyboard-state-notify-unstable-v1.xml": content},
            "matching categorized protocol",
            timestamp="2026-01-10T01:00:00+00:00",
        )

        result = self.track(inventory, candidate)

        self.assertEqual(
            inventory["commits"][0]["protocol_source_paths"],
            ["protocols/kde-keystate.xml"],
        )
        entry = result["entries"][0]
        self.assertEqual(entry["source_commit"], source_sha)
        self.assertEqual(entry["match_status"], "single-candidate")
        self.assertEqual(entry["candidates"][0]["commit"], candidate)
        self.assertEqual(
            entry["candidates"][0]["paths"],
            ["dde/treeland-keyboard-state-notify-unstable-v1.xml"],
        )
        self.assertNotIn("confirmed_commit", entry)

    def test_tracks_actual_parent_protocol_target_without_source_protocol(self) -> None:
        content = "<protocol name=\"virtual_output\"/>\n"
        source_sha = commit_files(
            self.source,
            {"src/app.cpp": "use virtual output\n"},
            "consume protocol",
            timestamp="2026-01-10T00:00:00+00:00",
        )
        inventory = build_unified_inventory(
            self.source,
            self.source_base,
            source_sha,
            self.policy,
            self.policy_path,
            set(),
        )
        parent = init_repo(self.root / "parent")
        commit_files(parent, {"README": "base\n"}, "parent base")
        parent_commit = commit_files(
            parent,
            {"protocols/compositor/xml/treeland-virtual-output-manager-v1.xml": content},
            "adapt protocol",
            timestamp="2026-01-10T00:30:00+00:00",
        )
        manifest = {
            "schema_version": 2,
            "kind": "treeland-unified-sync-manifest",
            "outcome": "pass",
            "entries": [
                {
                    "source_commit": source_sha,
                    "parent": {"commit": parent_commit},
                }
            ],
        }
        candidate = commit_files(
            self.protocols,
            {"dde/treeland-virtual-output-manager-v1.xml": content},
            "matching current protocol",
            timestamp="2026-01-10T00:15:00+00:00",
        )

        context = build_parent_protocol_context(parent, manifest)
        result = track_protocol_candidates(
            self.source,
            inventory,
            self.protocols,
            candidate,
            threshold=0.9,
            parent_context=context,
        )

        entry = result["entries"][0]
        self.assertEqual(entry["trigger_sources"], ["parent-target"])
        self.assertEqual(
            entry["target_paths"],
            ["protocols/compositor/xml/treeland-virtual-output-manager-v1.xml"],
        )
        self.assertEqual(entry["match_status"], "single-candidate")
        self.assertEqual(entry["candidates"][0]["commit"], candidate)

    def test_preserves_multiple_candidates_as_deterministic_ambiguity(self) -> None:
        _source_sha, inventory = self.inventory()
        farther = commit_files(
            self.protocols,
            {"xml/first.xml": "<protocol name=\"demo\"/>\n"},
            "first match",
            timestamp="2026-01-08T00:00:00+00:00",
        )
        nearer = commit_files(
            self.protocols,
            {"xml/second.xml": "<protocol name=\"demo\"/>\n"},
            "second match",
            timestamp="2026-01-10T00:30:00+00:00",
        )

        result = self.track(inventory, nearer)

        entry = result["entries"][0]
        self.assertEqual(entry["match_status"], "ambiguous-candidates")
        self.assertEqual(
            [item["commit"] for item in entry["candidates"]],
            [nearer, farther],
        )
        self.assertEqual(result["outcome"], "pass")

    def test_accepts_protocol_root_commit_as_candidate(self) -> None:
        _source_sha, inventory = self.inventory()
        root_repo = init_repo(self.root / "root-protocols")
        candidate = commit_files(
            root_repo,
            {"xml/demo.xml": "<protocol name=\"demo\"/>\n"},
            "root protocol",
            timestamp="2026-01-10T00:30:00+00:00",
        )

        result = track_protocol_candidates(
            self.source,
            inventory,
            root_repo,
            candidate,
            threshold=0.9,
            days_before=30,
            days_after=7,
        )

        self.assertEqual(result["entries"][0]["match_status"], "single-candidate")
        self.assertEqual(result["entries"][0]["candidates"][0]["commit"], candidate)

    def test_invalid_parameters_fail_even_when_tracking_is_not_triggered(self) -> None:
        head = commit_files(self.source, {"src/a.cpp": "a\n"}, "non protocol")
        inventory = build_unified_inventory(
            self.source,
            self.source_base,
            head,
            self.policy,
            self.policy_path,
            set(),
        )
        inventory_path = self.root / "inventory.json"
        output_path = self.root / "protocol-output.json"
        inventory_path.write_text(json.dumps(inventory), encoding="utf-8")

        with contextlib.redirect_stderr(io.StringIO()):
            exit_code = protocol_main(
                [
                    "--inventory",
                    str(inventory_path),
                    "--threshold",
                    "1.1",
                    "--output",
                    str(output_path),
                ]
            )

        payload = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(exit_code, 1)
        self.assertEqual(payload["outcome"], "fail")
        self.assertIn("between 0 and 1", payload["errors"][0])

    def test_cli_binds_manifest_and_uses_actual_parent_protocol_diff(self) -> None:
        content = "<protocol name=\"output\"/>\n"
        source_sha = commit_files(
            self.source,
            {"src/output.cpp": "consume output\n"},
            "consume output",
            timestamp="2026-01-10T00:00:00+00:00",
        )
        inventory = build_unified_inventory(
            self.source,
            self.source_base,
            source_sha,
            self.policy,
            self.policy_path,
            set(),
        )
        parent = init_repo(self.root / "cli-parent")
        commit_files(parent, {"README": "base\n"}, "base")
        parent_commit = commit_files(
            parent,
            {"protocols/compositor/xml/treeland-output-manager-v1.xml": content},
            "adapt output protocol",
            timestamp="2026-01-10T00:20:00+00:00",
        )
        manifest = {
            "schema_version": 2,
            "kind": "treeland-unified-sync-manifest",
            "outcome": "pass",
            "entries": [
                {"source_commit": source_sha, "parent": {"commit": parent_commit}}
            ],
        }
        candidate = commit_files(
            self.protocols,
            {"public/treeland-output-manager-v1.xml": content},
            "publish output protocol",
            timestamp="2026-01-10T00:10:00+00:00",
        )
        inventory_path = self.root / "cli-inventory.json"
        manifest_path = self.root / "cli-manifest.json"
        output_path = self.root / "cli-output.json"
        inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        exit_code = protocol_main(
            [
                "--source-repo",
                str(self.source),
                "--parent-repo",
                str(parent),
                "--manifest",
                str(manifest_path),
                "--inventory",
                str(inventory_path),
                "--protocol-repo",
                str(self.protocols),
                "--protocol-head",
                candidate,
                "--threshold",
                "0.9",
                "--output",
                str(output_path),
            ]
        )

        payload = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["manifest_sha256"], canonical_json_sha256(manifest))
        self.assertEqual(payload["entries"][0]["match_status"], "single-candidate")


if __name__ == "__main__":
    unittest.main()
