"""Gitlink consistency verification."""

from __future__ import annotations

from .protocol_update import companion_lane_errors, replay_head

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple

from .git_ops import changed_paths
from .git_ops import (
    GitError,
    canonical_repo,
    commit_changes,
    git_succeeds,
    resolve_commit,
    run_git,
    sha256_bytes,
    stable_unique,
)
from .patches import tree_entry
from .replay_types import GITLINK_PATH
from .schema import CHILD_CLASSIFICATIONS, is_full_sha
from .schema import WLROOTS_ROOT, inventory_errors
from .git_ops import canonical_json_sha256, common_git_dir
from .wlroots import baseline_projection, nested_transition, registration, required_by_inventory


def _commit_paths(repo: Path, commit: str) -> List[str]:
    paths: List[str] = []
    for change in commit_changes(repo, commit):
        paths.extend(changed_paths(change))
    return stable_unique(paths)


def _history(repo: Path, base: str, head: str) -> List[str]:
    if not git_succeeds(repo, "merge-base", "--is-ancestor", base, head):
        raise ValueError(f"target base is not an ancestor of head: {base}..{head}")
    return str(run_git(repo, "rev-list", "--reverse", f"{base}..{head}")).split()


def _manifest_shape_errors(manifest: Mapping[str, Any]) -> List[str]:
    errors: List[str] = []
    if manifest.get("schema_version") != 2:
        errors.append("manifest schema_version must be 2")
    if manifest.get("kind") != "treeland-unified-sync-manifest":
        errors.append("manifest kind is invalid")
    if manifest.get("outcome") != "pass":
        errors.append("manifest outcome must be pass")
    if not isinstance(manifest.get("entries"), list):
        errors.append("manifest entries must be an array")
    return errors


def _child_object_errors(
    child_repo: Path, child_sha: Any, child_head: str, source_sha: str
) -> List[str]:
    if not is_full_sha(child_sha):
        return [f"child commit must be a full SHA for {source_sha}"]
    object_type = ""
    try:
        object_type = str(run_git(child_repo, "cat-file", "-t", child_sha)).strip()
    except GitError:
        pass
    errors: List[str] = []
    if object_type != "commit":
        errors.append(f"child object is not a commit for {source_sha}: {child_sha}")
    elif not git_succeeds(child_repo, "merge-base", "--is-ancestor", child_sha, child_head):
        errors.append(f"child commit is not reachable from frozen child head: {child_sha}")
    return errors


def _entry_parts(
    item: Mapping[str, Any], source: str
) -> Tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any], List[str]]:
    values = (item.get("child"), item.get("parent"), item.get("gitlink"))
    names = ("child", "parent", "gitlink")
    errors = [
        f"manifest {name} must be an object for {source}"
        for name, value in zip(names, values)
        if not isinstance(value, dict)
    ]
    child, parent, link = (
        value if isinstance(value, dict) else {} for value in values
    )
    return child, parent, link, errors


