"""固定 C→R 边的基线投影、子模块登记和来源内容审计。"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional
from urllib.parse import urlsplit

from .adaptations import adaptation_semantic_errors
from .artifacts import artifact_errors, read_verified_artifact
from .git_ops import (
    canonical_repo, changed_paths, commit_changes, common_git_dir, is_linked_worktree,
    resolve_commit, run_git, sha256_bytes, stable_unique,
)
from .patches import commit_diff, source_metadata, source_patch, tree_entry, update_gitlink
from .projections import adapted_content_projection_errors, content_projection_errors
from .replay_types import ReplayBlocked, ReplayRequest
from .schema import WLROOTS_ROOT


UPDATER_GUARD = (
    b"#!/usr/bin/env bash\n"
    b"printf '%s\\n' 'waylib-shared uses a wlroots submodule; use unified sync to update it.' >&2\n"
    b"exit 64\n"
)
UPDATER_PATH = "wlroots/update-from-upstream.sh"


def updater_guard_errors(source_repo: Path, source: str, repo: Path, revision: str, previous: str) -> List[str]:
    """从暂存树或提交对象核验更新脚本；普通适配证明不能豁免保留与拒绝前缀。"""

    target = tree_entry(repo, revision, UPDATER_PATH)
    before = tree_entry(repo, previous, UPDATER_PATH)
    required = target is not None or before is not None
    if tree_entry(repo, revision, WLROOTS_ROOT) is not None:
        required = required or tree_entry(source_repo, source, UPDATER_PATH) is not None
    if not required:
        return []
    if target is None:
        return ["required wlroots updater is missing; omitted/empty cannot waive retention"]
    if target["type"] != "blob" or target["mode"] not in {"100644", "100755"}:
        return ["wlroots updater must remain a regular file, not a symlink, directory or gitlink"]
    content = bytes(run_git(repo, "cat-file", "blob", target["sha"], text=False))
    if not content.startswith(UPDATER_GUARD):
        return ["wlroots updater requires the documented pre-fetch/subtree rejection guard"]
    return []


def tree_files(repo: Path, commit: str, prefix: str = "") -> Dict[str, Any]:
    """读取普通文件的精确树投影；不展开或接受来源中的 gitlink。"""

    args = ["ls-tree", "-r", "-z", commit]
    if prefix:
        args += ["--", prefix]
    result = {}
    for record in bytes(run_git(repo, *args, text=False)).split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, kind, sha = metadata.decode("ascii").split()
        path = raw_path.decode("utf-8", errors="surrogateescape")
        if prefix:
            if not path.startswith(prefix + "/"):
                raise ReplayBlocked("wlroots source must be an ordinary directory")
            path = path[len(prefix) + 1:]
        if kind != "blob" or ".git" in Path(path).parts or ".." in Path(path).parts:
            raise ReplayBlocked(f"unsupported wlroots tree entry: {path}")
        result[path] = {"mode": mode, "type": kind, "sha": sha}
    return result


def blob(repo: Path, revision: str, path: str) -> Optional[bytes]:
    """从冻结 Git 树读取普通文件；缺失返回空值，symlink 等类型直接阻断。"""

    entry = tree_entry(repo, revision, path)
    if entry is None:
        return None
    if entry["type"] != "blob" or entry["mode"] == "120000":
        raise ReplayBlocked(f"expected a regular project file: {path}")
    return bytes(run_git(repo, "cat-file", "blob", entry["sha"], text=False))


def _module_config(repo: Path, content: Optional[bytes]) -> Dict[str, List[str]]:
    with tempfile.TemporaryDirectory(prefix="unified-gitmodules-") as directory:
        path = Path(directory) / "gitmodules"
        path.write_bytes(content or b"")
        raw = str(run_git(repo, "config", "--no-includes", "--null", "--file", str(path), "--list"))
    result: Dict[str, List[str]] = {}
    for item in raw.split("\0"):
        if item:
            name, _, value = item.partition("\n")
            result.setdefault(name, []).append(value)
    return result


def _module_name(config: Mapping[str, List[str]]) -> Optional[str]:
    matches = []
    for key, values in config.items():
        if key.startswith("submodule.") and key.endswith(".path"):
            if "wlroots" in values:
                raise ReplayBlocked("wlroots/ must remain ordinary project files, not a submodule")
            if WLROOTS_ROOT in values:
                if values != [WLROOTS_ROOT]:
                    raise ReplayBlocked("duplicate wlroots submodule path")
                matches.append(key[:-5])
    if len(matches) > 1:
        raise ReplayBlocked("multiple submodule registrations own 3rdparty/wlroots")
    return matches[0] if matches else None


def registration_bytes(repo: Path, before: Optional[bytes], url: str) -> bytes:
    """只新增固定 wlroots 登记，其他条目和注释由 Git 原样保留。"""

    config = _module_config(repo, before)
    if _module_name(config) is not None:
        raise ReplayBlocked("wlroots registration already exists")
    if any(key.startswith("submodule.wlroots.") for key in config):
        raise ReplayBlocked("submodule.wlroots name is already occupied")
    with tempfile.TemporaryDirectory(prefix="unified-register-") as directory:
        path = Path(directory) / "gitmodules"
        path.write_bytes(before or b"")
        for key, value in (("path", WLROOTS_ROOT), ("url", url)):
            run_git(repo, "config", "--no-includes", "--file", str(path), "--", f"submodule.wlroots.{key}", value)
        return path.read_bytes()


def registration(repo: Path, revision: str, expected_sha: Optional[str], url: str) -> Optional[Dict[str, str]]:
    """同时核验固定 R gitlink 与唯一 path/URL 登记，不允许两者只存在其一。"""

    wrapper = tree_entry(repo, revision, "wlroots")
    if wrapper and wrapper["type"] != "tree":
        raise ReplayBlocked("child wlroots/ must be an ordinary directory")
    config = _module_config(repo, blob(repo, revision, ".gitmodules"))
    name = _module_name(config)
    link = tree_entry(repo, revision, WLROOTS_ROOT)
    if link is None and name is None:
        return None
    if name is None or link is None or link["mode"] != "160000" or link["type"] != "commit":
        raise ReplayBlocked("wlroots gitlink and .gitmodules registration must both be valid")
    if config.get(name + ".url") != [url]:
        raise ReplayBlocked("wlroots submodule URL differs from frozen target URL")
    if expected_sha is not None and link["sha"] != expected_sha:
        raise ReplayBlocked("wlroots gitlink differs from expected commit")
    return link


def required_by_inventory(inventory: Mapping[str, Any]) -> bool:
    """判断来源是否触及包装层或 R 内容，而不是仅依赖分类名称。"""

    return any(
        item.get("wlroots", {}).get("included") or any(
            path.startswith("wlroots/") for path in item.get("waylib_shared", {}).get("source_paths", [])
        ) for item in inventory.get("commits", [])
    )


def baseline_projection(repo: Path, base: str, source_repo: Path, source_base: str, record: Any, root: Path) -> Optional[str]:
    """绑定来源子树与 R 基线；重读证明哈希及全部差异路径。"""

    source_tree = tree_entry(source_repo, source_base, WLROOTS_ROOT)
    source_files = tree_files(source_repo, source_base, WLROOTS_ROOT)
    target_files = tree_files(repo, base)
    differing = sorted(path for path in source_files.keys() | target_files.keys() if source_files.get(path) != target_files.get(path))
    source_sha = source_tree["sha"] if source_tree else None
    if not source_tree and target_files:
        raise ReplayBlocked("absent source subtree requires an explicit empty-tree wlroots base")
    if differing or record is not None:
        errors = artifact_errors(record, root, "wlroots baseline proof")
        if errors:
            raise ReplayBlocked("wlroots base differs from source subtree projection; " + "; ".join(errors))
        _, content = read_verified_artifact(record, root, "wlroots baseline proof")
        proof = json.loads(content.decode("utf-8"))
        expected = {"source_tree": source_sha, "target_tree": str(run_git(repo, "rev-parse", f"{base}^{{tree}}")).strip()}
        if not isinstance(proof, dict) or any(proof.get(k) != v for k, v in expected.items()) or proof.get("review_state") != "approved":
            raise ReplayBlocked("wlroots baseline proof does not bind the two frozen trees")
        paths = proof.get("paths")
        if not isinstance(paths, list) or [item.get("path") for item in paths if isinstance(item, dict)] != differing:
            raise ReplayBlocked("wlroots baseline proof must explain every differing path")
        if any(not isinstance(item.get("reason"), str) or not item["reason"].strip() for item in paths):
            raise ReplayBlocked("wlroots baseline proof requires substantive per-path reasons")
    return source_sha


def frozen_wlroots_identity(request: ReplayRequest) -> Optional[Dict[str, Any]]:
    """冻结独立 R 身份、基线投影及子模块 URL；不适用时返回空值。"""

    needed = required_by_inventory(request.inventory) or tree_entry(request.child_worktree, request.child_base, WLROOTS_ROOT) is not None
    provided = [request.wlroots_repo, request.wlroots_worktree, request.wlroots_base, request.wlroots_target_ref, request.wlroots_submodule_url]
    if not needed and not any(provided):
        # 即使不激活 R，也不能容忍另一种错误的 wlroots 子模块布局。
        registration(request.child_worktree, request.child_base, None, "")
        return None
    if not all(provided):
        raise ReplayBlocked("wlroots repo/worktree/base/target-ref/submodule-url are required together")
    repo = canonical_repo(request.wlroots_repo)
    worktree = canonical_repo(request.wlroots_worktree)
    if not is_linked_worktree(worktree) or common_git_dir(repo) != common_git_dir(worktree):
        raise ReplayBlocked("wlroots worktree must be linked to the supplied wlroots repository")
    if common_git_dir(repo) in {common_git_dir(request.child_worktree), common_git_dir(request.parent_worktree)}:
        raise ReplayBlocked("wlroots must be an independent Git repository")
    base = resolve_commit(repo, request.wlroots_base)
    ref = request.wlroots_target_ref
    if not ref.startswith("refs/heads/") or resolve_commit(repo, ref) != base:
        raise ReplayBlocked("wlroots target ref must resolve to the frozen base")
    url = request.wlroots_submodule_url
    if not url.strip() or url.startswith("-") or any(ord(c) < 32 or ord(c) == 127 for c in url) or urlsplit(url).password:
        raise ReplayBlocked("wlroots submodule URL must be a safe credential-free value")
    source_sha = baseline_projection(repo, base, request.source_repo, request.inventory["range"]["base"],
                                     request.wlroots_baseline_proof, request.artifact_root)
    initial = registration(request.child_worktree, request.child_base, base, url)
    return {
        "repo": str(repo), "worktree": str(worktree), "common_git_dir": str(common_git_dir(repo)),
        "base": base, "target_ref": ref, "submodule_url": url, "gitlink_path": WLROOTS_ROOT,
        "registered_at_base": initial is not None, "baseline_proof": request.wlroots_baseline_proof,
        "source_base_tree": source_sha,
    }


def nested_transition(repo: Path, before: str, after: str, expected_sha: str, url: str) -> Dict[str, Any]:
    """重算一条 C→R 变迁，并拒绝混入其他 .gitmodules 修改。"""

    old = registration(repo, before, None, url)
    new = registration(repo, after, expected_sha, url)
    if new is None:
        raise ReplayBlocked("required wlroots submodule registration is missing")
    before_modules = blob(repo, before, ".gitmodules")
    after_modules = blob(repo, after, ".gitmodules")
    expected_modules = before_modules if old else registration_bytes(repo, before_modules, url)
    if after_modules != expected_modules:
        raise ReplayBlocked(".gitmodules contains changes beyond the frozen wlroots registration")
    return {
        "status": "registered" if old is None else "updated" if old["sha"] != new["sha"] else "unchanged",
        "from": old["sha"] if old else None, "to": new["sha"],
        "url": url, "gitmodules_before": sha256_bytes(before_modules or b""),
        "gitmodules_after": sha256_bytes(after_modules or b""),
    }


def stage_wlroots_gitlink(request: ReplayRequest, item: Mapping[str, Any], sha: str) -> Optional[Dict[str, Any]]:
    """暂存已存在的 R commit；首次需要依赖时只增加固定登记。"""

    repo = request.child_worktree
    old = registration(repo, "HEAD", None, request.wlroots_submodule_url)
    if old is None and not required_by_inventory({"commits": [item]}):
        return None
    if str(run_git(request.wlroots_repo, "cat-file", "-t", sha)).strip() != "commit":
        raise ReplayBlocked("wlroots gitlink must identify an actual commit object")
    if old is None:
        content = registration_bytes(repo, blob(repo, "HEAD", ".gitmodules"), request.wlroots_submodule_url)
        (repo / ".gitmodules").write_bytes(content)
        run_git(repo, "add", "--", ".gitmodules")
    update_gitlink(repo, WLROOTS_ROOT, sha)
    staged_tree = str(run_git(repo, "write-tree")).strip()
    return nested_transition(repo, "HEAD", staged_tree, sha, request.wlroots_submodule_url)


def wlroots_source_audit(source_repo: Path, repo: Path, item: Mapping[str, Any], target: str, action: str, adaptations: Any, artifacts: Mapping[str, Any], root: Path) -> Dict[str, Any]:
    """独立核验 R 内容投影、逐路径证据与作者时间，不套用 C 的公共 API 冻结规则。"""

    source = item["source_commit"]
    paths = item["wlroots"]["target_paths"]
    patch = source_patch(source_repo, source, item["wlroots"]["source_paths"], WLROOTS_ROOT)
    actual = stable_unique(path for change in commit_changes(repo, target) for path in changed_paths(change))
    errors = []
    if set(actual) - set(paths):
        errors.append("wlroots target path expansion")
    if action == "applied":
        if set(actual) != set(paths):
            errors.append("wlroots applied paths differ from source")
        errors.extend(content_projection_errors(repo, target, paths, [(patch, None)], "wlroots"))
    elif action == "adapted":
        errors.extend(adaptation_semantic_errors(repo, target, adaptations, paths, actual, root, "wlroots"))
        errors.extend(adapted_content_projection_errors(repo, target, paths, artifacts.get("adaptation_patch"), root, "wlroots"))
        if not actual:
            errors.append("adapted wlroots commit has no content")
    elif action == "empty":
        errors.extend(artifact_errors(artifacts.get("equivalence_proof"), root, "wlroots equivalence proof"))
        if actual:
            errors.append("empty wlroots commit contains content")
    else:
        errors.append("unsupported wlroots action")
    left, right = source_metadata(source_repo, source), source_metadata(repo, target)
    if any(left[k] != right[k] for k in ("author", "email", "date")):
        errors.append("wlroots source author/date mismatch")
    return {"schema_version": 2, "kind": "wlroots-source-audit", "source_commit": source, "target_commit": target,
            "source_patch_sha256": sha256_bytes(patch), "target_diff_sha256": sha256_bytes(commit_diff(repo, target)),
            "blocked_reasons": errors, "outcome": "blocked" if errors else "pass"}
