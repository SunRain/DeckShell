"""History mapping cannot conceal source, author or message changes."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from records_fixture import RecordsFixture
from unified_sync_lib.git_ops import run_git
from unified_sync_lib.record_context import make_context
from unified_sync_lib.record_git import check_pair


class HistoryMetadataTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.f = RecordsFixture(self.root)
        path, _ = self.f.rewrite()
        self.context = make_context(self.f.source, self.f.repos["parent"], self.f.repos["child"],
                                    self.f.repos["wlroots"], "sample", self.root / "evidence", "history/sample", path)
        item = self.f.manifest["entries"][0]
        self.old, self.source = item["parent"]["commit"], item["source_commit"]
        self.new = self.context.target("parent", self.old)
        assert self.new is not None

    def changed_target(self, replace):
        repo = self.f.repos["parent"]
        assert self.new is not None
        raw = run_git(repo, "cat-file", "commit", self.new, text=False)
        new = run_git(repo, "hash-object", "-t", "commit", "-w", "--stdin",
                      input_data=replace(raw), text=False).decode().strip()
        self.context.history["parent"]["mapping"][self.old] = new

    def test_changed_author_is_not_a_metadata_only_refs_rewrite(self):
        self.changed_target(lambda raw: raw.replace(b"author ", b"author Other ", 1))
        with self.assertRaisesRegex(ValueError, "作者"):
            check_pair(self.context, "parent", self.old, self.source)

    def test_changed_original_message_is_rejected(self):
        self.changed_target(lambda raw: raw.replace(b"Original treeland commit:", b"Altered source:", 1))
        with self.assertRaisesRegex(ValueError, "非派生消息"):
            check_pair(self.context, "parent", self.old, self.source)

    def test_absolute_new_refs_is_rejected(self):
        self.changed_target(lambda raw: raw.replace(b"Refs: portable/record.md", b"Refs: /home/private/record.md"))
        with self.assertRaisesRegex(ValueError, "workspace-relative"):
            check_pair(self.context, "parent", self.old, self.source)

    def test_complete_fixture_rewrite_preserves_source_metadata(self):
        self.assertEqual(check_pair(self.context, "parent", self.old, self.source), self.new)
        for lane in self.f.repos:
            for pair in self.context.history[lane]["commits"]:
                old = pair["old"]
                trailer = next(line for line in run_git(self.f.repos[lane], "show", "-s", "--format=%B", old).splitlines()
                               if line.startswith("Treeland-Commit: "))
                check_pair(self.context, lane, old, trailer.split()[1])


if __name__ == "__main__":
    unittest.main()
