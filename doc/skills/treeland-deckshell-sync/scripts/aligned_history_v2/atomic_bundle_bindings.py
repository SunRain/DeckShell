"""Bind dependency bundles to their actual v2 Git objects."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any

from .atomic_bindings import (
    _blob,
    _blob_id,
    _commit,
    _parent,
    _records,
    _require_record,
    _terminal_component,
)
from .atomic_verifiers.cmake_contract import (
    detect_contract_roles,
    normalize_cmake_payload,
)
from .repository import GitRepository
from .tree_manifest import tree_diff_paths


def verify_bundle_materialization(
    repo: GitRepository,
    records: Sequence[Mapping[str, Any]],
    ledger: Mapping[str, Any],
    protocol_ledger: Mapping[str, Any],
    *,
    v1_records: Sequence[Mapping[str, Any]] = (),
) -> dict[str, int]:
    """Verify every bundle's local paths and semantic definitions at its owner."""

    by_index = _records(records)
    v1_by_index = _records(v1_records) if v1_records else {}
    components = {
        str(component["component_id"]): component
        for component in ledger.get("components", ())
    }
    protocol_expectations = _protocol_target_expectations(protocol_ledger)
    inherited_paths = checked_paths = external_source_paths = 0
    deferred_provider_paths = 0
    protocol_target_paths = semantic_checks = 0
    for bundle in ledger.get("bundles", ()):
        owner = int(bundle["owner_index"])
        record = _require_record(by_index, owner)
        commit = _commit(record)
        changed = set(tree_diff_paths(repo, _parent(record), commit))
        deferred_components = _deferred_bundle_components(
            bundle, components, v1_by_index.get(owner)
        )
        deferred_paths = _deferred_provider_paths(
            set(deferred_components), components
        )
        obsolete_deferred_uses = _deferred_obsolete_use_lines(
            deferred_components, components
        )
        external_paths = _bundle_external_source_paths(bundle, components)
        protocol_paths = _bundle_protocol_target_paths(bundle, components)
        occurrence_limits = _bundle_occurrence_limits(bundle, components)
        obsolete_definitions = {
            key for key, maximum in occurrence_limits.items() if maximum == 0
        }
        for raw_path in bundle.get("expected_changed_paths", ()):
            path = str(raw_path)
            if path.startswith("waylib/"):
                continue
            if path in external_paths:
                external_source_paths += 1
                continue
            if path in protocol_paths:
                _verify_protocol_target(
                    repo, commit, owner, path, protocol_expectations
                )
                protocol_target_paths += 1
                continue
            if path in deferred_paths:
                deferred_provider_paths += 1
                continue
            checked_paths += 1
            if path not in changed:
                if _blob_id(repo, commit, path) is None:
                    raise ValueError(
                        f"dependency bundle path is absent at {owner}: {path}"
                    )
                inherited_paths += 1
        semantic_checks += _verify_occurrence_limits(
            repo, commit, owner, occurrence_limits
        )
        for component_id in bundle.get("component_ids", ()):
            component = components[str(component_id)]
            if str(component_id) in deferred_components:
                semantic_checks += _verify_deferred_component_semantics(
                    repo,
                    by_index,
                    owner,
                    commit,
                    component,
                    component_status=str(
                        deferred_components[str(component_id)].get("status", "")
                    ),
                    obsolete_uses=obsolete_deferred_uses,
                )
            else:
                semantic_checks += _verify_component_semantics(
                    repo,
                    commit,
                    component,
                    obsolete_definitions=obsolete_definitions,
                )
    return {
        "bundle_count": len(ledger.get("bundles", ())),
        "component_count": len(components),
        "checked_local_path_count": checked_paths,
        "inherited_local_path_count": inherited_paths,
        "external_source_path_count": external_source_paths,
        "protocol_target_path_count": protocol_target_paths,
        "deferred_provider_path_count": deferred_provider_paths,
        "semantic_check_count": semantic_checks,
        "missing_path_count": 0,
    }


def _deferred_bundle_components(
    bundle: Mapping[str, Any],
    components: Mapping[str, Mapping[str, Any]],
    v1_record: Mapping[str, Any] | None,
) -> dict[str, Mapping[str, Any]]:
    if v1_record is None:
        return {}
    reports = {
        str(item["component_id"]): item
        for item in v1_record.get("symbol_components", ())
    }
    bundle_ids = {str(item) for item in bundle.get("component_ids", ())}
    has_deferred_seed = any(
        reports.get(component_id, {}).get("mode") == "deferred-consumer"
        and reports.get(component_id, {}).get("status") == "applied"
        for component_id in bundle_ids
    )
    if not has_deferred_seed:
        return {}
    return {
        component_id: reports[component_id]
        for component_id in bundle_ids
        if components[component_id].get("kind") == "symbol-cross-entry"
        and reports.get(component_id, {}).get("status")
        in {"applied", "obsolete-satisfied"}
    }


