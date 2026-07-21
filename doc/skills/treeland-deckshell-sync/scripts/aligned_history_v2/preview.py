"""Run one independent 330-entry object preview from frozen v2 inputs."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .actual_atomic import verify_compile_atomic_history
from .artifacts import write_hashed_json
from .context import InputPaths
from .freeze_inputs import collect_frozen_inputs
from .manifest import validate_input_manifest
from .object_inventory import inventory_loose_objects
from .prefix import seal_treeland_prefix
from .preview_entries import (
    PreviewEntryResult,
    render_regenerated_entry,
    replay_dependency_proven_entry,
    replay_rebuilt_anchor_entry,
    replay_remediated_entry,
    replay_rendered_entry,
)
from .preview_mapping import build_mapping_record, finalize_output_mapping
from .preview_regeneration import build_regeneration_overlay
from .preview_verification import verify_final_tree, verify_preview_history
from .repository import GitRepository
from .remediation import verify_remediation_sources


@dataclass(frozen=True)
class PreviewArtifacts:
    """Canonical artifacts produced by one isolated preview."""

    prefix: dict[str, Any]
    mapping: dict[str, Any]
    object_inventory: dict[str, Any]
    evidence: dict[str, Any]


def prepare_preview_directories(
    source_objects: Path, object_directory: Path, scratch_directory: Path
) -> tuple[Path, Path]:
    """Create fresh disjoint preview directories outside source objects."""

    source = source_objects.resolve()
    objects = object_directory.resolve()
    scratch = scratch_directory.resolve()
    pairs = ((source, objects), (source, scratch), (objects, scratch))
    if any(first == second or first.is_relative_to(second) or second.is_relative_to(first) for first, second in pairs):
        raise ValueError("preview directories must be disjoint from source objects and each other")
    for path in (objects, scratch):
        if path.is_symlink():
            raise ValueError(f"preview directory must not be a symlink: {path}")
        if path.exists() and any(path.iterdir()):
            raise ValueError(f"preview directory must be empty: {path}")
        path.mkdir(parents=True, exist_ok=True)
    return objects, scratch


def run_isolated_preview(
    paths: InputPaths,
    manifest: dict[str, Any],
    dry_run: dict[str, Any],
    *,
    preview_name: str,
    object_directory: Path,
    scratch_directory: Path,
) -> PreviewArtifacts:
    """Execute and fully verify one independent A or B preview."""

    _verify_preview_inputs(paths, manifest, dry_run, preview_name)
    source = GitRepository(paths.repo)
    objects, scratch = prepare_preview_directories(
        source.object_directory(), object_directory, scratch_directory
    )
    preview = GitRepository(
        paths.repo,
        object_directory=objects,
        alternates=(source.object_directory(),),
    )
    runner = _PreviewRunner(paths, source, preview, manifest, scratch)
    prefix, records = runner.run_entries()
    final_tree = records[-1]["new_tree"]
    final_summary = verify_final_tree(
        paths,
        preview,
        manifest=manifest,
        v1_tree=manifest["frozen_inputs"]["v1_head_tree"],
        v2_tree=final_tree,
        treeland_prefix=prefix,
        expected_gitlink=manifest["frozen_inputs"]["final_gitlink"],
        expected_tool_bundle_sha256=manifest["frozen_inputs"]["tool_bundle_sha256"],
    )
    history_summary = verify_preview_history(preview, manifest, records)
    atomic_summary = verify_compile_atomic_history(
        paths, preview, manifest, records
    )
    inventory = inventory_loose_objects(objects)
    _verify_inventory_commits(inventory, records)
    mapping = finalize_output_mapping(
        manifest,
        records,
        treeland_prefix_sha256=prefix["canonical_payload_sha256"],
        tool_bundle_sha256=manifest["frozen_inputs"]["tool_bundle_sha256"],
        product_manifest_sha256=final_summary["product_manifest_sha256"],
        final_gitlink=final_summary["final_gitlink"],
    )
    evidence = _preview_evidence(
        preview_name,
        source.object_directory(),
        objects,
        manifest,
        prefix,
        mapping,
        inventory,
        history_summary,
        final_summary,
        atomic_summary,
    )
    return PreviewArtifacts(prefix, mapping, inventory, evidence)


def write_preview_artifacts(
    output_directory: Path, artifacts: PreviewArtifacts
) -> dict[str, Any]:
    """Write one preview's canonical artifacts and hash-bound evidence."""

    output = output_directory.resolve()
    written = {}
    for name, payload in (
        ("treeland-target-prefix.v2.json", artifacts.prefix),
        ("rewrite-target-mapping.v2.json", artifacts.mapping),
        ("object-inventory.v2.json", artifacts.object_inventory),
    ):
        written[name] = write_hashed_json(output / name, payload)
    evidence = dict(artifacts.evidence)
    evidence["artifact_files"] = written
    evidence_hashes = write_hashed_json(output / "preview-evidence.v2.json", evidence)
    return {
        "outcome": "pass",
        "head": artifacts.mapping["head"],
        "head_tree": artifacts.mapping["head_tree"],
        "mapping_sha256": artifacts.mapping["canonical_payload_sha256"],
        "evidence": evidence_hashes,
    }


