"""特殊记录保留真实 companion 身份，拒绝错误的父子配对。"""

import copy
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from protocol_fixture import IMPLEMENTATION, UPSTREAM_XML, XML, ProtocolFixture
from support import commit_files
from unified_sync_lib.record_context import make_context
from unified_sync_lib.record_special import special_rows
from unified_sync_lib.record_special_render import special_document
from unified_sync_lib.replay import run_replay


class RecordSpecialTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.fixture = ProtocolFixture(self.root)
        f = self.fixture
        commit_files(f.source, {IMPLEMENTATION: "// renamed_v1 implementation\n"}, "rename implementation")
        commit_files(f.protocol, {UPSTREAM_XML: XML.replace("manager_v1", "renamed_v1")}, "rename wire")
        self.request = f.request()
        self.manifest = run_replay(self.request)
        self.context = make_context(f.source, self.request.parent_worktree, self.request.child_worktree,
                                    None, "sample", self.root, "history/sample", None)
        self.node = {"name": "N1", "path": self.request.artifact_root.name, "manifest": self.manifest}

    def test_protocol_companion_has_its_own_git_delta_not_a_fake_source(self):
        rows = special_rows(self.context, self.node)
        for lane in ("parent", "child"):
            self.assertEqual(len(rows[lane]), 1)
            row = rows[lane][0]
            self.assertEqual(row["kind"], "protocol-companion")
            self.assertIsNone(row["source"])
            self.assertEqual(row["target"], self.manifest["protocol_update"][lane]["head"])
            text = special_document(self.context, row, 2)
            self.assertIn("mode/type/blob", text)
            self.assertIn("renamed_v1", text)
            self.assertIn("manifest.json#protocol_update", text)
        self.assertEqual(rows["parent"][0]["transition"]["to"], rows["child"][0]["target"])

    def test_wrong_companion_pair_fails_before_rendering(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["protocol_update"]["child"]["head"] = self.fixture.child_base
        with self.assertRaisesRegex(ValueError, "未引用同轮 C 候选"):
            special_rows(self.context, {**self.node, "manifest": manifest})


if __name__ == "__main__":
    unittest.main()
