"""原生 Meson 包装层的真实编译、生成头与消费链回归。"""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.wrapper_build import record_wrapper_build, wrapper_build_errors


ROOT_CMAKE = """cmake_minimum_required(VERSION 3.27)
project(native_fixture LANGUAGES C)
cmake_file_api(QUERY API_VERSION 1 CODEMODEL 2)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
add_subdirectory(wlroots)
add_executable(consumer main.c)
target_include_directories(consumer PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/3rdparty/wlroots/include
  ${CMAKE_CURRENT_BINARY_DIR}/wlroots/native/include)
@LINK@
"""

WRAPPER_CMAKE = """set(native "${CMAKE_CURRENT_BINARY_DIR}/native")
execute_process(COMMAND "${CMAKE_COMMAND}" -E env "CC=${CMAKE_C_COMPILER}"
  meson setup "${native}" "${CMAKE_CURRENT_SOURCE_DIR}/../3rdparty/wlroots"
  --wrap-mode=nodownload COMMAND_ERROR_IS_FATAL ANY)
add_custom_target(waylib_wlroots_native ALL
  COMMAND meson compile -C "${native}"
  BYPRODUCTS "${native}/libwlroots-0.19.so")
add_library(NativeLibrary SHARED IMPORTED GLOBAL)
set_target_properties(NativeLibrary PROPERTIES
  IMPORTED_LOCATION "${native}/libwlroots-0.19.so"
  IMPORTED_SONAME "libwlroots-0.19.so")
add_dependencies(NativeLibrary waylib_wlroots_native)
"""


class NativeWrapperTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.child = self.root / "child"
        self.build = self.root / "build"
        self.artifacts = self.root / "artifacts"
        self.manifest = {"fixture": "native-wrapper-provenance"}

    def write(self, relative, text):
        path = self.child / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def build_fixture(self, *, linked=True, generated_used=True):
        link = "target_link_libraries(consumer PRIVATE NativeLibrary)" if linked else ""
        self.write("CMakeLists.txt", ROOT_CMAKE.replace("@LINK@", link))
        self.write("wlroots/CMakeLists.txt", WRAPPER_CMAKE)
        self.write("3rdparty/wlroots/meson.build", """project('native', 'c')
subdir('include/wlr')
shared_library('wlroots-0.19', 'native.c', include_directories: include_directories('include'))
""")
        self.write("3rdparty/wlroots/include/wlr/meson.build", """config = configuration_data()
config.set('NATIVE_VALUE', 7)
configure_file(output: 'config.h', configuration: config)
""")
        self.write("3rdparty/wlroots/include/wlr/native.h", "int native_value(void);\n")
        body = "#include <wlr/config.h>\nint native_value(void) { return NATIVE_VALUE; }\n"
        if not generated_used:
            body = "int native_value(void) { return 7; }\n"
        self.write("3rdparty/wlroots/native.c", body)
        call = "native_value() != NATIVE_VALUE" if linked else "NATIVE_VALUE != 7"
        self.write("main.c", "#include <wlr/native.h>\n#include <wlr/config.h>\n"
                   + "int main(void) { return " + call + "; }\n")
        self.run_command(["cmake", "-S", self.child, "-B", self.build, "-G", "Ninja"])
        self.run_command(["cmake", "--build", self.build])

    def run_command(self, command):
        result = subprocess.run(list(map(str, command)), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def record(self):
        command = ["cmake", "--build", str(self.build)]
        result = record_wrapper_build(command, self.child, self.manifest, self.artifacts,
                                      "waylib-base-build-attempt-1")
        return {"id": "waylib-base-build", "cwd": str(self.child), "command": command,
                "wrapper_build": result}

    def test_native_wrapper_binds_real_sources_generated_headers_and_consumer(self):
        self.build_fixture()
        entry = self.record()
        self.assertEqual(entry["wrapper_build"]["outcome"], "pass", entry)
        self.assertTrue(entry["wrapper_build"]["native_meson"]["generated_headers"])
        self.assertEqual(wrapper_build_errors(entry, self.manifest, self.artifacts), [])

    def test_building_native_library_without_linking_it_is_rejected(self):
        self.build_fixture(linked=False)
        entry = self.record()
        self.assertIn("actual consumer link inputs do not use the native wrapper artifact",
                      entry["wrapper_build"]["blocked_reasons"])

    def test_generated_header_not_used_by_r_compilation_is_rejected(self):
        self.build_fixture(generated_used=False)
        entry = self.record()
        self.assertIn("native wrapper generated headers are absent from R compiler dependencies",
                      entry["wrapper_build"]["blocked_reasons"])

    def test_report_recomputes_system_link_rejection_from_rehashed_commands(self):
        self.build_fixture()
        entry = self.record()
        artifact = entry["wrapper_build"]["artifacts"]["link_commands"]
        commands = (self.artifacts / artifact["path"]).read_bytes()
        changed = commands + b"\ncc -o system-consumer /usr/lib/libwlroots-0.19.so\n"
        entry["wrapper_build"]["artifacts"]["link_commands"] = write_artifact(
            self.artifacts, "wrapper/rehashed-system-link.log", changed)
        self.assertIn("C/P build links system wlroots instead of native candidate R",
                      wrapper_build_errors(entry, self.manifest, self.artifacts))

    def test_report_rejects_native_metadata_from_another_source(self):
        self.build_fixture()
        entry = self.record()
        artifact = entry["wrapper_build"]["native_meson"]["artifacts"]["targets"]
        targets = json.loads((self.artifacts / artifact["path"]).read_text())
        changed = copy.deepcopy(targets)
        for target in changed:
            if target["type"] == "shared library":
                target["defined_in"] = str(self.root / "other/meson.build")
        entry["wrapper_build"]["native_meson"]["artifacts"]["targets"] = write_artifact(
            self.artifacts, "wrapper/rehashed-targets.json", json.dumps(changed).encode())
        errors = wrapper_build_errors(entry, self.manifest, self.artifacts)
        self.assertTrue(any("one R-root Meson wlroots library" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
