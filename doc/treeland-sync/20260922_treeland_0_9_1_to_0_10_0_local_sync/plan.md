> 仓内参考副本；权威原文：`外层工作区（历史）/.helloagents/archive/2026-09/20260922_treeland_0_9_1_to_0_10_0_local_sync/plan.md`。
> 保留原同步方案的历史时点与验收边界；其中历史命令不是本次补档的执行指令。

# Treeland 0.9.1 → 0.10.0 本地实施

本文件落实 [PRD](prd.md)，不替代节点报告或收口记录。

## 完成结论（2026-09-27）

**本批本地同步已全部完成。** N8a 的 26 个来源提交与 N8b 的 15 个来源提交连续覆盖
冻结范围，两段各自通过验收并完成 R→C→P 收口，没有用末节点结果代替前节点。
恢复 session `01a0e21e-037b-7cd3-9ea3-996d4ace7f24` 后，本轮已核对真实 Git 对象、
原始报告及收口绑定、九项 gate、协议配对和干净隔离候选；不再次 replay 或移动产品 refs。

| 层 | 已收口目标 ref | 当前接受的完整 SHA |
|---|---|---|
| P | `refs/heads/master-merge` | `bee3531566e9d325e8d89db1ad124759033d7bc2` |
| C | `refs/heads/waylibshared-merge` | `d0344634c057b8c29ac2e138a935e5c80a89b768` |
| R | `refs/heads/master-merge-treeland-new` | `005b8c571c002d266ffdd560b7eb4e3bd46c4e3a` |

