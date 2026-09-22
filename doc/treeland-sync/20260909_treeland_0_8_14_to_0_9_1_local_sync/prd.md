# Treeland 0.8.14 → 0.9.1 本地三仓同步需求

## 留存说明（2026-09-15）

本文件来自外层原方案包 `.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/prd.md`，保留其完整实质正文、原授权、旧 SHA、失败记录及原验收结论。以下历史正文只调整链接定位；外层原件与证据仍留在原位置，没有被本副本替换或搬迁。

- **原同步事实**：N1—N7 的结果属于原报告记载的候选与环境。原文“不重写已同步历史”“只使用本地 URL”等约束保留为当时边界，不回改历史授权。
- **本次限定例外**：2026-09-14 获准对 P 502、C 386、R 332 个历史对应提交整理顶层 `Refs` 及派生父子引用，普通文件不变，R0 的 7528 个原始对象不变；本副本与本仓记录、C 的 R URL 更新均在历史区间之后新增。
- **记录与映射**：[本仓同步记录](summary.md) 区分 Treeland 来源、原目标与新目标。完整旧新映射位于外层 `.helloagents/plans/20260914_treeland_refs_portability/rewrite-map.json`；原三个旧头由各仓 `refs/backup/treeland-refs-portability-20260914/original` 保持可达。
- **工具交付**：仅在 P 末端独立交付来源 `3b1a8ab63c55091b43da2664014fa72636f57f0e` 的完整工具修订、Python 3.9+/CMake 3.27+ 要求及按仓记录生成器；不把新工具插入历史对应区间，不声称其当时用于全部节点。
- **引用语义**：短 `Refs: 20260909_treeland_0_8_14_to_0_9_1_local_sync/plan.md` 供维护者在当前 P/C 交付树查找共同文档，不承诺每个历史提交都已含副本。R 不新增方案副本；R 的短 Refs 是 P/C 共同文档标识，不是 R 仓内相对路径承诺。
- **证据边界**：`evidence/`、日志全集、worktrees、构建和安装树均未复制。标注“外层历史资料”的项只能在原外层方案包查询；“P 仓共享资料”按 P 仓内路径定位。仅有两份 Markdown 不代表独立克隆后可重放原验收。
- **发布边界**：R 的指定 SSH 地址为 `git@github.com:SunRain/waylib-wlroots.git`；本次只配置本地引用与地址，未 fetch/push/tag，未验证远端可达性、对象齐备或跨机器克隆。Git 内容对应核对及工具回归不替代原产品验收。

---

本需求承接 session `01a0818e-2fe1-7570-adba-d6e21b45ccbe` 已确认的决定：保留整体来源范围，导入前后逐提交同步，首次 wlroots 导入独立初始化并验收，采用 7 个必验节点，仅交付本地仓库结果，排除跨机器分发。

最初需求讨论只交付 PRD；实际同步已由 [实施方案](plan.md) 和后续授权承接。2026-09-11 用户明确允许 N5 的 qwlroots → 原生 wlroots 公共合同迁移，具体边界见第 5 节。首次导入仍不能交给普通 replay 隐式处理。

## 1. 目标与范围

维护者需要将本地已有的 Treeland 来源对象同步到 DeckShell 及其依赖仓库，同时保留逐提交追溯、目标项目结构，以及未被第 5 节明确授权迁移的 waylib-shared 公共合同。

- 使用 统一同步技能（P 仓共享资料：`doc/skills/treeland-deckshell-waylib-unified-sync/SKILL.md`），不分别运行旧的父仓、子仓同步流程。
- 来源标识为 DeckShell 仓库中的 `refs/remotes/treeland/master`。
- 整体范围固定为 `(7da2254d386935f753ed907f8d6e76c1639d01a9..fd573cf44fb06ee1eebcdd8c39716d1c797b64d4]`：起点不包含，终点包含。
- 起点是 `0.8.14`，已在目标历史的 `4d38d039aa226273fb0316daa9832396381cdf95` 中留有来源映射，不重复同步；终点是 `0.9.1`。
- 不以当前 `master` 的最新快照覆盖目标，也不随来源 ref 后续移动扩展已确认区间。

### 本轮只读核验的输入快照

以下 SHA 于 2026-09-09 从本地 Git 对象核验；不代表远端最新状态，也不代表产品验收通过。

| 对象 | 完整 SHA |
|---|---|
| 本地 `treeland/master` tip | `cb038ef766940545fd05d0a22578c7e9fbaa7324` |
| P：DeckShell `master-merge-treeland` 当前基线 | `4e5d37c144edee006a7ff2598c243f0f9715b979` |
| C：waylib-shared `waylibshared` 当前基线 | `26f52806c0432c70438a027b7e7659e1cb481b2b` |

