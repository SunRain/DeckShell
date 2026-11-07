> 仓内参考副本；权威原文：`.helloagents/plans/20261106_treeland_0_10_0_to_0_11_0_local_sync/prd.md`。
> 保留原同步方案的历史时点与验收边界；其中历史命令不是本次补档的执行指令。

# Treeland 0.10.0 → 0.11.0 三仓同步需求

## 当前结论与授权边界

用户已明确授权将 Treeland 实现范围 `(3a100f265970cb6acf9addf07e5c297aab9e9839..f342a5b6debd028ed9bc4bc3e806118efbcae8f2]` 同步到 DeckShell `master-merge-to-0-11-0`。本地预检已核对 64 个来源提交、0 个 merge、P/C/R 无范围重叠，路径审核后的 inventory 为 `pass`。尚未 replay、创建产品候选或更新目标 refs。

**实现范围、独立协议 XML 来源及 §4 的限定协议和工具适配均已获用户明确批准（2026-11-06）。** 使用本地已存在的 TreelandProtocols `0.7.0`，剥离 commit 为 `49e985e0fb0b55fd2299349f08bac14c4e09f2b3`，仅同步下文列出的本段必需 XML，不采用协议 master 的后续内容。

本文件记录产品目标、边界与接受条件；具体 worktree、命令和逐提交适配方案另记 `plan.md`，不把预检通过写成产品接受。

## 1. 目标与范围

维护者需要在保留 DeckShell 本地项目布局、安装包合同和子模块结构的前提下，获得 Treeland 0.11.0 的实现、客户端及测试变化，并能逐提交追溯对应的上游 SHA。不是将上游整树覆盖到本仓库，也不是合并协议和实现两个互不相干的 Git 历史。

- P：Treeland `src/`、`tests/`、`examples/` 等按权威路径策略映射到 `compositor/`；根拥有路径仍按策略处理。
- C：`qwlroots/`、`waylib/`、`wlroots/` 的普通内容进入 `3rdparty/waylib-shared` 对应仓库，保留相对路径。
- R：独立 wlroots 仓库。本段来源 `3rdparty/wlroots` 子树未变化，不创建虚假的 R 内容提交，但当前 C 已登记 R，三仓身份、R 构建与消费关系仍需验证。
- 只选整体终点 `f342a5b6...` / tag `0.11.0` 为本批必验关键节点；没有另外选择中间 tag，不声称普通中间提交可独立构建。
- 用户已要求继续执行该明确范围；报告和全部必要 gate 通过后进行本地收口，不再为同一已授权实现范围重复确认。新增协议输入及路径权限不能由该范围推定。

## 2. 本地冻结事实

以下是 2026-11-06 预检实际解析的值；实施前须再次核对，不能用移动后的分支替换。

| 项目 | 值 |
|---|---|
| 来源仓库 | `DeckShell/` |
| 来源标识 | `refs/remotes/treeland/master` |
| 本地来源 tip | `87485fdeccc93e134e897d479439db03e5730465` |
| 实现 base，不包含 | `3a100f265970cb6acf9addf07e5c297aab9e9839` / `0.10.0` |
| 实现 head，包含 | `f342a5b6debd028ed9bc4bc3e806118efbcae8f2` / `0.11.0` |
| P 目标 ref | `refs/heads/master-merge-to-0-11-0` |
| P 基线 | `36208f1f600bd64ee6b0047e112b26b4aea9f2ba` |
| P → C | `3rdparty/waylib-shared`，mode `160000`，`7f93d719aa33605b3c0de9684471698016d06b1a` |
| C 当前日常分支 | `waylibshared`，保持该 ref 不动 |
| 建议 C 同步目标 | 新建 `refs/heads/waylibshared-merge-to-0-11-0`，起点为上述 C 基线 |
| C → R | `3rdparty/wlroots`，mode `160000`，`c844d3549136a250231d3abb2fc5f6832ff05c4e` |
| R 当前日常分支 | `master-merge-treeland`，保持该 ref 不动 |
| 建议 R 验收目标 | 新建 `refs/heads/master-merge-treeland-to-0-11-0`，起点为上述 R 基线 |
| 已登记 R URL | `https://github.com/SunRain/waylib-wlroots.git`，本批不修改 |
| 协议本地仓库 | 外层工作区的 `treeland-protocols/` |
| 已接受实现/XML pair | 实现 `3a100f26...`；XML `284e3aac8a1ed5ece66c4cb248e8b24d33cb25a0: wine/treeland-remote-subsurface-unstable-v1.xml` |
| 已批准 XML head | `49e985e0fb0b55fd2299349f08bac14c4e09f2b3` / TreelandProtocols `0.7.0` |

