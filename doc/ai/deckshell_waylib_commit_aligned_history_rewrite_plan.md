# DeckShell commit-aligned history v1/v2 编译原子与协议历史对齐 - 实施记录

## 目标与范围

本方案是 predecessor
`.helloagents/plans/202607251119_commit-aligned-history-generator-v1-v2-correction/`
的后继修正，不是从 predecessor 任务 10 继续执行。

本方案重建两条证明链：

1. **编译依赖链**：C++、CMake、Waylib capability 与 workaround 生命周期在历史节点中
   形成可构建的原子 bundle；
2. **协议来源链**：`treeland-protocols` 的 XML 历史按提交顺序映射到 DeckShell 仓库内，
   并与消费端在同一 owner transition 落地。

本次 corrected-v1/v2 历史生成已获得执行授权；任务 1-16 可自动执行，`ds-mod` expected-old CAS 仍是唯一需要单独明确授权的 ref 事务。

## 事实基线

### Git 对象

| 角色 | 规划快照 |
| --- | --- |
| `ds-mod` | `6e96d91b6eb526e5dcc8ba6793fc152eb46dc495` |
| predecessor corrected-v2 | `821378261815d3af21a6ad13a709610ca3e253a9` |
| predecessor corrected-v2 tree | `0a5654fb4cf33418e9cdf7650236446707321ad0` |
| master oracle | `d83f92fc271ab830950345cd5bd109fc2ca36a28` |
| master tree | `6d9f8cc5ec56a071ef39ac8e95f503d82e3e09b0` |
| treeland-protocols expected endpoint | `becded8970ff0b7440a00e8c6d5c4f43867c55f1` |
| treeland-protocols expected tree | `ab850b37bf123fad630318cff815586cb1bbd403` |

这些值是方案创建快照。正式执行必须重新读取 live refs；除一次协议 remote fetch 外，
任何漂移都 fail closed，不能把表中 SHA 当作无条件更新授权。

### predecessor 失败边界

- index 133 fresh configure PASS、full build FAIL；
- 首个错误为 `XdgDialogManagerV1Bridge` incomplete type；
- 临时补入定义后继续暴露 `lcTlShell`、`qw_xdg_toplevel`、
  `SurfaceWrapper::setModal` 未到位；
- 移除过早 dialog workaround 后又暴露 wine protocol signature 错位；
- 任务 3 缺少其自身要求的首节点构建证明；
- 任务 4-9 只能视为 provisional artifacts；
- 任务 11-14 不具备进入条件。

### r4 失败与 r5 当前基线

- corrected-v2 r4 风险矩阵在 40/76 PASS 后于 index 148 的 `test_scroll_factor` 稳定失败；
  r4 partial、ledger 与 Task 5-13 evidence 已冻结，禁止复用其 PASS。
- 失败揭示测试运行时生命周期 consumer index 148 依赖 Waylib provider index 314；新增
  `test-runtime-waylib-capability` edge 后，bundle owner=148、source indices=`[148,314]`。
- r5 dependency authority 为 `D=129`、dependency components=669、bundles=226。
- corrected-v1 r5 ref 为
  `refs/heads/migration/commit-aligned-history-corrected-v1-compile-atomic-r5-20260729`，
  head=`8abf2c35212414f0cec38f2fdb8ff5fcb3295158`。
- corrected-v2 r5 ref 为
  `refs/heads/migration/commit-aligned-history-corrected-v2-compile-atomic-r5-20260729`，
  head=`c7c327522e9309c24771cc6aa2cf443dbb64a9a6`；Task 11/12 已通过。
- r5 正式分类器的双候选事实为 `14+1+21+20=S=56`、`P=6`、`R=11`、`B=70`；
  相对 r4 移除 `291,297,304,305,306,314`，index 148 新命中 `gitlinkAndCompositor`。

## 架构与实现策略

### 1. 权威来源顺序

执行器必须按以下顺序消费输入：

1. 本方案包 `requirements.md` 与 `detailed-conclusion.md`；
2. 执行时生成的 immutable input lock；
3. 冻结的 `treeland-protocols` commit/tree/range/XML object inventory；
4. `protocol-transition-ledger`；
5. `dependency-bundle-ledger`；
6. normalized Treeland source、精确 WaylibShared objects 与 predecessor remediation
   ownership evidence；
7. 冻结 master product oracle；
8. predecessor preview、mapping、formal evidence 和失败 candidate，仅作对照。

任何低优先级输入与高优先级合同冲突时，必须停止而不是兼容两套路线。

