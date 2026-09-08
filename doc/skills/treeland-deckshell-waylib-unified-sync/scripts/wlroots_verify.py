#!/usr/bin/env python3
"""核验独立 wlroots 来源回放和 waylib-shared 的嵌套 gitlink。"""

from __future__ import annotations

import argparse
from pathlib import Path

from unified_sync_lib.evidence import verify_waylib_sync
from unified_sync_lib.git_ops import atomic_write_json, canonical_json_sha256, read_json
from unified_sync_lib.gitlink import verify_nested_gitlink_consistency
from unified_sync_lib.schema import load_inventory
from unified_sync_lib.traces import build_waylib_traces


def verify_wlroots(source_repo, child_repo, repo, inventory, manifest, evidence, artifact_root):
    """分别返回 R 来源回放和 C→R gitlink 的完整验证结果。"""

    nested = verify_nested_gitlink_consistency(child_repo, repo, inventory, manifest, artifact_root)
    r = manifest.get("identity", {}).get("wlroots")
    if r is None:
        result = {"schema_version": 2, "kind": "treeland-unified-wlroots-verify", "status": "not-applicable",
                  "target_range": None, "inventory_sha256": canonical_json_sha256(inventory),
                  "verified_entries": 0, "blocked_reasons": list(nested["blocked_reasons"]), "outcome": nested["outcome"]}
    elif repo is None:
        raise ValueError("--repo is required for active wlroots")
    else:
        head = manifest["final_wlroots_head"]
        traces = build_waylib_traces(repo, r["base"], head, inventory, source_repo, "wlroots")
        result = verify_waylib_sync(repo, r["base"], head, inventory, traces, evidence, artifact_root, source_repo, "wlroots")
        result["status"] = "verified"
        targets = [node["wlroots"]["commit"] for node in manifest["entries"] if node["wlroots"]["commit"]]
        if targets != [entry["target_commit"] for entry in traces["entries"]]:
            result["blocked_reasons"].append("wlroots traces differ from manifest")
            result["outcome"] = "blocked"
    result["manifest_sha256"] = canonical_json_sha256(manifest)
    return result, nested


def main(argv=None):
    """通过公开 CLI 写入两份独立的 R 验证工件。"""

    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source-repo", "child-repo", "inventory", "manifest", "evidence", "artifact-root", "output", "gitlink-output"):
        parser.add_argument("--" + name, required=True, type=Path)
    parser.add_argument("--repo", type=Path, help="激活 R 时必需的本地 wlroots 仓库")
    args = parser.parse_args(argv)
    try:
        result, nested = verify_wlroots(args.source_repo, args.child_repo, args.repo, load_inventory(args.inventory),
                                        read_json(args.manifest), read_json(args.evidence), args.artifact_root)
    except (OSError, ValueError, RuntimeError) as error:
        result = {"schema_version": 2, "kind": "treeland-unified-wlroots-verify", "outcome": "fail", "errors": [str(error)]}
        nested = {"schema_version": 2, "kind": "treeland-unified-nested-gitlink-verify", "outcome": "fail", "errors": [str(error)]}
    atomic_write_json(args.output, result)
    atomic_write_json(args.gitlink_output, nested)
    return 0 if result["outcome"] == nested["outcome"] == "pass" else 1 if result["outcome"] == "fail" else 2


if __name__ == "__main__":
    raise SystemExit(main())
