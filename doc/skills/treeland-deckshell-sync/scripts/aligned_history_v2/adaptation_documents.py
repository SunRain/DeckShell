"""Render final v2 SHA-named adaptation records from the sealed prefix."""

from __future__ import annotations

import hashlib
from typing import Any

from .repository import GitRepository


FORBIDDEN_DOCUMENT_KEYS = (
    "Previous-Rewrite-Commit",
    "Legacy-DeckShell-Target",
    "Legacy-DeckShell-Commit",
    "Source-Ref",
    "Absorbed-DeckShell-Commit",
    "Derived-From-Commit",
    "Superseded-Source-Commit",
    "Excluded-Source-Commit",
)


def render_adaptation_documents(
    repo: GitRepository,
    prefix: dict[str, Any],
    adaptation_manifest: dict[str, Any],
    *,
    remediation_paths: set[str] | None = None,
) -> dict[str, bytes]:
    """Render exactly 58 documents from source metadata and the v2 prefix."""

    prefix_entries = prefix.get("entries")
    if not isinstance(prefix_entries, list) or len(prefix_entries) != 298:
        raise ValueError("Treeland target prefix must contain 298 entries")
    by_source = {
        entry["normalized_treeland_commit"]: entry for entry in prefix_entries
    }
    if len(by_source) != 298:
        raise ValueError("Treeland target prefix contains duplicate sources")
    entries = adaptation_manifest.get("entries")
    if not isinstance(entries, list):
        raise ValueError("adaptation manifest has no entries")
    adapted = [entry for entry in entries if entry.get("action") == "adapted"]
    if len(adapted) != 58:
        raise ValueError(f"adapted entry count mismatch: {len(adapted)}")
    documents: dict[str, bytes] = {}
    for entry in adapted:
        source = str(entry["source_commit"])
        prefix_entry = by_source.get(source)
        if prefix_entry is None:
            raise ValueError(f"adapted source lacks v2 target: {source}")
        evidence = collect_path_evidence(
            repo,
            entry,
            prefix_entry,
            remediation_paths=remediation_paths,
        )
        content = render_adaptation_document(entry, prefix_entry, evidence).encode(
            "utf-8"
        )
        for key in FORBIDDEN_DOCUMENT_KEYS:
            if key.encode("ascii") in content:
                raise ValueError(f"adaptation document contains retired key: {key}")
        path = f"doc/treeland-sync/adaptations/{prefix_entry['v2_target']}.md"
        if path in documents:
            raise ValueError(f"duplicate adaptation document path: {path}")
        documents[path] = content
    if len(documents) != 58:
        raise ValueError("adaptation document output count mismatch")
    return documents


