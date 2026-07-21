"""Build the frozen dependency-sensitive transition set and evidence graph."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from collections.abc import Callable, Mapping, Sequence
from typing import Any

from .dependency_scanner import scan_static_dependencies
from .runtime_dependency import build_runtime_dependency_edges


def _canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _edge_id(kind: str, payload: Mapping[str, Any]) -> str:
    return f"edge:{kind}:{_sha256(payload)[:20]}"


def _entry_category(entry: Mapping[str, Any]) -> str:
    if entry["ordered_index"] == 1:
        return "anchor"
    if entry.get("tree_transition") == "regenerate":
        return "regenerate"
    if entry.get("remediation_proof") is not None:
        return "remediation"
    return "ordinary"


def _synthesis_audit(
    bootstrap: Mapping[str, Any], entries_by_id: Mapping[str, Mapping[str, Any]]
) -> list[dict[str, Any]]:
    result = []
    for item in bootstrap["entries"]:
        replacement = item["replacement"]
        if replacement.get("kind") != "frozen-remediation-blob-transition":
            continue
        entry = entries_by_id[item["entry_id"]]
        remediation_paths = sorted(replacement.get("remediation_paths", ()))
        result.append(
            {
                "entry_id": item["entry_id"],
                "ordered_index": entry["ordered_index"],
                "classification": (
                    "remediation-proof"
                    if remediation_paths
                    else "carry-forward-dependency"
                ),
                "remediation_paths": remediation_paths,
                "synthesized_paths": sorted(
                    replacement.get("synthesized_paths", ())
                ),
            }
        )
    return sorted(result, key=lambda item: item["ordered_index"])


def _base_edges(
    ordinary: list[Mapping[str, Any]],
    synthesis: list[Mapping[str, Any]],
    remediation: Mapping[str, Any],
    protocol: Mapping[str, Any],
) -> list[dict[str, Any]]:
    ordinary_by_index = {entry["ordered_index"]: entry for entry in ordinary}
    carry_by_index = {
        item["ordered_index"]: item
        for item in synthesis
        if item["classification"] == "carry-forward-dependency"
    }
    gates_by_path: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for gate in remediation.get("occurrence_gates", ()):
        gates_by_path[gate["path"]].append(gate)
    edges: list[dict[str, Any]] = []

    for index, item in sorted(carry_by_index.items()):
        payload = {
            "kind": "carry-forward-lineage",
            "owner_index": index,
            "entry_id": item["entry_id"],
            "synthesized_paths": item["synthesized_paths"],
        }
        edges.append({"edge_id": _edge_id(payload["kind"], payload), **payload})
        for path in item["synthesized_paths"]:
            for gate in gates_by_path.get(path, ()):
                gate_payload = {
                    "kind": "workaround-lifecycle",
                    "owner_index": index,
                    "gate_id": gate["gate_id"],
                    "path": path,
                    "component_ids": sorted(gate.get("component_ids", ())),
                }
                edges.append(
                    {
                        "edge_id": _edge_id(gate_payload["kind"], gate_payload),
                        **gate_payload,
                    }
                )

    for component in protocol.get("components", ()):
        index = component["owner_index"]
        if index not in ordinary_by_index:
            continue
        payload = {
            "kind": "protocol-interface",
            "owner_index": index,
            "protocol_component_id": component["protocol_component_id"],
            "generated_signatures": component["generated_signatures"],
            "result_blob": component["result_blob"],
        }
        edges.append({"edge_id": _edge_id(payload["kind"], payload), **payload})

    for entry in ordinary:
        if entry.get("gitlink_before") == entry.get("gitlink_after"):
            continue
        payload = {
            "kind": "waylib-capability",
            "owner_index": entry["ordered_index"],
            "gitlink_before": entry.get("gitlink_before"),
            "gitlink_after": entry.get("gitlink_after"),
        }
        edges.append({"edge_id": _edge_id(payload["kind"], payload), **payload})
    return edges


def _static_edges(
    static_scan: Mapping[str, Any], ordinary_indexes: set[int]
) -> list[dict[str, Any]]:
    edges = []
    for raw in (*static_scan["symbol_edges"], *static_scan["cmake_edges"]):
        affected = sorted(
            set(raw["observed_member_indices"]) & ordinary_indexes
        )
        payload = {**raw, "affected_ordinary_indices": affected}
        edges.append(
            {"edge_id": _edge_id(payload["kind"], payload), **payload}
        )
    return edges


def _runtime_edges(
    entries: Sequence[Mapping[str, Any]],
    observations: Sequence[Mapping[str, Any]],
    ordinary_indexes: set[int],
    *,
    waylib_is_ancestor: Callable[[str, str], bool] | None,
    waylib_blob_reader: Callable[[str, str], str] | None,
) -> list[dict[str, Any]]:
    if not observations:
        return []
    if waylib_is_ancestor is None or waylib_blob_reader is None:
        raise ValueError("runtime dependencies require frozen Waylib readers")
    return [
        {"edge_id": _edge_id(edge["kind"], edge), **edge}
        for edge in build_runtime_dependency_edges(
            entries,
            observations,
            ordinary_indexes=ordinary_indexes,
            is_ancestor=waylib_is_ancestor,
            read_blob=waylib_blob_reader,
        )
    ]


def _classifications(
    ordinary: list[Mapping[str, Any]],
    mapping_by_index: Mapping[int, Mapping[str, Any]],
    edges: list[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    edges_by_index: dict[int, list[Mapping[str, Any]]] = defaultdict(list)
    for edge in edges:
        affected = edge.get("affected_ordinary_indices", (edge["owner_index"],))
        for index in affected:
            edges_by_index[index].append(edge)
    rows = []
    for entry in sorted(ordinary, key=lambda item: item["ordered_index"]):
        index = entry["ordered_index"]
        mapping = mapping_by_index[index]
        matched = sorted(edges_by_index.get(index, ()), key=lambda edge: edge["edge_id"])
        reasons = sorted({edge["kind"] for edge in matched})
        rows.append(
            {
                "ordered_index": index,
                "entry_id": entry["entry_id"],
                "classification": "dependency-sensitive" if matched else "independent",
                "reason_kinds": reasons,
                "edge_ids": [edge["edge_id"] for edge in matched],
                "expected_v1_commit": entry.get("expected_v1_commit"),
                "expected_v1_parent": entry.get("expected_v1_parent"),
                "expected_v1_tree": entry.get("expected_v1_tree"),
                "provisional_v2_commit": mapping.get("new_commit"),
                "provisional_v2_tree": mapping.get("new_tree"),
                "changed_paths": sorted(entry.get("expected_v1_changed_paths", ())),
                "gitlink_before": entry.get("gitlink_before"),
                "gitlink_after": entry.get("gitlink_after"),
                "audit_status": "complete",
            }
        )
    return rows


def build_dependency_set(
    manifest: Mapping[str, Any],
    mapping: Mapping[str, Any],
    bootstrap: Mapping[str, Any],
    remediation: Mapping[str, Any],
    protocol: Mapping[str, Any],
    *,
    patch_provider: Callable[[Mapping[str, Any]], str],
    baseline_symbol_exists: Callable[[str], bool] | None = None,
    runtime_observations: Sequence[Mapping[str, Any]] = (),
    waylib_is_ancestor: Callable[[str, str], bool] | None = None,
    waylib_blob_reader: Callable[[str, str], str] | None = None,
) -> dict[str, Any]:
    """Build a deterministic partition and graph from frozen predecessor inputs."""

    entries = sorted(manifest["entries"], key=lambda item: item["ordered_index"])
    entries_by_id = {entry["entry_id"]: entry for entry in entries}
    mapping_by_index = {
        entry["ordered_index"]: entry for entry in mapping["entries"]
    }
    categorized: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for entry in entries:
        categorized[_entry_category(entry)].append(entry)
    ordinary = categorized["ordinary"]
    rendered = ordinary + categorized["remediation"]
    synthesis = _synthesis_audit(bootstrap, entries_by_id)
    static_scan = scan_static_dependencies(
        rendered,
        patch_provider=patch_provider,
        baseline_symbol_exists=baseline_symbol_exists,
    )
    ordinary_indexes = {entry["ordered_index"] for entry in ordinary}
    edges = _base_edges(ordinary, synthesis, remediation, protocol)
    edges.extend(
        _static_edges(static_scan, ordinary_indexes)
    )
    edges.extend(
        _runtime_edges(
            entries,
            runtime_observations,
            ordinary_indexes,
            waylib_is_ancestor=waylib_is_ancestor,
            waylib_blob_reader=waylib_blob_reader,
        )
    )
    edges = sorted(edges, key=lambda edge: edge["edge_id"])
    classifications = _classifications(ordinary, mapping_by_index, edges)
    sensitive = [
        row["ordered_index"]
        for row in classifications
        if row["classification"] == "dependency-sensitive"
    ]
    counts = {
        "anchor": len(categorized["anchor"]),
        "ordinary_candidates": len(ordinary),
        "remediation_targets": len(categorized["remediation"]),
        "regenerate": len(categorized["regenerate"]),
        "synthesis_transitions": len(synthesis),
        "carry_forward": sum(
            item["classification"] == "carry-forward-dependency"
            for item in synthesis
        ),
        "dependency_sensitive": len(sensitive),
        "independent": len(ordinary) - len(sensitive),
        "unaudited": sum(row["audit_status"] != "complete" for row in classifications),
        "runtime_dependencies": len(runtime_observations),
    }
    graph = {
        "nodes": [
            {
                "node_id": f"transition:{entry['ordered_index']}",
                "ordered_index": entry["ordered_index"],
                "entry_id": entry["entry_id"],
                "category": _entry_category(entry),
            }
            for entry in entries
        ],
        "edges": edges,
    }
    return {
        "schema_version": 1,
        "kind": "dependency-sensitive-set-D",
        "source_hashes": {
            "manifest": manifest.get("canonical_payload_sha256"),
            "mapping": mapping.get("canonical_payload_sha256"),
            "bootstrap": bootstrap.get("manifest_sha256"),
            "remediation": remediation.get("canonical_sha256"),
            "protocol": protocol.get("artifact_sha256"),
            "runtime_observations": _sha256(list(runtime_observations)),
        },
        "counts": counts,
        "remediation_target_indices": sorted(
            entry["ordered_index"] for entry in categorized["remediation"]
        ),
        "carry_forward_entry_ids": [
            item["entry_id"]
            for item in synthesis
            if item["classification"] == "carry-forward-dependency"
        ],
        "dependency_sensitive_indices": sensitive,
        "ordinary_classifications_sha256": _sha256(classifications),
        "ordinary_classifications": classifications,
        "synthesis_audit": synthesis,
        "static_scan": {
            "audited_transition_count": static_scan["audited_transition_count"],
            "symbol_edge_count": len(static_scan["symbol_edges"]),
            "cmake_edge_count": len(static_scan["cmake_edges"]),
            "scan_sha256": _sha256(static_scan),
        },
        "graph_sha256": _sha256(graph),
        "graph": graph,
    }
