#!/usr/bin/env python3
"""Treeland 到 DeckShell、waylib-shared 与嵌套 wlroots 的统一同步编排器。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from unified_sync_lib.closeout import CloseoutBlocked, closeout_refs
from unified_sync_lib.git_ops import atomic_write_json, canonical_repo, read_json
from unified_sync_lib.inventory import build_unified_inventory
from unified_sync_lib.materialization import MaterializationBlocked, materialize_child_checkout
from unified_sync_lib.policy import load_policy
from unified_sync_lib.replay import ReplayBlocked, ReplayRequest, run_replay
from unified_sync_lib.schema import load_inventory
from unified_sync_lib.protocol_cli import add_protocol_parsers, run_protocol_command


def _inventory_parser(subparsers) -> None:
    command = subparsers.add_parser("inventory", help="冻结左开右闭来源区间并统一分类")
    command.add_argument("--repo", required=True, type=Path, help="包含 Treeland refs 的 Git 仓库")
    command.add_argument("--base", required=True, help="来源下界，不包含")
    command.add_argument("--head", required=True, help="来源上界，包含")
    command.add_argument(
        "--source-tip",
        required=True,
        help="用户提供并已冻结的来源 tip ref 或完整 SHA",
    )
    command.add_argument("--policy", required=True, type=Path, help="DeckShell path-policy.md")
    command.add_argument("--approve-review", action="append", default=[])
    command.add_argument("--output", required=True, type=Path, help="输出 inventory JSON")


def _replay_parser(subparsers) -> None:
    command = subparsers.add_parser("replay", help="按来源顺序执行 R→C→P 回放")
    command.add_argument("--source-repo", required=True, type=Path)
    command.add_argument("--parent-worktree", required=True, type=Path)
    command.add_argument("--child-worktree", required=True, type=Path)
    command.add_argument("--parent-base", required=True)
    command.add_argument("--child-base", required=True)
    command.add_argument("--wlroots-repo", type=Path)
    command.add_argument("--wlroots-worktree", type=Path)
    command.add_argument("--wlroots-base")
    command.add_argument("--wlroots-target-ref")
    command.add_argument("--wlroots-submodule-url")
    command.add_argument("--wlroots-baseline-proof", type=Path, help="包含已哈希基线证明 artifact 对象的 JSON")
    command.add_argument("--inventory", required=True, type=Path)
    command.add_argument("--artifact-root", required=True, type=Path)
    command.add_argument("--journal", type=Path)
    command.add_argument("--manifest", type=Path)
    command.add_argument("--waylib-evidence", type=Path)
    command.add_argument("--parent-evidence", type=Path)
    command.add_argument("--decisions", type=Path)
    command.add_argument("--protocol-update", type=Path, help="独立协议范围及配套适配补丁；最终接受前必须完成配套验证")
    command.add_argument("--run-id", required=True)
    command.add_argument("--refs-doc", required=True)
    command.add_argument("--resume", action="store_true")
    command.add_argument(
        "--test-allow-ephemeral-artifacts",
        action="store_true",
        help=argparse.SUPPRESS,
    )


def _closeout_parser(subparsers) -> None:
    command = subparsers.add_parser("closeout", help="验证通过后按 child-first 更新本地分支")
    command.add_argument("--parent-repo", required=True, type=Path)
    command.add_argument("--child-repo", required=True, type=Path)
    command.add_argument("--parent-ref", required=True)
    command.add_argument("--child-ref", required=True)
    command.add_argument("--parent-expected-old", required=True)
    command.add_argument("--child-expected-old", required=True)
    command.add_argument("--parent-new", required=True)
    command.add_argument("--child-new", required=True)
    command.add_argument("--wlroots-repo", type=Path)
    command.add_argument("--wlroots-ref")
    command.add_argument("--wlroots-expected-old")
    command.add_argument("--wlroots-new")
    command.add_argument("--report", required=True, type=Path)
    command.add_argument("--journal", required=True, type=Path)
    command.add_argument("--resume", action="store_true")


def _materialize_parser(subparsers) -> None:
    command = subparsers.add_parser(
        "materialize-child",
        help="物化并验证 C 基线、C 候选及 P 候选的两层依赖",
    )
    command.add_argument("--parent-worktree", required=True, type=Path)
    command.add_argument("--child-repo", required=True, type=Path)
    command.add_argument("--wlroots-repo", type=Path)
    command.add_argument("--child-base-worktree", type=Path)
    command.add_argument("--manifest", required=True, type=Path)
    command.add_argument("--output", required=True, type=Path)


def build_parser() -> argparse.ArgumentParser:
    """Build the unified inventory, replay, and closeout CLI parser."""

    result = argparse.ArgumentParser(description=__doc__)
    subparsers = result.add_subparsers(dest="command", required=True)
    _inventory_parser(subparsers)
    _replay_parser(subparsers)
    _materialize_parser(subparsers)
    _closeout_parser(subparsers)
    add_protocol_parsers(subparsers)
    return result


def _inventory(args: argparse.Namespace) -> int:
    try:
        repo = canonical_repo(args.repo)
        payload = build_unified_inventory(
            repo,
            args.base,
            args.head,
            load_policy(args.policy),
            args.policy,
            set(args.approve_review),
            args.source_tip,
        )
    except (OSError, ValueError, RuntimeError) as error:
        payload = {
            "schema_version": 2,
            "kind": "treeland-deckshell-waylib-unified-inventory",
            "outcome": "fail",
            "errors": [str(error)],
        }
    atomic_write_json(args.output, payload)
    return 0 if payload["outcome"] == "pass" else (1 if payload["outcome"] == "fail" else 2)


def _output_path(root: Path, requested: Optional[Path], name: str) -> Path:
    return requested if requested is not None else root / name


def _replay(args: argparse.Namespace) -> int:
    root = args.artifact_root.resolve()
    try:
        inventory = load_inventory(args.inventory)
        decisions = read_json(args.decisions) if args.decisions else {}
        request = ReplayRequest(
            source_repo=args.source_repo.resolve(),
            parent_worktree=args.parent_worktree.absolute(),
            child_worktree=args.child_worktree.absolute(),
            parent_base=args.parent_base,
            child_base=args.child_base,
            inventory=inventory,
            artifact_root=root,
            journal_path=_output_path(root, args.journal, "journal.json"),
            manifest_path=_output_path(root, args.manifest, "manifest.json"),
            waylib_evidence_path=_output_path(
                root, args.waylib_evidence, "waylib-evidence.json"
            ),
            parent_evidence_path=_output_path(
                root, args.parent_evidence, "parent-evidence.json"
            ),
            run_id=args.run_id,
            refs_doc=args.refs_doc,
            decisions=decisions,
            allow_ephemeral_artifacts=args.test_allow_ephemeral_artifacts,
            wlroots_repo=args.wlroots_repo,
            wlroots_worktree=args.wlroots_worktree.absolute() if args.wlroots_worktree else None,
            wlroots_base=args.wlroots_base,
            wlroots_target_ref=args.wlroots_target_ref,
            wlroots_submodule_url=args.wlroots_submodule_url,
            wlroots_baseline_proof=read_json(args.wlroots_baseline_proof) if args.wlroots_baseline_proof else None,
            protocol_update=read_json(args.protocol_update) if args.protocol_update else None,
        )
        run_replay(request, resume=args.resume)
        return 0
    except ReplayBlocked as error:
        print(f"同步被阻断：{error}", file=sys.stderr)
        return 2
    except (OSError, ValueError, RuntimeError) as error:
        print(f"同步失败：{error}", file=sys.stderr)
        return 1


def _closeout(args: argparse.Namespace) -> int:
    try:
        closeout_refs(
            args.parent_repo,
            args.child_repo,
            args.parent_ref,
            args.child_ref,
            args.parent_expected_old,
            args.child_expected_old,
            args.parent_new,
            args.child_new,
            read_json(args.report),
            args.journal,
            resume=args.resume,
            wlroots_repo=args.wlroots_repo,
            wlroots_ref=args.wlroots_ref,
            wlroots_expected_old=args.wlroots_expected_old,
            wlroots_new=args.wlroots_new,
        )
        return 0
    except CloseoutBlocked as error:
        print(f"收口被阻断：{error}", file=sys.stderr)
        return 2
    except (OSError, ValueError, RuntimeError) as error:
        print(f"收口失败：{error}", file=sys.stderr)
        return 1


def _materialize(args: argparse.Namespace) -> int:
    try:
        payload = materialize_child_checkout(
            args.parent_worktree,
            args.child_repo,
            read_json(args.manifest),
            wlroots_repo=args.wlroots_repo,
            child_base_worktree=args.child_base_worktree,
        )
    except MaterializationBlocked as error:
        payload = {
            "schema_version": 2,
            "kind": "treeland-unified-child-materialization",
            "outcome": "blocked",
            "status": "blocked",
            "blocked_reasons": [str(error)],
        }
    except (OSError, ValueError, RuntimeError) as error:
        payload = {
            "schema_version": 2,
            "kind": "treeland-unified-child-materialization",
            "outcome": "fail",
            "errors": [str(error)],
        }
    atomic_write_json(args.output, payload)
    if payload["outcome"] == "pass":
        return 0
    if payload["outcome"] == "blocked":
        return 2
    return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Dispatch a unified synchronization command."""

    args = build_parser().parse_args(argv)
    if args.command == "inventory":
        return _inventory(args)
    if args.command == "replay":
        return _replay(args)
    if args.command == "materialize-child":
        return _materialize(args)
    if args.command == "closeout":
        return _closeout(args)
    if args.command in {"protocol-inspect", "protocol-verify"}:
        return run_protocol_command(args)
    raise AssertionError(f"unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
