#!/usr/bin/env python3
"""Build manifests and deterministically rewrite Treeland sync metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from sync_audit_lib.manifest import (  # noqa: E402
    build_candidate_manifest,
    finalize_manifest,
)
from sync_audit_lib.history_rewrite import (  # noqa: E402
    mapping_payload,
    render_chain,
    write_commit_objects,
)
from sync_audit_lib.history_equivalence import verify_history_equivalence  # noqa: E402


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def canonical_json_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    candidates = subparsers.add_parser("candidates", help="生成未审定 manifest 候选")
    candidates.add_argument("--repo", type=Path, required=True)
    candidates.add_argument("--inventory", type=Path, required=True)
    candidates.add_argument("--traces", type=Path, required=True)
    candidates.add_argument("--legacy-evidence", type=Path, required=True)
    candidates.add_argument("--evidence-root", type=Path, required=True)
    candidates.add_argument("--migration-id", required=True)
    candidates.add_argument("--output", type=Path, required=True)

    finalize = subparsers.add_parser("finalize", help="应用独立审定并冻结 canonical manifest")
    finalize.add_argument("--candidates", type=Path, required=True)
    finalize.add_argument("--reviews", type=Path, required=True)
    finalize.add_argument("--output", type=Path, required=True)

    render = subparsers.add_parser("render", help="确定性渲染 raw commit 对象链")
    render.add_argument("--repo", type=Path, required=True)
    render.add_argument("--manifest", type=Path, required=True)
    render.add_argument("--tool-root", type=Path, required=True)
    render.add_argument("--expected-count", type=int, required=True)
    render.add_argument("--expected-head-tree", required=True)
    render.add_argument("--output", type=Path, required=True)
    mode = render.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--write-objects", action="store_true")
    render.add_argument("--rewrite-ref")
    render.add_argument("--expected-plan-digest")
    render.add_argument("--expected-tool-bundle")
    render.add_argument("--expected-manifest-sha256")

    equivalence = subparsers.add_parser(
        "verify-history", help="验证 rewritten commit 对象、补丁和链级等价"
    )
    equivalence.add_argument("--repo", type=Path, required=True)
    equivalence.add_argument("--manifest", type=Path, required=True)
    equivalence.add_argument("--mapping", type=Path, required=True)
    equivalence.add_argument("--expected-count", type=int, required=True)
    equivalence.add_argument("--expected-head-tree", required=True)
    equivalence.add_argument("--output", type=Path, required=True)
    return parser


def _verify_write_gates(args: argparse.Namespace, payload: dict[str, Any]) -> None:
    if not args.rewrite_ref:
        raise ValueError("--rewrite-ref is required with --write-objects")
    required = {
        "--expected-plan-digest": args.expected_plan_digest,
        "--expected-tool-bundle": args.expected_tool_bundle,
        "--expected-manifest-sha256": args.expected_manifest_sha256,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise ValueError(f"write mode is missing digest gates: {missing}")
    expected = {
        "plan_digest_sha256": args.expected_plan_digest,
        "tool_bundle_sha256": args.expected_tool_bundle,
        "manifest_sha256": args.expected_manifest_sha256,
    }
    for field, value in expected.items():
        if payload[field] != value:
            raise ValueError(f"{field} differs from approved dry-run")


def _render_payload(args: argparse.Namespace) -> dict[str, Any]:
    manifest = read_json(args.manifest)
    records, tool_bundle = render_chain(args.repo, manifest, args.tool_root)
    if len(records) != args.expected_count:
        raise ValueError(f"expected {args.expected_count} commits, rendered {len(records)}")
    if records[-1].tree != args.expected_head_tree:
        raise ValueError(
            f"expected head tree {args.expected_head_tree}, got {records[-1].tree}"
        )
    payload = mapping_payload(records, tool_bundle, canonical_json_sha256(manifest))
    if args.write_objects:
        _verify_write_gates(args, payload)
        write_commit_objects(args.repo, records, args.rewrite_ref)
    elif args.rewrite_ref:
        raise ValueError("--rewrite-ref is only valid with --write-objects")
    payload["mode"] = "write-objects" if args.write_objects else "dry-run"
    payload["rewrite_ref"] = args.rewrite_ref
    payload["rewritten_head"] = records[-1].rewritten_target
    payload["head_tree"] = records[-1].tree
    return payload


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "candidates":
        payload = build_candidate_manifest(
            repo=args.repo,
            inventory=read_json(args.inventory),
            traces=read_json(args.traces),
            legacy_evidence=read_json(args.legacy_evidence),
            evidence_root=args.evidence_root,
            migration_id=args.migration_id,
        )
    elif args.command == "finalize":
        payload = finalize_manifest(read_json(args.candidates), read_json(args.reviews))
    elif args.command == "render":
        payload = _render_payload(args)
    else:
        payload = verify_history_equivalence(
            args.repo,
            read_json(args.manifest),
            read_json(args.mapping),
            args.expected_count,
            args.expected_head_tree,
        )
    write_json(args.output, payload)
    return 2 if payload.get("outcome") == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
