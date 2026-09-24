"""把安装包中的 ELF 和 R 头文件追溯到本次已验证的 C 构建。"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from .git_ops import sha256_file
from .wrapper_build import _absolute, _inside


def _elf_without_rpath(path):
    # CMake install 会改写 RPATH；只归一化这一安装变换，不忽略其它 ELF 内容。
    with tempfile.TemporaryDirectory(prefix="sync-elf-") as directory:
        copy = Path(directory) / "library.so"
        shutil.copyfile(path, copy)
        script = Path(directory) / "remove-rpath.cmake"
        script.write_text(f'file(RPATH_REMOVE FILE "{copy}")\n', encoding="utf-8")
        result = subprocess.run(["cmake", "-P", str(script)], capture_output=True, text=True)
        if result.returncode:
            raise ValueError("cannot normalize installed ELF RPATH: " + result.stderr)
        return sha256_file(copy)


def installed_libraries(model, build, prefix, installed):
    """校验两个实际导出共享库；只接受本次 install manifest 中的相同 ELF。"""
    result = {}
    for name in ("WaylibSharedServer", "waylib_wlroots_native_library"):
        targets = [row for row in model["targets"] if row.get("name") == name
                   and row.get("type") == "SHARED_LIBRARY"]
        if len(targets) != 1:
            raise ValueError("installed package needs one compiled target: " + name)
        target = targets[0]
        outputs = {_absolute(row["path"], build) for row in target.get("artifacts", [])}
        if len(outputs) != 1:
            raise ValueError("installed library has ambiguous build outputs: " + name)
        source = outputs.pop()
        candidates = {(prefix / row["path"] / source.name).resolve()
                      for row in target.get("install", {}).get("destinations", [])}
        if len(candidates) != 1:
            raise ValueError("installed library has ambiguous install destinations: " + name)
        destination = candidates.pop()
        if not _inside(source, build) or not _inside(destination, prefix) or destination not in installed:
            raise ValueError("installed library is outside the candidate build/install manifest")
        if _elf_without_rpath(source) != _elf_without_rpath(destination):
            raise ValueError("installed ELF differs from the current candidate build: " + name)
        result[name] = {"build": str(source), "installed": str(destination),
                        "sha256": sha256_file(destination)}
    return result


def installed_headers(used, child, build, prefix, installed, generated):
    """核对消费者真正使用的 R 源头文件和生成头，不以 include 参数代替依赖。"""
    headers, has_source, has_generated = {}, False, False
    for path in sorted(used):
        if not _inside(path, prefix) or path.suffix != ".h":
            continue
        relative = path.relative_to(prefix)
        if "include" not in relative.parts:
            continue
        parts = relative.parts[relative.parts.index("include") + 1:]
        tail = Path(*parts)
        candidates = [child / "3rdparty/wlroots/include" / tail,
                      build / "wlroots/include" / tail,
                      build / "wlroots/protocol" / tail.name]
        matches = [p for p in candidates if p.is_file() and sha256_file(p) == sha256_file(path)]
        relevant = parts and (parts[0] == "wlr" or tail.name.endswith("-protocol.h"))
        if not relevant:
            continue
        if path not in installed or not matches:
            raise ValueError("installed R header differs from current source/build: " + str(path))
        source = matches[0]
        has_source |= _inside(source, child / "3rdparty/wlroots")
        has_generated |= str(source) in generated
        headers[str(path)] = {"source": str(source), "sha256": sha256_file(path)}
    if not has_source or not has_generated:
        raise ValueError("P compiler dependencies must use installed R source and generated headers")
    return headers
