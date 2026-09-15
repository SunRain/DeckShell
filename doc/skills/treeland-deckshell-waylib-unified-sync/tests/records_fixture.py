"""记录测试使用真实离线 Git/replay；产品验证数据明确为合成未验/失败记录。"""

from __future__ import annotations

import json
from pathlib import Path

from support import add_worktree, commit_files, init_repo, run, write_policy
from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.evidence import verify_waylib_sync
from unified_sync_lib.git_ops import atomic_write_json, canonical_json_sha256, read_json, run_git
from unified_sync_lib.gitlink import verify_gitlink_consistency
from unified_sync_lib.inventory import build_unified_inventory
from unified_sync_lib.parent_verify import verify_parent_sync
from unified_sync_lib.patches import commit_diff
from unified_sync_lib.policy import load_policy
from unified_sync_lib.record_replay import GATES
from unified_sync_lib.replay import ReplayRequest, run_replay
from unified_sync_lib.traces import build_waylib_traces
from wlroots_verify import verify_wlroots


def fixture_validations(root):
    """不运行产品命令，也不伪造产品 PASS。"""
    return {"schema_version": 2, "kind": "treeland-unified-command-validations", "entries": [
        {"id": "fixture-build", "attempt": 1, "outcome": "fail", "exit_code": 1,
         "log": write_artifact(root, "logs/failed.log", b"Synthetic fixture: compile failed\n")},
        {"id": "fixture-tests", "attempt": 1, "outcome": "no-tests", "exit_code": 0,
         "tests": {"total": 0, "passed": 0, "failed": 0, "skipped": 0},
         "log": write_artifact(root, "logs/no-tests.log", b"No tests were found!!!\n")},
        {"id": "fixture-not-run", "attempt": 1, "outcome": "unverified", "exit_code": None},
    ]}


