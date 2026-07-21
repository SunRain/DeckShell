"""Deterministic static dependency discovery across ordered transitions."""

from __future__ import annotations

import re
import posixpath
from collections import defaultdict
from collections.abc import Callable, Mapping, Sequence
from typing import Any

from .cmake_contract import (
    detect_contract_roles,
    is_cmake_path,
    is_negative_policy_fixture,
)
from .cpp_symbols import (
    SOURCE_SUFFIXES,
    SYMBOL_SUFFIXES,
    complete_uses,
    definition_matches,
    definitions,
    qt_signal_emits,
)
from .member_scope import (
    member_use_matches_definition_scope,
    symbol_use_matches_definition_scope,
)


_DIFF_HEADER = re.compile(r"^diff --git a/(.+) b/(.+)$")


def _patch_sections(patch: str) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for line in patch.splitlines():
        header = _DIFF_HEADER.match(line)
        if header:
            current = {
                "path": header.group(2),
                "new_file": False,
                "added_lines": [],
                "removed_lines": [],
            }
            sections.append(current)
            continue
        if current is None:
            continue
        if line == "new file mode 100644" or line == "--- /dev/null":
            current["new_file"] = True
        elif line.startswith("+") and not line.startswith("+++"):
            current["added_lines"].append(line[1:])
        elif line.startswith("-") and not line.startswith("---"):
            current["removed_lines"].append(line[1:])
    return sections


def _cmake_edges(
    transitions: Sequence[Mapping[str, Any]],
    patch_provider: Callable[[Mapping[str, Any]], str],
) -> list[dict[str, Any]]:
    added_sources: list[tuple[str, int]] = []
    cmake_sections: dict[int, list[tuple[str, list[str]]]] = defaultdict(list)
    for transition in transitions:
        index = transition["ordered_index"]
        for section in _patch_sections(patch_provider(transition)):
            path = section["path"]
            suffix = "." + path.rsplit(".", 1)[-1] if "." in path else ""
            if section["new_file"] and suffix in SOURCE_SUFFIXES:
                added_sources.append((path, index))
            if path.endswith("CMakeLists.txt") or path.endswith(".cmake"):
                cmake_sections[index].append((path, section["added_lines"]))

    edges = []
    for path, source_index in sorted(added_sources):
        basename = path.rsplit("/", 1)[-1]
        source_directory = path.rsplit("/", 1)[0] if "/" in path else ""
        registration_indexes = sorted(
            index
            for index, sections in cmake_sections.items()
            if any(
                any(
                    (
                        cmake_path.rsplit("/", 1)[0]
                        if "/" in cmake_path
                        else ""
                    )
                    == source_directory
                    and basename in line
                    or path in line
                    or posixpath.relpath(
                        path,
                        cmake_path.rsplit("/", 1)[0]
                        if "/" in cmake_path
                        else ".",
                    )
                    in line
                    for line in lines
                )
                for cmake_path, lines in sections
            )
        )
        if not registration_indexes:
            continue
        registration_index = registration_indexes[0]
        if registration_index == source_index:
            continue
        required_owner = max(source_index, registration_index)
        members = sorted({source_index, registration_index})
        roles: dict[str, list[str]] = {
            str(source_index): ["source-file"],
            str(registration_index): ["cmake-registration"],
        }
        edges.append(
            {
                "kind": "cmake-cross-entry",
                "path": path,
                "owner_index": required_owner,
                "required_owner_index": required_owner,
                "observed_member_indices": members,
                "first_member_index": members[0],
                "last_member_index": members[-1],
                "early_member_indices": [
                    index for index in members if index < required_owner
                ],
                "roles": roles,
            }
        )
    return edges


def _cmake_contract_edges(
    transitions: Sequence[Mapping[str, Any]],
    patch_provider: Callable[[Mapping[str, Any]], str],
) -> list[dict[str, Any]]:
    edges = []
    for transition in transitions:
        index = int(transition["ordered_index"])
        for section in _patch_sections(patch_provider(transition)):
            path = section["path"]
            if not is_cmake_path(path) or is_negative_policy_fixture(path):
                continue
            roles = detect_contract_roles(section["added_lines"], path=path)
            if not roles:
                continue
            edges.append(
                {
                    "kind": "cmake-contract",
                    "path": path,
                    "owner_index": index,
                    "required_owner_index": index,
                    "observed_member_indices": [index],
                    "first_member_index": index,
                    "last_member_index": index,
                    "early_member_indices": [],
                    "roles": {str(index): roles},
                }
            )
    return edges


def _new_symbol_observation() -> dict[str, Any]:
    return {
        "roles": defaultdict(set),
        "member_paths": defaultdict(set),
        "definition_kinds": defaultdict(set),
        "definition_lines": defaultdict(lambda: defaultdict(set)),
        "use_lines": defaultdict(lambda: defaultdict(list)),
        "use_kinds": defaultdict(set),
    }


