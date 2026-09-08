"""Replay manifest and lane evidence assembly."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Tuple

from .replay_types import ReplayRequest


def build_manifest(
    request: ReplayRequest, journal: Mapping[str, Any]
) -> Dict[str, Any]:
    """Build the cross-repository mapping without commit-message hash cycles."""

    entries = []
    for item in request.inventory["commits"]:
        node = journal["nodes"][item["source_commit"]]
        entries.append(
            {
                "source_commit": item["source_commit"],
                "classification": item["classification"],
                "child": node["child"],
                "parent": node["parent"],
                "gitlink": node["gitlink"],
                "wlroots": node["wlroots"],
                "nested_gitlink": node["nested_gitlink"],
            }
        )
    return {
        "schema_version": 2,
        "kind": "treeland-unified-sync-manifest",
        "outcome": "pass",
        "identity": journal["identity"],
        "final_parent_head": journal["current_parent_head"],
        "final_child_head": journal["current_child_head"],
        "final_wlroots_head": journal["current_wlroots_head"],
        "entries": entries,
    }


def _child_evidence_entry(
    source_sha: str,
    item: Mapping[str, Any],
    node: Mapping[str, Any],
    lane: str = "child",
) -> Dict[str, Any]:
    artifacts = dict(node["artifacts"][lane])
    target = node[lane]
    result = {
        "source_commit": source_sha,
        "target_commit": target["commit"],
        "classification": item["classification"],
        "action": target["action"],
        "content_action": target.get("content_action", target["action"]),
        "structural_paths": target.get("structural_paths", []),
        "nested_gitlink": node["nested_gitlink"] if lane == "child" else None,
        "drop_paths": item["waylib_shared" if lane == "child" else "wlroots"]["drop_paths"],
        "adaptation_notes": target["adaptation_notes"],
        "adaptation_paths": target.get("adaptation_paths", []),
        "artifacts": artifacts,
    }
    if "equivalence_proof" in artifacts:
        result["equivalence_proof"] = artifacts.pop("equivalence_proof")
    return result


def build_wlroots_evidence(request: ReplayRequest, journal: Mapping[str, Any]) -> Dict[str, Any]:
    """为每个实际 R 来源节点生成独立的内容证据，不制造 wrapper-only 的 R 提交。"""

    return {"schema_version": 2, "kind": "treeland-unified-wlroots-evidence", "entries": [
        _child_evidence_entry(item["source_commit"], item, journal["nodes"][item["source_commit"]], "wlroots")
        for item in request.inventory["commits"] if item["wlroots"]["included"]
    ]}


def _parent_evidence_entry(
    source_sha: str,
    item: Mapping[str, Any],
    node: Mapping[str, Any],
) -> Dict[str, Any]:
    artifacts = dict(node["artifacts"]["parent"])
    result = {
        "source_commit": source_sha,
        "target_commit": node["parent"]["commit"],
        "classification": item["classification"],
        "action": node["parent"]["action"],
        "drop_paths": item["deckshell"]["drop_paths"],
        "target_paths": item["deckshell"]["target_paths"],
        "adaptation_notes": node["parent"]["adaptation_notes"],
        "adaptation_paths": node["parent"].get("adaptation_paths", []),
        "gitlink": node["gitlink"],
        "child_commit": node["child"]["commit"],
        "artifacts": artifacts,
    }
    if "equivalence_proof" in artifacts:
        result["equivalence_proof"] = artifacts.pop("equivalence_proof")
    return result


def build_evidence_documents(
    request: ReplayRequest, journal: Mapping[str, Any]
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Build child and parent evidence documents from durable checkpoints."""

    child_entries: List[Dict[str, Any]] = []
    parent_entries: List[Dict[str, Any]] = []
    by_source = {item["source_commit"]: item for item in request.inventory["commits"]}
    for source_sha, node in journal["nodes"].items():
        item = by_source[source_sha]
        if node["child"]["commit"]:
            child_entries.append(_child_evidence_entry(source_sha, item, node))
        if node["parent"]["commit"]:
            parent_entries.append(_parent_evidence_entry(source_sha, item, node))
    return (
        {
            "schema_version": 2,
            "kind": "treeland-unified-waylib-evidence",
            "entries": child_entries,
        },
        {
            "schema_version": 2,
            "kind": "treeland-unified-parent-evidence",
            "entries": parent_entries,
        },
    )
