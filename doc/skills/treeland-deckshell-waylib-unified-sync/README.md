# treeland-deckshell-waylib-unified-sync

这是 DeckShell 仓库内的统一上游同步 skill。它把调用者指定来源仓库/ref 的显式左开右闭 commit 区间一次分类，并逐提交回放到 DeckShell parent 与 waylib-shared child。来源可以使用已有的 `treeland` remote-tracking ref，也可以完全由用户手工输入本地分支、其他 remote-tracking ref、tag 或完整 SHA；不要求固定 remote 名称或 URL，也不会自动创建 remote。

- DeckShell parent：按现有 path-policy 写入 `compositor/**` 或批准的根路径；
- `3rdparty/waylib-shared` child：接收 `qwlroots/**`、`waylib/**`、`wlroots/**` 普通文件；
- 独立 wlroots 仓库 R：接收去前缀的 `3rdparty/wlroots/**`；C 以同名子模块登记并保存 R commit；
- treeland-protocols：来源 `protocols/**/*.xml` 或 parent 实际 `protocols/compositor/**/*.xml` 变更时给出 advisory 候选，不复制协议内容。

实现包含 R→C→P 逐来源回放、schema-v2 journal、两层 gitlink/对象/可达性核验、递归本地物化、Waylib 安装合同与固定基线命名空间探针、Meson/CMake/CTest 真实记录和完整报告。applied/adapted 分别核对来源/获批补丁的 type/mode/blob 投影；适配另需逐路径审核。CMake 逐节点审计包含控制流、相关变量定义及目录入口；wrapper 绑定具体消费目标链接输入，Meson 日志绑定当前执行。中间 R/C 审计失败不得推进上层。旧两仓场景保持可用，R 明确 not-applicable；旧 journal 不能直接升级后续跑。

构建粒度是**关键节点分段验收**，不是逐提交编译：预先冻结所选 tag/SHA 和整体终点，按相邻节点分段运行既有流程，每段完整验收并获准收口后接续下一段。单段报告只覆盖其终点，不自动证明其他 tag；普通中间提交不作可构建承诺。具体输入、接续与完成条件见 [关键节点分段验收](references/key-node-validation.md)。

## 安装

必须安装整个目录，不能只复制 `SKILL.md`，否则脚本、references 和 examples 会缺失。

从 DeckShell 仓库根目录执行复制安装：

```bash
install -d "$HOME/.codex/skills"
cp -a "doc/skills/treeland-deckshell-waylib-unified-sync" \
  "$HOME/.codex/skills/treeland-deckshell-waylib-unified-sync"
```

或使用目录软链接：

```bash
install -d "$HOME/.codex/skills"
ln -s "$PWD/doc/skills/treeland-deckshell-waylib-unified-sync" \
  "$HOME/.codex/skills/treeland-deckshell-waylib-unified-sync"
```

已有同名路径时先审查其来源；不要用强制覆盖隐藏本地修改。

## 安装验证

```bash
test -f "$HOME/.codex/skills/treeland-deckshell-waylib-unified-sync/SKILL.md"
test -f "$HOME/.codex/skills/treeland-deckshell-waylib-unified-sync/scripts/unified_sync.py"
python3 "$HOME/.codex/skills/treeland-deckshell-waylib-unified-sync/scripts/unified_sync.py" --help
python3 -m unittest discover \
  -s "$HOME/.codex/skills/treeland-deckshell-waylib-unified-sync/tests" -v
```

## 调用

在 Codex/CLI 中明确点名：

```text
使用 $treeland-deckshell-waylib-unified-sync。

source_repo: <包含手工指定来源对象的本地 DeckShell 仓库>
source_ref: <可选、可省略的来源标识；不作为 remote 绑定>
source_tip: <用户手工输入的来源 tip ref/SHA>
range_base: <当前分段不包含的来源 SHA>
range_head: <当前分段包含的必验节点 SHA>
parent_target_ref: refs/heads/<目标分支>
child_repo: <DeckShell/3rdparty/waylib-shared>
child_target_ref: refs/heads/<目标分支>
artifact_root: <持久且位于所有 worktree 外的目录>

要求：在 refs_doc 中冻结整体范围和全部关键节点，当前分段按来源逐节点 R→C→P；构建前递归 materialize-child，段末完成九项门禁（含 protocol_pairing）、默认完整 build、安装/测试、package consumer 和报告。本段通过且授权覆盖后执行 expected-old closeout，再以新基线接续下一段。整批接受后以 finish --task sync 自动交付两仓记录；将接受结果归并到日常主分支时使用 finish --task consolidate。不自动提交、push 或改外层 gitlink；R 启用时补齐必要输入，不猜 SHA/URL。
```

详细顺序和阻断条件见 [SKILL.md](SKILL.md)，输入清单见 [examples/unified-sync.example.yaml](examples/unified-sync.example.yaml)。

## 公开脚本

