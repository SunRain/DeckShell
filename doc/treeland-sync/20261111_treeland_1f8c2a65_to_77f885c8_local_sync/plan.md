> 仓内参考副本；权威原文：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/plan.md`。
> 保留原同步方案的历史时点与验收边界；其中历史命令不是本次补档的执行指令。

---
verify:
  - git -C worktrees/N11-local-fix-3/parent diff --check
  - git -C worktrees/N11-local-fix-3/child diff --check
  - git -C worktrees/N11-local-fix-3/wlroots diff --check
---

# Treeland 1f8c2a65 → 77f885c8 实施方案

实施本轮已批准的 [PRD](prd.md) §3–§5。批次 `20261111_treeland_1f8c2a65_to_77f885c8_local_sync`，唯一验收节点 N11，完整来源 `(1f8c2a658b4b4e868e0650f9890c5e752fd1b839..77f885c8dbeb0e0e0bebdafdee02eadb1d150439]`。source tip 固定为右端 SHA，不包含当前 remote tip 后续两个提交。批准完整重构和必要调用方迁移；包名、namespace、安装布局、已接受 XML 和 WIP 保持不变。

## 最终候选验证与限定接受

当前候选为 `N11-local-fix-3`：P `b72a24a5688a6b02f67ededbb4483f0748938f28`、C `780ae6e53d52483d17f14d40fa44c8d67d5874fc`、R `b79b9b38a473ca57f5b54892280dfad4f25f8e42`；manifest（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/manifest.json`；未随仓携带） canonical SHA-256 为 `2ed345ba8b6048e3129a0cac3fba3cda192a68c751ac3fac5fa939949fdd33e6`。65 来源及三项独立修复分别追溯，旧候选与失败材料保持原样；下文 fix-1/fix-2 小节是历史结果，不代表当前仍失败。

| 当前实际验证 | 结果与证据 |
|---|---|
| P 正常配置默认完整 build / 未过滤 compositor CTest | build 成功；**102 total / 101 passed / 0 failed / 1 skipped**，CTest exit 0 |
| P 关闭 XWayland 默认完整 build / 未过滤 compositor CTest | build 成功；**100 total / 99 passed / 0 failed / 1 skipped**，CTest exit 0 |
| 原 Session-isolation | 两配置完整通过，各 **3 passed / 0 failed / 0 skipped**；原 fixture、C 客户端和 header 字节不变，包含桌面、窗口、三屏及切换后续断言 |
| R base/candidate | configure / build 成功；原生测试各真实 `NO_TESTS`，不称测试通过 |
| C base / 正常 candidate / 关闭 candidate | fresh configure、默认完整 build、完整 unstripped install 成功；CTest 各 **15/15**；两个 installed consumer 各 **9/9** |
| 完整安装合同 audit / namespace | 精确六头迁移，82 原绑定保留；候选 **88 个独立 installed-header 编译通过** |
| 所有权 / 快捷键五边界 / remote interaction 与 grab 状态 | 两配置当前真实库检查均通过；probe build/log 独立生成，不复用旧 PASS |
| 协议配套 / runtime | 当前 19 个输入 Git/blob 核验；`protocol-verify` 实际 exit 0、`pass / paired`；当前 manifest、两配置实际 binary、每配置六份 DSG 和私有 DConfig 日志绑定完整 |
| 关闭配置实际安装库消费 | 当前 C/R ELF 与 install 链核验，191 个 R 编译单元、89 个实际 installed R headers 及 C 生成协议头消费有效，无系统 wlroots 或源码/build header 回退 |
| 顶层注册覆盖 | 两配置真实 discovery 102/100，与已执行 compositor suite 的名称、命令、properties 完全相同；复用这次已完成运行，不将 discovery 说成新 runtime PASS |
| 私有记录工具 | finish/tail 受影响回归 **63 项通过**；限定接受及原 exception 回归 **17 项通过**，新增 installed-linkage guard **10 项通过**；synthetic 工具测试不是产品 finish |

