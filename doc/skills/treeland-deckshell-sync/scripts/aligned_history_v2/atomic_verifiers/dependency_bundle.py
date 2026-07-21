"""Independent validation for dependency bundle ownership ledgers."""

from __future__ import annotations

from collections import Counter
from collections import defaultdict
from collections.abc import Callable, Collection, Mapping, Sequence
from typing import Any


class DependencyBundleLedgerError(ValueError):
    """Raised when a dependency component lacks one atomic bundle owner."""

    def __init__(self, report: Mapping[str, int]) -> None:
        self.report = dict(report)
        summary = ", ".join(
            f"{key}={value}" for key, value in self.report.items() if value
        )
        super().__init__(f"invalid dependency bundle ledger: {summary}")


def _component_payload_mismatch(
    actual: Mapping[str, Any], expected: Mapping[str, Any]
) -> bool:
    return any(
        actual.get(field) != expected.get(field)
        for field in ("kind", "target_owner_index", "source_indices", "payload")
    )


def _forbidden_early_mismatch(bundle: Mapping[str, Any]) -> bool:
    owner = bundle.get("owner_index")
    expected = [
        {"component_id": component_id, "before_owner_index": owner}
        for component_id in sorted(bundle.get("component_ids", ()))
    ]
    actual = sorted(
        bundle.get("forbidden_early_members", ()),
        key=lambda member: member.get("component_id", ""),
    )
    return actual != expected


def _precondition_mismatch(
    bundle: Mapping[str, Any], components_by_id: Mapping[str, Mapping[str, Any]]
) -> bool:
    by_kind: dict[str, list[str]] = defaultdict(list)
    for component_id in bundle.get("component_ids", ()):
        component = components_by_id.get(component_id)
        if component is not None:
            by_kind[component.get("kind")].append(component_id)
    expected = [
        {"kind": kind, "component_ids": sorted(component_ids)}
        for kind, component_ids in sorted(by_kind.items())
    ]
    return bundle.get("preconditions") != expected


def verify_dependency_bundle_ledger(
    ledger: Mapping[str, Any],
    *,
    expected_components: Sequence[Mapping[str, Any]],
    valid_owner_indexes: Collection[int],
    is_ancestor: Callable[[int, int], bool] | None = None,
) -> dict[str, int]:
    """Verify component coverage, ownership, ordering, and capability snapshots."""

    components = ledger.get("components", ())
    bundles = ledger.get("bundles", ())
    expected_by_id = {
        component["component_id"]: component for component in expected_components
    }
    actual_counts = Counter(component.get("component_id") for component in components)
    actual_by_id = {component.get("component_id"): component for component in components}
    bundles_by_id = {bundle.get("bundle_id"): bundle for bundle in bundles}
    bundle_counts = Counter(bundle.get("bundle_id") for bundle in bundles)
    component_memberships = Counter(
        component_id
        for bundle in bundles
        for component_id in bundle.get("component_ids", ())
    )
    report = {
        "missing": len(set(expected_by_id) - set(actual_by_id)),
        "duplicate": sum(count - 1 for count in actual_counts.values() if count > 1),
        "unexpected": len(set(actual_by_id) - set(expected_by_id)),
        "unowned": sum(
            component.get("owner_index") not in valid_owner_indexes
            for component in components
        ),
        "owner_mismatch": sum(
            component_id in actual_by_id
            and actual_by_id[component_id].get("owner_index")
            != expected.get("owner_index")
            for component_id, expected in expected_by_id.items()
        ),
        "member_mismatch": sum(
            component_id in actual_by_id
            and _component_payload_mismatch(actual_by_id[component_id], expected)
            and expected.get("kind") != "waylib-capability"
            for component_id, expected in expected_by_id.items()
        ),
        "waylib_mismatch": sum(
            component_id in actual_by_id
            and _component_payload_mismatch(actual_by_id[component_id], expected)
            and expected.get("kind") == "waylib-capability"
            for component_id, expected in expected_by_id.items()
        ),
        "bundle_missing": sum(
            component.get("bundle_id") not in bundles_by_id for component in components
        ),
        "bundle_membership_mismatch": sum(
            component_memberships.get(component.get("component_id"), 0) != 1
            or component.get("component_id")
            not in bundles_by_id.get(component.get("bundle_id"), {}).get(
                "component_ids", ()
            )
            for component in components
        ),
        "bundle_owner_mismatch": sum(
            component.get("bundle_id") in bundles_by_id
            and bundles_by_id[component["bundle_id"]].get("owner_index")
            != component.get("owner_index")
            for component in components
        ),
        "duplicate_bundle": sum(
            count - 1 for count in bundle_counts.values() if count > 1
        ),
        "out_of_order": sum(
            list(component.get("source_indices", ()))
            != sorted(set(component.get("source_indices", ())))
            for component in components
        ) + sum(
            list(bundle.get("proof_nodes", ()))
            != sorted(set(bundle.get("proof_nodes", ())))
            for bundle in bundles
        ),
        "forbidden_early_mismatch": sum(
            _forbidden_early_mismatch(bundle) for bundle in bundles
        ),
        "precondition_mismatch": sum(
            _precondition_mismatch(bundle, actual_by_id) for bundle in bundles
        ),
        "ancestry_failure": 0
        if is_ancestor is None
        else sum(
            not is_ancestor(older, newer)
            for component in components
            for older, newer in zip(
                component.get("source_indices", ()),
                component.get("source_indices", ())[1:],
            )
        ),
    }
    if any(report.values()):
        raise DependencyBundleLedgerError(report)
    return report
