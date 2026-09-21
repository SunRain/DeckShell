"""Small Git-only protocol fixtures; these are not product-build evidence."""

from __future__ import annotations

import json
from pathlib import Path

from support import add_worktree, commit_files, init_repo, run, write_policy
from unified_sync_lib.inventory import build_unified_inventory
from unified_sync_lib.policy import load_policy
from unified_sync_lib.protocol_sources import PARENT_XML_PATH, PROVENANCE_PATH, XML_PATH
from unified_sync_lib.replay import ReplayRequest


IMPLEMENTATION = "waylib/src/server/protocols/manager.cpp"
UPSTREAM_XML = "xml/remote.xml"
CLIENT = "compositor/tests/client.cpp"
XML = '''<protocol name="remote">
<description summary="remote">Token-based references.</description>
<interface name="manager_v1" version="1">
<request name="destroy" type="destructor"/>
<request name="export"><arg name="id" type="new_id" interface="exported_v1"/></request>
</interface>
<interface name="exported_v1" version="1">
<event name="token"><arg name="value" type="string"/></event>
</interface></protocol>
'''


class ProtocolFixture:
    def __init__(self, root: Path):
        self.root = root
        self.source = init_repo(root / "source")
        self.protocol = init_repo(root / "protocol")
        self.child = init_repo(root / "child")
        self.parent = init_repo(root / "parent")
        self.source_base = commit_files(self.source, {IMPLEMENTATION: "// manager_v1 implementation\n"}, "source base")
        self.protocol_base = commit_files(self.protocol, {UPSTREAM_XML: XML}, "protocol base")
        self.pair = {
            "implementation": {"repository": "https://example.invalid/source", "commit": self.source_base,
                               "paths": [IMPLEMENTATION]},
            "protocol": {"repository": "https://example.invalid/protocol", "commit": self.protocol_base,
                         "path": UPSTREAM_XML},
            "notes": "Synthetic Git fixture, not product validation.",
        }
        self.child_base = commit_files(self.child, {IMPLEMENTATION: "// manager_v1 implementation\n",
                                                   XML_PATH: XML, PROVENANCE_PATH: json.dumps(self.pair)}, "child base")
        commit_files(self.parent, {PARENT_XML_PATH: XML, CLIENT: "// manager_v1 client\n"}, "parent files")
        run(self.parent, "update-index", "--add", "--cacheinfo", f"160000,{self.child_base},3rdparty/waylib-shared")
        run(self.parent, "commit", "-m", "parent base")
        self.parent_base = run(self.parent, "rev-parse", "HEAD")
        self.policy = write_policy(root / "policy.md")

    def inventory(self):
        return build_unified_inventory(self.source, self.source_base, "HEAD", load_policy(self.policy), self.policy, set())

    def selection(self):
        return {"repo": str(self.protocol), "base": self.protocol_base, "head": run(self.protocol, "rev-parse", "HEAD")}

    def request(self, suffix="one"):
        artifacts = self.root / f"artifacts-{suffix}"
        return ReplayRequest(
            source_repo=self.source,
            child_worktree=add_worktree(self.child, self.root / f"child-{suffix}", f"child-{suffix}", self.child_base),
            parent_worktree=add_worktree(self.parent, self.root / f"parent-{suffix}", f"parent-{suffix}", self.parent_base),
            child_base=self.child_base, parent_base=self.parent_base, inventory=self.inventory(),
            artifact_root=artifacts, journal_path=artifacts / "journal.json", manifest_path=artifacts / "manifest.json",
            waylib_evidence_path=artifacts / "waylib-evidence.json", parent_evidence_path=artifacts / "parent-evidence.json",
            run_id=f"protocol-{suffix}", refs_doc="plans/protocol.md", decisions={}, allow_ephemeral_artifacts=True,
            protocol_update={"selection": self.selection()},
        )
