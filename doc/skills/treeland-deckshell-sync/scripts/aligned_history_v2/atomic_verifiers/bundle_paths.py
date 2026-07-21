"""Collect the source paths owned by dependency bundle components."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


def bundle_paths(components: Sequence[Mapping[str, Any]]) -> list[str]:
    """Return the deterministic path union represented by components."""

    paths = set()
    for component in components:
        payload = component["payload"]
        paths.update(
            payload[key]
            for key in ("path", "source_path", "target_path")
            if payload.get(key)
        )
        paths.update(payload.get("synthesized_paths", ()))
        definition_lines = payload.get("definition_lines", {})
        if definition_lines:
            for lines_by_path in definition_lines.values():
                paths.update(lines_by_path)
        elif payload.get("member_paths"):
            provider = str(payload.get("owner_index"))
            paths.update(payload["member_paths"].get(provider, ()))
    return sorted(paths)
