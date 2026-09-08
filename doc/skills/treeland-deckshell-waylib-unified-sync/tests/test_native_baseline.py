from __future__ import annotations

import contextlib
import copy
import io
import json
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import test_wlroots_verify as wlroots_tests
from support import add_worktree, commit_files, run
from validation_record import main as record_main
from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.git_ops import read_json
from unified_sync_lib.native_validation import native_absence_errors
from unified_sync_lib.replay import run_replay
from unified_sync_lib.validation_gates import validation_errors


class NativeBaselineTests(unittest.TestCase):
    def setUp(self):
        self.case = wlroots_tests.ThreeRepositoryTests()
        self.case.setUp()
        self.addCleanup(self.case.tearDown)

    def prepare(self, empty=True, source_absent=True, wrapper_only=False):
        case = self.case
        self.nonempty_base = case.rb
        if source_absent:
            case.sb = commit_files(case.source, {"3rdparty/wlroots/core.c": None}, "before native import")
        if empty:
            case.rb = commit_files(case.wlroots, {"core.c": None}, "explicit empty R baseline")
        files = {
            "3rdparty/wlroots/core.c": "int core(void) { return 1; }\n",
            "3rdparty/wlroots/meson.build": "project('native-fixture', 'c')\nlibrary('fixture', 'core.c')\n",
        }
        head = commit_files(case.source, {"wlroots/cmake/vars.cmake": "set(PRIVATE_VALUE 1)\n"} if wrapper_only else files,
                            "linear native import")
        self.request = case.request(head)
        if empty and not source_absent:
            proof = {"source_tree": run(case.source, "rev-parse", case.sb + ":3rdparty/wlroots"),
                     "target_tree": run(case.wlroots, "rev-parse", case.rb + "^{tree}"), "review_state": "approved",
                     "paths": [{"path": "core.c", "reason": "Previously reviewed omission in the initialization baseline."}]}
            self.request.wlroots_baseline_proof = write_artifact(self.request.artifact_root, "baseline.json", json.dumps(proof).encode())
        self.manifest = run_replay(self.request)
        case.verify_lanes(self.request, self.manifest)
        self.base = add_worktree(case.wlroots, case.root / "native-base", "native-base", case.rb)
        self.bundle = self.request.artifact_root / "validations.json"

    def record_native(self, phase, step, expected=0):
        cwd = self.base if phase == "base" else self.request.wlroots_worktree
        build = self.case.root / ("native-build-" + phase)
        command = {
            "configure": ["meson", "setup", str(build), str(cwd), "--wrap-mode=nodownload"],
            "build": ["meson", "compile", "-C", str(build)],
            "test": ["meson", "test", "-C", str(build), "--print-errorlogs"],
        }[step]
        with contextlib.redirect_stderr(io.StringIO()) as errors:
            code = record_main([
                "--id", f"wlroots-{phase}-{step}", "--category", "test" if step == "test" else "build",
                "--cwd", str(cwd), "--artifact-root", str(self.request.artifact_root),
                "--bundle", str(self.bundle), "--manifest", str(self.request.manifest_path), "--", *command,
            ])
        entries = read_json(self.bundle)["entries"] if self.bundle.exists() else []
        entry = next((entry for entry in entries if entry["id"] == f"wlroots-{phase}-{step}"), None)
        log = (self.request.artifact_root / entry["log"]["path"]).read_text(encoding="utf-8") if entry else ""
        self.assertEqual(code, expected, errors.getvalue() + log)
        return entry

    def test_absent_source_and_empty_r_base_skip_only_baseline_commands(self):
        self.prepare()
        for step in ("configure", "build", "test"):
            entry = self.record_native("base", step)
            self.assertEqual(entry["outcome"], "not-applicable", entry)
            self.assertIs(entry["executed"], False)
            self.assertIsNone(entry["exit_code"])
            self.assertNotIn("tests", entry)
        self.assertFalse((self.case.root / "native-build-base").exists())
        for step in ("configure", "build", "test"):
            entry = self.record_native("candidate", step)
            self.assertIn(entry["outcome"], {"pass", "no-tests"}, entry)
        errors = validation_errors(read_json(self.bundle), self.request.artifact_root, self.manifest, {})
        self.assertFalse([error for error in errors if "wlroots" in error or "native" in error], errors)

    def test_nonempty_baseline_without_meson_cannot_claim_not_applicable(self):
        self.prepare(empty=False, source_absent=False)
        entry = self.record_native("base", "configure", expected=2)
        self.assertEqual(entry["outcome"], "fail", entry)
        self.assertNotIn("native_baseline", entry)

    def test_reviewed_empty_r_with_existing_source_subtree_is_not_exempt(self):
        self.prepare(source_absent=False)
        entry = self.record_native("base", "configure", expected=2)
        self.assertEqual(entry["outcome"], "fail", entry)

    def test_empty_candidate_still_requires_real_meson_build(self):
        self.prepare(wrapper_only=True)
        self.assertEqual(self.manifest["final_wlroots_head"], self.case.rb)
        entry = self.record_native("candidate", "configure", expected=2)
        self.assertEqual(entry["outcome"], "fail", entry)

    def test_report_reopens_source_and_r_git_objects_for_absence(self):
        self.prepare()
        entry = self.record_native("base", "configure")
        later = commit_files(self.case.source, {"vendor/note": "after native import\n"}, "later source")
        for mutation in ("source-exists", "r-nonempty", "r-tree-not-commit"):
            with self.subTest(mutation=mutation):
                manifest = copy.deepcopy(self.manifest)
                if mutation == "source-exists":
                    manifest["entries"][0]["source_commit"] = later
                else:
                    manifest["identity"]["wlroots"]["base"] = self.nonempty_base if mutation == "r-nonempty" else entry["native_baseline"]["wlroots_tree"]
                errors = native_absence_errors(entry, self.request.artifact_root, manifest)
                self.assertTrue(errors, mutation)
                result = validation_errors({"schema_version": 2, "kind": "treeland-unified-command-validations",
                                            "entries": [entry]}, self.request.artifact_root, manifest, {})
                self.assertTrue(set(errors).issubset(result), result)

    def test_absence_proof_and_rehashed_log_cannot_be_forged(self):
        self.prepare()
        entry = self.record_native("base", "configure")
        for mutation in ("proof", "log", "executed", "exit-code", "test-counts"):
            with self.subTest(mutation=mutation):
                broken = copy.deepcopy(entry)
                if mutation == "proof":
                    broken["native_baseline"]["source_base"] = self.manifest["entries"][0]["source_commit"]
                elif mutation == "log":
                    broken["log"] = write_artifact(self.request.artifact_root, "forged-proof.json", b'{"reason":"skip"}\n')
                elif mutation == "executed":
                    broken["executed"] = True
                elif mutation == "exit-code":
                    broken["exit_code"] = 0
                else:
                    broken["tests"] = dict(total=0, passed=0, failed=0, skipped=0)
                self.assertTrue(native_absence_errors(broken, self.request.artifact_root, self.manifest), mutation)

    def test_exemption_cannot_cover_candidate_c_or_p_validations(self):
        self.prepare()
        entry = self.record_native("base", "build")
        for name in ("wlroots-candidate-configure", "waylib-base-build", "deckshell-build"):
            with self.subTest(name=name):
                broken = {**entry, "id": name}
                errors = validation_errors({"schema_version": 2, "kind": "treeland-unified-command-validations",
                                            "entries": [broken]}, self.request.artifact_root, self.manifest, {})
                self.assertIn("not-applicable is limited to empty wlroots baseline validations", errors)

    def test_absent_baseline_still_requires_all_three_evidence_records(self):
        self.prepare()
        for step in ("configure", "build", "test"):
            self.record_native("base", step)
        validations = read_json(self.bundle)
        validations["entries"] = [entry for entry in validations["entries"] if entry["id"] != "wlroots-base-test"]
        errors = validation_errors(validations, self.request.artifact_root, self.manifest, {})
        self.assertIn("required validation is missing: wlroots-base-test", errors)

    def test_no_tests_cannot_replace_absent_baseline_evidence(self):
        self.prepare()
        entry = self.record_native("base", "test")
        entry.update(outcome="no-tests", exit_code=0, tests=dict(total=0, passed=0, failed=0, skipped=0))
        errors = validation_errors({"schema_version": 2, "kind": "treeland-unified-command-validations",
                                    "entries": [entry]}, self.request.artifact_root, self.manifest, {})
        self.assertIn("Meson test discovery evidence is missing", errors)


if __name__ == "__main__":
    unittest.main()
