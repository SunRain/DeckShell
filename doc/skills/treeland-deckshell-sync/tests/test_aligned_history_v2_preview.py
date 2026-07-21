"""Tests for isolated aligned-history v2 preview entry generation."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aligned_history_v2.git_objects import parse_raw_commit, render_raw_commit
from aligned_history_v2.preview_mapping import build_mapping_record
from aligned_history_v2.preview import prepare_preview_directories
from aligned_history_v2 import preview_entries
from aligned_history_v2.preview_entries import (
    render_regenerated_entry,
    replay_rendered_entry,
    reuse_exact_entry,
)
from aligned_history_v2.repository import GitRepository


class AlignedHistoryV2PreviewTests(unittest.TestCase):
    def test_rebuilt_anchor_is_independently_rendered_with_identical_delta(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo_path = root / "repo"
            self._init_repo(repo_path)
            (repo_path / "base.txt").write_text("base\n", encoding="utf-8")
            self._commit_all(repo_path, "base")
            base = self._rev_parse(repo_path, "HEAD")
            (repo_path / "anchor.txt").write_text("anchor\n", encoding="utf-8")
            self._commit_all(repo_path, "rebuilt anchor")
            anchor = self._rev_parse(repo_path, "HEAD")
            source = GitRepository(repo_path)
            preview = GitRepository(
                repo_path,
                object_directory=root / "objects",
                alternates=(source.object_directory(),),
            )
            transition = source.raw_transition(base, anchor)
            entry = {
                "ordered_index": 1,
                "expected_v1_commit": anchor,
                "expected_v1_parent": base,
                "expected_v1_tree": source.tree_id(anchor),
                "expected_v1_changed_paths": ["anchor.txt"],
                "expected_v1_delta_sha256": hashlib.sha256(transition).hexdigest(),
                "tree_transition": "replay-rebuilt-anchor",
                "message_inputs": {
                    "schema": "adaptation",
                    "subject_body": "replay rebuilt anchor\n",
                    "classification": "regenerate",
                    "action": "regenerate",
                    "paths": ["anchor.txt"],
                    "notes": ["Independently replay the corrected-v1 anchor."],
                    "derivation": "regenerate",
                },
            }

            result = preview_entries.replay_rebuilt_anchor_entry(
                source,
                preview,
                entry,
                rewrite_base=base,
            )

            self.assertNotEqual(result.commit, anchor)
            self.assertEqual(result.parent, base)
            self.assertEqual(result.tree, source.tree_id(anchor))
            self.assertEqual(result.v1_delta_sha256, result.v2_delta_sha256)
            self.assertEqual(result.actual_changed_paths, ("anchor.txt",))

    def test_preview_directories_must_be_fresh_and_outside_source_objects(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_objects = root / "source-objects"
            source_objects.mkdir()
            nonempty = root / "nonempty"
            nonempty.mkdir()
            (nonempty / "sentinel").write_text("occupied\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "must be empty"):
                prepare_preview_directories(
                    source_objects,
                    nonempty,
                    root / "scratch",
                )

            object_dir, scratch = prepare_preview_directories(
                source_objects,
                root / "objects",
                root / "scratch-fresh",
            )
            self.assertTrue(object_dir.is_dir())
            self.assertTrue(scratch.is_dir())

    def test_ordinary_entry_replays_delta_and_preserves_parent_overlay(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo_path = root / "repo"
            self._init_repo(repo_path)
            (repo_path / "file.txt").write_text("before\n", encoding="utf-8")
            self._commit_all(repo_path, "root")
            subprocess.run(
                ["git", "-C", str(repo_path), "commit", "--allow-empty", "-m", "parent"],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            v1_parent = self._rev_parse(repo_path, "HEAD")
            anchor_entry = {
                "ordered_index": 1,
                "expected_v1_commit": v1_parent,
                "expected_v1_parent": self._rev_parse(repo_path, f"{v1_parent}^"),
                "expected_v1_tree": source_tree
                if (source_tree := GitRepository(repo_path).tree_id(v1_parent))
                else "",
                "expected_v1_changed_paths": [],
                "expected_v1_delta_sha256": hashlib.sha256(
                    GitRepository(repo_path).raw_transition(f"{v1_parent}^", v1_parent)
                ).hexdigest(),
                "tree_transition": "reuse-exact-commit-object",
                "message_inputs": {
                    "schema": "passthrough",
                    "raw_message_sha256": hashlib.sha256(
                        parse_raw_commit(
                            GitRepository(repo_path).cat_file("commit", v1_parent)
                        ).message
                    ).hexdigest(),
                },
            }
            anchor = reuse_exact_entry(GitRepository(repo_path), anchor_entry)
            self.assertEqual(anchor.commit, v1_parent)
            self.assertEqual(anchor.tree, source_tree)
            self.assertEqual(anchor.inherited_overlay_paths, ())
            (repo_path / "file.txt").write_text("after\n", encoding="utf-8")
            self._commit_all(repo_path, "source")
            v1_commit = self._rev_parse(repo_path, "HEAD")

            source = GitRepository(repo_path)
            preview = GitRepository(
                repo_path,
                object_directory=root / "objects",
                alternates=(source.object_directory(),),
            )
            overlay_tree = preview.apply_files(
                source.tree_id(v1_parent),
                {"overlay.txt": b"kept\n"},
                root / "overlay.index",
            )
            raw_parent = parse_raw_commit(source.cat_file("commit", v1_parent))
            rendered_parent = render_raw_commit(
                raw_parent,
                tree=overlay_tree,
                parent=raw_parent.parent,
                message=b"v2 parent\n",
            )
            previous_v2_commit = preview.write_object(
                "commit", rendered_parent.payload
            )
            transition = source.raw_transition(v1_parent, v1_commit)
            entry = {
                "ordered_index": 2,
                "expected_v1_commit": v1_commit,
                "expected_v1_parent": v1_parent,
                "expected_v1_tree": source.tree_id(v1_commit),
                "expected_v1_changed_paths": ["file.txt"],
                "expected_v1_delta_sha256": hashlib.sha256(transition).hexdigest(),
                "tree_transition": "replay-v1-delta",
                "message_inputs": {
                    "schema": "adaptation",
                    "subject_body": "rewrite source\n",
                    "classification": "preserve-tail",
                    "action": "preserve-tail",
                    "paths": ["file.txt"],
                    "notes": ["Preserve the source delta."],
                    "derivation": "patch-equivalent",
                },
            }

            result = replay_rendered_entry(
                source,
                preview,
                entry,
                previous_v2_commit=previous_v2_commit,
                previous_v2_tree=overlay_tree,
                index_file=root / "entry.index",
            )

            self.assertEqual(result.actual_changed_paths, ("file.txt",))
            self.assertEqual(result.inherited_overlay_paths, ("overlay.txt",))
            self.assertEqual(
                preview.raw_transition(overlay_tree, result.tree), transition
            )
            self.assertEqual(
                preview.cat_file("blob", self._tree_object(preview, result.tree, "overlay.txt")),
                b"kept\n",
            )
            self.assertNotEqual(result.tree, source.tree_id(v1_commit))
            mapping = build_mapping_record(source, entry, result)
            self.assertEqual(mapping["new_commit"], result.commit)
            self.assertEqual(mapping["v1_delta_sha256"], mapping["v2_delta_sha256"])
            self.assertEqual(mapping["inherited_overlay_paths"], ["overlay.txt"])
            self.assertEqual(mapping["verification"], "pass")

            entry["tree_transition"] = "replay-dependency-proven-v1-delta"
            dependency_result = preview_entries.replay_dependency_proven_entry(
                source,
                preview,
                entry,
                previous_v2_commit=previous_v2_commit,
                previous_v2_tree=overlay_tree,
                index_file=root / "dependency-entry.index",
            )
            self.assertEqual(
                dependency_result.v1_delta_sha256,
                dependency_result.v2_delta_sha256,
            )

    def test_regenerated_entry_changes_only_authorized_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo_path = root / "repo"
            self._init_repo(repo_path)
            (repo_path / "legacy.txt").write_text("before\n", encoding="utf-8")
            self._commit_all(repo_path, "root")
            subprocess.run(
                ["git", "-C", str(repo_path), "commit", "--allow-empty", "-m", "parent"],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            v1_parent = self._rev_parse(repo_path, "HEAD")
            (repo_path / "legacy.txt").write_text("legacy output\n", encoding="utf-8")
            self._commit_all(repo_path, "legacy regeneration")
            v1_commit = self._rev_parse(repo_path, "HEAD")

            source = GitRepository(repo_path)
            preview = GitRepository(
                repo_path,
                object_directory=root / "objects",
                alternates=(source.object_directory(),),
            )
            overlay_tree = preview.apply_files(
                source.tree_id(v1_parent),
                {"overlay.txt": b"kept\n"},
                root / "overlay.index",
            )
            raw_parent = parse_raw_commit(source.cat_file("commit", v1_parent))
            rendered_parent = render_raw_commit(
                raw_parent,
                tree=overlay_tree,
                parent=raw_parent.parent,
                message=b"v2 parent\n",
            )
            previous_v2_commit = preview.write_object("commit", rendered_parent.payload)
            entry = {
                "ordered_index": 316,
                "expected_v1_commit": v1_commit,
                "expected_v1_parent": v1_parent,
                "expected_v1_tree": source.tree_id(v1_commit),
                "expected_v1_changed_paths": ["legacy.txt"],
                "expected_v1_delta_sha256": hashlib.sha256(
                    source.raw_transition(v1_parent, v1_commit)
                ).hexdigest(),
                "authorized_v2_delta_paths": ["generated.txt"],
                "tree_transition": "regenerate",
                "message_inputs": {
                    "schema": "adaptation",
                    "subject_body": "regenerate output\n",
                    "classification": "regenerate",
                    "action": "regenerate",
                    "paths": ["generated.txt"],
                    "notes": ["Regenerate from frozen input."],
                    "derivation": "regenerate",
                },
            }

            result = render_regenerated_entry(
                source,
                preview,
                entry,
                previous_v2_commit=previous_v2_commit,
                previous_v2_tree=overlay_tree,
                files={"generated.txt": b"generated\n"},
                index_file=root / "entry.index",
            )

            self.assertEqual(result.actual_changed_paths, ("generated.txt",))
            self.assertEqual(result.inherited_overlay_paths, ("overlay.txt",))
            self.assertNotEqual(result.v1_delta_sha256, result.v2_delta_sha256)
            self.assertEqual(
                preview.cat_file("blob", self._tree_object(preview, result.tree, "overlay.txt")),
                b"kept\n",
            )

    @staticmethod
    def _init_repo(repo: Path) -> None:
        subprocess.run(["git", "init", str(repo)], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(
            ["git", "-C", str(repo), "config", "user.name", "Test"], check=True
        )
        subprocess.run(
            ["git", "-C", str(repo), "config", "user.email", "test@example.test"],
            check=True,
        )

    @staticmethod
    def _commit_all(repo: Path, message: str) -> None:
        subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
        subprocess.run(
            ["git", "-C", str(repo), "commit", "-m", message],
            check=True,
            stdout=subprocess.DEVNULL,
        )

    @staticmethod
    def _rev_parse(repo: Path, revision: str) -> str:
        return subprocess.run(
            ["git", "-C", str(repo), "rev-parse", revision],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()

    @staticmethod
    def _tree_object(repo: GitRepository, tree: str, path: str) -> str:
        record = repo.run("ls-tree", tree, "--", path).decode().strip()
        return record.split()[2]


if __name__ == "__main__":
    unittest.main()
