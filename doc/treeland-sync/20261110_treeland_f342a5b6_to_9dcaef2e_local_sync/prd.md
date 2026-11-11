> 仓内参考副本；权威原文：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/prd.md`。
> 保留原同步方案的历史时点与验收边界；其中历史命令不是本次补档的执行指令。

# Treeland f342a5b6 → 1f8c2a65 三仓同步需求

## 当前结论

用户要求参考历史决策，使用 `treeland-deckshell-waylib-unified-sync`，将 Treeland `master` 的 `(f342a5b6debd028ed9bc4bc3e806118efbcae8f2..1f8c2a658b4b4e868e0650f9890c5e752fd1b839]` 移植到 DeckShell `master-merge-to-20261110-9dcaef2ed29dde1e6787936eb1f18546e7c79aea`。沿用技能的左开右闭语义：不重复移植已接受的 0.11.0 基线提交。

按用户最新指令，仅将来源 head / tip 和 N10 验收终点从 `9dcaef2ed29dde1e6787936eb1f18546e7c79aea` 延长至 `1f8c2a658b4b4e868e0650f9890c5e752fd1b839`。方案包目录、批次标识、`Refs:`、P/C/R 基线及目标分支名称、协议来源与 §4/§5 授权、验证和收口要求均保持不变；名称中保留的 `9dcaef2e` 是原有标识，不再表示本轮来源终点。

新终点已存在于本地，等于核对时的 `refs/remotes/treeland/master`，原终点是其祖先。新范围共 128 个来源提交、0 个 merge；新范围统一 inventory（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/preflight-1f8c2a65/inventory.json`；未随仓携带） 为 `pass`，没有未知或待审核路径。旧范围的预检、预览、replay、manifest、journal 和验证日志保留原始身份；不得改写其端点或将其 PASS 作为新终点验收。

最新候选 **N10-attempt-7 已完成 fresh 验证与限定接受**：P `29a647ed09d4265365e9bc376e2ed5ab2b89491e`、C `6a924124e56b27d85d28974df76913a0c7b289e0`、R `b79b9b38a473ca57f5b54892280dfad4f25f8e42`。完整 128 来源与配套 replay、独立三仓投影、两层 gitlink、递归物化和其余九项 gate 通过。相对 attempt-6 的 8 个 P 普通路径仅修复 DConfig 异步回声覆盖最新输出组成员写入、关闭配置解析可选 QML 类型的问题，并加强真实 alpha/QML 回归；绑定原来源节点，C/R 普通内容不变。原输出组 27 条断言保留，两相关目标在两种诊断配置中各连续运行 30 次无失败；另由本轮 fresh 完整正式验证验收，不借用诊断 PASS。

