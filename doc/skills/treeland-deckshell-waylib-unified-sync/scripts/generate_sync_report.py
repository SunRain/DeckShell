#!/usr/bin/env python3
"""仅从结构化真实证据生成统一同步报告。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from unified_sync_lib.git_ops import atomic_write_bytes, atomic_write_json, read_json, sha256_bytes
from unified_sync_lib.report import build_sync_report


def parser() -> argparse.ArgumentParser:
    """Build the unified report CLI parser."""

    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--inventory", required=True, type=Path)
    result.add_argument("--manifest", required=True, type=Path)
    result.add_argument("--deckshell-verify", required=True, type=Path)
    result.add_argument("--waylib-verify", required=True, type=Path)
    result.add_argument("--gitlink-verify", required=True, type=Path)
    result.add_argument("--protocol-tracking", required=True, type=Path)
    result.add_argument("--contract-audit", required=True, type=Path)
    result.add_argument("--child-materialization", required=True, type=Path)
    result.add_argument("--wlroots-verify", required=True, type=Path)
    result.add_argument("--nested-gitlink-verify", required=True, type=Path)
    result.add_argument("--validations", required=True, type=Path)
    result.add_argument("--artifact-root", required=True, type=Path)
    result.add_argument("--output", required=True, type=Path)
    result.add_argument("--summary-output", required=True, type=Path)
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Generate the evidence-bound report and return a CLI exit code."""

    args = parser().parse_args(argv)
    try:
        gates = {
            "deckshell_verify": read_json(args.deckshell_verify),
            "waylib_verify": read_json(args.waylib_verify),
            "gitlink_verify": read_json(args.gitlink_verify),
            "protocol_tracking": read_json(args.protocol_tracking),
            "contract_audit": read_json(args.contract_audit),
            "child_materialization": read_json(args.child_materialization),
            "wlroots_verify": read_json(args.wlroots_verify),
            "nested_gitlink_verify": read_json(args.nested_gitlink_verify),
        }
        result = build_sync_report(
            read_json(args.inventory),
            read_json(args.manifest),
            gates,
            read_json(args.validations),
            args.artifact_root,
        )
        markdown = result.pop("markdown")
    except (OSError, ValueError, RuntimeError) as error:
        result = {
            "schema_version": 2,
            "kind": "treeland-unified-sync-report",
            "outcome": "fail",
            "errors": [str(error)],
        }
        markdown = (
            "# Treeland → DeckShell + waylib-shared + wlroots 统一同步报告\n\n"
            f"## 结论\n\n- 总体结果：**FAIL**\n- 错误：{error}\n"
        )
    encoded = markdown.encode("utf-8")
    atomic_write_bytes(args.output, encoded)
    result["report"] = {
        "path": str(args.output.resolve()),
        "size": len(encoded),
        "sha256": sha256_bytes(encoded),
    }
    atomic_write_json(args.summary_output, result)
    if result["outcome"] == "fail":
        print(result["errors"][0], file=sys.stderr)
        return 1
    return 0 if result["outcome"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
