#!/usr/bin/env python3
"""从已有同步证据与 Git 对象生成 P/C 各自的中文批次记录（Python 3.9+）。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Sequence

from unified_sync_lib.record_context import make_context
from unified_sync_lib.repo_records import generate_records


def parser() -> argparse.ArgumentParser:
    """仓库、批次、证据位置由调用方指定，不推断浮动来源或目标。"""
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--source-repo", type=Path, required=True)
    result.add_argument("--parent-repo", type=Path, required=True)
    result.add_argument("--child-repo", type=Path, required=True)
    result.add_argument("--wlroots-repo", type=Path)
    result.add_argument("--batch", required=True)
    result.add_argument("--evidence-root", type=Path, required=True)
    result.add_argument("--evidence-label", required=True, help="无机器绝对前缀的外层历史资料标识")
    result.add_argument("--nodes", type=Path, required=True, help="有序 replay/initialization 节点目录索引")
    result.add_argument("--history-map", type=Path, help="可选的历史旧新对应；普通同步应省略")
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    """生成失败返回非零；成功仅说明记录生成，不是产品验收 PASS。"""
    args = parser().parse_args(argv)
    try:
        context = make_context(args.source_repo, args.parent_repo, args.child_repo, args.wlroots_repo,
                               args.batch, args.evidence_root, args.evidence_label, args.history_map)
        result = generate_records(context, args.nodes)
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as error:
        print(f"记录生成失败：{error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