### 2. 隔离执行工件

执行阶段在当前会话下创建新的版本化目录，不复用 predecessor 的可写 artifact：

```text
.helloagents/sessions/deckshell/<session>/artifacts/
  commit-aligned-history-compile-atomic-protocol-alignment/
    inputs/
      predecessor-lock.json
      refs-before.json
      build-environment.json
      treeland-protocols-lock.json
      treeland-protocols-xml-inventory.json
      anchor-protocol-provenance.json
      master-product-manifest.json
    ledgers/
      protocol-transition-ledger.v1.json
      dependency-bundle-ledger.v1.json
      dependency-sensitive-set-D.json
    tools/
      v1/
      v2/
      build-matrix/
    corrected-v1/
      preview-A/
      preview-B/
      formal/
    corrected-v2/
      preview-A/
      preview-B/
      formal/
    proof-nodes/
      index-1/
      index-81/
      index-83/
      index-133/
      index-136/
      index-141/
    build-matrix/
      risk-selected-70/
        selection-manifest.json
        nodes/
        summary.json
      selection-coverage-330/
        report.json
    qa/
      final/
      ref-transaction/
```

每个 JSON 使用 canonical serialization 并生成同目录 `.sha256`。对象库、build directory、
日志和 mapping 均不得在 preview A/B 之间共享。

### 3. 输入锁与远端协议冻结

任务 1 已完成本方案唯一一次 fetch；以下命令只记录已经发生的输入冻结动作，禁止重跑：

```text
git -C treeland-protocols fetch origin master
```

该 fetch 后已立即解析并冻结：

- `FETCH_HEAD`/`origin/master` commit 与 tree；
- endpoint ancestry；
- XML 变更提交的有序集合；
- 每个提交的 parent、tree、changed XML path、mode、before/after blob；
- endpoint 的 XML inventory 与 canonical SHA-256。

冻结完成后，所有生成和验证都只读取精确对象 ID。后续任务禁止再次 fetch 或读取可变
remote-tracking ref；endpoint 已验证等于规划快照 `becded897...`。

明确禁止读取 `/usr/share/treeland-protocols`。该路径只允许作为静态禁止字符串进入测试或
文档，不能作为命令参数、输入目录或 fallback。

### 4. self-contained anchor

旧 index 1 commit object 不能复用。新 anchor 由原节点的 parent、消息和业务 tree 派生，
只增加完成仓库自包含所必需的历史修正：

1. 解析旧 anchor 的协议集合；
2. 为每个 XML 建立 upstream commit provenance；
3. 无法匹配 upstream blob 的 hunk 登记为 DeckShell local overlay；
4. 物化该节点实际消费的协议版本，不提前引入未来 XML；
5. 将 in-tree 构建统一切换到 `DECKCOMPOSITOR_PROTOCOLS_DATA_DIR`；
6. 移除 `find_package(TreelandProtocols)` 与旧变量；
7. 静态验证生成命令只引用源码树 XML；
8. 在 fresh build directory 完成 configure、full build 与适用 CTest。

anchor 的 changed-path authority 只允许协议包、相关 consumer CMake 和必要 provenance 文档；
任何业务源码差异必须为 0。

### 5. `protocol-transition-ledger`

每个协议 component 至少包含：

```json
{
  "protocol_component_id": "treeland-protocols:<commit>:<path>",
  "source_commit": "...",
  "source_parent": "...",
  "source_tree": "...",
  "owner_index": 83,
  "source_path": "xml/wine-window-management-v1.xml",
  "target_path": "protocols/compositor/xml/wine-window-management-v1.xml",
  "before_blob": "...",
  "after_blob": "...",
  "consumer_paths": ["..."],
  "generated_signatures": ["..."],
  "local_overlay_components": ["..."],
  "result_blob": "...",
  "verification": ["ancestry", "owner", "signature", "build"]
}
```

生成规则：

- 按 source commit ancestry 排序；
- 同一 component 恰好一个 DeckShell owner；
- 同一 DeckShell owner 可以吸收多个有序 protocol component；
- source XML post-image 只覆盖 upstream-owned 区域；
- local overlay 使用独立 component ID 和 hunk hash；
- 协议加入、清单更新、包版本、生成命令和首次消费端必须属于同一编译原子；
- `1a55a4fc`/`4439beed` 的 wine-window-state component 固定归 index 81，
  wine-window-management component 固定归 index 83；
