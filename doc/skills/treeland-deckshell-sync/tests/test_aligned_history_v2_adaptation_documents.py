"""Tests for v2 SHA-named adaptation documents."""

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

from aligned_history_v2.adaptation_documents import (
    collect_path_evidence,
    render_adaptation_document,
)
from aligned_history_v2.repository import GitRepository


class AlignedHistoryV2AdaptationDocumentTests(unittest.TestCase):
    def test_document_names_the_v2_target_and_excludes_legacy_identity(self) -> None:
        source = "a" * 40
        target = "b" * 40
        entry = {
            "source_commit": source,
            "classification": "mixed",
            "action": "adapted",
            "adaptation_notes": "Use the DeckShell lifecycle.",
            "adaptation_paths": [
                {
                    "kind": "modified",
                    "path": "compositor/src/example.cpp",
                    "justification": "Keep the local lifecycle.",
                }
            ],
        }
        prefix_entry = {
            "v2_target": target,
            "subject": "fix: adapt example",
            "classification": "mixed",
            "action": "adapted",
        }
        path_evidence = {
            "compositor/src/example.cpp": {
                "source_path": "src/example.cpp",
                "source_diff_sha256": "c" * 64,
                "target_diff_sha256": "d" * 64,
            }
        }

        rendered = render_adaptation_document(entry, prefix_entry, path_evidence)

        self.assertIn(f"DeckShell commit: `{target}`", rendered)
        self.assertIn(f"Treeland commit: `{source}`", rendered)
        self.assertIn("Treeland-Tracking-Ref: `refs/remotes/treeland/master`", rendered)
        self.assertNotIn("Legacy-DeckShell", rendered)
        self.assertNotIn("legacy_target", rendered)

    def test_path_evidence_uses_real_source_and_target_commit_diffs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo_path = Path(directory) / "repo"
            subprocess.run(
                ["git", "init", str(repo_path)],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            subprocess.run(
                ["git", "-C", str(repo_path), "config", "user.name", "Test"],
                check=True,
            )
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(repo_path),
                    "config",
                    "user.email",
                    "test@example.test",
                ],
                check=True,
            )
            for path in (
                "source.txt",
                "omitted-source.txt",
                "inherited-source.txt",
                "target.txt",
                "inherited-target.txt",
            ):
                (repo_path / path).write_text("before\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(repo_path), "add", "."], check=True
            )
            subprocess.run(
                ["git", "-C", str(repo_path), "commit", "-m", "base"],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            base = self._rev_parse(repo_path, "HEAD")

            for path in (
                "source.txt",
                "omitted-source.txt",
                "inherited-source.txt",
            ):
                (repo_path / path).write_text("source change\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(repo_path), "commit", "-am", "source"],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            source = self._rev_parse(repo_path, "HEAD")

            subprocess.run(
                ["git", "-C", str(repo_path), "checkout", "--detach", base],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            (repo_path / "target.txt").write_text("target change\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(repo_path), "commit", "-am", "target"],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            target = self._rev_parse(repo_path, "HEAD")

            evidence = collect_path_evidence(
                GitRepository(repo_path),
                {
                    "source_commit": source,
                    "adaptation_paths": [
                        {"kind": "modified", "path": "target.txt"},
                        {
                            "kind": "modified",
                            "path": "inherited-target.txt",
                        },
                        {"kind": "omitted", "path": "omitted-target.txt"},
                    ],
                    "source_changes": [
                        {
                            "new": {
                                "source": "inherited-source.txt",
                                "target": "inherited-target.txt",
                            }
                        },
                        {
                            "new": {"source": "source.txt", "target": "target.txt"}
                        },
                        {
                            "new": {
                                "source": "omitted-source.txt",
                                "target": "omitted-target.txt",
                            }
                        },
                    ],
                },
                {"v2_target": target},
                remediation_paths={"inherited-target.txt"},
            )

            empty_hash = hashlib.sha256(b"").hexdigest()
            self.assertEqual(evidence["target.txt"]["source_path"], "source.txt")
            self.assertNotEqual(evidence["target.txt"]["target_diff_sha256"], empty_hash)
            self.assertEqual(
                evidence["inherited-target.txt"]["target_evidence_kind"],
                "remediation-inherited-post-image",
            )
            self.assertEqual(
                evidence["inherited-target.txt"]["target_diff_sha256"],
                empty_hash,
            )
            self.assertEqual(
                evidence["omitted-target.txt"]["source_path"], "omitted-source.txt"
            )
            self.assertEqual(
                evidence["omitted-target.txt"]["target_diff_sha256"], empty_hash
            )

    @staticmethod
    def _rev_parse(repo: Path, revision: str) -> str:
        return subprocess.run(
            ["git", "-C", str(repo), "rev-parse", revision],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()
