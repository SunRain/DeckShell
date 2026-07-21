#!/usr/bin/env python3
"""Generate or verify SHA-named Treeland adaptation documents."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from sync_audit_lib.adaptation_docs import (  # noqa: E402
    read_json,
    render_documents,
    verify_documents,
    write_documents,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("generate", "verify"))
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--docs-dir", type=Path, required=True)
    parser.add_argument("--expected-count", type=int)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        manifest, manifest_sha256 = read_json(args.manifest)
        mapping, mapping_sha256 = read_json(args.mapping)
        documents = render_documents(
            args.repo,
            manifest,
            mapping,
            args.base,
            args.head,
            manifest_sha256=manifest_sha256,
            mapping_sha256=mapping_sha256,
            expected_count=args.expected_count,
        )
        if args.command == "generate":
            write_documents(args.docs_dir, documents)
        else:
            verify_documents(args.docs_dir, documents)
    except (OSError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "outcome": "pass",
                "command": args.command,
                "documents": len(documents),
                "docs_dir": str(args.docs_dir),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
