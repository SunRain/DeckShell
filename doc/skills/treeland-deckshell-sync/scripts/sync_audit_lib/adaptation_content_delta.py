"""Render deterministic post-image differences for adaptation paths."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from .common import run_git


@dataclass(frozen=True)
class TreeBlob:
    """Describe one path's blob state in a commit tree."""

    exists: bool
    mode: str = ""
    object_type: str = ""
    oid: str = ""
    data: bytes = b""


def source_post_path_for_target(entry: dict[str, Any], target_path: str) -> str:
    """Resolve the source post-image path, preferring a change's new side."""

    new_paths: set[str] = set()
    old_paths: set[str] = set()
    changes = entry.get("source_changes")
    if not isinstance(changes, list):
        raise ValueError(f"source_changes must be a list for {target_path}")
    for change in changes:
        if not isinstance(change, dict):
            continue
        for side_name, candidates in (("new", new_paths), ("old", old_paths)):
            side = change.get(side_name)
            if not isinstance(side, dict) or side.get("target") != target_path:
                continue
            source = side.get("source")
            if isinstance(source, str) and source:
                candidates.add(source)
    if len(new_paths) == 1:
        return new_paths.pop()
    if len(new_paths) > 1:
        raise ValueError(
            f"target path maps to multiple source post-images: {target_path}: "
            f"{sorted(new_paths)}"
        )
    if len(old_paths) == 1:
        return old_paths.pop()
    raise ValueError(
        f"target path must map to one source post-image: {target_path}: "
        f"{sorted(old_paths)}"
    )


def render_content_delta(
    repo: Path,
    source_commit: str,
    target_commit: str,
    source_path: str,
    target_path: str,
) -> list[str]:
    """Render one source/target commit-tree comparison as Markdown."""

    source = _read_tree_blob(repo, source_commit, source_path)
    target = _read_tree_blob(repo, target_commit, target_path)
    result = _comparison_result(source, target)
    section = [
        "#### 提交后文件状态差异（Treeland 与 DeckShell）",
        "",
        "> 本节比较 Treeland source commit 与 DeckShell rewritten target "
        "commit 提交后的文件状态，可能包含此前已经存在的 DeckShell 长期差异，"
        "不等同于本次提交的纯 adaptation delta。",
        "",
        f"- Treeland source path: `{source_path}`",
        f"- Treeland post-image: {_blob_summary(source)}",
        f"- DeckShell target path: `{target_path}`",
        f"- DeckShell post-image: {_blob_summary(target)}",
        f"- Comparison result: `{result}`",
    ]
    if result in {"identical", "both-absent"}:
        return [*section, "- Content diff: `none`", ""]
    diff = _content_diff(repo, source, target, source_path, target_path)
    if not diff:
        raise ValueError(
            f"post-image states differ but Git produced no diff: {source_path} -> {target_path}"
        )
    digest = hashlib.sha256(diff.encode("utf-8")).hexdigest()
    section.extend([f"- Content diff SHA-256: `{digest}`", ""])
    section.extend(_fenced_diff(diff))
    return section


def _read_tree_blob(repo: Path, commit: str, path: str) -> TreeBlob:
    _safe_relative_path(path)
    output = bytes(run_git(repo, "ls-tree", "-z", commit, "--", path, text=False))
    matches: list[tuple[str, str, str]] = []
    for record in filter(None, output.split(b"\0")):
        metadata, raw_path = record.split(b"\t", 1)
        decoded_path = raw_path.decode("utf-8", errors="surrogateescape")
        if decoded_path == path:
            mode, object_type, oid = metadata.decode("ascii").split()
            matches.append((mode, object_type, oid))
    if not matches:
        return TreeBlob(False)
    if len(matches) != 1:
        raise ValueError(f"tree path is not unique: {commit}: {path}")
    mode, object_type, oid = matches[0]
    if object_type != "blob":
        raise ValueError(
            f"unsupported post-image object type: {commit}: {path}: {object_type}"
        )
    data = bytes(run_git(repo, "cat-file", "blob", oid, text=False))
    return TreeBlob(True, mode, object_type, oid, data)


