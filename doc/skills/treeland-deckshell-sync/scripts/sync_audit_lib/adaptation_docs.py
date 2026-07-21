"""Deterministically render and verify SHA-named adaptation documents."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from .adaptation import KIND_ORDER
from .adaptation_content_delta import (
    render_content_delta,
    source_post_path_for_target,
)
from .adaptation_doc_inputs import (
    mapping_by_legacy,
    read_json,
    required_sha,
    source_path_for_target,
    validate_inputs,
    validate_path_metadata,
    verify_commit_message,
    verify_target_in_range,
)
from .common import run_git


DOCUMENT_SUFFIX = ".md"


def render_documents(
    repo: Path,
    manifest: dict[str, Any],
    mapping: dict[str, Any],
    base: str,
    head: str,
    *,
    manifest_sha256: str,
    mapping_sha256: str,
    expected_count: int | None = None,
) -> dict[str, str]:
    """Render every adapted manifest entry into canonical Markdown."""

    entries = validate_inputs(repo, manifest, mapping, base, head)
    mappings = mapping_by_legacy(mapping)
    adapted = [entry for entry in entries if entry.get("action") == "adapted"]
    if expected_count is not None and len(adapted) != expected_count:
        raise ValueError(
            f"adapted count mismatch: expected {expected_count}, got {len(adapted)}"
        )
    documents: dict[str, str] = {}
    for entry in adapted:
        filename, content = _render_entry(
            repo,
            entry,
            mappings,
            base,
            head,
            manifest_sha256,
            mapping_sha256,
            str(mapping.get("plan_digest_sha256", "")),
        )
        if filename in documents:
            raise ValueError(f"duplicate rewritten target document: {filename}")
        documents[filename] = content
    return documents


def write_documents(docs_dir: Path, documents: dict[str, str]) -> None:
    """Write canonical documents without deleting unexpected Markdown files."""

    docs_dir.mkdir(parents=True, exist_ok=True)
    expected = set(documents)
    existing = _existing_documents(docs_dir)
    actual = set(existing)
    unexpected = sorted(actual - expected)
    if unexpected:
        raise ValueError(f"unexpected adaptation documents: {', '.join(unexpected)}")
    for filename, content in sorted(documents.items()):
        (docs_dir / filename).write_text(content, encoding="utf-8", newline="\n")


def verify_documents(docs_dir: Path, documents: dict[str, str]) -> None:
    """Require the directory to match the canonical document set byte-for-byte."""

    expected = set(documents)
    existing = _existing_documents(docs_dir)
    actual = set(existing)
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    findings = []
    if missing:
        findings.append(f"missing documents: {', '.join(missing)}")
    if unexpected:
        findings.append(f"unexpected documents: {', '.join(unexpected)}")
    for filename in sorted(expected & actual):
        content = existing[filename].read_bytes()
        if content != documents[filename].encode("utf-8"):
            findings.append(f"document content mismatch: {filename}")
    if findings:
        raise ValueError("; ".join(findings))


def _existing_documents(docs_dir: Path) -> dict[str, Path]:
    if docs_dir.is_symlink():
        raise ValueError(f"documents directory must not be a symlink: {docs_dir}")
    result: dict[str, Path] = {}
    for path in docs_dir.glob(f"*{DOCUMENT_SUFFIX}"):
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"document must be a regular file: {path.name}")
        result[path.name] = path
    return result


def _render_entry(
    repo: Path,
    entry: dict[str, Any],
    mappings: dict[str, dict[str, Any]],
    base: str,
    head: str,
    manifest_sha256: str,
    mapping_sha256: str,
    plan_digest: str,
) -> tuple[str, str]:
    source = required_sha(entry, "source_commit")
    legacy = required_sha(entry, "legacy_target_commit")
    mapping_row = mappings.get(legacy)
    target = required_sha(mapping_row, "rewritten_target_commit")
    mapped_source = required_sha(mapping_row, "source_commit")
    if mapped_source != source:
        raise ValueError(
            f"source mapping mismatch: {legacy}: {source} != {mapped_source}"
        )
    verify_target_in_range(repo, base, head, target)
    return (
        f"{target}{DOCUMENT_SUFFIX}",
        _render_document(
            repo,
            entry,
            target,
            manifest_sha256,
            mapping_sha256,
            plan_digest,
        ),
    )


def _render_document(
    repo: Path,
    entry: dict[str, Any],
    target: str,
    manifest_sha256: str,
    mapping_sha256: str,
    plan_digest: str,
) -> str:
    source = required_sha(entry, "source_commit")
    classification = str(entry.get("classification", ""))
    notes = str(entry.get("adaptation_notes", "")).strip()
    paths = entry.get("adaptation_paths")
    if not notes or not isinstance(paths, list) or not paths:
        raise ValueError(f"adapted entry lacks paths or notes: {source}")
    verify_commit_message(repo, target, source, classification, paths, notes)
    canonical = sorted(
        paths,
        key=lambda item: (
            KIND_ORDER[item["kind"]],
            item["path"].encode("utf-8"),
        ),
    )
    if paths != canonical:
        raise ValueError(f"adaptation paths are not canonical: {source}")
    subject = str(run_git(repo, "show", "-s", "--format=%s", target)).strip()
    sections = _document_header(target, source, subject, classification, notes)
    for path_entry in paths:
        sections.extend(_render_path(repo, entry, target, path_entry))
    sections.extend(
        _evidence_footer(manifest_sha256, mapping_sha256, plan_digest)
    )
    return "\n".join(sections)


def _document_header(
    target: str,
    source: str,
    subject: str,
    classification: str,
    notes: str,
) -> list[str]:
    return [
        "# Treeland 同步适配记录",
        "",
        f"- DeckShell commit: `{target}`",
        f"- Treeland commit: `{source}`",
        f"- Subject: {subject}",
        f"- Classification: `{classification}`",
        "- Action: `adapted`",
        "",
        "## 适配说明",
        "",
        notes,
        "",
        "## 适配路径",
        "",
    ]


def _evidence_footer(
    manifest_sha256: str, mapping_sha256: str, plan_digest: str
) -> list[str]:
    return [
        "## 输入证据",
        "",
        f"- Manifest SHA-256: `{manifest_sha256}`",
        f"- Mapping SHA-256: `{mapping_sha256}`",
        f"- Mapping plan digest: `{plan_digest}`",
        "",
    ]


def _render_path(
    repo: Path,
    entry: dict[str, Any],
    target: str,
    path_entry: dict[str, Any],
) -> list[str]:
    kind = str(path_entry.get("kind"))
    path = str(path_entry.get("path"))
    if kind not in {"modified", "materialized", "omitted"}:
        raise ValueError(f"unsupported adaptation path kind: {kind}")
    validate_path_metadata(repo, target, path_entry)
    justification = str(path_entry.get("justification", "")).strip()
    if not justification:
        raise ValueError(f"adaptation path lacks justification: {target}: {path}")
    if kind == "omitted":
        section = _render_omitted_path(repo, entry, target, path, justification)
    else:
        diff = _target_diff(repo, target, path)
        if not diff:
            raise ValueError(f"target path has no diff: {target}: {path}")
        section = _target_path_section(kind, path, justification, diff)
    source = required_sha(entry, "source_commit")
    source_path = source_post_path_for_target(entry, path)
    section.extend(render_content_delta(repo, source, target, source_path, path))
    return section


def _target_path_section(
    kind: str, path: str, justification: str, diff: str
) -> list[str]:
    digest = hashlib.sha256(diff.encode("utf-8")).hexdigest()
    section = [
        f"### `{kind}: {path}`",
        "",
        "#### 为什么这样适配",
        "",
        justification,
        "",
        "#### 完整目标提交 diff",
        "",
        "> 以下内容是该路径在目标提交中的完整实际修改，不等同于纯 adaptation delta。",
        "",
        f"- Diff SHA-256: `{digest}`",
        "",
    ]
    section.extend(_fenced_diff(diff))
    return section


def _render_omitted_path(
    repo: Path,
    entry: dict[str, Any],
    target: str,
    target_path: str,
    justification: str,
) -> list[str]:
    if _target_diff(repo, target, target_path):
        raise ValueError(f"omitted path appears in target diff: {target}: {target_path}")
    source = required_sha(entry, "source_commit")
    source_path = source_path_for_target(entry, target_path)
    diff = _mapped_source_diff(repo, source, source_path, target_path)
    if not diff:
        raise ValueError(f"omitted source path has no diff: {source}: {source_path}")
    digest = hashlib.sha256(diff.encode("utf-8")).hexdigest()
    section = [
        f"### `omitted: {target_path}`",
        "",
        "#### 为什么这样适配",
        "",
        justification,
        "",
        "#### 目标提交结果",
        "",
        "目标提交无该路径 diff；该路径按审定合同明确省略。",
        "",
        "#### 完整映射上游 diff",
        "",
        f"- Treeland source path: `{source_path}`",
        f"- Diff SHA-256: `{digest}`",
        "",
    ]
    section.extend(_fenced_diff(diff))
    return section


def _fenced_diff(diff: str) -> list[str]:
    longest = max((len(match) for match in re.findall(r"`+", diff)), default=0)
    fence = "`" * max(3, longest + 1)
    return [f"{fence}diff", diff.rstrip("\n"), fence, ""]


def _mapped_source_diff(
    repo: Path, source: str, source_path: str, target_path: str
) -> str:
    if not target_path.endswith(source_path):
        raise ValueError(f"target path is not a prefix mapping: {source_path} -> {target_path}")
    prefix = target_path[: -len(source_path)]
    parent = str(run_git(repo, "rev-parse", f"{source}^")).strip()
    return str(
        run_git(
            repo,
            "diff-tree",
            "--no-commit-id",
            "--full-index",
            "--binary",
            "--no-renames",
            "--no-ext-diff",
            "--no-color",
            f"--src-prefix=a/{prefix}",
            f"--dst-prefix=b/{prefix}",
            "-p",
            parent,
            source,
            "--",
            source_path,
        )
    )


def _target_diff(repo: Path, target: str, path: str) -> str:
    parent = str(run_git(repo, "rev-parse", f"{target}^")).strip()
    return str(
        run_git(
            repo,
            "diff-tree",
            "--no-commit-id",
            "--full-index",
            "--binary",
            "--no-renames",
            "--no-ext-diff",
            "--no-color",
            "-p",
            parent,
            target,
            "--",
            path,
        )
    )
