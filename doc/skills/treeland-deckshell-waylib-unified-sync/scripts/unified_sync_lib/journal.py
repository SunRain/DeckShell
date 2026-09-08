"""Atomic replay journal creation, validation, and checkpoints."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping

from .git_ops import atomic_write_json, read_json, sha256_bytes
from .schema import CHILD_ACTIONS, CHILD_CLASSIFICATIONS, LANE_ACTIONS, is_full_sha


JOURNAL_KIND = "treeland-unified-replay-journal"


def identity_digest(identity: Mapping[str, Any]) -> str:
    """Hash canonical replay identity data."""

    encoded = json.dumps(
        identity, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(encoded)


def _new_node(item: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "source_commit": item["source_commit"],
        "classification": item["classification"],
        "status": "pending",
        "wlroots": {"commit": None, "action": "not-applicable", "sequence": None},
        "nested_gitlink": None,
        "child": {"commit": None, "action": "not-applicable", "sequence": None},
        "parent": {"commit": None, "action": "not-applicable", "sequence": None},
        "gitlink": {"status": "unchanged", "from": None, "to": None},
        "artifacts": {"child": {}, "parent": {}, "wlroots": {}},
    }


def new_journal(
    identity: Mapping[str, Any],
    inventory_commits: List[Mapping[str, Any]],
) -> Dict[str, Any]:
    """Create an in-memory replay journal."""

    return {
        "schema_version": 2,
        "kind": JOURNAL_KIND,
        "identity": dict(identity),
        "identity_sha256": identity_digest(identity),
        "outcome": "running",
        "current_parent_head": identity["parent_base"],
        "current_child_head": identity["child_base"],
        "current_wlroots_head": identity["wlroots"]["base"] if identity.get("wlroots") else None,
        "next_sequence": 1,
        "nodes": {
            item["source_commit"]: _new_node(item) for item in inventory_commits
        },
        "events": [],
        "blocked": None,
    }


def _checkpoint_errors(
    node: Any, item: Mapping[str, Any], label: str
) -> List[str]:
    if not isinstance(node, dict):
        return [f"journal node must be an object: {label}"]
    errors: List[str] = []
    if node.get("source_commit") != item.get("source_commit"):
        errors.append(f"journal node source mismatch: {label}")
    if node.get("classification") != item.get("classification"):
        errors.append(f"journal node classification mismatch: {label}")
    lanes = {name: node.get(name) for name in ("wlroots", "child", "parent")}
    if not all(isinstance(lane, dict) for lane in lanes.values()):
        return errors + [f"journal node lane checkpoint is invalid: {label}"]
    sequences = []
    for lane_name, lane in lanes.items():
        commit, sequence = lane.get("commit"), lane.get("sequence")
        if commit is not None:
            if not is_full_sha(commit) or type(sequence) is not int or sequence < 1:
                errors.append(f"journal {lane_name} checkpoint is invalid: {label}")
            else:
                sequences.append(sequence)
            allowed = CHILD_ACTIONS if lane_name != "wlroots" else LANE_ACTIONS
            if lane.get("action") not in allowed:
                errors.append(f"journal {lane_name} action is invalid: {label}")
        elif sequence is not None:
            errors.append(f"journal {lane_name} has a sequence without commit: {label}")
    if sequences != sorted(set(sequences)):
        errors.append(f"journal wlroots/child checkpoint does not precede parent: {label}")
    errors.extend(_node_status_errors(node, item, lanes["child"], lanes["parent"], label))
    artifacts = node.get("artifacts")
    if not isinstance(artifacts, dict) or not all(isinstance(artifacts.get(lane), dict) for lane in lanes):
        errors.append(f"journal node artifacts are invalid: {label}")
    if not isinstance(node.get("gitlink"), dict):
        errors.append(f"journal node gitlink is invalid: {label}")
    return errors


def _node_status_errors(
    node: Mapping[str, Any],
    item: Mapping[str, Any],
    child: Mapping[str, Any],
    parent: Mapping[str, Any],
    label: str,
) -> List[str]:
    status = node.get("status")
    r = node.get("wlroots", {}).get("commit")
    c, p = child.get("commit"), parent.get("commit")
    has_r = bool(item.get("wlroots", {}).get("included"))
    has_c = item.get("classification") in CHILD_CLASSIFICATIONS
    if status == "pending":
        valid = not r and not c and not p
    elif status == "wlroots-complete":
        valid = has_r and bool(r) and not c and not p
    elif status == "child-complete":
        valid = has_c and bool(c) and not p and bool(r) == has_r
    elif status == "complete":
        valid = (not r and not c and not p) if item.get("classification") == "unowned-skip" else (
            bool(p) and bool(c) == has_c and bool(r) == has_r
        )
    else:
        valid = False
    return [] if valid else [f"journal node status/checkpoints disagree: {label}"]


def _event_errors(payload: Mapping[str, Any]) -> List[str]:
    events = payload.get("events")
    next_sequence = payload.get("next_sequence")
    if not isinstance(events, list):
        return ["replay journal events must be an array"]
    if not isinstance(next_sequence, int) or next_sequence < 1:
        return ["replay journal next_sequence is invalid"]
    sequences = [item.get("sequence") for item in events if isinstance(item, dict)]
    if len(sequences) != len(events) or sequences != list(range(1, next_sequence)):
        return ["replay journal event sequence is invalid"]
    return []


def _journal_errors(
    payload: Mapping[str, Any], inventory_commits: List[Mapping[str, Any]]
) -> List[str]:
    errors = _event_errors(payload)
    nodes = payload.get("nodes")
    expected_sources = [item.get("source_commit") for item in inventory_commits]
    if not isinstance(nodes, dict) or set(nodes) != set(expected_sources):
        return errors + ["replay journal nodes differ from the inventory"]
    pending_seen = False
    events = {event.get("sequence"): event for event in payload.get("events", []) if isinstance(event, dict)}
    for item in inventory_commits:
        source = item.get("source_commit")
        node = nodes.get(source)
        errors.extend(_checkpoint_errors(node, item, str(source)))
        if not isinstance(node, dict):
            continue
        if pending_seen and node.get("status") != "pending":
            errors.append("journal later source progressed before an earlier source completed")
        pending_seen = pending_seen or node.get("status") != "complete"
        for lane in ("wlroots", "child", "parent"):
            checkpoint = node.get(lane, {})
            if isinstance(checkpoint, dict) and checkpoint.get("commit"):
                event = events.get(checkpoint.get("sequence"), {})
                if any(event.get(k) != v for k, v in {"source_commit": source, "stage": lane, "status": "complete", "target_commit": checkpoint["commit"]}.items()):
                    errors.append(f"journal {lane} checkpoint differs from its event")
    for name in ("current_parent_head", "current_child_head"):
        if not is_full_sha(payload.get(name)):
            errors.append(f"replay journal {name} is invalid")
    rhead = payload.get("current_wlroots_head")
    if (payload.get("identity", {}).get("wlroots") and not is_full_sha(rhead)) or (not payload.get("identity", {}).get("wlroots") and rhead is not None):
        errors.append("replay journal wlroots HEAD is invalid")
    if payload.get("outcome") not in {"running", "blocked"}:
        errors.append("replay journal is not resumable")
    blocked = payload.get("blocked")
    if blocked is not None and not isinstance(blocked, dict):
        errors.append("replay journal blocked record is invalid")
    if payload.get("outcome") == "blocked" and not isinstance(blocked, dict):
        errors.append("blocked replay journal requires a blocker record")
    return errors


def load_journal(
    path: Path,
    identity: Mapping[str, Any],
    inventory_commits: List[Mapping[str, Any]],
) -> Dict[str, Any]:
    """Load a journal only when its immutable identity still matches."""

    payload = read_json(path)
    if payload.get("schema_version") != 2 or payload.get("kind") != JOURNAL_KIND:
        raise ValueError("unsupported replay journal schema")
    expected = identity_digest(identity)
    if payload.get("identity") != dict(identity) or payload.get("identity_sha256") != expected:
        raise ValueError("journal identity mismatch")
    errors = _journal_errors(payload, inventory_commits)
    if errors:
        raise ValueError("; ".join(errors))
    return payload


def add_event(
    journal: Dict[str, Any],
    source: str,
    stage: str,
    status: str,
    commit: Any = None,
    detail: Any = None,
) -> int:
    """Append one ordered journal event and return its sequence."""

    sequence = int(journal["next_sequence"])
    event = {
        "sequence": sequence,
        "source_commit": source,
        "stage": stage,
        "status": status,
    }
    if commit is not None:
        event["target_commit"] = commit
    if detail is not None:
        event["detail"] = detail
    journal["events"].append(event)
    journal["next_sequence"] = sequence + 1
    return sequence


def save_journal(path: Path, journal: Mapping[str, Any]) -> None:
    """Persist the complete replay journal atomically."""

    atomic_write_json(path, journal)
