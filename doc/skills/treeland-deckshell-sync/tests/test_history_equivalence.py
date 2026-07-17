"""Tests for object and patch equivalence verification."""

from __future__ import annotations

import copy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from sync_audit_lib.history_equivalence import verify_history_equivalence
from sync_audit_lib.history_rewrite import mapping_payload, render_chain, write_commit_objects


def message(source: str) -> bytes:
    return (
        "subject\n\n"
        "[treeland-sync] classification: other\n"
        "[treeland-sync] action: applied\n"
        "[treeland-sync] drop files:\n- none\n"
        "[treeland-sync] path mapping:\n- src/a.cpp -> compositor/src/a.cpp\n"
        "[treeland-sync] adaptation notes:\n- none\n\n"
        f"Treeland-Commit: {source}\n"
    ).encode()


def raw_commit(source: str, parent: str, tree: str) -> bytes:
    return (
        b"tree " + tree.encode() + b"\n"
        b"parent " + parent.encode() + b"\n"
        b"author A <a@example.test> 1 +0000\n"
        b"committer C <c@example.test> 2 +0000\n\n"
        + message(source)
    )


def write_object(repo: Path, object_type: str, content: bytes) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "hash-object", "-t", object_type, "-w", "--stdin"],
        check=True,
        input=content,
        stdout=subprocess.PIPE,
    )
    return result.stdout.decode().strip()


def write_legacy(repo: Path, source: str, parent: str, tree: str) -> str:
    return write_object(repo, "commit", raw_commit(source, parent, tree))


def build_manifest(first: str, second: str) -> dict[str, object]:
    return {
        "entries": [
            {
                "ordinal": 1,
                "source_commit": "a" * 40,
                "legacy_target_commit": first,
                "classification": "other",
                "action": "applied",
                "adaptation_paths": [],
                "adaptation_notes": "none",
            },
            {
                "ordinal": 2,
                "source_commit": "c" * 40,
                "legacy_target_commit": second,
                "classification": "other",
                "action": "applied",
                "adaptation_paths": [],
                "adaptation_notes": "none",
            },
        ]
    }


class HistoryEquivalenceTests(unittest.TestCase):
    def test_written_chain_passes_and_tampered_mapping_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            subprocess.run(
                ["git", "init", "--bare", str(repo)],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            tree = write_object(repo, "tree", b"")
            base = write_object(
                repo,
                "commit",
                (
                    f"tree {tree}\n"
                    "author A <a@example.test> 0 +0000\n"
                    "committer C <c@example.test> 0 +0000\n\n"
                    "base\n"
                ).encode(),
            )
            first = write_legacy(repo, "a" * 40, base, tree)
            second = write_legacy(repo, "c" * 40, first, tree)
            manifest = build_manifest(first, second)
            records, bundle = render_chain(repo, manifest, SKILL_DIR)
            write_commit_objects(repo, records, "refs/migrations/test")
            mapping = mapping_payload(records, bundle, "d" * 64)

            result = verify_history_equivalence(repo, manifest, mapping, 2, tree)
            self.assertEqual(result["outcome"], "pass")
            self.assertEqual(result["mismatch_counts"], {})

            tampered = copy.deepcopy(mapping)
            tampered["mappings"][1]["rewritten_target_commit"] = second
            blocked = verify_history_equivalence(repo, manifest, tampered, 2, tree)
            self.assertEqual(blocked["outcome"], "blocked")
            self.assertTrue(blocked["findings"])


if __name__ == "__main__":
    unittest.main()