- `36027231` 的 wine-window-management component 固定归 index 141；
- 同一 source commit 的不同 XML component 可以归属不同 owner，提交级 owner 不能替代
  component-specific owner；
- 无消费端 component 进入唯一 convergence owner，不在较早节点出现。

### 6. `dependency-bundle-ledger`

每个 dependency bundle 至少包含：

```json
{
  "bundle_id": "deck:<owner-index>:<capability>",
  "owner_index": 133,
  "members": [
    {"kind": "declaration", "path": "...", "fingerprint": "..."},
    {"kind": "definition", "path": "...", "fingerprint": "..."},
    {"kind": "call", "path": "...", "fingerprint": "..."},
    {"kind": "cmake-registration", "path": "...", "fingerprint": "..."},
    {"kind": "protocol-component", "id": "..."},
    {"kind": "waylib-capability", "gitlink": "...", "proof": "..."}
  ],
  "preconditions": ["..."],
  "forbidden_early_members": ["..."],
  "removal_components": ["..."],
  "expected_changed_paths": ["..."],
  "proof_nodes": [133, 136]
}
```

bundle 的所有必需成员必须在 owner transition 同时可用。后继节点可以 carry forward 已完成
bundle，但不得提前泄漏调用、成员、generated signature 或 workaround removal。

### 7. 集合 `D` 的发现算法

`D` 是生成结果，不是预设常量。发现流程：

1. 全量审计 65 个 synthesis transition；
2. 从其中 11 个 remediation target 分离出 remediation proof augmentation；
3. 对其余 54 个 carry-forward transition 建立 forward dependency graph；
4. 对 195 个 legacy-target diff 和其余 ordinary candidate 执行静态扫描；
5. 联结 C++ symbol、CMake registration、协议 generated signature、Waylib capability 与
   workaround lifecycle；
6. 将跨 entry edge 的最早安全 owner 与完整 member set 固化到 ledger；
7. 从 315 个 ordinary candidate 中导出 `D`；
8. 重新计算 `315 - |D|`，验证无负数、无重叠、无遗漏。

静态扫描必须有 mutation tests：删除任一成员、改变 owner、提前泄漏 member、替换 XML
signature 或改变 Waylib gitlink 时 verifier 必须失败。

### 8. corrected-v1 生成

transition 分类：

```text
rebuilt-self-contained-anchor         1
ordinary-replay                       315 - |D|
dependency-proven-replay              |D|
remediation-aware-synthesized-replay  11
regenerate                            3
total                                 330
```

生成器只消费冻结 ledger 和对象：

- ordinary replay 需先证明不属于 `D`；
- dependency-proven replay 原子应用完整 bundle；
- remediation replay 继续使用 predecessor 已验证的 component ownership，但必须附加新的
  protocol/dependency proof；
- regenerate 节点写入新的 authority、ledger hash、tool bundle 和 adaptation 文档；
- 任一 bundle/协议 component 无唯一 owner 时禁止生成 commit object；
- 禁止 target-SHA 特例、运行时三方模糊合并和人工修 preview。

corrected-v1 先生成两套隔离 preview，再导入新的 migration ref；不得移动 `ds-mod`。

### 9. corrected-v1 独立验证

verifier 从 Git 对象和冻结输入重新计算：

- 330 项 parent/commit/tree/message/changed-path 链；
- transition 分类和计数公式；
- `D` 集合与两个 ledger 的双向覆盖；
- protocol ancestry、XML blob、owner、generated signature 与 local overlay；
- dependency bundle 的 member 完整性、禁止提前泄漏与 Waylib capability；
- 11 个 remediation 的 source/local/removal/component proof；
- 外部协议 lookup occurrence 和实际生成输入路径；
- final product manifest 与 master oracle；
- preview A/B canonical bytes 和 object IDs。

verifier 不信任 generator 自报的 `pass` 字段。

### 10. corrected-v2 生成与独立信任根

v2 精确重放 corrected-v1 产品 transition，分类与 v1 一一对应：

- `replay-rebuilt-anchor`；
- `replay-ordinary-v1-delta`；
- `replay-dependency-proven-v1-delta`；
- `replay-remediated-v1-delta`；
- `regenerate`。

特殊 replay 的 tree 操作仍是 corrected-v1 raw transition 的字节级重放；差异只在独立验证
责任。v2 必须重新读取 protocol/dependency ledger、source objects、Waylib objects、Git tree
和 master oracle，不能只证明 v2 等于 v1。

corrected-v2 同样执行双 preview、formal import 和新的 migration ref，不覆盖 predecessor ref。

