"""Parent-side protocol path and diff context construction."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

from .git_ops import commit_changes, run_git, stable_unique
from .schema import is_full_sha


PROTOCOL_TARGET_PREFIX = "protocols/compositor/"


def _changed_paths(repo: Path, commit: str) -> List[str]:
    paths: List[str] = []
    for change in commit_changes(repo, commit):
        candidates = (
            (change.new_path,)
            if change.status.startswith("C")
            else (change.old_path, change.new_path)
        )
        paths.extend(path for path in candidates if path)
    return stable_unique(paths)


def _is_protocol_target(path: str) -> bool:
    return path.startswith(PROTOCOL_TARGET_PREFIX) and path.lower().endswith(".xml")


def normalized_diff(repo: Path, commit: str, paths: Sequence[str]) -> str:
    """Return a stable, content-only diff for the selected XML paths."""

    if not paths:
        return ""
    lineage = str(run_git(repo, "rev-list", "--parents", "-n", "1", commit)).split()
    common = ["--no-color", "--no-ext-diff", "--unified=0", "--find-renames"]
    if len(lineage) > 1:
        output = str(run_git(repo, "diff", *common, lineage[1], commit, "--", *paths))
    else:
        output = str(
            run_git(
                repo,
                "diff-tree",
                "--root",
                "--patch",
                "--no-commit-id",
                "-r",
                *common,
                commit,
                "--",
                *paths,
            )
        )
    lines = []
    for line in output.splitlines():
        if not line.startswith(("+", "-")) or line.startswith(("+++", "---")):
            continue
        lines.append(line[0] + " ".join(line[1:].split()))
    return "\n".join(lines)


def build_parent_protocol_context(
    parent_repo: Path, manifest: Mapping[str, Any]
) -> Dict[str, Dict[str, Any]]:
    """Return actual parent protocol paths and diffs keyed by source commit."""

    if manifest.get("schema_version") != 2 or manifest.get("kind") != "treeland-unified-sync-manifest":
        raise ValueError("manifest kind is invalid for protocol tracking")
    if manifest.get("outcome") != "pass":
        raise ValueError("manifest outcome must be pass for protocol tracking")
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        raise ValueError("manifest entries must be an array for protocol tracking")
    context: Dict[str, Dict[str, Any]] = {}
    for item in entries:
        if not isinstance(item, dict) or not is_full_sha(item.get("source_commit")):
            raise ValueError("manifest protocol source commit must be a full SHA")
        source_sha = item["source_commit"]
        if source_sha in context:
            raise ValueError(f"duplicate manifest protocol source commit: {source_sha}")
        parent = item.get("parent")
        parent_sha = parent.get("commit") if isinstance(parent, dict) else None
        paths = (
            [path for path in _changed_paths(parent_repo, parent_sha) if _is_protocol_target(path)]
            if is_full_sha(parent_sha)
            else []
        )
        context[source_sha] = {
            "paths": paths,
            "diff": normalized_diff(parent_repo, parent_sha, paths) if paths else "",
        }
    return context


__all__ = [
    "PROTOCOL_TARGET_PREFIX",
    "build_parent_protocol_context",
    "normalized_diff",
]
