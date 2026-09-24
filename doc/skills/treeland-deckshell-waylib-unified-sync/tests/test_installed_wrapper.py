"""真实离线 CMake install/消费链及旧包、替换产物和缺失来源记录的拒绝回归。"""

import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import three_repo_fixture as fixture
import test_three_repo_build as fixture_case
from unified_sync_lib.git_ops import read_json
from unified_sync_lib.wrapper_build import wrapper_build_errors, record_wrapper_build


class InstalledWrapperTests(unittest.TestCase):
    def setUp(self):
        child = dict(fixture.C_FILES)
        child["wlroots/CMakeLists.txt"] = """
set(R_SOURCE "${CMAKE_CURRENT_SOURCE_DIR}/../3rdparty/wlroots")
set(R_FEATURE 1)
configure_file("${R_SOURCE}/config.h.in" "${CMAKE_CURRENT_BINARY_DIR}/include/wlr/config.h" @ONLY)
add_library(waylib_wlroots_native_library SHARED "${R_SOURCE}/core.c")
add_library(Wlroots::wlroots ALIAS waylib_wlroots_native_library)
set_target_properties(waylib_wlroots_native_library PROPERTIES EXPORT_NAME waylib-wlroots INSTALL_RPATH "$ORIGIN")
target_include_directories(waylib_wlroots_native_library PUBLIC
  "$<BUILD_INTERFACE:${R_SOURCE}/include>" "$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/include>"
  "$<INSTALL_INTERFACE:include>")
install(TARGETS waylib_wlroots_native_library EXPORT WaylibSharedTargets LIBRARY DESTINATION lib)
install(DIRECTORY "${R_SOURCE}/include/" "${CMAKE_CURRENT_BINARY_DIR}/include/" DESTINATION include)
"""
        parent = dict(fixture.P_FILES)
        parent["CMakeLists.txt"] = """cmake_minimum_required(VERSION 3.21)
project(InstalledParent LANGUAGES C CXX)
option(WITH_SUBMODULE_WAYLIB "embedded" OFF)
find_package(WaylibShared REQUIRED)
add_subdirectory(compositor)
"""
        parent["compositor/CMakeLists.txt"] = """add_executable(test_compositor main.cpp)
target_link_libraries(test_compositor PRIVATE WaylibShared::SharedServer WaylibShared::waylib-wlroots)
"""
        parent["compositor/main.cpp"] = '#include <wlr/native.h>\n#include <wlr/config.h>\nint main() { return R_FEATURE < 0; }\n'
        native = dict(fixture.R_FILES)
        native["include/wlr/native.h"] = "#pragma once\nint core(void);\n"
        native["core.c"] = "#include <wlr/config.h>\nint core(void) { return R_FEATURE; }\n"
        with patch.dict(fixture.C_FILES, child, clear=True), patch.dict(fixture.P_FILES, parent, clear=True), patch.dict(fixture.R_FILES, native, clear=True):
            self.case = fixture_case.ThreeRepositoryBuildTests()
            self.case.setUp()
        self.addCleanup(self.case.tearDown)
        c = self.case
        self.cbuild, self.prefix, self.pbuild = (c.root / n for n in ("cbuild", "installed", "pbuild"))
        cw, pw = c.request.child_worktree, c.request.parent_worktree
        c.record("waylib-candidate-configure", "build", cw, ["cmake", "-S", cw, "-B", self.cbuild, "-G", "Ninja", "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON"])
        c.record("waylib-candidate-build", "build", cw, ["cmake", "--build", self.cbuild])
        c.record("waylib-candidate-install", "build", cw, ["cmake", "--install", self.cbuild, "--prefix", self.prefix])
        c.record("deckshell-configure", "build", pw, ["cmake", "-S", pw, "-B", self.pbuild, "-G", "Ninja", "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON", "-DCMAKE_PREFIX_PATH=" + str(self.prefix)])
        self.entry = c.record("deckshell-build", "build", pw, ["cmake", "--build", self.pbuild])

    def errors(self, entry=None):
        c = self.case
        return wrapper_build_errors(entry or self.entry, c.manifest, c.request.artifact_root)

    def test_installed_consumer_uses_current_libraries_and_generated_headers(self):
        self.assertEqual(self.errors(), [])
        self.assertTrue(self.entry["wrapper_build"]["installed_package"]["generated_headers"])

    def test_replaced_installed_library_is_rejected(self):
        record = self.entry["wrapper_build"]["installed_package"]["libraries"]["WaylibSharedServer"]
        with Path(record["installed"]).open("ab") as stream:
            stream.write(b"changed-library")
        self.assertIn("ELF differs", " ".join(self.errors()))

    def test_replaced_generated_header_is_rejected(self):
        (self.prefix / "include/wlr/config.h").write_text("#define R_FEATURE 99\n")
        self.assertIn("header differs", " ".join(self.errors()))

    def test_missing_candidate_install_record_is_rejected(self):
        c = self.case
        bundle = read_json(c.bundle)
        bundle["entries"] = [row for row in bundle["entries"] if row["id"] != "waylib-candidate-install"]
        with self.assertRaisesRegex(ValueError, "requires one waylib-candidate-install"):
            record_wrapper_build(self.entry["command"], c.request.parent_worktree, c.manifest,
                                 c.request.artifact_root, "deckshell-build-attempt-2", bundle)

    def test_source_manifest_identity_mismatch_is_rejected(self):
        altered = copy.deepcopy(self.case.manifest)
        altered["final_child_head"] = "a" * 40
        errors = wrapper_build_errors(self.entry, altered, self.case.request.artifact_root)
        self.assertTrue(any("binding mismatch" in error for error in errors), errors)
