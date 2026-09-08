"""Installed Waylib package contract snapshot and comparison."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

from .artifacts import artifact_errors
from .ctest_results import ctest_evidence_errors, discovery_errors
from .namespace_contract import namespace_contract
from .namespace_probe import namespace_probe_errors
from .pkg_config import installed_pkg_config, pkg_config_snapshot_errors
from .git_ops import (
    canonical_json_sha256,
    resolve_commit,
    sha256_bytes,
    sha256_file,
    stable_unique,
)
from .installed_targets import installed_target_properties
from .source_contracts import (
    build_source_contract_snapshot,
    build_source_contract_snapshot_at,
)


HEADER_SUFFIXES = {".h", ".hh", ".hpp", ".hxx"}
SOURCE_CONTRACT_FIELDS = (
    "core_targets",
    "install_directives",
    "package_directives",
    "public_include_directives",
    "export_namespaces",
    "target_contract_properties",
    "contract_variable_definitions",
    "cmake_execution_context",
    "cmake_presets",
    "public_namespaces",
)


def _relative_files(root: Path) -> List[Path]:
    return sorted(
        (path for path in root.rglob("*") if path.is_file() or path.is_symlink()),
        key=lambda path: path.relative_to(root).as_posix(),
    )


def _read_text(path: Path) -> str:
    if path.is_symlink():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _file_digest(path: Path) -> str:
    if path.is_symlink():
        return sha256_bytes(os.readlink(str(path)).encode("utf-8"))
    return sha256_file(path)


def _is_public_header(relative: Path) -> bool:
    return "include" in relative.parts and relative.suffix.lower() in HEADER_SUFFIXES


def _package_cmake(relative: Path) -> bool:
    name = relative.name.lower()
    return relative.suffix.lower() == ".cmake" and (
        "config" in name or "targets" in name
    )


def _snapshot_payload(root: Path, files: Sequence[Path]) -> Dict[str, Any]:
    relatives = [path.relative_to(root) for path in files]
    headers = [path for path in relatives if _is_public_header(path)]
    cmake_files = [path for path in relatives if _package_cmake(path)]
    properties = installed_target_properties(root, cmake_files)
    namespace_data = namespace_contract({relative.as_posix(): _read_text(root / relative) for relative in headers})
    if namespace_data["errors"]:
        raise ValueError("; ".join(namespace_data["errors"]))
    exported = sorted(properties)
    return {
        "installed_paths": [path.as_posix() for path in relatives],
        "file_sha256": {
            path.as_posix(): _file_digest(root / path) for path in relatives
        },
        "public_headers": [path.as_posix() for path in headers],
        "cmake_package_files": [path.as_posix() for path in cmake_files],
        "exported_targets": exported,
        "exported_target_properties": properties,
        "export_namespaces": sorted(
            {target.split("::", 1)[0] + "::" for target in exported if "::" in target}
        ),
        "public_namespaces": namespace_data["namespaces"],
        "namespace_headers": namespace_data["headers"],
        "pkg_config": installed_pkg_config(root, relatives),
    }


def build_install_snapshot(
    install_root: Path, source_root: Optional[Path] = None
) -> Dict[str, Any]:
    """Snapshot the complete installed file and package-facing contract."""

    root = install_root.resolve()
    if not root.is_dir():
        raise ValueError(f"install root is not a directory: {root}")
    data = _snapshot_payload(root, _relative_files(root))
    if source_root is not None:
        data["source_contract"] = build_source_contract_snapshot(source_root)
    canonical = json.dumps(
        data, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return {
        "schema_version": 2,
        "kind": "waylib-install-contract-snapshot",
        "install_root": str(root),
        "snapshot_sha256": sha256_bytes(canonical),
        **data,
    }


def _list_drift(before: Sequence[str], after: Sequence[str]) -> Dict[str, List[str]]:
    return {
        "removed": sorted(set(before) - set(after)),
        "added": sorted(set(after) - set(before)),
    }


def source_contract_drift(
    before: Mapping[str, Any], after: Mapping[str, Any]
) -> Dict[str, Any]:
    """Return protected source-contract changes between two frozen snapshots."""

    result = {
        field: _list_drift(before.get(field, []), after.get(field, []))
        for field in SOURCE_CONTRACT_FIELDS
        if before.get(field, []) != after.get(field, [])
    }
    left, right = before.get("cmake_execution_context", []), after.get("cmake_execution_context", [])
    if [value for value in left if value in right] != [value for value in right if value in left]:
        result["cmake_execution_context"] = {"removed": left, "added": right}
    return result


def build_source_contract_audit(
    repo: Path, before: str, after: str, approved_additions: Any = None,
) -> Dict[str, Any]:
    """Compare source CMake contracts for one adjacent child commit transition."""

    before_commit = resolve_commit(repo, before)
    after_commit = resolve_commit(repo, after)
    before_snapshot = build_source_contract_snapshot_at(repo, before_commit)
    after_snapshot = build_source_contract_snapshot_at(repo, after_commit)
    drift = source_contract_drift(before_snapshot, after_snapshot)
    blockers = [f"source contract drift: {field}" for field in drift]
    blockers.extend(before_snapshot.get("namespace_errors", []))
    blockers.extend(after_snapshot.get("namespace_errors", []))
    if approved_additions is not None:
        wrapper = after_snapshot.get("wrapper_contract") or {}
        if (not isinstance(approved_additions, dict)
                or approved_additions.get("review_state") != "approved"
                or approved_additions.get("before_snapshot_sha256") != canonical_json_sha256(before_snapshot)
                or approved_additions.get("after_snapshot_sha256") != canonical_json_sha256(after_snapshot)
                or approved_additions.get("additions") != {field: change["added"] for field, change in drift.items()}):
            blockers.append("wrapper contract approval does not bind the exact snapshots/additions")
        elif any(change["removed"] or field == "public_namespaces" or not set(change["added"]).issubset(wrapper.get(field, [])) for field, change in drift.items()):
            blockers.append("wrapper approval cannot relax existing Waylib contracts")
        else:
            blockers = [value for value in blockers if not value.startswith("source contract drift:")]
    return {
        "schema_version": 2,
        "kind": "waylib-source-contract-audit",
        "before_commit": before_commit,
        "after_commit": after_commit,
        "before_snapshot_sha256": canonical_json_sha256(before_snapshot),
        "after_snapshot_sha256": canonical_json_sha256(after_snapshot),
        "before_snapshot": before_snapshot,
        "after_snapshot": after_snapshot,
        "drift": drift,
        "approved_additions": approved_additions,
        "blocked_reasons": blockers,
        "outcome": "blocked" if blockers else "pass",
    }


def source_contract_audit_errors(
    repo: Path, before: str, after: str, audit: Any
) -> List[str]:
    """Recompute one child contract audit and return evidence integrity errors."""

    if not isinstance(audit, dict):
        return ["child source contract audit is missing"]
    expected = build_source_contract_audit(repo, before, after, audit.get("approved_additions"))
    if audit != expected:
        return ["child source contract audit differs from Git objects"]
    if expected["outcome"] != "pass":
        return list(expected["blocked_reasons"])
    return []


def _contract_drift(
    before: Mapping[str, Any], after: Mapping[str, Any]
) -> Dict[str, Any]:
    drift: Dict[str, Any] = {}
    list_fields = (
        "installed_paths",
        "public_headers",
        "cmake_package_files",
        "exported_targets",
        "export_namespaces",
        "public_namespaces",
    )
    for field in list_fields:
        if before.get(field) != after.get(field):
            drift[field] = _list_drift(before.get(field, []), after.get(field, []))
    for field in ("exported_target_properties", "pkg_config"):
        if before.get(field) != after.get(field):
            drift[field] = {"before": before.get(field, {}), "after": after.get(field, {})}
    source_before = before.get("source_contract")
    source_after = after.get("source_contract")
    if source_before is not None or source_after is not None:
        left = source_before if isinstance(source_before, dict) else {}
        right = source_after if isinstance(source_after, dict) else {}
        drift.update(
            {
                f"source_{field}": value
                for field, value in source_contract_drift(left, right).items()
            }
        )
    return drift


def _snapshot_errors(snapshot: Mapping[str, Any], label: str) -> List[str]:
    errors: List[str] = []
    if snapshot.get("schema_version") != 2:
        errors.append(f"{label} snapshot schema_version must be 2")
    if snapshot.get("kind") != "waylib-install-contract-snapshot":
        errors.append(f"{label} snapshot kind is invalid")
    required = (
        "installed_paths", "public_headers", "cmake_package_files",
        "exported_targets", "exported_target_properties", "export_namespaces",
        "public_namespaces", "pkg_config",
    )
    errors.extend(f"{label} snapshot missing {field}" for field in required if field not in snapshot)
    errors.extend(pkg_config_snapshot_errors(snapshot.get("pkg_config"), snapshot.get("installed_paths", []), label))
    source = snapshot.get("source_contract")
    if source is not None and (not isinstance(source, dict) or not isinstance(source.get("cmake_execution_context"), list)):
        errors.append(f"{label} source snapshot lacks CMake execution context; regenerate the snapshot")
    properties = snapshot.get("exported_target_properties")
    if not isinstance(properties, dict) or any(
        not isinstance(target, str) or not isinstance(values, dict)
        or any(not isinstance(name, str) or not isinstance(value, str) for name, value in values.items())
        for target, values in properties.items()
    ):
        errors.append(f"{label} exported_target_properties must map targets to string properties")
    return errors


def _consumer_errors(
    consumer: Any, artifact_root: Path
) -> List[str]:
    if not isinstance(consumer, dict):
        return ["passing package consumer evidence is required"]
    errors: List[str] = []
    if consumer.get("schema_version") != 2 or consumer.get("kind") != "waylib-package-consumer-result":
        errors.append("consumer evidence schema or kind is invalid")
    if consumer.get("outcome") != "pass" or consumer.get("exit_code") != 0:
        errors.append("package consumer did not pass")
    command = consumer.get("command")
    if not isinstance(command, list) or not command or not all(isinstance(arg, str) for arg in command):
        errors.append("consumer command must be a non-empty argument array")
    elif not (
        Path(command[0]).name == "ctest"
        and "--test-dir" in command
        and "--output-on-failure" in command
        and "--no-tests=error" in command
    ):
        errors.append("consumer command must run CTest with no-tests treated as error")
    errors.extend(artifact_errors(consumer.get("log"), artifact_root, "consumer log"))
    errors.extend(ctest_evidence_errors(consumer, artifact_root))
    errors.extend(discovery_errors(consumer, artifact_root))
    counts = consumer.get("tests", {})
    if not isinstance(counts, dict) or not all(type(counts.get(key)) is int for key in ("total", "passed", "failed", "skipped")) or counts["total"] <= 0 or counts["passed"] != counts["total"] or counts["failed"] != 0 or counts["skipped"] != 0:
        errors.append("package consumer requires nonzero tests with no failures or skips")
    return errors


def compare_contract_snapshots(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    consumer: Any,
    artifact_root: Path,
    namespace_probe: Any = None,
    approved_additions: Any = None,
) -> Dict[str, Any]:
    """Compare package contracts and require a content-addressed consumer run."""

    blockers = _snapshot_errors(before, "before")
    blockers.extend(_snapshot_errors(after, "after"))
    drift = _contract_drift(before, after)
    blockers.extend(f"install contract drift: {field}" for field in drift)
    blockers.extend(_consumer_errors(consumer, artifact_root))
    blockers.extend(namespace_probe_errors(namespace_probe, before, after, artifact_root))
    if approved_additions is not None:
        from .wrapper_contract import installed_addition_errors
        errors = installed_addition_errors(before, after, drift, approved_additions)
        blockers.extend(errors)
        if not errors:
            blockers = [reason for reason in blockers if not reason.startswith("install contract drift:")]
    blockers = stable_unique(blockers)
    return {
        "schema_version": 2,
        "kind": "waylib-install-contract-audit",
        "before_snapshot_sha256": before.get("snapshot_sha256"),
        "after_snapshot_sha256": after.get("snapshot_sha256"),
        "drift": drift,
        "consumer": consumer,
        "namespace_probe": namespace_probe,
        "approved_additions": approved_additions,
        "blocked_reasons": blockers,
        "outcome": "blocked" if blockers else "pass",
    }