P 的 `3rdparty/waylib-shared` 是 mode `160000` 的 gitlink，准确指向上述 C 基线；P/C 工作区当前干净。C 尚无 `3rdparty/wlroots` 登记，`waylibshared-merge-treeland` 尚未创建。实施前重新核验这些输入和目标分支状态，不能静默换用漂移后的基线。

## 2. 本地交付仓库与分支

| 仓库 | 本地目标分支 | 保留要求 |
|---|---|---|
| P：`DeckShell/` | `master-merge-treeland` | 从已核验的现有基线接续，不重写既有历史 |
| C：`DeckShell/3rdparty/waylib-shared/` | `waylibshared-merge-treeland` | 从上述 `waylibshared` 基线新建，保留原分支 |
| R：独立 wlroots 仓库 | `master-merge-treeland` | 从 Treeland 本地已有 Git 对象建立持久仓库 |

R 的唯一内容来源是已确认 Treeland 历史中的 `3rdparty/wlroots/`，不是另选的 wlroots 上游、当前 master 快照或 `UPSTREAM` 文本中的任意版本。该子树在 Treeland 中是普通目录，不是可直接克隆的独立仓库地址。

C 的 `.gitmodules` 中，`3rdparty/wlroots` 地址指向该持久本地 R 仓库，不嵌入凭据。实体仓库路径及对应本地 URL 由实施方案确定：不能位于 `/tmp` 或一次性 replay 工作树内，不能依赖会被删除的临时对象库。该地址只承诺本机可用。未来若开展跨机器分发，须另行配置其他机器可访问的仓库地址；此项不属于本次实施任务。

## 3. 来源路径与逐提交结果

| 来源路径 | 目标归属 |
|---|---|
| 父仓路径策略中的 mapped / root-owned 路径 | P，严格使用策略计算出的规范目标路径 |
| `qwlroots/**`、`waylib/**`、`wlroots/**` | C，保留相对路径，均为普通文件目录 |
| `3rdparty/wlroots/**` | R，去掉该前缀进入仓库根；C 仅以固定同名 gitlink 引用 R |

P 路径以 父仓路径策略（P 仓共享资料：`doc/skills/treeland-deckshell-sync/references/path-policy.md`） 为权威，C/R 扩展以 统一路径规则（P 仓共享资料：`doc/skills/treeland-deckshell-waylib-unified-sync/references/path-policy.md`） 为准。未知路径、未经逐项批准的 review-only 路径、路径类型漂移或目标结构漂移必须阻断，不能用排除列表或证据说明扩大可修改路径。

公共迁移所必需、但未出现在对应上游 diff 中的本地包配置、既有 consumer 和测试调用方，按第 5 节精确登记为迁移集成路径；这是已授权迁移的连带改动，不改变常规来源路径策略，不允许将上游实现搬入兄弟文件或放行任意路径。源明确删除的 `qwlroots/` 不要求在迁移后继续存在。

- 每个普通来源提交只分类一次，再按实际归属依次产生 R → C → P 结果；没有对应内容的层不伪造内容提交。
- R 有更新时，C 的普通内容与新 R gitlink 放在同一对应提交；C 审计通过后才创建 P 提交。
- 仅 C/R 更新时，P 仍创建只修改 C gitlink 的对应提交，并注明“这是一个单纯的 gitlink 变更”；混合提交同时包含授权 P 内容和新 C gitlink。
- 每个相关来源保留完整 SHA、作者、日期、原消息及目标映射。已映射来源不得重复同步；明确无归属的排除项仍需在清单中说明。
- 直接应用须证明来源内容投影一致；适配须有经审核的目标补丁和逐路径证明；等价空提交须有等价证明。不得静默跳过冲突或丢弃来源改动。
- C 的 `wlroots/` 不能改成 gitlink，也不能映射为 `qwlroots/`；P→C 与 C→R 的引用必须指向已存在的真实提交。

## 4. 首次 wlroots 导入的独立边界

首次导入提交为 `1ffe0010193a8c696ef6436a4c436f57bbb1e8ec`，其第一父提交是 `0.8.15`，第二父提交是 `88a869855742281c98c22cab9641b317b8d065ef`。