- N8a 的授权后报告（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/sync-report-authorized.md`；未随仓携带）与
  closeout（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/closeout-journal.json`；未随仓携带）仍有效；N8b 的
  最终可读报告（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/sync-report-final.md`；未随仓携带）复用相同候选及原始证据重新生成，
  仅修正例外说明中误写的节点名。原始报告（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/sync-report.json`；未随仓携带）与
  closeout（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/closeout-journal.json`；未随仓携带）按原字节保留，后者仍绑定原报告；
  最终报告不构成第二次收口，也没有改变判定或授权范围。
- 两段 P 完整 CTest 均为 66 项发现、65 passed、唯一 `test_drm` skipped、0 failed、
  exit 0，分别按 PRD §5.5、§5.6 接受限定例外；DRM/GPU 行为没有因此被证明通过。
  N8a C base/candidate 均为 11/11；N8b C base 为 11/11、candidate 为 12/12；
  两段 installed-only consumer 均为 9/9。R 两段的 base/candidate 均完成原生配置与
  构建，零注册测试如实为 `NO_TESTS`，不是测试 PASS 或 `NOT_APPLICABLE`。
- 上一 session 在完整工具回归中被中断，
  原日志（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/tool-tests-interrupted-20260927.log`；未随仓携带）已保留。
  两行报告措辞修正独立提交为 `a5c51adb4`，位于 `worktrees/N8b-exception-tooling`；
  本轮完整回归（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/tool-tests-final-20260927.log`；未随仓携带）原始结尾为
  `Ran 331 tests in 107.483s`、`OK`，进程 exit 0。未改产品代码或通用 SKIP 判定。
- 原 C/R 分支、主 DeckShell 工作区的既有 WIP 和外层暂存 gitlink 保留；未执行
  fetch、push、tag。主工作区仍是原 `9d14efb...` 的 detached checkout，不把它冒充为
  最新已接受候选；最终产品在上述目标 refs 和对应隔离 worktree 中。

方案正文 `plan.md`、`prd.md` 按约定归档至
`.helloagents/archive/2026-09/20260922_treeland_0_9_1_to_0_10_0_local_sync/`。
原始证据、构建/安装目录和 linked worktree 保持在
`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/`，不破坏 manifest、
CTest 命令和收口报告中的绝对路径绑定。下文代码形式的 `evidence/`、`worktrees/`
仍相对于这一原始目录；可点击链接已随正文归档调整。

## 固定边界

- 来源 tip：`c0d4bc214d4636aa4e2fa8557927a560190b7411`。
- 总范围：`(fd573cf44fb06ee1eebcdd8c39716d1c797b64d4..3a100f265970cb6acf9addf07e5c297aab9e9839]`。
- P：`master-merge`，初始 `9d14efb18d1d2413376e4369461a3e11f7d44689`。
- C：新建 `waylibshared-merge`，初始 `f14d7cdf718307945f492eb1c6d7608413e83c29`；原 `waylibshared` 不动。
- R：新建 `master-merge-treeland-new`，初始 `005b8c571c002d266ffdd560b7eb4e3bd46c4e3a`；原 `master-merge-treeland` 不动。
- remote-subsurface XML：N8a 从 `8dc1d1e788dc964cd0f756b4491d0225e70b1598:xml/treeland-remote-subsurface-unstable-v1.xml` 迁移到 `284e3aac8a1ed5ece66c4cb248e8b24d33cb25a0:wine/treeland-remote-subsurface-unstable-v1.xml`；N8b 沿用后者。
- 其它协议仅按 PRD §5.3.1 的精确来源与清单迁移；不整包覆盖，不增兼容别名或 fallback。
- 不 fetch/push/tag，不改外层 gitlink、子模块配置或未授权的公共合同，不清理旧现场。

## 节点和证据

| 节点 | 来源范围（左开右闭） | 正式证据 | 隔离源码 |
|---|---|---|---|
| N8a | `fd573cf44fb06ee1eebcdd8c39716d1c797b64d4..a5656ab80ae11a0068d507659f35bb999b6d815d` | `evidence/N8a-attempt-8/` | `worktrees/N8a-attempt-8/{parent,child,wlroots}` |
| N8b | `a5656ab80ae11a0068d507659f35bb999b6d815d..3a100f265970cb6acf9addf07e5c297aab9e9839` | `evidence/N8b-attempt-8/`；此前 attempt 均保留 | `worktrees/N8b-attempt-8/{parent,child,wlroots}` |

N8a 首次回放的第三个来源在本地 CMake 上下文冲突，原现场保留。
复核后的五项 P 适配使用 `evidence/N8a-attempt-2/decisions.json`；新回放位于
`worktrees/N8a-attempt-2/{parent,child,wlroots}`，正式证据位于
`evidence/N8a-attempt-2/`，来源范围、冻结基线和目标 ref 均不改变。

首次实施冻结输入见 `evidence/preflight.json`。各段由统一入口生成一次 inventory；
N8b 预检不代表已启动回放。回放按 R → C → P，构建/安装目录放各段证据目录下，
不放源码内。适配仅限规范映射路径，补丁和逐路径审核使用既有 decisions schema。
未经 PRD §5.3.1 精确授权的公共合同漂移，以及范围或身份漂移均停止；保留真实失败工件，不自批额外迁移。

## 命令路线与验收

使用 `DeckShell/doc/skills/treeland-deckshell-waylib-unified-sync/scripts/` 的现有工具：

1. `unified_sync.py inventory`、`protocol-inspect`，核对来源拓扑、路径和已接受配对。
2. 创建未检出的 C/R 目标 ref 与独立 detached linked worktree；`replay` 使用冻结输入。
3. 运行 P/C/R 内容验证、两层 gitlink 验证和协议 advisory；物化本段 C/R 消费链。
4. `validation_record.py` 记录本段 fresh C base/candidate 完整构建、安装、全量 CTest，
   安装包 consumer、固定基线 namespace probe、R base/candidate Meson 和 P 完整构建/CTest。
5. 协议交互审查、`protocol-verify`、安装合同审计和九项 gate 齐备后生成 `sync-report`。
6. 完整报告通过且获得该段收口授权后，先将干净 P 主工作区保持在原 SHA 的 detached
   状态，核对目标 ref 均未检出，再执行 R → C → P expected-old CAS；不自动回滚。
7. N8b 只以 N8a 实际收口 SHA 为基线；两段均实际收口才能声明整批完成。

每段原始 `manifest.json`、`validations.json`、`sync-report.json` 和
`closeout-journal.json` 均在其证据目录。不存在或未通过的工件不视为验收完成。

## 历史阻断：attempt-2 的协议输入不匹配

第二次回放完成前 25 个来源的 P 映射，并创建 10 个 C 来源提交；第 26 个来源
`a5656ab80ae11a0068d507659f35bb999b6d815d` 的 C 提交已存在，但 P 补丁失败。
详见 真实 journal（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-2/journal.json`；未随仓携带） 和
回放错误原文（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-2/replay.log`；未随仓携带）。

- 当时隔离 P HEAD：`fd95b8e7d03773686517249708fab29e5c89a8d4`，其 C gitlink 为
  `1d1319c06e580eb081a8c78630e3761543d07721`，没有传播未配套的末端 C 提交。
- 当时隔离 C HEAD：`93637bd81b3ce5f5c37ecced617cd49a54ea3132`；R 仍为
  `005b8c571c002d266ffdd560b7eb4e3bd46c4e3a`。10 份逐提交源码合同审计均为
  `outcome: pass`、`drift: {}`；这不证明协议 wire 配套或产品可构建。
- `a5656ab...` 把 C 实现基类改为 `QtWaylandServer::treeland_remote_subsurface_manager_v1`。
  PRD 固定的 `8dc1d1e...` XML 仍定义 `treeland_subsurface_manager_v1`；真实运行
  `qtwaylandscanner server-header` 后也未生成新名称。
- 同一来源的 P 消费者要求 `treeland-app-id-resolver-unstable-v2.xml`、
  `treeland-prelaunch-splash-unstable-v2.xml`、`treeland-screensaver-unstable-v2.xml`，
  冻结 P 的受控协议目录中均不存在。只改 CMake 路径不能补足这些输入。
- 原始生成头、命令和 Git/XML 检查结果保存在
  protocol-blocker/diagnostic.json（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-2/protocol-blocker/diagnostic.json`；未随仓携带）
  及 diagnostic.log（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-2/protocol-blocker/diagnostic.log`；未随仓携带）。这是不匹配诊断，
  不是 `protocol-verify` 或真实交互 PASS，配套结论为“尚未适配”。

该失败发生在协议迁移授权之前。2026-09-23 用户已授权修订固定输入与范围，
PRD §5.3、§5.3.1 已落实新 XML 和精确迁移清单；不再把此历史缺口作为待授权项。
attempt-2 的原始错误、Git 对象和诊断保留，不能用后续成功覆盖或改写。

局部 Git 对象复核（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-2/partial-git-check.log`；未随仓携带） 确认已创建提交的
作者/日期、唯一来源 trailer 和已完成部分的两层 gitlink 链连续。C 的
`git diff --check` 为 0；P 为 2，报告 logging 文件末尾空行以及来源 README 的
两处 Markdown 行末双空格，未把它写成全部通过。

