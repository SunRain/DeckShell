from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "sync_audit.py"
POLICY_PATH = Path(__file__).parents[1] / "references" / "path-policy.md"
SPEC = importlib.util.spec_from_file_location("sync_audit", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"无法加载审计脚本: {SCRIPT_PATH}")

sync_audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync_audit
SPEC.loader.exec_module(sync_audit)


class InventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = sync_audit.load_policy(POLICY_PATH)

    def test_cross_policy_rename_keeps_only_the_allowed_side(self) -> None:
        changes = sync_audit.parse_name_status_z(
            b"R100\0waylib/item.txt\0src/item.txt\0"
        )

        entry = sync_audit.summarize_commit(
            "a" * 40,
            "move implementation into compositor",
            changes,
            self.policy,
            set(),
        )

        self.assertEqual(entry["classification"], "mixed")
        self.assertEqual(entry["drop_paths"], ["waylib/item.txt"])
        self.assertEqual(entry["mapped_source_paths"], ["src/item.txt"])
        self.assertEqual(entry["root_source_paths"], [])
        self.assertEqual(entry["target_paths"], ["compositor/src/item.txt"])
        self.assertEqual(entry["changes"][0]["status"], "R100")
        self.assertEqual(entry["blocked_reasons"], [])

    def test_review_only_path_requires_explicit_policy_key_approval(self) -> None:
        changes = sync_audit.parse_name_status_z(b"M\0.github/workflows/ci.yml\0")

        blocked = sync_audit.summarize_commit(
            "b" * 40, "update CI", changes, self.policy, set()
        )
        approved = sync_audit.summarize_commit(
            "b" * 40, "update CI", changes, self.policy, {".github"}
        )

        self.assertEqual(blocked["classification"], "blocked")
        self.assertIn("--approve-review .github", blocked["blocked_reasons"][0])
        self.assertEqual(approved["classification"], "other")
        self.assertEqual(approved["target_paths"], [".github/workflows/ci.yml"])

    def test_builds_ordered_inventory_and_counts_commit_classes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            self._git(repo, "init")
            self._git(repo, "config", "user.name", "Audit Fixture")
            self._git(repo, "config", "user.email", "audit@example.invalid")
            self._write(repo, "src/base.txt", "base\n")
            self._write(repo, "waylib/base.txt", "base\n")
            self._commit_all(repo, "base")
            base = self._git(repo, "rev-parse", "HEAD").strip()

            self._write(repo, "waylib/base.txt", "dependency\n")
            self._commit_all(repo, "dependency only")
            dependency_sha = self._git(repo, "rev-parse", "HEAD").strip()

            self._write(repo, "waylib/base.txt", "mixed dependency\n")
            self._write(repo, "src/feature.txt", "feature\n")
            self._commit_all(repo, "mixed")
            mixed_sha = self._git(repo, "rev-parse", "HEAD").strip()

            self._write(repo, "protocols/feature.xml", "<protocol/>\n")
            self._commit_all(repo, "other")
            head = self._git(repo, "rev-parse", "HEAD").strip()

            inventory = sync_audit.build_inventory(repo, base, head, self.policy, set())

        self.assertEqual(
            inventory["ordered_source_commits"], [dependency_sha, mixed_sha, head]
        )
        self.assertEqual(
            inventory["counts"],
            {"total": 3, "dependency-only": 1, "mixed": 1, "other": 1},
        )
        self.assertEqual(inventory["outcome"], "pass")
        self.assertEqual(len(inventory["ordered_sha256"]), 64)

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

    @staticmethod
    def _write(repo: Path, relative: str, content: str) -> None:
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    @classmethod
    def _commit_all(cls, repo: Path, message: str) -> None:
        cls._git(repo, "add", "-A")
        cls._git(repo, "commit", "-m", message)


