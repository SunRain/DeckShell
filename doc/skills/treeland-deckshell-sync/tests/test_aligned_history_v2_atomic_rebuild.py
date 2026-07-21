"""Authority-selection tests for independent compile-atomic rebuilds."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aligned_history_v2 import atomic_rebuild


class AlignedHistoryV2AtomicRebuildTests(unittest.TestCase):
    def test_dependency_rebuild_uses_frozen_predecessor_manifest(self) -> None:
        paths = self._paths()
        mapping = {
            "entries": [
                {"ordered_index": index, "expected_v1_commit": f"commit-{index}"}
                for index in range(1, 331)
            ]
        }
        candidate = {
            "canonical_payload_sha256": "candidate",
            "entries": [{"ordered_index": 1, "expected_v1_commit": "candidate"}],
        }
        frozen = {
            "canonical_payload_sha256": "frozen",
            "entries": [{"ordered_index": 1, "expected_v1_commit": "frozen"}],
        }
        sidecars = {
            "protocol-lock.json": {},
            "anchor-provenance.json": {"protocol_source_commit": "protocol"},
            "anchor-generation.json": {
                "old_anchor": "old-anchor",
                "new_anchor": "new-anchor",
                "new_tree": "new-tree",
                "changed_paths": [],
            },
            "bootstrap.json": {},
            "remediation.json": {},
            "runtime-observations.json": {
                "artifact_sha256": "runtime-hash",
                "observations": [{"observation_id": "runtime-edge"}],
            },
            "protocol-ledger.json": {"artifact_sha256": "protocol-hash"},
            "dependency-set.json": {"artifact_sha256": "dependency-hash"},
            "dependency-bundle.json": {"artifact_sha256": "bundle-hash"},
        }

        def read_hashed(path: Path) -> dict[str, object]:
            if path == paths.legacy_v2_mapping:
                return mapping
            if path == paths.legacy_v2_candidate:
                return candidate
            if path == paths.legacy_v2_manifest:
                return frozen
            raise AssertionError(f"unexpected hashed input: {path}")

        dependency_builder = Mock(return_value={})
        with (
            patch.object(atomic_rebuild, "GitRepository"),
            patch.object(
                atomic_rebuild,
                "read_sidecar_json",
                side_effect=lambda path, _field=None: sidecars[path.name],
            ),
            patch.object(atomic_rebuild, "read_hashed_json", side_effect=read_hashed),
            patch.object(atomic_rebuild, "build_protocol_ledger", return_value={}),
            patch.object(atomic_rebuild, "build_dependency_set", dependency_builder),
            patch.object(
                atomic_rebuild, "build_dependency_bundle_ledger", return_value={}
            ),
            patch.object(atomic_rebuild, "source_components_from_lock", return_value=[]),
        ):
            atomic_rebuild.rebuild_atomic_ledgers(paths, Mock())

        self.assertIs(dependency_builder.call_args.args[0], frozen)
        self.assertIs(
            dependency_builder.call_args.kwargs["runtime_observations"],
            sidecars["runtime-observations.json"]["observations"],
        )
        self.assertTrue(
            callable(dependency_builder.call_args.kwargs["waylib_is_ancestor"])
        )
        self.assertTrue(
            callable(dependency_builder.call_args.kwargs["waylib_blob_reader"])
        )

    @staticmethod
    def _paths() -> SimpleNamespace:
        names = {
            "protocol_repo": "protocol-repo",
            "waylib_repo": "waylib-repo",
            "protocol_lock": "protocol-lock.json",
            "anchor_provenance": "anchor-provenance.json",
            "anchor_generation": "anchor-generation.json",
            "legacy_v2_mapping": "legacy-mapping.json",
            "legacy_v2_candidate": "legacy-candidate.json",
            "legacy_v2_manifest": "legacy-manifest.json",
            "bootstrap_transition_map": "bootstrap.json",
            "remediation_ledger": "remediation.json",
            "runtime_observations": "runtime-observations.json",
            "protocol_ledger": "protocol-ledger.json",
            "dependency_set": "dependency-set.json",
            "dependency_bundle": "dependency-bundle.json",
        }
        return SimpleNamespace(**{key: Path(value) for key, value in names.items()})


if __name__ == "__main__":
    unittest.main()
