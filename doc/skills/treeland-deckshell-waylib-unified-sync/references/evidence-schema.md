# Evidence schema v2

统一工具所有带版本的运行工件均为 `schema_version: 2`；与旧 DeckShell-only evidence v2 不是同一种 kind。旧 v1 journal/manifest/快照不得只改版本字段后续跑，必须按当前工具重新生成。decisions 是不带版本的输入对象。

## Inventory 与三仓身份

`treeland-deckshell-waylib-unified-inventory` 冻结 source_repo、range.base/head/source_tip、ordered_source_commits/ordered_sha256、merge_commits、path_policy.path/sha256、approved_review 和 counts。

`child_owned_roots = [qwlroots, waylib, wlroots]`，`wlroots_owned_root = 3rdparty/wlroots`。每项保存原始 status/old/new、deckshell 的 included/mapped_source_paths/root_source_paths/target_paths/drop_paths、waylib_shared 的 included/source_paths/drop_paths、wlroots 的 included/source_paths/target_paths/drop_paths 和两个 protocol 路径数组。waylib_shared.included 包含 R 引起的依赖变化。

`treeland-unified-replay-journal` 绑定不可变 identity、当前 P/C/R HEAD、每层 checkpoint、单调 sequence 和阻断阶段。manifest kind 为 `treeland-unified-sync-manifest`，保存 final_parent_head/final_child_head/final_wlroots_head，以及每来源的 wlroots/child/parent、gitlink、nested_gitlink。

`identity.wlroots` 不适用时必须为 null；激活时包含 repo、worktree、common_git_dir、base、target_ref、submodule_url、固定 gitlink_path、registered_at_base、source_base_tree、baseline_proof。C/P common Git directory 也独立绑定，不允许同一对象库冒充不同仓库。

## R 基线证明

来源与 R0 完全相等时 baseline_proof 可为 null；有审核后的差异时，`--wlroots-baseline-proof` 读取的是工件记录 `{path,size,sha256}` JSON，该工件正文为：

```json
{
  "source_tree": "<range_base:3rdparty/wlroots tree SHA>",
  "target_tree": "<R0 tree SHA>",
  "review_state": "approved",
  "paths": [{"path": "<R 根相对路径>", "reason": "<该差异的审核依据>"}]
}
```

paths 必须按字典序覆盖全部 type/mode/blob 差异。来源子树不存在时 source_tree 为 null，R0 必须为空树 commit，不允许用证明把任意非空仓库放行。

此处 `baseline_proof` 只解释内容投影差异，不授权构建豁免；空 R 基线的命令记录须另由工具重读 Git 对象，见下文。

## Decisions 与结构适配

唯一根结构为 `{"entries": {"<source-sha>": {"wlroots|child|parent": {...}}}}`。每个 SHA 只能声明实际拥有的 lane。示例见 [decisions.example.json](../examples/decisions.example.json)；其中的大小和摘要必须替换为 `artifact_record.py` 的真实输出。

普通字段为 action、adaptation_notes、adaptation_paths、adaptation_patch、equivalence_proof。action 只接受 applied/adapted/empty。adapted 必须有目标相对补丁和有序逐路径证明；empty 必须有等价证明。

| 字段 | 合同 |
|---|---|
| path | P 使用映射后路径，C 保留原相对路径，R 使用去掉 3rdparty/wlroots 前缀的路径 |
| kind | modified：原存在且发生修改/删除；materialized：原不存在且创建；omitted：不进入实际 diff |
| reason | 非空单行审核理由 |
| proof | 内容寻址工件，覆盖该路径的取舍 |
| review_state | approved；不能替未完成的审核代填 |

C 仅可在 R 模式的 adapted 决策中指定 `structural_paths: ["CMakeLists.txt"]`；把这个路径追加在 inventory 普通目标路径之后并提供同样的逐路径证明。`.gitmodules` 和 R gitlink 由工具生成并精确核验 transition，不允许 adaptation patch 任意改写。

新增 wrapper 核心/安装/导出定义还需 child `contract_additions` 工件，正文绑定逐节点源码快照：

```json
{
  "review_state": "approved",
  "before_snapshot_sha256": "<源码基线快照 canonical SHA-256>",
  "after_snapshot_sha256": "<该 C 节点源码快照 canonical SHA-256>",
  "additions": {"core_targets": ["<实际新增 wrapper target>"]}
}
```