class TraceAuditTests(unittest.TestCase):
    def test_prefers_treeland_trailer_and_filters_intermediate_history(self) -> None:
        source_one = "1" * 40
        source_two = "2" * 40
        intermediate = "f" * 40
        inventory = {
            "commits": [
                {"source_commit": source_one, "classification": "other"},
                {"source_commit": source_two, "classification": "mixed"},
            ]
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            InventoryTests._git(repo, "init")
            InventoryTests._git(repo, "config", "user.name", "Audit Fixture")
            InventoryTests._git(repo, "config", "user.email", "audit@example.invalid")
            InventoryTests._write(repo, "file.txt", "base\n")
            InventoryTests._commit_all(repo, "base")

            InventoryTests._write(repo, "file.txt", "legacy\n")
            InventoryTests._git(repo, "add", "file.txt")
            InventoryTests._git(
                repo,
                "commit",
                "-m",
                "legacy mapping",
                "-m",
                f"(cherry picked from {source_one})\n\n"
                f"(cherry picked from commit {intermediate})",
            )

            InventoryTests._write(repo, "file.txt", "new\n")
            InventoryTests._git(repo, "add", "file.txt")
            InventoryTests._git(
                repo,
                "commit",
                "-m",
                "new mapping",
                "-m",
                f"(cherry picked from commit {source_two})\n\n"
                f"Treeland-Commit: {source_two}",
            )

            audit = sync_audit.build_trace_audit(repo, "HEAD", inventory)

        self.assertEqual(audit["state"], "already-synced")
        self.assertEqual(
            [item["source_commit"] for item in audit["mappings"]],
            [source_one, source_two],
        )
        self.assertEqual([item["trace"] for item in audit["mappings"]], ["legacy", "new"])
        self.assertEqual(audit["blocked_reasons"], [])


class VerifyTests(unittest.TestCase):
    def test_accepts_fully_traced_applied_commit_with_saved_artifacts(self) -> None:
        source = "3" * 40
        policy = sync_audit.load_policy(POLICY_PATH)
        inventory = {
            "approved_review": [],
            "commits": [
                {
                    "source_commit": source,
                    "classification": "other",
                    "target_paths": ["compositor/src/feature.txt"],
                }
            ],
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "repo"
            repo.mkdir()
            InventoryTests._git(repo, "init")
            InventoryTests._git(repo, "config", "user.name", "Audit Fixture")
            InventoryTests._git(repo, "config", "user.email", "audit@example.invalid")
            InventoryTests._write(repo, "base.txt", "base\n")
            InventoryTests._commit_all(repo, "base")
            InventoryTests._write(repo, "compositor/src/feature.txt", "feature\n")
            InventoryTests._git(repo, "add", "compositor/src/feature.txt")
            InventoryTests._git(
                repo,
                "commit",
                "-m",
                "mapped feature",
                "-m",
                f"Treeland-Commit: {source}",
            )

            traces = sync_audit.build_trace_audit(repo, "HEAD", inventory)
            artifact_paths = self._write_evidence_artifacts(root)
            evidence = {
                "entries": [
                    {
                        "source_commit": source,
                        "target_commit": traces["mappings"][0]["target_commit"],
                        "action": "applied",
                        **artifact_paths,
                    }
                ]
            }

            result = sync_audit.verify_sync(repo, policy, inventory, traces, evidence)

        self.assertEqual(result["outcome"], "pass")
        self.assertEqual(result["findings"], [])

    def test_blocks_adapted_commit_without_difference_evidence(self) -> None:
        source = "4" * 40
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "repo"
            repo.mkdir()
            InventoryTests._git(repo, "init")
            InventoryTests._git(repo, "config", "user.name", "Audit Fixture")
            InventoryTests._git(repo, "config", "user.email", "audit@example.invalid")
            InventoryTests._write(repo, "base.txt", "base\n")
            InventoryTests._commit_all(repo, "base")
            InventoryTests._write(repo, "compositor/src/feature.txt", "adapted\n")
            InventoryTests._git(repo, "add", "compositor/src/feature.txt")
            InventoryTests._git(
                repo,
                "commit",
                "-m",
                "adapted feature",
                "-m",
                f"Treeland-Commit: {source}",
            )
            inventory = {
                "approved_review": [],
                "commits": [
                    {
                        "source_commit": source,
                        "classification": "other",
                        "target_paths": ["compositor/src/feature.txt"],
                    }
                ],
            }
            traces = sync_audit.build_trace_audit(repo, "HEAD", inventory)
            artifact_paths = self._write_evidence_artifacts(root)
            evidence = {
                "entries": [
                    {
                        "source_commit": source,
                        "target_commit": traces["mappings"][0]["target_commit"],
                        "action": "adapted",
                        "adaptation_notes": "target API adaptation",
                        **artifact_paths,
                    }
                ]
            }

            result = sync_audit.verify_sync(
                repo,
                sync_audit.load_policy(POLICY_PATH),
                inventory,
                traces,
                evidence,
            )

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("difference_report" in finding for finding in result["findings"])
        )

    @staticmethod
    def _write_evidence_artifacts(root: Path) -> dict[str, str]:
        artifacts = {}
        for name in ("mapped_patch", "staged_diff", "commit_diff", "path_audit"):
            artifact = root / f"{name}.txt"
            artifact.write_text(f"{name}\n", encoding="utf-8")
            artifacts[name] = str(artifact)
        return artifacts


if __name__ == "__main__":
    unittest.main()
