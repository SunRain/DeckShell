"""Independent v2 adapter for compile-atomic node verification."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from typing import Any

from .atomic_verifiers.dependency import validate_atomic_bundle
from .atomic_verifiers.dependency_bundle import verify_dependency_bundle_ledger
from .atomic_verifiers.dependency_set import verify_dependency_set
from .atomic_verifiers.protocol_ledger import verify_protocol_ledger
from .atomic_verifiers.protocol_source import (
    validate_protocol_alignment,
    validate_protocol_source,
)

from .product_oracle import compare_three_way_product_entries


def validate_atomic_replay_contract(contract: Mapping[str, Any]) -> dict[str, int]:
    """Recompute every independent v2 replay authority from raw inputs."""

    replay_pairs = _sequence(contract, "replay_pairs")
    nodes = _sequence(contract, "nodes")
    _verify_replay_pairs(replay_pairs)
    for node in nodes:
        validate_node_contract(_mapping_value(node, "node"))
    protocol = _verify_protocol(_mapping(contract, "protocol"))
    _verify_dependency_set(_mapping(contract, "dependency_set"))
    dependency = _verify_dependency_bundle(
        _mapping(contract, "dependency_bundle")
    )
    _verify_product(_mapping(contract, "product"))
    return {
        "replay_pair_count": len(replay_pairs),
        "node_count": len(nodes),
        "protocol_component_count": protocol,
        "dependency_component_count": dependency,
    }


def _verify_replay_pairs(pairs: Sequence[Any]) -> None:
    for raw_pair in pairs:
        pair = _mapping_value(raw_pair, "replay pair")
        source = pair.get("source_delta_sha256")
        v1 = pair.get("v1_delta_sha256")
        v2 = pair.get("v2_delta_sha256")
        if not all(_is_sha256(value) for value in (source, v1, v2)):
            raise ValueError("replay pair contains an invalid SHA-256")
        if v1 != source or v2 != source:
            raise ValueError(
                "shared v1/v2 replay drift at "
                f"{pair.get('ordered_index')}"
            )


def _verify_protocol(section: Mapping[str, Any]) -> int:
    ledger = _mapping(section, "ledger")
    source = _mapping_sequence(section, "source_components")
    verify_protocol_ledger(
        ledger,
        source,
        _string_sequence(section, "ancestry_order"),
        set(_int_sequence(section, "valid_owner_indexes")),
        is_ancestor=section.get("is_ancestor"),
        read_blob=section.get("read_blob"),
    )
    return len(ledger.get("components", ()))


def _verify_dependency_set(section: Mapping[str, Any]) -> None:
    verify_dependency_set(
        _mapping(section, "ledger"),
        ordinary_candidates=_mapping_sequence(section, "ordinary_candidates"),
        remediation_targets=set(_int_sequence(section, "remediation_targets")),
        carry_forward_entry_ids=set(
            _string_sequence(section, "carry_forward_entry_ids")
        ),
        protocol_components=_mapping_sequence(section, "protocol_components"),
    )


def _verify_dependency_bundle(section: Mapping[str, Any]) -> int:
    ledger = _mapping(section, "ledger")
    verify_dependency_bundle_ledger(
        ledger,
        expected_components=_mapping_sequence(section, "expected_components"),
        valid_owner_indexes=set(_int_sequence(section, "valid_owner_indexes")),
        is_ancestor=section.get("is_ancestor"),
    )
    return len(ledger.get("components", ()))


def _verify_product(section: Mapping[str, Any]) -> None:
    master = _mapping_sequence(section, "master_entries")
    expected = section.get("master_entries_sha256")
    if not _is_sha256(expected) or _canonical_sha256(master) != expected:
        raise ValueError("master oracle drift")
    compare_three_way_product_entries(
        master,
        _mapping_sequence(section, "v1_entries"),
        _mapping_sequence(section, "v2_entries"),
    )


def _canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _mapping(parent: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    return _mapping_value(parent.get(key), key)


def _mapping_value(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    return value


def _sequence(parent: Mapping[str, Any], key: str) -> Sequence[Any]:
    value = parent.get(key)
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{key} must be a sequence")
    return value


def _mapping_sequence(
    parent: Mapping[str, Any], key: str
) -> list[Mapping[str, Any]]:
    return [_mapping_value(value, key) for value in _sequence(parent, key)]


def _string_sequence(parent: Mapping[str, Any], key: str) -> list[str]:
    values = list(_sequence(parent, key))
    if any(not isinstance(value, str) for value in values):
        raise ValueError(f"{key} must contain strings")
    return values


def _int_sequence(parent: Mapping[str, Any], key: str) -> list[int]:
    values = list(_sequence(parent, key))
    if any(not isinstance(value, int) or isinstance(value, bool) for value in values):
        raise ValueError(f"{key} must contain integers")
    return values


def validate_node_contract(node: Mapping[str, Any]) -> None:
    """Recompute protocol and dependency contracts for one replayed node."""

    owner_index = node.get("owner_index")
    if not isinstance(owner_index, int) or owner_index < 1:
        raise ValueError("node owner_index must be a positive integer")
    validate_protocol_source(node.get("files", {}))
    validate_protocol_alignment(
        node.get("generated_signatures", {}),
        node.get("consumed_signatures", {}),
    )
    validate_atomic_bundle(owner_index, node.get("bundle_members", []))
