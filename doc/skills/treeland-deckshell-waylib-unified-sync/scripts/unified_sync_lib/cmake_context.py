"""Conservatively record public CMake execution context without executing source code."""

from __future__ import annotations

import json
import re
from pathlib import PurePosixPath

from .cmake_syntax import cmake_call_body, cmake_statements, is_cmake_source


SCOPES = {"if", "foreach", "while", "function", "macro", "block"}
BOUNDARIES = {"include", "add_subdirectory", "return", "break", "continue", "cmake_language"}
PUBLIC_CALLS = {"install", "export", "configure_package_config_file", "write_basic_package_version_file"}
TEST_PARTS = {"test", "tests", "example", "examples"}


def _anchor(name, call, helpers, variables):
    body = cmake_call_body(call)
    tokens = body.split()
    if name in {"set", "option", "unset"}:
        return call if tokens and tokens[0].strip('"') in variables else None
    if name in {"add_library", "add_executable"}:
        target = tokens[0] if tokens else ""
        return None if target.lower().startswith(("test_", "tst_", "example_")) else f"{name}({target})"
    if name == "target_include_directories":
        return call if re.search(r"\b(PUBLIC|INTERFACE)\b", body, re.IGNORECASE) else None
    if name in {"set_property", "set_target_properties"}:
        return name if re.search(r"\b(EXPORT_NAME|OUTPUT_NAME|PUBLIC_HEADER)\b", body, re.IGNORECASE) else None
    if name == "add_subdirectory" and tokens and TEST_PARTS.intersection(PurePosixPath(tokens[0].strip('"')).parts):
        return None
    return call if name in PUBLIC_CALLS | BOUNDARIES | helpers else None


def _file_context(path, statements, helpers, variables):
    scopes, result = [], []
    for name, call in statements:
        if name in SCOPES:
            scopes.append([name, [call]])
        elif name.startswith("end") and name[3:] in SCOPES:
            if not scopes or scopes[-1][0] != name[3:]:
                raise ValueError("unbalanced CMake scope in " + path)
            scopes.pop()
        elif name in {"else", "elseif"}:
            if not scopes or scopes[-1][0] != "if":
                raise ValueError("unbalanced CMake conditional in " + path)
            scopes[-1][1].append(call)
        else:
            anchor = _anchor(name, call, helpers, variables)
            if anchor is not None:
                context = [value for _, branches in scopes for value in branches]
                result.append(json.dumps([path, context, anchor], ensure_ascii=True, separators=(",", ":")))
    if scopes:
        raise ValueError("unclosed CMake scope in " + path)
    return result


def cmake_execution_context(contents, variables=()):
    """Record scopes, entry points, and order while excluding known private-only calls."""

    programs = {path: cmake_statements(content) for path, content in sorted(contents.items())
                if is_cmake_source(path)
                and not TEST_PARTS.intersection(PurePosixPath(path).parts)}
    helpers = {cmake_call_body(call).split()[0].lower()
               for statements in programs.values() for name, call in statements
               if name in {"function", "macro"} and cmake_call_body(call).split()}
    return [record for path, statements in programs.items() for record in _file_context(path, statements, helpers, variables)]


def wrapper_entry_context(contents):
    """Allow only the exact new root entry; existing contexts cannot be relaxed."""

    entry = cmake_execution_context({"CMakeLists.txt": "add_subdirectory(wlroots)\n"})
    return [value for value in entry if value in cmake_execution_context(contents)]
