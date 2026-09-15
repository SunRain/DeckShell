from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from generate_repo_records import main
from records_fixture import RecordsFixture
from records_initialization_fixture import initialization_fixture
from support import run
from unified_sync_lib.git_ops import atomic_write_json, canonical_json_sha256, read_json
from unified_sync_lib.record_context import make_context
from unified_sync_lib.repo_records import generate_records


class RepoRecordTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.fixture = RecordsFixture(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def context(self, mapping=None, batch="sample"):
        f = self.fixture
        return make_context(f.source, f.repos["parent"], f.repos["child"], f.repos["wlroots"],
                            batch, self.root / "evidence", "history/sample", mapping)

    def files(self, lane):
        directory = self.fixture.repos[lane] / ("doc" if lane == "parent" else "docs") / "treeland-sync/sample"
        return {p.relative_to(directory).as_posix(): p.read_bytes() for p in directory.rglob("*.md")}

    def _rebind_evidence(self, lane):
        filename, gatefile, key = {
            "parent": ("parent-evidence.json", "deckshell-verify.json", "deckshell_verify"),
            "child": ("waylib-evidence.json", "waylib-verify.json", "waylib_verify"),
        }[lane]
        root = self.fixture.artifacts
        gate = read_json(root / gatefile)
        gate["evidence_sha256"] = canonical_json_sha256(read_json(root / filename))
        atomic_write_json(root / gatefile, gate)
        report = read_json(root / "sync-report.json")
        report["gate_sha256"][key] = canonical_json_sha256(gate)
        atomic_write_json(root / "sync-report.json", report)

    def test_real_cli_separates_p_only_c_only_dual_and_r_ownership(self):
        f = self.fixture
        args = ["--source-repo", str(f.source), "--parent-repo", str(f.repos["parent"]),
                "--child-repo", str(f.repos["child"]), "--wlroots-repo", str(f.repos["wlroots"]),
                "--batch", "sample", "--evidence-root", str(self.root / "evidence"),
                "--evidence-label", "history/sample", "--nodes", str(f.nodes)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(main(args), 0)
        self.assertEqual(json.loads(output.getvalue())["parent"], {"records": 6, "files": 2, "adaptations": 1})
        p, c = self.files("parent"), self.files("child")
        parent_text, child_text = b"\n".join(p.values()).decode(), b"\n".join(c.values()).decode()
        self.assertNotIn("C_ONLY_LOCAL_REASON", parent_text)
        self.assertNotIn("C_DUAL_REASON", parent_text)
        self.assertIn("P_DUAL_REASON", parent_text)
        self.assertIn("C_ONLY_LOCAL_REASON", child_text)
        self.assertNotIn("P_DUAL_REASON", child_text)
        self.assertIn("R_ONLY_REASON", child_text)
        self.assertNotIn("R_ONLY_REASON", parent_text)
        self.assertIn("wlroots/cmake/private.cmake", child_text)
        self.assertIn("独立 R", child_text)
        self.assertIn("仅依赖引用传播", parent_text)
        self.assertIn("ALREADY_EQUIVALENT", parent_text)
        self.assertFalse((f.repos["wlroots"] / "docs").exists())

    def test_rewritten_details_use_new_target_sha_not_source_or_old_target(self):
        mapping, _ = self.fixture.rewrite()
        result = generate_records(self.context(mapping), self.fixture.nodes)
        self.assertEqual(result["child"]["adaptations"], 2)
        info = read_json(mapping)["repositories"]
        entry = self.fixture.manifest["entries"][2]
        new = next(v["new"] for v in info["parent"]["commits"] if v["old"] == entry["parent"]["commit"])
        files = self.files("parent")
        self.assertIn(f"adaptations/{new}.md", files)
        self.assertNotIn(f"adaptations/{entry['source_commit']}.md", files)
        self.assertNotIn(f"adaptations/{entry['parent']['commit']}.md", files)
        detail = files[f"adaptations/{new}.md"].decode()
        self.assertIn(entry["source_commit"], detail)
        self.assertIn(entry["parent"]["commit"], detail)
        self.assertIn("来源的本次增量", detail)
        self.assertIn("本仓的本次增量", detail)
        self.assertIn("upstream P", detail)
        self.assertIn("local P", detail)

    def test_normal_input_does_not_invent_old_target_column(self):
        generate_records(self.context(), self.fixture.nodes)
        summary = self.files("parent")["summary.md"].decode()
        self.assertNotIn("| 原目标 |", summary)
        self.assertIn("未提供历史改写映射", summary)

    def test_original_failed_no_tests_and_unverified_states_are_preserved(self):
        mapping, _ = self.fixture.rewrite()
        generate_records(self.context(mapping), self.fixture.nodes)
        summary = self.files("parent")["summary.md"].decode()
        self.assertIn("**blocked**", summary)
        self.assertIn("| FAIL | 1 |", summary)
        self.assertIn("| NO_TESTS | 0 |", summary)
        self.assertIn("| UNVERIFIED | None |", summary)
        original = self.fixture.manifest["final_parent_head"]
        self.assertIn(f"原候选 P / DeckShell：` {original} `", summary)
        self.assertIn("未替换成整理后 SHA", summary)

    def test_repeated_generation_is_identical_and_does_not_stage_or_update_refs(self):
        f = self.fixture
        indexes = {lane: (repo / ".git/index").read_bytes() for lane, repo in f.repos.items()}
        refs = {lane: run(repo, "for-each-ref", "--format=%(refname) %(objectname)") for lane, repo in f.repos.items()}
        generate_records(self.context(), f.nodes)
        before = {lane: self.files(lane) for lane in ("parent", "child")}
        generate_records(self.context(), f.nodes)
        self.assertEqual(before, {lane: self.files(lane) for lane in before})
        for lane, repo in f.repos.items():
            self.assertEqual(indexes[lane], (repo / ".git/index").read_bytes())
            self.assertEqual(refs[lane], run(repo, "for-each-ref", "--format=%(refname) %(objectname)"))

    def test_old_docs_and_other_batches_are_untouched(self):
        old = self.fixture.repos["parent"] / "doc/treeland-sync/adaptations/old.md"
        other = self.fixture.repos["child"] / "docs/treeland-sync/other/summary.md"
        for path in (old, other):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"handwritten old report\n")
        generate_records(self.context(), self.fixture.nodes)
        self.assertEqual(old.read_bytes(), b"handwritten old report\n")
        self.assertEqual(other.read_bytes(), b"handwritten old report\n")

    def test_conflict_in_child_prevents_any_parent_output(self):
        path = self.fixture.repos["child"] / "docs/treeland-sync/sample/summary.md"
        path.parent.mkdir(parents=True)
        path.write_text("handwritten\n")
        with self.assertRaisesRegex(ValueError, "已有内容冲突"):
            generate_records(self.context(), self.fixture.nodes)
        self.assertEqual(self.files("parent"), {})
        self.assertEqual(path.read_text(), "handwritten\n")

    def test_unexpected_handwritten_file_in_batch_is_not_removed(self):
        generate_records(self.context(), self.fixture.nodes)
        note = self.fixture.repos["parent"] / "doc/treeland-sync/sample/manual.md"
        note.write_text("manual\n")
        with self.assertRaisesRegex(ValueError, "手写"):
            generate_records(self.context(), self.fixture.nodes)
        self.assertEqual(note.read_text(), "manual\n")

    def test_output_symlink_is_rejected(self):
        parent = self.fixture.repos["parent"] / "doc/treeland-sync"
        parent.mkdir(parents=True)
        outside = self.root / "outside"
        outside.mkdir()
        (parent / "sample").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "符号链接"):
            generate_records(self.context(), self.fixture.nodes)
        self.assertEqual(list(outside.iterdir()), [])

    def test_bad_batch_and_node_path_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "批次"):
            self.context(batch="../escape")
        atomic_write_json(self.fixture.nodes, {"nodes": [{"name": "N1", "kind": "replay", "path": "../escape"}]})
        with self.assertRaisesRegex(ValueError, "越界"):
            generate_records(self.context(), self.fixture.nodes)
        self.assertFalse((self.fixture.repos["parent"] / "doc").exists())

    def test_empty_nested_directory_cannot_impersonate_r(self):
        f = self.fixture
        empty = f.repos["child"] / "empty-r"
        empty.mkdir()
        with self.assertRaisesRegex(ValueError, "worktree root"):
            make_context(f.source, f.repos["parent"], f.repos["child"], empty,
                         "sample", self.root / "evidence", "history/sample", None)

    def test_missing_mapping_entry_and_wrong_target_are_rejected(self):
        mapping, _ = self.fixture.rewrite()
        data = read_json(mapping)
        data["repositories"]["parent"]["commits"][0]["new"] = self.fixture.manifest["final_parent_head"]
        atomic_write_json(mapping, data)
        with self.assertRaisesRegex(ValueError, "错配"):
            generate_records(self.context(mapping), self.fixture.nodes)
        mapping, data = self.fixture.rewrite()
        payload = read_json(mapping)
        payload["repositories"]["child"]["commits"].pop()
        atomic_write_json(mapping, payload)
        with self.assertRaises(ValueError):
            generate_records(self.context(mapping), self.fixture.nodes)

    def test_missing_evidence_and_false_original_candidate_are_rejected(self):
        path = self.fixture.artifacts / "parent-evidence.json"
        saved = path.with_suffix(".saved")
        path.rename(saved)
        with self.assertRaises(FileNotFoundError):
            generate_records(self.context(), self.fixture.nodes)
        saved.rename(path)
        report = read_json(self.fixture.artifacts / "sync-report.json")
        report["final_parent_head"] = self.fixture.bases["parent"]
        atomic_write_json(self.fixture.artifacts / "sync-report.json", report)
        with self.assertRaisesRegex(ValueError, "终点失配"):
            generate_records(self.context(), self.fixture.nodes)

    def test_artifact_traversal_is_rejected_even_with_matching_report_binding(self):
        path = self.fixture.artifacts / "parent-evidence.json"
        evidence = read_json(path)
        evidence["entries"][0]["artifacts"]["target_diff"]["path"] = "../outside.diff"
        atomic_write_json(path, evidence)
        self._rebind_evidence("parent")
        with self.assertRaisesRegex(ValueError, "escapes root"):
            generate_records(self.context(), self.fixture.nodes)

    def test_mismatched_adaptation_target_is_rejected(self):
        path = self.fixture.artifacts / "waylib-evidence.json"
        evidence = read_json(path)
        evidence["entries"][0]["target_commit"] = evidence["entries"][1]["target_commit"]
        atomic_write_json(path, evidence)
        self._rebind_evidence("child")
        with self.assertRaisesRegex(ValueError, "目标错配"):
            generate_records(self.context(), self.fixture.nodes)


