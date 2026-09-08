"""Immutable replay identity and mutation-free preflight checks."""

from __future__ import annotations

import re
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple

from .adaptations import adaptation_path_errors, lane_target_paths
from .artifacts import artifact_errors
from .git_ops import (
    canonical_json_sha256,
    canonical_repo,
    common_git_dir,
    git_succeeds,
    is_linked_worktree,
    resolve_commit,
    run_git,
    sha256_file,
)
from .replay_types import GITLINK_PATH, ReplayBlocked, ReplayRequest
from .schema import LANE_ACTIONS, inventory_errors
from .wlroots import frozen_wlroots_identity


TRACE_TRAILER = re.compile(r"(?m)^Treeland-Commit: ([0-9a-f]{40})$")
LEGACY_CHERRY_PICK = re.compile(
    r"(?mi)^\(cherry picked from commit ([0-9a-f]{40})\)$"
)
RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,127}$")


def _single_line(value: Any) -> bool:
    return (
        isinstance(value, str)
        and bool(value.strip())
        and not any(ord(character) < 32 or ord(character) == 127 for character in value)
    )


def _message_metadata_errors(request: ReplayRequest) -> List[str]:
    errors: List[str] = []
    if not isinstance(request.run_id, str) or not RUN_ID.fullmatch(request.run_id):
        errors.append("run-id must be a safe single-line identifier")
    if not _single_line(request.refs_doc):
        errors.append("refs-doc must be a non-empty single-line value")
    if request.gitlink_path != GITLINK_PATH:
        errors.append(f"gitlink path must remain {GITLINK_PATH}")
    return errors


def build_replay_identity(request: ReplayRequest) -> Dict[str, Any]:
    """Return the complete immutable identity stored in a replay journal."""

    return {
        "run_id": request.run_id,
        "source_repo": str(request.source_repo.resolve()),
        "parent_worktree": str(request.parent_worktree.resolve()),
        "child_worktree": str(request.child_worktree.resolve()),
        "parent_base": resolve_commit(request.parent_worktree, request.parent_base),
        "child_base": resolve_commit(request.child_worktree, request.child_base),
        "inventory_sha256": canonical_json_sha256(request.inventory),
        "decisions_sha256": canonical_json_sha256(request.decisions),
        "gitlink_path": request.gitlink_path,
        "refs_doc": request.refs_doc,
        "parent_common_git_dir": str(common_git_dir(request.parent_worktree)),
        "child_common_git_dir": str(common_git_dir(request.child_worktree)),
        "wlroots": frozen_wlroots_identity(request),
    }


def _require_output_under_root(path: Path, root: Path) -> None:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError as error:
        raise ReplayBlocked(f"output path is outside artifact root: {path}") from error


def _is_inside(path: Path, possible_parent: Path) -> bool:
    try:
        path.resolve().relative_to(possible_parent.resolve())
        return True
    except ValueError:
        return False


def _decision_entries(
    decisions: Mapping[str, Any]
) -> Tuple[Mapping[str, Any], List[str]]:
    if not decisions:
        return {}, []
    if set(decisions) != {"entries"}:
        return {}, ["decisions must contain only an entries object"]
    entries = decisions.get("entries")
    if not isinstance(entries, dict):
        return {}, ["decisions entries must be an object keyed by source SHA"]
    return entries, []


def _adaptation_note_errors(notes, action, label):
    if not isinstance(notes, list) or not all(isinstance(note, str) for note in notes):
        return [f"{label} adaptation_notes must be a string array"]
    if not notes or not all(_single_line(note) for note in notes):
        return [f"{label} adaptation_notes must contain non-empty single-line values"]
    if action == "adapted" and not any(note.strip().lower() != "none" for note in notes):
        return [f"{label} adapted action requires substantive notes"]
    return []


