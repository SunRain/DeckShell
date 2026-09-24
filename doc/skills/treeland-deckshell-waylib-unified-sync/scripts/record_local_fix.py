#!/usr/bin/env python3
"""为显式批准的相邻 P/C 本地修复留证，不重放来源、不写源码或 refs。"""

import argparse
import sys
from pathlib import Path

from unified_sync_lib.artifacts import write_artifact
from unified_sync_lib.git_ops import atomic_write_json, read_json
from unified_sync_lib.local_fixes import record_local_fix


def main():
    """保留原 replay manifest，生成独立本地修复及各 lane 的新证据。"""
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("manifest", "approval", "artifact-root", "parent-worktree", "child-worktree",
                 "parent-evidence", "child-evidence", "output"):
        parser.add_argument("--" + name, required=True, type=Path)
    parser.add_argument("--wlroots-worktree", type=Path)
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError("refusing to replace an existing local-fix manifest")
        root = args.artifact_root.resolve()
        original = read_json(args.manifest)
        before = write_artifact(root, "local-fix/original-manifest.json", args.manifest.read_bytes())
        approval = write_artifact(root, "local-fix/approval.json", args.approval.read_bytes())
        trees = {lane: getattr(args, lane + "_worktree") for lane in ("child", "parent", "wlroots")}
        result = record_local_fix(original, approval, before, trees, root)
        for lane in ("parent", "child"):
            path = getattr(args, lane + "_evidence")
            evidence = read_json(path)
            if evidence.get("local_fix"):
                raise ValueError("source evidence already contains a local fix")
            evidence["local_fix"] = result["local_fix"]
            name = "parent-evidence.json" if lane == "parent" else "waylib-evidence.json"
            if (root / name).exists():
                raise ValueError("refusing to replace existing lane evidence")
            atomic_write_json(root / name, evidence)
        atomic_write_json(args.output, result)
        return 0
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as error:
        print(f"独立本地修复记录失败：{error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
