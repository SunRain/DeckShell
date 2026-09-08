"""Child and parent lane replay stages."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from .artifacts import artifact_errors, read_verified_artifact, write_artifact
from .contracts import build_source_contract_audit
from .git_ops import run_git, stable_unique
from .messages import child_message, parent_message
from .patches import (
    apply_index_patch,
    commit_diff,
    create_commit,
    enforce_staged_paths,
    source_metadata,
    source_patch,
    tree_entry,
    update_gitlink,
)
from .replay_types import ReplayBlocked, ReplayRequest
from .schema import LANE_ACTIONS, WLROOTS_ROOT
from .wlroots import blob, stage_wlroots_gitlink, updater_guard_errors, wlroots_source_audit


def _decision(
    request: ReplayRequest, source_sha: str, lane: str, default_action: str
) -> Tuple[str, List[str], List[Dict[str, Any]], Mapping[str, Any]]:
    entries = request.decisions.get("entries", request.decisions)
    source_decision = entries.get(source_sha, {}) if isinstance(entries, dict) else {}
    lane_decision = source_decision.get(lane, {}) if isinstance(source_decision, dict) else {}
    if not isinstance(lane_decision, dict):
        raise ReplayBlocked(f"decision for {source_sha}/{lane} must be an object")
    action = lane_decision.get("action", default_action)
    if not isinstance(action, str) or action not in LANE_ACTIONS:
        raise ReplayBlocked(f"unsupported {lane} action for {source_sha}: {action}")
    notes = lane_decision.get("adaptation_notes", ["none"])
    if not isinstance(notes, list) or not all(isinstance(item, str) for item in notes):
        raise ReplayBlocked(f"adaptation_notes for {source_sha}/{lane} must be strings")
    if action == "adapted" and not any(item.strip().lower() != "none" for item in notes):
        raise ReplayBlocked(f"adapted action requires notes for {source_sha}/{lane}")
    adaptation_paths = lane_decision.get("adaptation_paths", [])
    return action, notes or ["none"], list(adaptation_paths), lane_decision


def _decision_artifact(
    request: ReplayRequest,
    decision: Mapping[str, Any],
    name: str,
    label: str,
) -> Tuple[Mapping[str, Any], bytes]:
    record = decision.get(name)
    errors = artifact_errors(record, request.artifact_root, label)
    if errors:
        raise ReplayBlocked("; ".join(errors))
    _path, content = read_verified_artifact(record, request.artifact_root, label)
    return record, content


def _write_source_patch(
    request: ReplayRequest,
    source_sha: str,
    lane: str,
    name: str,
    paths: Sequence[str],
) -> Tuple[Dict[str, Any], bytes]:
    content = source_patch(request.source_repo, source_sha, paths, WLROOTS_ROOT if lane == "wlroots" else None)
    relative = f"commits/{source_sha}/{lane}-{name}.patch"
    return write_artifact(request.artifact_root, relative, content), content


def _apply_file_patch(request, repo, source_sha, lane, action, decision, patch, artifacts):
    if action == "applied":
        if patch:
            apply_index_patch(repo, patch)
        return
    if action == "not-applicable":
        return
    name = "adaptation_patch" if action == "adapted" else "equivalence_proof"
    record, content = _decision_artifact(request, decision, name, f"{source_sha}/{lane} {name}")
    artifacts[name] = dict(record)
    if action == "adapted":
        apply_index_patch(repo, content)


def wlroots_stage(request: ReplayRequest, item: Mapping[str, Any]):
    """先在独立 R 仓库产生真实来源提交，绝不使用来源 tree SHA 作为 gitlink。"""

    source_sha = item["source_commit"]
    action, notes, adaptations, decision = _decision(request, source_sha, "wlroots", "applied")
    record, patch = _write_source_patch(request, source_sha, "wlroots", "source", item["wlroots"]["source_paths"])
    artifacts = {"source_patch": record}
    repo = request.wlroots_worktree
    _apply_file_patch(request, repo, source_sha, "wlroots", action, decision, patch, artifacts)
    paths = set(item["wlroots"]["target_paths"])
    actual = enforce_staged_paths(repo, paths, paths if action == "applied" else set(), f"{source_sha}/wlroots")
    if (action == "empty" and actual) or (action == "adapted" and not actual):
        raise ReplayBlocked("wlroots action disagrees with staged content")
    metadata = source_metadata(request.source_repo, source_sha)
    message = child_message(metadata["subject"], metadata["message"], source_sha, item["classification"],
                            action, item["wlroots"]["drop_paths"], adaptations, notes, request.run_id,
                            request.refs_doc, lane="wlroots")
    commit = create_commit(repo, metadata, message, allow_empty=action == "empty")
    artifacts["target_diff"] = write_artifact(request.artifact_root, f"commits/{source_sha}/wlroots-target.diff", commit_diff(repo, commit))
    audit = wlroots_source_audit(request.source_repo, repo, item, commit, action, adaptations, artifacts, request.artifact_root)
    artifacts["source_audit"] = write_artifact(request.artifact_root, f"commits/{source_sha}/wlroots-source-audit.json", (json.dumps(audit, sort_keys=True) + "\n").encode())
    return commit, action, notes, adaptations, artifacts


def _wrapper_safety(request, item):
    if request.wlroots_worktree is None:
        return
    staged = str(run_git(request.child_worktree, "write-tree")).strip()
    errors = updater_guard_errors(request.source_repo, item["source_commit"], request.child_worktree, staged, "HEAD")
    if errors:
        raise ReplayBlocked("; ".join(errors))
    if "wlroots/UPSTREAM" in item["waylib_shared"]["source_paths"]:
        original = blob(request.source_repo, item["source_commit"], "wlroots/UPSTREAM")
        target = request.child_worktree / "wlroots/UPSTREAM"
        if original is not None and target.is_file():
            def pins(content):
                result = {}
                for line in content.decode("utf-8").splitlines():
                    key, sep, value = line.partition("=")
                    if sep and key in {"SOURCE_URL", "REF", "COMMIT", "VERSION"}:
                        result[key] = value.strip()
                return result
            if pins(original) != pins(target.read_bytes()):
                raise ReplayBlocked("UPSTREAM pure-source pin must not be replaced with a target commit")


def child_stage(request: ReplayRequest, item: Mapping[str, Any], wlroots_sha: Optional[str] = None):
    """把 C 普通内容与同一来源的 R gitlink 原子地放入同一个 C 提交。"""

    source_sha = item["source_commit"]
    action, notes, adaptations, decision = _decision(request, source_sha, "child", "applied")
    paths = item["waylib_shared"]["source_paths"]
    structural = decision.get("structural_paths", [])
    content_action = "not-applicable" if not paths and not decision else action
    record, patch = _write_source_patch(request, source_sha, "child", "source", paths)
    artifacts: Dict[str, Any] = {"source_patch": record}
    _apply_file_patch(request, request.child_worktree, source_sha, "child", content_action, decision, patch, artifacts)
    allowed = set(paths) | set(structural)
    actual = enforce_staged_paths(request.child_worktree, allowed, set(paths) if content_action == "applied" else set(), f"{source_sha}/child")
    if (content_action == "adapted" and not actual) or (content_action == "empty" and actual):
        raise ReplayBlocked("child content action disagrees with staged content")
    nested = stage_wlroots_gitlink(request, item, wlroots_sha) if wlroots_sha else None
    _wrapper_safety(request, item)
    if nested and nested["status"] != "unchanged":
        allowed.add(WLROOTS_ROOT)
        notes = list(notes) + [f"Includes wlroots submodule update to {wlroots_sha}."]
        if nested["status"] == "registered":
            allowed.add(".gitmodules")
            action = "adapted"
            notes.append("首次登记 3rdparty/wlroots 子模块；.gitmodules 是显式结构适配，不是纯 gitlink 变更。")
        elif not actual:
            action = "gitlink-only"
    elif content_action == "not-applicable":
        raise ReplayBlocked("child dependency-only node has no gitlink change")
    actual_all = enforce_staged_paths(request.child_worktree, allowed, set(actual), f"{source_sha}/child")
    metadata = source_metadata(request.source_repo, source_sha)
    message = child_message(metadata["subject"], metadata["message"], source_sha, item["classification"],
                            action, item["waylib_shared"]["drop_paths"], adaptations, notes, request.run_id,
                            request.refs_doc, content_action=content_action, nested_gitlink=nested)
    commit = create_commit(request.child_worktree, metadata, message, allow_empty=not actual_all)
    artifacts["target_diff"] = write_artifact(request.artifact_root, f"commits/{source_sha}/child-target.diff", commit_diff(request.child_worktree, commit))
    approval = None
    if "contract_additions" in decision:
        record, content = _decision_artifact(request, decision, "contract_additions", "child contract additions")
        approval = json.loads(content.decode("utf-8"))
        artifacts["contract_additions"] = dict(record)
    audit = build_source_contract_audit(request.child_worktree, f"{commit}^", commit, approval)
    artifacts["source_contract_audit"] = write_artifact(request.artifact_root, f"commits/{source_sha}/child-source-contract-audit.json", (json.dumps(audit, ensure_ascii=True, indent=2) + "\n").encode())
    details = {"content_action": content_action, "structural_paths": structural, "nested_gitlink": nested}
    return commit, action, notes, adaptations, artifacts, details


def _parent_path_mappings(item: Mapping[str, Any]) -> List[str]:
    mappings: List[str] = []
    for change in item.get("changes", []):
        sides = (change.get("new"),) if str(change.get("status", "")).startswith("C") else (
            change.get("old"),
            change.get("new"),
        )
        for side in sides:
            if side and side.get("category") in {"mapped", "root-owned"}:
                mappings.append(f"{side['source']} -> {side['target']}")
    return stable_unique(mappings)


def _apply_generated_parent_patches(
    request: ReplayRequest,
    source_sha: str,
    parent: Mapping[str, Any],
    mapped_patch: bytes,
    root_patch: bytes,
) -> None:
    mapped = parent["mapped_source_paths"]
    roots = parent["root_source_paths"]
    if mapped:
        expected = {f"compositor/{path}" for path in mapped}
        actual = set(parent["target_paths"]) - set(roots)
        if actual != expected:
            raise ReplayBlocked(f"unsupported non-canonical mapped target for {source_sha}")
        apply_index_patch(request.parent_worktree, mapped_patch, "compositor")
    if roots:
        if not set(roots).issubset(set(parent["target_paths"])):
            raise ReplayBlocked(f"root-owned target mapping drift for {source_sha}")
        apply_index_patch(request.parent_worktree, root_patch)


def _apply_parent_content(
    request: ReplayRequest,
    item: Mapping[str, Any],
    action: str,
    decision: Mapping[str, Any],
) -> Dict[str, Any]:
    source_sha = item["source_commit"]
    parent = item["deckshell"]
    mapped_record, mapped_patch = _write_source_patch(
        request, source_sha, "parent", "mapped-source", parent["mapped_source_paths"]
    )
    root_record, root_patch = _write_source_patch(
        request, source_sha, "parent", "root-source", parent["root_source_paths"]
    )
    artifacts: Dict[str, Any] = {
        "mapped_source_patch": mapped_record,
        "root_source_patch": root_record,
    }
    if action == "applied":
        _apply_generated_parent_patches(
            request, source_sha, parent, mapped_patch, root_patch
        )
        return artifacts
    artifact_name = "adaptation_patch" if action == "adapted" else "equivalence_proof"
    record, content = _decision_artifact(
        request, decision, artifact_name, f"{source_sha}/parent {artifact_name}"
    )
    artifacts[artifact_name] = dict(record)
    if action == "adapted":
        apply_index_patch(request.parent_worktree, content)
    return artifacts


def _verify_parent_staging(
    request: ReplayRequest,
    item: Mapping[str, Any],
    action: str,
    child_sha: Optional[str],
) -> List[str]:
    source_sha = item["source_commit"]
    allowed = set(item["deckshell"]["target_paths"])
    required: Set[str] = set(allowed) if action == "applied" else set()
    if child_sha:
        allowed.add(request.gitlink_path)
        required.add(request.gitlink_path)
    actual = enforce_staged_paths(
        request.parent_worktree, allowed, required, f"{source_sha}/parent"
    )
    content = set(actual) - {request.gitlink_path}
    if action == "adapted" and not content:
        raise ReplayBlocked(f"adapted parent action has no staged content: {source_sha}")
    if action == "empty" and content:
        raise ReplayBlocked(f"empty parent action staged content: {source_sha}")
    return actual


def _create_parent_commit(
    request: ReplayRequest,
    item: Mapping[str, Any],
    child_sha: Optional[str],
    action: str,
    adaptation_paths: List[Dict[str, Any]],
    notes: List[str],
    actual_paths: List[str],
) -> str:
    source_sha = item["source_commit"]
    metadata = source_metadata(request.source_repo, source_sha)
    message = parent_message(
        metadata["subject"], metadata["message"], source_sha,
        item["classification"], action, item["deckshell"]["drop_paths"],
        _parent_path_mappings(item), adaptation_paths, notes, child_sha,
        request.run_id, request.refs_doc,
    )
    return create_commit(
        request.parent_worktree, metadata, message, allow_empty=not actual_paths
    )


def parent_stage(
    request: ReplayRequest,
    item: Mapping[str, Any],
    child_sha: Optional[str],
) -> Tuple[str, str, List[str], List[Dict[str, Any]], Dict[str, Any], Dict[str, Any]]:
    """Apply parent content, update its gitlink, and create one commit."""

    source_sha = item["source_commit"]
    before = tree_entry(request.parent_worktree, "HEAD", request.gitlink_path)
    if not before or before["mode"] != "160000":
        raise ReplayBlocked(f"missing valid parent gitlink before {source_sha}")
    if item["classification"] == "waylib-only":
        action = "gitlink-only"
        notes = ["DeckShell contains only the gitlink update.", "这是一个单纯的 gitlink 变更。"]
        adaptation_paths: List[Dict[str, Any]] = []
        artifacts: Dict[str, Any] = {}
    else:
        action, notes, adaptation_paths, decision = _decision(
            request, source_sha, "parent", "applied"
        )
        artifacts = _apply_parent_content(request, item, action, decision)
    if child_sha:
        update_gitlink(request.parent_worktree, request.gitlink_path, child_sha)
        notes = list(notes) + [f"Includes waylib-shared update to {child_sha}.", "此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。"]
    actual = _verify_parent_staging(request, item, action, child_sha)
    commit = _create_parent_commit(
        request, item, child_sha, action, adaptation_paths, notes, actual
    )
    after = tree_entry(request.parent_worktree, commit, request.gitlink_path)
    expected_sha = child_sha or before["sha"]
    if not after or after["mode"] != "160000" or after["sha"] != expected_sha:
        raise ReplayBlocked(f"parent commit has an invalid gitlink after {source_sha}")
    artifacts["target_diff"] = write_artifact(
        request.artifact_root,
        f"commits/{source_sha}/parent-target.diff",
        commit_diff(request.parent_worktree, commit),
    )
    gitlink = {
        "status": "updated" if child_sha else "unchanged",
        "from": before["sha"],
        "to": after["sha"],
    }
    return commit, action, notes, adaptation_paths, artifacts, gitlink
