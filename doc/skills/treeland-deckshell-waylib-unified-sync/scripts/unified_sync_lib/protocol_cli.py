"""Protocol inspection and pairing-verification commands of unified_sync.py."""

from __future__ import annotations

from pathlib import Path

from .git_ops import atomic_write_json, canonical_repo, read_json
from .protocol_pairing import verify_pairing
from .protocol_sources import inspect_pairing
from .schema import load_inventory


def add_protocol_parsers(subparsers) -> None:
    """Register read-only source inspection and final pairing verification."""

    inspect = subparsers.add_parser("protocol-inspect", help="每轮检查两个来源范围；成功不等于适配完成")
    inspect.add_argument("--source-repo", required=True, type=Path)
    inspect.add_argument("--child-repo", required=True, type=Path)
    inspect.add_argument("--child-base", required=True)
    inspect.add_argument("--inventory", required=True, type=Path)
    inspect.add_argument("--selection", required=True, type=Path)
    inspect.add_argument("--output", required=True, type=Path)
    verify = subparsers.add_parser("protocol-verify", help="核验 XML/实现/客户端和真实交互；失败报告尚未适配")
    verify.add_argument("--inventory", required=True, type=Path)
    verify.add_argument("--manifest", required=True, type=Path)
    verify.add_argument("--review", required=True, type=Path)
    verify.add_argument("--validations", required=True, type=Path)
    verify.add_argument("--artifact-root", required=True, type=Path)
    verify.add_argument("--output", required=True, type=Path)


def run_protocol_command(args) -> int:
    """Write a useful failure result as well as a successful inspection/pairing."""

    try:
        inventory = load_inventory(args.inventory)
        if args.command == "protocol-inspect":
            result = inspect_pairing(inventory, canonical_repo(args.source_repo),
                                     canonical_repo(args.child_repo), args.child_base,
                                     read_json(args.selection))
        else:
            result = verify_pairing(inventory, read_json(args.manifest), read_json(args.review),
                                    read_json(args.validations), args.artifact_root)
    except (OSError, ValueError, RuntimeError) as error:
        result = {"schema_version": 2, "kind": "treeland-unified-protocol-input-error",
                  "outcome": "blocked", "status": "尚未适配", "failure_stage": "input",
                  "last_accepted_pair": None, "validation_results": [],
                  "requested_inputs": {name: str(getattr(args, name)) for name in
                                       ("inventory", "selection", "manifest", "review", "validations")
                                       if hasattr(args, name)},
                  "unfinished": [str(error)], "blocked_reasons": [str(error)]}
    atomic_write_json(args.output, result)
    return 0 if result["outcome"] == "pass" else 2
