from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_FILE = SKILL_ROOT / "SKILL.md"
PUBLIC_SCRIPTS = (
    "artifact_record.py",
    "deckshell_verify.py",
    "generate_sync_report.py",
    "generate_repo_records.py",
    "gitlink_verify.py",
    "protocol_tracker.py",
    "record_local_fix.py",
    "unified_sync.py",
    "validation_record.py",
    "waylib_contract_audit.py",
    "waylib_inventory.py",
    "waylib_traces.py",
    "waylib_verify.py",
    "wlroots_verify.py",
)


def _frontmatter(text: str):
    match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        raise AssertionError("SKILL.md lacks YAML frontmatter")
    values = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if not separator:
            raise AssertionError(f"invalid frontmatter line: {line}")
        values[key.strip()] = value.strip()
    return values


class SkillContractTests(unittest.TestCase):
    def test_entrypoint_frontmatter_and_size(self) -> None:
        text = SKILL_FILE.read_text(encoding="utf-8")
        metadata = _frontmatter(text)

        self.assertLessEqual(len(text.splitlines()), 500)
        self.assertEqual(
            metadata["name"], "treeland-deckshell-waylib-unified-sync"
        )
        self.assertTrue(metadata["description"])
        self.assertEqual(set(metadata), {"name", "description"})

    def test_public_scripts_exist_and_expose_help(self) -> None:
        scripts = SKILL_ROOT / "scripts"
        self.assertEqual(
            {path.name for path in scripts.glob("*.py")}, set(PUBLIC_SCRIPTS)
        )
        for name in PUBLIC_SCRIPTS:
            result = subprocess.run(
                [sys.executable, str(scripts / name), "--help"],
                cwd=str(SKILL_ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, msg=f"{name}: {result.stdout}")
            self.assertIn("usage:", result.stdout.lower(), msg=name)

        for command in ("inventory", "replay", "materialize-child", "closeout"):
            result = subprocess.run(
                [
                    sys.executable,
                    str(scripts / "unified_sync.py"),
                    command,
                    "--help",
                ],
                cwd=str(SKILL_ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, msg=result.stdout)

    def test_markdown_relative_links_resolve(self) -> None:
        pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
        for document in SKILL_ROOT.rglob("*.md"):
            text = document.read_text(encoding="utf-8")
            for raw_target in pattern.findall(text):
                target = raw_target.split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                path = (document.parent / target).resolve()
                self.assertTrue(
                    path.exists(), msg=f"broken link in {document}: {raw_target}"
                )

    def test_examples_are_data_only_and_parse(self) -> None:
        yaml_path = SKILL_ROOT / "examples" / "unified-sync.example.yaml"
        decisions_path = SKILL_ROOT / "examples" / "decisions.example.json"
        yaml_text = yaml_path.read_text(encoding="utf-8")

        self.assertNotIn("```", yaml_text)
        self.assertNotRegex(yaml_text, r"(?m)^#\s")
        self.assertNotRegex(yaml_text, r"(?i)\boutcome\s*:\s*pass\b")

        try:
            import yaml
        except ImportError:
            yaml = None
        if yaml is not None:
            parsed = yaml.safe_load(yaml_text)
            self.assertIsInstance(parsed, dict)
            self.assertEqual(parsed["source_ref"], "refs/heads/source-review")
            self.assertEqual(parsed["source_tip"], "refs/heads/source-review")

        import json

        decisions = json.loads(decisions_path.read_text(encoding="utf-8"))
        self.assertIsInstance(decisions.get("entries"), dict)
        self.assertNotIn("outcome", decisions)

    def test_removed_risks_do_not_reappear_as_workflow(self) -> None:
        documents = {
            path.relative_to(SKILL_ROOT).as_posix(): path.read_text(encoding="utf-8")
            for path in SKILL_ROOT.rglob("*.md")
        }
        all_text = "\n".join(documents.values())

        self.assertNotRegex(all_text, r"(?im)^\s*git\s+push\b")
        self.assertNotIn("refs/remotes/" + "treeland/master", all_text)
        self.assertNotIn("refs/remotes/" + "treeland-protocols/master", all_text)
        self.assertNotRegex(all_text, r"(?i)classification\s*:\s*dependency-only")
        self.assertNotRegex(all_text, r"PASS（\d+/\d+）")
        self.assertIn("必须安装整个目录，不能只复制 `SKILL.md`", documents["README.md"])

        messages = documents["references/commit-messages.md"]
        child_section = messages.split("## child commit", 1)[1].split(
            "## waylib-only parent", 1
        )[0]
        self.assertIn("parent association: manifest-only", child_section)
        self.assertNotRegex(child_section, r"(?i)parent commit:\s*<[A-Z0-9_-]*SHA")

        contract = documents["references/unified-contract.md"]
        self.assertIn("closeout 时的已激活仓库的完整 `refs/heads/**`", contract)
        self.assertIn("child-first", contract)

        skill = documents["SKILL.md"]
        waylib_contract = documents["references/waylib-contract.md"]
        for validation_id in (
            "waylib-package-consumer-configure",
            "waylib-package-consumer-build",
            "waylib-package-consumer",
        ):
            self.assertIn(validation_id, skill)
            self.assertIn(validation_id, waylib_contract)
        self.assertIn("--no-tests=error", waylib_contract)
        self.assertIn("materialize-child", skill)
        self.assertIn("九类结构化门禁", skill)
        self.assertIn("protocols/compositor/**/*.xml", skill)
        self.assertIn("source_ref", skill)
        self.assertIn("可省略", skill)
        self.assertIn("不要求 remote 名称或 URL", skill)
        self.assertIn("--source-tip", skill)
        self.assertIn("不会自动创建或刷新 remote", skill)


if __name__ == "__main__":
    unittest.main()
