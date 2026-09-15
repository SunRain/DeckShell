from __future__ import annotations

import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.contracts import build_install_snapshot, compare_contract_snapshots
from unified_sync_lib.git_ops import read_json
from unified_sync_lib.namespace_probe import run_namespace_probe
from waylib_contract_audit import main as audit_main

from support import commit_files, init_repo, ctest_fixture


class ContractAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.before = self.root / "install-before"
        self.after = self.root / "install-after"
        self._write_install_tree(self.before)
        shutil.copytree(self.before, self.after)
        self.artifacts = self.root / "artifacts"
        self.consumer = {
            "schema_version": 2,
            "kind": "waylib-package-consumer-result",
            "outcome": "pass",
            "command": [
                "ctest",
                "--test-dir",
                "consumer-build",
                "--output-on-failure",
                "--no-tests=error",
            ],
            "exit_code": 0,
            "cwd": str(self.root),
        }

        self.consumer.update(ctest_fixture(self.artifacts, "consumer", self.consumer["command"], str(self.root)))

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _write(self, root: Path, relative: str, content: str) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _write_install_tree(self, root: Path) -> None:
        self._write(
            root,
            "include/waylib/server.h",
            "namespace WaylibShared { class Server {}; }\n",
        )
        self._write(
            root,
            "lib/cmake/WaylibShared/WaylibSharedConfig.cmake",
            "include(${CMAKE_CURRENT_LIST_DIR}/WaylibSharedTargets.cmake)\n",
        )
        self._write(
            root,
            "lib/cmake/WaylibShared/WaylibSharedTargets.cmake",
            "add_library(WaylibShared::SharedServer INTERFACE IMPORTED)\n",
        )
        self._write(
            root,
            "lib/pkgconfig/waylib-shared.pc",
            "includedir=${pcfiledir}/../../include\nName: WaylibShared\nDescription: Fixture package\n"
            "Version: 1.0\nLibs: -lWaylibSharedServer\nCflags: -I${includedir}\n",
        )
        self._write(root, "lib/libWaylibSharedServer.so", "fixture\n")

    def compare(self):
        before = build_install_snapshot(self.before)
        after = build_install_snapshot(self.after)
        probe = run_namespace_probe(before, after, self.artifacts) if "WaylibShared::SharedServer" in after["exported_targets"] else None
        return compare_contract_snapshots(
            before,
            after,
            self.consumer,
            self.artifacts,
            probe,
        )

    def test_accepts_identical_complete_install_contract_with_consumer_proof(self) -> None:
        result = self.compare()

        self.assertEqual(result["outcome"], "pass")
        self.assertEqual(result["drift"], {})

    def test_namespace_probe_compiles_each_header_without_unity_include_collisions(self) -> None:
        for root in (self.before, self.after):
            self._write(root, "include/waylib/seat.h",
                        '#include "server.h"\nnamespace Seat { class API {}; }\n')

        result = self.compare()

        self.assertEqual(result["outcome"], "pass", result["blocked_reasons"])
        self.assertEqual(result["drift"], {})

    def test_namespace_probe_does_not_borrow_a_namespace_from_another_header(self) -> None:
        for root in (self.before, self.after):
            self._write(root, "include/waylib/a_provider.h",
                        "namespace HeaderLocal { class Provider {}; }\n")
        self._write(self.before, "include/waylib/z_client.h",
                    "namespace HeaderLocal { class Client {}; }\n")
        self._write(self.after, "include/waylib/z_client.h", "class Client {};\n")
        before = build_install_snapshot(self.before)
        after = build_install_snapshot(self.after)
        self.assertEqual(before["public_namespaces"], after["public_namespaces"])

        probe = run_namespace_probe(before, after, self.artifacts)

        self.assertEqual(probe["outcome"], "fail")

    def test_blocks_header_config_target_namespace_and_pkgconfig_drift(self) -> None:
        (self.after / "include/waylib/server.h").rename(
            self.after / "include/waylib/server-v2.h"
        )
        (self.after / "lib/cmake/WaylibShared/WaylibSharedConfig.cmake").rename(
            self.after / "lib/cmake/WaylibShared/OtherConfig.cmake"
        )
        self._write(
            self.after,
            "lib/cmake/WaylibShared/WaylibSharedTargets.cmake",
            "add_library(Broken::SharedServer SHARED IMPORTED)\n",
        )
        self._write(
            self.after,
            "lib/pkgconfig/waylib-shared.pc",
            "includedir=${pcfiledir}/../../include\nName: WaylibShared\nDescription: Fixture package\n"
            "Version: 2.0\nLibs: -lBroken\nCflags: -I${includedir}\n",
        )

        result = self.compare()

        self.assertEqual(result["outcome"], "blocked")
        self.assertIn("public_headers", result["drift"])
        self.assertIn("cmake_package_files", result["drift"])
        self.assertIn("exported_targets", result["drift"])
        self.assertIn("export_namespaces", result["drift"])
        self.assertIn("pkg_config", result["drift"])

    def test_blocks_exported_interface_property_drift(self) -> None:
        before_targets = self.before / "lib/cmake/WaylibShared/WaylibSharedTargets.cmake"
        after_targets = self.after / "lib/cmake/WaylibShared/WaylibSharedTargets.cmake"
        before_targets.write_text(
            "add_library(WaylibShared::SharedServer INTERFACE IMPORTED)\n"
            "set_target_properties(WaylibShared::SharedServer PROPERTIES\n"
            "  INTERFACE_INCLUDE_DIRECTORIES \"${_IMPORT_PREFIX}/include/old\")\n",
            encoding="utf-8",
        )
        after_targets.write_text(
            "add_library(WaylibShared::SharedServer INTERFACE IMPORTED)\n"
            "set_target_properties(WaylibShared::SharedServer PROPERTIES\n"
            "  INTERFACE_INCLUDE_DIRECTORIES \"${_IMPORT_PREFIX}/include/new\")\n",
            encoding="utf-8",
        )

        result = self.compare()

        self.assertEqual(result["outcome"], "blocked")
        self.assertIn("exported_target_properties", result["drift"])

    def test_compares_evaluated_exported_properties(self) -> None:
        for root, subdir in ((self.before, "old"), (self.after, "new")):
            self._write(
                root, "lib/cmake/WaylibShared/WaylibSharedTargets.cmake",
                'set(API_SUBDIR "' + subdir + '")\n'
                'add_library(WaylibShared::SharedServer INTERFACE IMPORTED)\n'
                'target_include_directories(WaylibShared::SharedServer INTERFACE\n'
                '  "${CMAKE_CURRENT_LIST_DIR}/../../../include/${API_SUBDIR}")\n',
            )

        result = self.compare()

        self.assertEqual(result["outcome"], "blocked")
        self.assertIn("exported_target_properties", result["drift"])

    def test_exported_properties_ignore_install_prefix_and_comments(self) -> None:
        for root in (self.before, self.after):
            self._write(
                root, "lib/cmake/WaylibShared/WaylibSharedTargets.cmake",
                'add_library(WaylibShared::SharedServer INTERFACE IMPORTED)\n'
                'set_target_properties(WaylibShared::SharedServer PROPERTIES\n'
                f'  INTERFACE_INCLUDE_DIRECTORIES "{root}/include/waylib")\n',
            )
        path = self.after / "lib/cmake/WaylibShared/WaylibSharedTargets.cmake"
        path.write_text(path.read_text() + '# set_property(TARGET Fake PROPERTY INTERFACE_X bad)\n')

        self.assertEqual(self.compare()["outcome"], "pass")

    def test_compares_config_specific_imported_link_interfaces(self) -> None:
        for root, dependency in ((self.before, "OldDependency"), (self.after, "NewDependency")):
            self._write(
                root, "lib/cmake/WaylibShared/WaylibSharedTargets.cmake",
                "add_library(WaylibShared::SharedServer SHARED IMPORTED)\n"
                "set_target_properties(WaylibShared::SharedServer PROPERTIES\n"
                "  IMPORTED_CONFIGURATIONS RELEASE\n"
                f'  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "{dependency}")\n',
            )

        result = self.compare()

        self.assertEqual(result["outcome"], "blocked")
        self.assertIn("exported_target_properties", result["drift"])

    def test_keeps_exported_list_order_and_config_entrypoint_mutations(self) -> None:
        for root, dependencies in ((self.before, "First;Second"), (self.after, "Second;First")):
            self._write(
                root, "lib/cmake/WaylibShared/WaylibSharedConfig.cmake",
                'include("${CMAKE_CURRENT_LIST_DIR}/WaylibSharedTargets.cmake")\n'
                f'set(_public_dependencies "{dependencies}")\n'
                "set_property(TARGET WaylibShared::SharedServer PROPERTY\n"
                '  INTERFACE_LINK_LIBRARIES "${_public_dependencies}")\n',
            )

        result = self.compare()

        self.assertEqual(result["outcome"], "blocked")
        properties = result["drift"]["exported_target_properties"]
        self.assertEqual(
            properties["after"]["WaylibShared::SharedServer"]["INTERFACE_LINK_LIBRARIES"],
            "Second;First",
        )

    def test_invalid_installed_cmake_fails_without_text_scan_fallback(self) -> None:
        self._write(
            self.after, "lib/cmake/WaylibShared/WaylibSharedConfig.cmake",
            'include("${CMAKE_CURRENT_LIST_DIR}/MissingTargets.cmake")\n',
        )

        with self.assertRaisesRegex(ValueError, "CMake target inspection failed"):
            self.compare()

    def test_blocks_private_header_exposure_and_missing_consumer_evidence(self) -> None:
        self._write(
            self.after,
            "include/waylib/private/internal_p.h",
            "namespace WaylibShared::Private { }\n",
        )
        before = build_install_snapshot(self.before)
        after = build_install_snapshot(self.after)

        result = compare_contract_snapshots(before, after, None, self.artifacts)

        self.assertEqual(result["outcome"], "blocked")
        self.assertIn("public_headers", result["drift"])
        self.assertTrue(
            any("consumer" in item for item in result["blocked_reasons"])
        )

    def test_blocks_tampered_consumer_log(self) -> None:
        (self.artifacts / self.consumer["log"]["path"]).write_text("tampered\n", encoding="utf-8")

        result = self.compare()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(any("sha256 mismatch" in item for item in result["blocked_reasons"]))

    def test_scans_complete_source_contract_and_blocks_core_target_drift(self) -> None:
        source_before = self.root / "source-before"
        source_after = self.root / "source-after"
        self._write(
            source_before,
            "qwlroots/CMakeLists.txt",
            "add_library(WaylibSharedServer SHARED server.cpp)\n"
            "install(TARGETS WaylibSharedServer EXPORT WaylibSharedTargets)\n",
        )
        shutil.copytree(source_before, source_after)
        self._write(
            source_after,
            "qwlroots/CMakeLists.txt",
            "add_library(BrokenServer SHARED server.cpp)\n"
            "install(TARGETS WaylibSharedServer EXPORT WaylibSharedTargets)\n",
        )
        before = build_install_snapshot(self.before, source_before)
        after = build_install_snapshot(self.after, source_after)

        result = compare_contract_snapshots(
            before, after, self.consumer, self.artifacts
        )

        self.assertEqual(result["outcome"], "blocked")
        self.assertIn("source_core_targets", result["drift"])

    def test_blocks_child_cmake_preset_contract_drift(self) -> None:
        source_before = self.root / "source-before"
        source_after = self.root / "source-after"
        self._write(
            source_before,
            "qwlroots/CMakePresets.json",
            '{"version": 6, "configurePresets": [{"name": "default"}]}\n',
        )
        shutil.copytree(source_before, source_after)
        self._write(
            source_after,
            "qwlroots/CMakePresets.json",
            '{"version": 6, "configurePresets": [{"name": "changed"}]}\n',
        )

        result = compare_contract_snapshots(
            build_install_snapshot(self.before, source_before),
            build_install_snapshot(self.after, source_after),
            self.consumer,
            self.artifacts,
        )

        self.assertEqual(result["outcome"], "blocked")
        self.assertIn("source_cmake_presets", result["drift"])

    def test_blocks_export_name_and_output_name_contract_drift(self) -> None:
        source_before = self.root / "source-before"
        source_after = self.root / "source-after"
        self._write(
            source_before,
            "waylib/CMakeLists.txt",
            "add_library(WaylibCore SHARED core.cpp)\n"
            "set_target_properties(WaylibCore PROPERTIES EXPORT_NAME Core OUTPUT_NAME waylib)\n",
        )
        shutil.copytree(source_before, source_after)
        self._write(
            source_after,
            "waylib/CMakeLists.txt",
            "add_library(WaylibCore SHARED core.cpp)\n"
            "set_target_properties(WaylibCore PROPERTIES EXPORT_NAME Broken OUTPUT_NAME broken)\n",
        )

        result = compare_contract_snapshots(
            build_install_snapshot(self.before, source_before),
            build_install_snapshot(self.after, source_after),
            self.consumer,
            self.artifacts,
        )

        self.assertEqual(result["outcome"], "blocked")
        self.assertIn("source_target_contract_properties", result["drift"])

    def test_cli_records_frozen_source_worktree_heads(self) -> None:
        source_before = init_repo(self.root / "source-before")
        source_after = init_repo(self.root / "source-after")
        before_head = commit_files(source_before, {"README": "before\n"}, "before")
        after_head = commit_files(source_after, {"README": "after\n"}, "after")
        consumer_path = self.root / "consumer.json"
        consumer_path.write_text(json.dumps(self.consumer), encoding="utf-8")
        output = self.root / "audit.json"

        status = audit_main(
            [
                "--before",
                str(self.before),
                "--after",
                str(self.after),
                "--source-before",
                str(source_before),
                "--source-after",
                str(source_after),
                "--consumer",
                str(consumer_path),
                "--artifact-root",
                str(self.artifacts),
                "--output",
                str(output),
            ]
        )

        result = read_json(output)
        self.assertEqual(status, 0)
        self.assertEqual(
            result["source_commits"], {"before": before_head, "after": after_head}
        )

    def test_cli_rejects_a_dirty_source_worktree(self) -> None:
        source_before = init_repo(self.root / "dirty-source-before")
        source_after = init_repo(self.root / "dirty-source-after")
        commit_files(source_before, {"README": "before\n"}, "before")
        commit_files(source_after, {"README": "after\n"}, "after")
        (source_after / "untracked.txt").write_text("dirty\n", encoding="utf-8")
        consumer_path = self.root / "dirty-consumer.json"
        consumer_path.write_text(json.dumps(self.consumer), encoding="utf-8")
        output = self.root / "dirty-audit.json"

        with contextlib.redirect_stderr(io.StringIO()):
            status = audit_main(
                [
                    "--before",
                    str(self.before),
                    "--after",
                    str(self.after),
                    "--source-before",
                    str(source_before),
                    "--source-after",
                    str(source_after),
                    "--consumer",
                    str(consumer_path),
                    "--artifact-root",
                    str(self.artifacts),
                    "--output",
                    str(output),
                ]
            )

        result = read_json(output)
        self.assertEqual(status, 1)
        self.assertEqual(result["outcome"], "fail")
        self.assertIn("must be clean", result["errors"][0])


if __name__ == "__main__":
    unittest.main()