该 merge 相对第一父提交新增 7529 个可达提交，不是一个可以直接应用的线性来源提交。按已确认的 首次导入边界（P 仓共享资料：`doc/skills/treeland-deckshell-waylib-unified-sync/references/unified-contract.md#首次-subtree-导入边界`），首次导入须独立授权、审核初始化；本次采用独立初始化，不用 first-parent 隐藏历史、不自动逐个回放被合入的 wlroots 历史，也不将 merge 压成普通 replay 提交。

R 初始真实提交确定为 `88a869855742281c98c22cab9641b317b8d065ef`。其根树与导入节点的 `3rdparty/wlroots` 子树均为 `905c266d5caa6a5667806e16b2d656cd0f9f0d9d`，本轮已核验一致；不得把这个 tree SHA 当成 R 的 commit SHA。

初始化必须交付：

1. 持久独立的 R 仓库、真实 R0 及可读取的关联 Git 对象，保留来源历史，不从当前 master 重新制作快照基线。
2. 与导入节点对应的 C0/P0、C 的本地子模块登记和两层准确的 gitlink；保留其他子模块条目，首次登记按结构适配审查。
3. 从导入前已验收结果到导入后三仓基线的可复核对应关系，以及包装层、实际依赖接入和更新脚本的审查结果。
4. 第 5 节 N2 的完整节点验收。仅“根树相等”“R 单独可构建”或创建了 gitlink，均不等于三仓初始化通过。

具体初始化步骤及其证据形式属于后续实施方案；不能伪造现有工具的普通 replay 清单、journal 或 PASS 来跨过 merge 禁令。

## 5. 七个必验节点

| 节点 | 来源快照 | 完整 SHA | 与前一节点的关系 |
|---|---|---|---|
| N1 | `0.8.15`，首次导入前 | `2df4c21c0499b46229f1ef0080cc265994b4fd60` | 从整体起点逐提交同步 28 个非 merge 提交 |
| N2 | 首次导入后的三仓基线 | `1ffe0010193a8c696ef6436a4c436f57bbb1e8ec` | 独立初始化，不走普通 replay |
| N3 | `0.8.16` | `4db6917f873990966f58578abe7dca8b8b371d36` | 从 N2 逐提交同步 21 个非 merge 提交 |
| N4 | `0.8.17` | `24c1a0b547fc8a1c6617bdff147efcbad03c2f98` | 从 N3 逐提交同步 20 个非 merge 提交 |
| N5 | `0.8.18` | `7134887c66e5215182e1a1f648bdc8971f17e864` | 从 N4 逐提交同步 43 个非 merge 提交 |
| N6 | `0.9.0` | `ce57dab0259c33eb183589928249ef9e2be149af` | 从 N5 逐提交同步 357 个非 merge 提交 |
| N7 | `0.9.1`，整体终点 | `fd573cf44fb06ee1eebcdd8c39716d1c797b64d4` | 从 N6 逐提交同步 32 个非 merge 提交 |

上述 Git 祖先顺序和数量已在本轮复核：普通线性分段合计 501 个来源提交，另有 N2 独立初始化。其中，导入后至整体终点共 473 个提交，无 merge。范围必须连续、不重叠、不遗漏；初始化独立处理不缩减用户确认的整体范围。

### 验收粒度

- 每个节点都验收其实际 P/C/R 候选。N1 尚无 R，R 明确为不适用；N2 起必须验收独立 R 和两层依赖关系，不伪造缺失层的 SHA。
- 普通中间提交保留内容、追溯、gitlink 和 C 源码合同检查，但不要求逐提交完整编译，也不能标为构建通过。未精确批准的中间公共合同漂移仍阻断，不因段末恢复而放行。
- 每个必验节点执行适用仓库的完整构建、测试、安装合同与安装包消费验证；不以最后节点成功代替前面节点。
- 任一节点失败即停止，不能跳到下一节点验证后再倒填成功。

### 每个节点必须证明的结果

1. P 完成全新配置、默认完整产品构建及 compositor CTest；C 的分段基线与候选分别完成全新配置、完整构建、安装和必需 CTest。
2. C 候选安装包由已有 `test_project/` 独立配置、构建、测试，并通过固定基线命名空间探针；不借用邻接源码或系统同名安装冒充本次消费链。
3. R 启用后完成适用基线与候选的 Meson 配置、构建、测试，并证明 C/P 的实际编译、生成头和消费目标链接输入使用本次 R，不回退系统 wlroots。N2 同样必须证明三仓真实接入。
4. 默认保持 Waylib 合同（P 仓共享资料：`doc/skills/treeland-deckshell-waylib-unified-sync/references/waylib-contract.md`） 规定的现有核心目标、安装与公共头路径、导出目标及其公共属性、公共命名空间和 pkg-config 合同。以下已授权的公共迁移必须逐项记录实际差异并验证新合同；不能用 consumer 一次通过豁免其他漂移，也不能把批准的迁移写成“无漂移”。
5. 实际工作树中的 C/R 与本节点记录一致，SHA、对象库、两层 gitlink 和干净状态均可复核；不能只核对索引中的指针。
6. 普通分段通过技能的八项结构化门禁及工具生成的完整报告；N2 提供独立初始化方案规定的可复算证明，不能把未经支持的 merge 写成普通分段通过。

