from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from support import add_worktree, commit_files, init_repo, run, write_policy
from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.contracts import build_install_snapshot, build_source_contract_audit
from unified_sync_lib.git_ops import read_json
from unified_sync_lib.inventory import build_unified_inventory
from unified_sync_lib.namespace_probe import run_namespace_probe
from unified_sync_lib.materialization import materialize_child_checkout
from unified_sync_lib.traces import build_waylib_traces
from unified_sync_lib.evidence import verify_waylib_sync
from unified_sync_lib.policy import load_policy
from unified_sync_lib.replay import ReplayBlocked, ReplayRequest, run_replay
from unified_sync_lib.wlroots import UPDATER_GUARD, UPDATER_PATH, updater_guard_errors


class WrapperContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source, self.parent, self.child, self.r = [init_repo(self.root / name)
                                                     for name in ("source", "parent", "child", "r")]
        self.rb = commit_files(self.r, {"core.c": "int value(void) { return 1; }\n"}, "R baseline")
        self.cb = commit_files(self.child, {"CMakeLists.txt": "add_library(Core INTERFACE)\n"}, "C baseline")
        run(self.parent, "update-index", "--add", "--cacheinfo", f"160000,{self.cb},3rdparty/waylib-shared")
        run(self.parent, "commit", "-m", "P baseline")
        self.pb = run(self.parent, "rev-parse", "HEAD")
        self.sb = commit_files(self.source, {"3rdparty/wlroots/core.c": "int value(void) { return 1; }\n"}, "source base")
        self.files = {
            "wlroots/CMakeLists.txt": "add_library(InternalWlr STATIC ../3rdparty/wlroots/core.c)\n"
                                     "add_library(Wlroots::wlroots ALIAS InternalWlr)\n",
            "wlroots/update-from-upstream.sh": "#!/usr/bin/env bash\ngit fetch upstream\ngit subtree merge\n",
            "wlroots/UPSTREAM": "SOURCE_URL=https://example.invalid/upstream/wlroots\nREF=main\n"
                                "COMMIT=" + "a" * 40 + "\nVERSION=0.20.2\n",
        }
        self.sh = commit_files(self.source, self.files, "import wrapper")
        policy = write_policy(self.root / "policy.md")
        self.inventory = build_unified_inventory(self.source, self.sb, self.sh, load_policy(policy), policy, set())
        self.artifacts = self.root / "evidence"

    def tearDown(self):
        self.temp.cleanup()

    def prepare(self, guard=True, change_core=False, approve=True):
        preview = add_worktree(self.child, self.root / "preview", "preview", self.cb)
        target = dict(self.files)
        target["CMakeLists.txt"] = ("add_library(BrokenCore INTERFACE)\n" if change_core
                                    else "add_library(Core INTERFACE)\n") + "add_subdirectory(wlroots)\n"
        if guard:
            target["wlroots/update-from-upstream.sh"] = UPDATER_GUARD.decode() + target["wlroots/update-from-upstream.sh"]
        target["wlroots/UPSTREAM"] += "TARGET_LAYOUT=submodule\n"
        proposed = commit_files(preview, target, "reviewed structural adaptation")
        audit = build_source_contract_audit(preview, self.cb, proposed)
        patch = subprocess.check_output(["git", "-C", str(preview), "diff", "--binary", self.cb, proposed])
        record = write_artifact(self.artifacts, "decisions/child.patch", patch)
        proof = write_artifact(self.artifacts, "decisions/review.md", b"Reviewed wrapper integration preserving the existing Core target.\n")
        paths = self.inventory["commits"][0]["waylib_shared"]["source_paths"] + ["CMakeLists.txt"]
        decision = {"action": "adapted", "adaptation_patch": record, "structural_paths": ["CMakeLists.txt"],
                    "adaptation_notes": ["Integrate wrapper without changing the Core public contract."],
                    "adaptation_paths": [{"path": path, "kind": "modified" if path == "CMakeLists.txt" else "materialized",
                                          "reason": "Reviewed submodule wrapper integration.", "proof": proof,
                                          "review_state": "approved"} for path in paths]}
        if approve:
            approval = {"review_state": "approved", "before_snapshot_sha256": audit["before_snapshot_sha256"],
                        "after_snapshot_sha256": audit["after_snapshot_sha256"],
                        "additions": {field: change["added"] for field, change in audit["drift"].items()}}
            decision["contract_additions"] = write_artifact(self.artifacts, "decisions/additions.json", json.dumps(approval).encode())
        return ReplayRequest(
            self.source, add_worktree(self.parent, self.root / "p-wt", "sync", self.pb),
            add_worktree(self.child, self.root / "c-wt", "sync", self.cb), self.pb, self.cb,
            self.inventory, self.artifacts, self.artifacts / "journal.json", self.artifacts / "manifest.json",
            self.artifacts / "waylib-evidence.json", self.artifacts / "parent-evidence.json", "wrapper", "plan.md",
            {"entries": {self.sh: {"child": decision}}}, True, wlroots_repo=self.r, wlroots_base=self.rb,
            wlroots_worktree=add_worktree(self.r, self.root / "r-wt", "sync", self.rb),
            wlroots_target_ref="refs/heads/main", wlroots_submodule_url=str(self.r),
        )

    def test_reviewed_wrapper_integration_and_updater_reject_before_git(self):
        request = self.prepare()
        manifest = run_replay(request)
        self.assertEqual(manifest["outcome"], "pass")
        self.assertIsNone(manifest["entries"][0]["wlroots"]["commit"])
        self.assertEqual(manifest["entries"][0]["child"]["action"], "adapted")
        traces = build_waylib_traces(request.child_worktree, self.cb, manifest["final_child_head"], self.inventory, self.source)
        verified = verify_waylib_sync(request.child_worktree, self.cb, manifest["final_child_head"], self.inventory,
                                      traces, read_json(request.waylib_evidence_path), self.artifacts, self.source)
        self.assertEqual(verified["outcome"], "pass", verified["blocked_reasons"])
        baseline = add_worktree(self.child, self.root / "c-base", "baseline", self.cb)
        materialized = materialize_child_checkout(request.parent_worktree, self.child, manifest, self.r, baseline)
        self.assertIsNone(materialized["wlroots_checkouts"]["child_base"])
        self.assertFalse((baseline / "3rdparty/wlroots").exists())
        marker = self.root / "git-was-run"
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        git = bin_dir / "git"
        git.write_text(f'#!/bin/sh\nprintf ran > "{marker}"\n', encoding="utf-8")
        git.chmod(0o755)
        script = request.child_worktree / "wlroots/update-from-upstream.sh"
        result = subprocess.run(["bash", str(script)], capture_output=True, text=True,
                                env={**os.environ, "PATH": str(bin_dir) + os.pathsep + os.environ["PATH"]})
        self.assertEqual(result.returncode, 64)
        self.assertIn("unified sync", result.stderr)
        self.assertFalse(marker.exists())
        self.assertIn("COMMIT=" + "a" * 40, (request.child_worktree / "wlroots/UPSTREAM").read_text())

    def test_updater_without_guard_blocks_before_child_commit(self):
        request = self.prepare(guard=False)
        with self.assertRaisesRegex(ReplayBlocked, "pre-fetch/subtree rejection guard"):
            run_replay(request)
        self.assertEqual(run(request.child_worktree, "rev-parse", "HEAD"), self.cb)
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.pb)

    def omission_request(self):
        self.files.pop("wlroots/update-from-upstream.sh")
        request = self.prepare(guard=False)
        decision = request.decisions["entries"][self.sh]["child"]
        for path in decision["adaptation_paths"]:
            if path["path"] == "wlroots/update-from-upstream.sh":
                path.update(kind="omitted", reason="Omit the subtree updater from the target.")
        return request

    def test_approved_omission_cannot_remove_required_updater(self):
        request = self.omission_request()
        with self.assertRaisesRegex(ReplayBlocked, "wlroots updater.*missing"):
            run_replay(request)
        self.assertEqual(run(request.child_worktree, "rev-parse", "HEAD"), self.cb)
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.pb)

    def test_resume_rechecks_legacy_child_checkpoint_before_parent(self):
        request = self.omission_request()

        def interrupt(stage, _source, _commit):
            if stage == "child":
                raise RuntimeError("pause after legacy child")

        # 构造旧版已省略脚本的中断现场；恢复时不替换任何验证函数。
        with patch("unified_sync_lib.replay_stages.updater_guard_errors", return_value=[]):
            with self.assertRaisesRegex(ReplayBlocked, "pause after legacy child"):
                run_replay(request, stage_hook=interrupt)
        child = run(request.child_worktree, "rev-parse", "HEAD")
        self.assertNotEqual(child, self.cb)
        with self.assertRaisesRegex(ReplayBlocked, "wlroots updater.*missing"):
            run_replay(request, resume=True)
        self.assertEqual(run(request.child_worktree, "rev-parse", "HEAD"), child)
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.pb)

    def test_independent_verifier_rejects_legacy_approved_omission(self):
        request = self.omission_request()
        with patch("unified_sync_lib.replay_stages.updater_guard_errors", return_value=[]), \
             patch("unified_sync_lib.replay.updater_guard_errors", return_value=[]):
            manifest = run_replay(request)
        traces = build_waylib_traces(request.child_worktree, self.cb, manifest["final_child_head"], self.inventory, self.source)
        verified = verify_waylib_sync(request.child_worktree, self.cb, manifest["final_child_head"], self.inventory,
                                      traces, read_json(request.waylib_evidence_path), self.artifacts, self.source)
        self.assertEqual(verified["outcome"], "blocked")
        self.assertTrue(any("updater is missing" in error for error in verified["blocked_reasons"]), verified)

    def test_commit_hook_removal_cannot_advance_parent(self):
        request = self.prepare()
        hooks = self.root / "hooks"
        hooks.mkdir()
        hook = hooks / "pre-commit"
        hook.write_text("#!/bin/sh\ngit update-index --force-remove -- 'wlroots/update-from-upstream.sh'\n", encoding="utf-8")
        hook.chmod(0o755)
        run(request.child_worktree, "config", "core.hooksPath", str(hooks))
        with self.assertRaisesRegex(ReplayBlocked, "wlroots updater.*missing"):
            run_replay(request)
        self.assertNotEqual(run(request.child_worktree, "rev-parse", "HEAD"), self.cb)
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.pb)
        self.assertIsNone(read_json(request.journal_path)["nodes"][self.sh]["parent"]["commit"])

    def test_guard_requires_regular_git_blob_not_symlink_directory_or_gitlink(self):
        regular = commit_files(self.child, {UPDATER_PATH: UPDATER_GUARD.decode()}, "retained updater")
        self.assertEqual(updater_guard_errors(self.source, self.sh, self.child, regular, self.cb), [])
        script = self.child / UPDATER_PATH
        script.unlink()
        script.symlink_to("missing-updater")
        run(self.child, "add", "--", UPDATER_PATH)
        for mode, sha in (("120000", run(self.child, "rev-parse", ":" + UPDATER_PATH)),
                          ("160000", regular), ("040000", run(self.child, "rev-parse", regular + "^{tree}"))):
            with self.subTest(mode=mode):
                if mode == "040000":
                    tree = run(self.child, "write-tree")
                    run(self.child, "read-tree", "--empty")
                    run(self.child, "read-tree", "--prefix=" + UPDATER_PATH + "/", tree)
                else:
                    run(self.child, "update-index", "--add", "--cacheinfo", f"{mode},{sha},{UPDATER_PATH}")
                tree = run(self.child, "write-tree")
                errors = updater_guard_errors(self.source, self.sh, self.child, tree, regular)
                self.assertTrue(any("regular file" in error for error in errors), errors)

    def test_source_deletion_does_not_waive_target_retention(self):
        regular = commit_files(self.child, {UPDATER_PATH: UPDATER_GUARD.decode()}, "retained updater")
        source = commit_files(self.source, {UPDATER_PATH: None}, "remove upstream updater")
        target = commit_files(self.child, {UPDATER_PATH: None}, "remove target updater")
        errors = updater_guard_errors(self.source, source, self.child, target, regular)
        self.assertTrue(any("updater is missing" in error for error in errors), errors)

    def test_unreviewed_new_wrapper_target_cannot_advance_parent(self):
        request = self.prepare(approve=False)
        with self.assertRaisesRegex(ReplayBlocked, "source contract drift"):
            run_replay(request)
        self.assertIsNone(read_json(request.journal_path)["nodes"][self.sh]["parent"]["commit"])

    def test_approval_cannot_rename_existing_core_target(self):
        request = self.prepare(change_core=True)
        with self.assertRaisesRegex(ReplayBlocked, "cannot relax existing Waylib contracts"):
            run_replay(request)
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.pb)

    def test_fixed_namespace_probe_fails_even_when_macro_consumer_compiles(self):
        snapshots = []
        for label, namespace in (("before", "Server"), ("after", "Other")):
            root = self.root / label
            (root / "include").mkdir(parents=True)
            (root / "include/api.h").write_text(
                f"#define SERVER_NAMESPACE {namespace}\nnamespace Waylib {{ namespace SERVER_NAMESPACE {{ class API {{}}; }} }}\n",
                encoding="utf-8",
            )
            package = root / "lib/cmake/WaylibShared"
            package.mkdir(parents=True)
            (package / "WaylibSharedConfig.cmake").write_text(
                "add_library(WaylibShared::SharedServer INTERFACE IMPORTED)\n", encoding="utf-8",
            )
            snapshots.append(build_install_snapshot(root))
        consumer = self.root / "consumer.cpp"
        consumer.write_text('#include "api.h"\nWaylib::SERVER_NAMESPACE::API value;\n', encoding="utf-8")
        result = subprocess.run(["c++", "-c", str(consumer), "-I", str(self.root / "after/include"),
                                 "-o", str(self.root / "consumer.o")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        probe = run_namespace_probe(*snapshots, self.artifacts)
        self.assertEqual(probe["outcome"], "fail")
        text = (self.artifacts / probe["source"]["path"]).read_text()
        self.assertIn("::Waylib::Server;", text)
        self.assertNotIn("SERVER_NAMESPACE", text)


if __name__ == "__main__":
    unittest.main()
