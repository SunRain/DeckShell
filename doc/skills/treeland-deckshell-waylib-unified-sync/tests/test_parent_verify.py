from __future__ import annotations

import copy
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from unified_sync_lib.git_ops import read_json
from unified_sync_lib.inventory import build_unified_inventory
from unified_sync_lib.parent_verify import verify_parent_sync
from unified_sync_lib.policy import load_policy
from unified_sync_lib.replay import ReplayRequest, run_replay

from support import add_worktree, commit_files, init_repo, run, write_policy


class ParentVerifyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.source = init_repo(self.root / "source")
        self.child = init_repo(self.root / "child")
        self.parent = init_repo(self.root / "parent")
        source_base = commit_files(self.source, {"README.local": "base\n"}, "base")
        self.source_sha = commit_files(
            self.source,
            {"waylib/a.cpp": "child\n", "src/a.cpp": "parent\n"},
            "feat(core): dual",
        )
        self.child_base = commit_files(self.child, {"README.local": "base\n"}, "base")
        run(
            self.parent,
            "update-index",
            "--add",
            "--cacheinfo",
            f"160000,{self.child_base},3rdparty/waylib-shared",
        )
        run(self.parent, "commit", "-m", "parent base")
        self.parent_base = run(self.parent, "rev-parse", "HEAD")
        policy_path = write_policy(self.root / "policy.md")
        self.inventory = build_unified_inventory(
            self.source,
            source_base,
            self.source_sha,
            load_policy(policy_path),
            policy_path,
            set(),
        )
        self.child_wt = add_worktree(
            self.child, self.root / "child-wt", "sync-child", self.child_base
        )
        self.parent_wt = add_worktree(
            self.parent, self.root / "parent-wt", "sync-parent", self.parent_base
        )
        self.artifacts = self.root / "artifacts"
        request = ReplayRequest(
            source_repo=self.source,
            parent_worktree=self.parent_wt,
            child_worktree=self.child_wt,
            parent_base=self.parent_base,
            child_base=self.child_base,
            inventory=self.inventory,
            artifact_root=self.artifacts,
            journal_path=self.artifacts / "journal.json",
            manifest_path=self.artifacts / "manifest.json",
            waylib_evidence_path=self.artifacts / "waylib-evidence.json",
            parent_evidence_path=self.artifacts / "parent-evidence.json",
            run_id="parent-verify",
            refs_doc="plans/test/plan.md",
            decisions={},
            allow_ephemeral_artifacts=True,
        )
        self.manifest = run_replay(request)
        self.evidence = read_json(request.parent_evidence_path)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def verify(self, manifest=None, evidence=None):
        current = manifest or self.manifest
        return verify_parent_sync(
            self.source,
            self.parent_wt,
            self.parent_base,
            current["final_parent_head"],
            self.inventory,
            current,
            evidence or self.evidence,
            self.artifacts,
        )

    def test_accepts_parent_path_authority_message_and_evidence(self) -> None:
        result = self.verify()

        self.assertEqual(result["outcome"], "pass")
        self.assertEqual(result["verified_entries"], 1)

    def test_blocks_target_path_expansion_and_history_drift(self) -> None:
        (self.parent_wt / "unexpected.txt").write_text("bad\n", encoding="utf-8")
        run(self.parent_wt, "add", "unexpected.txt")
        run(self.parent_wt, "commit", "-m", "bad expansion")
        bad_commit = run(self.parent_wt, "rev-parse", "HEAD")
        manifest = copy.deepcopy(self.manifest)
        manifest["entries"][0]["parent"]["commit"] = bad_commit
        manifest["final_parent_head"] = bad_commit
        evidence = copy.deepcopy(self.evidence)
        evidence["entries"][0]["target_commit"] = bad_commit

        result = self.verify(manifest, evidence)

        self.assertEqual(result["outcome"], "blocked")
        joined = "\n".join(result["blocked_reasons"])
        self.assertIn("target path expansion", joined)
        self.assertIn("parent history differs", joined)

    def test_blocks_tampered_parent_artifact(self) -> None:
        record = self.evidence["entries"][0]["artifacts"]["target_diff"]
        (self.artifacts / record["path"]).write_text("tampered\n", encoding="utf-8")

        result = self.verify()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(any("sha256 mismatch" in item for item in result["blocked_reasons"]))

    def test_blocks_rehashed_artifact_not_derived_from_git_objects(self) -> None:
        record = self.evidence["entries"][0]["artifacts"]["target_diff"]
        content = b"self-consistent but unrelated diff\n"
        (self.artifacts / record["path"]).write_bytes(content)
        record["size"] = len(content)
        record["sha256"] = hashlib.sha256(content).hexdigest()

        result = self.verify()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("content differs from Git objects" in item for item in result["blocked_reasons"])
        )

    def test_blocks_original_message_and_path_mapping_drift(self) -> None:
        old_commit = self.manifest["entries"][0]["parent"]["commit"]
        message = run(self.parent_wt, "show", "-s", "--format=%B", old_commit)
        message = message.replace(
            "Original treeland commit:\n    feat(core): dual",
            "Original treeland commit:\n    tampered source message",
        ).replace(
            "- src/a.cpp -> compositor/src/a.cpp",
            "- src/a.cpp -> compositor/src/not-a.cpp",
        )
        message_path = self.root / "tampered-message.txt"
        message_path.write_text(message + "\n", encoding="utf-8")
        run(self.parent_wt, "commit", "--amend", "--file", str(message_path))
        bad_commit = run(self.parent_wt, "rev-parse", "HEAD")
        manifest = copy.deepcopy(self.manifest)
        manifest["entries"][0]["parent"]["commit"] = bad_commit
        manifest["final_parent_head"] = bad_commit
        evidence = copy.deepcopy(self.evidence)
        evidence["entries"][0]["target_commit"] = bad_commit

        result = self.verify(manifest, evidence)

        self.assertEqual(result["outcome"], "blocked")
        joined = "\n".join(result["blocked_reasons"])
        self.assertIn("original message differs", joined)
        self.assertIn("path mapping mismatch", joined)

    def test_blocks_manifest_and_evidence_schema_drift(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        evidence = copy.deepcopy(self.evidence)
        manifest["kind"] = "wrong-kind"
        evidence["kind"] = "wrong-kind"

        result = self.verify(manifest, evidence)

        self.assertEqual(result["outcome"], "blocked")
        joined = "\n".join(result["blocked_reasons"])
        self.assertIn("manifest kind", joined)
        self.assertIn("parent evidence kind", joined)


if __name__ == "__main__":
    unittest.main()
