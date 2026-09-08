"""Semantic scan of Waylib CMake and package template sources."""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, Sequence

from .cmake_syntax import cmake_call_body, cmake_calls, is_cmake_source
from .cmake_context import cmake_execution_context, wrapper_entry_context
from .git_ops import resolve_commit, run_git, sha256_bytes, sha256_file
from .namespace_contract import HEADERS, namespace_contract


EXCLUDED_DIR_PREFIXES = ("build", "cmake-build")
PROTECTED_TARGET_PROPERTIES = {"EXPORT_NAME", "OUTPUT_NAME", "PUBLIC_HEADER"}


def _is_contract_file(relative: PurePosixPath) -> bool:
    name = relative.name
    if relative.parts[:2] == ("3rdparty", "wlroots"):
        return False
    return (
        name == "CMakeLists.txt"
        or name == "CMakePresets.json"
        or name.endswith(".cmake")
        or name.endswith(".cmake.in")
        or name.endswith("Config.in")
        or name.endswith(".pc.in")
        or (relative.suffix in HEADERS and not name.endswith("_p.h")
            and not {"private", "tests", "test", "examples", "example"}.intersection(relative.parts))
    )


def _contract_files(root: Path) -> List[Path]:
    result: List[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(root)
        if any(
            part == ".git" or part.startswith(EXCLUDED_DIR_PREFIXES)
            for part in relative.parts[:-1]
        ):
            continue
        if _is_contract_file(relative):
            result.append(path)
    return sorted(result, key=lambda path: path.relative_to(root).as_posix())


def _target_name(call: str) -> str:
    body = cmake_call_body(call)
    return body.split()[0] if body.split() else ""


def _is_test_target(relative: Path, target: str) -> bool:
    lowered_parts = {part.lower() for part in relative.parts}
    lowered = target.lower()
    return bool({"test", "tests", "example", "examples"} & lowered_parts) or lowered.startswith(
        ("test_", "tst_", "example_")
    )


def _namespace_tokens(calls: Sequence[str]) -> List[str]:
    result: List[str] = []
    for call in calls:
        result.extend(
            match.group(1)
            for match in re.finditer(
                r"\bNAMESPACE\s+([A-Za-z0-9_.:+-]+)", call, re.IGNORECASE
            )
        )
    return result


def _target_property_tokens(calls: Sequence[str]) -> List[str]:
    result: List[str] = []
    for call in calls:
        body = cmake_call_body(call)
        match = re.search(r"\bPROPERTIES\b(.*)$", body, re.IGNORECASE)
        if not match:
            continue
        targets = body[: match.start()].split()
        values = match.group(1).split()
        for index in range(0, len(values) - 1, 2):
            name = values[index].upper()
            if name in PROTECTED_TARGET_PROPERTIES:
                result.append(f"{' '.join(targets)}:{name}={values[index + 1]}")
    return result


def _set_property_tokens(calls: Sequence[str]) -> List[str]:
    result: List[str] = []
    pattern = re.compile(
        r"^TARGET\s+(.*?)\s+(?:APPEND(?:_STRING)?\s+)?PROPERTY\s+"
        r"(EXPORT_NAME|OUTPUT_NAME|PUBLIC_HEADER)\s+(.*)$",
        re.IGNORECASE,
    )
    for call in calls:
        match = pattern.match(cmake_call_body(call))
        if match:
            result.append(
                f"{match.group(1)}:{match.group(2).upper()}={match.group(3)}"
            )
    return result


def _contract_variable_definitions(
    contents: Dict[str, str], expressions: Sequence[str], contexts: Sequence[str]
):
    """保留受保护表达式引用的 set/option 定义及其传递依赖。"""

    reference = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
    variables = set(reference.findall("\n".join(expressions)))
    variables.update(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", "\n".join(contexts)))
    definitions = []
    for path, content in sorted(contents.items()):
        if not is_cmake_source(path):
            continue
        for command in ("set", "option", "unset"):
            for call in cmake_calls(content, command):
                tokens = cmake_call_body(call).split()
                if tokens:
                    definitions.append((path, tokens[0].strip('"'), call))
    while True:
        dependencies = {
            name for _path, variable, call in definitions if variable in variables
            for name in reference.findall(call)
        }
        if dependencies.issubset(variables):
            break
        variables.update(dependencies)
    return variables, [
        f"{path}:{call}" for path, variable, call in definitions
        if variable in variables
    ]


def _execution_semantics(contents, expressions):
    contexts = cmake_execution_context(contents)
    while True:
        variables, definitions = _contract_variable_definitions(contents, expressions, contexts)
        expanded = cmake_execution_context(contents, variables)
        if expanded == contexts:
            return {"cmake_execution_context": contexts, "contract_variable_definitions": definitions}
        contexts = expanded


def _wrapper_snapshot(contents, digests):
    selected = {path: value for path, value in contents.items() if path.startswith("wlroots/")}
    if not selected or len(selected) == len(contents):
        return None
    result = _source_contract_snapshot(selected, {path: digests[path] for path in selected})
    result["cmake_execution_context"].extend(wrapper_entry_context(contents))
    return result


def _cmake_source_semantics(contents):
    targets: List[str] = []
    installs: List[str] = []
    packages: List[str] = []
    public_includes: List[str] = []
    export_calls: List[str] = []
    target_properties: List[str] = []
    for relative_text in sorted(contents):
        relative = PurePosixPath(relative_text)
        content = contents[relative_text]
        if not is_cmake_source(relative_text):
            continue
        target_calls = cmake_calls(content, "add_library") + cmake_calls(content, "add_executable")
        targets.extend(
            target
            for target in (_target_name(call) for call in target_calls)
            if target and not _is_test_target(relative, target)
        )
        installs.extend(cmake_calls(content, "install"))
        export_calls.extend(cmake_calls(content, "install") + cmake_calls(content, "export"))
        packages.extend(cmake_calls(content, "configure_package_config_file"))
        packages.extend(cmake_calls(content, "write_basic_package_version_file"))
        public_includes.extend(
            call
            for call in cmake_calls(content, "target_include_directories")
            if re.search(r"\b(?:PUBLIC|INTERFACE)\b", call, re.IGNORECASE)
        )
        target_properties.extend(
            _target_property_tokens(cmake_calls(content, "set_target_properties"))
        )
        target_properties.extend(_set_property_tokens(cmake_calls(content, "set_property")))
    return {
        "core_targets": sorted(set(targets)),
        "install_directives": sorted(set(installs)),
        "package_directives": sorted(set(packages)),
        "public_include_directives": sorted(set(public_includes)),
        "export_namespaces": sorted(set(_namespace_tokens(export_calls))),
        "target_contract_properties": sorted(set(target_properties)),
        **_execution_semantics(contents, targets + installs + packages + public_includes + export_calls + target_properties),
    }


def _source_contract_snapshot(contents: Dict[str, str], digests: Dict[str, str]) -> Dict[str, Any]:
    """Build protected CMake and namespace semantics from frozen source files."""

    namespace_data = namespace_contract({path: content for path, content in contents.items() if PurePosixPath(path).suffix in HEADERS})
    return {
        "contract_files": sorted(contents),
        "contract_file_sha256": dict(sorted(digests.items())),
        **_cmake_source_semantics(contents),
        "cmake_presets": sorted(
            f"{path}:{digests[path]}"
            for path in sorted(contents)
            if PurePosixPath(path).name == "CMakePresets.json"
        ),
        "public_namespaces": namespace_data["namespaces"],
        "namespace_macro_definitions": namespace_data["macro_definitions"],
        "namespace_errors": namespace_data["errors"],
        "wrapper_contract": _wrapper_snapshot(contents, digests),
    }


def build_source_contract_snapshot(source_root: Path) -> Dict[str, Any]:
    """Scan all maintained CMake/config templates for protected semantics."""

    root = source_root.resolve()
    if not root.is_dir():
        raise ValueError(f"source root is not a directory: {root}")
    files = _contract_files(root)
    contents = {
        path.relative_to(root).as_posix(): path.read_text(
            encoding="utf-8", errors="replace"
        )
        for path in files
    }
    digests = {
        path.relative_to(root).as_posix(): sha256_file(path) for path in files
    }
    return _source_contract_snapshot(contents, digests)


def build_source_contract_snapshot_at(repo: Path, commit: str) -> Dict[str, Any]:
    """Scan protected CMake semantics directly from one immutable Git tree."""

    sha = resolve_commit(repo, commit)
    raw = run_git(repo, "ls-tree", "-r", "-z", sha, text=False)
    contents: Dict[str, str] = {}
    digests: Dict[str, str] = {}
    for record in bytes(raw).split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, object_type, object_sha = metadata.split()
        if mode == b"120000" or object_type != b"blob":
            continue
        path = raw_path.decode("utf-8", errors="surrogateescape")
        if not _is_contract_file(PurePosixPath(path)):
            continue
        content = bytes(run_git(repo, "cat-file", "blob", object_sha.decode("ascii"), text=False))
        contents[path] = content.decode("utf-8", errors="replace")
        digests[path] = sha256_bytes(content)
    return _source_contract_snapshot(contents, digests)
