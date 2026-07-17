"""Object, patch and chain equivalence checks for rewritten sync history."""

from __future__ import annotations

import hashlib
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from .history_rewrite import parse_raw_commit, read_raw_commit, render_commit


DIFF_TREE_ARGS = (
    "-c",
    "diff.renames=false",
    "diff-tree",
    "--no-commit-id",
    "--no-renames",
    "--binary",
    "--full-index",
    "--no-ext-diff",
    "--no-textconv",
    "-r",
)


def _run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _patch_sha256(repo: Path, parent: str, commit: str) -> str:
    output = _run_git(repo, *DIFF_TREE_ARGS, parent, commit).stdout
    return hashlib.sha256(output).hexdigest()


def _add_mismatch(
    findings: list[str], mismatches: Counter[str], kind: str, ordinal: int, detail: str
) -> None:
    mismatches[kind] += 1
    findings.append(f"ordinal {ordinal}: {kind}: {detail}")


def _verify_record(
    repo: Path,
    ordinal: int,
    entry: dict[str, Any],
    mapping: dict[str, Any],
    previous_new: str,
    findings: list[str],
    mismatches: Counter[str],
) -> None:
    old_id = str(mapping.get("legacy_target_commit", ""))
    new_id = str(mapping.get("rewritten_target_commit", ""))
    if entry.get("legacy_target_commit") != old_id or entry.get("source_commit") != mapping.get(
        "source_commit"
    ):
        _add_mismatch(findings, mismatches, "mapping", ordinal, "manifest and mapping differ")
        return
    try:
        old_raw, new_raw = read_raw_commit(repo, old_id), read_raw_commit(repo, new_id)
        old, new = parse_raw_commit(old_raw), parse_raw_commit(new_raw)
    except (subprocess.CalledProcessError, ValueError) as error:
        _add_mismatch(findings, mismatches, "object", ordinal, str(error))
        return

    expected_parent = previous_new or old.parent
    _, expected_raw, expected_id = render_commit(old_raw, entry, expected_parent)
    checks = (
        ("tree", old.tree, new.tree),
        ("author", old.author, new.author),
        ("committer", old.committer, new.committer),
        ("parent", expected_parent, new.parent),
        ("object-id", expected_id, new_id),
        ("message", expected_raw.partition(b"\n\n")[2], new.message),
    )
    for kind, expected, actual in checks:
        if expected != actual:
            _add_mismatch(findings, mismatches, kind, ordinal, "expected value mismatch")
    if expected_raw != new_raw:
        _add_mismatch(findings, mismatches, "raw-object", ordinal, "renderer output differs")

    old_patch = _patch_sha256(repo, old.parent, old_id)
    new_patch = _patch_sha256(repo, new.parent, new_id)
    if old_patch != new_patch:
        _add_mismatch(findings, mismatches, "patch", ordinal, "diff-tree SHA-256 differs")


def _verify_heads(
    repo: Path,
    mappings: list[dict[str, Any]],
    expected_head_tree: str,
    findings: list[str],
    mismatches: Counter[str],
) -> tuple[str, str]:
    old_head = str(mappings[-1].get("legacy_target_commit", "")) if mappings else ""
    new_head = str(mappings[-1].get("rewritten_target_commit", "")) if mappings else ""
    if mappings and mappings[-1].get("tree") != expected_head_tree:
        findings.append("mapping head tree differs from expected tree")
        mismatches["head-tree"] += 1
    if old_head and new_head:
        tree_diff = _run_git(
            repo,
            "diff",
            "--exit-code",
            "--no-ext-diff",
            "--no-textconv",
            old_head,
            new_head,
            "--",
            check=False,
        )
        if tree_diff.returncode:
            findings.append("legacy and rewritten heads have different trees")
            mismatches["head-diff"] += 1
    return old_head, new_head


def _source_order_digest(mappings: list[dict[str, Any]]) -> str:
    source_order = "\n".join(str(item.get("source_commit", "")) for item in mappings)
    return hashlib.sha256(source_order.encode("ascii")).hexdigest()


def verify_history_equivalence(
    repo: Path,
    manifest: dict[str, Any],
    mapping_payload: dict[str, Any],
    expected_count: int,
    expected_head_tree: str,
) -> dict[str, Any]:
    """Verify every rewritten object and the final tree against legacy history."""

    entries = manifest.get("entries", [])
    mappings = mapping_payload.get("mappings", [])
    findings: list[str] = []
    mismatches: Counter[str] = Counter()
    if len(entries) != expected_count or len(mappings) != expected_count:
        findings.append(
            f"expected {expected_count} entries, got manifest={len(entries)} mappings={len(mappings)}"
        )
        mismatches["count"] += 1

    previous_new = ""
    for ordinal, (entry, mapping) in enumerate(zip(entries, mappings), 1):
        _verify_record(
            repo,
            ordinal,
            entry,
            mapping,
            previous_new,
            findings,
            mismatches,
        )
        previous_new = str(mapping.get("rewritten_target_commit", ""))

    old_head, new_head = _verify_heads(
        repo, mappings, expected_head_tree, findings, mismatches
    )
    return {
        "schema_version": 1,
        "outcome": "blocked" if findings else "pass",
        "count": len(mappings),
        "legacy_head": old_head,
        "rewritten_head": new_head,
        "expected_head_tree": expected_head_tree,
        "source_order_sha256": _source_order_digest(mappings),
        "mismatch_counts": dict(mismatches),
        "findings": findings,
    }
