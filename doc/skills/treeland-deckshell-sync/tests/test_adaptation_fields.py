from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).parents[1]
SCRIPT_PATH = SKILL_DIR / "scripts" / "sync_audit.py"
POLICY_PATH = SKILL_DIR / "references" / "path-policy.md"
SPEC = importlib.util.spec_from_file_location("sync_audit_adaptation", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"无法加载审计脚本: {SCRIPT_PATH}")

sync_audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync_audit
SPEC.loader.exec_module(sync_audit)


class AdaptationFieldTests(unittest.TestCase):
    source = "a" * 40

    def test_schema_v1_adapted_evidence_remains_compatible(self) -> None:
        with self._fixture(schema_version=None, include_sync_fields=False) as fixture:
            result = self._verify(fixture)

        self.assertEqual(result["outcome"], "pass")
        self.assertEqual(result["findings"], [])

    def test_schema_v2_accepts_matching_structured_adaptation_fields(self) -> None:
        with self._fixture() as fixture:
            result = self._verify(fixture)

        self.assertEqual(result["outcome"], "pass")
        self.assertEqual(result["findings"], [])

    def test_strict_mode_rejects_missing_or_v1_evidence_schema(self) -> None:
        for schema_version in (None, 1):
            with self.subTest(schema_version=schema_version):
                with self._fixture(
                    schema_version=schema_version,
                    include_sync_fields=False,
                ) as fixture:
                    result = sync_audit.verify_sync(
                        fixture["repo"],
                        sync_audit.load_policy(POLICY_PATH),
                        fixture["inventory"],
                        fixture["traces"],
                        fixture["evidence"],
                        required_evidence_schema=2,
                    )

                self.assertFinding(result, "strict evidence schema 2 required")
                self.assertEqual(result["report_schema_version"], 2)
                self.assertEqual(result["evidence_schema_version"], schema_version or 1)
                self.assertEqual(result["strict_evidence_schema_required"], 2)

    def test_strict_mode_validates_relative_artifact_metadata(self) -> None:
        cases = {
            "size mismatch": {"size": 999},
            "sha256 mismatch": {"sha256": "0" * 64},
            "path escapes evidence root": {"path": "../outside.txt"},
        }
        for expected, override in cases.items():
            with self.subTest(expected=expected):
                with self._fixture(strict_artifacts=True) as fixture:
                    fixture["evidence"]["entries"][0]["mapped_patch"].update(override)
                    result = sync_audit.verify_sync(
                        fixture["repo"],
                        sync_audit.load_policy(POLICY_PATH),
                        fixture["inventory"],
                        fixture["traces"],
                        fixture["evidence"],
                        required_evidence_schema=2,
                        evidence_root=fixture["evidence_root"],
                    )

                self.assertFinding(result, expected)

    def test_strict_mode_rejects_symlink_artifact(self) -> None:
        with self._fixture(strict_artifacts=True) as fixture:
            artifact_root = fixture["evidence_root"]
            target = artifact_root / "mapped_patch.txt"
            link = artifact_root / "mapped_patch-link.txt"
            link.symlink_to(target.name)
            record = fixture["evidence"]["entries"][0]["mapped_patch"]
            record["path"] = link.name
            result = sync_audit.verify_sync(
                fixture["repo"],
                sync_audit.load_policy(POLICY_PATH),
                fixture["inventory"],
                fixture["traces"],
                fixture["evidence"],
                required_evidence_schema=2,
                evidence_root=artifact_root,
            )

        self.assertFinding(result, "artifact must be a regular file")

    def test_strict_mode_accepts_complete_path_review_metadata(self) -> None:
        with self._fixture(
            strict_artifacts=True,
            strict_path_metadata=True,
        ) as fixture:
            result = self._strict_verify(fixture)

        self.assertEqual(result["outcome"], "pass")
        self.assertEqual(result["findings"], [])

    def test_strict_mode_requires_proof_and_approved_review(self) -> None:
        with self._fixture(
            strict_artifacts=True,
            strict_path_metadata=True,
        ) as fixture:
            path = fixture["evidence"]["entries"][0]["adaptation_paths"][0]
            path["proof"] = []
            path["review_state"] = "candidate"
            result = self._strict_verify(fixture)

        self.assertFinding(result, "missing proof")
        self.assertFinding(result, "review_state is not approved")

    def test_strict_mode_rejects_materialized_existing_parent_and_non_add(self) -> None:
        paths = [{"kind": "materialized", "path": "compositor/src/feature.txt"}]
        with self._fixture(
            adaptation_paths=paths,
            strict_artifacts=True,
            strict_path_metadata=True,
        ) as fixture:
            result = self._strict_verify(fixture)

        self.assertFinding(result, "materialized target status is not A")
        self.assertFinding(result, "materialized parent path exists")

    def test_strict_mode_rejects_noncanonical_adaptation_path_order(self) -> None:
        paths = [
            {"kind": "modified", "path": "compositor/src/feature.txt"},
            {"kind": "omitted", "path": "compositor/src/omitted.txt"},
            {"kind": "materialized", "path": "compositor/src/new.txt"},
        ]
        with self._fixture(
            adaptation_paths=paths,
            strict_artifacts=True,
            strict_path_metadata=True,
        ) as fixture:
            result = self._strict_verify(fixture)

        self.assertFinding(result, "adaptation paths are not in canonical order")

    def test_strict_mode_rejects_reversed_adaptation_fields(self) -> None:
        with self._fixture(
            strict_artifacts=True,
            strict_path_metadata=True,
            reverse_sync_fields=True,
        ) as fixture:
            result = self._strict_verify(fixture)

        self.assertFinding(result, "adaptation fields are out of order")

    def test_strict_mode_rejects_mixed_applied_adaptation_note(self) -> None:
        with self._fixture(
            action="applied",
            adaptation_paths=[],
            adaptation_notes="dependency paths were stripped",
            strict_artifacts=True,
        ) as fixture:
            result = self._strict_verify(fixture)

        self.assertFinding(result, "applied action has adaptation_notes")

    def test_schema_v2_requires_paths_for_adapted_commit(self) -> None:
        with self._fixture(adaptation_paths=[]) as fixture:
            result = self._verify(fixture)

        self.assertFinding(result, "missing adaptation_paths")

    def test_schema_v2_rejects_invalid_or_duplicate_paths(self) -> None:
        cases = {
            "invalid kind": [
                {"kind": "changed", "path": "compositor/src/feature.txt"}
            ],
            "duplicate": [
                {"kind": "modified", "path": "compositor/src/feature.txt"},
                {"kind": "materialized", "path": "compositor/src/feature.txt"},
            ],
        }
        for expected, paths in cases.items():
            with self.subTest(expected=expected):
                with self._fixture(adaptation_paths=paths) as fixture:
                    result = self._verify(fixture)
                self.assertFinding(result, expected)

    def test_schema_v2_validates_each_adaptation_path_against_commit_paths(self) -> None:
        cases = {
            "modified adaptation path is not in target commit": [
                {"kind": "modified", "path": "compositor/src/omitted.txt"}
            ],
            "materialized adaptation path is not in target commit": [
                {"kind": "materialized", "path": "compositor/src/omitted.txt"}
            ],
            "omitted adaptation path is not expected by inventory": [
                {"kind": "omitted", "path": "compositor/src/unknown.txt"}
            ],
            "omitted adaptation path is present in target commit": [
                {"kind": "omitted", "path": "compositor/src/feature.txt"}
            ],
        }
        for expected, paths in cases.items():
            with self.subTest(expected=expected):
                with self._fixture(adaptation_paths=paths) as fixture:
                    result = self._verify(fixture)
                self.assertFinding(result, expected)

    def test_schema_v2_rejects_adaptation_paths_for_applied_commit(self) -> None:
        paths = [{"kind": "modified", "path": "compositor/src/feature.txt"}]
        with self._fixture(action="applied", adaptation_paths=paths) as fixture:
            result = self._verify(fixture)

        self.assertFinding(result, "applied action has adaptation_paths")

    def test_schema_v2_requires_commit_message_paths_to_match_evidence(self) -> None:
        message_paths = [
            {"kind": "materialized", "path": "compositor/src/feature.txt"}
        ]
        with self._fixture(message_paths=message_paths) as fixture:
            result = self._verify(fixture)

        self.assertFinding(result, "commit adaptation paths differ from evidence")

    def test_schema_v2_requires_commit_message_notes_to_match_evidence(self) -> None:
        with self._fixture(message_notes="different target adaptation") as fixture:
            result = self._verify(fixture)

        self.assertFinding(result, "commit adaptation notes differ from evidence")

    def test_schema_v2_requires_both_commit_message_fields(self) -> None:
        with self._fixture(include_sync_fields=False) as fixture:
            result = self._verify(fixture)

        self.assertFinding(result, "missing commit adaptation paths field")
        self.assertFinding(result, "missing commit adaptation notes field")

    @staticmethod
    def assertFinding(result: dict[str, Any], expected: str) -> None:
        if not any(expected in finding for finding in result["findings"]):
            raise AssertionError(f"未找到 {expected!r}: {result['findings']}")

    def _verify(self, fixture: dict[str, Any]) -> dict[str, Any]:
        return sync_audit.verify_sync(
            fixture["repo"],
            sync_audit.load_policy(POLICY_PATH),
            fixture["inventory"],
            fixture["traces"],
            fixture["evidence"],
        )

    def _strict_verify(self, fixture: dict[str, Any]) -> dict[str, Any]:
        return sync_audit.verify_sync(
            fixture["repo"],
            sync_audit.load_policy(POLICY_PATH),
            fixture["inventory"],
            fixture["traces"],
            fixture["evidence"],
            required_evidence_schema=2,
            evidence_root=fixture["evidence_root"],
        )

    def _fixture(
        self,
        *,
        schema_version: int | None = 2,
        action: str = "adapted",
        adaptation_paths: list[dict[str, str]] | None = None,
        message_paths: list[dict[str, str]] | None = None,
        adaptation_notes: str = "target API adaptation",
        message_notes: str | None = None,
        include_sync_fields: bool = True,
        strict_artifacts: bool = False,
        strict_path_metadata: bool = False,
        reverse_sync_fields: bool = False,
    ) -> _AdaptationFixture:
        paths = adaptation_paths
        if paths is None:
            paths = (
                [
                    {"kind": "omitted", "path": "compositor/src/omitted.txt"},
                    {"kind": "materialized", "path": "compositor/src/new.txt"},
                    {"kind": "modified", "path": "compositor/src/feature.txt"},
                ]
                if strict_path_metadata
                else [
                    {"kind": "modified", "path": "compositor/src/feature.txt"},
                    {"kind": "omitted", "path": "compositor/src/omitted.txt"},
                    {"kind": "materialized", "path": "compositor/src/new.txt"},
                ]
            )
        return _AdaptationFixture(
            source=self.source,
            schema_version=schema_version,
            action=action,
            adaptation_paths=paths,
            message_paths=message_paths if message_paths is not None else paths,
            adaptation_notes=adaptation_notes,
            message_notes=message_notes or adaptation_notes,
            include_sync_fields=include_sync_fields,
            strict_artifacts=strict_artifacts,
            strict_path_metadata=strict_path_metadata,
            reverse_sync_fields=reverse_sync_fields,
        )


