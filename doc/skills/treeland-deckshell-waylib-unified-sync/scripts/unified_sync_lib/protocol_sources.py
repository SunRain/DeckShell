"""Remote-subsurface source ranges and the source-shipped provenance record."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
from typing import Any, Mapping
from xml.etree import ElementTree

from .git_ops import canonical_repo, parse_name_status_z, resolve_commit, run_git
from .patches import tree_entry


PROVENANCE_PATH = "waylib/protocols/remote-subsurface.json"
XML_PATH = "waylib/protocols/treeland-remote-subsurface-unstable-v1.xml"
PARENT_XML_PATH = "protocols/compositor/xml/treeland-remote-subsurface-unstable-v1.xml"


def safe_path(value: Any) -> bool:
    """Accept an explicit repository-relative file, never a pathspec or escape."""

    return (isinstance(value, str) and bool(value)
            and not PurePosixPath(value).is_absolute()
            and not any(part in {".", "..", ".git"} for part in value.split("/"))
            and not any(c in value for c in "*?[]:\\")
            and not any(ord(c) < 32 or ord(c) == 127 for c in value))


def source_blob(repo: Path, commit: str, path: str) -> bytes:
    """Read an ordinary source file without using a working-tree fallback."""

    if not safe_path(path):
        raise ValueError(f"unsafe protocol source path: {path!r}")
    entry = tree_entry(repo, commit, path)
    if not entry or entry["type"] != "blob" or entry["mode"] not in {"100644", "100755"}:
        raise ValueError(f"missing ordinary source file: {commit}:{path}")
    return bytes(run_git(repo, "show", f"{commit}:{path}", text=False))


def read_pair(repo: Path, commit: str) -> dict:
    """Read the last accepted implementation/XML pair from the child commit."""

    pair = json.loads(source_blob(repo, commit, PROVENANCE_PATH))
    if not isinstance(pair, dict):
        raise ValueError("protocol provenance must be an object")
    for lane in ("implementation", "protocol"):
        row = pair.get(lane)
        if not isinstance(row, dict) or not row.get("repository") or not row.get("commit"):
            raise ValueError(f"protocol provenance lacks {lane} repository/commit")
    paths = pair["implementation"].get("paths")
    if not isinstance(paths, list) or not paths or not all(safe_path(p) for p in paths):
        raise ValueError("protocol provenance implementation paths are invalid")
    if not safe_path(pair["protocol"].get("path")):
        raise ValueError("protocol provenance XML path is invalid")
    return pair


def _range(repo: Path, base: str, head: str) -> tuple[str, str, list[str]]:
    if str(run_git(repo, "rev-parse", "--is-shallow-repository")).strip() != "false":
        raise ValueError("history is shallow; prepare complete selected source history")
    base, head = resolve_commit(repo, base), resolve_commit(repo, head)
    run_git(repo, "merge-base", "--is-ancestor", base, head)
    # Git must read the complete selected history; a partial clone must not fetch.
    objects = str(run_git(repo, "rev-list", "--objects", "--missing=print", f"{base}..{head}",
                          env={"GIT_NO_LAZY_FETCH": "1"}))
    if any(line.startswith("?") for line in objects.splitlines()):
        raise ValueError("selected source history has missing objects")
    commits = str(run_git(repo, "rev-list", "--reverse", "--topo-order", f"{base}..{head}")).split()
    return base, head, commits


def inspect_history(repo: Path, base: str, head: str, paths: list[str]) -> dict:
    """Inspect every selected commit, retaining moves, removals and reverted changes."""

    repo = canonical_repo(repo)
    if not paths or not all(safe_path(path) for path in paths):
        raise ValueError("source inspection needs explicit safe paths")
    base, head, commits = _range(repo, base, head)
    rows, tracked = [], set(paths)
    for commit in commits:
        parents = str(run_git(repo, "rev-list", "--parents", "-n", "1", commit)).split()[1:]
        for parent in parents:
            raw = run_git(repo, "diff", "--name-status", "--find-renames", "-z", parent, commit, text=False)
            rows.append((commit, parent, parse_name_status_z(bytes(raw))))
    # Resolve rename chains across the complete range, including merge parents.
    while True:
        before = set(tracked)
        for _, _, changes in rows:
            for change in changes:
                sides = {p for p in (change.old_path, change.new_path) if p}
                if change.status.startswith("R") and tracked & sides:
                    tracked.update(sides)
        if tracked == before:
            break
    changes = []
    for commit, parent, candidates in rows:
        selected = [c for c in candidates if tracked & {c.old_path, c.new_path}]
        if selected:
            touched = sorted({p for c in selected for p in (c.old_path, c.new_path) if p})
            diff = str(run_git(repo, "diff", "--no-ext-diff", "--no-textconv", parent, commit, "--", *touched))
            changes.append({"commit": commit, "parent": parent,
                            "paths": [vars(c) for c in selected], "diff": diff})
    present = [p for p in sorted(tracked) if tree_entry(repo, head, p)]
    for path in present:
        source_blob(repo, head, path)
    return {"repo": str(repo), "base": base, "head": head,
            "checked_commits": commits, "paths": sorted(tracked),
            "head_paths": present, "changes": changes}


def xml_contract(content: bytes) -> dict:
    """Describe wire order/types/enums separately from prose, without freezing a hash."""

    root = ElementTree.fromstring(content)
    if root.tag != "protocol" or not root.findall("interface"):
        raise ValueError("remote-subsurface XML has no protocol interfaces")

    def wire(node):
        return {"tag": node.tag, "attributes": dict(node.attrib),
                "children": [wire(c) for c in node if c.tag not in {"description", "copyright"}]}

    descriptions = [{"summary": node.get("summary"), "text": " ".join("".join(node.itertext()).split())}
                    for node in root.iter("description")]
    return {"wire": wire(root), "descriptions": descriptions}


def _inspect_sources(result, inventory, source_repo, child_repo, child_base, selection):
    pair = read_pair(child_repo, child_base)
    result["last_accepted_pair"] = pair
    impl_range = inventory["range"]
    if pair["implementation"]["commit"] != resolve_commit(source_repo, impl_range["base"]):
        raise ValueError("implementation range must start at the last accepted pair")
    extra = selection.get("implementation_paths", [])
    if not isinstance(extra, list) or not all(safe_path(p) for p in extra):
        raise ValueError("additional implementation paths must be explicit files")
    result["implementation"] = inspect_history(source_repo, impl_range["base"], impl_range["head"],
                                                 pair["implementation"]["paths"] + extra)
    protocol_repo = canonical_repo(Path(selection["repo"]))
    if resolve_commit(protocol_repo, selection["base"]) != pair["protocol"]["commit"]:
        raise ValueError("protocol range must start at the last accepted pair")
    paths = [pair["protocol"]["path"]]
    if selection.get("path"):
        paths.append(selection["path"])
    history = inspect_history(protocol_repo, selection["base"], selection["head"], paths)
    result["protocol"] = history
    head_path = selection.get("path")
    if not head_path:
        if len(history["head_paths"]) != 1:
            raise ValueError("XML removed or ambiguous after move; select the new path explicitly")
        head_path = history["head_paths"][0]
    before = source_blob(protocol_repo, history["base"], pair["protocol"]["path"])
    after = source_blob(protocol_repo, history["head"], head_path)
    old, new = xml_contract(before), xml_contract(after)
    history.update({"base_path": pair["protocol"]["path"], "head_path": head_path,
                    "wire_changed": old["wire"] != new["wire"],
                    "descriptions_changed": old["descriptions"] != new["descriptions"],
                    "contract_before": old, "contract_after": new})
    impl = result["implementation"]
    if not impl["head_paths"]:
        raise ValueError("selected implementation was removed; adaptation is required")
    result["proposed_pair"] = {
        "implementation": {**pair["implementation"], "commit": impl["head"], "paths": impl["head_paths"]},
        "protocol": {**pair["protocol"], "commit": history["head"], "path": head_path},
        "notes": "Paired through the unified sync workflow; see its protocol review and validation records.",
    }


def inspect_pairing(inventory: Mapping, source_repo: Path, child_repo: Path,
                    child_base: str, selection: Mapping) -> dict:
    """Inspect both explicit sources; an inspection PASS is not pairing acceptance."""

    result = {"schema_version": 2, "kind": "treeland-unified-protocol-inspection",
              "outcome": "blocked", "status": "尚未适配", "last_accepted_pair": None,
              "requested_ranges": {"implementation": inventory.get("range"), "protocol": dict(selection)},
              "blocked_reasons": [], "unfinished": [], "validation_results": [], "failure_stage": None}
    try:
        _inspect_sources(result, inventory, source_repo, child_repo, child_base, selection)
    except (OSError, ValueError, RuntimeError, KeyError, ElementTree.ParseError) as error:
        result["failure_stage"] = "source-inspection"
        result["blocked_reasons"] = [f"尚未适配：{error}"]
        result["unfinished"] = list(result["blocked_reasons"])
    else:
        result.update(outcome="pass", status="inspected-not-accepted")
    return result
