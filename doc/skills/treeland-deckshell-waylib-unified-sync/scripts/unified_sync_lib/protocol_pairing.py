"""Pairing review and real-validation requirements for final report acceptance."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from .artifacts import artifact_errors
from .ctest_results import ctest_evidence_errors, discovery_errors
from .git_ops import canonical_json_sha256, run_git, stable_unique
from .protocol_sources import inspect_pairing, read_pair, safe_path
from .protocol_update import companion_lane_errors
from .validation_dependencies import dependency_binding_errors


PAIRING_KIND = "treeland-unified-protocol-pairing"


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def _client_paths(repo, commit, names):
    args = ["grep", "-l", "-F"]
    for name in sorted(names):
        args.extend(["-e", name])
    # git grep returns 1 when no client references exist; other failures remain errors.
    import subprocess
    result = subprocess.run(["git", "-C", str(repo), *args, commit, "--", "*.cpp", "*.h", "*.qml"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode not in {0, 1}:
        raise ValueError(result.stderr.decode("utf-8", errors="replace"))
    return {line.split(":", 1)[1] for line in result.stdout.decode("utf-8").splitlines()}


def affected_clients(manifest, inspection) -> list[dict]:
    """Find tracked references in both baseline and candidate, including old interface names."""

    names = set()
    for label in ("contract_before", "contract_after"):
        for node in inspection["protocol"][label]["wire"]["children"]:
            if node["tag"] == "interface":
                names.add(node["attributes"]["name"])
    result = []
    identity = manifest["identity"]
    for lane in ("child", "parent"):
        repo = Path(identity[f"{lane}_worktree"])
        paths = set()
        for commit in (identity[f"{lane}_base"], manifest[f"final_{lane}_head"]):
            paths.update(_client_paths(repo, commit, names))
        if lane == "child":
            paths.difference_update(inspection["implementation"]["paths"])
        result.extend({"lane": lane, "path": path} for path in sorted(paths))
    return result


def _client_review_errors(review, clients, manifest):
    rows = review.get("clients")
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        return ["client review must enumerate affected tracked clients"]
    expected = {(row["lane"], row["path"]) for row in clients}
    actual = [(row.get("lane"), row.get("path")) for row in rows]
    errors = []
    if set(actual) != expected or len(actual) != len(set(actual)):
        errors.append("client review does not cover exactly the discovered baseline/candidate clients")
    for row in rows:
        if row.get("disposition") not in {"updated", "unchanged"} or not _nonempty(row.get("reason")):
            errors.append(f"client needs an explicit update/unchanged reason: {row.get('path')}")
        if row.get("disposition") != "updated" or (row.get("lane"), row.get("path")) not in expected:
            continue
        lane = row["lane"]
        repo = Path(manifest["identity"][f"{lane}_worktree"])
        diff = str(run_git(repo, "diff", "--name-only", manifest["identity"][f"{lane}_base"],
                           manifest[f"final_{lane}_head"], "--", row["path"]))
        if not diff.strip():
            errors.append(f"client marked updated but unchanged in Git: {row['path']}")
    return errors


def _review_errors(review, inspection, clients, manifest):
    if not isinstance(review, dict):
        return ["protocol pairing review is missing"]
    errors = []
    implementation = review.get("implementation", {})
    if (not isinstance(implementation, dict)
            or implementation.get("disposition") not in {"updated", "unchanged"}
            or not _nonempty(implementation.get("reason"))):
        errors.append("implementation needs an explicit pairing disposition and reason")
    for name in ("wire_review", "behavior_review", "client_upgrade"):
        if not _nonempty(review.get(name)):
            errors.append(f"protocol review is missing: {name}")
    if review.get("compatibility") != "direct-switch":
        errors.append("protocol upgrades must directly switch; no old-protocol fallback is accepted")
    if not isinstance(review.get("breaking"), bool):
        errors.append("protocol review must explicitly assess breaking changes")
    if inspection["protocol"]["wire_changed"] and review.get("breaking") is not True:
        errors.append("wire changes require an explicit breaking-change/client-upgrade review")
    errors.extend(_client_review_errors(review, clients, manifest))
    return errors


def _validation_errors(review, validations, manifest, root):
    selected = review.get("validations", {})
    if not isinstance(selected, dict) or set(selected) != {"build", "consumer", "interaction"}:
        return ["pairing requires build, consumer and real interaction validation ids"]
    entries = {row.get("id"): row for row in validations.get("entries", []) if isinstance(row, dict)}
    errors = []
    for role, validation_id in selected.items():
        row = entries.get(validation_id)
        if not isinstance(row, dict) or row.get("outcome") != "pass" or row.get("exit_code") != 0:
            errors.append(f"necessary {role} validation did not pass: {validation_id}")
            continue
        errors.extend(artifact_errors(row.get("log"), root, f"protocol {role} log"))
        errors.extend(dependency_binding_errors(row, manifest))
        command = row.get("command", [])
        if role == "build":
            if validation_id != "waylib-candidate-build":
                errors.append("pairing must use the existing complete Waylib candidate build")
        else:
            if not command or Path(command[0]).name != "ctest" or "--no-tests=error" not in command:
                errors.append(f"protocol {role} needs a real nonzero CTest run")
            errors.extend(ctest_evidence_errors(row, root))
            errors.extend(discovery_errors(row, root))
    return errors


def _expectation_errors(review, inspection, validations):
    expectations = review.get("expectations")
    if not isinstance(expectations, list) or not expectations:
        return ["record independent upstream-based interaction assertions, not just registry/compilation"]
    selected = review.get("validations", {})
    interaction = next((row for row in validations.get("entries", [])
                        if isinstance(row, dict) and row.get("id") == selected.get("interaction")), {})
    passed = {row.get("name") for row in interaction.get("test_results", []) if row.get("status") == "passed"}
    protocol = inspection["protocol"]
    reference = f"{protocol['head']}:{protocol['head_path']}"
    errors = []
    real_interaction = False
    for row in expectations:
        if not isinstance(row, dict):
            errors.append("protocol expectation must be an object")
            continue
        if row.get("source") != reference or not _nonempty(row.get("assertion")):
            errors.append("protocol assertion must reference the exact selected upstream XML and describe its expectation")
        if row.get("case") not in passed:
            errors.append(f"protocol assertion was not exercised by the interaction run: {row.get('case')}")
        real_interaction |= row.get("kind") == "interaction" and "registry" not in str(row.get("case", "")).lower()
    if not real_interaction:
        errors.append("registry-only evidence cannot accept a protocol pairing")
    return errors


def _verify_candidate(result, inventory, manifest, review, validations, root):
    from .local_fixes import local_fix_errors, preceding_head
    identity = manifest["identity"]
    update = manifest.get("protocol_update")
    if not isinstance(update, dict):
        raise ValueError("protocol companion inspection/update is missing from the replay")
    inspection = update["inspection"]
    result["inspection"] = inspection
    result["last_accepted_pair"] = inspection.get("last_accepted_pair")
    result["candidate_pair"] = inspection.get("proposed_pair")
    frozen = identity.get("protocol_update", {})
    if frozen.get("inspection") != inspection:
        raise ValueError("protocol inspection differs from the frozen replay input")
    protocol, impl = inspection["protocol"], inspection["implementation"]
    result["target_ranges"] = {"implementation": {"base": impl["base"], "head": impl["head"]},
                               "protocol": {"base": protocol["base"], "head": protocol["head"]}}
    selection = {"repo": protocol["repo"], "base": protocol["base"], "head": protocol["head"],
                 "path": protocol["head_path"], "implementation_paths": impl["paths"]}
    fresh = inspect_pairing(inventory, Path(identity["source_repo"]), Path(identity["child_worktree"]),
                            identity["child_base"], selection)
    for key in ("implementation", "protocol", "last_accepted_pair", "proposed_pair"):
        if fresh.get(key) != inspection.get(key) or fresh["outcome"] != "pass":
            raise ValueError("source inspection cannot be reproduced: " + "; ".join(fresh["blocked_reasons"] or [key]))
    result["failure_stage"] = "candidate-update"
    errors = local_fix_errors(manifest, root)
    for lane in ("child", "parent"):
        if update.get(lane, {}).get("head") != preceding_head(manifest, lane):
            errors.append(f"protocol companion differs from final {lane} candidate")
        errors.extend(companion_lane_errors(Path(identity[f"{lane}_worktree"]), update, lane, root))
    if errors:
        raise ValueError("; ".join(errors))
    clients = affected_clients(manifest, inspection)
    result["affected_clients"] = clients
    result["failure_stage"] = "review-and-validation"
    errors.extend(_review_errors(review, inspection, clients, manifest))
    if isinstance(review, dict):
        errors.extend(_validation_errors(review, validations, manifest, root))
        errors.extend(_expectation_errors(review, inspection, validations))
    return errors


def verify_pairing(inventory: Mapping, manifest: Mapping, review: Mapping,
                   validations: Mapping, artifact_root: Path) -> dict:
    """Produce the mandatory pairing result, retaining prior pair and failures on rejection."""

    result = {"schema_version": 2, "kind": PAIRING_KIND, "outcome": "blocked", "status": "尚未适配",
              "inventory_sha256": canonical_json_sha256(inventory),
              "manifest_sha256": canonical_json_sha256(manifest),
              "final_parent_head": manifest.get("final_parent_head"),
              "final_child_head": manifest.get("final_child_head"),
              "target_ranges": {"implementation": inventory.get("range"), "protocol": None},
              "last_accepted_pair": None, "candidate_pair": None,
              "failure_stage": "source-inspection", "review": review,
              "validation_results": [{"id": row.get("id"), "outcome": row.get("outcome")}
                                     for row in validations.get("entries", []) if isinstance(row, dict)]}
    try:
        identity = manifest["identity"]
        result["last_accepted_pair"] = read_pair(Path(identity["child_worktree"]), identity["child_base"])
        errors = _verify_candidate(result, inventory, manifest, review, validations, artifact_root)
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as error:
        errors = [str(error)]
    result["blocked_reasons"] = [f"尚未适配：{error}" for error in stable_unique(errors)]
    result["unfinished"] = list(result["blocked_reasons"])
    if not errors:
        result.update(outcome="pass", status="paired", failure_stage=None)
    return result


def pairing_report_errors(pairing, inventory, manifest, validations, artifact_root) -> list[str]:
    """Check acceptance inputs without accepting advisory or a missing pairing conclusion."""

    if not isinstance(pairing, dict):
        return ["尚未适配：缺少 protocol_pairing 配套结论"]
    errors = []
    if pairing.get("outcome") != "pass" or pairing.get("status") != "paired":
        errors.extend(pairing.get("blocked_reasons") or ["尚未适配：协议配套检查未通过"])
    if pairing.get("kind") != PAIRING_KIND or pairing.get("schema_version") != 2:
        errors.append("尚未适配：invalid pairing result")
    for key in ("final_parent_head", "final_child_head"):
        if pairing.get(key) != manifest.get(key):
            errors.append(f"尚未适配：pairing {key} differs from manifest")
    for key, value in (("inventory_sha256", inventory), ("manifest_sha256", manifest)):
        if pairing.get(key) != canonical_json_sha256(value):
            errors.append(f"尚未适配：pairing {key} differs from current input")
    inspection = pairing.get("inspection")
    if not isinstance(inspection, dict) or inspection.get("outcome") != "pass":
        errors.append("尚未适配：both source inspections are required")
    elif pairing.get("target_ranges", {}).get("implementation") != {
            key: (inventory.get("range") or {}).get(key) for key in ("base", "head")}:
        errors.append("尚未适配：pairing does not cover the complete selected implementation range")
    update = manifest.get("protocol_update") or {}
    if update and inspection != update.get("inspection"):
        errors.append("尚未适配：pairing inspection differs from the replayed protocol update")
    if isinstance(inspection, dict):
        for name, source in (("last_accepted_pair", "last_accepted_pair"), ("candidate_pair", "proposed_pair")):
            if not pairing.get(name) or pairing.get(name) != inspection.get(source):
                errors.append(f"尚未适配：{name} differs from inspected source pair")
    if pairing.get("blocked_reasons") != [] or pairing.get("unfinished") != []:
        errors.append("尚未适配：pairing has unfinished work")
    actual = [{"id": row.get("id"), "outcome": row.get("outcome")}
              for row in validations.get("entries", []) if isinstance(row, dict)]
    if pairing.get("validation_results") != actual:
        errors.append("尚未适配：validation results changed after pairing review")
    if isinstance(inspection, dict) and isinstance(pairing.get("review"), dict):
        errors.extend(_review_errors(pairing["review"], inspection,
                                     pairing.get("affected_clients", []), manifest))
        errors.extend(_validation_errors(pairing["review"], validations, manifest, artifact_root))
        errors.extend(_expectation_errors(pairing["review"], inspection, validations))
    else:
        errors.append("尚未适配：完整配套审查缺失")
    return stable_unique(errors)
