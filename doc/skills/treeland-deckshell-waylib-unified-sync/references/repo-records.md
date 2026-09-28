# 按仓同步记录生成

读者是维护 P/C 仓库、需要查询来源、适配和原验证边界的人。本入口消费已有证据，不重新同步，不创建替代节点报告的验收系统。Python 最低为 3.9；完整工具测试及安装合同审计要求 CMake 3.27+。

## 正常同步与归并的完成入口

按 [技能 §12](../SKILL.md#12-正常任务完成自动交付两仓记录) 调用 `unified_sync.py finish --task sync|consolidate`。这是正常任务的必做收尾，不是用户另外提出文档请求才执行的工具。执行者从当前任务及原方案取整批范围、批次、证据和方案目录；CLI 自动发现本批已接受节点，再直接准备副本、生成并核对两仓文件。无关任务和只读任务不触发。

- `--source-base/--source-head` 必须是整体范围的完整 SHA；不能用最后一个节点的局部范围冒充整批。扫描仅限显式证据根下的 `*/closeout-journal.json` 或 `evidence/*/closeout-journal.json`，不扫描所有历史。
- 只读取 `outcome=pass` 的原收口，并按其 `identity.report_sha256` 查找唯一接受报告。多个接受 attempt 覆盖同一来源、缺段、重叠或范围越界均失败；不是按最高 attempt、mtime、文件名 `final` 或浮动 HEAD 选结果。
- `sync` 核对 closeout 的原目标 refs 已包含候选；`consolidate` 核对所传仓库当前 HEAD 已包含候选。后者只完成相关批次文档，不替代已获准的归并，也不重新回放、移动任何 ref。重复同步/归并收尾使用相同证据生成相同字节，不记录会漂移的今天分支 tip。
- `--plan-dir` 指向原同步 `plan.md`/`prd.md` 所在目录（允许归档），不是补档或归并方案。完成入口在内存中准备参考副本，注明权威来源及历史时点，仅转换外部链接和本机前缀；原文不改。两份副本缺失、链接不安全或已有副本内容冲突时停止，不能降级成外部资料版后声称完成。
- 两仓全部证据和输出先预检，成功后共用现有不覆盖写入路径。中断后补缺失文件、复用相同文件，手写冲突与符号链接明确失败。生成异常以非零状态返回正常任务；产品节点已接受不等于文档已交付，不回滚产品。
- 只自动解释具备上述原收口布局的回放批次；初始化与历史改写仍按下面已有专属输入验证，不从缺失的初始化接受依据猜 PASS。遇到这种证据布局缺口须报告确切缺口，不能跳过节点而交付部分批次。

完成入口的 `records`、`adaptations` 不包含方案副本，`files` 包含实际交付的副本。`adaptations` 仅计 ordinary adapted；特殊提交另有详情页面，不伪装成普通 adapted。退出 0 表示实际两仓文档已写出或完全相同地复用，`git_committed: false`；不表示产品重新验证、Git 入库或发布完成。

## 低层记录生成调用

已有专属节点清单、历史改写映射或只需重现原记录时使用以下入口。正常同步/归并收尾不要求用户记忆这个命令。

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
- `report`（可省略）：接受报告文件名。有 closeout 时必须匹配其原绑定；不能将后补展示报告指定成接受报告。
- `bridges`（可省略）：仅用于节点之间已独立接受的结构修复，每项为 `{"lane": "parent", "path": "evidence/<node>/structural-repair-closeout.json"}`；路径相对证据根。正常 `finish` 按真实前后端点发现唯一匹配，不需用户手工列举。

普通节点读取 `inventory.json`、`manifest.json`、`parent-evidence.json`、`waylib-evidence.json`、适用的 `wlroots-evidence.json`、`validations.json` 和原接受报告绑定的 gate JSON。旧合同为八项；存在协议更新身份或配对报告时必须有第九项 `protocol_pairing`，缺少或绑定错误即失败，不能向旧报告补造 PASS。无 closeout 的低层历史读取仍保留原 `sync-report.json` 状态，但正常 `finish` 不将它当接受节点。

接受报告、原阻断报告和其它报告版本分开：N8a 的原 BLOCKED 与被 closeout 绑定的授权后报告同时展示；N8b 的后补 `sync-report-final.json` 不覆盖其原接受报告。限定 SKIP 只读校验原报告绑定的授权、批次/节点、manifest、验证 attempt、原 CTest 日志与完整发现集合；原 FAIL、唯一授权 SKIP 与原接受依据并列，不证明 DRM/GPU 行为，也不授予未来例外。错误节点/候选/attempt、缺日志、过滤命令、额外失败或超出跳过集合均失败。

`manifest.protocol_update` 和 `local_fix` 不进入普通来源计数。复用原 companion/local-fix 校验及 Git 增量，检查真实父子 gitlink 和相邻提交。节点间 bridge 只接受已有 `treeland-…structural-repair-closeout` 凭据，核对版本、授权、独立来源声明、前后节点精确端点和原验证日志；不允许隐含依赖变化。完整目标历史仍必须逐项相等，未知额外提交不能自动归类为修复。

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
- 低层 `generate_repo_records.py` 仍把规范批次根部 `plan.md`、`prd.md` 当受保护只读输入，不创建、复制、覆盖、删除或计入其输出数。正常 `finish` 负责先准备这两份副本并纳入同一次两仓预检/写入；既有副本必须字节一致，不覆盖不同内容。两入口均拒绝符号链接和同名目录，不复制日志、工作树或安装树。
- 只允许上述两个精确文件名作为非生成文件；`manual.md`、`adaptations/plan.md` 等其他批次文件仍视为冲突。summary 或 adaptation 内容不一致仍失败，不提供强制覆盖或忽略未知文件选项。

先验证全部证据、渲染两仓文件集合并检查所有目标冲突，再写入。重复执行同一输入只接受完全相同的文件集合和字节；旧报告、其他批次、手写内容和符号链接不被覆盖或删除。写入中途出现并发冲突会明确失败并保留已写事实，重试仍检查内容一致性；不伪装跨仓原子提交。生成器不执行任何暂存、提交、ref 更新、远端查询或发布。
