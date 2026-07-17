from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from sync_audit_lib.manifest import build_candidate_manifest, finalize_manifest
from sync_audit_lib.traces import build_trace_audit


class ManifestTests(unittest.TestCase):
    def test_candidate_generation_never_auto_approves_semantic_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture = self._fixture(Path(temp_dir))
            candidate = build_candidate_manifest(**fixture)

        self.assertEqual(candidate["counts"]["total"], 2)
        adapted = candidate["entries"][1]
        self.assertEqual(adapted["action"], "adapted")
        self.assertTrue(adapted["adaptation_candidates"])
        self.assertTrue(
            all(item["review_state"] == "candidate" for item in adapted["adaptation_candidates"])
        )
        self.assertNotIn("adaptation_paths", adapted)

    def test_finalization_requires_review_for_every_adapted_commit(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture = self._fixture(Path(temp_dir))
            candidate = build_candidate_manifest(**fixture)

            with self.assertRaisesRegex(ValueError, "missing adapted review"):
                finalize_manifest(candidate, {"schema_version": 2, "entries": []})

    def test_finalization_builds_canonical_approved_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture = self._fixture(Path(temp_dir))
            candidate = build_candidate_manifest(**fixture)
            adapted_source = candidate["entries"][1]["source_commit"]
            reviews = {
                "schema_version": 2,
                "entries": [
                    {
                        "source_commit": adapted_source,
                        "adaptation_paths": [
                            {"kind": "materialized", "path": "compositor/src/new.txt"},
                            {"kind": "omitted", "path": "compositor/src/omitted.txt"},
                        ],
                        "adaptation_notes": "materialized the local target and omitted the absent file",
                        "reviewed_by": "fixture-reviewer",
                        "reviewed_at": "2026-07-16T00:00:00Z",
                    }
                ],
            }
            manifest = finalize_manifest(candidate, reviews)

        self.assertEqual(manifest["counts"], {"total": 2, "applied": 1, "adapted": 1, "empty": 0})
        self.assertEqual(manifest["entries"][0]["adaptation_paths"], [])
        self.assertEqual(manifest["entries"][0]["adaptation_notes"], "none")
        paths = manifest["entries"][1]["adaptation_paths"]
        self.assertEqual([item["kind"] for item in paths], ["omitted", "materialized"])
        self.assertTrue(all(item["review_state"] == "approved" for item in paths))
        self.assertTrue(all(item["proof"] for item in paths))

    def test_delta_equivalent_path_requires_persistent_contract_justification(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture = self._fixture(Path(temp_dir))
            candidate = build_candidate_manifest(**fixture)
            adapted = candidate["entries"][1]
            observation = next(
                item
                for item in adapted["path_observations"]
                if item["target_status"] != "omitted"
            )
            observation["delta_equivalent"] = True
            adapted["adaptation_candidates"] = []
            base_review = {
                "source_commit": adapted["source_commit"],
                "adaptation_paths": [
                    {"kind": "modified", "path": observation["path"]}
                ],
                "adaptation_notes": "preserved the local public contract",
                "reviewed_by": "fixture-reviewer",
                "reviewed_at": "2026-07-16T00:00:00Z",
            }

            with self.assertRaisesRegex(ValueError, "persistent-contract"):
                finalize_manifest(candidate, {"schema_version": 2, "entries": [base_review]})

            base_review["adaptation_paths"][0].update(
                {
                    "review_basis": "persistent-contract",
                    "justification": "The target file keeps the DeckShell project identity as a documented public build contract.",
                }
            )
            manifest = finalize_manifest(
                candidate,
                {"schema_version": 2, "entries": [base_review]},
            )

        path = manifest["entries"][1]["adaptation_paths"][0]
        self.assertEqual(path["review_basis"], "persistent-contract")
        self.assertTrue(path["justification"])

    def _fixture(self, root: Path) -> dict[str, object]:
        repo = root / "repo"
        repo.mkdir()
        self._git(repo, "init")
        self._git(repo, "config", "user.name", "Manifest Fixture")
        self._git(repo, "config", "user.email", "manifest@example.invalid")
        self._write(repo, "compositor/src/base.txt", "base\n")
        self._write(repo, "compositor/src/omitted.txt", "legacy\n")
        self._commit_all(repo, "base")

        applied_source = "1" * 40
        self._write(repo, "compositor/src/base.txt", "applied\n")
        self._commit_sync(repo, "applied", applied_source)
        applied_target = self._git(repo, "rev-parse", "HEAD").strip()

        adapted_source = "2" * 40
        self._write(repo, "compositor/src/new.txt", "materialized\n")
        self._commit_sync(repo, "adapted", adapted_source)
        adapted_target = self._git(repo, "rev-parse", "HEAD").strip()
        inventory = {
            "range_base": "0" * 40,
            "range_head": "f" * 40,
            "approved_review": [],
            "commits": [
                {
                    "source_commit": applied_source,
                    "classification": "other",
                    "target_paths": ["compositor/src/base.txt"],
                    "changes": [
                        {
                            "status": "M",
                            "old": None,
                            "new": {"source": "src/base.txt", "target": "compositor/src/base.txt"},
                        }
                    ],
                },
                {
                    "source_commit": adapted_source,
                    "classification": "other",
                    "target_paths": ["compositor/src/new.txt", "compositor/src/omitted.txt"],
                    "changes": [
                        {
                            "status": "M",
                            "old": None,
                            "new": {"source": "src/new.txt", "target": "compositor/src/new.txt"},
                        },
                        {
                            "status": "D",
                            "old": {"source": "src/omitted.txt", "target": "compositor/src/omitted.txt"},
                            "new": None,
                        },
                    ],
                },
            ],
        }
        traces = build_trace_audit(repo, "HEAD", inventory)
        evidence_root = root / "evidence"
        legacy_evidence = self._legacy_evidence(
            evidence_root,
            applied_source,
            applied_target,
            adapted_source,
            adapted_target,
        )
        return {
            "repo": repo,
            "inventory": inventory,
            "traces": traces,
            "legacy_evidence": legacy_evidence,
            "evidence_root": evidence_root,
            "migration_id": "fixture-migration",
        }

    def _legacy_evidence(
        self,
        root: Path,
        applied_source: str,
        applied_target: str,
        adapted_source: str,
        adapted_target: str,
    ) -> dict[str, object]:
        adapted_dir = root / "source" / "adapted" / adapted_source
        adapted_dir.mkdir(parents=True)
        artifacts = {}
        for name in ("filtered.patch", "staged.diff", "commit.diff", "path-audit.txt", "difference-report.md"):
            path = adapted_dir / name
            path.write_text(f"{name}\n", encoding="utf-8")
            artifacts[name] = str(Path("/tmp") / adapted_source / name)
        return {
            "entries": [
                {
                    "source_commit": applied_source,
                    "target_commit": applied_target,
                    "action": "applied",
                },
                {
                    "source_commit": adapted_source,
                    "target_commit": adapted_target,
                    "action": "adapted",
                    "adaptation_notes": "legacy adapted note",
                    "mapped_patch": artifacts["filtered.patch"],
                    "staged_diff": artifacts["staged.diff"],
                    "commit_diff": artifacts["commit.diff"],
                    "path_audit": artifacts["path-audit.txt"],
                    "difference_report": artifacts["difference-report.md"],
                },
            ]
        }

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

    @classmethod
    def _commit_sync(cls, repo: Path, action: str, source: str) -> None:
        cls._git(repo, "add", "-A")
        cls._git(
            repo,
            "commit",
            "-m",
            action,
            "-m",
            f"[treeland-sync] action: {action}\nTreeland-Commit: {source}",
        )


if __name__ == "__main__":
    unittest.main()
