#!/usr/bin/env python3
"""Generate the unified Treeland parent/child path inventory."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from unified_sync_lib.git_ops import GitError, atomic_write_json
from unified_sync_lib.inventory import build_unified_inventory
from unified_sync_lib.policy import load_policy


def build_parser() -> argparse.ArgumentParser:
    """Build the standalone unified-inventory CLI parser."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="DeckShell Git worktree root")
    parser.add_argument("--base", required=True, help="excluded lower source commit")
    parser.add_argument("--head", required=True, help="included upper source commit")
    parser.add_argument(
        "--source-tip",
        required=True,
        help="user-selected and frozen source tip ref or full SHA",
    )
    parser.add_argument("--policy", type=Path, required=True, help="DeckShell path-policy.md")
    parser.add_argument("--approve-review", action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Generate a unified inventory and return a CLI exit code."""

    args = build_parser().parse_args(argv)
    try:
        result = build_unified_inventory(
            args.repo.resolve(),
            args.base,
            args.head,
            load_policy(args.policy),
            args.policy,
            set(args.approve_review),
            args.source_tip,
        )
    except (OSError, ValueError, GitError) as error:
        result = {
            "schema_version": 2,
            "kind": "treeland-deckshell-waylib-unified-inventory",
            "outcome": "fail",
            "errors": [str(error)],
        }
    atomic_write_json(args.output, result)
    if result.get("outcome") == "fail":
        print(result["errors"][0], file=sys.stderr)
        return 1
    return 0 if result.get("outcome") == "pass" else 2


if __name__ == "__main__":
    sys.exit(main())
