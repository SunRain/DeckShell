"""Independent validation for the protocol transition ledger."""

from __future__ import annotations

import hashlib
from collections import Counter
from collections.abc import Callable, Collection, Mapping, Sequence
from typing import Any

from .protocol_signature import generated_signatures


class ProtocolLedgerError(ValueError):
    """Raised when protocol component coverage or ordering is invalid."""

    def __init__(self, report: Mapping[str, Any]) -> None:
        self.report = dict(report)
        summary = ", ".join(
            f"{key}={self.report[key]}"
            for key in (
                "missing",
                "duplicate",
                "unowned",
                "out_of_order",
                "ancestry_failure",
                "mutation",
                "fixed_mapping_failure",
                "convergence_failure",
            )
        )
        super().__init__(f"invalid protocol transition ledger: {summary}")


def _owner_regressions(
    components: Sequence[Mapping[str, Any]], ancestry_order: Sequence[str]
) -> int:
    order = {commit: index for index, commit in enumerate(ancestry_order)}
    last_owner_by_path: dict[str, int] = {}
    regressions = 0
    for component in sorted(
        components, key=lambda item: order.get(item.get("source_commit"), len(order))
    ):
        path = component.get("source_path")
        owner = component.get("owner_index")
        previous = last_owner_by_path.get(path)
        if isinstance(owner, int) and previous is not None and owner < previous:
            regressions += 1
        if isinstance(owner, int):
            last_owner_by_path[path] = owner
    return regressions


def _source_mutations(
    components: Sequence[Mapping[str, Any]],
    source_components: Sequence[Mapping[str, Any]],
    read_blob: Callable[[str], bytes] | None,
) -> int:
    expected = {
        component["protocol_component_id"]: component
        for component in source_components
    }
    mutations = 0
    for component in components:
        source = expected.get(component.get("protocol_component_id"))
        if source is None:
            mutations += 1
            continue
        source_changed = any(
            component.get(key) != value for key, value in source.items()
        )
        unexplained_result = (
            not component.get("local_overlay_components")
            and component.get("result_blob") != component.get("after_blob")
        )
        content_changed = read_blob is not None and _content_mutated(
            component, read_blob
        )
        if source_changed or unexplained_result or content_changed:
            mutations += 1
    return mutations


def _content_mutated(
    component: Mapping[str, Any], read_blob: Callable[[str], bytes]
) -> bool:
    for side in ("before", "after"):
        object_id = component.get(f"{side}_blob")
        if object_id is None:
            if component.get(f"generated_signatures_{side}"):
                return True
            continue
        try:
            content = read_blob(object_id)
        except Exception:
            return True
        if hashlib.sha256(content).hexdigest() != component.get(f"{side}_sha256"):
            return True
        if list(generated_signatures(content)) != component.get(
            f"generated_signatures_{side}"
        ):
            return True
    return False


def _fixed_mapping_failures(
    components: Sequence[Mapping[str, Any]],
    fixed_mappings: Mapping[str, Any],
    fixed_component_mappings: Sequence[Mapping[str, Any]],
) -> int:
    failures = sum(
        component.get("source_commit") in fixed_mappings
        and component.get("owner_index")
        != fixed_mappings[component.get("source_commit")]
        for component in components
    )
    component_owners: dict[tuple[str, str], int] = {}
    for mapping in fixed_component_mappings:
        identity = (mapping.get("source_commit"), mapping.get("source_path"))
        owner = mapping.get("owner_index")
        if not all(isinstance(item, str) and item for item in identity):
            failures += 1
            continue
        if not isinstance(owner, int) or identity in component_owners:
            failures += 1
            continue
        component_owners[identity] = owner
    failures += sum(
        (component.get("source_commit"), component.get("source_path"))
        in component_owners
        and component.get("owner_index")
        != component_owners[
            (component.get("source_commit"), component.get("source_path"))
        ]
        for component in components
    )
    return failures


def verify_protocol_ledger(
    ledger: Mapping[str, Any],
    source_components: Sequence[Mapping[str, Any]],
    ancestry_order: Sequence[str],
    valid_owner_indexes: Collection[int],
    *,
    is_ancestor: Callable[[str, str], bool] | None = None,
    read_blob: Callable[[str], bytes] | None = None,
) -> dict[str, int]:
    """Verify source-to-ledger coverage and compile-atomic ownership invariants."""

    components = ledger.get("components", ())
    expected_ids = {
        component["protocol_component_id"] for component in source_components
    }
    actual_ids = Counter(
        component.get("protocol_component_id")
        for component in components
    )
    frozen_commits = set(ancestry_order)
    source_commits = {component.get("source_commit") for component in source_components}
    fixed_mappings = ledger.get("fixed_mappings", {})
    fixed_component_mappings = ledger.get("fixed_component_mappings", ())
    convergence_owner = ledger.get("convergence_owner_index")
    broken_ancestry_edges = 0
    if is_ancestor is not None:
        broken_ancestry_edges = sum(
            not is_ancestor(older, newer)
            for older, newer in zip(ancestry_order, ancestry_order[1:])
        )
    report = {
        "missing": len(expected_ids - actual_ids.keys()),
        "duplicate": sum(count - 1 for count in actual_ids.values() if count > 1),
        "unowned": sum(
            component.get("owner_index") not in valid_owner_indexes
            for component in components
        ),
        "out_of_order": _owner_regressions(components, ancestry_order),
        "ancestry_failure": (
            len(source_commits - frozen_commits) + broken_ancestry_edges
        ),
        "mutation": _source_mutations(components, source_components, read_blob),
        "fixed_mapping_failure": _fixed_mapping_failures(
            components, fixed_mappings, fixed_component_mappings
        ),
        "convergence_failure": sum(
            not component.get("anchor_absorbed")
            and not component.get("consumer_paths")
            and component.get("owner_index") != convergence_owner
            for component in components
        ),
    }
    if any(report.values()):
        raise ProtocolLedgerError(report)
    return report