原 strict 报告（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/sync-report.md`；未随仓携带） 实际生成 exit 2 / `blocked`，九项 gate 均 pass，只有原 DRM SKIP 对应的三条阻断。两配置保留 `test_drm` 原客户端退出 77、`wl_drm unavailable`、完整日志及 strict recorder `fail`；没有强制 SKIP、过滤、修改测试或 GPU 实验。

限定接受报告（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/sync-report-accepted.md`；未随仓携带） 已真实生成 exit 0 / `pass`，仅按本轮授权解除上述 DRM 前提不足的阻断。正常和关闭配置各有独立授权，精确绑定当前 manifest、候选、attempt、原日志及完整 discovery；原 strict 报告与两份 validation bundle 的字节核对未变。runtime（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/runtime-provenance.json`；未随仓携带）、关闭配置消费链（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/no-xwayland-installed-linkage.json`；未随仓携带） 与全部补充证据均未获豁免。

DRM/GPU 行为、连续 pointer/touch 序列、真实 XWayland 双进程及注销压力未被这些观察证明。日志中的 SourceOutput null-visible、webp 与 X11 socket 警告保留，未导致本轮测试失败，不宣称已经修复。

当前 build/install 根和 fresh driver 已执行完毕，禁止以头部命令或历史小节重启拒绝旧根的 fresh 验证。头部只保留当前源码的只读 diff 检查；真实验证结果使用本候选已经生成的不可变日志及 bundle。

## 本地收口与记录交付

真实 closeout（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/closeout-command.json`；未随仓携带） 已执行 **exit 0**，journal（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/closeout-journal.json`；未随仓携带） 为 `pass`，顺序为 R unchanged → C complete → P complete：

- P 本批专用 ref → `b72a24a5688a6b02f67ededbb4483f0748938f28`；C 本批专用 ref → `780ae6e53d52483d17f14d40fa44c8d67d5874fc`；R 本批专用 ref → 原 `b79b9b38a473ca57f5b54892280dfad4f25f8e42`。
- 主 P 已在相同旧 `1352256db1ea38476cf5e86b169bc3dd61822ad7` 安全 detach。五份 WIP 原文件字节及 patch SHA-256 `4158c32f2830157dd3c1f48fbe67890920c90b07542de7bef928cca6669af889` 未变；P index entries 未变。
- 外层 index SHA-256 仍为 `53fde58034db3773798a87a522582852b47c70fb0409fc6ca6047b331adca2c5`。日常 P `master` / C `waylibshared` / R `master-merge-treeland`、其它 refs、主 checkout HEAD 和外层已有文件未变，保护核对（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/closeout-protection-after.json`；未随仓携带） 为 pass。
- journal 只绑定当前限定接受报告；跨仓不原子、不自动回滚，没有提交生成文档、归并日常分支或远程发布。

整批记录使用本批私有 `unified_sync.py finish --task sync`，source-base/head 为本批完整 65 来源区间，evidence-root/plan-dir 均为原本方案根。命令及实际结果定位 finish-command（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/finish-command.json`；未随仓携带） / finish 输出（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/finish.log`；未随仓携带），不以 synthetic 工具测试或产品接受代替真实 exit 0。P 的 `doc/treeland-sync/`、C 的 `docs/treeland-sync/` 完整记录按原 Git 对象展开三项独立修复，保留 P 新修复的复数 `docs/` 说明和旧快捷键 `doc/` 说明，不自动暂存或提交。

`finish` 复制的是这一收口时点的 plan/prd 参考文本；完成输出及随后记录核对作为该次调用结果留在原 evidence，既有副本不得被后来改写的文本覆盖。

## 冻结基线与目标

| 仓库 | 初始提交 | 本批目标 ref |
|---|---|---|
| P DeckShell | `1352256db1ea38476cf5e86b169bc3dd61822ad7` | `refs/heads/master-merge-to-20261111-77f885c8dbeb0e0e0bebdafdee02eadb1d150439` |
| C waylib-shared | `a56cf9dcf7494db7266e9c5d407f170861d839e7` | `refs/heads/waylibshared-merge-to-20261111-77f885c8` |
| R wlroots | `b79b9b38a473ca57f5b54892280dfad4f25f8e42` | `refs/heads/master-merge-treeland-to-20261111-77f885c8` |

两层 gitlink 是 mode 160000，与初始提交一致。R URL 沿用 `https://github.com/SunRain/waylib-wlroots.git`。本批 R 无内容更新，但 R 已登记，仍须校验来源基线投影、两处既有本地差异和真实依赖。

