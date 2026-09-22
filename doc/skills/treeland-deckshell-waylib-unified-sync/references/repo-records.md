# 按仓同步记录生成

读者是维护 P/C 仓库、需要查询来源、适配和原验证边界的人。本入口消费已有证据，不重新同步，不创建替代节点报告的验收系统。Python 最低为 3.9；完整工具测试及安装合同审计要求 CMake 3.27+。

## 调用

```bash
python3 "$SKILL_DIR/scripts/generate_repo_records.py" \
  --source-repo "$SOURCE_REPO" \
  --parent-repo "$PARENT_REPO" \
  --child-repo "$CHILD_REPO" \
  --wlroots-repo "$WLROOTS_REPO" \
  --batch "$BATCH" \
  --evidence-root "$ORIGINAL_PLAN_ROOT" \
  --evidence-label ".helloagents/plans/$BATCH" \
  --nodes "$NODES_JSON"
```

- `source-repo`、P/C/R 必须是实际 Git 工作树根；不同 linked checkout 可以访问原 evidence 绑定的同一个 common Git directory。P/C/R 不能是同一对象库。空 R 子目录向上识别为 C 时明确失败。
- 无 R 的普通两仓输入省略 `--wlroots-repo`。整组含独立初始化或任何 R 内容时必须提供 R。
- `batch` 是调用方指定的稳定单目录标识，不使用每次生成时间；只接受字母、数字、点、下划线、连字符，不接受路径穿越。
- `evidence-root` 是原节点资料所在的目录。`evidence-label` 是无本机绝对前缀的历史资料标识；文档以“外层历史资料”定位，不把未复制资料伪装成本仓相对链接。
- `--nodes` 读取[节点输入示例](../examples/repo-records.example.json)。各节点来源区间及 P/C/R 内容端点必须连续，全部本仓对应提交必须覆盖，空提交也不能遗漏。
- 普通同步不需要 `--history-map`，文档只写来源与真实目标两类 SHA。只有独立获准整理过历史时才追加该参数；本入口不会自行重写历史。

命令成功时输出 P/C 各自的目标记录数、文件数和 adapted 数。退出 0 只说明记录生成完成，不表示产品或发布验收通过。错误返回非零并说明缺失或冲突；不降级为部分摘要。

## 节点输入

根对象为 `{"nodes": [...]}`，每个节点包含：

- `name`：稳定节点名，例如 `N1`；唯一且仅含安全标识字符。
- `kind`：`replay` 或 `initialization`。
- `path`：相对 `evidence-root` 的原工件目录，不允许绝对路径、`..` 或符号链接逃出证据根。
- `previous_runs`（可省略）：同一来源范围的先前普通节点报告，以同样的 `name/kind/path` 定位；只显示其原候选、状态和日志，不将其提交重复计入本仓覆盖。

普通节点读取既有默认文件名：`inventory.json`、`manifest.json`、`parent-evidence.json`、`waylib-evidence.json`、适用的 `wlroots-evidence.json`、`validations.json`、`sync-report.json` 及该报告绑定的八项 gate JSON。自定义文件名的历史运行需由调用方提供对应的只读证据布局；不得修改原工件内容、重新赋予旧报告新的身份。

独立初始化读取 `initialization-report.json`、`structure-proof.json`、`source-contract-approval.json`、`validations.json`。报告必须明确 `ordinary_replay: false`；候选、原始 merge 双亲、R 导入树与可达历史、相邻 P/C 差异及工作树身份必须可由真实 Git 对象重算。没有普通 manifest，不能给初始化编造普通 replay action。

生成器复用已有 schema、artifact 完整性和报告绑定；核对 lane evidence 与 manifest、实际来源/目标补丁、逐路径审核说明及 empty 等价证明。`pass`、`fail`、`blocked`、`no-tests`、`not-applicable` 和明确未执行的 `unverified`/`not-run` 原样区分；已执行记录没有日志时失败。未完成回放、来源/映射缺项或证据不一致时不生成貌似完整的记录。

## 可选旧新映射