R 两侧默认完整构建通过，原生测试真实 `NO_TESTS`；C baseline 12/12、正常与关闭 candidate 各 15/15、两种 installed consumer 各 9/9、fresh 独立 remote 断言1/1、安装/namespace 审计均通过。P 正常及关闭默认完整构建通过；完整 compositor 正常 **102 total / 101 passed / 0 failed / 1 skipped**，关闭 **100 / 99 / 0 / 1**，唯一 SKIP 都是原 `test_drm` 的运行前提不足，内部 QtTest 无其他失败/跳过。原报告（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/sync-report.json`；未随仓携带）和原 recorder 的 `FAIL/SKIP` 保留，限定接受报告（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/sync-report-accepted.json`；未随仓携带）仅绑定本轮用户允许的该真实 SKIP，不证明 DRM/GPU 行为。工具基线 expected-old 转换及正式 R→C→P CAS（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/closeout-journal.json`；未随仓携带）已完成；P/C 仓内记录由强制 `finish --task sync` 生成并核对，实际退出结果见 `evidence/N10-attempt-7/finish.log`；只有退出 0 与两仓实物核对通过才代表整批记录交付完成，不自动提交或归并日常分支。

**N10-attempt-6 保持 BLOCKED，不再接受**。其正常及关闭 P 全构建通过；正常完整 CTest 首次为 **101/0/1，共 102**，关闭配置为 **98/1/1，共 100**，输出组恢复源角色失败随后在两种配置均复现。关闭配置的 `XWaylandSurface is not a type` 也由增强真实客户端检查证实。全部原候选、失败、日志和报告状态保留，修复未改写该冻结源码。两配置注册差异仅为两个 XWayland 专用目标。按本轮最新授权排除 DRM GPU 实验改造，仅允许其运行前提不足的真实 SKIP，不将 SKIP 写成 PASS，详细记录见 [plan.md](plan.md)。attempt-5 的 BLOCKED 报告（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-5/sync-report.md`；未随仓携带）、attempt-6 原 BLOCKED 报告（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-6/sync-report.json`；未随仓携带）和全部旧候选保持原状；旧候选未 closeout，仅新的 attempt-7 已被本批 refs 接受。外层 HA-DeckShell index/gitlink 和日常 C/R refs 保持不变。

**用户已于本轮明确批准 §4、§5 的限定范围并要求继续完成移植与验证**：固定协议 0.9.0 来源，仅接入本批必需的 7 个 XML 和 remote-subsurface 配套；允许背景模糊公共头、XWayland 配置传播及 xcb-shape 所需的合同变化，保留 WaylibShared 包名、namespace 和安装布局。授权来自本轮确认，不继承上一批的测试例外。

## 1. 目标与沿用的历史决策

维护者需要获得该区间的窗口管理、输入、输出、调试、协议及依赖修复，同时继续使用 DeckShell 的项目布局、WaylibShared 安装包和嵌套 wlroots 子模块。交付后应能从每个来源 SHA 找到目标提交及其依赖，按照正常产品配置构建并运行相关测试。

沿用以下历史记录中经实际代码核对仍成立的决策：

- 0.10.0 → 0.11.0 PRD（外层历史资料：`外层工作区（历史）/.helloagents/plans/20261106_treeland_0_10_0_to_0_11_0_local_sync/prd.md`；未随仓携带）：P/C/R 所有权、独立协议来源、精确 XML 接入、完整验证及本地收口。
- 上一批实施方案（外层历史资料：`外层工作区（历史）/.helloagents/plans/20261106_treeland_0_10_0_to_0_11_0_local_sync/plan.md`；未随仓携带）：隔离工具链、DConfig 运行依赖、安装包消费以及真实协议交互验证。可以复用工具链材料，不复用旧候选的构建结果或 PASS。
- 日常分支接管结果（外层历史资料：`外层工作区（历史）/.helloagents/archive/2026-11/20261107_daily_takeover_worktree_retirement/plan.md`；未随仓携带）：当前 P/C/R 实际基线和两仓记录已入库；旧 N9 临时工作树已退役，不恢复旧 replay 或改写旧来源映射。

`.helloagents/context.md` 中早期“跳过 waylib/qwlroots”的规则已经与后续统一三仓模型不符；本批按用户指定的现行统一技能和实际子模块结构处理。

## 2. 冻结范围与目标

| 项目 | 本地核对值 |
|---|---|
| 来源仓库 P | `DeckShell/` |
| 来源标识 | `refs/remotes/treeland/master` |
| 来源 tip / 实现 head，包含 | `1f8c2a658b4b4e868e0650f9890c5e752fd1b839` |
| 实现 base，不包含 | `f342a5b6debd028ed9bc4bc3e806118efbcae8f2`，tag `0.11.0` |
| P 目标 ref | `refs/heads/master-merge-to-20261110-9dcaef2ed29dde1e6787936eb1f18546e7c79aea` |
| P 初始 HEAD | `a9d6cb854c4fe26d767f828f89c301c49fb44d59` |
| C 仓库 | `DeckShell/3rdparty/waylib-shared/` |
| P → C gitlink / C 初始 HEAD | `f1fe3771a9a8fa3037da1d6ab153cc538610b721`，mode `160000` |
| C 本批目标 | 新建 `refs/heads/waylibshared-merge-to-20261110-9dcaef2e`，从上述 C HEAD 起步 |
| R 仓库 | `DeckShell/3rdparty/waylib-shared/3rdparty/wlroots/` |
| C → R gitlink / R 初始 HEAD | `c844d3549136a250231d3abb2fc5f6832ff05c4e`，mode `160000` |
| R 本批目标 | 新建 `refs/heads/master-merge-treeland-to-20261110-9dcaef2e`，从上述 R HEAD 起步 |
| R 登记 URL | `https://github.com/SunRain/waylib-wlroots.git`，沿用现值 |
| 唯一完整验收节点 | N10：整体终点 `1f8c2a658b4b4e868e0650f9890c5e752fd1b839` |

