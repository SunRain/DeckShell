from __future__ import annotations

import json
from pathlib import Path

from pairing_report_fixture import PAIR, PROVENANCE_PATH
from support import add_worktree, commit_files, init_repo, run, write_policy
from unified_sync_lib.inventory import build_unified_inventory
from unified_sync_lib.policy import load_policy
from unified_sync_lib.replay import ReplayRequest
from unified_sync_lib.git_ops import atomic_write_json, read_json
from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.contracts import build_source_contract_audit
from unified_sync import main as sync_main


R_FILES = {
    "core.c": '#include "config.h"\nint core(void) { return R_FEATURE; }\n',
    "config.h.in": "#define R_FEATURE @R_FEATURE@\n",
    "meson.build": "project('wlroots-fixture', 'c', version: '0.20.2')\n"
                   "config = configuration_data()\nconfig.set('R_FEATURE', 1)\n"
                   "configure_file(input: 'config.h.in', output: 'config.h', configuration: config)\n"
                   "library('fixture-wlroots', 'core.c')\n",
}
C_FILES = {
    PROVENANCE_PATH: json.dumps(PAIR),
    "CMakeLists.txt": "cmake_minimum_required(VERSION 3.21)\n"
                       "project(WaylibShared VERSION 1.0 LANGUAGES C CXX)\n"
                       "add_subdirectory(wlroots)\nadd_subdirectory(waylib)\n",
    "wlroots/CMakeLists.txt": 'set(R_SOURCE "${CMAKE_CURRENT_SOURCE_DIR}/../3rdparty/wlroots")\n'
                              "set(R_FEATURE 1)\n"
                              'configure_file("${R_SOURCE}/config.h.in" "${CMAKE_CURRENT_BINARY_DIR}/include/config.h" @ONLY)\n'
                              'add_library(fixture-wlroots STATIC "${R_SOURCE}/core.c")\n'
                              "set_target_properties(fixture-wlroots PROPERTIES POSITION_INDEPENDENT_CODE ON)\n"
                              'target_include_directories(fixture-wlroots PRIVATE "${CMAKE_CURRENT_BINARY_DIR}/include")\n'
                              "add_library(Wlroots::wlroots ALIAS fixture-wlroots)\n",
    "waylib/CMakeLists.txt": "add_library(WaylibSharedServer SHARED server.cpp)\n"
                            "target_link_libraries(WaylibSharedServer PRIVATE Wlroots::wlroots)\n"
                            'target_include_directories(WaylibSharedServer PUBLIC "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>" "$<INSTALL_INTERFACE:include>")\n'
                            "set_target_properties(WaylibSharedServer PROPERTIES EXPORT_NAME SharedServer)\n"
                            "install(TARGETS WaylibSharedServer EXPORT WaylibSharedTargets LIBRARY DESTINATION lib)\n"
                            "install(DIRECTORY include/ DESTINATION include)\n"
                            "install(EXPORT WaylibSharedTargets NAMESPACE WaylibShared:: DESTINATION lib/cmake/WaylibShared)\n"
                            "install(FILES WaylibSharedConfig.cmake DESTINATION lib/cmake/WaylibShared)\n"
                            "enable_testing()\nadd_executable(test_waylib test.cpp)\n"
                            "target_link_libraries(test_waylib PRIVATE WaylibSharedServer)\n"
                            "add_test(NAME waylib_link COMMAND test_waylib)\n",
    "waylib/include/waylib/server.h": "#pragma once\n#define SERVER_NAMESPACE Server\n"
                                     "namespace Waylib { namespace SERVER_NAMESPACE { int value(); } }\n",
    "waylib/server.cpp": '#include "waylib/server.h"\nextern "C" int core(void);\n'
                         "int Waylib::Server::value() { return core(); }\n",
    "waylib/test.cpp": '#include "waylib/server.h"\nint main() { return Waylib::Server::value() > 0 ? 0 : 1; }\n',
    "waylib/WaylibSharedConfig.cmake": 'include("${CMAKE_CURRENT_LIST_DIR}/WaylibSharedTargets.cmake")\n',
    "test_project/CMakeLists.txt": "cmake_minimum_required(VERSION 3.21)\nproject(Consumer LANGUAGES CXX)\n"
                                   "find_package(WaylibShared REQUIRED COMPONENTS SharedServer)\n"
                                   "add_executable(consumer main.cpp)\ntarget_link_libraries(consumer PRIVATE WaylibShared::SharedServer)\n"
                                   "enable_testing()\nadd_test(NAME installed_consumer COMMAND consumer)\n",
    "test_project/main.cpp": '#include "waylib/server.h"\nint main() { return Waylib::Server::value() > 0 ? 0 : 1; }\n',
}
P_FILES = {
    "CMakeLists.txt": "cmake_minimum_required(VERSION 3.21)\nproject(DeckShell LANGUAGES C CXX)\n"
                       "add_subdirectory(3rdparty/waylib-shared)\nadd_subdirectory(compositor)\n",
    "compositor/CMakeLists.txt": "add_executable(test_compositor main.cpp)\n"
                                 "target_link_libraries(test_compositor PRIVATE WaylibSharedServer)\n"
                                 "enable_testing()\nadd_test(NAME compositor_link COMMAND test_compositor)\n"
                                 "add_executable(DeckCompositor src/production.cpp)\n",
    "compositor/main.cpp": '#include "waylib/server.h"\nint main() { return Waylib::Server::value() > 0 ? 0 : 1; }\n',
    "compositor/src/production.cpp": "int main() { return 0; }\n",
}


