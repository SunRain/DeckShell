# Treeland 0.8.14 → 0.9.1 本地同步实施方案

## 留存说明（2026-09-15）

本文件来自外层原方案包 `.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/plan.md`，保留其完整实质正文、原授权、旧 SHA、失败记录及原验收结论。以下历史正文只调整链接定位；外层原件与证据仍留在原位置，没有被本副本替换或搬迁。

- **原同步事实**：N1—N7 的结果属于原报告记载的候选与环境。原文“不重写已同步历史”“只使用本地 URL”等约束保留为当时边界，不回改历史授权。
- **本次限定例外**：2026-09-14 获准对 P 502、C 386、R 332 个历史对应提交整理顶层 `Refs` 及派生父子引用，普通文件不变，R0 的 7528 个原始对象不变；本副本与本仓记录、C 的 R URL 更新均在历史区间之后新增。
- **记录与映射**：[本仓同步记录](summary.md) 区分 Treeland 来源、原目标与新目标。完整旧新映射位于外层 `.helloagents/plans/20260914_treeland_refs_portability/rewrite-map.json`；原三个旧头由各仓 `refs/backup/treeland-refs-portability-20260914/original` 保持可达。
- **工具交付**：仅在 P 末端独立交付来源 `3b1a8ab63c55091b43da2664014fa72636f57f0e` 的完整工具修订、Python 3.9+/CMake 3.27+ 要求及按仓记录生成器；不把新工具插入历史对应区间，不声称其当时用于全部节点。
- **引用语义**：短 `Refs: 20260909_treeland_0_8_14_to_0_9_1_local_sync/plan.md` 供维护者在当前 P/C 交付树查找共同文档，不承诺每个历史提交都已含副本。R 不新增方案副本；R 的短 Refs 是 P/C 共同文档标识，不是 R 仓内相对路径承诺。
- **证据边界**：`evidence/`、日志全集、worktrees、构建和安装树均未复制。标注“外层历史资料”的项只能在原外层方案包查询；“P 仓共享资料”按 P 仓内路径定位。仅有两份 Markdown 不代表独立克隆后可重放原验收。
- **发布边界**：R 的指定 SSH 地址为 `git@github.com:SunRain/waylib-wlroots.git`；本次只配置本地引用与地址，未 fetch/push/tag，未验证远端可达性、对象齐备或跨机器克隆。Git 内容对应核对及工具回归不替代原产品验收。

---

本方案承接 [PRD](prd.md)；2026-09-09 的 `hello-auto` 实施请求覆盖七个节点、独立初始化和通过验收后的本地分段收口。历史 PRD 的“本轮只读”描述针对需求讨论，不替代本次明确实施授权。仍不 fetch、push、打发布 tag 或暂存/提交外层 gitlink。

**执行结果（2026-09-14）：N1—N7 均已验收并完成本地收口，501 个普通来源与 N2 独立初始化完整覆盖。** 各节点证据见第 6 节，整组连续性及最终分支核对见第 7 节。

## 1. 冻结输入与目录

