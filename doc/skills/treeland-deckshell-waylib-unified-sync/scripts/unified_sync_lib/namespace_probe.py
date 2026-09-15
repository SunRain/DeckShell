"""按基线或显式迁移审批固定命名空间，独立编译候选安装头。"""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Mapping

from .artifacts import artifact_errors, read_verified_artifact, write_artifact
from .contract_migration import migration_probe_snapshot


def probe_source(snapshot: Mapping[str, Any]) -> str:
    """逐头生成显式全限定命名空间别名，避免头文件之间互相补齐定义。"""

    lines = []
    index = 0
    headers = [(header, namespaces) for header, namespaces
               in sorted(snapshot.get("namespace_headers", {}).items()) if namespaces]
    if headers:
        lines.extend(["#if !defined(UNIFIED_BASELINE_HEADER)",
                      '#error "A baseline header must be selected"'])
    for header_index, (header, namespaces) in enumerate(headers):
        lines.append(f"#elif UNIFIED_BASELINE_HEADER == {header_index}")
        lines.append(f"#include {json.dumps(header)}")
        for namespace in namespaces:
            name = namespace.partition("=")[0]
            if not re.fullmatch(r"[A-Za-z_]\w*(?:::[A-Za-z_]\w*)*", name):
                raise ValueError(f"cannot compile a fixed namespace probe: {namespace}")
            lines.append(f"namespace unified_baseline_namespace_{index} = ::{name};")
            index += 1
    if snapshot.get("public_namespaces") and not index:
        raise ValueError("baseline namespaces have no public header bindings")
    if headers:
        lines.extend(["#else", '#error "Unknown baseline header selection"', "#endif"])
    lines.append("int main() { return 0; }")
    return "\n".join(lines) + "\n"


def _cmake_source(prefix: Path, target: str, header_count: int) -> str:
    if not re.fullmatch(r"[A-Za-z_]\w*(?:::[A-Za-z_]\w*)*", target):
        raise ValueError("namespace probe exported target is invalid")
    return "\n".join([
        "cmake_minimum_required(VERSION 3.21)",
        "project(UnifiedNamespaceProbe LANGUAGES CXX)",
        "set(CMAKE_CXX_STANDARD 20)",
        f"list(PREPEND CMAKE_PREFIX_PATH [==[{prefix}]==])",
        "find_package(WaylibShared REQUIRED COMPONENTS SharedServer)",
        f"foreach(header_index RANGE 0 {max(1, header_count) - 1})",
        "  add_library(namespace_probe_${header_index} OBJECT probe.cpp)",
        "  target_compile_definitions(namespace_probe_${header_index} PRIVATE"
        " UNIFIED_BASELINE_HEADER=${header_index})",
        f"  target_include_directories(namespace_probe_${{header_index}} PRIVATE [==[{prefix}]==])",
        f"  target_link_libraries(namespace_probe_${{header_index}} PRIVATE {target})",
        "endforeach()", "",
    ])


def run_namespace_probe(before: Mapping[str, Any], after: Mapping[str, Any], root: Path,
                        approved_migration: Any = None) -> Dict[str, Any]:
    """加载候选安装包，编译基线或已精确批准迁移后的固定命名空间。"""

    expected = migration_probe_snapshot(before, after, approved_migration)
    source = probe_source(expected)
    snapshot_ids = {key: value["snapshot_sha256"] for key, value in (("before", before), ("after", after))}
    targets = after.get("exported_targets", [])
    target = "WaylibShared::SharedServer" if "WaylibShared::SharedServer" in targets else None
    if target is None:
        raise ValueError("fixed namespace probe requires WaylibShared::SharedServer")
    header_count = sum(bool(namespaces) for namespaces in expected.get("namespace_headers", {}).values())
    with tempfile.TemporaryDirectory(prefix="unified-namespace-probe-") as directory:
        path = Path(directory)
        (path / "probe.cpp").write_text(source, encoding="utf-8")
        (path / "CMakeLists.txt").write_text(_cmake_source(Path(after["install_root"]), target, header_count), encoding="utf-8")
        commands = [["cmake", "-S", str(path), "-B", str(path / "build")], ["cmake", "--build", str(path / "build"), "--parallel", "4"]]
        results = []
        for index, command in enumerate(commands):
            completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
            results.append({"command": command, "exit_code": completed.returncode,
                            "log": write_artifact(root, f"namespace-probe/{index}.log", completed.stdout)})
            if completed.returncode:
                break
    return {"schema_version": 2, "kind": "waylib-fixed-namespace-probe", "snapshots": snapshot_ids,
            "source": write_artifact(root, "namespace-probe/probe.cpp", source.encode("utf-8")),
            "commands": results, "outcome": "pass" if len(results) == 2 and all(row["exit_code"] == 0 for row in results) else "fail"}


def namespace_probe_errors(probe: Any, before: Mapping[str, Any], after: Mapping[str, Any], root: Path,
                           approved_migration: Any = None):
    """核验固定探针源码、快照绑定及两条真实编译命令的结果工件。"""

    if not isinstance(probe, dict) or probe.get("schema_version") != 2 or probe.get("kind") != "waylib-fixed-namespace-probe":
        return ["fixed baseline namespace probe evidence is missing"]
    try:
        expected_snapshot = migration_probe_snapshot(before, after, approved_migration)
    except ValueError as error:
        return [str(error)]
    errors = artifact_errors(probe.get("source"), root, "namespace probe source")
    if not errors:
        _, content = read_verified_artifact(probe["source"], root, "namespace probe source")
        if content != probe_source(expected_snapshot).encode("utf-8"):
            errors.append("namespace probe does not use fixed baseline namespaces")
    expected = {key: value["snapshot_sha256"] for key, value in (("before", before), ("after", after))}
    if probe.get("snapshots") != expected or probe.get("outcome") != "pass":
        errors.append("namespace probe failed or belongs to different snapshots")
    commands = probe.get("commands")
    if not isinstance(commands, list) or len(commands) != 2:
        return errors + ["namespace probe requires configure and build results"]
    for index, row in enumerate(commands):
        command = row.get("command", []) if isinstance(row, dict) else []
        if not command or Path(command[0]).name != "cmake" or ("-S" if index == 0 else "--build") not in command or row.get("exit_code") != 0:
            errors.append("namespace probe command did not compile the candidate package")
        if isinstance(row, dict):
            errors.extend(artifact_errors(row.get("log"), root, "namespace probe build log"))
    return errors
