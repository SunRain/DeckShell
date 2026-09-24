#!/usr/bin/env python3
"""无 shell 执行验证命令，并把日志与结果写入证据 bundle。"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.build_commands import full_build_command_errors
from unified_sync_lib.git_ops import atomic_write_json, canonical_json_sha256, read_json
from unified_sync_lib.validation_dependencies import (
    capture_dependencies, checkout_errors as _nested_identity_errors,
    checkout_identity as _nested_identity, git_identity as _git_identity,
)
from unified_sync_lib.validation_paths import fresh_path_evidence, validation_output_path_errors
from unified_sync_lib.ctest_results import parse_ctest as _test_result, record_ctest_discovery, discovery_errors
from unified_sync_lib.native_validation import (
    BASE_NATIVE_IDS, empty_native_baseline, native_absence_errors,
    prepare_native_test, record_native_discovery, record_native_result,
)
from unified_sync_lib.wrapper_build import prepare_cmake_query, record_wrapper_build


VALID_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")


def parser() -> argparse.ArgumentParser:
    """Build the command-validation CLI parser."""

    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--id", required=True)
    result.add_argument("--category", required=True, choices=("build", "test", "consumer"))
    result.add_argument("--cwd", required=True, type=Path)
    result.add_argument("--artifact-root", required=True, type=Path)
    result.add_argument("--bundle", required=True, type=Path)
    result.add_argument("--manifest", type=Path, help="冻结的三仓 manifest；激活 R 时必需")
    result.add_argument(
        "--nested-checkout",
        type=Path,
        help="parent 命令实际使用的 nested child checkout",
    )
    result.add_argument(
        "--nested-head",
        help="nested child checkout 必须保持的完整 candidate SHA",
    )
    result.add_argument("command", nargs=argparse.REMAINDER)
    return result


def _load_bundle(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {
            "schema_version": 2,
            "kind": "treeland-unified-command-validations",
            "entries": [],
        }
    payload = read_json(path)
    if payload.get("schema_version") != 2 or payload.get("kind") != "treeland-unified-command-validations":
        raise ValueError("validation bundle schema or kind is invalid")
    if not isinstance(payload.get("entries"), list):
        raise ValueError("validation bundle entries must be an array")
    return payload


def _command(args: argparse.Namespace) -> List[str]:
    command = list(args.command)
    if command and command[0] == "--":
        command.pop(0)
    if not command:
        raise ValueError("validation command is required after --")
    return command


def _attempt_number(bundle: Mapping[str, Any], validation_id: str) -> int:
    matches = [
        entry for entry in bundle["entries"]
        if isinstance(entry, dict) and entry.get("id") == validation_id
    ]
    if len(matches) > 1:
        raise ValueError(f"validation bundle has duplicate id: {validation_id}")
    if not matches:
        return 1
    previous = matches[0].get("attempt", 1)
    if not isinstance(previous, int) or previous < 1:
        raise ValueError(f"validation attempt is invalid: {validation_id}")
    return previous + 1


def _store_entry(bundle: Dict[str, Any], entry: Dict[str, Any]) -> None:
    for index, current in enumerate(bundle["entries"]):
        if not isinstance(current, dict) or current.get("id") != entry["id"]:
            continue
        history = current.get("previous_attempts", [])
        if not isinstance(history, list):
            raise ValueError(f"validation history is invalid: {entry['id']}")
        snapshot = {key: value for key, value in current.items() if key != "previous_attempts"}
        entry["previous_attempts"] = [*history, snapshot]
        bundle["entries"][index] = entry
        return
    bundle["entries"].append(entry)


def _fresh_paths_before(
    validation_id: str, command: Sequence[str], cwd: Path
) -> Dict[str, Dict[str, Any]]:
    evidence = fresh_path_evidence(validation_id, list(command), str(cwd))
    if not evidence:
        return {}
    path = Path(next(iter(evidence.values()))["path"])
    if os.path.lexists(str(path)):
        raise ValueError(
            f"fresh path must not exist before validation {validation_id}: {path}"
        )
    return evidence


def _prepare_wrapper_query(args, manifest, command, cwd):
    active_wrapper = manifest is not None and manifest["identity"].get("wlroots") is not None
    if active_wrapper and args.id == "waylib-base-configure":
        active_wrapper = manifest["identity"]["wlroots"]["registered_at_base"]
    if active_wrapper and args.id in {"deckshell-configure", "waylib-base-configure", "waylib-candidate-configure"}:
        prepare_cmake_query(command, cwd)


def _prepare_test_evidence(args, command, cwd, attempt, native_baseline):
    discovery, native_discovery, native_log_identity = None, None, None
    if native_baseline is None:
        if args.category in {"test", "consumer"} and Path(command[0]).name == "ctest":
            discovery = record_ctest_discovery(command, cwd, args.artifact_root, f"{args.id}-attempt-{attempt}")
        elif args.id in {"wlroots-base-test", "wlroots-candidate-test"}:
            command, native_log_identity = prepare_native_test(command, cwd, f"{args.id}-attempt-{attempt}")
            native_discovery = record_native_discovery(command, cwd, args.artifact_root, f"{args.id}-attempt-{attempt}")
    return command, discovery, native_discovery, native_log_identity


def _prepare_validation(args: argparse.Namespace) -> Dict[str, Any]:
    if not VALID_ID.fullmatch(args.id):
        raise ValueError(
            "validation id may contain only lowercase letters, digits, and hyphens"
        )
    if not args.cwd.resolve().is_dir():
        raise ValueError(f"validation cwd is not a directory: {args.cwd}")
    command = _command(args)
    command_errors = full_build_command_errors(args.id, command)
    if command_errors:
        raise ValueError("; ".join(command_errors))
    if bool(args.nested_checkout) != bool(args.nested_head):
        raise ValueError("--nested-checkout 和 --nested-head 必须同时提供")
    nested_path = args.nested_checkout.absolute() if args.nested_checkout else None
    if args.nested_head and not FULL_SHA.fullmatch(args.nested_head):
        raise ValueError("--nested-head 必须是 40 位完整 commit SHA")
    bundle = _load_bundle(args.bundle)
    attempt = _attempt_number(bundle, args.id)
    cwd = args.cwd.resolve()
    fresh_paths = _fresh_paths_before(args.id, command, cwd)
    manifest = read_json(args.manifest) if args.manifest else None
    checkouts = capture_dependencies(manifest, args.id, cwd) if manifest else None
    native_baseline = empty_native_baseline(manifest) if args.id in BASE_NATIVE_IDS else None
    path_errors = validation_output_path_errors(fresh_paths, cwd, manifest, args.artifact_root)
    if path_errors:
        raise ValueError("; ".join(path_errors))
    nested_head = args.nested_head
    if checkouts and nested_path is None and "child" in checkouts["dependencies"]:
        child = checkouts["dependencies"]["child"]
        nested_path, nested_head = Path(child["worktree"]), child["head"]
    command, discovery, native_discovery, native_log_identity = _prepare_test_evidence(
        args, command, cwd, attempt, native_baseline
    )
    nested_before = (
        _nested_identity(nested_path) if nested_path is not None else None
    )
    if nested_path is not None:
        nested_errors = _nested_identity_errors(
            nested_before, nested_path, nested_head
        )
        if nested_errors:
            raise ValueError("; ".join(nested_errors))
    _prepare_wrapper_query(args, manifest, command, cwd)
    return {
        "command": command,
        "bundle": bundle,
        "attempt": attempt,
        "cwd": cwd,
        "fresh_paths": fresh_paths,
        "git_before": _git_identity(cwd),
        "nested_path": nested_path,
        "nested_before": nested_before,
        "nested_head": nested_head,
        "manifest": manifest,
        "checkouts_before": checkouts,
        "test_discovery": discovery,
        "native_discovery": native_discovery,
        "native_log_identity": native_log_identity,
        "native_baseline": native_baseline,
    }


def _record_absent_native_base(args, prepared):
    manifest, cwd = prepared["manifest"], prepared["cwd"]
    entry = {
        "id": args.id, "attempt": prepared["attempt"], "category": args.category,
        "command": prepared["command"], "cwd": str(cwd),
        "outcome": "not-applicable", "executed": False, "exit_code": None,
        "native_baseline": prepared["native_baseline"],
        "manifest_sha256": canonical_json_sha256(manifest),
        "git_identity": {"before": prepared["git_before"], "after": _git_identity(cwd)},
        "checkout_identity": {"before": prepared["checkouts_before"],
                              "after": capture_dependencies(manifest, args.id, cwd)},
        "log": write_artifact(
            args.artifact_root, f"logs/{args.id}-attempt-{prepared['attempt']}-not-applicable.json",
            (json.dumps(prepared["native_baseline"], sort_keys=True) + "\n").encode("utf-8"),
        ),
    }
    errors = native_absence_errors(entry, args.artifact_root, manifest)
    if errors:
        raise ValueError("; ".join(errors))
    return entry


def _run_validation(
    command: Sequence[str],
    cwd: Path,
    nested_path: Optional[Path],
    nested_head: Optional[str],
) -> Dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=str(cwd),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    nested_after = (
        _nested_identity(nested_path) if nested_path is not None else None
    )
    nested_errors = (
        _nested_identity_errors(nested_after, nested_path, nested_head)
        if nested_path is not None and nested_head is not None
        else []
    )
    return {
        "completed": completed,
        "git_after": _git_identity(cwd),
        "nested_after": nested_after,
        "nested_errors": nested_errors,
    }


def _validation_details(
    category: str, output: bytes, exit_code: int, nested_errors: Sequence[str]
) -> Dict[str, Any]:
    details = (
        _test_result(output, exit_code)
        if category in {"test", "consumer"}
        else {"outcome": "pass" if exit_code == 0 else "fail"}
    )
    if nested_errors:
        details["outcome"] = "fail"
        details["nested_checkout_errors"] = list(nested_errors)
    return details


def _record_dependency_bindings(args, prepared, entry, completed):
    if prepared["manifest"] is not None:
        entry["manifest_sha256"] = canonical_json_sha256(prepared["manifest"])
        after = None
        try:
            after = capture_dependencies(prepared["manifest"], args.id, prepared["cwd"])
        except (ValueError, RuntimeError) as error:
            entry.update(outcome="fail", dependency_errors=[str(error)])
        entry["checkout_identity"] = {"before": prepared["checkouts_before"], "after": after}
        r = prepared["manifest"]["identity"].get("wlroots")
        build_ids = {"deckshell-build", "waylib-candidate-build"}
        if r and r["registered_at_base"]:
            build_ids.add("waylib-base-build")
        if r and args.id in build_ids and completed.returncode == 0:
            try:
                entry["wrapper_build"] = record_wrapper_build(prepared["command"], prepared["cwd"], prepared["manifest"],
                                                              args.artifact_root, f"{args.id}-attempt-{prepared['attempt']}",
                                                              prepared["bundle"])
                if entry["wrapper_build"]["outcome"] != "pass":
                    entry["outcome"] = "fail"
            except (OSError, ValueError, RuntimeError, KeyError) as error:
                entry.update(outcome="fail", wrapper_errors=[str(error)])


def _build_entry(
    args: argparse.Namespace,
    prepared: Mapping[str, Any],
    result: Mapping[str, Any],
    log: Mapping[str, Any],
) -> Dict[str, Any]:
    completed = result["completed"]
    details = _validation_details(args.category, completed.stdout, completed.returncode, result["nested_errors"])
    if prepared["native_discovery"] is not None:
        details = record_native_result(prepared["command"], prepared["cwd"], prepared["native_discovery"], completed.returncode,
                                       args.artifact_root, f"{args.id}-attempt-{prepared['attempt']}", prepared["native_log_identity"])
    entry = {
        "id": args.id,
        "attempt": prepared["attempt"],
        "category": args.category,
        "command": prepared["command"],
        "cwd": str(prepared["cwd"]),
        "exit_code": completed.returncode,
        "log": log,
        "git_identity": {
            "before": prepared["git_before"],
            "after": result["git_after"],
        },
        "fresh_paths": prepared["fresh_paths"],
        **details,
    }
    if prepared["nested_path"] is not None:
        entry["nested_checkout"] = {
            "path": str(prepared["nested_path"]),
            "expected_head": prepared["nested_head"],
            "before": prepared["nested_before"],
            "after": result["nested_after"],
        }
    if prepared["test_discovery"] is not None:
        entry["test_discovery"] = prepared["test_discovery"]
        errors = discovery_errors(entry, args.artifact_root)
        if errors:
            entry.update(outcome="fail", discovery_errors=errors)
    if prepared["git_before"] != result["git_after"]:
        entry.update(outcome="fail", git_identity_errors=["Git identity changed during validation"])
    _record_dependency_bindings(args, prepared, entry, completed)
    return entry


def _persist_entry(
    args: argparse.Namespace,
    bundle: Dict[str, Any],
    entry: Dict[str, Any],
) -> None:
    _store_entry(bundle, entry)
    atomic_write_json(args.bundle, bundle)
    if args.category == "consumer":
        atomic_write_json(
            args.artifact_root / "waylib-package-consumer-result.json",
            {
                "schema_version": 2,
                "kind": "waylib-package-consumer-result",
                **entry,
            },
        )


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run one command without a shell and persist its validation evidence."""

    args = parser().parse_args(argv)
    try:
        prepared = _prepare_validation(args)
        if prepared["native_baseline"] is not None:
            entry = _record_absent_native_base(args, prepared)
            _persist_entry(args, prepared["bundle"], entry)
            return 0
        result = _run_validation(
            prepared["command"],
            prepared["cwd"],
            prepared["nested_path"],
            prepared["nested_head"],
        )
        log = write_artifact(
            args.artifact_root,
            f"logs/{args.id}-attempt-{prepared['attempt']}.log",
            result["completed"].stdout,
        )
        entry = _build_entry(args, prepared, result, log)
        _persist_entry(args, prepared["bundle"], entry)
        return 0 if entry["outcome"] in {"pass", "no-tests"} else 2
    except (OSError, ValueError, RuntimeError) as error:
        print(f"验证记录失败：{error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
