"""One protocol companion step inside the existing journaled R/C/P replay."""

from __future__ import annotations

import json
from pathlib import Path

from .artifacts import read_verified_artifact, write_artifact
from .contracts import build_source_contract_audit, source_contract_audit_errors
from .git_ops import atomic_write_bytes, resolve_commit, run_git
from .journal import add_event, save_journal
from .patches import (apply_index_patch, commit_diff, create_commit, enforce_staged_paths,
                      source_metadata, tree_entry, update_gitlink)
from .protocol_sources import (PARENT_XML_PATH, PROVENANCE_PATH, XML_PATH,
                               inspect_pairing, safe_path, source_blob)
from .replay_types import GITLINK_PATH, ReplayBlocked


def _adaptation_errors(lane, decision, inspection, root):
    if not isinstance(decision, dict) or set(decision) - {"paths", "reason", "adaptation_patch"}:
        raise ValueError(f"invalid protocol {lane} adaptation")
    paths = decision.get("paths", [])
    if not isinstance(paths, list) or not all(safe_path(p) for p in paths):
        raise ValueError(f"protocol {lane} adaptation requires explicit file paths")
    if not paths and not decision:
        return
    if not paths or not isinstance(decision.get("reason"), str) or not decision["reason"].strip():
        raise ValueError(f"protocol {lane} adaptation lacks paths or reason")
    impl_paths = inspection["implementation"]["paths"]
    for path in paths:
        if lane == "child":
            allowed = (path in impl_paths or path.startswith(("waylib/tests/", "test_project/")))
        else:
            allowed = path.startswith(("compositor/", "treeland-dde-shell-client/"))
        if not allowed:
            raise ValueError(f"protocol adaptation leaves implementation/client/test scope: {path}")
    read_verified_artifact(decision.get("adaptation_patch"), root, f"protocol {lane} adaptation")


def freeze_protocol_update(request) -> dict | None:
    """Resolve both source ranges before any replay mutation; preserve the exact input."""

    supplied = request.protocol_update
    if supplied is None:
        return None
    if not isinstance(supplied, dict) or set(supplied) - {"selection", "child", "parent"}:
        raise ReplayBlocked("尚未适配：invalid protocol-update input")
    inspection = inspect_pairing(request.inventory, request.source_repo,
                                 request.child_worktree, request.child_base,
                                 supplied.get("selection", {}))
    if inspection["outcome"] != "pass":
        raise ReplayBlocked("; ".join(inspection["blocked_reasons"]))
    for lane in ("child", "parent"):
        _adaptation_errors(lane, supplied.get(lane, {}), inspection, request.artifact_root)
    return {"inspection": inspection, "child": supplied.get("child", {}),
            "parent": supplied.get("parent", {})}


def _write_source(repo, path, content):
    target = repo / path
    if any(p.is_symlink() for p in (target, *target.parents)):
        raise ReplayBlocked(f"protocol output traverses a symlink: {target}")
    atomic_write_bytes(target, content)
    run_git(repo, "add", "--", path)


def _stage_content(request, lane, repo, frozen, child_head):
    decision = frozen[lane]
    if decision:
        _, patch = read_verified_artifact(decision["adaptation_patch"], request.artifact_root,
                                          f"protocol {lane} adaptation")
        apply_index_patch(repo, patch)
    # Check caller-supplied paths before adding the workflow-owned snapshot/gitlink.
    enforce_staged_paths(repo, set(decision.get("paths", [])), set(decision.get("paths", [])),
                         f"protocol {lane} adaptation")
    inspection = frozen["inspection"]
    protocol = inspection["protocol"]
    xml = source_blob(Path(protocol["repo"]), protocol["head"], protocol["head_path"])
    path = XML_PATH if lane == "child" else PARENT_XML_PATH
    _write_source(repo, path, xml)
    allowed = set(decision.get("paths", [])) | {path}
    if lane == "child":
        content = (json.dumps(inspection["proposed_pair"], ensure_ascii=False, indent=2) + "\n").encode()
        _write_source(repo, PROVENANCE_PATH, content)
        allowed.add(PROVENANCE_PATH)
    else:
        update_gitlink(repo, GITLINK_PATH, child_head)
        allowed.add(GITLINK_PATH)
    return enforce_staged_paths(repo, allowed, set(), f"protocol {lane}")


