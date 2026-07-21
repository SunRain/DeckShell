"""Tests for product-tree equivalence outside approved v2 overlays."""

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

from aligned_history_v2.repository import GitRepository
from aligned_history_v2.tree_manifest import build_product_manifest


class AlignedHistoryV2TreeManifestTests(unittest.TestCase):
    def test_manifest_ignores_only_approved_overlay_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "repo"
            subprocess.run(["git", "init", str(repo)], check=True, stdout=subprocess.DEVNULL)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.email", "test@example.test"],
                check=True,
            )
            (repo / "product.txt").write_text("stable\n", encoding="utf-8")
            (repo / "doc").mkdir()
            (repo / "doc" / "overlay.md").write_text("v1\n", encoding="utf-8")
            self._commit(repo, "v1")
            first = self._rev_parse(repo, "HEAD^{tree}")
            (repo / "doc" / "overlay.md").write_text("v2\n", encoding="utf-8")
            self._commit(repo, "overlay")
            second = self._rev_parse(repo, "HEAD^{tree}")
            git = GitRepository(repo)

            first_manifest = build_product_manifest(git, first, ("doc/",))
            second_manifest = build_product_manifest(git, second, ("doc/",))

            self.assertEqual(first_manifest, second_manifest)
            (repo / "product.txt").write_text("drift\n", encoding="utf-8")
            self._commit(repo, "product drift")
            third = self._rev_parse(repo, "HEAD^{tree}")
            self.assertNotEqual(
                first_manifest,
                build_product_manifest(git, third, ("doc/",)),
            )

    @staticmethod
    def _commit(repo: Path, message: str) -> None:
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


if __name__ == "__main__":
    unittest.main()