## N8a attempt-7 候选记录（历史）

以下记录 attempt-7 当时的恢复点和状态；当前候选及验收结果以本文件后续
“N8a attempt-8 正式验证与当前阻断”为准。attempt-7 的源码、manifest 和失败工件均保留。

当时根据 session `01a0ce13-1ba7-7a23-b2e4-cf029370e0ba` 和实际 Git 对象，
继续 attempt-7 manifest（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-7/manifest.json`；未随仓携带） 对应候选，不重放已经完成的 26 个来源。
先前 attempt 的 journal、适配及诊断工件保留，不把旧候选结果移作新候选证据。

- P：`0ba8ee8fb414e5711e4299d1142dc7d8276ed75c`。
- C：`0369fbcbfcf8c97573336e54d0cccc98b29f6a8f`。
- R：`005b8c571c002d266ffdd560b7eb4e3bd46c4e3a`，本段无来源内容变化。
- 基线验证源码位于 `worktrees/N8a-attempt-7/{child-base,wlroots-base}`；依赖物化见
  child-materialization.json（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-7/child-materialization.json`；未随仓携带）。
- attempt-7 保留本地 Helper 接口及 `DISABLE_DDM` 等条件分支，仅作来源要求的
  screensaver V1→V2 迁移，并修正 input-method、screensaver 模块和测试的规范路径。
  未纳入首帧初始化实验修复、临时渲染日志或延长 screencopy 等待的实验代码。

