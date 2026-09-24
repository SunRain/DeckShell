"""显式公共合同迁移的精确审批；不改变无审批时的严格比较。"""

from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

from .artifacts import artifact_errors, read_verified_artifact
from .schema import is_full_sha


MIGRATION_KIND = "waylib-public-contract-migration"
PARENT_INTEGRATION_FILES = frozenset({
    "CMakeLists.txt",
    "compositor/src/CMakeLists.txt",
    "compositor/src/core/qml/PrelaunchSplash.qml",
    "qtwaylandscanner/CMakeLists.txt",
    "qtwaylandscanner/qtwaylandscanner.cpp",
    "protocols/compositor/CMakeLists.txt",
    "protocols/compositor/xml/treeland-remote-subsurface-unstable-v1.xml",
    "protocols/compositor/xml/treeland-app-id-resolver-v1.xml",
    "protocols/compositor/xml/treeland-app-id-resolver-unstable-v2.xml",
    "protocols/compositor/xml/treeland-prelaunch-splash-v2.xml",
    "protocols/compositor/xml/treeland-prelaunch-splash-unstable-v2.xml",
    "protocols/compositor/xml/treeland-screensaver-v1.xml",
    "protocols/compositor/xml/treeland-screensaver-unstable-v2.xml",
    "protocols/compositor/xml/treeland-wallpaper-shell-unstable-v1.xml",
    "protocols/compositor/xml/treeland-wine-window-management-unstable-v1.xml",
    "protocols/compositor/xml/treeland-wine-window-state-unstable-v1.xml",
    "protocols/compositor/xml/treeland-window-management-v1.xml",
    "protocols/compositor/xml/treeland-show-desktop-unstable-v1.xml",
    "protocols/compositor/xml/treeland-foreign-toplevel-manager-v1.xml",
    "protocols/compositor/xml/treeland-foreign-toplevel-manager-unstable-v2.xml",
})


def _single_line(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and not any(
        ord(character) < 32 or ord(character) == 127 for character in value
    )


def _integration_path(path: Any, lane: str) -> bool:
    if not _single_line(path) or any(character in path for character in "\\*?[]:"):
        return False
    value = PurePosixPath(path)
    if value.is_absolute() or value.as_posix() != path:
        return False
    if any(part in {"..", ".git"} for part in value.parts):
        return False
    if lane == "parent":
        return path in PARENT_INTEGRATION_FILES or path.startswith("compositor/tests/")
    return lane == "child" and (
        path == "CMakeLists.txt" or path.startswith("test_project/")
        or path.startswith("waylib/src/cmake/")
    )


def migration_shape_errors(approval: Any, scope: str, source: str | None = None) -> list[str]:
    """核验审批类型、具体来源和有限的本地调用方路径，不接受通配授权。"""

    if not isinstance(approval, dict):
        return ["public contract migration approval must be an object"]
    expected = {"kind": MIGRATION_KIND, "scope": scope, "review_state": "approved"}
    errors = [f"public contract migration has invalid {key}" for key, value in expected.items()
              if approval.get(key) != value]
    allowed = {"kind", "scope", "review_state", "reason", "refs_doc", "source_commits",
               "before_snapshot_sha256", "after_snapshot_sha256", "drift", "structural_paths"}
    if scope == "installation":
        allowed.add("namespace_bindings")
    errors.extend(f"public contract migration has unsupported field: {key}"
                  for key in approval if key not in allowed)
    for name in ("before_snapshot_sha256", "after_snapshot_sha256"):
        if not isinstance(approval.get(name), str) or not re.fullmatch(r"[0-9a-f]{64}", approval[name]):
            errors.append(f"public contract migration requires a complete {name}")
    if not isinstance(approval.get("drift"), dict):
        errors.append("public contract migration requires the complete drift object")
    for name in ("reason", "refs_doc"):
        if not _single_line(approval.get(name)):
            errors.append(f"public contract migration requires a single-line {name}")
    sources = approval.get("source_commits")
    if (not isinstance(sources, list) or not sources
            or not all(is_full_sha(value) for value in sources)
            or len(sources) != len(set(sources))):
        errors.append("public contract migration requires unique complete source SHAs")
    elif scope == "source" and (len(sources) != 1 or source is not None and sources != [source]):
        errors.append("public contract migration does not bind this source commit")
    paths = approval.get("structural_paths", {})
    if not isinstance(paths, dict) or set(paths) - {"child", "parent"}:
        return errors + ["public contract migration has invalid structural path lanes"]
    for lane, values in paths.items():
        if (not isinstance(values, list) or not all(_integration_path(path, lane) for path in values)
                or len(values) != len(set(values))):
            errors.append(f"public contract migration has unauthorized {lane} integration paths")
    return errors


def migration_contract_errors(approval: Any, before_id: str, after_id: str,
                              drift: Mapping[str, Any], scope: str) -> list[str]:
    """要求审批与真实前后快照、全部实际差异相等，不能只批准字段名称。"""

    errors = migration_shape_errors(approval, scope)
    if not isinstance(approval, dict):
        return errors
    expected = {"before_snapshot_sha256": before_id, "after_snapshot_sha256": after_id,
                "drift": drift}
    errors.extend(f"public contract migration does not bind exact {key}"
                  for key, value in expected.items() if approval.get(key) != value)
    return errors


def read_migration(artifacts: Mapping[str, Any], root: Path, source: str):
    """读取内容寻址的来源审批；缺省不授权任何合同或路径变化。"""

    if not isinstance(artifacts, Mapping):
        return None, ["public contract migration artifacts must be an object"]
    if "contract_migration" not in artifacts:
        return None, []
    record = artifacts["contract_migration"]
    errors = artifact_errors(record, root, "public contract migration")
    if errors:
        return None, errors
    try:
        _, content = read_verified_artifact(record, root, "public contract migration")
        approval = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as error:
        return None, [f"invalid public contract migration JSON: {error}"]
    errors = migration_shape_errors(approval, "source", source)
    return (None, errors) if errors else (approval, [])


def migration_paths(artifacts: Mapping[str, Any], root: Path, source: str, lane: str):
    """仅返回当前来源、当前层已批准的具体调用方路径。"""

    approval, errors = read_migration(artifacts, root, source)
    paths = approval.get("structural_paths", {}).get(lane, []) if approval else []
    return paths, errors


def migration_probe_snapshot(before: Mapping[str, Any], after: Mapping[str, Any], approval: Any):
    """为迁移后的所有命名空间头生成固定绑定，删除旧头必须显式获批。"""

    if approval is None:
        return before
    errors = migration_shape_errors(approval, "installation")
    if isinstance(approval, dict):
        for key, snapshot in (("before", before), ("after", after)):
            if approval.get(f"{key}_snapshot_sha256") != snapshot.get("snapshot_sha256"):
                errors.append("namespace migration approval belongs to different snapshots")
        bindings = approval.get("namespace_bindings")
        if not isinstance(bindings, dict) or bindings != after.get("namespace_headers"):
            errors.append("namespace migration approval must bind every candidate namespace header")
    if errors:
        raise ValueError("; ".join(errors))
    return {**after, "namespace_headers": approval["namespace_bindings"]}