def _entry_shape_errors(
    parent_repo: Path,
    child_repo: Path,
    item: Mapping[str, Any],
    current_child: str,
    final_parent: str,
    final_child: str,
    gitlink_path: str,
) -> List[str]:
    source = str(item.get("source_commit"))
    classification = item.get("classification")
    child, parent, link, errors = _entry_parts(item, source)
    if errors:
        return errors
    child_sha = child.get("commit")
    parent_sha = parent.get("commit")
    if classification not in {"deckshell-only", "waylib-only", "dual", "unowned-skip"}:
        errors.append(f"manifest classification is invalid for {source}")
        return errors
    child_owned = classification in CHILD_CLASSIFICATIONS
    if child_owned:
        errors.extend(_child_object_errors(child_repo, child_sha, final_child, source))
    elif child_sha is not None:
        errors.append(f"non-child classification has a child commit: {source}")
    if classification == "unowned-skip":
        if parent_sha is not None:
            errors.append(f"unowned-skip has a parent commit: {source}")
        return errors
    if not is_full_sha(parent_sha) or not git_succeeds(
        parent_repo, "merge-base", "--is-ancestor", str(parent_sha), final_parent
    ):
        errors.append(f"parent commit is not reachable for {source}: {parent_sha}")
        return errors
    expected_to = str(child_sha) if child_owned else current_child
    expected_status = "updated" if child_owned else "unchanged"
    if link.get("from") != current_child or link.get("to") != expected_to:
        errors.append(f"gitlink transition mismatch for {source}")
    if link.get("status") != expected_status:
        errors.append(f"gitlink status mismatch for {source}")
    entry = tree_entry(parent_repo, str(parent_sha), gitlink_path)
    if not entry or entry["mode"] != "160000" or entry["type"] != "commit":
        errors.append(f"gitlink must have mode 160000 and type commit for {source}")
    elif entry["sha"] != expected_to:
        errors.append(f"parent tree gitlink SHA mismatch for {source}")
    paths = _commit_paths(parent_repo, str(parent_sha))
    if classification == "waylib-only" and paths != [gitlink_path]:
        errors.append(f"gitlink-only purity violation for {source}: {paths}")
    if classification == "waylib-only" and parent.get("action") != "gitlink-only":
        errors.append(f"waylib-only parent action must be gitlink-only: {source}")
    if classification == "dual" and gitlink_path not in paths:
        errors.append(f"dual parent commit does not update gitlink: {source}")
    if classification == "deckshell-only" and gitlink_path in paths:
        errors.append(f"deckshell-only parent commit changes gitlink: {source}")
    if child_owned and not _child_precedes_parent(child, parent):
        errors.append(f"child stage does not precede parent stage: {source}")
    return errors


def _child_precedes_parent(
    child: Mapping[str, Any], parent: Mapping[str, Any]
) -> bool:
    child_sequence = child.get("sequence")
    parent_sequence = parent.get("sequence")
    return (
        isinstance(child_sequence, int)
        and isinstance(parent_sequence, int)
        and child_sequence < parent_sequence
    )


def _final_gitlink_errors(
    parent_repo: Path,
    final_parent: str,
    expected_child: str,
    gitlink_path: str,
) -> List[str]:
    if not is_full_sha(final_parent):
        return ["final parent gitlink cannot be inspected without a full parent SHA"]
    entry = tree_entry(parent_repo, final_parent, gitlink_path)
    if not entry or entry["mode"] != "160000" or entry["sha"] != expected_child:
        return ["final parent gitlink differs from final child mapping"]
    return []


def _verify_entries(
    parent_repo: Path,
    child_repo: Path,
    entries: Sequence[Any],
    initial_child: str,
    final_parent: str,
    final_child: str,
    gitlink_path: str,
) -> Tuple[List[str], str]:
    errors: List[str] = []
    current_child = initial_child
    for item in entries:
        if not isinstance(item, dict):
            errors.append("manifest entry must be an object")
            continue
        errors.extend(
            _entry_shape_errors(
                parent_repo, child_repo, item, current_child,
                final_parent, final_child, gitlink_path,
            )
        )
        child = item.get("child")
        child_sha = child.get("commit") if isinstance(child, dict) else None
        if item.get("classification") in CHILD_CLASSIFICATIONS and is_full_sha(child_sha):
            current_child = child_sha
    return errors, current_child


