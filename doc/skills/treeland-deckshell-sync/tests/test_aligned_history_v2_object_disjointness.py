from __future__ import annotations

import sys
from pathlib import Path

import pytest


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


from aligned_history_v2.preview_verification import (
    _verify_legacy_object_disjointness,
)
from aligned_history_v2.freeze_inputs import _preserved_corrected_candidate_refs


class FakeRepository:
    def run(self, *args: str) -> bytes:
        assert args[:2] == ("rev-list", "86942a0d65d9a202fb2efa0ee1b57d6a7d9ac6ce..legacy") or args[:2] == (
            "rev-list",
            "86942a0d65d9a202fb2efa0ee1b57d6a7d9ac6ce..preserved",
        )
        return b"legacy-object\n" if args[1].endswith("legacy") else b"shared-object\n"


def _manifest(*, preserve_failed_candidate: bool) -> dict[str, object]:
    return {
        "frozen_inputs": {
            "refs": {
                "refs/heads/legacy": "legacy",
                "refs/heads/failed-candidate": "preserved",
            },
            "preserved_candidate_refs": (
                ["refs/heads/failed-candidate"]
                if preserve_failed_candidate
                else []
            ),
        }
    }


def test_failed_candidate_object_overlap_is_allowed_when_frozen() -> None:
    _verify_legacy_object_disjointness(
        FakeRepository(),
        _manifest(preserve_failed_candidate=True),
        [{"new_commit": "shared-object"}],
    )


def test_unclassified_branch_object_overlap_is_rejected() -> None:
    with pytest.raises(ValueError, match="retired-branch commit objects"):
        _verify_legacy_object_disjointness(
            FakeRepository(),
            _manifest(preserve_failed_candidate=False),
            [{"new_commit": "shared-object"}],
        )


def test_all_corrected_candidate_refs_are_preserved_from_frozen_snapshot() -> None:
    refs = {
        "refs/heads/migration/commit-aligned-history-corrected-v1-20260725": "v1",
        "refs/heads/migration/commit-aligned-history-corrected-v1-compile-atomic-r4-20260729": "v1-r4",
        "refs/heads/migration/commit-aligned-history-corrected-v2-compile-atomic-20260727": "v2-invalid",
        "refs/heads/migration/commit-aligned-history-corrected-v2-compile-atomic-r3-20260728": "v2-r3",
        "refs/heads/migration/unrelated": "other-migration",
        "refs/heads/master": "master",
        "refs/remotes/priv/migration/commit-aligned-history-corrected-v2-legacy": "remote",
    }

    assert _preserved_corrected_candidate_refs(refs) == [
        "refs/heads/migration/commit-aligned-history-corrected-v1-20260725",
        "refs/heads/migration/commit-aligned-history-corrected-v1-compile-atomic-r4-20260729",
        "refs/heads/migration/commit-aligned-history-corrected-v2-compile-atomic-20260727",
        "refs/heads/migration/commit-aligned-history-corrected-v2-compile-atomic-r3-20260728",
    ]
