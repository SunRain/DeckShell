"""Derive remediation owner shifts for complete existing-file capabilities."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def promoted_provider_owners(
    dependency_set: Mapping[str, Any],
) -> dict[int, int]:
    """Map an existing-file member provider to its earliest required owner."""

    owners: dict[int, int] = {}
    for edge in dependency_set["graph"]["edges"]:
        if edge.get("kind") != "symbol-cross-entry":
            continue
        provider = int(edge["owner_index"])
        kinds = edge.get("definition_kinds", {}).get(str(provider), ())
        if "member" not in kinds or edge.get("provider_new_file_paths"):
            continue
        required = int(edge.get("required_owner_index", provider))
        owners[provider] = min(required, owners.get(provider, provider))
    return owners


def remediation_target_owners(
    dependency_set: Mapping[str, Any], *, xdg_targets: set[int]
) -> dict[int, int]:
    """Combine the established xdg grouping with generic provider promotion."""

    owners = {target: 133 for target in xdg_targets}
    for provider, required in promoted_provider_owners(dependency_set).items():
        owners[provider] = min(required, owners.get(provider, provider))
    return owners
