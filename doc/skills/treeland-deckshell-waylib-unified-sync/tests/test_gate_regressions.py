from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import test_native_validation as native_tests
import test_replay as replay_tests
import test_three_repo_build as build_tests
import test_wlroots_verify as wlroots_tests
import three_repo_fixture
from support import commit_files, init_repo, run
from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.git_ops import read_json
from unified_sync_lib.inventory import build_unified_inventory
from unified_sync_lib.patches import source_patch
from unified_sync_lib.replay import ReplayBlocked, run_replay
from unified_sync_lib.report import build_sync_report


class GateRegressionTests(unittest.TestCase):
    def fixture(self, cls):
        case = cls()
        case.setUp()
        self.addCleanup(case.tearDown)
        return case

    def adapted_decision(self, root, artifacts, lane, path, before=None):
        preview = init_repo(root / ("preview-" + lane))
        commit_files(preview, {path: before} if before else {"README": "base\n"}, "base")
        proposed = commit_files(preview, {path: "int value = 2;\n"}, "approved adaptation")
        proof = write_artifact(artifacts, lane + "-review.txt", b"Approved only int value = 2.\n")
        return {
            "action": "adapted", "adaptation_notes": ["Use reviewed value 2."],
            "adaptation_patch": write_artifact(artifacts, lane + ".patch", source_patch(preview, proposed, [path])),
            "adaptation_paths": [{"path": path, "kind": "modified" if before else "materialized",
                                  "reason": "Reviewed value 2.", "proof": proof, "review_state": "approved"}],
        }

    def install_hook(self, root, repo, lane, path):
        hooks = root / (lane + "-hooks")
        hooks.mkdir()
        hook = hooks / "pre-commit"
        hook.write_text("#!/bin/sh\n" + f"printf 'int value = 999;\\n' > '{path}'\n"
                        + f"git add -- '{path}'\n", encoding="utf-8")
        hook.chmod(0o700)
        run(repo, "config", "core.hooksPath", str(hooks))

    def test_adapted_parent_and_child_reject_unapproved_committed_blobs(self):
        case = self.fixture(replay_tests.ReplayIntegrationTests)
        sha = commit_files(case.source, {"qwlroots/value.cpp": "source\n", "src/value.cpp": "source\n"}, "source")
        inventory = build_unified_inventory(case.source, case.source_base, sha, case.policy, case.policy_path, set())
        request = case.request(inventory)
        decisions = {}
        for lane, repo, path in (("child", request.child_worktree, "qwlroots/value.cpp"),
                                 ("parent", request.parent_worktree, "compositor/src/value.cpp")):
            decisions[lane] = self.adapted_decision(case.root, request.artifact_root, lane, path)
            self.install_hook(case.root, repo, lane, path)
        request.decisions = {"entries": {sha: decisions}}
        manifest = run_replay(request)
        self.assertEqual(run(request.child_worktree, "show", "HEAD:qwlroots/value.cpp"), "int value = 999;")
        self.assertEqual(run(request.parent_worktree, "show", "HEAD:compositor/src/value.cpp"), "int value = 999;")
        for result in case.verify_lanes(request, manifest):
            self.assertEqual(result["outcome"], "blocked", result)
            self.assertTrue(any("projection" in error for error in result["blocked_reasons"]))

    def test_adapted_r_rejects_unapproved_blob_before_advancing_child(self):
        case = self.fixture(wlroots_tests.ThreeRepositoryTests)
        sha = commit_files(case.source, {"3rdparty/wlroots/core.c": "source\n"}, "source")
        request = case.request(sha)
        decision = self.adapted_decision(case.root, request.artifact_root, "wlroots", "core.c", case.rfiles["core.c"])
        request.decisions = {"entries": {sha: {"wlroots": decision}}}
        self.install_hook(case.root, request.wlroots_worktree, "wlroots", "core.c")
        with self.assertRaisesRegex(ReplayBlocked, "projection"):
            run_replay(request)
        self.assertEqual(run(request.child_worktree, "rev-parse", "HEAD"), case.cb)
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), case.pb)
        with self.assertRaisesRegex(ReplayBlocked, "projection"):
            run_replay(request, resume=True)

    def test_reviewed_r_adaptation_still_replays_and_verifies(self):
        case = self.fixture(wlroots_tests.ThreeRepositoryTests)
        sha = commit_files(case.source, {"3rdparty/wlroots/core.c": "source\n"}, "source")
        request = case.request(sha)
        decision = self.adapted_decision(case.root, request.artifact_root, "wlroots", "core.c", case.rfiles["core.c"])
        request.decisions = {"entries": {sha: {"wlroots": decision}}}
        manifest = run_replay(request)
        self.assertEqual(run(request.wlroots_worktree, "show", "HEAD:core.c"), "int value = 2;")
        case.verify_lanes(request, manifest)

    def test_intermediate_conditional_install_blocks_before_parent(self):
        case = self.fixture(replay_tests.ReplayIntegrationTests)
        normal = "add_library(Core INTERFACE)\ninstall(FILES core.h DESTINATION include)\n"
        broken = "add_library(Core INTERFACE)\nif(FALSE)\ninstall(FILES core.h DESTINATION include)\nendif()\n"
        case.assert_intermediate_contract_blocked(normal, broken)

    def test_order_only_wrapper_dependency_fails_build_record(self):
        files = copy.deepcopy(three_repo_fixture.C_FILES)
        files["waylib/CMakeLists.txt"] = files["waylib/CMakeLists.txt"].replace(
            "target_link_libraries(WaylibSharedServer PRIVATE Wlroots::wlroots)",
            "add_dependencies(WaylibSharedServer fixture-wlroots)",
        )
        files["waylib/server.cpp"] = '#include "waylib/server.h"\nint Waylib::Server::value() { return 1; }\n'
        with patch.dict(three_repo_fixture.C_FILES, files, clear=True):
            case = self.fixture(build_tests.ThreeRepositoryBuildTests)
        cwd, build = case.request.child_worktree, case.root / "build"
        case.record("waylib-candidate-configure", "build", cwd,
                    ["cmake", "-S", cwd, "-B", build, "-G", "Ninja", "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON"])
        entry = case.record("waylib-candidate-build", "build", cwd, ["cmake", "--build", build], expected=2)
        self.assertEqual(entry["wrapper_build"]["outcome"], "blocked")
        self.assertTrue(any("link" in error for error in entry["wrapper_build"]["blocked_reasons"]))

    def test_native_list_mode_cannot_reuse_a_previous_pass(self):
        case = self.fixture(native_tests.NativeValidationTests)
        case.configure([("one", 0)])
        code, previous = case.record()
        self.assertEqual(code, 0, previous)
        code, current = case.record(["--list"])
        self.assertEqual(code, 1, current)
        self.assertEqual(current, previous)

    def test_full_report_recomputes_consumer_links_and_current_native_attempt(self):
        native = copy.deepcopy(three_repo_fixture.R_FILES)
        native["meson.build"] += "smoke = executable('smoke', 'smoke.c')\ntest('smoke', smoke)\n"
        native["smoke.c"] = "int main(void) { return 0; }\n"
        with patch.dict(three_repo_fixture.R_FILES, native, clear=True):
            case = self.fixture(build_tests.ThreeRepositoryBuildTests)
        gates, validations = case.gates(case.build_all()), read_json(case.bundle)
        request = case.request
        good = build_sync_report(request.inventory, case.manifest, gates, validations, request.artifact_root)
        self.assertEqual(good["outcome"], "pass", good["blocked_reasons"])
        for mutation in ("wrapper-only-command", "native-list", "native-old-path"):
            with self.subTest(mutation=mutation):
                broken = copy.deepcopy(validations)
                if mutation == "wrapper-only-command":
                    entry = next(row for row in broken["entries"] if row["id"] == "waylib-candidate-build")
                    artifacts = entry["wrapper_build"]["artifacts"]
                    commands = (request.artifact_root / artifacts["link_commands"]["path"]).read_text(encoding="utf-8")
                    own = "\n".join(line for line in commands.splitlines() if "libfixture-wlroots" in line and "-o waylib/" not in line)
                    self.assertIn("libfixture-wlroots", own)
                    artifacts["link_commands"] = write_artifact(request.artifact_root, "own-link.log", own.encode("utf-8"))
                else:
                    entry = next(row for row in broken["entries"] if row["id"] == "wlroots-candidate-test")
                    if mutation == "native-list":
                        entry["command"].append("--list")
                    else:
                        entry["native_log_identity"]["path"] = str(case.root / "r-build-candidate/meson-logs/testlog.json")
                report = build_sync_report(request.inventory, case.manifest, gates, broken, request.artifact_root)
                self.assertEqual(report["outcome"], "blocked", report["blocked_reasons"])


if __name__ == "__main__":
    unittest.main()
