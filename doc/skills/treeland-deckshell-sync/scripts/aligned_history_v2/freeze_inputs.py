"""Freeze corrected-v1 and all independent compile-atomic v2 authorities."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .artifacts import canonical_bytes
from .bundle import bundle_files, bundle_sha256
from .context import InputPaths
from .remediation import validate_remediation_ledger
from .repository import GitRepository


REWRITE_BASE = "62addfbee457d7a15b8aad65165774b954f37d4f"
SHARED_ANCHOR = "86942a0d65d9a202fb2efa0ee1b57d6a7d9ac6ce"
SHARED_ANCHOR_TREE = "a80871ae40573fdb81701508cf888e76793c91ca"
CORRECTED_V1_HEAD = "ae62643041e859039ac2e348f106737314387a53"
CORRECTED_V1_HEAD_TREE = "d165a3343a8533215241f074ce1380c2ba6c4173"
CORRECTED_V1_REF = (
    "refs/heads/migration/"
    "commit-aligned-history-corrected-v1-compile-atomic-r7-20260730"
)
DS_MOD_SNAPSHOT = "6e96d91b6eb526e5dcc8ba6793fc152eb46dc495"
MASTER_COMMIT = "d83f92fc271ab830950345cd5bd109fc2ca36a28"
MASTER_TREE = "6d9f8cc5ec56a071ef39ac8e95f503d82e3e09b0"
NORMALIZED_TREELAND_HEAD = "7da2254d386935f753ed907f8d6e76c1639d01a9"
FINAL_GITLINK = "26f52806c0432c70438a027b7e7659e1cb481b2b"
PROTOCOL_ENDPOINT = "becded8970ff0b7440a00e8c6d5c4f43867c55f1"
PROTOCOL_TREE = "ab850b37bf123fad630318cff815586cb1bbd403"
BUNDLE_REPO_PREFIX = "doc/skills/treeland-deckshell-sync"
CORRECTED_CANDIDATE_REF_PREFIXES = (
    "refs/heads/migration/commit-aligned-history-corrected-v1-",
    "refs/heads/migration/commit-aligned-history-corrected-v2-",
)


def collect_frozen_inputs(paths: InputPaths) -> dict[str, Any]:
    """Fail closed on ref, object, ledger, oracle, or environment drift."""

    repo = GitRepository(paths.repo)
    current = _current_artifacts(paths)
    refs = _verify_refs_and_worktrees(paths, repo, current["refs_before"])
    mapping = current["v1_mapping"]
    _verify_corrected_v1(repo, mapping, current["task8"], current["task9"])
    _verify_authority_links(current, mapping)
    remediation = _read_json(paths.remediation_ledger)
    remediation_summary = validate_remediation_ledger(remediation)
    bundle = bundle_files(paths.bundle_root, BUNDLE_REPO_PREFIX)
    hashes = _input_hashes(paths)
    dependency_indices = list(
        current["dependency_set"]["dependency_sensitive_indices"]
    )
    return {
        "authority_version": "compile-atomic-protocol-alignment-v5-signal-dependency-20260729",
        "rewrite_base": REWRITE_BASE,
        "shared_anchor": SHARED_ANCHOR,
        "shared_anchor_tree": SHARED_ANCHOR_TREE,
        "v1_head": CORRECTED_V1_HEAD,
        "v1_head_tree": CORRECTED_V1_HEAD_TREE,
        "v1_migration_ref": CORRECTED_V1_REF,
        "normalized_treeland_head": NORMALIZED_TREELAND_HEAD,
        "final_gitlink": FINAL_GITLINK,
        "master_commit": MASTER_COMMIT,
        "master_tree": MASTER_TREE,
        "protocol_endpoint": PROTOCOL_ENDPOINT,
        "protocol_endpoint_tree": PROTOCOL_TREE,
        "environment_fingerprint_sha256": current["environment"][
            "fingerprint_sha256"
        ],
        "remediation_ledger_sha256": remediation["canonical_sha256"],
        "remediation_target_count": remediation_summary["target_count"],
        "protocol_ledger_sha256": current["protocol_ledger"][
            "artifact_sha256"
        ],
        "dependency_set_sha256": current["dependency_set"]["artifact_sha256"],
        "dependency_bundle_sha256": current["dependency_bundle"][
            "artifact_sha256"
        ],
        "runtime_dependency_observations_sha256": current[
            "runtime_observations"
        ]["artifact_sha256"],
        "runtime_dependency_observation_count": current[
            "runtime_observations"
        ]["observation_count"],
        "dependency_sensitive_indices": dependency_indices,
        "overlay_rules_sha256": current["overlay_rules"]["artifact_sha256"],
        "master_product_manifest_sha256": current["master_product"][
            "artifact_sha256"
        ],
        "corrected_v1_product_manifest_sha256": current["v1_product"][
            "artifact_sha256"
        ],
        "master_product_entry_count": current["master_product"]["entry_count"],
        "refs": refs,
        "preserved_candidate_refs": _preserved_corrected_candidate_refs(refs),
        "input_file_sha256": hashes,
        "tool_bundle_sha256": bundle_sha256(bundle),
        "tool_bundle_file_count": len(bundle),
        "remote_writes": "forbidden",
    }


def _preserved_corrected_candidate_refs(refs: dict[str, str]) -> list[str]:
    """Classify every frozen local corrected-v1/v2 candidate as preserved."""

    return sorted(
        ref
        for ref in refs
        if ref.startswith(CORRECTED_CANDIDATE_REF_PREFIXES)
    )


def _current_artifacts(paths: InputPaths) -> dict[str, dict[str, Any]]:
    return {
        "refs_before": _read_current(paths.refs_before),
        "environment": _read_current(paths.build_environment),
        "protocol_lock": _read_current(paths.protocol_lock),
        "anchor": _read_current(paths.anchor_provenance),
        "protocol_ledger": _read_current(paths.protocol_ledger),
        "dependency_set": _read_current(paths.dependency_set),
        "dependency_bundle": _read_current(paths.dependency_bundle),
        "runtime_observations": _read_current(paths.runtime_observations),
        "v1_mapping": _read_current(paths.v1_atomic_mapping),
        "v1_history": _read_current(paths.v1_history_contract),
        "v1_product": _read_current(paths.v1_product_manifest),
        "task8": _read_current(paths.task8_evidence),
        "task9": _read_current(paths.task9_evidence),
        "master_product": _read_current(paths.master_product_manifest),
        "overlay_rules": _read_current(paths.product_overlay_rules),
    }


def _verify_refs_and_worktrees(
    paths: InputPaths,
    repo: GitRepository,
    refs_before: dict[str, Any],
) -> dict[str, str]:
    expected = {item["ref"]: item["object"] for item in refs_before["refs"]}
    task = _read_current(paths.atomic_root / "verification/task-8.json")
    expected[str(task["migration_ref"])] = str(task["head"])
    actual = _snapshot_refs(repo)
    if actual != dict(sorted(expected.items())):
        raise ValueError("frozen DeckShell ref set drift")
    if _status(repo) != refs_before["deck_shell_status"]:
        raise ValueError("DeckShell worktree status drift")
    target = GitRepository(paths.target_worktree)
    if _status(target) != refs_before["ds_mod_status"]:
        raise ValueError("ds-mod worktree status drift")
    if target.run("rev-parse", "HEAD").decode().strip() != DS_MOD_SNAPSHOT:
        raise ValueError("ds-mod expected-old drift")
    return dict(sorted(expected.items()))


def _verify_corrected_v1(
    repo: GitRepository,
    mapping: dict[str, Any],
    task8: dict[str, Any],
    task9: dict[str, Any],
) -> None:
    if mapping.get("head") != CORRECTED_V1_HEAD:
        raise ValueError("corrected-v1 mapping head drift")
    if mapping.get("head_tree") != CORRECTED_V1_HEAD_TREE:
        raise ValueError("corrected-v1 mapping tree drift")
    records = mapping.get("records", ())
    if len(records) != 330 or records[0].get("commit") != SHARED_ANCHOR:
        raise ValueError("corrected-v1 mapping record drift")
    if repo.run("rev-parse", CORRECTED_V1_REF).decode().strip() != CORRECTED_V1_HEAD:
        raise ValueError("corrected-v1 migration ref drift")
    if repo.tree_id(CORRECTED_V1_HEAD) != CORRECTED_V1_HEAD_TREE:
        raise ValueError("corrected-v1 formal object tree drift")
    if task8.get("head") != CORRECTED_V1_HEAD or task9.get("head") != CORRECTED_V1_HEAD:
        raise ValueError("corrected-v1 task evidence drift")
    if task8.get("outcome") != "pass" or task9.get("outcome") != "pass":
        raise ValueError("corrected-v1 task evidence is not passing")


def _verify_authority_links(
    current: dict[str, dict[str, Any]], mapping: dict[str, Any]
) -> None:
    protocol_lock = current["protocol_lock"]
    if (
        protocol_lock.get("endpoint") != PROTOCOL_ENDPOINT
        or protocol_lock.get("endpoint_tree") != PROTOCOL_TREE
    ):
        raise ValueError("frozen protocol endpoint drift")
    if current["anchor"].get("protocol_source_commit") not in {
        item["commit"] for item in protocol_lock["history"]
    }:
        raise ValueError("anchor protocol provenance drift")
    if len(current["dependency_set"].get("dependency_sensitive_indices", ())) != 129:
        raise ValueError("dependency-sensitive set size drift")
    if current["dependency_bundle"].get("component_count") != 670:
        raise ValueError("dependency component count drift")
    if current["runtime_observations"].get("observation_count") != 1:
        raise ValueError("runtime dependency observation count drift")
    if current["protocol_ledger"].get("source_component_count") != 97:
        raise ValueError("protocol component count drift")
    if mapping["records"][-1].get("gitlink") != FINAL_GITLINK:
        raise ValueError("corrected-v1 final gitlink drift")
    if current["v1_history"].get("outcome") != "pass":
        raise ValueError("corrected-v1 history contract is not passing")
    if current["task9"].get("product_entries_sha256") != current[
        "master_product"
    ].get("entries_sha256"):
        raise ValueError("corrected-v1 product oracle binding drift")


def _input_hashes(paths: InputPaths) -> dict[str, str]:
    files = {
        "legacy_v2_candidate": paths.legacy_v2_candidate,
        "legacy_v2_manifest": paths.legacy_v2_manifest,
        "legacy_v2_mapping": paths.legacy_v2_mapping,
        "bootstrap_transition_map": paths.bootstrap_transition_map,
        "anchor_generation": paths.anchor_generation,
        "legacy_v1_manifest": paths.v1_manifest,
        "remediation_ledger": paths.remediation_ledger,
        "v1_atomic_mapping": paths.v1_atomic_mapping,
        "v1_history_contract": paths.v1_history_contract,
        "v1_product_manifest": paths.v1_product_manifest,
        "protocol_ledger": paths.protocol_ledger,
        "dependency_set": paths.dependency_set,
        "dependency_bundle": paths.dependency_bundle,
        "runtime_observations": paths.runtime_observations,
        "master_product_manifest": paths.master_product_manifest,
        "product_overlay_rules": paths.product_overlay_rules,
        "build_environment": paths.build_environment,
        "plan": paths.plan,
    }
    return {name: _sha256_file(path) for name, path in files.items()}


def _read_current(path: Path) -> dict[str, Any]:
    value = _read_json(path)
    payload = dict(value)
    expected = payload.pop("artifact_sha256", None)
    actual = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    if expected != actual:
        raise ValueError(f"current artifact canonical hash drift: {path}")
    _verify_sidecar(path)
    return value


def _verify_sidecar(path: Path) -> None:
    sidecar = path.with_name(path.name + ".sha256")
    parts = sidecar.read_text(encoding="utf-8").split()
    if len(parts) != 2 or parts[1] != path.name:
        raise ValueError(f"invalid artifact sidecar: {sidecar}")
    if parts[0] != _sha256_file(path):
        raise ValueError(f"artifact raw hash drift: {path}")


def _snapshot_refs(repo: GitRepository) -> dict[str, str]:
    payload = repo.run("for-each-ref", "--format=%(refname)%00%(objectname)")
    refs: dict[str, str] = {}
    for line in payload.decode().splitlines():
        ref, separator, object_id = line.partition("\0")
        if not separator:
            raise ValueError("invalid ref snapshot record")
        refs[ref] = object_id
    return dict(sorted(refs.items()))


def _status(repo: GitRepository) -> list[str]:
    value = repo.run("status", "--short").decode().strip()
    return value.splitlines() if value else []


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