### 11. 构建与选择覆盖证明顺序

#### 11.1 六个首轮节点

1. index 1：self-contained anchor；
2. index 81：wine window state XML + state C++ module；
3. index 83：wine window management XML + management C++ module；
4. index 133：xdg-dialog remediation + 完整 C++ bundle；
5. index 136：carry-forward 无过早依赖泄漏；
6. index 141：serial XML + serial call site。

首轮证明用于尽早验证 corrected-v1 的原子边界。六个节点还必须进入最终 corrected-v2 的
70 节点风险矩阵；最终矩阵中每个唯一节点只 fresh build 一次，但执行其全部适用标签断言。

#### 11.2 选择清单

从最终 corrected-v2 mapping 和 Git objects 独立重算 `requirements.md` 定义的四个谓词：

```text
S = 56 个选择性节点
P = 6 个 proof 节点
R = 11 个 remediation 节点
B = S ∪ P ∪ R = 70 个唯一节点
```

选择清单必须记录每个节点命中的标签、父子 tree/gitlink、changed paths、entry 类型、入选原因
和 canonical SHA-256。index 133 同时命中三组，只出现一次并绑定三组断言。corrected-v1/v2
r5 的 56/6/11/70 成员必须一致；后续再次漂移时停止并回到方案阶段。

#### 11.3 70/70 风险选择矩阵

对 `B` 中 70 个唯一节点分别执行 detached materialization、精确 Waylib gitlink checkout、
fresh configure、full build、protocol source-path gate，以及该节点适用的 proof/remediation/
选择性断言。每个节点使用独立 SHA 命名 build directory；PASS=70、FAIL=0、SKIP=0。

旧 `1..141` 前缀、独立 11/11 remediation 和 330/330 full build 不再作为三个重复构建阶段。
已冻结的旧失败运行继续作为负向基线，不删除、不改写为新 PASS。

#### 11.3.1 精简执行与失败前移

在不改变 70/70 合同的前提下，Task 14 采用以下单一路线压缩执行时间：

1. 当前 index 231 不再按缺失符号逐项修补；一次性比较 candidate-30、已通过的 index 174
   和冻结 replay/component evidence，导出 keyboard-state 能力的完整 provider settlement；
2. 先以 RED test 固化“调用端已经物化、支持声明/定义/静态状态/连接函数未完整物化”的通用
   缺陷，再修复 provider materialization；
3. 新 candidate 在 full build 前先执行静态 settlement gate，验证成员闭合、双向基数、函数
   边界、残缺片段和禁止语法结构；静态门禁失败时不消耗完整构建；
4. index 231 通过 fresh configure、full build、适用 CTest 与协议源扫描后，才重建
   corrected-v1/v2 双 preview、formal refs 与 Task 8-13 evidence；
5. 在一个代表性通过节点上对 `-j8` 与 `-j12` 做冻结环境基准；`-j12` 只有在稳定通过且没有
   OOM、swap 抖动、超时或性能回退时才成为最终矩阵参数，否则固定 `-j8`；
6. 最终矩阵前按 ccache 冻结上限执行 LRU 收敛并记录前后统计，保留全部 evidence、失败对象库
   与 Git objects；
7. 最终 70 节点仍由单执行器按 canonical order 执行。若进程中断，只允许复用同一最终
   candidate、环境合同和 artifact root 中经 verifier 通过的结果，不复用任何旧 candidate PASS。

本路线不引入多 worktree 并行矩阵。当前机器内存与磁盘余量不足以证明双 worker 可稳定获益，
且并行结果仍需重新合并为 canonical order，实施成本高于本次净收益。

#### 11.4 全 330 节点选择覆盖审计

独立 verifier 对全部 330 个 mapping record 重算四个选择谓词及 proof/remediation membership，
要求 selected=70、unselected=260、missing=0、duplicate=0、unclassified=0，并确认全部 selected
节点均有绑定的 fresh build evidence。260 个 unselected 节点只具备结构、ledger、tree/gitlink、
协议来源和选择分类证据；不得生成或继承 build PASS，也不得声称全历史可构建。

#### 11.5 最终 HEAD

最终 HEAD 继续执行完整产品、安装、consumer 和 Git QA，不能替代 70/70 风险选择矩阵。

### 12. 构建环境冻结

`build-environment.json` 必须记录：

