"""限定例外的记录读取测试；合成日志不代表任何产品验证。"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.ctest_results import parse_ctest
from unified_sync_lib.git_ops import canonical_json_sha256
from unified_sync_lib.record_reports import exception_record, check_accepted_results


class RecordExceptionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = {"identity": {"refs_doc": "sample/plan.md"}}
        self.inventory = {"range": {"head": "a" * 40}}
        raw = (b"1/2 Test #1: works ........................ Passed 0.01 sec\n"
               b"2/2 Test #2: test_drm ..................... ***Skipped 0.01 sec\n"
               b"100% tests passed, 0 tests failed out of 2\n")
        parsed = parse_ctest(raw, 0)
        command = ["ctest", "--test-dir", str(self.root / "build"), "--output-on-failure", "--no-tests=error"]
        discovery = {"tests": [{"name": "works"}, {"name": "test_drm"}]}
        self.entry = {"id": "ctest", "attempt": 1, "exit_code": 0, **parsed,
                      "manifest_sha256": canonical_json_sha256(self.manifest), "command": command,
                      "cwd": str(self.root), "log": write_artifact(self.root, "logs/test.log", raw),
                      "test_discovery": {"command": command[:3] + ["--show-only=json-v1"],
                                         "cwd": str(self.root), "exit_code": 0,
                                         "tests": [{"id": 1, "name": "works"}, {"id": 2, "name": "test_drm"}],
                                         "log": write_artifact(self.root, "logs/discovery.json", json.dumps(discovery).encode())}}
        self.validation = {"entries": [self.entry]}
        self.auth = {"kind": "treeland-plan-specific-ctest-skip-exception", "schema_version": 1,
                     "authorization": "synthetic original authorization", "plan": "sample", "node": "N1",
                     "scope": {"source_head": "a" * 40, "validation_id": "ctest", "validation_attempt": 1,
                               "allowed_skips": ["test_drm"]},
                     "evidence": {"raw_ctest_log": "logs/test.log", "full_test_discovery": "logs/discovery.json"},
                     "acceptance": {"status": "authorized-non-blocking-skip", "full_unfiltered_test_set": True,
                                    "drm_behavior_proven": False, "exit_code": 0,
                                    **{"tests_" + k: v for k, v in parsed["tests"].items()}}}

    def read(self, closeout=None):
        bundle = {key: write_artifact(self.root, key + ".json", json.dumps(value).encode())
                  for key, value in {"skip_authorization": self.auth, "inventory": self.inventory,
                                     "manifest": self.manifest, "validations": self.validation}.items()}
        return exception_record(SimpleNamespace(batch="sample"), {"name": "N1"}, self.root,
                                {"skip_exception": bundle}, self.inventory, self.manifest,
                                self.validation, {"outcome": "pass"} if closeout is None else closeout)

    def test_original_fail_and_exact_skip_are_not_rewritten_to_pass(self):
        result = self.read()
        self.assertEqual(self.entry["outcome"], "fail")
        self.assertFalse(result["authorization"]["acceptance"]["drm_behavior_proven"])
        check_accepted_results({}, {"sample": {"outcome": "pass"}}, self.validation, result)

    def test_different_node_authorization_is_rejected(self):
        self.auth["node"] = "N2"
        with self.assertRaisesRegex(ValueError, "其它批次或节点"):
            self.read()

    def test_wrong_attempt_is_rejected(self):
        self.auth["scope"]["validation_attempt"] = 2
        with self.assertRaisesRegex(ValueError, "验证身份"):
            self.read()

    def test_missing_original_log_is_rejected(self):
        (self.root / "logs/test.log").rename(self.root / "saved-test.log")
        with self.assertRaises((OSError, ValueError)):
            self.read()

    def test_unapproved_skip_is_rejected(self):
        self.auth["scope"]["allowed_skips"] = ["other_test"]
        with self.assertRaisesRegex(ValueError, "跳过集合"):
            self.read()

    def test_filtered_command_is_rejected_even_when_filter_would_match_all(self):
        self.entry["command"] += ["-R", ".*"]
        with self.assertRaisesRegex(ValueError, "过滤"):
            self.read()

    def test_exception_does_not_hide_another_validation_failure(self):
        exception = self.read()
        self.validation["entries"].append({"id": "another-test", "outcome": "fail"})
        with self.assertRaisesRegex(ValueError, "未经原授权"):
            check_accepted_results({}, {"sample": {"outcome": "pass"}}, self.validation, exception)


if __name__ == "__main__":
    unittest.main()
