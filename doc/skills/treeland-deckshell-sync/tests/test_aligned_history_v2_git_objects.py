"""Tests for raw Git object handling in aligned-history v2."""

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
from aligned_history_v2.object_inventory import inventory_loose_objects
from aligned_history_v2.repository import GitRepository
from aligned_history_v2.tree_transition import parse_raw_transition


def raw_commit(*, extra_header: bytes = b"") -> bytes:
    return (
        b"tree " + b"1" * 40 + b"\n"
        b"parent " + b"2" * 40 + b"\n"
        b"author Author <author@example.test> 100 +0800\n"
        b"committer Committer <committer@example.test> 200 -0700\n"
        + extra_header
        + b"\nsubject\n"
    )


class AlignedHistoryV2GitObjectTests(unittest.TestCase):
    def test_raw_commit_rewrite_preserves_identity_headers(self) -> None:
        parsed = parse_raw_commit(raw_commit())

        rendered = render_raw_commit(
            parsed,
            tree="3" * 40,
            parent="4" * 40,
            message=b"new subject\n",
        )

        expected_payload = (
            b"tree " + b"3" * 40 + b"\n"
            b"parent " + b"4" * 40 + b"\n"
            b"author Author <author@example.test> 100 +0800\n"
            b"committer Committer <committer@example.test> 200 -0700\n\n"
            b"new subject\n"
        )
        expected_id = hashlib.sha1(
            f"commit {len(expected_payload)}\0".encode("ascii") + expected_payload
        ).hexdigest()
        self.assertEqual(rendered.payload, expected_payload)
        self.assertEqual(rendered.object_id, expected_id)

    def test_raw_commit_rejects_unapproved_headers(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported commit headers"):
            parse_raw_commit(raw_commit(extra_header=b"encoding UTF-8\n"))

    def test_raw_tree_transition_preserves_modes_objects_and_paths(self) -> None:
        old_object = "5" * 40
        new_object = "6" * 40
        payload = (
            f":100644 100755 {old_object} {new_object} M".encode("ascii")
            + b"\0path with spaces.sh\0"
        )

        changes = parse_raw_transition(payload)

        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].old_mode, "100644")
        self.assertEqual(changes[0].new_mode, "100755")
        self.assertEqual(changes[0].old_object, old_object)
        self.assertEqual(changes[0].new_object, new_object)
        self.assertEqual(changes[0].path, "path with spaces.sh")

    def test_exact_transition_replay_writes_only_to_preview_objects(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "repo"
            subprocess.run(["git", "init", str(repo)], check=True, stdout=subprocess.DEVNULL)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.email", "test@example.test"],
                check=True,
            )
            (repo / "file.txt").write_text("before\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "file.txt"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-m", "before"], check=True, stdout=subprocess.DEVNULL)
            parent = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "HEAD"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            ).stdout.strip()
            (repo / "file.txt").write_text("after\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "commit", "-am", "after"], check=True, stdout=subprocess.DEVNULL)
            commit = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "HEAD"],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            ).stdout.strip()
            original = GitRepository(repo)
            preview_objects = Path(directory) / "preview-objects"
            preview = GitRepository(
                repo,
                object_directory=preview_objects,
                alternates=(original.object_directory(),),
            )

            changes = parse_raw_transition(original.raw_transition(parent, commit))
            tree = preview.replay_transition(
                original.tree_id(parent),
                changes,
                Path(directory) / "preview.index",
            )

            self.assertEqual(tree, original.tree_id(commit))
            self.assertEqual(preview.object_directory(), preview_objects.resolve())
            preview.write_object("blob", b"preview-only\n")
            inventory = inventory_loose_objects(preview_objects)
            self.assertGreaterEqual(inventory["object_count"], 1)
            self.assertIn("blob", inventory["counts_by_type"])
            self.assertTrue(
                all(len(item["payload_sha256"]) == 64 for item in inventory["objects"])
            )


if __name__ == "__main__":
    unittest.main()