def _comparison_result(source: TreeBlob, target: TreeBlob) -> str:
    if not source.exists and not target.exists:
        return "both-absent"
    if source.exists and not target.exists:
        return "upstream-only"
    if not source.exists and target.exists:
        return "deckshell-only"
    same_content = source.oid == target.oid
    same_mode = source.mode == target.mode
    if same_content and same_mode:
        return "identical"
    if same_content:
        return "mode-only"
    if not same_mode:
        return "content-and-mode-different"
    return "content-different"


def _blob_summary(blob: TreeBlob) -> str:
    if not blob.exists:
        return "state `absent`"
    return (
        f"state `present`; type `{blob.object_type}`; mode `{blob.mode}`; "
        f"blob `{blob.oid}`; size `{len(blob.data)}` bytes"
    )


def _content_diff(
    repo: Path,
    source: TreeBlob,
    target: TreeBlob,
    source_path: str,
    target_path: str,
) -> str:
    with tempfile.TemporaryDirectory(prefix="treeland-adaptation-delta-") as raw_dir:
        root = Path(raw_dir)
        source_file = _materialize_blob(root, "upstream", source_path, source)
        target_file = _materialize_blob(root, "deckshell", target_path, target)
        command = _diff_command(repo, source_file, target_file)
        environment = {**os.environ, "LC_ALL": "C", "GIT_PAGER": "cat"}
        completed = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=environment,
        )
    if completed.returncode not in {0, 1}:
        error = completed.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"post-image Git diff failed: {error}")
    try:
        diff = completed.stdout.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(
            f"post-image diff is not UTF-8: {source_path} -> {target_path}"
        ) from error
    return _canonicalize_headers(diff, source, target, source_path, target_path)


def _diff_command(repo: Path, source: Path, target: Path) -> list[str]:
    return [
        "git",
        "-C",
        str(repo),
        "-c",
        "core.fileMode=true",
        "--no-pager",
        "diff",
        "--no-index",
        "--full-index",
        "--binary",
        "--no-color",
        "--no-ext-diff",
        "--no-textconv",
        "--no-renames",
        "--diff-algorithm=myers",
        "--no-indent-heuristic",
        "--unified=3",
        "--",
        str(source),
        str(target),
    ]


def _materialize_blob(root: Path, label: str, path: str, blob: TreeBlob) -> Path:
    if not blob.exists:
        return Path("/dev/null")
    destination = root / label / _safe_relative_path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if blob.mode == "120000":
        try:
            link_target = blob.data.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError(f"symlink target is not UTF-8: {path}") from error
        destination.symlink_to(link_target)
        return destination
    if blob.mode not in {"100644", "100755"}:
        raise ValueError(f"unsupported blob mode: {path}: {blob.mode}")
    destination.write_bytes(blob.data)
    destination.chmod(0o755 if blob.mode == "100755" else 0o644)
    return destination


def _safe_relative_path(path: str) -> Path:
    logical = PurePosixPath(path)
    if not path or logical.is_absolute() or any(part in {"", ".", ".."} for part in logical.parts):
        raise ValueError(f"unsafe adaptation path: {path!r}")
    return Path(*logical.parts)


def _canonicalize_headers(
    diff: str,
    source: TreeBlob,
    target: TreeBlob,
    source_path: str,
    target_path: str,
) -> str:
    source_label = _quote_diff_path(f"a/upstream/{source_path}")
    target_label = _quote_diff_path(f"b/deckshell/{target_path}")
    old_label = source_label if source.exists else "/dev/null"
    new_label = target_label if target.exists else "/dev/null"
    lines = diff.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("diff --git "):
            lines[index] = f"diff --git {source_label} {target_label}"
        elif line.startswith("--- "):
            lines[index] = f"--- {old_label}"
        elif line.startswith("+++ "):
            lines[index] = f"+++ {new_label}"
        elif line.startswith("Binary files "):
            lines[index] = f"Binary files {old_label} and {new_label} differ"
    return "\n".join(lines) + ("\n" if diff.endswith("\n") else "")


def _quote_diff_path(path: str) -> str:
    if re.search(r"[\s\"\\]", path):
        return json.dumps(path, ensure_ascii=False)
    return path


def _fenced_diff(diff: str) -> list[str]:
    longest = max((len(match) for match in re.findall(r"`+", diff)), default=0)
    fence = "`" * max(3, longest + 1)
    return [f"{fence}diff", diff.rstrip("\n"), fence, ""]
