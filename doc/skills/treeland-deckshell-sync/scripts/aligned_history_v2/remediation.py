"""Independent corrected-v2 remediation provenance and count gates."""

from __future__ import annotations

import hashlib
import subprocess
from collections import Counter
from typing import Any

from .artifacts import canonical_bytes
from .git_objects import parse_raw_commit
from .repository import GitRepository
from .tree_transition import parse_raw_transition


REMEDIATED_INDICES = (133, 146, 148, 159, 174, 180, 194, 231, 233, 278, 284)
REGENERATION_INDICES = (316, 329, 330)


def validate_remediation_ledger(
    ledger: dict[str, Any], *, expected_canonical_sha256: str | None = None
) -> dict[str, int]:
    """Validate the self-hash and one-to-one component ownership partition."""

    payload = dict(ledger)
    expected = payload.pop("canonical_sha256", None)
    actual = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    if expected != actual:
        raise ValueError("remediation ledger canonical hash drift")
    if expected_canonical_sha256 and actual != expected_canonical_sha256:
        raise ValueError("remediation ledger frozen hash drift")
    components = ledger.get("components")
    targets = ledger.get("targets")
    if not isinstance(components, list) or not isinstance(targets, list):
        raise ValueError("remediation ledger inventory is invalid")
    inventory = [str(row.get("component_id")) for row in components]
    if len(inventory) != len(set(inventory)) or "None" in inventory:
        raise ValueError("remediation component inventory is invalid")
    indices = [row.get("target_index") for row in targets]
    if tuple(indices) != REMEDIATED_INDICES:
        raise ValueError("remediation target indices drift")
    assigned = [
        str(component_id)
        for target in targets
        for component_id in target.get("component_ids", [])
    ]
    counts = Counter(assigned)
    if set(counts) != set(inventory) or any(count != 1 for count in counts.values()):
        raise ValueError("remediation component partition drift")
    for target in targets:
        _validate_target(target)
    return {
        "component_count": len(inventory),
        "target_count": len(targets),
        "missing": 0,
        "duplicate": 0,
        "unexplained": 0,
    }


def build_remediation_proof(
    repo: GitRepository,
    waylib_repo: GitRepository,
    entry: dict[str, Any],
    target: dict[str, Any],
    ledger_sha256: str,
) -> dict[str, Any]:
    """Recompute one target proof from Git objects, not v1 pass fields."""

    index = int(entry["ordered_index"])
    if target["target_index"] != index:
        raise ValueError(f"remediation target mismatch at {index}")
    source = str(target["source_commit"])
    source_raw = parse_raw_commit(repo.cat_file("commit", source))
    source_delta = repo.raw_transition(source_raw.parent, source)
    source_paths = [
        change.path for change in parse_raw_transition(source_delta)
    ]
    legacy = str(target["legacy_target_commit"])
    if repo.run("cat-file", "-t", legacy).decode().strip() != "commit":
        raise ValueError(f"legacy remediation target is not a commit at {index}")
    v1_legacy = str(entry["source_objects"].get("legacy_deckshell_target"))
    if repo.run("cat-file", "-t", v1_legacy).decode().strip() != "commit":
        raise ValueError(f"v1 legacy target is not a commit at {index}")
    corrected_commit = str(entry["expected_v1_commit"])
    corrected_parent = str(entry["expected_v1_parent"])
    corrected_delta = repo.raw_transition(corrected_parent, corrected_commit)
    corrected_paths = [
        change.path for change in parse_raw_transition(corrected_delta)
    ]
    waylib = str(target["waylib_gitlink"])
    if waylib_repo.run("cat-file", "-t", waylib).decode().strip() != "commit":
        raise ValueError(f"remediation Waylib target is not a commit at {index}")
    gitlink_after = str(entry["gitlink_after"])
    try:
        waylib_repo.run("merge-base", "--is-ancestor", waylib, gitlink_after)
    except subprocess.CalledProcessError as error:
        raise ValueError(f"remediation Waylib ancestry failed at {index}") from error
    if entry["source_objects"].get("normalized_treeland_commit") != source:
        raise ValueError(f"remediation normalized source drift at {index}")
    if entry.get("expected_v1_changed_paths") != corrected_paths:
        raise ValueError(f"remediation corrected-v1 paths drift at {index}")
    return {
        "ledger_sha256": ledger_sha256,
        "target_index": index,
        "source_commit": source,
        "source_parent": source_raw.parent,
        "source_tree": source_raw.tree,
        "source_delta_sha256": hashlib.sha256(source_delta).hexdigest(),
        "source_changed_paths": source_paths,
        "legacy_target_commit": legacy,
        "v1_legacy_deckshell_target": v1_legacy,
        "waylib_gitlink": waylib,
        "waylib_ancestry_pass": True,
        "component_ids": list(target["component_ids"]),
        "paths": list(target["paths"]),
        "corrected_v1_commit": corrected_commit,
        "corrected_v1_parent": corrected_parent,
        "corrected_v1_tree": entry["expected_v1_tree"],
        "corrected_v1_delta_sha256": hashlib.sha256(corrected_delta).hexdigest(),
        "corrected_v1_changed_paths": corrected_paths,
    }