```json
{
  "batch": "调用方的批次",
  "repositories": {
    "parent": {
      "base": "区间左端完整 SHA",
      "old_head": "原内容终点完整 SHA",
      "new_head": "整理后内容终点完整 SHA",
      "commits": [{"old": "原目标完整 SHA", "new": "整理后目标完整 SHA"}]
    },
    "child": {"base": "...", "old_head": "...", "new_head": "...", "commits": []},
    "wlroots": {"base": "...", "old_head": "...", "new_head": "...", "commits": []}
  }
}
```

这是格式说明，不是可直接运行的 SHA 示例。`commits` 按原 Git 历史顺序完整列出，不能漏掉初始化或 empty；R0 等区间外基线不放入重写列表。没有 R 时省略 `wlroots`。新旧目标须一一对应，保留直接父拓扑、原来源 trailer，以及除两层指定 gitlink 外的所有普通文件项；消息中原验收引用仍属于旧证据，不被替换后声称重新通过。文档、URL 或工具维护等后继提交不放进内容映射。

## 输出与归属

| 仓库 | 总记录 | adapted 详情 | 只读方案副本 |
|---|---|---|---|
| P | `doc/treeland-sync/<batch>/summary.md` | 同目录 `adaptations/<P 当前目标完整 SHA>.md` | 同目录 `plan.md`、`prd.md` |
| C | `docs/treeland-sync/<batch>/summary.md` | 同目录 `adaptations/<C 当前目标完整 SHA>.md` | 同目录 `plan.md`、`prd.md` |

- P/C 各自展开本仓内容、实际路径、保留/排除范围及适配；dual 以同一 Treeland SHA 和对方仓库标识关联，不使用无法解析的跨仓相对链接。
- P 的纯 C gitlink 传播不生成伪源码适配。C 的普通 `wlroots/**` 包装层与 R 的源码分开，R 普通提交、路径、适配与旧新目标在 C 的独立依赖章节记录；R 不新增文档目录。
- overall `adapted` 与 `content_action` 分开。首次登记 `.gitmodules` 可以是 overall adapted，而普通内容仍为 applied 或不适用；不捏造空的 C 源码适配理由。
- 适配详情以逐路径审核为依据，对比“来源父提交 → 来源提交”与“原目标父提交 → 原目标”的零上下文增量，并列出 mode/type/blob。补丁的文本对照会保留 hunk 位置与既有本地差异；尾空格和 Tab 分别显示为 `␠` 和 `⇥`，避免把原补丁空白变成新 Markdown 的格式错误。对照不宣称是可直接应用的纯适配 delta，也不拿完整目标 diff 或整树长期差异冒充纯适配；原始字节仍可按 Git 对象与原工件定位核对。
- 总记录明确验收属于原节点、原候选、原环境；新旧内容对应核对不等于重新运行产品构建或测试。N2 独立初始化不混入普通来源计数。
- 仅在表列规范批次目录中发现本仓方案。`prd.md` 和 `plan.md` 两份普通文件同时存在时，总记录使用 `prd.md`、`plan.md` 同目录相对链接；缺少任一份时标记为外部资料，不回退到仓库根部的 `<batch>/` 查找。
- 规范批次目录根部的 `plan.md`、`prd.md` 是受保护的只读输入，不是生成文件；无论是否成对存在，生成器均不创建、复制、覆盖或删除它们，也不计入输出文件数。符号链接和同名目录不能充当方案副本；日志、工作树或安装树也不由生成器复制。
- 只允许上述两个精确文件名作为非生成文件；`manual.md`、`adaptations/plan.md` 等其他批次文件仍视为冲突。summary 或 adaptation 内容不一致仍失败，不提供强制覆盖或忽略未知文件选项。

先验证全部证据、渲染两仓文件集合并检查所有目标冲突，再写入。重复执行同一输入只接受完全相同的文件集合和字节；旧报告、其他批次、手写内容和符号链接不被覆盖或删除。写入中途出现并发冲突会明确失败并保留已写事实，重试仍检查内容一致性；不伪装跨仓原子提交。生成器不执行任何暂存、提交、ref 更新、远端查询或发布。
