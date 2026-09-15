# 统一分类与回放合同

## 范围与所有权

每次仅处理显式左开右闭 `(base..head]`，冻结完整 SHA，检查 `base <= head <= source_tip`，按 `git rev-list --reverse --topo-order` 回放。整体范围按 [关键节点](key-node-validation.md) 拆为连续分段，每段终点完整验收，不要求普通中间提交编译。merge 仍阻断。`source_ref` 是可省略的说明，不要求 remote 名称或 URL，不自动创建或刷新 remote。

| 来源 | 仓库 | 目标表示 |
|---|---|---|
| path-policy mapped/root-owned | P：DeckShell | 保留外部权威的规范映射 |
| 显式批准的 review-only | P | 按 policy_key 批准，不扩展其他路径 |
| `qwlroots/**`、`waylib/**`、`wlroots/**` | C：waylib-shared | 保留完整相对路径的普通文件 |
| `3rdparty/wlroots/**` | R：独立 wlroots | 去掉该前缀的普通文件；C 只登记子模块并记录 R commit |
| 明确 excluded 且无 owner | 无 | unowned-skip，不创建提交 |
| unknown、未批准 review-only、受管根类型漂移 | 未决 | blocked |

固定两条边为 P 的 `3rdparty/waylib-shared` 和 C 的 `3rdparty/wlroots`。C 的 `wlroots/` 不能成为 gitlink，也不映射为 `qwlroots/`。协议触发独立于 owner；候选不授权替换 XML。

| P 内容 | C 内容 | R 内容 | classification | 顺序 |
|---|---|---|---|---|
| 无 | 无 | 无 | unowned-skip | 无提交 |
| 有 | 无 | 无 | deckshell-only | P |
| 无 | 有 | 无 | waylib-only | C→P |
| 无 | 无 | 有 | waylib-only | R→C→P |
| 无 | 有 | 有 | waylib-only | R→C→P |
| 有 | 有 | 无 | dual | C→P |
| 有 | 无 | 有 | dual | R→C→P |
| 有 | 有 | 有 | dual | R→C→P |

`wlroots-wrapper-only`、`wlroots-submodule-only`、`wlroots-dual` 仅是场景名称，不是新 classification。`dependency-only` 不是统一分类。

## 初始化

来源触及任一种 wlroots 路径，或 C 基线已有 R 时，必须提供 R repo/base/ref/worktree/submodule URL。旧两仓区间且 C 无 R 时不要求无关输入；R 身份为 null，两个 R gate 均由工具生成 not-applicable 结果。

R0 必须是独立仓库中的 commit，根树与来源 `range_base:3rdparty/wlroots` 的路径、mode、blob 投影相等；差异需要绑定两棵树和每个差异路径的预先审核证明。来源基线无该子树时只接受明确准备的空树 commit。不能把源 tree SHA、纯上游 UPSTREAM pin 或某个碰巧可编译的 commit 当成 R0。

P0 gitlink 必须等于 C0。已有 C0→R0 时校验 mode、SHA、path、URL 和对象库。尚未登记时，在第一个需要 R 的 C 节点生成 `.gitmodules` 登记和 gitlink，保留其他条目；wrapper-only 指向 R0，不创建虚假的 R 来源提交。

### 首次 subtree 导入边界

普通目录映射不等于支持 Git subtree 的首次合并导入。Treeland 的历史提交 `1ffe0010193a8c696ef6436a4c436f57bbb1e8ec` 有两个父提交；其 `(M^1..M]` 含 7529 个提交，不是一个普通目录新增。包含此类 merge 的区间仍阻断，不能改用 first-parent 隐藏被合入历史，也不能自动展开或压成单提交回放。

首次导入须单独授权、审核初始化：选择已完成 subtree 导入的来源基线，准备与其投影相符的真实 R0、C0/P0 及依赖绑定，审核包装层接入和更新脚本，再处理后续非 merge 区间。该初始化不由本 skill 自动实施。空树 R0 仅适用于来源基线确无该子树、后续提交本身符合非 merge 规则的线性导入，不是上述历史 merge 的例外。

## 逐节点 child-first 回放

每个来源先完成 R 内容提交及投影审计，再在同一个 C 提交中写普通内容和该节点的新 R gitlink，完成 C 源码合同审计后才创建 P。仅 C/R 更新时，P 仍创建纯 C gitlink 提交，并写“这是一个单纯的 gitlink 变更”；mixed P 同时写内容和 gitlink，并写“此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新”。

上层只引用已经存在的下层 SHA；R/C 使用 `parent association: manifest-only`，不为获得未来父 SHA 而 amend。manifest 保存三仓完整映射、action、sequence 及两层 gitlink from/to。来源作者、日期与时区、完整原消息和 Treeland-Commit 保留。

rename 的 old/new 分别是删除/添加，均判断 owner；copy 的 old 只保留来源关系，只有 new 是实际变更。P/C/R 使用同一语义，不能因 copy 生成虚假的 old-owner 提交或越界报错。

