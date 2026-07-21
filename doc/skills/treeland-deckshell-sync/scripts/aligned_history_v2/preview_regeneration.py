"""Build the three authorized regeneration overlays for object previews."""

from __future__ import annotations

import json
from typing import Any

from .adaptation_documents import render_adaptation_documents
from .bundle import bundle_files, bundle_overlay, bundle_sha256
from .context import InputPaths
from .freeze_inputs import BUNDLE_REPO_PREFIX
from .regeneration import finalize_plan_document, render_audit_document
from .repository import GitRepository
from .tree_manifest import path_matches_any
from .tree_transition import parse_raw_transition


AUDIT_PATH = "doc/ai/waylibshared_7dc11a_regression_audit.md"
PLAN_PATH = "doc/ai/deckshell_waylib_commit_aligned_history_rewrite_plan.md"
ADAPTATION_DOCS_PREFIX = "doc/treeland-sync/adaptations/"
GITATTRIBUTES = (
    b"doc/treeland-sync/adaptations/*.md "
    b"whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab\n"
)


def build_regeneration_overlay(
    paths: InputPaths,
    repo: GitRepository,
    entry: dict[str, Any],
    *,
    parent_tree: str,
    treeland_prefix: dict[str, Any],
    expected_tool_bundle_sha256: str,
) -> dict[str, bytes | None]:
    """Dispatch one fixed regeneration index without reading output mapping."""

    index = int(entry["ordered_index"])
    if index == 316:
        return build_audit_overlay(entry, treeland_prefix)
    if index == 329:
        return build_tool_overlay(
            paths,
            repo,
            entry,
            parent_tree=parent_tree,
            expected_bundle_sha256=expected_tool_bundle_sha256,
        )
    if index == 330:
        return build_final_document_overlay(
            paths,
            repo,
            entry,
            parent_tree=parent_tree,
            treeland_prefix=treeland_prefix,
        )
    raise ValueError(f"unsupported regeneration index: {index}")


def build_audit_overlay(
    entry: dict[str, Any], treeland_prefix: dict[str, Any]
) -> dict[str, bytes]:
    """Render the index-316 audit from only the sealed Treeland prefix."""

    overlay = {AUDIT_PATH: render_audit_document(treeland_prefix)}
    _verify_overlay_contract(entry, overlay, expected_outputs=1)
    return overlay


def build_tool_overlay(
    paths: InputPaths,
    repo: GitRepository,
    entry: dict[str, Any],
    *,
    parent_tree: str,
    expected_bundle_sha256: str,
) -> dict[str, bytes | None]:
    """Make index 329 contain the exact bundle executing both previews."""

    bundle = bundle_files(paths.bundle_root, BUNDLE_REPO_PREFIX)
    actual_hash = bundle_sha256(bundle)
    if actual_hash != expected_bundle_sha256:
        raise ValueError(f"tool bundle hash drift: {actual_hash}")
    overlay = bundle_overlay(
        repo,
        parent_tree,
        bundle,
        BUNDLE_REPO_PREFIX,
    )
    _verify_overlay_contract(entry, overlay, expected_outputs=len(overlay))
    return overlay


def build_final_document_overlay(
    paths: InputPaths,
    repo: GitRepository,
    entry: dict[str, Any],
    *,
    parent_tree: str,
    treeland_prefix: dict[str, Any],
) -> dict[str, bytes | None]:
    """Render the final plan, attributes, and 58 v2 SHA-named records."""

    adaptation_manifest = json.loads(paths.adaptation_manifest.read_text(encoding="utf-8"))
    ledger = json.loads(paths.remediation_ledger.read_text(encoding="utf-8"))
    remediation_paths = {
        path
        for target in ledger["targets"]
        for path in target["paths"]
    }
    documents = render_adaptation_documents(
        repo,
        treeland_prefix,
        adaptation_manifest,
        remediation_paths=remediation_paths,
    )
    overlay = _v1_non_document_overlay(repo, entry)
    document_overlay = bundle_overlay(
        repo,
        parent_tree,
        documents,
        ADAPTATION_DOCS_PREFIX,
    )
    overlap = set(overlay) & set(document_overlay)
    if overlap:
        raise ValueError(f"final document/product overlay overlap: {sorted(overlap)}")
    overlay.update(document_overlay)
    overlay[".gitattributes"] = GITATTRIBUTES
    overlay[PLAN_PATH] = finalize_plan_document(paths.plan.read_bytes())
    _verify_overlay_contract(entry, overlay, expected_outputs=len(overlay))
    return overlay


def _v1_non_document_overlay(
    repo: GitRepository, entry: dict[str, Any]
) -> dict[str, bytes | None]:
    transition = repo.raw_transition(
        str(entry["expected_v1_parent"]),
        str(entry["expected_v1_commit"]),
    )
    changes = parse_raw_transition(transition)
    if [change.path for change in changes] != entry["expected_v1_changed_paths"]:
        raise ValueError("final corrected-v1 transition path drift")
    overlay: dict[str, bytes | None] = {}
    for change in changes:
        if change.path.startswith(ADAPTATION_DOCS_PREFIX):
            continue
        if change.new_mode == "000000":
            overlay[change.path] = None
            continue
        if change.new_mode != "100644":
            raise ValueError(
                f"unsupported final product mode {change.new_mode}: {change.path}"
            )
        overlay[change.path] = repo.cat_file("blob", change.new_object)
    return overlay


def _verify_overlay_contract(
    entry: dict[str, Any], overlay: dict[str, bytes | None], *, expected_outputs: int
) -> None:
    job = entry.get("regeneration_job")
    if not isinstance(job, dict) or job.get("expected_output_count") != expected_outputs:
        raise ValueError(f"regeneration output count drift at {entry['ordered_index']}")
    rules = tuple(str(rule) for rule in entry["authorized_v2_delta_paths"])
    unauthorized = [path for path in overlay if not path_matches_any(path, rules)]
    if unauthorized:
        raise ValueError(
            f"regeneration overlay exceeds authorization at {entry['ordered_index']}: "
            f"{unauthorized}"
        )