def _stage_lane(request, lane, frozen, child_head):
    repo = getattr(request, f"{lane}_worktree")
    base = resolve_commit(repo, "HEAD")
    if str(run_git(repo, "status", "--porcelain=v1", "--untracked-files=all")):
        raise ReplayBlocked(f"protocol {lane} worktree is not clean")
    paths = _stage_content(request, lane, repo, frozen, child_head)
    expected_tree = str(run_git(repo, "write-tree")).strip()
    head = base
    if paths:
        inspection = frozen["inspection"]
        protocol = inspection["protocol"]
        message = ("chore(protocol): 同步 remote-subsurface 配套快照\n\n"
                   f"Protocol-Implementation-Commit: {inspection['implementation']['head']}\n"
                   f"Treeland-Protocols-Commit: {protocol['head']}\n"
                   f"Refs: {request.refs_doc}\n")
        head = create_commit(repo, source_metadata(Path(protocol["repo"]), protocol["head"]), message)
    result = {"base": base, "head": head, "paths": paths, "expected_tree": expected_tree}
    if paths:
        result["target_diff"] = write_artifact(request.artifact_root, f"protocol/{lane}-target.diff",
                                                commit_diff(repo, head))
    if lane == "child":
        audit = build_source_contract_audit(repo, base, head)
        result["source_contract_audit"] = write_artifact(
            request.artifact_root, "protocol/child-source-contract-audit.json",
            (json.dumps(audit, ensure_ascii=True, indent=2) + "\n").encode())
    return result


def companion_lane_errors(repo, update, lane, artifact_root=None) -> list[str]:
    """Verify a companion commit without treating it as a fabricated Treeland commit."""

    row = update.get(lane)
    if not isinstance(row, dict):
        return [f"protocol {lane} companion is missing"]
    try:
        base, head = row["base"], row["head"]
        actual = str(run_git(repo, "rev-list", "--reverse", f"{base}..{head}")).split()
        if actual != ([head] if head != base else []):
            raise ValueError(f"protocol {lane} companion is not one adjacent commit")
        if str(run_git(repo, "rev-parse", f"{head}^{{tree}}")).strip() != row["expected_tree"]:
            raise ValueError(f"protocol {lane} commit differs from the prepared tree")
        inspection = update["inspection"]
        protocol = inspection["protocol"]
        xml = source_blob(Path(protocol["repo"]), protocol["head"], protocol["head_path"])
        path = XML_PATH if lane == "child" else PARENT_XML_PATH
        if source_blob(repo, head, path) != xml:
            raise ValueError(f"protocol {lane} XML differs from the selected upstream contract")
        if lane == "child":
            if json.loads(source_blob(repo, head, PROVENANCE_PATH)) != inspection["proposed_pair"]:
                raise ValueError("protocol provenance differs from inspected sources")
            if tree_entry(repo, base, "3rdparty/wlroots") != tree_entry(repo, head, "3rdparty/wlroots"):
                raise ValueError("protocol companion must not change native wlroots")
        if artifact_root is not None:
            if head != base:
                _, recorded = read_verified_artifact(row.get("target_diff"), artifact_root, f"protocol {lane} diff")
                if recorded != commit_diff(repo, head):
                    raise ValueError(f"protocol {lane} diff differs from Git")
            if lane == "child":
                _, content = read_verified_artifact(row.get("source_contract_audit"), artifact_root,
                                                    "protocol child source contract")
                return source_contract_audit_errors(repo, base, head, json.loads(content))
    except (OSError, ValueError, RuntimeError, KeyError) as error:
        return [str(error)]
    return []


def run_protocol_update(request, journal, stage_hook=None) -> None:
    """Finish paired XML/source/client changes inside the existing replay journal."""

    frozen = journal["identity"].get("protocol_update")
    if frozen is None:
        return
    update = journal.setdefault("protocol_update", {"inspection": frozen["inspection"]})
    for lane in ("child", "parent"):
        if lane not in update:
            update[lane] = _stage_lane(request, lane, frozen, journal["current_child_head"])
            journal[f"current_{lane}_head"] = update[lane]["head"]
            add_event(journal, "", f"protocol-{lane}", "complete", update[lane]["head"])
            save_journal(request.journal_path, journal)
            if stage_hook:
                stage_hook(f"protocol-{lane}", "", update[lane]["head"])
        errors = companion_lane_errors(getattr(request, f"{lane}_worktree"), update,
                                       lane, request.artifact_root)
        if errors:
            raise ReplayBlocked("尚未适配：" + "; ".join(errors))


def replay_head(manifest, lane):
    """Return the ordinary replay endpoint, before an optional protocol companion."""

    update = manifest.get("protocol_update", {})
    from .local_fixes import preceding_head
    return update.get(lane, {}).get("base", preceding_head(manifest, lane))
