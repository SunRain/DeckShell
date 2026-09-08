#!/usr/bin/env python3
"""生成 treeland-protocols 的 advisory 候选列表。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from unified_sync_lib.git_ops import (
    atomic_write_json,
    canonical_json_sha256,
    canonical_repo,
    read_json,
)
from unified_sync_lib.protocols import (
    PROTOCOL_SEARCH_ROOTS,
    build_parent_protocol_context,
    protocol_tracking_required,
    track_protocol_candidates,
    tracking_parameter_errors,
)
from unified_sync_lib.schema import load_inventory


def parser() -> argparse.ArgumentParser:
    """Build the protocol-tracking CLI parser."""

    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--source-repo", type=Path)
    result.add_argument("--parent-repo", type=Path)
    result.add_argument("--manifest", type=Path)
    result.add_argument("--inventory", required=True, type=Path)
    result.add_argument("--protocol-repo", type=Path)
    result.add_argument("--protocol-head")
    result.add_argument("--threshold", type=float, default=0.7)
    result.add_argument("--days-before", type=int, default=30)
    result.add_argument("--days-after", type=int, default=7)
    result.add_argument("--output", required=True, type=Path)
    return result


def _load_parent_context(args, inventory):
    if bool(args.parent_repo) != bool(args.manifest):
        raise ValueError("--parent-repo 和 --manifest 必须同时提供")
    manifest = read_json(args.manifest) if args.manifest else None
    parent_context = (
        build_parent_protocol_context(canonical_repo(args.parent_repo), manifest)
        if args.parent_repo and manifest
        else {}
    )
    return manifest, parent_context


def _not_triggered_payload(args, inventory):
    return {
        "schema_version": 2,
        "kind": "treeland-unified-protocol-candidates",
        "outcome": "pass",
        "advisory": True,
        "inventory_sha256": canonical_json_sha256(inventory),
        "protocol_head": None,
        "parent_context_used": False,
        "search_paths": [f"{root}/**/*.xml" for root in PROTOCOL_SEARCH_ROOTS],
        "threshold": args.threshold,
        "window": {
            "days_before": args.days_before,
            "days_after": args.days_after,
        },
        "entries": [],
        "status": "not-triggered",
        "blocked_reasons": [],
    }


def _tracked_payload(args, inventory, parent_context):
    if not args.source_repo or not args.protocol_repo or not args.protocol_head:
        raise ValueError(
            "协议路径已触发，必须提供 --source-repo、--protocol-repo 和 --protocol-head"
        )
    return track_protocol_candidates(
        canonical_repo(args.source_repo),
        inventory,
        canonical_repo(args.protocol_repo),
        args.protocol_head,
        threshold=args.threshold,
        days_before=args.days_before,
        days_after=args.days_after,
        parent_context=parent_context,
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Generate advisory protocol candidates and return a CLI exit code."""

    args = parser().parse_args(argv)
    try:
        inventory = load_inventory(args.inventory)
        parameter_errors = tracking_parameter_errors(
            args.threshold, args.days_before, args.days_after
        )
        if parameter_errors:
            raise ValueError("; ".join(parameter_errors))
        manifest, parent_context = _load_parent_context(args, inventory)
        touched = protocol_tracking_required(inventory, parent_context)
        payload = (
            _tracked_payload(args, inventory, parent_context)
            if touched
            else _not_triggered_payload(args, inventory)
        )
        payload["manifest_sha256"] = (
            canonical_json_sha256(manifest) if manifest else None
        )
        payload["parent_context_used"] = manifest is not None
    except (OSError, ValueError, RuntimeError) as error:
        payload = {
            "schema_version": 2,
            "kind": "treeland-unified-protocol-candidates",
            "outcome": "fail",
            "errors": [str(error)],
        }
    atomic_write_json(args.output, payload)
    if payload["outcome"] == "fail":
        print(payload["errors"][0], file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
