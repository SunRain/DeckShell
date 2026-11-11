> 仓内参考副本；权威原文：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/plan.md`。
> 保留原同步方案的历史时点与验收边界；其中历史命令不是本次补档的执行指令。

# Treeland f342a5b6 → 1f8c2a65 实施方案

实施本轮已明确批准的 [PRD](prd.md)。批次为 `20261110_treeland_f342a5b6_to_9dcaef2e_local_sync`，唯一节点 N10。来源 `(f342a5b6debd028ed9bc4bc3e806118efbcae8f2..1f8c2a658b4b4e868e0650f9890c5e752fd1b839]`，source tip 等于 head。协议来源固定为 `578263755cb80b56f2e13fde34da1c294418e608`；用户已授权七个 XML、remote-subsurface 配套和 PRD §5 的有限合同迁移。

按用户最新指令，来源终点由 `9dcaef2ed29dde1e6787936eb1f18546e7c79aea` 延长至上述新 head；其余选项和要求不变。新范围为 128 个提交、0 个 merge，统一 inventory（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/preflight-1f8c2a65/inventory.json`；未随仓携带） 与 remote-subsurface 配套预检（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/preflight-1f8c2a65/proposed-protocol-inspection.json`；未随仓携带） 已通过；后者仍保留当时的 `inspected-not-accepted` 身份，最新正式配套 gate 见下。原方案包路径、批次名称、`Refs:` 及以下目标 refs 保持原样。

旧范围的预检、预览、正式回放和验证工件继续保留原始端点。新范围已在独立 `N10-attempt-7` 冻结并回放完整 128 提交，使用 fresh build/install；不改写旧工件，不复用旧候选 PASS 作为新终点验收。

## 当前实施结果：N10-attempt-7 / 已接受

本轮冻结 P `29a647ed09d4265365e9bc376e2ed5ab2b89491e`、C `6a924124e56b27d85d28974df76913a0c7b289e0`、R `b79b9b38a473ca57f5b54892280dfad4f25f8e42`，128 来源与同一 journal 的 remote 配套 replay 均完成；独立 P/C/R 投影、两层 gitlink、协议 advisory 及递归物化均通过。相对 attempt-6，仅 8 个已审 P 普通路径变化，C/R 普通树不变。

输出组修复绑定来源 `32dc1dea21f09c3aace8c2a8a5cd95fd8c9a223a`：生成 DConfig setter 同步更新字段但异步写入 backend，旧回声可覆盖刚写入的成员信息；会话内最新成员写入保存在 OutputManager，仍执行原持久化 setter，未写过的 UUID 继续读取已加载配置。可选类型修复及真实 alpha/QML 回归绑定 `a6907cee5a903ee39d88b247dc35d0c086ce524c`：不在 QML 解析时引用关闭配置缺失的 XWaylandSurface 类型，保留开启配置的裁剪路径；真实客户端同时验证原生 alpha、生产 content multiplier 和 QML root opacity 的 0→1，并排除 QML 创建失败后的 fallback content。原输出组 27 条断言未改动。

独立诊断证据（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/no-xwayland-review-1`；未随仓携带） 在正常与关闭配置中，每个相关目标均连续运行 30 次无失败；3 个改动 C/C++ translation unit 的原 compile-command 严格语法检查通过。探针日志与未修复时的失败保留，临时探针代码已移出正式候选。诊断结果不替代新冻结候选的完整验收。

fresh R baseline/candidate 默认完整构建通过，原生测试均为真实 `NO_TESTS`；C baseline 构建/安装和 12/12 CTest 通过。正常及关闭配置的 C 候选完整构建/安装、各 15/15 CTest、各 9/9 installed consumer，以及 P 默认完整构建均通过。完整、未过滤 compositor 的原始观察如下，两套注册集合只差两个 XWayland 专用目标；96 / 94 个内部 QtTest 摘要检查无其它失败或跳过，Glass 与 debug 前提已实际满足。

