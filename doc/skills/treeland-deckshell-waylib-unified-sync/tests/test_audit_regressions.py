from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from validation_record import _test_result, main as record_main
from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.contracts import _consumer_errors, build_source_contract_audit
from unified_sync_lib.namespace_contract import namespace_contract
from unified_sync_lib.parent_verify import _paths
from unified_sync_lib.protocols import _candidate
from support import commit_files, init_repo, run


class AuditRegressionTests(unittest.TestCase):
    def test_namespace_conditions_empty_macros_and_scoped_keyword_macro(self):
        headers = {
            "qwlroots/qwglobal.h": "#pragma once\n#ifdef QW_NAMESPACE\n"
                "#define QW_BEGIN_NAMESPACE namespace QW_NAMESPACE {\n"
                "#define QW_END_NAMESPACE }\n#else\n#define QW_NAMESPACE\n"
                "#define QW_BEGIN_NAMESPACE\n#define QW_END_NAMESPACE\n#endif\n"
                "QW_BEGIN_NAMESPACE\nnamespace qw {}\nQW_END_NAMESPACE\n",
            "qwlroots/types.h": '#pragma once\n#include "qwglobal.h"\n'
                '#define namespace scope\n#include <external-c-header.h>\n#undef namespace\n',
            "waylib/wglobal.h": '#pragma once\n#include <qwglobal.h>\n'
                '#define SERVER_NAMESPACE Server\n#ifndef SERVER_NAMESPACE\n'
                '#define WAYLIB_SERVER_BEGIN_NAMESPACE\n#define WAYLIB_SERVER_END_NAMESPACE\n'
                '#else\n#define WAYLIB_SERVER_BEGIN_NAMESPACE namespace Waylib { namespace SERVER_NAMESPACE {\n'
                '#define WAYLIB_SERVER_END_NAMESPACE }}\n#endif\n'
                '#if QT_CONFIG(vulkan)\n#define PRIVATE_RENDERER_ENABLED\n#endif\n'
                'WAYLIB_SERVER_BEGIN_NAMESPACE\nclass Object {};\nWAYLIB_SERVER_END_NAMESPACE\n',
            "waylib/object.h": '#pragma once\n#include "wglobal.h"\n'
                'WAYLIB_SERVER_BEGIN_NAMESPACE\nclass Other {};\nWAYLIB_SERVER_END_NAMESPACE\n',
        }
        result = namespace_contract(headers)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["namespaces"], ["Waylib", "Waylib::Server", "qw"])
        self.assertEqual(result["headers"]["waylib/object.h"], ["Waylib", "Waylib::Server"])

    def test_namespace_dependency_macro_expansion_and_unresolved_condition(self):
        header = '#define NAME Core\n#define PUBLIC_NAMESPACE NAME\nnamespace PUBLIC_NAMESPACE {}\n'
        self.assertEqual(namespace_contract({"api.h": header})["namespaces"], ["Core"])
        broken = '#if UNKNOWN_FEATURE(enabled)\nnamespace Hidden {}\n#endif\n'
        self.assertTrue(namespace_contract({"api.h": broken})["errors"])

    def test_ctest_contradictory_success_percentage_is_not_pass(self):
        result = _test_result(b"0% tests passed, 0 tests failed out of 3\n", 0)
        self.assertEqual(result["outcome"], "fail")

    def test_ctest_new_success_summary(self):
        result = _test_result(b"100% tests passed out of 3\n", 0)
        self.assertEqual(result["outcome"], "pass")
        self.assertEqual(result["tests"], dict(total=3, passed=3, failed=0, skipped=0))

    def test_ctest_skip_footer_is_not_counted_twice(self):
        output = (
            b"1/2 Test #1: ok ........... Passed 0.01 sec\n"
            b"2/2 Test #2: demo .........***Skipped 0.01 sec\n"
            b"100% tests passed, 0 tests failed out of 2\n"
            b"The following tests did not run:\n 2 - demo (Skipped)\n"
        )
        self.assertEqual(
            _test_result(output, 0)["tests"],
            dict(total=2, passed=1, failed=0, skipped=1),
        )

    def test_real_consumer_skipped_exit_zero_is_not_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "CTestTestfile.cmake").write_text(
                f'add_test(skipped "{sys.executable}" "-c" "raise SystemExit(77)")\n'
                'set_tests_properties(skipped PROPERTIES SKIP_RETURN_CODE 77)\n',
                encoding="utf-8",
            )
            code = record_main([
                "--id", "waylib-package-consumer", "--category", "consumer",
                "--cwd", str(root), "--artifact-root", str(root / "evidence"),
                "--bundle", str(root / "evidence/validations.json"), "--",
                "ctest", "--test-dir", str(root), "--output-on-failure", "--no-tests=error",
            ])
            self.assertEqual(code, 2)
            entry = json.loads((root / "evidence/waylib-package-consumer-result.json").read_text())
            self.assertEqual(entry["tests"], dict(total=1, passed=0, failed=0, skipped=1))

    def test_ctest_subset_cannot_replace_the_discovered_required_set(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "CTestTestfile.cmake").write_text(
                f'add_test(one "{sys.executable}" "-c" "pass")\n'
                f'add_test(two "{sys.executable}" "-c" "pass")\n', encoding="utf-8",
            )
            common = ["--id", "waylib-package-consumer", "--category", "consumer", "--cwd", str(root),
                      "--artifact-root", str(root / "evidence"), "--bundle", str(root / "evidence/bundle.json"),
                      "--", "ctest", "--test-dir", str(root), "--output-on-failure", "--no-tests=error"]
            self.assertEqual(record_main(common + ["-R", "one"]), 2)
            subset = json.loads((root / "evidence/waylib-package-consumer-result.json").read_text())
            self.assertEqual(subset["exit_code"], 0)
            self.assertTrue(_consumer_errors(subset, root / "evidence"))
            self.assertEqual(record_main(common), 0)
            complete = json.loads((root / "evidence/waylib-package-consumer-result.json").read_text())
            self.assertEqual(_consumer_errors(complete, root / "evidence"), [])

    def test_independent_consumer_audit_rejects_forged_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            consumer = {
                "schema_version": 2, "kind": "waylib-package-consumer-result",
                "command": ["ctest", "--test-dir", str(root), "--output-on-failure", "--no-tests=error"],
                "outcome": "pass", "exit_code": 0,
                "tests": dict(total=1, passed=1, failed=0, skipped=0),
                "log": write_artifact(root, "consumer.log", b"100% tests passed out of 1\n1 - demo (Skipped)\n"),
            }
            self.assertTrue(_consumer_errors(consumer, root))

    def test_copy_old_side_does_not_become_an_actual_parent_change(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = init_repo(Path(directory) / "repo")
            text = "source line\n" * 30
            commit_files(repo, {"src/old.cpp": text}, "base")
            copied = commit_files(repo, {"src/new.cpp": text}, "copy")
            self.assertEqual(_paths(repo, copied), ["src/new.cpp"])

    def test_macro_namespace_change_blocks_adjacent_source_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = init_repo(Path(directory) / "repo")
            header = "#define SERVER_NAMESPACE Server\nnamespace Waylib { namespace SERVER_NAMESPACE { class Object {}; } }\n"
            base = commit_files(repo, {"waylib/src/server/wglobal.h": header}, "base")
            head = commit_files(repo, {"waylib/src/server/wglobal.h": header.replace("Server\n", "Other\n")}, "namespace drift")
            self.assertEqual(build_source_contract_audit(repo, base, head)["outcome"], "blocked")

    def test_empty_xml_candidate_is_not_comparable(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = init_repo(Path(directory) / "protocols")
            commit_files(repo, {"xml/demo.xml": "<protocol/>\n"}, "base")
            (repo / "xml/demo.xml").chmod(0o755)
            run(repo, "add", "xml/demo.xml")
            run(repo, "commit", "-m", "mode only")
            result = _candidate(repo, run(repo, "rev-parse", "HEAD"), "", 0)
            self.assertIsNone(result["similarity"])
            self.assertEqual(result["comparison_status"], "not-comparable")


if __name__ == "__main__":
    unittest.main()
