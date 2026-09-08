"""构建命令使用的固定 P→C→R checkout 身份及其前后核验。"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from .git_ops import GitError, canonical_json_sha256, common_git_dir, is_linked_worktree, run_git
from .patches import tree_entry
from .replay_types import GITLINK_PATH
from .schema import WLROOTS_ROOT, is_full_sha


def git_identity(cwd: Path) -> Optional[Dict[str, Any]]:
    """读取命令所在 Git 工作树的基本身份，非 Git 目录返回空值。"""

    try:
        root = Path(str(run_git(cwd, "rev-parse", "--show-toplevel")).strip()).resolve()
        head = str(run_git(cwd, "rev-parse", "HEAD^{commit}")).strip()
        clean = not bool(str(run_git(cwd, "status", "--porcelain=v1", "--untracked-files=all")))
    except GitError:
        return None
    return {"worktree": str(root), "head": head, "clean": clean}


def checkout_identity(path: Path) -> Optional[Dict[str, Any]]:
    """读取实际对象库与 linked-worktree 身份，不把父目录的 Git 发现当子仓。"""

    identity = git_identity(path)
    if identity is not None:
        identity.update(common_git_dir=str(common_git_dir(path)), linked_worktree=is_linked_worktree(path))
    return identity


def checkout_errors(identity: Any, path: Path, head: str, common: Optional[str] = None) -> List[str]:
    """核验精确路径、SHA、对象库与 clean 状态，不修改已有 checkout。"""

    if not isinstance(identity, dict):
        return [f"nested checkout is not a readable Git worktree: {path}"]
    expected = {"worktree": str(path.resolve()), "head": head, "clean": True, "linked_worktree": True}
    if common is not None:
        expected["common_git_dir"] = common
    errors = [f"nested checkout {key} differs from expected candidate: {path}" for key, value in expected.items() if identity.get(key) != value]
    if any(part.is_symlink() for part in (path, *path.parents)):
        errors.append(f"nested checkout path traverses a symlink: {path}")
    return errors


def _source_requirement(manifest: Mapping[str, Any], validation_id: str, cwd: Path) -> Dict[str, Any]:
    identity = manifest["identity"]
    r = identity.get("wlroots")
    if validation_id.startswith("deckshell-"):
        return {"path": identity["parent_worktree"], "head": manifest["final_parent_head"], "common": identity["parent_common_git_dir"]}
    if validation_id.startswith("wlroots-"):
        if not isinstance(r, dict):
            raise ValueError("wlroots validation is not applicable to this manifest")
        base = validation_id.startswith("wlroots-base-")
        return {"path": str(cwd) if base else r["worktree"], "head": r["base"] if base else manifest["final_wlroots_head"], "common": r["common_git_dir"]}
    base = validation_id.startswith("waylib-base-")
    return {"path": str(cwd) if base else identity["child_worktree"], "head": identity["child_base"] if base else manifest["final_child_head"], "common": identity["child_common_git_dir"]}


def dependency_requirements(manifest: Mapping[str, Any], validation_id: str, cwd: Path) -> Dict[str, Any]:
    """仅为固定两条边派生实际依赖；旧 C 基线未登记 R 时不注入 R。"""

    identity, result = manifest["identity"], {}
    r = identity.get("wlroots")
    parent = validation_id.startswith("deckshell-")
    if parent:
        child_path = Path(identity["parent_worktree"]) / GITLINK_PATH
        result["child"] = {"path": str(child_path), "head": manifest["final_child_head"], "common": identity["child_common_git_dir"], "owner": str(child_path.parent.parent), "relative": GITLINK_PATH}
    if isinstance(r, dict) and not validation_id.startswith("wlroots-"):
        base = validation_id.startswith("waylib-base-")
        if not base or r["registered_at_base"]:
            owner = Path(identity["parent_worktree"]) / GITLINK_PATH if parent else cwd
            result["wlroots"] = {"path": str(owner / WLROOTS_ROOT), "head": r["base"] if base else manifest["final_wlroots_head"], "common": r["common_git_dir"], "owner": str(owner), "relative": WLROOTS_ROOT}
    return result


def capture_dependencies(manifest: Mapping[str, Any], validation_id: str, cwd: Path) -> Dict[str, Any]:
    """在命令前后捕获并核验源工作树及每层实际依赖身份。"""

    if manifest.get("schema_version") != 2 or manifest.get("kind") != "treeland-unified-sync-manifest" or manifest.get("outcome") != "pass":
        raise ValueError("validation requires a complete schema-v2 manifest")
    source = _source_requirement(manifest, validation_id, cwd)
    source_identity = checkout_identity(cwd)
    errors = checkout_errors(source_identity, Path(source["path"]), source["head"], source["common"])
    if str(cwd) != source["path"]:
        errors.append("validation cwd differs from its frozen source worktree")
    result = {"source": source_identity, "dependencies": {}}
    for name, spec in dependency_requirements(manifest, validation_id, cwd).items():
        value = checkout_identity(Path(spec["path"]))
        errors.extend(checkout_errors(value, Path(spec["path"]), spec["head"], spec["common"]))
        link = tree_entry(Path(spec["owner"]), "HEAD", spec["relative"])
        if not link or any(link.get(key) != value for key, value in {"mode": "160000", "type": "commit", "sha": spec["head"]}.items()):
            errors.append(f"validation {name} gitlink differs from the manifest")
        result["dependencies"][name] = value
    if errors:
        raise ValueError("; ".join(errors))
    return result


def dependency_binding_errors(entry: Mapping[str, Any], manifest: Mapping[str, Any]) -> List[str]:
    """报告端核验记录的两层依赖与 manifest，不凭仅有的 parent gitlink 放行。"""

    if entry.get("manifest_sha256") != canonical_json_sha256(manifest):
        return [f"validation manifest binding mismatch: {entry.get('id')}"]
    binding = entry.get("checkout_identity")
    if not isinstance(binding, dict):
        return [f"validation checkout identities are missing: {entry.get('id')}"]
    errors = []
    try:
        cwd = Path(entry["cwd"])
        source = _source_requirement(manifest, entry["id"], cwd)
        expected = dependency_requirements(manifest, entry["id"], cwd)
        for phase in ("before", "after"):
            snapshot = binding.get(phase)
            if not isinstance(snapshot, dict):
                errors.append(f"validation checkout {phase} snapshot is missing")
                continue
            errors.extend(checkout_errors(snapshot.get("source"), Path(source["path"]), source["head"], source["common"]))
            dependencies = snapshot.get("dependencies")
            if not isinstance(dependencies, dict) or set(dependencies) != set(expected):
                errors.append(f"validation {phase} dependency set differs from manifest")
                continue
            for name, spec in expected.items():
                errors.extend(checkout_errors(dependencies[name], Path(spec["path"]), spec["head"], spec["common"]))
    except (KeyError, TypeError, ValueError) as error:
        errors.append(f"invalid validation dependency binding: {error}")
    return errors
