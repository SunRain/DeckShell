> 仓内参考副本；权威原文：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/prd.md`。
> 保留原同步方案的历史时点与验收边界；其中历史命令不是本次补档的执行指令。

# Treeland 1f8c2a65 → 77f885c8 同步需求

## 当前结论与本轮授权

用户指定参考 上一批方案包（外层历史资料：`外层工作区（历史）/.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/plan.md`；未随仓携带），使用 统一同步技能（外层历史资料：`Treeland 来源仓库/doc/skills/treeland-deckshell-waylib-unified-sync/SKILL.md`；未随仓携带），将 Treeland 的 `(1f8c2a658b4b4e868e0650f9890c5e752fd1b839..77f885c8dbeb0e0e0bebdafdee02eadb1d150439]` 同步到 DeckShell 的 `master-merge-to-20261111-77f885c8dbeb0e0e0bebdafdee02eadb1d150439`。

用户已明确批准本 PRD §3–§5：完整纳入 Session/DesktopEnvironment 重构及必要调用方迁移，保持 WaylibShared 包名、namespace、安装布局和已接受 XML 来源不变，保留当前 WIP。本轮另行明确批准“DRM test 依旧 SKIP”，仅允许原运行前提不足产生的真实 SKIP，不强制跳过或修改断言。

用户随后明确批准 §8 的独立空客户端修复，要求使用单独 commit，并在 C 的 `docs/treeland-sync/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/` 保留独立说明。该授权不改变 65 个来源提交的冻结范围，不将本地修复混入来源映射。

§9 的独立快捷键提交为 P `bf2b6c2395275e74703933d9296640de26968631`，§10 的独立桌面归属提交为其直接子提交 P `b72a24a5688a6b02f67ededbb4483f0748938f28`；保留冻结判空 P/C 提交。当前 `N11-local-fix-3` 两配置 fresh 完整构建成功，完整 CTest 为 **102 total / 101 passed / 0 failed / 1 skipped** 与 **100 / 99 / 0 / 1**，原 Session-isolation 两配置完整通过，fixture、C 客户端和 header 字节未改。下文 null、快捷键和桌面失败描述属于原候选，不代表当前仍失败。

当前九项 gate、协议配套、runtime、真实安装库消费与补充边界检查均已完成；限定接受报告（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/sync-report-accepted.md`；未随仓携带） 实际 exit 0 / `pass`，只按本轮授权使原 `test_drm` 前提不足 SKIP 不阻断，原 strict `blocked`、recorder `fail` 和日志原样保留。DRM/GPU 行为没有被证明通过，其余测试没有豁免。本批专用 refs 的 R→C→P expected-old CAS 已真实 exit 0，主 P 在同旧 HEAD 安全 detach，五份 WIP、外层 index 和日常 refs 未变。整批两仓记录使用原方案根及完整区间执行 `finish --task sync`；其真实退出状态和记录核对以 [实施方案](plan.md) 定位的 finish 工件为准，不把 CAS 成功说成文档已经交付。

完整接纳是因为输入、输出、窗口及协议域之间存在依赖；只摘取末尾修复会改变用户给出的完整范围。

本批保留上一批已接受代码作为基线，不把旧授权自动扩展到未知合同漂移或其它测试豁免；本轮批准与上一批证据分别记录。

## 1. 目标与已有项目约束

维护者需要在指定同步分支获得该区间的完整上游行为，同时保留 DeckShell 的项目结构、WaylibShared 包与实际子模块依赖。现有桌面用户的窗口、输入、输出及账户切换功能不能因移植回归；涉及多用户的私人模型、协议对象和事件须按所属用户处理。

保留经本地状态核实仍成立的约束：

- P 为 DeckShell，C 为 `3rdparty/waylib-shared`，R 为 C 内独立的 `3rdparty/wlroots` 子模块；不能沿用早期“全部跳过 waylib/qwlroots”的旧两仓规则。
- 保留 `WaylibShared::SharedServer`、`WaylibShared::waylib-wlroots`、`WaylibShared.QuickSharedServer 1.0` 及现有安装布局；不恢复上游包名和隐式系统 TreelandProtocols 来源。
- 使用完整 SHA 和逐提交来源映射，保留作者、时间、原消息及合法适配证据。普通中间提交不承诺可构建，最后来源节点必须完整验收。
- 新批次和上一批的证据、来源范围与结果分开，不续写上一批 journal，不借用旧候选的 PASS。