class RecordsFixture:
    def __init__(self, root: Path, active_r=True, registration=False):
        self.root, self.active_r, self.registration = root, active_r, registration
        self.repos = {lane: init_repo(root / lane) for lane in ("parent", "child", "wlroots")}
        self.source = init_repo(root / "source")
        r0 = commit_files(self.repos["wlroots"], {"core.c": "int core(void) { return 1; }\n"}, "R base")
        child_files = {"README": "child baseline\n"}
        if active_r and not registration:
            self._link("child", r0, "3rdparty/wlroots")
            child_files[".gitmodules"] = f'[submodule "wlroots"]\n path = 3rdparty/wlroots\n url = {self.repos["wlroots"]}\n'
        c0 = commit_files(self.repos["child"], child_files, "C base")
        self._link("parent", c0, "3rdparty/waylib-shared")
        p0 = commit_files(self.repos["parent"], {"compositor/src/already.cpp": "already applied\n"}, "P base")
        self.bases = {"parent": p0, "child": c0, "wlroots": r0}
        source_files = {"3rdparty/wlroots/core.c": "int core(void) { return 1; }\n"} if active_r else {"README": "source\n"}
        self.source_base = commit_files(self.source, source_files, "source base")
        self.artifacts = root / "evidence/N1"
        self.sources, decisions = self._sources()
        policy = write_policy(root / "policy.md")
        inventory = build_unified_inventory(self.source, self.source_base, self.sources[-1], load_policy(policy), policy, set())
        atomic_write_json(self.artifacts / "inventory.json", inventory)
        self.request = self._request(inventory, decisions)
        self.manifest = run_replay(self.request)
        self._reports()
        self.nodes = root / "nodes.json"
        atomic_write_json(self.nodes, {"nodes": [{"name": "N1", "kind": "replay", "path": "N1"}]})

    def _link(self, lane, sha, path):
        run(self.repos[lane], "update-index", "--add", "--cacheinfo", f"160000,{sha},{path}")
        (self.repos[lane] / path).mkdir(parents=True, exist_ok=True)

    def _adaptation(self, lane, source, path, text, reason):
        preview = add_worktree(self.repos[lane], self.root / f"review-{lane}-{source[:8]}",
                               f"review-{source[:8]}", self.bases[lane])
        target = commit_files(preview, {path: text}, "fixture review")
        patch = write_artifact(self.artifacts, f"decisions/{source}-{lane}.patch", commit_diff(preview, target))
        proof = write_artifact(self.artifacts, f"decisions/{source}-{lane}.txt", reason.encode())
        return {"action": "adapted", "adaptation_notes": [reason], "adaptation_patch": patch,
                "adaptation_paths": [{"path": path, "kind": "modified" if lane == "wlroots" else "materialized",
                                      "reason": reason, "review_state": "approved", "proof": proof}]}

    def _sources(self):
        sources, decisions = [], {"entries": {}}
        if self.registration:
            source = commit_files(self.source, {"3rdparty/wlroots/core.c": "int core(void) { return 2; }\n"}, "first R registration")
            return [source], decisions
        sources.append(commit_files(self.source, {"src/p.cpp": "parent only\n"}, "parent-only"))
        child = commit_files(self.source, {"waylib/c.cpp": "upstream child\n"}, "child-only")
        sources.append(child)
        decisions["entries"][child] = {"child": self._adaptation("child", child, "waylib/c.cpp", "local child\n", "C_ONLY_LOCAL_REASON")}
        dual = commit_files(self.source, {"src/dual.cpp": "upstream P\n", "waylib/dual.cpp": "upstream C\n"}, "dual")
        sources.append(dual)
        decisions["entries"][dual] = {
            "parent": self._adaptation("parent", dual, "compositor/src/dual.cpp", "local P\n", "P_DUAL_REASON"),
            "child": self._adaptation("child", dual, "waylib/dual.cpp", "local C\n", "C_DUAL_REASON"),
        }
        if self.active_r:
            r = commit_files(self.source, {"3rdparty/wlroots/core.c": "int core(void) { return 2; }\n"}, "R-only")
            sources.append(r)
            decisions["entries"][r] = {"wlroots": self._adaptation("wlroots", r, "core.c", "int core(void) { return 3; }\n", "R_ONLY_REASON")}
            sources.append(commit_files(self.source, {"wlroots/cmake/private.cmake": "set(PRIVATE_VALUE 1)\n"}, "wrapper-only"))
        empty = commit_files(self.source, {"src/already.cpp": "already applied\n"}, "equivalent")
        sources.append(empty)
        decisions["entries"][empty] = {"parent": {"action": "empty", "adaptation_notes": ["Already present in target baseline."],
            "equivalence_proof": write_artifact(self.artifacts, "decisions/equivalent.txt", b"ALREADY_EQUIVALENT\n")}}
        return sources, decisions

    def _request(self, inventory, decisions):
        worktrees = {lane: add_worktree(repo, self.root / f"{lane}-wt", "sync", self.bases[lane])
                     for lane, repo in self.repos.items() if lane != "wlroots" or self.active_r}
        options = {} if not self.active_r else {
            "wlroots_repo": self.repos["wlroots"], "wlroots_worktree": worktrees["wlroots"],
            "wlroots_base": self.bases["wlroots"], "wlroots_target_ref": "refs/heads/main",
            "wlroots_submodule_url": str(self.repos["wlroots"]),
        }
        return ReplayRequest(self.source, worktrees["parent"], worktrees["child"], self.bases["parent"],
                             self.bases["child"], inventory, self.artifacts, self.artifacts / "journal.json",
                             self.artifacts / "manifest.json", self.artifacts / "waylib-evidence.json",
                             self.artifacts / "parent-evidence.json", "record-fixture", "plans/record.md", decisions,
                             True, **options)

    def _reports(self):
        req, manifest = self.request, self.manifest
        pe = read_json(req.parent_evidence_path)
        ce = read_json(req.waylib_evidence_path)
        re = read_json(self.artifacts / "wlroots-evidence.json")
        parent = verify_parent_sync(req.source_repo, req.parent_worktree, req.parent_base,
                                    manifest["final_parent_head"], req.inventory, manifest, pe, self.artifacts)
        traces = build_waylib_traces(req.child_worktree, req.child_base, manifest["final_child_head"], req.inventory, req.source_repo)
        child = verify_waylib_sync(req.child_worktree, req.child_base, manifest["final_child_head"],
                                   req.inventory, traces, ce, self.artifacts, req.source_repo)
        r, nested = verify_wlroots(req.source_repo, req.child_worktree, req.wlroots_repo,
                                   req.inventory, manifest, re, self.artifacts)
        gitlink = verify_gitlink_consistency(req.parent_worktree, req.child_worktree, req.parent_base, req.child_base, manifest)
        gates = {"deckshell_verify": parent, "waylib_verify": child, "wlroots_verify": r,
                 "gitlink_verify": gitlink, "nested_gitlink_verify": nested,
                 "protocol_tracking": {"outcome": "pass", "status": "not-triggered"},
                 "contract_audit": {"outcome": "unverified"}, "child_materialization": {"outcome": "unverified"}}
        for gate in (parent, child, r, nested, gitlink):
            if gate["outcome"] != "pass":
                raise AssertionError(gate)
        for key, value in gates.items():
            atomic_write_json(self.artifacts / GATES[key], value)
        validation = fixture_validations(self.artifacts)
        atomic_write_json(self.artifacts / "validations.json", validation)
        report = {"schema_version": 2, "kind": "treeland-unified-sync-report", "outcome": "blocked",
                  "build_scope": {"kind": "range-head-only", "source_head": req.inventory["range"]["head"]},
                  "replay_identity": manifest["identity"],
                  **{f"final_{lane}_head": manifest[f"final_{lane}_head"] for lane in self.repos},
                  "inventory_sha256": canonical_json_sha256(req.inventory),
                  "manifest_sha256": canonical_json_sha256(manifest), "validations_sha256": canonical_json_sha256(validation),
                  "gate_sha256": {key: canonical_json_sha256(value) for key, value in gates.items()}}
        atomic_write_json(self.artifacts / "sync-report.json", report)

    def rewrite(self, batch="sample"):
        """仅用于 fixture：真实创建重写对象，使新旧身份测试不靠假 SHA。"""
        result = {}
        lanes = ("wlroots", "child", "parent") if self.active_r else ("child", "parent")
        for lane in lanes:
            repo, base = self.repos[lane], self.bases[lane]
            head = self.manifest[f"final_{lane}_head"]
            mapping, lower = {}, {}
            dependency = {"child": ("wlroots", "3rdparty/wlroots"), "parent": ("child", "3rdparty/waylib-shared")}.get(lane)
            if dependency and dependency[0] in result:
                lower = {v["old"]: v["new"] for v in result[dependency[0]]["commits"]}
            for old in run(repo, "rev-list", "--reverse", f"{base}..{head}").split():
                mapping[old] = self._rewrite_commit(lane, old, mapping, lower, dependency)
            result[lane] = {"base": base, "old_head": head, "new_head": mapping.get(head, head),
                            "commits": [{"old": old, "new": new} for old, new in mapping.items()]}
        path = self.root / "history-map.json"
        atomic_write_json(path, {"batch": batch, "repositories": result})
        return path, result

    def _rewrite_commit(self, lane, old, mapping, lower, dependency):
        repo = self.repos[lane]
        raw = run_git(repo, "cat-file", "commit", old, text=False)
        header, message = raw.split(b"\n\n", 1)
        tree, parent = [line.split()[1].decode() for line in header.splitlines()[:2]]
        index = self.root / f"{lane}-rewrite-index"
        env = {"GIT_INDEX_FILE": str(index)}
        run(repo, "read-tree", old, env=env)
        if dependency:
            entry = run(repo, "ls-tree", old, "--", dependency[1])
            if entry and entry.split()[2] in lower:
                run(repo, "update-index", "--cacheinfo", f"160000,{lower[entry.split()[2]]},{dependency[1]}", env=env)
        new_tree = run(repo, "write-tree", env=env)
        header = header.replace(tree.encode(), new_tree.encode(), 1).replace(parent.encode(), mapping.get(parent, parent).encode(), 1)
        message = message.replace(b"Refs: plans/record.md", b"Refs: portable/record.md")
        for before, after in lower.items():
            message = message.replace(before.encode(), after.encode())
        return str(run_git(repo, "hash-object", "-t", "commit", "-w", "--stdin",
                           input_data=header + b"\n\n" + message, text=False).decode()).strip()