def _deferred_provider_paths(
    component_ids: set[str],
    components: Mapping[str, Mapping[str, Any]],
) -> set[str]:
    paths: set[str] = set()
    for component_id in component_ids:
        payload = components[component_id].get("payload", {})
        paths.update(str(path) for path in payload.get("provider_new_file_paths", ()))
        provider = str(payload.get("owner_index", ""))
        for path in payload.get("definition_lines", {}).get(provider, {}):
            paths.add(str(path))
    return paths


def _deferred_obsolete_use_lines(
    reports: Mapping[str, Mapping[str, Any]],
    components: Mapping[str, Mapping[str, Any]],
) -> set[tuple[str, str]]:
    uses: set[tuple[str, str]] = set()
    for component_id, report in reports.items():
        if report.get("status") != "obsolete-satisfied":
            continue
        payload = components[component_id].get("payload", {})
        for paths in payload.get("use_lines", {}).values():
            for path, lines in paths.items():
                uses.update((str(path), str(line)) for line in lines)
    return uses


def _verify_deferred_component_semantics(
    repo: GitRepository,
    by_index: Mapping[int, Mapping[str, Any]],
    owner: int,
    owner_commit: str,
    component: Mapping[str, Any],
    *,
    component_status: str,
    obsolete_uses: set[tuple[str, str]],
) -> int:
    payload = component.get("payload", {})
    provider = int(payload.get("owner_index", 0))
    required_owner = int(payload.get("required_owner_index", 0))
    if required_owner != owner or provider <= owner:
        raise ValueError(
            f"invalid deferred consumer boundary: {component['component_id']}"
        )
    provider_commit = _commit(_require_record(by_index, provider))
    checks = _verify_deferred_use_lines(
        repo,
        owner_commit,
        provider_commit,
        owner,
        provider,
        payload,
        restore_at_provider=component_status != "obsolete-satisfied",
        obsolete_uses=obsolete_uses,
    )
    for path in payload.get("provider_new_file_paths", ()):
        if _blob_id(repo, provider_commit, str(path)) is None:
            raise ValueError(
                f"deferred provider path is absent at {provider}: {path}"
            )
        checks += 1
    for index, paths in payload.get("definition_lines", {}).items():
        if int(index) > provider:
            continue
        for path, lines in paths.items():
            owner_content = (
                _blob(repo, owner_commit, str(path)).decode("utf-8")
                if _blob_id(repo, owner_commit, str(path)) is not None
                else ""
            )
            content = _blob(repo, provider_commit, str(path)).decode("utf-8")
            for line in lines:
                if str(line) in owner_content:
                    raise ValueError(
                        f"deferred provider definition appears before provider at {owner}: {path}: {line}"
                    )
                if component_status == "obsolete-satisfied":
                    if str(line) in content:
                        raise ValueError(
                            f"obsolete deferred provider definition remains at {provider}: {path}: {line}"
                        )
                    checks += 1
                    continue
                if str(line) not in content:
                    raise ValueError(
                        f"deferred provider definition differs at {provider}: {path}: {line}"
                    )
                checks += 1
    return checks


def _verify_deferred_use_lines(
    repo: GitRepository,
    owner_commit: str,
    provider_commit: str,
    owner: int,
    provider: int,
    payload: Mapping[str, Any],
    *,
    restore_at_provider: bool,
    obsolete_uses: set[tuple[str, str]],
) -> int:
    checks = 0
    for index, paths in payload.get("use_lines", {}).items():
        source_index = int(index)
        if source_index > provider:
            continue
        for path, lines in paths.items():
            provider_content = _blob(repo, provider_commit, str(path)).decode("utf-8")
            owner_content = (
                _blob(repo, owner_commit, str(path)).decode("utf-8")
                if source_index == owner
                else ""
            )
            for line in lines:
                text = str(line)
                obsolete = not restore_at_provider or (str(path), text) in obsolete_uses
                if source_index == owner and text in owner_content:
                    raise ValueError(
                        f"deferred consumer remains at {owner}: {path}: {text}"
                    )
                if not obsolete and text not in provider_content:
                    raise ValueError(
                        f"deferred consumer is not restored at {provider}: {path}: {text}"
                    )
                if obsolete and text in provider_content:
                    raise ValueError(
                        f"obsolete deferred consumer is present at {provider}: {path}: {text}"
                    )
                checks += 1
    return checks


