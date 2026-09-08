#!/usr/bin/env python3
"""验证 DeckShell lane 的顺序、路径权威、消息和证据。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from unified_sync_lib.git_ops import atomic_write_json, canonical_repo, read_json
from unified_sync_lib.parent_verify import verify_parent_sync
from unified_sync_lib.schema import load_inventory


def parser() -> argparse.ArgumentParser:
    """Build the DeckShell verification CLI parser."""

    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--source-repo", required=True, type=Path)
    result.add_argument("--parent-repo", required=True, type=Path)
    result.add_argument("--parent-base", required=True)
    result.add_argument("--parent-head", required=True)
    result.add_argument("--inventory", required=True, type=Path)
    result.add_argument("--manifest", required=True, type=Path)
    result.add_argument("--evidence", required=True, type=Path)
    result.add_argument("--artifact-root", required=True, type=Path)
    result.add_argument("--output", required=True, type=Path)
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Verify the parent lane and return a CLI exit code."""

    args = parser().parse_args(argv)
    try:
        payload = verify_parent_sync(
            canonical_repo(args.source_repo),
            canonical_repo(args.parent_repo),
            args.parent_base,
            args.parent_head,
            load_inventory(args.inventory),
            read_json(args.manifest),
            read_json(args.evidence),
            args.artifact_root,
        )
    except (OSError, ValueError, RuntimeError) as error:
        payload = {
            "schema_version": 2,
            "kind": "treeland-unified-parent-verify",
            "outcome": "fail",
            "errors": [str(error)],
        }
    atomic_write_json(args.output, payload)
    if payload["outcome"] == "fail":
        print(payload["errors"][0], file=sys.stderr)
        return 1
    return 0 if payload["outcome"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
