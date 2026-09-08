from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
import json
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from unified_sync_lib.git_ops import canonical_json_sha256
from unified_sync_lib.materialization import (
    MaterializationBlocked,
    materialize_child_checkout,
)

from support import add_worktree, commit_files, init_repo, run


GITLINK_PATH = "3rdparty/waylib-shared"


class MaterializationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        source_child = init_repo(self.root / "child-source")
        commit_files(source_child, {"CMakeLists.txt": "# base\n"}, "child base")

        self.parent = init_repo(self.root / "parent")
        subprocess.run(
            [
                "git",
                "-C",
                str(self.parent),
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "add",
                str(source_child),
                GITLINK_PATH,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        commit_files(self.parent, {}, "parent base")
        self.child_repo = self.parent / GITLINK_PATH
        self.child_base = run(self.child_repo, "rev-parse", "HEAD")
        self.child_wt = add_worktree(
            self.child_repo,
            self.root / "child-wt",
            "candidate-child",
            self.child_base,
        )
        self.child_candidate = commit_files(
            self.child_wt,
            {"CMakeLists.txt": "# candidate\n"},
            "child candidate",
        )

        self.parent_wt = add_worktree(
            self.parent,
            self.root / "parent-wt",
            "candidate-parent",
            run(self.parent, "rev-parse", "HEAD"),
        )
        run(
            self.parent_wt,
            "update-index",
            "--cacheinfo",
            f"160000,{self.child_candidate},{GITLINK_PATH}",
        )
        run(self.parent_wt, "commit", "-m", "point to child candidate")
        self.parent_candidate = run(self.parent_wt, "rev-parse", "HEAD")
        self.manifest = {
            "schema_version": 2,
            "kind": "treeland-unified-sync-manifest",
            "outcome": "pass",
            "identity": {"parent_worktree": str(self.parent_wt.resolve())},
            "final_parent_head": self.parent_candidate,
            "final_child_head": self.child_candidate,
            "entries": [],
        }

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_materializes_local_only_candidate_and_is_idempotent(self) -> None:
        destination = self.parent_wt / GITLINK_PATH

        created = materialize_child_checkout(
            self.parent_wt, self.child_repo, self.manifest
        )
        verified = materialize_child_checkout(
            self.parent_wt, self.child_repo, self.manifest
        )

        self.assertEqual(created["status"], "created")
        self.assertEqual(verified["status"], "verified")
        self.assertEqual(created["manifest_sha256"], canonical_json_sha256(self.manifest))
        self.assertEqual(run(destination, "rev-parse", "HEAD"), self.child_candidate)
        self.assertEqual(run(self.parent_wt, "status", "--short"), "")
        self.assertTrue(created["checkout"]["linked_worktree"])
        self.assertTrue(created["checkout"]["clean"])

    def test_rejects_existing_checkout_at_wrong_commit_without_resetting_it(self) -> None:
        destination = self.parent_wt / GITLINK_PATH
        run(
            self.child_repo,
            "worktree",
            "add",
            "--detach",
            str(destination),
            self.child_base,
        )

        with self.assertRaisesRegex(
            MaterializationBlocked, "checkout HEAD differs from final child"
        ):
            materialize_child_checkout(self.parent_wt, self.child_repo, self.manifest)

        self.assertEqual(run(destination, "rev-parse", "HEAD"), self.child_base)

    def test_cli_writes_materialization_evidence(self) -> None:
        output = self.root / "materialization.json"
        manifest_path = self.root / "manifest.json"
        manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "unified_sync.py"),
                "materialize-child",
                "--parent-worktree",
                str(self.parent_wt),
                "--child-repo",
                str(self.child_repo),
                "--manifest",
                str(manifest_path),
                "--output",
                str(output),
            ],
            cwd=str(SCRIPTS.parent),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(payload["outcome"], "pass")
        self.assertEqual(payload["child_head"], self.child_candidate)


if __name__ == "__main__":
    unittest.main()