additions 精确覆盖全部 drift.added；旧值不得删除、重命名或改变，新增项必须来自 wrapper，公共 namespace 不可借此变化。安装审计的 `--approved-additions` 则读取另一份正文 JSON：相同两侧安装快照摘要、完整 drift、review_state、非空 reason、全部新增 installed_paths。两类批准不可混用，不能只写 adaptation note 代替。

## Lane evidence 与提交消息

C/R/P kinds 分别为 treeland-unified-waylib-evidence、treeland-unified-wlroots-evidence、treeland-unified-parent-evidence。每项含 source_commit、target_commit、classification、action、drop_paths、adaptation_notes、adaptation_paths 和 artifacts。

C/R 额外保存 content_action、structural_paths、nested_gitlink（仅 C）。C 的 overall action 可因首次登记成为 adapted，普通内容仍是 applied；R-only 的 C 可为 gitlink-only/content=not-applicable。非 adapted 普通内容不带 adaptation_paths。

artifacts 保存 source_patch、target_diff；C 必需 source_contract_audit，R 必需 source_audit；adapted 另有 adaptation_patch，empty 的 equivalence_proof 放 evidence 顶层。P 使用 mapped_source_patch/root_source_patch，并保存 target_paths、child_commit、gitlink。

nested_gitlink 记录 status=registered/updated/unchanged、from/to、冻结 URL、gitmodules_before/after SHA-256；首次登记 .gitmodules 必须只新增指定条目，既有条目字节保留。两层 gitlink 对象都必须在正确的下层仓库实际存在且为 commit，不能只信 ls-tree 的 mode。

工件 path 相对 artifact_root，禁止绝对路径、.. 或逃逸；size 和 SHA-256 必须匹配。applied/adapted 分别从目标父树重放来源/获批 adaptation_patch 并比较 type/mode/blob；adapted 另核对路径语义与消息。C 的精确 structural_paths 参与适配投影，派生登记/gitlink 单独验证。empty 有审核证明且保留空提交。详见 [提交消息](commit-messages.md)。

## 合同快照与固定命名空间探针

C source_contract_audit 绑定相邻 Git commit、两侧源码快照/摘要、drift、approved_additions 和结果；`cmake_execution_context` 有序保存路径、条件/作用域及公共调用，含相关变量定义、入口与 helper 调用。顺序变化也属于漂移，不能由集合比较消除。恢复与 verifier 重算；缺少该字段的旧源码快照须重新生成，不能补字段、重哈希或靠后续恢复原状放行。

waylib-install-contract-snapshot 保存安装路径、public_headers、file_sha256、CMake package、导出 target/namespace、pkg-config、public_namespaces、namespace_headers 及 source_contract。exported_target_properties 来自实际 CMake 求值，只归一化本次安装根，保留列表顺序和生成器表达式。

`pkg_config` 按安装相对 .pc 路径覆盖全部包；每项为原生求值后的 Name、Version、Requires、Requires.private、Cflags、Libs、Cflags.static、Libs.static 字符串。动态/静态参数包含实际依赖，保留参数顺序，仅归一化安装根。缺求值字段的旧快照直接阻断，不能补字段、重哈希冒充本次查询。

waylib-fixed-namespace-probe 绑定两侧快照摘要、固定基线全限定 namespace 的 probe.cpp 及 configure/build 日志。源码预处理保留项目 include、宏条件和 undef；外部头由最终编译探针验证。candidate consumer 使用自身宏能编译，不代表固定基线 namespace 存在。

## 递归物化与命令记录

treeland-unified-child-materialization 绑定 manifest 摘要、P/C/R heads、P 下 C checkout；wlroots_checkouts 必须含 child_base、child_candidate、parent_candidate。每个适用项保存 path/head/common_git_dir/linked_worktree/clean；旧基线未登记 R 时 child_base=null；R 不适用时三个值均 null。

treeland-unified-command-validations 保存当前 entries 与 previous_attempts。执行型记录包含 id/category、参数数组、cwd、exit_code、内容寻址 log、git_identity before/after、fresh_paths。R 模式必需 manifest_sha256 和 checkout_identity before/after，包含源工作树及所有实际依赖；P 还保留兼容的 nested_checkout 字段。

`deckshell-build`、`waylib-base-build`、`waylib-candidate-build`、`waylib-package-consumer-build` 只允许默认完整 CMake build；可附配置、并行数、详细输出和 clean-first，不允许 target 选择、原生参数、帮助和空跑。记录器执行前和报告端独立核验同一规则；诊断 ID 的结果不替代这四项。