P/C/R 当前源码工作树均干净。外层仓库有既有改动，不纳入本任务、不暂存、不提交、不改变其 DeckShell gitlink。

两个建议 C/R 目标名称在预检时尚不存在。使用新分支是为避免同步期间移动用户日常分支；不是从旧同步分支 tip 取起点。若实施前名称被占用，停止核对，不覆盖同名分支。

## 3. 来源盘点与路径审核

权威策略为 `DeckShell/doc/skills/treeland-deckshell-sync/references/path-policy.md`，统一 inventory 用指定技能生成。

| 分类 | 审核后的来源提交数 |
|---|---:|
| `deckshell-only` | 52 |
| `waylib-only` | 5 |
| `dual` | 7 |
| `unowned-skip` | 0 |
| `blocked` | 0 |

原始 inventory 保留在 evidence/preflight/inventory.json（外层历史资料：`.helloagents/plans/20261106_treeland_0_10_0_to_0_11_0_local_sync/evidence/preflight/inventory.json`；未随仓携带），其中一个 `.github` 提交因需人工审核而 blocked；审核后结果为 inventory-reviewed.json（外层历史资料：`.helloagents/plans/20261106_treeland_0_10_0_to_0_11_0_local_sync/evidence/preflight/inventory-reviewed.json`；未随仓携带）。这不是删除来源提交或放宽未知路径。

提交 `a1474780df3be655ac49b4f8c8ca9559d56cbb72` 仅移除以下五个 workflow 的 `push` 触发，保留 `pull_request`：

- `.github/workflows/treeland-archlinux-build.yml`
- `.github/workflows/treeland-deepin-build.yml`
- `.github/workflows/waylib-archlinux-build.yml`
- `.github/workflows/waylib-debian-build.yml`
- `.github/workflows/waylib-deepin-build.yml`

上述提交属于已确认的完整来源范围，已逐文件审核后通过 `--approve-review .github` 分类。目标适配仅移除对应触发块，保留本地 `3rdparty/waylib-shared` 路径、PR 过滤及其余 job；不执行 workflow、不修改远端 CI 或其它 `.github` 文件。

R 来源子树在实现 base/head 均为 `d1801201aed147c476f19ccfd64180a59472ad5b`。当前 R 根树为 `67c793a1dd5c6fcb91c61874647c9ab76f030f0e`，存在两条已继承的本地差异，须按基线证明格式完整审核，不冒充完全等价：

1. `.gitignore` 增加 `.helloagents/`。
2. `types/buffer/buffer.c` 为已有 `waylib_buffer_get_count(void)` 增加前置声明和注释。

本批保留这两处既有差异，不将它们伪造为本段 Treeland 来源提交，也不借此豁免 R 原生构建。

## 4. 协议配套：已批准的限定范围

### 4.1 来源选择

XML 范围固定为 `(284e3aac8a1ed5ece66c4cb248e8b24d33cb25a0..49e985e0fb0b55fd2299349f08bac14c4e09f2b3]`，remote-subsurface 路径保持 `wine/treeland-remote-subsurface-unstable-v1.xml`。

