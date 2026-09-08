#!/usr/bin/env python3
"""把既有文件复制到持久工件根并生成 size/SHA-256 记录。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.git_ops import atomic_write_json


def parser() -> argparse.ArgumentParser:
    """Build the artifact-recording CLI parser."""

    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--artifact-root", required=True, type=Path)
    result.add_argument("--relative", required=True, help="工件根内的相对路径")
    result.add_argument("--source", required=True, type=Path)
    result.add_argument("--output", required=True, type=Path)
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Record one persistent artifact and return a CLI exit code."""

    args = parser().parse_args(argv)
    try:
        if not args.source.is_file():
            raise ValueError(f"source artifact is not a file: {args.source}")
        record = write_artifact(
            args.artifact_root, args.relative, args.source.read_bytes()
        )
        atomic_write_json(
            args.output,
            {
                "schema_version": 2,
                "kind": "treeland-unified-artifact-record",
                "artifact": record,
            },
        )
        return 0
    except (OSError, ValueError) as error:
        print(f"工件记录失败：{error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
