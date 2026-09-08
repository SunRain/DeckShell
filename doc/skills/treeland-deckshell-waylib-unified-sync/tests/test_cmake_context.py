from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from support import add_worktree, commit_files, init_repo
from unified_sync_lib.cmake_syntax import cmake_calls
from unified_sync_lib.contracts import build_source_contract_audit


class CMakeContextTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = init_repo(self.root / "source")

    def audit(self, before, after):
        base = commit_files(self.repo, before, "base")
        head = commit_files(self.repo, after, "candidate")
        return build_source_contract_audit(self.repo, base, head)

    def test_install_condition_matches_actual_cmake_installation(self):
        prefix = "cmake_minimum_required(VERSION 3.21)\nproject(Context NONE)\n"
        install = "install(FILES core.h DESTINATION include)\n"
        result = self.audit({"CMakeLists.txt": prefix + install, "core.h": "namespace Core {}\n"},
                            {"CMakeLists.txt": prefix + "if(FALSE)\n" + install + "endif()\n"})
        installed = []
        for phase, sha in (("base", result["before_commit"]), ("candidate", result["after_commit"])):
            tree = add_worktree(self.repo, self.root / phase, phase, sha)
            build, dest = self.root / (phase + "-build"), self.root / (phase + "-install")
            for command in (["cmake", "-S", str(tree), "-B", str(build), "-G", "Ninja"],
                            ["cmake", "--install", str(build), "--prefix", str(dest)]):
                run = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            installed.append((dest / "include/core.h").exists())
        self.assertEqual(installed, [True, False])
        self.assertEqual(result["outcome"], "blocked", result)
        self.assertIn("cmake_execution_context", result["drift"])

    def test_bare_condition_variable_default_change_blocks(self):
        tail = "if(INSTALL_HEADERS)\ninstall(FILES core.h DESTINATION include)\nendif()\n"
        result = self.audit({"CMakeLists.txt": 'option(INSTALL_HEADERS "Headers" ON)\n' + tail},
                            {"CMakeLists.txt": 'option(INSTALL_HEADERS "Headers" OFF)\n' + tail})
        self.assertEqual(result["outcome"], "blocked", result)
        self.assertIn("contract_variable_definitions", result["drift"])

    def test_condition_controlling_variable_definition_is_protected(self):
        setup = "option(ENABLE_INSTALL \"Install\" ON)\nif(ENABLE_INSTALL)\nset(INSTALL_HEADERS ON)\nendif()\n"
        tail = "if(INSTALL_HEADERS)\ninstall(FILES core.h DESTINATION include)\nendif()\n"
        result = self.audit({"CMakeLists.txt": setup + tail},
                            {"CMakeLists.txt": setup.replace('"Install" ON', '"Install" OFF') + tail})
        self.assertEqual(result["outcome"], "blocked", result)

    def test_moving_variable_definition_under_false_condition_blocks(self):
        tail = "if(INSTALL_HEADERS)\ninstall(FILES core.h DESTINATION include)\nendif()\n"
        result = self.audit({"CMakeLists.txt": "set(INSTALL_HEADERS ON)\n" + tail},
                            {"CMakeLists.txt": "if(FALSE)\nset(INSTALL_HEADERS ON)\nendif()\n" + tail})
        self.assertEqual(result["outcome"], "blocked", result)

    def test_removing_directory_entry_does_not_hide_unchanged_declarations(self):
        result = self.audit({"CMakeLists.txt": "add_subdirectory(waylib)\n",
                             "waylib/CMakeLists.txt": "add_library(Core INTERFACE)\n"},
                            {"CMakeLists.txt": "# directory no longer reached\n"})
        self.assertEqual(result["before_snapshot"]["core_targets"], result["after_snapshot"]["core_targets"])
        self.assertEqual(result["outcome"], "blocked", result)

    def test_removing_helper_invocation_blocks(self):
        helper = "function(install_headers)\ninstall(FILES core.h DESTINATION include)\nendfunction()\n"
        result = self.audit({"CMakeLists.txt": helper + "install_headers()\n"}, {"CMakeLists.txt": helper})
        self.assertEqual(result["outcome"], "blocked", result)

    def test_moving_return_before_public_call_blocks(self):
        install = "install(FILES core.h DESTINATION include)\n"
        result = self.audit({"CMakeLists.txt": install + "return()\n"}, {"CMakeLists.txt": "return()\n" + install})
        self.assertEqual(result["outcome"], "blocked", result)
        self.assertTrue(result["drift"]["cmake_execution_context"]["removed"])

    def test_private_conditions_and_header_syntax_remain_allowed(self):
        prefix = "add_library(Core INTERFACE)\n"
        private = "if(ENABLE_PRIVATE)\ntarget_include_directories(Core PRIVATE private)\nendif()\n"
        result = self.audit({"CMakeLists.txt": prefix + private,
                             "core.h": "namespace Core {}\nstatic_assert(1'000 > 0);\n"},
                            {"CMakeLists.txt": prefix + private.replace("ENABLE_PRIVATE", "OTHER_PRIVATE")})
        self.assertEqual(result["outcome"], "pass", result)

    def test_comments_and_string_arguments_do_not_define_fake_calls(self):
        content = '# install(FILES bad DESTINATION bad)\nmessage("install(FILES bad DESTINATION bad)")\n'
        self.assertEqual(cmake_calls(content, "install"), [])
        self.assertEqual(cmake_calls(content + "install(FILES core.h DESTINATION include)\n", "install"),
                         ["install(FILES core.h DESTINATION include)"])

    def test_bracket_comments_arguments_and_apostrophes_keep_cmake_semantics(self):
        content = "#[=[\ninstall(FILES bad DESTINATION bad)\n]=]\nmessage([[don't parse ) if(FALSE)]])\n"
        self.assertEqual(cmake_calls(content, "install"), [])
        self.assertEqual(cmake_calls(content, "if"), [])
        result = self.audit({"CMakeLists.txt": "add_library(Core INTERFACE)\n"},
                            {"CMakeLists.txt": content + "add_library(Core INTERFACE)\n"})
        self.assertEqual(result["outcome"], "pass", result)


if __name__ == "__main__":
    unittest.main()