依据：本批来源 `f07097fb...` 的 compositor-action 模块明确要求 TreelandProtocols `0.7.0`；该发布对象在本地完整可解析，包含本批新增和迁移的接口。后续协议 `0.8.0`/`0.9.0` 包含本实现范围之外的变化，不采用。

只读 proposed-protocol-inspection.json（外层历史资料：`.helloagents/plans/20261106_treeland_0_10_0_to_0_11_0_local_sync/evidence/preflight/proposed-protocol-inspection.json`；未随仓携带） 为 `pass / inspected-not-accepted`：从 C provenance 核对了两个已接受 base；实现相关变化为 `3c31ceb6...`，XML 相关变化为 `8edebdaf...`、`aa2e38db...`。检查报告的 `wire_changed` 为 true，最终还须区分生成接口与描述语义、评估客户端影响并完成真实交互测试；不能据此宣称已适配。

### 4.2 P 的精确 XML 清单

所有 P 文件继续放在 `protocols/compositor/xml/` 并从 `${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}` 生成，不引入系统最新 TreelandProtocols。

| XML 来源路径（0.7.0 固定 commit） | P 同名文件 | 动作 / 对应实现 |
|---|---|---|
| `dde/treeland-layer-shell-extension-unstable-v1.xml` | `treeland-layer-shell-extension-unstable-v1.xml` | 新增；`7543988408...` |
| `dde/treeland-xwindow-control-unstable-v1.xml` | `treeland-xwindow-control-unstable-v1.xml` | 新增；`49ef208f21...` |
| `public/treeland-appearance-unstable-v1.xml` | `treeland-appearance-unstable-v1.xml` | 新增；`0b4b32cd36...` |
| `dde/treeland-appearance-manager-unstable-v1.xml` | `treeland-appearance-manager-unstable-v1.xml` | 新增；`0b4b32cd36...` |
| `public/treeland-decoration-unstable-v1.xml` | `treeland-decoration-unstable-v1.xml` | 新增；`2436034c5c...` |
| `dde/treeland-active-notify-unstable-v1.xml` | `treeland-active-notify-unstable-v1.xml` | 新增；`a4189913ea...` |
| `dde/treeland-region-watch-unstable-v1.xml` | `treeland-region-watch-unstable-v1.xml` | 新增；`2dfaa7f544...` |
| `dde/treeland-compositor-action-unstable-v1.xml` | `treeland-compositor-action-unstable-v1.xml` | 新增；`f07097fb98...` |
| `public/treeland-snap-target-unstable-v1.xml` | `treeland-snap-target-unstable-v1.xml` | 新增；`abc37ce7b3...` |
| `dde/treeland-dde-shell-unstable-v2.xml` | `treeland-dde-shell-unstable-v2.xml` | 新增；`6ed299b0f9...` |
| `dde/treeland-input-manager-unstable-v1.xml` | `treeland-input-manager-unstable-v1.xml` | 更新；XKB 接口 version 2，`40f5a97456...` |
| `deprecated/treeland-dde-shell-v1.xml` | `treeland-dde-shell-v1.xml` | 更新；与本批 DDE 功能拆分及上游 v1/v2 过渡同步 |
| `wine/treeland-remote-subsurface-unstable-v1.xml` | `treeland-remote-subsurface-unstable-v1.xml` | 更新；C/P 配套步骤管理，空字符串 bottom sentinel 与 `3c31ceb6...` 对齐 |

其余已有 XML 不因字节不同而批量刷新。C 的同一 remote-subsurface XML 与来源 provenance 由统一配套阶段更新；两份 XML、相关实现、原生客户端和测试必须一起验证。remote-subsurface 固定 `direct-switch`，不添加别名、双版本或运行时回退。

来源 `6ed299b0...` 自身保留 DDE Shell v1 并新增 v2；该过渡与 remote-subsurface 的单协议直接切换是不同事项。不得借同步自行删除上游保留的 v1、DeckShell 的既有 `treeland-dde-shell-client/` 或增加其它兼容层。若本地客户端因本批协议变化需要额外修改，必须先明确具体调用方和授权范围。

