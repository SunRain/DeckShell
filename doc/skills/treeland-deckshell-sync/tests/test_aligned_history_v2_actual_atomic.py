"""Behavior tests for the Git-object-backed v2 atomic verifier."""

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

from aligned_history_v2.actual_atomic import projected_transition_sha256
from aligned_history_v2.product_oracle import (
    EXPECTED_BOUNDED_PATTERNS,
    EXPECTED_EXACT_EXCLUSIONS,
    EXPECTED_PREFIX_EXCLUSIONS,
    OVERLAY_RULES_VERSION,
)
from aligned_history_v2.repository import GitRepository


def _rules() -> dict[str, object]:
    return {
        "version": OVERLAY_RULES_VERSION,
        "policy": "include-by-default-explicit-exclusions-only",
        "exact_exclusions": sorted(EXPECTED_EXACT_EXCLUSIONS),
        "prefix_exclusions": sorted(EXPECTED_PREFIX_EXCLUSIONS),
        "bounded_patterns": [
            {"prefix": prefix, "suffix": suffix}
            for prefix, suffix in sorted(EXPECTED_BOUNDED_PATTERNS)
        ],
        "forbidden_patterns": ["doc/**"],
    }


class AlignedHistoryV2ActualAtomicTests(unittest.TestCase):
    def test_product_transition_projection_ignores_only_approved_overlay(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo_path = Path(directory) / "repo"
            self._init_repo(repo_path)
            product = repo_path / "product.txt"
            excluded = repo_path / "doc/ai/waylibshared_7dc11a_regression_audit.md"
            excluded.parent.mkdir(parents=True)
            product.write_text("before\n", encoding="utf-8")
            excluded.write_text("before\n", encoding="utf-8")
            self._commit_all(repo_path, "base")
            base = self._rev_parse(repo_path, "HEAD")

            product.write_text("after\n", encoding="utf-8")
            excluded.write_text("v1 overlay\n", encoding="utf-8")
            self._commit_all(repo_path, "v1")
            v1 = self._rev_parse(repo_path, "HEAD")

            subprocess.run(
                ["git", "-C", str(repo_path), "checkout", "--detach", base],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            product.write_text("after\n", encoding="utf-8")
            excluded.write_text("v2 overlay\n", encoding="utf-8")
            self._commit_all(repo_path, "v2")
            v2 = self._rev_parse(repo_path, "HEAD")
            repo = GitRepository(repo_path)

            self.assertNotEqual(repo.raw_transition(base, v1), repo.raw_transition(base, v2))
            self.assertEqual(
                projected_transition_sha256(repo, base, v1, _rules()),
                projected_transition_sha256(repo, base, v2, _rules()),
            )

            product.write_text("tampered\n", encoding="utf-8")
            self._commit_all(repo_path, "tampered")
            tampered = self._rev_parse(repo_path, "HEAD")
            self.assertNotEqual(
                projected_transition_sha256(repo, base, v1, _rules()),
                projected_transition_sha256(repo, v2, tampered, _rules()),
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


if __name__ == "__main__":
    unittest.main()
