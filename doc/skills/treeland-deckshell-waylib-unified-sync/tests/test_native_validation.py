from __future__ import annotations

import contextlib
import copy
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from validation_record import main as record_main
from unified_sync_lib.git_ops import read_json
from unified_sync_lib.native_validation import native_evidence_errors, native_path_errors


class NativeValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source, self.build = self.root / "source", self.root / "build"
        self.source.mkdir()
        self.artifacts = self.root / "evidence"
        self.bundle = self.artifacts / "validations.json"

    def tearDown(self):
        self.temp.cleanup()

    def configure(self, tests):
        text = "project('native-fixture')\npython = find_program('python3')\n"
        for name, code in tests:
            text += f"test('{name}', python, args: ['-c', 'raise SystemExit({code})'])\n"
        (self.source / "meson.build").write_text(text, encoding="utf-8")
        result = subprocess.run(["meson", "setup", str(self.build), str(self.source),
                                 "--wrap-mode=nodownload"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def record(self, extra=()):
        with contextlib.redirect_stderr(io.StringIO()) as errors:
            code = record_main([
                "--id", "wlroots-candidate-test", "--category", "test", "--cwd", str(self.source),
                "--artifact-root", str(self.artifacts), "--bundle", str(self.bundle), "--",
                "meson", "test", "-C", str(self.build), "--print-errorlogs", *extra,
            ])
        self.assertTrue(self.bundle.exists(), errors.getvalue())
        return code, read_json(self.bundle)["entries"][0]

    def test_real_native_tests_pass_and_bind_both_logs(self):
        self.configure([("one", 0), ("two", 0)])
        code, entry = self.record()
        self.assertEqual(code, 0, entry)
        self.assertEqual(entry["tests"], dict(total=2, passed=2, failed=0, skipped=0))
        self.assertEqual(native_evidence_errors(entry, self.artifacts), [])
        rows = [json.loads(line) for line in (self.artifacts / entry["native_test_log"]["path"]).read_text().splitlines()]
        self.assertTrue(all(set(row) == {"name", "result", "returncode"} for row in rows))

    def test_native_subset_skips_and_failure_do_not_pass(self):
        for name, cases, extra in (
            ("subset", [("one", 0), ("two", 0)], ["one"]),
            ("skip", [("skip", 77)], []),
            ("fail", [("fail", 1)], []),
        ):
            with self.subTest(name=name):
                self.build = self.root / ("build-" + name)
                self.configure(cases)
                code, entry = self.record(extra)
                self.assertEqual(code, 2, entry)
                self.assertTrue(native_evidence_errors(entry, self.artifacts))

    def test_native_build_paths_must_not_overlap_any_replay_worktree(self):
        entries = {}
        for phase in ("base", "candidate"):
            cwd = self.root / phase
            build = self.root / "parent-wt" / ("r-build-" + phase)
            for step, command in (
                ("configure", ["meson", "setup", str(build), str(cwd), "--wrap-mode=nodownload"]),
                ("build", ["meson", "compile", "-C", str(build)]),
                ("test", ["meson", "test", "-C", str(build)]),
            ):
                entries[f"wlroots-{phase}-{step}"] = {"command": command, "cwd": str(cwd)}
        manifest = {"identity": {"parent_worktree": str(self.root / "parent-wt"),
                                 "child_worktree": str(self.root / "child-wt"),
                                 "wlroots": {"worktree": str(self.root / "candidate")}}}
        self.assertTrue(native_path_errors(entries, manifest))

    def test_retries_use_distinct_logs_and_evidence_rejects_stale_identity(self):
        self.configure([("one", 0)])
        code, before = self.record()
        self.assertEqual(code, 0, before)
        code, after = self.record()
        self.assertEqual(code, 0, after)
        self.assertNotEqual(before["native_log_identity"]["path"], after["native_log_identity"]["path"])
        self.assertEqual(after["previous_attempts"], [before])
        for mutation in ("list", "missing", "old-path", "not-fresh"):
            with self.subTest(mutation=mutation):
                broken = copy.deepcopy(after)
                if mutation == "list":
                    broken["command"].append("--list")
                elif mutation == "missing":
                    broken.pop("native_log_identity")
                elif mutation == "old-path":
                    broken["native_log_identity"] = before["native_log_identity"]
                else:
                    broken["native_log_identity"]["existed_before"] = True
                self.assertTrue(native_evidence_errors(broken, self.artifacts))

    def test_preexisting_attempt_log_is_not_overwritten_or_reused(self):
        self.configure([("one", 0)])
        code, before = self.record()
        self.assertEqual(code, 0, before)
        next_log = Path(before["native_log_identity"]["path"].replace("attempt-1", "attempt-2"))
        next_log.write_text("unreviewed prior result\n", encoding="utf-8")
        code, after = self.record()
        self.assertEqual(code, 1)
        self.assertEqual(after, before)
        self.assertEqual(next_log.read_text(encoding="utf-8"), "unreviewed prior result\n")


if __name__ == "__main__":
    unittest.main()
