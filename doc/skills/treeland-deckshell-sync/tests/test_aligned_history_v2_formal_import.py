"""Tests for verified preview-object import into the formal object database."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aligned_history_v2.formal_import import (
    create_migration_ref,
    import_verified_objects,
)
from aligned_history_v2.object_inventory import inventory_loose_objects
from aligned_history_v2.repository import GitRepository


class AlignedHistoryV2FormalImportTests(unittest.TestCase):
    def test_import_requires_matching_inventories_and_preserves_object_payload(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo_path = root / "repo"
            subprocess.run(["git", "init", str(repo_path)], check=True, stdout=subprocess.DEVNULL)
            subprocess.run(
                ["git", "-C", str(repo_path), "config", "user.name", "Test"], check=True
            )
            subprocess.run(
                ["git", "-C", str(repo_path), "config", "user.email", "test@example.test"],
                check=True,
            )
            (repo_path / "tracked.txt").write_text("tracked\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo_path), "add", "."], check=True)
            subprocess.run(
                ["git", "-C", str(repo_path), "commit", "-m", "tracked"],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            formal = GitRepository(repo_path)
            first = GitRepository(
                repo_path,
                object_directory=root / "objects-a",
                alternates=(formal.object_directory(),),
            )
            second = GitRepository(
                repo_path,
                object_directory=root / "objects-b",
                alternates=(formal.object_directory(),),
            )
            object_id = first.write_object("blob", b"verified preview payload\n")
            self.assertEqual(
                second.write_object("blob", b"verified preview payload\n"), object_id
            )
            first_inventory = inventory_loose_objects(first.object_directory())
            second_inventory = inventory_loose_objects(second.object_directory())

            result = import_verified_objects(
                formal,
                first.object_directory(),
                second.object_directory(),
                first_inventory,
                second_inventory,
            )

            self.assertEqual(result["imported_object_count"], 1)
            self.assertEqual(formal.cat_file("blob", object_id), b"verified preview payload\n")
            head = formal.run("rev-parse", "HEAD").decode().strip()
            migration_ref = (
                "refs/heads/migration/"
                "commit-aligned-history-corrected-v2-test"
            )
            self.assertEqual(
                create_migration_ref(formal, migration_ref, head), migration_ref
            )
            with self.assertRaisesRegex(ValueError, "already exists"):
                create_migration_ref(formal, migration_ref, head)
            second.write_object("blob", b"unexpected object\n")
            with self.assertRaisesRegex(ValueError, "inventories differ"):
                import_verified_objects(
                    formal,
                    first.object_directory(),
                    second.object_directory(),
                    first_inventory,
                    inventory_loose_objects(second.object_directory()),
                )


if __name__ == "__main__":
    unittest.main()