class _AdaptationFixture:
    def __init__(
        self,
        *,
        source: str,
        schema_version: int | None,
        action: str,
        adaptation_paths: list[dict[str, str]],
        message_paths: list[dict[str, str]],
        adaptation_notes: str,
        message_notes: str,
        include_sync_fields: bool,
        strict_artifacts: bool,
        strict_path_metadata: bool,
        reverse_sync_fields: bool,
    ) -> None:
        self.source = source
        self.schema_version = schema_version
        self.action = action
        self.adaptation_paths = adaptation_paths
        self.message_paths = message_paths
        self.adaptation_notes = adaptation_notes
        self.message_notes = message_notes
        self.include_sync_fields = include_sync_fields
        self.strict_artifacts = strict_artifacts
        self.strict_path_metadata = strict_path_metadata
        self.reverse_sync_fields = reverse_sync_fields
        self._temporary = tempfile.TemporaryDirectory()

    def __enter__(self) -> dict[str, Any]:
        root = Path(self._temporary.name)
        repo = self._build_repo(root)
        inventory = self._inventory()
        traces = sync_audit.build_trace_audit(repo, "HEAD", inventory)
        evidence = self._evidence(root, traces)
        return {
            "root": root,
            "evidence_root": root / "evidence-artifacts",
            "repo": repo,
            "inventory": inventory,
            "traces": traces,
            "evidence": evidence,
        }

    def _build_repo(self, root: Path) -> Path:
        repo = root / "repo"
        repo.mkdir()
        self._git(repo, "init")
        self._git(repo, "config", "user.name", "Audit Fixture")
        self._git(repo, "config", "user.email", "audit@example.invalid")
        self._write(repo, "compositor/src/feature.txt", "base\n")
        self._write(repo, "compositor/src/omitted.txt", "base\n")
        self._commit_all(repo, "base")
        self._write(repo, "compositor/src/feature.txt", "adapted\n")
        self._write(repo, "compositor/src/new.txt", "materialized\n")
        self._git(repo, "add", "compositor/src/feature.txt", "compositor/src/new.txt")
        self._git(repo, "commit", "-m", "adapted feature", "-m", self._message())
        return repo

    def _inventory(self) -> dict[str, Any]:
        return {
            "approved_review": [],
            "commits": [
                {
                    "source_commit": self.source,
                    "classification": "other",
                    "target_paths": [
                        "compositor/src/feature.txt",
                        "compositor/src/omitted.txt",
                        "compositor/src/new.txt",
                    ],
                }
            ],
        }

    def _evidence(
        self, root: Path, traces: dict[str, Any]
    ) -> dict[str, Any]:
        artifacts = self._artifacts(root)
        paths = self._evidence_paths(artifacts)
        evidence: dict[str, Any] = {
            "entries": [
                {
                    "source_commit": self.source,
                    "target_commit": traces["mappings"][0]["target_commit"],
                    "action": self.action,
                    "adaptation_paths": paths,
                    "adaptation_notes": self.adaptation_notes,
                    **artifacts,
                }
            ]
        }
        if self.schema_version is not None:
            evidence["schema_version"] = self.schema_version
        return evidence

    def _evidence_paths(self, artifacts: dict[str, Any]) -> list[dict[str, Any]]:
        if not self.strict_path_metadata:
            return self.adaptation_paths
        statuses = {
            "compositor/src/feature.txt": ("M", True),
            "compositor/src/omitted.txt": ("omitted", True),
            "compositor/src/new.txt": ("A", False),
        }
        paths = []
        for item in self.adaptation_paths:
            target_status, parent_exists = statuses[item["path"]]
            paths.append(
                {
                    **item,
                    "target_status": target_status,
                    "source_status": "M",
                    "parent_exists": parent_exists,
                    "proof": [artifacts["difference_report"]],
                    "review_state": "approved",
                }
            )
        return paths

    def __exit__(self, *args: object) -> None:
        self._temporary.cleanup()

    def _message(self) -> str:
        lines = [
            f"[treeland-sync] action: {self.action}",
        ]
        if self.include_sync_fields:
            path_lines = ["[treeland-sync] adaptation paths:"]
            path_lines.extend(
                f"- {item['kind']}: {item['path']}" for item in self.message_paths
            )
            if not self.message_paths:
                path_lines.append("- none")
            note_lines = ["[treeland-sync] adaptation notes:"]
            note_lines.extend(f"- {line}" for line in self.message_notes.splitlines())
            lines.extend(note_lines if self.reverse_sync_fields else path_lines)
            lines.extend(path_lines if self.reverse_sync_fields else note_lines)
        lines.append(f"Treeland-Commit: {self.source}")
        return "\n".join(lines)

    def _artifacts(self, root: Path) -> dict[str, Any]:
        artifact_root = root / "evidence-artifacts"
        artifact_root.mkdir()
        artifacts: dict[str, Any] = {}
        for name in (
            "mapped_patch",
            "staged_diff",
            "commit_diff",
            "path_audit",
            "difference_report",
        ):
            artifact = artifact_root / f"{name}.txt"
            artifact.write_text(f"{name}\n", encoding="utf-8")
            if self.strict_artifacts:
                artifacts[name] = {
                    "path": artifact.name,
                    "size": artifact.stat().st_size,
                    "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
                }
            else:
                artifacts[name] = str(artifact)
        return artifacts

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