整体区间内没有本地发布 tag。采用用户给出的终点作为唯一必验节点，普通中间提交保留逐提交审计，不承诺逐提交可构建。

首次预检时，P 目标分支已经存在并检出，C/R 分别检出日常 `waylibshared` / `master-merge-treeland`；旧范围实施期间已从冻结基线建立 C/R 本批目标 refs，尚未接受候选。实施前再次核对冻结值和目标名称；本批只接受专用同步 refs，日常 P `master`、C `waylibshared`、R `master-merge-treeland` 不随之归并。收口前必须让本批目标 ref 未被工作树检出。

外层 HA-DeckShell 有既有未提交及暂存内容；不纳入本批，不改变外层 index 或 DeckShell gitlink。

## 3. 内容边界与关键场景

统一 inventory（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/preflight-1f8c2a65/inventory.json`；未随仓携带） 按新范围和权威路径策略实际生成，结果为：

| 分类 | 提交数 |
|---|---:|
| `deckshell-only` | 106 |
| `waylib-only` | 15 |
| `dual` | 7 |
| `unowned-skip` | 0 |
| `blocked` | 0 |

相对原终点新增 3 个来源提交，仍按既有归属、逐提交追溯和验收要求处理：

- `4abd1b9a1d30a79dee6d98951cfb0a4836952cce`：Dock preview 组件拆分，归 P。
- `a6907cee5a903ee39d88b247dc35d0c086ce524c`：XWayland X Shape 裁剪，归 C/P。
- `1f8c2a658b4b4e868e0650f9890c5e752fd1b839`：foreign-toplevel 标题修复，归 P。

P 的 `src/`、`tests/`、`examples/` 等继续映射到 `compositor/`。C 接收 `waylib/`、`qwlroots/`、`wlroots/` 普通内容；R 接收 `3rdparty/wlroots/` 去前缀投影。本批共 5 个来源提交实际修改 R，涉及 X11 焦点、X Shape 输入区域和剪贴板 offer 生命周期，必须生成真实 R 提交，再传播 C/P gitlink。

R 基线相对于来源 base 子树仍只有已继承的两处差异：`.gitignore` 的 `.helloagents/` 排除项、`types/buffer/buffer.c` 中 `waylib_buffer_get_count(void)` 的前置声明及注释。保留这些差异并按当前技能核验基线证明；不得将它们冒充本段上游修改。

需要保留和验收的本批主要行为：

- Helper 拆分后的窗口、焦点、会话锁、输入、截图和桌面服务继续完整工作，本地测试调用方随接口变化调整。
- 快捷键管理切换 v3，输出管理切换 UUID/v2 并接入 output-group；foreign-toplevel 切换 v3，Dock tooltip 使用客户端 surface。
- window-transition 和 ext-background-effect 接入其服务端、示例及协议测试；动画、背景模糊和装饰行为与来源终点一致。
- 父 surface 销毁后 remote-subsurface 子对象仍可由客户端安全销毁；生命周期、解除映射及重复请求不能导致崩溃。
- X Shape 输入区域、剪贴板同客户端焦点切换、输入法 grab 和输出配置只应答一次等修复必须落到实际依赖与测试中。
- 默认保持 XWayland 开启的正常产品配置；来源新增的 `DISABLE_XWAYLAND` 必须在关闭配置中一致控制 C/R/P，不能通过关闭它来代替正常配置验收。

保留 DeckShell 本地包名、QML URI、安装布局、DDM 配置和项目集成。冲突以目标相对补丁逐路径解释；不整树覆盖，不把上游实现挪到不在 inventory 中的兄弟文件。

## 4. 已批准：独立协议来源与精确 XML 清单

### 4.1 固定来源

本地 `treeland-protocols/` 的 tag `0.9.0` 剥离为 `578263755cb80b56f2e13fde34da1c294418e608`。已批准以它作为本批必需 XML 的固定来源，以及协议 advisory 的固定 head。

理由：源码终点的 CMake 声明最低 TreelandProtocols 0.8.0，但 `169d459600a928b9209396538abe39f6b5855612` 实际依赖 foreign-toplevel v3 和 `show_tooltip_surface`，这份 XML 在本地 0.8.0 之后才加入；只按 CMake 的最低版本选 0.8.0 会缺少实际接口。0.9.0 已包含下表全部文件，无需 fetch。

已接受的 remote-subsurface 配对为实现 `f342a5b6...` / XML `49e985e0fb0b55fd2299349f08bac14c4e09f2b3`。已批准的 XML 范围是 `(49e985e0... ..57826375...]`，路径仍为 `wine/treeland-remote-subsurface-unstable-v1.xml`。

新范围候选配套检查（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/preflight-1f8c2a65/proposed-protocol-inspection.json`；未随仓携带） 为 `pass / inspected-not-accepted`，它只是预检。remote-subsurface XML 在此范围没有变化，但实现有变化；N10-attempt-4 已完成来源记录更新、客户端审查和真实交互验证，正式配套 gate（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-4/protocol-pairing.json`；未随仓携带） 为 `pass / paired`。这不等于整批产品接受；三个目标 refs 及最后已接受配对仍未改变，协议来源沿用已批准的固定值。

### 4.2 P 新增的 7 个 XML

所有目标都位于 `protocols/compositor/xml/`，保留来源 basename，从项目内数据目录生成并安装。它们在冻结 P 初始基线均缺失，N10-attempt-4 已按首次相关实现节点接入；其它现存 XML 不因候选版本较新而批量覆盖。

| 0.9.0 中的来源路径 | 首次相关实现提交 | 用途 |
|---|---|---|
| `public/treeland-window-transition-unstable-v1.xml` | `b63b97c1694526829dbd067d8843882a107b9291` | 窗口过渡协议 |
| `dde/treeland-shortcut-manager-unstable-v3.xml` | `c23556c1d3e86f26819bd331f67468bde3ed9381` | 快捷键 v3 |
| `public/treeland-output-uuid-unstable-v1.xml` | `e8187f31fbe19f17df2c28809cf6eb09aa751206` | 输出 UUID |
| `public/treeland-output-uuid-head-unstable-v1.xml` | `e8187f31fbe19f17df2c28809cf6eb09aa751206` | 输出 head 与 UUID 绑定 |
| `dde/treeland-output-manager-unstable-v2.xml` | `a76c8ef59982900f5b9c4e3bf06e272d7194b972` | 基于 UUID 的输出管理 v2 |
| `dde/treeland-output-group-manager-unstable-v1.xml` | `ec1819c8e4e6c08e7f8636803829a474e1d9cc09` | 输出分组 |
| `dde/treeland-foreign-toplevel-manager-unstable-v3.xml` | `169d459600a928b9209396538abe39f6b5855612` | 窗口管理与 Dock tooltip surface |

配套范围还包括 `protocols/compositor/CMakeLists.txt` 的必要注册/安装项，以及 C/P remote-subsurface 来源记录与现有双份 XML 的一致性核验。remote-subsurface XML 字节相同就保留，不伪造 XML 内容修改。

**明确排除**：协议 0.9.0 新增的 activation-token、prelaunch-splash 单例语义、仅版本差异带来的其它 XML 刷新。当前实现区间没有修改 prelaunch-splash 模块；因此不采用 `ac20cb07...` 新增的 singleton/error 合同。保留现存历史 XML 不表示继续注册已被来源替换的旧 global，也不额外实现兼容层。

### 4.3 同步工具的有限适配

P 初始基线的 `contract_migration.PARENT_INTEGRATION_FILES` 未包含这 7 个新增目标。已批准的精确路径扩展已在工具工作树实现，形成正式 replay 工具基线 `079202453e901d61ef85bd2f5a72c48b8e0bc779`，对应迁移正反向测试 16/16 通过；该基线在 attempt-7 完整验收后以 expected-old 转换接受，再由正式 R→C→P closeout 接受新候选。不改变 source path-policy、不开放整个 XML 目录。

其它已支持的本地测试/CMake 集成仍按现有机制绑定具体来源 SHA、相邻快照、实际补丁和逐路径证明。此授权不扩大到任意生产路径。

### 4.4 已批准：DDE shell v2 缺失配套

实现 `9dcaef2ed29dde1e6787936eb1f18546e7c79aea` 要求 `role` 事件及 `always_on_top` 角色，但固定 0.9.0 的 `dde/treeland-dde-shell-unstable-v2.xml` 和 P 当前 XML 均缺少这些定义；已检查的本地协议历史没有匹配修订。N10-attempt-4 的正常及关闭 XWayland 完整构建均在 `ddeshellmanagerinterfacev2.cpp` 的 `ROLE_SINCE_VERSION` / `send_role` 处失败。这不是七个新增 XML 或 §5 合同迁移的批准范围。

保留的本地草案（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/dde-shell-v2-proposal/proposed.patch`；未随仓携带） 仅拟修改 P 的 `protocols/compositor/xml/treeland-dde-shell-unstable-v2.xml`：manager/surface version 升至 2，新增 `always_on_top=2`（`since=2`），追加 `role` 事件（`since=2`）。它根据冻结实现与测试推导，**不是上游协议提交**；提案阶段仅通过 scanner/C 语法检查，attempt-5 已另行获得生成与完整编译链中的通过证据，但 P 总体仍受后续本地测试调用阻断。提案状态（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/dde-shell-v2-proposal/proposal.json`；未随仓携带） 保持提出时的 `proposed-not-approved / applied=false`。

用户已明确批准“按 PRD §4.4 实施这一额外配套”。授权覆盖上述精确本地 XML，以及将其绑定到 `9dcaef2e…` P 适配节点所需的同步证据和测试集成。使用现有精确路径迁移能力，不扩展通用白名单，不冒充上游协议来源。旧提案、attempt-4 及此前失败证据保留原身份；新候选另行冻结、fresh 构建和验证，完整通过后沿用既有本地收口授权。

## 5. 已批准：有限公共合同迁移

本批上游差异不仅包含 private 实现。保持“所有公共合同完全不变”会阻止完整移植以下来源行为：

| 来源 | 已核对的必要变化 | 已批准的边界 |
|---|---|---|
| `dfb4d0b86d09ba6bf469b163e005a12d743a9f68` | `wlroots_extra/wlr_ext_background_effect_v1.h` 加入公共头；增加相应构建 include | 在现有 WaylibShared 安装根内新增该头及必需生成/包含关系；不改变旧 namespace、target 名和安装根 |
| `da6deb69eee9e7d76c54ddaf3a545d11269fe96e` | `DISABLE_XWAYLAND` 成为 PUBLIC 条件定义，XWayland 源文件及公共头按配置选择，R feature 同步 | 默认开启时保留既有 XWayland 头与能力；关闭时按来源明确排除并向 consumer 传播配置；验证与所选配置一致 |
| `4258d3fd990988da31d8bb41b563b36b98535878`，配套 R 的 `8e7f5d53...` | XWayland 新增 `xcb-shape` 依赖 | 允许该依赖及其确实必要的链接/包元数据传播；不引入无关依赖 |

已批准以上来源所需的源码及安装合同迁移。实施时仍生成精确 `contract_migration`，绑定实际前后快照、完整 drift 和 `Refs:`，并通过安装 consumer 与固定 namespace 编译。N10-attempt-4 已取得真实安装差异（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-4/install-review/drift.json`；未随仓携带），按本节既有授权生成精确安装审批（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-4/installation-migration-approval.json`；未随仓携带），安装合同/namespace 审计（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-4/waylib-contract-audit.json`；未随仓携带） 为 `pass`。本轮实际新增背景效果头及其生成协议头，传播 `DISABLE_XWAYLAND` 定义，既有 namespace、目标标识和求值后的 pkg-config 结果不变；该局部审计通过不豁免 P 构建失败，未来出现超出表中语义的漂移仍须重新分析。