def _lane_decision_errors(
    source: str,
    lane: str,
    decision: Any,
    expected_paths: List[str],
    artifact_root: Path,
) -> List[str]:
    label = f"decision for {source}/{lane}"
    if not isinstance(decision, dict):
        return [f"{label} must be an object"]
    allowed = {
        "action",
        "adaptation_notes",
        "adaptation_paths",
        "adaptation_patch",
        "equivalence_proof",
        "structural_paths",
        "contract_additions",
    }
    errors = [
        f"{label} has unsupported field: {name}"
        for name in decision
        if name not in allowed
    ]
    action = decision.get("action")
    if not isinstance(action, str) or action not in LANE_ACTIONS:
        return errors + [f"{label} has unsupported action: {action}"]
    if "contract_additions" in decision:
        if lane != "child" or action == "empty":
            errors.append(f"{label} contract additions require a nonempty child action")
        errors.extend(artifact_errors(decision["contract_additions"], artifact_root, f"{label} contract additions"))
    notes = decision.get("adaptation_notes", ["none"])
    errors.extend(_adaptation_note_errors(notes, action, label))
    required = (
        "adaptation_patch"
        if action == "adapted"
        else "equivalence_proof"
        if action == "empty"
        else None
    )
    if required:
        errors.extend(
            artifact_errors(decision.get(required), artifact_root, f"{label} {required}")
        )
    if action == "adapted":
        errors.extend(
            adaptation_path_errors(
                decision.get("adaptation_paths"), expected_paths, artifact_root, label
            )
        )
    elif "adaptation_paths" in decision:
        errors.append(f"{label} must not contain adaptation_paths for {action}")
    forbidden = {"adaptation_patch", "equivalence_proof"} - (
        {required} if required else set()
    )
    errors.extend(
        f"{label} must not contain {name}" for name in forbidden if name in decision
    )
    return errors


def _decision_errors(
    decisions: Mapping[str, Any], inventory: Mapping[str, Any], artifact_root: Path,
    wlroots_active: bool = False,
) -> List[str]:
    entries, errors = _decision_entries(decisions)
    by_source = {
        item.get("source_commit"): item
        for item in inventory.get("commits", [])
        if isinstance(item, dict) and isinstance(item.get("source_commit"), str)
    }
    allowed_lanes = {
        "deckshell-only": {"parent"},
        "waylib-only": {"child"},
        "dual": {"child", "parent"},
        "unowned-skip": set(),
    }
    for source, value in entries.items():
        if source not in by_source:
            errors.append(f"decision references unknown source commit: {source}")
            continue
        if not isinstance(value, dict):
            errors.append(f"decision for {source} must be an object")
            continue
        permitted = set(allowed_lanes.get(by_source[source].get("classification"), set()))
        if by_source[source].get("wlroots", {}).get("included"):
            permitted.add("wlroots")
        errors.extend(
            f"decision for {source} has unsupported lane: {lane}"
            for lane in value
            if lane not in permitted
        )
        for lane in permitted & set(value):
            decision = value[lane]
            extra = decision.get("structural_paths", []) if isinstance(decision, dict) else []
            if extra and (not wlroots_active or lane != "child" or extra != ["CMakeLists.txt"] or decision.get("action") != "adapted"):
                errors.append(f"decision for {source}/{lane} has unauthorized structural paths")
                extra = []
            errors.extend(
                _lane_decision_errors(
                    source,
                    lane,
                    value[lane],
                    lane_target_paths(by_source[source], lane) + (extra if isinstance(extra, list) else []),
                    artifact_root,
                )
            )
    return errors


def _baseline_trace_errors(request: ReplayRequest) -> List[str]:
    expected = {
        item.get("source_commit")
        for item in request.inventory.get("commits", [])
        if isinstance(item, dict)
    }
    errors: List[str] = []
    lanes = [
        ("parent", request.parent_worktree, request.parent_base),
        ("child", request.child_worktree, request.child_base),
    ]
    if request.wlroots_worktree is not None:
        lanes.append(("wlroots", request.wlroots_worktree, request.wlroots_base))
    for label, repo, base in lanes:
        frozen_base = resolve_commit(repo, base)
        messages = str(run_git(repo, "log", "--format=%B%x00", frozen_base))
        already_mapped = sorted(expected & set(TRACE_TRAILER.findall(messages)))
        legacy_mapped = sorted(expected & set(LEGACY_CHERRY_PICK.findall(messages)))
        errors.extend(
            f"source commit is already mapped in {label} baseline: {source}"
            for source in already_mapped
        )
        errors.extend(
            f"source commit has a legacy cherry-pick mapping in {label} baseline: {source}"
            for source in legacy_mapped
        )
    return errors