class RecordBoundaryTests(unittest.TestCase):
    def test_two_repo_node_keeps_inactive_r_not_applicable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = RecordsFixture(root, active_r=False)
            context = make_context(fixture.source, fixture.repos["parent"], fixture.repos["child"], None,
                                   "two", root / "evidence", "history/two", None)
            result = generate_records(context, fixture.nodes)
            self.assertEqual(result["parent"]["records"], 4)
            summary = (fixture.repos["child"] / "docs/treeland-sync/two/summary.md").read_text()
            self.assertIn("not-applicable", summary)
            self.assertIn("没有 R 普通来源提交", summary)

    def test_first_registration_adapted_is_not_fake_c_source_adaptation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = RecordsFixture(root, registration=True)
            context = make_context(fixture.source, fixture.repos["parent"], fixture.repos["child"], fixture.repos["wlroots"],
                                   "registration", root / "evidence", "history/registration", None)
            generate_records(context, fixture.nodes)
            first_child = next(v["child"] for v in fixture.manifest["entries"] if v["child"].get("commit"))
            self.assertEqual(first_child["action"], "adapted")
            self.assertEqual(first_child["content_action"], "not-applicable")
            detail = fixture.repos["child"] / f"docs/treeland-sync/registration/adaptations/{first_child['commit']}.md"
            self.assertIn("仅来自 .gitmodules 显式登记", detail.read_text())

    def test_n2_uses_independent_proof_and_does_not_forge_ordinary_action(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, repos, nodes, candidate = initialization_fixture(root)
            context = make_context(source, repos["parent"], repos["child"], repos["wlroots"],
                                   "init", root / "evidence", "history/init", None)
            result = generate_records(context, nodes)
            self.assertEqual(result["parent"], {"records": 1, "files": 1, "adaptations": 0})
            self.assertEqual(result["child"], {"records": 1, "files": 1, "adaptations": 0})
            text = (repos["child"] / "docs/treeland-sync/init/summary.md").read_text()
            self.assertIn("本仓普通目标：**0**；独立初始化：**1**", text)
            self.assertIn(candidate["source_merge"], text)
            self.assertIn(candidate["wlroots_base"], text)
            self.assertIn("FIXTURE_INIT_REASON", text)
            self.assertFalse((root / "evidence/N2/manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