| 配置 | CTest total / passed / failed / skipped | CTest 退出码 | recorder 原状态 | 原始完整日志 |
|---|---|---|---|---|
| 正常 XWayland | **102 / 101 / 0 / 1**，46.19 秒 | 0 | **FAIL**（严格规则拒绝 SKIP） | 正常日志（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/logs/deckshell-compositor-ctest-attempt-1.log`；未随仓携带） |
| 关闭 XWayland | **100 / 99 / 0 / 1**，46.15 秒 | 0 | **FAIL**（严格规则拒绝 SKIP） | 关闭日志（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/logs/deckshell-no-xwayland-compositor-ctest-attempt-1.log`；未随仓携带） |

两套唯一 SKIP 都是原 `test_drm`：`drm: wl_drm unavailable (no DRM-capable renderer); skipped`。该用例仍实际启动、保留原退出码 77 和所有断言，不包含 GPU 实验或强制 SKIP。canonical 与 supplemental bundle 分开保存，不把上述 FAIL/SKIP 改写成 PASS；正常限定授权（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/test-drm-skip-authorization.json`；未随仓携带）及关闭配置限定授权（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/test-drm-no-xwayland-skip-authorization.json`；未随仓携带）仅使该真实运行前提 SKIP 不阻断，不证明 DRM/GPU 行为。

安装快照最初在非隔离环境报同名协议头歧义，失败日志保留；改在本批 Qt/ABI 隔离环境后完整快照成功，无工具或安装内容放宽。fresh 安装/namespace 审计（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/waylib-contract-audit.json`；未随仓携带）为 `pass / blocked_reasons=[]`，完整 drift 等于 §5 已批准范围；独立 remote 断言（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/logs/waylib-remote-export-contract-acceptance-attempt-1.log`；未随仓携带）针对 fresh C 安装包重建并通过 1/1。最终协议配套（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/protocol-pairing.json`；未随仓携带）及其余八项 gate 均通过。当前 DSG 数据逐字节匹配本候选源码，运行身份见 runtime-provenance.json（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/runtime-provenance.json`；未随仓携带）。

原完整报告（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/sync-report.json`；未随仓携带）保留 `BLOCKED` 和严格 SKIP 阻断，限定接受报告（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/sync-report-accepted.json`；未随仓携带）已由上述精确授权产生；过滤、缺少注册、错 attempt/候选、额外内部 SKIP/FAIL 均在边界检查中拒绝。P 工具基线先以 expected-old 从初始值转换到 `079202453e901d61ef85bd2f5a72c48b8e0bc779`，随后真实 closeout（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/closeout-journal.json`；未随仓携带）按 **R→C→P** 完成 CAS，三个本批 refs 已分别指向本节冻结候选。P 主工作树仅在原初始 HEAD 上安全 detach，外层 `MM DeckShell`、index/gitlink 及日常 C/R refs 均未改变；候选源码树仍干净。两仓摘要、逐路径适配说明和本方案/PRD 副本由强制 `finish --task sync` 交付；命令和真实结果保留在 `evidence/N10-attempt-7/finish-command.json`、`finish.log`。只有命令返回 0 且 P/C 实物内容核对通过，才代表整批包含仓内记录的交付完成；不自动暂存、提交或发布。

本次改动的 3 个 C/C++ translation unit 严格语法检查及 `accept_drm_skip.py` active LSP 检查通过；其他工具原有 `coverage: opengrep silent — diagnostics are incomplete (not a clean result)` 限制保留，不宣称全仓静态分析无问题。

## 历史结果：N10-attempt-6 / BLOCKED

本轮冻结 P `a06cc0efbbe62a2db9cd48d04dc5a93f1b50a831`、C `259996f611cd4e906801c0ebf0c81396b48e1986`、R `a6022a4acfaecc6a51c3ef513eafe0a4e5518451`，128 来源和同一 journal 的 remote 配套 replay 均完成；P/C/R 内容投影、两层 gitlink、协议 advisory 及递归依赖物化已通过。相对 attempt-5，P 普通文件仅改动 10 个已审本地测试/说明，C/R 普通树不变，两层 gitlink 为新冻结提交派生。

正常 P 默认完整构建已通过；正式完整 compositor 日志（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-6/logs/deckshell-compositor-ctest-attempt-1.log`；未随仓携带） 实际为 **101 passed / 0 failed / 1 skipped**，共 102 个目标（50.40 秒）。唯一跳过 `test_drm` 的原始原因：`wl_drm unavailable (no DRM-capable renderer)`。Glass 默认 benchmark 和 debug 进程名检查已实际执行，内部 QtTest 无其他跳过。recorder 按通用严格规则仍记录该 suite 的 `outcome=fail`；接受时仅适用下述本次用户限定授权，不改写原始结果。

