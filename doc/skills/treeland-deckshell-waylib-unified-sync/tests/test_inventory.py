from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from typing import Dict, Optional, Set

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from unified_sync_lib.inventory import build_unified_inventory
from unified_sync_lib.policy import load_policy

from support import commit_files, init_repo, run, write_policy


class UnifiedInventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.repo = init_repo(self.root / "source")
        self.base = commit_files(self.repo, {"README.local": "base\n"}, "base")
        self.policy_path = write_policy(self.root / "path-policy.md")
        self.policy = load_policy(self.policy_path)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def inventory(self, head: str, approvals: Optional[Set[str]] = None) -> Dict:
        return build_unified_inventory(
            self.repo,
            self.base,
            head,
            self.policy,
            self.policy_path,
            approvals or set(),
        )

    def test_classifies_each_owned_lane_without_dependency_only_alias(self) -> None:
        commit_files(self.repo, {"src/a.cpp": "a\n"}, "parent")
        commit_files(self.repo, {"qwlroots/q.cpp": "q\n"}, "child")
        commit_files(
            self.repo,
            {"src/b.cpp": "b\n", "waylib/w.cpp": "w\n"},
            "dual",
        )
        head = commit_files(self.repo, {"vendor/notice": "ignored\n"}, "unowned")

        result = self.inventory(head)

        self.assertEqual(result["outcome"], "pass")
        self.assertEqual(
            [entry["classification"] for entry in result["commits"]],
            ["deckshell-only", "waylib-only", "dual", "unowned-skip"],
        )
        self.assertEqual(
            result["commits"][1]["waylib_shared"]["source_paths"],
            ["qwlroots/q.cpp"],
        )
        self.assertEqual(
            result["commits"][2]["deckshell"]["target_paths"],
            ["compositor/src/b.cpp"],
        )

    def test_wrapper_files_remain_child_files_without_qwlroots_alias(self) -> None:
        head = commit_files(self.repo, {"wlroots/backend.c": "x\n"}, "layout drift")

        result = self.inventory(head)

        self.assertEqual(result["outcome"], "pass")
        item = result["commits"][0]
        self.assertEqual(item["waylib_shared"]["source_paths"], ["wlroots/backend.c"])
        self.assertEqual(item["wlroots"]["source_paths"], [])

    def test_blocks_source_paths_that_cannot_be_serialized_safely(self) -> None:
        head = commit_files(
            self.repo,
            {"src/unsafe\nmarker.cpp": "bad\n"},
            "unsafe path",
        )

        result = self.inventory(head)

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("unsafe source path" in reason for reason in result["blocked_reasons"])
        )

    def test_splits_cross_lane_rename_into_both_lanes(self) -> None:
        commit_files(self.repo, {"src/old.cpp": "same\n"}, "add old")
        self.base = run(self.repo, "rev-parse", "HEAD")
        (self.repo / "qwlroots").mkdir()
        run(self.repo, "mv", "src/old.cpp", "qwlroots/new.cpp")
        run(self.repo, "commit", "-m", "move across lanes")
        head = run(self.repo, "rev-parse", "HEAD")

        result = self.inventory(head)

        entry = result["commits"][0]
        self.assertEqual(entry["classification"], "dual")
        self.assertEqual(entry["deckshell"]["target_paths"], ["compositor/src/old.cpp"])
        self.assertEqual(entry["waylib_shared"]["source_paths"], ["qwlroots/new.cpp"])
        self.assertTrue(entry["changes"][0]["status"].startswith("R"))

    def test_preserves_both_sides_of_cross_lane_copy(self) -> None:
        commit_files(self.repo, {"src/original.cpp": "same\n"}, "add source")
        self.base = run(self.repo, "rev-parse", "HEAD")
        target = self.repo / "waylib/copied.cpp"
        target.parent.mkdir()
        target.write_text("same\n", encoding="utf-8")
        run(self.repo, "add", "waylib/copied.cpp")
        run(self.repo, "commit", "-m", "copy across lanes")
        head = run(self.repo, "rev-parse", "HEAD")

        result = self.inventory(head)

        entry = result["commits"][0]
        self.assertEqual(entry["classification"], "waylib-only")
        self.assertEqual(entry["deckshell"]["target_paths"], [])
        self.assertEqual(entry["waylib_shared"]["source_paths"], ["waylib/copied.cpp"])
        self.assertTrue(entry["changes"][0]["status"].startswith("C"))
        self.assertEqual(entry["changes"][0]["old"]["source"], "src/original.cpp")
        self.assertEqual(entry["changes"][0]["new"]["source"], "waylib/copied.cpp")

    def test_copy_source_relation_does_not_claim_an_unknown_mutation(self) -> None:
        commit_files(self.repo, {"unknown/original.cpp": "same\n"}, "add source")
        self.base = run(self.repo, "rev-parse", "HEAD")
        target = self.repo / "waylib/copied.cpp"
        target.parent.mkdir()
        target.write_text("same\n", encoding="utf-8")
        run(self.repo, "add", "waylib/copied.cpp")
        run(self.repo, "commit", "-m", "copy unknown source into child")
        head = run(self.repo, "rev-parse", "HEAD")

        result = self.inventory(head)

        entry = result["commits"][0]
        self.assertEqual(result["outcome"], "pass")
        self.assertEqual(entry["classification"], "waylib-only")
        self.assertEqual(entry["blocked_reasons"], [])
        self.assertEqual(entry["changes"][0]["old"]["category"], "unknown")
        self.assertEqual(entry["waylib_shared"]["source_paths"], ["waylib/copied.cpp"])

    def test_copy_source_relation_is_not_reported_as_a_dropped_mutation(self) -> None:
        commit_files(self.repo, {"waylib/original.cpp": "same\n"}, "add source")
        self.base = run(self.repo, "rev-parse", "HEAD")
        target = self.repo / "src/copied.cpp"
        target.parent.mkdir()
        target.write_text("same\n", encoding="utf-8")
        run(self.repo, "add", "src/copied.cpp")
        run(self.repo, "commit", "-m", "copy child source into parent")
        head = run(self.repo, "rev-parse", "HEAD")

        result = self.inventory(head)

        entry = result["commits"][0]
        self.assertEqual(entry["classification"], "deckshell-only")
        self.assertEqual(entry["deckshell"]["drop_paths"], [])
        self.assertEqual(entry["waylib_shared"]["source_paths"], [])
        self.assertEqual(entry["changes"][0]["old"]["source"], "waylib/original.cpp")

    def test_requires_review_approval_before_parent_lane_is_authorized(self) -> None:
        head = commit_files(self.repo, {".github/workflows/ci.yml": "x\n"}, "ci")

        blocked = self.inventory(head)
        approved = self.inventory(head, {".github"})

        self.assertEqual(blocked["outcome"], "blocked")
        self.assertEqual(approved["outcome"], "pass")
        self.assertEqual(approved["commits"][0]["classification"], "deckshell-only")
        self.assertEqual(
            approved["commits"][0]["deckshell"]["target_paths"],
            [".github/workflows/ci.yml"],
        )

    def test_binds_range_head_to_frozen_source_tip(self) -> None:
        head = commit_files(self.repo, {"src/a.cpp": "a\n"}, "range head")
        source_tip = commit_files(self.repo, {"src/b.cpp": "b\n"}, "source tip")

        result = build_unified_inventory(
            self.repo,
            self.base,
            head,
            self.policy,
            self.policy_path,
            set(),
            source_tip,
        )

        self.assertEqual(result["range"]["head"], head)
        self.assertEqual(result["range"]["source_tip"], source_tip)
        self.assertEqual(result["range"]["ordered_source_commits"], [head])

    def test_rejects_range_head_outside_frozen_source_tip(self) -> None:
        head = commit_files(self.repo, {"src/a.cpp": "a\n"}, "range head")
        run(self.repo, "checkout", "-b", "divergent", self.base)
        source_tip = commit_files(self.repo, {"src/b.cpp": "b\n"}, "other tip")

        result = build_unified_inventory(
            self.repo,
            self.base,
            head,
            self.policy,
            self.policy_path,
            set(),
            source_tip,
        )

        self.assertEqual(result["outcome"], "blocked")
        self.assertIn(
            "range head is not an ancestor of frozen source tip",
            result["blocked_reasons"],
        )


if __name__ == "__main__":
    unittest.main()
