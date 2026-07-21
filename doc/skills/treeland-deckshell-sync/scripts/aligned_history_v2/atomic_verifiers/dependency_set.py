"""Independent validation for the dependency-sensitive transition set."""

from __future__ import annotations

from collections import Counter
from collections.abc import Collection, Mapping, Sequence
from typing import Any

from .runtime_dependency import RUNTIME_WAYLIB_EDGE_KIND


class DependencySetError(ValueError):
    """Raised when the ordinary transition partition is not complete."""

    def __init__(self, report: Mapping[str, int]) -> None:
        self.report = dict(report)
        summary = ", ".join(
            f"{key}={value}" for key, value in self.report.items() if value
        )
        super().__init__(f"invalid dependency-sensitive set: {summary}")


def _identity(entry: Mapping[str, Any]) -> tuple[int, str]:
    return entry.get("ordered_index"), entry.get("entry_id")


def _member_timeline_invalid(edge: Mapping[str, Any]) -> bool:
    if edge.get("kind") not in {
        "symbol-cross-entry",
        "cmake-cross-entry",
        RUNTIME_WAYLIB_EDGE_KIND,
    }:
        return False
    members = edge.get("observed_member_indices", ())
    required_owner = edge.get("required_owner_index")
    if not members or not isinstance(required_owner, int):
        return True
    ordered = sorted(set(members))
    return any(
        (
            list(members) != ordered,
            edge.get("first_member_index") != ordered[0],
            edge.get("last_member_index") != ordered[-1],
            edge.get("early_member_indices")
            != [index for index in ordered if index < required_owner],
        )
    )


def _edge_owner_mismatch(
    entry: Mapping[str, Any], edge: Mapping[str, Any]
) -> bool:
    affected = edge.get("affected_ordinary_indices")
    if affected is not None:
        return entry.get("ordered_index") not in affected
    return edge.get("owner_index") != entry.get("ordered_index")


def _is_remediation_only_edge(
    edge: Mapping[str, Any], remediation_indexes: Collection[int]
) -> bool:
    affected = edge.get("affected_ordinary_indices")
    members = edge.get("observed_member_indices")
    if affected != [] or not isinstance(members, Sequence) or not members:
        return False
    involved = (
        edge.get("owner_index"),
        edge.get("required_owner_index"),
        *members,
    )
    return all(
        isinstance(index, int) and index in remediation_indexes
        for index in involved
    )


