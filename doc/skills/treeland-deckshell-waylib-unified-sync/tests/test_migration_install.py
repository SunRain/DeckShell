from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from support import ctest_fixture
from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.contract_migration import MIGRATION_KIND
from unified_sync_lib.contracts import build_install_snapshot, compare_contract_snapshots, _contract_drift
from unified_sync_lib.namespace_probe import run_namespace_probe
from unified_sync_lib.validation_gates import _migration_binding_errors


class MigrationInstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.before_root, self.after_root = self.root / "before", self.root / "after"
        self._install(self.before_root, "Legacy")
        self._install(self.after_root, "Native")
        self.before = build_install_snapshot(self.before_root)
        self.after = build_install_snapshot(self.after_root)
        self.artifacts = self.root / "artifacts"
        self.approval = {
            "kind": MIGRATION_KIND, "scope": "installation", "review_state": "approved",
            "reason": "Retire the approved legacy header and publish the native API.",
            "refs_doc": "plan.md", "source_commits": ["a" * 40],
            "before_snapshot_sha256": self.before["snapshot_sha256"],
            "after_snapshot_sha256": self.after["snapshot_sha256"],
            "drift": _contract_drift(self.before, self.after),
            "structural_paths": {}, "namespace_bindings": self.after["namespace_headers"],
        }
        command = ["ctest", "--test-dir", "consumer", "--output-on-failure", "--no-tests=error"]
        self.consumer = {"schema_version": 2, "kind": "waylib-package-consumer-result",
                         "outcome": "pass", "exit_code": 0, "command": command,
                         "cwd": str(self.root)}
        self.consumer.update(ctest_fixture(self.artifacts, "consumer", command, str(self.root)))

    def tearDown(self):
        self.temp.cleanup()

    def _install(self, root, name):
        header = root / "include" / f"{name}.h"
        header.parent.mkdir(parents=True)
        header.write_text("namespace WaylibShared { namespace Server { class API {}; } }\n",
                          encoding="utf-8")
        config = root / "lib/cmake/WaylibShared/WaylibSharedConfig.cmake"
        config.parent.mkdir(parents=True)
        config.write_text("add_library(WaylibShared::SharedServer INTERFACE IMPORTED)\n",
                          encoding="utf-8")

    def compare(self, probe, approval=None, consumer=None):
        return compare_contract_snapshots(
            self.before, self.after, self.consumer if consumer is None else consumer,
            self.artifacts, probe, approved_migration=approval,
        )

    def test_default_fixed_probe_still_rejects_retired_headers(self):
        probe = run_namespace_probe(self.before, self.after, self.artifacts)
        self.assertEqual(probe["outcome"], "fail")
        self.assertEqual(self.compare(probe)["outcome"], "blocked")

    def test_approved_migration_compiles_all_new_namespace_headers(self):
        probe = run_namespace_probe(self.before, self.after, self.artifacts, self.approval)
        result = self.compare(probe, self.approval)
        self.assertEqual(result["outcome"], "pass", result["blocked_reasons"])
        self.assertTrue(result["drift"])
        source = (self.artifacts / probe["source"]["path"]).read_text()
        self.assertIn('"include/Native.h"', source)
        self.assertNotIn("Legacy.h", source)
        self.assertIn("::WaylibShared", source)

    def test_namespace_bindings_cannot_omit_a_new_public_header(self):
        approval = copy.deepcopy(self.approval)
        approval["namespace_bindings"] = {}
        with self.assertRaisesRegex(ValueError, "every candidate namespace header"):
            run_namespace_probe(self.before, self.after, self.artifacts, approval)

    def test_probe_does_not_adapt_to_wrong_namespace_in_the_installed_header(self):
        (self.after_root / "include/Native.h").write_text("namespace Wrong {}\n", encoding="utf-8")
        probe = run_namespace_probe(self.before, self.after, self.artifacts, self.approval)
        self.assertEqual(probe["outcome"], "fail")

    def test_approval_does_not_hide_failed_consumer(self):
        probe = run_namespace_probe(self.before, self.after, self.artifacts, self.approval)
        consumer = {**self.consumer, "outcome": "fail", "exit_code": 8}
        result = self.compare(probe, self.approval, consumer)
        self.assertEqual(result["outcome"], "blocked")
        self.assertIn("package consumer did not pass", result["blocked_reasons"])

    def test_approval_must_cover_the_entire_observed_installation_drift(self):
        probe = run_namespace_probe(self.before, self.after, self.artifacts, self.approval)
        approval = copy.deepcopy(self.approval)
        approval["drift"].pop("public_headers")
        result = self.compare(probe, approval)
        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(any("exact drift" in error for error in result["blocked_reasons"]))

    def test_report_binds_installation_approval_to_ordered_source_approvals(self):
        source_approval = {key: value for key, value in self.approval.items()
                           if key != "namespace_bindings"}
        source_approval["scope"] = "source"
        record = write_artifact(self.artifacts, "source-migration.json", json.dumps(source_approval).encode())
        manifest = {"identity": {"refs_doc": "plan.md"}, "entries": [
            {"source_commit": "a" * 40, "child": {"contract_migration": record}},
        ]}
        audit = {"approved_migration": copy.deepcopy(self.approval)}
        self.assertEqual(_migration_binding_errors(audit, manifest, self.artifacts), [])
        audit["approved_migration"]["source_commits"] = ["b" * 40]
        self.assertTrue(_migration_binding_errors(audit, manifest, self.artifacts))
        self.assertTrue(_migration_binding_errors({}, manifest, self.artifacts))


if __name__ == "__main__":
    unittest.main()
