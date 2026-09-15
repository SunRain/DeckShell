"""独立初始化 fixture：真实 merge、R 历史和两层 gitlink，无普通 manifest。"""

from __future__ import annotations

from support import commit_files, init_repo, run
from records_fixture import fixture_validations
from unified_sync_lib.git_ops import atomic_write_json, common_git_dir, run_git
from unified_sync_lib.record_git import changed


def initialization_fixture(root):
    """构造可从 Git 重算的独立初始化事实，产品状态明确未验。"""
    repos = {lane: init_repo(root / lane) for lane in ("parent", "child", "wlroots")}
    source = init_repo(root / "source")
    r0 = commit_files(repos["wlroots"], {"core.c": "int core(void) { return 1; }\n"}, "R original")
    source_base = commit_files(source, {"README": "source\n"}, "source first parent")
    pack = run_git(repos["wlroots"], "pack-objects", "--stdout", "--revs", input_data=(r0 + "\n").encode(), text=False)
    run_git(source, "unpack-objects", input_data=pack, text=False)
    commit_files(source, {"3rdparty/wlroots/core.c": "int core(void) { return 1; }\n"}, "subtree contents")
    tree = run(source, "rev-parse", "HEAD^{tree}")
    merge = run(source, "commit-tree", tree, "-p", source_base, "-p", r0, "-m", "independent subtree merge")
    message = (f"fixture initialization\n\nTreeland-Initialization: {merge}\n"
               f"Treeland-First-Parent: {source_base}\nTreeland-Imported-Commit: {r0}\nRefs: approved-init.md")
    cbase = commit_files(repos["child"], {"README": "child\n"}, "C base")
    run(repos["parent"], "update-index", "--add", "--cacheinfo", f"160000,{cbase},3rdparty/waylib-shared")
    (repos["parent"] / "3rdparty/waylib-shared").mkdir(parents=True)
    pbase = commit_files(repos["parent"], {"README": "parent\n"}, "P base")
    run(repos["child"], "update-index", "--add", "--cacheinfo", f"160000,{r0},3rdparty/wlroots")
    (repos["child"] / "3rdparty/wlroots").mkdir(parents=True)
    c0 = commit_files(repos["child"], {
        ".gitmodules": f'[submodule "wlroots"]\n path = 3rdparty/wlroots\n url = {repos["wlroots"]}\n',
        "wlroots/CMakeLists.txt": "# explicit native integration fixture\n",
    }, message)
    run(repos["parent"], "update-index", "--cacheinfo", f"160000,{c0},3rdparty/waylib-shared")
    run(repos["parent"], "commit", "-m", message)
    p0 = run(repos["parent"], "rev-parse", "HEAD")
    candidate = {"kind": "treeland-independent-initialization-candidate", "ordinary_replay": False,
                 "source_merge": merge, "source_first_parent": source_base,
                 "parent_base": pbase, "child_base": cbase, "wlroots_base": r0,
                 "parent_candidate": p0, "child_candidate": c0, "wlroots_candidate": r0,
                 "integration": "synthetic-native-integration-not-built",
                 **{f"{lane}_worktree": str(repo) for lane, repo in repos.items()}}
    evidence = root / "evidence/N2"
    validation = fixture_validations(evidence)
    atomic_write_json(evidence / "validations.json", validation)
    _write_initialization_proof(evidence, source, repos, candidate, validation)
    nodes = root / "nodes.json"
    atomic_write_json(nodes, {"nodes": [{"name": "N2", "kind": "initialization", "path": "N2"}]})
    return source, repos, nodes, candidate


def _write_initialization_proof(evidence, source, repos, candidate, validation):
    r0 = candidate["wlroots_base"]
    tree = run(repos["wlroots"], "rev-parse", r0 + "^{tree}")
    proof = {"kind": "treeland-independent-initialization-structure", "candidate": candidate,
             "merge_parents": [candidate["source_first_parent"], r0], "source_tree": tree, "wlroots_tree": tree,
             "source_history_count": 1, "imported_history_count": 1,
             **{f"{lane}_changed_paths": changed(repos[lane], candidate[f"{lane}_base"], candidate[f"{lane}_candidate"])
                for lane in ("parent", "child")},
             "checkouts": {str(repo): {"common_git_dir": str(common_git_dir(repo))} for repo in repos.values()}}
    atomic_write_json(evidence / "structure-proof.json", proof)
    atomic_write_json(evidence / "source-contract-approval.json", {
        "review_state": "approved", "reason": "FIXTURE_INIT_REASON: independent local dependency wiring, not product validation."})
    atomic_write_json(evidence / "initialization-report.json", {
        "kind": "treeland-independent-initialization-report", "ordinary_replay": False,
        "outcome": "unverified", "candidate": candidate,
        "validation_results": {entry["id"]: {k: entry.get(k) for k in ("outcome", "exit_code", "tests", "log")}
                               for entry in validation["entries"]},
    })
