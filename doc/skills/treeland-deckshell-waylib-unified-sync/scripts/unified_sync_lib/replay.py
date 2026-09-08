"""Journaled child-first replay orchestration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Dict, Mapping, Optional

from .artifacts import artifact_errors, read_verified_artifact
from .contracts import source_contract_audit_errors
from .git_ops import (
    atomic_write_json,
    resolve_commit,
    run_git,
)
from .journal import add_event, load_journal, new_journal, save_journal
from .patches import tree_entry
from .replay_outputs import build_evidence_documents, build_manifest, build_wlroots_evidence
from .replay_preflight import build_replay_identity, run_static_preflight
from .replay_stages import child_stage, parent_stage, wlroots_stage
from .replay_types import ReplayBlocked, ReplayRequest
from .schema import CHILD_CLASSIFICATIONS
from .wlroots import nested_transition, required_by_inventory, updater_guard_errors, wlroots_source_audit
from .schema import WLROOTS_ROOT


StageHook = Callable[[str, str, str], None]


def _require_wlroots_audit(request, item, node):
    lane, artifacts = node["wlroots"], node["artifacts"]["wlroots"]
    _, content = read_verified_artifact(artifacts.get("source_audit"), request.artifact_root, "wlroots source audit")
    expected = wlroots_source_audit(request.source_repo, request.wlroots_worktree, item, lane["commit"],
                                    lane["action"], lane.get("adaptation_paths", []), artifacts, request.artifact_root)
    if json.loads(content.decode("utf-8")) != expected or expected["outcome"] != "pass":
        raise ReplayBlocked("wlroots source audit failed: " + "; ".join(expected["blocked_reasons"]))


def _require_child_contract_audit(
    request: ReplayRequest, node: Mapping[str, Any], source: str
) -> None:
    child = node.get("child", {})
    artifacts = node.get("artifacts", {}).get("child", {})
    commit = child.get("commit") if isinstance(child, dict) else None
    record = artifacts.get("source_contract_audit") if isinstance(artifacts, dict) else None
    errors = artifact_errors(record, request.artifact_root, "child source contract audit")
    errors.extend(updater_guard_errors(request.source_repo, source, request.child_worktree, str(commit), f"{commit}^"))
    if not errors:
        try:
            _path, content = read_verified_artifact(
                record, request.artifact_root, "child source contract audit"
            )
            audit = json.loads(content.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as error:
            errors.append(f"child source contract audit is invalid JSON: {error}")
        else:
            errors.extend(
                source_contract_audit_errors(
                    request.child_worktree, f"{commit}^", str(commit), audit
                )
            )
    if errors:
        raise ReplayBlocked("; ".join(errors))


def _require_clean_head(repo: Path, expected: str, label: str) -> None:
    actual = resolve_commit(repo, "HEAD")
    if actual != expected:
        raise ReplayBlocked(f"{label} HEAD mismatch: expected {expected}, got {actual}")
    status = str(run_git(repo, "status", "--porcelain=v1", "--untracked-files=all"))
    if status:
        raise ReplayBlocked(f"{label} linked worktree is not clean")


def _checkpoint_history_errors(
    request: ReplayRequest, journal: Mapping[str, Any]
) -> list:
    errors = []
    nodes = journal["nodes"]
    lanes = [
        ("parent", request.parent_worktree, request.parent_base, journal["current_parent_head"]),
        ("child", request.child_worktree, request.child_base, journal["current_child_head"]),
    ]
    if request.wlroots_worktree is not None:
        lanes.append(("wlroots", request.wlroots_worktree, request.wlroots_base, journal["current_wlroots_head"]))
    for lane, repo, base, head in lanes:
        expected = [
            nodes[item["source_commit"]][lane]["commit"]
            for item in request.inventory["commits"]
            if nodes[item["source_commit"]][lane]["commit"]
        ]
        actual = str(run_git(repo, "rev-list", "--reverse", f"{base}..{head}")).split()
        if actual != expected:
            errors.append(f"{lane} history differs from replay journal checkpoints")
    expected_gitlink = resolve_commit(request.child_worktree, request.child_base)
    for item in request.inventory["commits"]:
        node = nodes[item["source_commit"]]
        if node["parent"]["commit"]:
            expected_gitlink = node["gitlink"].get("to")
    actual_gitlink = tree_entry(
        request.parent_worktree, journal["current_parent_head"], request.gitlink_path
    )
    if not actual_gitlink or actual_gitlink.get("sha") != expected_gitlink:
        errors.append("parent gitlink differs from replay journal checkpoints")
    errors.extend(_checkpoint_dependency_errors(request, journal))
    return errors


def _checkpoint_dependency_errors(request, journal):
    identity = journal["identity"]
    r = identity.get("wlroots")
    current_r = r["base"] if r else None
    current_c, parent_c = identity["child_base"], identity["child_base"]
    errors = []
    for item in request.inventory["commits"]:
        node = journal["nodes"][item["source_commit"]]
        rcommit, ccommit, pcommit = [node[lane]["commit"] for lane in ("wlroots", "child", "parent")]
        if rcommit:
            if resolve_commit(request.wlroots_worktree, rcommit + "^") != current_r:
                errors.append("wlroots checkpoint parent differs from replay order")
            current_r = rcommit
        if ccommit:
            if resolve_commit(request.child_worktree, ccommit + "^") != current_c:
                errors.append("child checkpoint parent differs from replay order")
            current_c = ccommit
            expected = None
            if r and (tree_entry(request.child_worktree, ccommit, WLROOTS_ROOT)
                      or required_by_inventory({"commits": [item]})):
                expected = nested_transition(request.child_worktree, ccommit + "^", ccommit,
                                             current_r, r["submodule_url"])
            if node.get("nested_gitlink") != expected:
                errors.append("nested gitlink differs from replay checkpoint Git objects")
        if pcommit:
            link = tree_entry(request.parent_worktree, pcommit, request.gitlink_path)
            expected = {"status": "updated" if ccommit else "unchanged", "from": parent_c, "to": current_c}
            if not link or link["mode"] != "160000" or link["sha"] != current_c or node["gitlink"] != expected:
                errors.append("parent gitlink differs from completed child checkpoint")
            parent_c = current_c
    return errors


def _resume_journal(
    request: ReplayRequest, identity: Mapping[str, Any]
) -> Dict[str, Any]:
    if not request.journal_path.is_file():
        raise ReplayBlocked("resume requested but replay journal is missing")
    try:
        journal = load_journal(
            request.journal_path, identity, request.inventory["commits"]
        )
    except ValueError as error:
        raise ReplayBlocked(str(error)) from error
    _require_clean_head(
        request.parent_worktree, journal["current_parent_head"], "parent"
    )
    _require_clean_head(request.child_worktree, journal["current_child_head"], "child")
    if request.wlroots_worktree is not None:
        _require_clean_head(request.wlroots_worktree, journal["current_wlroots_head"], "wlroots")
    errors = _checkpoint_history_errors(request, journal)
    if errors:
        raise ReplayBlocked("; ".join(errors))
    journal["blocked"] = None
    journal["outcome"] = "running"
    add_event(journal, "", "resume", "started")
    save_journal(request.journal_path, journal)
    return journal


def _new_journal(
    request: ReplayRequest, identity: Mapping[str, Any]
) -> Dict[str, Any]:
    if request.journal_path.exists():
        raise ReplayBlocked("replay journal already exists; use explicit resume")
    for output in (
        request.manifest_path,
        request.waylib_evidence_path,
        request.parent_evidence_path,
        request.wlroots_evidence_path,
    ):
        if output.exists():
            raise ReplayBlocked(f"output already exists: {output}")
    _require_clean_head(request.parent_worktree, identity["parent_base"], "parent")
    _require_clean_head(request.child_worktree, identity["child_base"], "child")
    if identity.get("wlroots"):
        _require_clean_head(request.wlroots_worktree, identity["wlroots"]["base"], "wlroots")
    initial = tree_entry(request.parent_worktree, identity["parent_base"], request.gitlink_path)
    if not initial or initial["mode"] != "160000" or initial["sha"] != identity["child_base"]:
        raise ReplayBlocked("parent baseline gitlink must equal the child baseline commit")
    request.artifact_root.mkdir(parents=True, exist_ok=True)
    journal = new_journal(identity, request.inventory["commits"])
    save_journal(request.journal_path, journal)
    return journal


def _checkpoint_lane(
    request: ReplayRequest,
    journal: Dict[str, Any],
    source_sha: str,
    lane: str,
    commit: str,
    action: str,
    notes,
    adaptation_paths,
    artifacts,
    details=None,
) -> None:
    sequence = add_event(journal, source_sha, lane, "complete", commit)
    node = journal["nodes"][source_sha]
    node[lane] = {
        "commit": commit,
        "action": action,
        "sequence": sequence,
        "adaptation_notes": notes,
        "adaptation_paths": adaptation_paths,
    }
    node["artifacts"][lane] = artifacts
    if details is not None:
        node[lane].update({key: value for key, value in details.items() if key != "nested_gitlink"})
        node["nested_gitlink"] = details.get("nested_gitlink")
    journal[f"current_{lane}_head"] = commit
    node["status"] = {"wlroots": "wlroots-complete", "child": "child-complete", "parent": "complete"}[lane]
    save_journal(request.journal_path, journal)


def _complete_skip(
    request: ReplayRequest, journal: Dict[str, Any], source_sha: str
) -> None:
    node = journal["nodes"][source_sha]
    if node["status"] == "complete":
        return
    add_event(journal, source_sha, "unowned-skip", "complete")
    current = tree_entry(request.parent_worktree, "HEAD", request.gitlink_path)
    node["gitlink"] = {
        "status": "unchanged",
        "from": current["sha"] if current else None,
        "to": current["sha"] if current else None,
    }
    node["status"] = "complete"
    save_journal(request.journal_path, journal)


def _finish(request: ReplayRequest, journal: Dict[str, Any]) -> Dict[str, Any]:
    manifest = build_manifest(request, journal)
    child_evidence, parent_evidence = build_evidence_documents(request, journal)
    atomic_write_json(request.waylib_evidence_path, child_evidence)
    atomic_write_json(request.parent_evidence_path, parent_evidence)
    atomic_write_json(request.wlroots_evidence_path, build_wlroots_evidence(request, journal))
    atomic_write_json(request.manifest_path, manifest)
    journal["outcome"] = "pass"
    journal["blocked"] = None
    save_journal(request.journal_path, journal)
    return manifest


def _record_block(
    request: ReplayRequest,
    journal: Dict[str, Any],
    source_sha: str,
    stage: str,
    error: Exception,
) -> None:
    journal["outcome"] = "blocked"
    journal["blocked"] = {
        "source_commit": source_sha,
        "stage": stage,
        "reason": str(error),
    }
    add_event(journal, source_sha, stage, "blocked", detail=str(error))
    save_journal(request.journal_path, journal)


def _checkpoint_parent(request, item, node, journal, stage_hook):
    current_source = item["source_commit"]
    commit, action, notes, adaptation_paths, artifacts, gitlink = parent_stage(
        request, item, node["child"]["commit"]
    )
    node["gitlink"] = gitlink
    _checkpoint_lane(
        request,
        journal,
        current_source,
        "parent",
        commit,
        action,
        notes,
        adaptation_paths,
        artifacts,
    )
    if stage_hook:
        stage_hook("parent", current_source, commit)


def run_replay(
    request: ReplayRequest,
    resume: bool = False,
    stage_hook: Optional[StageHook] = None,
) -> Dict[str, Any]:
    """Replay a frozen inventory in source order with child-first checkpoints."""

    run_static_preflight(request)
    identity = build_replay_identity(request)
    journal = _resume_journal(request, identity) if resume else _new_journal(request, identity)
    current_source = ""
    current_stage = "preflight"
    try:
        for item in request.inventory["commits"]:
            current_source = item["source_commit"]
            node = journal["nodes"][current_source]
            if item["classification"] == "unowned-skip":
                _complete_skip(request, journal, current_source)
                continue
            if item["wlroots"]["included"]:
                if not node["wlroots"]["commit"]:
                    current_stage = "wlroots"
                    commit, action, notes, adaptation_paths, artifacts = wlroots_stage(request, item)
                    _checkpoint_lane(request, journal, current_source, "wlroots", commit, action, notes, adaptation_paths, artifacts)
                    if stage_hook:
                        stage_hook("wlroots", current_source, commit)
                current_stage = "wlroots-contract"
                _require_wlroots_audit(request, item, node)
            if item["classification"] in CHILD_CLASSIFICATIONS and not node["child"]["commit"]:
                current_stage = "child"
                commit, action, notes, adaptation_paths, artifacts, details = child_stage(
                    request, item, journal["current_wlroots_head"]
                )
                _checkpoint_lane(
                    request, journal, current_source, "child", commit,
                    action, notes, adaptation_paths, artifacts,
                    details,
                )
                if stage_hook:
                    stage_hook("child", current_source, commit)
            if item["classification"] in CHILD_CLASSIFICATIONS:
                current_stage = "child-contract"
                _require_child_contract_audit(request, node, current_source)
            if not node["parent"]["commit"]:
                current_stage = "parent"
                _checkpoint_parent(request, item, node, journal, stage_hook)
        return _finish(request, journal)
    except Exception as error:
        _record_block(request, journal, current_source, current_stage, error)
        if isinstance(error, ReplayBlocked):
            raise
        raise ReplayBlocked(str(error)) from error


__all__ = ["ReplayBlocked", "ReplayRequest", "run_replay"]
