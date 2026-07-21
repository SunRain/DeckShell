"""Compile-atomic dependency bundle validation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


class DependencyBundleError(ValueError):
    """Raised when dependency members do not share one transition owner."""


def validate_atomic_bundle(
    owner_index: int,
    members: Sequence[Mapping[str, Any]],
) -> None:
    """Require every declared bundle member to exist at its owning node."""

    misplaced = [
        member
        for member in members
        if member.get("owner_index") != owner_index
    ]
    if misplaced:
        details = ", ".join(
            f"{member.get('kind')}@{member.get('owner_index')}"
            for member in misplaced
        )
        raise DependencyBundleError(
            f"cross-owner dependency bundle for {owner_index}: {details}"
        )
