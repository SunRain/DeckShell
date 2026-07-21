"""Validate build-discovered test/runtime dependencies on future Waylib providers."""

from __future__ import annotations

import re
from collections.abc import Callable, Collection, Mapping, Sequence
from typing import Any


RUNTIME_WAYLIB_EDGE_KIND = "test-runtime-waylib-capability"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class RuntimeDependencyError(ValueError):
    """Raised when a runtime dependency observation is incomplete or inconsistent."""


def _required_text(value: Mapping[str, Any], field: str, *, context: str) -> str:
    result = value.get(field)
    if not isinstance(result, str) or not result:
        raise RuntimeDependencyError(f"{context} {field} is missing")
    return result


def _required_index(value: Mapping[str, Any], field: str) -> int:
    result = value.get(field)
    if not isinstance(result, int):
        raise RuntimeDependencyError(f"runtime dependency {field} is missing")
    return result


def _observation_members(
    observation: Mapping[str, Any],
    entries_by_index: Mapping[int, Mapping[str, Any]],
) -> tuple[str, int, int, Mapping[str, Any], Mapping[str, Any], list[str], str]:
    observation_id = _required_text(
        observation, "observation_id", context="runtime dependency"
    )
    consumer_index = _required_index(observation, "consumer_index")
    provider_index = _required_index(observation, "provider_index")
    if provider_index <= consumer_index:
        raise RuntimeDependencyError(
            f"runtime provider must follow consumer: {observation_id}"
        )
    consumer = entries_by_index.get(consumer_index)
    provider = entries_by_index.get(provider_index)
    if consumer is None or provider is None:
        raise RuntimeDependencyError(
            f"runtime dependency transition is missing: {observation_id}"
        )
    if observation.get("consumer_entry_id") != consumer.get("entry_id"):
        raise RuntimeDependencyError(
            f"runtime consumer identity drift: {observation_id}"
        )
    if observation.get("provider_entry_id") != provider.get("entry_id"):
        raise RuntimeDependencyError(
            f"runtime provider identity drift: {observation_id}"
        )

    consumer_paths = observation.get("consumer_paths")
    if not isinstance(consumer_paths, Sequence) or isinstance(consumer_paths, str):
        raise RuntimeDependencyError(
            f"runtime consumer paths are missing: {observation_id}"
        )
    consumer_paths = sorted({str(path) for path in consumer_paths if path})
    if not consumer_paths or not set(consumer_paths).issubset(
        set(consumer.get("expected_v1_changed_paths", ()))
    ):
        raise RuntimeDependencyError(
            f"runtime consumer path drift: {observation_id}"
        )

    proof_sha256 = _required_text(
        observation, "failure_proof_sha256", context="runtime dependency"
    )
    if _SHA256.fullmatch(proof_sha256) is None:
        raise RuntimeDependencyError(
            f"runtime failure proof hash is invalid: {observation_id}"
        )
    return (
        observation_id,
        consumer_index,
        provider_index,
        consumer,
        provider,
        consumer_paths,
        proof_sha256,
    )


def _capability_payload(
    observation_id: str,
    capability: Mapping[str, Any],
    consumer: Mapping[str, Any],
    provider: Mapping[str, Any],
    *,
    is_ancestor: Callable[[str, str], bool],
    read_blob: Callable[[str, str], str],
) -> dict[str, Any]:
    if not isinstance(capability, Mapping):
        raise RuntimeDependencyError(
            f"runtime capability is missing: {observation_id}"
        )
    required_gitlink = _required_text(
        capability, "gitlink_after", context="runtime capability"
    )
    introduced_by = _required_text(
        capability, "introduced_by", context="runtime capability"
    )
    path = _required_text(capability, "path", context="runtime capability")
    needle = _required_text(capability, "needle", context="runtime capability")
    consumer_gitlink = _required_text(
        consumer, "gitlink_after", context="runtime consumer"
    )
    if provider.get("gitlink_after") != required_gitlink:
        raise RuntimeDependencyError(
            f"runtime provider gitlink drift: {observation_id}"
        )
    if not is_ancestor(consumer_gitlink, required_gitlink):
        raise RuntimeDependencyError(
            f"runtime provider is not a consumer descendant: {observation_id}"
        )
    if not is_ancestor(introduced_by, required_gitlink):
        raise RuntimeDependencyError(
            f"runtime capability introduction is outside provider: {observation_id}"
        )
    if needle not in read_blob(required_gitlink, path):
        raise RuntimeDependencyError(
            f"runtime capability content is missing: {observation_id}"
        )

    return {
        "consumer_gitlink": consumer_gitlink,
        "gitlink_before": provider.get("gitlink_before"),
        "gitlink_after": required_gitlink,
        "introduced_by": introduced_by,
        "label": _required_text(
            capability, "label", context="runtime capability"
        ),
        "path": path,
        "needle": needle,
    }


def _validate_observation(
    observation: Mapping[str, Any],
    *,
    entries_by_index: Mapping[int, Mapping[str, Any]],
    ordinary_indexes: Collection[int],
    is_ancestor: Callable[[str, str], bool],
    read_blob: Callable[[str, str], str],
) -> dict[str, Any]:
    (
        observation_id,
        consumer_index,
        provider_index,
        consumer,
        provider,
        consumer_paths,
        proof_sha256,
    ) = _observation_members(observation, entries_by_index)
    capability = observation.get("capability")
    if not isinstance(capability, Mapping):
        raise RuntimeDependencyError(
            f"runtime capability is missing: {observation_id}"
        )
    capability_payload = _capability_payload(
        observation_id,
        capability,
        consumer,
        provider,
        is_ancestor=is_ancestor,
        read_blob=read_blob,
    )
    members = [consumer_index, provider_index]
    return {
        "kind": RUNTIME_WAYLIB_EDGE_KIND,
        "observation_id": observation_id,
        "owner_index": provider_index,
        "required_owner_index": consumer_index,
        "observed_member_indices": members,
        "first_member_index": consumer_index,
        "last_member_index": provider_index,
        "early_member_indices": [],
        "affected_ordinary_indices": sorted(
            set(members) & set(ordinary_indexes)
        ),
        "roles": {
            str(consumer_index): ["runtime-test-consumer"],
            str(provider_index): ["waylib-provider"],
        },
        "consumer_paths": consumer_paths,
        "test_name": _required_text(
            observation, "test_name", context="runtime dependency"
        ),
        "failure_proof_sha256": proof_sha256,
        **capability_payload,
    }


def build_runtime_dependency_edges(
    transitions: Sequence[Mapping[str, Any]],
    observations: Sequence[Mapping[str, Any]],
    *,
    ordinary_indexes: Collection[int],
    is_ancestor: Callable[[str, str], bool],
    read_blob: Callable[[str, str], str],
) -> list[dict[str, Any]]:
    """Convert validated failure observations into deterministic dependency edges."""

    entries_by_index = {
        int(entry["ordered_index"]): entry for entry in transitions
    }
    if len(entries_by_index) != len(transitions):
        raise RuntimeDependencyError("duplicate transition index")
    edges = [
        _validate_observation(
            observation,
            entries_by_index=entries_by_index,
            ordinary_indexes=ordinary_indexes,
            is_ancestor=is_ancestor,
            read_blob=read_blob,
        )
        for observation in observations
    ]
    identities = [edge["observation_id"] for edge in edges]
    if len(identities) != len(set(identities)):
        raise RuntimeDependencyError("duplicate runtime dependency observation")
    return sorted(edges, key=lambda edge: edge["observation_id"])