固定 CMake configure 的 -B、install 的 --prefix、Meson setup 的 meson-build 在执行前必须不存在；构建/安装与 P/C/R 工作树不重叠，base/candidate 独立。`--manifest` 使记录器在写 CMake query 前拒绝越界。fresh_paths 必须匹配命令解析出的绝对路径。

CTest 记录无过滤 --show-only=json-v1 的命令和原始发现日志、完整测试集合以及 test_results。支持旧摘要与 CTest 4.4 的 `100% tests passed out of N`；按测试编号去重，Not Run 为失败，Skipped/Disabled 不算通过。日志、计数、JSON、发现集合不一致或只运行子集都失败。

consumer 独立审计重读已哈希的日志，要求非零、全通过、无跳过，与 bundle 当前 attempt 完全相同。不能以 exit 0 或手写 outcome=pass 放行。

R 的 native_discovery 来自 Meson introspect --tests，native_test_log 保存当前执行 JSON 的 name/result/returncode 投影，不复制进程环境。记录器注入 `--logbase=treeland-<id>-attempt-<N>`；`native_log_identity = {path: <该 build/meson-logs 下对应 JSON 绝对路径>, existed_before: false}` 绑定命令和 ID/attempt。旧默认 testlog.json、只列举模式、缺少或失配的日志身份均不能放行；旧记录须实际重跑，不能补写 freshness。结果核对全量发现集合，零注册测试仍为 NO_TESTS。

仅 `wlroots-base-configure`、`wlroots-base-build`、`wlroots-base-test` 允许 `outcome: not-applicable`，且三个记录必须齐全。它们保留计划命令、cwd、attempt、Git/manifest/checkout 身份，明确 `executed: false`、`exit_code: null`；没有测试计数、Meson 发现/结果日志或 `fresh_paths` 执行证据。`native_baseline` 与内容寻址 `log` 的 JSON 正文必须同为：

```json
{
  "reason": "absent-source-subtree-and-empty-r-base",
  "source_base": "<首个来源节点唯一父提交的完整 SHA>",
  "source_path": "3rdparty/wlroots",
  "source_tree": null,
  "wlroots_base": "<真实 R0 commit SHA>",
  "wlroots_tree": "<R0 的整个空根树 SHA>"
}
```

记录器与报告从冻结 Git 对象重新证明上述两项事实，不接受只改 JSON、重哈希日志或删除 `meson.build` 来获得豁免。记录器 exit 0 表示证明已核验、记录已写入，不表示 Meson 已执行；报告显示 `NOT_APPLICABLE` 而非 PASS/NO_TESTS。R 候选及 C/P 不能使用此状态，两个 R gate 仍为 `verified`，不是 R lane 整体不适用。

C/P wrapper_build 保存 codemodel、compile_commands、Ninja 命令、真实编译依赖和生成头摘要，绑定 manifest。报告按具体消费目标的 codemodel 链接库及真实链接命令输入核验完整产物路径，不用全局产物名搜索，也不把纯构建顺序关系当作链接；系统 wlroots 仍拒绝。

## 报告与收口

八个 gate 名称固定为：

```text
deckshell_verify
waylib_verify
wlroots_verify
gitlink_verify
nested_gitlink_verify
protocol_tracking
contract_audit
child_materialization
```

两个 R gate 不适用时仍由 wlroots_verify.py 核验并输出，不省略或伪造。report 保存三仓候选、replay_identity、inventory/manifest/gate/validation digests 与 Markdown 工件；重算合同快照、consumer、递归物化与真实验证绑定。缺任一必需项、错误的 not-applicable、失败或篡改都 blocked。

`build_scope = {kind: range-head-only, source_head: <本段 range.head 完整 SHA>}` 明确只验收本段终点对应候选及必需基线；普通中间提交不要求构建，不证明其他 tag 已通过。closeout 拒绝缺少该范围声明的旧报告；须通过当前生成器重新验收，不是手填字段升级。多节点汇总只在已有 refs_doc 中链接各段真实报告，不新增能替代它们的全局 PASS 工件，见 [分段规则](key-node-validation.md)。

treeland-unified-closeout-journal 保存 R/C/P expected-old CAS 身份、更新标记、事件与部分失败。完整 report 通过不是收口授权；获准后只更新未被检出的指定 refs，不自动回滚或 push。
