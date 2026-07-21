"""End-state verification for one isolated aligned-history v2 preview."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from typing import Any

from .artifacts import canonical_bytes
from .bundle import bundle_files, bundle_sha256
from .context import InputPaths
from .dry_run import FORBIDDEN_FINAL_KEYS
from .freeze_inputs import BUNDLE_REPO_PREFIX, SHARED_ANCHOR
from .git_objects import git_object_id, parse_raw_commit
from .message import parse_message
from .product_oracle import (
    build_product_entries,
    compare_three_way_product_entries,
    path_is_excluded,
    project_master_product_entries,
    validate_master_manifest,
    validate_overlay_rules,
    validate_product_evidence,
)
from .preview_regeneration import (
    ADAPTATION_DOCS_PREFIX,
    AUDIT_PATH,
    GITATTRIBUTES,
    PLAN_PATH,
)
from .regeneration import finalize_plan_document, render_audit_document
from .repository import GitRepository
from .remediation import verify_remediation_sources
from .tree_manifest import (
    gitlink_object,
    tree_diff_paths,
    tree_entries,
)


def verify_final_tree(
    paths: InputPaths,
    repo: GitRepository,
    *,
    manifest: dict[str, Any],
    v1_tree: str,
    v2_tree: str,
    treeland_prefix: dict[str, Any],
    expected_gitlink: str,
    expected_tool_bundle_sha256: str,
) -> dict[str, Any]:
    """Verify product equivalence and every approved overlay in the final tree."""

    rules = _read_json(paths.product_overlay_rules)
    master = _read_json(paths.master_product_manifest)
    v1_evidence = _read_json(paths.v1_product_manifest)
    validate_overlay_rules(
        rules,
        expected_artifact_sha256=manifest["frozen_inputs"][
            "overlay_rules_sha256"
        ],
    )
    validate_master_manifest(
        master,
        rules,
        expected_artifact_sha256=manifest["frozen_inputs"][
            "master_product_manifest_sha256"
        ],
    )
    v1_product = build_product_entries(repo, v1_tree, rules)
    v2_product = build_product_entries(repo, v2_tree, rules)
    projected_master, rewrite_authority = project_master_product_entries(
        repo, master["entries"]
    )
    validate_product_evidence(
        v1_evidence,
        master["entries"],
        projected_master,
        rewrite_authority,
        expected_artifact_sha256=manifest["frozen_inputs"][
            "corrected_v1_product_manifest_sha256"
        ],
    )
    oracle = compare_three_way_product_entries(
        projected_master, v1_product, v2_product
    )
    changed_paths = tree_diff_paths(repo, v1_tree, v2_tree)
    unauthorized = [
        path for path in changed_paths if not path_is_excluded(path, rules)
    ]
    if unauthorized:
        raise ValueError(f"final tree has unauthorized differences: {unauthorized}")
    tool_summary = _verify_tool_bundle(
        paths, repo, v2_tree, expected_tool_bundle_sha256
    )
    document_summary = _verify_generated_documents(
        paths, repo, v2_tree, treeland_prefix
    )
    actual_gitlink = gitlink_object(repo, v2_tree, "3rdparty/waylib-shared")
    if actual_gitlink != expected_gitlink:
        raise ValueError(f"final WaylibShared gitlink drift: {actual_gitlink}")
    remediation = verify_remediation_sources(
        manifest,
        _read_json(paths.remediation_ledger),
        GitRepository(paths.repo),
        GitRepository(paths.waylib_repo),
    )
    return {
        "product_manifest_sha256": master["entries_sha256"],
        "actual_product_entries_sha256": oracle["entries_sha256"],
        "product_entry_count": oracle["entry_count"],
        "product_rewrite_authority_count": len(rewrite_authority),
        "three_way_product_oracle": "pass",
        "product_mismatches": 0,
        "full_tree_difference_paths": list(changed_paths),
        "final_gitlink": actual_gitlink,
        "remediation_verification": remediation,
        **tool_summary,
        **document_summary,
    }


def verify_preview_history(
    repo: GitRepository,
    manifest: dict[str, Any],
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    """Re-read every generated commit and verify history/message provenance."""

    head = records[-1]["new_commit"]
    base = manifest["frozen_inputs"]["rewrite_base"]
    if int(repo.run("rev-list", "--count", f"{base}..{head}")) != 330:
        raise ValueError("preview successor count drift")
    if repo.run("rev-list", "--min-parents=2", f"{base}..{head}"):
        raise ValueError("preview history contains a merge commit")
    counts = _verify_commit_records(repo, manifest, records)
    _verify_legacy_object_disjointness(repo, manifest, records)
    repo.run("fsck", "--strict", "--no-reflogs", "--no-dangling", head)
    return {"successor_count": 330, "rendered_count": 330, **counts}


def _verify_commit_records(
    repo: GitRepository,
    manifest: dict[str, Any],
    records: list[dict[str, Any]],
) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for entry, record in zip(manifest["entries"], records, strict=True):
        new_payload = repo.cat_file("commit", record["new_commit"])
        old_payload = repo.cat_file("commit", record["expected_v1_commit"])
        new = parse_raw_commit(new_payload)
        old = parse_raw_commit(old_payload)
        _verify_record_bytes(repo, entry, record, old, new, new_payload)
        if entry["ordered_index"] == 1:
            if new_payload == old_payload:
                raise ValueError("rebuilt anchor reused corrected-v1 object bytes")
            counts["rebuilt_anchor"] += 1
        if new.author_header != old.author_header or new.committer_header != old.committer_header:
            raise ValueError(f"identity header drift at {entry['ordered_index']}")
        parsed = parse_message(new.message, entry["message_schema"])
        _count_message_provenance(entry, parsed, counts)
    _verify_message_counts(counts)
    return dict(sorted(counts.items()))


def _verify_record_bytes(
    repo: GitRepository,
    entry: dict[str, Any],
    record: dict[str, Any],
    old: Any,
    new: Any,
    new_payload: bytes,
) -> None:
    index = entry["ordered_index"]
    if git_object_id("commit", new_payload) != record["new_commit"]:
        raise ValueError(f"new commit object ID drift at {index}")
    if new.parent != record["new_parent"] or new.tree != record["new_tree"]:
        raise ValueError(f"new commit identity drift at {index}")
    if old.parent != record["old_parent"] or old.tree != record["old_tree"]:
        raise ValueError(f"old commit identity drift at {index}")
    transition = repo.raw_transition(new.parent, record["new_commit"])
    if hashlib.sha256(transition).hexdigest() != record["v2_delta_sha256"]:
        raise ValueError(f"v2 transition hash drift at {index}")
    if list(tree_diff_paths(repo, new.parent, record["new_commit"])) != record[
        "actual_v2_changed_paths"
    ]:
        raise ValueError(f"v2 transition path drift at {index}")
    if hashlib.sha256(new_payload).hexdigest() != record["raw_commit_sha256"]:
        raise ValueError(f"raw commit SHA-256 drift at {index}")
    if hashlib.sha256(new.message).hexdigest() != record["new_message_sha256"]:
        raise ValueError(f"rendered message SHA-256 drift at {index}")


def _count_message_provenance(
    entry: dict[str, Any], parsed: dict[str, Any], counts: Counter[str]
) -> None:
    message = canonical_bytes(parsed)
    if any(key in message for key in FORBIDDEN_FINAL_KEYS):
        raise ValueError(f"retired source key at {entry['ordered_index']}")
    schema = entry["message_schema"]
    counts[f"schema_{schema}"] += 1
    if schema == "treeland":
        counts["treeland_target"] += 1
        if parsed.get("legacy_treeland_commit"):
            counts["legacy_treeland_pair"] += 1
        if parsed.get("waylib_commit"):
            counts["waylib_provenance"] += 1
    elif schema == "waylib":
        counts["waylib_provenance"] += 1
        if parsed.get("absorbed_waylib_commit"):
            counts["absorbed_waylib"] += 1
    elif parsed.get("waylib_commit"):
        counts["waylib_provenance"] += 1


def _verify_message_counts(counts: Counter[str]) -> None:
    expected = {
        "rebuilt_anchor": 1,
        "schema_treeland": 298,
        "schema_waylib": 7,
        "schema_adaptation": 25,
        "treeland_target": 298,
        "legacy_treeland_pair": 26,
        "waylib_provenance": 73,
        "absorbed_waylib": 1,
    }
    if counts != Counter(expected):
        raise ValueError(f"preview message provenance count drift: {counts}")


def _verify_legacy_object_disjointness(
    repo: GitRepository,
    manifest: dict[str, Any],
    records: list[dict[str, Any]],
) -> None:
    generated = {record["new_commit"] for record in records}
    legacy: set[str] = set()
    preserved = set(
        manifest["frozen_inputs"].get("preserved_candidate_refs", ())
    )
    for ref, commit in manifest["frozen_inputs"]["refs"].items():
        if (
            ref == "refs/heads/ds-mod"
            or ref in preserved
            or not ref.startswith("refs/heads/")
        ):
            continue
        output = repo.run("rev-list", f"{SHARED_ANCHOR}..{commit}").decode().splitlines()
        legacy.update(output)
    reused = sorted(generated & legacy)
    if reused:
        raise ValueError(f"preview reuses retired-branch commit objects: {reused}")


def _verify_tool_bundle(
    paths: InputPaths,
    repo: GitRepository,
    tree: str,
    expected_hash: str,
) -> dict[str, Any]:
    expected = bundle_files(paths.bundle_root, BUNDLE_REPO_PREFIX)
    if bundle_sha256(expected) != expected_hash:
        raise ValueError("final tool bundle hash differs from frozen input")
    actual_entries = {
        entry["path"]: entry
        for entry in tree_entries(repo, tree)
        if entry["path"].startswith(f"{BUNDLE_REPO_PREFIX}/")
    }
    if set(actual_entries) != set(expected):
        raise ValueError("final tool bundle path set drift")
    for path, content in expected.items():
        item = actual_entries[path]
        if item["mode"] != "100644" or item["kind"] != "blob":
            raise ValueError(f"final tool bundle mode drift: {path}")
        if repo.cat_file("blob", item["object_id"]) != content:
            raise ValueError(f"final tool bundle byte drift: {path}")
    return {"tool_bundle_sha256": expected_hash, "tool_bundle_file_count": len(expected)}


def _verify_generated_documents(
    paths: InputPaths,
    repo: GitRepository,
    tree: str,
    prefix: dict[str, Any],
) -> dict[str, Any]:
    entries = {entry["path"]: entry for entry in tree_entries(repo, tree)}
    expected_docs = {
        f"{ADAPTATION_DOCS_PREFIX}{item['v2_target']}.md"
        for item in prefix["entries"]
        if item["action"] == "adapted"
    }
    actual_docs = {path for path in entries if path.startswith(ADAPTATION_DOCS_PREFIX)}
    if len(expected_docs) != 58 or actual_docs != expected_docs:
        raise ValueError("final adaptation document path set drift")
    expected_static = {
        AUDIT_PATH: render_audit_document(prefix),
        ".gitattributes": GITATTRIBUTES,
        PLAN_PATH: finalize_plan_document(paths.plan.read_bytes()),
    }
    for path, content in expected_static.items():
        entry = entries.get(path)
        if entry is None or repo.cat_file("blob", entry["object_id"]) != content:
            raise ValueError(f"final generated document byte drift: {path}")
    for path in actual_docs:
        content = repo.cat_file("blob", entries[path]["object_id"])
        if any(key in content for key in FORBIDDEN_FINAL_KEYS):
            raise ValueError(f"final adaptation document contains retired key: {path}")
    return {"adaptation_document_count": 58, "static_document_count": 3}


def _read_json(path: Any) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value
