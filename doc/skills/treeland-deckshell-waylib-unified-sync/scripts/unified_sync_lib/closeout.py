"""Child-first local branch closeout with expected-old CAS."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional

from .git_ops import (
    atomic_write_json,
    canonical_json_sha256,
    canonical_repo,
    common_git_dir,
    git_succeeds,
    read_json,
    resolve_commit,
    run_git,
    sha256_bytes,
    sha256_file,
)
from .patches import tree_entry
from .replay_types import GITLINK_PATH
from .schema import SHA256, is_full_sha
from .wlroots import registration
from .protocol_sources import read_pair


REPORT_GATES = {
    "deckshell_verify",
    "waylib_verify",
    "gitlink_verify",
    "protocol_tracking",
    "protocol_pairing",
    "contract_audit",
    "child_materialization",
    "wlroots_verify",
    "nested_gitlink_verify",
}


class CloseoutBlocked(RuntimeError):
    """Raised when a ref closeout precondition or CAS operation fails."""


def _digest(payload: Mapping[str, Any]) -> str:
    content = json.dumps(
        payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(content)


def _checked_out_refs(repo: Path) -> List[str]:
    output = str(run_git(repo, "worktree", "list", "--porcelain"))
    return [line[7:] for line in output.splitlines() if line.startswith("branch ")]


def _ref_value(repo: Path, ref: str) -> str:
    return str(run_git(repo, "show-ref", "--verify", "--hash", ref)).strip()


def _identity(
    parent_repo: Path,
    child_repo: Path,
    parent_ref: str,
    child_ref: str,
    parent_old: str,
    child_old: str,
    parent_new: str,
    child_new: str,
    report: Mapping[str, Any],
) -> Dict[str, Any]:
    return {
        "parent_repo": str(parent_repo),
        "child_repo": str(child_repo),
        "parent_ref": parent_ref,
        "child_ref": child_ref,
        "parent_expected_old": parent_old,
        "child_expected_old": child_old,
        "parent_new": parent_new,
        "child_new": child_new,
        "report_sha256": _digest(report),
    }


def _report_artifact_errors(record: Any) -> List[str]:
    if not isinstance(record, dict):
        return ["report artifact record is missing"]
    path_value = record.get("path")
    if not isinstance(path_value, str) or not path_value:
        return ["report artifact path is invalid"]
    path = Path(path_value)
    if not path.is_absolute() or not path.is_file():
        return ["report artifact path must be an existing absolute file"]
    errors: List[str] = []
    if record.get("size") != path.stat().st_size:
        errors.append("report artifact size mismatch")
    if record.get("sha256") != sha256_file(path):
        errors.append("report artifact sha256 mismatch")
    return errors


def _report_errors(report: Mapping[str, Any]) -> List[str]:
    errors: List[str] = []
    if report.get("schema_version") != 2:
        errors.append("schema_version must be 2")
    if report.get("kind") != "treeland-unified-sync-report":
        errors.append("kind is invalid")
    if report.get("outcome") != "pass":
        errors.append("outcome is not pass")
    scope = report.get("build_scope")
    if not isinstance(scope, dict) or scope.get("kind") != "range-head-only" or not is_full_sha(scope.get("source_head")):
        errors.append("build_scope must bind the validated range head; regenerate the report")
    for name in ("final_parent_head", "final_child_head"):
        if not is_full_sha(report.get(name)):
            errors.append(f"{name} must be a full SHA")
    for name in ("inventory_sha256", "manifest_sha256", "validations_sha256"):
        value = report.get(name)
        if not isinstance(value, str) or not SHA256.fullmatch(value):
            errors.append(f"{name} must be a SHA-256 digest")
    gate_digests = report.get("gate_sha256")
    if not isinstance(gate_digests, dict) or set(gate_digests) != REPORT_GATES:
        errors.append("gate_sha256 must cover every required report gate")
    elif not all(isinstance(value, str) and SHA256.fullmatch(value) for value in gate_digests.values()):
        errors.append("gate_sha256 contains an invalid digest")
    if report.get("blocked_reasons") != []:
        errors.append("blocked_reasons must be an empty array")
    pairing = report.get("protocol_pairing")
    if (not isinstance(pairing, dict) or pairing.get("outcome") != "pass"
            or pairing.get("status") != "paired" or pairing.get("blocked_reasons") != []
            or pairing.get("unfinished") != [] or not pairing.get("last_accepted_pair")
            or not pairing.get("candidate_pair")):
        errors.append("尚未适配：closeout requires the complete protocol pairing conclusion")
    elif (not isinstance(gate_digests, dict)
          or gate_digests.get("protocol_pairing") != canonical_json_sha256(pairing)):
        errors.append("尚未适配：protocol pairing differs from the report gate")
    errors.extend(_report_artifact_errors(report.get("report")))
    return errors


def _gitlink_errors(
    parent_repo: Path,
    parent_old: str,
    child_old: str,
    parent_new: str,
    child_new: str,
) -> List[str]:
    errors: List[str] = []
    for label, parent_commit, child_commit in (
        ("baseline", parent_old, child_old),
        ("candidate", parent_new, child_new),
    ):
        entry = tree_entry(parent_repo, parent_commit, GITLINK_PATH)
        if (
            not entry
            or entry.get("mode") != "160000"
            or entry.get("type") != "commit"
            or entry.get("sha") != child_commit
        ):
            errors.append(f"{label} gitlink does not match the child commit")
    return errors


def _validate_static(
    parent_repo: Path,
    child_repo: Path,
    parent_ref: str,
    child_ref: str,
    parent_old: str,
    child_old: str,
    parent_new: str,
    child_new: str,
    report: Mapping[str, Any],
    resume: bool,
) -> None:
    report_errors = _report_errors(report)
    if report_errors:
        raise CloseoutBlocked(
            "closeout requires a complete passing sync report: "
            + "; ".join(report_errors)
        )
    if report.get("final_parent_head") != parent_new or report.get("final_child_head") != child_new:
        raise CloseoutBlocked("sync report final heads differ from requested closeout heads")
    for repo, ref in ((parent_repo, parent_ref), (child_repo, child_ref)):
        if not ref.startswith("refs/heads/") or not git_succeeds(repo, "check-ref-format", ref):
            raise CloseoutBlocked(f"closeout only accepts full local branch refs: {ref}")
    if parent_ref in _checked_out_refs(parent_repo) or child_ref in _checked_out_refs(child_repo):
        raise CloseoutBlocked("target closeout refs must not be checked out in any worktree")
    if not git_succeeds(parent_repo, "merge-base", "--is-ancestor", parent_old, parent_new):
        raise CloseoutBlocked("parent candidate is not a fast-forward from expected-old")
    if not git_succeeds(child_repo, "merge-base", "--is-ancestor", child_old, child_new):
        raise CloseoutBlocked("child candidate is not a fast-forward from expected-old")
    gitlink_errors = _gitlink_errors(
        parent_repo, parent_old, child_old, parent_new, child_new
    )
    if gitlink_errors:
        raise CloseoutBlocked("; ".join(gitlink_errors))
    parent_actual = _ref_value(parent_repo, parent_ref)
    child_actual = _ref_value(child_repo, child_ref)
    allowed_parent = {parent_old, parent_new} if resume else {parent_old}
    allowed_child = {child_old, child_new} if resume else {child_old}
    if parent_actual not in allowed_parent:
        raise CloseoutBlocked("parent target ref moved outside the closeout identity")
    if child_actual not in allowed_child:
        raise CloseoutBlocked("child target ref moved outside the closeout identity")
    if parent_actual == parent_new and child_actual != child_new:
        raise CloseoutBlocked("parent ref cannot precede child ref during closeout")


def _new_journal(identity: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": 2,
        "kind": "treeland-unified-closeout-journal",
        "identity": dict(identity),
        "identity_sha256": _digest(identity),
        "outcome": "running",
        "wlroots_updated": False if identity.get("wlroots_repo") else None,
        "child_updated": False,
        "parent_updated": False,
        "next_sequence": 1,
        "events": [],
        "blocked": None,
    }


def _event(journal: Dict[str, Any], stage: str, status: str) -> None:
    journal["events"].append(
        {"sequence": journal["next_sequence"], "stage": stage, "status": status}
    )
    journal["next_sequence"] += 1


def _journal_shape_errors(journal: Mapping[str, Any]) -> List[str]:
    errors: List[str] = []
    if not isinstance(journal.get("child_updated"), bool) or not isinstance(
        journal.get("parent_updated"), bool
    ):
        errors.append("closeout journal checkpoint flags are invalid")
    elif journal.get("parent_updated") and not journal.get("child_updated"):
        errors.append("closeout journal records parent before child")
    if journal.get("identity", {}).get("wlroots_repo"):
        if type(journal.get("wlroots_updated")) is not bool:
            errors.append("closeout wlroots checkpoint flag is invalid")
        elif journal.get("child_updated") and not journal.get("wlroots_updated"):
            errors.append("closeout journal records child before wlroots")
    elif journal.get("wlroots_updated") is not None:
        errors.append("inactive wlroots must not have an update checkpoint")
    events = journal.get("events")
    next_sequence = journal.get("next_sequence")
    if not isinstance(events, list):
        errors.append("closeout journal events must be an array")
    if not isinstance(next_sequence, int) or next_sequence < 1:
        errors.append("closeout journal next_sequence is invalid")
    if isinstance(events, list) and isinstance(next_sequence, int):
        sequences = [item.get("sequence") for item in events if isinstance(item, dict)]
        if len(sequences) != len(events) or sequences != list(range(1, next_sequence)):
            errors.append("closeout journal event sequence is invalid")
    if journal.get("outcome") not in {"running", "blocked", "pass"}:
        errors.append("closeout journal outcome is invalid")
    return errors


def _open_journal(
    path: Path, identity: Mapping[str, Any], resume: bool
) -> Dict[str, Any]:
    if resume:
        if not path.is_file():
            raise CloseoutBlocked("closeout resume requested but journal is missing")
        journal = read_json(path)
        if journal.get("schema_version") != 2 or journal.get("kind") != "treeland-unified-closeout-journal":
            raise CloseoutBlocked("closeout journal schema or kind is invalid")
        if journal.get("identity") != dict(identity) or journal.get("identity_sha256") != _digest(identity):
            raise CloseoutBlocked("closeout journal identity mismatch")
        errors = _journal_shape_errors(journal)
        if errors:
            raise CloseoutBlocked("; ".join(errors))
        return journal
    if path.exists():
        raise CloseoutBlocked("closeout journal already exists; use explicit resume")
    journal = _new_journal(identity)
    atomic_write_json(path, journal)
    return journal


def _ref_rows(identity):
    for lane in ("wlroots", "child", "parent"):
        if identity.get(f"{lane}_repo"):
            yield lane, Path(identity[f"{lane}_repo"]), identity[f"{lane}_ref"], identity[f"{lane}_expected_old"], identity[f"{lane}_new"]


def _reconcile_journal(journal, journal_path):
    for lane, repo, ref, old, new in _ref_rows(journal["identity"]):
        actual = _ref_value(repo, ref)
        flag = f"{lane}_updated"
        if journal[flag] and actual != new:
            raise CloseoutBlocked(f"{lane} ref no longer matches its checkpoint")
        if not journal[flag] and actual == new:
            journal[flag] = True
            _event(journal, f"{lane}-ref-updated", "unchanged" if old == new else "recovered")
            atomic_write_json(journal_path, journal)


def _advance_refs(journal, journal_path, stage_hook):
    for lane, repo, ref, old, new in _ref_rows(journal["identity"]):
        if journal[f"{lane}_updated"]:
            continue
        if ref in _checked_out_refs(repo):
            raise CloseoutBlocked(f"{lane} target ref became checked out before CAS")
        run_git(repo, "update-ref", ref, new, old)
        if stage_hook:
            stage_hook(f"{lane}-ref-written")
        journal[f"{lane}_updated"] = True
        _event(journal, f"{lane}-ref-updated", "complete")
        atomic_write_json(journal_path, journal)


def _wlroots_closeout_identity(repo, ref, old, new, report, child_repo, child_old, child_new, resume):
    frozen = report.get("replay_identity", {}).get("wlroots")
    if frozen is None:
        if any((repo, ref, old, new)) or report.get("final_wlroots_head") is not None:
            raise CloseoutBlocked("wlroots closeout arguments disagree with inactive report")
        return {}
    if not all((repo, ref, old, new)) or not isinstance(frozen, dict):
        raise CloseoutBlocked("active wlroots closeout needs repo/ref/expected-old/new")
    repo = canonical_repo(repo)
    old, new = resolve_commit(repo, old), resolve_commit(repo, new)
    if (str(common_git_dir(repo)) != frozen.get("common_git_dir") or old != frozen.get("base")
            or ref != frozen.get("target_ref") or new != report.get("final_wlroots_head")):
        raise CloseoutBlocked("wlroots closeout identity differs from complete report")
    if not ref.startswith("refs/heads/") or not git_succeeds(repo, "check-ref-format", ref) or ref in _checked_out_refs(repo):
        raise CloseoutBlocked("wlroots target must be an unchecked-out full local branch ref")
    if not git_succeeds(repo, "merge-base", "--is-ancestor", old, new):
        raise CloseoutBlocked("wlroots candidate is not a fast-forward from expected-old")
    actual = _ref_value(repo, ref)
    if actual not in ({old, new} if resume else {old}):
        raise CloseoutBlocked("wlroots target ref moved outside the closeout identity")
    baseline = registration(child_repo, child_old, old, frozen["submodule_url"])
    if bool(baseline) != frozen.get("registered_at_base"):
        raise CloseoutBlocked("wlroots baseline registration mismatch")
    if registration(child_repo, child_new, new, frozen["submodule_url"]) is None:
        raise CloseoutBlocked("candidate child does not point to the wlroots candidate")
    return {"wlroots_repo": str(repo), "wlroots_ref": ref, "wlroots_expected_old": old, "wlroots_new": new}


def _validate_replay_identity(report, parent_repo, child_repo, parent_old, child_old):
    frozen = report.get("replay_identity")
    if not isinstance(frozen, dict) or frozen.get("parent_base") != parent_old or frozen.get("child_base") != child_old:
        raise CloseoutBlocked("report replay baselines differ from requested closeout")
    if frozen.get("parent_common_git_dir") != str(common_git_dir(parent_repo)) or frozen.get("child_common_git_dir") != str(common_git_dir(child_repo)):
        raise CloseoutBlocked("closeout repositories differ from frozen object stores")


def _validate_protocol_pair(report, child_repo, child_old, child_new):
    pairing = report["protocol_pairing"]
    try:
        if (read_pair(child_repo, child_old) != pairing["last_accepted_pair"]
                or read_pair(child_repo, child_new) != pairing["candidate_pair"]):
            raise ValueError("source-shipped pair differs from the accepted report")
    except (OSError, ValueError, RuntimeError) as error:
        raise CloseoutBlocked(f"尚未适配：{error}") from error


def closeout_refs(
    parent_repo: Path,
    child_repo: Path,
    parent_ref: str,
    child_ref: str,
    parent_expected_old: str,
    child_expected_old: str,
    parent_new: str,
    child_new: str,
    report: Mapping[str, Any],
    journal_path: Path,
    resume: bool = False,
    stage_hook: Optional[Callable[[str], None]] = None,
    *,
    wlroots_repo: Optional[Path] = None,
    wlroots_ref: Optional[str] = None,
    wlroots_expected_old: Optional[str] = None,
    wlroots_new: Optional[str] = None,
) -> Dict[str, Any]:
    """Advance local refs child-first with expected-old CAS and a resume journal."""

    parent_repo = canonical_repo(parent_repo)
    child_repo = canonical_repo(child_repo)
    parent_old = resolve_commit(parent_repo, parent_expected_old)
    child_old = resolve_commit(child_repo, child_expected_old)
    parent_new = resolve_commit(parent_repo, parent_new)
    child_new = resolve_commit(child_repo, child_new)
    _validate_static(
        parent_repo, child_repo, parent_ref, child_ref, parent_old,
        child_old, parent_new, child_new, report, resume,
    )
    identity = _identity(
        parent_repo, child_repo, parent_ref, child_ref, parent_old,
        child_old, parent_new, child_new, report,
    )
    _validate_replay_identity(report, parent_repo, child_repo, parent_old, child_old)
    _validate_protocol_pair(report, child_repo, child_old, child_new)
    identity.update(_wlroots_closeout_identity(wlroots_repo, wlroots_ref, wlroots_expected_old, wlroots_new,
                                               report, child_repo, child_old, child_new, resume))
    rows = list(_ref_rows(identity))
    for lower, higher in zip(rows, rows[1:]):
        if higher[3] != higher[4] and _ref_value(higher[1], higher[2]) == higher[4] and _ref_value(lower[1], lower[2]) != lower[4]:
            raise CloseoutBlocked("higher ref cannot precede its dependency during closeout")
    journal = _open_journal(journal_path, identity, resume)
    try:
        _reconcile_journal(journal, journal_path)
        _advance_refs(journal, journal_path, stage_hook)
        journal["outcome"] = "pass"
        journal["blocked"] = None
        atomic_write_json(journal_path, journal)
        return journal
    except Exception as error:
        journal["outcome"] = "blocked"
        journal["blocked"] = str(error)
        _event(journal, "closeout", "blocked")
        atomic_write_json(journal_path, journal)
        if isinstance(error, CloseoutBlocked):
            raise
        raise CloseoutBlocked(str(error)) from error