`master-merge`、`waylibshared-merge`、`master-merge-treeland-new` 仍为冻结基线，
原 C/R 分支和外层暂存 gitlink 未动。P 主工作区已有本批同步工具修订 WIP，保留不覆盖；
产品验证使用干净隔离候选。N8a 尚未收口，N8b 尚未开始；完整报告通过且取得覆盖
本段的收口授权后才执行 CAS，不能跨过当前阻断。

## N8a attempt-7 正式验证（历史 BLOCKED，2026-09-24）

本节是 attempt-7 的原始正式结果，不代表当前候选。attempt-8 已独立重验并修复首帧
初始化及安装包取证缺口；attempt-7 的失败记录仍作为历史证据保留。

完整结果由现有工具生成：sync-report.md（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-7/sync-report.md`；未随仓携带）、
sync-report.json（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-7/sync-report.json`；未随仓携带）。总体为 **BLOCKED**，
`build_scope` 为 `range-head-only`，绑定 `a5656ab80ae11a0068d507659f35bb999b6d815d`。
九项结构化 gate 均通过不等于节点通过：P 必需构建取证和全量 CTest 仍未满足。

validations.json（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-7/validations.json`；未随仓携带） 原样合并本候选的 20 条命令记录，
保留各记录的 `previous_attempts`。P 已有完整构建和 CTest 结果复用；本次补齐 C 基线、
consumer、R 两套原生验证、安装合同及协议配套，不借用其它 attempt 的 PASS。

| 检查 | 实际结果 | 证据与边界 |
|---|---|---|
| P/C/R 内容、两层 gitlink、协议 advisory、依赖物化 | PASS | 对应七项结构化结果均绑定 attempt-7 manifest |
| C base/candidate fresh configure、默认完整 build、install | PASS | 两套独立 `builds/waylib-*`、`installs/waylib-*`，未复用历史构建树 |
| C base/candidate 全量 CTest | 各 11/11，零失败、零跳过 | candidate 的沙箱连接失败保留为 attempt-1；沙箱外 attempt-2 通过 |
| 已安装 C 包的 `test_project` | configure/build PASS；CTest 9/9 | 仅连接 candidate install，覆盖 CMake/pkg-config/native/QML/协议生成及版本拒绝路径 |
| C 安装合同及固定基线 namespace 探针 | PASS，`drift: {}` | waylib-contract-audit.json（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-7/waylib-contract-audit.json`；未随仓携带） |
| R base/candidate 原生 Meson | setup/compile PASS；test 均 NO_TESTS | 两套 fresh build，真实发现集合均为 0；不是 NOT_APPLICABLE，也不写成测试 PASS |
| remote-subsurface 配套 | PASS，`direct-switch` | protocol-pairing.json（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-7/protocol-pairing.json`；未随仓携带）；重算来源范围，包含三个真实 socket 交互用例 |
| P 默认安装包路线 | configure exit 0；完整 build 883/883、exit 0；构建记录 FAIL | 取证器不识别 installed-package 路线，详见下述第 3 项 |
| P compositor 全量 CTest | 64 通过、1 失败、1 跳过，exit 8 | 原始日志（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-7/logs/deckshell-compositor-ctest-attempt-1.log`；未随仓携带）；未过滤测试或放宽断言 |

### 1. screencopy 首帧状态初始化缺陷

C 的 `waylib/src/server/qtquick/woutputhelper.cpp:92` 默认构造非空 `ExtraState`，
首次 commit 因此进入 state-only 分支，丢弃已经渲染的 buffer。该文件相对冻结 C 基线
没有变化，不属于 N8a inventory 或 PRD §5.3.1 的协议迁移授权路径。

正式候选失败原文：`events=(buffer=1 done=1 ready=0 failed=0 flags=0 ...)`。
上一 session 的隔离 A/B 证据仍有效：attempt-6 与 attempt-7 的 C 整树相同；将等待
延长到 5 秒仍失败，而只改变初始 `extraState` 是否为空这一功能变量后，未修改的
screencopy 客户端通过。诊断日志不是正式候选 PASS：

