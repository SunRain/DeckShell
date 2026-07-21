#!/usr/bin/env python3
"""Execute commit-aligned-history-rewrite-v2 preparation and previews."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from aligned_history_v2.artifacts import read_hashed_json, write_hashed_json
from aligned_history_v2.context import InputPaths
from aligned_history_v2.dry_run import run_sequential_dry_run
from aligned_history_v2.formal_import import run_formal_import
from aligned_history_v2.input_builder import build_candidate_manifest, freeze_candidate
from aligned_history_v2.preview import run_isolated_preview, write_preview_artifacts
from aligned_history_v2.preview_compare import compare_previews


SKILL_ROOT = Path(__file__).resolve().parents[1]


def build_parser() -> argparse.ArgumentParser:
    """Build the fail-closed v2 command-line interface."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        required=True,
        choices=("commit-aligned-history-rewrite-v2",),
    )
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("candidate")
    freeze = subparsers.add_parser("freeze")
    freeze.add_argument("--candidate", type=Path, required=True)
    dry_run = subparsers.add_parser("dry-run")
    dry_run.add_argument("--manifest", type=Path, required=True)
    preview = subparsers.add_parser("preview")
    preview.add_argument("--manifest", type=Path, required=True)
    preview.add_argument("--dry-run", type=Path, required=True)
    preview.add_argument("--preview-name", choices=("A", "B"), required=True)
    preview.add_argument("--object-directory", type=Path, required=True)
    preview.add_argument("--scratch-directory", type=Path, required=True)
    compare = subparsers.add_parser("compare-previews")
    compare.add_argument("--preview-a", type=Path, required=True)
    compare.add_argument("--preview-b", type=Path, required=True)
    formal_import = subparsers.add_parser("import-preview")
    formal_import.add_argument("--manifest", type=Path, required=True)
    formal_import.add_argument("--preview-a", type=Path, required=True)
    formal_import.add_argument("--preview-b", type=Path, required=True)
    formal_import.add_argument("--dual-verification", type=Path, required=True)
    formal_import.add_argument("--migration-ref", required=True)
    return parser


def input_paths(args: argparse.Namespace) -> InputPaths:
    """Resolve all contract inputs from one explicit workspace root."""

    workspace = args.workspace.resolve()
    correction = (
        workspace
        / ".helloagents/sessions/deckshell/host-a0a6f569/artifacts/"
        "commit-aligned-history-generator-correction"
    )
    atomic = SKILL_ROOT.parents[2]
    archive = workspace / ".helloagents/archive/2026-07/202607161902_rewrite-treeland-sync-adaptation-fields-v2/evidence"
    repo = workspace / "DeckShell"
    target = workspace / "ds-mod"
    return InputPaths(
        workspace=workspace,
        atomic_root=atomic,
        repo=repo,
        target_worktree=target,
        waylib_repo=repo / "3rdparty/waylib-shared",
        protocol_repo=workspace / "treeland-protocols",
        v1_manifest=correction / "final-manifest.json",
        v1_source_mapping=correction / "source-mapping.json",
        v1_rewrite_mapping=correction / "verification/rewrite-target-mapping.json",
        v1_object_result=correction / "verification/object-rewrite-result.json",
        v1_applied_verification=(
            correction / "verification/applied-history-verification.json"
        ),
        v1_product_manifest=atomic / "corrected-v1/formal/product-manifest.json",
        v1_atomic_mapping=atomic / "corrected-v1/preview-A/mapping.json",
        v1_history_contract=(
            atomic / "corrected-v1/formal/history-contract-verification.json"
        ),
        task8_evidence=atomic / "verification/task-8.json",
        task9_evidence=atomic / "verification/task-9.json",
        refs_before=atomic / "inputs/remediation-atomic-replay-correction-refs-before.json",
        build_environment=atomic / "inputs/build-environment.json",
        protocol_ledger=atomic / "ledgers/protocol-transition-ledger.v1.json",
        dependency_set=atomic / "ledgers/dependency-sensitive-set-D.json",
        dependency_bundle=atomic / "ledgers/dependency-bundle-ledger.v1.json",
        runtime_observations=(
            atomic / "inputs/runtime-dependency-observations.v1.json"
        ),
        protocol_lock=atomic / "inputs/treeland-protocols-lock.json",
        anchor_provenance=atomic / "inputs/anchor-protocol-provenance.json",
        legacy_v2_candidate=(
            correction / "corrected-v2/formal/candidate-input-manifest.v2.json"
        ),
        legacy_v2_manifest=(
            correction / "corrected-v2/formal/input-manifest.v2.json"
        ),
        legacy_v2_mapping=(
            correction / "corrected-v2/preview-A/rewrite-target-mapping.v2.json"
        ),
        bootstrap_transition_map=(
            correction / "inputs/bootstrap-transition-map.v1.json"
        ),
        anchor_generation=atomic / "proof-nodes/index-1/generation.json",
        input_lock=correction / "inputs/input-lock.json",
        remediation_ledger=(
            correction / "inputs/remediation-ownership-ledger.v2.json"
        ),
        master_product_manifest=atomic / "inputs/master-product-manifest.json",
        product_overlay_rules=atomic / "inputs/product-overlay-rules.v1.json",
        adaptation_manifest=archive / "manifest/adaptation-manifest.v2.json",
        legacy_inventory=archive / "source/legacy/inventory.json",
        equivalence_evidence=archive / "verification/equivalence-r3.json",
        waylib_sync_record=repo / "3rdparty/waylib-shared/docs/treeland-waylib-qwlroots-sync_202605220117_zh.md",
        waylib_mapping_gate=repo / "3rdparty/waylib-shared/docs/treeland-waylib-qwlroots-history-mapping-gate_20260713_zh.md",
        plan=args.plan.resolve(),
        bundle_root=SKILL_ROOT,
        output_directory=args.output.resolve(),
    )