### 4.3 同步工具的有限适配权限

当前 `contract_migration.PARENT_INTEGRATION_FILES` 已支持 remote-subsurface，但不支持上表其它 12 个 P XML 路径。完成本批需精确扩展这些路径，并同步相关技能说明和拒绝路径测试；不得改变权威 source path-policy、放行整个 XML 目录或放宽任意生产文件。

**用户已明确批准的授权**：采用第 4.1 节固定 XML 来源，允许第 4.2 节 13 个 P XML 及 `protocols/compositor/CMakeLists.txt` 的必要安装清单适配、C/P 的 remote-subsurface 配套，并允许为其中新增的 12 个路径更新同步工具的精确白名单及相关测试/说明。每个实际补丁仍绑定具体来源 SHA、相邻快照和逐路径审核证据。

本授权不包含 Waylib exported target、安装路径、namespace、pkg-config 或其它公共包合同迁移。后续用户明确要求“跳过 `当前阻塞：DRM 测试`，继续执行剩下任务”：仅授权本批 N9 的 `test_drm` 在完整、未过滤 CTest 中真实 SKIP 时不阻断接受；不覆盖真实失败、其它 SKIP 或缺测，不证明 DRM/GPU 行为。此为本轮独立授权，不沿用旧 N8a/N8b 例外。

## 5. 接受条件

1. 本地冻结对象、祖先关系、范围顺序和 P/C/R 基线再次核对；inventory 为 `pass`，没有 merge/unknown/未审核路径或重复来源映射。
2. 在独立 clean linked worktree 逐提交 R→C→P；保留原作者、时间和完整来源消息，每个来源都有唯一 trailer、manifest 和真实 gitlink 对应关系。
3. 普通 `applied` 补丁按来源投影；冲突仅使用已审核目标相对 `adapted` 补丁及完整逐路径证据，不能静默丢弃、改写既有历史或扩大规范目标。
4. 所有中间 C 源码合同通过；任何未经授权的公共合同漂移立即停止，不以终点恢复或一次 consumer 通过豁免。
5. 本节点完成 C base/candidate fresh configure、默认完整 build、install、完整 CTest、既有 `test_project` consumer 和固定 namespace 编译；R base/candidate 均实际执行 Meson configure/build/test，并证明 C/P 使用本次 R。
6. P 候选使用正常产品配置 fresh configure、默认完整 build、compositor 完整 CTest；测试失败、缺依赖、SKIP 或缺测不能写成 PASS。仅 §4.3 本轮授权的 `test_drm` SKIP 可作为明确的非阻断例外，原始验证仍记录真实结果。真实零注册测试只记 `NO_TESTS`；不复用历史构建/测试目录。
7. 协议来源、wire/行为/客户端审查、真实交互和 `protocol-verify` 全部通过，最终报告具备技能要求的九项 gate，并绑定本批唯一必验终点。
8. 报告有效且目标未被检出后，按 R→C→P expected-old CAS 收口到本批目标 refs；失败保留工作树、journal 和原证据，不自动回滚任何已接受层。
9. 全批接受后执行统一技能 `finish --task sync`，自动生成/核对 P/C 仓内记录；文档未完成时不得声明整批交付完成。记录生成不等于自动暂存或提交。

## 6. 明确不做

- 不同步 0.10.0 之前或 0.11.0 之后的来源提交，不把协议 commit 当成 Treeland 实现 base。
- 不自动 fetch、push、tag，不修改 remote/子模块 URL、外层 Git index 或外层 DeckShell gitlink。
- 不移动 P `master`、C `waylibshared`、R `master-merge-treeland` 等日常 refs，不清理旧工作树或本地 WIP。
- 不整体覆盖协议目录，不采纳协议 0.7.0 之后的内容，不自行移除来源保留的 DDE v1 过渡。
- 不新增无关抽象、发布流程、广义白名单、公共 API 迁移、测试豁免或用于代替真实验证的报告。
