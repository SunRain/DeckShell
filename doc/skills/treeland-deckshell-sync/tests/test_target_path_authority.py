from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).parents[1]
SCRIPT_PATH = SKILL_DIR / "scripts" / "sync_audit.py"
POLICY_PATH = SKILL_DIR / "references" / "path-policy.md"
SPEC = importlib.util.spec_from_file_location("sync_audit_target_authority", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"无法加载审计脚本: {SCRIPT_PATH}")

sync_audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync_audit
SPEC.loader.exec_module(sync_audit)


class TargetPathAuthorityTests(unittest.TestCase):
    source = "d" * 40
    canonical_path = "compositor/src/feature.cpp"
    sibling_path = "compositor/src/feature_devices.cpp"
    local_helper_path = "compositor/src/local_helper.cpp"

    def test_blocks_adapted_target_path_expansion(self) -> None:
        paths = [
            {"kind": "modified", "path": self.canonical_path},
            {"kind": "modified", "path": self.sibling_path},
        ]
        result = self._verify_case(
            {
                self.canonical_path: "canonical base\n",
                self.sibling_path: "split base\n",
            },
            {
                self.canonical_path: "canonical adapted\n",
                self.sibling_path: "split adapted\n",
            },
            paths,
        )

        self.assertEqual(result["outcome"], "blocked")
        self.assertEqual(result["target_path_authority"], "blocked")
        expansions = result["target_path_expansions"]
        self.assertEqual(
            [
                {"source_commit": item["source_commit"], "path": item["path"]}
                for item in expansions
            ],
            [
                {
                    "source_commit": self.source,
                    "path": self.sibling_path,
                }
            ],
        )
        self.assertEqual(len(expansions[0]["target_commit"]), 40)
        self.assertIn(
            f"target-path-expansion for {self.source}: {self.sibling_path}",
            result["findings"],
        )
        self.assertIn(
            "adaptation path is outside inventory target paths: "
            f"{self.source}: {self.sibling_path}",
            result["findings"],
        )

    def test_allows_materializing_the_canonical_target_path(self) -> None:
        paths = [{"kind": "materialized", "path": self.canonical_path}]

        result = self._verify_case(
            {self.local_helper_path: "local helper\n"},
            {self.canonical_path: "materialized upstream implementation\n"},
            paths,
        )

        self.assertEqual(result["outcome"], "pass", result["findings"])
        self.assertEqual(result["target_path_authority"], "pass")
        self.assertEqual(result["target_path_expansions"], [])

    def test_blocks_evidence_path_self_authorization(self) -> None:
        paths = [
            {"kind": "omitted", "path": self.sibling_path},
            {"kind": "modified", "path": self.canonical_path},
        ]

        result = self._verify_case(
            {self.canonical_path: "canonical base\n"},
            {self.canonical_path: "canonical adapted\n"},
            paths,
        )

        self.assertEqual(result["outcome"], "blocked")
        self.assertEqual(result["target_path_authority"], "blocked")
        self.assertEqual(result["target_path_expansions"], [])
        self.assertIn(
            "adaptation path is outside inventory target paths: "
            f"{self.source}: {self.sibling_path}",
            result["findings"],
        )

    def test_ignores_untouched_local_only_files(self) -> None:
        paths = [{"kind": "modified", "path": self.canonical_path}]

        result = self._verify_case(
            {
                self.canonical_path: "canonical base\n",
                self.local_helper_path: "local helper\n",
            },
            {self.canonical_path: "canonical adapted\n"},
            paths,
        )

        self.assertEqual(result["outcome"], "pass", result["findings"])
        self.assertEqual(result["target_path_authority"], "pass")
        self.assertEqual(result["target_path_expansions"], [])

    def test_reports_expansion_when_evidence_entry_is_missing(self) -> None:
        paths = [{"kind": "modified", "path": self.canonical_path}]

        result = self._verify_case(
            {
                self.canonical_path: "canonical base\n",
                self.sibling_path: "split base\n",
            },
            {
                self.canonical_path: "canonical adapted\n",
                self.sibling_path: "split adapted\n",
            },
            paths,
            include_evidence=False,
        )

        self.assertEqual(result["outcome"], "blocked")
        self.assertEqual(result["target_path_authority"], "blocked")
        self.assertEqual(
            [item["path"] for item in result["target_path_expansions"]],
            [self.sibling_path],
        )

    def _verify_case(
        self,
        parent_files: dict[str, str],
        changed_files: dict[str, str],
        adaptation_paths: list[dict[str, str]],
        *,
        include_evidence: bool = True,
    ) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / "repo"
            repo.mkdir()
            self._init_repo(repo)
            for path, content in parent_files.items():
                self._write(repo, path, content)
            self._commit_all(repo, "base")

            for path, content in changed_files.items():
                self._write(repo, path, content)
            self._git(repo, "add", "-A")
            self._git(
                repo,
                "commit",
                "-m",
                "adapted feature",
                "-m",
                self._message(adaptation_paths),
            )

            inventory = self._inventory()
            traces = sync_audit.build_trace_audit(repo, "HEAD", inventory)
            evidence = self._evidence(root, traces, adaptation_paths)
            if not include_evidence:
                evidence["entries"] = []
            return sync_audit.verify_sync(
                repo,
                sync_audit.load_policy(POLICY_PATH),
                inventory,
                traces,
                evidence,
            )

    def _message(self, adaptation_paths: list[dict[str, str]]) -> str:
        path_lines = [f"- {item['kind']}: {item['path']}" for item in adaptation_paths]
        return "\n".join(
            [
                "[treeland-sync] action: adapted",
                "[treeland-sync] adaptation paths:",
                *path_lines,
                "[treeland-sync] adaptation notes:",
                "- target API adaptation",
                f"Treeland-Commit: {self.source}",
            ]
        )

    def _inventory(self) -> dict[str, object]:
        return {
            "approved_review": [],
            "commits": [
                {
                    "source_commit": self.source,
                    "classification": "other",
                    "target_paths": [self.canonical_path],
                }
            ],
        }

    def _evidence(
        self,
        root: Path,
        traces: dict[str, object],
        adaptation_paths: list[dict[str, str]],
    ) -> dict[str, object]:
        artifacts = {}
        for name in (
            "mapped_patch",
            "staged_diff",
            "commit_diff",
            "path_audit",
            "difference_report",
        ):
            path = root / f"{name}.txt"
            path.write_text(f"{name}\n", encoding="utf-8")
            artifacts[name] = str(path)
        mappings = traces["mappings"]
        assert isinstance(mappings, list)
        return {
            "schema_version": 2,
            "entries": [
                {
                    "source_commit": self.source,
                    "target_commit": mappings[0]["target_commit"],
                    "action": "adapted",
                    "adaptation_paths": adaptation_paths,
                    "adaptation_notes": "target API adaptation",
                    **artifacts,
                }
            ],
        }

    @classmethod
    def _init_repo(cls, repo: Path) -> None:
        cls._git(repo, "init")
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