- applied：binary/no-renames 来源补丁；独立 index 在目标父树重放，核对每条授权路径的 type/mode/blob，而不是仅比路径或 diff 哈希。
- adapted：只应用经审核的目标相对补丁；从目标父树重放该补丁，核对实际 type/mode/blob。按 inventory 顺序解释每个 ordinary-content 目标路径的 modified/omitted/materialized、reason、proof、approved 状态，派生 gitlink 不混入补丁投影。
- empty：经审核的等价证明加可追溯空提交；相关 owner 仍保持 1:1，依赖指针随该空提交传播。
- gitlink-only：P 只改 C gitlink，或 C 已登记且只改 R gitlink；首次 `.gitmodules` 登记必须 adapted。
- not-applicable（节点动作）：仅表示该节点没有对应普通内容或 R lane，不冒充 empty、skipped 或成功回放；命令记录的空 R 基线例外见下文。

C 的 overall action 与 `content_action` 分开：首次登记可为 adapted/content=applied；R-only 传播可为 gitlink-only/content=not-applicable。派生 `.gitmodules`/gitlink 由冻结 URL、真实 transition、消息和 diff 精确核验；不把它们混入普通源码的 adaptation_paths。默认唯一额外普通目标路径是显式审核的 C 根 `CMakeLists.txt`；另获公共迁移授权时，可通过 `contract_migration` 精确登记必要的本地包配置、consumer 与 P 测试调用方及现有 `compositor/src/CMakeLists.txt` 运行时安装入口，以及已授权 scanner/协议迁移的 P 根 `CMakeLists.txt`、`qtwaylandscanner/CMakeLists.txt`、`qtwaylandscanner/qtwaylandscanner.cpp`、`protocols/compositor/CMakeLists.txt` 和 `protocols/compositor/xml/treeland-remote-subsurface-unstable-v1.xml`，仍须完整逐路径证明，不改变普通 owner，见 [证据格式](evidence-schema.md#显式公共合同迁移)。

另有明确的单文件 QML 授权时，允许将既有 `compositor/src/core/qml/PrelaunchSplash.qml` 的导入修正登记到对应来源的 `contract_migration`。仅映射为既定 `WaylibShared.QuickSharedServer 1.0`，不放行其兄弟文件、不建立旧 URI 兼容层；仍执行完整逐路径投影验证。

## Journal 与恢复

schema_version 为 2。identity 绑定 source repo、P/C/R 工作树与 common Git directory、基线、R target ref/URL/基线证明、inventory/decisions 摘要、run-id、refs_doc。旧 schema journal 直接拒绝，不填默认 SHA。

每层提交后原子写 journal，再进入下一层。resume 要求完全相同的身份、三个当前 HEAD 与历史、两层 gitlink transition、事件顺序、clean linked worktree；重算已完成 R/C 审计。C 源码合同包含公共调用及相关变量定义的执行上下文，`if(FALSE)`、入口删除或提前 return 不能靠相同调用文字绕过。任何中间失败不由后续恢复合同的提交抵消。

更新脚本的保留、普通文件类型和拒绝前缀在 C 暂存树、提交后、恢复及独立验证中均从 Git 对象核验。旧版已批准的 `omitted` 或旧 PASS 不能豁免该规则；失败时不得创建对应 P。

三个基线都扫描 Treeland-Commit 及旧 `(cherry picked from commit …)` 标记，范围内已映射来源阻断；不恢复 already-synced、partial-prefix 或 history-rewrite 状态机。内容冲突保留现场，以新 worktree/run-id 和已审核补丁重开，不自动 reset/abort/清理。

## 验证与收口

单段报告只证明其来源终点对应的候选；不能替代其他所选 tag 的独立验收。每段通过且获准收口后，新目标 SHA 才成为下一段基线。完整组完成要求所有冻结节点的报告、分段接续及获准收口均有效，详见 [分段规则](key-node-validation.md)。

构建前物化 C baseline（仅已登记 R 时）、C candidate、P candidate 的 C/R。已有 checkout 仅验证；缺失/空目录才创建本地 detached linked worktree。每条验证命令前后重查实际依赖，不能只证明索引 gitlink 正确。

四个必需 CMake build ID 只能执行默认完整构建，不接受目标选择、原生工具参数、帮助或空跑；不能通过关闭必需产品配置来绕过。pkg-config 合同比较本次安装树实际展开的依赖与动态/静态参数，查询失败或旧字面快照均不放行。

完整报告要求八项 gate、C base/candidate fresh build/install/CTest、已有 test_project consumer、固定基线命名空间探针、P build/compositor CTest；R 激活时还要求 R base/candidate Meson 记录和 C/P wrapper 的实际消费目标链接输入。仅当 Git 对象证明来源基线无该子树且 R0 整个根树为空时，三个 R 基线记录可由工具生成 `not-applicable`，明确未执行并保存证明；否则必须有当前执行日志。R 候选、C/P 验证及两个 R gate 不获豁免。仅构建顺序依赖、自身产物输出和复用旧测试日志都不算证据。R 零注册测试如实 NO_TESTS，不等于基线不适用，不能替代构建或豁免必需 CTest。

另获收口授权后，closeout 时的已激活仓库的完整 `refs/heads/**` 必须未被检出，且满足 expected-old 和可快进关系；按 R→C→P CAS。部分成功保留已更新下层 ref，失败记入 journal，同身份 resume 只续作剩余部分，不自动反向 reset。

只写指定工作树、证据目录、构建物化目录和获准的本地 refs。不操作外层 HA-DeckShell、远端 refs、tag 或 push；fixture 通过不表示真实来源区间或产品构建已完成。