必需 CMake 构建不能挑选局部目标、空跑或关闭产品配置来制造成功。必需 CTest/consumer 不能为零测试、跳过或只跑子集。P 顶层或 R 原生工程确无测试时如实记录 `NO_TESTS`，不是 PASS，也不能替代其他必需测试；不适用项必须符合技能的实际条件并留有证明。

各节点使用独立的源码外构建、安装和持久证据目录，不复用上一节点的缓存、安装树或旧 PASS。原始命令、日志、候选 SHA、来源映射及节点结果须可复核；正式证据不能只存 `/tmp`。

### 已授权的 qwlroots → 原生 wlroots 公共迁移

授权依据：用户在 N5 第 31 个来源的合同冲突说明后明确回复“允许这项公共合同迁移”。从 `9582881ddc2e71c73f01eb1f8f5efd0b87a8b107` 接入原生 API，并同步固定区间内该迁移的直接后续实现；不保留旧/新两套包装路径，不伪造旧包或旧头的兼容壳。

- 允许随来源删除 qwlroots 源码、核心 target、安装包、公共头和依赖；允许新增/替换原生 API 所需的 Waylib 公共头、生成配置、native wlroots 包及 CMake/pkg-config 依赖。`WWaylandResource` 等直接后续拆分同样按实际来源节点审核。
- 保留 CMake 目标 `WaylibShared::SharedServer`、现有 C++ `Waylib::Server`（包括 `Waylib::Server::WEvent`）命名空间和 `WaylibShared.QuickSharedServer` QML URI；被删除 qwlroots 包的 `qw` 命名空间明确退休，其余无关公共合同仍按默认规则保护。C/R 的物理仓库、两层 gitlink、来源范围和节点顺序不变。
- 同步改完既有包配置、`test_project/` 和本地测试的旧 API 调用。超出来源 inventory 的连带文件必须逐个列在对应来源的迁移审批与适配证明中，禁止目录通配审批、任意根文件放行或改写 inventory 伪装来源变更。
- 原生库必须包含在既有 QML 运行时安装组件中；其唯一 P 安装入口 `compositor/src/CMakeLists.txt` 可随对应迁移来源逐文件审批，不扩展为其他生产文件或任意 CMake 路径。安装 smoke 仍清除构建树搜索路径验证真实安装产物。
- 源码审批绑定相邻候选的真实快照和全部批准差异；安装审批绑定本节点旧/新真实安装快照、迁移来源及明确的命名空间/头绑定。旧头仅在明确删除清单中退休，保留的命名空间及新公共头必须由安装包独立编译验证。
- 基线仍按旧合同 fresh 验证，候选按迁移后的完整源码、测试和安装消费链验收；必需构建、完整 CTest、失败路径、内容投影、来源追溯和两层依赖检查不获豁免。N1—N4 不回溯放宽、不重写已验收历史。

### 已授权的 N6 公共合同增量（2026-09-12）

用户明确允许固定 N6 来源内的跨进程子表面、相对指针、指针约束公共 API、qtwaylandscanner 迁移及开发文件安装开关调整；不重复请求该范围授权。仅统一实际 CMake 依赖/链接引用为 `WaylibShared::SharedServer`，保留 C++ `Waylib::Server` 命名空间和 `WaylibShared.QuickSharedServer` QML URI。

- 继续逐来源记录精确源码差异及必要集成路径，节点终点完整验收；Waylib standalone 必须保留完整开发文件安装与独立消费，P 顶层的开发文件开关不能使 C 独立开发包缩水。
- qtwaylandscanner 与本地协议输入的迁移可精确适配 P 根 `CMakeLists.txt`、原 scanner 的具体文件及 `protocols/compositor/CMakeLists.txt` 和新增 XML；不改变 inventory，不放行任意生产目录。具体改动仍须列入对应来源的审批和投影证明。
- 协议提取仅采用第 6 节冻结的已授权本地 Git 对象；C standalone 和 P 必须使用本次协议输入，不回退系统 TreelandProtocols。

