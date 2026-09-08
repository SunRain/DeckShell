from __future__ import annotations

import contextlib
import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from three_repo_fixture import build_fixture
from support import run
from validation_record import main as record_main
from waylib_contract_audit import main as audit_main
from protocol_tracker import main as protocol_main
from generate_sync_report import main as report_main
from unified_sync import main as sync_main
from unified_sync_lib.git_ops import atomic_write_json, read_json
from unified_sync_lib.gitlink import verify_gitlink_consistency
from unified_sync_lib.parent_verify import verify_parent_sync
from unified_sync_lib.report import build_sync_report
from unified_sync_lib.traces import build_waylib_traces
from unified_sync_lib.evidence import verify_waylib_sync
from unified_sync_lib.closeout import closeout_refs, CloseoutBlocked
from unified_sync_lib.materialization import materialize_child_checkout, MaterializationBlocked
from unified_sync_lib.artifacts import write_artifact
from wlroots_verify import main as wlroots_main


class ThreeRepositoryBuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.request, self.manifest, self.materialization, self.cbase, self.rbase = build_fixture(
            self.root, source_updates=getattr(self, "source_updates", None), source_count=getattr(self, "source_count", None))
        self.bundle = self.request.artifact_root / "validations.json"

    def tearDown(self):
        self.temp.cleanup()

    def record(self, name, category, cwd, command, expected=0):
        with contextlib.redirect_stderr(io.StringIO()) as errors:
            code = record_main(["--id", name, "--category", category, "--cwd", str(cwd),
                                "--artifact-root", str(self.request.artifact_root), "--bundle", str(self.bundle),
                                "--manifest", str(self.request.manifest_path), "--", *map(str, command)])
        payload = read_json(self.bundle) if self.bundle.exists() else {}
        log = ""
        if payload.get("entries"):
            entry = payload["entries"][-1]
            log = (self.request.artifact_root / entry["log"]["path"]).read_text(encoding="utf-8")
        self.assertEqual(code, expected, errors.getvalue() + log + json.dumps(payload, indent=2))
        return payload.get("entries", [])[-1] if payload else None

    def build_all(self, parent_build_expected=0, audit_expected=0):
        request = self.request
        for phase, cwd in (("base", self.rbase), ("candidate", request.wlroots_worktree)):
            build = self.root / ("r-build-" + phase)
            prefix = "wlroots-" + phase
            self.record(prefix + "-configure", "build", cwd, ["meson", "setup", build, cwd, "--wrap-mode=nodownload"])
            self.record(prefix + "-build", "build", cwd, ["meson", "compile", "-C", build])
            self.record(prefix + "-test", "test", cwd, ["meson", "test", "-C", build, "--print-errorlogs"])
        for phase, cwd in (("base", self.cbase), ("candidate", request.child_worktree)):
            build, install = self.root / ("c-build-" + phase), self.root / ("install-" + phase)
            prefix = "waylib-" + phase
            self.record(prefix + "-configure", "build", cwd, ["cmake", "-S", cwd, "-B", build, "-G", "Ninja", "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON"])
            self.record(prefix + "-build", "build", cwd, ["cmake", "--build", build])
            self.record(prefix + "-install", "build", cwd, ["cmake", "--install", build, "--prefix", install])
            if phase == "base":
                self.record("waylib-base-ctest", "test", cwd,
                            ["ctest", "--test-dir", build / "waylib", "--output-on-failure", "--no-tests=error"])
        self.record("waylib-ctest", "test", request.child_worktree,
                    ["ctest", "--test-dir", self.root / "c-build-candidate/waylib", "--output-on-failure", "--no-tests=error"])
        cwd, build = request.child_worktree, self.root / "consumer-build"
        self.record("waylib-package-consumer-configure", "build", cwd,
                    ["cmake", "-S", cwd / "test_project", "-B", build, "-G", "Ninja", "-DCMAKE_PREFIX_PATH=" + str(self.root / "install-candidate")])
        self.record("waylib-package-consumer-build", "build", cwd, ["cmake", "--build", build])
        self.record("waylib-package-consumer", "consumer", cwd, ["ctest", "--test-dir", build, "--output-on-failure", "--no-tests=error"])
        cwd, build = request.parent_worktree, self.root / "p-build"
        self.record("deckshell-configure", "build", cwd, ["cmake", "-S", cwd, "-B", build, "-G", "Ninja", "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON"])
        self.record("deckshell-build", "build", cwd, ["cmake", "--build", build], expected=parent_build_expected)
        if parent_build_expected == 0:
            self.record("deckshell-compositor-ctest", "test", cwd, ["ctest", "--test-dir", build / "compositor", "--output-on-failure", "--no-tests=error"])
        output = request.artifact_root / "contract.json"
        arguments = ["--before", str(self.root / "install-base"), "--after", str(self.root / "install-candidate"),
                     "--source-before", str(self.cbase), "--source-after", str(request.child_worktree),
                     "--consumer", str(request.artifact_root / "waylib-package-consumer-result.json"),
                     "--artifact-root", str(request.artifact_root), "--output", str(output)]
        code = audit_main(arguments)
        if request.decisions:
            initial = read_json(output)
            self.assertEqual(code, 2, initial)
            self.assertEqual(set(initial["drift"]), {"source_core_targets", "source_cmake_execution_context"})
            self.assertEqual(initial["drift"]["source_core_targets"], {"removed": [], "added": ["Wlroots::wlroots", "fixture-wlroots"]})
            approval = {key: initial[key] for key in ("before_snapshot_sha256", "after_snapshot_sha256", "drift")}
            approval.update(review_state="approved", installed_paths=[], reason="Reviewed two private wrapper targets and their CMake entry; installed API unchanged.")
            path = request.artifact_root / "install-approval.json"
            atomic_write_json(path, approval)
            code = audit_main([*arguments, "--approved-additions", str(path)])
        self.assertEqual(code, audit_expected, read_json(output))
        return read_json(output)

    def gates(self, audit):
        q, m = self.request, self.manifest
        inventory_path = q.artifact_root / "inventory.json"
        protocol_path = q.artifact_root / "protocols.json"
        atomic_write_json(inventory_path, q.inventory)
        self.assertEqual(protocol_main([
            "--inventory", str(inventory_path), "--parent-repo", str(q.parent_worktree),
            "--manifest", str(q.manifest_path), "--output", str(protocol_path),
        ]), 0)
        rpath, npath = q.artifact_root / "r-verify.json", q.artifact_root / "nested-verify.json"
        self.assertEqual(wlroots_main([
            "--source-repo", str(q.source_repo), "--child-repo", str(q.child_worktree), "--repo", str(q.wlroots_repo),
            "--inventory", str(inventory_path), "--manifest", str(q.manifest_path),
            "--evidence", str(q.wlroots_evidence_path), "--artifact-root", str(q.artifact_root),
            "--output", str(rpath), "--gitlink-output", str(npath),
        ]), 0)
        traces = build_waylib_traces(q.child_worktree, q.child_base, m["final_child_head"], q.inventory, q.source_repo)
        return {
            "wlroots_verify": read_json(rpath), "nested_gitlink_verify": read_json(npath),
            "deckshell_verify": verify_parent_sync(q.source_repo, q.parent_worktree, q.parent_base, m["final_parent_head"], q.inventory, m, read_json(q.parent_evidence_path), q.artifact_root),
            "waylib_verify": verify_waylib_sync(q.child_worktree, q.child_base, m["final_child_head"], q.inventory, traces, read_json(q.waylib_evidence_path), q.artifact_root, q.source_repo),
            "gitlink_verify": verify_gitlink_consistency(q.parent_worktree, q.child_worktree, q.parent_base, q.child_base, m),
            "protocol_tracking": read_json(protocol_path),
            "contract_audit": audit, "child_materialization": self.materialization,
        }

    def test_real_three_repo_build_report_and_partial_closeout_resume(self):
        audit = self.build_all()
        q, m = self.request, self.manifest
        gates, validations = self.gates(audit), read_json(self.bundle)
        report = build_sync_report(q.inventory, m, gates, validations, q.artifact_root)
        self.assertEqual(report["outcome"], "pass", report["blocked_reasons"])
        self.assertIn("NO_TESTS", report["markdown"])
        self.assert_rejects_missing_nested_evidence(gates, validations)
        report, report_path = self.generate_report(gates)
        arguments = dict(parent_repo=q.parent_worktree, child_repo=q.child_worktree,
                         parent_ref="refs/heads/target", child_ref="refs/heads/target",
                         parent_expected_old=q.parent_base, child_expected_old=q.child_base,
                         parent_new=m["final_parent_head"], child_new=m["final_child_head"], report=report,
                         journal_path=self.root / "closeout.json", wlroots_repo=q.wlroots_repo,
                         wlroots_ref="refs/heads/target", wlroots_expected_old=q.wlroots_base, wlroots_new=m["final_wlroots_head"])
        self.assert_closeout_preflight_blocks(arguments)
        def interrupt(stage):
            if stage == "wlroots-ref-written":
                raise RuntimeError("injected interruption after R CAS")
        with self.assertRaisesRegex(CloseoutBlocked, "injected interruption"):
            closeout_refs(**arguments, stage_hook=interrupt)
        self.assertEqual(run(q.wlroots_repo, "rev-parse", "target"), m["final_wlroots_head"])
        self.assertEqual(run(q.child_worktree, "rev-parse", "target"), q.child_base)
        self.assertEqual(sync_main([
            "closeout", "--parent-repo", str(q.parent_worktree), "--child-repo", str(q.child_worktree),
            "--parent-ref", "refs/heads/target", "--child-ref", "refs/heads/target",
            "--parent-expected-old", q.parent_base, "--child-expected-old", q.child_base,
            "--parent-new", m["final_parent_head"], "--child-new", m["final_child_head"],
            "--wlroots-repo", str(q.wlroots_repo), "--wlroots-ref", "refs/heads/target",
            "--wlroots-expected-old", q.wlroots_base, "--wlroots-new", m["final_wlroots_head"],
            "--report", str(report_path), "--journal", str(arguments["journal_path"]), "--resume",
        ]), 0)
        done = read_json(arguments["journal_path"])
        self.assertEqual(done["outcome"], "pass")
        self.assertEqual([e["stage"] for e in done["events"] if e["status"] in {"complete", "recovered"}],
                         ["wlroots-ref-updated", "child-ref-updated", "parent-ref-updated"])
        self.assertEqual(run(q.parent_worktree, "rev-parse", "target"), m["final_parent_head"])

    def test_linear_initial_import_builds_candidate_and_reports_empty_base(self):
        self.root = self.root / "bootstrap"
        self.request, self.manifest, self.materialization, self.cbase, self.rbase = build_fixture(self.root, bootstrap=True)
        self.bundle = self.request.artifact_root / "validations.json"
        audit = self.build_all()
        q, m = self.request, self.manifest
        gates, validations = self.gates(audit), read_json(self.bundle)
        report = build_sync_report(q.inventory, m, gates, validations, q.artifact_root)
        self.assertEqual(report["outcome"], "pass", report["blocked_reasons"])
        absent = [entry for entry in validations["entries"] if entry["outcome"] == "not-applicable"]
        self.assertEqual({entry["id"] for entry in absent},
                         {"wlroots-base-configure", "wlroots-base-build", "wlroots-base-test"})
        self.assertFalse((self.root / "r-build-base").exists())
        self.assertIn("NOT_APPLICABLE", report["markdown"])
        self.assertEqual(gates["wlroots_verify"]["status"], "verified")
        self.assertEqual(gates["nested_gitlink_verify"]["status"], "verified")
        self.generate_report(gates)
        broken = copy.deepcopy(validations)
        candidate = next(entry for entry in broken["entries"] if entry["id"] == "wlroots-candidate-build")
        candidate.update(outcome="not-applicable", executed=False, exit_code=None,
                         native_baseline=absent[0]["native_baseline"])
        report = build_sync_report(q.inventory, m, gates, broken, q.artifact_root)
        self.assertEqual(report["outcome"], "blocked")
        self.assertIn("not-applicable is limited to empty wlroots baseline validations", report["blocked_reasons"])

    def generate_report(self, gates, expected=0):
        root = self.request.artifact_root
        args = ["--inventory", str(root / "inventory.json"), "--manifest", str(self.request.manifest_path),
                "--validations", str(self.bundle), "--artifact-root", str(root),
                "--output", str(root / "report.md"), "--summary-output", str(root / "report.json")]
        for name, gate in gates.items():
            path = root / (name + ".json")
            atomic_write_json(path, gate)
            args.extend(["--" + name.replace("_", "-"), str(path)])
        self.assertEqual(report_main(args), expected)
        return read_json(root / "report.json"), root / "report.json"

    def assert_closeout_preflight_blocks(self, arguments):
        q, m = self.request, self.manifest
        run(q.wlroots_repo, "switch", "target")
        with self.assertRaisesRegex(CloseoutBlocked, "unchecked-out"):
            closeout_refs(**arguments)
        run(q.wlroots_repo, "switch", "main")
        run(q.wlroots_repo, "update-ref", "refs/heads/target", m["final_wlroots_head"], q.wlroots_base)
        with self.assertRaisesRegex(CloseoutBlocked, "moved"):
            closeout_refs(**arguments)
        # Restore fixture setup explicitly; the closeout tool itself must never roll back.
        run(q.wlroots_repo, "update-ref", "refs/heads/target", q.wlroots_base, m["final_wlroots_head"])
        self.assertFalse(arguments["journal_path"].exists())
        self.assertEqual(run(q.child_worktree, "rev-parse", "target"), q.child_base)
        self.assertEqual(run(q.parent_worktree, "rev-parse", "target"), q.parent_base)

    def assert_rejects_missing_nested_evidence(self, gates, validations):
        q, m = self.request, self.manifest
        for label in ("child_base", "child_candidate", "parent_candidate"):
            with self.subTest(materialization=label):
                broken = copy.deepcopy(gates)
                broken["child_materialization"]["wlroots_checkouts"][label] = None
                result = build_sync_report(q.inventory, m, broken, validations, q.artifact_root)
                self.assertEqual(result["outcome"], "blocked", result["blocked_reasons"])
        for name in ("wlroots_verify", "nested_gitlink_verify"):
            with self.subTest(gate=name):
                broken = copy.deepcopy(gates)
                broken[name]["status"] = "not-applicable"
                result = build_sync_report(q.inventory, m, broken, validations, q.artifact_root)
                self.assertEqual(result["outcome"], "blocked")
        for name, content in (("compiler_dependencies", b""), ("link_commands", b"c++ -lwlroots-0.19\n")):
            with self.subTest(wrapper=name):
                broken = copy.deepcopy(validations)
                build = next(row for row in broken["entries"] if row["id"] == "waylib-candidate-build")
                build["wrapper_build"]["artifacts"][name] = write_artifact(q.artifact_root, "bad-wrapper-" + name, content)
                result = build_sync_report(q.inventory, m, gates, broken, q.artifact_root)
                self.assertEqual(result["outcome"], "blocked")

    def test_fresh_build_cannot_be_created_inside_a_replay_worktree(self):
        q = self.request
        build = q.child_worktree / "unapproved-build"
        self.record("waylib-candidate-configure", "build", q.child_worktree,
                    ["cmake", "-S", q.child_worktree, "-B", build, "-G", "Ninja",
                     "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON"], expected=1)
        self.assertFalse(build.exists())

    def test_materialization_idempotence_and_wrong_r_head_are_not_overwritten(self):
        q = self.request
        again = materialize_child_checkout(q.parent_worktree, q.child_worktree, self.manifest, q.wlroots_repo, self.cbase)
        self.assertEqual(again["wlroots_checkouts"], self.materialization["wlroots_checkouts"])
        nested = q.parent_worktree / "3rdparty/waylib-shared/3rdparty/wlroots"
        run(nested, "checkout", "--detach", q.wlroots_base)
        with self.assertRaises(MaterializationBlocked):
            materialize_child_checkout(q.parent_worktree, q.child_worktree, self.manifest, q.wlroots_repo, self.cbase)
        self.assertEqual(run(nested, "rev-parse", "HEAD"), q.wlroots_base)

    def test_command_rejects_missing_r_before_execution_and_detects_r_mutation(self):
        q = self.request
        nested = q.child_worktree / "3rdparty/wlroots"
        marker = self.root / "command-ran"
        run(nested, "checkout", "--detach", q.wlroots_base)
        self.record("waylib-dependency-probe", "build", q.child_worktree,
                    [sys.executable, "-c", f"from pathlib import Path; Path({str(marker)!r}).touch()"], expected=1)
        self.assertFalse(marker.exists())
        run(nested, "checkout", "--detach", self.manifest["final_wlroots_head"])
        self.record("waylib-dependency-probe", "build", q.child_worktree,
                    [sys.executable, "-c", f"from pathlib import Path; Path({str(nested / 'core.c')!r}).write_text('dirty')"], expected=2)


if __name__ == "__main__":
    unittest.main()
