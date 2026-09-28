"""特殊提交的可读增量及原授权展示，不借用普通 adapted 的来源语义。"""

from .git_ops import run_git
from .record_git import entries


def special_document(context, row, index):
    """为真实特殊目标展示逐路径 Git 增量和原说明，不制造上游来源。"""
    from .record_render import block, code
    repo, head, base = context.repos[row["lane"]], row["target"], row["base"]
    lines = [f"# {row['kind']}：{row['subject']}", "", f"- 类型：{row['kind']}；不属于普通 Treeland 来源映射。",
             f"- 直接父提交：{code(base)}；本仓目标：{code(head)}。",
             f"- [本仓总记录](../summary.md#entry-{index})。", "", "## 原依据与取舍", ""]
    lines += ["- " + code(context.portable(note)) for note in row["notes"] if note]
    lines += ["- " + context.external(row["node_path"], path) for path in row["evidence_locations"]]
    lines += ["", "原授权说明适用于其列出的修复范围；下列逐路径增量来自真实 Git，不从主题推测额外理由。", ""]
    before, after = entries(repo, base), entries(repo, head)
    for path in row["paths"]:
        diff = str(run_git(repo, "diff", "--no-ext-diff", "--no-textconv", "--no-renames", "--unified=0", base, head, "--", path))
        lines += [f"## {code(path)}", "", f"- mode/type/blob：{code(before.get(path))} → {code(after.get(path))}。",
                  "", block(context.portable(diff), "diff"), ""]
    lines += ["原记录不等于本次重新构建/测试；未把后续补档提交作为已接受产品候选。", ""]
    return "\n".join(lines)


def exception_lines(context, node):
    """并列原失败观察与限定接受依据，保持授权作用域和原始状态。"""
    from .record_render import code
    result = []
    before = node.get("original_report")
    if before:
        result += [f"- 原报告状态：{before['outcome'].upper()}；"
                   + context.external(node["path"], before["path"]) + "；原字节保留。"]
    if node.get("closeout"):
        result += ["- 原接受收口：" + context.external(node["path"], "closeout-journal.json")]
        root = context.node_root(node["path"])
        supplements = [p.name for p in sorted(root.glob("sync-report*.json"))
                       if p.name not in (node["report_path"], "sync-report.json")]
        for name in supplements:
            result += ["- 其他报告版本：" + context.external(node["path"], name)
                       + "；未被该次 closeout 绑定，不替代原接受报告，也不表示重新收口。"]
    exception = node.get("exception")
    if exception:
        auth = exception["authorization"]
        result += ["- 限定授权：" + context.external(node["path"], exception["path"]),
                   f"- 授权仅属 {code(auth['plan'])} / {code(auth['node'])}："
                   + code(auth["scope"]) + "。",
                   "- 原验证 FAIL/SKIP 保持原样；按该节点原授权接受唯一限定跳过，"
                   "不证明 DRM/GPU 行为通过，不外推到其它节点或未来批次。"]
    return result
