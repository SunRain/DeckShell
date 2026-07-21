"""Tests for deterministic v2 regeneration outputs."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aligned_history_v2.regeneration import finalize_plan_document, render_audit_document
from aligned_history_v2.preview_regeneration import build_audit_overlay


class AlignedHistoryV2RegenerationTests(unittest.TestCase):
    def test_final_plan_records_compile_atomic_execution_with_cas_pending(self) -> None:
        source = (
            "# DeckShell commit-aligned history v1/v2 编译原子与协议历史对齐 - 实施规划\n\n"
            "最终交付是 migration refs。"
            "本次修订只更新方案合同，不执行\n"
            "实现或 ref 事务。\n"
        ).encode("utf-8")

        rendered = finalize_plan_document(source).decode("utf-8")

        self.assertIn("编译原子与协议历史对齐 - 实施记录", rendered)
        self.assertIn("任务 1-16 可自动执行", rendered)
        self.assertIn("dependency-proven transition", rendered)
        self.assertIn("`ds-mod` expected-old CAS 不包含在本提交中", rendered)
        self.assertNotIn("本次修订只更新方案合同", rendered)

    def test_final_plan_accepts_the_frozen_r5_execution_scope(self) -> None:
        source = (
            "# DeckShell commit-aligned history v1/v2 编译原子与协议历史对齐 - 实施规划\n\n"
            "最终交付是新的 corrected-v1/corrected-v2 migration refs、70/70 风险选择构建证据、全 330\n"
            "节点选择覆盖证据和单次 `ds-mod` expected-old CAS 候选。当前 corrected-v1/v2 r5 已生成；\n"
            "本次修订同步 r5 事实与后续 Task 13-16 合同，不执行 Task 17 CAS。\n"
        ).encode("utf-8")

        rendered = finalize_plan_document(source).decode("utf-8")

        self.assertIn("任务 1-16 可自动执行", rendered)
        self.assertNotIn("当前 corrected-v1/v2 r5 已生成", rendered)

    def test_index_316_audit_uses_only_the_sealed_treeland_prefix(self) -> None:
        entries = []
        classifications = ["other"] * 233 + ["mixed"] * 29 + ["dependency-only"] * 36
        for index, classification in enumerate(classifications, 1):
            entries.append(
                {
                    "normalized_treeland_commit": f"{index:040x}",
                    "v2_target": f"{index + 500:040x}",
                    "classification": classification,
                }
            )
        prefix = {"entries": entries, "canonical_payload_sha256": "a" * 64}

        rendered = render_audit_document(prefix)

        self.assertIn(b"Treeland targets | 298", rendered)
        self.assertNotIn(b"Legacy-DeckShell", rendered)
        self.assertNotIn(b"rewrite-target-mapping", rendered)

        overlay = build_audit_overlay(
            {
                "ordered_index": 316,
                "authorized_v2_delta_paths": [
                    "doc/ai/waylibshared_7dc11a_regression_audit.md"
                ],
                "regeneration_job": {"expected_output_count": 1},
            },
            prefix,
        )
        self.assertEqual(
            list(overlay), ["doc/ai/waylibshared_7dc11a_regression_audit.md"]
        )
        self.assertEqual(next(iter(overlay.values())), rendered)


if __name__ == "__main__":
    unittest.main()
