"""记录已明确授权的相邻本地修复，不改变来源映射或协议 companion。"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from .artifacts import read_verified_artifact, write_artifact
from .contracts import build_source_contract_audit, source_contract_audit_errors
from .git_ops import canonical_json_sha256, common_git_dir, resolve_commit, run_git
from .patches import commit_diff, tree_entry
from .protocol_sources import PARENT_XML_PATH, PROVENANCE_PATH, XML_PATH, safe_path
from .schema import WLROOTS_ROOT
from .replay_types import GITLINK_PATH
from .validation_dependencies import checkout_errors, checkout_identity


def preceding_head(document, lane):
    """返回本地修复前的终点；没有修复时保持原有终点语义。"""
    fix = document.get("local_fix") or {}
    return fix.get(lane, {}).get("base", document.get(f"final_{lane}_head"))


def _artifact_json(record, root, label):
    _, raw = read_verified_artifact(record, root, label)
    return json.loads(raw)


def _approval(fix, root):
    approved = _artifact_json(fix["approval"], root, "local fix approval")
    original = _artifact_json(fix["original_manifest"], root, "original replay manifest")
    if (approved.get("kind") != "treeland-unified-local-fix-approval"
            or approved.get("review_state") != "approved"
            or not isinstance(approved.get("authorization"), str)
            or not approved["authorization"].strip()):
        raise ValueError("local fix requires explicit recorded user authorization")
    if approved.get("original_manifest_sha256") != canonical_json_sha256(original):
        raise ValueError("local fix approval is not bound to the original manifest")
    if approved.get("refs_doc") != original["identity"]["refs_doc"]:
        raise ValueError("local fix approval references a different plan")
    if not approved.get("id") or not approved.get("reason") or original.get("local_fix"):
        raise ValueError("local fix id/reason is missing or original manifest already has a local fix")
    if any(key in fix and fix[key] != approved[key] for key in ("id", "reason")):
        raise ValueError("local fix description differs from its approval")
    return approved, original


def _approved_paths(approved, original, lane):
    paths = approved.get("paths", {}).get(lane)
    if (not isinstance(paths, list) or not paths
            or len(set(paths)) != len(paths) or not all(safe_path(p) for p in paths)):
        raise ValueError(f"local {lane} fix requires unique explicit file paths")
    protected = {".gitmodules", WLROOTS_ROOT, PROVENANCE_PATH, XML_PATH, PARENT_XML_PATH}
    inspection = (original.get("protocol_update") or {}).get("inspection", {})
    if lane == "child":
        protected.update(inspection.get("implementation", {}).get("paths", []))
    if any(p in protected or p.startswith((WLROOTS_ROOT + "/", ".git/"))
           or p.endswith(".xml") for p in paths):
        raise ValueError("local fix cannot change R, protocol sources, or pairing provenance")
    if lane == "parent" and GITLINK_PATH not in paths:
        raise ValueError("local parent fix must propagate the approved child gitlink")
    return paths


def _lane_paths(repo, base, head):
    parents = str(run_git(repo, "show", "-s", "--format=%P", head)).split()
    if parents != [base]:
        raise ValueError("local fix must be exactly one adjacent non-merge commit")
    return str(run_git(repo, "diff", "--name-only", "--no-renames", base, head)).splitlines()


def local_lane_errors(repo, fix, lane, root=None):
    """从真实 Git 对象复核单层本地修复；完整证据由报告端再次核验。"""
    try:
        row = fix[lane]
        paths = _lane_paths(repo, row["base"], row["head"])
        if sorted(paths) != sorted(row["paths"]):
            raise ValueError(f"local {lane} fix paths differ from Git")
        message = str(run_git(repo, "show", "-s", "--format=%B", row["head"]))
        if any(line.startswith(("Treeland-Commit:", "Protocol-Implementation-Commit:",
                                "Treeland-Protocols-Commit:"))
               for line in message.splitlines()):
            raise ValueError("local fix must not impersonate a source or protocol companion commit")
        if lane == "child":
            if tree_entry(repo, row["base"], WLROOTS_ROOT) != tree_entry(repo, row["head"], WLROOTS_ROOT):
                raise ValueError("local child fix changed its R gitlink")
        else:
            link = tree_entry(repo, row["head"], GITLINK_PATH)
            if link != {"mode": "160000", "type": "commit", "sha": fix["child"]["head"], "path": GITLINK_PATH}:
                raise ValueError("local parent fix does not reference the repaired child")
        if root is not None:
            approved, original = _approval(fix, root)
            if row["base"] != original[f"final_{lane}_head"]:
                raise ValueError("local fix baseline differs from original candidate")
            if sorted(paths) != sorted(_approved_paths(approved, original, lane)):
                raise ValueError("local fix changes paths outside its exact approval")
            _, patch = read_verified_artifact(row["target_diff"], root, "local fix diff")
            if patch != commit_diff(repo, row["head"]):
                raise ValueError("local fix diff differs from Git")
            if lane == "child":
                audit = _artifact_json(row["source_contract_audit"], root, "local source contract")
                return source_contract_audit_errors(repo, row["base"], row["head"], audit)
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as error:
        return [str(error)]
    return []


def local_fix_errors(manifest, root):
    """拒绝本地修复记录中隐含的来源、基线、仓库或普通映射变更。"""
    fix = manifest.get("local_fix")
    if fix is None:
        return []
    try:
        _, original = _approval(fix, root)
        expected = copy.deepcopy(original)
        expected["local_fix"] = fix
        errors = []
        for lane in ("child", "parent"):
            path = Path(manifest["identity"][f"{lane}_worktree"])
            if str(common_git_dir(path)) != original["identity"][f"{lane}_common_git_dir"]:
                raise ValueError("local fix worktree belongs to a different repository")
            expected["identity"][f"{lane}_worktree"] = str(path)
            expected[f"final_{lane}_head"] = fix[lane]["head"]
            errors.extend(local_lane_errors(path, fix, lane, root))
        old_r = expected["identity"].get("wlroots")
        if old_r is not None:
            path = Path(manifest["identity"]["wlroots"]["worktree"])
            if str(common_git_dir(path)) != old_r["common_git_dir"]:
                raise ValueError("local fix R worktree belongs to a different repository")
            old_r["worktree"] = str(path)
        if manifest != expected:
            errors.append("local fix changed frozen replay identity, mappings or protocol companion")
        return errors
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as error:
        return [str(error)]


def record_local_fix(original, approval_record, original_record, worktrees, root):
    """为已提交的独立本地修复生成派生 manifest；不写源码、提交或目标 refs。"""
    result = copy.deepcopy(original)
    fix = {"approval": approval_record, "original_manifest": original_record}
    approved, _ = _approval(fix, root)
    fix.update(id=approved["id"], reason=approved["reason"])
    for lane in ("child", "parent"):
        repo = worktrees[lane].resolve()
        base, head = original[f"final_{lane}_head"], resolve_commit(repo, "HEAD")
        failures = checkout_errors(checkout_identity(repo), repo, head,
                                   original["identity"][f"{lane}_common_git_dir"])
        if failures:
            raise ValueError("; ".join(failures))
        paths = _lane_paths(repo, base, head)
        if sorted(paths) != sorted(_approved_paths(approved, original, lane)):
            raise ValueError(f"local {lane} fix differs from approved paths")
        row = {"base": base, "head": head, "paths": paths}
        row["target_diff"] = write_artifact(root, f"local-fix/{lane}.diff", commit_diff(repo, head))
        if lane == "child":
            audit = build_source_contract_audit(repo, base, head)
            if audit.get("outcome") != "pass":
                raise ValueError("local fix changed the protected Waylib source contract")
            row["source_contract_audit"] = write_artifact(
                root, "local-fix/child-source-contract.json",
                (json.dumps(audit, indent=2) + "\n").encode())
        fix[lane] = row
        result["identity"][f"{lane}_worktree"] = str(repo)
        result[f"final_{lane}_head"] = head
    if original["identity"].get("wlroots") is not None:
        repo = worktrees["wlroots"].resolve()
        failures = checkout_errors(checkout_identity(repo), repo, original["final_wlroots_head"],
                                   original["identity"]["wlroots"]["common_git_dir"])
        if failures:
            raise ValueError("; ".join(failures))
        result["identity"]["wlroots"]["worktree"] = str(repo)
    result["local_fix"] = fix
    failures = local_fix_errors(result, root)
    if failures:
        raise ValueError("; ".join(failures))
    return result
