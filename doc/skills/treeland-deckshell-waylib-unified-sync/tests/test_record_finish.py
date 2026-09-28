"""正常任务入口的离线集成测试；原产品接受状态仅为显式合成 fixture。"""

from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from records_fixture import RecordsFixture
from support import commit_files
from unified_sync import main
from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.git_ops import atomic_write_json, canonical_json_sha256, read_json
from unified_sync_lib.record_context import make_context
from unified_sync_lib.record_replay import GATES
from unified_sync_lib.record_special import bridge_rows


class RecordFinishTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.f = RecordsFixture(self.root)
        self.plan = self.root / "plan"
        self.plan.mkdir()
        for name in ("plan.md", "prd.md"):
            (self.plan / name).write_text("# 原方案\n\n[需求](prd.md)\n[日志](../evidence/N1/logs/accepted.log)\n")
        self.accept_fixture()

    def accept_fixture(self):
        """构造明确标为 synthetic 的接受输入，不将 fixture 结果称为产品 PASS。"""
        f = self.f
        report = read_json(f.artifacts / "sync-report.json")
        for key, filename in GATES.items():
            value = read_json(f.artifacts / filename)
            value["outcome"] = "pass"
            atomic_write_json(f.artifacts / filename, value)
            report["gate_sha256"][key] = canonical_json_sha256(value)
        validations = {"kind": "treeland-unified-command-validations", "entries": [
            {"id": "synthetic-accepted-step", "outcome": "pass", "exit_code": 0,
             "log": write_artifact(f.artifacts, "logs/accepted.log", b"Synthetic accepted result, not a product run\n")}]}
        atomic_write_json(f.artifacts / "validations.json", validations)
        report.update(outcome="pass", validations_sha256=canonical_json_sha256(validations))
        self.bind_report(report)

    def bind_report(self, report, filename="sync-report.json"):
        atomic_write_json(self.f.artifacts / filename, report)
        identity = {"report_sha256": canonical_json_sha256(report)}
        for lane in self.f.repos:
            identity.update({lane + "_new": self.f.manifest["final_" + lane + "_head"],
                             lane + "_expected_old": self.f.bases[lane], lane + "_ref": "refs/heads/sync"})
        atomic_write_json(self.f.artifacts / "closeout-journal.json", {
            "kind": "treeland-unified-closeout-journal", "outcome": "pass", "identity": identity,
            **{lane + "_updated": True for lane in self.f.repos}})

    def args(self, task="consolidate"):
        f = self.f
        return ["finish", "--task", task, "--source-repo", str(f.source),
                "--parent-repo", str(f.request.parent_worktree), "--child-repo", str(f.request.child_worktree),
                "--wlroots-repo", str(f.request.wlroots_worktree), "--batch", "sample",
                "--evidence-root", str(f.artifacts.parent), "--evidence-label", "history/sample",
                "--plan-dir", str(self.plan), "--source-base", f.request.inventory["range"]["base"],
                "--source-head", f.request.inventory["range"]["head"]]

    def invoke(self, task="consolidate"):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(self.args(task))
        return code, out.getvalue(), err.getvalue()

    def documents(self):
        files = {}
        for repo in (self.f.request.parent_worktree, self.f.request.child_worktree):
            for path in repo.rglob("*/treeland-sync/sample/**/*.md"):
                files[str(path)] = path.read_bytes()
        return files

    def context(self):
        f = self.f
        return make_context(f.source, f.request.parent_worktree, f.request.child_worktree,
                            f.request.wlroots_worktree, "sample", f.artifacts.parent, "history/sample", None)

    def test_sync_finish_generates_both_repositories_and_plans_without_extra_command(self):
        code, output, errors = self.invoke("sync")
        self.assertEqual((code, errors), (0, ""))
        result = json.loads(output)
        self.assertFalse(result["git_committed"])
        self.assertEqual(result["records"]["parent"]["records"], 6)
        self.assertEqual(result["records"]["child"]["records"], 4)
        self.assertEqual(len(self.documents()), 9)

    def test_consolidation_finish_is_repeatable_and_preserves_refs_index_and_original_plans(self):
        repo = self.f.request.parent_worktree
        before = subprocess.check_output(["git", "-C", str(repo), "ls-files", "--stage", "-z"])
        self.assertEqual(self.invoke()[0], 0)
        documents = self.documents()
        self.assertEqual(self.invoke()[0], 0)
        self.assertEqual(self.documents(), documents)
        self.assertEqual(subprocess.check_output(["git", "-C", str(repo), "ls-files", "--stage", "-z"]), before)
        self.assertIn("[日志](../evidence/", (self.plan / "plan.md").read_text())

    def test_partial_parent_output_resumes_without_overwriting_it(self):
        context = self.context()
        from unified_sync_lib.record_finish import discover_nodes
        from unified_sync_lib.record_sidecars import plan_documents
        from unified_sync_lib.repo_records import collect_records
        from unified_sync_lib.record_render import render_documents
        inputs = discover_nodes(context, *[self.f.request.inventory["range"][k] for k in ("base", "head")], "consolidate")
        context.plan_documents = plan_documents(context, self.plan)
        nodes, rows = collect_records(context, inputs)
        documents = render_documents(context, nodes, rows)
        path = self.f.request.parent_worktree / "doc/treeland-sync/sample/summary.md"
        path.parent.mkdir(parents=True)
        path.write_text(documents[("parent", "doc/treeland-sync/sample/summary.md")])
        before = path.stat().st_mtime_ns
        self.assertEqual(self.invoke()[0], 0)
        self.assertEqual(path.stat().st_mtime_ns, before)
        self.assertEqual(len(self.documents()), 9)

    def test_generator_error_is_a_failure_of_the_normal_task(self):
        with patch("unified_sync_lib.record_finish.generate_from_inputs", side_effect=OSError("disk unavailable")):
            code, _, errors = self.invoke()
        self.assertEqual(code, 1)
        self.assertIn("disk unavailable", errors)
        self.assertFalse(self.documents())

    def test_real_cli_propagates_child_conflict_before_any_parent_writes(self):
        path = self.f.request.child_worktree / "docs/treeland-sync/sample/summary.md"
        path.parent.mkdir(parents=True)
        path.write_text("USER DOCUMENT\n")
        result = subprocess.run([sys.executable, str(SCRIPTS / "unified_sync.py"), *self.args()],
                                capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        self.assertEqual(result.returncode, 1)
        self.assertIn("已有内容冲突", result.stderr)
        self.assertEqual(path.read_text(), "USER DOCUMENT\n")
        self.assertEqual(len(self.documents()), 1)

    def test_missing_sidecar_is_not_silently_replaced_by_external_only_records(self):
        self.plan.joinpath("plan.md").rename(self.plan / "saved-plan.md")
        self.assertEqual(self.invoke()[0], 1)
        self.assertFalse(self.documents())

    def test_missing_or_ambiguous_acceptance_fails_before_output(self):
        journal = self.f.artifacts / "closeout-journal.json"
        data = read_json(journal)
        data["outcome"] = "blocked"
        atomic_write_json(journal, data)
        self.assertEqual(self.invoke()[0], 1)
        self.assertFalse(self.documents())

    def test_report_is_selected_by_closeout_not_final_filename(self):
        report = read_json(self.f.artifacts / "sync-report.json")
        self.bind_report(report, "sync-report-authorized.json")
        blocked = dict(report, outcome="blocked")
        atomic_write_json(self.f.artifacts / "sync-report.json", blocked)
        atomic_write_json(self.f.artifacts / "sync-report-final.json", dict(report, note="display-only"))
        code, _, errors = self.invoke()
        self.assertEqual((code, errors), (0, ""))
        text = (self.f.request.parent_worktree / "doc/treeland-sync/sample/summary.md").read_text()
        self.assertIn("sync-report-authorized.json", text)
        self.assertIn("BLOCKED", text)

    def test_current_pairing_gate_cannot_be_dropped(self):
        report = read_json(self.f.artifacts / "sync-report.json")
        report["protocol_pairing"] = {"outcome": "pass"}
        self.bind_report(report)
        code, _, errors = self.invoke()
        self.assertEqual(code, 1)
        self.assertIn("gate", errors)

    def test_nine_gates_render_without_reassigning_the_legacy_eight(self):
        report = read_json(self.f.artifacts / "sync-report.json")
        gate = {"outcome": "pass", "status": "synthetic-paired"}
        atomic_write_json(self.f.artifacts / "protocol-pairing.json", gate)
        report["protocol_pairing"] = gate
        report["gate_sha256"]["protocol_pairing"] = canonical_json_sha256(gate)
        self.bind_report(report)
        code, _, errors = self.invoke()
        self.assertEqual((code, errors), (0, ""))
        summary = (self.f.request.parent_worktree / "doc/treeland-sync/sample/summary.md").read_text()
        self.assertIn("protocol_pairing：pass / synthetic-paired", summary)

    def test_changed_report_cannot_reuse_original_closeout(self):
        path = self.f.artifacts / "sync-report.json"
        report = read_json(path)
        report["final_parent_head"] = self.f.bases["parent"]
        atomic_write_json(path, report)
        code, _, errors = self.invoke()
        self.assertEqual(code, 1)
        self.assertIn("收口绑定的接受报告", errors)
        self.assertFalse(self.documents())

    def test_duplicate_accepted_reports_are_ambiguous(self):
        shutil.copyfile(self.f.artifacts / "sync-report.json", self.f.artifacts / "sync-report-copy.json")
        code, _, errors = self.invoke()
        self.assertEqual(code, 1)
        self.assertIn("不唯一", errors)
        self.assertFalse(self.documents())

    def test_overlapping_accepted_attempts_are_not_selected_by_number(self):
        shutil.copytree(self.f.artifacts, self.f.artifacts.parent / "N1-attempt-999")
        code, _, errors = self.invoke()
        self.assertEqual(code, 1)
        self.assertIn("缺段、重叠或歧义", errors)
        self.assertFalse(self.documents())

    def test_unaccepted_tail_does_not_publish_a_partial_batch(self):
        tail = commit_files(self.f.source, {"src/next.cpp": "next node\n"}, "not yet accepted")
        args = self.args()
        args[args.index("--source-head") + 1] = tail
        with contextlib.redirect_stderr(io.StringIO()) as errors:
            self.assertEqual(main(args), 1)
        self.assertIn("缺段、重叠或歧义", errors.getvalue())
        self.assertFalse(self.documents())

    def test_sync_then_consolidation_reuses_identical_records(self):
        self.assertEqual(self.invoke("sync")[0], 0)
        before = self.documents()
        self.assertEqual(self.invoke("consolidate")[0], 0)
        self.assertEqual(self.documents(), before)

    def test_closeout_candidate_mismatch_fails(self):
        path = self.f.artifacts / "closeout-journal.json"
        data = read_json(path)
        data["identity"]["parent_new"] = self.f.bases["parent"]
        atomic_write_json(path, data)
        self.assertEqual(self.invoke()[0], 1)

    def test_unknown_extra_target_commit_is_not_ignored(self):
        f = self.f
        extra = commit_files(f.request.parent_worktree, {"unknown.txt": "unexpected"}, "unknown local change")
        f.manifest["final_parent_head"] = extra
        atomic_write_json(f.artifacts / "manifest.json", f.manifest)
        report = read_json(f.artifacts / "sync-report.json")
        report.update(final_parent_head=extra, manifest_sha256=canonical_json_sha256(f.manifest))
        self.bind_report(report)
        code, _, errors = self.invoke()
        self.assertEqual(code, 1)
        self.assertIn("未完整覆盖历史", errors)

    def test_structural_bridge_preserves_type_and_rejects_wrong_endpoint(self):
        f = self.f
        base = f.manifest["final_parent_head"]
        head = commit_files(f.request.parent_worktree, {"repair.cpp": "fixed\n"}, "local structural repair")
        receipt = {"kind": "treeland-structural-repair-closeout", "schema_version": 1,
                   "authorization": "synthetic explicit approval", "changes": ["repair canonical implementation"],
                   "expected_old": base, "new_head": head, "parent_ref": "refs/heads/sync",
                   "source_range": "none; local structural repair only", "verified_build": "N1/logs/accepted.log"}
        path = f.artifacts / "structural-repair-closeout.json"
        atomic_write_json(path, receipt)
        descriptor = [{"lane": "parent", "path": "N1/structural-repair-closeout.json"}]
        heads = {lane: f.manifest["final_" + lane + "_head"] for lane in f.repos}
        node = {"name": "N2", "path": "N1", "bases": {**heads, "parent": head}}
        previous = {"name": "N1", "heads": heads}
        rows = bridge_rows(self.context(), previous, node, descriptor)
        self.assertEqual(rows["parent"][0]["kind"], "structural-repair")
        self.assertIsNone(rows["parent"][0]["source"])
        receipt["expected_old"] = f.bases["parent"]
        atomic_write_json(path, receipt)
        with self.assertRaisesRegex(ValueError, "端点错配"):
            bridge_rows(self.context(), previous, node, descriptor)


if __name__ == "__main__":
    unittest.main()