XML repo 为外层 `treeland-protocols/`，base=head=`578263755cb80b56f2e13fde34da1c294418e608`，路径 `wine/treeland-remote-subsurface-unstable-v1.xml`。批准前的拟议 selection/inspection 不改写；正式输入绑定本轮批准。

## 工作树与执行安排

1. 复核 统一 inventory（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/preflight/inventory.json`；未随仓携带）：65 个提交、52 P-only、10 C-only、3 dual，0 merge/unknown/review-only。保留主 P 的 5 个 WIP 和外层 index，不把排版修改纳入来源映射。
2. 在 `worktrees/preview-1/{parent,child,wlroots}` 建立 linked worktrees；对每个来源只按统一 inventory 投影，保留 DeckShell 包名、QML URI、DDM 和已有回归保障。已有可靠的三路 merge helper 只作为库复用，不执行旧批次调度器。
3. 逐节点记录目标相对补丁和每个路径的取舍；必要测试/consumer 调用方通过精确 `contract_migration` 绑定来源、相邻 C 源码快照和真实 drift。唯一预期安装扩展为 PRD 六个输入法 manager 头及确实必要依赖；未知漂移仍阻断。冲突保留三侧输入，审核后继续，不 reset/abort。
4. 在 `evidence/N11-attempt-1/` 冻结 decisions、R 基线证明和 protocol-update；`Refs:` 为 `.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/plan.md`。建立同名正式 linked worktrees，使用统一 replay 创建完整来源映射及协议 companion。不复用旧 journal，冻结后变化使用新 attempt。
5. 独立 P/C/R verify、两层 gitlink、advisory 和递归 materialization；物化 C base/candidate 与 P 内真实 C/R。构建和安装全部位于对应 evidence 目录，与源码工作树分开。
6. 复用已核实的 N10 Qt 6.11.2 / Dtk 隔离工具链和 DConfig 包材料，以只读 overlay 和本批可写目录运行。记录实际使用路径与来源，fresh 构建/安装，绝不复用旧候选 PASS。当前磁盘约 45 GiB 可用、内存压力较高，构建先采用低并行，不自动清理历史材料。
7. 运行技能所有固定 validation IDs：R base/candidate Meson，C base/candidate 完整 build/install/CTest、现有 installed consumer、P 正常完整 build/CTest；补充关闭 XWayland C/P 完整回归。新 session-isolation 必须真实执行，运行依赖不足不能写 PASS。重点核对多用户模型/协议域、输入交接、共享显示、后台展示恢复，以及终点 revert 的注销生命周期。
8. fresh 安装审计生成精确安装迁移审批，保留真实 drift。remote-subsurface 使用本批真实交互和客户端审查生成 protocol-verify，随后生成九项 gate 和 N11 完整报告。
9. 本轮只接受 `test_drm` 因原运行前提不足的真实 SKIP；保留原 recorder FAIL/SKIP，复用经过审阅的限定接受逻辑时绑定新 manifest、完整发现、实际 attempt 和日志，不覆盖任何其它失败/跳过。正常和关闭配置分别验明，不继承旧实例授权。
10. 完整报告通过后，在主 P 相同初始 HEAD 安全 detach 并核对 WIP 字节不变，目标 ref 无 worktree 检出后 R→C→P expected-old CAS。日常 refs、外层 index 与 remote 不动。最后 `finish --task sync` 按整批范围自动交付并核对两仓记录，不自动提交记录。

## 失败与完成边界

保留全部 worktree、原始日志和失败证据。不得删除测试、放松断言、强制 SKIP 或在失败后改写冻结 identity。允许已批准重构的必要本地调用方迁移；独立生产缺陷或超出六头/API语义的公共漂移另行说明和取得对应授权。

完成须完整 65 来源映射、当前节点真实验证、限定 DRM SKIP、九项 gate、实际 closeout 和 `finish` 都有效。产品接受与记录交付分开，未通过部分不宣称完成。

## N11 原来源候选与判空授权起点

原来源候选为 N11-attempt-3 manifest（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-attempt-3/manifest.json`；未随仓携带）：P `ac8f4b1928105fdcfc809c8cf11cbe65c12ecccd`、C `a0f86a62a8cf3038e306ce191f5ded1a09b58fed`、R 仍为初始 `b79b9b38a473ca57f5b54892280dfad4f25f8e42`。完整 65 来源和协议 companion 已独立验证；来源适配冻结自 `preview-4`，旧 attempts、journal、失败日志均保留。当前派生候选为下一节的 `N11-local-fix-1`，以下表格仅记录未判空的原候选，不挪用为派生候选的 PASS。