def validate_remediation_transitions(
    manifest: dict[str, Any], ledger: dict[str, Any]
) -> dict[str, int]:
    """Require exact transition counts and ledger-bound proofs at 11 indices."""

    validate_remediation_ledger(ledger)
    entries = manifest.get("entries")
    if not isinstance(entries, list) or len(entries) != 330:
        raise ValueError("remediation validation requires 330 entries")
    counts = Counter(str(entry.get("tree_transition")) for entry in entries)
    expected_counts = {
        "replay-rebuilt-anchor": 1,
        "replay-v1-delta": 186,
        "replay-dependency-proven-v1-delta": 129,
        "replay-remediated-v1-delta": 11,
        "regenerate": 3,
    }
    if counts != Counter(expected_counts):
        raise ValueError(f"transition distribution drift: {dict(counts)}")
    actual_indices = tuple(
        int(entry["ordered_index"])
        for entry in entries
        if entry["tree_transition"] == "replay-remediated-v1-delta"
    )
    if actual_indices != REMEDIATED_INDICES:
        raise ValueError(f"remediated indices drift: {actual_indices}")
    targets = {target["target_index"]: target for target in ledger["targets"]}
    for entry in entries:
        index = int(entry["ordered_index"])
        proof = entry.get("remediation_proof")
        if index not in targets:
            if proof is not None:
                raise ValueError(f"unexpected remediation proof at {index}")
            continue
        _validate_proof(proof, targets[index], ledger["canonical_sha256"], index)
    return {
        "rebuilt_anchor": 1,
        "ordinary": 186,
        "dependency_proven": 129,
        "remediated": 11,
        "regenerate": 3,
        "total": 330,
    }


def verify_remediation_sources(
    manifest: dict[str, Any],
    ledger: dict[str, Any],
    repo: GitRepository,
    waylib_repo: GitRepository,
) -> dict[str, int]:
    """Recompute every stored proof against source and Waylib objects."""

    summary = validate_remediation_transitions(manifest, ledger)
    targets = {target["target_index"]: target for target in ledger["targets"]}
    for index in REMEDIATED_INDICES:
        entry = manifest["entries"][index - 1]
        actual = build_remediation_proof(
            repo, waylib_repo, entry, targets[index], ledger["canonical_sha256"]
        )
        if entry["remediation_proof"] != actual:
            raise ValueError(f"remediation proof drift at {index}")
    return {"source_proofs": 11, "waylib_ancestry_proofs": 11, **summary}


def _validate_target(target: dict[str, Any]) -> None:
    required = {
        "target_index",
        "source_commit",
        "legacy_target_commit",
        "waylib_gitlink",
        "component_ids",
        "paths",
    }
    if not required.issubset(target):
        raise ValueError("remediation target lacks required fields")
    for field in ("source_commit", "legacy_target_commit", "waylib_gitlink"):
        value = target[field]
        if not isinstance(value, str) or len(value) != 40:
            raise ValueError(f"remediation target has invalid {field}")
    for field in ("component_ids", "paths"):
        value = target[field]
        if not isinstance(value, list) or not value or len(value) != len(set(value)):
            raise ValueError(f"remediation target has invalid {field}")


def _validate_proof(
    proof: Any,
    target: dict[str, Any],
    ledger_sha256: str,
    index: int,
) -> None:
    if not isinstance(proof, dict):
        raise ValueError(f"remediation proof missing at {index}")
    expected = {
        "ledger_sha256": ledger_sha256,
        "target_index": index,
        "source_commit": target["source_commit"],
        "legacy_target_commit": target["legacy_target_commit"],
        "waylib_gitlink": target["waylib_gitlink"],
        "component_ids": target["component_ids"],
        "paths": target["paths"],
    }
    for field, value in expected.items():
        if proof.get(field) != value:
            label = "component IDs" if field == "component_ids" else field
            raise ValueError(f"remediation {label} drift at {index}")
