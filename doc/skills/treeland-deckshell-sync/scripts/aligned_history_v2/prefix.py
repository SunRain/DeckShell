"""Seal the non-self-referential Treeland target prefix at index 303."""

from __future__ import annotations

from collections import Counter
from typing import Any

from .artifacts import with_canonical_hash
from .git_objects import SHA1_PATTERN


EXPECTED_CLASSIFICATIONS = Counter(
    {"other": 233, "mixed": 29, "dependency-only": 36}
)


def seal_treeland_prefix(
    manifest_entries: list[dict[str, Any]], target_commits: dict[int, str]
) -> dict[str, Any]:
    """Build the 298-entry source-to-v2 projection used by later generators."""

    treeland_entries = [
        entry for entry in manifest_entries if entry.get("message_schema") == "treeland"
    ]
    if len(treeland_entries) != 298:
        raise ValueError(f"Treeland prefix entry count mismatch: {len(treeland_entries)}")
    if max(int(entry["ordered_index"]) for entry in treeland_entries) != 303:
        raise ValueError("Treeland target prefix is not sealed at index 303")
    projected = [
        _project_entry(entry, target_commits[int(entry["ordered_index"])])
        for entry in treeland_entries
    ]
    classifications = Counter(item["classification"] for item in projected)
    if classifications != EXPECTED_CLASSIFICATIONS:
        raise ValueError(f"Treeland prefix classification drift: {classifications}")
    sources = [item["normalized_treeland_commit"] for item in projected]
    targets = [item["v2_target"] for item in projected]
    if len(set(sources)) != 298 or len(set(targets)) != 298:
        raise ValueError("Treeland prefix contains duplicate source or target")
    return with_canonical_hash(
        {
            "schema_version": 2,
            "workflow_mode": "commit-aligned-history-rewrite-v2",
            "status": "sealed-at-index-303",
            "sealed_at_ordered_index": 303,
            "entry_count": 298,
            "entries": projected,
        }
    )


def _project_entry(entry: dict[str, Any], target: str) -> dict[str, Any]:
    message = entry["message_inputs"]
    source = str(message["source_commit"])
    normalized = entry["source_objects"].get("normalized_treeland_commit")
    if source != normalized:
        raise ValueError(f"Treeland source identity drift at {entry['ordered_index']}")
    _require_sha(source, "Treeland source")
    _require_sha(target, "v2 target")
    subject = str(message["subject_body"]).splitlines()[0]
    if not subject:
        raise ValueError(f"Treeland subject is empty at {entry['ordered_index']}")
    return {
        "ordered_index": entry["ordered_index"],
        "normalized_treeland_commit": source,
        "v2_target": target,
        "subject": subject,
        "classification": message["classification"],
        "action": message["action"],
        "treeland_remote": "treeland",
        "treeland_remote_branch": "master",
        "treeland_tracking_ref": "refs/remotes/treeland/master",
        "treeland_commit": source,
    }


def _require_sha(value: str, label: str) -> None:
    if SHA1_PATTERN.fullmatch(value) is None:
        raise ValueError(f"{label} must be a full lowercase SHA-1")