def verify_dependency_set(
    ledger: Mapping[str, Any],
    *,
    ordinary_candidates: Sequence[Mapping[str, Any]],
    remediation_targets: Collection[int],
    carry_forward_entry_ids: Collection[str],
    protocol_components: Sequence[Mapping[str, Any]],
) -> dict[str, int]:
    """Verify the complete, disjoint ordinary transition partition."""

    classifications = ledger.get("ordinary_classifications", ())
    expected = {_identity(entry) for entry in ordinary_candidates}
    ordinary_indexes = {index for index, _ in expected}
    candidate_by_identity = {
        _identity(entry): entry for entry in ordinary_candidates
    }
    actual = Counter(_identity(entry) for entry in classifications)
    actual_identities = set(actual)
    remediation_indexes = set(remediation_targets)
    sensitive_from_rows = sorted(
        entry.get("ordered_index")
        for entry in classifications
        if entry.get("classification") == "dependency-sensitive"
    )
    declared_sensitive = ledger.get("dependency_sensitive_indices", ())
    expected_carry = set(carry_forward_entry_ids)
    audited_carry = {
        entry.get("entry_id")
        for entry in ledger.get("synthesis_audit", ())
        if entry.get("classification") == "carry-forward-dependency"
    }
    classification_by_entry = {
        entry.get("entry_id"): entry for entry in classifications
    }
    edges = ledger.get("graph", {}).get("edges", ())
    edge_counts = Counter(edge.get("edge_id") for edge in edges)
    edge_by_id = {edge.get("edge_id"): edge for edge in edges}
    referenced_edges = [
        (entry, edge_id)
        for entry in classifications
        for edge_id in entry.get("edge_ids", ())
    ]
    referenced_edge_ids = {edge_id for _, edge_id in referenced_edges}
    expected_protocol = {
        component.get("protocol_component_id"): component
        for component in protocol_components
        if component.get("owner_index") in ordinary_indexes
    }
    protocol_edges = [
        edge for edge in edges if edge.get("kind") == "protocol-interface"
    ]
    protocol_edge_counts = Counter(
        edge.get("protocol_component_id") for edge in protocol_edges
    )
    protocol_edge_by_component = {
        edge.get("protocol_component_id"): edge for edge in protocol_edges
    }
    expected_waylib = {
        entry.get("ordered_index"): entry
        for entry in ordinary_candidates
        if entry.get("gitlink_before") != entry.get("gitlink_after")
    }
    waylib_edges = [
        edge for edge in edges if edge.get("kind") == "waylib-capability"
    ]
    waylib_edge_counts = Counter(edge.get("owner_index") for edge in waylib_edges)
    waylib_edge_by_owner = {edge.get("owner_index"): edge for edge in waylib_edges}
    report = {
        "ordinary_missing": len(expected - actual_identities),
        "ordinary_duplicate": sum(count - 1 for count in actual.values() if count > 1),
        "ordinary_unexpected": len(actual_identities - expected),
        "remediation_overlap": sum(
            entry.get("ordered_index") in remediation_indexes
            for entry in classifications
        ),
        "invalid_classification": sum(
            entry.get("classification")
            not in {"dependency-sensitive", "independent"}
            for entry in classifications
        ),
        "sensitive_index_mismatch": int(
            list(declared_sensitive) != sensitive_from_rows
        ),
        "carry_forward_missing": len(expected_carry - audited_carry),
        "carry_forward_unexpected": len(audited_carry - expected_carry),
        "carry_forward_reason_missing": sum(
            entry_id not in classification_by_entry
            or "carry-forward-lineage"
            not in classification_by_entry[entry_id].get("reason_kinds", ())
            for entry_id in expected_carry
        ),
        "missing_edge": sum(
            edge_id not in edge_by_id for _, edge_id in referenced_edges
        ),
        "duplicate_edge": sum(
            count - 1 for count in edge_counts.values() if count > 1
        ),
        "unreferenced_edge": len(
            [
                edge
                for edge_id, edge in edge_by_id.items()
                if edge_id not in referenced_edge_ids
                and not _is_remediation_only_edge(edge, remediation_indexes)
            ]
        ),
        "edge_owner_mismatch": sum(
            edge_id in edge_by_id
            and _edge_owner_mismatch(entry, edge_by_id[edge_id])
            for entry, edge_id in referenced_edges
        ),
        "reason_edge_mismatch": sum(
            reason
            not in {
                edge_by_id[edge_id].get("kind")
                for edge_id in entry.get("edge_ids", ())
                if edge_id in edge_by_id
            }
            for entry in classifications
            for reason in entry.get("reason_kinds", ())
        ),
        "member_timeline_mismatch": sum(
            _member_timeline_invalid(edge) for edge in edges
        ),
        "protocol_missing": len(
            set(expected_protocol) - set(protocol_edge_by_component)
        ),
        "protocol_duplicate": sum(
            count - 1 for count in protocol_edge_counts.values() if count > 1
        ),
        "protocol_unexpected": len(
            set(protocol_edge_by_component) - set(expected_protocol)
        ),
        "protocol_snapshot_mismatch": sum(
            component_id in protocol_edge_by_component
            and any(
                protocol_edge_by_component[component_id].get(field)
                != component.get(field)
                for field in (
                    "owner_index",
                    "generated_signatures",
                    "result_blob",
                )
            )
            for component_id, component in expected_protocol.items()
        ),
        "gitlink_snapshot_mismatch": sum(
            identity in candidate_by_identity
            and any(
                entry.get(field) != candidate_by_identity[identity].get(field)
                for field in ("gitlink_before", "gitlink_after")
            )
            for entry in classifications
            for identity in [_identity(entry)]
        ),
        "waylib_edge_missing": len(
            set(expected_waylib) - set(waylib_edge_by_owner)
        ),
        "waylib_edge_duplicate": sum(
            count - 1 for count in waylib_edge_counts.values() if count > 1
        ),
        "waylib_edge_unexpected": len(
            set(waylib_edge_by_owner) - set(expected_waylib)
        ),
        "waylib_edge_mismatch": sum(
            index in waylib_edge_by_owner
            and any(
                waylib_edge_by_owner[index].get(field) != entry.get(field)
                for field in ("gitlink_before", "gitlink_after")
            )
            for index, entry in expected_waylib.items()
        ),
    }
    if any(report.values()):
        raise DependencySetError(report)
    return report
