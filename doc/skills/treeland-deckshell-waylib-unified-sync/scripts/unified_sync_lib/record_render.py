"""中文按仓记录；原候选验收与新身份核对始终分开。"""

from __future__ import annotations

import re
from collections import Counter

from .record_context import LINKS, ROLES, RecordContext
from .record_evidence import EVIDENCE
from .record_git import path_comparison
from .record_replay import GATES


def code(value) -> str:
    """将证据值作为 Markdown 代码值显示，不解释其链接或 HTML。"""
    value = str(value).replace("|", "&#124;").replace("\n", " ")
    fence = "`" * (max((len(v) for v in re.findall(r"`+", value)), default=0) + 1)
    return f"{fence} {value} {fence}"


def block(value, language="text") -> str:
    """原文可能包含代码围栏，使用更长的 fence 保持显示边界。"""
    if language == "diff":
        value = re.sub(r"[ \t]+$", lambda match: match[0].replace(" ", "␠").replace("\t", "⇥"),
                       value, flags=re.MULTILINE)
    fence = "`" * max(3, max((len(v) + 1 for v in re.findall(r"`+", value)), default=3))
    return f"{fence}{language}\n{value.rstrip()}\n{fence}\n"


def path_list(values) -> str:
    """按证据顺序展示路径，不排序改变原取舍顺序。"""
    return "、".join(code(value) for value in values) if values else "无"


def _identity(context, lane, nodes, rows):
    ordinary = [row for row in rows if row["kind"] == "replay"]
    first, last = nodes[0], nodes[-1]
    base, old_head = first["bases"][lane], last["heads"][lane]
    lines = [f"# {ROLES[lane]} 同步记录：{context.batch}", "",
             "这是按仓归属生成的同步事实记录，不是新的产品验收报告。",
             "原节点结果只绑定下文列出的原候选与原环境；本次生成未执行同步、构建、测试、收口或远端发布。", "",
             f"- 来源范围（左开右闭）：{code(first['source_base'])} → {code(last['source_head'])}。",
             f"- 本仓内容基线：{code(context.target(lane, base))}。",
             f"- 本仓内容终点：{code(context.target(lane, old_head))}；不含后继文档、URL/gitlink 或工具维护提交。",
             f"- 本仓普通目标：**{len(ordinary)}**；独立初始化：**{len(rows) - len(ordinary)}**；合计 **{len(rows)}**。",
             f"- 普通 action：{dict(Counter(row['action'] for row in ordinary))}。"]
    if context.history:
        lines += [f"- 原同步内容基线/终点：{code(base)} → {code(old_head)}。",
                  "- 三类身份严格区分：Treeland 来源不变；原目标由旧证据验收；整理后目标由旧新映射及 Git 对象对应。",
                  "- 生成时已逐目标核对来源、映射顺序、普通文件不变及派生 gitlink；这不是产品重新验收。"]
    else:
        lines += ["- 本批次未提供历史改写映射，仅记录真实来源 → 目标，不虚构原目标列。"]
    lines += [f"- 原需求与实施记录：[PRD](../../../{context.batch}/prd.md)、[plan](../../../{context.batch}/plan.md)。"
              if (context.repos[lane] / context.batch / "plan.md").is_file()
              and (context.repos[lane] / context.batch / "prd.md").is_file()
              else f"- 原需求/方案资料：{context.external('')}（未声称已随仓携带）。",
              "- 外层历史资料仅用标识和相对定位列出，不是本仓链接；记录不包含完整日志、构建树或安装树。",
              "- R 的短 Refs 是 P/C 共同方案标识，不承诺 R 仓内存在方案副本。", ""]
    return lines


def _mapping(context, rows):
    original = "原目标 | " if context.history else ""
    lines = ["## 有序提交映射", "", f"| 序号 / 节点 | Treeland 来源 | {original}本仓目标 | action（C 另列 content_action） | 归属 |",
             "|---|---|" + ("---|" if context.history else "") + "---|---|---|"]
    for index, row in enumerate(rows, 1):
        old = f"{code(row['old'])} | " if context.history else ""
        destination = f"[适配详情](adaptations/{row['target']}.md)" if row["action"] == "adapted" else f"[条目](#entry-{index})"
        action = row["action"] if row["lane"] == "parent" else f"{row['action']} / {row['content_action']}"
        lines.append(f"| {index} / {row['node']} | {code(row['source'])} | {old}{code(row['target'])} {destination} | "
                     f"{action} | {row['classification']} |")
    return lines + [""]


def _dependency(context, row):
    transition = row.get("transition")
    if not transition:
        return []
    path, lower = LINKS[row["lane"]]
    old_from, old_to = transition.get("from"), transition.get("to")
    lines = [f"- 依赖 {code(path)}：{transition['status']}；"
             f"{code(context.target(lower, old_from))} → {code(context.target(lower, old_to))}。"]
    if context.history:
        lines += [f"  原证据引用：{code(old_from)} → {code(old_to)}。"]
    if transition.get("url"):
        lines += [f"  当时 URL：{code(context.portable(transition['url']))}；这里只记录历史，不修改当前配置。"]
    return lines