| 原来源候选验证 | 实际结果 |
|---|---|
| R base/candidate configure、完整 build | 均通过；原生测试各真实 `NO_TESTS`，不称测试通过 |
| C base/candidate 默认完整 build/install/CTest | 均通过，各 15/15；installed consumer 9/9 |
| no-XWayland C 默认完整 build/install/CTest、consumer | 通过，15/15 和 9/9 |
| P 正常默认完整 build、完整 compositor CTest | build 通过；102 total / 100 passed / 1 failed / 1 skipped |
| P no-XWayland 默认完整 build、完整 compositor CTest | build 通过；100 total / 98 passed / 1 failed / 1 skipped |
| 实际安装合同、固定 namespace 逐头编译 | 通过；仅获批六头增量，保留原 82 项 namespace bindings，候选 88 项独立编译 |
| remote-subsurface 配套、自然协议子目录、grab 状态探针 | pairing 通过；两配置子目录和本候选 fresh installed-library 状态探针各 1/1；不证明持续拖放输入或 GPU |

两配置唯一失败均为 `test_session_isolation`：现有断言调用 `ownsClient(nullptr)`，`WClient::socket()` 在地址 `0x18` 解引用后 SIGSEGV。唯一 SKIP 均为获准原 `test_drm` 缺 DRM renderer，原 recorder `FAIL/SKIP` 不改写。no-XWayland 新增三个 QML 失败已由 `241cff919d3972a88d6e2ce4267ac314053b0c63` 阶段的精确类型适配消除；仍保留 X Shape 掩码语义，不提前混入后续 `overrideCursor` 来源。

