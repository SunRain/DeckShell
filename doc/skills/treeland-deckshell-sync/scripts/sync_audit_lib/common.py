"""Shared policy and Git parsing primitives for sync audits."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


Policy = dict[str, Any]


@dataclass(frozen=True)
class PathDecision:
    """Describe how one source path is handled by the sync policy."""

    source: str
    category: str
    target: str | None
    policy_key: str | None = None


@dataclass(frozen=True)
class Change:
    """Represent one Git name-status record, including rename/copy sides."""

    status: str
    old_path: str | None
    new_path: str | None


def load_policy(path: Path) -> Policy:
    """Load the first JSON code block from the path-policy Markdown file."""

    content = path.read_text(encoding="utf-8")
    marker = "```json\n"
    start = content.find(marker)
    if start < 0:
        raise ValueError(f"路径策略缺少 JSON 代码块: {path}")
    start += len(marker)
    end = content.find("\n```", start)
    if end < 0:
        raise ValueError(f"路径策略 JSON 代码块未闭合: {path}")
    policy = json.loads(content[start:end])
    if policy.get("version") != 1:
        raise ValueError(f"不支持的路径策略版本: {policy.get('version')}")
    return policy


def match_path(path: str, directories: Any, files: Any) -> tuple[str, str] | None:
    """Match a path against exact files or directory-prefix mappings."""

    if isinstance(files, dict) and path in files:
        return path, str(files[path])
    if not isinstance(directories, dict):
        return None
    for source_root, target_root in directories.items():
        if path == source_root:
            return str(source_root), str(target_root)
        prefix = f"{source_root}/"
        if path.startswith(prefix):
            return str(source_root), f"{target_root}/{path[len(prefix):]}"
    return None


def classify_path(path: str, policy: Policy, approved_review: set[str]) -> PathDecision:
    """Classify a source path and calculate its deterministic target path."""

    for category, label in (("mapped", "mapped"), ("root_owned", "root-owned")):
        section = policy.get(category, {})
        match = match_path(path, section.get("directories", {}), section.get("files", {}))
        if match:
            policy_key, target = match
            return PathDecision(path, label, target, policy_key)

    excluded = policy.get("excluded", {})
    if path in set(excluded.get("files", [])):
        return PathDecision(path, "excluded", None, path)
    for source_root in excluded.get("directories", []):
        if path == source_root or path.startswith(f"{source_root}/"):
            return PathDecision(path, "excluded", None, str(source_root))

    review = policy.get("review_only", {})
    match = match_path(path, review.get("directories", {}), review.get("files", {}))
    if match:
        policy_key, target = match
        category = "root-owned" if policy_key in approved_review else "review-only"
        return PathDecision(path, category, target, policy_key)
    return PathDecision(path, "unknown", None)


def parse_name_status_z(data: bytes) -> list[Change]:
    """Parse `git diff --name-status -z` output without path quoting loss."""

    fields = data.split(b"\0")
    if fields and fields[-1] == b"":
        fields.pop()
    changes: list[Change] = []
    index = 0
    while index < len(fields):
        status = fields[index].decode("ascii")
        index += 1
        if status.startswith(("R", "C")):
            if index + 1 >= len(fields):
                raise ValueError(f"不完整的 rename/copy 记录: {status}")
            old_path = fields[index].decode("utf-8", errors="surrogateescape")
            new_path = fields[index + 1].decode("utf-8", errors="surrogateescape")
            changes.append(Change(status, old_path, new_path))
            index += 2
            continue
        if index >= len(fields):
            raise ValueError(f"不完整的路径记录: {status}")
        path = fields[index].decode("utf-8", errors="surrogateescape")
        change = (
            Change(status, path, None)
            if status.startswith("D")
            else Change(status, None, path)
        )
        changes.append(change)
        index += 1
    return changes


def run_git(repo: Path, *args: str, text: bool = True) -> str | bytes:
    """Run Git in a repository and return stdout, raising on command failure."""

    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
    )
    return completed.stdout
