"""Recognize conservative C++ symbol definitions and complete uses."""

from __future__ import annotations

import re


_CLASS_DEFINITION = re.compile(
    r"^\s*class\s+(?:[A-Za-z_]\w*::)*([A-Za-z_]\w*)\b(?![^;]*;)"
)
_NEW_EXPRESSION = re.compile(r"\bnew\s+([A-Za-z_]\w*)\b")
_METHOD_DEFINITION = re.compile(
    r"\b(?:[A-Za-z_]\w*::)+([A-Za-z_]\w*)\s*\("
)
_METHOD_DECLARATION = re.compile(
    r"^\s*(?!Q_EMIT\b)(?:virtual\s+)?"
    r"(?:[A-Za-z_]\w*(?:::[A-Za-z_]\w*)?\s+)+"
    r"(?:[*&]\s*)?([A-Za-z_]\w*)\s*\([^;{}]*\)\s*"
    r"(?:const\s*)?(?:override\s*)?;"
)
_METHOD_CALL = re.compile(r"(?:->|\.)\s*([A-Za-z_]\w*)\s*\(")
_QT_SIGNAL_EMIT = re.compile(r"\bQ_EMIT\s+([A-Za-z_]\w*)\s*\(")
_LOGGING_DEFINITION = re.compile(
    r"\bQ_(?:DECLARE_)?LOGGING_CATEGORY\(\s*([A-Za-z_]\w*)"
)
_LOGGING_USE = re.compile(
    r"\bqC(?:Debug|Info|Warning|Critical)\(\s*([A-Za-z_]\w*)"
)
_MEMBER_DECLARATION = re.compile(
    r"^\s*(?:[A-Za-z_]\w*(?:::[A-Za-z_]\w*)?(?:\s*<[^;{}]+>)?\s+)+"
    r"(?:[*&]\s*)?(m_[A-Za-z_]\w*)\s*(?:=[^;]*)?;"
)
_MEMBER_USE = re.compile(r"\b(m_[A-Za-z_]\w*)\b")

SOURCE_SUFFIXES = {".c", ".cc", ".cpp", ".cxx", ".m", ".mm", ".qml"}
HEADER_SUFFIXES = {".h", ".hh", ".hpp", ".hxx"}
SYMBOL_SUFFIXES = SOURCE_SUFFIXES - {".qml"} | HEADER_SUFFIXES


def definition_matches(
    line: str, *, path: str | None = None
) -> list[tuple[str, str]]:
    """Return every supported symbol definition on one added line."""

    matches = []
    for kind, pattern in (
        ("class", _CLASS_DEFINITION),
        ("method", _METHOD_DEFINITION),
        ("method", _METHOD_DECLARATION),
        ("logging-category", _LOGGING_DEFINITION),
    ):
        match = pattern.search(line)
        if match:
            matches.append((match.group(1), kind))
    if path is not None and any(path.endswith(suffix) for suffix in HEADER_SUFFIXES):
        match = _MEMBER_DECLARATION.search(line)
        if match:
            matches.append((match.group(1), "member"))
    return matches


def definitions(line: str, *, path: str | None = None) -> set[str]:
    """Return supported symbols defined on one added or removed line."""

    return {symbol for symbol, _kind in definition_matches(line, path=path)}


def complete_uses(line: str) -> set[str]:
    """Return uses whose spelling alone is sufficient for a conservative edge."""

    uses = {
        match.group(1)
        for pattern in (_NEW_EXPRESSION, _LOGGING_USE)
        for match in pattern.finditer(line)
    }
    # Snake-case receiver calls are generated Wayland APIs; without receiver
    # type resolution, joining them to handwritten definitions creates false edges.
    uses.update(
        match.group(1)
        for match in _METHOD_CALL.finditer(line)
        if "_" not in match.group(1)
    )
    uses.update(match.group(1) for match in _MEMBER_USE.finditer(line))
    return uses


def qt_signal_emits(line: str) -> set[str]:
    """Return Qt signals emitted without an explicit receiver."""

    return {match.group(1) for match in _QT_SIGNAL_EMIT.finditer(line)}
