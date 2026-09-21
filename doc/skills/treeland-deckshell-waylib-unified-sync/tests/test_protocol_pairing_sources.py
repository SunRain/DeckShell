from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from protocol_fixture import IMPLEMENTATION, UPSTREAM_XML, XML, ProtocolFixture
from support import commit_files, run
from unified_sync_lib.protocol_sources import inspect_pairing


class ProtocolSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.fixture = ProtocolFixture(Path(self.temp.name))

    def tearDown(self):
        self.temp.cleanup()

    def inspect(self, **selection):
        f = self.fixture
        return inspect_pairing(f.inventory(), f.source, f.child, f.child_base,
                               {**f.selection(), **selection})

    def test_no_changes_still_checks_both_explicit_ranges(self):
        result = self.inspect()
        self.assertEqual(result["outcome"], "pass", result)
        self.assertEqual(result["status"], "inspected-not-accepted")
        self.assertEqual(result["implementation"]["changes"], [])
        self.assertEqual(result["protocol"]["changes"], [])

    def test_xml_only_change_is_not_gated_by_treeland_inventory(self):
        f = self.fixture
        commit_files(f.protocol, {UPSTREAM_XML: XML.replace("Token-based references.", "Tokens must be revoked.")}, "semantic update")
        result = self.inspect()
        self.assertEqual(result["outcome"], "pass", result)
        self.assertEqual(result["implementation"]["changes"], [])
        self.assertTrue(result["protocol"]["descriptions_changed"])
        self.assertFalse(result["protocol"]["wire_changed"])

    def test_implementation_only_change_is_checked(self):
        f = self.fixture
        commit_files(f.source, {IMPLEMENTATION: "// manager_v1 changed behavior\n"}, "implementation update")
        result = self.inspect()
        self.assertEqual(result["outcome"], "pass", result)
        self.assertTrue(result["implementation"]["changes"])
        self.assertFalse(result["protocol"]["changes"])

    def test_both_changes_and_constant_interface_version_are_detected(self):
        f = self.fixture
        commit_files(f.source, {IMPLEMENTATION: "// renamed_v1 implementation\n"}, "implementation update")
        commit_files(f.protocol, {UPSTREAM_XML: XML.replace("manager_v1", "renamed_v1")}, "wire update")
        result = self.inspect()
        self.assertTrue(result["implementation"]["changes"])
        self.assertTrue(result["protocol"]["wire_changed"])
        self.assertIn('version="1"', result["protocol"]["changes"][0]["diff"])

    def test_move_and_rename_follow_the_actual_history(self):
        f = self.fixture
        (f.protocol / "wine").mkdir()
        run(f.protocol, "mv", UPSTREAM_XML, "wine/renamed.xml")
        run(f.protocol, "commit", "-m", "move protocol")
        result = self.inspect()
        self.assertEqual(result["outcome"], "pass", result)
        self.assertEqual(result["protocol"]["head_path"], "wine/renamed.xml")
        self.assertFalse(result["protocol"]["wire_changed"])

    def test_deleted_xml_is_not_misreported_as_no_change(self):
        f = self.fixture
        # Only the isolated fixture's index loses the file; no checkout is deleted.
        run(f.protocol, "update-index", "--force-remove", UPSTREAM_XML)
        run(f.protocol, "commit", "-m", "delete protocol")
        result = self.inspect()
        self.assertEqual(result["status"], "尚未适配")
        self.assertIn("removed", result["blocked_reasons"][0])
        self.assertEqual(result["last_accepted_pair"], f.pair)

    def test_reverted_intermediate_changes_remain_visible(self):
        f = self.fixture
        commit_files(f.protocol, {UPSTREAM_XML: XML.replace("manager_v1", "renamed_v1")}, "change")
        commit_files(f.protocol, {UPSTREAM_XML: XML}, "revert")
        result = self.inspect()
        self.assertEqual(len(result["protocol"]["changes"]), 2)
        self.assertFalse(result["protocol"]["wire_changed"])

    def test_missing_source_reports_stage_target_and_last_pair(self):
        result = self.inspect(repo=str(self.fixture.root / "absent"))
        self.assertEqual(result["status"], "尚未适配")
        self.assertEqual(result["failure_stage"], "source-inspection")
        self.assertEqual(result["last_accepted_pair"], self.fixture.pair)
        self.assertIn("absent", result["blocked_reasons"][0])

    def test_incomplete_history_is_not_an_incompatibility_verdict(self):
        f = self.fixture
        (f.protocol / ".git/shallow").write_text(f.protocol_base + "\n", encoding="utf-8")
        result = self.inspect()
        self.assertEqual(result["outcome"], "blocked")
        self.assertIn("history is shallow", result["blocked_reasons"][0])
        self.assertNotIn("incompatible", result["blocked_reasons"][0])

    def test_skipping_the_last_accepted_protocol_range_is_rejected(self):
        f = self.fixture
        head = commit_files(f.protocol, {UPSTREAM_XML: XML.replace("references", "handles")}, "change")
        result = self.inspect(base=head)
        self.assertEqual(result["outcome"], "blocked")
        self.assertIn("last accepted", result["blocked_reasons"][0])


if __name__ == "__main__":
    unittest.main()