不变的产品要求：继续提供 `WaylibShared::SharedServer`、`WaylibShared::waylib-wlroots`、`WaylibShared.QuickSharedServer 1.0` 和既有安装布局；不恢复上游 `Waylib` 包名或系统 TreelandProtocols 隐式依赖，不增加旧包别名兼容层。

## 6. 验收条件

1. 128 个来源提交全部有合法归属和唯一来源映射，保留作者、时间及完整消息；R→C→P 顺序和两层 gitlink 连续，未重复导入基线。普通中间提交完成内容投影、追溯及 C 源码合同审计。
2. 关键节点 N10 运行 C baseline/candidate fresh configure、默认完整 build、install、完整 CTest；使用现有 `test_project` 做安装包 consumer，检查全部基线 namespace 和获批新头。
3. R baseline/candidate 各自完成真实 Meson configure/build/test；由编译与链接证据证明 C/P 使用本轮 R。真实零注册测试记 `NO_TESTS`，不伪造 PASS。
4. P 候选以正常产品配置 fresh configure、默认完整 build 和完整 compositor CTest。针对本批 XWayland 开关补充关闭配置验证，确认 C/R/P feature 一致；该结果不能代替默认开启配置。
5. 验证 §3 相关协议、焦点、剪贴板、输出和 remote-subsurface 生命周期；测试应包含真实 server/client 交互、失败与销毁边界。缺少运行依赖不能改成测试通过。
6. 配套协议审查覆盖真实请求/事件、行为与客户端升级；`protocol-verify` 和 advisory 各自正确，XML 生成来源是项目内文件。`protocol_pairing` 的 pass 依赖本轮真实交互证据。
7. 九项 gate、源码与安装合同、必需构建日志和 N10 完整报告通过，才接受到专用目标 refs。已授权的实现目标、§4/§5 限定适配与本地收口不重复确认。
8. 全批接受后调用正常 `finish --task sync`，检查完整范围覆盖并生成/核对 P/C 仓内记录。记录生成成功不代表自动提交文档或归并日常主线。

