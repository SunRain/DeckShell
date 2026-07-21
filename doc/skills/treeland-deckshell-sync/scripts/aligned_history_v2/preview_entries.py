"""Generate and verify individual rendered commits in an isolated preview."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .dry_run import audit_rendered_message
from .git_objects import git_object_id, parse_raw_commit, render_raw_commit
from .message import render_message
from .repository import GitRepository
from .tree_transition import parse_raw_transition


@dataclass(frozen=True)
class PreviewEntryResult:
    """Verified object and transition data for one rendered v2 commit."""

    commit: str
    tree: str
    parent: str
    payload: bytes
    message: bytes
    v1_delta_sha256: str
    v2_delta_sha256: str
    actual_changed_paths: tuple[str, ...]
    inherited_overlay_paths: tuple[str, ...]


def replay_rebuilt_anchor_entry(
    source_repo: GitRepository,
    preview_repo: GitRepository,
    entry: dict[str, Any],
    *,
    rewrite_base: str,
) -> PreviewEntryResult:
    """Independently render the corrected-v1 anchor on the frozen base."""

    if entry.get("tree_transition") != "replay-rebuilt-anchor":
        raise ValueError("anchor entry must use replay-rebuilt-anchor")
    raw = _validated_source_commit(source_repo, entry)
    if raw.parent != rewrite_base:
        raise ValueError("rebuilt anchor parent differs from rewrite base")
    transition = source_repo.raw_transition(rewrite_base, raw.tree)
    changed_paths = tuple(
        change.path for change in parse_raw_transition(transition)
    )
    _verify_v1_transition(entry, transition, changed_paths)
    transition_hash = hashlib.sha256(transition).hexdigest()
    result = _write_rendered_result(
        preview_repo,
        entry,
        raw=raw,
        tree=raw.tree,
        parent=rewrite_base,
        v1_delta_sha256=transition_hash,
        v2_delta_sha256=transition_hash,
        actual_paths=changed_paths,
        inherited_paths=(),
    )
    if result.commit == entry["expected_v1_commit"]:
        raise ValueError("v2 rebuilt anchor reused the corrected-v1 commit object")
    return result


def reuse_exact_entry(
    source_repo: GitRepository, entry: dict[str, Any]
) -> PreviewEntryResult:
    """Verify and return the unchanged shared-anchor commit object."""

    if entry.get("tree_transition") != "reuse-exact-commit-object":
        raise ValueError("passthrough entry must reuse the exact commit object")
    payload = source_repo.cat_file("commit", entry["expected_v1_commit"])
    raw = parse_raw_commit(payload)
    if git_object_id("commit", payload) != entry["expected_v1_commit"]:
        raise ValueError("passthrough commit object ID drift")
    if raw.parent != entry["expected_v1_parent"] or raw.tree != entry["expected_v1_tree"]:
        raise ValueError("passthrough commit identity drift")
    message_hash = hashlib.sha256(raw.message).hexdigest()
    if message_hash != entry["message_inputs"]["raw_message_sha256"]:
        raise ValueError("passthrough message hash drift")
    transition = source_repo.raw_transition(raw.parent, entry["expected_v1_commit"])
    changed_paths = tuple(change.path for change in parse_raw_transition(transition))
    _verify_v1_transition(entry, transition, changed_paths)
    transition_hash = hashlib.sha256(transition).hexdigest()
    return PreviewEntryResult(
        commit=entry["expected_v1_commit"],
        tree=raw.tree,
        parent=raw.parent,
        payload=payload,
        message=raw.message,
        v1_delta_sha256=transition_hash,
        v2_delta_sha256=transition_hash,
        actual_changed_paths=changed_paths,
        inherited_overlay_paths=(),
    )


def replay_rendered_entry(
    source_repo: GitRepository,
    preview_repo: GitRepository,
    entry: dict[str, Any],
    *,
    previous_v2_commit: str,
    previous_v2_tree: str,
    index_file: Path,
) -> PreviewEntryResult:
    """Replay one v1 transition on the current v2 parent and write its commit."""

    if entry.get("tree_transition") != "replay-v1-delta":
        raise ValueError("ordinary preview entry must replay the v1 delta")
    return _replay_delta(
        source_repo,
        preview_repo,
        entry,
        previous_v2_commit=previous_v2_commit,
        previous_v2_tree=previous_v2_tree,
        index_file=index_file,
    )


def replay_dependency_proven_entry(
    source_repo: GitRepository,
    preview_repo: GitRepository,
    entry: dict[str, Any],
    *,
    previous_v2_commit: str,
    previous_v2_tree: str,
    index_file: Path,
) -> PreviewEntryResult:
    """Replay one transition classified by the frozen dependency ledger."""

    if entry.get("tree_transition") != "replay-dependency-proven-v1-delta":
        raise ValueError("dependency-proven entry must use its explicit type")
    return _replay_delta(
        source_repo,
        preview_repo,
        entry,
        previous_v2_commit=previous_v2_commit,
        previous_v2_tree=previous_v2_tree,
        index_file=index_file,
    )


def replay_remediated_entry(
    source_repo: GitRepository,
    preview_repo: GitRepository,
    entry: dict[str, Any],
    *,
    previous_v2_commit: str,
    previous_v2_tree: str,
    index_file: Path,
) -> PreviewEntryResult:
    """Replay a corrected-v1 delta whose provenance is independently gated."""

    if entry.get("tree_transition") != "replay-remediated-v1-delta":
        raise ValueError("remediated preview entry must use its explicit type")
    return _replay_delta(
        source_repo,
        preview_repo,
        entry,
        previous_v2_commit=previous_v2_commit,
        previous_v2_tree=previous_v2_tree,
        index_file=index_file,
    )


def _replay_delta(
    source_repo: GitRepository,
    preview_repo: GitRepository,
    entry: dict[str, Any],
    *,
    previous_v2_commit: str,
    previous_v2_tree: str,
    index_file: Path,
) -> PreviewEntryResult:
    raw = _validated_source_commit(source_repo, entry)
    transition = source_repo.raw_transition(raw.parent, entry["expected_v1_commit"])
    changes = parse_raw_transition(transition)
    changed_paths = tuple(change.path for change in changes)
    _verify_v1_transition(entry, transition, changed_paths)
    inherited = _overlay_paths(
        preview_repo, entry["expected_v1_parent"], previous_v2_tree
    )
    overlap = sorted(set(changed_paths) & set(inherited))
    if overlap:
        raise ValueError(f"ordinary transition intersects inherited overlay: {overlap}")
    new_tree = preview_repo.replay_transition(previous_v2_tree, changes, index_file)
    v2_transition = preview_repo.raw_transition(previous_v2_tree, new_tree)
    if v2_transition != transition:
        raise ValueError(f"v2 transition drift at {entry['ordered_index']}")
    if _overlay_paths(preview_repo, entry["expected_v1_tree"], new_tree) != inherited:
        raise ValueError(f"inherited overlay drift at {entry['ordered_index']}")
    transition_hash = hashlib.sha256(transition).hexdigest()
    return _write_rendered_result(
        preview_repo,
        entry,
        raw=raw,
        tree=new_tree,
        parent=previous_v2_commit,
        v1_delta_sha256=transition_hash,
        v2_delta_sha256=transition_hash,
        actual_paths=changed_paths,
        inherited_paths=inherited,
    )


def render_regenerated_entry(
    source_repo: GitRepository,
    preview_repo: GitRepository,
    entry: dict[str, Any],
    *,
    previous_v2_commit: str,
    previous_v2_tree: str,
    files: dict[str, bytes | None],
    index_file: Path,
) -> PreviewEntryResult:
    """Apply one authorized regeneration overlay and write its v2 commit."""

    if entry.get("tree_transition") != "regenerate":
        raise ValueError("regenerated preview entry must use regenerate")
    if not files:
        raise ValueError("regeneration overlay must not be empty")
    raw = _validated_source_commit(source_repo, entry)
    v1_transition = source_repo.raw_transition(raw.parent, entry["expected_v1_commit"])
    v1_paths = tuple(change.path for change in parse_raw_transition(v1_transition))
    _verify_v1_transition(entry, v1_transition, v1_paths)
    inherited = _overlay_paths(
        preview_repo, entry["expected_v1_parent"], previous_v2_tree
    )
    _verify_authorized_paths(entry, tuple(files), inherited)
    new_tree = preview_repo.apply_files(previous_v2_tree, files, index_file)
    v2_transition = preview_repo.raw_transition(previous_v2_tree, new_tree)
    actual_paths = tuple(
        change.path for change in parse_raw_transition(v2_transition)
    )
    if not actual_paths:
        raise ValueError(f"regeneration produced no delta at {entry['ordered_index']}")
    _verify_authorized_paths(entry, actual_paths, inherited)
    resulting_overlay = set(
        _overlay_paths(preview_repo, entry["expected_v1_tree"], new_tree)
    )
    if not set(inherited).issubset(resulting_overlay):
        raise ValueError(f"regeneration dropped inherited overlay at {entry['ordered_index']}")
    return _write_rendered_result(
        preview_repo,
        entry,
        raw=raw,
        tree=new_tree,
        parent=previous_v2_commit,
        v1_delta_sha256=hashlib.sha256(v1_transition).hexdigest(),
        v2_delta_sha256=hashlib.sha256(v2_transition).hexdigest(),
        actual_paths=actual_paths,
        inherited_paths=inherited,
    )


def _write_rendered_result(
    repo: GitRepository,
    entry: dict[str, Any],
    *,
    raw: Any,
    tree: str,
    parent: str,
    v1_delta_sha256: str,
    v2_delta_sha256: str,
    actual_paths: tuple[str, ...],
    inherited_paths: tuple[str, ...],
) -> PreviewEntryResult:
    message = render_message(entry["message_inputs"])
    audit_rendered_message(entry["message_inputs"])
    rendered = render_raw_commit(raw, tree=tree, parent=parent, message=message)
    written = repo.write_object("commit", rendered.payload)
    if written != rendered.object_id:
        raise ValueError(f"commit object ID drift at {entry['ordered_index']}")
    return PreviewEntryResult(
        commit=written,
        tree=tree,
        parent=parent,
        payload=rendered.payload,
        message=message,
        v1_delta_sha256=v1_delta_sha256,
        v2_delta_sha256=v2_delta_sha256,
        actual_changed_paths=actual_paths,
        inherited_overlay_paths=inherited_paths,
    )


def _validated_source_commit(
    repo: GitRepository, entry: dict[str, Any]
):
    raw = parse_raw_commit(repo.cat_file("commit", entry["expected_v1_commit"]))
    if raw.parent != entry["expected_v1_parent"]:
        raise ValueError(f"v1 parent drift at {entry['ordered_index']}")
    if raw.tree != entry["expected_v1_tree"]:
        raise ValueError(f"v1 tree drift at {entry['ordered_index']}")
    return raw


def _verify_v1_transition(
    entry: dict[str, Any], transition: bytes, changed_paths: tuple[str, ...]
) -> None:
    actual_hash = hashlib.sha256(transition).hexdigest()
    if actual_hash != entry["expected_v1_delta_sha256"]:
        raise ValueError(f"v1 transition hash drift at {entry['ordered_index']}")
    if list(changed_paths) != entry["expected_v1_changed_paths"]:
        raise ValueError(f"v1 transition path drift at {entry['ordered_index']}")


def _overlay_paths(
    repo: GitRepository, expected_v1_treeish: str, v2_tree: str
) -> tuple[str, ...]:
    transition = repo.raw_transition(expected_v1_treeish, v2_tree)
    return tuple(change.path for change in parse_raw_transition(transition))


def _verify_authorized_paths(
    entry: dict[str, Any], paths: tuple[str, ...], inherited: tuple[str, ...]
) -> None:
    unauthorized = [
        path
        for path in paths
        if not any(
            path == rule or (str(rule).endswith("/") and path.startswith(str(rule)))
            for rule in entry["authorized_v2_delta_paths"]
        )
    ]
    if unauthorized:
        raise ValueError(
            f"regeneration path is not authorized at {entry['ordered_index']}: "
            f"{unauthorized}"
        )
    overlap = sorted(set(paths) & set(inherited))
    if overlap:
        raise ValueError(f"regeneration intersects inherited overlay: {overlap}")
