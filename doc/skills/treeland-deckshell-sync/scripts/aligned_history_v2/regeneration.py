"""Deterministic plan and audit regeneration for v2 transitions."""

from __future__ import annotations

from collections import Counter
from typing import Any

from .artifacts import canonical_payload_sha256


PLAN_TITLE = (
    "# DeckShell commit-aligned history v1/v2 编译原子与协议历史对齐 - 实施规划"
)
EXECUTION_TITLE = (
    "# DeckShell commit-aligned history v1/v2 编译原子与协议历史对齐 - 实施记录"
)
PLANNING_SCOPE = "本次修订只更新方案合同，不执行\n实现或 ref 事务。"
R5_EXECUTION_SCOPE = (
    "最终交付是新的 corrected-v1/corrected-v2 migration refs、70/70 风险选择构建证据、全 330\n"
    "节点选择覆盖证据和单次 `ds-mod` expected-old CAS 候选。当前 corrected-v1/v2 r5 已生成；\n"
    "本次修订同步 r5 事实与后续 Task 13-16 合同，不执行 Task 17 CAS。"
)
EXECUTION_SCOPE = (
    "本次 corrected-v1/v2 历史生成已获得执行授权；任务 1-16 可自动执行，"
    "`ds-mod` expected-old CAS 仍是唯一需要单独明确授权的 ref 事务。"
)
AUTHORITY_SECTION = """

## corrected-v1/v2 编译原子执行权威

本次生成受
`.helloagents/plans/202607262338_commit-aligned-history-compile-atomic-protocol-alignment/`
约束。corrected-v2 独立重放 rebuilt anchor、186 个 ordinary transition、129 个
dependency-proven transition 与 11 个 remediation transition，并重新生成 3 个固定
adaptation transition。协议来源、dependency bundle、Waylib ancestry 与冻结 master
product oracle 均由独立验证器重算；`ds-mod` expected-old CAS 不包含在本提交中。
"""


def finalize_plan_document(source: bytes) -> bytes:
    """Render the compile-atomic plan as a CAS-pending execution record."""

    if b"\r" in source:
        raise ValueError("rewrite plan contains CR line endings")
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("rewrite plan is not UTF-8") from error
    text = _replace_once(text, PLAN_TITLE, EXECUTION_TITLE)
    source_scopes = [
        scope
        for scope in (PLANNING_SCOPE, R5_EXECUTION_SCOPE)
        if text.count(scope) == 1
    ]
    if len(source_scopes) != 1:
        raise ValueError("plan execution-scope authority is missing or ambiguous")
    text = text.replace(source_scopes[0], EXECUTION_SCOPE, 1)
    if "本次修订只更新方案合同" in text:
        raise ValueError("final plan retains the planning-only scope")
    if "当前 corrected-v1/v2 r5 已生成" in text:
        raise ValueError("final plan retains the superseded r5 execution scope")
    if "## corrected-v1/v2 编译原子执行权威" in text:
        raise ValueError("rewrite plan already contains execution authority")
    text = text.rstrip("\n") + AUTHORITY_SECTION
    if not text.endswith("\n"):
        text += "\n"
    return text.encode("utf-8")


def render_audit_document(prefix: dict[str, Any]) -> bytes:
    """Render the index-316 audit using only the sealed Treeland prefix."""

    entries = prefix.get("entries")
    if not isinstance(entries, list) or len(entries) != 298:
        raise ValueError("Treeland target prefix must contain 298 entries")
    source_ids = [entry["normalized_treeland_commit"] for entry in entries]
    target_ids = [entry["v2_target"] for entry in entries]
    if len(set(source_ids)) != 298 or len(set(target_ids)) != 298:
        raise ValueError("Treeland target prefix contains duplicate provenance")
    counts = Counter(entry["classification"] for entry in entries)
    if counts != Counter({"other": 233, "mixed": 29, "dependency-only": 36}):
        raise ValueError(f"Treeland prefix classification drift: {counts}")
    prefix_hash = prefix.get("canonical_payload_sha256") or canonical_payload_sha256(prefix)
    content = f"""# WaylibShared 7dc11a v2 历史回归审核

## 审核目的

本文只使用第 303 项封口的 `treeland-target-prefix.v2.json`，记录
commit-aligned-history-rewrite-v2 的 Treeland 来源与目标映射。产品构建、运行测试和
完整 330 项 mapping 由后续独立门禁验证，不作为本文输入。

## 冻结投影

- Treeland remote: `treeland`
- Treeland branch: `master`
- Treeland tracking ref: `refs/remotes/treeland/master`
- first source: `{source_ids[0]}`
- last source: `{source_ids[-1]}`
- sync head target: `{target_ids[-1]}`
- target prefix canonical SHA-256: `{prefix_hash}`

## 数量门禁

| 项目 | 数量 |
| --- | ---: |
| Treeland targets | 298 |
| other | 233 |
| mixed | 29 |
| dependency-only | 36 |
| duplicate source | 0 |
| duplicate target | 0 |

## 结构性结论

1. 298 个来源均有唯一 v2 target，且来源身份固定为 `treeland/master`。
2. 29 个 mixed 与 36 个 dependency-only 条目均保留 WaylibShared gitlink 承载语义。
3. `fd7baaa323c4c23cf021c29704cf1bb3c89dc244` 保持 `adapted/omitted`，没有降级为 `empty`。
4. 本文不引用 legacy target、v1 target、完整 output mapping 或第 330 项自身 SHA。
"""
    return content.encode("utf-8")


def _replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"plan replacement count mismatch for {old!r}")
    return text.replace(old, new)