def _verify_protocol_target(
    repo: GitRepository,
    commit: str,
    owner: int,
    path: str,
    expectations: Mapping[tuple[int, str], str | None],
) -> None:
    key = (owner, path)
    if key not in expectations:
        raise ValueError(
            f"dependency protocol target has no terminal proof: {owner}: {path}"
        )
    if _blob_id(repo, commit, path) != expectations[key]:
        raise ValueError(f"dependency protocol target differs at {owner}: {path}")


def _verify_occurrence_limits(
    repo: GitRepository,
    commit: str,
    owner: int,
    limits: Mapping[tuple[str, str], int],
) -> int:
    for (path, needle), maximum in limits.items():
        content = _blob(repo, commit, path).decode("utf-8")
        if content.count(needle) > maximum:
            raise ValueError(
                f"obsolete dependency occurrence remains at {owner}: {path}: {needle}"
            )
    return len(limits)


def _bundle_external_source_paths(
    bundle: Mapping[str, Any], components: Mapping[str, Mapping[str, Any]]
) -> set[str]:
    paths = set()
    for component_id in bundle.get("component_ids", ()):
        component = components[str(component_id)]
        if component.get("kind") != "protocol-interface":
            continue
        payload = component.get("payload", {})
        source = payload.get("source_path")
        target = payload.get("target_path")
        if source and source != target:
            paths.add(str(source))
    return paths


def _bundle_protocol_target_paths(
    bundle: Mapping[str, Any], components: Mapping[str, Mapping[str, Any]]
) -> set[str]:
    paths = set()
    for component_id in bundle.get("component_ids", ()):
        component = components[str(component_id)]
        if component.get("kind") != "protocol-interface":
            continue
        target = component.get("payload", {}).get("target_path")
        if target:
            paths.add(str(target))
    return paths


def _protocol_target_expectations(
    protocol_ledger: Mapping[str, Any],
) -> dict[tuple[int, str], str | None]:
    grouped: dict[tuple[int, str], list[Mapping[str, Any]]] = defaultdict(list)
    for component in protocol_ledger.get("components", ()):
        key = (int(component["owner_index"]), str(component["target_path"]))
        grouped[key].append(component)
    return {
        key: _terminal_component(items).get("result_blob")
        for key, items in grouped.items()
    }


def _bundle_occurrence_limits(
    bundle: Mapping[str, Any], components: Mapping[str, Mapping[str, Any]]
) -> dict[tuple[str, str], int]:
    limits = {}
    for component_id in bundle.get("component_ids", ()):
        component = components[str(component_id)]
        if component.get("kind") != "workaround-lifecycle":
            continue
        payload = component.get("payload", {})
        has_needle = "needle" in payload
        has_maximum = "maximum" in payload
        if not has_needle and not has_maximum:
            continue
        if has_needle != has_maximum:
            raise ValueError(
                f"incomplete dependency occurrence limit: {component_id}"
            )
        key = (str(payload["path"]), str(payload["needle"]))
        maximum = int(payload["maximum"])
        if key in limits and limits[key] != maximum:
            raise ValueError(f"conflicting dependency occurrence limits: {key}")
        limits[key] = maximum
    return limits


def _verify_component_semantics(
    repo: GitRepository,
    commit: str,
    component: Mapping[str, Any],
    *,
    obsolete_definitions: set[tuple[str, str]],
) -> int:
    payload = component.get("payload", {})
    checks = 0
    for paths in payload.get("definition_lines", {}).values():
        for path, lines in paths.items():
            content = _blob(repo, commit, str(path)).decode("utf-8")
            for line in lines:
                if (str(path), str(line)) in obsolete_definitions:
                    continue
                if str(line) not in content:
                    raise ValueError(
                        f"dependency definition differs at {commit}: {path}: {line}"
                    )
                checks += 1
    if component.get("kind") == "cmake-contract" and payload.get("path"):
        path = str(payload["path"])
        content = _blob(repo, commit, path)
        remaining = set(
            detect_contract_roles(content.decode("utf-8").splitlines(), path=path)
        )
        required = {
            role for roles in payload.get("roles", {}).values() for role in roles
        }
        normalized, _ = normalize_cmake_payload(path, content)
        if remaining or normalized != content:
            raise ValueError(f"CMake contract differs at {commit}: {path}")
        checks += len(required)
    return checks