- 等待真实终态仍失败（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-6/diagnostic-waylib/screencopy-wait-terminal-fail.log`；未随仓携带）
- 空初始状态、原始客户端通过（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-6/diagnostic-waylib/screencopy-original-client-null-state-pass.log`；未随仓携带）

独立本地修复尚未纳入候选，须有范围外修复授权，不能夹入来源映射或协议配套提交。
历史实验补丁还包含观测日志，不能整包当作正式修复应用。

### 2. DRM 必测条件不满足

正式测试 fixture 使用 `pixman`，`test_drm` 返回跳过。上一 session 已在沙箱外用
GLES2 验证真实 NVIDIA render node；global、认证和非法请求拒绝可执行，但该主机
GBM 对 `XRGB8888 + RENDERING|LINEAR` 分配返回 `EINVAL`，DMA-BUF 像素读回仍不可验证。
这不是“主机没有 DRM 设备”，也不能靠强制 GLES2 就认定通过。

现有 GLES2 诊断日志（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-6/diagnostic-parent/drm-gles2-skip.log`；未随仓携带）
保留为环境诊断，不借作 attempt-7 验收。需要满足真实 DMA-BUF 分配/读回合同的执行
环境，再跑完整必需集合；不删除用例、伪造 buffer 或把 SKIP 改成 PASS。

### 3. 默认 installed-package 路线的取证器限制

P 的实际链接命令使用 attempt-7 安装目录下的 `libWaylibSharedServer.so.0.7.0`
和 `libwaylib-wlroots.so`，受控协议输入也未指向系统协议目录。
但现有 `wrapper_build.py` / `native_wrapper.py` 只接受 P 内嵌编译的 wrapper target，
因此 构建记录（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-7/validations-parent.json`；未随仓携带） 保留：
`CMake codemodel has no compiled wlroots wrapper target`，`exit_code: 0`、`outcome: fail`。

这是默认安装包消费链的正式取证缺口，不是 P 编译失败。未手改结果，也未用内嵌路线
替代默认路线制造 PASS。补足取证应绑定本次 C build/install 的 R 来源、安装产物、
P 实际头文件和链接输入；该工具维护与当前已授权的 XML 路径迁移维护分开确认。

### 协议测试运行依赖

P 正式 CTest 复用已经核验的本地 Arch `extra/deepin-app-services 1.0.45-1` x86_64
隔离包，来源及仓库校验依据见
dependency.json（外层历史资料：`外层工作区（历史）/.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-1/runtime-dependency/dependency.json`；未随仓携带）。
实际 daemon 为该记录的 `runtime-dependency/root/usr/bin/dde-dconfig-daemon`，仅把此
目录加入验证进程的 `PATH`；未安装或启用宿主服务。DSG 数据来自 attempt-7 P candidate
的 CMake 配置，Waylib 来自本次 candidate install，不使用诊断库替换正式动态库。
复用的是运行依赖，不是 N7 的测试结果；本节点记录和失败结果仍独立保存。

## N8a attempt-8 正式验证与 DRM 例外（2026-09-24 历史记录）

本节保留当时尚未收口的状态；后续实际接受结果见下方“N8a 已收口”和本文完成结论。

