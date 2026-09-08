from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from unified_sync_lib.inventory import build_unified_inventory
from unified_sync_lib.policy import load_policy
from unified_sync_lib.replay import ReplayBlocked, ReplayRequest, run_replay
from unified_sync_lib.evidence import verify_waylib_sync
from unified_sync_lib.traces import build_waylib_traces
from unified_sync_lib.parent_verify import verify_parent_sync
from unified_sync_lib.gitlink import verify_nested_gitlink_consistency
from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.git_ops import read_json
from unified_sync_lib.wlroots import wlroots_source_audit
from wlroots_verify import verify_wlroots
from support import add_worktree, commit_files, init_repo, run, write_policy


class ThreeRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = init_repo(self.root / "source")
        self.child = init_repo(self.root / "child")
        self.parent = init_repo(self.root / "parent")
        self.wlroots = init_repo(self.root / "wlroots")
        self.rfiles = {"core.c": "int core(void) { return 1; }\n"}
        self.rb = commit_files(self.wlroots, self.rfiles, "wlroots baseline")
        self.sb = commit_files(self.source, {"3rdparty/wlroots/" + k: v for k, v in self.rfiles.items()}, "source baseline")
        self.cb = commit_files(self.child, {"README": "child baseline\n"}, "child baseline")
        run(self.parent, "update-index", "--add", "--cacheinfo", f"160000,{self.cb},3rdparty/waylib-shared")
        run(self.parent, "commit", "-m", "parent baseline")
        self.pb = run(self.parent, "rev-parse", "HEAD")
        self.policy_path = write_policy(self.root / "policy.md")
        self.policy = load_policy(self.policy_path)

    def tearDown(self):
        self.temp.cleanup()

    def inventory(self, head):
        return build_unified_inventory(self.source, self.sb, head, self.policy, self.policy_path, set())

    def request(self, head, suffix="one"):
        root = self.root / ("artifacts-" + suffix)
        return ReplayRequest(
            source_repo=self.source,
            parent_worktree=add_worktree(self.parent, self.root / ("p-"+suffix), "sync-"+suffix, self.pb),
            child_worktree=add_worktree(self.child, self.root / ("c-"+suffix), "sync-"+suffix, self.cb),
            parent_base=self.pb, child_base=self.cb,
            inventory=self.inventory(head), artifact_root=root,
            journal_path=root/"journal.json", manifest_path=root/"manifest.json",
            waylib_evidence_path=root/"waylib-evidence.json", parent_evidence_path=root/"parent-evidence.json",
            run_id="three-"+suffix, refs_doc="test-plan.md", decisions={}, allow_ephemeral_artifacts=True,
            wlroots_repo=self.wlroots, wlroots_base=self.rb, wlroots_target_ref="refs/heads/main",
            wlroots_worktree=add_worktree(self.wlroots, self.root / ("r-"+suffix), "sync-"+suffix, self.rb),
            wlroots_submodule_url=str(self.wlroots),
        )

    def test_inventory_distinguishes_wrapper_and_submodule_source(self):
        sha = commit_files(self.source, {
            "wlroots/cmake/sources.cmake": "# wrapper\n",
            "3rdparty/wlroots/core.c": "int core(void) { return 2; }\n",
        }, "update both wlroots layers")
        inventory = self.inventory(sha)
        self.assertEqual(inventory["outcome"], "pass", inventory["blocked_reasons"])
        item = inventory["commits"][0]
        self.assertEqual(item["classification"], "waylib-only")
        self.assertEqual(item["waylib_shared"]["source_paths"], ["wlroots/cmake/sources.cmake"])
        self.assertEqual(item["wlroots"]["target_paths"], ["core.c"])

    def test_replays_three_repositories_and_first_registration(self):
        sha = commit_files(self.source, {"3rdparty/wlroots/core.c": "int core(void) { return 2; }\n"}, "wlroots source change")
        request = self.request(sha)
        manifest = run_replay(request)
        node = manifest["entries"][0]
        self.assertLess(node["wlroots"]["sequence"], node["child"]["sequence"])
        self.assertLess(node["child"]["sequence"], node["parent"]["sequence"])
        self.assertEqual(run(request.wlroots_worktree, "show", "HEAD:core.c"), "int core(void) { return 2; }")
        self.assertEqual(run(request.child_worktree, "rev-parse", "HEAD:3rdparty/wlroots"), node["wlroots"]["commit"])
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD:3rdparty/waylib-shared"), node["child"]["commit"])
        self.assertEqual(run(request.child_worktree, "config", "--blob=HEAD:.gitmodules", "submodule.wlroots.path"), "3rdparty/wlroots")
        self.assertEqual(node["child"]["action"], "adapted")
        self.assertEqual(node["parent"]["action"], "gitlink-only")
        self.verify_lanes(request, manifest)

    def test_wrapper_only_registers_proved_base_without_fake_r_commit(self):
        sha = commit_files(self.source, {"wlroots/cmake/vars.cmake": "set(PRIVATE_VALUE 1)\n"}, "wrapper only")
        request = self.request(sha)
        manifest = run_replay(request)
        node = manifest["entries"][0]
        self.assertIsNone(node["wlroots"]["commit"])
        self.assertEqual(manifest["final_wlroots_head"], self.rb)
        self.assertEqual(node["nested_gitlink"]["from"], None)
        self.assertEqual(node["nested_gitlink"]["to"], self.rb)
        self.assertEqual(run(request.child_worktree, "cat-file", "-t", "HEAD:wlroots"), "tree")
        self.verify_lanes(request, manifest)

    def test_source_matrix_propagates_each_gitlink_before_next_source(self):
        scenarios = [
            ({"wlroots/cmake/vars.cmake": "set(PRIVATE_VALUE 1)\n"}, "waylib-only"),
            ({"3rdparty/wlroots/core.c": "int core(void) { return 2; }\n"}, "waylib-only"),
            ({"wlroots/cmake/vars.cmake": "set(PRIVATE_VALUE 2)\n", "3rdparty/wlroots/core.c": "int core(void) { return 3; }\n"}, "waylib-only"),
            ({"src/p.cpp": "p1\n", "3rdparty/wlroots/core.c": "int core(void) { return 4; }\n"}, "dual"),
            ({"src/p.cpp": "p2\n", "qwlroots/c.cpp": "c1\n", "3rdparty/wlroots/core.c": "int core(void) { return 5; }\n"}, "dual"),
            ({"src/p.cpp": "p3\n"}, "deckshell-only"),
            ({"waylib/c.cpp": "c2\n"}, "waylib-only"),
            ({"vendor/ignored.txt": "ignored\n"}, "unowned-skip"),
        ]
        for files, classification in scenarios:
            head = commit_files(self.source, files, "matrix " + classification, timestamp="2026-01-02T12:34:56+08:00")
        request = self.request(head)
        manifest = run_replay(request)
        self.assertEqual([node["classification"] for node in manifest["entries"]], [row[1] for row in scenarios])
        self.verify_lanes(request, manifest)
        for node in manifest["entries"]:
            if node["parent"]["commit"]:
                message = run(request.parent_worktree, "show", "-s", "--format=%B", node["parent"]["commit"])
                self.assertIn("Treeland-Commit: " + node["source_commit"], message)
                if node["classification"] == "waylib-only":
                    self.assertIn("这是一个单纯的 gitlink 变更", message)

    def test_r_and_c_interruption_resume_preserves_completed_commits(self):
        sha = commit_files(self.source, {"3rdparty/wlroots/core.c": "int core(void) { return 2; }\n"}, "r change")
        for stage in ("wlroots", "child"):
            request = self.request(sha, stage)
            def stop(lane, source, commit):
                if lane == stage:
                    raise RuntimeError("injected interruption")
            with self.assertRaisesRegex(ReplayBlocked, "injected interruption"):
                run_replay(request, stage_hook=stop)
            journal = read_json(request.journal_path)
            rcommit = journal["nodes"][sha]["wlroots"]["commit"]
            self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.pb)
            manifest = run_replay(request, resume=True)
            self.assertEqual(manifest["entries"][0]["wlroots"]["commit"], rcommit)
            self.verify_lanes(request, manifest)

    def test_missing_inputs_and_bad_r_projection_block_before_journal(self):
        sha = commit_files(self.source, {"wlroots/README": "wrapper\n"}, "wrapper")
        request = self.request(sha, "missing")
        request.wlroots_submodule_url = None
        with self.assertRaisesRegex(ReplayBlocked, "required together"):
            run_replay(request)
        self.assertFalse(request.journal_path.exists())
        wrong = commit_files(self.wlroots, {"core.c": "wrong baseline\n"}, "unproved pin")
        request = self.request(sha, "projection")
        request.wlroots_base = wrong
        run(request.wlroots_worktree, "checkout", "--detach", wrong)
        with self.assertRaisesRegex(ReplayBlocked, "source subtree projection"):
            run_replay(request)
        self.assertFalse(request.journal_path.exists())

    def test_preserves_unrelated_gitmodules_and_registration_is_not_gitlink_only(self):
        modules = '[submodule "other"]\n\tpath = extras/other\n\turl = ../other.git\n'
        self.cb = commit_files(self.child, {".gitmodules": modules}, "unrelated registration")
        run(self.parent, "update-index", "--add", "--cacheinfo", f"160000,{self.cb},3rdparty/waylib-shared")
        run(self.parent, "commit", "-m", "new child baseline")
        self.pb = run(self.parent, "rev-parse", "HEAD")
        sha = commit_files(self.source, {"3rdparty/wlroots/core.c": "int core(void) { return 2; }\n"}, "r change")
        request = self.request(sha)
        manifest = run_replay(request)
        self.assertTrue((request.child_worktree / ".gitmodules").read_text().startswith(modules))
        self.assertEqual(manifest["entries"][0]["child"]["action"], "adapted")
        self.verify_lanes(request, manifest)

    def test_copy_across_owners_only_mutates_new_side(self):
        sha = commit_files(self.source, {"wlroots/copied.c": self.rfiles["core.c"]}, "copy from R to C")
        inventory = self.inventory(sha)
        self.assertFalse(inventory["commits"][0]["wlroots"]["included"])
        self.assertEqual(inventory["commits"][0]["waylib_shared"]["source_paths"], ["wlroots/copied.c"])
        request = self.request(sha)
        self.verify_lanes(request, run_replay(request))

    def test_rename_across_owners_replays_both_sides(self):
        sha = commit_files(self.source, {"3rdparty/wlroots/core.c": None, "wlroots/moved.c": self.rfiles["core.c"]}, "move R source into wrapper")
        request = self.request(sha)
        manifest = run_replay(request)
        self.assertEqual(run(request.wlroots_worktree, "ls-tree", "-r", "HEAD"), "")
        self.verify_lanes(request, manifest)

    def test_r_empty_commit_keeps_mapping_and_propagates_dependency(self):
        sha = commit_files(self.source, {"3rdparty/wlroots/core.c": "int core(void) { return 2; }\n"}, "already equivalent")
        request = self.request(sha)
        proof = write_artifact(request.artifact_root, "equivalence.md", b"Reviewed: target behavior is equivalent for the selected input.\n")
        request.decisions = {"entries": {sha: {"wlroots": {"action": "empty", "equivalence_proof": proof}}}}
        manifest = run_replay(request)
        node = manifest["entries"][0]
        self.assertEqual(node["wlroots"]["action"], "empty")
        self.assertNotEqual(node["wlroots"]["commit"], self.rb)
        self.assertEqual(run(request.wlroots_worktree, "rev-parse", "HEAD^{tree}"), run(self.wlroots, "rev-parse", self.rb + "^{tree}"))
        self.verify_lanes(request, manifest)

    def test_nested_verifier_rejects_tampered_base_proof_and_sequence(self):
        sha = commit_files(self.source, {"wlroots/README": "wrapper\n"}, "wrapper")
        request = self.request(sha)
        manifest = run_replay(request)
        broken = copy.deepcopy(manifest)
        broken["entries"][0]["child"]["sequence"] = broken["entries"][0]["parent"]["sequence"] + 1
        result = verify_nested_gitlink_consistency(request.child_worktree, self.wlroots, request.inventory, broken, request.artifact_root)
        self.assertEqual(result["outcome"], "blocked")
        broken = copy.deepcopy(manifest)
        broken["identity"]["wlroots"]["baseline_proof"] = {"path": "missing", "size": 1, "sha256": "0" * 64}
        result = verify_nested_gitlink_consistency(request.child_worktree, self.wlroots, request.inventory, broken, request.artifact_root)
        self.assertEqual(result["outcome"], "blocked")

    def test_resume_rejects_tampered_nested_transition_before_parent(self):
        sha = commit_files(self.source, {"3rdparty/wlroots/core.c": "int core(void) { return 2; }\n"}, "R change")
        request = self.request(sha)
        def stop(lane, source, commit):
            if lane == "child":
                raise RuntimeError("stop after C")
        with self.assertRaises(ReplayBlocked):
            run_replay(request, stage_hook=stop)
        journal = read_json(request.journal_path)
        journal["nodes"][sha]["nested_gitlink"]["to"] = self.rb
        request.journal_path.write_text(json.dumps(journal), encoding="utf-8")
        with self.assertRaisesRegex(ReplayBlocked, "nested gitlink"):
            run_replay(request, resume=True)
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.pb)

    def test_source_owned_roots_must_remain_directories(self):
        for index, prefix in enumerate(("qwlroots", "waylib", "wlroots", "3rdparty/wlroots")):
            with self.subTest(prefix=prefix):
                repo = init_repo(self.root / f"drift-{index}")
                base = commit_files(repo, {prefix + "/a.c": "before\n"}, "base")
                run(repo, "rm", "-r", "--cached", "--", prefix)
                run(repo, "update-index", "--add", "--cacheinfo", f"160000,{base},{prefix}")
                run(repo, "commit", "-m", "invalid gitlink layout")
                result = build_unified_inventory(repo, base, "HEAD", self.policy, self.policy_path, set())
                self.assertEqual(result["outcome"], "blocked")
                self.assertTrue(any("source-layout-drift" in value for value in result["blocked_reasons"]))

    def test_absent_source_subtree_accepts_explicit_empty_r_commit(self):
        self.sb = commit_files(self.source, {"3rdparty/wlroots/core.c": None}, "remove source subtree")
        self.rb = commit_files(self.wlroots, {"core.c": None}, "prepared empty R baseline")
        sha = commit_files(self.source, {"wlroots/README": "ordinary wrapper files\n"}, "wrapper import")
        request = self.request(sha)
        manifest = run_replay(request)
        self.assertIsNone(manifest["identity"]["wlroots"]["source_base_tree"])
        self.assertEqual(manifest["final_wlroots_head"], self.rb)
        self.verify_lanes(request, manifest)

    def test_r_binary_mode_deletion_projection_rejects_same_path_tampering(self):
        self.sb = commit_files(self.source, {"3rdparty/wlroots/obsolete.c": "old\n"}, "source baseline")
        self.rb = commit_files(self.wlroots, {"obsolete.c": "old\n"}, "R baseline")
        binary = self.source / "3rdparty/wlroots/data.bin"
        binary.write_bytes(b"\x00\xff\x01\x02")
        binary.chmod(0o755)
        sha = commit_files(self.source, {"3rdparty/wlroots/obsolete.c": None}, "binary and deletion")
        request = self.request(sha)
        manifest = run_replay(request)
        self.verify_lanes(request, manifest)
        target = request.wlroots_worktree / "data.bin"
        self.assertEqual(target.read_bytes(), binary.read_bytes())
        self.assertTrue(target.stat().st_mode & 0o111)
        self.assertFalse((request.wlroots_worktree / "obsolete.c").exists())
        target.write_bytes(b"wrong binary content")
        run(request.wlroots_worktree, "add", "--", "data.bin")
        run(request.wlroots_worktree, "commit", "--amend", "--no-edit")
        result = wlroots_source_audit(self.source, request.wlroots_worktree, request.inventory["commits"][0],
                                      "HEAD", "applied", [], {}, request.artifact_root)
        self.assertEqual(result["outcome"], "blocked")

    def test_namespace_changed_then_restored_still_blocks_first_parent(self):
        header = "#define SERVER_NAMESPACE Server\nnamespace Waylib { namespace SERVER_NAMESPACE { class API {}; } }\n"
        self.sb = commit_files(self.source, {"waylib/global.h": header}, "source namespace base")
        self.cb = commit_files(self.child, {"waylib/global.h": header}, "C namespace base")
        run(self.parent, "update-index", "--cacheinfo", f"160000,{self.cb},3rdparty/waylib-shared")
        run(self.parent, "commit", "-m", "P namespace base")
        self.pb = run(self.parent, "rev-parse", "HEAD")
        changed = commit_files(self.source, {"waylib/global.h": header.replace("Server\n", "Broken\n")}, "drift")
        restored = commit_files(self.source, {"waylib/global.h": header}, "restore")
        request = self.request(restored)
        with self.assertRaisesRegex(ReplayBlocked, "source contract drift"):
            run_replay(request)
        self.assertIsNone(read_json(request.journal_path)["nodes"][changed]["parent"]["commit"])
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.pb)
        with self.assertRaisesRegex(ReplayBlocked, "source contract drift"):
            run_replay(request, resume=True)

    def test_preflight_rejects_aliased_and_foreign_r_worktrees(self):
        sha = commit_files(self.source, {"wlroots/README": "wrapper\n"}, "wrapper")
        alias = self.root / "alias"
        alias.symlink_to(self.root, target_is_directory=True)
        request = self.request(sha, "alias")
        request.wlroots_worktree = alias / request.wlroots_worktree.name
        with self.assertRaisesRegex(ReplayBlocked, "symlink"):
            run_replay(request)
        self.assertFalse(request.journal_path.exists())
        request = self.request(sha, "foreign")
        request.wlroots_repo = self.child
        with self.assertRaisesRegex(ReplayBlocked, "linked to the supplied"):
            run_replay(request)
        self.assertFalse(request.journal_path.exists())

    def test_reviewed_r_baseline_difference_binds_every_path(self):
        self.rb = commit_files(self.wlroots, {"local-note.txt": "local preparation\n"}, "adapted R baseline")
        sha = commit_files(self.source, {"wlroots/README": "wrapper\n"}, "wrapper")
        request = self.request(sha)
        proof = {"source_tree": run(self.source, "rev-parse", self.sb + ":3rdparty/wlroots"),
                 "target_tree": run(self.wlroots, "rev-parse", self.rb + "^{tree}"), "review_state": "approved",
                 "paths": [{"path": "local-note.txt", "reason": "Keep the reviewed target-local preparation note."}]}
        request.wlroots_baseline_proof = write_artifact(request.artifact_root, "baseline.json", json.dumps(proof).encode())
        manifest = run_replay(request)
        self.verify_lanes(request, manifest)
        self.assertEqual((request.wlroots_worktree / "local-note.txt").read_text(), "local preparation\n")

    def test_copy_from_parent_source_to_r_only_updates_parent_gitlink(self):
        self.sb = commit_files(self.source, {"src/original.c": self.rfiles["core.c"]}, "copy baseline")
        sha = commit_files(self.source, {"3rdparty/wlroots/copied.c": self.rfiles["core.c"]}, "copy P source to R")
        request = self.request(sha)
        self.assertEqual(request.inventory["commits"][0]["classification"], "waylib-only")
        manifest = run_replay(request)
        self.verify_lanes(request, manifest)
        self.assertEqual(run(request.parent_worktree, "diff", "--name-only", self.pb, "HEAD"), "3rdparty/waylib-shared")

    def verify_lanes(self, request, manifest):
        result, nested = verify_wlroots(self.source, request.child_worktree, self.wlroots, request.inventory,
                                         manifest, read_json(request.wlroots_evidence_path), request.artifact_root)
        self.assertEqual(result["outcome"], "pass", result["blocked_reasons"])
        self.assertEqual(nested["outcome"], "pass", nested["blocked_reasons"])
        parent = verify_parent_sync(self.source, request.parent_worktree, self.pb,
                                   manifest["final_parent_head"], request.inventory, manifest,
                                   json.loads(request.parent_evidence_path.read_text()), request.artifact_root)
        self.assertEqual(parent["outcome"], "pass", parent["blocked_reasons"])
        for lane, repo, base, head, proof in (
            ("child", request.child_worktree, self.cb, manifest["final_child_head"], request.waylib_evidence_path),
            ("wlroots", request.wlroots_worktree, self.rb, manifest["final_wlroots_head"], request.wlroots_evidence_path),
        ):
            traces = build_waylib_traces(repo, base, head, request.inventory, self.source, lane)
            result = verify_waylib_sync(repo, base, head, request.inventory, traces, json.loads(proof.read_text()), request.artifact_root, self.source, lane)
            self.assertEqual(result["outcome"], "pass", result["blocked_reasons"])


if __name__ == "__main__":
    unittest.main()
