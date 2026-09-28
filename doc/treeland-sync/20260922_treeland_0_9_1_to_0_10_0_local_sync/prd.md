> 仓内参考副本；权威原文：`外层工作区（历史）/.helloagents/archive/2026-09/20260922_treeland_0_9_1_to_0_10_0_local_sync/prd.md`。
> 保留原同步方案的历史时点与验收边界；其中历史命令不是本次补档的执行指令。

# Treeland 0.9.1 -> 0.10.0 三仓统一同步需求

## 文档状态

- 状态：本地同步与 N8a/N8b 分段收口已完成（2026-09-27），证据见[实施与验收记录](plan.md#完成结论2026-09-27)。本 PRD 保留需求与授权，不替代节点报告和原始收口记录。
- 授权修订：2026-09-23 增补精确协议迁移，2026-09-27 精确修订 N8b foreign-toplevel V2 协议来源并单独授权 N8b DRM 非阻断例外；不据此宣称 DRM/GPU 行为通过。
- 日期：2026-09-22。
- 修订依据：session `01a0c861-f7a5-7951-9532-768b2f757713` 最后一轮结论，以及用户明确的 C/R 新建分支决定。
- 技能依据：`DeckShell/doc/skills/treeland-deckshell-waylib-unified-sync/SKILL.md` 及其 references。
- 批次标识：`20260922_treeland_0_9_1_to_0_10_0_local_sync`。

## 1. 目标与使用场景

DeckShell 维护者需要把本地已存在的 Treeland `master` 来源对象中，
从 0.9.1 之后到 0.10.0 的明确提交区间，按来源提交粒度同步到三个相互依赖的
本地 Git 仓库：DeckShell 父仓、`waylib-shared` 子仓以及其独立的 wlroots 子仓。
目标是保留来源追溯和逐层依赖关系，使 `master-merge` 能消费与候选 C/R 完全匹配
的代码；目标不是把 Treeland 快照或当前远端最新内容直接覆盖到目标分支。

同步必须使用统一流程一次生成 inventory，并按每个来源提交执行 R -> C -> P：

1. 来源触及 `wlroots/**`、`3rdparty/wlroots/**`，或 C 基线已登记 R 时，必须启用
   R；有来源内容变化时先完成 R 内容与审计，无内容变化时仍核验真实 R 基线、
   消费关系及全部 R gate，不创建虚假来源提交，也不标记为两仓 `not-applicable`。
2. C 写入 `waylib-shared` 普通文件及 R gitlink，并通过 Waylib 源码合同审计。
3. P 写入 DeckShell 映射后的内容及 C gitlink。

没有内容变化的层不伪造内容提交；但 C-only/R-only 变化仍需要 P 的纯 gitlink
传播提交，保证三仓映射连续。

## 2. 冻结输入与当前基线

以下值是本轮调查时从本地 Git 对象解析出的快照。实施前必须重新核对；任何漂移、
对象缺失或工作区变脏都阻断，不用分支名或远端最新值替代冻结 SHA。

| 项目 | 冻结值 |
|---|---|
| 来源仓库 | `DeckShell/` |
| 来源标识 | `refs/remotes/treeland/master` |
| 来源 tip | `c0d4bc214d4636aa4e2fa8557927a560190b7411` |
| 范围 | `(fd573cf44fb06ee1eebcdd8c39716d1c797b64d4..3a100f265970cb6acf9addf07e5c297aab9e9839]` |
| 范围基线 | `fd573cf44fb06ee1eebcdd8c39716d1c797b64d4`，0.9.1，左端不包含 |
| 范围终点 | `3a100f265970cb6acf9addf07e5c297aab9e9839`，tag `0.10.0`，右端包含 |
| 来源拓扑 | 41 个提交，0 个 merge，基线是终点祖先 |
| P 目标 ref | `refs/heads/master-merge` |
| P 当前基线 | `9d14efb18d1d2413376e4369461a3e11f7d44689` |
| P 当前 C gitlink | `3rdparty/waylib-shared -> f14d7cdf718307945f492eb1c6d7608413e83c29` |
| C 当前检出 ref | `refs/heads/waylibshared`，保留不动 |
| C 目标 ref | 基于当前 C 基线新建 `refs/heads/waylibshared-merge` |
| C 当前基线 / 新目标初始 SHA | `f14d7cdf718307945f492eb1c6d7608413e83c29` |
| C 当前 R gitlink | `3rdparty/wlroots -> 005b8c571c002d266ffdd560b7eb4e3bd46c4e3a` |
| R 当前检出 ref | `refs/heads/master-merge-treeland`，保留不动 |
| R 目标 ref | 基于当前 R 基线新建 `refs/heads/master-merge-treeland-new` |
| R 当前基线 / 新目标初始 SHA | `005b8c571c002d266ffdd560b7eb4e3bd46c4e3a` |

P、C、R 当前工作区均干净。P 的 gitlink 与 C 基线、C 的 gitlink 与 R 基线均已
通过对象核对。P 继续以 `master-merge` 为目标；C/R 按用户决定从上述完整 SHA
分别新建 `waylibshared-merge`、`master-merge-treeland-new`，不从旧同步分支、
备份 ref 或届时移动后的分支 tip 取起点。

本次核验时两个新目标 ref 均不存在；本 PRD 只确定分支选择，不实际创建。获授权
进入实施后，须在首次 replay 前核对名称未占用，再以对应冻结基线创建未检出的
本地目标 ref。若发现同名现有分支，先停止核对，不覆盖或强制重置；恢复本批次时
须以实际创建/收口记录核对其身份。原 C `waylibshared`、原 R
`master-merge-treeland` 及其主工作区保留不动，不更改子模块 URL 或分支配置。

来源对象、目标基线、协议对象均必须已经在本地；本轮不自动 fetch、创建 remote、
push、tag，也不修改外层 `HA-DeckShell -> DeckShell` gitlink。

## 3. 范围盘点与归属

统一 inventory 已在冻结范围上得到 `outcome: pass`，路径策略哈希为
`a9c6935a53c27e4c568bc49a556f3bb0a52236445e2845b704c2b37ab8f37145`。分类结果：

| 分类 | 来源提交数 | 处理方式 |
|---|---:|---|
| `deckshell-only` | 27 | P 提交 |
| `waylib-only` | 7 | C 提交后 P 纯 gitlink 提交 |
| `dual` | 7 | C 提交后 P 内容加 gitlink 提交 |
| `unowned-skip` | 0 | 不生成提交，但仍须留在 inventory |
| `blocked` | 0 | 任一出现即停止 |

按 `git diff-tree --name-only` 统计，本范围有 242 个来源路径条目，其中 25 个触及
C 的 `waylib/**`、`wlroots/**` 或 `qwlroots/**`，0 个触及来源
`3rdparty/wlroots/**`（inventory 对 rename 两侧分别留证，条目数可能更高）。因此本轮 R 不产生来源内容提交，但 C 基线已有 R，R 仍是
激活的三仓验收层，必须提供真实 R 仓库、基线对象、独立 worktree、目标 ref 和
子模块 URL，并完成 R gate；不能把 R 标记为普通两仓 `not-applicable`。

路径合同固定如下：

- Treeland `qwlroots/**`、`waylib/**`、`wlroots/**` 原相对路径进入 C 普通文件。
- Treeland `3rdparty/wlroots/**` 若未来出现在冻结范围内，去此前缀进入 R；本轮
  inventory 已证明没有该类来源路径，不能从当前 R 快照反向制造来源提交。
- 其它 P 路径只按 DeckShell 权威 path-policy 映射；unknown、类型漂移、未经
  审批的 review-only 路径和 merge 均阻断。
- rename 的 old/new 两侧都进入审计；copy 只把 new 作为实际变更，不能重复写入
  unchanged 的来源 old 文件。

## 4. 关键节点与分段

为覆盖协议/命名迁移这一高影响边界，本批不把 41 个提交当成一个无中间验收的大段。
固定两个连续、互不重叠的左开右闭分段：

| 节点 | 分段 | 来源提交数 | 验收理由 |
|---|---|---:|---|
| N8a | `(fd573cf44fb06ee1eebcdd8c39716d1c797b64d4..a5656ab80ae11a0068d507659f35bb999b6d815d]` | 26 | `treeland-protocols` unstable-v2/Wine 命名迁移及 Waylib 相关变化 |
| N8b | `(a5656ab80ae11a0068d507659f35bb999b6d815d..3a100f265970cb6acf9addf07e5c297aab9e9839]` | 15 | 0.10.0 最终候选，包含后续窗口、远程子表面和输出行为修复 |

每段普通中间提交仍逐提交做内容投影、来源 trailer、C 源码合同和两层 gitlink
检查，但不承诺逐提交完整编译。每段终点必须独立 fresh build/install/CTest、
consumer、namespace、R 原生验证和协议配套验证；后一段只从前一段已经收口的
真实 P/C/R SHA 接续。N8b 的 PASS 不能覆盖 N8a 的缺证或失败。

### 4.1 N8b 前已授权的独立结构修复

2026-09-25 用户已单独授权将 foreign-toplevel 状态编码收敛回规范 v1 实现、保留回归，
然后从修复基线重放 N8b。独立提交 `38ca30d3e220e99a119dca7465d1acb887e7f186`
是 N8a 已收口 P `cb9c6bf6bbc4a53bc50212204f34ad0cd5308ffb` 的直接后继；
只将 codec `.cpp` 的实现移回 `foreigntoplevelmanagerv1.cpp` 并移除原编译入口，
既有 codec 头和测试合同保留。它不算作 15 个 N8b 来源提交或协议配套提交。

N8b 的真实 replay P 基线为 `38ca30d...`，C/R 仍为 N8a 已收口值。最终接受时须先
单独记录并核验这项已授权本地修复，以 expected-old CAS 将 P 从 `cb9c6bf...` 快进到
`38ca30d...`，再由标准 closeout 从实际 replay 基线执行 R→C→P。不能伪造
manifest 的基线、跳过 CAS 或把结构修复混作 Treeland 来源映射。

## 5. 可观察行为合同

### 5.1 历史与三仓映射

- 每个来源提交保留完整 SHA、作者、时间、原始消息和 `Treeland-Commit` trailer；
  目标提交不能伪装为来源 SHA。
- C/R/P 目标提交按 R -> C -> P 顺序创建；上层只能引用已经存在的下层提交。
- P 的 `3rdparty/waylib-shared` 必须在每个候选提交指向同一节点中已创建的 C
  提交；C 的 `3rdparty/wlroots` 在本轮保持 `005b8c571c002d266ffdd560b7eb4e3bd46c4e3a`，
  不得改成目录、tree SHA、系统 wlroots 或未经证明的上游 pin。
- manifest 必须记录每个来源 SHA 的 P/C/R 归属、action、目标 SHA、gitlink
  from/to、适配路径和工件摘要；`applied`、`adapted`、`empty` 的证明必须符合
  skill schema，不能用 drop list 掩盖冲突。
- 失败、冲突、合同漂移或部分收口时保留 worktree、journal 和证据，不 reset、
  abort、清理、改写用户分支或自动回滚。

### 5.2 Waylib 公共合同

本请求仅新增下述精确协议迁移授权，不授权其它公共包合同变更。Waylib 现有 exported target、安装路径、public
header、namespace、pkg-config、CMake 包配置、核心 target 和安装入口继续受
`waylib-contract.md` 保护。来源中的 Waylib 修复可以按普通 inventory 回放，但
任何未获本轮精确批准的公共 target/header/namespace/install drift 都必须在首次
出现的来源提交处阻断；不能等到终点恢复后放行，也不能添加旧 API 兼容壳、双路线
或运行时 fallback。

候选 C 必须保留现有 `3rdparty/wlroots` 子模块结构及更新脚本的拒绝前缀，且独立
构建时仍能由安装包消费。C-only 或 dual 来源提交中的 core CMake、PUBLIC/INTERFACE
include、导出 namespace 和安装变化，均需逐提交源码合同审计并在节点终点做安装
合同比较。

### 5.3 remote-subsurface 协议配套

remote-subsurface 配套每段必做，即使 XML 没有变化。C 基线记录的已接受 pair 为：

- implementation：Treeland `fd573cf44fb06ee1eebcdd8c39716d1c797b64d4` 及现有
  `waylib` implementation paths；
- XML：独立仓 `treeland-protocols` 的
  `8dc1d1e788dc964cd0f756b4491d0225e70b1598:xml/treeland-remote-subsurface-unstable-v1.xml`。

本批 remote-subsurface XML 的已接受基线仍为 `8dc1d1e788dc964cd0f756b4491d0225e70b1598`。
用户于 2026-09-23 明确授权修订协议固定输入与范围，实施 `a5656ab...` 必需迁移。
N8a 的新 XML 终点选定本地对象 `284e3aac8a1ed5ece66c4cb248e8b24d33cb25a0`
（包含 Wine 接口规范化 `ffbc937...`、internal v2 迁移 `30745c...`），路径为
`wine/treeland-remote-subsurface-unstable-v1.xml`。不追随协议 master 最新 tip。
每段 implementation base 和 XML base 仍必须匹配 C 基线已接受 provenance。

| 节点 | implementation base（不包含） | implementation head（包含） | XML base → head |
|---|---|---|---|
| N8a | `fd573cf44fb06ee1eebcdd8c39716d1c797b64d4` | `a5656ab80ae11a0068d507659f35bb999b6d815d` | `8dc1d1e788dc964cd0f756b4491d0225e70b1598` → `284e3aac8a1ed5ece66c4cb248e8b24d33cb25a0` |
| N8b | `a5656ab80ae11a0068d507659f35bb999b6d815d` | `3a100f265970cb6acf9addf07e5c297aab9e9839` | base = head = `284e3aac8a1ed5ece66c4cb248e8b24d33cb25a0` |

N8a 包含 remote-subsurface implementation 变化，其配套候选 provenance 必须记录
`a5656ab80ae11a0068d507659f35bb999b6d815d` 和上述新选定 XML；只有该 pair 验收并
随节点实际收口后，N8b 才能以它为已接受起点。N8b 不得重新从 `fd573...` 扫描，
候选 provenance 应记录最终实现终点 `3a100f265970cb6acf9addf07e5c297aab9e9839`。
各段均检查中间修改、回退、客户端引用和新旧文件列表；实际 C 基线记录与表中
起点不一致时停止核对，不覆盖 provenance 或跳过 `protocol-inspect` 基线检查。

配套结果必须明确 wire 顺序/类型/枚举、行为语义、客户端升级影响和
`compatibility: direct-switch`。至少运行真实的非零 Wayland/remote-subsurface
CTest 交互用例；编译或 XML 字节相等不能替代交互证据。失败统一报告为“尚未适配”，
保留上一已接受 pair，禁止旧接口别名、双实现和运行时回退。

### 5.3.1 精确协议迁移范围（2026-09-23 新授权）

不整包覆盖 TreelandProtocols，不引入其最新其它协议。P 保持
`protocols/compositor/xml/` 的本地受控目录和 `DECKCOMPOSITOR_PROTOCOLS_DATA_DIR`，
仅变更下列来源当前实际要求的 XML、对应安装清单及规范映射的消费者：

| 触发来源 | 协议来源 commit | 本轮允许的协议 |
|---|---|---|
| N8a `a5656ab80ae11a0068d507659f35bb999b6d815d` | `284e3aac8a1ed5ece66c4cb248e8b24d33cb25a0` | internal 的 app-id-resolver-unstable-v2、prelaunch-splash-unstable-v2、screensaver-unstable-v2、wallpaper-shell-unstable-v1；wine 的 remote-subsurface-unstable-v1、wine-window-management-unstable-v1、wine-window-state-unstable-v1 |
| N8b `5023ac25718db141361d66018746e66bd8e56bc6` | `108d969c26775bf22ef674105f1b3cc22e036ff8` | dde/treeland-show-desktop-unstable-v1.xml |
| N8b `2f5bb78f3e8b5fc73b7cf1f4a8ea09c38a946339` | `07d336875741f08d73001fa2409b2c2ed621dc26` | dde/treeland-foreign-toplevel-manager-unstable-v2.xml |

2026-09-27 用户明确授权将本表 foreign-toplevel V2 的原来源 `4038433...` 精确更新为
`07d336875741f08d73001fa2409b2c2ed621dc26`，并完成相应实现/测试适配。两对象间仅此 XML
变化：增加 `context_already_exists=1`，重复创建 dock preview context 时拒绝请求，客户端
须先销毁旧 context；不采用旧 XML 的“服务器替换旧 context”语义。这与来源 `2f5bb78...`
已有实现一致。接口名后缀 `v2` 不代表公告版本 2；该 XML 的三个接口版本均为 1，实现与
真实客户端测试必须与之对齐。原 attempt-5 的编译失败、XML 和候选保留，不改写为通过。

迁移按对应来源逐提交执行，去掉已被替代的旧协议安装项和旧消费者，不添加旧接口别名、
双实现或 fallback。其它已有协议 XML 不改。remote-subsurface 的 C/P XML 与 provenance
继续由原有配套阶段统一更新；受影响的 C `waylib/tests/`、`test_project/` 及 P
`compositor/` 客户端/测试须同步，不以编译通过替代真实交互验收。

WaylibShared 的 exported target、public header 路径、namespace、pkg-config 和安装
合同继续保持。允许为这次精确协议 XML 清单补足同步工具已有迁移路径校验；工具维护使用
独立 worktree，不改变已冻结 P/C/R 基线、path-policy 或历史失败证据，必须有相应拒绝路径测试。
额外路径仍通过绑定来源 SHA、相邻快照和逐路径补丁的现有迁移审批进入 verifier，不扩大普通 owner。

### 5.4 R 基线与消费链

虽然本批没有来源 `3rdparty/wlroots/**` 变更，R 候选仍须用当前 C gitlink 指向的
真实 commit 进行独立 Meson configure/build/test，并证明 C wrapper、P 编译数据库、
生成头和消费目标实际使用该 R，而非系统库或其它 worktree。R base/candidate、C
base/candidate、P candidate 都使用源码树外的新构建和安装目录；不得复用历史 PASS。

### 5.5 N8a DRM 测试的方案包专用例外（2026-09-24 用户授权）

本条仅适用于本方案包的 N8a P compositor 全量 CTest：来源提交
`8bfa446c589f06d4f427a39b93a585a2406f5cdb` 新增的上游同步测试 `test_drm`，在本次
headless/非 GPU 验收环境因 DRM/GBM 前提不可用而按测试自身约定返回 SKIP，可作为
**不阻断项**接受。它不表示 DRM/PRIME 行为已通过验收，也不改变其它节点、验证 ID、
Waylib/R 测试或通用 unified-sync skill 对跳过测试的默认严格规则。

接受该例外必须同时满足：本段仍运行无过滤的完整 compositor CTest；测试发现与执行
记录的集合一致；全量集合中恰好只有 `test_drm` 为 skipped，失败数为 0，其余测试全部
通过，CTest 进程退出码为 0；保留实际 `SKIP`、完整发现记录和原始日志。任何额外
skip、失败、漏测、过滤运行或非零退出码仍阻断。方案包执行日志及 N8a 验收证据必须
明确标出此例外，不得把 `test_drm` 改写成测试通过。

### 5.6 N8b DRM 测试的独立限定例外（2026-09-27 用户授权）

用户本次单独答复“授权 N8b 限定例外”。这不是从 N8a 推定授权：仅对 N8b 的
`deckshell-compositor-ctest`，在 headless 环境中继承自上游 `8bfa446c...`、未经修改的
`test_drm` 可以作为非阻断 SKIP 接受。必须执行无过滤的完整发现集合，恰好只有
`test_drm` 一项 SKIP、其余全部通过、零失败、CTest 进程退出码为 0；原始记录、
发现集合及日志保留。任何额外 skip、失败、漏测、过滤或非零退出码仍阻断。

验收工具与本段授权记录绑定本方案、N8b、attempt-8 的精确 P/C/R 候选、来源终点
`3a100f265970cb6acf9addf07e5c297aab9e9839`、验证 attempt 1 和实际日志。
同时从 Git 核对继承的 DRM 来源映射及测试目录字节不变；不把该来源伪造成 N8b
新提交。它不证明 DRM/PRIME/DMA-BUF/GBM/GPU 行为通过，不适用于 C/R、consumer、
其它节点或其它测试，也不改变通用工具默认拒绝 SKIP 的规则。

## 6. 验收标准

每个 N8 节点都必须同时满足以下条件，才允许进入该节点收口：

1. 预检冻结输入、祖先关系、clean worktree、path-policy、inventory；inventory
   为 `pass`，无 merge/unknown/blocked。N8a 的 C/R 新目标 ref 必须已按第 2 节从
   各自当前基线创建；N8b 从 N8a 实际收口后的目标 SHA 接续，原 C/R 分支保持不变。
2. 完成该段全部来源提交的 R -> C -> P 回放及 manifest/evidence；普通提交无静默
   丢弃，C/P 的 two-level gitlink 对象真实存在且 mode 为 `160000 commit`。
3. C 源码合同审计、R 内容审计、P 内容审计和 adapted/empty 证明全部通过；任何
   公共合同漂移都只有在本轮新增的显式审批存在时才可继续；第 5.3.1 节之外无迁移审批。
4. C base/candidate 完成 fresh configure、默认完整 build、install、CTest；自带
   `test_project` 仅连接 candidate install 完成 configure/build/CTest，并通过固定
   基线 namespace probe。CTest 必须使用 `--no-tests=error`，缺测试、跳过、失败或
   只跑子集均不算通过。
5. R base/candidate 完成 Meson setup/compile/test，或仅在工具依据 Git 对象证明真实
   空树基线时记录合约允许的 `NOT_APPLICABLE`；本批 R 基线非空，不能使用该豁免。
6. P candidate 完成 fresh configure、默认完整产品 build 和 compositor CTest；顶层
   0 tests 只能如实记为 `NO_TESTS`，不能升级为 PASS。仅 N8a、N8b P compositor
   全量 CTest 中分别符合第 5.5、5.6 节全部边界的 `test_drm` SKIP 可例外；记录为“通过（用户授权
   非阻断 SKIP 例外）”，而非 DRM 测试本身 PASS。其它 P 测试跳过仍阻断。
7. remote-subsurface 按第 5.3 节逐段核对已接受 implementation/XML base，
   `protocol-inspect`、配套回放、客户端/真实交互验证和 `protocol-verify` 均通过；
   报告必须包含九项 gate：
   `deckshell_verify`、`waylib_verify`、`wlroots_verify`、`gitlink_verify`、
   `nested_gitlink_verify`、`protocol_tracking`、`protocol_pairing`、
   `contract_audit`、`child_materialization`。
8. 节点报告绑定本段 `build_scope: range-head-only` 和该段完整终点 SHA，保留
   PASS/fail/NO_TESTS/NOT_APPLICABLE/未执行原状态；不能手写 PASS、借用旧日志或用
   后段报告替代前段。
9. 报告通过且取得该段收口授权后，对 R `master-merge-treeland-new`、C
   `waylibshared-merge`、P `master-merge` 依次做 expected-old CAS。N8a 的 expected-old
   为第 2 节冻结基线；N8b 的 C/R 为 N8a 实际收口 SHA，P 为第 4.1 节单独接受的
   `38ca30d...` 结构修复基线。本批 R 无来源内容变化，目标仍保持
   其初始 SHA，但 R 身份核对和 gate 不豁免。收口前三个目标 ref 必须未被任何
   worktree 检出。当前只有 P 主工作区检出本轮目标 ref，实施须用可恢复方式安排
   其非检出状态；C/R 主工作区可继续检出原分支，replay 使用独立 linked worktree，
   不检出新目标 ref，不强制覆盖或扰动用户 WIP。

整批完成的定义是 N8a、N8b 均有完整报告和实际收口，最终 P/C/R refs 连续，P/C/R
两层 gitlink、protocol pair、安装合同和 evidence 可由真实 Git 对象重算。仅生成
PRD、仅通过工具测试、仅通过单独 Waylib 或仅构建 0.10.0 快照都不满足完成定义。

## 7. 明确不做

- 不把 `fd573...` 之前的历史重新同步，不扩展到 `3a100...` 之后或
  `treeland/master` 后续移动内容。
- 不把普通 `git merge`、整树覆盖、当前 Treeland tip 快照或子模块 URL 变更当作
  统一同步的替代品。
- 历史 PRD 阶段没有授权实施；当前按用户 hello-auto 授权实施，但不重写已接受历史。
- 不改外层仓库 gitlink、无关分支、tag、remote 配置、CI/发布配置或第 5.3.1 节之外的协议 XML。
- 仅第 5.3.1 节的协议迁移已获授权；仍须生成与具体来源 SHA、相邻快照、路径和安装差异绑定的精确审批，不能授权其它公共合同变化。

## 8. 完成后的复核边界

第 2 节是实施前的冻结快照，不是完成后的当前 checkout 或目标分支 tip。当前接受的
P/C/R SHA、两段报告、限定 SKIP 和收口记录以同目录 `plan.md` 的完成结论为入口。
后续恢复先核对真实 refs、Git 对象和原始证据，不重放已接受的 41 个来源提交，不用
已经前移的来源跟踪 ref 替换本批完整 SHA。新范围、新基线或其它协议迁移须另行明确；
本批授权不扩展到远程发布或外层 gitlink 更新。
