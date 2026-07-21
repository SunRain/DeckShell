"""Independent frozen-master oracle tests for corrected-v2."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aligned_history_v2.product_oracle import (
    compare_three_way_product_entries,
    path_is_excluded,
    validate_overlay_rules,
)
from aligned_history_v2.product_projection import project_product_payload


def _entry(path: str, object_id: str) -> dict[str, str]:
    return {
        "mode": "100644",
        "kind": "blob",
        "object_id": object_id,
        "path": path,
    }


def _rules() -> dict[str, object]:
    return {
        "version": "commit-aligned-product-overlay-v1",
        "policy": "include-by-default-explicit-exclusions-only",
        "exact_exclusions": [
            ".gitattributes",
            "doc/ai/deckshell_waylib_commit_aligned_history_rewrite_plan.md",
            "doc/ai/waylibshared_7dc11a_regression_audit.md",
            "doc/skills/treeland-deckshell-sync/scripts/aligned_history_v2.py",
        ],
        "prefix_exclusions": [
            "doc/skills/treeland-deckshell-sync/scripts/aligned_history_v2/",
            "doc/treeland-sync/adaptations/",
        ],
        "bounded_patterns": [
            {
                "prefix": "doc/skills/treeland-deckshell-sync/tests/"
                "test_aligned_history_v2_",
                "suffix": ".py",
            }
        ],
        "forbidden_patterns": ["doc/**"],
    }


class AlignedHistoryV2MasterOracleTests(unittest.TestCase):
    def test_v1_and_v2_same_wrong_blob_still_fail_master_oracle(self) -> None:
        master = [_entry("compositor/src/seat/helper.cpp", "a" * 40)]
        identically_wrong = [
            _entry("compositor/src/seat/helper.cpp", "b" * 40)
        ]

        with self.assertRaisesRegex(
            ValueError, "compositor/src/seat/helper.cpp"
        ):
            compare_three_way_product_entries(
                master, identically_wrong, identically_wrong
            )

    def test_local_contract_deletion_with_same_path_set_is_rejected(self) -> None:
        master = [_entry("compositor/src/seat/helper.cpp", "a" * 40)]
        local_contract_deleted = [
            _entry("compositor/src/seat/helper.cpp", "c" * 40)
        ]

        with self.assertRaisesRegex(ValueError, "product mismatch"):
            compare_three_way_product_entries(
                master, local_contract_deleted, master
            )

    def test_broad_overlay_cannot_hide_product_code(self) -> None:
        rules = _rules()
        rules["prefix_exclusions"].append("compositor/")

        with self.assertRaisesRegex(ValueError, "broad overlay"):
            validate_overlay_rules(rules)

    def test_bounded_test_pattern_does_not_exclude_other_documents(self) -> None:
        rules = _rules()
        validate_overlay_rules(rules)

        self.assertTrue(
            path_is_excluded(
                "doc/skills/treeland-deckshell-sync/tests/"
                "test_aligned_history_v2_remediation.py",
                rules,
            )
        )
        self.assertFalse(path_is_excluded("doc/other-product-contract.md", rules))

    def test_master_cmake_projection_recomputes_compile_atomic_authority(self) -> None:
        root, root_reasons = project_product_payload(
            "CMakeLists.txt",
            b"set(CMAKE_CXX_EXTENSIONS OFF)\n",
        )
        gamepad, gamepad_reasons = project_product_payload(
            "lib/gamepad/src/CMakeLists.txt",
            b"set(PROTOCOL_DIR ${TREELAND_PROTOCOLS_DATA_DIR})\n",
        )

        self.assertIn(b"-include unistd.h", root)
        self.assertEqual(root_reasons, ["root-compile-compatibility"])
        self.assertIn(b"DECKCOMPOSITOR_PROTOCOLS_DATA_DIR", gamepad)
        self.assertEqual(gamepad_reasons, ["legacy-protocol-variable"])


if __name__ == "__main__":
    unittest.main()