当前候选及原始报告： sync-report.md（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/sync-report.md`；未随仓携带）、
执行日志（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/execution-log.md`；未随仓携带）、
验证命令与 attempt 历史（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/validations.json`；未随仓携带）。该报告在本次 DRM
例外授权前由通用工具生成，结果为 **BLOCKED**；它绑定来源终点
`a5656ab80ae11a0068d507659f35bb999b6d815d`，最终候选为：

- P：`cb9c6bf6bbc4a53bc50212204f34ad0cd5308ffb`。
- C：`a2b1c5752afca1581a95a8bd8ac6d3dbe115b8e4`。
- R：`005b8c571c002d266ffdd560b7eb4e3bd46c4e3a`，与冻结基线一致。

### 用户授权的两项独立本地修复

用户在 session `01a0d124-ce74-7023-9068-d7bba1a2c919` 明确授权，并要求在执行日志中
着重注明：修复首帧 `extraState` 初始化，以及让同步取证器支持已安装 Waylib/wlroots
消费链。两项均为独立本地修复，不计入 26 个 Treeland 来源映射或协议配套，不改变
来源范围、Waylib 公共包合同、验收标准或 R 基线；不把 DRM 条件并入这两项修复。

- C 提交 `a2b1c5752afca1581a95a8bd8ac6d3dbe115b8e4` 将首帧初始 `extraState` 置空，
  避免首次输出提交误入 state-only 分支并丢弃已渲染 buffer；复用 screencopy 真交互回归。
- P 提交 `cb9c6bf6bbc4a53bc50212204f34ad0cd5308ffb` 为默认 installed-package 路线
  记录本轮 C 构建/安装 ELF、P 的真实链接输入，以及 R 来源和生成头依赖。该提交同时
  携带此前已授权的协议迁移工具 WIP；不把既有 WIP 表述为本次新增修复。
- 两个提交位于隔离的 attempt-8 候选；未移动目标 refs、未收口，也未覆盖 attempt-7
  的源码、失败日志或报告。

候选 worktree 均为 detached HEAD；目标 refs 仍指向冻结基线：P `master-merge` 为
`9d14efb18d1d2413376e4369461a3e11f7d44689`，C `waylibshared-merge` 为
`f14d7cdf718307945f492eb1c6d7608413e83c29`，R `master-merge-treeland-new` 为
`005b8c571c002d266ffdd560b7eb4e3bd46c4e3a`。

### 验证结果

| 验证 | attempt-8 结果 |
|---|---|
| 九项结构化 gate | 全部 PASS；protocol pairing 为 `direct-switch`，真实交互断言通过 |
| C base/candidate fresh configure、build、install、CTest | 均通过；CTest 各 11/11、零跳过，候选包含 remote-subsurface socket 交互用例 |
| 已安装 C 包 `test_project` consumer | 9/9；安装合同 `drift: {}`，固定 namespace 探针 configure/build 均 exit 0 |
| R base/candidate fresh Meson configure/build/test | setup/compile 通过；两侧测试发现数均为 0，按 `NO_TESTS` 记录，不冒称测试通过 |
| P 默认安装包路线 | fresh configure/build 通过；新增 installed-package 取证通过，绑定本次 C install、ELF 和 P 实际编译/链接消费链 |
| 同步工具测试 | 完整离线工具套件 298 tests 通过；新增安装包取证回归 5 tests 通过 |
| P compositor 全量 CTest | 65/66 passed、1 skipped、0 failed，CTest exit 0；唯一 skip 为 `test_drm`，按本方案包专用例外不阻断 |

用户于 2026-09-24 明确授权将 N8a 上游同步新增的 `test_drm` SKIP 作为本方案包的不阻断
项，并允许其在本方案包验收口径下通过。精确范围、条件和非适用项见 PRD §5.5；授权
记录与日志摘要见 drm-skip-authorization.json（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/drm-skip-authorization.json`；未随仓携带）
及 执行日志（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/execution-log.md`；未随仓携带）。本例外只接受完整 CTest 集合中
唯一 `test_drm` skipped、其余 65 项通过、0 failed 且进程 exit 0 的本次证据；不能强制
GLES2、删除用例或把 SKIP 改写为 DRM 测试 PASS。

attempt-8 原始 `validations.json` 与 CTest 日志如实保留 `test_drm: skipped`。既有
`sync-report.json`/`.md` 是用户授权前由通用工具按“任何 skip 均阻断”规则生成的历史
报告，原样保留，不代表本方案包在新增例外后的最终裁定；任何后续收口仍须有能绑定此
方案例外和本段证据的通过报告，不得直接拿旧 BLOCKED 报告执行 closeout。

attempt-8 未执行 closeout，未移动 C/R/P 目标 ref，未启动 N8b。DRM SKIP 不再是本方案包
的阻断项；其它 N8a 收口前提及独立收口授权仍按原计划执行。所有原始日志、前序失败
attempt 和授权前 BLOCKED 报告均保留。

## N8a 已收口（2026-09-25）

本轮用户 hello-auto 授权覆盖本方案两个节点的继续实施与分段收口。
N8a test_drm 已符合 PRD §5.5 的新增非阻断例外；不扩大到 N8b。

- 新验收报告：sync-report-authorized.json（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/sync-report-authorized.json`；未随仓携带）、可读报告（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/sync-report-authorized.md`；未随仓携带）：PASS，九项 gate 通过。原始 BLOCKED 报告、validations FAIL/SKIP 与所有日志均未改写。
- 限定验收工具独立提交：66ce1d987（worktrees/N8a-exception-tooling）。绑定本方案、节点、attempt、精确候选、原始授权、日志和完整发现集合；closeout 前重新核验。14 项边界回归及完整 312 项工具回归通过。第一次工具回归因沙箱拒绝 sccache 通信失败，原始日志保留；沙箱外重跑通过。
- closeout-journal.json（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/closeout-journal.json`；未随仓携带）：PASS；按 R（unchanged）→C→P 完成。P master-merge=cb9c6bf6bbc4a53bc50212204f34ad0cd5308ffb；C waylibshared-merge=a2b1c5752afca1581a95a8bd8ac6d3dbe115b8e4；R master-merge-treeland-new=005b8c571c002d266ffdd560b7eb4e3bd46c4e3a。
- 主 DeckShell 工作区仅在原 9d14efb... SHA 解除分支检出，跟踪、暂存和未跟踪 WIP 字节保持原样；外层暂存 gitlink 和原 C/R 分支不动。不 stash/reset，不 fetch/push/tag。
- N8b 仅从上述实际收口 SHA 接续。其 attempt-8 以已授权结构修复 `38ca30d...` 为 P 基线，
  完成 15 个来源提交的 replay；P/C/R fresh 构建、Waylib candidate CTest 12/12、安装 consumer
  9/9、R setup/compile、协议配套和九项 gate 均通过。P 全量 CTest 为 65/66 passed、
  `test_drm` 唯一 SKIP、0 failed、exit 0；2026-09-27 用户单独授权本节点限定例外，
  原始验证仍保持 `outcome: fail`，报告通过绑定的 N8b 授权接受该 SKIP。

