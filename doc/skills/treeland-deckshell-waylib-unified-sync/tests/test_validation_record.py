from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from validation_record import _test_result, main
from support import add_worktree, commit_files, init_repo, run


class ValidationRecordTests(unittest.TestCase):
    def test_parses_pass_failure_skip_and_explicit_zero_tests(self) -> None:
        passed = _test_result(b"100% tests passed, 0 tests failed out of 3\n", 0)
        failed = _test_result(b"67% tests passed, 1 tests failed out of 3\n", 8)
        skipped = _test_result(
            b"100% tests passed, 0 tests failed out of 3\n2 - demo (Skipped)\n", 0
        )
        empty = _test_result(b"No tests were found!!!\n", 0)

        self.assertEqual(passed["outcome"], "pass")
        self.assertEqual(failed["outcome"], "fail")
        self.assertEqual(skipped["outcome"], "fail")
        self.assertEqual(empty["outcome"], "no-tests")

    def test_retry_replaces_current_result_and_preserves_prior_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = root / "validations.json"
            common = [
                "--id",
                "retry-probe",
                "--category",
                "build",
                "--cwd",
                str(root),
                "--artifact-root",
                str(root),
                "--bundle",
                str(bundle),
                "--",
                sys.executable,
                "-c",
            ]

            self.assertEqual(main(common + ["raise SystemExit(1)"]), 2)
            self.assertEqual(main(common + ["raise SystemExit(0)"]), 0)

            payload = json.loads(bundle.read_text(encoding="utf-8"))
            self.assertEqual(len(payload["entries"]), 1)
            current = payload["entries"][0]
            self.assertEqual(current["attempt"], 2)
            self.assertEqual(current["outcome"], "pass")
            self.assertEqual(len(current["previous_attempts"]), 1)
            self.assertEqual(current["previous_attempts"][0]["outcome"], "fail")
            self.assertTrue((root / current["log"]["path"]).is_file())
            previous = current["previous_attempts"][0]["log"]["path"]
            self.assertTrue((root / previous).is_file())

    def test_records_git_identity_before_and_after_the_command(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = init_repo(root / "repo")
            head = commit_files(repo, {"README": "fixture\n"}, "fixture")
            bundle = root / "validations.json"

            exit_code = main(
                [
                    "--id",
                    "identity-probe",
                    "--category",
                    "build",
                    "--cwd",
                    str(repo),
                    "--artifact-root",
                    str(root),
                    "--bundle",
                    str(bundle),
                    "--",
                    sys.executable,
                    "-c",
                    "raise SystemExit(0)",
                ]
            )

            entry = json.loads(bundle.read_text(encoding="utf-8"))["entries"][0]
            expected = {"worktree": str(repo.resolve()), "head": head, "clean": True}
            self.assertEqual(exit_code, 0)
            self.assertEqual(entry["git_identity"], {"before": expected, "after": expected})
            self.assertEqual(entry["fresh_paths"], {})

    def test_records_nested_candidate_checkout_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = init_repo(root / "repo")
            base = commit_files(repo, {"README": "base\n"}, "base")
            nested = add_worktree(repo, root / "nested", "nested", base)
            bundle = root / "validations.json"

            exit_code = main(
                [
                    "--id",
                    "nested-probe",
                    "--category",
                    "build",
                    "--cwd",
                    str(repo),
                    "--artifact-root",
                    str(root),
                    "--bundle",
                    str(bundle),
                    "--nested-checkout",
                    str(nested),
                    "--nested-head",
                    base,
                    "--",
                    sys.executable,
                    "-c",
                    "raise SystemExit(0)",
                ]
            )

            entry = json.loads(bundle.read_text(encoding="utf-8"))["entries"][0]
            self.assertEqual(exit_code, 0)
            nested_identity = entry["nested_checkout"]
            self.assertEqual(nested_identity["path"], str(nested.resolve()))
            self.assertEqual(nested_identity["expected_head"], base)
            self.assertEqual(nested_identity["before"]["head"], base)
            self.assertEqual(nested_identity["after"]["head"], base)
            self.assertTrue(nested_identity["before"]["linked_worktree"])
            self.assertTrue(nested_identity["after"]["clean"])

    def test_rejects_wrong_nested_candidate_before_running_command(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = init_repo(root / "repo")
            base = commit_files(repo, {"README": "base\n"}, "base")
            nested = add_worktree(repo, root / "nested", "nested", base)
            bundle = root / "validations.json"

            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                exit_code = main(
                    [
                        "--id",
                        "nested-probe",
                        "--category",
                        "build",
                        "--cwd",
                        str(repo),
                        "--artifact-root",
                        str(root),
                        "--bundle",
                        str(bundle),
                        "--nested-checkout",
                        str(nested),
                        "--nested-head",
                        "f" * 40,
                        "--",
                        sys.executable,
                        "-c",
                        "raise SystemExit(0)",
                    ]
                )

            self.assertEqual(exit_code, 1)
            self.assertFalse(bundle.exists())
            self.assertIn("nested checkout", stderr.getvalue())

    def test_rejects_a_preexisting_required_fresh_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build = root / "existing-build"
            build.mkdir()
            bundle = root / "validations.json"

            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                exit_code = main(
                    [
                        "--id",
                        "deckshell-configure",
                        "--category",
                        "build",
                        "--cwd",
                        str(root),
                        "--artifact-root",
                        str(root),
                        "--bundle",
                        str(bundle),
                        "--",
                        "cmake",
                        "-S",
                        str(root),
                        "-B",
                        str(build),
                    ]
                )

            self.assertEqual(exit_code, 1)
            self.assertFalse(bundle.exists())
            self.assertIn("fresh path", stderr.getvalue())

    def test_records_and_enforces_a_fresh_install_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prefix = root / "fresh-install"
            bundle = root / "validations.json"
            common = [
                "--id",
                "waylib-base-install",
                "--category",
                "build",
                "--cwd",
                str(root),
                "--artifact-root",
                str(root),
                "--bundle",
                str(bundle),
                "--",
                sys.executable,
                "-c",
                "raise SystemExit(0)",
                "--prefix",
                str(prefix),
            ]

            self.assertEqual(main(common), 0)
            entry = json.loads(bundle.read_text(encoding="utf-8"))["entries"][0]
            self.assertEqual(
                entry["fresh_paths"],
                {"--prefix": {"path": str(prefix.resolve()), "existed_before": False}},
            )

            prefix.mkdir()
            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                self.assertEqual(main(common), 1)
            self.assertIn("fresh path", stderr.getvalue())
            self.assertEqual(
                json.loads(bundle.read_text(encoding="utf-8"))["entries"][0]["attempt"],
                1,
            )

    def test_rejects_duplicate_fresh_path_options(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = root / "validations.json"

            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                exit_code = main(
                    [
                        "--id",
                        "deckshell-configure",
                        "--category",
                        "build",
                        "--cwd",
                        str(root),
                        "--artifact-root",
                        str(root),
                        "--bundle",
                        str(bundle),
                        "--",
                        "cmake",
                        "-S",
                        str(root),
                        "-B",
                        str(root / "one"),
                        "-B",
                        str(root / "two"),
                    ]
                )

            self.assertEqual(exit_code, 1)
            self.assertFalse(bundle.exists())
            self.assertIn("fresh path", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
