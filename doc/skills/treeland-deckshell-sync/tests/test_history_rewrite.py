"""Tests for raw metadata-only commit object reconstruction."""

from __future__ import annotations

import sys
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from sync_audit_lib.history_rewrite import (
    mapping_payload,
    parse_raw_commit,
    render_chain,
    render_commit,
    render_message,
)


def message_block(source: str = "a" * 40, *, duplicate: bool = False) -> bytes:
    block = (
        "[treeland-sync] classification: mixed\n"
        "[treeland-sync] action: adapted\n"
        "[treeland-sync] drop files:\n"
        "- waylib/example.cpp\n"
        "[treeland-sync] path mapping:\n"
        "- src/example.cpp -> compositor/src/example.cpp\n"
        "[treeland-sync] adaptation notes:\n"
        "- Legacy fallback.\n"
    )
    return ("subject\n\n" + block + (block if duplicate else "") + "\nTreeland-Commit: " + source + "\n").encode()


def manifest_entry(source: str = "a" * 40, legacy: str = "b" * 40, ordinal: int = 1) -> dict[str, object]:
    return {
        "ordinal": ordinal,
        "source_commit": source,
        "legacy_target_commit": legacy,
        "classification": "mixed",
        "action": "adapted",
        "adaptation_paths": [
            {"kind": "omitted", "path": "compositor/example.cpp"},
            {"kind": "modified", "path": "compositor/src/example.cpp"},
        ],
        "adaptation_notes": "Legacy fallback.",
    }


def raw_commit(message: bytes, header: bytes = b"", parent: str = "2" * 40) -> bytes:
    return (
        b"tree " + b"1" * 40 + b"\n"
        b"parent " + parent.encode() + b"\n"
        b"author A <a@example.test> 1 +0000\n"
        b"committer C <c@example.test> 2 +0000\n"
        + header
        + b"\n"
        + message
    )


class HistoryRewriteTests(unittest.TestCase):
    def test_renders_paths_before_notes_and_preserves_headers(self) -> None:
        parsed, content, object_id = render_commit(raw_commit(message_block()), manifest_entry(), "3" * 40)
        self.assertEqual(parsed.tree, "1" * 40)
        self.assertTrue(object_id)
        self.assertIn(b"parent " + b"3" * 40, content)
        self.assertLess(content.index(b"adaptation paths:"), content.index(b"adaptation notes:"))
        self.assertIn(b"- omitted: compositor/example.cpp\n", content)
        self.assertIn(b"- modified: compositor/src/example.cpp\n", content)
        self.assertTrue(content.endswith(b"\n"))
        self.assertFalse(content.endswith(b"\n\n"))

    def test_rejects_unknown_header(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported commit headers"):
            parse_raw_commit(raw_commit(message_block(), b"encoding UTF-8\n"))

    def test_rejects_duplicate_sync_block(self) -> None:
        with self.assertRaisesRegex(ValueError, "exactly one classification"):
            render_message(message_block(duplicate=True), manifest_entry())

    def test_rejects_cr_and_noncanonical_final_newline(self) -> None:
        with self.assertRaisesRegex(ValueError, "CR line endings"):
            render_message(message_block().replace(b"\n", b"\r\n"), manifest_entry())
        with self.assertRaisesRegex(ValueError, "exactly one trailing LF"):
            render_message(message_block() + b"\n", manifest_entry())

    def test_rejects_manifest_note_drift(self) -> None:
        entry = manifest_entry()
        entry["adaptation_notes"] = "Different note."
        with self.assertRaisesRegex(ValueError, "differ from manifest"):
            render_message(message_block(), entry)

    def test_chain_render_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            subprocess.run(["git", "init", "--bare", str(repo)], check=True, stdout=subprocess.DEVNULL)
            source_one, source_two = "a" * 40, "c" * 40
            first = subprocess.run(
                ["git", "-C", str(repo), "hash-object", "-t", "commit", "-w", "--stdin"],
                check=True,
                input=raw_commit(message_block(source_one)),
                stdout=subprocess.PIPE,
            ).stdout.decode().strip()
            second = subprocess.run(
                ["git", "-C", str(repo), "hash-object", "-t", "commit", "-w", "--stdin"],
                check=True,
                input=raw_commit(message_block(source_two), parent=first),
                stdout=subprocess.PIPE,
            ).stdout.decode().strip()
            manifest = {
                "entries": [
                    manifest_entry(source_one, first, 1),
                    manifest_entry(source_two, second, 2),
                ]
            }
            first_run, bundle = render_chain(repo, manifest, SKILL_DIR)
            second_run, second_bundle = render_chain(repo, manifest, SKILL_DIR)
            self.assertEqual(bundle, second_bundle)
            self.assertEqual(
                mapping_payload(first_run, bundle, "d" * 64),
                mapping_payload(second_run, second_bundle, "d" * 64),
            )
            self.assertEqual(first_run[1].rewritten_parent, first_run[0].rewritten_target)


if __name__ == "__main__":
    unittest.main()
