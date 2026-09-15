#!/usr/bin/env python3
"""Generate deterministic source-to-waylib-shared history traces."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from unified_sync_lib.git_ops import atomic_write_json, canonical_repo, read_json
from unified_sync_lib.schema import load_inventory
from unified_sync_lib.traces import build_waylib_traces


def parser() -> argparse.ArgumentParser:
    """Build the Waylib trace-generation CLI parser."""

    result = argparse.ArgumentParser(description="生成 waylib-shared 有序追溯证据。")
    result.add_argument("--source-repo", required=True, type=Path, help="Treeland commits 所在仓库")
    result.add_argument("--repo", required=True, type=Path, help="waylib-shared worktree 根目录")
    result.add_argument("--base", required=True, help="目标范围下界，不包含")
    result.add_argument("--head", required=True, help="目标范围上界，包含")
    result.add_argument("--inventory", required=True, type=Path, help="统一 inventory JSON")
    result.add_argument("--output", required=True, type=Path, help="输出 traces JSON")
    result.add_argument("--evidence", type=Path, help="含显式公共迁移审批的 child evidence")
    result.add_argument("--artifact-root", type=Path, help="迁移工件根目录，与 --evidence 成对提供")
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Generate ordered child-lane traces and return a CLI exit code."""

    args = parser().parse_args(argv)
    try:
        repo = canonical_repo(args.repo)
        inventory = load_inventory(args.inventory)
        result = build_waylib_traces(
            repo,
            args.base,
            args.head,
            inventory,
            canonical_repo(args.source_repo),
            evidence=read_json(args.evidence) if args.evidence else None,
            artifact_root=args.artifact_root,
        )
    except (OSError, ValueError, RuntimeError) as error:
        result = {
            "schema_version": 2,
            "kind": "treeland-unified-waylib-traces",
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