### 已授权的 N7 单文件 QML 导入修正（2026-09-14）

用户明确采用“修正一行导入名称，并明确批准这一个集成文件”的方案。允许将 `compositor/src/core/qml/PrelaunchSplash.qml` 精确登记为 N7 的必要集成路径，仅把 `import Waylib.Server 1.0` 改为 `import WaylibShared.QuickSharedServer 1.0`，保留既定模块名称、版本和组件行为。

- 适配绑定引入实际桌面协议测试的来源 `cf2dc0a911759ef9cc94fd9d8d81c76f4ccb4769`，使用原有 `contract_migration` 与逐路径投影证明；不改写 inventory，不扩大来源区间，不放行整个 QML 目录或建立旧 URI 兼容模块。
- 同步工具只增加这个具体文件的审批能力，无审批、其他生产路径或与批准补丁内容不符时仍阻断。两个失败用例必须真实复验，N7 的完整构建、全部 55 项 compositor 测试、依赖安装消费和其他门禁不获豁免。

## 6. 协议候选边界

本轮只读扫描的导入前后线性区间没有来源 `protocols/**/*.xml` 改动；这不豁免实际 P 候选的独立检查。

继续遵守 协议追踪规则（P 仓共享资料：`doc/skills/treeland-deckshell-waylib-unified-sync/references/protocol-tracking.md`）：来源协议 XML 或实际 P 的 `protocols/compositor/**/*.xml` 任一发生修改时，使用用户指定的协议仓库与冻结 ref/SHA 查询。用户已更新 `DeckShell` 的 `treeland-protocols` remote，并授权从其对应提交提取所需 XML；本次冻结 `refs/remotes/treeland-protocols/master` 为 `dada26e01c1c6564a961981769df4854e2a4fec5`，不重新 fetch。

N6 `8e41511b7dbc1ad148a23f5817b36527def9ddce` 使用旧 manager 名 `treeland_subsurface_manager_v1`，因此从该冻结历史的引入提交 `8dc1d1e788dc964cd0f756b4491d0225e70b1598` 提取 `xml/treeland-remote-subsurface-unstable-v1.xml`，安装到 P 的现有协议包。remote 最新 `wine/` 文件包含区间外的 manager 更名，不直接使用；不借用系统安装副本。提取来源是已审查的具体输入，tracker 候选仍仅 advisory。

零候选、单候选、多候选均仅是参考信息，不能写成已确认对应，也不因候选歧义阻断内容同步。候选查询本身不授权自动替换协议 XML；未触发也须由工具结合实际 P 映射生成相应证据。

## 7. 分段收口、失败与完成定义

- 后续实施授权覆盖明确的节点和目标分支后，每段完整验收通过即按 R → C → P 更新对应本地分支；R 不适用时为 C → P。后一段只从前一段已收口的真实 SHA 接续。
- 收口须验证目标 ref 未被工作树检出、旧 SHA 符合预期且可快进。目标已移动或仍被检出时停止，不强制覆盖。
- 跨仓和跨节点均非原子操作。后段失败保留此前已通过的分支结果；部分收口失败保留已更新的下层 ref，并按技能记录恢复剩余步骤，不自动回滚。
- 冲突或验证失败保留 worktree、journal 和证据，不自动 reset、abort、清理或改写用户分支。同身份续跑必须满足技能要求，不能修改既有记录来伪造可续跑状态。
- 整组完成必须同时满足：501 个普通来源提交均有归属与处理记录、N2 初始化完整、7 个节点各有独立有效验收结果、分段基线连续、获准的本地目标分支均已收口、最终 P→C→R 对应准确。最后一个报告通过不等于整组完成。

## 8. 明确不做

- 不执行跨机器分发，不建设远端 wlroots 仓库，也不保证本地子模块 URL 在其他机器可用。
- 不自动 fetch，不 push，不创建发布 tag；使用当前本地已有来源对象。
- 不修改、暂存或提交外层 `HA-DeckShell → DeckShell` gitlink；保留外层已有暂存和未提交改动。
- 不修改 C 的原 `waylibshared` 分支，不重写既有同步历史，不将全部来源压成一次快照更新。
- 不扩大来源区间或常规路径所有权；除第 5 节已授权、逐路径登记的公共迁移及必要调用方适配外，不放宽合同，不绕过 merge 限制或自动进行无关重构。
- 不把本 PRD、本轮只读 Git 核验、技能自身测试或隔离夹具结果称为真实同步、产品构建或发布完成。