- compiler/linker/Qt/CMake/Ninja/ccache 版本；
- 系统依赖包与解析路径；
- CMake cache 输入、generator、toolchain 和 feature options；
- `PATH`、`PKG_CONFIG_PATH`、`CMAKE_PREFIX_PATH`、协议相关变量；
- 禁止路径扫描结果；
- source/submodule/object/build 路径模板；
- 环境 canonical hash。

每个被选节点记录命令、退出码、耗时、log hash、gitlink expected/actual、协议输入
expected/actual。
环境或依赖身份不完整时矩阵状态必须为 BLOCKED，而不是把失败归因于历史。

### 13. 产品 oracle 与 overlay

最终仍要求：

```text
product_manifest(corrected-v1)
== product_manifest(corrected-v2)
== product_manifest(master@d83f92fc/tree@6d9f8cc5)
```

产品清单包含协议、C++、测试、CMake、打包和 Waylib gitlink。允许 overlay 只能是冻结的
rewrite authority、工具 bundle、adaptation 文档和已批准 `.gitattributes` 差异；禁止宽泛
`doc/**` 排除。

若协议 remote endpoint 漂移导致该等式不可满足，必须回到方案阶段重新冻结 master oracle，
不得在执行中修改过滤规则掩盖差异。

### 14. ref 事务

1. corrected-v1/v2 只写入新的 migration refs；
2. 所有生成和验证阶段保持 `master`、`integrate`、`ds-mod` 与 predecessor refs 不变；
3. 最终深度 QA 通过后重新读取 live `ds-mod`；
4. expected-old 与输入锁一致时等待唯一 HITL 授权；
5. 仅执行一次 `update-ref <ds-mod> <new> <expected-old>`；
6. mismatch 立即停止，不重试、不 rebase、不强推；
7. CAS 后复验 refs、head/tree/count、product manifest、gitlink、worktree 和 reflog；
8. 不删除旧 refs，不执行 push。

## 领域语言

| 标准术语 | 定义 | 避免用语 |
| --- | --- | --- |
| self-contained anchor | 从 index 1 起只消费当前节点仓库内协议与依赖的重建锚点 | 复用旧 index 1 |
| protocol component | 一个冻结协议提交中某个 XML 的可映射变更单元 | 最终 XML 快照 |
| protocol owner | 首次消费该协议接口并原子落地 XML/CMake/代码的 DeckShell index | 最近提交、方便放置 |
| local XML overlay | DeckShell 自有且不能由上游 XML post-image 静默覆盖的 hunk | 本地杂项 |
| dependency bundle | 必须在同一节点可用的声明、定义、调用、注册、协议和依赖能力集合 | SHA 特例 |
| `D` | 315 个 ordinary candidate 中经审计证明需要 dependency-proven replay 的集合 | 全部 ordinary、仅 11 节点 |
| dependency-proven replay | 按冻结 bundle 原子落地并独立验证的 ordinary transition | 普通 replay 加标签 |
| protocol convergence | 无历史消费端的剩余协议变化集中落地的唯一最终节点 | 提前同步全部协议 |

## 完成定义

`qaMode=deep`。只有 `requirements.md` 的完成判定、`contract.json` 的全部 `qaFocus`、当前
会话 qa-review 与 closeout evidence 均为 PASS，才允许声称实施完成。任何 BLOCKED 项都
禁止进入 `ds-mod` CAS。

## 文件结构

### 本方案包

- `.helloagents/plans/202607262338_commit-aligned-history-compile-atomic-protocol-alignment/requirements.md`
- `.helloagents/plans/202607262338_commit-aligned-history-compile-atomic-protocol-alignment/plan.md`
- `.helloagents/plans/202607262338_commit-aligned-history-compile-atomic-protocol-alignment/tasks.md`
- `.helloagents/plans/202607262338_commit-aligned-history-compile-atomic-protocol-alignment/contract.json`
- `.helloagents/plans/202607262338_commit-aligned-history-compile-atomic-protocol-alignment/detailed-conclusion.md`

### 后续实现重点

- 新 artifact 下的 input freeze、ledger builder 和 verifier；
- predecessor v1/v2 tool copy 的版本化修订；
- `DeckShell/doc/skills/treeland-deckshell-sync/scripts/aligned_history_v2/` 的最终持久工具；
- protocol source policy 的历史节点静态/动态门禁；
- proof nodes、70/70 risk-selected matrix 与 330-node selection coverage evidence；
- final QA、ref snapshot 与 CAS evidence。

## UI / 设计约束

不适用。本任务不修改 UI、QML 视觉合同或交互。

