from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).parents[1]
SCRIPT = SKILL_DIR / "scripts" / "generate_adaptation_docs.py"


class AdaptationDocsCliTests(unittest.TestCase):
    def test_generate_writes_sha_named_document_with_complete_target_diff(self) -> None:
        with _Fixture() as fixture:
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            document = fixture.docs / f"{fixture.target}.md"
            content = document.read_text(encoding="utf-8")
            self.assertIn(f"DeckShell commit: `{fixture.target}`", content)
            self.assertIn("modified: compositor/feature.txt", content)
            self.assertIn("为什么这样适配", content)
            self.assertIn("Kept DeckShell's local feature contract.", content)
            self.assertIn("-target baseline", content)
            self.assertIn("+target adapted", content)

    def test_generate_renders_mapped_source_diff_for_omitted_path(self) -> None:
        with _Fixture(kind="omitted") as fixture:
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (fixture.docs / f"{fixture.target}.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("omitted: compositor/src/feature.txt", content)
            self.assertIn("目标提交无该路径 diff", content)
            self.assertIn("diff --git a/compositor/src/feature.txt", content)
            self.assertIn("-source baseline", content)
            self.assertIn("+source upstream", content)

    def test_generate_rejects_materialized_path_with_existing_parent(self) -> None:
        with _Fixture(kind="materialized") as fixture:
            fixture.update_path(parent_exists=True)
            result = fixture.run_cli("generate")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("materialized parent path exists", result.stderr)

    def test_generate_rejects_manifest_count_drift(self) -> None:
        with _Fixture() as fixture:
            fixture.update_manifest_counts(adapted=2)
            result = fixture.run_cli("generate")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("manifest adapted count mismatch", result.stderr)

    def test_generate_rejects_commit_classification_mismatch(self) -> None:
        with _Fixture() as fixture:
            fixture.update_entry(classification="mixed")
            result = fixture.run_cli("generate")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("classification mismatch", result.stderr)

    def test_generate_rejects_source_mapping_mismatch(self) -> None:
        with _Fixture() as fixture:
            fixture.update_mapping(source_commit="f" * 40)
            result = fixture.run_cli("generate")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source mapping mismatch", result.stderr)

    def test_generate_renders_materialized_file_as_complete_target_diff(self) -> None:
        with _Fixture(kind="materialized") as fixture:
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (fixture.docs / f"{fixture.target}.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("materialized: compositor/new-feature.txt", content)
            self.assertIn("new file mode 100644", content)
            self.assertIn("+target adapted", content)

    def test_generate_is_idempotent_and_verify_detects_tampering(self) -> None:
        with _Fixture() as fixture:
            first = fixture.run_cli("generate")
            document = fixture.docs / f"{fixture.target}.md"
            first_content = document.read_bytes()
            second = fixture.run_cli("generate")
            verify = fixture.run_cli("verify")

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(verify.returncode, 0, verify.stderr)
            self.assertEqual(document.read_bytes(), first_content)

            document.write_text("tampered\n", encoding="utf-8")
            tampered = fixture.run_cli("verify")
            self.assertNotEqual(tampered.returncode, 0)
            self.assertIn("document content mismatch", tampered.stderr)

    def test_verify_rejects_unexpected_sha_document(self) -> None:
        with _Fixture() as fixture:
            self.assertEqual(fixture.run_cli("generate").returncode, 0)
            (fixture.docs / f"{'f' * 40}.md").write_text("extra\n", encoding="utf-8")

            result = fixture.run_cli("verify")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unexpected documents", result.stderr)

    def test_generate_uses_longer_markdown_fence_when_diff_contains_backticks(self) -> None:
        with _Fixture(target_content="target adapted\n```\n") as fixture:
            result = fixture.run_cli("generate")

            self.assertEqual(result.returncode, 0, result.stderr)
            content = (fixture.docs / f"{fixture.target}.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("````diff", content)
            self.assertIn("\n````\n", content)

    def test_generate_rejects_unapproved_adaptation_path(self) -> None:
        with _Fixture() as fixture:
            fixture.update_path(review_state="candidate")
            result = fixture.run_cli("generate")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("review_state is not approved", result.stderr)

    def test_verify_compares_document_bytes_without_newline_normalization(self) -> None:
        with _Fixture() as fixture:
            self.assertEqual(fixture.run_cli("generate").returncode, 0)
            document = fixture.docs / f"{fixture.target}.md"
            document.write_bytes(document.read_bytes().replace(b"\n", b"\r\n"))

            result = fixture.run_cli("verify")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("document content mismatch", result.stderr)

    def test_verify_rejects_symlink_document(self) -> None:
        with _Fixture() as fixture:
            self.assertEqual(fixture.run_cli("generate").returncode, 0)
            document = fixture.docs / f"{fixture.target}.md"
            outside = fixture.root / "outside.md"
            outside.write_bytes(document.read_bytes())
            document.unlink()
            document.symlink_to(outside)

            result = fixture.run_cli("verify")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("document must be a regular file", result.stderr)


class _Fixture:
    def __init__(
        self,
        *,
        kind: str = "modified",
        source_content: str | bytes | None = "source upstream\n",
        target_content: str | bytes | None = "target adapted\n",
        source_executable: bool = False,
        target_executable: bool = False,
        source_link_target: str | None = None,
        target_link_target: str | None = None,
        target_gitlink: bool = False,
        omitted_baseline_content: str | bytes | None = None,
    ) -> None:
        self._temporary = tempfile.TemporaryDirectory()
        self.root = Path(self._temporary.name)
        self.repo = self.root / "repo"
        self.docs = self.root / "docs"
        self.manifest = self.root / "manifest.json"
        self.mapping = self.root / "mapping.json"
        self.repo.mkdir()
        self._git("init")
        self._git("config", "user.name", "Test User")
        self._git("config", "user.email", "test@example.com")

        self._write("src/feature.txt", "source baseline\n")
        self._git("add", "src/feature.txt")
        self._git("commit", "-m", "source parent")
        source_file = self.repo / "src/feature.txt"
        if source_link_target is not None:
            source_file.unlink()
            source_file.symlink_to(source_link_target)
        elif source_content is None:
            source_file.unlink()
        else:
            self._write("src/feature.txt", source_content)
            if source_executable:
                source_file.chmod(0o755)
        self._git("commit", "-am", "source change")
        self.source = self._git("rev-parse", "HEAD").stdout.strip()
        self.source_deleted = source_content is None and source_link_target is None
        self.source_type_changed = source_link_target is not None

        self.kind = kind
        if kind == "omitted":
            self.adaptation_path = "compositor/src/feature.txt"
        elif kind == "materialized":
            self.adaptation_path = "compositor/new-feature.txt"
        else:
            self.adaptation_path = "compositor/feature.txt"
        target_file = (
            "compositor/other.txt"
            if kind in {"omitted", "materialized"}
            else self.adaptation_path
        )
        self._write(target_file, "target baseline\n")
        self._git("add", target_file)
        if kind == "omitted" and omitted_baseline_content is not None:
            self._write(self.adaptation_path, omitted_baseline_content)
            self._git("add", self.adaptation_path)
        self.omitted_parent_exists = omitted_baseline_content is not None
        self._git("commit", "-m", "range base")
        self.base = self._git("rev-parse", "HEAD").stdout.strip()
        if kind == "materialized":
            target_file = self.adaptation_path
        target_path = self.repo / target_file
        if target_gitlink:
            if target_path.exists() or target_path.is_symlink():
                target_path.unlink()
            self._git(
                "update-index",
                "--add",
                "--cacheinfo",
                f"160000,{self.source},{target_file}",
            )
        elif target_link_target is not None:
            if target_path.exists() or target_path.is_symlink():
                target_path.unlink()
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.symlink_to(target_link_target)
        elif target_content is None:
            target_path.unlink()
        else:
            self._write(target_file, target_content)
            if target_executable:
                target_path.chmod(0o755)
        self.target_deleted = (
            target_content is None and target_link_target is None and not target_gitlink
        )
        self.target_type_changed = target_link_target is not None or target_gitlink
        notes = (
            "The mapped source path was already absent in DeckShell."
            if kind == "omitted"
            else "Kept DeckShell's local feature contract."
        )
        message = "\n".join(
            [
                "adapt target feature",
                "",
                "[treeland-sync] classification: other",
                "[treeland-sync] action: adapted",
                "[treeland-sync] adaptation paths:",
                f"- {kind}: {self.adaptation_path}",
                "[treeland-sync] adaptation notes:",
                f"- {notes}",
                "",
                f"Treeland-Commit: {self.source}",
            ]
        )
        if not target_gitlink:
            self._git("add", target_file)
        self._git("commit", "-m", message)
        self.target = self._git("rev-parse", "HEAD").stdout.strip()
        self.notes = notes
        self._write_inputs()

    def __enter__(self) -> _Fixture:
        return self

    def __exit__(self, *_args: object) -> None:
        self._temporary.cleanup()

    def run_cli(self, command: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "python3",
                str(SCRIPT),
                command,
                "--repo",
                str(self.repo),
                "--manifest",
                str(self.manifest),
                "--mapping",
                str(self.mapping),
                "--base",
                self.base,
                "--head",
                self.target,
                "--docs-dir",
                str(self.docs),
                "--expected-count",
                "1",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def update_path(self, **values: object) -> None:
        payload = json.loads(self.manifest.read_text(encoding="utf-8"))
        payload["entries"][0]["adaptation_paths"][0].update(values)
        self.manifest.write_text(json.dumps(payload), encoding="utf-8")

    def update_manifest_counts(self, **values: int) -> None:
        payload = json.loads(self.manifest.read_text(encoding="utf-8"))
        payload["counts"].update(values)
        self.manifest.write_text(json.dumps(payload), encoding="utf-8")

    def update_entry(self, **values: object) -> None:
        payload = json.loads(self.manifest.read_text(encoding="utf-8"))
        payload["entries"][0].update(values)
        self.manifest.write_text(json.dumps(payload), encoding="utf-8")

    def update_mapping(self, **values: object) -> None:
        payload = json.loads(self.mapping.read_text(encoding="utf-8"))
        payload["mappings"][0].update(values)
        self.mapping.write_text(json.dumps(payload), encoding="utf-8")

    def update_source_changes(self, changes: list[dict[str, object]]) -> None:
        payload = json.loads(self.manifest.read_text(encoding="utf-8"))
        payload["entries"][0]["source_changes"] = changes
        self.manifest.write_text(json.dumps(payload), encoding="utf-8")

    def _write_inputs(self) -> None:
        source_side = {
            "source": "src/feature.txt",
            "target": self.adaptation_path,
        }
        source_change = (
            {"status": "D", "old": source_side, "new": None}
            if self.source_deleted
            else {
                "status": "T" if self.source_type_changed else "M",
                "old": None,
                "new": source_side,
            }
        )
        manifest = {
            "schema_version": 2,
            "migration_id": "test-adaptation-docs",
            "counts": {"entries": 1, "adapted": 1},
            "entries": [
                {
                    "ordinal": 1,
                    "source_commit": self.source,
                    "legacy_target_commit": "1" * 40,
                    "classification": "other",
                    "action": "adapted",
                    "source_changes": [source_change],
                    "adaptation_paths": [
                        {
                            "kind": self.kind,
                            "path": self.adaptation_path,
                            "target_status": (
                                "omitted"
                                if self.kind == "omitted"
                                else "A"
                                if self.kind == "materialized"
                                else "D"
                                if self.target_deleted
                                else "T"
                                if self.target_type_changed
                                else "M"
                            ),
                            "source_status": (
                                "D"
                                if self.source_deleted
                                else "T"
                                if self.source_type_changed
                                else "M"
                            ),
                            "parent_exists": (
                                self.kind == "modified" or self.omitted_parent_exists
                            ),
                            "proof": [
                                {
                                    "path": "proof.txt",
                                    "size": 1,
                                    "sha256": "0" * 64,
                                }
                            ],
                            "review_state": "approved",
                            "justification": "The path follows the reviewed DeckShell contract.",
                        }
                    ],
                    "adaptation_notes": self.notes,
                }
            ],
        }
        mapping = {
            "schema_version": 1,
            "count": 1,
            "plan_digest_sha256": "2" * 64,
            "mappings": [
                {
                    "source_commit": self.source,
                    "legacy_target_commit": "1" * 40,
                    "rewritten_target_commit": self.target,
                }
            ],
        }
        self.manifest.write_text(json.dumps(manifest), encoding="utf-8")
        self.mapping.write_text(json.dumps(mapping), encoding="utf-8")

    def _write(self, relative: str, content: str | bytes) -> None:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")

    def _git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(self.repo), *args],
            text=True,
            capture_output=True,
            check=True,
        )


if __name__ == "__main__":
    unittest.main()
