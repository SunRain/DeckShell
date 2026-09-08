"""必需 CMake 构建只接受默认完整目标，不接受局部目标或原生工具空跑。"""

from __future__ import annotations

from pathlib import Path
from typing import List, Sequence


REQUIRED_BUILD_IDS = {
    "deckshell-build", "waylib-base-build", "waylib-candidate-build",
    "waylib-package-consumer-build",
}


def _positive_jobs(value: str) -> bool:
    return value.isascii() and value.isdigit() and int(value) > 0


def _safe_build_options(options: Sequence[str]) -> bool:
    index = 0
    while index < len(options):
        value = options[index]
        index += 1
        if value in {"--verbose", "-v", "--clean-first"}:
            continue
        if value == "--config":
            if index == len(options) or not options[index] or options[index].startswith("-"):
                return False
            index += 1
        elif value.startswith("--config="):
            if not value[len("--config="):]:
                return False
        elif value in {"--parallel", "-j"}:
            if index < len(options) and not options[index].startswith("-"):
                if not _positive_jobs(options[index]):
                    return False
                index += 1
        elif value.startswith("--parallel="):
            if not _positive_jobs(value[len("--parallel="):]):
                return False
        elif value.startswith("-j"):
            if not _positive_jobs(value[2:]):
                return False
        else:
            # 不转发 -- 后的参数：它们可以选择目标、替换构建文件或只打印命令。
            return False
    return True


def full_build_command_errors(validation_id: str, command: Sequence[str]) -> List[str]:
    """复核必需构建命令；记录器执行前和报告验收时共用同一规则。"""

    if validation_id not in REQUIRED_BUILD_IDS:
        return []
    error = [f"validation command contract requires a complete default build: {validation_id}"]
    if not command or not all(isinstance(value, str) for value in command) or Path(command[0]).name != "cmake":
        return error
    if len(command) >= 3 and command[1] == "--build":
        build, options = command[2], command[3:]
    elif len(command) >= 2 and command[1].startswith("--build="):
        build, options = command[1][len("--build="):], command[2:]
    else:
        return error
    if not build or build.startswith("-") or not _safe_build_options(options):
        return error
    return []
