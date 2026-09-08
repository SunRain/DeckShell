"""Small, shell-free Git and artifact primitives."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


class GitError(RuntimeError):
    """Raised when a Git command cannot satisfy a workflow contract."""


@dataclass(frozen=True)
class Change:
    """One Git name-status record, including both rename/copy sides."""

    status: str
    old_path: Optional[str]
    new_path: Optional[str]


def changed_paths(change: Change) -> List[str]:
    """复制只改变目标侧；重命名的两侧都属于实际变更。"""

    sides = (change.new_path,) if change.status.startswith("C") else (change.old_path, change.new_path)
    return [path for path in sides if path is not None]


def run_git(
    repo: Path,
    *args: str,
    text: bool = True,
    input_data: Optional[Union[str, bytes]] = None,
    env: Optional[Mapping[str, str]] = None,
) -> Union[str, bytes]:
    """Run Git with an argument array and return stdout."""

    command = ["git", "-C", str(repo), *args]
    process_env = os.environ.copy()
    if env:
        process_env.update(env)
    completed = subprocess.run(
        command,
        check=False,
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
        env=process_env,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip() if text else completed.stderr.decode(errors="replace").strip()
        raise GitError(f"git command failed ({completed.returncode}): {' '.join(args)}: {stderr}")
    return completed.stdout


def git_succeeds(repo: Path, *args: str) -> bool:
    """Return whether a read-only Git command succeeds."""

    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return completed.returncode == 0


def resolve_commit(repo: Path, value: str) -> str:
    """Resolve one revision to a full commit SHA."""

    return str(run_git(repo, "rev-parse", f"{value}^{{commit}}")).strip()


def canonical_repo(repo: Path) -> Path:
    """Resolve and validate a Git worktree root."""

    requested = repo.expanduser().resolve()
    actual = Path(str(run_git(requested, "rev-parse", "--show-toplevel")).strip()).resolve()
    if requested != actual:
        raise ValueError(f"repo path is not its Git worktree root: {requested} != {actual}")
    return actual


def _resolved_git_path(repo: Path, value: str) -> Path:
    path = Path(value.strip())
    return path.resolve() if path.is_absolute() else (repo / path).resolve()


def is_linked_worktree(repo: Path) -> bool:
    """Return whether a worktree has separate per-worktree Git metadata."""

    root = canonical_repo(repo)
    git_dir = _resolved_git_path(
        root, str(run_git(root, "rev-parse", "--absolute-git-dir"))
    )
    common_dir = _resolved_git_path(
        root, str(run_git(root, "rev-parse", "--git-common-dir"))
    )
    return git_dir != common_dir


def common_git_dir(repo: Path) -> Path:
    """返回工作树所属对象库身份，不能用 checkout 路径代替它。"""

    return _resolved_git_path(repo, str(run_git(repo, "rev-parse", "--git-common-dir")))


def parse_name_status_z(data: bytes) -> List[Change]:
    """Parse NUL-separated `git diff --name-status` output."""

    fields = data.split(b"\0")
    if fields and fields[-1] == b"":
        fields.pop()
    changes: List[Change] = []
    index = 0
    while index < len(fields):
        status = fields[index].decode("ascii")
        index += 1
        if status.startswith(("R", "C")):
            if index + 1 >= len(fields):
                raise ValueError(f"incomplete rename/copy record: {status}")
            old_path = fields[index].decode("utf-8", errors="surrogateescape")
            new_path = fields[index + 1].decode("utf-8", errors="surrogateescape")
            changes.append(Change(status, old_path, new_path))
            index += 2
            continue
        if index >= len(fields):
            raise ValueError(f"incomplete path record: {status}")
        path = fields[index].decode("utf-8", errors="surrogateescape")
        changes.append(Change(status, path, None) if status.startswith("D") else Change(status, None, path))
        index += 1
    return changes


def commit_changes(repo: Path, commit: str) -> List[Change]:
    """Return canonical first-parent changes for a non-merge commit."""

    raw = run_git(
        repo,
        "diff-tree",
        "--no-commit-id",
        "--name-status",
        "-r",
        "--find-renames",
        "--find-copies",
        "--find-copies-harder",
        "-z",
        f"{commit}^",
        commit,
        text=False,
    )
    return parse_name_status_z(bytes(raw))


def stable_unique(values: Sequence[str]) -> List[str]:
    """Remove duplicates while preserving first-seen order."""

    return list(dict.fromkeys(values))


def sha256_bytes(content: bytes) -> str:
    """Return a lowercase SHA-256 digest."""

    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    """Hash a regular file."""

    return sha256_bytes(path.read_bytes())


def canonical_json_sha256(payload: Mapping[str, Any]) -> str:
    """Hash a JSON object using a stable, whitespace-free encoding."""

    encoded = json.dumps(
        payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(encoded)


def read_json(path: Path) -> Dict[str, Any]:
    """Read a JSON object from disk."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return payload


def atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
    """Write JSON through an atomic same-directory replacement."""

    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def atomic_write_bytes(path: Path, content: bytes) -> None:
    """Write bytes through an atomic same-directory replacement."""

    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise
