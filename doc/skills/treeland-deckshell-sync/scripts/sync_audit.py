#!/usr/bin/env python3
"""Deterministic audit helpers for Treeland to DeckShell commit-range syncs."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from sync_audit_lib import (  # noqa: E402
    Change,
    PathDecision,
    build_inventory,
    build_trace_audit,
    classify_path,
    classify_target_path,
    load_policy,
    parse_name_status_z,
    summarize_commit,
    verify_sync,
)

__all__ = [
    "Change",
    "PathDecision",
    "build_inventory",
    "build_trace_audit",
    "classify_path",
    "classify_target_path",
    "load_policy",
    "parse_name_status_z",
    "summarize_commit",
    "verify_sync",
]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_result(result: dict[str, Any], output: Path | None) -> None:
    content = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
    else:
        sys.stdout.write(content)


def build_parser() -> argparse.ArgumentParser:
    """Build the public command-line interface."""

    default_policy = SCRIPT_DIR.parent / "references" / "path-policy.md"
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    inventory = subparsers.add_parser("inventory", help="生成来源提交路径清单和分类")
    inventory.add_argument("--repo", type=Path, required=True)
    inventory.add_argument("--base", required=True)
    inventory.add_argument("--head", required=True)
    inventory.add_argument("--policy", type=Path, default=default_policy)
    inventory.add_argument("--approve-review", action="append", default=[])
    inventory.add_argument("--output", type=Path)

    traces = subparsers.add_parser("traces", help="解析目标历史并判断幂等状态")
    traces.add_argument("--repo", type=Path, required=True)
    traces.add_argument("--target", required=True)
    traces.add_argument("--inventory", type=Path, required=True)
    traces.add_argument("--output", type=Path)

    verify = subparsers.add_parser("verify", help="验证目标提交、路径和执行证据")
    verify.add_argument("--repo", type=Path, required=True)
    verify.add_argument("--policy", type=Path, default=default_policy)
    verify.add_argument("--inventory", type=Path, required=True)
    verify.add_argument("--traces", type=Path, required=True)
    verify.add_argument("--evidence", type=Path, required=True)
    verify.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run one audit subcommand and return 2 for a blocked result."""

    args = build_parser().parse_args(argv)
    try:
        if args.command == "inventory":
            result = build_inventory(
                args.repo,
                args.base,
                args.head,
                load_policy(args.policy),
                set(args.approve_review),
            )
        elif args.command == "traces":
            result = build_trace_audit(args.repo, args.target, _read_json(args.inventory))
        else:
            result = verify_sync(
                args.repo,
                load_policy(args.policy),
                _read_json(args.inventory),
                _read_json(args.traces),
                _read_json(args.evidence),
            )
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        result = {
            "schema_version": 1,
            "outcome": "blocked",
            "error": str(error),
        }
    _write_result(result, args.output)
    return 2 if result.get("outcome") == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