def _row_summary(context, row, index):
    lines = [f'<a id="entry-{index}"></a>', f"### {index}. {row['node']} / {code(row['subject'])}", "",
             f"- 本仓内容路径：{path_list(row['paths'])}。",
             f"- 实际改变：{path_list(row['actual_paths'])}。",
             f"- 排除的来源路径：{path_list(row['drop_paths'])}。"]
    if row["structural_paths"]:
        lines += [f"- 已审本地集成路径：{path_list(row['structural_paths'])}。"]
    lines += _dependency(context, row)
    if row["kind"] == "initialization":
        init = row["initialization"]
        lines += ["- **独立初始化，不属于普通 replay/action 计数。**",
                  f"- 来源第一父提交：{code(init['source_first_parent'])}；导入原始 R：{code(init['wlroots_base'])}。",
                  f"- 接入方式：{code(init['integration'])}；原始历史对象不重写。",
                  f"- 依据：{context.external(row['node_path'], 'initialization-report.json')}；"
                  f"{context.external(row['node_path'], 'structure-proof.json')}。"]
    else:
        lines += [f"- lane 依据：{context.external(row['node_path'], EVIDENCE[row['lane']][0])}；"
                  f"以来源 {code(row['source'])} 和原目标 {code(row['old'])} 查询。"]
    for note in row["notes"]:
        if note != "none" and not note.startswith("Includes "):
            lines += [f"- 原审核说明：{code(context.portable(note))}。"]
    if row["action"] == "gitlink-only":
        lines += ["- **仅依赖引用传播，不是本仓源码适配。**"]
    if row["action"] == "adapted":
        lines += [f"- 逐路径理由与增量对照：[本仓适配详情](adaptations/{row['target']}.md)。"]
    if row["equivalence"] is not None:
        lines += ["- empty 的原等价证明（不把未改文件说成新适配）：", "",
                  block(context.portable(row["equivalence"]), "json")]
    other = "child" if row["lane"] == "parent" else "parent"
    if row["related"].get(other):
        directory = "docs" if other == "child" else "doc"
        lines += [f"- 同一 Treeland 来源的 {ROLES[other]} 目标：{code(row['related'][other])}；"
                  f"跨仓定位 {code(directory + '/treeland-sync/' + context.batch + '/summary.md')}，不是本仓相对链接。"]
    return lines + [""]


def _verification(context, node, previous=False):
    heading = "历史失败/先前尝试" if previous else "原节点验收"
    lines = [f"### {node['name']} / {heading}", "", f"- 原报告状态：**{node['status']}**。",
             f"- 来源验收终点：{code(node['source_head'])}；普通中间提交不作构建承诺。"]
    for lane, sha in node["heads"].items():
        lines += [f"- 原候选 {ROLES[lane]}：{code(sha)}。"]
    filename = "initialization-report.json" if node["kind"] == "initialization" else "sync-report.json"
    lines += [f"- 原报告：{context.external(node['path'], filename)}。"]
    for name, gate in node["gates"].items():
        lines += [f"- {name}：{gate.get('outcome', 'unverified')} / {gate.get('status', '未另设状态')}；"
                  f"{context.external(node['path'], GATES[name])}。"]
    lines += ["", "| 原验证项 | 结果 | 退出码 | 原测试计数 | 原始日志 |", "|---|---|---|---|---|"]
    for entry in node["validations"] + node["previous_attempts"]:
        state = entry["outcome"].upper().replace("-", "_")
        log = context.external(node["path"], entry["log"]["path"]) if entry.get("log") else "未执行/未验证，无日志"
        lines += [f"| {code(entry['id'])} / attempt {entry.get('attempt', '未记录')} | {state} | "
                  f"{entry.get('exit_code')} | {code(entry.get('tests'))} | {log} |"]
    return lines + ["", "以上状态属于原候选；未替换成整理后 SHA，也未因本次生成而重新通过。", ""]


def _path_detail(context, row, item):
    comparison = path_comparison(context, row, item["path"])
    lines = [f"### {code(item['path'])} / {item['kind']}", "",
             f"- 原审核理由：{code(context.portable(item['reason']))}。",
             f"- 路径证明：{context.external(row['node_path'], item['proof']['path'])}。",
             f"- 来源路径：{path_list(comparison['sources'])}；无来源路径表示本地集成，不冒充上游修改。",
             f"- 来源增量端点：{code(comparison['source_before'])} → {code(row['source'])}。",
             f"- 原目标增量端点：{code(comparison['target_before'])} → {code(row['old'])}。",
             f"- 本次目标：{code(context.target(row['lane'], comparison['target_before']))} → {code(row['target'])}。",
             f"- 目标文件项（mode/type/blob）：{code(comparison['target_entries'][0])} → {code(comparison['target_entries'][1])}。"]
    for source in comparison["source_entries"]:
        lines += [f"- 来源文件项 {code(source['path'])}：{code(source['before'])} → {code(source['after'])}。"]
    if comparison["comparison"]:
        lines += ["", "两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：", "",
                  block(comparison["comparison"], "diff")]
    else:
        lines += ["- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。"]
    return lines + [""]


