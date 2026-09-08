#!/usr/bin/env python3
"""Verify the waylib-shared lane against inventory, traces, and evidence."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from unified_sync_lib.evidence import verify_waylib_sync
from unified_sync_lib.git_ops import atomic_write_json, canonical_repo, read_json
from unified_sync_lib.schema import load_inventory


def parser() -> argparse.ArgumentParser:
    """Build the Waylib verification CLI parser."""

    result = argparse.ArgumentParser(description="验证 waylib-shared 路径、顺序与证据合同。")
    result.add_argument("--source-repo", required=True, type=Path, help="Treeland commits 所在仓库")
    result.add_argument("--repo", required=True, type=Path, help="waylib-shared worktree 根目录")
    result.add_argument("--base", required=True, help="目标范围下界，不包含")
    result.add_argument("--head", required=True, help="目标范围上界，包含")
    result.add_argument("--inventory", required=True, type=Path, help="统一 inventory JSON")
    result.add_argument("--traces", required=True, type=Path, help="waylib traces JSON")
    result.add_argument("--evidence", required=True, type=Path, help="waylib evidence JSON")
    result.add_argument(
        "--artifact-root",
        type=Path,
        help="证据工件根目录；默认使用 evidence 所在目录",
    )
    result.add_argument("--output", required=True, type=Path, help="输出 verify JSON")
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Verify child-lane traces and evidence and return a CLI exit code."""

    args = parser().parse_args(argv)
    try:
        repo = canonical_repo(args.repo)
        inventory = load_inventory(args.inventory)
        traces = read_json(args.traces)
        evidence = read_json(args.evidence)
        artifact_root = args.artifact_root or args.evidence.resolve().parent
        result = verify_waylib_sync(
            repo,
            args.base,
            args.head,
            inventory,
            traces,
            evidence,
            artifact_root,
            canonical_repo(args.source_repo),
        )
    except (OSError, ValueError, RuntimeError) as error:
        result = {
            "schema_version": 2,
            "kind": "treeland-unified-waylib-verify",
            "outcome": "fail",
            "errors": [str(error)],
        }
    atomic_write_json(args.output, result)
    if result["outcome"] == "fail":
        print(result["errors"][0], file=sys.stderr)
        return 1
    return 0 if result["outcome"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
