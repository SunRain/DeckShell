"""Build the 330-entry input-only manifest from frozen v1 evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .artifacts import canonical_bytes, read_hashed_json
from .bundle import bundle_files, bundle_overlay
from .context import InputPaths
from .freeze_inputs import BUNDLE_REPO_PREFIX, REWRITE_BASE, collect_frozen_inputs
from .git_objects import parse_raw_commit
from .manifest import validate_input_manifest
from .remediation import (
    REMEDIATED_INDICES,
    build_remediation_proof,
    validate_remediation_ledger,
    validate_remediation_transitions,
)
from .repository import GitRepository
from .tree_transition import parse_raw_transition


REGENERATION_INDICES = {316, 329, 330}
AUDIT_PATH = "doc/ai/waylibshared_7dc11a_regression_audit.md"
PLAN_PATH = "doc/ai/deckshell_waylib_commit_aligned_history_rewrite_plan.md"
ADAPTATION_DOCS_PREFIX = "doc/treeland-sync/adaptations/"
LEGACY_SOURCE_DISPOSITIONS = {
    "63c0784ef49aac5783f121d7c163fa56aaf45987": ("superseded", []),
    "b36ded6fef4d0482abc477ce690f027e5fe019d7": ("contribution", [329]),
    "5ddf13c4c06695ae6e49cf8d4d44e4d2414d5e71": ("contribution", [329]),
    "58170bea2ba9c6075f3ba9ac3236e191ac779cd4": ("contribution", [330]),
    "f1483a00da89976db133e8ff544c00362147827a": ("excluded", []),
}


def build_candidate_manifest(paths: InputPaths) -> dict[str, Any]:
    """Build and validate a candidate manifest without writing Git objects."""

    frozen_inputs = collect_frozen_inputs(paths)
    template = read_hashed_json(paths.legacy_v2_candidate)
    mapping = _read_json(paths.v1_atomic_mapping)
    ledger = _read_json(paths.remediation_ledger)
    validate_remediation_ledger(
        ledger,
        expected_canonical_sha256=frozen_inputs["remediation_ledger_sha256"],
    )
    entries = template.get("entries")
    records = mapping.get("records")
    if not isinstance(entries, list) or not isinstance(records, list):
        raise ValueError("v2 template or corrected-v1 mapping is invalid")
    if len(entries) != 330 or len(records) != 330:
        raise ValueError("v2 template and corrected-v1 mapping require 330 entries")
    repo = GitRepository(paths.repo)
    waylib_repo = GitRepository(paths.waylib_repo)
    remediation_targets = {
        target["target_index"]: target for target in ledger["targets"]
    }
    bundle = bundle_files(paths.bundle_root, BUNDLE_REPO_PREFIX)
    tool_overlay = bundle_overlay(
        repo,
        records[327]["commit"],
        bundle,
        BUNDLE_REPO_PREFIX,
    )
    dependency_indices = set(frozen_inputs["dependency_sensitive_indices"])
    manifest_entries = []
    for index, (entry, record) in enumerate(zip(entries, records, strict=True), 1):
        previous_gitlink = None if index == 1 else records[index - 2]["gitlink"]
        manifest_entries.append(
            _build_entry(
                repo,
                waylib_repo,
                entry,
                record,
                previous_gitlink,
                dependency_indices,
                sorted(tool_overlay),
                remediation_targets.get(index),
                ledger["canonical_sha256"],
            )
        )
    candidate = {
        "schema_version": 2,
        "workflow_mode": "commit-aligned-history-rewrite-v2",
        "status": "candidate",
        "frozen_inputs": frozen_inputs,
        "remediation_contract": {
            "ledger_sha256": ledger["canonical_sha256"],
            "target_indices": list(REMEDIATED_INDICES),
            "target_count": len(REMEDIATED_INDICES),
        },
        "compile_atomic_contract": {
            "protocol_ledger_sha256": frozen_inputs["protocol_ledger_sha256"],
            "dependency_set_sha256": frozen_inputs["dependency_set_sha256"],
            "dependency_bundle_sha256": frozen_inputs["dependency_bundle_sha256"],
            "dependency_sensitive_indices": frozen_inputs[
                "dependency_sensitive_indices"
            ],
        },
        "product_oracle_contract": {
            "master_commit": frozen_inputs["master_commit"],
            "master_tree": frozen_inputs["master_tree"],
            "overlay_rules_sha256": frozen_inputs["overlay_rules_sha256"],
            "master_product_manifest_sha256": frozen_inputs[
                "master_product_manifest_sha256"
            ],
        },
        "legacy_source_proofs": _legacy_source_proofs(repo),
        "counts": _contract_counts(),
        "entries": manifest_entries,
    }
    actual_counts = validate_input_manifest(candidate)
    _verify_counts(actual_counts)
    validate_remediation_transitions(candidate, ledger)
    return candidate


def freeze_candidate(
    candidate: dict[str, Any], paths: InputPaths
) -> dict[str, Any]:
    """Promote an unchanged validated candidate to the dry-run input state."""

    validate_input_manifest(candidate)
    if collect_frozen_inputs(paths) != candidate.get("frozen_inputs"):
        raise ValueError("candidate frozen inputs differ from current inputs")
    validate_remediation_transitions(
        candidate, _read_json(paths.remediation_ledger)
    )
    frozen = json.loads(json.dumps(candidate, ensure_ascii=False))
    frozen["status"] = "frozen-input-ready-for-v2-dry-run"
    validate_input_manifest(frozen)
    validate_remediation_transitions(
        frozen, _read_json(paths.remediation_ledger)
    )
    return frozen


def _build_entry(
    repo: GitRepository,
    waylib_repo: GitRepository,
    v1_entry: dict[str, Any],
    record: dict[str, Any],
    previous_gitlink: str | None,
    dependency_indices: set[int],
    tool_overlay_paths: list[str],
    remediation_target: dict[str, Any] | None,
    ledger_sha256: str,
) -> dict[str, Any]:
    index = int(v1_entry["ordered_index"])
    if record["entry_id"] != v1_entry["entry_id"]:
        raise ValueError(f"v1 entry/record mismatch at {index}")
    commit = str(record["commit"])
    raw = parse_raw_commit(repo.cat_file("commit", commit))
    parent = str(record["parent"])
    tree = str(record["tree"])
    if raw.parent != parent or raw.tree != tree:
        raise ValueError(f"v1 raw commit drift at {index}")
    transition_bytes = repo.raw_transition(parent, commit)
    changes = parse_raw_transition(transition_bytes)
    changed_paths = [change.path for change in changes]
    if changed_paths != record["changed_paths"]:
        raise ValueError(f"corrected-v1 changed-path drift at {index}")
    authorized_paths = _authorized_paths(index, changed_paths, tool_overlay_paths)
    message_inputs = _message_inputs_from_template(
        v1_entry,
        raw.message,
        changed_paths,
        authorized_paths,
    )
    transition = _transition_type(
        index,
        dependency_indices=dependency_indices,
        remediated=remediation_target is not None,
    )
    built = {
        "ordered_index": index,
        "entry_id": v1_entry["entry_id"],
        "target_kind": (
            "deckshell-tool-rebuilt-anchor"
            if index == 1
            else v1_entry["target_kind"]
        ),
        "expected_v1_commit": commit,
        "expected_v1_parent": parent,
        "expected_v1_tree": tree,
        "expected_v2_parent": f"commit:{REWRITE_BASE}" if index == 1 else f"entry:{index - 1}",
        "message_schema": message_inputs["schema"],
        "expected_v1_changed_paths": changed_paths,
        "expected_v1_delta_sha256": hashlib.sha256(transition_bytes).hexdigest(),
        "authorized_v2_delta_paths": authorized_paths,
        "tree_transition": transition,
        "remediation_proof": None,
        "gitlink_before": previous_gitlink,
        "gitlink_after": record.get("gitlink"),
        "source_objects": _source_objects_from_template(v1_entry, commit, index),
        "message_inputs": message_inputs,
        "message_inputs_sha256": hashlib.sha256(canonical_bytes(message_inputs)).hexdigest(),
        "regeneration_job": _regeneration_job(index, authorized_paths),
        "test_action": v1_entry.get("test_action", "static-check"),
        "post_assertions": _post_assertions(v1_entry, record, index),
    }
    if remediation_target is not None:
        built["remediation_proof"] = build_remediation_proof(
            repo,
            waylib_repo,
            built,
            remediation_target,
            ledger_sha256,
        )
    return built


def _message_inputs_from_template(
    entry: dict[str, Any],
    raw_message: bytes,
    changed_paths: list[str],
    authorized_paths: list[str],
) -> dict[str, Any]:
    index = int(entry["ordered_index"])
    if index == 1:
        return {
            "schema": "adaptation",
            "subject_body": raw_message.decode("utf-8"),
            "classification": "preserve-tail",
            "action": "preserve-tail",
            "paths": changed_paths,
            "notes": [
                "Replay the corrected-v1 self-contained anchor on the frozen "
                "rewrite base with an independently rendered commit object."
            ],
            "derivation": "patch-equivalent",
        }
    message = json.loads(json.dumps(entry["message_inputs"], ensure_ascii=False))
    if index in REGENERATION_INDICES:
        message["paths"] = authorized_paths
    return message


def _transition_type(
    index: int, *, dependency_indices: set[int], remediated: bool
) -> str:
    if index == 1:
        return "replay-rebuilt-anchor"
    if index in REGENERATION_INDICES:
        return "regenerate"
    if remediated:
        return "replay-remediated-v1-delta"
    if index in dependency_indices:
        return "replay-dependency-proven-v1-delta"
    return "replay-v1-delta"


def _authorized_paths(
    index: int, changed_paths: list[str], tool_overlay_paths: list[str]
) -> list[str]:
    if index == 316:
        return [AUDIT_PATH]
    if index == 329:
        if not tool_overlay_paths:
            raise ValueError("v2 tool bundle has no delta at index 329")
        return tool_overlay_paths
    if index == 330:
        exact = [
            path
            for path in changed_paths
            if not path.startswith(ADAPTATION_DOCS_PREFIX)
        ]
        return [*exact, ADAPTATION_DOCS_PREFIX]
    return changed_paths


def _source_objects_from_template(
    entry: dict[str, Any], commit: str, index: int
) -> dict[str, Any]:
    if index == 1:
        return {
            "corrected_v1_anchor": commit,
            "predecessor_anchor": entry["expected_v1_commit"],
        }
    return json.loads(json.dumps(entry["source_objects"], ensure_ascii=False))


def _post_assertions(
    entry: dict[str, Any], record: dict[str, Any], index: int
) -> list[str]:
    if index == 1:
        return [
            f"parent={REWRITE_BASE}",
            f"tree={record['tree']}",
            "external_protocol_lookup=0",
        ]
    return [
        f"gitlink={record['gitlink']}" if value.startswith("gitlink=") else value
        for value in entry.get("post_assertions", [])
    ]


def _regeneration_job(index: int, authorized_paths: list[str]) -> dict[str, Any] | None:
    if index not in REGENERATION_INDICES:
        return None
    final_output_count = sum(
        not path.endswith("/") for path in authorized_paths
    ) + 58
    jobs = {
        316: ("waylibshared-regression-audit-v2", 1),
        329: ("aligned-history-v2-tool-bundle", len(authorized_paths)),
        330: ("aligned-history-v2-final-documents", final_output_count),
    }
    job, expected_count = jobs[index]
    return {
        "job": job,
        "authorized_paths": authorized_paths,
        "expected_output_count": expected_count,
        "input_projection": "treeland-target-prefix.v2.json" if index in {316, 330} else "frozen-tool-bundle",
        "deterministic": True,
    }


def _legacy_source_proofs(repo: GitRepository) -> list[dict[str, Any]]:
    proofs = []
    for commit, (disposition, target_indices) in LEGACY_SOURCE_DISPOSITIONS.items():
        transition = repo.raw_transition(f"{commit}^", commit)
        changed_paths = [change.path for change in parse_raw_transition(transition)]
        if disposition == "excluded" and not all(path.startswith(".helloagents/") for path in changed_paths):
            raise ValueError("excluded feature source contains non-.helloagents paths")
        proofs.append(
            {
                "commit": commit,
                "parent": repo.run("rev-parse", f"{commit}^").decode().strip(),
                "tree": repo.tree_id(commit),
                "disposition": disposition,
                "target_indices": target_indices,
                "changed_paths": changed_paths,
                "delta_sha256": hashlib.sha256(transition).hexdigest(),
            }
        )
    return proofs


def _contract_counts() -> dict[str, int]:
    return {
        "entries": 330,
        "rebuilt_anchor": 1,
        "rendered": 330,
        "ordinary_rendered_transitions": 186,
        "dependency_proven_rendered_transitions": 129,
        "remediated_rendered_transitions": 11,
        "regeneration_transitions": 3,
        "treeland_targets": 298,
        "other": 233,
        "mixed": 29,
        "dependency_only": 36,
        "waylib_local": 4,
        "waylib_convergence": 3,
        "adaptation_outputs": 25,
        "preserve_tail": 20,
        "paired_dependency_fix": 1,
        "regenerate": 3,
    }


def _verify_counts(counts: dict[str, int]) -> None:
    expected = {
        "deckshell-tool-rebuilt-anchor": 1,
        "treeland-other": 233,
        "treeland-mixed": 29,
        "treeland-dependency-only": 36,
        "waylib-local": 4,
        "waylib-convergence": 3,
        "adaptation-tail": 20,
        "adaptation-paired-dependency": 1,
        "adaptation-regenerated": 3,
    }
    if counts != expected:
        raise ValueError(f"v2 target-kind count mismatch: {counts}")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
