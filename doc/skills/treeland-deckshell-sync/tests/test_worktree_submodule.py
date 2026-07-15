from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


class WorktreeSubmoduleTests(unittest.TestCase):
    def test_linked_worktree_requires_explicit_submodule_initialization(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dependency = root / "dependency"
            super_repo = root / "super"
            linked = root / "linked"

            self._git_init(dependency)
            (dependency / "payload.txt").write_text("dependency\n", encoding="utf-8")
            self._git(dependency, "add", "payload.txt")
            self._git(dependency, "commit", "-m", "dependency")

            self._git_init(super_repo)
            self._git(
                super_repo,
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "add",
                str(dependency),
                "thirdparty/dependency",
            )
            self._git(super_repo, "commit", "-m", "add submodule")
            self._git(super_repo, "worktree", "add", "--detach", str(linked), "HEAD")

            payload = linked / "thirdparty/dependency/payload.txt"
            self.assertFalse(payload.exists())

            self._git(
                linked,
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "update",
                "--init",
                "--recursive",
            )
            self.assertEqual(payload.read_text(encoding="utf-8"), "dependency\n")

    @classmethod
    def _git_init(cls, repo: Path) -> None:
        cls._git(repo.parent, "init", str(repo))
        cls._git(repo, "config", "user.name", "Audit Fixture")
        cls._git(repo, "config", "user.email", "audit@example.invalid")

    @staticmethod
    def _git(repo: Path, *args: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return completed.stdout


if __name__ == "__main__":
    unittest.main()
