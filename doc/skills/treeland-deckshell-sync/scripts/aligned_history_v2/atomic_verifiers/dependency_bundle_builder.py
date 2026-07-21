"""Build atomic dependency bundles from frozen transition and remediation ledgers."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from collections.abc import Mapping
from typing import Any

from .bundle_paths import bundle_paths
from .provider_closure import remediation_target_owners
from .runtime_dependency import RUNTIME_WAYLIB_EDGE_KIND


_XDG_SYMBOLS = {"XdgDialogManagerV1Bridge", "setModal", "lcTlShell"}


def _canonical_sha256(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8") + b"\n"
    return hashlib.sha256(raw).hexdigest()


def _component_id(prefix: str, value: str) -> str:
    return f"{prefix}:{value}"


def _edge_source_indices(edge: Mapping[str, Any]) -> list[int]:
    return sorted(
        set(edge.get("observed_member_indices", (edge["owner_index"],)))
    )


def _xdg_edge(edge: Mapping[str, Any]) -> bool:
    return (
        edge.get("kind") == "symbol-cross-entry"
        and edge.get("symbol") in _XDG_SYMBOLS
    )


def _bundle_id(owner_index: int, capability: str, *, xdg: bool = False) -> str:
    if xdg:
        return "deck:133:xdg-dialog-v1"
    return f"deck:{owner_index}:{capability}"


def _graph_components(
    dependency_set: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, str], bool]:
    components = []
    edge_components: dict[str, str] = {}
    xdg_present = any(_xdg_edge(edge) for edge in dependency_set["graph"]["edges"])
    for edge in dependency_set["graph"]["edges"]:
        if edge["kind"] == "protocol-interface":
            continue
        xdg = _xdg_edge(edge)
        owner = 133 if xdg else edge.get("required_owner_index", edge["owner_index"])
        component_kind = (
            "waylib-capability"
            if edge["kind"] == RUNTIME_WAYLIB_EDGE_KIND
            else edge["kind"]
        )
        component_id = _component_id("graph", edge["edge_id"])
        edge_components[edge["edge_id"]] = component_id
        components.append(
            {
                "component_id": component_id,
                "kind": component_kind,
                "owner_index": owner,
                "target_owner_index": owner,
                "source_indices": _edge_source_indices(edge),
                "payload": dict(edge),
                "bundle_id": _bundle_id(owner, component_kind, xdg=xdg),
            }
        )
    return components, edge_components, xdg_present


def _protocol_components(
    protocol: Mapping[str, Any], dependency_set: Mapping[str, Any]
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    graph_edge_by_component = {
        edge["protocol_component_id"]: edge["edge_id"]
        for edge in dependency_set["graph"]["edges"]
        if edge["kind"] == "protocol-interface"
    }
    components = []
    edge_components = {}
    for component in protocol["components"]:
        owner = component["owner_index"]
        component_id = _component_id("protocol", component["protocol_component_id"])
        edge_id = graph_edge_by_component.get(component["protocol_component_id"])
        if edge_id is not None:
            edge_components[edge_id] = component_id
        payload = {
            "protocol_component_id": component["protocol_component_id"],
            "owner_index": owner,
            "source_path": component["source_path"],
            "target_path": component["target_path"],
            "generated_signatures": component["generated_signatures"],
            "result_blob": component["result_blob"],
        }
        if edge_id is not None:
            payload["edge_id"] = edge_id
        components.append(
            {
                "component_id": component_id,
                "kind": "protocol-interface",
                "owner_index": owner,
                "target_owner_index": owner,
                "source_indices": [owner],
                "payload": payload,
                "bundle_id": _bundle_id(owner, "protocol-interface"),
            }
        )
    return components, edge_components


def _remediation_deltas(
    remediation: Mapping[str, Any],
    target_by_component: Mapping[str, Mapping[str, Any]],
    target_owners: Mapping[int, int],
    xdg_targets: set[int],
) -> list[dict[str, Any]]:
    components = []
    for source in sorted(
        remediation["components"], key=lambda item: item["component_id"]
    ):
        component_id = source["component_id"]
        target = target_by_component[component_id]
        target_index = target["target_index"]
        xdg = target_index in xdg_targets
        owner = target_owners.get(target_index, target_index)
        components.append(
            {
                "component_id": _component_id("remediation", component_id),
                "kind": "remediation-component",
                "owner_index": owner,
                "target_owner_index": owner,
                "source_indices": [target_index],
                "payload": {
                    "component_id": component_id,
                    "target_index": target_index,
                    "path": source["path"],
                    "owner_source": source["owner_source"],
                    "before_sha256": source["before_sha256"],
                    "after_sha256": source["after_sha256"],
                },
                "bundle_id": _bundle_id(owner, "remediation", xdg=xdg),
            }
        )
    return components


def _remediation_capabilities(
    remediation: Mapping[str, Any],
    target_owners: Mapping[int, int],
    xdg_targets: set[int],
) -> list[dict[str, Any]]:
    components = []
    for target in remediation["targets"]:
        target_index = target["target_index"]
        xdg = target_index in xdg_targets
        owner = target_owners.get(target_index, target_index)
        for proof in target.get("capability_proofs", ()):
            identity = _canonical_sha256(
                {"target_index": target_index, "proof": proof}
            )[:20]
            components.append(
                {
                    "component_id": _component_id("waylib-capability", identity),
                    "kind": "waylib-capability",
                    "owner_index": owner,
                    "target_owner_index": owner,
                    "source_indices": [target_index],
                    "payload": {
                        "target_index": target_index,
                        "gitlink_after": target["waylib_gitlink"],
                        "label": proof["label"],
                        "path": proof["path"],
                        "needle": proof["needle"],
                        "introduced_by": proof["introduced_by"],
                    },
                    "bundle_id": _bundle_id(owner, "waylib-capability", xdg=xdg),
                }
            )
    return components


def _gate_owner(
    gate: Mapping[str, Any],
    target_by_component: Mapping[str, Mapping[str, Any]],
    target_by_source: Mapping[str, Mapping[str, Any]],
) -> int:
    owners = {
        target_by_component[component_id]["target_index"]
        for component_id in gate["component_ids"]
    }
    owners.update(
        target_by_source[source]["target_index"]
        for source in gate.get("owner_sources", ())
    )
    if not owners:
        raise ValueError(f"unowned workaround gate: {gate['gate_id']}")
    return min(owners)


def _remediation_gates(
    remediation: Mapping[str, Any],
    target_by_component: Mapping[str, Mapping[str, Any]],
    target_by_source: Mapping[str, Mapping[str, Any]],
    target_owners: Mapping[int, int],
    xdg_targets: set[int],
) -> list[dict[str, Any]]:
    components = []
    for gate in remediation.get("occurrence_gates", ()):
        original_owner = _gate_owner(
            gate, target_by_component, target_by_source
        )
        xdg = original_owner in xdg_targets
        owner = target_owners.get(original_owner, original_owner)
        components.append(
            {
                "component_id": _component_id("workaround-gate", gate["gate_id"]),
                "kind": "workaround-lifecycle",
                "owner_index": owner,
                "target_owner_index": owner,
                "source_indices": [original_owner],
                "payload": dict(gate),
                "bundle_id": _bundle_id(owner, "workaround-lifecycle", xdg=xdg),
            }
        )
    return components


def _remediation_components(
    remediation: Mapping[str, Any],
    dependency_set: Mapping[str, Any],
    xdg_present: bool,
) -> list[dict[str, Any]]:
    target_by_component = {
        component_id: target
        for target in remediation["targets"]
        for component_id in target["component_ids"]
    }
    target_by_source = {
        target["source_commit"]: target
        for target in remediation["targets"]
        if target.get("source_commit")
    }
    xdg_targets = {133, 278} if xdg_present else set()
    target_owners = remediation_target_owners(
        dependency_set, xdg_targets=xdg_targets
    )
    return (
        _remediation_deltas(
            remediation, target_by_component, target_owners, xdg_targets
        )
        + _remediation_capabilities(
            remediation, target_owners, xdg_targets
        )
        + _remediation_gates(
            remediation,
            target_by_component,
            target_by_source,
            target_owners,
            xdg_targets,
        )
    )


def expected_bundle_components(
    dependency_set: Mapping[str, Any],
    protocol: Mapping[str, Any],
    remediation: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Derive every uniquely owned bundle component from frozen ledgers."""

    graph, graph_edge_ids, xdg_present = _graph_components(dependency_set)
    protocol_components, protocol_edge_ids = _protocol_components(
        protocol, dependency_set
    )
    components = graph + protocol_components + _remediation_components(
        remediation, dependency_set, xdg_present
    )
    component_ids = [component["component_id"] for component in components]
    if len(component_ids) != len(set(component_ids)):
        raise ValueError("dependency component id collision")
    for component in components:
        edge_id = component["payload"].get("edge_id")
        if edge_id is not None:
            graph_edge_ids[edge_id] = component["component_id"]
    components.sort(key=lambda component: component["component_id"])
    return components