def render_adaptation_document(
    entry: dict[str, Any],
    prefix_entry: dict[str, Any],
    path_evidence: dict[str, dict[str, str]],
) -> str:
    """Render one final record without legacy DeckShell identity fields."""

    source = _sha(entry.get("source_commit"), "source_commit")
    target = _sha(prefix_entry.get("v2_target"), "v2_target")
    if entry.get("action") != "adapted" or prefix_entry.get("action") != "adapted":
        raise ValueError(f"adaptation document input is not adapted: {source}")
    classification = str(entry.get("classification"))
    if prefix_entry.get("classification") != classification:
        raise ValueError(f"adaptation classification drift: {source}")
    notes = str(entry.get("adaptation_notes", "")).strip()
    paths = entry.get("adaptation_paths")
    if not notes or not isinstance(paths, list) or not paths:
        raise ValueError(f"adaptation entry lacks paths or notes: {source}")
    lines = [
        "# Treeland 同步适配记录",
        "",
        f"- DeckShell commit: `{target}`",
        f"- Treeland commit: `{source}`",
        "- Treeland-Remote: `treeland`",
        "- Treeland-Remote-Branch: `master`",
        "- Treeland-Tracking-Ref: `refs/remotes/treeland/master`",
        f"- Subject: {prefix_entry['subject']}",
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
    for path_entry in paths:
        kind = str(path_entry.get("kind"))
        path = str(path_entry.get("path"))
        justification = str(path_entry.get("justification", "")).strip()
        evidence = path_evidence.get(path)
        if kind not in {"modified", "materialized", "omitted"}:
            raise ValueError(f"unsupported adaptation path kind: {kind}")
        if not justification or not isinstance(evidence, dict):
            raise ValueError(f"missing adaptation path evidence: {source}: {path}")
        lines.extend(
            [
                f"### `{kind}: {path}`",
                "",
                justification,
                "",
                f"- Treeland source path: `{evidence['source_path']}`",
                f"- Treeland source diff SHA-256: `{evidence['source_diff_sha256']}`",
                f"- DeckShell target evidence: "
                f"`{evidence.get('target_evidence_kind', 'commit-delta')}`",
                f"- DeckShell target diff SHA-256: `{evidence['target_diff_sha256']}`",
            ]
        )
        if evidence.get("target_post_image_sha256"):
            lines.append(
                "- DeckShell target post-image SHA-256: "
                f"`{evidence['target_post_image_sha256']}`"
            )
        lines.append("")
    return "\n".join(lines)


def _sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or len(value) != 40 or any(
        character not in "0123456789abcdef" for character in value
    ):
        raise ValueError(f"{label} must be a full lowercase SHA-1")
    return value


def collect_path_evidence(
    repo: GitRepository,
    entry: dict[str, Any],
    prefix_entry: dict[str, Any],
    *,
    remediation_paths: set[str] | None = None,
) -> dict[str, dict[str, str]]:
    """Collect source and target path-diff hashes from real Git commits."""

    source = str(entry["source_commit"])
    target = str(prefix_entry["v2_target"])
    result: dict[str, dict[str, str]] = {}
    for path_entry in entry["adaptation_paths"]:
        kind = str(path_entry["kind"])
        target_path = str(path_entry["path"])
        source_path = _source_path(entry, target_path)
        source_diff = _path_diff(repo, source, source_path)
        target_diff = _path_diff(repo, target, target_path)
        if not source_diff:
            raise ValueError(f"adaptation source path has no diff: {source}: {source_path}")
        if kind == "omitted" and target_diff:
            raise ValueError(f"omitted adaptation path appears in target: {target_path}")
        evidence = {
            "source_path": source_path,
            "source_diff_sha256": hashlib.sha256(source_diff).hexdigest(),
            "target_diff_sha256": hashlib.sha256(target_diff).hexdigest(),
        }
        if kind == "omitted":
            evidence["target_evidence_kind"] = "omitted"
        elif target_diff:
            evidence["target_evidence_kind"] = "commit-delta"
        else:
            if target_path not in (remediation_paths or set()):
                raise ValueError(
                    f"adaptation target path has no diff: {target}: {target_path}"
                )
            post_image = _path_post_image(repo, target, target_path)
            evidence["target_evidence_kind"] = "remediation-inherited-post-image"
            evidence["target_post_image_sha256"] = hashlib.sha256(
                post_image
            ).hexdigest()
        result[target_path] = evidence
    return result


def _source_path(entry: dict[str, Any], target_path: str) -> str:
    matches: list[str] = []
    for change in entry.get("source_changes", []):
        for side in ("old", "new"):
            decision = change.get(side)
            if isinstance(decision, dict) and decision.get("target") == target_path:
                matches.append(str(decision["source"]))
    unique = list(dict.fromkeys(matches))
    if len(unique) != 1:
        raise ValueError(
            f"target path does not map to one Treeland source: {target_path}: {unique}"
        )
    return unique[0]


def _path_diff(repo: GitRepository, commit: str, path: str) -> bytes:
    parent = repo.run("rev-parse", f"{commit}^").decode().strip()
    return repo.run(
        "diff-tree",
        "--no-commit-id",
        "--full-index",
        "--binary",
        "--no-renames",
        "--no-ext-diff",
        "--no-color",
        "-p",
        parent,
        commit,
        "--",
        path,
    )


def _path_post_image(repo: GitRepository, commit: str, path: str) -> bytes:
    record = repo.run("ls-tree", "-z", commit, "--", path)
    rows = record.rstrip(b"\0").split(b"\0") if record else []
    if len(rows) != 1:
        raise ValueError(f"remediation target path lacks one post-image: {path}")
    metadata, separator, actual_path = rows[0].partition(b"\t")
    if not separator or actual_path.decode("utf-8") != path:
        raise ValueError(f"invalid remediation target post-image: {path}")
    mode, kind, object_id = metadata.decode("ascii").split(" ")
    if kind != "blob":
        raise ValueError(f"remediation target post-image is not a blob: {path}")
    return mode.encode("ascii") + b"\0" + repo.cat_file("blob", object_id)
