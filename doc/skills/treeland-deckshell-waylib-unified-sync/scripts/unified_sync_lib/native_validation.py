"""R 的 Meson 原生构建和测试证据，零测试明确记 NO_TESTS。"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Mapping

from .artifacts import artifact_errors, read_verified_artifact, write_artifact
from .git_ops import resolve_commit, run_git
from .patches import tree_entry
from .schema import WLROOTS_ROOT


NATIVE_IDS = {f"wlroots-{phase}-{step}" for phase in ("base", "candidate") for step in ("configure", "build", "test")}
BASE_NATIVE_IDS = {name for name in NATIVE_IDS if name.startswith("wlroots-base-")}


def empty_native_baseline(manifest):
    """仅在冻结来源基线无 R 子树且 R0 确为完整空树 commit 时返回 Git 对象证明。"""

    if manifest is None or not isinstance(manifest.get("identity", {}).get("wlroots"), dict):
        return None
    identity, entries = manifest["identity"], manifest.get("entries", [])
    if not entries:
        return None
    r = identity["wlroots"]
    source_repo, repo = Path(identity["source_repo"]), Path(r["repo"])
    first = resolve_commit(source_repo, entries[0]["source_commit"])
    # inventory 只允许连续的非 merge 区间，其首节点的唯一父提交就是左开端点。
    parents = str(run_git(source_repo, "show", "-s", "--format=%P", first)).split()
    if len(parents) != 1:
        raise ValueError("native baseline requires the first source commit's unique parent")
    source_base = parents[0]
    base = resolve_commit(repo, r["base"])
    target_tree = str(run_git(repo, "rev-parse", f"{base}^{{tree}}")).strip()
    if tree_entry(source_repo, source_base, WLROOTS_ROOT) is not None or run_git(repo, "ls-tree", "-z", target_tree, text=False):
        return None
    if "source_base_tree" not in r or r["source_base_tree"] is not None:
        raise ValueError("native baseline source tree differs from the manifest")
    return {"reason": "absent-source-subtree-and-empty-r-base", "source_base": source_base,
            "source_path": WLROOTS_ROOT, "source_tree": None, "wlroots_base": base, "wlroots_tree": target_tree}


def native_absence_errors(entry, root: Path, manifest):
    """重读 Git 对象与证明日志，拒绝把任意构建、候选或 NO_TESTS 伪装成不适用。"""

    name = entry.get("id")
    if name not in BASE_NATIVE_IDS:
        return ["not-applicable is limited to empty wlroots baseline validations"]
    errors = []
    try:
        expected = empty_native_baseline(manifest)
        if expected is None:
            return ["not-applicable requires absent source subtree and empty R base Git objects"]
        if entry.get("native_baseline") != expected:
            errors.append("native baseline proof differs from frozen Git objects")
        category = "test" if name.endswith("-test") else "build"
        if entry.get("category") != category or entry.get("executed") is not False or "exit_code" not in entry or entry["exit_code"] is not None:
            errors.append("not-applicable native validation must record no execution or exit code")
        if any(key in entry for key in ("tests", "native_discovery", "native_test_log", "native_log_identity")):
            errors.append("not-applicable is not a Meson test result or NO_TESTS")
        command, cwd = entry["command"], Path(entry["cwd"])
        native_build_path(command, cwd)
        operation = {"configure": "setup", "build": "compile", "test": "test"}[name.rsplit("-", 1)[1]]
        if command[1] != operation:
            errors.append("not-applicable native command differs from its validation id")
        if operation == "setup" and (len(command) < 4 or (cwd / command[3]).resolve() != cwd or "--wrap-mode=nodownload" not in command):
            errors.append("not-applicable native configure does not bind offline R source")
        errors.extend(artifact_errors(entry.get("log"), root, "native baseline proof log"))
        if not errors:
            _, raw = read_verified_artifact(entry["log"], root, "native baseline proof log")
            if json.loads(raw.decode("utf-8")) != expected:
                errors.append("native baseline proof log differs from frozen Git objects")
    except (KeyError, TypeError, ValueError, RuntimeError) as error:
        errors.append(f"invalid native baseline proof: {error}")
    return errors


def native_build_path(command, cwd: Path) -> Path:
    """解析固定 Meson setup/compile/test 形式，拒绝重复或缺少路径。"""

    if not isinstance(command, list) or len(command) < 3 or Path(command[0]).name != "meson":
        raise ValueError("wlroots native validation requires Meson")
    if command[1] == "setup":
        value = command[2]
    elif command[1] in {"compile", "test"} and command.count("-C") == 1:
        index = command.index("-C")
        value = command[index + 1] if index + 1 < len(command) else ""
    else:
        raise ValueError("Meson command requires setup or compile/test with one -C")
    if not value or value.startswith("-"):
        raise ValueError("Meson build directory is missing")
    path = Path(value)
    return path.resolve() if path.is_absolute() else (cwd / path).resolve()


def _native_test_command_errors(command):
    if len(command) < 2 or Path(command[0]).name != "meson" or command[1] != "test":
        return ["native test evidence requires meson test"]
    forbidden = {"--list", "-l", "--no-log", "--benchmark", "--help", "-h"}
    return ["Meson native tests require execution with result logging"
            for argument in command if argument.split("=", 1)[0] in forbidden]


def _native_log_path(command, cwd, name):
    expected = "--logbase=treeland-" + name
    options = [argument for argument in command if argument == "--logbase" or argument.startswith("--logbase=")]
    errors = _native_test_command_errors(command)
    if options != [expected]:
        errors.append("Meson test logbase must bind the current validation attempt")
    if errors:
        raise ValueError("; ".join(errors))
    return native_build_path(command, cwd) / "meson-logs" / ("treeland-" + name + ".json")


def prepare_native_test(command, cwd: Path, name: str):
    """为本次测试分配独立日志，拒绝只列举、关闭日志及复用已有结果。"""

    if any(argument == "--logbase" or argument.startswith("--logbase=") for argument in command):
        raise ValueError("Meson test logbase is assigned by the validation recorder")
    command = [*command, "--logbase=treeland-" + name]
    path = _native_log_path(command, cwd, name)
    if os.path.lexists(str(path)):
        raise ValueError("fresh Meson test log must not exist before execution: " + str(path))
    return command, {"path": str(path), "existed_before": False}


def record_native_discovery(command, cwd: Path, root: Path, name: str):
    """保存 Meson 原生测试注册集合，不用 CTest 代替 R 测试发现。"""

    build = native_build_path(command, cwd)
    discover = [command[0], "introspect", "--tests", str(build)]
    result = subprocess.run(discover, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode:
        raise ValueError("Meson test discovery failed: " + result.stderr.decode("utf-8", errors="replace"))
    tests = json.loads(result.stdout.decode("utf-8"))
    _test_names(tests)
    return {"command": discover, "tests": tests, "exit_code": 0,
            "log": write_artifact(root, f"logs/{name}-meson-tests.json", result.stdout)}


def _test_names(tests):
    if not isinstance(tests, list) or any(not isinstance(test, dict) or not isinstance(test.get("name"), str) for test in tests):
        raise ValueError("Meson introspection must contain named tests")
    names = [test["name"] for test in tests]
    if len(names) != len(set(names)):
        raise ValueError("Meson test names must be unambiguous")
    return names


def _qualified_names(tests):
    names = {}
    for test in tests:
        name = test["name"]
        names[name] = name
        suites = test.get("suite", [])
        if not isinstance(suites, list) or not suites or not all(isinstance(value, str) for value in suites):
            continue
        projects = {suite.partition(":")[0] for suite in suites}
        if len(projects) != 1:
            raise ValueError("Meson test suites disagree on their project")
        labels = [suite.partition(":")[2] for suite in suites if ":" in suite]
        prefix = "+".join(labels) + " - " if labels else ""
        qualified = prefix + next(iter(projects)) + ":" + name
        names[qualified] = name
    return names


def native_test_result(discovered, raw: bytes, code: int):
    """按 Meson JSON 日志重算结果，skips、子集或未知状态均不通过。"""

    names = _test_names(discovered)
    qualified = _qualified_names(discovered)
    rows = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
    outcomes = [row.get("result") for row in rows if isinstance(row, dict)]
    actual = [qualified.get(row.get("name"), "") for row in rows if isinstance(row, dict)]
    skipped = sum(value == "SKIP" for value in outcomes)
    passed = sum(value == "OK" for value in outcomes)
    failed = len(outcomes) - passed - skipped
    valid = sorted(actual) == sorted(names) and len(actual) == len(rows)
    valid = valid and all(row.get("returncode") == 0 for row in rows if isinstance(row, dict) and row.get("result") == "OK")
    outcome = "pass" if names else "no-tests"
    if not valid or code or failed or skipped:
        outcome = "fail"
    return {"outcome": outcome, "tests": {"total": len(names), "passed": passed, "failed": failed, "skipped": skipped}}


def record_native_result(command, cwd: Path, discovery, code: int, root: Path, name: str, log_identity):
    """保存本次 Meson test 的结构化日志，缺少非空测试日志即失败。"""

    path = _native_log_path(command, cwd, name)
    if log_identity != {"path": str(path), "existed_before": False} or path.is_symlink():
        raise ValueError("Meson result log does not bind the fresh execution path")
    original = path.read_bytes() if path.is_file() else b""
    rows = [json.loads(line) for line in original.decode("utf-8").splitlines() if line.strip()]
    # Meson 的日志包含完整进程环境；证据只保存测试身份、状态和返回码，避免复制凭据。
    selected = [{key: row.get(key) for key in ("name", "result", "returncode")} for row in rows]
    raw = "".join(json.dumps(row, sort_keys=True) + "\n" for row in selected).encode("utf-8")
    return {**native_test_result(discovery["tests"], raw, code), "native_discovery": discovery,
            "native_log_identity": log_identity,
            "native_test_log": write_artifact(root, f"logs/{name}-meson-testlog.json", raw)}


def native_evidence_errors(entry: Mapping[str, Any], root: Path):
    """独立验证发现与结果日志，JSON 中的 PASS 不能覆盖实际失败。"""

    discovery = entry.get("native_discovery")
    if not isinstance(discovery, dict):
        return ["Meson test discovery evidence is missing"]
    errors = artifact_errors(discovery.get("log"), root, "Meson discovery")
    errors.extend(artifact_errors(entry.get("native_test_log"), root, "Meson test log"))
    if errors:
        return errors
    try:
        name = f"{entry['id']}-attempt-{entry['attempt']}"
        path = _native_log_path(entry["command"], Path(entry["cwd"]), name)
        if entry.get("native_log_identity") != {"path": str(path), "existed_before": False}:
            errors.append("Meson test log lacks current-attempt freshness evidence")
        _, raw = read_verified_artifact(discovery["log"], root, "Meson discovery")
        tests = json.loads(raw.decode("utf-8"))
        build = native_build_path(entry["command"], Path(entry["cwd"]))
        if discovery.get("tests") != tests or discovery.get("command") != [entry["command"][0], "introspect", "--tests", str(build)] or discovery.get("exit_code") != 0:
            errors.append("Meson discovery identity differs from its log/command")
        _, log = read_verified_artifact(entry["native_test_log"], root, "Meson test log")
        actual = native_test_result(tests, log, entry["exit_code"])
        if any(entry.get(key) != value for key, value in actual.items()) or actual["outcome"] == "fail":
            errors.append("Meson test counts/status differ from passing native results")
    except (KeyError, TypeError, ValueError) as error:
        errors.append(f"invalid Meson test evidence: {error}")
    return errors


def native_path_errors(entries, manifest):
    """要求 R 基线/候选分别 configure、build、test，同一链绑定相同源码与构建目录。"""

    errors = []
    builds = []
    for phase in ("base", "candidate"):
        if phase == "base" and all(entries.get(name, {}).get("outcome") == "not-applicable" for name in BASE_NATIVE_IDS):
            continue
        prefix = f"wlroots-{phase}"
        try:
            configure = entries[prefix + "-configure"]
            command, cwd = configure["command"], Path(configure["cwd"])
            build = native_build_path(command, cwd)
            if command[1] != "setup" or len(command) < 4 or (cwd / command[3]).resolve() != cwd or "--wrap-mode=nodownload" not in command:
                errors.append(f"{prefix} configure does not bind offline R source")
            for step in ("build", "test"):
                entry = entries[prefix + "-" + step]
                expected = "compile" if step == "build" else "test"
                if entry["command"][1] != expected or entry["cwd"] != str(cwd) or native_build_path(entry["command"], cwd) != build:
                    errors.append(f"{prefix} {step} path binding mismatch")
            builds.append(build)
        except (KeyError, IndexError, TypeError, ValueError) as error:
            errors.append(f"{prefix} native validation is incomplete: {error}")
    if len(builds) == 2 and builds[0] == builds[1]:
        errors.append("wlroots base/candidate require independent fresh build directories")
    from .validation_paths import disjoint_path_errors, _resolved_option
    identity = manifest.get("identity", {})
    r = identity.get("wlroots") or {}
    worktrees = [Path(value) for value in (identity.get("parent_worktree"), identity.get("child_worktree"),
                 r.get("worktree"), *(entry.get("cwd") for entry in entries.values())) if value]
    other_builds = [_resolved_option(entry, option) for entry in entries.values()
                    for option in ("-B", "--prefix")]
    errors.extend(disjoint_path_errors(builds, worktrees + [path for path in other_builds if path]))
    return errors
