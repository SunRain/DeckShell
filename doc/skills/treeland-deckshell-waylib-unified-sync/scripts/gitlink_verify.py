#!/usr/bin/env python3
"""验证 DeckShell 到 waylib-shared 的 gitlink 因果链。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from unified_sync_lib.git_ops import atomic_write_json, read_json
from unified_sync_lib.gitlink import verify_gitlink_consistency


def parser() -> argparse.ArgumentParser:
    """Build the gitlink verification CLI parser."""

    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--parent-repo", required=True, type=Path)
    result.add_argument("--child-repo", required=True, type=Path)
    result.add_argument("--parent-base", required=True)
    result.add_argument("--child-base", required=True)
    result.add_argument("--manifest", required=True, type=Path)
    result.add_argument("--output", required=True, type=Path)
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Verify the gitlink chain and return a CLI exit code."""

    args = parser().parse_args(argv)
    try:
        payload = verify_gitlink_consistency(
            args.parent_repo,
            args.child_repo,
            args.parent_base,
            args.child_base,
            read_json(args.manifest),
        )
    except (OSError, ValueError, RuntimeError) as error:
        payload = {
            "schema_version": 2,
            "kind": "treeland-unified-gitlink-verify",
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