用户现已明确批准 [PRD §8](prd.md#8-已批准socket-owned-空客户端独立修复)：仅 C `waylib/src/server/kernel/wserver.cpp` 在无 socket 早退之后拒绝空 client，保留 unowned/globalFilter 例外和非空 socket 链。C 同一独立提交携带 `docs/treeland-sync/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/null-client-ownership-fix.md`；P 另作相邻提交，仅传播 C gitlink。按 `references/local-fixes.md` 从本来源候选新建 `worktrees/N11-local-fix-1/{parent,child,wlroots}`，生成精确 approval、派生 manifest 和 fresh 全部验证，不改原 manifest/journal/失败材料，不伪造来源提交。

在该判空授权起点，本批目标 refs 仍是表中初始 SHA，主 P WIP 逐字节核对一致，尚未 detach、CAS 或执行 `finish`。判空不置于函数入口：那会扩大为未绑定 socket 也拒绝空客户端，改变现有同进程未包装 client 的全局接口例外。补充 artifact-only 安装库检查覆盖这项保留行为及真实 socket/parentSocket 链，原 Session-isolation 断言保持不变。

原严格报告（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-attempt-3/sync-report.md`；未随仓携带） 已生成并核对，结果为 `blocked`：九项结构化 gate 均通过，完整 compositor 的实际失败和 SKIP 仍阻断产品接受，未生成限定接受报告。完整原日志、验证 bundle 和 runtime 记录均在 N11-attempt-3 evidence（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-attempt-3`；未随仓携带）；DConfig 使用可信只读包和该候选 DSG，服务就绪检查仍在 `preInit/postInit` 后，不声称启动前诊断已修复。旧探针静态/LSP 证据仅对应其实际 source 和 CDB，不能替代当前候选验证或称 pi-lens 已刷新。

## N11-local-fix-1 历史实际结果

已按 §8 授权创建 C/P 各一个相邻非 merge 提交，独立说明随 C 保存：

- C `780ae6e53d52483d17f14d40fa44c8d67d5874fc`，仅 `wserver.cpp` 三行判空和同批 `null-client-ownership-fix.md`。
- P `da94bafea5d130bdee98e2c7854e2b352c7d5224`，仅传播 C gitlink；R 不变。
- 派生 manifest（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-1/manifest.json`；未随仓携带） canonical SHA-256 为 `2b5499409ddab0db81192e1dab8883e9e26386420cad06760146b6416fe26b6b`。保留原 65 entries、原来源 run-id、协议 companion 和失败材料，不复制旧 build/install/validation PASS。

| 当前派生候选 fresh 验证 | 实际结果 |
|---|---|
| R base/candidate | configure、完整 build 通过；原生测试各真实 `NO_TESTS` |
| C base/candidate 正常及 C 关闭 XWayland | 默认完整 build/install/CTest 全部通过，各 15/15 |
| 两配置 installed consumer | 各 9/9 |
| 两配置 P 默认完整 build | 均通过 |
| 正常完整 compositor CTest | **102 total / 100 passed / 1 failed / 1 skipped**；exit 8 |
| 关闭 XWayland 完整 compositor CTest | **100 total / 98 passed / 1 failed / 1 skipped**；exit 8 |
| 所有权安装库 probe | 两配置各 1/1，QtTest 各 4 passed / 0 failed / 0 skipped |
| remote-subsurface 自然子目录和 fresh grab probe | 两配置各 1/1；配套重新核验通过 |
| 实际安装合同、来源/追溯、两层 gitlink、R、物化等九项 gate | 全部 pass；仅批准六头增量，原 82 namespace 绑定保持、候选 88 项独立编译通过 |

原 null-client SIGSEGV 已消失。两配置现在都在原 `inactive upsert followed by unbind leaves no stale binding` 断言失败：后台 B 改名后解绑 F10，deleter 只移除内层 action，`matchesShortcut()` 仍将残留的空外层 key 视为匹配。该实现及测试与冻结来源终点逐字节一致。未独立运行纯 Treeland，不声称其 CI 已复现；该断言后的完整 Session 场景尚未运行到。

当前严格报告（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-1/sync-report.md`；未随仓携带） 由工具生成并重新核验当前候选及原始编译/链接/安装证据，结果仍为 **blocked**。详细 实际验证与阻断说明（外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-1/local-fix-validation.md`；未随仓携带） 保留 probe 首次错误前提、原失败日志及更正后的实际通过；独立 current-source 正确 CDB/LSP 发布零诊断，pi-lens 9 项 fallback findings 按证据标记误报，不声称其缓存已刷新。runtime 使用本次 DSG 和私有 D-Bus，实际观察 Session-isolation global/user 初始化，不声称启动前 readiness 已修。

该候选的 fresh 验证命令已实际执行；已有 build/install/probe 目录不可作为全新验收再次运行，脚本按约定拒绝重用。normal probe 首次前提错误后的 retry 只重新执行原 recorder 的 build/test，保留 attempt-1；当前 source 的 CDB 检查另行记录，不伪称首次全程通过。

用户现已明确批准 [PRD §9](prd.md#9-已批准快捷键解绑残留项的独立修复) 的精确范围及独立提交，授权缺口解除。原判空 C/P 提交和本目录失败材料不修改；完整验收仍按原标准判断，原断言不放宽。本批 refs 仍在初始 SHA、主 P 五份 WIP 字节不变；未生成限定接受、主 P detach、CAS、两仓整批 `finish` 记录或远程发布。

## 已批准 §9 的接续实施

1. 新建 `worktrees/N11-local-fix-2/{parent,child,wlroots}` detached linked worktrees，P 起点 `da94bafea5d130bdee98e2c7854e2b352c7d5224`，C 保持 `780ae6e53d52483d17f14d40fa44c8d67d5874fc`、R 保持原 SHA。只在新 P 的 `compositor/src/modules/shortcut/shortcutcontroller.cpp` key deleter 中移除最后 action 后清理空外层 key；同 key 其它 action 保留，原匹配/手势/协议路径不改。
2. 独立 P 提交同时保存 `doc/treeland-sync/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/shortcut-empty-key-fix.md`。不改、amend、重建之前的 C/P 判空提交，不制造 C 内容提交。用真实生产控制器的 artifact-only 边界 probe 覆盖最后解绑、同 key 多 action、改名、重复/未知解绑和 clear；原 Session-isolation 客户端保持原 bytes。
3. 当前正式工具只能记录单次相邻 P/C local_fix，不能表达在已有修复后再增加 P-only 提交。因此本批复制一份显式私有工具到 `scripts/tooling-parent-tail/`，仅增加 `parent_tail_repair`：单个相邻、精确批准的 P 尾部提交，独立绑定原 local-fix manifest/approval/diff，保持原 `local_fix` 对象原样。源码/协议/gitlink/报告及 finish 都实际复核该尾部；不改主 P 的同步技能、不嵌套 local_fix、不扩大来源 owner、也不手写 PASS。
4. 新 artifact root `evidence/N11-local-fix-2/` 仅复制经内容核对的不可变来源/修复工件。所有 validation/build/install、安装审计、协议/runtime 结果和报告重新真实执行，低并行 2；原失败和所有历史材料不清理。
5. 当前候选完整正常/关闭 suite 和全部原 gate 通过，且仅有已授权原 DRM 真实 SKIP 时，才制作精确限定接受、复核 WIP/外层 index、安全释放目标 P ref，执行已有授权的 R→C→P CAS 与 `finish --task sync`。发现其它独立缺陷仅留证，不擅自扩大 §9。

## 已批准 §10：DockPreviewSurface 桌面归属修复

`N11-local-fix-2` 完整两配置 build 通过，suite 为正常 102/100/1/1、关闭 100/98/1/1；快捷键原断言及补充五组边界通过。新的唯一失败已由只读 GDB 精确归因于 DockPreviewSurface 未声明直接 desktop 属性。原 source/测试/运行观测保存在该候选的 `session-model-diagnosis/`，原候选维持未接受。

1. 新建 `worktrees/N11-local-fix-3/{parent,child,wlroots,child-base,wlroots-base}`，P 从 `bf2b6c2395275e74703933d9296640de26968631` detached 建立，其余使用既有冻结 SHA；旧工作树和验证目录不改。核对主P五份WIP、外层index和本批refs仍与预检相符。
2. 只在 `DockPreviewSurface.qml` 的 required preview 后添加 `readonly property DesktopEnvironment desktop: preview.desktop`。保持原 fixture/客户端字节和其它生产路径。按用户指定的复数目录保存独立说明 `docs/treeland-sync/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/dock-preview-desktop-ownership-fix.md`，与一行代码同作独立P提交；标识 `N11-dock-preview-desktop-ownership-1`，不冒充来源或协议提交。
3. 在新的本批私有工具副本 `scripts/tooling-desktop-tail/` 中接入精确的桌面归属尾部记录；保留原 `local_fix` 和 `parent_tail_repair` 全对象、原manifest/diff/授权及65来源。验证实际相邻提交、两条精确路径、未变gitlink和消息；独立文档按已验证Git普通blob保留，最终记录单列该提交，不放行任意手写文件。
4. 新 evidence 根为 `evidence/N11-local-fix-3/`，只复制核验过的不可变来源输入；所有构建、安装、运行结果和接受证据重新生成。并行度2，使用既有只读Qt/Dtk工具链、私有D-Bus及当前候选DSG。
5. 先确认原 Session-isolation 能越过 desktop 检查并完整运行，再完成正常/关闭两配置完整suite及既有独立gate。出现新失败则保留真实日志、只读定位，不顺手扩大生产补丁。只有全部原验收满足才按已授权流程接受及finish；独立提交本身不代表整批通过。

