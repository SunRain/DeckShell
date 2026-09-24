"""独立本地修复的真实相邻提交及原来源映射保护。"""

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from three_repo_fixture import build_fixture
from support import commit_files, run
from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.git_ops import canonical_json_sha256, read_json
from unified_sync_lib.local_fixes import record_local_fix, local_fix_errors
from unified_sync_lib.parent_verify import verify_parent_sync
from unified_sync_lib.gitlink import verify_gitlink_consistency
from unified_sync_lib.traces import build_waylib_traces
from unified_sync_lib.evidence import verify_waylib_sync


class LocalFixTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.q, self.original, _, _, _ = build_fixture(Path(temporary.name))
        q = self.q
        self.root = q.artifact_root
        self.before = write_artifact(self.root, "fix/original.json", json.dumps(self.original).encode())
        self.approval = {
            "kind": "treeland-unified-local-fix-approval", "review_state": "approved",
            "authorization": "Explicit fixture repair approval", "id": "fixture-fix",
            "reason": "Independent repair without rewriting imported commits",
            "original_manifest_sha256": canonical_json_sha256(self.original),
            "refs_doc": self.original["identity"]["refs_doc"],
            "paths": {"child": ["waylib/server.cpp"], "parent": ["3rdparty/waylib-shared", "doc/fix.md"]},
        }
        path = q.child_worktree / "waylib/server.cpp"
        head = commit_files(q.child_worktree, {"waylib/server.cpp": path.read_text() + "// independent fix\n"}, "fix: local child")
        run(q.parent_worktree / "3rdparty/waylib-shared", "switch", "--detach", head)
        commit_files(q.parent_worktree, {"doc/fix.md": "Independent local repair\n"}, "fix: local parent")

    def record(self):
        q = self.q
        approval = write_artifact(self.root, "fix/approval.json", json.dumps(self.approval).encode())
        return record_local_fix(self.original, approval, self.before,
                                {"parent": q.parent_worktree, "child": q.child_worktree,
                                 "wlroots": q.wlroots_worktree}, self.root)

    def test_local_tail_preserves_source_mapping_and_passes_content_and_gitlinks(self):
        q, m = self.q, self.record()
        self.assertEqual(m["entries"], self.original["entries"])
        self.assertEqual(local_fix_errors(m, self.root), [])
        pe, ce = read_json(q.parent_evidence_path), read_json(q.waylib_evidence_path)
        for evidence in (pe, ce):
            evidence["local_fix"] = m["local_fix"]
        parent = verify_parent_sync(q.source_repo, q.parent_worktree, q.parent_base, m["final_parent_head"],
                                    q.inventory, m, pe, self.root)
        traces = build_waylib_traces(q.child_worktree, q.child_base, m["final_child_head"],
                                     q.inventory, q.source_repo, evidence=ce, artifact_root=self.root)
        child = verify_waylib_sync(q.child_worktree, q.child_base, m["final_child_head"],
                                   q.inventory, traces, ce, self.root, q.source_repo)
        links = verify_gitlink_consistency(q.parent_worktree, q.child_worktree, q.parent_base, q.child_base, m)
        for result in (parent, child, links):
            self.assertEqual(result["outcome"], "pass", result)

    def test_modified_original_source_mapping_is_rejected(self):
        manifest = self.record()
        manifest["entries"][0]["source_commit"] = "a" * 40
        self.assertIn("changed frozen replay", " ".join(local_fix_errors(manifest, self.root)))

    def test_unapproved_extra_file_is_rejected(self):
        self.approval["paths"]["parent"] = ["3rdparty/waylib-shared"]
        with self.assertRaisesRegex(ValueError, "differs from approved paths"):
            self.record()

    def test_changed_protected_public_contract_is_rejected(self):
        path = self.q.child_worktree / "waylib/CMakeLists.txt"
        commit_files(self.q.child_worktree, {"waylib/CMakeLists.txt": path.read_text() + "add_library(NewPublic INTERFACE)\n"}, "additional unapproved fix")
        with self.assertRaisesRegex(ValueError, "exactly one adjacent"):
            self.record()
