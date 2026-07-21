"""Canonicalize historical CMake consumers to the DeckShell build contract."""

from __future__ import annotations

import re
from collections.abc import Iterable


CONTRACT_RULES = (
    ("legacy-protocol-variable", re.compile(r"\bTREELAND_PROTOCOLS_DATA_DIR\b")),
    (
        "legacy-target",
        re.compile(
            r"\blocal_qtwayland_server_protocol_treeland\s*\(\s*libtreeland\b"
        ),
    ),
    ("legacy-module-helper", re.compile(r"\bimpl_treeland\s*\(")),
    (
        "legacy-generated-path",
        re.compile(r"\$\{CMAKE_BINARY_DIR\}/src/modules/"),
    ),
    (
        "legacy-protocol-version",
        re.compile(r"\b(?:TreelandProtocols_VERSION|TREELAND_PROTOCOLS_VERSION)\b"),
    ),
)
_TREELAND_PACKAGE = re.compile(
    r"\bfind_package\s*\(\s*TreelandProtocols\b"
)
_DECK_PACKAGE = re.compile(
    r"\bfind_package\s*\(\s*DeckCompositorProtocols\b"
)
_TREELAND_PACKAGE_LINE = re.compile(
    r"^\s*find_package\s*\(\s*TreelandProtocols\b[^)]*\)\s*(?:#.*)?$"
)
_DECK_PACKAGE_LINE = re.compile(
    r"^\s*find_package\s*\(\s*DeckCompositorProtocols\b[^)]*\)"
    r"\s*(?:#.*)?$"
)
_PROTOCOL_GUARD_LINE = re.compile(
    r"^\s*if\s*\(\s*NOT\s+(?:DEFINED\s+)?"
    r"(?:TREELAND_PROTOCOLS_DATA_DIR|DECKCOMPOSITOR_PROTOCOLS_DATA_DIR)"
    r"\s*\)\s*(?:#.*)?$"
)
_ENDIF_LINE = re.compile(r"^\s*endif\s*\(\s*\)\s*(?:#.*)?$")
_LEGACY_TARGET = re.compile(
    r"(\blocal_qtwayland_server_protocol_treeland\s*\(\s*)libtreeland\b"
)
_LEGACY_HELPER = re.compile(r"\bimpl_treeland\s*\(")
_LEGACY_GENERATED_PATH = re.compile(
    r"\$\{CMAKE_BINARY_DIR\}/src/modules/[^/\s)]+/"
)
_LEGACY_VERSION_VARIABLE = re.compile(
    r"\b(?:TreelandProtocols_VERSION|TREELAND_PROTOCOLS_VERSION)\b"
)
_DECK_VERSION_LINE = re.compile(
    r"^\s*set\s*\(\s*DeckCompositorProtocols_VERSION\s+"
    r"(?P<value>[^)]*?)\s*\)\s*(?:#.*)?$",
    re.IGNORECASE,
)
def is_cmake_path(path: str) -> bool:
    """Return whether a repository path is an executable CMake input."""

    return path.endswith(("CMakeLists.txt", ".cmake", ".cmake.in"))


def is_negative_policy_fixture(path: str) -> bool:
    """Return whether CMake text is data for the protocol-policy regression test."""

    return "/test_protocol_source_policy/" in f"/{path}"


def _is_standalone_project_entry(path: str) -> bool:
    return path.endswith("CMakeLists.txt") and path.count("/") <= 1


def detect_contract_roles(lines: Iterable[str], *, path: str = "") -> list[str]:
    """Classify legacy build-contract expressions in CMake source lines."""

    materialized = tuple(lines)
    roles = {
        role
        for role, pattern in CONTRACT_RULES
        if any(pattern.search(line) for line in materialized)
    }
    has_external_lookup = any(
        _TREELAND_PACKAGE.search(line) for line in materialized
    )
    has_nested_deck_lookup = (
        not _is_standalone_project_entry(path)
        and any(_DECK_PACKAGE.search(line) for line in materialized)
    )
    if has_external_lookup or has_nested_deck_lookup:
        roles.add("external-protocol-package")
    return sorted(roles)


def _without_external_package_lookup(
    lines: list[str], *, remove_deck_package: bool
) -> list[str]:
    def removable_package(line: str) -> bool:
        return bool(
            _TREELAND_PACKAGE_LINE.match(line)
            or (remove_deck_package and _DECK_PACKAGE_LINE.match(line))
        )

    filtered: list[str] = []
    index = 0
    while index < len(lines):
        current = lines[index].rstrip("\r\n")
        if _PROTOCOL_GUARD_LINE.match(current):
            package_index = index + 1
            while package_index < len(lines) and not lines[package_index].strip():
                package_index += 1
            end_index = package_index + 1
            while end_index < len(lines) and not lines[end_index].strip():
                end_index += 1
            if (
                package_index < len(lines)
                and removable_package(lines[package_index].rstrip("\r\n"))
                and end_index < len(lines)
                and _ENDIF_LINE.match(lines[end_index].rstrip("\r\n"))
            ):
                index = end_index + 1
                if index < len(lines) and not lines[index].strip():
                    index += 1
                continue
        if removable_package(current):
            index += 1
            if index < len(lines) and not lines[index].strip():
                index += 1
            continue
        filtered.append(lines[index])
        index += 1
    return filtered


def _without_duplicate_protocol_versions(lines: list[str]) -> list[str]:
    filtered: list[str] = []
    for line in lines:
        current = _DECK_VERSION_LINE.match(line.rstrip("\r\n"))
        previous = (
            _DECK_VERSION_LINE.match(filtered[-1].rstrip("\r\n"))
            if filtered
            else None
        )
        if current is not None and previous is not None:
            if current.group("value") != previous.group("value"):
                raise RuntimeError("conflicting DeckCompositorProtocols version aliases")
            continue
        filtered.append(line)
    return filtered


def normalize_cmake_payload(path: str, payload: bytes) -> tuple[bytes, list[str]]:
    """Normalize one historical CMake post-image without using a commit special case."""

    if not is_cmake_path(path) or is_negative_policy_fixture(path):
        return payload, []
    text = payload.decode("utf-8", errors="strict")
    roles = detect_contract_roles(text.splitlines(), path=path)
    filtered = _without_external_package_lookup(
        text.splitlines(keepends=True),
        remove_deck_package=not _is_standalone_project_entry(path),
    )
    normalized = "".join(filtered).replace(
        "TREELAND_PROTOCOLS_DATA_DIR", "DECKCOMPOSITOR_PROTOCOLS_DATA_DIR"
    )
    normalized = _LEGACY_TARGET.sub(r"\1libdeckcompositor", normalized)
    normalized = _LEGACY_HELPER.sub("impl_deckcompositor(", normalized)
    normalized = _LEGACY_GENERATED_PATH.sub(
        "${CMAKE_CURRENT_BINARY_DIR}/", normalized
    )
    normalized = _LEGACY_VERSION_VARIABLE.sub(
        "DeckCompositorProtocols_VERSION", normalized
    )
    normalized = "".join(
        _without_duplicate_protocol_versions(normalized.splitlines(keepends=True))
    )
    return normalized.encode("utf-8"), roles
