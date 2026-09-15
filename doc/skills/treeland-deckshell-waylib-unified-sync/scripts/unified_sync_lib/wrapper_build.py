"""从 CMake file API、编译数据库和实际链接命令核验 wrapper 使用本次 R。"""

from __future__ import annotations

import json
import shlex
import subprocess
from pathlib import Path
from typing import Any, Mapping

from .artifacts import artifact_errors, read_verified_artifact, write_artifact
from .git_ops import canonical_json_sha256, sha256_file
from .replay_types import GITLINK_PATH
from .schema import WLROOTS_ROOT


def _inside(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def _absolute(value: str, root: Path) -> Path:
    path = Path(value)
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def prepare_cmake_query(command, cwd: Path) -> None:
    """fresh configure 前请求 codemodel；创建 query 不复用既有 build。"""

    from .validation_paths import _resolved_option
    build = _resolved_option({"command": command, "cwd": str(cwd)}, "-B")
    if build is None or "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON" not in command:
        raise ValueError("active wlroots CMake configure requires CMAKE_EXPORT_COMPILE_COMMANDS=ON")
    query = build / ".cmake/api/v1/query/codemodel-v2"
    query.parent.mkdir(parents=True, exist_ok=True)
    query.touch()


def _read_model(build: Path):
    reply = build / ".cmake/api/v1/reply"
    indexes = sorted(reply.glob("index-*.json"))
    if len(indexes) != 1:
        raise ValueError("fresh CMake build requires exactly one file API reply index")
    index = json.loads(indexes[0].read_text(encoding="utf-8"))
    model_file = index["reply"]["codemodel-v2"]["jsonFile"]
    model = json.loads((reply / model_file).read_text(encoding="utf-8"))
    targets = [json.loads((reply / target["jsonFile"]).read_text(encoding="utf-8"))
               for config in model["configurations"] for target in config["targets"]]
    return {"index": index, "model": model, "targets": targets}


def _ninja_dependencies(output: str, build: Path):
    result, current = {}, None
    for line in output.splitlines():
        if ": #deps " in line:
            name, details = line.split(": #deps ", 1)
            current = _absolute(name, build) if "(VALID)" in details else None
            if current is not None:
                result[current] = []
        elif current is not None and line.startswith("    "):
            result[current].append(_absolute(line[4:], build))
    return result


def _generated_headers(selected, compiled, dependencies, build):
    headers = set()
    for path in selected:
        row = compiled.get(path)
        if row is None:
            continue
        arguments = row.get("arguments") or shlex.split(row["command"])
        output = row.get("output")
        if not output and "-o" in arguments and arguments.index("-o") + 1 < len(arguments):
            output = arguments[arguments.index("-o") + 1]
        if output:
            object_path = _absolute(output, Path(row["directory"]))
            headers.update(path for path in dependencies.get(object_path, [])
                           if _inside(path, build) and path.suffix == ".h" and path.is_file())
    return headers


def _link_segments(commands, build):
    for line in commands.splitlines():
        lexer = shlex.shlex(line, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        lexer.commenters = ""
        segment = []
        cwd = build
        for token in lexer:
            if token in {";", "&&", "||", "|", "&"}:
                if len(segment) == 2 and segment[0] == "cd":
                    cwd = _absolute(segment[1], cwd)
                elif segment:
                    yield segment, cwd
                segment = []
            else:
                segment.append(token)
        if segment:
            yield segment, cwd


def _consumer_links_wrapper(consumer, outputs, links, build):
    libraries = {_absolute(token, build)
                 for fragment in consumer.get("link", {}).get("commandFragments", [])
                 if fragment.get("role") == "libraries"
                 for token in shlex.split(fragment["fragment"]) if not token.startswith("-")}
    required = outputs & libraries
    artifacts = {_absolute(row["path"], build) for row in consumer.get("artifacts", [])}
    if not required or not artifacts:
        return False
    for arguments, cwd in _link_segments(links, build):
        if "-o" not in arguments or "-c" in arguments:
            continue
        index = arguments.index("-o")
        if index + 1 >= len(arguments) or _absolute(arguments[index + 1], cwd) not in artifacts:
            continue
        inputs = {_absolute(token, cwd) for i, token in enumerate(arguments)
                  if i not in {index, index + 1} and not token.startswith("-")}
        if required.issubset(inputs):
            return True
    return False


def _wrapper_link_errors(target, targets, links, build, source, wrapper):
    outputs = {_absolute(row["path"], build) for row in target.get("artifacts", [])}
    consumers = [row for row in targets
                 if _absolute(row["paths"]["source"], source) != wrapper
                 and any(dep["id"] == target["id"] for dep in row.get("dependencies", []))]
    errors = []
    if not outputs or not any(_consumer_links_wrapper(row, outputs, links, build) for row in consumers):
        errors.append("actual consumer link inputs do not use the candidate wrapper artifact")
    if any(not path.is_file() for path in outputs):
        errors.append("wrapper compiled artifact is missing")
    return errors


def _wrapper_errors(model, commands, links: str, child: Path, build: Path, dependencies):
    source = Path(model["model"]["paths"]["source"]).resolve()
    dependency = child / WLROOTS_ROOT
    wrapper = child / "wlroots"
    targets = model["targets"]
    wrappers = [target for target in targets if _absolute(target["paths"]["source"], source) == wrapper]
    actual = [target for target in wrappers if target.get("type") in {"SHARED_LIBRARY", "STATIC_LIBRARY", "OBJECT_LIBRARY"}]
    if not actual:
        return ["CMake codemodel has no compiled wlroots wrapper target"]
    errors = []
    compiled = {_absolute(row["file"], Path(row["directory"])): row for row in commands}
    for target in actual:
        upstream = [_absolute(row["path"], build if row.get("isGenerated") else source)
                    for row in target.get("sources", []) if "compileGroupIndex" in row]
        selected = [path for path in upstream if _inside(path, dependency)]
        if not selected or any(path not in compiled for path in selected):
            errors.append("wrapper compilation does not include candidate R sources")
        if any(not _inside(path, dependency) and not _inside(path, build) for path in upstream):
            errors.append("wrapper compiles sources outside candidate R or its generated build tree")
        for path in selected:
            if path not in compiled:
                continue
            row = compiled[path]
            arguments = row.get("arguments") or shlex.split(row["command"])
            if str(path) not in arguments:
                errors.append("wrapper compile command does not name its actual R source")
            if any("/usr/" in value and "wlroots" in value for value in arguments):
                errors.append("wrapper compile command uses system wlroots headers")
        headers = _generated_headers(selected, compiled, dependencies, build)
        if not headers:
            errors.append("wrapper generated headers are absent from actual compiler dependencies")
        errors.extend(_wrapper_link_errors(target, targets, links, build, source, wrapper))
    if "-lwlroots" in links or any("/usr/" in token and "libwlroots" in token for token in shlex.split(links)):
        errors.append("C/P build links system wlroots instead of candidate R")
    return errors


def _ninja_output(build: Path, action: str) -> bytes:
    result = subprocess.run(["ninja", "-C", str(build), "-t", action], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    if result.returncode:
        raise ValueError(f"cannot inspect Ninja {action}: " + result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def _header_digests(commands, dependencies, build, child):
    compiled = {_absolute(row["file"], Path(row["directory"])): row for row in commands}
    selected = [path for path in compiled if _inside(path, child / WLROOTS_ROOT)]
    headers = _generated_headers(selected, compiled, dependencies, build)
    return {str(path): sha256_file(path) for path in sorted(headers)}


def record_wrapper_build(command, cwd: Path, manifest: Mapping[str, Any], root: Path, name: str):
    """构建完成后保存编译数据库、codemodel 与 Ninja 实际命令。"""

    from .validation_paths import _resolved_option
    from .native_wrapper import record_native_wrapper
    build = _resolved_option({"command": command, "cwd": str(cwd)}, "--build")
    if build is None:
        raise ValueError("wrapper build requires a CMake --build directory")
    child = cwd / GITLINK_PATH if name.startswith("deckshell-") else cwd
    model = _read_model(build)
    commands = json.loads((build / "compile_commands.json").read_text(encoding="utf-8"))
    links, raw_dependencies = _ninja_output(build, "commands"), _ninja_output(build, "deps")
    dependencies = _ninja_dependencies(raw_dependencies.decode("utf-8"), build)
    native = record_native_wrapper(model, links.decode("utf-8"), dependencies, child, build, root, name)
    errors = native["blocked_reasons"] if native is not None else _wrapper_errors(
        model, commands, links.decode("utf-8"), child, build, dependencies)
    records = {key: write_artifact(root, f"wrapper/{name}-{key}.json", (json.dumps(value, sort_keys=True) + "\n").encode())
               for key, value in (("codemodel", model), ("compile_commands", commands))}
    records["link_commands"] = write_artifact(root, f"wrapper/{name}-commands.log", links)
    records["compiler_dependencies"] = write_artifact(root, f"wrapper/{name}-dependencies.log", raw_dependencies)
    result = {"manifest_sha256": canonical_json_sha256(manifest), "child": str(child), "build": str(build),
              "generated_headers": native["generated_headers"] if native is not None else _header_digests(commands, dependencies, build, child),
              "artifacts": records, "blocked_reasons": errors, "outcome": "blocked" if errors else "pass"}
    if native is not None:
        result["native_meson"] = native
    return result


def wrapper_build_errors(entry: Mapping[str, Any], manifest: Mapping[str, Any], root: Path):
    """报告端重读原始构建证据，验证候选 R 与顶层构建的实际绑定。"""

    from .validation_paths import _resolved_option
    from .native_wrapper import native_wrapper_errors
    record = entry.get("wrapper_build")
    if not isinstance(record, dict):
        return [f"wrapper build evidence is missing: {entry.get('id')}"]
    build = _resolved_option(entry, "--build")
    child = Path(entry["cwd"]) / GITLINK_PATH if entry["id"].startswith("deckshell-") else Path(entry["cwd"])
    errors = []
    if record.get("manifest_sha256") != canonical_json_sha256(manifest) or record.get("child") != str(child) or record.get("build") != str(build):
        errors.append("wrapper build identity differs from the current candidate")
    values = {}
    for key in ("codemodel", "compile_commands", "link_commands", "compiler_dependencies"):
        artifact = record.get("artifacts", {}).get(key)
        failures = artifact_errors(artifact, root, "wrapper " + key)
        errors.extend(failures)
        if not failures:
            _, raw = read_verified_artifact(artifact, root, key)
            values[key] = raw.decode("utf-8") if key in {"link_commands", "compiler_dependencies"} else json.loads(raw.decode("utf-8"))
    if len(values) == 4:
        dependencies = _ninja_dependencies(values["compiler_dependencies"], build)
        if "native_meson" in record:
            findings, headers = native_wrapper_errors(record["native_meson"], values["codemodel"], values["link_commands"], dependencies, child, build, root)
            errors.extend(findings)
        else:
            errors.extend(_wrapper_errors(values["codemodel"], values["compile_commands"], values["link_commands"], child, build, dependencies))
            headers = _header_digests(values["compile_commands"], dependencies, build, child)
        if record.get("generated_headers") != headers:
            errors.append("wrapper generated header digests differ from actual compiler dependencies")
    if record.get("outcome") != "pass" or record.get("blocked_reasons") != []:
        errors.append("wrapper build did not pass")
    return errors