C 基线完整构建/安装与 12/12 CTest、候选完整构建/安装与 15/15 CTest、安装包 consumer 9/9、字节相同的独立 remote 断言 1/1 通过。R base/candidate 完整 Meson 构建通过，原生套件均真实 `NO_TESTS`。fresh 安装合同/namespace 审计（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-6/waylib-contract-audit.json`；未随仓携带） 为 `pass / blocked_reasons=[]`，真实 drift 与已批准 attempt-5 完全相同。

关闭 XWayland 的 C 构建/安装、15/15 CTest、consumer 9/9 及 P 默认完整构建均已通过，但完整 compositor CTest 为 **98 passed / 1 failed / 1 skipped，共 100**，退出码 8。失败为 `test_treeland_output_group_manager_v1` 的 `group.promotion.re_enable_source`（26/27 客户端检查通过）；唯一 SKIP 仍为 `test_drm`。100 与正常 102 的注册差异仅为关闭配置不注册 `test_protocol_xwindow-control`、`test_treeland_xwindow_control_v1`，不是过滤测试。原始记录位于 `evidence/N10-attempt-6/no-xwayland-validations.json`。

该输出组失败在冻结正常及关闭配置的重复诊断中均复现，不能用正常配置首次成功或后续偶然成功替代修复。关闭配置另有 `SurfaceContent.qml: XWaylandSurface is not a type`；增强的真实 alpha-modifier 客户端检查在未修改生产库时验证到原生乘数为 0、QML opacity 仍为 1。独立 `worktrees/no-xwayland-review-1/parent` 已完成修复及两配置连续 30 次验证，证据位于 `evidence/no-xwayland-review-1/`；诊断工作树不是正式候选，修复已重新投影到新的 attempt-7，仅其 fresh 完整验证可用于接受。

attempt-6 不适用仅 DRM 的接受路径。独立 remote 的 1/1 最初只在单独 bundle，首次追加 canonical 的前置计数断言失败；原失败保留。主验证 writer 结束后，已另行串行执行并以 `waylib-remote-export-contract-acceptance` 追加实际 1/1，remote 配套 gate 通过，不抵消本轮 P 缺陷。attempt-6 原 BLOCKED 报告（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-6/sync-report.json`；未随仓携带）已生成；该报告的常规 bundle 只含正常初次102目标运行，关闭配置100目标的失败及两配置重复失败另保留于原 supplemental/诊断工件，不能据常规报告仅有 DRM 阻断而接受本轮。attempt-6 未执行限定授权接受、CAS 或 `finish`。

## 历史结果：N10-attempt-5 / BLOCKED

完整报告（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-5/sync-report.md`；未随仓携带） 与机器摘要（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-5/sync-report.json`；未随仓携带） 已生成，128 来源 replay、九项结构化 gate、R/C/consumer 验证均完成。P `8091edc9b72d1f81d5264af8f36fb765bc41625c`、C `837596add994d3feb165d71cc7eae6e5e586acb1`、R `05b0a8aad339aef07bf3d912e5028605dbe404f1` 均未接受。

获批 DDE XML 已在 `9dcaef2e…` 的 P 节点集成，生成角色事件并编译通过；正常及关闭 P 完整构建随后均在 `compositor/tests/protocols/treeland-dde-shell-lockscreen-desktop-v1/setup.cpp:24` 的旧 `helper` 引用处失败。两个 compositor CTest 均未运行。C 基线 12/12、候选与关闭配置各 15/15、两种 consumer 各 9/9、原独立 remote 断言 1/1 通过；native R 两侧确为 `NO_TESTS`。本轮 fresh 安装审计与 remote 配套 gate 均 `pass`，不豁免 P 失败。

