"""Build-path and Git-identity bindings for command validations."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Set, Tuple


FRESH_PATH_OPTIONS = {
    "deckshell-configure": "-B",
    "waylib-base-configure": "-B",
    "waylib-candidate-configure": "-B",
    "waylib-package-consumer-configure": "-B",
    "waylib-base-install": "--prefix",
    "waylib-candidate-install": "--prefix",
}


def disjoint_path_errors(paths, protected) -> List[str]:
    """拒绝构建/安装目录相互嵌套或覆盖源工作树，不以 resolve 后的相等替代边界检查。"""

    errors = []
    for index, path in enumerate(paths):
        for other in list(paths[index + 1:]) + list(protected):
            if path == other or path in other.parents or other in path.parents:
                errors.append("validation build/install/worktree paths must be disjoint")
    return errors


def validation_output_path_errors(fresh_paths, cwd: Path, manifest, artifact_root: Path) -> List[str]:
    """在执行命令和创建 CMake query 前拒绝会写进三仓工作树的输出路径。"""

    if manifest is None:
        return []
    identity = manifest["identity"]
    r = identity.get("wlroots") or {}
    worktrees = {cwd, *(Path(value) for value in (
        identity.get("parent_worktree"), identity.get("child_worktree"), r.get("worktree"),
    ) if value)}
    outputs = [Path(value["path"]) for value in fresh_paths.values()]
    errors = disjoint_path_errors(outputs, worktrees)
    errors.extend(disjoint_path_errors([artifact_root.resolve()], worktrees))
    return errors


def _option_value(command: Any, option: str) -> Optional[str]:
    if not isinstance(command, list):
        return None
    matches: List[Any] = []
    for index, value in enumerate(command):
        if value == option:
            matches.append(command[index + 1] if index + 1 < len(command) else None)
        if isinstance(value, str) and value.startswith(f"{option}="):
            matches.append(value[len(option) + 1 :])
    return matches[0] if len(matches) == 1 and isinstance(matches[0], str) else None


def _resolved_option(entry: Mapping[str, Any], option: str) -> Optional[Path]:
    value = _option_value(entry.get("command"), option)
    cwd = entry.get("cwd")
    if not isinstance(value, str) or not isinstance(cwd, str):
        return None
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (Path(cwd) / path).resolve()


def fresh_path_evidence(
    validation_id: str, command: Any, cwd: Any
) -> Dict[str, Dict[str, Any]]:
    """Build canonical pre-execution path evidence for a fixed validation ID."""

    if validation_id in {"wlroots-base-configure", "wlroots-candidate-configure"}:
        from .native_validation import native_build_path
        return {"meson-build": {"path": str(native_build_path(command, Path(cwd))), "existed_before": False}}
    option = FRESH_PATH_OPTIONS.get(validation_id)
    if option is None:
        return {}
    path = _resolved_option({"command": command, "cwd": cwd}, option)
    if path is None:
        raise ValueError(
            f"validation fresh path option is missing: {validation_id} {option}"
        )
    return {option: {"path": str(path), "existed_before": False}}


def fresh_path_errors(entry: Mapping[str, Any]) -> List[str]:
    """Verify exact fresh build/install path evidence against the command."""

    validation_id = entry.get("id")
    if not isinstance(validation_id, str):
        return ["validation fresh path id must be a string"]
    try:
        expected = fresh_path_evidence(
            validation_id, entry.get("command"), entry.get("cwd")
        )
    except ValueError as error:
        return [str(error)]
    if entry.get("fresh_paths") != expected:
        return [f"validation fresh path evidence mismatch: {validation_id}"]
    return []


def _same_option_path(
    entry: Mapping[str, Any], option: str, expected: Optional[Path], label: str
) -> List[str]:
    if expected is None or _resolved_option(entry, option) != expected.resolve():
        return [f"validation path binding mismatch: {label}"]
    return []


def _configure_chain_errors(
    entries: Mapping[str, Mapping[str, Any]],
    prefix: str,
    source: Optional[Path],
    install: Optional[Path] = None,
) -> Tuple[List[str], Optional[Path]]:
    configure = entries.get(f"{prefix}-configure", {})
    build = entries.get(f"{prefix}-build", {})
    build_dir = _resolved_option(configure, "-B")
    errors = _same_option_path(configure, "-S", source, f"{prefix} source")
    errors.extend(
        _same_option_path(build, "--build", build_dir, f"{prefix} build")
    )
    if install is not None:
        install_entry = entries.get(f"{prefix}-install", {})
        errors.extend(
            _same_option_path(
                install_entry,
                "--install",
                build_dir,
                f"{prefix} install build",
            )
        )
        errors.extend(
            _same_option_path(
                install_entry,
                "--prefix",
                install,
                f"{prefix} install prefix",
            )
        )
    return errors, build_dir


def _path_or_none(value: Any) -> Optional[Path]:
    return Path(value).resolve() if isinstance(value, str) and value else None


def _expected_git_identity(worktree: Optional[Path], head: Any) -> Mapping[str, Any]:
    value = {
        "worktree": str(worktree) if worktree is not None else None,
        "head": head,
        "clean": True,
    }
    return {"before": value, "after": dict(value)}


def _git_identity_groups(
    manifest: Mapping[str, Any], audit: Mapping[str, Any]
) -> Tuple[Tuple[Set[str], Optional[Path], Any], ...]:
    identity = manifest.get("identity")
    identity = identity if isinstance(identity, dict) else {}
    source_roots = audit.get("source_roots")
    source_roots = source_roots if isinstance(source_roots, dict) else {}
    return (
        (
            {"deckshell-configure", "deckshell-build", "deckshell-compositor-ctest"},
            _path_or_none(identity.get("parent_worktree")),
            manifest.get("final_parent_head"),
        ),
        (
            {"waylib-base-configure", "waylib-base-build", "waylib-base-install", "waylib-base-ctest"},
            _path_or_none(source_roots.get("before")),
            identity.get("child_base"),
        ),
        (
            {
                "waylib-candidate-configure",
                "waylib-candidate-build",
                "waylib-candidate-install",
                "waylib-ctest",
                "waylib-package-consumer-configure",
                "waylib-package-consumer-build",
                "waylib-package-consumer",
            },
            _path_or_none(identity.get("child_worktree")),
            manifest.get("final_child_head"),
        ),
    )


def _git_identity_group_errors(
    entries: Mapping[str, Mapping[str, Any]],
    groups: Tuple[Tuple[Set[str], Optional[Path], Any], ...],
) -> List[str]:
    errors: List[str] = []
    for validation_ids, worktree, head in groups:
        expected = _expected_git_identity(worktree, head)
        for validation_id in sorted(validation_ids):
            entry = entries.get(validation_id, {})
            if entry.get("git_identity") != expected or entry.get("cwd") != str(worktree):
                errors.append(f"validation Git identity mismatch: {validation_id}")
    optional = entries.get("deckshell-top-level-ctest")
    if optional is not None:
        worktree = groups[0][1]
        expected = _expected_git_identity(worktree, groups[0][2])
        if optional.get("git_identity") != expected:
            errors.append("validation Git identity mismatch: deckshell-top-level-ctest")
    return errors


def _nested_checkout_errors(
    entries: Mapping[str, Mapping[str, Any]],
    manifest: Mapping[str, Any],
    materialization: Optional[Mapping[str, Any]],
) -> List[str]:
    if materialization is None:
        return []
    checkout = materialization.get("checkout")
    expected_nested = (
        {
            "path": checkout.get("path"),
            "expected_head": manifest.get("final_child_head"),
            "head": manifest.get("final_child_head"),
            "linked_worktree": True,
            "clean": True,
            "common_git_dir": checkout.get("common_git_dir"),
            "worktree": checkout.get("path"),
        }
        if isinstance(checkout, dict)
        else None
    )
    parent_ids = {
        "deckshell-configure",
        "deckshell-build",
        "deckshell-compositor-ctest",
        "deckshell-top-level-ctest",
    }
    errors: List[str] = []
    for validation_id in sorted(parent_ids & set(entries)):
        nested = entries[validation_id].get("nested_checkout")
        if not isinstance(nested, dict):
            errors.append(f"nested child checkout evidence is missing: {validation_id}")
            continue
        if not isinstance(expected_nested, dict):
            errors.append("nested child checkout evidence cannot bind materialization")
            continue
        errors.extend(_nested_identity_errors(validation_id, nested, expected_nested))
    return errors


def _nested_identity_errors(
    validation_id: str,
    nested: Mapping[str, Any],
    expected: Mapping[str, Any],
) -> List[str]:
    errors: List[str] = []
    if nested.get("path") != expected["path"]:
        errors.append(f"nested child checkout path binding mismatch: {validation_id}")
    if nested.get("expected_head") != expected["expected_head"]:
        errors.append(f"nested child checkout head binding mismatch: {validation_id}")
    for phase in ("before", "after"):
        identity = nested.get(phase)
        if not isinstance(identity, dict):
            errors.append(
                f"nested child checkout {phase} identity is missing: {validation_id}"
            )
            continue
        for key in ("head", "linked_worktree", "clean", "common_git_dir", "worktree"):
            if identity.get(key) != expected[key]:
                errors.append(
                    f"nested child checkout {phase} identity mismatch: {validation_id}"
                )
    return errors


def _git_identity_errors(
    entries: Mapping[str, Mapping[str, Any]],
    manifest: Mapping[str, Any],
    audit: Mapping[str, Any],
    materialization: Optional[Mapping[str, Any]] = None,
) -> List[str]:
    errors = _git_identity_group_errors(
        entries, _git_identity_groups(manifest, audit)
    )
    errors.extend(_nested_checkout_errors(entries, manifest, materialization))
    return errors


def _consumer_path_errors(
    entries: Mapping[str, Mapping[str, Any]],
    source_roots: Mapping[str, Any],
    install_roots: Mapping[str, Any],
) -> List[str]:
    configure = entries.get("waylib-package-consumer-configure", {})
    build_dir = _resolved_option(configure, "-B")
    source = _path_or_none(source_roots.get("after"))
    errors = _same_option_path(
        configure,
        "-S",
        source / "test_project" if source else None,
        "waylib package consumer source",
    )
    prefix = _resolved_option(configure, "-DCMAKE_PREFIX_PATH")
    expected_prefix = _path_or_none(install_roots.get("after"))
    if expected_prefix is None or prefix != expected_prefix:
        errors.append("validation path binding mismatch: waylib package prefix")
    errors.extend(
        _same_option_path(
            entries.get("waylib-package-consumer-build", {}),
            "--build",
            build_dir,
            "waylib package consumer build",
        )
    )
    errors.extend(
        _same_option_path(
            entries.get("waylib-package-consumer", {}),
            "--test-dir",
            build_dir,
            "waylib package consumer CTest",
        )
    )
    return errors


def path_binding_errors(
    entries: Mapping[str, Mapping[str, Any]],
    manifest: Mapping[str, Any],
    audit: Mapping[str, Any],
    materialization: Optional[Mapping[str, Any]] = None,
) -> List[str]:
    """Validate one configure/build/install/test chain and its source commits."""

    identity = manifest.get("identity")
    identity = identity if isinstance(identity, dict) else {}
    source_roots = audit.get("source_roots")
    source_roots = source_roots if isinstance(source_roots, dict) else {}
    install_roots = audit.get("install_roots")
    install_roots = install_roots if isinstance(install_roots, dict) else {}
    errors, parent_build = _configure_chain_errors(
        entries, "deckshell", _path_or_none(identity.get("parent_worktree"))
    )
    errors.extend(
        _same_option_path(
            entries.get("deckshell-compositor-ctest", {}),
            "--test-dir",
            parent_build / "compositor" if parent_build else None,
            "deckshell compositor CTest",
        )
    )
    base_errors, _base_build = _configure_chain_errors(
        entries,
        "waylib-base",
        _path_or_none(source_roots.get("before")),
        _path_or_none(install_roots.get("before")),
    )
    candidate_errors, candidate_build = _configure_chain_errors(
        entries,
        "waylib-candidate",
        _path_or_none(source_roots.get("after")),
        _path_or_none(install_roots.get("after")),
    )
    errors.extend(base_errors + candidate_errors)
    errors.extend(_same_option_path(
        entries.get("waylib-base-ctest", {}), "--test-dir",
        _base_build / "waylib" if _base_build else None, "waylib baseline CTest",
    ))
    errors.extend(
        _same_option_path(
            entries.get("waylib-ctest", {}),
            "--test-dir",
            candidate_build / "waylib" if candidate_build else None,
            "waylib CTest",
        )
    )
    errors.extend(_consumer_path_errors(entries, source_roots, install_roots))
    errors.extend(_git_identity_errors(entries, manifest, audit, materialization))
    paths = [path for path in (parent_build, _base_build, candidate_build,
                              _resolved_option(entries.get("waylib-package-consumer-configure", {}), "-B"),
                              _path_or_none(install_roots.get("before")), _path_or_none(install_roots.get("after"))) if path]
    worktrees = [_path_or_none(identity.get("parent_worktree")), _path_or_none(source_roots.get("before")), _path_or_none(source_roots.get("after"))]
    errors.extend(disjoint_path_errors(paths, [value for value in worktrees if value]))
    return errors