def _bootstrap_child_files():
    before = {path: text for path, text in C_FILES.items() if not path.startswith("wlroots/")}
    before["CMakeLists.txt"] = before["CMakeLists.txt"].replace("add_subdirectory(wlroots)\n", "")
    before["waylib/CMakeLists.txt"] = before["waylib/CMakeLists.txt"].replace(
        "target_link_libraries(WaylibSharedServer PRIVATE Wlroots::wlroots)\n", "")
    before["waylib/server.cpp"] = '#include "waylib/server.h"\nint Waylib::Server::value() { return 1; }\n'
    after = {**C_FILES, "CMakeLists.txt": before["CMakeLists.txt"] + "add_subdirectory(wlroots)\n"}
    return before, after


def _bootstrap_decisions(root, child, base, before, after, inventory, artifacts):
    preview = add_worktree(child, root / "preview", "preview", base)
    proposed = commit_files(preview, after, "reviewed wrapper integration")
    audit = build_source_contract_audit(preview, base, proposed)
    patch = run(preview, "diff", "--binary", base, proposed).encode("utf-8") + b"\n"
    proof = write_artifact(artifacts, "decisions/review.md", b"Reviewed private wrapper integration; public API unchanged.\n")
    item = inventory["commits"][0]
    paths = item["waylib_shared"]["source_paths"] + ["CMakeLists.txt"]
    decision = {
        "action": "adapted", "structural_paths": ["CMakeLists.txt"],
        "adaptation_patch": write_artifact(artifacts, "decisions/child.patch", patch),
        "adaptation_notes": ["Add native wrapper without changing the Waylib public API."],
        "adaptation_paths": [{"path": path, "kind": "modified" if path in before else "materialized",
                              "reason": "Reviewed private wrapper integration.", "proof": proof,
                              "review_state": "approved"} for path in paths],
        "contract_additions": write_artifact(artifacts, "decisions/additions.json", json.dumps({
            "review_state": "approved", "before_snapshot_sha256": audit["before_snapshot_sha256"],
            "after_snapshot_sha256": audit["after_snapshot_sha256"],
            "additions": {field: change["added"] for field, change in audit["drift"].items()},
        }).encode("utf-8")),
    }
    return {"entries": {item["source_commit"]: {"child": decision}}}