独立 `worktrees/test-caller-review-1/parent` 保留完整诊断构建及失败，修正本地测试随已批准来源迁移遗漏的调用：Helper→WaylandServer、foreign-toplevel v2→v3、virtual-output→output-group，保留真实资源销毁/断连/服务停止断言及 generated-contract 检查。七个 XML 加入后包清单断言为 39，不删除原测试或恢复退休 global。诊断默认完整构建及 7 个改动 C/C++ 文件的严格语法检查通过；补齐私有 `/proc` 与 `GLASS_BENCH=1` 后，完整诊断日志（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/test-caller-review-1/ctest-3.log`；未随仓携带） 为 102/102 CTest 通过、内部 QtTest 0 跳过（46.77 秒）。其中 DRM 使用了独立 GPU 实验改造，不能当作未改造正式用例的通过证据。按下述最新指令，正式候选不纳入 DRM 实验，仅将必要调用方、包清单及 DockPreview 尺寸/警告检查绑定原来源节点进入新的 `N10-attempt-6`。不得续写 attempt-5 候选或把诊断 PASS 当正式验收。

### 最新执行指令：仅 `test_drm` 的运行前提 SKIP

用户明确要求：`test_drm` 用例“因运行前提不满足”而跳过（SKIP），并同步记录到执行记录。本轮仅接受正常及关闭 XWayland 的完整、未过滤 CTest 中该目标的真实 SKIP；不覆盖 FAIL、其它用例的 SKIP、未运行、禁用或过滤测试，不宣称 DRM/GPU 行为通过。

原默认 headless/pixman 验证上下文不具备该用例要求的 DRM global/渲染条件，最初诊断（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/test-caller-review-1/ctest-1.log`；未随仓携带） 已记录 `test_drm ***Skipped`。可访问 GPU 不等于原测试的运行前提全部满足。后续 GLES2/GBM/native provider 采样实验及 Qt item-grab 黑图日志保留，但四个 DRM 实验文件和 INDEX 中的对应实验说明不进入正式候选；不添加强制 skip、不改变原用例断言或注册。新正式验证继续运行完整发现集合，原始日志和 recorder 状态不改写，另以绑定 N10 候选/日志/测试集合的限定授权记录接受依据；最终 P/C 仓内执行记录必须同时展示该 SKIP 与其余真实结果。

## 历史结果：N10-attempt-4 / BLOCKED

完整报告（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-4/sync-report.md`；未随仓携带） 与机器摘要（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-4/sync-report.json`；未随仓携带） 已生成，`build_scope = {kind: range-head-only, source_head: 1f8c2a658b4b4e868e0650f9890c5e752fd1b839}`。总体为 `blocked`，不是已接受同步。九项结构化 gate 均为 `pass`，两个 P 默认完整构建失败，compositor CTest 未运行；报告中额外的 wrapper-build 缺证据是 P 构建未成功的从属结果。

| 层 | 冻结 candidate HEAD | 状态 |
|---|---|---|
| P | `6766c71aa729efd75086bb83661ce32c84094b28` | 正常及关闭 XWayland configure 通过，完整 build 失败；未接受 |
| C | `fefa553c5bd6b93fc8275b3f69a6f9ecdf5774e0` | 默认完整构建/安装、15/15 CTest、9/9 installed consumer 通过；未接受 |
| R | `0d95b31a05e97ccf511fb6b457e9653611802f11` | base/candidate Meson configure/build 通过，两个原生测试入口均为 `NO_TESTS`；未接受 |

