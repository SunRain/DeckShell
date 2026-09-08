"""Single-pass unified source inventory construction."""

from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from .git_ops import (
    Change,
    changed_paths,
    commit_changes,
    git_succeeds,
    resolve_commit,
    run_git,
    sha256_bytes,
    sha256_file,
    stable_unique,
)
from .policy import PathDecision, decide_path, decision_payload
from .schema import CHILD_ROOTS, WLROOTS_ROOT
from .patches import tree_entry


PROTOCOL_SOURCE_ROOT = "protocols"
PROTOCOL_TARGET_PREFIX = "protocols/compositor/"


def _is_under(path: str, roots: Sequence[str]) -> bool:
    return any(path == root or path.startswith(f"{root}/") for root in roots)


def _is_protocol_xml(path: str, prefix: str) -> bool:
    return path.startswith(prefix) and PurePosixPath(path).suffix.lower() == ".xml"


def _paths(change: Change) -> List[str]:
    return changed_paths(change)


def _mutated_decisions(
    change: Change,
    old: Optional[PathDecision],
    new: Optional[PathDecision],
) -> List[PathDecision]:
    candidates = (new,) if change.status.startswith("C") else (old, new)
    return [item for item in candidates if item is not None]


def _classify(has_parent: bool, has_child: bool) -> str:
    if has_parent and has_child:
        return "dual"
    if has_parent:
        return "deckshell-only"
    if has_child:
        return "waylib-only"
    return "unowned-skip"


def _is_safe_source_path(path: str) -> bool:
    return (
        bool(path)
        and not path.startswith("/")
        and ".." not in PurePosixPath(path).parts
        and not any(ord(character) < 32 or ord(character) == 127 for character in path)
    )


def _unsafe_path_blockers(decisions: Sequence[PathDecision]) -> List[str]:
    return stable_unique(
        f"unsafe source path cannot be serialized: {item.source!r}"
        for item in decisions
        if not _is_safe_source_path(item.source)
    )


def _path_blockers(decisions: Sequence[PathDecision]) -> List[str]:
    findings: List[str] = []
    for item in decisions:
        if item.category == "unknown":
            findings.append(f"unknown source path: {item.source}")
        elif item.category == "review-only":
            findings.append(
                f"review-only path requires approval {item.policy_key}: {item.source}"
            )
    return stable_unique(findings)


def _change_payload(
    change: Change,
    old: Optional[PathDecision],
    new: Optional[PathDecision],
) -> Dict[str, Any]:
    return {
        "status": change.status,
        "old": decision_payload(old),
        "new": decision_payload(new),
        "child_old": bool(change.old_path and _is_under(change.old_path, CHILD_ROOTS)),
        "child_new": bool(change.new_path and _is_under(change.new_path, CHILD_ROOTS)),
        "wlroots_old": bool(change.old_path and _is_under(change.old_path, (WLROOTS_ROOT,))),
        "wlroots_new": bool(change.new_path and _is_under(change.new_path, (WLROOTS_ROOT,))),
    }


def _collect_commit_changes(
    repo: Path,
    sha: str,
    policy: Mapping[str, Any],
    approvals: Set[str],
) -> Tuple[List[PathDecision], List[PathDecision], List[Dict[str, Any]], List[str]]:
    decisions: List[PathDecision] = []
    mutations: List[PathDecision] = []
    payloads: List[Dict[str, Any]] = []
    source_paths: List[str] = []
    for change in commit_changes(repo, sha):
        old = _owner_decision(change.old_path, policy, approvals) if change.old_path else None
        new = _owner_decision(change.new_path, policy, approvals) if change.new_path else None
        decisions.extend(item for item in (old, new) if item is not None)
        mutations.extend(_mutated_decisions(change, old, new))
        payloads.append(_change_payload(change, old, new))
        source_paths.extend(_paths(change))
    return decisions, mutations, payloads, source_paths


def _owner_decision(path: str, policy: Mapping[str, Any], approvals: Set[str]) -> PathDecision:
    for root in (*CHILD_ROOTS, WLROOTS_ROOT):
        if _is_under(path, (root,)):
            return PathDecision(path, "excluded", None, root)
    return decide_path(path, policy, approvals)


def _layout_blockers(repo: Path, sha: str, source_paths):
    blockers = []
    for root in (*CHILD_ROOTS, WLROOTS_ROOT):
        if not any(_is_under(path, (root,)) for path in source_paths):
            continue
        for revision in (f"{sha}^", sha):
            entry = tree_entry(repo, revision, root)
            if entry and entry["type"] != "tree":
                blockers.append(f"source-layout-drift: {root} must be an ordinary source directory")
    return blockers


