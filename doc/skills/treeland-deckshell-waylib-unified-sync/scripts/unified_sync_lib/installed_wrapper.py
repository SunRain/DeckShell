"""核验 P 默认安装包路线：C 源码/R 构建 → 安装产物 → P 实际链接和编译依赖。"""

from __future__ import annotations

import json
import shlex
from pathlib import Path

from .artifacts import read_verified_artifact, write_artifact
from .git_ops import canonical_json_sha256
from .installed_artifacts import installed_headers, installed_libraries
from .validation_dependencies import dependency_binding_errors
from .validation_paths import _resolved_option
from .wrapper_build import _absolute, _consumer_links_wrapper, _inside, wrapper_build_errors


def _candidate_chain(entries, manifest, root):
    from .validation_gates import _validation_entry_errors

    selected = {}
    for suffix in ("configure", "build", "install"):
        name = "waylib-candidate-" + suffix
        rows = [row for row in entries if row.get("id") == name]
        if len(rows) != 1:
            raise ValueError("installed-package evidence requires one " + name)
        row = rows[0]
        errors = _validation_entry_errors(row, root, manifest) + dependency_binding_errors(row, manifest)
        if errors:
            raise ValueError("; ".join(errors))
        selected[suffix] = row
    configure, compiled, install = (selected[key] for key in ("configure", "build", "install"))
    child = Path(manifest["identity"]["child_worktree"])
    build, prefix = _resolved_option(configure, "-B"), _resolved_option(install, "--prefix")
    if (build is None or prefix is None or _resolved_option(configure, "-S") != child
            or _resolved_option(compiled, "--build") != build
            or _resolved_option(install, "--install") != build):
        raise ValueError("installed-package configure/build/install chain differs")
    if any(token.startswith(("--component", "--strip")) for token in install["command"]):
        raise ValueError("installed-package evidence requires the full unstripped install")
    errors = wrapper_build_errors(compiled, manifest, root)
    if errors:
        raise ValueError("; ".join(errors))
    record = compiled["wrapper_build"]
    _, raw = read_verified_artifact(record["artifacts"]["codemodel"], root, "candidate codemodel")
    model = json.loads(raw)
    return selected, child, build, prefix, model, record["generated_headers"]


def _consumer_headers(target, model, commands, dependencies, build):
    source = Path(model["model"]["paths"]["source"])
    selected = {_absolute(row["path"], build if row.get("isGenerated") else source)
                for row in target.get("sources", []) if "compileGroupIndex" in row}
    result = set()
    for row in commands:
        cwd = Path(row["directory"])
        if _absolute(row["file"], cwd) not in selected:
            continue
        arguments = row.get("arguments") or shlex.split(row["command"])
        output = row.get("output")
        if not output and "-o" in arguments:
            output = arguments[arguments.index("-o") + 1]
        if output:
            result.update(dependencies.get(_absolute(output, cwd), []))
    return result


def _checks(entries, manifest, root, model, commands, links, dependencies, build):
    selected, child, cbuild, prefix, cmodel, generated = _candidate_chain(entries, manifest, root)
    raw_manifest = (cbuild / "install_manifest.txt").read_text(encoding="utf-8")
    installed = {Path(line).resolve() for line in raw_manifest.splitlines() if line}
    libraries = installed_libraries(cmodel, cbuild, prefix, installed)
    outputs = [Path(row["installed"]) for row in libraries.values()]
    consumers = [row for row in model["targets"] if all(
        _consumer_links_wrapper(row, {output}, links, build) for output in outputs)]
    if not consumers:
        raise ValueError("P actual consumer does not link both candidate installed libraries")
    used = set().union(*dependencies.values()) if dependencies else set()
    if any("wlroots" in str(p) and str(p).startswith("/usr/") for p in used):
        raise ValueError("P compiler dependencies use system wlroots headers")
    if any(_inside(p, child) or _inside(p, cbuild) for p in used):
        raise ValueError("installed-package P consumes C source/build headers")
    if "-lwlroots" in links or any("/usr/" in p and "libwlroots" in p for p in shlex.split(links)):
        raise ValueError("P links system wlroots")
    headers, failures = None, []
    for target in consumers:
        try:
            headers = installed_headers(_consumer_headers(target, model, commands, dependencies, build),
                                        child, cbuild, prefix, installed, generated)
            break
        except ValueError as error:
            failures.append(str(error))
    if headers is None:
        raise ValueError("; ".join(failures))
    return {"prefix": str(prefix), "candidate_build": str(cbuild),
            "libraries": libraries, "headers": headers,
            "generated_headers": {p: row["sha256"] for p, row in headers.items()
                                  if row["source"] in generated}}, list(selected.values())


def record_installed_wrapper(bundle, manifest, root, name, model, commands, links, dependencies, build):
    """保存已验证的 C 构建/安装记录，并与 P 的真实消费输入交叉核对。"""
    if not isinstance(bundle, dict):
        raise ValueError("installed-package P requires candidate validations in the same bundle")
    result, entries = _checks(bundle.get("entries", []), manifest, root, model, commands,
                             links, dependencies, build)
    result["candidate_validations"] = write_artifact(
        root, f"wrapper/{name}-installed-candidate.json",
        (json.dumps(entries, sort_keys=True) + "\n").encode())
    result["manifest_sha256"] = canonical_json_sha256(manifest)
    return result


def installed_wrapper_errors(record, manifest, root, model, commands, links, dependencies, build):
    """报告端重算安装消费链；替换旧包、库、头文件或验证身份都会失败。"""
    try:
        _, raw = read_verified_artifact(record["candidate_validations"], root, "installed candidate validations")
        expected, _ = _checks(json.loads(raw), manifest, root, model, commands, links, dependencies, build)
        expected.update(candidate_validations=record["candidate_validations"],
                        manifest_sha256=canonical_json_sha256(manifest))
        if expected != record:
            return ["installed package artifacts differ from the recorded candidate"], {}
        return [], expected["generated_headers"]
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as error:
        return [f"invalid installed-package evidence: {error}"], {}
