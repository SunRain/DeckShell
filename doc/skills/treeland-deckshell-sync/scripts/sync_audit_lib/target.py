"""Canonical target commit change inspection."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import Change, parse_name_status_z, run_git


def canonicalize_changes(changes: list[Change]) -> dict[str, Any]:
    """Canonicalize status records while retaining both rename/copy sides."""

    canonical = []
    all_paths = []
    for change in changes:
        all_paths.extend(
            path for path in (change.old_path, change.new_path) if path is not None
        )
        path = change.old_path if change.status.startswith("D") else change.new_path
        if path:
            canonical.append(
                {
                    "status": change.status,
                    "path": path,
                    "old_path": change.old_path,
                    "new_path": change.new_path,
                }
            )
    return {
        "all_paths": list(dict.fromkeys(all_paths)),
        "canonical_changes": canonical,
        "statuses": {item["path"]: item["status"] for item in canonical},
    }


def inspect_target_commit(repo: Path, target: str) -> dict[str, Any]:
    """Return parent, all touched paths, and canonical status-bearing changes."""

    parent_line = str(run_git(repo, "rev-list", "--parents", "-n", "1", target)).strip()
    parts = parent_line.split()
    if len(parts) != 2:
        return {
            "single_parent": False,
            "parent": "",
            "all_paths": [],
            "canonical_changes": [],
            "statuses": {},
        }
    raw = run_git(
        repo,
        "diff-tree",
        "--no-commit-id",
        "--name-status",
        "-r",
        "--find-renames",
        "--find-copies",
        "-z",
        f"{target}^",
        target,
        text=False,
    )
    changes = parse_name_status_z(bytes(raw))
    normalized = canonicalize_changes(changes)
    return {
        "single_parent": True,
        "parent": parts[1],
        **normalized,
    }
