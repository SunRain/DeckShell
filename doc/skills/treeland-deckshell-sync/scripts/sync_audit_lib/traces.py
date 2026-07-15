"""Target history trace parsing and idempotency classification."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .common import run_git


TREELAND_TRAILER = re.compile(r"^Treeland-Commit: ([0-9a-f]{40})$", re.MULTILINE)
LEGACY_TRAILER = re.compile(
    r"^\(cherry picked from(?: commit)? ([0-9a-f]{7,40})\)$", re.MULTILINE
)


def _resolve_inventory_sha(candidate: str, source_shas: list[str]) -> str | None:
    matches = [sha for sha in source_shas if sha.startswith(candidate)]
    return matches[0] if len(matches) == 1 else None


def _collect_mappings(
    repo: Path, target_commits: list[str], source_shas: list[str]
) -> tuple[list[dict[str, Any]], list[str]]:
    mappings: list[dict[str, Any]] = []
    blocked: list[str] = []
    for position, target_commit in enumerate(target_commits):
        body = str(run_git(repo, "show", "-s", "--format=%B", target_commit))
        new_candidates = list(dict.fromkeys(TREELAND_TRAILER.findall(body)))
        if new_candidates:
            relevant = [sha for sha in new_candidates if sha in source_shas]
            trace = "new"
        else:
            resolved = [
                _resolve_inventory_sha(candidate, source_shas)
                for candidate in LEGACY_TRAILER.findall(body)
            ]
            relevant = list(dict.fromkeys(sha for sha in resolved if sha))
            trace = "legacy"

        if len(relevant) > 1:
            blocked.append(
                "target commit maps multiple inventory sources: "
                f"{target_commit}: {','.join(relevant)}"
            )
        elif len(relevant) == 1:
            mappings.append(
                {
                    "source_commit": relevant[0],
                    "target_commit": target_commit,
                    "trace": trace,
                    "target_position": position,
                }
            )
    return mappings, blocked


def _classify_state(
    mappings: list[dict[str, Any]], non_dependency: list[str], blocked: list[str]
) -> tuple[str, list[dict[str, Any]], list[str]]:
    by_source: dict[str, list[dict[str, Any]]] = {}
    for mapping in mappings:
        by_source.setdefault(mapping["source_commit"], []).append(mapping)
    for source, source_mappings in by_source.items():
        if len(source_mappings) > 1:
            blocked.append(f"source has duplicate target mappings: {source}")

    unique = [items[0] for items in by_source.values() if len(items) == 1]
    unique.sort(key=lambda item: item["target_position"])
    mapped = [item["source_commit"] for item in unique]
    expected_mapped = [sha for sha in non_dependency if sha in by_source]
    if mapped != expected_mapped:
        blocked.append("target mapping order differs from source inventory")

    if blocked:
        state = "blocked"
    elif not mapped:
        state = "new-sync"
    elif mapped == non_dependency:
        state = "already-synced"
    elif mapped == non_dependency[: len(mapped)]:
        state = "partial-prefix"
    else:
        state = "blocked"
        blocked.append("mapped sources are not a strict ordered prefix")
    return state, unique, mapped


def build_trace_audit(repo: Path, target: str, inventory: dict[str, Any]) -> dict[str, Any]:
    """Parse target history and classify the current range's idempotency state."""

    entries = inventory.get("commits", [])
    source_shas = [item["source_commit"] for item in entries]
    non_dependency = [
        item["source_commit"]
        for item in entries
        if item["classification"] not in {"dependency-only", "blocked"}
    ]
    dependency_only = {
        item["source_commit"]
        for item in entries
        if item["classification"] == "dependency-only"
    }
    target_commits = str(run_git(repo, "rev-list", "--reverse", target)).split()
    mappings, blocked = _collect_mappings(repo, target_commits, source_shas)
    mapped_dependency = sorted(
        dependency_only.intersection(item["source_commit"] for item in mappings)
    )
    if mapped_dependency:
        blocked.append(
            "dependency-only sources have target mappings: "
            f"{','.join(mapped_dependency)}"
        )
    state, unique, mapped = _classify_state(mappings, non_dependency, blocked)

    positions = [item["target_position"] for item in unique]
    contiguous = bool(positions) and positions == list(
        range(positions[0], positions[-1] + 1)
    )
    first_parent = None
    if unique:
        parent_line = str(
            run_git(repo, "rev-list", "--parents", "-n", "1", unique[0]["target_commit"])
        ).strip()
        fields = parent_line.split()
        first_parent = fields[1] if len(fields) == 2 else None
    mapped_set = set(mapped)
    return {
        "schema_version": 1,
        "target": str(run_git(repo, "rev-parse", f"{target}^{{commit}}")).strip(),
        "state": state,
        "mappings": unique,
        "mapped_source_commits": mapped,
        "unmapped_source_commits": [sha for sha in non_dependency if sha not in mapped_set],
        "mapped_segment_contiguous": contiguous,
        "first_mapped_parent": first_parent,
        "last_mapped_commit": unique[-1]["target_commit"] if unique else None,
        "blocked_reasons": list(dict.fromkeys(blocked)),
        "outcome": "blocked" if state == "blocked" else "pass",
    }
