from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from protocol_fixture import IMPLEMENTATION, UPSTREAM_XML, XML, ProtocolFixture
from support import commit_files, run
from unified_sync_lib.evidence import verify_waylib_sync
from unified_sync_lib.git_ops import read_json
from unified_sync_lib.gitlink import verify_gitlink_consistency
from unified_sync_lib.parent_verify import verify_parent_sync
from unified_sync_lib.protocol_pairing import verify_pairing
from unified_sync_lib.protocol_sources import PARENT_XML_PATH, PROVENANCE_PATH, XML_PATH
from unified_sync_lib.replay import ReplayBlocked, run_replay
from unified_sync_lib.traces import build_waylib_traces


class ProtocolReplayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.fixture = ProtocolFixture(Path(self.temp.name))

    def tearDown(self):
        self.temp.cleanup()

    def verify_lanes(self, request, manifest):
        f = self.fixture
        child_evidence = read_json(request.waylib_evidence_path)
        traces = build_waylib_traces(request.child_worktree, f.child_base, manifest["final_child_head"],
                                    request.inventory, f.source, evidence=child_evidence,
                                    artifact_root=request.artifact_root)
        reports = [traces,
                   verify_waylib_sync(request.child_worktree, f.child_base, manifest["final_child_head"],
                                      request.inventory, traces, child_evidence, request.artifact_root, f.source),
                   verify_parent_sync(f.source, request.parent_worktree, f.parent_base,
                                      manifest["final_parent_head"], request.inventory, manifest,
                                      read_json(request.parent_evidence_path), request.artifact_root),
                   verify_gitlink_consistency(request.parent_worktree, request.child_worktree,
                                              f.parent_base, f.child_base, manifest)]
        for report in reports:
            self.assertEqual(report["outcome"], "pass", report)

    def test_xml_only_companion_updates_both_copies_and_provenance(self):
        f = self.fixture
        changed = XML.replace("references", "exported references")
        head = commit_files(f.protocol, {UPSTREAM_XML: changed}, "protocol update")
        request = f.request()
        manifest = run_replay(request)
        self.assertEqual(manifest["entries"], [])
        self.assertEqual((request.child_worktree / XML_PATH).read_text(), changed)
        self.assertEqual((request.parent_worktree / PARENT_XML_PATH).read_text(), changed)
        pair = json.loads((request.child_worktree / PROVENANCE_PATH).read_text())
        self.assertEqual(pair["protocol"]["commit"], head)
        self.verify_lanes(request, manifest)

    def test_both_sources_are_replayed_before_the_protocol_companion(self):
        f = self.fixture
        commit_files(f.source, {IMPLEMENTATION: "// renamed_v1 implementation\n"}, "rename implementation")
        commit_files(f.protocol, {UPSTREAM_XML: XML.replace("manager_v1", "renamed_v1")}, "rename wire")
        request = f.request()
        manifest = run_replay(request)
        self.assertEqual(len(manifest["entries"]), 1)
        self.assertEqual(manifest["protocol_update"]["child"]["base"], manifest["entries"][0]["child"]["commit"])
        self.verify_lanes(request, manifest)

    def test_missing_review_or_real_validation_never_accepts_a_candidate(self):
        f = self.fixture
        request = f.request()
        manifest = run_replay(request)
        result = verify_pairing(request.inventory, manifest, {}, {"entries": []}, request.artifact_root)
        self.assertEqual(result["status"], "尚未适配")
        self.assertEqual(result["last_accepted_pair"], f.pair)
        self.assertTrue(result["affected_clients"])
        self.assertIn("validation", " ".join(result["blocked_reasons"]))
        self.assertEqual(run(f.parent, "rev-parse", "HEAD"), f.parent_base)
        self.assertEqual(run(f.child, "rev-parse", "HEAD"), f.child_base)

    def test_resume_after_protocol_child_keeps_the_single_companion_commit(self):
        f = self.fixture
        request = f.request()

        def stop(stage, _source, _commit):
            if stage == "protocol-child":
                raise RuntimeError("test interruption after child checkpoint")

        with self.assertRaises(ReplayBlocked):
            run_replay(request, stage_hook=stop)
        child = run(request.child_worktree, "rev-parse", "HEAD")
        manifest = run_replay(request, resume=True)
        self.assertEqual(manifest["final_child_head"], child)
        self.verify_lanes(request, manifest)


if __name__ == "__main__":
    unittest.main()