def _dependency_lanes(source_paths):
    child_paths = [path for path in source_paths if _is_under(path, CHILD_ROOTS)]
    wlroots_paths = [path for path in source_paths if _is_under(path, (WLROOTS_ROOT,))]
    return {
        "waylib_shared": {
            "included": bool(child_paths or wlroots_paths),
            "source_paths": stable_unique(child_paths),
            "drop_paths": stable_unique(
                [path for path in source_paths if not _is_under(path, CHILD_ROOTS)]
            ),
        },
        "wlroots": {
            "included": bool(wlroots_paths),
            "source_paths": stable_unique(wlroots_paths),
            "target_paths": stable_unique(path[len(WLROOTS_ROOT) + 1:] for path in wlroots_paths),
            "drop_paths": stable_unique(path for path in source_paths if path not in wlroots_paths),
        },
    }


def _summarize_commit(
    repo: Path,
    sha: str,
    policy: Mapping[str, Any],
    approvals: Set[str],
) -> Dict[str, Any]:
    decisions, mutations, payloads, source_paths = _collect_commit_changes(
        repo, sha, policy, approvals
    )

    parent = [item for item in mutations if item.category in {"mapped", "root-owned"}]
    dependencies = _dependency_lanes(source_paths)
    protocol_source_paths = stable_unique(
        path
        for path in source_paths
        if _is_protocol_xml(path, f"{PROTOCOL_SOURCE_ROOT}/")
    )
    blockers = _unsafe_path_blockers(decisions) + _path_blockers(mutations)
    blockers.extend(_layout_blockers(repo, sha, source_paths))
    classification = "blocked" if blockers else _classify(bool(parent), dependencies["waylib_shared"]["included"])
    target_paths = stable_unique([item.target for item in parent if item.target])
    return {
        "source_commit": sha,
        "subject": str(run_git(repo, "show", "-s", "--format=%s", sha)).rstrip("\n"),
        "classification": classification,
        "changes": payloads,
        "deckshell": {
            "included": bool(parent),
            "mapped_source_paths": stable_unique(
                [item.source for item in parent if item.category == "mapped"]
            ),
            "root_source_paths": stable_unique(
                [item.source for item in parent if item.category == "root-owned"]
            ),
            "target_paths": target_paths,
            "drop_paths": stable_unique(
                [item.source for item in mutations if item.category == "excluded"]
            ),
        },
        **dependencies,
        "protocol_source_paths": protocol_source_paths,
        "protocol_target_paths": [
            path
            for path in target_paths
            if _is_protocol_xml(path, PROTOCOL_TARGET_PREFIX)
        ],
        "blocked_reasons": blockers,
    }


def _range_commits(repo: Path, base: str, head: str) -> List[str]:
    output = str(run_git(repo, "rev-list", "--reverse", "--topo-order", f"{base}..{head}"))
    return output.split()


def build_unified_inventory(
    repo: Path,
    base: str,
    head: str,
    policy: Mapping[str, Any],
    policy_path: Path,
    approvals: Set[str],
    source_tip: Optional[str] = None,
) -> Dict[str, Any]:
    """Build one authoritative inventory for parent and child lanes."""

    base_sha = resolve_commit(repo, base)
    head_sha = resolve_commit(repo, head)
    source_tip_sha = resolve_commit(repo, source_tip or head_sha)
    base_is_ancestor = git_succeeds(repo, "merge-base", "--is-ancestor", base_sha, head_sha)
    head_is_on_source = git_succeeds(
        repo, "merge-base", "--is-ancestor", head_sha, source_tip_sha
    )
    ordered = _range_commits(repo, base_sha, head_sha) if base_is_ancestor else []
    merges = (
        str(run_git(repo, "rev-list", "--merges", f"{base_sha}..{head_sha}")).split()
        if base_is_ancestor
        else []
    )
    entries = [_summarize_commit(repo, sha, policy, approvals) for sha in ordered]
    blocked = []
    if not base_is_ancestor:
        blocked.append("range base is not an ancestor of range head")
    if not head_is_on_source:
        blocked.append("range head is not an ancestor of frozen source tip")
    blocked.extend(f"range contains merge commit: {sha}" for sha in merges)
    blocked.extend(reason for entry in entries for reason in entry["blocked_reasons"])
    counts = {
        name: sum(entry["classification"] == name for entry in entries)
        for name in ("deckshell-only", "waylib-only", "dual", "unowned-skip", "blocked")
    }
    return {
        "schema_version": 2,
        "kind": "treeland-deckshell-waylib-unified-inventory",
        "source_repo": str(repo.resolve()),
        "range": {
            "base": base_sha,
            "head": head_sha,
            "source_tip": source_tip_sha,
            "ordered_source_commits": ordered,
            "ordered_sha256": sha256_bytes("".join(f"{sha}\n" for sha in ordered).encode("ascii")),
            "merge_commits": merges,
        },
        "path_policy": {"path": str(policy_path.resolve()), "sha256": sha256_file(policy_path)},
        "approved_review": sorted(approvals),
        "child_owned_roots": list(CHILD_ROOTS),
        "wlroots_owned_root": WLROOTS_ROOT,
        "counts": counts,
        "commits": entries,
        "blocked_reasons": stable_unique(blocked),
        "outcome": "blocked" if blocked else "pass",
    }
