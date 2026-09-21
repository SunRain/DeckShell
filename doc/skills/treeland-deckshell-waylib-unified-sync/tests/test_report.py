from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.git_ops import canonical_json_sha256
from unified_sync_lib.report import build_sync_report
from unified_sync_lib.namespace_probe import probe_source
from support import ctest_fixture
from pairing_report_fixture import report_pairing


SOURCE_ONE = "1" * 40
SOURCE_TWO = "2" * 40
PARENT_ONE = "3" * 40
CHILD_ONE = "4" * 40


class ReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.inventory = {
            "schema_version": 2,
            "kind": "treeland-deckshell-waylib-unified-inventory",
            "outcome": "pass",
            "source_repo": "/frozen/source",
            "range": {
                "base": "0" * 40,
                "head": SOURCE_TWO,
                "source_tip": SOURCE_TWO,
                "ordered_source_commits": [SOURCE_ONE, SOURCE_TWO],
                "ordered_sha256": hashlib.sha256(
                    f"{SOURCE_ONE}\n{SOURCE_TWO}\n".encode("ascii")
                ).hexdigest(),
                "merge_commits": [],
            },
            "path_policy": {"path": "/frozen/path-policy.md", "sha256": "5" * 64},
            "approved_review": [],
            "child_owned_roots": ["qwlroots", "waylib", "wlroots"],
            "wlroots_owned_root": "3rdparty/wlroots",
            "counts": {
                "deckshell-only": 0,
                "waylib-only": 1,
                "dual": 0,
                "unowned-skip": 1,
                "blocked": 0,
            },
            "blocked_reasons": [],
            "commits": [
                {
                    "source_commit": SOURCE_ONE,
                    "subject": "child",
                    "classification": "waylib-only",
                    "changes": [],
                    "deckshell": {
                        "included": False,
                        "mapped_source_paths": [],
                        "root_source_paths": [],
                        "target_paths": [],
                        "drop_paths": ["waylib/a.cpp"],
                    },
                    "waylib_shared": {
                        "included": True,
                        "source_paths": ["waylib/a.cpp"],
                        "drop_paths": [],
                    },
                    "wlroots": {"included": False, "source_paths": [], "target_paths": [], "drop_paths": []},
                    "protocol_source_paths": [],
                    "protocol_target_paths": [],
                    "blocked_reasons": [],
                },
                {
                    "source_commit": SOURCE_TWO,
                    "subject": "skip",
                    "classification": "unowned-skip",
                    "changes": [],
                    "deckshell": {
                        "included": False,
                        "mapped_source_paths": [],
                        "root_source_paths": [],
                        "target_paths": [],
                        "drop_paths": [],
                    },
                    "waylib_shared": {
                        "included": False,
                        "source_paths": [],
                        "drop_paths": [],
                    },
                    "wlroots": {"included": False, "source_paths": [], "target_paths": [], "drop_paths": []},
                    "protocol_source_paths": [],
                    "protocol_target_paths": [],
                    "blocked_reasons": [],
                },
            ],
        }
        self.manifest = {
            "schema_version": 2,
            "kind": "treeland-unified-sync-manifest",
            "outcome": "pass",
            "identity": {
                "wlroots": None,
                "child_common_git_dir": str(self.root / "child-repo/.git"),
                "parent_common_git_dir": str(self.root / "parent-repo/.git"),
                "parent_base": "7" * 40,
                "child_base": "6" * 40,
                "child_worktree": str((self.root / "child-wt").resolve()),
                "parent_worktree": str((self.root / "parent-wt").resolve()),
            },
            "final_parent_head": PARENT_ONE,
            "final_child_head": CHILD_ONE,
            "final_wlroots_head": None,
            "entries": [
                {
                    "source_commit": SOURCE_ONE,
                    "classification": "waylib-only",
                    "wlroots": {"commit": None, "action": "not-applicable"},
                    "parent": {"commit": PARENT_ONE, "action": "gitlink-only"},
                    "child": {"commit": CHILD_ONE, "action": "applied"},
                    "gitlink": {"status": "updated"},
                },
                {
                    "source_commit": SOURCE_TWO,
                    "classification": "unowned-skip",
                    "wlroots": {"commit": None, "action": "not-applicable"},
                    "parent": {"commit": None, "action": "not-applicable"},
                    "child": {"commit": None, "action": "not-applicable"},
                    "gitlink": {"status": "unchanged"},
                },
            ],
        }
        self.gates = {
            "deckshell_verify": {
                **self.gate("treeland-unified-parent-verify"),
                "inventory_sha256": canonical_json_sha256(self.inventory),
                "manifest_sha256": canonical_json_sha256(self.manifest),
                "target_range": {
                    "base": self.manifest["identity"]["parent_base"],
                    "head": self.manifest["final_parent_head"],
                },
            },
            "waylib_verify": {
                **self.gate("treeland-unified-waylib-verify"),
                "inventory_sha256": canonical_json_sha256(self.inventory),
                "target_range": {
                    "base": self.manifest["identity"]["child_base"],
                    "head": self.manifest["final_child_head"],
                },
            },
            "gitlink_verify": {
                **self.gate("treeland-unified-gitlink-verify"),
                "manifest_sha256": canonical_json_sha256(self.manifest),
                "parent_base": self.manifest["identity"]["parent_base"],
                "child_base": self.manifest["identity"]["child_base"],
                "final_parent_head": self.manifest["final_parent_head"],
                "final_child_head": self.manifest["final_child_head"],
            },
            "protocol_tracking": {
                **self.gate("treeland-unified-protocol-candidates"),
                "inventory_sha256": canonical_json_sha256(self.inventory),
                "manifest_sha256": canonical_json_sha256(self.manifest),
                "parent_context_used": True,
                "advisory": True,
                "entries": [
                    {
                        "source_commit": SOURCE_ONE,
                        "match_status": "ambiguous-candidates",
                        "candidates": [
                            {"commit": "a" * 40, "similarity": 0.91},
                            {"commit": "b" * 40, "similarity": 0.88},
                        ],
                    }
                ],
            },
            "contract_audit": self.gate("waylib-install-contract-audit"),
        }
        for name, kind in (("wlroots_verify", "treeland-unified-wlroots-verify"),
                           ("nested_gitlink_verify", "treeland-unified-nested-gitlink-verify")):
            self.gates[name] = {**self.gate(kind), "status": "not-applicable", "target_range": None,
                                "inventory_sha256": canonical_json_sha256(self.inventory),
                                "manifest_sha256": canonical_json_sha256(self.manifest),
                                "final_child_head": CHILD_ONE, "final_wlroots_head": None}
        self.validations = {
            "schema_version": 2,
            "kind": "treeland-unified-command-validations",
            "entries": [
                self.validation("deckshell-configure", "build"),
                self.validation("deckshell-build", "build"),
                self.validation("deckshell-compositor-ctest", "test", total=3),
                self.validation("waylib-base-configure", "build"),
                self.validation("waylib-base-build", "build"),
                self.validation("waylib-base-install", "build"),
                self.validation("waylib-base-ctest", "test", total=2),
                self.validation("waylib-candidate-configure", "build"),
                self.validation("waylib-candidate-build", "build"),
                self.validation("waylib-candidate-install", "build"),
                self.validation("waylib-ctest", "test", total=2),
                self.validation("waylib-package-consumer-configure", "build"),
                self.validation("waylib-package-consumer-build", "build"),
                self.validation("waylib-package-consumer", "consumer"),
                self.validation(
                    "deckshell-top-level-ctest", "test", outcome="no-tests", total=0
                ),
            ],
        }
        consumer = next(
            item
            for item in self.validations["entries"]
            if item["id"] == "waylib-package-consumer"
        )
        self.gates["contract_audit"]["consumer"] = {
            "schema_version": 2,
            "kind": "waylib-package-consumer-result",
            **consumer,
        }
        self.gates["contract_audit"]["source_commits"] = {
            "before": self.manifest["identity"]["child_base"],
            "after": self.manifest["final_child_head"],
        }
        self.gates["contract_audit"]["source_roots"] = {
            "before": str((self.root / "child-base-wt").resolve()),
            "after": self.manifest["identity"]["child_worktree"],
        }
        self.gates["contract_audit"]["install_roots"] = {
            "before": str((self.root / "install-base").resolve()),
            "after": str((self.root / "install-candidate").resolve()),
        }
        self.gates["contract_audit"]["snapshot_artifacts"] = {}
        self.gates["contract_audit"]["drift"] = {}
        snapshots = {}
        for label in ("before", "after"):
            data = {
                "installed_paths": ["include/waylib/server.h"],
                "file_sha256": {"include/waylib/server.h": "7" * 64},
                "public_headers": ["include/waylib/server.h"],
                "cmake_package_files": [],
                "exported_targets": [],
                "exported_target_properties": {},
                "export_namespaces": [],
                "public_namespaces": ["WaylibShared"],
                "namespace_headers": {"include/waylib/server.h": ["WaylibShared"]},
                "pkg_config": {},
            }
            digest = canonical_json_sha256(data)
            snapshot = {
                "schema_version": 2,
                "kind": "waylib-install-contract-snapshot",
                "install_root": self.gates["contract_audit"]["install_roots"][label],
                "snapshot_sha256": digest,
                **data,
            }
            snapshots[label] = snapshot
            self.gates["contract_audit"][f"{label}_snapshot_sha256"] = digest
            self.gates["contract_audit"]["snapshot_artifacts"][label] = write_artifact(
                self.root,
                f"snapshots/{label}.json",
                (json.dumps(snapshot, sort_keys=True) + "\n").encode("utf-8"),
            )
        self.gates["child_materialization"] = self.materialization()
        self.gates["contract_audit"]["namespace_probe"] = {
            "schema_version": 2, "kind": "waylib-fixed-namespace-probe", "outcome": "pass",
            "snapshots": {label: value["snapshot_sha256"] for label, value in snapshots.items()},
            "source": write_artifact(self.root, "probe.cpp", probe_source(snapshots["before"]).encode()),
            "commands": [{"command": command, "exit_code": 0, "log": write_artifact(self.root, f"probe-{index}.log", b"fixture compile result\n")}
                         for index, command in enumerate((["cmake", "-S", "probe", "-B", "build"], ["cmake", "--build", "build"]))],
        }

        self.gates["protocol_pairing"] = report_pairing(self.inventory, self.manifest, self.validations)
        self.gates["contract_audit"]["consumer"].update(consumer)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def gate(self, kind: str):
        return {
            "schema_version": 2,
            "kind": kind,
            "outcome": "pass",
            "blocked_reasons": [],
        }

    def validation(
        self, validation_id: str, category: str, outcome: str = "pass", total=None
    ):
        log = write_artifact(
            self.root, f"logs/{validation_id}.log", f"{validation_id}\n".encode()
        )
        command = self.validation_command(validation_id)
        result = {
            "id": validation_id,
            "category": category,
            "outcome": outcome,
            "command": command,
            "cwd": self.validation_git_identity(validation_id)["before"]["worktree"],
            "exit_code": 0,
            "log": log,
            "git_identity": self.validation_git_identity(validation_id),
            "fresh_paths": self.validation_fresh_paths(validation_id, command),
        }
        if total is not None:
            result["tests"] = {
                "total": total,
                "passed": total,
                "failed": 0,
                "skipped": 0,
            }
        if validation_id.startswith("deckshell-"):
            nested_path = (self.root / "parent-wt" / "3rdparty/waylib-shared").resolve()
            nested_identity = {
                "worktree": str(nested_path),
                "head": self.manifest["final_child_head"],
                "clean": True,
                "linked_worktree": True,
                "common_git_dir": str(self.root / "child-repo/.git"),
            }
            result["nested_checkout"] = {
                "path": str(nested_path),
                "expected_head": self.manifest["final_child_head"],
                "before": dict(nested_identity),
                "after": dict(nested_identity),
            }
        if category in {"test", "consumer"}:
            result.update(ctest_fixture(self.root, validation_id, command, result["cwd"], total if total is not None else 1))
        return result

    def validation_fresh_paths(self, validation_id: str, command):
        option = None
        if validation_id.endswith("-configure"):
            option = "-B"
        elif validation_id in {"waylib-base-install", "waylib-candidate-install"}:
            option = "--prefix"
        if option is None:
            return {}
        index = command.index(option)
        path = Path(command[index + 1]).resolve()
        return {option: {"path": str(path), "existed_before": False}}

    def validation_git_identity(self, validation_id: str):
        if validation_id.startswith("deckshell-"):
            worktree = self.root / "parent-wt"
            head = PARENT_ONE
        elif validation_id.startswith("waylib-base-"):
            worktree = self.root / "child-base-wt"
            head = self.manifest["identity"]["child_base"]
        else:
            worktree = self.root / "child-wt"
            head = CHILD_ONE
        value = {"worktree": str(worktree.resolve()), "head": head, "clean": True}
        return {"before": value, "after": dict(value)}

    def validation_command(self, validation_id: str):
        paths = {
            "parent-source": self.root / "parent-wt",
            "parent-build": self.root / "parent-build",
            "base-source": self.root / "child-base-wt",
            "base-build": self.root / "base-build",
            "base-install": self.root / "install-base",
            "candidate-source": self.root / "child-wt",
            "candidate-build": self.root / "candidate-build",
            "candidate-install": self.root / "install-candidate",
            "consumer-build": self.root / "consumer-build",
        }
        if validation_id == "deckshell-configure":
            return ["cmake", "-S", str(paths["parent-source"]), "-B", str(paths["parent-build"])]
        if validation_id == "deckshell-build":
            return ["cmake", "--build", str(paths["parent-build"])]
        if validation_id == "deckshell-compositor-ctest":
            return ["ctest", "--test-dir", str(paths["parent-build"] / "compositor"), "--output-on-failure"]
        if validation_id == "deckshell-top-level-ctest":
            return ["ctest", "--test-dir", str(paths["parent-build"]), "--output-on-failure"]
        for prefix, source_key, build_key, install_key in (
            ("waylib-base", "base-source", "base-build", "base-install"),
            ("waylib-candidate", "candidate-source", "candidate-build", "candidate-install"),
        ):
            if validation_id == f"{prefix}-configure":
                return ["cmake", "-S", str(paths[source_key]), "-B", str(paths[build_key])]
            if validation_id == f"{prefix}-build":
                return ["cmake", "--build", str(paths[build_key])]
            if validation_id == f"{prefix}-install":
                return ["cmake", "--install", str(paths[build_key]), "--prefix", str(paths[install_key])]
        if validation_id == "waylib-ctest":
            return ["ctest", "--test-dir", str(paths["candidate-build"] / "waylib"), "--output-on-failure"]
        if validation_id == "waylib-base-ctest":
            return ["ctest", "--test-dir", str(paths["base-build"] / "waylib"), "--output-on-failure"]
        if validation_id == "waylib-package-consumer-configure":
            return [
                "cmake", "-S", str(paths["candidate-source"] / "test_project"),
                "-B", str(paths["consumer-build"]),
                f"-DCMAKE_PREFIX_PATH={paths['candidate-install']}",
            ]
        if validation_id == "waylib-package-consumer-build":
            return ["cmake", "--build", str(paths["consumer-build"])]
        command = ["ctest", "--test-dir", str(paths["consumer-build"]), "--output-on-failure"]
        if validation_id == "waylib-package-consumer":
            command.append("--no-tests=error")
        return command

    def build(self):
        return build_sync_report(
            self.inventory,
            self.manifest,
            self.gates,
            self.validations,
            self.root,
        )

    def materialization(self):
        return {
            "schema_version": 2,
            "kind": "treeland-unified-child-materialization",
            "outcome": "pass",
            "status": "verified",
            "manifest_sha256": canonical_json_sha256(self.manifest),
            "parent_head": self.manifest["final_parent_head"],
            "child_head": self.manifest["final_child_head"],
            "gitlink_path": "3rdparty/waylib-shared",
            "wlroots_head": None,
            "wlroots_checkouts": {"child_base": None, "child_candidate": None, "parent_candidate": None},
            "checkout": {
                "path": str((self.root / "parent-wt" / "3rdparty/waylib-shared").resolve()),
                "head": self.manifest["final_child_head"],
                "common_git_dir": str((self.root / "child-repo" / ".git").resolve()),
                "linked_worktree": True,
                "clean": True,
            },
            "blocked_reasons": [],
        }

    def test_materialization_gate_requires_nested_parent_checkout_evidence(self) -> None:
        self.gates["child_materialization"] = self.materialization()
        for entry in self.validations["entries"]:
            if entry["id"].startswith("deckshell-"):
                entry.pop("nested_checkout", None)

        result = self.build()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("nested child checkout" in item for item in result["blocked_reasons"])
        )

    def test_reports_only_real_mappings_gates_and_zero_test_state(self) -> None:
        result = self.build()

        self.assertEqual(result["outcome"], "pass")
        report = result["markdown"]
        self.assertIn(SOURCE_ONE[:12], report)
        self.assertIn(PARENT_ONE[:12], report)
        self.assertIn(CHILD_ONE[:12], report)
        self.assertIn("ambiguous-candidates", report)
        self.assertIn("NO_TESTS（total=0）", report)
        self.assertNotIn("PASS（0/0）", report)

    def test_protocol_gate_cannot_omit_actual_parent_context(self):
        self.gates["protocol_tracking"]["parent_context_used"] = False
        self.gates["protocol_tracking"].pop("manifest_sha256")
        result = self.build()
        self.assertEqual(result["outcome"], "blocked")

    def test_materialization_common_directory_must_match_manifest(self):
        foreign = str(self.root / "foreign/.git")
        self.gates["child_materialization"]["checkout"]["common_git_dir"] = foreign
        for entry in self.validations["entries"]:
            if "nested_checkout" in entry:
                for phase in ("before", "after"):
                    entry["nested_checkout"][phase]["common_git_dir"] = foreign
        result = self.build()
        self.assertEqual(result["outcome"], "blocked")

    def test_missing_gate_and_validation_are_blocked_not_fabricated_pass(self) -> None:
        del self.gates["contract_audit"]
        self.validations["entries"] = [
            item
            for item in self.validations["entries"]
            if item["id"] != "waylib-candidate-build"
        ]

        result = self.build()

        self.assertEqual(result["outcome"], "blocked")
        self.assertIn("MISSING", result["markdown"])
        joined = "\n".join(result["blocked_reasons"])
        self.assertIn("contract_audit", joined)
        self.assertIn("waylib-candidate-build", joined)

    def test_tampered_validation_log_blocks_report(self) -> None:
        record = self.validations["entries"][0]["log"]
        (self.root / record["path"]).write_text("tampered\n", encoding="utf-8")

        result = self.build()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(any("sha256 mismatch" in item for item in result["blocked_reasons"]))

    def test_tampered_inventory_order_digest_blocks_report(self) -> None:
        self.inventory["range"]["ordered_sha256"] = "0" * 64

        result = self.build()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("ordered_sha256" in item for item in result["blocked_reasons"])
        )

    def test_gate_digest_mismatch_blocks_report(self) -> None:
        self.gates["deckshell_verify"]["manifest_sha256"] = "0" * 64

        result = self.build()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("does not bind manifest" in item for item in result["blocked_reasons"])
        )

    def test_gate_ranges_must_bind_manifest_heads(self) -> None:
        self.gates["waylib_verify"]["target_range"]["head"] = "f" * 40

        result = self.build()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("waylib_verify target range" in item for item in result["blocked_reasons"])
        )

    def test_gate_cannot_claim_pass_with_blocked_reasons(self) -> None:
        self.gates["waylib_verify"]["blocked_reasons"] = ["stale failure"]

        result = self.build()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("blocked reasons" in item for item in result["blocked_reasons"])
        )

    def test_noop_command_cannot_satisfy_required_validation_id(self) -> None:
        entry = next(
            item for item in self.validations["entries"]
            if item["id"] == "deckshell-build"
        )
        entry["command"] = ["true"]

        result = self.build()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("command contract" in item for item in result["blocked_reasons"])
        )

    def test_required_builds_reject_target_selection_and_native_dry_run(self) -> None:
        names = {"deckshell-build", "waylib-base-build", "waylib-candidate-build", "waylib-package-consumer-build"}
        for entry in self.validations["entries"]:
            if entry["id"] not in names:
                continue
            original = entry["command"]
            for flags in (["--target", "test_compositor"], ["-t", "all"], ["--target=help"], ["--", "-n"]):
                with self.subTest(name=entry["id"], flags=flags):
                    entry["command"] = [*original, *flags]
                    result = self.build()
                    self.assertEqual(result["outcome"], "blocked")
                    self.assertTrue(any("complete default build" in error for error in result["blocked_reasons"]), result)
            entry["command"] = original

    def test_invalid_range_is_blocked_without_fabricating_a_build_scope(self) -> None:
        self.inventory["range"] = None
        result = self.build()
        self.assertEqual(result["outcome"], "blocked")
        self.assertIsNone(result["build_scope"]["source_head"])

    def test_contract_audit_must_bind_current_consumer_attempt(self) -> None:
        self.gates["contract_audit"]["consumer"]["attempt"] = 99

        result = self.build()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("consumer evidence" in item for item in result["blocked_reasons"])
        )

    def test_contract_audit_must_bind_child_candidate_identity(self) -> None:
        self.gates["contract_audit"]["source_commits"]["after"] = "f" * 40

        result = self.build()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("source commits" in item for item in result["blocked_reasons"])
        )

    def test_build_validation_paths_must_form_one_candidate_chain(self) -> None:
        entry = next(
            item
            for item in self.validations["entries"]
            if item["id"] == "waylib-candidate-build"
        )
        entry["command"] = ["cmake", "--build", str(self.root / "other-build")]

        result = self.build()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("path binding mismatch" in item for item in result["blocked_reasons"])
        )

    def test_build_validation_must_capture_the_frozen_source_head(self) -> None:
        entry = next(
            item
            for item in self.validations["entries"]
            if item["id"] == "deckshell-build"
        )
        entry["git_identity"]["after"]["head"] = "f" * 40

        result = self.build()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("Git identity" in item for item in result["blocked_reasons"])
        )

    def test_configure_validation_must_prove_a_fresh_build_directory(self) -> None:
        entry = next(
            item
            for item in self.validations["entries"]
            if item["id"] == "waylib-candidate-configure"
        )
        entry["fresh_paths"]["-B"]["existed_before"] = True

        result = self.build()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("fresh path" in item for item in result["blocked_reasons"])
        )

    def test_install_validation_must_prove_a_fresh_prefix(self) -> None:
        entry = next(
            item
            for item in self.validations["entries"]
            if item["id"] == "waylib-base-install"
        )
        entry["fresh_paths"] = {}

        result = self.build()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("fresh path" in item for item in result["blocked_reasons"])
        )

    def test_contract_snapshot_artifact_tampering_blocks_report(self) -> None:
        record = self.gates["contract_audit"]["snapshot_artifacts"]["after"]
        (self.root / record["path"]).write_text("{}\n", encoding="utf-8")

        result = self.build()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("snapshot" in item and "mismatch" in item for item in result["blocked_reasons"])
        )

    def replace_contract_snapshot(self, label, edit) -> None:
        audit = self.gates["contract_audit"]
        record = audit["snapshot_artifacts"][label]
        snapshot = json.loads((self.root / record["path"]).read_text(encoding="utf-8"))
        edit(snapshot)
        data = {
            key: value for key, value in snapshot.items()
            if key not in {"schema_version", "kind", "install_root", "snapshot_sha256"}
        }
        digest = canonical_json_sha256(data)
        snapshot["snapshot_sha256"] = digest
        audit[f"{label}_snapshot_sha256"] = digest
        audit["snapshot_artifacts"][label] = write_artifact(
            self.root, record["path"],
            (json.dumps(snapshot, sort_keys=True) + "\n").encode("utf-8"),
        )

    def test_report_rejects_snapshots_without_evaluated_target_properties(self) -> None:
        for label in ("before", "after"):
            self.replace_contract_snapshot(label, lambda snapshot: snapshot.pop("exported_target_properties"))

        result = self.build()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(any("exported_target_properties" in error for error in result["blocked_reasons"]))

    def test_report_recomputes_property_drift_instead_of_trusting_pass(self) -> None:
        self.replace_contract_snapshot(
            "after", lambda snapshot: snapshot["exported_target_properties"].update(
                {"WaylibShared::SharedServer": {"INTERFACE_INCLUDE_DIRECTORIES": "<install-root>/changed"}}
            ),
        )

        result = self.build()

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(any("contract drift" in error for error in result["blocked_reasons"]))


if __name__ == "__main__":
    unittest.main()