def adaptation_document(context: RecordContext, row: dict, index: int) -> str:
    """只为本仓 adapted 目标展开证据对应的适配路径。"""
    lines = [f"# {ROLES[row['lane']]} 适配：{row['subject']}", "",
             f"- Treeland 来源：{code(row['source'])}。", f"- 本仓目标：{code(row['target'])}。"]
    if context.history:
        lines += [f"- 原同步目标：{code(row['old'])}；本页文件名采用整理后的完整目标 SHA。"]
    content_action = "" if row["lane"] == "parent" else f"；content_action={row['content_action']}"
    lines += [f"- 节点：{row['node']}；action={row['action']}{content_action}。",
              f"- [本仓总记录](../summary.md#entry-{index})。", "",
              "## 比较口径", "",
              "比较来源唯一父提交 → 来源提交，与原目标唯一父提交 → 原目标提交的逐路径增量。",
              "零上下文补丁对照会呈现基线位置、既有命名和本次实现差异；它不是整棵来源树与目标树的长期差异，也不声称所有显示行都是本次新增适配。",
              "改写后的普通文件与原目标相同；派生 gitlink 在总记录单列，不混进源码适配。原验收只适用于总记录列出的原节点候选。", "",
              "## 已审说明", "",
              "以下保留原证据文字；其中依赖 SHA 属于原运行，新依赖身份见下文与总记录。", ""]
    lines += [f"- {code(context.portable(note))}" for note in row["notes"] if note != "none"]
    lines += ["", f"保留/映射路径：{path_list(row['paths'])}。",
              f"排除路径：{path_list(row['drop_paths'])}。", "", "## 逐路径取舍与实际差异", ""]
    for item in row["adaptation_paths"]:
        lines += _path_detail(context, row, item)
    if not row["adaptation_paths"]:
        lines += ["本条 overall adapted 仅来自 .gitmodules 显式登记；普通内容没有伪造 adapted 路径。", ""]
    lines += _dependency(context, row)
    lines += ["", "## 原工件定位", ""]
    lines += [f"- {key}：{context.external(row['node_path'], value['path'])}。"
              for key, value in row["evidence"]["artifacts"].items()]
    return "\n".join(lines).rstrip("\n") + "\n"


def _r_dependencies(context, rows):
    lines = ["## 独立 R 的依赖内容", "",
             "以下源码属于独立 R，不属于 C 的普通 wlroots/ 包装层。C 的 gitlink 更新在对应条目单列；R 不新增独立记录目录。", ""]
    for row in rows:
        lines += [f"### R 来源 {code(row['source'])}", "",
                  f"- R 目标：{code(row['target'])}；action={row['action']}。"]
        if context.history:
            lines += [f"- 原 R 目标：{code(row['old'])}。"]
        lines += [f"- R 内容路径：{path_list(row['paths'])}。",
                  f"- 关联 C：{code(row['related'].get('child'))}；节点 {row['node']}。",
                  f"- 依据：{context.external(row['node_path'], 'wlroots-evidence.json')}。"]
        lines += [f"- 原 R 说明：{code(context.portable(note))}。" for note in row["notes"] if note != "none"]
        for item in row["adaptation_paths"]:
            lines += _path_detail(context, row, item)
        if row["equivalence"]:
            lines += [block(context.portable(row["equivalence"]), "json")]
        lines += [""]
    if not rows:
        lines += ["本批次没有 R 普通来源提交；初始化或未变化的 R0 见对应节点。", ""]
    return lines


def render_documents(context: RecordContext, nodes: list, rows: dict) -> dict:
    """一次渲染 P/C 文件集合，尚不写入任何仓库。"""
    documents = {}
    for lane in ("parent", "child"):
        prefix = ("doc" if lane == "parent" else "docs") + f"/treeland-sync/{context.batch}"
        lines = _identity(context, lane, nodes, rows[lane]) + _mapping(context, rows[lane])
        lines += ["## 逐项归属、路径与依赖", ""]
        for index, row in enumerate(rows[lane], 1):
            lines += _row_summary(context, row, index)
            if row["action"] == "adapted":
                documents[(lane, f"{prefix}/adaptations/{row['target']}.md")] = adaptation_document(context, row, index)
        if lane == "child":
            lines += _r_dependencies(context, rows.get("wlroots", []))
        lines += ["## 节点验证与历史边界", ""]
        for node in nodes:
            lines += _verification(context, node)
            for previous in node.get("previous_runs", []):
                lines += _verification(context, previous, previous=True)
        documents[(lane, f"{prefix}/summary.md")] = "\n".join(lines).rstrip("\n") + "\n"
    return documents