## 风险与验证

| 风险 | 阻断措施 | 必须证据 |
| --- | --- | --- |
| 远端协议 endpoint 漂移 | 一次 fetch 后比对规划快照，不同即停止重规划 | drift report / frozen lock |
| 最终 XML 提前污染旧节点 | commit-ordered ledger + owner gate | index 83/141 与 ancestry proof |
| local XML hunk 被覆盖 | upstream/local 双 provenance | overlay component coverage |
| C++ 依赖仍跨 entry | dependency bundle member gate | index 133/136 full build |
| 只修 11 个节点 | 65 synthesis 全审计 + 全 ordinary 静态扫描 | 可重算集合 `D` |
| 无差别重算 315 个节点 | ordinary/non-ordinary 双向分类 | `315-|D|` 与 `|D|` 清单 |
| 外部系统协议影响结果 | source-path gate + environment freeze | lookup=0、禁止路径读取=0 |
| v2 循环证明 | 独立重算两个 ledger 与 oracle | mutation tests |
| 选择器漏选或重复 | 独立重算四个谓词并与 proof/remediation 双向 join | selected=70、unselected=260、missing=0、duplicate=0 |
| 把选择性结果误报为全历史可构建 | evidence schema 区分 build coverage 与 structural coverage | 70 个 build PASS、260 个明确 unbuilt |
| 历史误更新 | 新 migration refs + 单次 CAS | refs-before/after 与 post-CAS audit |

## 决策记录

- [2026-07-26] predecessor corrected-v2 保持 BLOCKED，不从任务 10 续跑。
- [2026-07-26] 采用“编译 dependency bundle + protocol transition”双 ledger，而不是 index
  133/136 特例。
- [2026-07-26] `D` 由 65 个 synthesis transition 全审计和其余 transition 静态扫描产生，
  禁止预设为 315。
- [2026-07-26] 从 index 1 重建 self-contained anchor，拒绝精确复用旧 commit object。
- [2026-07-26] `treeland-protocols` 只 fetch 一次并冻结；远端漂移需重新规划。
- [2026-07-26] 只按提交顺序映射 XML，不导入其他仓库元数据，不提前复制最终 21 XML。
- [2026-07-26，已由 2026-07-28 决策取代] 曾规划在首轮证明后依次执行 `1..141`、
  独立 11/11、330/330 和最终深度 QA。
- [2026-07-28，已由 2026-07-29 r5 决策取代] 将 61 个选择性节点、六节点 proof 与 11 个 remediation 合并为一个去重的
  76/76 风险矩阵；index 133 只构建一次但执行三组断言。
- [2026-07-28，已由 2026-07-29 r5 计数取代] 全 330 节点保留结构与选择覆盖审计，254 个未选节点不得声明 fresh build
  PASS；最终交付不再声称 330/330 全历史可构建。
- [2026-07-29] r4 在 40/76 后由 index 148 的运行时生命周期依赖证伪；新增通用
  `test-runtime-waylib-capability` edge 并生成 corrected-v1/v2 r5，不复用 r4 PASS。
- [2026-07-29] r5 双候选正式重算得到 `S=56`、`P=6`、`R=11`、`B=70`；从正式集合移除
  `291,297,304,305,306,314`，Task 14 改为从零执行 70/70。
- [2026-07-30] Task 14 采用不降低证明强度的精简执行：index 231 先批量闭合 provider
  settlement 并执行静态失败前移；通过后再重建 Task 8-13；最终矩阵只在基准通过时从
  `-j8` 提升为 `-j12`，允许同一最终 candidate/环境/artifact root 的断点续跑，拒绝旧 PASS
  复用和多 worktree 并行调度。
- [2026-07-26] `ds-mod` expected-old CAS 继续作为唯一 HITL；禁止 push、强推、修改
  master/integrate 或删除 refs。
- [2026-07-26] 方案包创建阶段未执行实现；后续执行进度以 `tasks.md` 与当前会话状态为准。

## corrected-v1/v2 编译原子执行权威

本次生成受
`.helloagents/plans/202607262338_commit-aligned-history-compile-atomic-protocol-alignment/`
约束。corrected-v2 独立重放 rebuilt anchor、186 个 ordinary transition、129 个
dependency-proven transition 与 11 个 remediation transition，并重新生成 3 个固定
adaptation transition。协议来源、dependency bundle、Waylib ancestry 与冻结 master
product oracle 均由独立验证器重算；`ds-mod` expected-old CAS 不包含在本提交中。
