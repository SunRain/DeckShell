"""Rebuild compile-atomic ledgers from their frozen source inputs."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from .atomic_bindings import is_ancestor
from .artifacts import canonical_bytes, read_hashed_json
from .atomic_verifiers.dependency_builder import build_dependency_set
from .atomic_verifiers.dependency_bundle_builder import (
    build_dependency_bundle_ledger,
)
from .atomic_verifiers.protocol_ledger_builder import (
    build_protocol_ledger,
    source_components_from_lock,
)
from .context import InputPaths
from .repository import GitRepository


def rebuild_atomic_ledgers(
    paths: InputPaths, repo: GitRepository
) -> dict[str, Any]:
    """Recompute protocol, dependency-set, and bundle authorities."""

    protocol_repo = GitRepository(paths.protocol_repo)
    waylib_repo = GitRepository(paths.waylib_repo)
    lock = read_sidecar_json(paths.protocol_lock, "artifact_sha256")
    provenance = read_sidecar_json(paths.anchor_provenance, "artifact_sha256")
    generation = read_sidecar_json(paths.anchor_generation, "artifact_sha256")
    legacy_mapping = read_hashed_json(paths.legacy_v2_mapping)
    stored_protocol = read_sidecar_json(paths.protocol_ledger, "artifact_sha256")
    rebuilt_protocol = build_protocol_ledger(
        lock,
        anchor_commit=provenance["protocol_source_commit"],
        owner_entries=_owner_entries(legacy_mapping, generation),
        read_blob=lambda object_id: protocol_repo.cat_file("blob", object_id),
    )
    _require_equal("protocol transition ledger", stored_protocol, rebuilt_protocol)

    legacy_manifest = read_hashed_json(paths.legacy_v2_manifest)
    bootstrap = read_sidecar_json(paths.bootstrap_transition_map)
    remediation = read_sidecar_json(paths.remediation_ledger, "canonical_sha256")
    runtime = read_sidecar_json(paths.runtime_observations, "artifact_sha256")
    stored_dependency = read_sidecar_json(paths.dependency_set, "artifact_sha256")
    anchor_commit = next(
        entry["expected_v1_commit"]
        for entry in legacy_manifest["entries"]
        if entry["ordered_index"] == 1
    )
    rebuilt_dependency = build_dependency_set(
        legacy_manifest,
        legacy_mapping,
        bootstrap,
        remediation,
        stored_protocol,
        patch_provider=lambda entry: repo.run(
            "diff",
            "--no-ext-diff",
            "--unified=0",
            entry["expected_v1_parent"],
            entry["expected_v1_commit"],
        ).decode("utf-8", errors="strict"),
        baseline_symbol_exists=lambda symbol: _symbol_exists(
            repo, anchor_commit, symbol
        ),
        runtime_observations=runtime["observations"],
        waylib_is_ancestor=lambda older, newer: is_ancestor(
            waylib_repo, older, newer
        ),
        waylib_blob_reader=lambda commit, path: waylib_repo.run(
            "show", f"{commit}:{path}"
        ).decode("utf-8", errors="strict"),
    )
    _require_equal("dependency-sensitive set", stored_dependency, rebuilt_dependency)

    stored_bundle = read_sidecar_json(paths.dependency_bundle, "artifact_sha256")
    protocol_for_bundle = dict(rebuilt_protocol)
    protocol_for_bundle["artifact_sha256"] = stored_protocol["artifact_sha256"]
    dependency_for_bundle = dict(rebuilt_dependency)
    dependency_for_bundle["artifact_sha256"] = stored_dependency["artifact_sha256"]
    rebuilt_bundle = build_dependency_bundle_ledger(
        dependency_for_bundle,
        protocol_for_bundle,
        remediation,
    )
    _require_equal("dependency bundle ledger", stored_bundle, rebuilt_bundle)
    source_components = source_components_from_lock(
        lock, anchor_commit=provenance["protocol_source_commit"]
    )
    return {
        "protocol_lock": lock,
        "protocol_source_components": source_components,
        "protocol": stored_protocol,
        "dependency": stored_dependency,
        "bundle": stored_bundle,
        "rebuilt_bundle": rebuilt_bundle,
        "remediation": remediation,
        "runtime_observations": runtime,
        "legacy_manifest": legacy_manifest,
        "protocol_recomputed_sha256": _payload_sha256(rebuilt_protocol),
        "dependency_recomputed_sha256": _payload_sha256(rebuilt_dependency),
        "bundle_recomputed_sha256": _payload_sha256(rebuilt_bundle),
    }


def read_sidecar_json(
    path: Path, canonical_field: str | None = None
) -> dict[str, Any]:
    """Read a raw-sidecar JSON artifact and optionally verify its self hash."""

    raw = path.read_bytes()
    sidecar = path.with_name(path.name + ".sha256")
    parts = sidecar.read_text(encoding="ascii").strip().split()
    if (
        len(parts) != 2
        or parts[1] != path.name
        or parts[0] != hashlib.sha256(raw).hexdigest()
    ):
        raise ValueError(f"file SHA-256 mismatch: {path}")
    payload = json.loads(raw.decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    if canonical_field is not None:
        expected = payload.get(canonical_field)
        unhashed = copy.deepcopy(payload)
        unhashed.pop(canonical_field, None)
        if expected != _payload_sha256(unhashed):
            raise ValueError(f"canonical payload hash mismatch: {path}")
    return payload


def _owner_entries(
    mapping: dict[str, Any], generation: dict[str, Any]
) -> dict[int, dict[str, Any]]:
    owners = {entry["ordered_index"]: entry for entry in mapping["entries"]}
    owners[1] = {
        **owners[1],
        "expected_v1_commit": generation["old_anchor"],
        "new_commit": generation["new_anchor"],
        "new_tree": generation["new_tree"],
        "actual_v2_changed_paths": generation["changed_paths"],
    }
    if sorted(owners) != list(range(1, 331)):
        raise ValueError("protocol owner mapping is not 1..330")
    return owners


def _symbol_exists(repo: GitRepository, commit: str, symbol: str) -> bool:
    try:
        repo.run(
            "grep",
            "-q",
            "-w",
            symbol,
            commit,
            "--",
            "*.c",
            "*.cc",
            "*.cpp",
            "*.cxx",
            "*.h",
            "*.hpp",
        )
        return True
    except subprocess.CalledProcessError as error:
        if error.returncode == 1:
            return False
        raise


def _require_equal(
    label: str, stored: dict[str, Any], rebuilt: dict[str, Any]
) -> None:
    comparable = copy.deepcopy(stored)
    comparable.pop("artifact_sha256", None)
    if canonical_bytes(comparable) != canonical_bytes(rebuilt):
        raise ValueError(f"{label} independent recomputation drift")


def _payload_sha256(payload: Any) -> str:
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()