上一批 `test_drm` 的 SKIP 是 N9 专属接受例外，本批不继承旧授权。用户本轮最新另行明确要求：`test_drm` 因运行前提不满足而跳过（SKIP），并同步记录到执行记录。因此仅允许 N10 正常及关闭 XWayland 的完整、未过滤 CTest 中该用例的真实 SKIP 不阻断接受；不覆盖任何 FAIL、其它 SKIP、禁用/过滤或缺测，不证明 DRM/GPU 行为已通过。原始日志及 recorder 状态保留，限定接受依据绑定本轮 manifest、实际验证 attempt、完整发现集合和原始日志，最终 P/C 记录必须明确列出该 SKIP。其它验收条件不变。Qt 6.11.2 / Dtk 6.7.49 隔离工具链仍是可复用的历史兼容路线，不修改系统包来碰运气。

## 7. 不在本批范围内

- 不纳入实现 base 之前或 head 之后的提交，不以协议 commit 替代实现端点。
- 不重写历史、不自动 reset/abort/回滚，不清理旧工作树、证据或用户 WIP。
- 不 fetch、push、tag，不修改 remote 或子模块 URL，不改外层 index/gitlink。
- 不自动归并日常主分支，不提交自动生成的仓内文档。
- 不整体替换 XML，不新增双协议回退，不采用未经确认的公共合同或测试豁免。
- 不为满足通用行数阈值拆散来源的规范路径；跨路径改造或无关重构应另行处理。

## 8. 实施授权

用户已明确同意 §4、§5 的限定范围并要求继续完成移植与验证；最新指令将实现 head / tip 改为 `1f8c2a658b4b4e868e0650f9890c5e752fd1b839`，其余既有目标、选项、基线、追溯和验收要求不变。

本地推导配套的批准与验证仍独立记录；固定七个 XML 和 remote-subsurface 的上游协议来源不变。

具体隔离工作树、补丁适配和执行顺序记录在独立 `plan.md`，按 hello-plan/hello-build 进入实现；本 PRD 继续只记录需求与接受边界。
