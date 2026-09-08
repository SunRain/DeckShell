"""Advisory protocol history candidate tracking."""

from __future__ import annotations

import difflib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from .git_ops import (
    canonical_json_sha256,
    resolve_commit,
    run_git,
    stable_unique,
)
from .protocol_context import (
    build_parent_protocol_context,
    normalized_diff as _normalized_diff,
)
from .schema import inventory_errors


PROTOCOL_SEARCH_ROOTS = (
    "xml",
    "dde",
    "public",
    "internal",
    "wine",
    "deprecated",
)


def _protocol_source_paths(item: Mapping[str, Any]) -> List[str]:
    paths = item.get("protocol_source_paths", [])
    return stable_unique(path for path in paths if isinstance(path, str))


def _metadata(repo: Path, commit: str) -> Dict[str, Any]:
    output = str(
        run_git(repo, "show", "-s", "--format=%at%x00%an%x00%ae%x00%s", commit)
    ).rstrip("\n")
    timestamp, author, email, subject = output.split("\0", 3)
    epoch = int(timestamp)
    return {
        "timestamp": epoch,
        "date": datetime.fromtimestamp(epoch, timezone.utc).isoformat(),
        "author": author,
        "email": email,
        "subject": subject,
    }


def _protocol_history(repo: Path, head: str) -> List[str]:
    return str(
        run_git(repo, "rev-list", "--reverse", head, "--", *PROTOCOL_SEARCH_ROOTS)
    ).split()


def _protocol_commit_paths(repo: Path, commit: str) -> List[str]:
    raw = run_git(
        repo,
        "diff-tree",
        "--root",
        "--no-commit-id",
        "--name-only",
        "--no-renames",
        "-r",
        "-z",
        commit,
        text=False,
    )
    roots = tuple(f"{root}/" for root in PROTOCOL_SEARCH_ROOTS)
    return stable_unique(
        field.decode("utf-8", errors="surrogateescape")
        for field in bytes(raw).split(b"\0")
        if field
        and field.decode("utf-8", errors="surrogateescape").startswith(roots)
        and field.decode("utf-8", errors="surrogateescape").lower().endswith(".xml")
    )


def _candidate(
    protocol_repo: Path,
    commit: str,
    source_diff: str,
    source_time: int,
) -> Dict[str, Any]:
    paths = _protocol_commit_paths(protocol_repo, commit)
    candidate_diff = _normalized_diff(protocol_repo, commit, paths)
    similarity = (
        round(difflib.SequenceMatcher(None, source_diff, candidate_diff).ratio(), 6)
        if source_diff and candidate_diff else None
    )
    metadata = _metadata(protocol_repo, commit)
    return {
        "commit": commit,
        "paths": paths,
        "similarity": similarity,
        "comparison_status": "comparable" if similarity is not None else "not-comparable",
        "time_distance_seconds": abs(metadata["timestamp"] - source_time),
        "author": metadata["author"],
        "email": metadata["email"],
        "date": metadata["date"],
        "subject": metadata["subject"],
    }


def _match_status(source_diff, candidates):
    if not source_diff:
        return "not-comparable"
    if not candidates:
        return "no-candidate"
    return "single-candidate" if len(candidates) == 1 else "ambiguous-candidates"


def _track_one(
    source_repo: Path,
    item: Mapping[str, Any],
    protocol_repo: Path,
    protocol_commits: Sequence[str],
    threshold: float,
    before_seconds: int,
    after_seconds: int,
    parent_context: Mapping[str, Mapping[str, Any]],
) -> Dict[str, Any]:
    source_sha = item["source_commit"]
    source_paths = _protocol_source_paths(item)
    target_context = parent_context.get(source_sha, {})
    target_paths = stable_unique(
        [*item.get("protocol_target_paths", []), *target_context.get("paths", [])]
    )
    source_diff = str(target_context.get("diff") or "")
    if not source_diff:
        source_diff = _normalized_diff(source_repo, source_sha, source_paths)
    source_time = _metadata(source_repo, source_sha)["timestamp"]
    candidates = []
    not_comparable = []
    for commit in protocol_commits:
        candidate_time = _metadata(protocol_repo, commit)["timestamp"]
        if not source_time - before_seconds <= candidate_time <= source_time + after_seconds:
            continue
        candidate = _candidate(
            protocol_repo, commit, source_diff, source_time
        )
        if candidate["similarity"] is None:
            not_comparable.append(candidate)
        elif candidate["similarity"] >= threshold:
            candidates.append(candidate)
    candidates.sort(
        key=lambda item: (
            -item["similarity"], item["time_distance_seconds"], item["commit"]
        )
    )
    return {
        "source_commit": source_sha,
        "source_paths": source_paths,
        "target_paths": target_paths,
        "trigger_sources": [
            name
            for name, active in (
                ("source-path", bool(source_paths)),
                ("parent-target", bool(target_paths)),
            )
            if active
        ],
        "match_status": _match_status(source_diff, candidates),
        "candidates": candidates,
        "not_comparable": not_comparable,
    }


