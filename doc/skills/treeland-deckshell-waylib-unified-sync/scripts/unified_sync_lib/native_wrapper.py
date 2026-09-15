"""核验由 CMake 包装、原生 Meson 编译的固定 wlroots 子模块。"""

from __future__ import annotations

import json
import shlex
from pathlib import Path

from .artifacts import artifact_errors, read_verified_artifact, write_artifact
from .git_ops import sha256_file


def native_layout(model, child: Path, build: Path):
    """识别已验收的原生包装层；不把任意 utility target 当作编译证明。"""
    from .wrapper_build import _absolute

    source = Path(model["model"]["paths"]["source"]).resolve()
    wrappers = [target for target in model["targets"]
                if _absolute(target["paths"]["source"], source) == child / "wlroots"]
    if any(target.get("type") in {"SHARED_LIBRARY", "STATIC_LIBRARY", "OBJECT_LIBRARY"}
           for target in wrappers):
        return None
    native = [target for target in wrappers if target.get("type") == "UTILITY"
              and target.get("name") == "waylib_wlroots_native"]
    if len(native) != 1:
        return None
    return _absolute(native[0]["paths"]["build"], build) / "native"


def _library(targets, source, build):
    candidates = [target for target in targets if target.get("type") == "shared library"
                  and target.get("name", "").startswith("wlroots-")
                  and Path(target.get("defined_in", "")).resolve() == source / "meson.build"]
    if len(candidates) != 1 or len(candidates[0].get("filename", [])) != 1:
        raise ValueError("native wrapper must identify one R-root Meson wlroots library")
    library = Path(candidates[0]["filename"][0]).resolve()
    if library.parent != build or not library.is_file():
        raise ValueError("native wrapper library does not belong to its current build")
    return candidates[0], library


def _compiled_sources(target, commands, dependencies, source, build):
    from .wrapper_build import _absolute, _generated_headers

    compiled = {_absolute(row["file"], Path(row["directory"])): row for row in commands}
    upstream = {_absolute(path, source) for group in target.get("target_sources", [])
                for path in group.get("sources", [])}
    selected = {path for path in upstream if source in path.parents}
    errors = []
    if any(source not in path.parents and build not in path.parents for path in upstream):
        errors.append("native wrapper compiles sources outside candidate R or its generated tree")
    if not selected or not selected.issubset(compiled):
        errors.append("native wrapper compilation does not cover its actual R library sources")
    for path in selected & compiled.keys():
        row = compiled[path]
        arguments = row.get("arguments") or shlex.split(row["command"])
        cwd = Path(row["directory"])
        index = arguments.index("-c") if "-c" in arguments else len(arguments)
        if index + 1 >= len(arguments) or _absolute(arguments[index + 1], cwd) != path:
            errors.append("native wrapper compile command does not name its R source")
        output = row.get("output")
        index = arguments.index("-o") if "-o" in arguments else len(arguments)
        if not output and index + 1 < len(arguments):
            output = arguments[index + 1]
        if not output or _absolute(output, cwd) not in dependencies:
            errors.append("native wrapper R object lacks current compiler dependencies")
        if any("/usr/" in token and "wlroots" in token for token in arguments):
            errors.append("native wrapper compile command uses system wlroots headers")
    headers = _generated_headers(selected, compiled, dependencies, build)
    if not headers:
        errors.append("native wrapper generated headers are absent from R compiler dependencies")
    return errors, {str(path): sha256_file(path) for path in sorted(headers)}


def _checks(values, model, links, dependencies, child, build, native):
    from .wrapper_build import _consumer_links_wrapper, _ninja_dependencies

    source = child / "3rdparty/wlroots"
    target, library = _library(values["targets"], source, native)
    native_dependencies = _ninja_dependencies(values["dependencies"], native)
    errors, headers = _compiled_sources(target, values["compile_commands"], native_dependencies,
                                        source, native)
    consumers = [target for target in model["targets"]
                 if _consumer_links_wrapper(target, {library}, links, build)]
    if not consumers:
        errors.append("actual consumer link inputs do not use the native wrapper artifact")
    used = {path for paths in dependencies.values() for path in paths}
    if not any(source in path.parents for path in used) or not set(map(Path, headers)) & used:
        errors.append("C/P compiler dependencies do not use native R headers and generated headers")
    if "-lwlroots" in links or any("/usr/" in token and "libwlroots" in token
                                   for token in shlex.split(links)):
        errors.append("C/P build links system wlroots instead of native candidate R")
    if any(str(path).startswith("/usr/") and "wlroots" in str(path) for path in used):
        errors.append("C/P compiler dependencies use system wlroots headers")
    return errors, headers


def record_native_wrapper(model, links, dependencies, child, build, root, name):
    """保存真实 Meson 元数据及编译依赖，并验证 C/P 的具体消费目标。"""
    from .wrapper_build import _ninja_output

    native = native_layout(model, child, build)
    if native is None:
        return None
    values = {
        "targets": json.loads((native / "meson-info/intro-targets.json").read_text()),
        "compile_commands": json.loads((native / "compile_commands.json").read_text()),
        "dependencies": _ninja_output(native, "deps").decode(),
        "commands": _ninja_output(native, "commands").decode(),
    }
    errors, headers = _checks(values, model, links, dependencies, child, build, native)
    artifacts = {}
    for key, value in values.items():
        raw = value.encode() if isinstance(value, str) else (json.dumps(value, sort_keys=True) + "\n").encode()
        artifacts[key] = write_artifact(root, f"wrapper/{name}-native-{key}.json", raw)
    return {"build": str(native), "source": str(child / "3rdparty/wlroots"),
            "artifacts": artifacts, "generated_headers": headers,
            "blocked_reasons": errors, "outcome": "blocked" if errors else "pass"}


def native_wrapper_errors(record, model, links, dependencies, child, build, root):
    """报告端重读原生工件，不接受单独的 Meson 成功或未被使用的生成头。"""
    native = native_layout(model, child, build)
    if not isinstance(record, dict) or native is None or record.get("build") != str(native) or record.get("source") != str(child / "3rdparty/wlroots"):
        return ["native wrapper identity differs from the CMake model"], {}
    errors, values = [], {}
    for key in ("targets", "compile_commands", "dependencies", "commands"):
        artifact = record.get("artifacts", {}).get(key)
        failures = artifact_errors(artifact, root, "native wrapper " + key)
        errors.extend(failures)
        if not failures:
            _, raw = read_verified_artifact(artifact, root, key)
            values[key] = raw.decode() if key in {"dependencies", "commands"} else json.loads(raw)
    headers = {}
    if len(values) == 4:
        try:
            findings, headers = _checks(values, model, links, dependencies, child, build, native)
            errors.extend(findings)
            if record.get("generated_headers") != headers:
                errors.append("native generated header digests differ from actual compiler dependencies")
        except (OSError, KeyError, TypeError, ValueError) as error:
            errors.append(f"invalid native wrapper evidence: {error}")
    if record.get("outcome") != "pass" or record.get("blocked_reasons") != []:
        errors.append("native wrapper build did not pass")
    return errors, headers
