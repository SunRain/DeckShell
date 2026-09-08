"""记录器与独立审计共用的 CTest 结果解析；跳过不等于通过。"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Mapping

from .artifacts import artifact_errors, read_verified_artifact, write_artifact


SUMMARY = re.compile(rb"(?m)^\s*(\d+)% tests passed(?:,\s*(\d+) tests failed)? out of\s+(\d+)\s*$")
CASE = re.compile(rb"(?m)^\s*\d+/\d+\s+Test\s+#(\d+):\s+(.*?)\s+\.{2,}\s*(.*?)\r?$")
FOOTER = re.compile(rb"(?m)^\s*(\d+)\s+-\s+(.*?)\s+\(([^)]+)\)\s*$")


def parse_ctest(output: bytes, exit_code: int) -> Dict[str, Any]:
    """接受新旧摘要，按测试编号去重；不能解析或计数矛盾时失败关闭。"""

    summaries = list(SUMMARY.finditer(output))
    no_tests = b"No tests were found" in output
    error = None
    if len(summaries) != 1 and not (not summaries and no_tests):
        error = "CTest summary was not found or is ambiguous"
    match = summaries[0] if len(summaries) == 1 else None
    failed = int(match.group(2) or 0) if match else 0
    total = int(match.group(3)) if match else 0
    if match and (int(match.group(1)) > 100 or (failed == 0 and int(match.group(1)) != 100)):
        error = "CTest success percentage is inconsistent"
    if no_tests and total:
        error = "CTest zero-test message contradicts the summary"
    statuses: Dict[int, str] = {}
    names: Dict[int, str] = {}
    for case in [*CASE.finditer(output), *FOOTER.finditer(output)]:
        number = int(case.group(1))
        detail = case.group(3).strip().lstrip(b"*")
        status = "skipped" if detail.startswith((b"Skipped", b"Disabled")) else (
            "passed" if detail.startswith(b"Passed") else "failed"
        )
        name = case.group(2).decode("utf-8", errors="replace")
        if number in statuses and (statuses[number] != status or names[number] != name):
            error = "CTest test status is inconsistent"
        statuses[number] = status
        names[number] = name
    skipped = sum(status == "skipped" for status in statuses.values())
    observed_failed = sum(status == "failed" for status in statuses.values())
    passed = total - failed - skipped
    if passed < 0 or observed_failed > failed or len(statuses) > total:
        error = "CTest test counts are inconsistent"
    if CASE.search(output) and len(statuses) != total:
        error = "CTest individual results do not cover the summary"
    if len(statuses) == total and (observed_failed != failed or sum(s == "passed" for s in statuses.values()) != passed):
        error = "CTest observed statuses contradict summary counts"
    outcome = "no-tests" if total == 0 else "pass"
    if error or exit_code != 0 or failed or skipped:
        outcome = "fail"
    result: Dict[str, Any] = {
        "outcome": outcome,
        "tests": {"total": total, "passed": max(0, passed), "failed": failed, "skipped": skipped},
        "test_results": [
            {"id": number, "name": names[number], "status": statuses[number]}
            for number in sorted(statuses)
        ],
    }
    if error:
        result["parse_error"] = error
    return result


def ctest_evidence_errors(entry: Mapping[str, Any], root: Path) -> List[str]:
    """从已哈希日志重算，拒绝手写 outcome/counts 或缺失的通过证据。"""

    errors = artifact_errors(entry.get("log"), root, "CTest log")
    if errors:
        return errors
    _path, output = read_verified_artifact(entry["log"], root, "CTest log")
    code = entry.get("exit_code")
    if type(code) is not int:
        return ["CTest exit_code must be an integer"]
    actual = parse_ctest(output, code)
    for key in ("outcome", "tests", "test_results"):
        if entry.get(key) != actual[key]:
            errors.append(f"CTest {key} differs from recorded log")
    if actual["outcome"] not in {"pass", "no-tests"}:
        errors.append("CTest log contains failures, skipped tests or invalid results")
    return errors


def _discovered_tests(output: bytes) -> List[Dict[str, Any]]:
    payload = json.loads(output.decode("utf-8"))
    tests = payload.get("tests") if isinstance(payload, dict) else None
    if not isinstance(tests, list) or any(not isinstance(test, dict) or not isinstance(test.get("name"), str) or not test["name"] for test in tests):
        raise ValueError("CTest discovery must contain named tests")
    names = [test["name"] for test in tests]
    if len(names) != len(set(names)):
        raise ValueError("CTest discovery contains duplicate test names")
    return [{"id": index + 1, "name": name} for index, name in enumerate(names)]


def discovery_command(command: List[str], cwd: Path) -> List[str]:
    """从实际 CTest 命令生成无过滤的发现命令，不能用筛选后的集合代替全量集合。"""

    from .validation_paths import _resolved_option

    directory = _resolved_option({"command": command, "cwd": str(cwd)}, "--test-dir")
    if not command or Path(command[0]).name != "ctest" or directory is None:
        raise ValueError("CTest discovery requires one explicit --test-dir")
    return [command[0], "--test-dir", str(directory), "--show-only=json-v1"]


def record_ctest_discovery(command: List[str], cwd: Path, root: Path, name: str) -> Dict[str, Any]:
    """执行真实测试发现并保存原始 JSON，失败或非法输出不进入执行阶段。"""

    discover = discovery_command(command, cwd)
    completed = subprocess.run(discover, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if completed.returncode:
        raise ValueError("CTest discovery failed: " + completed.stderr.decode("utf-8", errors="replace"))
    tests = _discovered_tests(completed.stdout)
    return {"command": discover, "cwd": str(cwd), "exit_code": 0, "tests": tests,
            "log": write_artifact(root, f"logs/{name}-discovery.json", completed.stdout)}


def discovery_errors(entry: Mapping[str, Any], root: Path) -> List[str]:
    """核对发现日志、实际运行结果与必需集合，拒绝只运行可通过的子集。"""

    discovery = entry.get("test_discovery")
    if not isinstance(discovery, dict):
        return ["CTest test discovery evidence is missing"]
    errors = artifact_errors(discovery.get("log"), root, "CTest discovery")
    if errors:
        return errors
    try:
        _, output = read_verified_artifact(discovery["log"], root, "CTest discovery")
        expected = _discovered_tests(output)
        command = discovery_command(entry["command"], Path(entry["cwd"]))
        if discovery.get("command") != command or discovery.get("cwd") != entry["cwd"] or discovery.get("exit_code") != 0:
            errors.append("CTest discovery command/directory differs from executed tests")
        if discovery.get("tests") != expected:
            errors.append("CTest discovery set differs from its hashed log")
        actual = [{"id": value.get("id"), "name": value.get("name")} for value in entry.get("test_results", []) if isinstance(value, dict)]
        if actual != expected or entry.get("tests", {}).get("total") != len(expected):
            errors.append("CTest results do not cover the complete discovered test set")
    except (KeyError, TypeError, ValueError) as error:
        errors.append(f"invalid CTest discovery evidence: {error}")
    return errors