def tracking_parameter_errors(
    threshold: float, days_before: int, days_after: int
) -> List[str]:
    """Validate advisory threshold and time-window inputs."""

    errors: List[str] = []
    if not 0.0 <= threshold <= 1.0:
        errors.append("similarity threshold must be between 0 and 1")
    if days_before < 0 or days_after < 0:
        errors.append("time window days must be non-negative")
    return errors


def protocol_tracking_required(
    inventory: Mapping[str, Any],
    parent_context: Optional[Mapping[str, Mapping[str, Any]]] = None,
) -> bool:
    """Return whether source or actual parent protocol paths require tracking."""

    context = parent_context or {}
    return any(
        item.get("protocol_source_paths")
        or item.get("protocol_target_paths")
        or context.get(item.get("source_commit"), {}).get("paths")
        for item in inventory.get("commits", [])
        if isinstance(item, dict)
    )


def _tracking_inputs(
    inventory: Mapping[str, Any],
    protocol_repo: Path,
    protocol_head: str,
    threshold: float,
    days_before: int,
    days_after: int,
    parent_context: Optional[Mapping[str, Mapping[str, Any]]],
) -> Tuple[str, List[str], Mapping[str, Mapping[str, Any]]]:
    errors = inventory_errors(inventory)
    if inventory.get("outcome") != "pass":
        errors.append("inventory outcome must be pass")
    errors.extend(tracking_parameter_errors(threshold, days_before, days_after))
    if errors:
        raise ValueError("; ".join(errors))
    frozen_head = resolve_commit(protocol_repo, protocol_head)
    history = _protocol_history(protocol_repo, frozen_head)
    context = parent_context or {}
    source_commits = {item.get("source_commit") for item in inventory["commits"]}
    unknown_context = sorted(set(context) - source_commits)
    if unknown_context:
        raise ValueError(
            "parent protocol context contains unknown source commits: "
            + ", ".join(unknown_context)
        )
    return frozen_head, history, context


def _tracked_protocol_entries(
    source_repo: Path,
    inventory: Mapping[str, Any],
    protocol_repo: Path,
    history: Sequence[str],
    threshold: float,
    days_before: int,
    days_after: int,
    context: Mapping[str, Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    tracked = [
        item
        for item in inventory["commits"]
        if item.get("protocol_source_paths")
        or item.get("protocol_target_paths")
        or context.get(item.get("source_commit"), {}).get("paths")
    ]
    return [
        _track_one(
            source_repo,
            item,
            protocol_repo,
            history,
            threshold,
            days_before * 86400,
            days_after * 86400,
            context,
        )
        for item in tracked
    ]


def _protocol_candidates_payload(
    inventory: Mapping[str, Any],
    frozen_head: str,
    parent_context: Optional[Mapping[str, Mapping[str, Any]]],
    threshold: float,
    days_before: int,
    days_after: int,
    entries: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    return {
        "schema_version": 2,
        "kind": "treeland-unified-protocol-candidates",
        "outcome": "pass",
        "advisory": True,
        "inventory_sha256": canonical_json_sha256(inventory),
        "protocol_head": frozen_head,
        "parent_context_used": bool(parent_context),
        "manifest_sha256": None,
        "search_paths": [f"{root}/**/*.xml" for root in PROTOCOL_SEARCH_ROOTS],
        "threshold": threshold,
        "window": {"days_before": days_before, "days_after": days_after},
        "entries": list(entries),
        "blocked_reasons": [],
    }


def track_protocol_candidates(
    source_repo: Path,
    inventory: Mapping[str, Any],
    protocol_repo: Path,
    protocol_head: str,
    threshold: float = 0.7,
    days_before: int = 30,
    days_after: int = 7,
    parent_context: Optional[Mapping[str, Mapping[str, Any]]] = None,
) -> Dict[str, Any]:
    """Return deterministic advisory candidates without asserting equivalence."""

    frozen_head, history, context = _tracking_inputs(
        inventory,
        protocol_repo,
        protocol_head,
        threshold,
        days_before,
        days_after,
        parent_context,
    )
    entries = _tracked_protocol_entries(
        source_repo,
        inventory,
        protocol_repo,
        history,
        threshold,
        days_before,
        days_after,
        context,
    )
    return _protocol_candidates_payload(
        inventory,
        frozen_head,
        parent_context,
        threshold,
        days_before,
        days_after,
        entries,
    )


__all__ = [
    "PROTOCOL_SEARCH_ROOTS",
    "build_parent_protocol_context",
    "protocol_tracking_required",
    "track_protocol_candidates",
    "tracking_parameter_errors",
]