| 脚本 | 职责 |
|---|---|
| `unified_sync.py` | `inventory`、journaled `replay`、`materialize-child`、child-first `closeout`；整批 `finish` 自动准备方案副本、核对接受历史并生成两仓记录 |
| `deckshell_verify.py` | parent 顺序、目标路径权威、消息和证据 |
| `waylib_inventory.py` | 兼容的独立 inventory 入口 |
| `waylib_traces.py` | child trailer、顺序、分类与路径边界 |
| `waylib_verify.py` | child action、内容证据、工件哈希与更新脚本保留规则 |
| `gitlink_verify.py` | gitlink mode/object/reachability/from-to/purity |
| `wlroots_verify.py` | R 内容投影/追溯及 C→R 嵌套 gitlink；输出两个 gate |
| `protocol_tracker.py` | 零/单/多协议候选的 advisory 输出 |
| `waylib_contract_audit.py` | 安装树、真实 CMake 导出属性、namespace、pkg-config 展开后的动态/静态参数与 consumer 合同 |
| `validation_record.py` | 无 shell 执行验证；必需 CMake build 只接受默认完整构建；经 Git 证明的空 R 基线记录为不适用 |
| `artifact_record.py` | 为 adapted/empty 决策复制并哈希工件 |
| `generate_sync_report.py` | 仅从真实 JSON 证据生成当前分段终点报告，不声称覆盖其他 tag |
| `generate_repo_records.py` | 从有序节点原证据、实际 Git 对象及可选旧新映射生成 P/C 各自的批次总记录和 adapted 详情，不执行同步或 Git 写操作 |

## 同步记录留存

同步整批完成、相关主分支归并和中断恢复的正常收尾均使用 [SKILL.md §12](SKILL.md#12-正常任务完成自动交付两仓记录) 的 `finish`，不需要用户另外要求生成记录。它自动从本批原 closeout 选择接受节点、拒绝缺段和歧义，再准备副本、核对并生成/复用两仓文档；失败以非零状态返回，不能宣布完整交付。P 仅展开 P 内容和依赖传播，C 展开 C 内容并单列独立 R 依赖；dual 通过同一 Treeland SHA 关联。原节点 FAIL/SKIP、限定授权、未验证与 `NO_TESTS` 均保留，记录不能替代节点验收。

调用参数、节点输入、可选历史映射及输出保护见 [按仓记录生成](references/repo-records.md)，输入示例见 [repo-records.example.json](examples/repo-records.example.json)。普通同步省略 `--history-map`；经另行授权重写历史后才提供完整旧新对应。输出只进入 P `doc/treeland-sync/<batch>/` 和 C `docs/treeland-sync/<batch>/`；任何已有内容冲突明确失败，不覆盖旧文档。

本仓 `plan.md`、`prd.md` 副本与 summary 同目录保存。正常 `finish` 负责从原同步方案准备可携带副本并纳入同次预检/交付；已有副本必须字节相同，不能覆盖冲突。低层 `generate_repo_records.py` 仍把它们当只读输入，不创建、修改、删除或计数；该入口也继续支持专属初始化证明与历史映射。不查找旧根目录，不删除未知批次文件或符号链接解除冲突。

## 运行要求

- Python 3.9+；仅使用标准库。
- Git 支持 linked worktree、`update-index --cacheinfo` 和 `update-ref <new> <old>`。
- 安装合同审计及测试需要 CMake 3.27+、C/C++20 编译器、CTest、Ninja、Meson、pkg-config 及被审 package 的配置依赖；失败不能退回文本扫描或空属性快照。
- 产品验证还需要 Qt/Wayland 依赖；工具的隔离三仓 fixture 不替代真实产品验证。
- replay 不负责解决内容冲突；冲突会写 journal 并阻断。人工适配需形成目标相对补丁和内容寻址记录后，用新运行重开。

## 边界

- 普通中间提交可不构建，但所有选定关键节点和整体终点必须有独立段末证据；最后一段 PASS 不代表整组完成。旧局部构建记录、旧字面 pkg-config 快照和旧报告须重新验证，不能补字段沿用。
- `wlroots/**` 始终是 C 普通文件，只有 `3rdparty/wlroots` 是子模块。R0 须绑定来源基线投影，不拿目录 tree SHA 或 UPSTREAM pin 充当 candidate。
- 仅来源基线无 R 子树且 R0 整个根树为空时，三个 R 基线构建记录自动记 `not-applicable`；候选仍真实构建，不把豁免写成 NO_TESTS，也不省略 R 内容/gitlink gate。
- 应保留的更新脚本不能被普通 `omitted`/`empty` 证明免除；回放、恢复与独立验证均从 Git 对象检查文件存在性、普通类型和拒绝执行前缀。
- 首次 subtree 导入若为 merge，必须先单独授权、审核初始化基线，再处理后续非 merge 区间；空 R0 不开放 merge 回放，见 [初始化边界](references/unified-contract.md#首次-subtree-导入边界)。
- 来源 ref、协议 ref 均由调用者提供；不检查 remote 名称、URL 或固定 tracking ref。
- protocol candidate 只表示相似度候选，不表示来源确认；候选搜索覆盖 `xml/`、`dde/`、`public/`、`internal/`、`wine/`、`deprecated/`。
- C/P 构建使用 manifest 绑定的递归候选；缺 R、错误对象库、脏工作树、目录越界或缺物化记录都会阻断。
- closeout 只更新获准的两仓或三仓本地目标 refs，按 R→C→P CAS；refs 必须未被检出，部分成功保留现场并支持同身份续作。
- 本地同步完成不等于远程发布。
