"""Git-object binding tests for compile-atomic dependency bundles."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import ANY, Mock, patch


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aligned_history_v2 import atomic_bundle_bindings


class AlignedHistoryV2AtomicBindingsTests(unittest.TestCase):
    def test_bundle_materialization_checks_protocol_target_not_source_path(self) -> None:
        source_path = "xml/example.xml"
        target_path = "protocols/compositor/xml/example.xml"
        component_id = "protocol:example"
        ledger = {
            "components": [
                {
                    "component_id": component_id,
                    "kind": "protocol-interface",
                    "owner_index": 2,
                    "payload": {
                        "source_path": source_path,
                        "target_path": target_path,
                    },
                }
            ],
            "bundles": [
                {
                    "bundle_id": "deck:2:protocol-interface",
                    "owner_index": 2,
                    "component_ids": [component_id],
                    "expected_changed_paths": [target_path, source_path],
                }
            ],
        }
        records = [{"ordered_index": 2, "new_parent": "parent", "new_commit": "commit"}]
        protocol_ledger = {
            "components": [
                {
                    "owner_index": 2,
                    "source_sequence": 0,
                    "component_sequence": 0,
                    "target_path": target_path,
                    "result_blob": "target-blob",
                }
            ]
        }

        with (
            patch.object(
                atomic_bundle_bindings, "tree_diff_paths", return_value=[target_path]
            ),
            patch.object(
                atomic_bundle_bindings, "_blob_id", return_value="target-blob"
            ) as blob_id,
        ):
            result = atomic_bundle_bindings.verify_bundle_materialization(
                Mock(), records, ledger, protocol_ledger
            )

        self.assertEqual(result["checked_local_path_count"], 0)
        self.assertEqual(result["external_source_path_count"], 1)
        self.assertEqual(result["protocol_target_path_count"], 1)
        blob_id.assert_called_once_with(ANY, "commit", target_path)

    def test_bundle_materialization_accepts_terminal_protocol_deletion(self) -> None:
        source_path = "xml/removed.xml"
        target_path = "protocols/compositor/xml/removed.xml"
        component_ids = ["protocol:add", "protocol:delete"]
        ledger = {
            "components": [
                {
                    "component_id": component_id,
                    "kind": "protocol-interface",
                    "owner_index": 1,
                    "payload": {
                        "source_path": source_path,
                        "target_path": target_path,
                    },
                }
                for component_id in component_ids
            ],
            "bundles": [
                {
                    "bundle_id": "deck:1:protocol-interface",
                    "owner_index": 1,
                    "component_ids": component_ids,
                    "expected_changed_paths": [target_path, source_path],
                }
            ],
        }
        protocol_ledger = {
            "components": [
                {
                    "owner_index": 1,
                    "source_sequence": sequence,
                    "component_sequence": 0,
                    "target_path": target_path,
                    "result_blob": result_blob,
                }
                for sequence, result_blob in ((0, "added-blob"), (1, None))
            ]
        }
        records = [
            {"ordered_index": 1, "new_parent": "parent", "new_commit": "commit"}
        ]

        with (
            patch.object(atomic_bundle_bindings, "tree_diff_paths", return_value=[]),
            patch.object(atomic_bundle_bindings, "_blob_id", return_value=None),
        ):
            result = atomic_bundle_bindings.verify_bundle_materialization(
                Mock(), records, ledger, protocol_ledger
            )

        self.assertEqual(result["protocol_target_path_count"], 1)

    def test_bundle_semantics_accepts_definition_removed_by_obsolete_gate(self) -> None:
        path = "compositor/src/seat/helper.cpp"
        obsolete = "class Helper::XdgDialogManagerV1Bridge"
        graph_id = "graph:xdg-dialog"
        gate_id = "gate:xdg-dialog"
        lineage_id = "graph:xdg-dialog-lifecycle"
        ledger = {
            "components": [
                {
                    "component_id": graph_id,
                    "kind": "symbol-cross-entry",
                    "owner_index": 133,
                    "payload": {"definition_lines": {"136": {path: [obsolete]}}},
                },
                {
                    "component_id": gate_id,
                    "kind": "workaround-lifecycle",
                    "owner_index": 133,
                    "payload": {"path": path, "needle": obsolete, "maximum": 0},
                },
                {
                    "component_id": lineage_id,
                    "kind": "workaround-lifecycle",
                    "owner_index": 133,
                    "payload": {
                        "gate_id": "legacy-workaround:xdg-dialog",
                        "path": path,
                        "component_ids": [],
                    },
                },
            ],
            "bundles": [
                {
                    "bundle_id": "deck:133:xdg-dialog-v1",
                    "owner_index": 133,
                    "component_ids": [graph_id, gate_id, lineage_id],
                    "expected_changed_paths": [path],
                }
            ],
        }
        records = [
            {"ordered_index": 133, "new_parent": "parent", "new_commit": "commit"}
        ]

        with (
            patch.object(
                atomic_bundle_bindings, "tree_diff_paths", return_value=[path]
            ),
            patch.object(
                atomic_bundle_bindings, "_blob", return_value=b"replacement\n"
            ),
        ):
            result = atomic_bundle_bindings.verify_bundle_materialization(
                Mock(), records, ledger, {"components": []}
            )

        self.assertEqual(result["semantic_check_count"], 1)

    def test_bundle_semantics_accepts_normalized_cmake_contract(self) -> None:
        content = (
            b"qt_generate_wayland_protocol_client_sources(app FILES\n"
            b"    ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/example.xml\n)\n"
        )

        result = self._verify_cmake_bundle(content)

        self.assertEqual(result["semantic_check_count"], 2)

    def test_bundle_semantics_rejects_remaining_legacy_cmake_contract(self) -> None:
        content = (
            b"find_package(TreelandProtocols REQUIRED)\n"
            b"set(PROTOCOL ${TREELAND_PROTOCOLS_DATA_DIR}/example.xml)\n"
        )

        with self.assertRaisesRegex(ValueError, "CMake contract differs"):
            self._verify_cmake_bundle(content)

    def test_bundle_materialization_accepts_verified_deferred_consumer(self) -> None:
        result = self._verify_deferred_consumer_bundle(
            owner_content=b"void ShellHandler::handle() {}\n"
        )

        self.assertEqual(result["deferred_provider_path_count"], 2)
        self.assertGreaterEqual(result["semantic_check_count"], 4)

    def test_bundle_materialization_rejects_consumer_left_before_provider(self) -> None:
        with self.assertRaisesRegex(ValueError, "deferred consumer remains"):
            self._verify_deferred_consumer_bundle(
                owner_content=b"if (m_manager)\n    m_manager->cancel();\n"
            )

    def test_bundle_materialization_accepts_obsolete_deferred_consumer(self) -> None:
        result = self._verify_deferred_consumer_bundle(
            owner_content=b"void ShellHandler::handle() {}\n",
            include_obsolete_component=True,
        )

        self.assertGreaterEqual(result["semantic_check_count"], 6)

    def test_bundle_materialization_rejects_restored_obsolete_consumer(self) -> None:
        with self.assertRaisesRegex(ValueError, "obsolete deferred consumer"):
            self._verify_deferred_consumer_bundle(
                owner_content=b"void ShellHandler::handle() {}\n",
                include_obsolete_component=True,
                restore_obsolete_use=True,
            )

    @staticmethod
    def _verify_deferred_consumer_bundle(
        owner_content: bytes,
        *,
        include_obsolete_component: bool = False,
        restore_obsolete_use: bool = False,
    ) -> dict[str, int]:
        consumer_path = "compositor/src/core/shellhandler.cpp"
        header_path = "compositor/src/core/shellhandler.h"
        provider_path = "compositor/src/core/manager.cpp"
        component_id = "graph:deferred-manager"
        use_lines = ["if (m_manager)", "    m_manager->cancel();"]
        definition = "    Manager *m_manager = nullptr;"
        component = {
            "component_id": component_id,
            "kind": "symbol-cross-entry",
            "owner_index": 146,
            "payload": {
                "owner_index": 231,
                "required_owner_index": 146,
                "provider_new_file_paths": [provider_path, header_path],
                "definition_lines": {"231": {header_path: [definition]}},
                "use_lines": {
                    "146": {consumer_path: use_lines},
                    "231": {consumer_path: ["m_manager = new Manager;"]},
                },
            },
        }
        components = [component]
        component_ids = [component_id]
        symbol_reports = [
            {
                "component_id": component_id,
                "status": "applied",
                "mode": "deferred-consumer",
            }
        ]
        obsolete_use = "    m_manager->cancelLegacy();"
        if include_obsolete_component:
            obsolete_id = "graph:obsolete-deferred-manager"
            component["payload"]["use_lines"]["146"][consumer_path].append(
                obsolete_use
            )
            components.append(
                {
                    "component_id": obsolete_id,
                    "kind": "symbol-cross-entry",
                    "owner_index": 146,
                    "payload": {
                        "owner_index": 231,
                        "required_owner_index": 146,
                        "provider_new_file_paths": [provider_path],
                        "definition_lines": {
                            "231": {provider_path: ["void Manager::cancelLegacy() {}"]}
                        },
                        "use_lines": {"146": {consumer_path: [obsolete_use]}},
                    },
                }
            )
            component_ids.append(obsolete_id)
            symbol_reports.append(
                {
                    "component_id": obsolete_id,
                    "status": "obsolete-satisfied",
                }
            )
        ledger = {
            "components": components,
            "bundles": [
                {
                    "bundle_id": "deck:146:symbol-cross-entry",
                    "owner_index": 146,
                    "component_ids": component_ids,
                    "expected_changed_paths": [provider_path, header_path],
                }
            ],
        }
        records = [
            {"ordered_index": 146, "new_parent": "p145", "new_commit": "v2-146"},
            {"ordered_index": 231, "new_parent": "p230", "new_commit": "v2-231"},
        ]
        v1_records = [
            {
                "ordered_index": 146,
                "symbol_components": symbol_reports,
            },
            {"ordered_index": 231, "symbol_components": []},
        ]
        provider_consumer = (
            b"if (m_manager)\n    m_manager->cancel();\n"
            b"m_manager = new Manager;\n"
        )
        if restore_obsolete_use:
            provider_consumer += obsolete_use.encode() + b"\n"
        blobs = {
            ("v2-146", consumer_path): owner_content,
            ("v2-146", header_path): b"class ShellHandler {};\n",
            ("v2-231", consumer_path): provider_consumer,
            ("v2-231", header_path): definition.encode() + b"\n",
            ("v2-231", provider_path): (
                b"void Manager::cancel() {}\nvoid Manager::cancelLegacy() {}\n"
            ),
        }
        if include_obsolete_component:
            blobs[("v2-231", provider_path)] = b"void Manager::cancel() {}\n"

        def blob(_repo: object, commit: str, path: str) -> bytes:
            return blobs[(commit, path)]

        def blob_id(_repo: object, commit: str, path: str) -> str | None:
            return "blob" if (commit, path) in blobs else None

        with (
            patch.object(
                atomic_bundle_bindings,
                "tree_diff_paths",
                return_value=[consumer_path],
            ),
            patch.object(atomic_bundle_bindings, "_blob", side_effect=blob),
            patch.object(atomic_bundle_bindings, "_blob_id", side_effect=blob_id),
        ):
            return atomic_bundle_bindings.verify_bundle_materialization(
                Mock(),
                records,
                ledger,
                {"components": []},
                v1_records=v1_records,
            )

    @staticmethod
    def _verify_cmake_bundle(content: bytes) -> dict[str, int]:
        path = "compositor/examples/test_example/CMakeLists.txt"
        component_id = "cmake:example"
        ledger = {
            "components": [
                {
                    "component_id": component_id,
                    "kind": "cmake-contract",
                    "owner_index": 3,
                    "payload": {
                        "path": path,
                        "roles": {
                            "3": [
                                "external-protocol-package",
                                "legacy-protocol-variable",
                            ]
                        },
                    },
                }
            ],
            "bundles": [
                {
                    "bundle_id": "deck:3:cmake-contract",
                    "owner_index": 3,
                    "component_ids": [component_id],
                    "expected_changed_paths": [path],
                }
            ],
        }
        records = [
            {"ordered_index": 3, "new_parent": "parent", "new_commit": "commit"}
        ]
        with (
            patch.object(
                atomic_bundle_bindings, "tree_diff_paths", return_value=[path]
            ),
            patch.object(atomic_bundle_bindings, "_blob", return_value=content),
        ):
            return atomic_bundle_bindings.verify_bundle_materialization(
                Mock(), records, ledger, {"components": []}
            )


if __name__ == "__main__":
    unittest.main()