- C 基线完整构建/安装及 **12/12** CTest 通过。关闭 XWayland 的 C 完整构建/安装、**15/15** CTest 及 consumer **9/9** 通过。
- fresh 安装合同/namespace 审计（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-4/waylib-contract-audit.json`；未随仓携带） 为 `pass / blocked_reasons=[]`；完整 drift 严格位于 PRD §5 已批准范围，现有 package、namespace、target 和安装根保留。
- remote-subsurface 配套 gate（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-4/protocol-pairing.json`；未随仓携带） 为 `pass / paired / blocked_reasons=[]`；审查（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-4/protocol-review.json`；未随仓携带） 覆盖 wire、行为、C/P 客户端及兼容性。attempt-3 曾失败的独立撤销断言保留原字节、重新针对本轮安装包构建，**1/1** 通过。
- artifact root 为 `evidence/N10-attempt-4/`，五个独立源码工作树及递归依赖位于 `worktrees/N10-attempt-4/`。`manifest.json`、`journal.json`、实际命令和日志保留；准备/验证脚本以 `N10_REPLAY_ATTEMPT=N10-attempt-4` 选择此身份，不续写旧尝试。
- 产品 P/C/R 工作树干净，三个目标 refs 仍为下列初始值；外层 HA-DeckShell 原有变更未纳入本批。未执行 expected-old 接受、closeout、`finish` 或生成最终 P/C 仓内记录。

### 已解除授权阻断：DDE shell 配套

用户已批准 [PRD §4.4](prd.md#44-已批准dde-shell-v2-缺失配套)。独立 **N10-attempt-5** 已在 `9dcaef2ed29dde1e6787936eb1f18546e7c79aea` 的 adapted P 节点加入精确本地 XML、批准说明与逐路径投影证明；通用迁移工具已支持该路径，无需扩展。七个 XML / remote / §5 既有授权不变，工具基线仍为 `079202453e901d61ef85bd2f5a72c48b8e0bc779`。下列失败是不可改写的 attempt-4 历史事实。

两个 P 完整构建都在 `compositor/src/modules/dde-shell/ddeshellmanagerinterfacev2.cpp` 的 81/82、294/295 行失败：缺少 `TREELAND_DDE_SHELL_SURFACE_V2_ROLE_SINCE_VERSION`、`treeland_dde_shell_surface_v2_send_role` / `send_role`。正常/关闭日志分别为 `evidence/N10-attempt-4/logs/deckshell-build-attempt-1.log`、`deckshell-no-xwayland-build-attempt-1.log`；依赖这两次完整构建的 compositor CTest 均未运行，不能写成 PASS 或 SKIP。

固定 0.9.0 及已检查本地历史没有这份匹配 XML。原本地提案（外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/dde-shell-v2-proposal/proposed.patch`；未随仓携带） 及其 `proposed-not-approved / applied=false` 元数据按提出时身份保留；本轮批准另记入新候选的输入证据，不覆盖原记录。attempt-4 中此 XML 仍逐字节等于初始基线；attempt-5 仅在获批的对应节点集成提案内容，不伪造上游修订。

保留 attempt-4 与旧失败证据，为变化内容创建新 frozen replay/manifest 及 fresh 验证身份；不得重标本次 PASS，也不得通过禁用产品目标或删除角色事件来绕过要求。完成正常及关闭 P 全构建/测试、当前运行依赖记录和有效完整报告后，才按原安排执行 expected-old R→C→P 接受并 `finish --task sync`。

### 后续同类验证可复用的决策

- export token 的撤销与原生 `wl_surface` 的销毁是不同生命周期：前者只撤销寻址权，测试须验证已存在且有真实 buffer 的关系仍映射；后者才解除映射/关联。真实 socket 检查可揭示编译和同源生成 bindings 无法发现的语义错误。
- 共享 `validations.json` 的 recorder 必须串行；独立实验使用单独 bundle。原子替换本身不能防止并行读改写覆盖记录。
- fresh Meson 隔离配置明确使用 `CC=/usr/bin/cc`、`CXX=/usr/bin/c++`；仅关闭 ccache 不阻止自动选择 sccache，失败的旧配置身份不复用。
- CTest 目标 PASS 不排除内部 QtTest SKIP；隔离环境需要私有 `/proc` 和真实 `GLASS_BENCH=1` 才能执行原 debug/benchmark 断言。正常/关闭配置的注册数按实际 CMake 条件核对，不要求人为相等。
- DConfig 异步旧回声可能覆盖新字段，输出成员的会话内权威值须保留；可选 QML 类型必须在解析阶段也可缺失，真实 content/opacity 检查能揭示仅原生协议状态测试漏掉的 QML fallback。