def build_fixture(root: Path, bootstrap=False, source_updates=None, source_count=None):
    """建立离线 P/C/R，覆盖已登记基线或空 R0 后的普通线性导入，再回放与物化。"""

    source, parent, child, r = [init_repo(root / name) for name in ("source", "parent", "child", "wlroots")]
    if bootstrap:
        run(r, "commit", "--allow-empty", "-m", "explicit empty R baseline")
        rb = run(r, "rev-parse", "HEAD")
        files, candidate = _bootstrap_child_files()
    else:
        rb = commit_files(r, R_FILES, "R baseline")
        files = {**C_FILES, ".gitmodules": f'[submodule "wlroots"]\n\tpath = 3rdparty/wlroots\n\turl = {r}\n'}
        run(child, "update-index", "--add", "--cacheinfo", f"160000,{rb},3rdparty/wlroots")
        (child / "3rdparty/wlroots").mkdir(parents=True)
    cb = commit_files(child, files, "C baseline")
    run(parent, "update-index", "--add", "--cacheinfo", f"160000,{cb},3rdparty/waylib-shared")
    (parent / "3rdparty/waylib-shared").mkdir(parents=True)
    pb = commit_files(parent, P_FILES, "P baseline")
    native = {"3rdparty/wlroots/" + key: value for key, value in R_FILES.items()}
    source_files = files if bootstrap else {**C_FILES, **native}
    sb = commit_files(source, {**source_files, "src/production.cpp": P_FILES["compositor/src/production.cpp"]}, "source baseline")
    changes = ({**native, **{path: text for path, text in candidate.items()
                            if path != "CMakeLists.txt" and text != files.get(path)}} if bootstrap else {})
    changes["3rdparty/wlroots/core.c"] = R_FILES["core.c"].replace("return R_FEATURE", "return R_FEATURE + 1")
    updates = [changes] if source_updates is None else source_updates
    source_heads = []
    for update in updates:
        source_heads.append(commit_files(source, update, "linear R import" if bootstrap else "R improvement"))
    sh = source_heads[-1 if source_count is None else source_count - 1]
    policy = write_policy(root / "policy.md")
    inventory = build_unified_inventory(source, sb, sh, load_policy(policy), policy, set(), source_tip=source_heads[-1])
    artifacts = root / "evidence"
    decisions = _bootstrap_decisions(root, child, cb, files, candidate, inventory, artifacts) if bootstrap else {}
    request = ReplayRequest(source, add_worktree(parent, root / "p-wt", "sync", pb),
                            add_worktree(child, root / "c-wt", "sync", cb), pb, cb, inventory, artifacts,
                            artifacts / "journal.json", artifacts / "manifest.json", artifacts / "waylib-evidence.json",
                            artifacts / "parent-evidence.json", "fixture", "approved-plan.md", decisions, True,
                            wlroots_repo=r, wlroots_worktree=add_worktree(r, root / "r-wt", "sync", rb),
                            wlroots_base=rb, wlroots_target_ref="refs/heads/target", wlroots_submodule_url=str(r))
    for repo, base in ((r, rb), (child, cb), (parent, pb)):
        run(repo, "branch", "target", base)
    inventory_path = artifacts / "inventory.json"
    atomic_write_json(inventory_path, inventory)
    decision_args = []
    if bootstrap:
        decision_path = artifacts / "decisions.json"
        atomic_write_json(decision_path, decisions)
        decision_args = ["--decisions", str(decision_path)]
    code = sync_main([
        "replay", "--source-repo", str(source), "--parent-worktree", str(request.parent_worktree),
        "--child-worktree", str(request.child_worktree), "--parent-base", pb, "--child-base", cb,
        "--wlroots-repo", str(r), "--wlroots-worktree", str(request.wlroots_worktree),
        "--wlroots-base", rb, "--wlroots-target-ref", "refs/heads/target", "--wlroots-submodule-url", str(r),
        "--inventory", str(inventory_path), "--artifact-root", str(artifacts), "--run-id", "fixture",
        "--refs-doc", "approved-plan.md", "--test-allow-ephemeral-artifacts", *decision_args,
    ])
    if code:
        raise RuntimeError(f"three-repository replay CLI failed: {code}")
    manifest = read_json(request.manifest_path)
    cbase = add_worktree(child, root / "c-base", "baseline", cb)
    rbase = add_worktree(r, root / "r-base", "baseline", rb)
    materialization_path = artifacts / "materialization.json"
    code = sync_main([
        "materialize-child", "--parent-worktree", str(request.parent_worktree), "--child-repo", str(child),
        "--wlroots-repo", str(r), "--child-base-worktree", str(cbase),
        "--manifest", str(request.manifest_path), "--output", str(materialization_path),
    ])
    if code:
        raise RuntimeError(f"recursive materialization CLI failed: {code}")
    materialization = read_json(materialization_path)
    return request, manifest, materialization, cbase, rbase
