"""Project frozen master CMake blobs through compile-atomic authority."""

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
_TREELAND_PACKAGE = re.compile(r"\bfind_package\s*\(\s*TreelandProtocols\b")
_DECK_PACKAGE = re.compile(r"\bfind_package\s*\(\s*DeckCompositorProtocols\b")
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
_ROOT_COMPILE_MARKER = "set(CMAKE_CXX_EXTENSIONS OFF)\n"
_ROOT_COMPILE_COMPATIBILITY = """

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    add_compile_options(
        "$<$<COMPILE_LANGUAGE:CXX>:SHELL:-include unistd.h>"
        "$<$<COMPILE_LANGUAGE:CXX>:SHELL:-include sys/syscall.h>"
    )
endif()
"""
_OUTPUT_CONFIG_MOC_MARKER = "target_compile_definitions(libdeckcompositor\n"
_OUTPUT_CONFIG_MOC_COMPATIBILITY = """set_property(TARGET libdeckcompositor APPEND PROPERTY AUTOMOC_MOC_OPTIONS
    "-b;${CMAKE_CURRENT_BINARY_DIR}/outputconfig.hpp"
)

"""


def project_product_payload(path: str, payload: bytes) -> tuple[bytes, list[str]]:
    """Return the approved product payload and its projection reasons."""

    projected = payload
    reasons: list[str] = []
    if _is_cmake_path(path) and not _is_negative_fixture(path):
        projected, roles = _normalize_cmake_payload(path, projected)
        if projected != payload:
            reasons.extend(roles or ["repository-protocol-source"])
    if path == "CMakeLists.txt":
        updated = _insert_once(
            projected.decode("utf-8"),
            _ROOT_COMPILE_MARKER,
            _ROOT_COMPILE_MARKER + _ROOT_COMPILE_COMPATIBILITY,
            _ROOT_COMPILE_COMPATIBILITY.strip(),
        ).encode("utf-8")
        if updated != projected:
            reasons.append("root-compile-compatibility")
        projected = updated
    if path == "compositor/src/CMakeLists.txt":
        updated = _insert_once(
            projected.decode("utf-8"),
            _OUTPUT_CONFIG_MOC_MARKER,
            _OUTPUT_CONFIG_MOC_COMPATIBILITY + _OUTPUT_CONFIG_MOC_MARKER,
            _OUTPUT_CONFIG_MOC_COMPATIBILITY.strip(),
        ).encode("utf-8")
        if updated != projected:
            reasons.append("output-config-moc-compatibility")
        projected = updated
    return projected, sorted(set(reasons))


def _normalize_cmake_payload(path: str, payload: bytes) -> tuple[bytes, list[str]]:
    text = payload.decode("utf-8")
    lines = text.splitlines(keepends=True)
    roles = _detect_roles(lines, path)
    filtered = _without_external_lookup(
        lines, remove_deck_package=not _is_standalone_project(path)
    )
    normalized = "".join(filtered).replace(
        "TREELAND_PROTOCOLS_DATA_DIR", "DECKCOMPOSITOR_PROTOCOLS_DATA_DIR"
    )
    normalized = _LEGACY_TARGET.sub(r"\1libdeckcompositor", normalized)
    normalized = _LEGACY_HELPER.sub("impl_deckcompositor(", normalized)
    normalized = _LEGACY_GENERATED_PATH.sub("${CMAKE_CURRENT_BINARY_DIR}/", normalized)
    normalized = _LEGACY_VERSION_VARIABLE.sub(
        "DeckCompositorProtocols_VERSION", normalized
    )
    normalized = "".join(
        _without_duplicate_versions(normalized.splitlines(keepends=True))
    )
    return normalized.encode("utf-8"), roles


def _detect_roles(lines: Iterable[str], path: str) -> list[str]:
    materialized = tuple(lines)
    roles = {
        role
        for role, pattern in CONTRACT_RULES
        if any(pattern.search(line) for line in materialized)
    }
    if any(_TREELAND_PACKAGE.search(line) for line in materialized):
        roles.add("external-protocol-package")
    if not _is_standalone_project(path) and any(
        _DECK_PACKAGE.search(line) for line in materialized
    ):
        roles.add("external-protocol-package")
    return sorted(roles)


def _without_external_lookup(
    lines: list[str], *, remove_deck_package: bool
) -> list[str]:
    def removable(line: str) -> bool:
        return bool(
            _TREELAND_PACKAGE_LINE.match(line)
            or (remove_deck_package and _DECK_PACKAGE_LINE.match(line))
        )

    filtered: list[str] = []
    index = 0
    while index < len(lines):
        current = lines[index].rstrip("\r\n")
        if _PROTOCOL_GUARD_LINE.match(current):
            package = index + 1
            while package < len(lines) and not lines[package].strip():
                package += 1
            end = package + 1
            while end < len(lines) and not lines[end].strip():
                end += 1
            if (
                package < len(lines)
                and removable(lines[package].rstrip("\r\n"))
                and end < len(lines)
                and _ENDIF_LINE.match(lines[end].rstrip("\r\n"))
            ):
                index = end + 1
                if index < len(lines) and not lines[index].strip():
                    index += 1
                continue
        if removable(current):
            index += 1
            if index < len(lines) and not lines[index].strip():
                index += 1
            continue
        filtered.append(lines[index])
        index += 1
    return filtered


def _without_duplicate_versions(lines: list[str]) -> list[str]:
    filtered: list[str] = []
    for line in lines:
        current = _DECK_VERSION_LINE.match(line.rstrip("\r\n"))
        previous = _DECK_VERSION_LINE.match(filtered[-1].rstrip("\r\n")) if filtered else None
        if current is not None and previous is not None:
            if current.group("value") != previous.group("value"):
                raise ValueError("conflicting DeckCompositorProtocols version aliases")
            continue
        filtered.append(line)
    return filtered


def _insert_once(text: str, marker: str, replacement: str, present: str) -> str:
    if present in text:
        return text
    if text.count(marker) != 1:
        raise ValueError(f"product projection marker is not unique: {marker!r}")
    return text.replace(marker, replacement, 1)


def _is_cmake_path(path: str) -> bool:
    return path.endswith(("CMakeLists.txt", ".cmake", ".cmake.in"))


def _is_negative_fixture(path: str) -> bool:
    return "/test_protocol_source_policy/" in f"/{path}"


def _is_standalone_project(path: str) -> bool:
    return path.endswith("CMakeLists.txt") and path.count("/") <= 1
