"""Read evaluated installed target properties using CMake's JSON trace API."""

from __future__ import annotations

import json
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Sequence


PROPERTY_MARKER = "__TREELAND_CONTRACT_PROPERTY__"
TARGET_MARKER = "__TREELAND_CONTRACT_TARGET__"


def _cmake(arguments: Sequence[str]) -> subprocess.CompletedProcess:
    result = subprocess.run(
        ["cmake", *arguments], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, check=False,
    )
    if result.returncode:
        raise ValueError(f"CMake target inspection failed: {result.stdout}\n{result.stderr}")
    return result


@lru_cache(maxsize=1)
def _properties() -> List[str]:
    names = _cmake(["--help-property-list"]).stdout.splitlines()
    return sorted({
        name for name in names
        if name.startswith(("INTERFACE_", "IMPORTED_", "MAP_IMPORTED_CONFIG_", "COMPATIBLE_INTERFACE_"))
        and ("<" not in name or "<CONFIG>" in name)
    } | {"TYPE", "SYSTEM"})


def _literal(value: str) -> str:
    delimiter = "="
    while f"]{delimiter}]" in value:
        delimiter += "="
    return f"[{delimiter}[{value}]{delimiter}]"


def _query(root: Path, files: Sequence[Path]) -> str:
    # 从 Config 入口读取，保留加载 Targets 之后追加的公共属性。
    configs = [path for path in files if path.name.lower().endswith("config.cmake")]
    targets = [path for path in files if path.name.lower().endswith("targets.cmake")]
    includes = [f"include({_literal(str(root / path))})" for path in configs or targets]
    plain = [name for name in _properties() if "<CONFIG>" not in name]
    configured = [name.replace("<CONFIG>", "${_config}") for name in _properties() if "<CONFIG>" in name]
    return "\n".join([
        "cmake_minimum_required(VERSION 3.21)",
        "project(UnifiedInstalledContract LANGUAGES C CXX)",
        f"list(PREPEND CMAKE_PREFIX_PATH {_literal(str(root))})",
        *includes,
        "get_property(_targets DIRECTORY PROPERTY IMPORTED_TARGETS)",
        "foreach(_target IN LISTS _targets)",
        f'  message(STATUS "{TARGET_MARKER}" "${{_target}}")',
        '  get_target_property(_configs "${_target}" IMPORTED_CONFIGURATIONS)',
        "  list(APPEND _configs DEBUG RELEASE RELWITHDEBINFO MINSIZEREL NOCONFIG)",
        "  set(_props " + " ".join(plain) + ")",
        "  foreach(_config IN LISTS _configs)",
        '    string(TOUPPER "${_config}" _config)',
        "    list(APPEND _props " + " ".join(configured) + ")",
        "  endforeach()",
        "  list(REMOVE_DUPLICATES _props)",
        "  foreach(_prop IN LISTS _props)",
        '    get_property(_set TARGET "${_target}" PROPERTY "${_prop}" SET)',
        "    if(_set)",
        '      get_property(_value TARGET "${_target}" PROPERTY "${_prop}")',
        f'      message(STATUS "{PROPERTY_MARKER}" "${{_target}}" "${{_prop}}" "${{_value}}")',
        "    endif()",
        "  endforeach()",
        "endforeach()",
        "",
    ])


def installed_target_properties(root: Path, files: Sequence[Path]) -> Dict[str, Dict[str, str]]:
    """Evaluate public properties without linking a consumer or writing source trees."""

    if not files:
        return {}
    with tempfile.TemporaryDirectory(prefix="unified-installed-contract-") as directory:
        temporary = Path(directory)
        script = temporary / "CMakeLists.txt"
        script.write_text(_query(root, files), encoding="utf-8")
        result = _cmake([
            "-S", str(temporary), "-B", str(temporary / "build"),
            "--trace-expand", "--trace-format=json-v1",
        ])
        properties: Dict[str, Dict[str, str]] = {}
        for line in result.stderr.splitlines():
            if not line.startswith("{"):
                continue
            event = json.loads(line)
            if event.get("cmd") != "message" or event.get("file") != str(script):
                continue
            args = event.get("args", [])
            if len(args) == 3 and args[1] == TARGET_MARKER:
                properties.setdefault(args[2], {})
            elif len(args) == 5 and args[1] == PROPERTY_MARKER:
                properties.setdefault(args[2], {})[args[3]] = args[4].replace(
                    str(root), "<install-root>"
                )
        return properties
