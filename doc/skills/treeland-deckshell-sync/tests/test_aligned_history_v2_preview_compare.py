"""Tests for byte-identical independent preview comparison."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from aligned_history_v2.artifacts import write_hashed_json
from aligned_history_v2.preview_compare import compare_previews


class AlignedHistoryV2PreviewCompareTests(unittest.TestCase):
    def test_cli_exposes_explicit_preview_and_compare_commands(self) -> None:
        script = SKILL_DIR / "scripts" / "aligned_history_v2.py"
        namespace: dict[str, object] = {"__file__": str(script), "__name__": "v2_cli_test"}
        exec(compile(script.read_bytes(), str(script), "exec"), namespace)
        parser = namespace["build_parser"]()
        args = parser.parse_args(
            [
                "--mode",
                "commit-aligned-history-rewrite-v2",
                "--workspace",
                "/workspace",
                "--plan",
                "/plan.md",
                "--output",
                "/output",
                "preview",
                "--manifest",
                "/manifest.json",
                "--dry-run",
                "/dry-run.json",
                "--preview-name",
                "A",
                "--object-directory",
                "/objects",
                "--scratch-directory",
                "/scratch",
            ]
        )
        self.assertEqual(args.command, "preview")
        compare = parser.parse_args(
            [
                "--mode",
                "commit-aligned-history-rewrite-v2",
                "--workspace",
                "/workspace",
                "--plan",
                "/plan.md",
                "--output",
                "/output",
                "compare-previews",
                "--preview-a",
                "/A",
                "--preview-b",
                "/B",
            ]
        )
        self.assertEqual(compare.command, "compare-previews")
        formal_import = parser.parse_args(
            [
                "--mode",
                "commit-aligned-history-rewrite-v2",
                "--workspace",
                "/workspace",
                "--plan",
                "/plan.md",
                "--output",
                "/output",
                "import-preview",
                "--manifest",
                "/manifest.json",
                "--preview-a",
                "/A",
                "--preview-b",
                "/B",
                "--dual-verification",
                "/dual.json",
                "--migration-ref",
                "refs/migrations/commit-aligned-history-rewrite-v2/run",
            ]
        )
        self.assertEqual(formal_import.command, "import-preview")

    def test_compare_requires_identical_payloads_and_distinct_object_directories(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "A"
            second = root / "B"
            for output, name in ((first, "A"), (second, "B")):
                self._write_preview(output, name, root)

            result = compare_previews(first, second)

            self.assertEqual(result["outcome"], "pass")
            self.assertEqual(result["head"], "1" * 40)
            write_hashed_json(
                second / "rewrite-target-mapping.v2.json",
                {"head": "9" * 40, "head_tree": "2" * 40},
            )
            with self.assertRaisesRegex(ValueError, "mapping payloads differ"):
                compare_previews(first, second)

    @staticmethod
    def _write_preview(output: Path, name: str, root: Path) -> None:
        mapping = {"head": "1" * 40, "head_tree": "2" * 40}
        prefix = {"entries": [{"v2_target": "3" * 40}]}
        inventory = {"objects": [{"object_id": "4" * 40}]}
        write_hashed_json(output / "rewrite-target-mapping.v2.json", mapping)
        write_hashed_json(output / "treeland-target-prefix.v2.json", prefix)
        write_hashed_json(output / "object-inventory.v2.json", inventory)
        write_hashed_json(
            output / "preview-evidence.v2.json",
            {
                "preview_name": name,
                "outcome": "pass",
                "head": mapping["head"],
                "head_tree": mapping["head_tree"],
                "compile_atomic_verification": {
                    "outcome": "pass",
                    "replay_pair_count": 330,
                },
                "isolation": {
                    "writable_object_directory": str(root / f"objects-{name}"),
                    "read_only_alternate": str(root / "source-objects"),
                    "alternate_count": 1,
                    "other_preview_is_alternate": False,
                    "formal_object_writes": 0,
                },
            },
        )


if __name__ == "__main__":
    unittest.main()