class _PreviewRunner:
    def __init__(
        self,
        paths: InputPaths,
        source: GitRepository,
        preview: GitRepository,
        manifest: dict[str, Any],
        scratch: Path,
    ) -> None:
        self.paths = paths
        self.source = source
        self.preview = preview
        self.manifest = manifest
        self.scratch = scratch
        self.targets: dict[int, str] = {}
        self.prefix: dict[str, Any] | None = None

    def run_entries(self) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        previous_commit = self.manifest["frozen_inputs"]["rewrite_base"]
        previous_tree = self.source.tree_id(previous_commit)
        records = []
        for entry in self.manifest["entries"]:
            result = self._render_entry(entry, previous_commit, previous_tree)
            record = build_mapping_record(self.source, entry, result)
            records.append(record)
            index = int(entry["ordered_index"])
            self.targets[index] = result.commit
            previous_commit, previous_tree = result.commit, result.tree
            if index == 303:
                self.prefix = seal_treeland_prefix(
                    self.manifest["entries"], self.targets
                )
        if self.prefix is None:
            raise ValueError("Treeland prefix was not sealed during preview")
        return self.prefix, records

    def _render_entry(
        self,
        entry: dict[str, Any],
        previous_commit: str,
        previous_tree: str,
    ) -> PreviewEntryResult:
        transition = entry["tree_transition"]
        if transition == "replay-rebuilt-anchor":
            return replay_rebuilt_anchor_entry(
                self.source,
                self.preview,
                entry,
                rewrite_base=self.manifest["frozen_inputs"]["rewrite_base"],
            )
        index_file = self.scratch / "preview.index"
        if transition == "replay-v1-delta":
            return replay_rendered_entry(
                self.source,
                self.preview,
                entry,
                previous_v2_commit=previous_commit,
                previous_v2_tree=previous_tree,
                index_file=index_file,
            )
        if transition == "replay-dependency-proven-v1-delta":
            return replay_dependency_proven_entry(
                self.source,
                self.preview,
                entry,
                previous_v2_commit=previous_commit,
                previous_v2_tree=previous_tree,
                index_file=index_file,
            )
        if transition == "replay-remediated-v1-delta":
            return replay_remediated_entry(
                self.source,
                self.preview,
                entry,
                previous_v2_commit=previous_commit,
                previous_v2_tree=previous_tree,
                index_file=index_file,
            )
        if self.prefix is None:
            raise ValueError(f"regeneration precedes sealed prefix: {entry['ordered_index']}")
        files = build_regeneration_overlay(
            self.paths,
            self.preview,
            entry,
            parent_tree=previous_tree,
            treeland_prefix=self.prefix,
            expected_tool_bundle_sha256=self.manifest["frozen_inputs"][
                "tool_bundle_sha256"
            ],
        )
        return render_regenerated_entry(
            self.source,
            self.preview,
            entry,
            previous_v2_commit=previous_commit,
            previous_v2_tree=previous_tree,
            files=files,
            index_file=index_file,
        )


def _verify_preview_inputs(
    paths: InputPaths,
    manifest: dict[str, Any],
    dry_run: dict[str, Any],
    preview_name: str,
) -> None:
    if preview_name not in {"A", "B"}:
        raise ValueError("preview name must be A or B")
    validate_input_manifest(manifest)
    if manifest.get("status") != "frozen-input-ready-for-v2-dry-run":
        raise ValueError("preview requires a frozen input manifest")
    if collect_frozen_inputs(paths) != manifest.get("frozen_inputs"):
        raise ValueError("preview frozen inputs differ from current contract inputs")
    ledger = json.loads(paths.remediation_ledger.read_text(encoding="utf-8"))
    verify_remediation_sources(
        manifest,
        ledger,
        GitRepository(paths.repo),
        GitRepository(paths.waylib_repo),
    )
    if dry_run.get("outcome") != "pass":
        raise ValueError("preview requires a passing sequential dry-run")
    if dry_run.get("input_manifest_sha256") != manifest["canonical_payload_sha256"]:
        raise ValueError("preview dry-run is bound to another input manifest")
    if dry_run.get("remediated_transition_count") != 11:
        raise ValueError("preview dry-run remediation count drift")
    if dry_run.get("dependency_proven_transition_count") != 129:
        raise ValueError("preview dry-run dependency count drift")
    if dry_run.get("rebuilt_anchor_count") != 1:
        raise ValueError("preview dry-run rebuilt-anchor count drift")


def _verify_inventory_commits(
    inventory: dict[str, Any], records: list[dict[str, Any]]
) -> None:
    local_commits = {
        item["object_id"]
        for item in inventory["objects"]
        if item["kind"] == "commit"
    }
    expected = {record["new_commit"] for record in records}
    if local_commits != expected or len(local_commits) != 330:
        raise ValueError("preview object inventory does not contain exactly 330 commits")


def _preview_evidence(
    preview_name: str,
    source_objects: Path,
    object_directory: Path,
    manifest: dict[str, Any],
    prefix: dict[str, Any],
    mapping: dict[str, Any],
    inventory: dict[str, Any],
    history_summary: dict[str, Any],
    final_summary: dict[str, Any],
    atomic_summary: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": 2,
        "workflow_mode": "commit-aligned-history-rewrite-v2",
        "preview_name": preview_name,
        "outcome": "pass",
        "input_manifest_sha256": manifest["canonical_payload_sha256"],
        "treeland_prefix_sha256": prefix["canonical_payload_sha256"],
        "mapping_sha256": mapping["canonical_payload_sha256"],
        "object_inventory_sha256": inventory["canonical_payload_sha256"],
        "head": mapping["head"],
        "head_tree": mapping["head_tree"],
        "isolation": {
            "writable_object_directory": str(object_directory),
            "read_only_alternate": str(source_objects),
            "alternate_count": 1,
            "other_preview_is_alternate": False,
            "formal_object_writes": 0,
        },
        "history_verification": history_summary,
        "final_tree_verification": final_summary,
        "compile_atomic_verification": atomic_summary,
    }
