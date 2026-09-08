from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from unified_sync_lib.git_ops import read_json, sha256_file
from unified_sync_lib.closeout import CloseoutBlocked, closeout_refs
from unified_sync_lib.gitlink import verify_gitlink_consistency
from unified_sync_lib.inventory import build_unified_inventory
from unified_sync_lib.policy import load_policy
from unified_sync_lib.replay import ReplayRequest, run_replay

from support import add_worktree, commit_files, init_repo, run, write_policy


class GitlinkVerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.source = init_repo(self.root / "source")
        self.child = init_repo(self.root / "child")
        self.parent = init_repo(self.root / "parent")
        source_base = commit_files(self.source, {"README.local": "base\n"}, "base")
        self.source_sha = commit_files(
            self.source, {"qwlroots/a.cpp": "a\n"}, "fix(qwlroots): sync"
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
        inventory = build_unified_inventory(
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
        artifacts = self.root / "artifacts"
        request = ReplayRequest(
            source_repo=self.source,
            parent_worktree=self.parent_wt,
            child_worktree=self.child_wt,
            parent_base=self.parent_base,
            child_base=self.child_base,
            inventory=inventory,
            artifact_root=artifacts,
            journal_path=artifacts / "journal.json",
            manifest_path=artifacts / "manifest.json",
            waylib_evidence_path=artifacts / "waylib-evidence.json",
            parent_evidence_path=artifacts / "parent-evidence.json",
            run_id="gitlink-test",
            refs_doc="plans/test/plan.md",
            decisions={},
            allow_ephemeral_artifacts=True,
        )
        self.manifest = run_replay(request)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def verify(self, manifest=None):
        return verify_gitlink_consistency(
            self.parent_wt,
            self.child_wt,
            self.parent_base,
            self.child_base,
            manifest or self.manifest,
        )

    def passing_report(self):
        markdown = self.root / "sync-report.md"
        markdown.write_text("# passing fixture report\n", encoding="utf-8")
        return {
            "schema_version": 2,
            "kind": "treeland-unified-sync-report",
            "outcome": "pass",
            "build_scope": {"kind": "range-head-only", "source_head": self.manifest["entries"][-1]["source_commit"]},
            "final_parent_head": self.manifest["final_parent_head"],
            "final_child_head": self.manifest["final_child_head"],
            "replay_identity": self.manifest["identity"],
            "final_wlroots_head": None,
            "inventory_sha256": "a" * 64,
            "manifest_sha256": "b" * 64,
            "gate_sha256": {
                name: str(index) * 64
                for index, name in enumerate(
                    (
                        "deckshell_verify",
                        "waylib_verify",
                        "gitlink_verify",
                        "protocol_tracking",
                        "contract_audit",
                        "child_materialization",
                        "wlroots_verify",
                        "nested_gitlink_verify",
                    ),
                    start=1,
                )
            },
            "validations_sha256": "6" * 64,
            "blocked_reasons": [],
            "report": {
                "path": str(markdown.resolve()),
                "size": markdown.stat().st_size,
                "sha256": sha256_file(markdown),
            },
        }

    def test_accepts_mode_object_reachability_and_gitlink_only_purity(self) -> None:
        result = self.verify()

        self.assertEqual(result["outcome"], "pass")
        self.assertEqual(result["verified_gitlink_updates"], 1)

    def test_blocks_gitlink_only_extra_path_and_wrong_mode(self) -> None:
        leak = self.parent_wt / "leak.txt"
        leak.write_text("leak\n", encoding="utf-8")
        run(self.parent_wt, "add", "leak.txt")
        run(self.parent_wt, "commit", "-m", "bad purity")
        bad_purity = run(self.parent_wt, "rev-parse", "HEAD")
        purity_manifest = copy.deepcopy(self.manifest)
        purity_manifest["entries"][0]["parent"]["commit"] = bad_purity
        purity_manifest["final_parent_head"] = bad_purity

        purity = self.verify(purity_manifest)

        self.assertEqual(purity["outcome"], "blocked")
        self.assertTrue(
            any("gitlink-only purity" in item for item in purity["blocked_reasons"])
        )

        blob_path = self.root / "blob"
        blob_path.write_text("not a gitlink\n", encoding="utf-8")
        blob = run(self.parent_wt, "hash-object", "-w", str(blob_path))
        run(
            self.parent_wt,
            "update-index",
            "--cacheinfo",
            f"100644,{blob},3rdparty/waylib-shared",
        )
        run(self.parent_wt, "commit", "-m", "bad mode")
        bad_mode = run(self.parent_wt, "rev-parse", "HEAD")
        mode_manifest = copy.deepcopy(self.manifest)
        mode_manifest["entries"][0]["parent"]["commit"] = bad_mode
        mode_manifest["final_parent_head"] = bad_mode

        mode = self.verify(mode_manifest)

        self.assertEqual(mode["outcome"], "blocked")
        self.assertTrue(any("mode 160000" in item for item in mode["blocked_reasons"]))

    def test_blocks_child_commit_not_reachable_from_frozen_child_head(self) -> None:
        tree = run(self.child_wt, "rev-parse", f"{self.child_base}^{{tree}}")
        env = {
            "GIT_AUTHOR_DATE": "2026-01-02T00:00:00+00:00",
            "GIT_COMMITTER_DATE": "2026-01-02T00:00:00+00:00",
        }
        orphan = run(self.child_wt, "commit-tree", tree, "-m", "orphan", env=env)
        run(
            self.parent_wt,
            "update-index",
            "--add",
            "--cacheinfo",
            f"160000,{orphan},3rdparty/waylib-shared",
        )
        run(self.parent_wt, "commit", "-m", "point at unreachable child")
        parent_commit = run(self.parent_wt, "rev-parse", "HEAD")
        manifest = copy.deepcopy(self.manifest)
        manifest["entries"][0]["child"]["commit"] = orphan
        manifest["entries"][0]["gitlink"]["to"] = orphan
        manifest["entries"][0]["parent"]["commit"] = parent_commit
        manifest["final_parent_head"] = parent_commit

        result = self.verify(manifest)

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(any("not reachable" in item for item in result["blocked_reasons"]))

    def test_malformed_manifest_lane_is_reported_without_crashing(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["entries"][0]["child"] = []

        result = self.verify(manifest)

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("manifest child must be an object" in item for item in result["blocked_reasons"])
        )

    def test_closeout_is_child_first_and_resumes_after_interruption(self) -> None:
        verification = self.passing_report()
        child_ref = "refs/heads/target-child"
        parent_ref = "refs/heads/target-parent"
        run(self.child, "branch", "target-child", self.child_base)
        run(self.parent, "branch", "target-parent", self.parent_base)
        closeout_journal = self.root / "closeout.json"

        def interrupt(stage: str) -> None:
            if stage == "child-ref-written":
                raise RuntimeError("injected closeout stop")

        with self.assertRaises(CloseoutBlocked):
            closeout_refs(
                self.parent,
                self.child,
                parent_ref,
                child_ref,
                self.parent_base,
                self.child_base,
                self.manifest["final_parent_head"],
                self.manifest["final_child_head"],
                verification,
                closeout_journal,
                stage_hook=interrupt,
            )
        self.assertEqual(run(self.child, "rev-parse", child_ref), self.manifest["final_child_head"])
        self.assertEqual(run(self.parent, "rev-parse", parent_ref), self.parent_base)

        result = closeout_refs(
            self.parent,
            self.child,
            parent_ref,
            child_ref,
            self.parent_base,
            self.child_base,
            self.manifest["final_parent_head"],
            self.manifest["final_child_head"],
            verification,
            closeout_journal,
            resume=True,
        )

        self.assertEqual(result["outcome"], "pass")
        self.assertEqual(run(self.parent, "rev-parse", parent_ref), self.manifest["final_parent_head"])
        events = read_json(closeout_journal)["events"]
        child_sequence = next(item["sequence"] for item in events if item["stage"] == "child-ref-updated")
        parent_sequence = next(item["sequence"] for item in events if item["stage"] == "parent-ref-updated")
        self.assertLess(child_sequence, parent_sequence)

    def test_closeout_rejects_gitlink_only_proof(self) -> None:
        child_ref = "refs/heads/target-child"
        parent_ref = "refs/heads/target-parent"
        run(self.child, "branch", "target-child", self.child_base)
        run(self.parent, "branch", "target-parent", self.parent_base)

        with self.assertRaisesRegex(CloseoutBlocked, "complete passing sync report"):
            closeout_refs(
                self.parent,
                self.child,
                parent_ref,
                child_ref,
                self.parent_base,
                self.child_base,
                self.manifest["final_parent_head"],
                self.manifest["final_child_head"],
                self.verify(),
                self.root / "rejected-closeout.json",
            )

    def test_closeout_rejects_simplified_or_tampered_report(self) -> None:
        child_ref = "refs/heads/target-child"
        parent_ref = "refs/heads/target-parent"
        run(self.child, "branch", "target-child", self.child_base)
        run(self.parent, "branch", "target-parent", self.parent_base)
        simplified = {
            "schema_version": 2,
            "kind": "treeland-unified-sync-report",
            "outcome": "pass",
            "final_parent_head": self.manifest["final_parent_head"],
            "final_child_head": self.manifest["final_child_head"],
        }

        with self.assertRaisesRegex(CloseoutBlocked, "complete passing sync report"):
            closeout_refs(
                self.parent,
                self.child,
                parent_ref,
                child_ref,
                self.parent_base,
                self.child_base,
                self.manifest["final_parent_head"],
                self.manifest["final_child_head"],
                simplified,
                self.root / "simplified-closeout.json",
            )

        report = self.passing_report()
        Path(report["report"]["path"]).write_text("tampered\n", encoding="utf-8")
        with self.assertRaisesRegex(CloseoutBlocked, "report artifact"):
            closeout_refs(
                self.parent,
                self.child,
                parent_ref,
                child_ref,
                self.parent_base,
                self.child_base,
                self.manifest["final_parent_head"],
                self.manifest["final_child_head"],
                report,
                self.root / "tampered-closeout.json",
            )

    def test_closeout_rejects_parent_candidate_with_wrong_gitlink(self) -> None:
        child_ref = "refs/heads/target-child"
        parent_ref = "refs/heads/target-parent"
        run(self.child, "branch", "target-child", self.child_base)
        run(self.parent, "branch", "target-parent", self.parent_base)
        run(
            self.parent_wt,
            "update-index",
            "--add",
            "--cacheinfo",
            f"160000,{self.child_base},3rdparty/waylib-shared",
        )
        run(self.parent_wt, "commit", "-m", "wrong final gitlink")
        wrong_parent = run(self.parent_wt, "rev-parse", "HEAD")
        report = self.passing_report()
        report["final_parent_head"] = wrong_parent

        with self.assertRaisesRegex(CloseoutBlocked, "candidate gitlink"):
            closeout_refs(
                self.parent,
                self.child,
                parent_ref,
                child_ref,
                self.parent_base,
                self.child_base,
                wrong_parent,
                self.manifest["final_child_head"],
                report,
                self.root / "wrong-gitlink-closeout.json",
            )

    def test_closeout_resume_rejects_corrupted_journal_shape(self) -> None:
        child_ref = "refs/heads/target-child"
        parent_ref = "refs/heads/target-parent"
        run(self.child, "branch", "target-child", self.child_base)
        run(self.parent, "branch", "target-parent", self.parent_base)
        journal_path = self.root / "corrupt-closeout.json"
        report = self.passing_report()

        def interrupt(stage: str) -> None:
            if stage == "child-ref-written":
                raise RuntimeError("injected closeout stop")

        with self.assertRaises(CloseoutBlocked):
            closeout_refs(
                self.parent,
                self.child,
                parent_ref,
                child_ref,
                self.parent_base,
                self.child_base,
                self.manifest["final_parent_head"],
                self.manifest["final_child_head"],
                report,
                journal_path,
                stage_hook=interrupt,
            )
        journal = read_json(journal_path)
        journal["events"] = "corrupt"
        journal_path.write_text(json.dumps(journal), encoding="utf-8")

        with self.assertRaisesRegex(CloseoutBlocked, "events"):
            closeout_refs(
                self.parent,
                self.child,
                parent_ref,
                child_ref,
                self.parent_base,
                self.child_base,
                self.manifest["final_parent_head"],
                self.manifest["final_child_head"],
                report,
                journal_path,
                resume=True,
            )


if __name__ == "__main__":
    unittest.main()