## 基线与写入边界

P 初始 `a9d6cb854c4fe26d767f828f89c301c49fb44d59`，目标 `refs/heads/master-merge-to-20261110-9dcaef2ed29dde1e6787936eb1f18546e7c79aea`。C 初始 `f1fe3771a9a8fa3037da1d6ab153cc538610b721`，本批目标 `refs/heads/waylibshared-merge-to-20261110-9dcaef2e`；R 初始 `c844d3549136a250231d3abb2fc5f6832ff05c4e`，本批目标 `refs/heads/master-merge-treeland-to-20261110-9dcaef2e`。两层 gitlink 及 R URL 沿用 PRD。

所有预览、工具和正式 replay 使用本方案 `worktrees/` 下的独立 linked worktree；证据和源码外 build/install 使用 `evidence/`。发生冲突保留旧现场，不 reset/abort 或删除 journal。`Refs:` 固定使用 `.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/plan.md`。

## 执行安排

1. 独立工具工作树只扩展七个已授权 XML 精确路径，同步说明并运行迁移正反向测试。提交工具修改作为正式 P replay 基线；目标 ref 在验收前保持初始值，最终先以 expected-old 接受工具基线，再用正式 closeout 接受回放结果。
2. 从冻结 P/C/R 基线建立预览，按来源顺序审查目标相对补丁，保留本地包名、QML URI、安装、DDM 和已有回归保障。新增 XML 在首次相关实现节点接入；基线已经拆出的本地构建列表通过规范 CMake 入口必要适配，禁止无依据的兄弟路径扩张。
3. 将每个适配补丁与完整路径说明持久化；对授权合同变化绑定相邻源码快照与真实 drift，R 基线两处本地差异单独证明。正式 decisions 冻结后执行 R→C→P replay，并在同一 journal 完成协议配套。
4. 独立运行 P/C/R 内容投影、两层 gitlink、来源追溯、协议 advisory 和物化验证。检查实际依赖对象及 worktree 身份，不能用预览提交代替正式候选。
5. 使用 `validation_record.py --manifest ...` 运行 C base/candidate configure/build/install/完整 CTest、既有 consumer；R base/candidate Meson configure/build/test；P 正常配置完整构建与 compositor CTest。检查本批 XWayland 关闭配置传播。安装合同迁移仅批准 PRD 明确的差异，保持 namespace/target/install root。
6. 使用本批真实交互证据完成 `protocol-verify`，由 `generate_sync_report.py` 生成完整报告。报告通过且目标 refs 未检出后，执行 R→C→P expected-old CAS。本轮授权已涵盖这些目标与收口，无需重复确认。
7. 运行 `unified_sync.py finish --task sync`，按整批来源范围自动生成并核对 P/C 仓内记录。不自动提交记录、不归并日常 refs、不操作外层 index 或远端。

## 验证与失败处理

工具：`python3 -m unittest discover -s <tooling>/doc/skills/treeland-deckshell-waylib-unified-sync/tests -p test_contract_migration.py` 及实际受影响的测试，`git diff --check`。

产品：技能要求的全部固定 validation IDs、九项 gate、实际 closeout 和 finish。必需构建使用默认完整 `cmake --build`；C/P CTest 使用 `--no-tests=error` 并保留完整发现与结果。失败、SKIP 和缺测原样报告；最新用户指令仅豁免 `test_drm` 因运行前提不满足的真实 SKIP，范围及记录要求见上节，不扩展到其它目标或真实失败。

优先核对历史 Qt 6.11.2 / Dtk 6.7.49 隔离工具链和 DConfig 依赖仍可使用；复用材料但每轮 fresh build，不复用历史测试结果。若失败来自现有条件，先寻找不降低验收标准的可行方案；只有超出已批准范围或缺少必要权限/条件时停止受影响操作，保留全部证据。
