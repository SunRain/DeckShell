from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from support import commit_files, init_repo
from validation_record import main as record_main
from unified_sync_lib.git_ops import read_json


class RequiredBuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = init_repo(self.root / "source")
        self.build = self.root / "build"
        self.artifacts = self.root / "evidence"
        self.bundle = self.artifacts / "validations.json"
        commit_files(self.source, {
            "CMakeLists.txt": "cmake_minimum_required(VERSION 3.21)\nproject(RequiredBuild LANGUAGES CXX)\n"
                              "add_executable(DeckCompositor production.cpp)\n"
                              "add_executable(test_compositor test.cpp)\n",
            "production.cpp": "#error REQUIRED_PRODUCT_MUST_FAIL\nint main() { return 0; }\n",
            "test.cpp": "int main() { return 0; }\n",
        }, "product failure fixture")
        self.assertEqual(self.record("deckshell-configure", [
            "cmake", "-S", str(self.source), "-B", str(self.build), "-G", "Ninja",
        ])[0], 0)

    def tearDown(self):
        self.temp.cleanup()

    def record(self, name, command):
        with contextlib.redirect_stderr(io.StringIO()) as errors:
            code = record_main([
                "--id", name, "--category", "build", "--cwd", str(self.source),
                "--artifact-root", str(self.artifacts), "--bundle", str(self.bundle), "--", *command,
            ])
        return code, errors.getvalue()

    def test_rejects_test_only_build_before_it_can_hide_product_failure(self):
        code, error = self.record("deckshell-build", [
            "cmake", "--build", str(self.build), "--target", "test_compositor",
        ])
        self.assertEqual(code, 1, error)
        self.assertIn("complete default build", error)
        self.assertFalse((self.build / "test_compositor").exists())
        self.assertEqual([row["id"] for row in read_json(self.bundle)["entries"]], ["deckshell-configure"])

    def test_rejects_help_dry_run_and_native_target_overrides(self):
        for flags in (["--", "-n"], ["--target=help"], ["-ttest_compositor"], ["--", "test_compositor"],
                      ["--help"], ["--resolve-package-references=only"]):
            with self.subTest(flags=flags):
                code, error = self.record("deckshell-build", ["cmake", "--build", str(self.build), *flags])
                self.assertEqual(code, 1, error)
                self.assertIn("complete default build", error)
        self.assertFalse((self.build / "DeckCompositor").exists())

    def test_complete_build_records_the_real_product_failure(self):
        code, error = self.record("deckshell-build", ["cmake", "--build", str(self.build), "--parallel", "2"])
        self.assertEqual(code, 2, error)
        entry = read_json(self.bundle)["entries"][-1]
        self.assertEqual(entry["outcome"], "fail")
        self.assertIn("REQUIRED_PRODUCT_MUST_FAIL", (self.artifacts / entry["log"]["path"]).read_text(encoding="utf-8"))

    def test_complete_build_accepts_parallel_config_and_verbose_options(self):
        commit_files(self.source, {"production.cpp": "int main() { return 0; }\n"}, "repair product")
        code, error = self.record("deckshell-build", [
            "cmake", "--build", str(self.build), "--parallel=2", "--config", "Release", "--verbose",
        ])
        self.assertEqual(code, 0, error)
        self.assertTrue((self.build / "DeckCompositor").is_file())
        self.assertTrue((self.build / "test_compositor").is_file())


if __name__ == "__main__":
    unittest.main()