实施前重读 Git 对象，确认与 PRD 一致，原始结果见 inputs.json（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/preflight/inputs.json`）：

- 来源标识：P 的 `refs/remotes/treeland/master`，冻结 tip `cb038ef766940545fd05d0a22578c7e9fbaa7324`。
- 整体范围：`(7da2254d386935f753ed907f8d6e76c1639d01a9..fd573cf44fb06ee1eebcdd8c39716d1c797b64d4]`。
- P 基线：`4e5d37c144edee006a7ff2598c243f0f9715b979`；目标 `refs/heads/master-merge-treeland`。
- C 基线：`26f52806c0432c70438a027b7e7659e1cb481b2b`；新目标 `refs/heads/waylibshared-merge-treeland`，不改原 `waylibshared`。
- P→C 已核对为上述 C 的 `160000 commit`；两个源码工作区干净。外层已有修改保留，外层索引摘要及暂存 gitlink 已单独冻结。
- R 持久对象库：`/home/wangguojian/Project/sde-project/HA-DeckShell/local-repositories/treeland-wlroots.git`，目标 `refs/heads/master-merge-treeland`。C 子模块 URL 使用此绝对本地路径，只承诺本机可用。
- 普通同步 CLI 的仓库入口要求工作树，因此 R 另设持久 detached 访问工作树 `local-repositories/treeland-wlroots/`；`--wlroots-repo` 使用该入口，common Git directory 和子模块 URL 仍指向上述 bare 对象库，不迁移对象、不更换来源或目标 ref。
- 各节点源码工作树：本方案目录的 `worktrees/<节点>-attempt-<次数>/{parent,child,child-base,wlroots,wlroots-base}`。
- 各次运行证据、构建和安装：`evidence/<节点>-attempt-<次数>/`。该目录与所有源码工作树分离；不复用前次 build/install，不依赖 `/tmp`。
- `run_id` 使用 `treeland-20260909-<节点>-attempt-<次数>`；`refs_doc` 始终指向本文件。冲突现场与失败 journal 保留，重新审核后使用新身份和新工作树，不修改旧身份。

## 2. 连续分段

| 节点 | 来源左端（不含） | 来源终点（含） | 处理 |
|---|---|---|---|
| N1 / 0.8.15 | `7da2254d386935f753ed907f8d6e76c1639d01a9` | `2df4c21c0499b46229f1ef0080cc265994b4fd60` | 28 个普通来源，P/C |
| N2 / 首次导入 | N1 | `1ffe0010193a8c696ef6436a4c436f57bbb1e8ec` | 独立初始化，禁止普通 replay |
| N3 / 0.8.16 | N2 | `4db6917f873990966f58578abe7dca8b8b371d36` | 21 个普通来源，R→C→P |
| N4 / 0.8.17 | N3 | `24c1a0b547fc8a1c6617bdff147efcbad03c2f98` | 20 个普通来源，R→C→P |
| N5 / 0.8.18 | N4 | `7134887c66e5215182e1a1f648bdc8971f17e864` | 43 个普通来源，R→C→P |
| N6 / 0.9.0 | N5 | `ce57dab0259c33eb183589928249ef9e2be149af` | 357 个普通来源，R→C→P |
| N7 / 0.9.1 | N6 | `fd573cf44fb06ee1eebcdd8c39716d1c797b64d4` | 32 个普通来源，R→C→P |

全部祖先关系、六个 tag、501 个普通来源和各段无 merge 已重算。N2 相对第一父节点可达新增 7529 个提交，单独保留其历史，不挤入 501 个普通来源清单。

## 3. 执行与适配

### 公共合同迁移补充（2026-09-11 已授权）

- 用户已明确允许 N5 的 qwlroots → 原生 wlroots 公共合同迁移，按 [PRD 第 5 节](prd.md#已授权的-qwlroots--原生-wlroots-公共迁移) 接入来源 `9582881d…` 及固定区间内的直接后续实现；不再以保留 qwlroots 包阻断，不新增兼容壳。保留 `WaylibShared::SharedServer` CMake target、`Waylib::Server` C++ 命名空间及原 QML URI；`qw` 随旧包退休，其他范围约束不变。
- 复用统一工具现有的 decisions、逐路径工件和快照比较，补充显式 `contract_migration` 审批：绑定来源、方案、相邻源码快照、完整批准差异及精确集成路径；安装端单独绑定真实安装快照和头/命名空间绑定。默认无审批仍阻断；旧 wrapper-only 批准不能代替公共迁移，错误/漂移审批不能放行。
- 首次迁移的必要本地集成包括 C 根 `CMakeLists.txt`、`waylib/src/cmake/WaylibSharedServerConfig.cmake.in`、现有 `test_project` 的配置/原生 API 消费检查；P 包含 `test_protocol_foreign-toplevel`、`test_multi_seat`、`test_scroll_factor`、`test_manager_resource_lifecycle`、`test_late_dde_listener` 的旧 qwlroots 调用。实际改动逐文件登记，不扩大为目录白名单；标准来源目标仍由原 inventory 决定。
- N5 原生迁移验收发现既有 `DeckShellQmlRuntime` 组件漏装新的直接运行时依赖；将唯一入口 P `compositor/src/CMakeLists.txt` 精确登记到来源 `9582881d…` 的迁移审批，按真实 target 安装原生库。此为已授权公共包迁移的必要集成，不放行其他生产路径，不改 smoke 测试借用系统/构建树库。
- 保留 `N5-review-1` 前 30 个审核结果，在新的审核工作树承接迁移；列出来源删除文件并先移入回收站，再暂存精确删除。原目标分支、旧尝试和外层索引不动。
- 工具变更先覆盖无审批、错误来源/快照、未批准额外路径、旧审批误用和消费者失败等拒绝路径，再运行相关回归。N5 整段正式回放及八项门禁仍完整执行；C 基线/候选、R 基线/候选和 P 候选全部 fresh 验证，候选 consumer 必须消费迁移后的实际安装包。

### N6 增量与协议输入补充（2026-09-12 已授权）

- 同步 N6 跨进程子表面、相对指针和指针约束公共 API、scanner 迁移及开发文件开关；仅统一 CMake target 引用，保留实际 C++ 命名空间。源/安装差异沿用精确审批，独立 C 的开发文件完整安装消费仍为必验项。
- 安装开关须在 P/C 根进入 wlroots 前确定：P 默认关闭，独立 C 默认开启。`EXPORT` 和公共头不能只绑定 `NAMELINK_ONLY`：N6 attempt-1 的真实安装产生空导出，consumer 报 `Component SharedServer not found`；改为开启时导出真实库、用 `NAMELINK_COMPONENT` 区分开发符号链接，关闭时仅安装运行库。旧失败证据保留，新候选完整重验。
- 已更新的 P `treeland-protocols/master` 冻结为 `dada26e01c1c6564a961981769df4854e2a4fec5`；从其祖先 `8dc1d1e788dc964cd0f756b4491d0225e70b1598:xml/treeland-remote-subsurface-unstable-v1.xml` 提取 N6 所用接口，保留 Git blob 与提取说明。最新协议的 manager 更名不属于本次来源实现；不 fetch、不读取系统副本作输入。
- 新 XML 与安装登记、P 根依赖顺序及原 scanner 文件，按对应来源逐文件记录必要集成，不改写来源 inventory。C standalone 显式选择本次协议目录；P 使用自己的协议子项目。tracker 读取实际 P XML 改动并绑定上述冻结协议历史，候选不冒充确认映射。
- N6 从 N5 已收口的 R=`c254362a1f79c88d21c773e22373ebe538194169`、C=`11e096a97e13d4b8740cea0d735f758e66b6534c`、P=`d24d389a597f9be2e619586bcc76b3c0518ceef3` 开始。R 与源基线的唯一差异是 `types/buffer/buffer.c` 的已验收前置声明，使用现有逐路径 baseline proof，不宣称树相等。

1. 六个线性范围分别运行统一 inventory；预检原件位于 `evidence/preflight/`。未知路径和类型漂移不能批准。当前待审核项仅为既有策略的 `.github`，先逐来源审阅变更，再按 `.github` policy key 明确批准纳入 P；纳入不等于批准绕过 CI 安全边界或保留错误的 monorepo 路径。
2. 从冻结基线建立独立 linked worktree。P 主工作树在同一 SHA 脱离目标分支，以满足 closeout 的“目标未被检出”；不改变其文件或外层索引。新建 C 目标分支但不检出，不改原分支。
3. 普通来源按原顺序回放；只有真实冲突、项目路径差异或合同差异才制作目标相对适配补丁。逐路径写清取舍和内容寻址证明；常规适配不扩大 inventory 的目标集合，公共迁移只附加上述精确批准的本地集成文件，不把上游实现挪到兄弟文件。
   - 回放进程显式使用 `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.cleanup GIT_CONFIG_VALUE_0=verbatim`，仅覆盖该进程的 Git 提交消息清理方式，不改仓库或全局配置。N1 attempt-2 的真实提交证明默认清理会删除原文缩进块中空行的空格，导致 P/C 原始消息校验失败；保留该现场，使用新 attempt 回放，不放宽验证器或改写旧提交。
4. 每个 C 节点运行技能源码合同审计，R 内容及两层 gitlink 依次核对；仅 C/R 变化也产生对应 P gitlink-only 提交。原作者、时间、完整消息和来源 SHA 由技能记录。
5. 中间节点不编译。段末使用本段基线和候选，运行技能必需的真实构建、安装与消费链，然后生成八项门禁及完整报告。
6. 每段完整报告通过后以 expected-old、可快进条件按 R→C→P 更新本地目标 ref。后一段仅从已收口结果接续。失败不越过节点，不倒填 PASS，不回滚已通过节点。

## 4. N2 独立初始化

N2 不调用普通 replay，不伪造其 inventory、manifest 或 journal。

1. 仅在 N1 完整验收并收口后创建持久独立 bare R。通过本地 Git 对象传输导入 `88a869855742281c98c22cab9641b317b8d065ef` 及其完整可达历史，不取远端对象、不使用 alternates 或一次性对象库。
2. R0 保持该真实 commit 不变；重算 `R0^{tree}` 与 `N2:3rdparty/wlroots`，两者必须为 `905c266d5caa6a5667806e16b2d656cd0f9f0d9d`，并运行对象完整性检查。当前对象中的原生版本为 wlroots 0.19.3，不从 UPSTREAM 文字选择其他提交。
3. 在 N1 的 C 上建立 C0：保留既有 `.gitmodules` 条目，仅新增 `3rdparty/wlroots` 的本地 URL 和准确 R0 gitlink。初始化所需的 C 根接入和普通 `wlroots/` 包装层单独审核；不提前回放 N3 的来源提交。优先用 R 的原生 Meson 构建及精确的本地链接接入，既有核心 target、公共头路径、命名空间、导出属性与 pkg-config 合同不变。
   - N2 实际接入使用未导出的 imported SHARED target，显式记录本次产物 location/SONAME，避免配置时库尚未生成导致 CMake 改用 `-L/-l` 搜索。Meson uninstalled 元数据缺少能力字段，须从同次正式 `.pc` 补齐全部 `have_[a-z0-9_]+` 字段；不能漏掉 X11/GLES2 或从系统库推定能力。
4. 若来源尚无更新脚本，不凭空导入未来脚本；来源引入脚本时必须保留普通文件并加技能规定的拒绝前缀。包装层接入必须证明 C/P 实际使用本次 R 的头、生成头与链接产物，系统同名库不能充当证据。
5. C0 源码合同审查通过后建立 P0，只变更 `3rdparty/waylib-shared` gitlink；消息明确独立初始化及原始 merge 的双亲，不称线性 cherry-pick。
6. 初始化证据使用单独的 `initialization/` 目录，记录真实命令、R0 对象历史、源树投影、C0/P0 相邻差异与对应关系、两层工作树身份、源码与安装合同。所有证明必须可从 Git 对象和原始日志重算，不能手写技能 PASS。
7. N2 执行与普通节点同等级的完整三仓验收：N1 C 基线和 C0 分别 fresh configure/build/install/CTest，C0 安装包 consumer 与固定 namespace 探针，R0 原生 Meson 配置/构建/测试，P0 全新完整产品构建与 compositor CTest。N2 的 R 基线与候选同为 R0，仍分离构建目录；原生零测试只记 NO_TESTS。
8. 独立初始化验收通过且所有 refs 未被检出，使用实际 Git expected-old CAS 顺序建立/更新 R、C、P，记录每次原始输出。后续 N3 的普通工具链从真实 N2 三仓基线开始。

无法在保持公共合同的前提下接入 R 时，保留 N1 已验收结果和 N2 现场，停止该节点；不借初始化权限放宽公共 API。

## 5. 验证与证据

- 工具入口固定为 `DeckShell/doc/skills/treeland-deckshell-waylib-unified-sync/`；旧父仓 skill 仅提供 path-policy，不另跑一条同步线。
- 每个普通节点保存 `inventory.json`、技能生成的 manifest/journal、逐提交证据、八项门禁、`validations.json` 和 `sync-report.{json,md}`；最终在本文件链接真实节点报告，不建立替代技能报告的全局 PASS。
- C 基线/候选：Ninja、Release、导出编译数据库，开启现有 `BUILD_WAYLIB_TESTS` 和 `BUILD_QWLROOTS_TESTS`，默认完整构建，独立安装，运行完整 `build/waylib` CTest。
- consumer：仅使用候选自带 `test_project/` 和本次安装路径，fresh configure、默认完整 build、完整非零 CTest，然后执行安装合同审计与固定基线 namespace 编译探针。
- P：正常产品配置、全新 Ninja build、默认完整构建、完整 compositor CTest。顶层无测试如实 NO_TESTS。配置失败不能靠关闭产品目标补成成功。
- R 启用后：基线/候选独立 Meson configure/build/test，禁止下载；记录器绑定每次真实测试日志与编译依赖，C/P 的具体消费目标链接输入必须使用当前 R。
- source XML 或实际 P 协议 XML 变化时运行协议追踪；N6 使用上述用户已授权并冻结的协议仓库/head，未触发仍由工具输出事实，不再请求重复输入。
- 收尾核对最终目标 refs、两层 gitlink、工作树、普通来源覆盖和外层索引摘要。主工作树是否切到已通过候选不替代这些验证；不更新外层暂存 gitlink。

## 6. 节点结果入口

实际运行结果及失败边界在此追加真实证据链接；没有报告的节点不标记通过。

### N1 / 0.8.15：已验收并完成本地收口

- 完整报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/sync-report.md`）、结构化报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/sync-report.json`）、逐提交映射（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/manifest.json`）、命令与日志索引（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/validations.json`）、收口记录（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/closeout-journal.json`）。28 个来源提交全部有对应处理记录，八项门禁通过；R 尚不适用。
- 已按 C→P 更新目标分支：C=`5832583291b2ad14c4e723e26f5c5b851e6dbe03`，P=`055be261d35138ec678b3a7aaf1521bfc2d9a05e`。原 `waylibshared` 仍为 `26f52806c0432c70438a027b7e7659e1cb481b2b`；外层索引摘要仍与预检一致，未暂存或提交外层 gitlink。
- P 完整构建通过，compositor CTest **21/21**；C 基线与候选各自完整构建、安装、CTest **3/3**；候选安装包 consumer **3/3**；65 个基线公共头的固定命名空间独立编译通过，安装合同 `drift={}`。P 顶层为 `NO_TESTS`，不计作测试通过。
- attempt-2 的提交消息清理失败、attempt-3 的两处外部锁屏解锁回调编译失败均保留。attempt-4 在对应来源提交的 `helper.cpp` 适配中完整迁移激活状态与焦点恢复，不扩展规范目标路径、不追加冒充来源的修复提交。
- 验收发现旧命名空间探针将所有公共头合并编译，既触发基线已有 `wevent.h` 无重复包含保护的问题，也会借其他头的声明掩盖本头命名空间缺失。工具改为逐头独立编译，固定基线命名空间与候选安装包绑定不变；相关回归（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/namespace-probe-regressions.log`） **50/50**，旧失败探针及绑定工件保留于 原审计（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/contract-audit-unity-failed/waylib-contract-audit.json`）。工具改动保留在主工作树，不混入来源同步提交；产品公共头未修改。

