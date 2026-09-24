from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.git_ops import read_json
from unified_sync_lib.evidence import verify_waylib_sync
from unified_sync_lib.inventory import build_unified_inventory
from unified_sync_lib.parent_verify import verify_parent_sync
from unified_sync_lib.patches import source_patch
from unified_sync_lib.policy import load_policy
from unified_sync_lib.replay import ReplayBlocked, ReplayRequest, run_replay
from unified_sync_lib.replay_preflight import run_static_preflight
from unified_sync_lib.traces import build_waylib_traces

from support import (
    add_worktree,
    commit_files,
    init_repo,
    init_repo_with_separate_git_dir,
    run,
    write_policy,
)


class ReplayIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.source = init_repo(self.root / "source")
        self.child = init_repo(self.root / "child")
        self.parent = init_repo(self.root / "parent")
        self.source_base = commit_files(self.source, {"README.local": "base\n"}, "base")
        self.child_base = commit_files(self.child, {"README.local": "base\n"}, "base")
        run(
            self.parent,
            "update-index",
            "--add",
            "--cacheinfo",
            f"160000,{self.child_base},3rdparty/waylib-shared",
        )
        run(self.parent, "commit", "-m", "parent base")
        self.parent_base = run(self.parent, "rev-parse", "HEAD")
        self.policy_path = write_policy(self.root / "path-policy.md")
        self.policy = load_policy(self.policy_path)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def prepare_source(self):
        waylib_only = commit_files(
            self.source, {"qwlroots/a.cpp": "a\n"}, "fix(qwlroots): one"
        )
        dual = commit_files(
            self.source,
            {"waylib/b.cpp": "b\n", "src/app.cpp": "app\n"},
            "feat(core): two",
        )
        parent_only = commit_files(
            self.source, {"src/only.cpp": "only\n"}, "fix(core): three"
        )
        inventory = build_unified_inventory(
            self.source,
            self.source_base,
            parent_only,
            self.policy,
            self.policy_path,
            set(),
        )
        return waylib_only, dual, parent_only, inventory

    def request(self, inventory, suffix: str = "one") -> ReplayRequest:
        child_wt = add_worktree(
            self.child,
            self.root / f"child-wt-{suffix}",
            f"sync-child-{suffix}",
            self.child_base,
        )
        parent_wt = add_worktree(
            self.parent,
            self.root / f"parent-wt-{suffix}",
            f"sync-parent-{suffix}",
            self.parent_base,
        )
        artifacts = self.root / f"artifacts-{suffix}"
        return ReplayRequest(
            source_repo=self.source,
            parent_worktree=parent_wt,
            child_worktree=child_wt,
            parent_base=self.parent_base,
            child_base=self.child_base,
            inventory=inventory,
            artifact_root=artifacts,
            journal_path=artifacts / "journal.json",
            manifest_path=artifacts / "manifest.json",
            waylib_evidence_path=artifacts / "waylib-evidence.json",
            parent_evidence_path=artifacts / "parent-evidence.json",
            run_id=f"test-{suffix}",
            refs_doc="plans/test/plan.md",
            decisions={},
            allow_ephemeral_artifacts=True,
        )

    def verify_lanes(self, request, manifest):
        parent = verify_parent_sync(
            self.source, request.parent_worktree, self.parent_base,
            manifest["final_parent_head"], request.inventory, manifest,
            read_json(request.parent_evidence_path), request.artifact_root,
        )
        traces = build_waylib_traces(
            request.child_worktree, self.child_base, manifest["final_child_head"],
            request.inventory, self.source,
        )
        child = verify_waylib_sync(
            request.child_worktree, self.child_base, manifest["final_child_head"],
            request.inventory, traces, read_json(request.waylib_evidence_path),
            request.artifact_root, self.source,
        )
        return parent, child

    def test_replays_waylib_only_and_dual_child_first_with_exact_gitlinks(self) -> None:
        waylib_only, dual, parent_only, inventory = self.prepare_source()
        request = self.request(inventory)

        manifest = run_replay(request)

        self.assertEqual(manifest["outcome"], "pass")
        by_source = {entry["source_commit"]: entry for entry in manifest["entries"]}
        first = by_source[waylib_only]
        second = by_source[dual]
        third = by_source[parent_only]
        self.assertLess(first["child"]["sequence"], first["parent"]["sequence"])
        self.assertLess(second["child"]["sequence"], second["parent"]["sequence"])
        self.assertEqual(first["parent"]["action"], "gitlink-only")
        self.assertEqual(third["gitlink"]["status"], "unchanged")
        self.assertIsNone(third["child"]["commit"])

        first_paths = run(
            request.parent_worktree,
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            first["parent"]["commit"],
        ).splitlines()
        dual_paths = run(
            request.parent_worktree,
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            second["parent"]["commit"],
        ).splitlines()
        self.assertEqual(first_paths, ["3rdparty/waylib-shared"])
        self.assertEqual(
            sorted(dual_paths),
            ["3rdparty/waylib-shared", "compositor/src/app.cpp"],
        )
        final_gitlink = run(
            request.parent_worktree,
            "rev-parse",
            "HEAD:3rdparty/waylib-shared",
        )
        self.assertEqual(final_gitlink, second["child"]["commit"])
        child_message = run(
            request.child_worktree, "show", "-s", "--format=%B", second["child"]["commit"]
        )
        parent_message = run(
            request.parent_worktree, "show", "-s", "--format=%B", second["parent"]["commit"]
        )
        self.assertNotIn(second["parent"]["commit"], child_message)
        self.assertIn(second["child"]["commit"], parent_message)
        traces = build_waylib_traces(
            request.child_worktree,
            self.child_base,
            manifest["final_child_head"],
            inventory,
            self.source,
        )
        verify = verify_waylib_sync(
            request.child_worktree,
            self.child_base,
            manifest["final_child_head"],
            inventory,
            traces,
            read_json(request.waylib_evidence_path),
            request.artifact_root,
            self.source,
        )
        self.assertEqual(verify["outcome"], "pass")

    def test_preserves_blank_lines_in_original_message_trace(self) -> None:
        source_sha = commit_files(
            self.source,
            {"src/blank.cpp": "blank\n"},
            "fix(core): preserve message\n\nfirst paragraph\n\nsecond paragraph",
        )
        inventory = build_unified_inventory(
            self.source,
            self.source_base,
            source_sha,
            self.policy,
            self.policy_path,
            set(),
        )
        request = self.request(inventory, "blank-message")

        manifest = run_replay(request)

        self.assertEqual(manifest["outcome"], "pass")
        parent_sha = manifest["entries"][0]["parent"]["commit"]
        message = run(request.parent_worktree, "show", "-s", "--format=%B", parent_sha)
        self.assertIn(
            "Original treeland commit:\n"
            "    fix(core): preserve message\n"
            "    \n"
            "    first paragraph\n"
            "    \n"
            "    second paragraph\n",
            message,
        )
        parent, child = self.verify_lanes(request, manifest)
        self.assertEqual(parent["outcome"], "pass")
        self.assertEqual(child["outcome"], "pass")

    def test_resume_after_child_checkpoint_does_not_duplicate_child_commit(self) -> None:
        waylib_only, _dual, _parent_only, inventory = self.prepare_source()
        request = self.request(inventory, "resume")

        def interrupt(stage: str, source: str, _commit: str) -> None:
            if stage == "child" and source == waylib_only:
                raise RuntimeError("injected stop")

        with self.assertRaises(ReplayBlocked):
            run_replay(request, stage_hook=interrupt)
        child_after_stop = run(request.child_worktree, "rev-parse", "HEAD")

        manifest = run_replay(request, resume=True)

        first = manifest["entries"][0]
        self.assertEqual(first["child"]["commit"], child_after_stop)
        self.assertEqual(
            run(
                request.child_worktree,
                "rev-list",
                "--count",
                f"{self.child_base}..HEAD",
            ),
            "2",
        )
        journal = read_json(request.journal_path)
        self.assertEqual(journal["outcome"], "pass")
        self.assertIsNone(journal["blocked"])

    def test_resume_rejects_identity_drift_without_mutating_heads(self) -> None:
        waylib_only, _dual, _parent_only, inventory = self.prepare_source()
        request = self.request(inventory, "identity")

        def interrupt(stage: str, source: str, _commit: str) -> None:
            if stage == "child" and source == waylib_only:
                raise RuntimeError("injected stop")

        with self.assertRaises(ReplayBlocked):
            run_replay(request, stage_hook=interrupt)
        parent_before = run(request.parent_worktree, "rev-parse", "HEAD")
        child_before = run(request.child_worktree, "rev-parse", "HEAD")
        changed = copy.deepcopy(inventory)
        changed["commits"][0]["subject"] += " changed"
        request.inventory = changed

        with self.assertRaisesRegex(ReplayBlocked, "inventory path projection differs from source Git objects"):
            run_replay(request, resume=True)

        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), parent_before)
        self.assertEqual(run(request.child_worktree, "rev-parse", "HEAD"), child_before)

    def test_resume_rejects_corrupted_checkpoint_sequence(self) -> None:
        waylib_only, _dual, _parent_only, inventory = self.prepare_source()
        request = self.request(inventory, "corrupt-journal")

        def interrupt(stage: str, source: str, _commit: str) -> None:
            if stage == "child" and source == waylib_only:
                raise RuntimeError("injected stop")

        with self.assertRaises(ReplayBlocked):
            run_replay(request, stage_hook=interrupt)
        parent_before = run(request.parent_worktree, "rev-parse", "HEAD")
        child_before = run(request.child_worktree, "rev-parse", "HEAD")
        journal = read_json(request.journal_path)
        journal["next_sequence"] = 99
        request.journal_path.write_text(json.dumps(journal), encoding="utf-8")

        with self.assertRaisesRegex(ReplayBlocked, "event sequence"):
            run_replay(request, resume=True)

        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), parent_before)
        self.assertEqual(run(request.child_worktree, "rev-parse", "HEAD"), child_before)

    def test_rejects_non_worktree_targets_before_mutation(self) -> None:
        _one, _two, _three, inventory = self.prepare_source()
        artifacts = self.root / "unsafe-artifacts"
        request = ReplayRequest(
            source_repo=self.source,
            parent_worktree=self.parent,
            child_worktree=self.child,
            parent_base=self.parent_base,
            child_base=self.child_base,
            inventory=inventory,
            artifact_root=artifacts,
            journal_path=artifacts / "journal.json",
            manifest_path=artifacts / "manifest.json",
            waylib_evidence_path=artifacts / "waylib-evidence.json",
            parent_evidence_path=artifacts / "parent-evidence.json",
            run_id="unsafe",
            refs_doc="plans/test/plan.md",
            decisions={},
            allow_ephemeral_artifacts=True,
        )

        with self.assertRaisesRegex(ReplayBlocked, "linked worktree"):
            run_replay(request)

        self.assertEqual(run(self.parent, "rev-parse", "HEAD"), self.parent_base)
        self.assertEqual(run(self.child, "rev-parse", "HEAD"), self.child_base)

    def test_rejects_primary_worktree_with_gitfile_layout(self) -> None:
        _one, _two, _three, inventory = self.prepare_source()
        primary = init_repo_with_separate_git_dir(
            self.root / "gitfile-primary", self.root / "gitfile-primary.git"
        )
        run(
            primary,
            "update-index",
            "--add",
            "--cacheinfo",
            f"160000,{self.child_base},3rdparty/waylib-shared",
        )
        run(primary, "commit", "-m", "parent base")
        primary_base = run(primary, "rev-parse", "HEAD")
        request = self.request(inventory, "gitfile-primary")
        request.parent_worktree = primary
        request.parent_base = primary_base

        with self.assertRaisesRegex(ReplayBlocked, "secondary linked worktree"):
            run_replay(request)

        self.assertEqual(run(primary, "rev-parse", "HEAD"), primary_base)
        self.assertFalse(request.journal_path.exists())

    def test_rejects_unknown_decision_before_creating_journal(self) -> None:
        _one, _two, _three, inventory = self.prepare_source()
        request = self.request(inventory, "bad-decision")
        request.decisions = {
            "entries": {
                "f" * 40: {
                    "child": {"action": "empty", "equivalence_proof": {}}
                }
            }
        }

        with self.assertRaisesRegex(ReplayBlocked, "unknown source commit"):
            run_replay(request)

        self.assertFalse(request.journal_path.exists())
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.parent_base)
        self.assertEqual(run(request.child_worktree, "rev-parse", "HEAD"), self.child_base)

    def test_rejects_malformed_inventory_before_creating_journal(self) -> None:
        _one, _two, _three, inventory = self.prepare_source()
        request = self.request(inventory, "malformed-inventory")
        request.inventory = copy.deepcopy(inventory)
        request.inventory["commits"][0] = "not-an-object"

        with self.assertRaisesRegex(ReplayBlocked, r"inventory commit\[0\]"):
            run_replay(request)

        self.assertFalse(request.journal_path.exists())

    def test_rejects_malformed_decision_details_before_creating_journal(self) -> None:
        waylib_only, _two, _three, inventory = self.prepare_source()
        request = self.request(inventory, "malformed-decision")
        patch = write_artifact(
            request.artifact_root,
            "decisions/child.patch",
            b"not used because preflight must reject notes\n",
        )
        request.decisions = {
            "entries": {
                waylib_only: {
                    "child": {
                        "action": "adapted",
                        "adaptation_notes": "must be an array",
                        "adaptation_patch": patch,
                    }
                }
            }
        }

        with self.assertRaisesRegex(ReplayBlocked, "adaptation_notes"):
            run_replay(request)

        self.assertFalse(request.journal_path.exists())

    def test_rejects_message_metadata_injection_before_creating_journal(self) -> None:
        waylib_only, _two, _three, inventory = self.prepare_source()
        unsafe_run = self.request(inventory, "unsafe-run-id")
        unsafe_run.run_id = "run\nTreeland-Commit: " + waylib_only

        with self.assertRaisesRegex(ReplayBlocked, "run-id"):
            run_replay(unsafe_run)
        self.assertFalse(unsafe_run.journal_path.exists())

        unsafe_note = self.request(inventory, "unsafe-note")
        unsafe_note.decisions = {
            "entries": {
                waylib_only: {
                    "child": {
                        "action": "applied",
                        "adaptation_notes": ["note\n[treeland-unified-sync] action: empty"],
                    }
                }
            }
        }

        with self.assertRaisesRegex(ReplayBlocked, "single-line"):
            run_replay(unsafe_note)
        self.assertFalse(unsafe_note.journal_path.exists())

    def test_rejects_a_noncanonical_gitlink_path_before_creating_journal(self) -> None:
        _one, _two, _three, inventory = self.prepare_source()
        request = self.request(inventory, "unsafe-gitlink")
        request.gitlink_path = "3rdparty/another-submodule"

        with self.assertRaisesRegex(ReplayBlocked, "gitlink path"):
            run_replay(request)

        self.assertFalse(request.journal_path.exists())

    def test_rejects_source_already_mapped_in_frozen_baseline(self) -> None:
        waylib_only, _dual, _parent_only, inventory = self.prepare_source()
        self.child_base = commit_files(
            self.child,
            {"qwlroots/existing.cpp": "existing\n"},
            "existing sync\n\nTreeland-Commit: " + waylib_only,
        )
        run(
            self.parent,
            "update-index",
            "--add",
            "--cacheinfo",
            f"160000,{self.child_base},3rdparty/waylib-shared",
        )
        run(self.parent, "commit", "-m", "update baseline gitlink")
        self.parent_base = run(self.parent, "rev-parse", "HEAD")
        request = self.request(inventory, "duplicate-source")

        with self.assertRaisesRegex(ReplayBlocked, "already mapped"):
            run_replay(request)

        self.assertFalse(request.journal_path.exists())

    def test_rejects_legacy_cherry_pick_mapping_in_frozen_baseline(self) -> None:
        source_sha = commit_files(
            self.source, {"src/already-synced.cpp": "synced\n"}, "source change"
        )
        inventory = build_unified_inventory(
            self.source,
            self.source_base,
            source_sha,
            self.policy,
            self.policy_path,
            set(),
        )
        target = self.parent / "compositor/src/already-synced.cpp"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("synced\n", encoding="utf-8")
        run(self.parent, "add", "compositor/src/already-synced.cpp")
        run(
            self.parent,
            "commit",
            "-m",
            f"legacy sync\n\n(cherry picked from commit {source_sha})",
        )
        self.parent_base = run(self.parent, "rev-parse", "HEAD")
        request = self.request(inventory, "legacy-duplicate")
        request.decisions = {"entries": {source_sha: {"parent": {
            "action": "empty",
            "equivalence_proof": write_artifact(
                request.artifact_root, "legacy-equivalence.txt",
                b"The frozen parent already contains the source content.\n",
            ),
        }}}}

        with self.assertRaisesRegex(ReplayBlocked, "legacy cherry-pick"):
            run_replay(request)

        self.assertFalse(request.journal_path.exists())

    def test_rejects_child_legacy_overlap_but_not_unrelated_history(self) -> None:
        source_sha, _dual, _parent, inventory = self.prepare_source()
        self.child_base = commit_files(
            self.child, {"qwlroots/already.cpp": "base\n"},
            f"unrelated history\n\n(cherry picked from commit {self.source_base})",
        )
        run(self.parent, "update-index", "--cacheinfo", f"160000,{self.child_base},3rdparty/waylib-shared")
        run(self.parent, "commit", "-m", "advance child baseline")
        self.parent_base = run(self.parent, "rev-parse", "HEAD")
        run_static_preflight(self.request(inventory, "unrelated-legacy"))

        self.child_base = commit_files(
            self.child, {"qwlroots/a.cpp": "a\n"},
            f"legacy sync\n\n(cherry picked from commit {source_sha})",
        )
        run(self.parent, "update-index", "--cacheinfo", f"160000,{self.child_base},3rdparty/waylib-shared")
        run(self.parent, "commit", "-m", "advance child mapping")
        self.parent_base = run(self.parent, "rev-parse", "HEAD")
        request = self.request(inventory, "child-legacy")

        with self.assertRaisesRegex(ReplayBlocked, "legacy cherry-pick mapping in child"):
            run_replay(request)

        self.assertFalse(request.journal_path.exists())
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.parent_base)
        self.assertEqual(run(request.child_worktree, "rev-parse", "HEAD"), self.child_base)

    def test_replays_reviewed_adapted_omissions_and_checks_path_dispositions(self) -> None:
        source_sha = commit_files(
            self.source,
            {f"{directory}/{name}.cpp": "source\n"
             for directory in ("src", "qwlroots") for name in ("kept", "omitted")},
            "dual adaptation",
        )
        inventory = build_unified_inventory(
            self.source, self.source_base, source_sha, self.policy, self.policy_path, set(),
        )
        request = self.request(inventory, "reviewed-adaptation")
        decisions = {}
        for lane, directory in (("parent", "compositor/src"), ("child", "qwlroots")):
            kept = f"{directory}/kept.cpp"
            omitted = f"{directory}/omitted.cpp"
            patch_repo = init_repo(self.root / f"adapted-patch-{lane}")
            commit_files(patch_repo, {"README": "fixture\n"}, "base")
            patch_commit = commit_files(patch_repo, {kept: "adapted\n"}, "reviewed content")
            proof = write_artifact(
                request.artifact_root, f"decisions/{lane}-review.txt",
                f"Approved {kept} adaptation and intentional exclusion of {omitted}.\n".encode(),
            )
            decisions[lane] = {
                "action": "adapted",
                "adaptation_notes": ["Retain the reviewed subset for the target."],
                "adaptation_patch": write_artifact(
                    request.artifact_root, f"decisions/{lane}.patch",
                    source_patch(patch_repo, patch_commit, [kept]),
                ),
                "adaptation_paths": [
                    {"path": kept, "kind": "materialized", "reason": "Add the target-specific implementation.",
                     "proof": proof, "review_state": "approved"},
                    {"path": omitted, "kind": "omitted", "reason": "Exclude the reviewed source-only implementation.",
                     "proof": proof, "review_state": "approved"},
                ],
            }
        request.decisions = {"entries": {source_sha: decisions}}
        valid = copy.deepcopy(request.decisions)
        for lane in decisions:
            request.decisions = copy.deepcopy(valid)
            request.decisions["entries"][source_sha][lane]["adaptation_paths"].pop()
            with self.subTest(lane=lane), self.assertRaisesRegex(ReplayBlocked, "cover inventory"):
                run_replay(request)
            self.assertFalse(request.journal_path.exists())
        request.decisions = valid

        manifest = run_replay(request)
        for result in self.verify_lanes(request, manifest):
            self.assertEqual(result["outcome"], "pass", msg=result["blocked_reasons"])
        for path in (request.parent_evidence_path, request.waylib_evidence_path):
            evidence = read_json(path)
            evidence["entries"][0]["adaptation_paths"][0]["kind"] = "omitted"
            path.write_text(json.dumps(evidence), encoding="utf-8")
        for result in self.verify_lanes(request, manifest):
            self.assertEqual(result["outcome"], "blocked")
            self.assertTrue(any("omitted adaptation path appears" in error for error in result["blocked_reasons"]))

    def test_rejects_adapted_decision_without_complete_path_review(self) -> None:
        source_sha = commit_files(
            self.source, {"qwlroots/adapted.cpp": "adapted\n"}, "adapted"
        )
        inventory = build_unified_inventory(
            self.source,
            self.source_base,
            source_sha,
            self.policy,
            self.policy_path,
            set(),
        )
        request = self.request(inventory, "missing-adaptation-paths")
        patch = write_artifact(
            request.artifact_root,
            "decisions/adapted.patch",
            b"non-empty artifact required by the current decision contract\n",
        )
        request.decisions = {
            "entries": {
                source_sha: {
                    "child": {
                        "action": "adapted",
                        "adaptation_notes": ["Reviewed target adaptation."],
                        "adaptation_patch": patch,
                    }
                }
            }
        }

        with self.assertRaisesRegex(ReplayBlocked, "adaptation_paths"):
            run_static_preflight(request)

        self.assertFalse(request.journal_path.exists())
        path = {
            "path": "qwlroots/adapted.cpp", "kind": "materialized",
            "reason": "Approved target implementation.", "proof": patch,
            "review_state": "approved",
        }
        decision = request.decisions["entries"][source_sha]["child"]
        for field, value in (("kind", {}), ("review_state", "pending"),
                             ("reason", " "), ("proof", {"path": "../outside.txt"})):
            decision["adaptation_paths"] = [dict(path, **{field: value})]
            with self.subTest(field=field), self.assertRaises(ReplayBlocked):
                run_static_preflight(request)
        decision["adaptation_paths"] = [path, path]
        with self.assertRaisesRegex(ReplayBlocked, "duplicate"):
            run_static_preflight(request)
        self.assertFalse(request.journal_path.exists())

    def test_blocks_intermediate_child_contract_drift_before_parent_replay(self) -> None:
        self.assert_intermediate_contract_blocked(
            "add_library(Core INTERFACE)\n", "add_library(BrokenCore INTERFACE)\n",
        )

    def test_blocks_intermediate_variable_contract_drift_before_parent_replay(self) -> None:
        self.assert_intermediate_contract_blocked(
            "set(TARGET_NAME Core)\nadd_library(${TARGET_NAME} INTERFACE)\n",
            "set(TARGET_NAME BrokenCore)\nadd_library(${TARGET_NAME} INTERFACE)\n",
        )

    def assert_intermediate_contract_blocked(self, source_contract, changed_contract) -> None:
        self.source_base = commit_files(
            self.source,
            {"waylib/CMakeLists.txt": source_contract},
            "source contract base",
        )
        self.child_base = commit_files(
            self.child,
            {"waylib/CMakeLists.txt": source_contract},
            "child contract base",
        )
        run(
            self.parent,
            "update-index",
            "--add",
            "--cacheinfo",
            f"160000,{self.child_base},3rdparty/waylib-shared",
        )
        run(self.parent, "commit", "-m", "advance child contract baseline")
        self.parent_base = run(self.parent, "rev-parse", "HEAD")
        changed = commit_files(
            self.source,
            {"waylib/CMakeLists.txt": changed_contract},
            "change child contract",
        )
        restored = commit_files(
            self.source,
            {"waylib/CMakeLists.txt": source_contract},
            "restore child contract",
        )
        inventory = build_unified_inventory(
            self.source,
            self.source_base,
            restored,
            self.policy,
            self.policy_path,
            set(),
        )
        request = self.request(inventory, "intermediate-contract")

        with self.assertRaisesRegex(ReplayBlocked, "source contract drift"):
            run_replay(request)

        journal = read_json(request.journal_path)
        first = journal["nodes"][changed]
        self.assertIsNotNone(first["child"]["commit"])
        self.assertIsNone(first["parent"]["commit"])
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.parent_base)
        self.assertEqual(run(request.child_worktree, "rev-parse", "HEAD"), first["child"]["commit"])
        with self.assertRaisesRegex(ReplayBlocked, "source contract drift"):
            run_replay(request, resume=True)
        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.parent_base)

    def test_resume_rechecks_rehashed_child_contract_audit_before_parent(self) -> None:
        source_sha, _dual, _parent, inventory = self.prepare_source()
        request = self.request(inventory, "audit-integrity")

        def interrupt(lane, source, commit):
            raise RuntimeError("fixture interruption")

        with self.assertRaisesRegex(ReplayBlocked, "fixture interruption"):
            run_replay(request, stage_hook=interrupt)
        journal = read_json(request.journal_path)
        node = journal["nodes"][source_sha]
        record = node["artifacts"]["child"]["source_contract_audit"]
        audit = read_json(request.artifact_root / record["path"])
        audit["after_commit"] = self.child_base
        node["artifacts"]["child"]["source_contract_audit"] = write_artifact(
            request.artifact_root, record["path"], json.dumps(audit).encode(),
        )
        request.journal_path.write_text(json.dumps(journal), encoding="utf-8")

        with self.assertRaisesRegex(ReplayBlocked, "source contract audit differs from Git objects"):
            run_replay(request, resume=True)

        self.assertEqual(run(request.parent_worktree, "rev-parse", "HEAD"), self.parent_base)
        self.assertIsNone(read_json(request.journal_path)["nodes"][source_sha]["parent"]["commit"])

    def test_applied_projection_keeps_target_baseline_context(self) -> None:
        source_content = "int value = 1;\n" + "// shared context\n" * 10
        self.source_base = commit_files(
            self.source, {"src/value.cpp": source_content, "waylib/value.cpp": source_content},
            "source baseline",
        )
        local_content = source_content + "// target-only implementation detail\n"
        self.child_base = commit_files(
            self.child, {"waylib/value.cpp": local_content}, "child baseline",
        )
        target = self.parent / "compositor/src/value.cpp"
        target.parent.mkdir(parents=True)
        target.write_text(local_content, encoding="utf-8")
        run(self.parent, "add", "compositor/src/value.cpp")
        run(self.parent, "update-index", "--cacheinfo", f"160000,{self.child_base},3rdparty/waylib-shared")
        run(self.parent, "commit", "-m", "parent baseline")
        self.parent_base = run(self.parent, "rev-parse", "HEAD")
        source_sha = commit_files(
            self.source, {"src/value.cpp": source_content.replace("1", "2"),
                          "waylib/value.cpp": source_content.replace("1", "2")},
            "change value",
        )
        inventory = build_unified_inventory(
            self.source, self.source_base, source_sha, self.policy, self.policy_path, set(),
        )
        request = self.request(inventory, "target-context")

        manifest = run_replay(request)

        for result in self.verify_lanes(request, manifest):
            self.assertEqual(result["outcome"], "pass", msg=result["blocked_reasons"])
        self.assertEqual(
            (request.parent_worktree / "compositor/src/value.cpp").read_text(encoding="utf-8"),
            local_content.replace("1", "2"),
        )
        self.assertEqual(run(request.parent_worktree, "status", "--porcelain"), "")
        self.assertEqual(run(request.child_worktree, "status", "--porcelain"), "")

    def test_verifiers_reject_applied_content_not_matching_source_projection(self) -> None:
        source_sha = commit_files(
            self.source,
            {"waylib/value.cpp": "int value = 1;\n", "src/value.cpp": "int value = 1;\n"},
            "dual content",
        )
        inventory = build_unified_inventory(
            self.source,
            self.source_base,
            source_sha,
            self.policy,
            self.policy_path,
            set(),
        )
        request = self.request(inventory, "content-projection")
        for name, worktree, path in (
            ("child", request.child_worktree, "waylib/value.cpp"),
            ("parent", request.parent_worktree, "compositor/src/value.cpp"),
        ):
            hooks = self.root / f"{name}-hooks"
            hooks.mkdir()
            hook = hooks / "pre-commit"
            hook.write_text(
                "#!/bin/sh\n"
                f"printf 'int value = 999;\\n' > '{path}'\n"
                f"git add -- '{path}'\n",
                encoding="utf-8",
            )
            hook.chmod(0o700)
            run(worktree, "config", "core.hooksPath", str(hooks))

        manifest = run_replay(request)
        parent = verify_parent_sync(
            self.source,
            request.parent_worktree,
            self.parent_base,
            manifest["final_parent_head"],
            inventory,
            manifest,
            read_json(request.parent_evidence_path),
            request.artifact_root,
        )
        traces = build_waylib_traces(
            request.child_worktree,
            self.child_base,
            manifest["final_child_head"],
            inventory,
            self.source,
        )
        child = verify_waylib_sync(
            request.child_worktree,
            self.child_base,
            manifest["final_child_head"],
            inventory,
            traces,
            read_json(request.waylib_evidence_path),
            request.artifact_root,
            self.source,
        )

        self.assertEqual(manifest["outcome"], "pass")
        self.assertEqual(parent["outcome"], "blocked")
        self.assertEqual(child["outcome"], "blocked")
        self.assertTrue(
            any("content projection" in item for item in parent["blocked_reasons"])
        )
        self.assertTrue(
            any("content projection" in item for item in child["blocked_reasons"])
        )

    def test_rejects_source_repo_or_path_policy_drift_before_journal(self) -> None:
        _one, _two, _three, inventory = self.prepare_source()
        source_mismatch = self.request(inventory, "source-mismatch")
        source_mismatch.inventory = copy.deepcopy(inventory)
        source_mismatch.inventory["source_repo"] = str(self.child.resolve())

        with self.assertRaisesRegex(ReplayBlocked, "source_repo differs"):
            run_replay(source_mismatch)
        self.assertFalse(source_mismatch.journal_path.exists())

        policy_mismatch = self.request(inventory, "policy-mismatch")
        self.policy_path.write_text("changed after inventory\n", encoding="utf-8")

        with self.assertRaisesRegex(ReplayBlocked, "path-policy"):
            run_replay(policy_mismatch)
        self.assertFalse(policy_mismatch.journal_path.exists())

    def test_replays_explicit_empty_child_with_hashed_equivalence_proof(self) -> None:
        source_sha = commit_files(
            self.source, {"qwlroots/equivalent.cpp": "already present\n"}, "equivalent"
        )
        inventory = build_unified_inventory(
            self.source,
            self.source_base,
            source_sha,
            self.policy,
            self.policy_path,
            set(),
        )
        request = self.request(inventory, "empty")
        proof = write_artifact(
            request.artifact_root,
            f"decisions/{source_sha}-child-equivalence.md",
            b"Reviewed equivalence against the frozen child baseline.\n",
        )
        request.decisions = {
            "entries": {
                source_sha: {
                    "child": {
                        "action": "empty",
                        "adaptation_notes": ["Equivalent implementation already exists."],
                        "equivalence_proof": proof,
                    }
                }
            }
        }

        manifest = run_replay(request)

        entry = manifest["entries"][0]
        self.assertEqual(entry["child"]["action"], "empty")
        self.assertEqual(entry["parent"]["action"], "gitlink-only")
        self.assertEqual(
            run(
                request.child_worktree,
                "diff-tree",
                "--no-commit-id",
                "--name-only",
                "-r",
                entry["child"]["commit"],
            ),
            "",
        )

    def test_replays_parent_empty_with_a_top_level_equivalence_proof(self) -> None:
        source_sha = commit_files(
            self.source,
            {"waylib/child.cpp": "child\n", "src/equivalent.cpp": "equivalent\n"},
            "dual with equivalent parent",
        )
        inventory = build_unified_inventory(
            self.source,
            self.source_base,
            source_sha,
            self.policy,
            self.policy_path,
            set(),
        )
        request = self.request(inventory, "parent-empty")
        proof = write_artifact(
            request.artifact_root,
            f"decisions/{source_sha}-parent-equivalence.md",
            b"Reviewed equivalence against the frozen parent baseline.\n",
        )
        request.decisions = {
            "entries": {
                source_sha: {
                    "parent": {
                        "action": "empty",
                        "adaptation_notes": ["Equivalent parent behavior already exists."],
                        "equivalence_proof": proof,
                    }
                }
            }
        }

        manifest = run_replay(request)
        evidence = read_json(request.parent_evidence_path)
        entry = evidence["entries"][0]

        self.assertIn("equivalence_proof", entry)
        self.assertNotIn("equivalence_proof", entry["artifacts"])
        result = verify_parent_sync(
            self.source,
            request.parent_worktree,
            self.parent_base,
            manifest["final_parent_head"],
            inventory,
            manifest,
            evidence,
            request.artifact_root,
        )
        self.assertEqual(result["outcome"], "pass")


if __name__ == "__main__":
    unittest.main()
