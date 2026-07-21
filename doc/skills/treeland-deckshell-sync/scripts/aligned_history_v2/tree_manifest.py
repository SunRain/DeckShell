"""Canonical final-tree and approved-overlay verification helpers."""

from __future__ import annotations

from typing import Any

from .repository import GitRepository
from .tree_transition import parse_raw_transition


def build_product_manifest(
    repo: GitRepository, tree: str, excluded_rules: tuple[str, ...]
) -> dict[str, Any]:
    """Return mode, kind, object, and path outside approved overlay rules."""

    entries = [
        entry
        for entry in tree_entries(repo, tree)
        if not path_matches_any(entry["path"], excluded_rules)
    ]
    return {"entry_count": len(entries), "entries": entries}


def tree_entries(repo: GitRepository, tree: str) -> list[dict[str, str]]:
    """Read a recursive tree without losing path boundaries."""

    payload = repo.run("ls-tree", "-r", "-z", tree)
    result: list[dict[str, str]] = []
    seen: set[str] = set()
    for record in payload.rstrip(b"\0").split(b"\0") if payload else []:
        metadata, separator, path_bytes = record.partition(b"\t")
        if not separator:
            raise ValueError("invalid recursive tree record")
        mode, kind, object_id = metadata.decode("ascii").split(" ")
        path = path_bytes.decode("utf-8")
        if not path or path in seen:
            raise ValueError(f"invalid or duplicate tree path: {path!r}")
        seen.add(path)
        result.append(
            {"mode": mode, "kind": kind, "object_id": object_id, "path": path}
        )
    return result


def tree_diff_paths(repo: GitRepository, old_tree: str, new_tree: str) -> tuple[str, ...]:
    """Return canonical changed paths between two tree objects."""

    return tuple(
        change.path
        for change in parse_raw_transition(repo.raw_transition(old_tree, new_tree))
    )


def gitlink_object(repo: GitRepository, tree: str, path: str) -> str:
    """Return one exact gitlink object from a tree."""

    matches = [entry for entry in tree_entries(repo, tree) if entry["path"] == path]
    if len(matches) != 1 or matches[0]["mode"] != "160000":
        raise ValueError(f"tree does not contain one gitlink at {path}")
    return matches[0]["object_id"]


def path_matches_any(path: str, rules: tuple[str, ...]) -> bool:
    """Match an exact path or an explicitly directory-suffixed prefix."""

    return any(path == rule or (rule.endswith("/") and path.startswith(rule)) for rule in rules)
