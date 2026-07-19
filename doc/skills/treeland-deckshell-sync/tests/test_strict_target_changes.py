from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from sync_audit_lib.common import parse_name_status_z
from sync_audit_lib.target import canonicalize_changes


SKILL_DIR = Path(__file__).parents[1]
SCRIPT_PATH = SKILL_DIR / "scripts" / "sync_audit.py"
POLICY_PATH = SKILL_DIR / "references" / "path-policy.md"
SPEC = importlib.util.spec_from_file_location("sync_audit_strict_changes", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"无法加载审计脚本: {SCRIPT_PATH}")

sync_audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync_audit
SPEC.loader.exec_module(sync_audit)


class StrictTargetChangeTests(unittest.TestCase):
    def test_rename_copy_and_delete_use_canonical_path_and_status(self) -> None:
        cases = {
            "rename": ("compositor/src/renamed.txt", "R", False),
            "delete": ("compositor/src/original.txt", "D", True),
        }
        for operation, expected in cases.items():
            with self.subTest(operation=operation):
                with tempfile.TemporaryDirectory() as temp_dir:
                    result = self._verify_case(Path(temp_dir), operation, *expected)

                self.assertEqual(result["outcome"], "pass", result["findings"])

    def test_copy_status_uses_new_canonical_path(self) -> None:
        changes = parse_name_status_z(
            b"C100\0compositor/src/original.txt\0compositor/src/copied.txt\0"
        )

        result = canonicalize_changes(changes)

        self.assertEqual(result["all_paths"], [
            "compositor/src/original.txt",
            "compositor/src/copied.txt",
        ])
        self.assertEqual(result["canonical_changes"], [
            {
                "status": "C100",
                "path": "compositor/src/copied.txt",
                "old_path": "compositor/src/original.txt",
                "new_path": "compositor/src/copied.txt",
            }
        ])

    def _verify_case(
        self,
        root: Path,
        operation: str,
        canonical_path: str,
        target_status: str,
        parent_exists: bool,
    ) -> dict[str, object]:
        repo = root / "repo"
        repo.mkdir()
        self._git(repo, "init")
        self._git(repo, "config", "user.name", "Audit Fixture")
        self._git(repo, "config", "user.email", "audit@example.invalid")
        original = "compositor/src/original.txt"
        self._write(repo, original, "stable copy source\n")
        self._commit_all(repo, "base")
        self._apply_operation(repo, operation, original, canonical_path)

        source = {"rename": "a", "delete": "c"}[operation] * 40
        message = "\n".join(
            [
                "[treeland-sync] action: adapted",
                "[treeland-sync] adaptation paths:",
                f"- modified: {canonical_path}",
                "[treeland-sync] adaptation notes:",
                f"- canonical {operation} adaptation",
                f"Treeland-Commit: {source}",
            ]
        )
        if operation == "copy":
            self._git(repo, "add", canonical_path)
        self._git(repo, "commit", "-m", "canonical change", "-m", message)

        expected_paths = [canonical_path]
        if operation == "rename":
            expected_paths.insert(0, original)
        inventory = {
            "approved_review": [],
            "commits": [
                {
                    "source_commit": source,
                    "classification": "other",
                    "target_paths": expected_paths,
                }
            ],
        }
        traces = sync_audit.build_trace_audit(repo, "HEAD", inventory)
        artifact_root, artifacts = self._artifacts(root)
        evidence = {
            "schema_version": 2,
            "entries": [
                {
                    "source_commit": source,
                    "target_commit": traces["mappings"][0]["target_commit"],
                    "action": "adapted",
                    "adaptation_paths": [
                        {
                            "kind": "modified",
                            "path": canonical_path,
                            "target_status": target_status,
                            "source_status": target_status,
                            "parent_exists": parent_exists,
                            "proof": [artifacts["difference_report"]],
                            "review_state": "approved",
                        }
                    ],
                    "adaptation_notes": f"canonical {operation} adaptation",
                    **artifacts,
                }
            ],
        }
        return sync_audit.verify_sync(
            repo,
            sync_audit.load_policy(POLICY_PATH),
            inventory,
            traces,
            evidence,
            required_evidence_schema=2,
            evidence_root=artifact_root,
        )

    @classmethod
    def _apply_operation(
        cls, repo: Path, operation: str, original: str, canonical: str
    ) -> None:
        if operation == "rename":
            cls._git(repo, "mv", original, canonical)
        elif operation == "copy":
            cls._write(repo, original, "updated copy source\n")
            cls._write(repo, canonical, "updated copy source\n")
        else:
            cls._git(repo, "rm", original)

    @staticmethod
    def _artifacts(root: Path) -> tuple[Path, dict[str, dict[str, object]]]:
        artifact_root = root / "evidence"
        artifact_root.mkdir()
        artifacts = {}
        for name in (
            "mapped_patch",
            "staged_diff",
            "commit_diff",
            "path_audit",
            "difference_report",
        ):
            path = artifact_root / f"{name}.txt"
            path.write_text(f"{name}\n", encoding="utf-8")
            artifacts[name] = {
                "path": path.name,
                "size": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        return artifact_root, artifacts

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


if __name__ == "__main__":
    unittest.main()