## 2. 已核实的范围与冻结基线

| 项目 | 本地核对值 |
|---|---|
| 来源仓库 P | `DeckShell/` |
| 用户指定来源标识 | `refs/remotes/treeland/master` |
| 来源 base，不包含 | `1f8c2a658b4b4e868e0650f9890c5e752fd1b839` |
| 来源 head / 本轮 source tip，包含 | `77f885c8dbeb0e0e0bebdafdee02eadb1d150439` |
| P 指定目标 ref | `refs/heads/master-merge-to-20261111-77f885c8dbeb0e0e0bebdafdee02eadb1d150439` |
| P 预检时提交基线 | `1352256db1ea38476cf5e86b169bc3dd61822ad7` |
| P → C 基线 gitlink / C 预检 HEAD | `a56cf9dcf7494db7266e9c5d407f170861d839e7`，mode `160000` |
| C → R 基线 gitlink / R 预检 HEAD | `b79b9b38a473ca57f5b54892280dfad4f25f8e42`，mode `160000` |
| 预检时检出的 C / R 分支 | `waylibshared` / `master-merge-treeland` |
| C 本批专用目标 | `refs/heads/waylibshared-merge-to-20261111-77f885c8`；预检时位于初始 C SHA，最终 CAS 见 plan |
| R 本批专用目标 | `refs/heads/master-merge-treeland-to-20261111-77f885c8`；本段无 R 内容修改，最终 CAS 见 plan |
| 唯一完整验收节点 | N11：`77f885c8dbeb0e0e0bebdafdee02eadb1d150439` |

预检时指定 P 分支已存在并检出，包含上一批已接受 P `29a647ed09d4265365e9bc376e2ed5ab2b89491e`，之后有上一批记录提交和 C 日常头引用。当前 C 包含上一批已接受 C `6a924124e56b27d85d28974df76913a0c7b289e0`；不能错误地从旧候选重建新基线，丢掉已有记录提交。

核对时 `refs/remotes/treeland/master` 为 `f25618156fdce90fc5339ed0ba9ba15cb01b7844`，比用户给定 head 多出两个提交。它只是来源标识，**不用于扩大本轮 source tip 或范围**。本轮不含 `24ac7aaebebf8ad508fe713956efc353df9238f6` 和 `f25618156fdce90fc5339ed0ba9ba15cb01b7844`。