def _bundles(components: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for component in components:
        grouped[component["bundle_id"]].append(component)
    bundles = []
    for bundle_id, members in sorted(grouped.items()):
        owner_indexes = {member["owner_index"] for member in members}
        if len(owner_indexes) != 1:
            raise ValueError(f"inconsistent bundle owner: {bundle_id}")
        owner = next(iter(owner_indexes))
        component_ids = sorted(member["component_id"] for member in members)
        proof_nodes = sorted(
            {index for member in members for index in member["source_indices"]}
        )
        by_kind: dict[str, list[str]] = defaultdict(list)
        for member in members:
            by_kind[member["kind"]].append(member["component_id"])
        bundles.append(
            {
                "bundle_id": bundle_id,
                "owner_index": owner,
                "component_ids": component_ids,
                "preconditions": [
                    {"kind": kind, "component_ids": sorted(ids)}
                    for kind, ids in sorted(by_kind.items())
                ],
                "forbidden_early_members": [
                    {
                        "component_id": component_id,
                        "before_owner_index": owner,
                    }
                    for component_id in component_ids
                ],
                "expected_changed_paths": bundle_paths(members),
                "proof_nodes": proof_nodes,
            }
        )
    return bundles


def _dependency_coverage(
    dependency_set: Mapping[str, Any], components: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    edge_to_component = {
        component["payload"]["edge_id"]: component
        for component in components
        if component["payload"].get("edge_id")
    }
    rows_by_index = {
        row["ordered_index"]: row
        for row in dependency_set["ordinary_classifications"]
    }
    coverage = []
    for index in dependency_set["dependency_sensitive_indices"]:
        matched = [
            edge_to_component[edge_id]
            for edge_id in rows_by_index[index]["edge_ids"]
        ]
        coverage.append(
            {
                "ordered_index": index,
                "component_ids": sorted(
                    component["component_id"] for component in matched
                ),
                "bundle_ids": sorted(
                    component["bundle_id"] for component in matched
                ),
            }
        )
    return coverage


def build_dependency_bundle_ledger(
    dependency_set: Mapping[str, Any],
    protocol: Mapping[str, Any],
    remediation: Mapping[str, Any],
) -> dict[str, Any]:
    """Build a deterministic dependency-bundle ledger for task 6."""

    components = expected_bundle_components(dependency_set, protocol, remediation)
    bundles = _bundles(components)
    coverage = _dependency_coverage(dependency_set, components)
    return {
        "schema_version": 1,
        "kind": "dependency-bundle-ledger-v1",
        "source_hashes": {
            "dependency_set": dependency_set.get("artifact_sha256"),
            "protocol": protocol.get("artifact_sha256"),
            "remediation": remediation.get("canonical_sha256"),
        },
        "component_count": len(components),
        "bundle_count": len(bundles),
        "components_sha256": _canonical_sha256(components),
        "bundles_sha256": _canonical_sha256(bundles),
        "components": components,
        "bundles": bundles,
        "dependency_transition_coverage": coverage,
    }
