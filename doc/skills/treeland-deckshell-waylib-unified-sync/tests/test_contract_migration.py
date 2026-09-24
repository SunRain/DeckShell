from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from support import add_worktree, commit_files, init_repo, run, write_policy
from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.contract_migration import (
    MIGRATION_KIND, migration_shape_errors,
)
from unified_sync_lib.contracts import build_source_contract_audit
from unified_sync_lib.evidence import verify_waylib_sync
from unified_sync_lib.git_ops import read_json
from unified_sync_lib.inventory import build_unified_inventory
from unified_sync_lib.parent_verify import verify_parent_sync
from unified_sync_lib.patches import tree_entry
from unified_sync_lib.policy import load_policy
from unified_sync_lib.replay import ReplayBlocked, ReplayRequest, run_replay
from unified_sync_lib.traces import build_waylib_traces


class ContractMigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = init_repo(self.root / "source")
        self.child = init_repo(self.root / "child")
        self.parent = init_repo(self.root / "parent")
        old = "add_library(Legacy INTERFACE)\n"
        self.sb = commit_files(self.source, {
            "waylib/CMakeLists.txt": old, "src/app.cpp": "old app\n",
        }, "source baseline")
        self.cb = commit_files(self.child, {
            "CMakeLists.txt": "add_subdirectory(waylib)\n",
            "waylib/CMakeLists.txt": old, "test_project/main.cpp": "old consumer\n",
        }, "child baseline")
        commit_files(self.parent, {
            "CMakeLists.txt": "add_subdirectory(qtwaylandscanner)\n",
            "compositor/src/app.cpp": "old app\n",
            "compositor/src/CMakeLists.txt": "add_library(shell INTERFACE)\n",
            "compositor/src/core/qml/PrelaunchSplash.qml": "import Waylib.Server 1.0\n",
            "compositor/tests/local.cpp": "old fixture\n",
        }, "parent baseline")
        run(self.parent, "update-index", "--add", "--cacheinfo",
            f"160000,{self.cb},3rdparty/waylib-shared")
        run(self.parent, "commit", "-m", "parent gitlink")
        self.pb = run(self.parent, "rev-parse", "HEAD")
        self.sh = commit_files(self.source, {
            "waylib/CMakeLists.txt": "add_library(Native INTERFACE)\n",
            "src/app.cpp": "native app\n",
        }, "migrate to native API")
        policy = write_policy(self.root / "policy.md")
        self.inventory = build_unified_inventory(
            self.source, self.sb, self.sh, load_policy(policy), policy, set()
        )
        self.artifacts = self.root / "artifacts"

    def tearDown(self):
        self.temp.cleanup()

    def _decision(self, preview, base, head, paths, extra, lane):
        content = subprocess.check_output([
            "git", "-C", str(preview), "diff", "--binary", base, head,
        ])
        proof = write_artifact(self.artifacts, f"{lane}-review.txt",
                               b"Reviewed native API migration and its existing local callers.\n")
        return {
            "action": "adapted", "structural_paths": extra,
            "adaptation_notes": ["Migrate the explicitly approved API and local callers."],
            "adaptation_patch": write_artifact(self.artifacts, f"{lane}.patch", content),
            "adaptation_paths": [
                {"path": path, "kind": "modified" if tree_entry(preview, base, path)
                 else "materialized", "review_state": "approved",
                 "reason": "Existing caller follows the approved native API.", "proof": proof}
                for path in paths + extra
            ],
        }

    def _prepare_parent(self, runtime_install, protocol_integration, prelaunch_import):
        """Prepare only the explicitly selected integration paths."""
        parent = add_worktree(self.parent, self.root / "p-preview", "p-preview", self.pb)
        changes = {"compositor/src/app.cpp": "native app\n",
                   "compositor/tests/local.cpp": "native fixture\n"}
        parent_paths = ["compositor/tests/local.cpp"]
        if runtime_install:
            changes["compositor/src/CMakeLists.txt"] = (
                "add_library(shell INTERFACE)\ninstall(TARGETS shell)\n")
            parent_paths.append("compositor/src/CMakeLists.txt")
        if protocol_integration:
            for path in ("CMakeLists.txt", "qtwaylandscanner/CMakeLists.txt",
                         "qtwaylandscanner/qtwaylandscanner.cpp",
                         "protocols/compositor/CMakeLists.txt",
                         "protocols/compositor/xml/treeland-remote-subsurface-unstable-v1.xml",
                         "protocols/compositor/xml/treeland-app-id-resolver-v1.xml",
                         "protocols/compositor/xml/treeland-app-id-resolver-unstable-v2.xml",
                         "protocols/compositor/xml/treeland-prelaunch-splash-v2.xml",
                         "protocols/compositor/xml/treeland-prelaunch-splash-unstable-v2.xml",
                         "protocols/compositor/xml/treeland-screensaver-v1.xml",
                         "protocols/compositor/xml/treeland-screensaver-unstable-v2.xml",
                         "protocols/compositor/xml/treeland-wallpaper-shell-unstable-v1.xml",
                         "protocols/compositor/xml/treeland-wine-window-management-unstable-v1.xml",
                         "protocols/compositor/xml/treeland-wine-window-state-unstable-v1.xml",
                         "protocols/compositor/xml/treeland-window-management-v1.xml",
                         "protocols/compositor/xml/treeland-show-desktop-unstable-v1.xml",
                         "protocols/compositor/xml/treeland-foreign-toplevel-manager-v1.xml",
                         "protocols/compositor/xml/treeland-foreign-toplevel-manager-unstable-v2.xml",
                         ):
                changes[path] = "reviewed scanner/protocol integration\n"
                parent_paths.append(path)
        if prelaunch_import:
            path = "compositor/src/core/qml/PrelaunchSplash.qml"
            changes[path] = "import WaylibShared.QuickSharedServer 1.0\n"
            parent_paths.append(path)
        ph = commit_files(parent, changes, "review parent")
        return parent, ph, parent_paths

    def prepare(self, runtime_install=False, protocol_integration=False, prelaunch_import=False):
        child = add_worktree(self.child, self.root / "c-preview", "c-preview", self.cb)
        ch = commit_files(child, {"waylib/CMakeLists.txt": "add_library(Native INTERFACE)\n",
                                  "test_project/main.cpp": "native consumer\n"}, "review child")
        audit = build_source_contract_audit(child, self.cb, ch)
        self.assertEqual(audit["outcome"], "blocked")
        parent, ph, parent_paths = self._prepare_parent(
            runtime_install, protocol_integration, prelaunch_import)
        item = self.inventory["commits"][0]
        self.approval = {
            "kind": MIGRATION_KIND, "scope": "source", "review_state": "approved",
            "reason": "Explicitly authorized native API migration.", "refs_doc": "plan.md",
            "source_commits": [self.sh],
            "before_snapshot_sha256": audit["before_snapshot_sha256"],
            "after_snapshot_sha256": audit["after_snapshot_sha256"], "drift": audit["drift"],
            "structural_paths": {"child": ["test_project/main.cpp"],
                                 "parent": parent_paths},
        }
        decisions = {
            "child": self._decision(child, self.cb, ch, item["waylib_shared"]["source_paths"],
                                     self.approval["structural_paths"]["child"], "child"),
            "parent": self._decision(parent, self.pb, ph, item["deckshell"]["target_paths"],
                                      self.approval["structural_paths"]["parent"], "parent"),
        }
        request = ReplayRequest(
            self.source, add_worktree(self.parent, self.root / "p-wt", "sync", self.pb),
            add_worktree(self.child, self.root / "c-wt", "sync", self.cb), self.pb, self.cb,
            self.inventory, self.artifacts, self.artifacts / "journal.json",
            self.artifacts / "manifest.json", self.artifacts / "waylib-evidence.json",
            self.artifacts / "parent-evidence.json", "migration", "plan.md",
            {"entries": {self.sh: decisions}}, True,
        )
        self.bind_approval(request, self.approval)
        return request

    def bind_approval(self, request, approval):
        record = write_artifact(self.artifacts, "migration.json", json.dumps(approval).encode())
        for lane in request.decisions["entries"][self.sh].values():
            lane["contract_migration"] = record

    def verify_child(self, request, manifest):
        evidence = read_json(request.waylib_evidence_path)
        traces = build_waylib_traces(request.child_worktree, self.cb,
                                     manifest["final_child_head"], self.inventory, self.source,
                                     evidence=evidence, artifact_root=self.artifacts)
        return verify_waylib_sync(request.child_worktree, self.cb, manifest["final_child_head"],
                                  self.inventory, traces, evidence,
                                  self.artifacts, self.source)

    def test_trace_default_does_not_accept_extra_paths_from_message_markers(self):
        request = self.prepare()
        manifest = run_replay(request)
        traces = build_waylib_traces(request.child_worktree, self.cb, manifest["final_child_head"],
                                     self.inventory, self.source)
        self.assertEqual(traces["outcome"], "blocked")
        self.assertTrue(any("path boundary violation" in reason for reason in traces["blocked_reasons"]))

    def test_explicit_exact_migration_replays_and_independently_verifies_both_lanes(self):
        request = self.prepare(runtime_install=True)
        manifest = run_replay(request)
        child = self.verify_child(request, manifest)
        parent = verify_parent_sync(self.source, request.parent_worktree, self.pb,
                                    manifest["final_parent_head"], self.inventory, manifest,
                                    read_json(request.parent_evidence_path), self.artifacts)
        self.assertEqual(child["outcome"], "pass", child["blocked_reasons"])
        self.assertEqual(parent["outcome"], "pass", parent["blocked_reasons"])
        self.assertIn("contract_migration", manifest["entries"][0]["child"])

    def test_runtime_install_path_requires_explicit_parent_migration_approval(self):
        request = self.prepare(runtime_install=True)
        request.decisions["entries"][self.sh]["parent"].pop("contract_migration")
        with self.assertRaisesRegex(ReplayBlocked, "unauthorized structural paths"):
            run_replay(request)
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.pb)

    def test_exact_scanner_and_protocol_integration_replays_and_verifies(self):
        request = self.prepare(protocol_integration=True)
        manifest = run_replay(request)
        result = verify_parent_sync(self.source, request.parent_worktree, self.pb,
                                    manifest["final_parent_head"], self.inventory, manifest,
                                    read_json(request.parent_evidence_path), self.artifacts)
        self.assertEqual(result["outcome"], "pass", result["blocked_reasons"])

    def test_protocol_integration_without_approval_cannot_advance_parent(self):
        request = self.prepare(protocol_integration=True)
        request.decisions["entries"][self.sh]["parent"].pop("contract_migration")
        with self.assertRaisesRegex(ReplayBlocked, "unauthorized structural paths"):
            run_replay(request)
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.pb)

    def test_exact_prelaunch_import_integration_replays_and_verifies(self):
        request = self.prepare(prelaunch_import=True)
        manifest = run_replay(request)
        result = verify_parent_sync(self.source, request.parent_worktree, self.pb,
                                    manifest["final_parent_head"], self.inventory, manifest,
                                    read_json(request.parent_evidence_path), self.artifacts)
        self.assertEqual(result["outcome"], "pass", result["blocked_reasons"])
        self.assertEqual(run(request.parent_worktree, "show",
                             "HEAD:compositor/src/core/qml/PrelaunchSplash.qml"),
                         "import WaylibShared.QuickSharedServer 1.0")

    def test_prelaunch_import_without_approval_cannot_advance_parent(self):
        request = self.prepare(prelaunch_import=True)
        request.decisions["entries"][self.sh]["parent"].pop("contract_migration")
        with self.assertRaisesRegex(ReplayBlocked, "unauthorized structural paths"):
            run_replay(request)
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.pb)

    def test_protocol_blob_modified_by_hook_is_not_covered_by_path_approval(self):
        request = self.prepare(protocol_integration=True)
        path = "protocols/compositor/xml/treeland-remote-subsurface-unstable-v1.xml"
        hook = self.parent / ".git/hooks/pre-commit"
        hook.write_text(f"#!/bin/sh\nprintf 'not reviewed\\n' >> {path}\ngit add -- {path}\n",
                        encoding="utf-8")
        hook.chmod(0o755)
        manifest = run_replay(request)
        result = verify_parent_sync(self.source, request.parent_worktree, self.pb,
                                    manifest["final_parent_head"], self.inventory, manifest,
                                    read_json(request.parent_evidence_path), self.artifacts)
        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(any("projection" in reason for reason in result["blocked_reasons"]), result)

    def test_missing_migration_does_not_authorize_extra_callers(self):
        request = self.prepare()
        for lane in request.decisions["entries"][self.sh].values():
            lane.pop("contract_migration")
        with self.assertRaisesRegex(ReplayBlocked, "unauthorized structural paths"):
            run_replay(request)
        self.assertEqual(run(request.child_worktree, "rev-parse", "HEAD"), self.cb)

    def test_wrong_source_is_rejected_before_replay(self):
        request = self.prepare()
        self.approval["source_commits"] = ["f" * 40]
        self.bind_approval(request, self.approval)
        with self.assertRaisesRegex(ReplayBlocked, "this source commit"):
            run_replay(request)

    def test_different_plan_is_rejected_before_replay(self):
        request = self.prepare()
        self.approval["refs_doc"] = "other-plan.md"
        self.bind_approval(request, self.approval)
        with self.assertRaisesRegex(ReplayBlocked, "different plan"):
            run_replay(request)

    def test_incomplete_approved_drift_cannot_advance_parent(self):
        request = self.prepare()
        self.approval["drift"] = {}
        self.bind_approval(request, self.approval)
        with self.assertRaisesRegex(ReplayBlocked, "exact drift"):
            run_replay(request)
        self.assertNotEqual(run(request.child_worktree, "rev-parse", "HEAD"), self.cb)
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.pb)

    def test_wrong_snapshot_cannot_advance_parent(self):
        request = self.prepare()
        self.approval["after_snapshot_sha256"] = "1" * 64
        self.bind_approval(request, self.approval)
        with self.assertRaisesRegex(ReplayBlocked, "exact after_snapshot_sha256"):
            run_replay(request)
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.pb)

    def test_wildcards_traversal_and_production_path_expansion_are_rejected(self):
        self.prepare()
        for lane, path in [("child", "test_project/*.cpp"), ("child", "test_project/../.git/config"),
                           ("parent", "compositor/src/unrelated.cpp"),
                           ("parent", "compositor/src/common/CMakeLists.txt"),
                           ("parent", "compositor/src/core/qml/*"),
                           ("parent", "compositor/src/core/qml/Other.qml"),
                           ("parent", "compositor/src/core/qml/PrelaunchSplash.qml.bak"),
                           ("parent", "protocols/compositor/xml/unrelated.xml"),
                           ("parent", "qtwaylandscanner/unrelated.cpp"),
                           ("parent", "/tmp/caller.cpp")]:
            with self.subTest(lane=lane, path=path):
                approval = copy.deepcopy(self.approval)
                approval["structural_paths"][lane] = [path]
                self.assertTrue(migration_shape_errors(approval, "source", self.sh))

    def test_parent_verifier_rejects_missing_approval_even_with_adaptation_markers(self):
        request = self.prepare()
        manifest = run_replay(request)
        evidence = read_json(request.parent_evidence_path)
        evidence["entries"][0]["artifacts"].pop("contract_migration")
        result = verify_parent_sync(self.source, request.parent_worktree, self.pb,
                                    manifest["final_parent_head"], self.inventory, manifest,
                                    evidence, self.artifacts)
        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(any("path expansion" in reason for reason in result["blocked_reasons"]))

    def test_consumer_blob_modified_by_commit_hook_is_not_covered_by_path_approval(self):
        request = self.prepare()
        hook = self.child / ".git/hooks/pre-commit"
        hook.write_text("#!/bin/sh\nprintf 'not reviewed\\n' >> test_project/main.cpp\n"
                        "git add -- test_project/main.cpp\n", encoding="utf-8")
        hook.chmod(0o755)
        manifest = run_replay(request)
        result = self.verify_child(request, manifest)
        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(any("projection" in reason for reason in result["blocked_reasons"]), result)


if __name__ == "__main__":
    unittest.main()