### N2 / 首次 wlroots 导入：已独立验收并完成本地收口

- 初始化完整报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/initialization-report.md`）、结构化报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/initialization-report.json`）、结构与历史证明（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/structure-proof.json`）、真实验证记录（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/validations.json`）、收口记录（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/closeout.json`）。未调用普通 merge replay，未伪造普通分段 manifest/journal。
- 已按 R→C→P 执行 expected-old CAS：R=`88a869855742281c98c22cab9641b317b8d065ef`，C=`05e24276e3d5878b653adf692cd33391038dd398`，P=`4071efb9caf5adc60d236f41c9ca1bbfb49f8c10`。R 的 7528 个原始历史提交完整可读、根树与 N2 源子树一致、fsck 返回 0；原 C 分支与外层暂存索引未改变。
- 23 条真实命令完成：P 默认完整构建、compositor CTest **21/21**；C 基线和候选各自完整构建、安装、CTest **3/3**；安装包 consumer **3/3**；安装合同与固定基线逐头命名空间探针通过。R 基线/候选分别完成 Meson 配置、构建、测试与隔离安装，原生零测试和 P 顶层零测试均为 **NO_TESTS**。
- 原生接入证明（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/native-integration-proof.json`） 绑定实际 Meson/Ninja 源码编译、生成头、C/P 具体目标的精确库路径及运行时解析；3 个安装 consumer 使用本次 C/R 安装。8 个 linked checkout 及两层 gitlink 与候选一致、干净；既有公共合同未迁移，只精确批准未导出的 wrapper target 和根入口新增。
- attempt-1 的能力元数据配置失败、attempt-2 的 X11/GLES2 字段提取遗漏构建失败、attempt-3 的链接搜索形式审查均保留。attempt-4 修正真实能力提取并固定 SONAME，不关闭功能、不改产品公共头、不提前导入 N3 包装层。