def _source_inventory_errors(request: ReplayRequest) -> List[str]:
    errors: List[str] = []
    inventory = request.inventory
    source_repo = canonical_repo(request.source_repo)
    recorded_repo = inventory.get("source_repo")
    if not isinstance(recorded_repo, str) or Path(recorded_repo).resolve() != source_repo:
        errors.append("inventory source_repo differs from the replay source repo")
    range_data = inventory.get("range", {})
    try:
        range_spec = f"{range_data['base']}..{range_data['head']}"
        actual_order = str(
            run_git(source_repo, "rev-list", "--reverse", "--topo-order", range_spec)
        ).split()
        if actual_order != range_data.get("ordered_source_commits"):
            errors.append("inventory source order differs from the replay source history")
        actual_merges = str(
            run_git(source_repo, "rev-list", "--merges", range_spec)
        ).split()
        if actual_merges != range_data.get("merge_commits"):
            errors.append("inventory merge list differs from the replay source history")
        ancestry = (
            (range_data["base"], range_data["head"], "base", "head"),
            (range_data["head"], range_data["source_tip"], "head", "source tip"),
        )
        for older, newer, older_label, newer_label in ancestry:
            if not git_succeeds(
                source_repo, "merge-base", "--is-ancestor", older, newer
            ):
                errors.append(
                    f"inventory {older_label} is not an ancestor of its {newer_label}"
                )
    except (KeyError, RuntimeError) as error:
        errors.append(f"inventory source range cannot be reproduced: {error}")
    policy = inventory.get("path_policy", {})
    policy_path = Path(str(policy.get("path", "")))
    if not policy_path.is_file() or sha256_file(policy_path) != policy.get("sha256"):
        errors.append("inventory path-policy file or digest has drifted")
    if not errors:
        from .inventory import build_unified_inventory
        from .policy import load_policy
        rebuilt = build_unified_inventory(source_repo, range_data["base"], range_data["head"],
                                          load_policy(policy_path), policy_path,
                                          set(inventory["approved_review"]), range_data["source_tip"])
        if rebuilt != inventory:
            errors.append("inventory path projection differs from source Git objects")
    return errors


def _worktree_errors(request: ReplayRequest) -> List[str]:
    canonical_repo(request.source_repo)
    canonical_repo(request.parent_worktree)
    canonical_repo(request.child_worktree)
    errors: List[str] = []
    if not is_linked_worktree(request.parent_worktree):
        errors.append("parent target must be a secondary linked worktree")
    if not is_linked_worktree(request.child_worktree):
        errors.append("child target must be a secondary linked worktree")
    if common_git_dir(request.parent_worktree) == common_git_dir(request.child_worktree):
        errors.append("parent and child must be independent Git repositories")
    worktrees = [request.parent_worktree, request.child_worktree]
    if request.wlroots_worktree is not None:
        worktrees.append(request.wlroots_worktree)
    for index, path in enumerate(worktrees):
        if any(part.is_symlink() for part in (path, *path.parents)):
            errors.append("replay worktree must not traverse a symlink")
        if any(_is_inside(path, other) or _is_inside(other, path) for other in worktrees[index + 1:]):
            errors.append("replay worktrees must be disjoint")
        if _is_inside(request.artifact_root, path) or _is_inside(path, request.artifact_root):
            errors.append("artifact root and replay worktrees must be disjoint")
    if _is_inside(request.artifact_root, request.parent_worktree) or _is_inside(
        request.artifact_root, request.child_worktree
    ):
        errors.append("artifact root must be outside both mutable worktrees")
    temp_root = Path(tempfile.gettempdir()).resolve()
    if _is_inside(request.artifact_root, temp_root) and not request.allow_ephemeral_artifacts:
        errors.append("persistent artifact root must not be under the system temp directory")
    return errors


def run_static_preflight(request: ReplayRequest) -> None:
    """Reject all reproducible input and topology errors before journal creation."""

    errors = inventory_errors(request.inventory)
    errors.extend(_message_metadata_errors(request))
    if request.inventory.get("outcome") != "pass":
        errors.append("inventory outcome must be pass before replay")
    wlroots = frozen_wlroots_identity(request) if not errors else None
    errors.extend(
        _decision_errors(request.decisions, request.inventory, request.artifact_root, wlroots is not None)
    )
    if not errors:
        errors.extend(_source_inventory_errors(request))
    if errors:
        raise ReplayBlocked("; ".join(errors))
    errors.extend(_worktree_errors(request))
    errors.extend(_baseline_trace_errors(request))
    if errors:
        raise ReplayBlocked("; ".join(errors))
    for path in (
        request.journal_path,
        request.manifest_path,
        request.waylib_evidence_path,
        request.parent_evidence_path,
        request.wlroots_evidence_path,
    ):
        _require_output_under_root(path, request.artifact_root)