def verify_gitlink_consistency(
    parent_repo: Path,
    child_repo: Path,
    parent_base: str,
    child_base: str,
    manifest: Mapping[str, Any],
) -> Dict[str, Any]:
    """Verify gitlink mode, object, reachability, transitions, and purity."""

    parent_repo = canonical_repo(parent_repo)
    child_repo = canonical_repo(child_repo)
    parent_base_sha = resolve_commit(parent_repo, parent_base)
    child_base_sha = resolve_commit(child_repo, child_base)
    blockers = _manifest_shape_errors(manifest)
    final_parent = str(manifest.get("final_parent_head", ""))
    final_child = str(manifest.get("final_child_head", ""))
    entries = manifest.get("entries", []) if isinstance(manifest.get("entries"), list) else []
    if not is_full_sha(final_parent) or not is_full_sha(final_child):
        blockers.append("manifest final heads must be full SHAs")
    initial = tree_entry(parent_repo, parent_base_sha, GITLINK_PATH)
    if not initial or initial["mode"] != "160000" or initial["sha"] != child_base_sha:
        blockers.append("parent baseline gitlink differs from child baseline")
    entry_errors, current_child = _verify_entries(
        parent_repo, child_repo, entries, child_base_sha,
        final_parent, final_child, GITLINK_PATH,
    )
    blockers.extend(entry_errors)
    blockers.extend(
        _history_alignment_errors(
            parent_repo, child_repo, parent_base_sha, child_base_sha,
            replay_head(manifest, "parent"), replay_head(manifest, "child"), entries,
        )
    )
    update = manifest.get("protocol_update")
    if update is not None:
        for lane, repo, head in (("child", child_repo, final_child), ("parent", parent_repo, final_parent)):
            if update.get(lane, {}).get("head") != head:
                blockers.append(f"protocol {lane} companion differs from the final head")
            blockers.extend(companion_lane_errors(repo, update, lane))
        if update.get("child", {}).get("base") != current_child:
            blockers.append("protocol companion does not start at the ordinary child replay head")
        current_child = final_child
    blockers.extend(
        _final_gitlink_errors(parent_repo, final_parent, current_child, GITLINK_PATH)
    )
    blockers = stable_unique(blockers)
    return {
        "schema_version": 2,
        "kind": "treeland-unified-gitlink-verify",
        "parent_base": parent_base_sha,
        "child_base": child_base_sha,
        "final_parent_head": final_parent,
        "final_child_head": final_child,
        "manifest_sha256": _mapping_digest(manifest),
        "verified_gitlink_updates": sum(
            isinstance(item, dict)
            and isinstance(item.get("gitlink"), dict)
            and item["gitlink"].get("status") == "updated"
            for item in entries
        ),
        "blocked_reasons": blockers,
        "outcome": "blocked" if blockers else "pass",
    }


def _history_alignment_errors(
    parent_repo: Path,
    child_repo: Path,
    parent_base: str,
    child_base: str,
    final_parent: str,
    final_child: str,
    entries: Sequence[Any],
) -> List[str]:
    errors: List[str] = []
    expected_parent = [
        item["parent"].get("commit")
        for item in entries
        if isinstance(item, dict)
        and isinstance(item.get("parent"), dict)
        and item["parent"].get("commit")
    ]
    expected_child = [
        item["child"].get("commit")
        for item in entries
        if isinstance(item, dict)
        and isinstance(item.get("child"), dict)
        and item["child"].get("commit")
    ]
    try:
        if _history(parent_repo, parent_base, final_parent) != expected_parent:
            errors.append("parent history differs from manifest order")
        if _history(child_repo, child_base, final_child) != expected_child:
            errors.append("child history differs from manifest order")
    except (GitError, ValueError) as error:
        errors.append(str(error))
    return errors


