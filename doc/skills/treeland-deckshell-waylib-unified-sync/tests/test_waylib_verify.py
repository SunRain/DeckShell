from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Dict, List

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from unified_sync_lib.git_ops import commit_changes
from unified_sync_lib.patches import commit_diff, source_patch
from unified_sync_lib.traces import build_waylib_traces
from unified_sync_lib.evidence import verify_waylib_sync
from unified_sync_lib.contracts import build_source_contract_audit

from support import commit_files, init_repo, run


def source_entry(sha: str, classification: str, path: str) -> Dict:
    parent_included = classification == "dual"
    return {
        "source_commit": sha,
        "subject": "fixture",
        "classification": classification,
        "changes": [],
        "deckshell": {
            "included": parent_included,
            "mapped_source_paths": ["src/fixture.cpp"] if parent_included else [],
            "root_source_paths": [],
            "target_paths": ["compositor/src/fixture.cpp"] if parent_included else [],
            "drop_paths": [path],
        },
        "waylib_shared": {
            "included": True,
            "source_paths": [path],
            "drop_paths": [],
        },
        "wlroots": {"included": False, "source_paths": [], "target_paths": [], "drop_paths": [path]},
        "protocol_source_paths": [],
        "protocol_target_paths": [],
        "blocked_reasons": [],
    }


class WaylibVerifyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.source = init_repo(self.root / "source")
        self.child = init_repo(self.root / "child")
        self.source_base = commit_files(self.source, {"README": "base\n"}, "base")
        self.child_base = commit_files(self.child, {"README": "base\n"}, "base")
        self.artifacts = self.root / "artifacts"
        self.artifacts.mkdir()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def source_commit(self, path: str, content: str, message: str) -> str:
        return commit_files(self.source, {path: content}, message)

    def child_commit(
        self,
        source_sha: str,
        classification: str,
        action: str,
        files: Dict[str, str],
    ) -> str:
        subject = run(self.source, "show", "-s", "--format=%s", source_sha)
        original = run(self.source, "show", "-s", "--format=%B", source_sha)
        original_block = "\n".join(f"    {line}" for line in original.splitlines())
        message = (
            f"{subject}\n\n"
            f"Original treeland commit:\n{original_block}\n\n"
            f"[treeland-unified-sync] classification: {classification}\n"
            f"[treeland-unified-sync] action: {action}\n"
            f"[treeland-unified-sync] content action: {action}\n"
            "[treeland-unified-sync] lane: child\n"
            "[treeland-unified-sync] nested gitlink: null\n"
            "[treeland-unified-sync] drop files:\n- none\n"
            "[treeland-unified-sync] adaptation paths:\n- none\n"
            "[treeland-unified-sync] adaptation notes:\n- none\n"
            "[treeland-unified-sync] parent association: manifest-only\n"
            "[treeland-unified-sync] run-id: test\n\n"
            f"Treeland-Commit: {source_sha}\n"
        )
        if files:
            return commit_files(self.child, files, message)
        env = {
            "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+00:00",
            "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+00:00",
        }
        run(self.child, "commit", "--allow-empty", "-m", message, env=env)
        return run(self.child, "rev-parse", "HEAD")

    def inventory(self, entries: List[Dict]) -> Dict:
        ordered = [item["source_commit"] for item in entries]
        head = entries[-1]["source_commit"] if entries else self.source_base
        return {
            "schema_version": 2,
            "kind": "treeland-deckshell-waylib-unified-inventory",
            "outcome": "pass",
            "source_repo": str(self.source.resolve()),
            "range": {
                "base": self.source_base,
                "head": head,
                "source_tip": head,
                "ordered_source_commits": ordered,
                "ordered_sha256": hashlib.sha256(
                    "".join(f"{item}\n" for item in ordered).encode("ascii")
                ).hexdigest(),
                "merge_commits": [],
            },
            "path_policy": {"path": "/fixture/path-policy.md", "sha256": "5" * 64},
            "approved_review": [],
            "child_owned_roots": ["qwlroots", "waylib", "wlroots"],
            "wlroots_owned_root": "3rdparty/wlroots",
            "counts": {
                name: sum(item["classification"] == name for item in entries)
                for name in (
                    "deckshell-only",
                    "waylib-only",
                    "dual",
                    "unowned-skip",
                    "blocked",
                )
            },
            "blocked_reasons": [],
            "commits": entries,
        }

    def artifact(self, name: str, content: bytes = b"proof\n") -> Dict:
        path = self.artifacts / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return {
            "path": name,
            "size": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
        }

    def evidence_entry(
        self,
        source_sha: str,
        target_sha: str,
        classification: str,
        action: str,
    ) -> Dict:
        paths = []
        for change in commit_changes(self.source, source_sha):
            paths.extend(
                path for path in (change.old_path, change.new_path) if path is not None
            )
        artifacts = {
            "source_patch": self.artifact(
                f"{source_sha}/source.patch",
                source_patch(self.source, source_sha, paths),
            ),
            "target_diff": self.artifact(
                f"{source_sha}/target.diff", commit_diff(self.child, target_sha)
            ),
            "source_contract_audit": self.artifact(
                f"{source_sha}/source-contract-audit.json",
                (json.dumps(
                    build_source_contract_audit(self.child, f"{target_sha}^", target_sha),
                    ensure_ascii=True,
                    indent=2,
                ) + "\n").encode("utf-8"),
            ),
        }
        entry = {
            "source_commit": source_sha,
            "target_commit": target_sha,
            "classification": classification,
            "action": action,
            "drop_paths": [],
            "adaptation_notes": ["none"],
            "artifacts": artifacts,
        }
        if action == "empty":
            entry["equivalence_proof"] = self.artifact(
                f"{source_sha}/equivalence.md"
            )
        return entry

    def test_accepts_ordered_applied_and_empty_mapping(self) -> None:
        source_one = self.source_commit("qwlroots/a.cpp", "a\n", "one")
        source_two = self.source_commit("waylib/b.cpp", "b\n", "two")
        inventory = self.inventory(
            [
                source_entry(source_one, "waylib-only", "qwlroots/a.cpp"),
                source_entry(source_two, "dual", "waylib/b.cpp"),
            ]
        )
        child_one = self.child_commit(
            source_one, "waylib-only", "applied", {"qwlroots/a.cpp": "a\n"}
        )
        child_two = self.child_commit(source_two, "dual", "empty", {})
        evidence = {
            "schema_version": 2,
            "kind": "treeland-unified-waylib-evidence",
            "entries": [
                self.evidence_entry(
                    source_one, child_one, "waylib-only", "applied"
                ),
                self.evidence_entry(source_two, child_two, "dual", "empty"),
            ],
        }

        traces = build_waylib_traces(
            self.child, self.child_base, child_two, inventory, self.source
        )
        result = verify_waylib_sync(
            self.child,
            self.child_base,
            child_two,
            inventory,
            traces,
            evidence,
            self.artifacts,
            self.source,
        )

        self.assertEqual(traces["outcome"], "pass")
        self.assertEqual(result["outcome"], "pass")
        self.assertEqual(result["verified_entries"], 2)

    def test_blocks_duplicate_and_out_of_order_source_mapping(self) -> None:
        source_one = self.source_commit("qwlroots/a.cpp", "a\n", "one")
        source_two = self.source_commit("waylib/b.cpp", "b\n", "two")
        inventory = self.inventory(
            [
                source_entry(source_one, "waylib-only", "qwlroots/a.cpp"),
                source_entry(source_two, "dual", "waylib/b.cpp"),
            ]
        )
        self.child_commit(source_two, "dual", "applied", {"waylib/b.cpp": "b\n"})
        head = self.child_commit(
            source_two, "dual", "applied", {"waylib/c.cpp": "c\n"}
        )

        traces = build_waylib_traces(
            self.child, self.child_base, head, inventory, self.source
        )

        self.assertEqual(traces["outcome"], "blocked")
        joined = "\n".join(traces["blocked_reasons"])
        self.assertIn("duplicate source mapping", joined)
        self.assertIn("source order mismatch", joined)

    def test_blocks_target_path_outside_child_roots(self) -> None:
        source_sha = self.source_commit("qwlroots/a.cpp", "a\n", "one")
        inventory = self.inventory(
            [source_entry(source_sha, "waylib-only", "qwlroots/a.cpp")]
        )
        child_sha = self.child_commit(
            source_sha, "waylib-only", "applied", {"docs/leak.md": "leak\n"}
        )

        traces = build_waylib_traces(
            self.child, self.child_base, child_sha, inventory, self.source
        )

        self.assertEqual(traces["outcome"], "blocked")
        self.assertTrue(
            any("path boundary violation" in item for item in traces["blocked_reasons"])
        )

    def test_requires_adaptation_notes_and_empty_equivalence_proof(self) -> None:
        source_one = self.source_commit("qwlroots/a.cpp", "a\n", "one")
        source_two = self.source_commit("waylib/b.cpp", "b\n", "two")
        inventory = self.inventory(
            [
                source_entry(source_one, "waylib-only", "qwlroots/a.cpp"),
                source_entry(source_two, "dual", "waylib/b.cpp"),
            ]
        )
        child_one = self.child_commit(
            source_one, "waylib-only", "adapted", {"qwlroots/a.cpp": "adapted\n"}
        )
        child_two = self.child_commit(source_two, "dual", "empty", {})
        adapted = self.evidence_entry(
            source_one, child_one, "waylib-only", "adapted"
        )
        adapted["adaptation_notes"] = ["none"]
        adapted["artifacts"]["adaptation_patch"] = self.artifact(
            f"{source_one}/adaptation.patch"
        )
        adapted["adaptation_paths"] = [
            {
                "kind": "materialized",
                "path": "qwlroots/a.cpp",
                "reason": "Create the canonical child path.",
                "proof": self.artifact(f"{source_one}/adaptation-proof.md"),
                "review_state": "approved",
            }
        ]
        empty = self.evidence_entry(source_two, child_two, "dual", "empty")
        del empty["equivalence_proof"]
        evidence = {
            "schema_version": 2,
            "kind": "treeland-unified-waylib-evidence",
            "entries": [adapted, empty],
        }
        traces = build_waylib_traces(
            self.child, self.child_base, child_two, inventory, self.source
        )

        result = verify_waylib_sync(
            self.child,
            self.child_base,
            child_two,
            inventory,
            traces,
            evidence,
            self.artifacts,
            self.source,
        )

        self.assertEqual(result["outcome"], "blocked")
        joined = "\n".join(result["blocked_reasons"])
        self.assertIn("adapted action requires substantive adaptation notes", joined)
        self.assertIn("equivalence_proof must be an artifact object", joined)

    def test_blocks_path_expansion_inside_child_roots(self) -> None:
        source_sha = self.source_commit("qwlroots/a.cpp", "a\n", "one")
        inventory = self.inventory(
            [source_entry(source_sha, "waylib-only", "qwlroots/a.cpp")]
        )
        child_sha = self.child_commit(
            source_sha, "waylib-only", "applied", {"qwlroots/other.cpp": "a\n"}
        )
        evidence = {
            "schema_version": 2,
            "kind": "treeland-unified-waylib-evidence",
            "entries": [
                self.evidence_entry(
                    source_sha, child_sha, "waylib-only", "applied"
                )
            ],
        }
        traces = build_waylib_traces(
            self.child, self.child_base, child_sha, inventory, self.source
        )

        result = verify_waylib_sync(
            self.child,
            self.child_base,
            child_sha,
            inventory,
            traces,
            evidence,
            self.artifacts,
            self.source,
        )

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(
            any("child path expansion" in item for item in result["blocked_reasons"])
        )

    def test_blocks_child_author_identity_drift(self) -> None:
        source_sha = self.source_commit("qwlroots/a.cpp", "a\n", "one")
        inventory = self.inventory(
            [source_entry(source_sha, "waylib-only", "qwlroots/a.cpp")]
        )
        run(self.child, "config", "user.name", "Different Author")
        child_sha = self.child_commit(
            source_sha, "waylib-only", "applied", {"qwlroots/a.cpp": "a\n"}
        )

        traces = build_waylib_traces(
            self.child, self.child_base, child_sha, inventory, self.source
        )

        self.assertEqual(traces["outcome"], "blocked")
        self.assertTrue(
            any("author identity/date mismatch" in item for item in traces["blocked_reasons"])
        )


if __name__ == "__main__":
    unittest.main()
