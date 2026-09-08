"""通过 pkg-config 求值安装包合同，拒绝环境覆盖和旧的字面字段快照。"""

from __future__ import annotations

import os
import re
import shlex
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence


QUERIES = {
    "Version": ["--modversion"],
    "Requires": ["--print-requires"],
    "Requires.private": ["--print-requires-private"],
    "Cflags": ["--cflags"],
    "Libs": ["--libs"],
    "Cflags.static": ["--static", "--cflags"],
    "Libs.static": ["--static", "--libs"],
}


def _query(path: Path, environment: Mapping[str, str], arguments: Sequence[str]) -> str:
    environment = {**environment, "PKG_CONFIG_PATH": os.pathsep.join([
        str(path.parent), environment["PKG_CONFIG_PATH"],
    ])}
    result = subprocess.run(
        ["pkg-config", "--print-errors", *arguments, path.stem], env=environment,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", check=False,
    )
    if result.returncode:
        raise ValueError(f"pkg-config inspection failed for {path}: {result.stderr.strip()}")
    return result.stdout.strip()


def _variable(path: Path, environment: Mapping[str, str], name: str) -> str:
    value = _query(path, environment, ["--variable=" + name])
    parts = shlex.split(value)
    return parts[0] if len(parts) == 1 else value


def _package_name(path: Path, environment: Mapping[str, str]) -> str:
    content = path.read_text(encoding="utf-8").replace("\\\n", "")
    field = re.search(r"(?m)^[ \t]*Name[ \t]*:[ \t]*(.*)$", content)
    if field is None:
        raise ValueError(f"pkg-config Name field is missing: {path}")
    # pkg-config 没有 Name 查询开关；变量值仍交给原生解析器展开，不重写递归求值器。
    return re.sub(r"\$\{([^}]+)\}", lambda match: _variable(
        path, environment, match.group(1),
    ), field.group(1).strip())


def _normalized_value(name: str, value: str, root: Path) -> str:
    pattern = re.escape(str(root)) + r"(?=/|$|[\"'\s,:;])"
    if name in {"Cflags", "Libs", "Cflags.static", "Libs.static"}:
        return shlex.join([re.sub(pattern, "<install-root>", part) for part in shlex.split(value)])
    return re.sub(pattern, "<install-root>", value)


def installed_pkg_config(root: Path, files: Sequence[Path]) -> Dict[str, Dict[str, str]]:
    """固定顶层 .pc 的实际路径，比较动态/静态调用方可观察到的完整参数。"""

    packages = [root / path for path in files if path.suffix.lower() == ".pc"]
    if not packages:
        return {}
    environment = {key: value for key, value in os.environ.items() if not key.startswith("PKG_CONFIG")}
    environment.update(
        PKG_CONFIG_PATH=os.pathsep.join(sorted({str(path.parent) for path in packages})),
        PKG_CONFIG_DISABLE_UNINSTALLED="1",
        PKG_CONFIG_ALLOW_SYSTEM_CFLAGS="1", PKG_CONFIG_ALLOW_SYSTEM_LIBS="1",
    )
    result = {}
    for path in packages:
        directory = _variable(path, environment, "pcfiledir")
        if not directory or Path(directory).resolve() != path.parent.resolve():
            raise ValueError(f"pkg-config resolved a different installed package: {path}")
        values = {name: _query(path, environment, arguments) for name, arguments in QUERIES.items()}
        values["Name"] = _package_name(path, environment)
        result[path.relative_to(root).as_posix()] = {
            name: _normalized_value(name, value, root) for name, value in values.items()
        }
    return result


def pkg_config_snapshot_errors(packages: Any, installed_paths: Sequence[str], label: str) -> List[str]:
    """要求每个已安装 .pc 都有实际求值字段，旧字面快照不能继续参与放行。"""

    if not isinstance(installed_paths, (list, tuple)):
        return [f"{label} pkg-config installed paths are invalid; regenerate the snapshot"]
    expected = {path for path in installed_paths if isinstance(path, str) and path.lower().endswith(".pc")}
    fields = {*QUERIES, "Name"}
    if not isinstance(packages, dict) or set(packages) != expected:
        return [f"{label} pkg-config snapshot coverage is invalid; regenerate the snapshot"]
    if any(not isinstance(values, dict) or not fields.issubset(values)
           or any(not isinstance(value, str) for value in values.values()) for values in packages.values()):
        return [f"{label} pkg-config snapshot lacks evaluated fields; regenerate the snapshot"]
    return []
