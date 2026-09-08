"""Filtered patch application and isolated-worktree commit primitives."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence, Set

from .git_ops import changed_paths
from .git_ops import parse_name_status_z, resolve_commit, run_git, stable_unique


def source_patch(repo: Path, source_sha: str, paths: Sequence[str], strip_prefix: Optional[str] = None) -> bytes:
    """Create a binary, no-rename patch for exact source paths."""

    if not paths:
        return b""
    output = run_git(
        repo,
        "diff",
        "--binary",
        "--full-index",
        "--no-ext-diff",
        "--no-renames",
        *([f"--relative={strip_prefix}"] if strip_prefix else []),
        f"{source_sha}^",
        source_sha,
        "--",
        *stable_unique(list(paths)),
        text=False,
    )
    return bytes(output)


def apply_index_patch(repo: Path, content: bytes, directory: Optional[str] = None) -> None:
    """Apply one patch directly to the index and matching worktree."""

    if not content:
        raise ValueError("cannot apply an empty patch")
    args = ["apply", "--index", "--whitespace=nowarn"]
    if directory:
        args.append(f"--directory={directory}")
    args.append("-")
    run_git(repo, *args, text=False, input_data=content)


def staged_paths(repo: Path) -> List[str]:
    """Return every old/new path currently staged."""

    raw = run_git(
        repo,
        "diff",
        "--cached",
        "--name-status",
        "--find-renames",
        "-z",
        text=False,
    )
    values: List[str] = []
    for change in parse_name_status_z(bytes(raw)):
        values.extend(changed_paths(change))
    return stable_unique(values)


def enforce_staged_paths(
    repo: Path,
    allowed: Set[str],
    required: Set[str],
    label: str,
) -> List[str]:
    """Reject staged expansion or missing required paths."""

    actual = staged_paths(repo)
    actual_set = set(actual)
    unexpected = sorted(actual_set - allowed)
    missing = sorted(required - actual_set)
    if unexpected:
        raise ValueError(f"{label} staged path expansion: {unexpected}")
    if missing:
        raise ValueError(f"{label} required staged paths missing: {missing}")
    return actual


def update_gitlink(repo: Path, path: str, child_sha: str) -> None:
    """Stage one gitlink without mutating the checked-out submodule directory."""

    checkout = repo / path
    if any(part.is_symlink() for part in (checkout, *checkout.parents)):
        raise ValueError("gitlink path must not traverse symlinks")
    # Git checkout creates empty submodule directories. Match that representation
    # for a first registration, without materializing any dependency contents.
    checkout.mkdir(parents=True, exist_ok=True)
    run_git(repo, "update-index", "--add", "--cacheinfo", f"160000,{child_sha},{path}")


def tree_entry(repo: Path, commit: str, path: str) -> Optional[Dict[str, str]]:
    """Read a single tree entry at a revision."""

    output = str(run_git(repo, "ls-tree", commit, "--", path)).strip()
    if not output:
        return None
    metadata, actual_path = output.split("\t", 1)
    mode, object_type, sha = metadata.split()
    return {"mode": mode, "type": object_type, "sha": sha, "path": actual_path}


def source_metadata(repo: Path, source_sha: str) -> Dict[str, str]:
    """Read author and message fields used for traceable target commits."""

    raw = str(
        run_git(
            repo,
            "show",
            "-s",
            "--format=%an%x00%ae%x00%aI%x00%s%x00%B",
            source_sha,
        )
    )
    author, email, date, subject, message = raw.split("\0", 4)
    return {
        "author": author,
        "email": email,
        "date": date,
        "subject": subject,
        "message": message.rstrip("\n"),
    }


def create_commit(
    repo: Path,
    source: Mapping[str, str],
    message: str,
    allow_empty: bool = False,
) -> str:
    """Create a target commit preserving source author identity and date."""

    args = [
        "commit",
        "--file=-",
        f"--author={source['author']} <{source['email']}>",
        f"--date={source['date']}",
    ]
    if allow_empty:
        args.append("--allow-empty")
    run_git(
        repo,
        *args,
        input_data=message,
        env={"GIT_COMMITTER_DATE": source["date"]},
    )
    return resolve_commit(repo, "HEAD")


def commit_diff(repo: Path, commit: str) -> bytes:
    """Return a full binary commit diff suitable for evidence hashing."""

    output = run_git(
        repo,
        "diff-tree",
        "--binary",
        "--full-index",
        "--patch",
        "--no-ext-diff",
        f"{commit}^",
        commit,
        text=False,
    )
    return bytes(output)
