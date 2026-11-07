"""Relative public references are enforced before replay mutates Git."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from protocol_fixture import IMPLEMENTATION, UPSTREAM_XML, XML, ProtocolFixture
from support import commit_files, run
from unified_sync_lib.history_messages import mapped_message
from unified_sync_lib.replay import ReplayBlocked, run_replay


class RelativeRefsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.fixture = ProtocolFixture(Path(temporary.name))
        f = self.fixture
        commit_files(f.source, {IMPLEMENTATION: "// renamed_v1 implementation\n"}, "rename")
        commit_files(f.protocol, {UPSTREAM_XML: XML.replace("manager_v1", "renamed_v1")}, "wire")

    def test_unsafe_refs_fail_before_journal_or_commits(self):
        values = ["/home/person/plan.md", "../plan.md", "C:/work/plan.md", "C:\\work\\plan.md",
                  "./plan.md", "plan//a.md", "~user/plan.md", "", "plan.md\nTrailer: injected"]
        for index, value in enumerate(values):
            with self.subTest(value=value):
                request = self.fixture.request(str(index))
                request.refs_doc = value
                with self.assertRaisesRegex(ReplayBlocked, "refs-doc"):
                    run_replay(request)
                self.assertFalse(request.journal_path.exists())
                for lane in ("parent", "child"):
                    self.assertEqual(run(getattr(request, lane + "_worktree"), "rev-parse", "HEAD"),
                                     getattr(request, lane + "_base"))

    def test_ordinary_and_companion_commits_share_the_portable_reference(self):
        request = self.fixture.request()
        request.refs_doc = ".helloagents/plans/example/plan.md"
        manifest = run_replay(request)
        for lane in ("parent", "child"):
            repo = getattr(request, lane + "_worktree")
            commits = run(repo, "rev-list", getattr(request, lane + "_base") + "..HEAD").split()
            self.assertIn(manifest["protocol_update"][lane]["head"], commits)
            for sha in commits:
                refs = [line for line in run(repo, "show", "-s", "--format=%B", sha).splitlines()
                        if line.startswith("Refs:")]
                self.assertEqual(refs, ["Refs: " + request.refs_doc])

    def test_message_mapping_preserves_source_and_unrelated_text(self):
        old, new = "a" * 40, "b" * 40
        raw = (f"subject {old}\n\nOriginal treeland commit:\n    Refs: /old/plan.md\n"
               f"    - commit: {old}\n\n- Includes waylib-shared update to {old}.\n"
               f"- commit: {old}\nRefs: /old/plan.md\nTreeland-Commit: {old}\n").encode()
        result = mapped_message(raw, "/old/plan.md", "plans/plan.md", {old: new}).decode()
        self.assertIn(f"    - commit: {old}", result)
        self.assertIn(f"subject {old}", result)
        self.assertIn(f"Treeland-Commit: {old}", result)
        self.assertIn(f"\n- commit: {new}\nRefs: plans/plan.md", result)
        with self.assertRaisesRegex(ValueError, "unique"):
            mapped_message(raw + b"Refs: duplicate\n", "/old/plan.md", "plans/plan.md", {})


if __name__ == "__main__":
    unittest.main()
