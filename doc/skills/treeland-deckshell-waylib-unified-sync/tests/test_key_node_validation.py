from __future__ import annotations

import contextlib
import copy
import io
import subprocess
import sys
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import test_three_repo_build as build_tests
import three_repo_fixture
from support import add_worktree, run
from unified_sync import main as sync_main
from unified_sync_lib.git_ops import atomic_write_json, read_json
from unified_sync_lib.inventory import build_unified_inventory
from unified_sync_lib.policy import load_policy


BROKEN_PRODUCT = "#error KEY_NODE_PRODUCT_MUST_FAIL\nint main() { return 0; }\n"
FIXED_PRODUCT = "int main() { return 0; } // repaired endpoint\n"
PC = ("prefix=${pcfiledir}/../..\napi_cflags=-DAPI_LEVEL=1\n"
      "Name: WaylibFixture\nDescription: Fixture public flags\nVersion: 1.0\nCflags: ${api_cflags}\n")


class KeyNodeValidationTests(unittest.TestCase):
    def fixture(self, updates=None, source_count=None):
        case = build_tests.ThreeRepositoryBuildTests()
        case.source_updates = updates
        case.source_count = source_count
        self.addCleanup(lambda: case.tearDown() if hasattr(case, "temp") else None)
        case.setUp()
        return case

    def next_segment(self, previous):
        case = build_tests.ThreeRepositoryBuildTests()
        case.root = previous.root / "second-node"
        old, heads = previous.request, previous.manifest
        policy = Path(old.inventory["path_policy"]["path"])
        tip = old.inventory["range"]["source_tip"]
        inventory = build_unified_inventory(old.source_repo, old.inventory["range"]["head"], tip,
                                            load_policy(policy), policy, set(), source_tip=tip)
        artifacts = case.root / "evidence"
        q = replace(old, inventory=inventory, artifact_root=artifacts, run_id="second-node",
                    parent_base=heads["final_parent_head"], child_base=heads["final_child_head"],
                    wlroots_base=heads["final_wlroots_head"],
                    parent_worktree=add_worktree(old.parent_worktree, case.root / "p-wt", "second", heads["final_parent_head"]),
                    child_worktree=add_worktree(old.child_worktree, case.root / "c-wt", "second", heads["final_child_head"]),
                    wlroots_worktree=add_worktree(old.wlroots_repo, case.root / "r-wt", "second", heads["final_wlroots_head"]),
                    journal_path=artifacts / "journal.json", manifest_path=artifacts / "manifest.json",
                    parent_evidence_path=artifacts / "parent-evidence.json", waylib_evidence_path=artifacts / "waylib-evidence.json")
        atomic_write_json(artifacts / "inventory.json", inventory)
        self.assertEqual(sync_main([
            "replay", "--source-repo", str(q.source_repo), "--parent-worktree", str(q.parent_worktree),
            "--child-worktree", str(q.child_worktree), "--parent-base", q.parent_base, "--child-base", q.child_base,
            "--wlroots-repo", str(q.wlroots_repo), "--wlroots-worktree", str(q.wlroots_worktree),
            "--wlroots-base", q.wlroots_base, "--wlroots-target-ref", q.wlroots_target_ref,
            "--wlroots-submodule-url", q.wlroots_submodule_url, "--inventory", str(artifacts / "inventory.json"),
            "--artifact-root", str(artifacts), "--run-id", q.run_id, "--refs-doc", q.refs_doc,
            "--test-allow-ephemeral-artifacts",
        ]), 0)
        case.request, case.manifest = q, read_json(q.manifest_path)
        case.cbase = add_worktree(old.child_worktree, case.root / "c-base", "second-base", q.child_base)
        case.rbase = add_worktree(old.wlroots_repo, case.root / "r-base", "second-base", q.wlroots_base)
        self.assertEqual(sync_main([
            "materialize-child", "--parent-worktree", str(q.parent_worktree), "--child-repo", str(q.child_worktree),
            "--wlroots-repo", str(q.wlroots_repo), "--child-base-worktree", str(case.cbase),
            "--manifest", str(q.manifest_path), "--output", str(artifacts / "materialization.json"),
        ]), 0)
        case.materialization = read_json(artifacts / "materialization.json")
        case.bundle = artifacts / "validations.json"
        return case

    def closeout(self, case, report_path, expected):
        q, m = case.request, case.manifest
        with contextlib.redirect_stderr(io.StringIO()) as errors:
            code = sync_main([
                "closeout", "--parent-repo", str(q.parent_worktree), "--child-repo", str(q.child_worktree),
                "--parent-ref", "refs/heads/target", "--child-ref", "refs/heads/target",
                "--parent-expected-old", q.parent_base, "--child-expected-old", q.child_base,
                "--parent-new", m["final_parent_head"], "--child-new", m["final_child_head"],
                "--wlroots-repo", str(q.wlroots_repo), "--wlroots-ref", "refs/heads/target",
                "--wlroots-expected-old", q.wlroots_base, "--wlroots-new", m["final_wlroots_head"],
                "--report", str(report_path), "--journal", str(case.root / "closeout.json"),
            ])
        self.assertEqual(code, expected, errors.getvalue())
        if expected:
            self.assertIn("complete passing sync report", errors.getvalue())
            for repo, base in ((q.parent_worktree, q.parent_base), (q.child_worktree, q.child_base),
                              (q.wlroots_repo, q.wlroots_base)):
                self.assertEqual(run(repo, "rev-parse", "refs/heads/target"), base)

    def test_intermediate_failure_is_allowed_when_only_the_repaired_endpoint_is_required(self):
        case = self.fixture([{"src/production.cpp": BROKEN_PRODUCT}, {"src/production.cpp": FIXED_PRODUCT}])
        q, m = case.request, case.manifest
        commits = run(q.parent_worktree, "rev-list", "--reverse", q.parent_base + ".." + m["final_parent_head"]).splitlines()
        self.assertEqual(len(commits), 2)
        broken = run(q.parent_worktree, "show", commits[0] + ":compositor/src/production.cpp")
        result = subprocess.run(["c++", "-x", "c++", "-fsyntax-only", "-"], input=broken,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("KEY_NODE_PRODUCT_MUST_FAIL", result.stderr)
        report, path = case.generate_report(case.gates(case.build_all()))
        self.assertEqual(report["build_scope"], {"kind": "range-head-only", "source_head": q.inventory["range"]["head"]})
        self.assertTrue((case.root / "p-build/compositor/DeckCompositor").is_file())
        self.closeout(case, path, expected=0)

    def test_two_frozen_nodes_validate_and_close_out_as_separate_contiguous_segments(self):
        native = three_repo_fixture.R_FILES["core.c"]
        first = self.fixture([
            {"3rdparty/wlroots/core.c": native.replace("return R_FEATURE", "return R_FEATURE + 1")},
            {"3rdparty/wlroots/core.c": native.replace("return R_FEATURE", "return R_FEATURE + 2")},
        ], source_count=1)
        report_one, path_one = first.generate_report(first.gates(first.build_all()))
        self.closeout(first, path_one, expected=0)
        second = self.next_segment(first)
        report_two, path_two = second.generate_report(second.gates(second.build_all()))
        self.assertEqual(second.request.inventory["range"]["base"], report_one["build_scope"]["source_head"])
        self.assertEqual(second.request.parent_base, report_one["final_parent_head"])
        self.assertEqual(second.request.child_base, report_one["final_child_head"])
        self.assertEqual(second.request.wlroots_base, report_one["final_wlroots_head"])
        self.assertNotEqual(path_one, path_two)
        self.assertEqual(report_two["build_scope"]["source_head"], first.request.inventory["range"]["source_tip"])
        self.closeout(second, path_two, expected=0)

    def test_selected_broken_tag_endpoint_blocks_report_and_all_target_refs(self):
        case = self.fixture([{"src/production.cpp": BROKEN_PRODUCT}])
        q = case.request
        run(q.source_repo, "tag", "required-key-node", q.inventory["range"]["head"])
        audit = case.build_all(parent_build_expected=2)
        report, path = case.generate_report(case.gates(audit), expected=2)
        self.assertEqual(report["outcome"], "blocked")
        self.assertTrue(any("deckshell-build=fail" in error for error in report["blocked_reasons"]), report)
        self.closeout(case, path, expected=2)

    def test_old_test_only_record_is_rejected_by_public_report_and_closeout(self):
        case = self.fixture()
        gates = case.gates(case.build_all())
        report, path = case.generate_report(gates)
        report.pop("build_scope")
        atomic_write_json(path, report)
        self.closeout(case, path, expected=2)
        validations = read_json(case.bundle)
        build = next(row for row in validations["entries"] if row["id"] == "deckshell-build")
        build["command"] += ["--target", "test_compositor"]
        atomic_write_json(case.bundle, validations)
        report, path = case.generate_report(gates, expected=2)
        self.assertTrue(any("complete default build" in error for error in report["blocked_reasons"]), report)
        self.closeout(case, path, expected=2)

    def test_pkg_config_variable_drift_blocks_even_when_builds_and_consumer_pass(self):
        files = copy.deepcopy(three_repo_fixture.C_FILES)
        files["waylib/WaylibFixture.pc.in"] = PC
        files["waylib/CMakeLists.txt"] += (
            "\nconfigure_file(WaylibFixture.pc.in WaylibFixture.pc @ONLY)\n"
            'install(FILES "${CMAKE_CURRENT_BINARY_DIR}/WaylibFixture.pc" DESTINATION lib/pkgconfig)\n'
        )
        files["test_project/CMakeLists.txt"] += (
            "\nfind_package(PkgConfig REQUIRED)\n"
            'get_filename_component(FIXTURE_PREFIX "${WaylibShared_DIR}/../../.." ABSOLUTE)\n'
            'set(ENV{PKG_CONFIG_PATH} "${FIXTURE_PREFIX}/lib/pkgconfig")\n'
            "pkg_check_modules(FIXTURE_PC REQUIRED IMPORTED_TARGET WaylibFixture)\n"
            "target_link_libraries(consumer PRIVATE PkgConfig::FIXTURE_PC)\n"
        )
        with patch.dict(three_repo_fixture.C_FILES, files, clear=True):
            case = self.fixture([{"waylib/WaylibFixture.pc.in": PC.replace("API_LEVEL=1", "API_LEVEL=2")}])
        audit = case.build_all(audit_expected=2)
        self.assertEqual(set(audit["drift"]), {"pkg_config"})
        entries = read_json(case.bundle)["entries"]
        self.assertEqual(next(row for row in entries if row["id"] == "deckshell-build")["outcome"], "pass")
        consumer = next(row for row in entries if row["id"] == "waylib-package-consumer")
        self.assertEqual(consumer["tests"], {"total": 1, "passed": 1, "failed": 0, "skipped": 0})
        drift = audit["drift"]["pkg_config"]
        self.assertEqual(drift["before"]["lib/pkgconfig/WaylibFixture.pc"]["Cflags"], "-DAPI_LEVEL=1")
        self.assertEqual(drift["after"]["lib/pkgconfig/WaylibFixture.pc"]["Cflags"], "-DAPI_LEVEL=2")
        report, path = case.generate_report(case.gates(audit), expected=2)
        self.assertEqual(report["outcome"], "blocked")
        self.closeout(case, path, expected=2)


if __name__ == "__main__":
    unittest.main()
