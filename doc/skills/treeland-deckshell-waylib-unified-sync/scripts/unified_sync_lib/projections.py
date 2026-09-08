"""Verify committed content against source or approved adaptation patches."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

from .artifacts import artifact_errors, read_verified_artifact
from .git_ops import GitError, run_git, stable_unique
from .patches import tree_entry


PatchOperation = Tuple[bytes, Optional[str]]


def _projected_tree(
    repo: Path, target_commit: str, operations: Sequence[PatchOperation]
) -> str:
    with tempfile.TemporaryDirectory(prefix="treeland-unified-projection-") as directory:
        environment = {"GIT_INDEX_FILE": str(Path(directory) / "index")}
        run_git(repo, "read-tree", f"{target_commit}^", env=environment)
        for patch, target_directory in operations:
            if not patch:
                continue
            arguments = ["apply", "--cached", "--whitespace=nowarn"]
            if target_directory:
                arguments.append(f"--directory={target_directory}")
            arguments.append("-")
            run_git(
                repo,
                *arguments,
                text=False,
                input_data=patch,
                env=environment,
            )
        return str(run_git(repo, "write-tree", env=environment)).strip()


def content_projection_errors(
    repo: Path,
    target_commit: str,
    target_paths: Sequence[str],
    operations: Sequence[PatchOperation],
    label: str,
) -> List[str]:
    """Compare target paths with an isolated-index application of frozen patches."""

    try:
        projected_tree = _projected_tree(repo, target_commit, operations)
    except (GitError, ValueError) as error:
        return [f"cannot recreate content projection for {label}: {error}"]
    errors: List[str] = []
    for path in stable_unique(target_paths):
        projected = tree_entry(repo, projected_tree, path)
        actual = tree_entry(repo, target_commit, path)
        projected_identity = (
            projected.get("mode"), projected.get("type"), projected.get("sha")
        ) if projected else None
        actual_identity = (
            actual.get("mode"), actual.get("type"), actual.get("sha")
        ) if actual else None
        if projected_identity != actual_identity:
            errors.append(
                f"content projection differs for {label}: {path}"
            )
    return errors


def adapted_content_projection_errors(repo, target, paths, record, root, label):
    """Bind approved target-relative patches to blobs; gitlink gates handle derived paths."""

    errors = artifact_errors(record, root, label + " adaptation_patch")
    if errors:
        return errors
    _, patch = read_verified_artifact(record, root, label + " adaptation_patch")
    return content_projection_errors(repo, target, paths, [(patch, None)], label + " adapted")
