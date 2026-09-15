#!/usr/bin/env python3
"""比较 Waylib 安装快照并验证 package consumer 证据。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Sequence

from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.contracts import build_install_snapshot, compare_contract_snapshots
from unified_sync_lib.namespace_probe import run_namespace_probe
from unified_sync_lib.git_ops import (
    atomic_write_json,
    canonical_repo,
    read_json,
    resolve_commit,
    run_git,
)


def parser() -> argparse.ArgumentParser:
    """Build the Waylib package-contract audit CLI parser."""

    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--before", required=True, type=Path)
    result.add_argument("--after", required=True, type=Path)
    result.add_argument("--source-before", required=True, type=Path)
    result.add_argument("--source-after", required=True, type=Path)
    result.add_argument("--consumer", required=True, type=Path)
    result.add_argument("--artifact-root", required=True, type=Path)
    result.add_argument("--output", required=True, type=Path)
    approvals = result.add_mutually_exclusive_group()
    approvals.add_argument("--approved-additions", type=Path, help="逐项批准的新 wrapper 安装合同，不可修改既有合同")
    approvals.add_argument("--approved-migration", type=Path, help="绑定真实安装快照和头/命名空间的显式公共迁移审批")
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Compare package contracts and return a CLI exit code."""

    args = parser().parse_args(argv)
    try:
        source_before = canonical_repo(args.source_before)
        source_after = canonical_repo(args.source_after)
        for label, source in (("before", source_before), ("after", source_after)):
            status = str(
                run_git(source, "status", "--porcelain=v1", "--untracked-files=all")
            )
            if status:
                raise ValueError(f"{label} source worktree must be clean for contract audit")
        before = build_install_snapshot(args.before, source_before)
        after = build_install_snapshot(args.after, source_after)
        consumer = read_json(args.consumer)
        migration = read_json(args.approved_migration) if args.approved_migration else None
        probe = run_namespace_probe(before, after, args.artifact_root, migration)
        result = compare_contract_snapshots(
            before, after, consumer, args.artifact_root, probe,
            read_json(args.approved_additions) if args.approved_additions else None,
            migration,
        )
        result["install_roots"] = {
            "before": str(args.before.resolve()),
            "after": str(args.after.resolve()),
        }
        result["source_roots"] = {
            "before": str(source_before),
            "after": str(source_after),
        }
        result["source_commits"] = {
            "before": resolve_commit(source_before, "HEAD"),
            "after": resolve_commit(source_after, "HEAD"),
        }
        result["snapshot_artifacts"] = {
            "before": write_artifact(
                args.artifact_root, "snapshots/before.json", _json_bytes(before)
            ),
            "after": write_artifact(
                args.artifact_root, "snapshots/after.json", _json_bytes(after)
            ),
        }
    except (OSError, ValueError, RuntimeError) as error:
        result = {
            "schema_version": 2,
            "kind": "waylib-install-contract-audit",
            "outcome": "fail",
            "errors": [str(error)],
        }
    atomic_write_json(args.output, result)
    if result["outcome"] == "fail":
        print(result["errors"][0], file=sys.stderr)
        return 1
    return 0 if result["outcome"] == "pass" else 2


def _json_bytes(payload) -> bytes:
    return (json.dumps(payload, ensure_ascii=True, indent=2) + "\n").encode("utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
