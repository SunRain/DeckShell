"""Source range inventory construction."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from .common import Change, PathDecision, Policy, classify_path, parse_name_status_z, run_git


def _decision_payload(decision: PathDecision | None) -> dict[str, Any] | None:
    if decision is None:
        return None
    return {
        "source": decision.source,
        "category": decision.category,
        "target": decision.target,
        "policy_key": decision.policy_key,
    }


def _classify_decisions(
    decisions: list[PathDecision],
) -> tuple[str, list[PathDecision], list[str]]:
    blocked = []
    for decision in decisions:
        if decision.category == "unknown":
            blocked.append(f"unknown path: {decision.source}")
        elif decision.category == "review-only":
            blocked.append(
                "review-only path requires --approve-review "
                f"{decision.policy_key}: {decision.source}"
            )

    retained = [item for item in decisions if item.category in {"mapped", "root-owned"}]
    has_excluded = any(item.category == "excluded" for item in decisions)
    if blocked:
        return "blocked", retained, blocked
    if has_excluded and retained:
        return "mixed", retained, blocked
    if has_excluded:
        return "dependency-only", retained, blocked
    if retained:
        return "other", retained, blocked
    return "blocked", retained, ["commit has no classifiable paths"]


def summarize_commit(
    sha: str,
    subject: str,
    changes: list[Change],
    policy: Policy,
    approved_review: set[str],
) -> dict[str, Any]:
    """Classify one source commit and calculate retained and dropped paths."""

    decisions: list[PathDecision] = []
    change_payloads: list[dict[str, Any]] = []
    for change in changes:
        old = classify_path(change.old_path, policy, approved_review) if change.old_path else None
        new = classify_path(change.new_path, policy, approved_review) if change.new_path else None
        decisions.extend(item for item in (old, new) if item is not None)
        change_payloads.append(
            {"status": change.status, "old": _decision_payload(old), "new": _decision_payload(new)}
        )

    classification, retained, blocked_reasons = _classify_decisions(decisions)

    return {
        "source_commit": sha,
        "subject": subject,
        "classification": classification,
        "changes": change_payloads,
        "retained_paths": list(dict.fromkeys(item.source for item in retained)),
        "mapped_source_paths": list(
            dict.fromkeys(item.source for item in retained if item.category == "mapped")
        ),
        "root_source_paths": list(
            dict.fromkeys(item.source for item in retained if item.category == "root-owned")
        ),
        "drop_paths": list(
            dict.fromkeys(item.source for item in decisions if item.category == "excluded")
        ),
        "target_paths": list(dict.fromkeys(item.target for item in retained if item.target)),
        "blocked_reasons": list(dict.fromkeys(blocked_reasons)),
    }


def build_inventory(
    repo: Path,
    base: str,
    head: str,
    policy: Policy,
    approved_review: set[str],
) -> dict[str, Any]:
    """Build the ordered source inventory for one fixed commit range."""

    run_git(repo, "merge-base", "--is-ancestor", base, head)
    ordered = str(run_git(repo, "rev-list", "--reverse", "--topo-order", f"{base}..{head}")).split()
    merges = str(run_git(repo, "rev-list", "--merges", f"{base}..{head}")).split()
    entries = []
    blocked_reasons = [f"range contains merge commit: {sha}" for sha in merges]
    for sha in ordered:
        subject = str(run_git(repo, "show", "-s", "--format=%s", sha)).rstrip("\n")
        raw = run_git(
            repo,
            "diff-tree",
            "--no-commit-id",
            "--name-status",
            "-r",
            "--find-renames",
            "--find-copies",
            "-z",
            f"{sha}^",
            sha,
            text=False,
        )
        entry = summarize_commit(
            sha, subject, parse_name_status_z(bytes(raw)), policy, approved_review
        )
        entries.append(entry)
        blocked_reasons.extend(f"{sha}: {reason}" for reason in entry["blocked_reasons"])

    counts = {
        "total": len(entries),
        "dependency-only": sum(item["classification"] == "dependency-only" for item in entries),
        "mixed": sum(item["classification"] == "mixed" for item in entries),
        "other": sum(item["classification"] == "other" for item in entries),
    }
    blocked_count = sum(item["classification"] == "blocked" for item in entries)
    if blocked_count:
        counts["blocked"] = blocked_count
    digest = hashlib.sha256("".join(f"{sha}\n" for sha in ordered).encode("ascii")).hexdigest()
    return {
        "schema_version": 1,
        "range_base": str(run_git(repo, "rev-parse", f"{base}^{{commit}}")).strip(),
        "range_head": str(run_git(repo, "rev-parse", f"{head}^{{commit}}")).strip(),
        "ordered_source_commits": ordered,
        "ordered_sha256": digest,
        "merge_commits": merges,
        "approved_review": sorted(approved_review),
        "counts": counts,
        "commits": entries,
        "blocked_reasons": list(dict.fromkeys(blocked_reasons)),
        "outcome": "blocked" if blocked_reasons else "pass",
    }