def _mapping_digest(payload: Mapping[str, Any]) -> str:
    content = json.dumps(
        payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(content)

__all__ = ["verify_gitlink_consistency"]


def _nested_replay_entries(child, repo, inventory, manifest, r, base, head):
    errors = []
    current = base
    commits = []
    previous_sequence = 0
    if [x.get("source_commit") for x in manifest["entries"]] != inventory["range"]["ordered_source_commits"]:
        errors.append("nested manifest source order mismatch")
    for source, node in zip(inventory["commits"], manifest["entries"]):
        rlane, clane = node.get("wlroots", {}), node.get("child", {})
        if bool(rlane.get("commit")) != bool(source["wlroots"]["included"]):
            errors.append("wlroots source/target inclusion mismatch")
        sequence = [node.get(lane, {}).get("sequence") for lane in ("wlroots", "child", "parent") if node.get(lane, {}).get("commit")]
        if any(type(value) is not int or value <= previous_sequence for value in sequence) or sequence != sorted(set(sequence)):
            errors.append("three-repository sequence is not source-ordered child-first")
        elif sequence:
            previous_sequence = sequence[-1]
        if rlane.get("commit"):
            errors.extend(_child_object_errors(repo, rlane["commit"], head, source["source_commit"]))
            current = rlane["commit"]
            commits.append(current)
        if clane.get("commit"):
            existing = tree_entry(child, clane["commit"], WLROOTS_ROOT)
            if existing is not None or required_by_inventory({"commits": [source]}):
                expected = nested_transition(child, f"{clane['commit']}^", clane["commit"], current, r["submodule_url"])
                if node.get("nested_gitlink") != expected:
                    errors.append("nested gitlink record differs from the actual C commit")
                if clane.get("action") == "gitlink-only" and _commit_paths(child, clane["commit"]) != [WLROOTS_ROOT]:
                    errors.append("nested gitlink-only purity violation")
                if expected["status"] == "registered" and clane.get("action") != "adapted":
                    errors.append("first registration must be an adapted child commit")
            elif node.get("nested_gitlink") is not None:
                errors.append("unexpected nested gitlink record")
    return errors, current, commits


def verify_nested_gitlink_consistency(child_repo, wlroots_repo, inventory, manifest, artifact_root):
    """核验 R 的实际提交链及每一条 C→R 边，不接受只在区间末尾补指针。"""

    errors = _manifest_shape_errors(manifest) + inventory_errors(inventory)
    identity = manifest.get("identity", {})
    r = identity.get("wlroots")
    active = r is not None
    result = {
        "schema_version": 2, "kind": "treeland-unified-nested-gitlink-verify",
        "manifest_sha256": canonical_json_sha256(manifest),
        "inventory_sha256": canonical_json_sha256(inventory),
        "status": "verified" if active else "not-applicable",
        "final_child_head": manifest.get("final_child_head"),
        "final_wlroots_head": manifest.get("final_wlroots_head"),
    }
    try:
        child = canonical_repo(child_repo)
        if manifest.get("protocol_update") is not None:
            errors.extend(companion_lane_errors(child, manifest["protocol_update"], "child", artifact_root))
        if not active:
            if required_by_inventory(inventory) or tree_entry(child, manifest["final_child_head"], WLROOTS_ROOT) or manifest.get("final_wlroots_head") is not None:
                errors.append("wlroots cannot be marked not-applicable for this source/target layout")
            registration(child, manifest["final_child_head"], None, "")
        elif not isinstance(r, dict) or wlroots_repo is None:
            errors.append("active wlroots repository is missing")
        else:
            repo = canonical_repo(wlroots_repo)
            if str(common_git_dir(repo)) != r.get("common_git_dir"):
                errors.append("wlroots common Git directory mismatch")
            base, head = r["base"], manifest["final_wlroots_head"]
            initial = registration(child, identity["child_base"], base, r["submodule_url"])
            if bool(initial) != r.get("registered_at_base"):
                errors.append("initial wlroots registration differs from manifest")
            source_tree = baseline_projection(repo, base, Path(inventory["source_repo"]), inventory["range"]["base"], r.get("baseline_proof"), artifact_root)
            if source_tree != r.get("source_base_tree"):
                errors.append("wlroots baseline source tree differs from frozen inventory")
            entry_errors, current, commits = _nested_replay_entries(child, repo, inventory, manifest, r, base, head)
            errors.extend(entry_errors)
            if _history(repo, base, head) != commits or current != head:
                errors.append("wlroots history differs from manifest source order")
            if registration(child, manifest["final_child_head"], head, r["submodule_url"]) is None:
                errors.append("final child has no required wlroots gitlink")
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as error:
        errors.append(f"nested gitlink verification failed: {error}")
    result.update(blocked_reasons=stable_unique(errors), outcome="blocked" if errors else "pass")
    return result
