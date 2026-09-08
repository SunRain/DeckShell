from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from support import commit_files, init_repo


class InstalledContractIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.artifacts = self.root / "artifacts"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def command(self, *args: str, expected: int = 0) -> str:
        result = subprocess.run(
            list(args), cwd=str(self.root), text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
        )
        self.assertEqual(result.returncode, expected, msg=result.stdout)
        return result.stdout

    def install(self, label: str, subdir: str, comment: str = ""):
        # 两侧 CMake 源码相同，只改变配置值，确保反例确实依赖安装属性求值。
        source = init_repo(self.root / f"source-{label}")
        commit_files(
            source,
            {
                "CMakeLists.txt": (
                    "cmake_minimum_required(VERSION 3.21)\n"
                    "project(WaylibShared LANGUAGES NONE)\n"
                    'set(API_SUBDIR old CACHE STRING "Exported include subdirectory")\n'
                    "add_library(SharedServer INTERFACE)\n"
                    "target_include_directories(SharedServer INTERFACE\n"
                    '  "$<INSTALL_INTERFACE:include/${API_SUBDIR}>")\n'
                    "install(TARGETS SharedServer EXPORT WaylibSharedTargets)\n"
                    "install(EXPORT WaylibSharedTargets NAMESPACE WaylibShared::\n"
                    "  DESTINATION lib/cmake/WaylibShared)\n"
                    "install(FILES WaylibSharedConfig.cmake DESTINATION lib/cmake/WaylibShared)\n"
                    'install(DIRECTORY "include/" DESTINATION include)\n'
                ),
                "WaylibSharedConfig.cmake": (
                    'include("${CMAKE_CURRENT_LIST_DIR}/WaylibSharedTargets.cmake")\n'
                ),
                "include/old/common.h": "#pragma once\ninline int value() { return 7; }\n" + comment,
                "include/new/common.h": "#pragma once\ninline int value() { return 7; }\n" + comment,
                "test_project/CMakeLists.txt": (
                    "cmake_minimum_required(VERSION 3.21)\n"
                    "project(PackageConsumer LANGUAGES CXX)\n"
                    "find_package(WaylibShared CONFIG REQUIRED)\n"
                    "add_executable(consumer main.cpp)\n"
                    "target_link_libraries(consumer PRIVATE WaylibShared::SharedServer)\n"
                    "enable_testing()\nadd_test(NAME consumer COMMAND consumer)\n"
                ),
                "test_project/main.cpp": (
                    "#include <common.h>\nint main() { return value() == 7 ? 0 : 1; }\n"
                ),
            },
            "package fixture",
        )
        build = self.root / f"build-{label}"
        prefix = self.root / f"install-{label}"
        self.command("cmake", "-S", str(source), "-B", str(build), f"-DAPI_SUBDIR={subdir}")
        self.command("cmake", "--build", str(build))
        self.command("cmake", "--install", str(build), "--prefix", str(prefix))
        return source, prefix

    def consume(self, source: Path, prefix: Path) -> None:
        build = self.root / f"consumer-{source.name}"
        self.command(
            "cmake", "-S", str(source / "test_project"), "-B", str(build),
            f"-DCMAKE_PREFIX_PATH={prefix}",
        )
        self.command("cmake", "--build", str(build))
        self.command(
            sys.executable, str(SCRIPTS / "validation_record.py"),
            "--id", "waylib-package-consumer", "--category", "consumer",
            "--cwd", str(source), "--artifact-root", str(self.artifacts),
            "--bundle", str(self.artifacts / "validations.json"), "--",
            "ctest", "--test-dir", str(build), "--output-on-failure", "--no-tests=error",
        )
        evidence = json.loads(
            (self.artifacts / "waylib-package-consumer-result.json").read_text(encoding="utf-8")
        )
        self.assertEqual((evidence["outcome"], evidence["exit_code"]), ("pass", 0))
        log = (self.artifacts / evidence["log"]["path"]).read_text(encoding="utf-8")
        self.assertRegex(log, r"100% tests passed(?:, 0 tests failed)? out of 1\b")

    def audit(self, before, after, status: int):
        output = self.root / "audit.json"
        self.command(
            sys.executable, str(SCRIPTS / "waylib_contract_audit.py"),
            "--before", str(before[1]), "--after", str(after[1]),
            "--source-before", str(before[0]), "--source-after", str(after[0]),
            "--consumer", str(self.artifacts / "waylib-package-consumer-result.json"),
            "--artifact-root", str(self.artifacts), "--output", str(output),
            expected=status,
        )
        return json.loads(output.read_text(encoding="utf-8"))

    def test_public_audit_blocks_include_drift_even_when_both_consumers_pass(self) -> None:
        before = self.install("before", "old")
        after = self.install("after", "new")
        self.consume(*before)
        self.consume(*after)

        result = self.audit(before, after, status=2)

        self.assertEqual(result["outcome"], "blocked")
        self.assertEqual(set(result["drift"]), {"exported_target_properties"})
        drift = result["drift"]["exported_target_properties"]
        target = "WaylibShared::SharedServer"
        self.assertEqual(drift["before"][target]["INTERFACE_INCLUDE_DIRECTORIES"], "<install-root>/include/old")
        self.assertEqual(drift["after"][target]["INTERFACE_INCLUDE_DIRECTORIES"], "<install-root>/include/new")

    def test_public_audit_allows_relocated_prefix_and_noncontract_header_bytes(self) -> None:
        before = self.install("before", "old")
        after = self.install("after", "old", comment="// Package documentation changed.\n")
        self.consume(*after)

        result = self.audit(before, after, status=0)

        self.assertEqual(result["outcome"], "pass")
        self.assertEqual(result["drift"], {})
        self.assertNotEqual(result["before_snapshot_sha256"], result["after_snapshot_sha256"])


if __name__ == "__main__":
    unittest.main()
