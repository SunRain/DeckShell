"""Materialize the manifest child candidate inside the parent worktree."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Tuple

from .git_ops import (
    GitError,
    canonical_json_sha256,
    canonical_repo,
    is_linked_worktree,
    resolve_commit,
    run_git,
)
from .patches import tree_entry
from .replay_types import GITLINK_PATH
from .schema import WLROOTS_ROOT, is_full_sha
from .wlroots import registration


class MaterializationBlocked(RuntimeError):
    """Raised when a child checkout cannot be created without overwriting state."""


def _common_git_dir(repo: Path) -> Path:
    value = Path(str(run_git(repo, "rev-parse", "--git-common-dir")).strip())
    return value.resolve() if value.is_absolute() else (repo / value).resolve()


def _is_clean(repo: Path) -> bool:
    return not bool(
        str(run_git(repo, "status", "--porcelain=v1", "--untracked-files=all"))
    )


def _manifest_heads(
    parent_worktree: Path, child_repo: Path, manifest: Mapping[str, Any]
) -> Tuple[str, str]:
    if manifest.get("schema_version") != 2:
        raise MaterializationBlocked("unsupported manifest schema")
    if manifest.get("kind") != "treeland-unified-sync-manifest":
        raise MaterializationBlocked("manifest kind is invalid")
    if manifest.get("outcome") != "pass":
        raise MaterializationBlocked("manifest outcome must be pass")
    parent_head = manifest.get("final_parent_head")
    child_head = manifest.get("final_child_head")
    if not is_full_sha(parent_head) or not is_full_sha(child_head):
        raise MaterializationBlocked("manifest final heads must be full SHAs")
    identity = manifest.get("identity")
    recorded_parent = identity.get("parent_worktree") if isinstance(identity, dict) else None
    if recorded_parent != str(parent_worktree):
        raise MaterializationBlocked("manifest parent worktree differs from request")
    if resolve_commit(parent_worktree, "HEAD") != parent_head:
        raise MaterializationBlocked("parent worktree HEAD differs from final parent")
    try:
        resolved_child = resolve_commit(child_repo, child_head)
    except GitError as error:
        raise MaterializationBlocked("final child commit is unavailable locally") from error
    return parent_head, resolved_child


def _checkout_evidence(
    checkout: Path, child_common_dir: Path, child_head: str
) -> Dict[str, Any]:
    if not os.path.lexists(str(checkout / ".git")):
        raise MaterializationBlocked("existing gitlink path is not a child checkout")
    try:
        if canonical_repo(checkout) != checkout:
            raise MaterializationBlocked("child checkout root is not the gitlink path")
        head = resolve_commit(checkout, "HEAD")
        common_dir = _common_git_dir(checkout)
        clean = _is_clean(checkout)
        linked = is_linked_worktree(checkout)
    except (GitError, ValueError) as error:
        raise MaterializationBlocked("child checkout cannot be inspected") from error
    if common_dir != child_common_dir:
        raise MaterializationBlocked("child checkout belongs to a different Git repository")
    if head != child_head:
        raise MaterializationBlocked("checkout HEAD differs from final child")
    if not linked:
        raise MaterializationBlocked("child checkout must be a linked worktree")
    if not clean:
        raise MaterializationBlocked("child checkout must be clean")
    return {
        "path": str(checkout),
        "head": head,
        "common_git_dir": str(common_dir),
        "linked_worktree": linked,
        "clean": clean,
    }


def _can_create_at(checkout: Path) -> bool:
    if checkout.is_symlink() or (checkout.exists() and not checkout.is_dir()):
        return False
    return not checkout.exists() or not any(checkout.iterdir())


def _materialize_at(owner: Path, relative: str, dependency: Path, head: str):
    checkout = owner / relative
    if any(part.is_symlink() for part in (checkout, *checkout.parents)):
        raise MaterializationBlocked("gitlink checkout path must not traverse symlinks")
    link = tree_entry(owner, "HEAD", relative)
    if not link or link["mode"] != "160000" or link["sha"] != head:
        raise MaterializationBlocked("owner gitlink differs from expected dependency")
    if str(run_git(dependency, "cat-file", "-t", head)).strip() != "commit":
        raise MaterializationBlocked("dependency is not a local commit object")
    common = _common_git_dir(dependency)
    if os.path.lexists(str(checkout / ".git")):
        evidence = _checkout_evidence(checkout, common, head)
        status = "verified"
    else:
        if not _can_create_at(checkout):
            raise MaterializationBlocked("gitlink path is non-empty and cannot be overwritten")
        if not _is_clean(owner):
            raise MaterializationBlocked("owner worktree must be clean before materialization")
        try:
            run_git(dependency, "worktree", "add", "--detach", str(checkout), head)
        except GitError as error:
            raise MaterializationBlocked(f"child worktree creation failed: {error}") from error
        evidence = _checkout_evidence(checkout, common, head)
        status = "created"
    if not _is_clean(owner):
        raise MaterializationBlocked("owner worktree is dirty after dependency materialization")
    return evidence, status


def materialize_child_checkout(
    parent_worktree: Path,
    child_repo: Path,
    manifest: Mapping[str, Any],
    wlroots_repo: Optional[Path] = None,
    child_base_worktree: Optional[Path] = None,
) -> Dict[str, Any]:
    """物化 C 独立构建及 P 构建所需的固定两层依赖，不覆盖已有 checkout。"""

    paths = (parent_worktree, child_repo, wlroots_repo, child_base_worktree)
    if any(part.is_symlink() for path in paths if path is not None for part in (path, *path.parents)):
        raise MaterializationBlocked("worktree inputs must not be symlinks")
    parent, child = canonical_repo(parent_worktree), canonical_repo(child_repo)
    if not is_linked_worktree(parent):
        raise MaterializationBlocked("parent target must be a secondary linked worktree")
    parent_head, child_head = _manifest_heads(parent, child, manifest)
    identity = manifest["identity"]
    if identity.get("child_common_git_dir") not in (None, str(_common_git_dir(child))):
        raise MaterializationBlocked("child repository differs from frozen identity")
    r = identity.get("wlroots")
    nested = {"child_base": None, "child_candidate": None, "parent_candidate": None}
    if r is not None:
        if not isinstance(r, dict) or wlroots_repo is None:
            raise MaterializationBlocked("active wlroots requires an explicit local repository")
        dep = canonical_repo(wlroots_repo)
        if str(_common_git_dir(dep)) != r.get("common_git_dir"):
            raise MaterializationBlocked("wlroots repository differs from frozen identity")
        rhead = manifest.get("final_wlroots_head")
        if not is_full_sha(rhead):
            raise MaterializationBlocked("wlroots candidate must be a full SHA")
        candidate = canonical_repo(Path(identity["child_worktree"]))
        _checkout_evidence(candidate, _common_git_dir(child), child_head)
        registration(candidate, "HEAD", rhead, r["submodule_url"])
        nested["child_candidate"], _ = _materialize_at(candidate, WLROOTS_ROOT, dep, rhead)
        if r["registered_at_base"]:
            if child_base_worktree is None:
                raise MaterializationBlocked("registered wlroots baseline requires --child-base-worktree")
            base = canonical_repo(child_base_worktree)
            _checkout_evidence(base, _common_git_dir(child), identity["child_base"])
            registration(base, "HEAD", r["base"], r["submodule_url"])
            nested["child_base"], _ = _materialize_at(base, WLROOTS_ROOT, dep, r["base"])
    elif wlroots_repo is not None:
        raise MaterializationBlocked("manifest has no active wlroots repository")
    evidence, status = _materialize_at(parent, GITLINK_PATH, child, child_head)
    if r is not None:
        nested["parent_candidate"], _ = _materialize_at(parent / GITLINK_PATH, WLROOTS_ROOT, dep, rhead)
    return {
        "schema_version": 2, "kind": "treeland-unified-child-materialization", "outcome": "pass",
        "status": status, "manifest_sha256": canonical_json_sha256(manifest),
        "parent_head": parent_head, "child_head": child_head, "gitlink_path": GITLINK_PATH,
        "checkout": evidence, "wlroots_head": manifest.get("final_wlroots_head"),
        "wlroots_checkouts": nested, "blocked_reasons": [],
    }


def _parent_materialization_errors(record, manifest):
    identity = manifest.get("identity") or {}
    parent = identity.get("parent_worktree")
    path = str((Path(parent) / GITLINK_PATH).resolve()) if isinstance(parent, str) else None
    expected = {"manifest_sha256": canonical_json_sha256(manifest),
                "parent_head": manifest.get("final_parent_head"),
                "child_head": manifest.get("final_child_head"), "gitlink_path": GITLINK_PATH,
                "checkout": {"path": path, "head": manifest.get("final_child_head"),
                             "common_git_dir": identity.get("child_common_git_dir"),
                             "linked_worktree": True, "clean": True}}
    return [f"child materialization {key} differs from manifest" for key, value in expected.items()
            if record.get(key) != value]


def recursive_materialization_errors(record, manifest, source_before):
    """让完整报告核对 C 基线、C 候选、P 候选的每个 R 物化工件。"""

    identity = manifest.get("identity", {})
    r = identity.get("wlroots")
    if not isinstance(record, dict):
        return ["recursive materialization evidence is missing"]
    errors = _parent_materialization_errors(record, manifest)
    if record.get("wlroots_head") != manifest.get("final_wlroots_head"):
        errors.append("recursive materialization wlroots HEAD differs from manifest")
    expected = {"child_base": None, "child_candidate": None, "parent_candidate": None}
    if isinstance(r, dict):
        locations = {"child_candidate": (identity["child_worktree"], manifest["final_wlroots_head"]),
                     "parent_candidate": (str(Path(identity["parent_worktree"]) / GITLINK_PATH), manifest["final_wlroots_head"])}
        if r.get("registered_at_base"):
            if not isinstance(source_before, str):
                return errors + ["recursive materialization needs the audited child baseline worktree"]
            locations["child_base"] = (source_before, r["base"])
        for name, (owner, head) in locations.items():
            expected[name] = {"path": str(Path(owner) / WLROOTS_ROOT), "head": head,
                              "common_git_dir": r["common_git_dir"], "clean": True,
                              "linked_worktree": True}
    if record.get("wlroots_checkouts") != expected:
        errors.append("recursive materialization checkout set differs from the frozen C/P/R identities")
    return errors


__all__ = ["MaterializationBlocked", "materialize_child_checkout"]
