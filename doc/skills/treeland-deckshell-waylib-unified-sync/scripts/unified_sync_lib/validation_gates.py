"""Validation command contracts and cross-artifact identity binding."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, List, Mapping, Sequence

from .artifacts import artifact_errors, read_verified_artifact
from .build_commands import full_build_command_errors
from .contracts import compare_contract_snapshots
from .ctest_results import ctest_evidence_errors, discovery_errors
from .validation_dependencies import dependency_binding_errors
from .native_validation import BASE_NATIVE_IDS, NATIVE_IDS, native_absence_errors, native_evidence_errors, native_path_errors
from .wrapper_build import wrapper_build_errors
from .git_ops import canonical_json_sha256, stable_unique
from .validation_paths import fresh_path_errors, path_binding_errors


REQUIRED_VALIDATIONS = {
    "deckshell-configure",
    "deckshell-build",
    "deckshell-compositor-ctest",
    "waylib-base-configure",
    "waylib-base-build",
    "waylib-base-install",
    "waylib-base-ctest",
    "waylib-candidate-configure",
    "waylib-candidate-build",
    "waylib-candidate-install",
    "waylib-ctest",
    "waylib-package-consumer-configure",
    "waylib-package-consumer-build",
    "waylib-package-consumer",
}
VALIDATION_COMMANDS = {
    "deckshell-configure": ("build", "configure"),
    "deckshell-build": ("build", "build"),
    "deckshell-compositor-ctest": ("test", "ctest"),
    "deckshell-top-level-ctest": ("test", "ctest"),
    "waylib-base-configure": ("build", "configure"),
    "waylib-base-build": ("build", "build"),
    "waylib-base-install": ("build", "install"),
    "waylib-base-ctest": ("test", "ctest"),
    "waylib-candidate-configure": ("build", "configure"),
    "waylib-candidate-build": ("build", "build"),
    "waylib-candidate-install": ("build", "install"),
    "waylib-ctest": ("test", "ctest"),
    "waylib-package-consumer-configure": ("build", "configure"),
    "waylib-package-consumer-build": ("build", "build"),
    "waylib-package-consumer": ("consumer", "consumer-ctest"),
}


def _test_count_errors(entry: Mapping[str, Any]) -> List[str]:
    outcome = entry.get("outcome")
    if entry.get("category") not in {"test", "consumer"}:
        return []
    counts = entry.get("tests")
    if not isinstance(counts, dict):
        return [f"test validation lacks counts: {entry.get('id')}"]
    values = [counts.get(name) for name in ("total", "passed", "failed", "skipped")]
    if not all(type(value) is int and value >= 0 for value in values):
        return [f"test validation has invalid counts: {entry.get('id')}"]
    total, passed, failed, skipped = values
    if outcome == "pass" and (total == 0 or passed != total or failed or skipped):
        return [f"passing test validation has non-passing counts: {entry.get('id')}"]
    if outcome == "no-tests" and total != 0:
        return [f"no-tests validation must report total=0: {entry.get('id')}"]
    return []


def _has_option(command: Sequence[str], option: str) -> bool:
    return any(value == option or value.startswith(f"{option}=") for value in command)


def _command_contract_errors(entry: Mapping[str, Any]) -> List[str]:
    validation_id = entry.get("id")
    expected = VALIDATION_COMMANDS.get(validation_id)
    if expected is None:
        return []
    category, shape = expected
    command = entry.get("command")
    if not isinstance(command, list) or not command:
        return []
    executable = Path(command[0]).name
    valid = entry.get("category") == category
    if shape == "configure":
        valid = valid and executable == "cmake" and _has_option(command, "-S") and _has_option(command, "-B")
    elif shape == "build":
        if valid:
            return full_build_command_errors(validation_id, command)
    elif shape == "install":
        valid = valid and executable == "cmake" and _has_option(command, "--install") and _has_option(command, "--prefix")
    else:
        valid = valid and executable == "ctest" and _has_option(command, "--test-dir") and "--output-on-failure" in command
        if shape == "consumer-ctest":
            valid = valid and "--no-tests=error" in command
    return [] if valid else [f"validation command contract mismatch: {validation_id}"]


def _validation_entry_errors(
    entry: Mapping[str, Any], artifact_root: Path, manifest: Mapping[str, Any]
) -> List[str]:
    if entry.get("outcome") == "not-applicable":
        return native_absence_errors(entry, artifact_root, manifest)
    validation_id = entry.get("id")
    errors: List[str] = []
    command = entry.get("command")
    if not isinstance(validation_id, str) or not validation_id:
        errors.append("validation id must be a non-empty string")
    if not isinstance(command, list) or not command or not all(isinstance(arg, str) for arg in command):
        errors.append(f"validation command must be an argument array: {validation_id}")
    if not isinstance(entry.get("cwd"), str) or not entry.get("cwd"):
        errors.append(f"validation cwd must be non-empty: {validation_id}")
    if entry.get("outcome") in {"pass", "no-tests"} and entry.get("exit_code") != 0:
        errors.append(f"successful validation has nonzero exit code: {validation_id}")
    if entry.get("outcome") not in {"pass", "no-tests"}:
        errors.append(f"validation did not pass: {validation_id}={entry.get('outcome')}")
    errors.extend(_test_count_errors(entry))
    errors.extend(_command_contract_errors(entry))
    errors.extend(fresh_path_errors(entry))
    errors.extend(artifact_errors(entry.get("log"), artifact_root, f"validation {validation_id} log"))
    if validation_id in {"wlroots-base-test", "wlroots-candidate-test"}:
        errors.extend(native_evidence_errors(entry, artifact_root))
    if isinstance(command, list) and command and Path(command[0]).name == "ctest":
        errors.extend(ctest_evidence_errors(entry, artifact_root))
        errors.extend(discovery_errors(entry, artifact_root))
    return errors


def validation_errors(
    validations: Mapping[str, Any],
    artifact_root: Path,
    manifest: Mapping[str, Any],
    gates: Mapping[str, Any],
) -> List[str]:
    """Validate the required command results and their shared build paths."""

    errors: List[str] = []
    if validations.get("schema_version") != 2 or validations.get("kind") != "treeland-unified-command-validations":
        errors.append("validations schema or kind is invalid")
    raw_entries = validations.get("entries")
    if not isinstance(raw_entries, list):
        return errors + ["validations entries must be an array"]
    ids = [entry.get("id") for entry in raw_entries if isinstance(entry, dict)]
    if manifest.get("identity", {}).get("wlroots") is not None:
        errors.extend(f"required validation is missing: {item}" for item in sorted(NATIVE_IDS - set(ids)))
    errors.extend(f"duplicate validation id: {item}" for item in stable_unique([item for item in ids if item and ids.count(item) > 1]))
    errors.extend(f"required validation is missing: {item}" for item in sorted(REQUIRED_VALIDATIONS - set(ids)))
    for entry in raw_entries:
        errors.extend(_validation_entry_errors(entry, artifact_root, manifest) if isinstance(entry, dict) else ["validation entry must be an object"])
    entries = {entry["id"]: entry for entry in raw_entries if isinstance(entry, dict) and isinstance(entry.get("id"), str)}
    for entry in entries.values():
        if manifest.get("identity", {}).get("wlroots") is not None or "manifest_sha256" in entry:
            errors.extend(dependency_binding_errors(entry, manifest))
    for required in REQUIRED_VALIDATIONS:
        if required in entries and entries[required].get("outcome") != "pass":
            errors.append(f"required validation must pass: {required}")
    if manifest.get("identity", {}).get("wlroots") is not None:
        errors.extend(native_path_errors(entries, manifest))
        build_ids = {"deckshell-build", "waylib-candidate-build"}
        if manifest["identity"]["wlroots"]["registered_at_base"]:
            build_ids.add("waylib-base-build")
        for name in build_ids & entries.keys():
            errors.extend(wrapper_build_errors(entries[name], manifest, artifact_root))
        for required in NATIVE_IDS:
            entry = entries.get(required, {})
            if required in BASE_NATIVE_IDS and entry.get("outcome") == "not-applicable":
                continue
            allowed = {"pass", "no-tests"} if required.endswith("-test") else {"pass"}
            if entry.get("outcome") not in allowed or entry.get("category") != ("test" if required.endswith("-test") else "build"):
                errors.append(f"required native validation did not pass: {required}")
    audit = gates.get("contract_audit")
    materialization = gates.get("child_materialization")
    if isinstance(audit, dict) and REQUIRED_VALIDATIONS.issubset(entries):
        errors.extend(path_binding_errors(entries, manifest, audit, materialization))
    return errors


def _snapshot_binding_errors(
    audit: Mapping[str, Any], artifact_root: Path
) -> List[str]:
    records = audit.get("snapshot_artifacts")
    install_roots = audit.get("install_roots")
    if not isinstance(records, dict) or not isinstance(install_roots, dict):
        return ["contract audit snapshot bindings are missing"]
    errors: List[str] = []
    snapshots = {}
    for label in ("before", "after"):
        record = records.get(label)
        record_errors = artifact_errors(
            record, artifact_root, f"contract audit {label} snapshot"
        )
        errors.extend(record_errors)
        if record_errors:
            continue
        try:
            _path, content = read_verified_artifact(
                record, artifact_root, f"contract audit {label} snapshot"
            )
            snapshot = json.loads(content.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as error:
            errors.append(f"contract audit {label} snapshot is invalid JSON: {error}")
            continue
        if not isinstance(snapshot, dict):
            errors.append(f"contract audit {label} snapshot root must be an object")
            continue
        digest = snapshot.get("snapshot_sha256")
        data = {
            key: value
            for key, value in snapshot.items()
            if key not in {"schema_version", "kind", "install_root", "snapshot_sha256"}
        }
        if digest != canonical_json_sha256(data):
            errors.append(f"contract audit {label} snapshot semantic digest mismatch")
        if digest != audit.get(f"{label}_snapshot_sha256"):
            errors.append(f"contract audit {label} snapshot identity mismatch")
        if snapshot.get("install_root") != install_roots.get(label):
            errors.append(f"contract audit {label} install root mismatch")
        snapshots[label] = snapshot
    if len(snapshots) == 2:
        expected = compare_contract_snapshots(
            snapshots["before"], snapshots["after"], audit.get("consumer"), artifact_root,
            audit.get("namespace_probe"), audit.get("approved_additions"),
        )
        errors.extend(expected["blocked_reasons"])
        if audit.get("drift") != expected["drift"]:
            errors.append("contract drift differs from the recorded snapshots")
    return errors


def contract_binding_errors(
    gates: Mapping[str, Any],
    validations: Mapping[str, Any],
    manifest: Mapping[str, Any],
    artifact_root: Path,
) -> List[str]:
    """Validate that contract audit evidence belongs to the current run."""

    audit = gates.get("contract_audit")
    raw_entries = validations.get("entries")
    if not isinstance(audit, dict) or not isinstance(raw_entries, list):
        return []
    entries = [entry for entry in raw_entries if isinstance(entry, dict)]
    matches = [entry for entry in entries if entry.get("id") == "waylib-package-consumer"]
    errors: List[str] = []
    if len(matches) == 1:
        expected = {"schema_version": 2, "kind": "waylib-package-consumer-result", **matches[0]}
        if audit.get("consumer") != expected:
            errors.append("contract audit consumer evidence differs from current validation attempt")
    identity = manifest.get("identity")
    identity = identity if isinstance(identity, dict) else {}
    source_commits = audit.get("source_commits")
    if not isinstance(source_commits, dict) or source_commits != {"before": identity.get("child_base"), "after": manifest.get("final_child_head")}:
        errors.append("contract audit source commits differ from the child mapping")
    source_roots = audit.get("source_roots")
    if not isinstance(source_roots, dict) or source_roots.get("after") != identity.get("child_worktree"):
        errors.append("contract audit candidate source root differs from the child worktree")
    errors.extend(_snapshot_binding_errors(audit, artifact_root))
    return errors