`base` 是 `head` 的祖先，区间共 **65 个来源提交、0 个 merge**。统一 inventory（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/preflight/inventory.json`；未随仓携带） 退出 0，结果：

| 分类 | 提交数 |
|---|---:|
| `deckshell-only` | 52 |
| `waylib-only` | 10 |
| `dual` | 3 |
| `unowned-skip` | 0 |
| `blocked` | 0 |

没有未知或待批准 review-only 路径。本区间没有 R 内容提交、来源 XML 提交或区间内发布 tag。R 已登记，因此仍须绑定真实 R 基线、核实新来源 base 的子树投影，并满足统一技能的依赖验证；“R 无变化”不等于 R gate 不适用。

### 工作区已有修改

P 有以下 5 个未暂存修改，未纳入本轮输入：

- `compositor/src/core/rootsurfacecontainer.h`
- `compositor/src/modules/wine-window-management/winewindowmanagement.cpp`
- `compositor/src/session/session.cpp`
- `compositor/src/workspace/workspace.cpp`
- `compositor/tests/protocols/drm/setup.cpp`

当前 diff 主要涉及排版、include 顺序及注释，不能据此直接宣称其行为已验证等价。前四个文件与新区间直接重叠；DRM setup 是受接口变化影响的本地测试调用方。按本轮授权保留这些工作区修改，以提交基线建立隔离候选，不覆盖、暂存、提交、清理或自动 stash 它们。

工作区修改不会阻止隔离预检，但预检时指定 P ref 正被检出，不满足 closeout 前提。最终接受前在相同旧 HEAD 安全 detach，保留工作区内容，释放目标 ref 后才执行 CAS；不强行检出会覆盖 WIP 的新候选。外层 HA-DeckShell 同样有既有暂存与未提交内容，全部保留，不更新其 index/gitlink。

## 3. 已批准：完整纳入的行为边界

本区间净变化涉及 158 个文件，6997 行新增、2371 行删除。规模主要来自跨模块的会话隔离组装，而非独立修复集合。

### 3.1 会话、桌面与协议归属

- 同一进程和 `wl_display` 下，每个 Session 独立组装 DesktopEnvironment、Workspace、输入、逻辑输出、壁纸、切换器与预启动对象。
- 协议和客户端所有权按所属根 socket 及 `parentSocket` 链解析，包括 XWayland/子 socket；不以“当前活动用户”替代请求者。
- foreign-toplevel 初次及重新绑定只枚举所属用户窗口；预览请求不能获得另一用户的私人窗口。
- appearance、personalization、快捷键、selection、IME、xdg-foreign 等已迁移协议实例与事件域按用户隔离。
- 停用用户的展示域关闭 rendering/input；切回只恢复展示许可，不强行改变映射、最小化、工作区或锁屏状态。
- 销毁和注销按真实对象所有权收尾，不允许重复解除 globals 或另一用户的对象被连带销毁。

### 3.2 输入与工作区

- 输入过滤器、手势识别器、快捷键控制器与逻辑 seat 固定绑定所属桌面；停用时取消旧 swipe/hold/捕获，避免旧序列触发新用户动作。
- IME 和虚拟键盘路由按 seat 对象身份，不按可能重复的 seat 名；焦点交接停止旧键盘自动重复并清理过滤键状态。
- Workspace 和 QML 预览使用所属对象；非活动工作区不能触发前台焦点变更，动画可以取消。

### 3.3 共享显示与窗口行为

- 系统显示模式与每屏参数继续使用共享系统配置；用户切换不能回滚硬件缩放/模式，各用户的窗口及 LayerShell exclusive zone 分别计算。
- 输出配置应答留在原请求协议对象，同一配置只应答一次；三屏往返切换不重复发布 head。
- 保留 Dock 小数缩放 resize 修复、X Shape 输入区域/光标 resize 修复、拖放 mouse/touch grab 保持及输出测试工具的拒绝后回滚行为。
- Prelaunch 请求、闪屏和关闭操作按所属用户匹配，后台子 socket 窗口激活后能够恢复展示。

本批只移植这 65 个提交中实际完成的隔离范围，**不宣称所有 Wayland 协议、捕获授权和基础 global 都已实现全量多用户隔离**。上游新增文档和 session-isolation README 明确记录多项未编译、未运行或未覆盖的场景，不能把其文字视为测试结果。

终点 `77f885c8…` 明确撤销 `b3bf7bb0…` 中 detach 前的 `wl_global_remove`，而新文档仍描述“detach 前撤下 global”。验收须以终点源码及实际创建者销毁路径为准，核实注销后不暴露失去归属的 global、无重复移除/销毁；不能用文档替代证据，也不自行撤销用户指定的终点 revert。

## 4. 已批准：必要公共合同迁移

允许与该范围直接相关的以下变化，并对本地调用方同步适配；保留既有 package/namespace/target 和安装根，不新增旧接口回退层，不承诺旧二进制 ABI 兼容。

| 来源 / 位置 | 已核实变化 | 本轮授权边界 |
|---|---|---|
| `adca75e4eb9b7f6ca471e082e3abc149103a61cc`，`wserver.h` | `WServerInterface` 新增 socket/client 归属 API 和成员 | 接纳范围内归属 API，消费方与候选重编译；所有权边界验证不豁免 |
| `4d1a9839feb4ba8817680273bd58c946aca727b9`，`winputmethodhelper.h` | 构造函数由 `(server, seat)` 改为 `(server, seat, Protocols)` | 移植显式依赖组装；同步 C 示例、现有 consumer、P shell/session 及受影响测试调用方，不保留旧构造函数伪兼容 |
| 同一来源，`waylib/src/server/CMakeLists.txt` | 额外安装 6 个协议 manager 头 | 仅在既有安装根接入下列精确文件及真实必需依赖；不开放整个 private 头目录 |
| `7b5fc457aea1f4b85ca931c47cda5dcd15cfafd3`，`woutputmanagerv1.h` | 新增 `sendTestResult`、`setOutputStates` | 接纳显式状态发布及请求应答变化，验证实际协议应答和 head 生命周期 |
| `0dce4704b8338c4533ca20276abd60f0d7492e58`，`wseat.h` | 新增 `clearFilteredKeys` | 接纳 seat 交接所需能力，保留正常输入路径 |

六个来源文件位于 `waylib/src/server/protocols/private/`：

1. `winputmethodv2_p.h`
2. `wtextinput_p.h`
3. `wtextinputv1_p.h`
4. `wtextinputv2_p.h`
5. `wtextinputv3_p.h`
6. `wvirtualkeyboardv1_p.h`

源码和安装审计仍须绑定本批相邻快照、真实差异与来源；批准这些语义不等于批准未知公共合同漂移。额外集成文件只能使用现有精确迁移机制，不能通过扩大 path-policy、删测试或搬到兄弟路径绕过门禁。确有独立本地缺陷时另记原因与修复边界，不将其冒充上游原补丁。

## 5. 已批准：协议来源与预检

C 基线的 `waylib/protocols/remote-subsurface.json` 已接受实现 base `1f8c2a65…`，XML 为 `578263755cb80b56f2e13fde34da1c294418e608:wine/treeland-remote-subsurface-unstable-v1.xml`。本地 `treeland-protocols/` HEAD 与 tag `0.9.0` 都是该提交。

已批准本批保留同一 XML head，不批量升级其它协议。批准前生成的 selection（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/preflight/protocol-selection.proposed.json`；未随仓携带） 与 配套检查（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/preflight/protocol-inspection.proposed.json`；未随仓携带） 保留原身份，工具退出 0，状态为 `pass / inspected-not-accepted`；正式 replay 另用本轮获批输入：

- XML 范围为空，wire 与描述不变。
- 实现范围仍完整检查 65 个提交；`34572180b867290b45e53483ed831a9d03e775bc` 修改配套路径 `waylib/src/server/qtquick/wsurfaceitem.cpp`，加入 mouse/touch grab 保持。
- 预检不是最终 pairing 接受。正式候选仍需审查客户端、运行真实交互，并生成 `protocol-verify` 结果；不借用上批 remote 测试 PASS。

本区间来源没有 XML 改动；最终 advisory 是否触发还须根据实际 parent candidate 判定，不能在 replay 前用“无来源 XML”替代该判断。

## 6. 验收要求与本轮限定 DRM SKIP

以下来自统一技能的正常交付要求，不使用上一批测试计数作为本批预期值：

1. 65 个来源按唯一归属完整追溯，包含被终点撤销的中间提交；P/C 内容投影、C 逐提交源码合同、两层 gitlink 和 R 基线检查有效。仅需完整构建 N11，不要求普通中间提交编译。
2. C base/candidate 各自 fresh configure、默认完整 build、install、完整 CTest；现有 `test_project` consumer 和固定 namespace 头探针实际通过，真实安装差异在本轮获批边界内。
3. R 已登记，按技能提供真实基线/候选 Meson 验证与 C/P 实际依赖证据。本段 R 内容不变，不伪造 R 来源提交。真实零注册测试只记 `NO_TESTS`。
4. P fresh 正常产品配置完整构建、未过滤 compositor CTest；保留 XWayland 默认开启，并建议补充关闭配置的完整回归，防止可选类型再次在 QML 解析阶段失败。
5. 新增 `test_session_isolation` 必须实际执行，覆盖真实 A/B socket、窗口/协议域、后台绑定、三屏状态、桌面/输入对象归属、跨用户预览拒绝与展示恢复。第二账户缺失导致返回 77 时不能计为通过；不擅自创建系统账户或将测试禁用。
6. 上游测试尚未覆盖的真实 XWayland 双进程、持续输入尾部、GPU 帧与注销压力等场景须据影响确认验证条件。没有真实观察就明确未验证，不把 registry/对象指针检查表述为全部资源隔离已通过。
7. remote-subsurface 配套、其它八项 gate、必需运行依赖、安装消费链和 N11 完整报告通过后，才按已确认范围接受本批专用 refs；任何 FAIL、未执行或未经本轮批准的 SKIP 都阻断接受。
8. 整批接受后必须 `finish --task sync` 生成并核对 P/C 仓内记录。生成记录不隐含提交文档、归并日常分支、改外层 index 或远程发布。

用户本轮再次明确授权 **DRM test 依旧 SKIP**：仅使正常及关闭 XWayland 的完整、未过滤 CTest 中 `test_drm` 因原运行前提不足产生的真实 SKIP 不阻断接受。保留原日志、退出码 77、recorder 的严格 FAIL/SKIP，另生成绑定本批候选、实际 attempt、完整发现集合和日志的限定接受依据；不强制跳过，不纳入上一批 GPU 实验，不宣称 DRM/GPU 行为通过。任何其它 SKIP、FAIL、过滤、禁用或未执行仍阻断，包括新增 `test_session_isolation`。

## 7. 明确不做

- 不重复同步 `1f8c2a65…` 本身或之前的提交，不纳入 `77f885c8…` 后的两个来源提交。
- 不整树替换、不压成无法逐提交追溯的笼统 merge，不更改所有权策略来绕过结构冲突。
- 不覆盖、提交或清理当前 P 的 5 个 WIP、外层变更和上一批证据；不自动 reset、abort、stash 或回滚。
- 不自动 fetch、push、tag，不修改 remote/子模块 URL，不更新外层 HA-DeckShell gitlink。
- 不移动日常 P `master`、C `waylibshared` 或 R `master-merge-treeland`；只接受表中本批专用 C/R 目标。
- 不批量刷新 XML、引入旧协议/API 双轨回退、扩展无关隔离功能或为通用行数指标拆散来源路径。

本轮批准已覆盖上述限定迁移、完整验证、本批专用 refs 的本地收口与 `finish`，不重复索取授权；§8 判空及 §9 快捷键解绑窄修均已独立批准，其外的未知公共漂移或其它独立本地缺陷另行分析。实施工作树、适配、运行环境和收口安排记录在独立 [plan.md](plan.md)。

## 8. 已批准：socket-owned 空客户端独立修复

### 问题与目标

`N11-attempt-3` 两配置完整 CTest 的唯一失败均为 `test_session_isolation`：原测试主动调用 socket-owned `ownsClient(nullptr)`，实现随后调用 `client->socket()` 并 SIGSEGV。冻结来源 `77f885c8dbeb0e0e0bebdafdee02eadb1d150439` 的 `wserver.cpp`、`wsocket.cpp` 和该测试 setup 与候选逐字节一致；API 来自 `adca75e4eb9b7f6ca471e082e3abc149103a61cc`，空指针负向断言来自 `f3e6d407f58f84ecf884d08653d5f8db1b31caac`。这是来源实现与测试预期不一致，经同步运行暴露，不是本地调用方适配写错；未独立运行纯 Treeland，不宣称其 CI 已复现。

维护者需要保留所有权检查：绑定 socket 的接口对空客户端返回 `false`，不崩溃、不误放行；非空客户端仍按自身 socket 及父 socket 链判断，同用户接受、其它用户拒绝。

### 授权边界与交付

- 先保留 `if (!ownsSocket()) return true;`，仅在其后拒绝空 client。函数入口判空会改变未绑定 socket 的全局接口行为，并阻断 `globalFilter()` 既有同进程、尚未包装客户端例外，不属于这次授权。
- 生产源码只改 C `waylib/src/server/kernel/wserver.cpp`。C 同一独立修复 commit 保存 `docs/treeland-sync/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/null-client-ownership-fix.md`；P 另作相邻 commit，仅传播 C gitlink。
- 保留原来源 manifest、journal、候选及失败证据；新的 detached P/C 提交通过精确审批派生 manifest。R、XML、协议实现配套/provenance、public headers、包名、namespace 和安装合同不变。
- 不删改原 Session-isolation 空客户端、A/B 隔离及子 socket 断言，不引入全局判空策略、mock 生产所有权对象或额外豁免。

### 可独立判断的验收条件

1. 原 `test_session_isolation` 在正常与关闭 XWayland 配置真实通过，无崩溃、超时、SKIP 或断言放宽。
2. 真实安装库的补充检查确认：socket-owned 空 client 为 `false`；无 socket 空 client 仍为 `true`；非空同 socket/子 socket 接受、无关 socket 拒绝；无 socket 的同进程未包装客户端仍能通过真实 registry 的 `globalFilter()` 例外。
3. 两配置 fresh 完整产品构建/未过滤 CTest、C/R 依赖及安装消费链、所有原结构化 gate、协议与 runtime 记录重新绑定新候选；旧 PASS 不换摘要复用。只有原 `test_drm` 真实前提不足 SKIP 可按 §6 限定接受。
4. 实际 Git 对象显示 C/P 各一个相邻非 merge 本地提交；修复说明随 C 提交保存，最终两仓记录单列 local-fix，不计入 65 个来源。完整验收后才执行已获准的专用 refs closeout 和 `finish`。

### N11-local-fix-1 历史结果，不降低原验收条件

C `780ae6e53d52483d17f14d40fa44c8d67d5874fc` 已提交判空和独立说明，P `da94bafea5d130bdee98e2c7854e2b352c7d5224` 仅传播 C gitlink。真实安装库的 normal/no-XWayland 探针均通过 socket-owned/null、unowned/null、同/子/孙 socket、其它 socket和同进程未包装 client 的 registry 路径；C/consumer、九项 gate 与当前协议/runtime 证据有效。

该 fix-1 候选的第 1、3 项完整产品验收当时不满足：正常 102/100/1/1、关闭 100/98/1/1，唯一失败均为后续 `inactive upsert followed by unbind leaves no stale binding`。这是不同于原判空崩溃的新失败，不能把探针 PASS 当成整个 Session 测试 PASS，也不修改上面的验收标准。所有本批 refs、原 WIP、原来源/失败材料保留；未 CAS 或 `finish`。

## 9. 已批准：快捷键解绑残留项的独立修复

### 问题、原因与影响

原 Session-isolation 客户端让后台 B 将 F10 同 key/action 的绑定改名为 `renamed` 后解绑，随后要求 A 的 F9 仍有效而 B 的 F10 不再匹配。两配置日志均实际越过判空和前面的隔离检查，在此原断言失败。

`ShortcutController::registerKey()` 的 deleter 只移除内层 action，留下空的外层 `m_keyMap[combined]`；`unregisterShortcut()` 调用它之后，`matchesShortcut()` 只检查外层 key 是否存在，因而仍报告匹配。该实现与原测试均与冻结来源终点逐字节一致，不是本地调用方/冲突适配写错；未运行纯 Treeland，不宣称其 CI 已复现。后续窗口、三屏与切换断言还未运行到，不能宣称全套隔离通过。

### 用户明确批准的范围

用户本轮明确批准按本节另作独立修复提交，仅清理最后一个 action 解绑后的空 key，保留同 key 的其它 action 和原测试断言。该授权不批准重写之前判空提交、修改协议或额外生产行为。

- 仅修正 P `compositor/src/modules/shortcut/shortcutcontroller.cpp` 的 key 解绑索引清理：移除最后一个 action 时移除空的外层 key；同 key 仍有其它 action 时必须保留它们。不顺手改手势、协议 wire、action 路由或接口；不删改原 Session-isolation 断言。
- 修复另作独立提交和同批说明，不混入、amend 或覆盖已经冻结的判空 C/P 提交。保留已有 C 判空提交、R、XML/provenance、公共包合同、WIP 与全部失败证据。
- 当前 `record_local_fix.py` 明确拒绝给已有 `local_fix` 的 manifest 再嵌套修复。先核实并明确新的记录方式：保留原 C/P 判空记录，P 窄修另记显式相邻尾部提交；不得伪造 C 内容提交、修改已有来源/修复身份或重绑定旧 PASS。必要的记录能力限于本批私有工具副本，不修改日常 P/C 源码树的同步工具。

### 可独立判断的验收条件

1. 最后一个 key/action 解绑后不再匹配；同 key 的其它 action 不受影响，重复/未知解绑及清空后不留下空 key 的误匹配。
2. 保留原断言，两配置完整 `test_session_isolation` 真实通过；完整、未过滤 compositor CTest 无其它失败或跳过，仅 §6 原 `test_drm` 真实 SKIP 可限定接受。
3. 新候选保留本批 65 来源及判空独立修复的完整追溯；本次新结果使用实际候选 fresh 验证，原失败和旧报告保持原样。全部验收满足后才按既有授权 CAS 与 `finish`。

本节授权已实施为独立 P `bf2b6c2395275e74703933d9296640de26968631`。其原 fix-2 候选仍因后续桌面归属检查失败而保持 blocked；当前 fix-3 的原 Session 全流程及快捷键五组边界两配置均通过，不将后续成功改写到旧报告。实际收尾遵循 [实施方案](plan.md)，不能仅因修复已提交提前 CAS 或 `finish`。

## 10. 已批准：DockPreviewSurface 桌面归属独立修复

### 问题与目标

`N11-local-fix-2` 两配置都已越过原判空和快捷键断言，在桌面对象归属检查失败。原 fixture 要求 `viewRoot()->childItems()` 中每个直接视觉子项的 `desktop` 指针等于所属 DesktopEnvironment；DockPreview 控制器满足条件，作为其视觉兄弟的 DockPreviewSurface 只有 `preview` 属性。真实 GDB 观察确认面板的 `property("desktop")` 返回无效 QVariant，转换后为 null；没有证据表明发生跨用户桌面泄漏。

该检查来自 `f3e6d407f58f84ecf884d08653d5f8db1b31caac`；桌面组装和控制器依赖注入来自 `b6b80c3ef7e693cc596658d5e1f428c1aeacf144`，面板拆分及视觉兄弟结构来自已在基线内的 `4abd1b9a1d30a79dee6d98951cfb0a4836952cce`。因果文件与冻结来源相同或仅项目 QML URI 不同，归因限于来源代码/测试合同，不宣称运行了纯 Treeland CI。

### 用户明确批准的范围与交付

用户明确要求按已讨论方案执行修复，并要求此项独立修复使用单独 commit、保留独立文档，文档位于 `docs/treeland-sync/` 对应目录。

- 面板显式暴露只读、强类型 DesktopEnvironment 属性，绑定已有 `preview.desktop`；不允许调用方单独覆写为另一份桌面状态。
- 保留原 Session-isolation 源码和断言、`preview` 的 QtObject 类型、视觉 parent、动画、输入处理及现有鼠标事件路由。不跳过缺属性对象，不增加全局桌面回退。
- 生产改动仅 P `compositor/src/core/qml/DockPreview/DockPreviewSurface.qml` 一处属性。与独立说明 `docs/treeland-sync/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/dock-preview-desktop-ownership-fix.md` 放入一个新的相邻 P commit。
- 直接父为冻结 `bf2b6c2395275e74703933d9296640de26968631`；保留判空 P `da94bafea5d130bdee98e2c7854e2b352c7d5224`、C `780ae6e53d52483d17f14d40fa44c8d67d5874fc`。不 amend、不伪造 C/R 提交、不改变两层 gitlink、65 来源映射、协议和包合同。
- 新隔离候选及追溯单独记录，旧候选、原失败和旧验证原样保留。记录工具必要适配限定本批私有副本，不修改主 P/C 工具。

### 可独立判断的验收条件

1. 新候选 QML 编译和真实组件创建成功；原测试能读取面板的 DesktopEnvironment 指针，且它与 preview 及所属桌面一致。
2. 原正常/关闭 XWayland 的 Session-isolation 测试保持完整，越过当前断言并执行其后续场景；任何新失败继续阻断整批接受，不扩展本修复范围。
3. 生产 diff 只有一行绑定，独立提交恰含该 QML 和上述独立文档；测试字节、历史修复、C/R/gitlink 不变。
4. 新候选按原流程 fresh 验证完整两配置及依赖、安装、协议/runtime 和记录；旧 PASS 不换摘要复用。仅原获准的 DRM 前提不足 SKIP 可限定接受，全部条件满足后才能 CAS 与真实 `finish`。

