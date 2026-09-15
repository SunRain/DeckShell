"""独立初始化事实；不把 subtree merge 伪装成普通 replay。"""

from __future__ import annotations

from pathlib import Path

from .git_ops import common_git_dir, read_json, run_git
from .record_context import LINKS, RecordContext, require
from .record_git import changed, check_pair, check_transition, entries, parent_of, target_message
from .record_replay import validations


def _check_initialization(context, candidate, proof):
    require(proof.get("kind") == "treeland-independent-initialization-structure", "初始化结构证明类型错误")
    require(proof.get("candidate") == candidate, "初始化候选与结构证明错配")
    source = candidate["source_merge"]
    parents = str(run_git(context.source, "show", "-s", "--format=%P", source)).split()
    require(parents == proof["merge_parents"] == [candidate["source_first_parent"], candidate["wlroots_base"]],
            "初始化 merge 双亲不符")
    r0 = candidate["wlroots_candidate"]
    require(r0 == candidate["wlroots_base"], "初始化不得伪造 R 普通对应提交")
    source_tree = str(run_git(context.source, "rev-parse", f"{source}:3rdparty/wlroots")).strip()
    r_tree = str(run_git(context.repos["wlroots"], "rev-parse", f"{r0}^{{tree}}")).strip()
    require(source_tree == r_tree == proof["source_tree"] == proof["wlroots_tree"], "初始化 R 子树不符")
    original = str(run_git(context.source, "rev-list", r0)).split()
    imported = str(run_git(context.repos["wlroots"], "rev-list", r0)).split()
    require(original == imported and len(original) == proof["source_history_count"] == proof["imported_history_count"],
            "初始化导入历史不完整")
    for lane in ("parent", "child"):
        old = candidate[f"{lane}_candidate"]
        require(parent_of(context.repos[lane], old) == candidate[f"{lane}_base"], "初始化父提交错误")
        paths = changed(context.repos[lane], candidate[f"{lane}_base"], old)
        require(paths == proof[f"{lane}_changed_paths"], f"初始化 {lane} 路径证明错误")
        checkout = proof["checkouts"][candidate[f"{lane}_worktree"]]
        require(Path(checkout["common_git_dir"]).resolve() == common_git_dir(context.repos[lane]),
                f"初始化 {lane} 仓库身份错配")
        lines = target_message(context.repos[lane], old)
        for key, value in (("Treeland-First-Parent", parents[0]), ("Treeland-Imported-Commit", r0)):
            require(lines.count(f"{key}: {value}") == 1, "初始化来源 trailer 错误")


def initialization_node(context: RecordContext, descriptor: dict) -> tuple:
    """从独立报告、结构证明和实际对象读取初始化，不补造 manifest。"""
    require("wlroots" in context.repos, "初始化需要真实 R 仓库")
    root = context.node_root(descriptor["path"])
    report = read_json(root / "initialization-report.json")
    require(report.get("kind") == "treeland-independent-initialization-report"
            and report.get("ordinary_replay") is False, "不是独立初始化报告")
    candidate = report["candidate"]
    require(candidate.get("ordinary_replay") is False, "初始化候选不能是普通 replay")
    proof = read_json(root / "structure-proof.json")
    _check_initialization(context, candidate, proof)
    validation = read_json(root / "validations.json")
    records = validations(root, validation)
    require(set(report["validation_results"]) == {v["id"] for v in records}, "初始化验证条目不完整")
    for record in records:
        result = report["validation_results"][record["id"]]
        require(all(result.get(k) == record.get(k) for k in ("outcome", "exit_code", "tests", "log")),
                "初始化报告与原验证状态不一致")
    node = {"name": descriptor["name"], "kind": "initialization", "path": descriptor["path"],
            "source_base": candidate["source_first_parent"], "source_head": candidate["source_merge"],
            "bases": {lane: candidate[f"{lane}_base"] for lane in context.repos},
            "heads": {lane: candidate[f"{lane}_candidate"] for lane in context.repos},
            "report": report, "gates": {}, "validations": records,
            "previous_attempts": validation.get("previous_attempts", []), "status": report["outcome"],
            "initialization_proof": proof}
    approval = read_json(root / "source-contract-approval.json")
    require(approval.get("review_state") == "approved" and bool(approval.get("reason")), "初始化接入理由缺失")
    rows = {lane: [] for lane in context.repos}
    for lane in ("parent", "child"):
        rows[lane].append(_initialization_row(context, node, lane, candidate, approval))
    return node, rows


def _initialization_row(context, node, lane, candidate, approval):
    old, source = candidate[f"{lane}_candidate"], candidate["source_merge"]
    new = check_pair(context, lane, old, source, initialization=True)
    path, _ = LINKS[lane]
    repo = context.repos[lane]
    before, after = entries(repo, candidate[f"{lane}_base"]), entries(repo, old)
    transition = {"from": before[path].split()[-1] if path in before else None,
                  "to": after[path].split()[-1], "status": "registered" if path not in before else "updated"}
    check_transition(context, lane, old, transition)
    actual = node["initialization_proof"][f"{lane}_changed_paths"]
    if lane == "parent":
        require(actual == [path], "P 初始化不是纯 gitlink 更新")
    notes = ["独立初始化，只传播已审核的 C 依赖；没有 P 源码适配。"] if lane == "parent" else [approval["reason"]]
    return {"kind": "initialization", "lane": lane, "node": node["name"], "node_path": node["path"],
            "source": source, "old": old, "target": new, "subject": "首次 wlroots 独立初始化",
            "classification": "独立初始化", "action": "initialization", "content_action": "非普通 replay",
            "paths": [v for v in actual if v != path], "actual_paths": actual, "structural_paths": [],
            "drop_paths": [], "notes": notes, "adaptation_paths": [], "equivalence": None,
            "transition": transition, "initialization": candidate,
            "related": {role: context.target(role, value) for role, value in node["heads"].items()}}