### N3 / 0.8.16：已验收并完成本地收口

- 完整报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/sync-report.md`）、结构化报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/sync-report.json`）、逐提交映射（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/manifest.json`）、真实验证记录（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/validations.json`）、收口记录（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/closeout-journal.json`）。21 个来源全部按 R→C→P 处理，八项门禁通过。
- 目标分支已收口为 R=`4bc1705abf5b1250ea5888b6387b66d54718e331`、C=`1db059be68d697b7c47c7003f7433e0d1836139a`、P=`dc4f7d20294b8b6fa9decc39a783bf504246f34e`。N1 与 N3 累计覆盖 49 个普通来源提交，N2 为独立初始化，不计入 501 个普通来源。
- P 默认完整构建、compositor CTest **21/21**；C 基线/候选各自完整构建、安装、CTest **3/3**；安装包 consumer **3/3**；安装合同与固定基线命名空间探针通过。R 基线和候选分别完整构建、安装；R 原生测试与 P 顶层测试为 **NO_TESTS**。
- 上游 CMake wrapper 已接入实际 R 源码；保留既有 `PkgConfig::WLROOTS` 公共合同与 native target 名称，仅批准 wrapper 自身定义及新增 `lib/libwlroots-0.19.so`。更新脚本保留并前置拒绝执行，未执行上游更新脚本或 CI。输出拓扑合并保留本地协议销毁处理与回调身份；源明确移除的旧实现原件已移入回收站。
- attempt-2 完整编译后有 3 项 P 测试失败；根因是新增 QML `IMPORTS` 仍使用上游 `Waylib.Server`。在对应来源提交中映射到既有 `WaylibShared.QuickSharedServer`，并同步 Tinywl；第三次候选全部测试通过，未用测试豁免或运行时兜底。旧 失败报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/sync-report.json`） 保留。
- 普通记录器原先只识别 CMake 直接编译的 wrapper，无法核验 N2 的原生 Meson 基线。现补齐真实 Meson 来源、对象依赖、生成头及 C/P 精确链接证据，基线仍 fresh 验收；相关工具回归（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-review-1/native-wrapper-focused-tests.log`） **40/40**。工具修改保留在主工作树，不混入来源同步提交。

### N4 / 0.8.17：已验收并完成本地收口

- 完整报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/sync-report.md`）、结构化报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/sync-report.json`）、逐提交映射（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/manifest.json`）、真实验证记录（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/validations.json`）、收口记录（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/closeout-journal.json`）。20 个来源全部完成逐提交处理，八项门禁通过；与 N1、N3 累计覆盖 69 个普通来源，N2 仍单列为独立初始化。
- 已按 R→C→P 更新目标分支：R=`4507a6f414191bcfc150a966ba251c89f864663f`、C=`0d8c99c886084818a1caee37995390bb69603184`、P=`d1be07121ea0f20bf87a128208a703a0dbbf3b68`。后一段只从这组已验收结果接续。
- P 全新默认完整构建通过，compositor CTest **21/21**；C 基线、候选分别完整构建、安装、CTest **3/3**，安装包 consumer **3/3**，安装合同 `drift={}` 与固定基线命名空间探针通过。R 基线/候选分别完成 Meson 配置、构建、测试和安装；原生零测试与 P 顶层零测试均记 **NO_TESTS**。
- 第 18 个来源 `371d3224…` 的键盘分组冲突已按来源等价结构合并：保留物理键盘成员限制、共享 keymap 和修饰符去重；后续虚拟键盘销毁恢复仍保留为独立来源提交，没有压入前面的拖拽修复。
- attempt-2 的完整构建通过，但 `test_effect_glass::dconfigDefaultsMatch` 因 `SOURCE_DIR` 指向测试目录而非 compositor 根失败，旧 失败报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/sync-report.json`） 与工作树保留。attempt-3 在来源 `cd0879de…` 对应的 CMake 适配中修正根路径，不改默认值断言或复制配置文件；玻璃测试 **29 passed, 0 failed, 0 skipped**，包含以 `GLASS_BENCH=1` 启用的来源自带 benchmark。

### N5 / 0.8.18：已验收并完成本地收口

- 完整报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/sync-report.md`）、结构化报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/sync-report.json`）、43 个来源映射（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/manifest.json`）、23 条真实验证记录（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/validations.json`）、收口记录（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/closeout-journal.json`）。八项门禁通过，与 N1、N3、N4 累计覆盖 **112 / 501** 个普通来源；N2 独立初始化仍单列。
- 已按 R→C→P 收口：R=`c254362a1f79c88d21c773e22373ebe538194169`、C=`11e096a97e13d4b8740cea0d735f758e66b6534c`、P=`d24d389a597f9be2e619586bcc76b3c0518ceef3`。原 `waylibshared` 与外层暂存索引未改变。
- P 全新默认完整构建与 compositor CTest **21/21**；C 基线完整构建/安装/CTest **3/3**，候选 **8/8**；独立安装包 consumer **3/3**；**77 个**固定命名空间头逐头编译通过。R 两侧分别 fresh Meson 构建、测试与安装；R 原生零测试和 P 顶层零测试明确为 **NO_TESTS**。
- 安装审批（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/approved-installation-migration.json`） 与 安装合同（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/waylib-contract-audit.json`） 保留真实迁移差异：退休 qwlroots/`qw`，接入原生库、监听器与 `WWaylandResource`；保留 `WaylibShared::SharedServer`、`Waylib::Server`/`WEvent` 和原 QML URI，不将迁移写成 `drift={}`。不安装已无类声明和调用方的 `wsurfacehandler_p.h`，不补造旧接口。
- 源码修复均回到对应来源：`9582881d…` 补齐 R 计数器原型、既有测试的原生链接和运行时组件真实库安装；`b6dfb352…` 在配置失败时只发布当前输出、不应用失败配置，并用单次标记和对象存活检查处理异步失败。锁屏输出调整和隔离安装 QML smoke 均真实通过。
- attempt-2 的原生 `-Wmissing-prototypes`、attempt-3 的字面 `.pc` 检查/旧链接目标、attempt-4/5 的输出发布和 QML 运行时缺库、attempt-6 的陈旧安装头失败全部保留。修正后的 consumer 用原生 pkg-config 求值，正反向检查（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-review-3/consumer-path-regression.log`）证明合法变量展开通过、缺失本地库目录仍拒绝。
- 同步工具补齐唯一运行时入口的精确迁移路径和安装 namespace 投影；路径/迁移回归（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-review-3/runtime-migration-focused-regressions.log`） **54/54**，include/条件作用域回归（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-6/namespace-projection-regressions.log`） **40/40**。工具修改保留在主工作树，不混入来源同步提交。
- R 候选相对来源子树只保留 `types/buffer/buffer.c` 的前置声明适配；N6 必须据实际两棵树准备已有 schema 的逐路径基线证明，不能再声称根树完全相等。

### N6 / 0.9.0：已验收并完成本地收口

- 完整报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/sync-report.md`）、结构化报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/sync-report.json`）、357 个来源映射（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/manifest.json`）、23 条真实验证记录（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/validations.json`）、收口记录（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/closeout-journal.json`）。八项门禁通过，累计覆盖 **469 / 501** 个普通来源；N2 独立初始化仍单列。
- 已按 R→C→P 收口：R=`eace3155cdc96d6bea3b708255e27f3b28499078`、C=`83365fc20abbfdb29b710446d5e3cc5fabc86efe`、P=`77d487cedd0b1f1eabf1ec38ee744af3fe4a0930`。原 `waylibshared` 和外层暂存索引保持不变；N7 仅从这组结果接续。
- P 全新默认完整构建与 compositor CTest **22/22**；C 基线和候选各自完整构建、安装、CTest **8/8**；独立安装包 consumer **3/3**；**82 个**公共头的固定命名空间逐头编译通过。R 两侧分别 fresh Meson 构建、测试与安装；R 原生零测试和 P 顶层零测试明确为 **NO_TESTS**。
- 安装审批（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/approved-installation-migration.json`） 和 安装审计（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/waylib-contract-audit.json`） 记录真实增量：原生 wlroots 0.20.2、跨进程子表面、相对指针、指针约束、scanner 迁移及开发文件安装开关；保留既有导出目标、`Waylib::Server`/`WEvent` 和 QML URI，不将批准的差异写成无漂移。
- 两次早期失败的安装导出和 C++ 原生头入口问题已回到对应来源修正。第三次候选的 失败报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/sync-report.json`） 保留：新增协议后旧测试仍固定 21 个 XML，且生命周期测试在 `stop()` 释放 display 后再次访问事件循环。第四次候选在对应迁移中精确登记现有测试调用方：来源和安装包固定检查 **22** 个 XML；保留三种销毁路径及各资源恰好销毁一次的断言，并验证停止后的空句柄，不放宽测试。
- R 与 N7 源基线的唯一差异仍为 `types/buffer/buffer.c` 的已验收前置声明；N7 已使用该精确基线证明，不以源码树完全相等代替审查。

### N7 / 0.9.1：已验收并完成本地收口

- 完整报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/sync-report.md`）、结构化报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/sync-report.json`）、32 个来源映射（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/manifest.json`）、23 条真实验证记录（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/validations.json`）、收口记录（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/closeout-journal.json`）。第三次正式候选的八项门禁均通过；32 个来源产生 12 个 C 提交和 32 个 P 提交，R 无新增来源内容。此前的失败记录均保留。
- 已按 R→C→P 完成 expected-old 收口：R 保持 `eace3155cdc96d6bea3b708255e27f3b28499078`，C 更新为 `eadc4da0c975dbb65489bd990b48524b23489cc5`，P 更新为 `bf1092f11da49ffe4cdaacf148dab7f60d02198d`。P 的 `DeckCompositor` 版本为 **0.9.1**，两层 gitlink 与实际干净工作树一致。
- P 全新默认完整构建通过，compositor CTest 原始日志（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/deckshell-compositor-ctest-attempt-1.log`）为 **55/55，无跳过**；C 基线与候选分别 fresh 构建、安装、CTest **8/8**；安装 consumer **3/3**；**82 个**固定命名空间公共头逐头编译通过。R 两侧分别完成 fresh Meson 构建与安装；R 原生测试、P 顶层测试均如实记录 **NO_TESTS**。
- 安装审批（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/approved-installation-migration.json`）与安装审计（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/waylib-contract-audit.json`）绑定本次真实快照。N7 的已授权原生 tag 实现移除两处重复协议生成入口，实际源码执行上下文差异完整保留；安装路径、导出目标、pkg-config 和公共命名空间不变。
- 前两次正式回放同样完成了 32 个来源，但第一轮 P 配置因 `DISABLE_DDM=ON` 下不存在的 `lockscreen` target 失败；第二轮按实际配置保留条件依赖后，P 完整构建又遇到快捷键测试的错误 wlroots XML 路径。第二轮失败报告（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/sync-report.json`）仍为 `blocked`；当时 R/C、consumer 或安装合同的成功未被用来代替 P 验收，也未提前收口。
- `worktrees/N7-review-3/parent` 的诊断修复包括：快捷键 XML 使用实际嵌套 R；非 DDM 保留 ext-session-lock 判断；DDM 关闭时通过真实 registry 验证 global 缺席；协议测试使用独立短 runtime 路径并关闭私有 D-Bus 的 portal 激活；恢复上游禁用的 foreign-toplevel 测试；继承 canonical XML 目录；QPA 检查跟踪实际 `main.cpp → treelandinit.cpp`；foreign-toplevel singleton 使用实际 DeckShell URI；fixture 等待真实就绪状态；无 locker 时验证锁屏请求不改变 Normal 模式。
- 新增协议测试揭示了非 DDM 模式未初始化 `WallpaperManager` 的生产缺陷。`helper.cpp` 在现有 `/dde` 配置已就绪或成功初始化信号到达时调用既有初始化入口，不改变持久化路径、schema 或 DDM 分支。壁纸诊断测试（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-review-3/diagnostic-wallpaper-7.log`）通过，仍断言请求指定的壁纸值。
- foreign-toplevel 不再以动画 `finished()` 代替最终窗口状态和客户端确认。保留默认动画速度，每个请求只发送一次，在有界协商循环中推进实际帧及 configure/ack/commit，直到目标状态成立且几何动画结束。正向验证（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-review-3/diagnostic-foreign-7.log`） **17/17**；隔离负向对照（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-review-3/foreign-missing-request-control/run.log`）故意不发送取消全屏请求，明确超时并返回 1，仅对应断言失败 **16/17**，证明不会靠等待制造 PASS。对照未修改审核源码。
- 审核提交 `2fba673e6` 的完整 P 诊断测试（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-review-3/diagnostic-all-7.log`）实际执行 **55** 项，**53 通过、2 失败，无跳过**。两项失败均从真实 `PrelaunchSplash.qml:6` 的 `Waylib.Server` 导入错误触发 fatal，最终由 CTest 超时收回；不是协议超时容限不足。此结果仅属于诊断工作树，不能用于正式节点收口。
- **2026-09-14 已获用户精确授权并落实**：将不在固定来源改动清单中的 `compositor/src/core/qml/PrelaunchSplash.qml` 列为 N7 必要集成路径，仅将导入改为 `WaylibShared.QuickSharedServer 1.0`。适配绑定测试引入来源 `cf2dc0a9…`，按 [PRD 第 5 节](prd.md#已授权的-n7-单文件-qml-导入修正2026-09-14)记录；不建立旧 URI 兼容层、不放行整个 QML 目录。原失败用例复验（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-review-3/diagnostic-prelaunch-8.log`） **2/2**，路径审批回归（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-review-4/prelaunch-migration-regressions.log`） **16/16**，随后正式候选全量验收通过。
- 其余诊断修复先折回来源审核（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-review-3/fold-into-source-review.log`），得到审核 P=`7ddcd0c8c03db0bb2672ba162ebf1d71ae3717a9`、C=`a0ef0a0f1150a6d8f107c19bbe857a524de29ca5`；12 个 C 来源合同审核均通过。获批的 Prelaunch 修正随后登记到同一来源（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-review-4/prelaunch-source-integration.log`），在第三轮 journal 创建前完成 decisions；正式回放结果与审核后的诊断内容相符，仅派生 C gitlink 不同。QPA 的本地测试集成路径精确绑定第 4 个来源 `debeeb678…`，未混入普通 inventory。旧 attempts 的身份和证据保持不变。
- 运行依赖为已核对并隔离解包的 DConfig daemon（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-1/runtime-dependency/dependency.json`），未安装系统包。验证采用现有正常产品配置和隔离 headless/DBus 环境，不代表物理设备或真实桌面会话的全面验收；源内无测试的部分不另宣称运行态覆盖。

## 7. 整组交付核对

- 连续性与最终引用核对（外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/node-continuity-check.log`）重新读取本地 Git 对象及七个节点的实际报告、验证与收口记录：六个普通区间连续且互不重叠，**501/501** 个来源恰好各有一个 P 映射；加上独立 N2，共 **502 个**新增 P 提交。N2 原始 R 历史的 **7528 个**提交与导入根树一致，未当作普通来源重复回放。
- 每个普通节点的报告与八项门禁、manifest、验证记录绑定一致，各段 P/C/R 基线等于前段实际收口值。七节点均分别验收通过，不以 N7 的 **55/55** 代替历史节点；最终两层 gitlink、九个 N7 linked checkout 的 SHA 与干净状态已复核。
- 原 C `waylibshared` 仍为 `26f52806c0432c70438a027b7e7659e1cb481b2b`；外层索引 SHA-256 仍为 `53fde58034db3773798a87a522582852b47c70fb0409fc6ca6047b331adca2c5`。未切换主工作树、未暂存或提交外层 gitlink、未 fetch/push/tag。同步工具修订保留在主工作树 WIP，未混入上游逐提交结果。
- 本包同时承载已登记的 Git linked worktree、构建树和含固定绝对路径的验收证据，因此保留原目录，不为归档移动或清理这些路径，避免使已核验的身份和报告引用失效。
