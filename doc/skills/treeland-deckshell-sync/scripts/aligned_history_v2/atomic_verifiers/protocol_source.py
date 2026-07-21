"""Validate that protocol generation only consumes repository-owned XML."""

from __future__ import annotations

import re
from collections.abc import Collection, Mapping


class ProtocolSourceError(ValueError):
    """Raised when a history node violates the protocol source contract."""


_FORBIDDEN = (
    re.compile(r"\bfind_package\s*\(\s*TreelandProtocols\b"),
    re.compile(r"(?<!DECKCOMPOSITOR_)\bTREELAND_PROTOCOLS_DATA_DIR\b"),
)


def _active_lines(content: str) -> str:
    return "\n".join(line.split("#", 1)[0] for line in content.splitlines())


def validate_protocol_source(files: Mapping[str, str]) -> None:
    """Reject active CMake expressions that resolve mutable external XML."""

    violations = []
    for path, content in sorted(files.items()):
        active = _active_lines(content)
        for pattern in _FORBIDDEN:
            if pattern.search(active):
                violations.append(path)
                break
    if violations:
        joined = ", ".join(violations)
        raise ProtocolSourceError(f"external protocol lookup: {joined}")


def validate_protocol_alignment(
    generated: Mapping[str, Collection[str]],
    consumed: Mapping[str, Collection[str]],
) -> None:
    """Require every consumed generated signature at the same history node."""

    mismatches = []
    for protocol, required in sorted(consumed.items()):
        available = set(generated.get(protocol, ()))
        missing = sorted(set(required) - available)
        if missing:
            mismatches.append(f"{protocol}: {', '.join(missing)}")
    if mismatches:
        raise ProtocolSourceError(
            "generated signature mismatch: " + "; ".join(mismatches)
        )
