from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "sync_audit.py"
POLICY_PATH = Path(__file__).parents[1] / "references" / "path-policy.md"
SPEC = importlib.util.spec_from_file_location("sync_audit_path_policy", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"无法加载审计脚本: {SCRIPT_PATH}")

sync_audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync_audit
SPEC.loader.exec_module(sync_audit)


class PathPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = {
            "mapped": {
                "directories": {"src": "compositor/src"},
                "files": {"CMakeLists.txt": "compositor/CMakeLists.txt"},
            },
            "root_owned": {
                "directories": {"protocols": "protocols"},
                "files": {".editorconfig": ".editorconfig"},
            },
            "excluded": {"directories": ["waylib", "qwlroots"], "files": []},
            "review_only": {
                "directories": {".github": ".github"},
                "files": {".gitmodules": ".gitmodules"},
            },
        }

    def test_classifies_every_policy_category(self) -> None:
        mapped = sync_audit.classify_path("src/core/main.cpp", self.policy, set())
        root = sync_audit.classify_path("protocols/kde.xml", self.policy, set())
        excluded = sync_audit.classify_path("waylib/server.cpp", self.policy, set())
        review = sync_audit.classify_path(".github/workflows/ci.yml", self.policy, set())
        unknown = sync_audit.classify_path("unexpected/file.txt", self.policy, set())

        self.assertEqual(
            (mapped.category, mapped.target),
            ("mapped", "compositor/src/core/main.cpp"),
        )
        self.assertEqual((root.category, root.target), ("root-owned", "protocols/kde.xml"))
        self.assertEqual((excluded.category, excluded.target), ("excluded", None))
        self.assertEqual(
            (review.category, review.target),
            ("review-only", ".github/workflows/ci.yml"),
        )
        self.assertEqual((unknown.category, unknown.target), ("unknown", None))

    def test_loads_the_repository_path_policy(self) -> None:
        policy = sync_audit.load_policy(POLICY_PATH)

        self.assertEqual(policy["version"], 1)
        self.assertEqual(
            policy["mapped"]["directories"]["translations"],
            "compositor/translations",
        )
        self.assertEqual(policy["review_only"]["directories"][".github"], ".github")

    def test_repository_policy_maps_project_metadata_into_compositor(self) -> None:
        policy = sync_audit.load_policy(POLICY_PATH)
        changes = sync_audit.parse_name_status_z(
            b"M\0.agents/rules/qt.md\0"
            b"M\0AGENTS.md\0"
            b"M\0scripts/pre-commit.sh\0"
            b"M\0waylib/server.cpp\0"
        )

        entry = sync_audit.summarize_commit(
            "c" * 40,
            "update project metadata and dependency",
            changes,
            policy,
            set(),
        )

        self.assertEqual(entry["classification"], "mixed")
        self.assertEqual(entry["drop_paths"], ["waylib/server.cpp"])
        self.assertEqual(
            entry["mapped_source_paths"],
            [".agents/rules/qt.md", "AGENTS.md", "scripts/pre-commit.sh"],
        )
        self.assertEqual(
            entry["target_paths"],
            [
                "compositor/.agents/rules/qt.md",
                "compositor/AGENTS.md",
                "compositor/scripts/pre-commit.sh",
            ],
        )
        self.assertEqual(entry["blocked_reasons"], [])

    def test_cli_exposes_inventory_traces_and_verify_commands(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--help"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        self.assertIn("inventory", completed.stdout)
        self.assertIn("traces", completed.stdout)
        self.assertIn("verify", completed.stdout)


if __name__ == "__main__":
    unittest.main()