def _symbol_observations(
    transitions: Sequence[Mapping[str, Any]],
    patch_provider: Callable[[Mapping[str, Any]], str],
) -> tuple[dict[str, dict[str, Any]], dict[int, set[str]]]:
    observations: dict[str, dict[str, Any]] = defaultdict(
        _new_symbol_observation
    )
    new_files_by_index: dict[int, set[str]] = defaultdict(set)
    for transition in transitions:
        index = transition["ordered_index"]
        sections = [
            section
            for section in _patch_sections(patch_provider(transition))
            if any(section["path"].endswith(suffix) for suffix in SYMBOL_SUFFIXES)
        ]
        new_files_by_index[index].update(
            section["path"] for section in sections if section["new_file"]
        )
        replaced_definitions = {
            symbol
            for section in sections
            for line in section["removed_lines"]
            for symbol in definitions(line, path=section["path"])
        }
        for section in sections:
            path = section["path"]
            for line in section["added_lines"]:
                for symbol, kind in definition_matches(line, path=path):
                    if symbol in replaced_definitions:
                        continue
                    observation = observations[symbol]
                    observation["roles"][index].add("definition")
                    observation["member_paths"][index].add(path)
                    observation["definition_kinds"][index].add(kind)
                    observation["definition_lines"][index][path].add(line)
                for symbol in complete_uses(line):
                    observation = observations[symbol]
                    observation["roles"][index].add("complete-use")
                    observation["member_paths"][index].add(path)
                    observation["use_lines"][index][path].append(line)
                for symbol in qt_signal_emits(line):
                    observation = observations[symbol]
                    observation["roles"][index].add("complete-use")
                    observation["member_paths"][index].add(path)
                    observation["use_lines"][index][path].append(line)
                    observation["use_kinds"][index].add("qt-signal-emit")
    return observations, new_files_by_index


def _symbol_edge_metadata(
    observation: Mapping[str, Any], members: Sequence[int], provider_new_files: set[str]
) -> dict[str, Any]:
    definition_indices = [
        index
        for index in members
        if "definition" in observation["roles"][index]
    ]
    metadata = {
        "member_paths": {
            str(index): sorted(observation["member_paths"][index])
            for index in members
        },
        "definition_kinds": {
            str(index): sorted(observation["definition_kinds"][index])
            for index in definition_indices
        },
        "definition_lines": {
            str(index): {
                path: sorted(lines)
                for path, lines in sorted(
                    observation["definition_lines"][index].items()
                )
            }
            for index in definition_indices
        },
        "use_lines": {
            str(index): {
                path: list(lines)
                for path, lines in sorted(observation["use_lines"][index].items())
            }
            for index in members
            if observation["use_lines"][index]
        },
        "provider_new_file_paths": sorted(provider_new_files),
    }
    use_kinds = {
        str(index): sorted(observation["use_kinds"][index])
        for index in members
        if observation["use_kinds"][index]
    }
    if use_kinds:
        metadata["use_kinds"] = use_kinds
    return metadata


def _symbol_edges(
    observations: Mapping[str, Mapping[str, Any]],
    new_files_by_index: Mapping[int, set[str]],
    baseline_symbol_exists: Callable[[str], bool] | None,
) -> list[dict[str, Any]]:
    edges = []
    for symbol, observation in sorted(observations.items()):
        if baseline_symbol_exists is not None and baseline_symbol_exists(symbol):
            continue
        roles_by_index = observation["roles"]
        definitions = sorted(
            index
            for index, roles in roles_by_index.items()
            if "definition" in roles
        )
        uses = sorted(
            index
            for index, roles in roles_by_index.items()
            if "complete-use" in roles
        )
        if not definitions or not uses or uses[0] >= definitions[0]:
            continue
        if (
            "member" in observation["definition_kinds"][definitions[0]]
            and not member_use_matches_definition_scope(
                observation["member_paths"],
                provider_index=definitions[0],
                first_use_index=uses[0],
            )
        ):
            continue
        if (
            "qt-signal-emit" in observation["use_kinds"][uses[0]]
            and not symbol_use_matches_definition_scope(
                observation["member_paths"],
                provider_index=definitions[0],
                first_use_index=uses[0],
            )
        ):
            continue
        members = sorted(set(definitions[:1] + uses))
        required_owner = uses[0]
        edge = {
            "kind": "symbol-cross-entry",
            "symbol": symbol,
            "owner_index": definitions[0],
            "required_owner_index": required_owner,
            "observed_member_indices": members,
            "first_member_index": members[0],
            "last_member_index": members[-1],
            "early_member_indices": [
                index for index in members if index < required_owner
            ],
            "roles": {
                str(index): sorted(roles_by_index[index]) for index in members
            },
        }
        edge.update(
            _symbol_edge_metadata(
                observation, members, new_files_by_index[definitions[0]]
            )
        )
        edges.append(edge)
    return edges


def scan_static_dependencies(
    transitions: Sequence[Mapping[str, Any]],
    *,
    patch_provider: Callable[[Mapping[str, Any]], str],
    baseline_symbol_exists: Callable[[str], bool] | None = None,
) -> dict[str, Any]:
    """Scan every supplied transition and return cross-entry static edges."""

    ordered = sorted(transitions, key=lambda entry: entry["ordered_index"])
    observations, new_files_by_index = _symbol_observations(ordered, patch_provider)
    cmake_edges = _cmake_edges(ordered, patch_provider)
    cmake_edges.extend(_cmake_contract_edges(ordered, patch_provider))
    cmake_edges.sort(
        key=lambda edge: (
            edge["kind"],
            edge.get("path", ""),
            edge["owner_index"],
        )
    )
    return {
        "audited_transition_count": len(ordered),
        "symbol_edges": _symbol_edges(
            observations, new_files_by_index, baseline_symbol_exists
        ),
        "cmake_edges": cmake_edges,
    }