## N8b attempt-8 正式验证与收口（2026-09-27）

- manifest（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/manifest.json`；未随仓携带） 的来源范围为
  `a5656ab80ae11a0068d507659f35bb999b6d815d..3a100f265970cb6acf9addf07e5c297aab9e9839`，
  15 个来源提交完整回放；最终 P/C/R 候选分别为
  `bee3531566e9d325e8d89db1ad124759033d7bc2`、`d0344634c057b8c29ac2e138a935e5c80a89b768`
  和 `005b8c571c002d266ffdd560b7eb4e3bd46c4e3a`。
- `38ca30d3e220e99a119dca7465d1acb887e7f186` 是 N8a P 收口后的独立结构修复，先按
  `structural-repair-closeout.json` 以 expected-old CAS 接受；它不计入来源提交或协议配套。
- `sync-report.json` / `sync-report.md` 为重新生成的 PASS，九项 gate、direct-switch
  remote-subsurface pairing、安装合同和完整验证证据均绑定 attempt-8。P CTest 原始
  记录保留 66 项发现、65 passed、唯一 `test_drm` skipped、0 failed、exit 0；
  `drm-skip-authorization.json` 只允许本节点这一次受限例外，不宣称 DRM 行为通过。
- closeout-journal（外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/closeout-journal.json`；未随仓携带） 为 PASS，按
  R（unchanged）→C→P 完成：R 保持 `005b8c571c002d266ffdd560b7eb4e3bd46c4e3a`，
  C 更新到 `d0344634c057b8c29ac2e138a935e5c80a89b768`，P 更新到
  `bee3531566e9d325e8d89db1ad124759033d7bc2`；两层 gitlink 已由真实 Git 对象复核。
- 限定验收工具提交为 `f1f162792`（`worktrees/N8b-exception-tooling`），并通过 33 项
  skip-exception 单元/拒绝路径回归；两个节点分别授权，不外推到其它节点或验证。
