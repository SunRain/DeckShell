"""同步/归并的整批完成入口：接受历史核对和两仓文档交付，不移动 refs。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .git_ops import git_succeeds, read_json, run_git
from .record_context import make_context, require
from .record_reports import accepted_report, check_closeout
from .record_sidecars import plan_documents
from .repo_records import generate_from_inputs
from .schema import is_full_sha


def add_finish_parser(subparsers):
    """正常任务入口接收已有冻结范围，不要求用户手工选择接受 attempts。"""
    command = subparsers.add_parser("finish", help="完成整批同步或归并并自动交付两仓记录（不提交）")
    command.add_argument("--task", choices=("sync", "consolidate"), required=True)
    for name in ("source-repo", "parent-repo", "child-repo", "evidence-root", "plan-dir"):
        command.add_argument("--" + name, type=Path, required=True)
    command.add_argument("--wlroots-repo", type=Path)
    for name in ("batch", "source-base", "source-head", "evidence-label"):
        command.add_argument("--" + name, required=True)


def _closed_nodes(context, order):
    result = []
    paths = set(context.evidence_root.glob("*/closeout-journal.json"))
    paths.update(context.evidence_root.glob("evidence/*/closeout-journal.json"))
    for path in sorted(paths):
        root = context.node_root(path.parent.relative_to(context.evidence_root).as_posix())
        journal = read_json(path)
        if journal.get("outcome") != "pass":
            continue
        inventory = read_json(root / "inventory.json")
        sources = inventory["range"]["ordered_source_commits"]
        if not set(sources) & set(order):
            continue
        require(sources and set(sources) <= set(order), "接受节点超出本次冻结范围")
        report, filename, closeout = accepted_report(root)
        manifest = read_json(root / "manifest.json")
        check_closeout(closeout, manifest)
        require(report.get("outcome") == "pass", "批次含未接受节点")
        name = root.name.split("-attempt-", 1)[0]
        descriptor = {"name": name, "kind": "replay", "path": root.relative_to(context.evidence_root).as_posix(),
                      "report": filename}
        result.append((sources, descriptor, manifest, closeout))
    result.sort(key=lambda item: order.index(item[0][0]))
    require([sha for sources, *_ in result for sha in sources] == order,
            "接受节点存在缺段、重叠或歧义，不能完成整批交付")
    return result


def _bridges(context, previous, descriptor, manifest):
    bridges = []
    root = context.node_root(descriptor["path"])
    for lane in context.repos:
        base = manifest["identity"].get(lane + "_base") if lane != "wlroots" else (
            manifest["identity"].get("wlroots") or {}).get("base")
        old = previous.get("final_" + lane + "_head")
        if base == old:
            continue
        candidates = []
        for path in sorted(root.glob("*repair*closeout.json")):
            require(not path.is_symlink(), "独立修复凭据不能为符号链接")
            receipt = read_json(path)
            if receipt.get("expected_old") == old and receipt.get("new_head") == base and lane + "_ref" in receipt:
                candidates.append(path)
        require(len(candidates) == 1, f"{lane} 节点间差异缺少唯一原接受凭据")
        bridges.append({"lane": lane, "path": candidates[0].relative_to(context.evidence_root).as_posix()})
    return bridges


def discover_nodes(context, source_base, source_head, task):
    """只在本批范围内沿原 closeout 找完整节点链，分支当前位置不是接受依据。"""
    require(is_full_sha(source_base) and is_full_sha(source_head), "完成入口需要冻结的完整来源 SHA")
    order = str(run_git(context.source, "rev-list", "--reverse", f"{source_base}..{source_head}")).split()
    require(order and git_succeeds(context.source, "merge-base", "--is-ancestor", source_base, source_head),
            "冻结来源范围为空或不是祖先关系")
    found = _closed_nodes(context, order)
    descriptors, previous = [], None
    for sources, descriptor, manifest, closeout in found:
        if previous is not None:
            descriptor["bridges"] = _bridges(context, previous, descriptor, manifest)
        for lane, repo in context.repos.items():
            head = manifest.get("final_" + lane + "_head")
            if head is None:
                continue
            ref = "HEAD" if task == "consolidate" else closeout["identity"][lane + "_ref"]
            require(git_succeeds(repo, "merge-base", "--is-ancestor", head, ref),
                    f"{lane} 当前归并/同步目标未包含接受候选")
        descriptors.append(descriptor)
        previous = manifest
    return {"nodes": descriptors}


def finish_batch(args):
    """完成实际文档交付；失败向正常任务入口传播，不回滚已经接受的产品节点。"""
    context = make_context(args.source_repo, args.parent_repo, args.child_repo, args.wlroots_repo,
                           args.batch, args.evidence_root, args.evidence_label, None)
    inputs = discover_nodes(context, args.source_base, args.source_head, args.task)
    context.plan_documents = plan_documents(context, args.plan_dir)
    result = generate_from_inputs(context, inputs)
    return {"task": args.task, "batch": context.batch, "records": result,
            "nodes": [node["name"] for node in inputs["nodes"]], "git_committed": False}


def run_finish(args):
    """返回的是文档交付结果，不把产品已接受等同于记录生成成功。"""
    try:
        print(json.dumps(finish_batch(args), ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as error:
        print(f"整批交付未完成（不回滚产品 refs）：{error}", file=sys.stderr)
        return 1
