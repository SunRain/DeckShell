"""Small CMake call parser shared by source and installed-contract scans."""

from __future__ import annotations

import re
from pathlib import PurePosixPath
from typing import List


def is_cmake_source(path: str) -> bool:
    """Select CMake scripts and package templates, excluding C++ and JSON snapshots."""

    return PurePosixPath(path).name == "CMakeLists.txt" or path.endswith((".cmake", ".cmake.in", "Config.in"))


def _literal_end(content: str, index: int):
    bracket = re.match(r"\[(=*)\[", content[index:]) if content[index] == "[" else None
    if bracket:
        closing = "]" + bracket.group(1) + "]"
        end = content.find(closing, index + bracket.end())
        if end < 0:
            raise ValueError("unterminated CMake bracket argument/comment")
        return end + len(closing)
    if content[index] == '"':
        index += 1
        while index < len(content):
            if content[index] == '"':
                return index + 1
            index += 2 if content[index] == "\\" else 1
        raise ValueError("unterminated CMake quoted argument")
    return None


def _call_end(content: str, start: int) -> int:
    """Return the closing-parenthesis offset for a CMake call body."""

    depth = 1
    index = start
    while index < len(content):
        char = content[index]
        end = _literal_end(content, index)
        if end is not None:
            index = end
            continue
        if char == "\\":
            index += 2
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return len(content)


def cmake_calls(content: str, command: str) -> List[str]:
    """Return normalized complete calls for one CMake command name."""

    return [call for name, call in cmake_statements(content) if name == command.lower()]


def cmake_statements(content: str):
    """Read ordered complete statements, excluding command text inside arguments."""

    pattern = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(")
    masked = _mask_comments(content)
    index = 0
    result = []
    while True:
        match = pattern.search(masked, index)
        if match is None:
            return result
        body_start = match.end()
        body_end = _call_end(masked, body_start)
        if body_end == len(masked):
            raise ValueError("unterminated CMake statement: " + match.group(1))
        body = " ".join(masked[body_start:body_end].split())
        name = match.group(1).lower()
        result.append((name, f"{name}({body})"))
        index = body_end + 1


def _mask_comments(content: str) -> str:
    """Mask comments while preserving offsets used to extract call bodies."""

    chars = list(content)
    index = 0
    while index < len(content):
        char = content[index]
        end = _literal_end(content, index)
        if end is not None:
            index = end
            continue
        if char == "#":
            end = _literal_end(content, index + 1) if index + 1 < len(content) and content[index + 1] == "[" else None
            if end is None:
                end = content.find("\n", index)
                end = len(content) if end < 0 else end
            chars[index:end] = ["\n" if value == "\n" else " " for value in content[index:end]]
            index = end
        else:
            index += 2 if char == "\\" else 1
    return "".join(chars)


def cmake_call_body(call: str) -> str:
    """Return a normalized call body previously returned by ``cmake_calls``."""

    return call.split("(", 1)[1].rsplit(")", 1)[0]
