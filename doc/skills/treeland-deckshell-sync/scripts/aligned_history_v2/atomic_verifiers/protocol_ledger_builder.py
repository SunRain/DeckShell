"""Build a protocol transition ledger from frozen Git object metadata."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from collections.abc import Callable, Mapping
from typing import Any

from .protocol_policy import assign_protocol_owner
from .protocol_signature import generated_signatures


_FIXED_COMPONENT_OWNERS = (
    (
        "1a55a4fc7ae13285e7b6f809720c02c1b1175f88",
        "xml/treeland-wine-window-management-unstable-v1.xml",
        83,
    ),
    (
        "1a55a4fc7ae13285e7b6f809720c02c1b1175f88",
        "xml/treeland-wine-window-state-unstable-v1.xml",
        81,
    ),
    (
        "4439beed371577c01090e4cb4bd91e34a054fecc",
        "xml/treeland-wine-window-management-unstable-v1.xml",
        83,
    ),
    (
        "4439beed371577c01090e4cb4bd91e34a054fecc",
        "xml/treeland-wine-window-state-unstable-v1.xml",
        81,
    ),
)


def _canonical_sha256(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8") + b"\n"
    return hashlib.sha256(raw).hexdigest()


def _side_fields(side: Mapping[str, Any] | None) -> tuple[str | None, str | None]:
    if side is None:
        return None, None
    return side["object"], side["sha256"]


def source_components_from_lock(
    lock: Mapping[str, Any], *, anchor_commit: str
) -> list[dict[str, Any]]:
    """Flatten every frozen XML change without losing source ordering."""

    commits = [item["commit"] for item in lock["history"]]
    try:
        anchor_sequence = commits.index(anchor_commit)
    except ValueError as error:
        raise ValueError(f"anchor source commit is not frozen: {anchor_commit}") from error

    components = []
    for source_sequence, history_entry in enumerate(lock["history"]):
        for component_sequence, change in enumerate(history_entry["changes"]):
            before_blob, before_sha256 = _side_fields(change["before"])
            after_blob, after_sha256 = _side_fields(change["after"])
            source_path = change["path"]
            components.append(
                {
                    "protocol_component_id": (
                        f"treeland-protocols:{history_entry['commit']}:{source_path}"
                    ),
                    "source_sequence": source_sequence,
                    "component_sequence": component_sequence,
                    "source_commit": history_entry["commit"],
                    "source_parent": history_entry["parents"][0],
                    "source_parents": history_entry["parents"],
                    "source_tree": history_entry["tree"],
                    "source_path": source_path,
                    "target_path": f"protocols/compositor/{source_path}",
                    "status": change["status"],
                    "old_mode": change["old_mode"],
                    "new_mode": change["new_mode"],
                    "before_blob": before_blob,
                    "before_sha256": before_sha256,
                    "after_blob": after_blob,
                    "after_sha256": after_sha256,
                    "anchor_absorbed": source_sequence <= anchor_sequence,
                }
            )
    return components


def _signatures(
    object_id: str | None, read_blob: Callable[[str], bytes]
) -> list[str]:
    if object_id is None:
        return []
    return list(generated_signatures(read_blob(object_id)))


def build_protocol_ledger(
    lock: Mapping[str, Any],
    *,
    anchor_commit: str,
    owner_entries: Mapping[int, Mapping[str, Any]],
    read_blob: Callable[[str], bytes],
) -> dict[str, Any]:
    """Join frozen changes, generated signatures, and explicit DeckShell owners."""

    source_components = source_components_from_lock(lock, anchor_commit=anchor_commit)
    components = []
    owner_counts: Counter[int] = Counter()
    for source in source_components:
        decision = assign_protocol_owner(
            source["source_commit"],
            source["source_path"],
            anchor_absorbed=source["anchor_absorbed"],
        )
        try:
            owner = owner_entries[decision.owner_index]
        except KeyError as error:
            raise ValueError(f"owner index is unavailable: {decision.owner_index}") from error
        before_signatures = _signatures(source["before_blob"], read_blob)
        after_signatures = _signatures(source["after_blob"], read_blob)
        owner_counts[decision.owner_index] += 1
        components.append(
            {
                **source,
                "owner_index": decision.owner_index,
                "owner_source_commit": owner["expected_v1_commit"],
                "provisional_owner_commit": owner["new_commit"],
                "provisional_owner_tree": owner["new_tree"],
                "owner_basis": decision.basis,
                "consumer_paths": list(decision.consumer_paths),
                "generated_signatures_before": before_signatures,
                "generated_signatures_after": after_signatures,
                "generated_signatures": after_signatures,
                "generated_signature_changed": before_signatures != after_signatures,
                "local_overlay_components": [],
                "result_blob": source["after_blob"],
                "result_sha256": source["after_sha256"],
                "build_proof_status": "pending-task-7",
                "verification": [
                    "ancestry",
                    "owner",
                    "source-blob",
                    "generated-signature",
                    "result-blob",
                ],
            }
        )

    component_identities = {
        (component["source_commit"], component["source_path"])
        for component in components
    }
    fixed_component_mappings = [
        {
            "source_commit": source_commit,
            "source_path": source_path,
            "owner_index": owner_index,
        }
        for source_commit, source_path, owner_index in _FIXED_COMPONENT_OWNERS
        if (source_commit, source_path) in component_identities
    ]

    return {
        "schema_version": 1,
        "kind": "protocol-transition-ledger-v1",
        "source_endpoint": lock["endpoint"],
        "source_endpoint_tree": lock["endpoint_tree"],
        "anchor_source_commit": anchor_commit,
        "source_component_count": len(source_components),
        "convergence_owner_index": 318,
        "fixed_mappings": {
            "36027231fdff84f11c79616aeeaa59e9757c4368": 141,
        },
        "fixed_component_mappings": fixed_component_mappings,
        "owner_component_counts": {
            str(owner): count for owner, count in sorted(owner_counts.items())
        },
        "components_sha256": _canonical_sha256(components),
        "components": components,
    }
