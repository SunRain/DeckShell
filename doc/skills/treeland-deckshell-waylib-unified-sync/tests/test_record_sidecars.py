from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from records_fixture import RecordsFixture
from unified_sync_lib.record_context import make_context
from unified_sync_lib.repo_records import generate_records


class RecordSidecarTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.fixture = RecordsFixture(self.root)

    def directory(self, lane, batch):
        return self.fixture.repos[lane] / ("doc" if lane == "parent" else "docs") / "treeland-sync" / batch

    def plans(self, lane, batch, names=("plan.md", "prd.md")):
        directory = self.directory(lane, batch)
        directory.mkdir(parents=True, exist_ok=True)
        contents = {}
        for name in names:
            path = directory / name
            contents[path] = f"# {lane} 的手写方案：{name}\n\n保留原授权与验收边界。\n".encode("utf-8")
            path.write_bytes(contents[path])
        return contents

    def generate(self, batch):
        f = self.fixture
        context = make_context(f.source, f.repos["parent"], f.repos["child"], f.repos["wlroots"],
                               batch, self.root / "evidence", "history/sample", None)
        return generate_records(context, f.nodes)

    def files(self, batch):
        return {path: path.read_bytes() for lane in ("parent", "child")
                for path in self.directory(lane, batch).rglob("*")
                if not path.is_symlink() and path.is_file()}

    def assert_plan_links(self, lane, batch, present):
        summary = (self.directory(lane, batch) / "summary.md").read_text(encoding="utf-8")
        line = "- 原需求与实施记录：[PRD](prd.md)、[plan](plan.md)。"
        if present:
            self.assertIn(line, summary)
            self.assertNotIn("未声称已随仓携带", summary)
        else:
            self.assertNotIn("[PRD](", summary)
            self.assertNotIn("[plan](", summary)
            self.assertIn("未声称已随仓携带", summary)

    def test_local_plans_survive_repeated_generation_and_are_not_counted(self):
        expected = {}
        for lane in ("parent", "child"):
            expected.update(self.plans(lane, "sample"))
        result = self.generate("sample")
        self.assertEqual(result["parent"]["files"], 2)
        self.assertEqual(result["child"]["files"], 3)
        for lane in ("parent", "child"):
            self.assert_plan_links(lane, "sample", True)
        first = self.files("sample")
        self.assertEqual(self.generate("sample"), result)
        self.assertEqual(self.files("sample"), first)
        self.assertEqual({path: path.read_bytes() for path in expected}, expected)

    def test_root_plans_are_neither_discovered_nor_copied(self):
        expected = {}
        for lane in ("parent", "child"):
            old = self.fixture.repos[lane] / "sample"
            old.mkdir()
            for name in ("plan.md", "prd.md"):
                expected[old / name] = b"old root plan\n"
                (old / name).write_bytes(expected[old / name])
        self.generate("sample")
        for lane in ("parent", "child"):
            self.assert_plan_links(lane, "sample", False)
            for name in ("plan.md", "prd.md"):
                self.assertFalse((self.directory(lane, "sample") / name).exists())
        self.assertEqual({path: path.read_bytes() for path in expected}, expected)

    def test_missing_or_incomplete_pairs_stay_external_without_creating_plans(self):
        for index, names in enumerate(((), ("plan.md",), ("prd.md",))):
            batch = f"incomplete-{index}"
            with self.subTest(names=names):
                expected = {}
                for lane in ("parent", "child"):
                    expected.update(self.plans(lane, batch, names))
                self.generate(batch)
                for lane in ("parent", "child"):
                    self.assert_plan_links(lane, batch, False)
                    for name in ("plan.md", "prd.md"):
                        self.assertEqual((self.directory(lane, batch) / name).exists(), name in names)
                self.assertEqual({path: path.read_bytes() for path in expected}, expected)

    def test_plan_discovery_does_not_cross_repository_boundaries(self):
        for lane, other in (("parent", "child"), ("child", "parent")):
            with self.subTest(lane=lane):
                self.plans(lane, lane)
                self.generate(lane)
                self.assert_plan_links(lane, lane, True)
                self.assert_plan_links(other, lane, False)

    def test_unknown_files_with_plans_prevent_all_output(self):
        names = ("manual.md", "plan.md.bak", "adaptations/plan.md", "extra/prd.md")
        for index, name in enumerate(names):
            batch = f"unknown-{index}"
            with self.subTest(name=name):
                for lane in ("parent", "child"):
                    self.plans(lane, batch)
                unknown = self.directory("child", batch) / name
                unknown.parent.mkdir(parents=True, exist_ok=True)
                unknown.write_text("handwritten\n", encoding="utf-8")
                before = self.files(batch)
                with self.assertRaisesRegex(ValueError, "手写"):
                    self.generate(batch)
                self.assertEqual(self.files(batch), before)

    def test_summary_and_adaptation_conflicts_with_plans_prevent_all_output(self):
        self.generate("reference")
        detail = next((self.directory("child", "reference") / "adaptations").glob("*.md"))
        for index, name in enumerate(("summary.md", f"adaptations/{detail.name}")):
            batch = f"conflict-{index}"
            with self.subTest(name=name):
                for lane in ("parent", "child"):
                    self.plans(lane, batch)
                conflict = self.directory("child", batch) / name
                conflict.parent.mkdir(parents=True, exist_ok=True)
                conflict.write_text("handwritten\n", encoding="utf-8")
                before = self.files(batch)
                with self.assertRaisesRegex(ValueError, "已有内容冲突"):
                    self.generate(batch)
                self.assertEqual(self.files(batch), before)

    def test_regular_and_dangling_sidecar_symlinks_are_rejected(self):
        outside = self.root / "outside.md"
        outside.write_text("outside\n", encoding="utf-8")
        for lane in ("parent", "child"):
            for name in ("plan.md", "prd.md"):
                for dangling in (False, True):
                    batch = f"symlink-{lane}-{name}-{dangling}"
                    with self.subTest(lane=lane, name=name, dangling=dangling):
                        for current in ("parent", "child"):
                            names = tuple(n for n in ("plan.md", "prd.md") if current != lane or n != name)
                            self.plans(current, batch, names)
                        link = self.directory(lane, batch) / name
                        link.symlink_to(self.root / "missing.md" if dangling else outside)
                        before = self.files(batch)
                        with self.assertRaisesRegex(ValueError, "符号链接"):
                            self.generate(batch)
                        self.assertEqual(self.files(batch), before)
                        self.assertTrue(link.is_symlink())
        self.assertEqual(outside.read_text(encoding="utf-8"), "outside\n")

    def test_directories_cannot_impersonate_plan_files(self):
        for lane in ("parent", "child"):
            for name in ("plan.md", "prd.md"):
                batch = f"directory-{lane}-{name}"
                with self.subTest(lane=lane, name=name):
                    path = self.directory(lane, batch) / name
                    path.mkdir(parents=True)
                    before = self.files(batch)
                    with self.assertRaisesRegex(ValueError, "普通文件"):
                        self.generate(batch)
                    self.assertEqual(self.files(batch), before)
                    self.assertTrue(path.is_dir())


if __name__ == "__main__":
    unittest.main()