def main(argv: list[str] | None = None) -> int:
    """Run one explicit v2 preparation stage."""

    args = build_parser().parse_args(argv)
    output = args.output.resolve()
    if args.command == "preview":
        artifacts = run_isolated_preview(
            input_paths(args),
            read_hashed_json(args.manifest.resolve()),
            read_hashed_json(args.dry_run.resolve()),
            preview_name=args.preview_name,
            object_directory=args.object_directory.resolve(),
            scratch_directory=args.scratch_directory.resolve(),
        )
        summary = {
            "stage": "preview",
            "preview_name": args.preview_name,
            **write_preview_artifacts(output, artifacts),
        }
        print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
        return 0
    if args.command == "compare-previews":
        payload = compare_previews(
            args.preview_a.resolve(), args.preview_b.resolve()
        )
        destination = output / "dual-preview-verification.v2.json"
        hashes = write_hashed_json(destination, payload)
        print(
            json.dumps(
                {
                    "outcome": "pass",
                    "stage": "compare-previews",
                    "artifact": str(destination),
                    "head": payload["head"],
                    **hashes,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "import-preview":
        payload = run_formal_import(
            input_paths(args),
            read_hashed_json(args.manifest.resolve()),
            preview_a_directory=args.preview_a.resolve(),
            preview_b_directory=args.preview_b.resolve(),
            dual_verification_path=args.dual_verification.resolve(),
            migration_ref=args.migration_ref,
        )
        destination = output / "formal-object-import.v2.json"
        hashes = write_hashed_json(destination, payload)
        print(
            json.dumps(
                {
                    "outcome": "pass",
                    "stage": "import-preview",
                    "artifact": str(destination),
                    "head": payload["head"],
                    "migration_ref": payload["migration_ref"],
                    **hashes,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "candidate":
        payload = build_candidate_manifest(input_paths(args))
        destination = output / "candidate-input-manifest.v2.json"
    elif args.command == "freeze":
        payload = freeze_candidate(
            read_hashed_json(args.candidate.resolve()), input_paths(args)
        )
        destination = output / "input-manifest.v2.json"
    else:
        payload = run_sequential_dry_run(
            input_paths(args).repo,
            read_hashed_json(args.manifest.resolve()),
            json.loads(
                input_paths(args).remediation_ledger.read_text(encoding="utf-8")
            ),
        )
        destination = output / "sequential-dry-run-v2.json"
    hashes = write_hashed_json(destination, payload)
    print(
        json.dumps(
            {
                "outcome": "pass",
                "stage": args.command,
                "artifact": str(destination),
                "entries": len(payload.get("entries", payload.get("records", []))),
                **hashes,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
