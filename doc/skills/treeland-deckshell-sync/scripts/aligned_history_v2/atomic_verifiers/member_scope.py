"""Conservative scope matching for private C++ member observations."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import PurePosixPath


def _source_stems(paths: Sequence[str]) -> set[str]:
    return {
        PurePosixPath(path).stem.removesuffix("_p")
        for path in paths
    }


def member_use_matches_definition_scope(
    member_paths: Mapping[int, set[str]],
    *,
    provider_index: int,
    first_use_index: int,
) -> bool:
    """Return whether a private member use belongs to the provider file family."""

    return symbol_use_matches_definition_scope(
        member_paths,
        provider_index=provider_index,
        first_use_index=first_use_index,
    )


def symbol_use_matches_definition_scope(
    member_paths: Mapping[int, set[str]],
    *,
    provider_index: int,
    first_use_index: int,
) -> bool:
    """Return whether a symbol use belongs to the provider file family."""

    provider_stems = _source_stems(sorted(member_paths[provider_index]))
    consumer_stems = _source_stems(sorted(member_paths[first_use_index]))
    return bool(provider_stems & consumer_stems)
