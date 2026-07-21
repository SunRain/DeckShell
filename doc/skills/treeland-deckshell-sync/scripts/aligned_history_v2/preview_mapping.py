"""Build deterministic v1-to-v2 mapping records from verified preview entries."""

from __future__ import annotations

import hashlib
from typing import Any

from .artifacts import with_canonical_hash
from .git_objects import parse_raw_commit
from .preview_entries import PreviewEntryResult
from .repository import GitRepository


def build_mapping_record(
    source_repo: GitRepository,
    entry: dict[str, Any],
    result: PreviewEntryResult,
) -> dict[str, Any]:
    """Describe one rendered object without embedding preview-specific paths."""

    raw_v1 = parse_raw_commit(
        source_repo.cat_file("commit", entry["expected_v1_commit"])
    )
    if raw_v1.parent != entry["expected_v1_parent"]:
        raise ValueError(f"mapping v1 parent drift at {entry['ordered_index']}")
    if raw_v1.tree != entry["expected_v1_tree"]:
        raise ValueError(f"mapping v1 tree drift at {entry['ordered_index']}")
    message_hash = hashlib.sha256(result.message).hexdigest()
    return {
        "ordered_index": entry["ordered_index"],
        "target_kind": entry.get("target_kind"),
        "expected_v1_commit": entry["expected_v1_commit"],
        "new_commit": result.commit,
        "old_parent": raw_v1.parent,
        "new_parent": result.parent,
        "old_tree": raw_v1.tree,
        "new_tree": result.tree,
        "v1_delta_sha256": result.v1_delta_sha256,
        "v2_delta_sha256": result.v2_delta_sha256,
        "actual_v2_changed_paths": list(result.actual_changed_paths),
        "inherited_overlay_paths": list(result.inherited_overlay_paths),
        "old_message_sha256": hashlib.sha256(raw_v1.message).hexdigest(),
        "new_message_sha256": message_hash,
        "rendered_message_sha256": message_hash,
        "raw_commit_sha256": hashlib.sha256(result.payload).hexdigest(),
        "verification": "pass",
    }


def finalize_output_mapping(
    manifest: dict[str, Any],
    records: list[dict[str, Any]],
    *,
    treeland_prefix_sha256: str,
    tool_bundle_sha256: str,
    product_manifest_sha256: str,
    final_gitlink: str,
) -> dict[str, Any]:
    """Validate the complete linear result and freeze its output mapping."""

    entries = manifest.get("entries")
    if not isinstance(entries, list) or len(entries) != 330 or len(records) != 330:
        raise ValueError("output mapping requires exactly 330 entries")
    _verify_record_order(entries, records)
    _verify_parent_chain(manifest, records)
    ordinary, dependency, remediated = _verify_transition_contract(
        entries, records
    )
    _verify_object_freshness(entries, records)
    head = records[-1]
    return with_canonical_hash(
        {
            "schema_version": 2,
            "workflow_mode": "commit-aligned-history-rewrite-v2",
            "status": "object-preview-verified",
            "input_manifest_sha256": manifest["canonical_payload_sha256"],
            "treeland_prefix_sha256": treeland_prefix_sha256,
            "tool_bundle_sha256": tool_bundle_sha256,
            "product_manifest_sha256": product_manifest_sha256,
            "final_gitlink": final_gitlink,
            "entry_count": 330,
            "head": head["new_commit"],
            "head_tree": head["new_tree"],
            "counts": {
                "rebuilt_anchor": 1,
                "rendered": 330,
                "ordinary_transitions": ordinary,
                "dependency_proven_transitions": dependency,
                "remediated_transitions": remediated,
                "regeneration_transitions": 3,
            },
            "entries": records,
        }
    )


def _verify_record_order(
    entries: list[dict[str, Any]], records: list[dict[str, Any]]
) -> None:
    for index, (entry, record) in enumerate(zip(entries, records, strict=True), 1):
        if entry["ordered_index"] != index or record["ordered_index"] != index:
            raise ValueError(f"output mapping order drift at {index}")
        if record["expected_v1_commit"] != entry["expected_v1_commit"]:
            raise ValueError(f"output mapping v1 identity drift at {index}")
        if record.get("verification") != "pass":
            raise ValueError(f"output mapping verification missing at {index}")
        for key in ("actual_v2_changed_paths", "inherited_overlay_paths"):
            paths = record[key]
            if len(paths) != len(set(paths)):
                raise ValueError(f"output mapping duplicate {key} at {index}")


def _verify_parent_chain(
    manifest: dict[str, Any], records: list[dict[str, Any]]
) -> None:
    previous = manifest["frozen_inputs"]["rewrite_base"]
    for index, record in enumerate(records, 1):
        if record["new_parent"] != previous:
            raise ValueError(f"output mapping parent drift at {index}")
        previous = record["new_commit"]


def _verify_transition_contract(
    entries: list[dict[str, Any]], records: list[dict[str, Any]]
) -> tuple[int, int, int]:
    regenerate_indices = []
    rebuilt = 0
    ordinary = 0
    dependency = 0
    remediated = 0
    for entry, record in zip(entries, records, strict=True):
        transition = entry["tree_transition"]
        if transition == "regenerate":
            regenerate_indices.append(entry["ordered_index"])
        elif transition in {
            "replay-rebuilt-anchor",
            "replay-v1-delta",
            "replay-dependency-proven-v1-delta",
            "replay-remediated-v1-delta",
        }:
            if record["v1_delta_sha256"] != record["v2_delta_sha256"]:
                raise ValueError(
                    f"replayed transition delta drift at {entry['ordered_index']}"
                )
            if transition == "replay-rebuilt-anchor":
                rebuilt += 1
            elif transition == "replay-v1-delta":
                ordinary += 1
            elif transition == "replay-dependency-proven-v1-delta":
                dependency += 1
            else:
                remediated += 1
        else:
            raise ValueError(f"unsupported transition: {transition}")
    if (
        rebuilt != 1
        or ordinary != 186
        or dependency != 129
        or remediated != 11
        or regenerate_indices != [316, 329, 330]
    ):
        raise ValueError("output mapping transition counts drift")
    return ordinary, dependency, remediated


def _verify_object_freshness(
    entries: list[dict[str, Any]], records: list[dict[str, Any]]
) -> None:
    old_rendered = {entry["expected_v1_commit"] for entry in entries}
    new_rendered = [record["new_commit"] for record in records]
    if len(set(new_rendered)) != 330:
        raise ValueError("rendered v2 commit IDs are not unique")
    reused = sorted(old_rendered & set(new_rendered))
    if reused:
        raise ValueError(f"rendered v2 history reuses v1 commit objects: {reused}")
