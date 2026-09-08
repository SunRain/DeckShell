---
name: treeland-deckshell-waylib-unified-sync
description: 将指定 Treeland ref 的显式左开右闭 commit 区间逐提交同步到 DeckShell、waylib-shared 和嵌套 wlroots 仓库，按所选关键节点分段验收；用于统一同步、恢复回放、核验两层 gitlink 与安装合同、追踪协议候选。不要求普通中间提交编译，不猜来源范围，不自动远程发布。
---

# Treeland → DeckShell + waylib-shared + wlroots 统一同步

## 顶部铁律

1. 每次运行只处理显式 `(range_base..range_head]`：左侧不包含，右侧包含，冻结完整 SHA。按 [关键节点规则](references/key-node-validation.md) 将整体范围拆为连续分段；所选节点及整体终点必验，普通中间提交不要求构建。
2. 每个来源提交只扫描一次，再分出 P（DeckShell）、C（waylib-shared）和条件启用的 R（独立 wlroots 仓库）。禁止拼接两个旧 skill 的独立分类结果。
3. `qwlroots/**`、`waylib/**`、`wlroots/**` 保留相对路径进入 C 的普通文件；仅 `3rdparty/wlroots/**` 去前缀进入 R。P 路径仍由外部 `treeland-deckshell-sync/references/path-policy.md` 决定；未知路径、普通目录变 gitlink 等类型漂移继续阻断。
4. 分类只允许 `deckshell-only`、`waylib-only`、`dual`、`unowned-skip`；输入缺口使用 `blocked`。禁止再用 `dependency-only` 表示 child-owned 内容。
5. 每个相关来源节点严格 R（若有变化）→ C（内容与 R gitlink 同一提交）→ P。R 内容审计、C 源码合同审计失败都不得推进上层。`waylib-only` 的 P 只能改 C gitlink；`dual` 的 P 同时包含授权内容和 C gitlink。
6. 上层只引用已存在的下层 commit；R/C 不引用未来父 SHA。完整三仓映射写 manifest/report。C 的首次 `.gitmodules` 登记是 `adapted`，不是纯 gitlink 变更。
7. 协议追踪由两类事实独立触发：来源提交实际修改 `protocols/**/*.xml`，或 parent candidate 实际修改 `protocols/compositor/**/*.xml`。treeland-protocols 的零、单、多候选都是 advisory；多候选不得伪装成唯一确认提交。
8. replay 只写显式、互不重叠的 linked worktree；artifact/build/install 位于源码工作树之外。正式证据不得只放 `/tmp`；临时 fixture 的例外不用于真实同步。
9. 失败时保留 worktree 与 journal，不自动 reset、abort、清理、回滚或改写用户分支。`--resume` 只接受完全相同的冻结身份和与 journal 一致的 clean HEAD。
10. 不改外层 `HA-DeckShell -> DeckShell` gitlink，不自动 fetch、push、tag。每段完整报告通过且授权覆盖该段后，显式执行 R→C→P expected-old CAS，再接续下一段；跨仓及跨分段不原子，不自动回滚。

## 按需读取 references

- 开始前读取 [关键节点分段验收](references/key-node-validation.md)、[统一合同](references/unified-contract.md) 与 [路径策略引用](references/path-policy.md)，再加载其中指向的 DeckShell 权威 path-policy。
- 准备 replay 或 adapted/empty 决策时读取 [提交消息](references/commit-messages.md) 与 [证据格式](references/evidence-schema.md)。
- inventory 触达协议目标时读取 [协议候选](references/protocol-tracking.md)。
- 存在 child lane 时读取 [Waylib 合同](references/waylib-contract.md)。
- 不要把所有 reference 内容复制进上下文；仅在进入对应阶段时读取。

## 必需输入

```yaml
source_repo: <包含用户手工指定来源对象的本地 DeckShell Git 仓库>
source_ref: <可选、可省略的来源标识；仅作记录，不要求 remote 名称或 URL>
source_tip: <用户手工输入并可解析的来源 tip ref 或完整 SHA>
range_base: <当前分段的完整或可解析 SHA；不包含>
range_head: <当前分段的必验终点 SHA；包含>
parent_target_ref: refs/heads/<DeckShell 本地目标分支>
child_repo: <DeckShell/3rdparty/waylib-shared 的 Git 仓库>
child_target_ref: refs/heads/<waylib-shared 本地目标分支>
parent_worktree: <显式 linked worktree>
child_worktree: <显式 linked worktree>
artifact_root: <所有 replay worktree 外、非 /tmp 的持久目录>
run_id: <本次唯一且稳定的标识>
refs_doc: <持久方案或审计文档路径>
```

来源涉及 `wlroots/**`、`3rdparty/wlroots/**`，或 C 基线已登记 R 时，以下输入缺一不可：

```yaml
wlroots_repo: <已有本地独立 Git 仓库>
wlroots_base: <与来源 range_base 子树投影绑定的完整 commit SHA>
wlroots_target_ref: refs/heads/<R 目标分支>
wlroots_worktree: <独立 linked worktree>
wlroots_submodule_url: <登记到 C/.gitmodules 的无凭据目标 URL>
```

R0 必须是真实 commit，不是来源 tree SHA 或未经证明的 `UPSTREAM` pin。基线允许有逐路径审核证明，格式见 [证据格式](references/evidence-schema.md)。旧两仓区间且 C 无 R 时不提供这些参数，R gate 明确 `not-applicable`，不填假 SHA。

来源基线无 R 子树时只接受真实空树 R0；其构建豁免必须由 Git 对象证明，不能靠缺少 `meson.build` 推定。首次 subtree 导入若是 merge，须在单独授权、审核的初始化中建立导入后的基线，再同步后续非 merge 区间；空 R0 不开放 merge 回放，见 [初始化边界](references/unified-contract.md#首次-subtree-导入边界)。

协议触发时还需要：

```yaml
protocol_repo: <包含用户手工指定协议来源对象的本地 Git 仓库>
protocol_ref: <用户手工输入并可解析的协议 ref 或完整 SHA>
```

完整示例见 [unified-sync.example.yaml](examples/unified-sync.example.yaml)。整体范围和关键节点清单记入 `refs_doc`；该 YAML 是输入清单，不是脚本配置文件。公开 CLI 仍逐段接收范围，按 `--help` 调用，不接受清单自动调度参数。

## 顺序检查清单

- [ ] 冻结来源 tip、整体范围、关键节点清单及本段范围；确认所有分段连续且通过预检，再冻结本段协议 ref（若触发）与 P/C/R 目标 SHA；不检查 remote 名称或 URL。
- [ ] 确认 P0→C0；R 启用时核对 R0 来源子树投影、已有 C0→R0、登记 URL 和独立对象库。
- [ ] 生成一次统一 inventory；`outcome` 必须为 `pass`。
- [ ] 人工复核 `unowned-skip`、review-only 批准、rename 两侧，以及 copy 的 old 来源关系与 new 实际变更。
- [ ] 建立两个或三个 clean linked worktree；证据目录位于其外且可持久保存。
- [ ] 按 inventory 逐节点 R→C→P 回放，审计不过不推进上层。
- [ ] 运行 P/C/R 内容验证与两层 gitlink 验证；确认 `applied` 投影、`adapted` 逐路径证据和每个 C 合同审计均有效。
- [ ] 协议触发时冻结 protocol ref 后生成 advisory 候选；未触发时写 `not-triggered` 证据。
- [ ] 物化 C 基线、C 候选及 P 候选的依赖；对 C base/candidate 分别 fresh build/install/CTest，运行已有 `test_project` consumer 和固定基线命名空间探针。
- [ ] R 启用时取得 base/candidate 六条 Meson 记录；仅经 Git 证明的空 R 基线记 `not-applicable`，候选仍实际执行，核对 C/P 编译数据库、生成头和链接命令使用本次 R。
- [ ] 对 parent candidate fresh configure/build/CTest；顶层 0 tests 原样记为 `NO_TESTS`，不能写成 PASS。
- [ ] 报告生成器结果必须为 `pass`；不得手写补成 PASS。
- [ ] 八项 gate 和本段完整报告通过且授权覆盖后，目标 refs 未被检出时执行 R→C→P closeout；新 SHA 成为下一段基线。
- [ ] 逐段复核 refs、gitlink、journal 和节点报告；未验节点不得用最后一段 PASS 替代，保持 remote push 为未执行。

## 1. 冻结输入

`source_ref` 是可选的来源标识，不是脚本必须接收的 remote 参数；`protocol_ref` 同样只描述协议来源。真正参与解析的是调用者手工提供的 `source_tip`、`range_base`、`range_head` 和（协议触发时）`protocol_ref` 对应的 `--protocol-head`。这些值可以是本地分支、任意 remote-tracking ref、tag 或完整 SHA；skill 不要求名称为 `treeland` 或 `treeland-protocols`，不从 URL 推断来源身份，也不会自动创建或刷新 remote。若对象尚未存在，用户必须先在 skill 外准备可解析的本地对象；随后立即冻结：

```bash
SOURCE_TIP_REF="<用户提供的 source_tip ref 或完整 SHA>"
SOURCE_TIP="$(git -C "$SOURCE_REPO" rev-parse "$SOURCE_TIP_REF^{commit}")"
BASE_SHA="$(git -C "$SOURCE_REPO" rev-parse "$RANGE_BASE^{commit}")"
HEAD_SHA="$(git -C "$SOURCE_REPO" rev-parse "$RANGE_HEAD^{commit}")"
PARENT_BASE="$(git -C "$SOURCE_REPO" rev-parse "$PARENT_TARGET_REF^{commit}")"
CHILD_BASE="$(git -C "$CHILD_REPO" rev-parse "$CHILD_TARGET_REF^{commit}")"
git -C "$SOURCE_REPO" merge-base --is-ancestor "$BASE_SHA" "$HEAD_SHA"
git -C "$SOURCE_REPO" merge-base --is-ancestor "$HEAD_SHA" "$SOURCE_TIP"
git -C "$SOURCE_REPO" ls-tree "$PARENT_BASE" -- "3rdparty/waylib-shared"
```

`ls-tree` 必须得到 `160000 commit $CHILD_BASE`。禁止用当前分支名替代后续命令中的冻结 SHA。若用户提供的 ref/SHA 无法解析，直接阻断；不以默认 remote 名称补齐。`source_ref` 省略时，不影响手工 `source_tip`、范围端点和协议 ref 的解析。

## 2. 生成统一 inventory

```bash
python3 "$SKILL_DIR/scripts/unified_sync.py" inventory \
  --repo "$SOURCE_REPO" \
  --base "$BASE_SHA" \
  --head "$HEAD_SHA" \
  --source-tip "$SOURCE_TIP" \
  --policy "$SOURCE_REPO/doc/skills/treeland-deckshell-sync/references/path-policy.md" \
  --output "$ARTIFACT_ROOT/inventory.json"
```

review-only 路径只可按 inventory 指出的 `policy_key` 重跑并逐项追加 `--approve-review <policy-key>`。任何 merge、unknown、未批准 review-only 或路径类型漂移都必须先阻断；不得靠 drop list 掩盖。`wlroots/**` 不映射为 `qwlroots/**`，也不是 C 中的子模块路径。

## 3. 建立隔离 worktree

从冻结 SHA 建立专用工作分支。路径必须不存在，且不得复用主工作树或旧 journal：

```bash
git -C "$CHILD_REPO" worktree add -b "$CHILD_WORK_BRANCH" "$CHILD_WT" "$CHILD_BASE"
git -C "$SOURCE_REPO" worktree add -b "$PARENT_WORK_BRANCH" "$PARENT_WT" "$PARENT_BASE"
```

此阶段不要在 parent worktree 内初始化 child 子模块；replay 使用 index gitlink，不会触碰主工作树中的子模块 checkout。

为后续命令定义条件参数；两仓模式保留空数组。R 模式先提供并冻结上面的输入，再执行条件块：

```bash
WLROOTS_REPLAY_ARGS=()
WLROOTS_VERIFY_ARGS=()
WLROOTS_MATERIALIZE_ARGS=()
WLROOTS_CLOSEOUT_ARGS=()
# WLROOTS_BASE 已验证为来源基线投影；仅 R 模式执行。
if test -n "${WLROOTS_REPO:-}"; then
git -C "$WLROOTS_REPO" worktree add -b "$WLROOTS_WORK_BRANCH" "$WLROOTS_WT" "$WLROOTS_BASE"
WLROOTS_REPLAY_ARGS=(--wlroots-repo "$WLROOTS_REPO" --wlroots-worktree "$WLROOTS_WT"
  --wlroots-base "$WLROOTS_BASE" --wlroots-target-ref "$WLROOTS_TARGET_REF"
  --wlroots-submodule-url "$WLROOTS_SUBMODULE_URL")
WLROOTS_VERIFY_ARGS=(--repo "$WLROOTS_REPO")
WLROOTS_MATERIALIZE_ARGS=(--wlroots-repo "$WLROOTS_REPO")
fi
```

首次需要依赖的 C 节点生成固定 `3rdparty/wlroots` 登记并保留其他条目；wrapper-only 指向已核验的 R0，不伪造 R 来源提交。必要的 C 根 `CMakeLists.txt` 接入须显式结构适配；应保留的更新脚本不得缺失，必须是普通文件并在 fetch/subtree/写 ref 之前拒绝执行，见 [Waylib 合同](references/waylib-contract.md)。

## 4. 可选 decisions

默认 lane action 是 `applied`，工具直接生成过滤补丁并以 `git apply --index` 应用。只有已审查的等价证明或目标相对补丁才能选择：

- `adapted`：必须提供持久 `adaptation_patch`、实质说明和完整 `adaptation_paths`；补丁实际路径仍不能越过 inventory。
- `empty`：必须提供持久 `equivalence_proof`；工具创建可追溯空提交。
- `skipped` 不存在。

工件先用 `artifact_record.py` 复制并取哈希，再把返回的 `artifact` 对象写入 decisions；格式见 [decisions.example.json](examples/decisions.example.json)。decisions 是 replay 身份的一部分，续跑期间不可修改。

`adaptation_paths` 按 inventory 顺序覆盖该 lane 的全部目标路径，每项包含 `path`、`kind`、`reason`、内容寻址 `proof` 和 `review_state: approved`。`modified` 表示已有路径发生修改或删除；`materialized` 表示原本不存在的路径被创建；`omitted` 表示该路径不进入实际 diff，但仍须说明取舍并提供已审核的证明。遗漏路径不是一律禁止，但普通 `omitted`/`empty` 证明不能豁免更新脚本的强制保留与拒绝前缀；未说明、未批准、证明缺失或与真实 diff 不符仍阻断。细节见 [证据格式](references/evidence-schema.md)。

decisions 根对象只能包含 `entries`；每个来源 SHA 下仅允许实际拥有的 `wlroots`/`child`/`parent` lane。C 的 `structural_paths` 只可精确声明 `CMakeLists.txt`，并提供逐路径适配证明；新增 wrapper 合同还要 `contract_additions`。不是任意根文件白名单。

## 5. R→C→P replay

```bash
python3 "$SKILL_DIR/scripts/unified_sync.py" replay \
  --source-repo "$SOURCE_REPO" \
  --parent-worktree "$PARENT_WT" \
  --child-worktree "$CHILD_WT" \
  --parent-base "$PARENT_BASE" \
  --child-base "$CHILD_BASE" \
  --inventory "$ARTIFACT_ROOT/inventory.json" \
  --artifact-root "$ARTIFACT_ROOT" \
  --run-id "$RUN_ID" \
  --refs-doc "$REFS_DOC" "${WLROOTS_REPLAY_ARGS[@]}"
```

有 decisions 时追加 `--decisions "$ARTIFACT_ROOT/decisions.json"`。R 基线有适配时追加 `--wlroots-baseline-proof`，输入为真实工件记录 JSON。相同身份因外部中断且所有 worktree 与 journal HEAD 均 clean 时追加 `--resume`；旧 schema journal 不可续跑，不能补默认 SHA。冲突保留现场，以新 worktree/run-id 和已审核补丁重开，不删除 journal 伪装新运行。

replay 在创建 journal 前扫描所有激活仓库的冻结 baseline 的 `Treeland-Commit` trailer 和旧 `(cherry picked from commit <完整 SHA>)` 标记；任一范围内来源已被映射时必须阻断，即使显式选择 `empty` 也不能再次创建追踪提交。不恢复旧 `already-synced`、`partial-prefix` 或历史重写状态机。

每个 child commit 都生成内容寻址的 `source_contract_audit`，比较该提交父节点与自身的源码合同；同时保留受保护调用及相关变量定义的条件、作用域、顺序、函数调用和目录入口。控制流或入口变化不能靠未改变的 `install(...)` 文字放行。审核失败时保留已创建的 child 和 journal，不创建对应 parent；`--resume` 从 Git 对象重算，后续恢复合同不能抵消中间漂移。该检查不是任意 CMake 求值器，也不执行逐提交完整构建；每段终点 fresh build/install/consumer 仍必需。

更新脚本的存在性、普通 blob 类型和固定拒绝前缀在 C 暂存树、提交后、恢复及独立 Waylib 验证中共用同一检查；不信任工作目录中残留的文件或旧版 PASS。

## 6. 结构化验证

```bash
python3 "$SKILL_DIR/scripts/deckshell_verify.py" \
  --source-repo "$SOURCE_REPO" --parent-repo "$PARENT_WT" \
  --parent-base "$PARENT_BASE" --parent-head "$PARENT_CANDIDATE" \
  --inventory "$ARTIFACT_ROOT/inventory.json" \
  --manifest "$ARTIFACT_ROOT/manifest.json" \
  --evidence "$ARTIFACT_ROOT/parent-evidence.json" \
  --artifact-root "$ARTIFACT_ROOT" --output "$ARTIFACT_ROOT/deckshell-verify.json"

python3 "$SKILL_DIR/scripts/waylib_traces.py" \
  --source-repo "$SOURCE_REPO" --repo "$CHILD_WT" \
  --base "$CHILD_BASE" --head "$CHILD_CANDIDATE" \
  --inventory "$ARTIFACT_ROOT/inventory.json" --output "$ARTIFACT_ROOT/waylib-traces.json"

python3 "$SKILL_DIR/scripts/waylib_verify.py" \
  --source-repo "$SOURCE_REPO" --repo "$CHILD_WT" \
  --base "$CHILD_BASE" --head "$CHILD_CANDIDATE" \
  --inventory "$ARTIFACT_ROOT/inventory.json" \
  --traces "$ARTIFACT_ROOT/waylib-traces.json" \
  --evidence "$ARTIFACT_ROOT/waylib-evidence.json" \
  --artifact-root "$ARTIFACT_ROOT" --output "$ARTIFACT_ROOT/waylib-verify.json"

python3 "$SKILL_DIR/scripts/gitlink_verify.py" \
  --parent-repo "$PARENT_WT" --child-repo "$CHILD_WT" \
  --parent-base "$PARENT_BASE" --child-base "$CHILD_BASE" \
  --manifest "$ARTIFACT_ROOT/manifest.json" --output "$ARTIFACT_ROOT/gitlink-verify.json"

python3 "$SKILL_DIR/scripts/wlroots_verify.py" \
  --source-repo "$SOURCE_REPO" --child-repo "$CHILD_WT" "${WLROOTS_VERIFY_ARGS[@]}" \
  --inventory "$ARTIFACT_ROOT/inventory.json" --manifest "$ARTIFACT_ROOT/manifest.json" \
  --evidence "$ARTIFACT_ROOT/wlroots-evidence.json" --artifact-root "$ARTIFACT_ROOT" \
  --output "$ARTIFACT_ROOT/wlroots-verify.json" \
  --gitlink-output "$ARTIFACT_ROOT/nested-gitlink-verify.json"
```

任一命令退出码 `2` 表示合同阻断，退出码 `1` 表示执行/输入失败；两者都不能进入 closeout。

P/C/R verifier 对 `applied` 重放来源补丁，对 `adapted` 重放获批的目标相对 `adaptation_patch`：均使用独立临时 index，从目标提交父树比较授权路径的对象类型、mode 与 blob SHA。适配还核对已批准的 omitted/modified/materialized 取舍与精确结构路径；不能只比较路径和工件哈希。派生 `.gitmodules` 与两层 gitlink 由独立门禁核对。提交钩子改写内容不能放行；`replay` 的机械回放成功不能替代 verifier。

## 7. 协议 advisory

协议追踪必须同时读取 source inventory 和 replay 后的 parent manifest。这样即使来源提交没有 `protocols/**/*.xml`，但适配后的 parent commit 实际写入 `protocols/compositor/**/*.xml`，仍会触发候选追踪。`protocol_tracker.py` 的 `--parent-repo` 与 `--manifest` 必须成对提供。

无协议触发时：

```bash
python3 "$SKILL_DIR/scripts/protocol_tracker.py" \
  --inventory "$ARTIFACT_ROOT/inventory.json" \
  --parent-repo "$PARENT_WT" \
  --manifest "$ARTIFACT_ROOT/manifest.json" \
  --output "$ARTIFACT_ROOT/protocol-candidates.json"
```

存在协议触发时，使用同一命令并追加用户指定的来源和协议仓库冻结值：

```bash
python3 "$SKILL_DIR/scripts/protocol_tracker.py" \
  --source-repo "$SOURCE_REPO" \
  --parent-repo "$PARENT_WT" \
  --manifest "$ARTIFACT_ROOT/manifest.json" \
  --inventory "$ARTIFACT_ROOT/inventory.json" \
  --protocol-repo "$PROTOCOL_REPO" \
  --protocol-head "$PROTOCOL_HEAD" \
  --output "$ARTIFACT_ROOT/protocol-candidates.json"
```

`PROTOCOL_HEAD` 必须由用户输入的 `protocol_ref`（或完整 SHA）解析并冻结；不要求 `treeland-protocols` remote 名称。详情和候选排序见 [协议候选](references/protocol-tracking.md)。

## 8. 物化 parent 使用的 child candidate

replay 只在 parent index 中写入 gitlink，不会自动把未发布的 child commit 放进 parent 工作树。由于 DeckShell 顶层 CMake 直接执行 `add_subdirectory(3rdparty/waylib-shared)`，在 parent configure/build/CTest 前必须把 manifest 指定的 child candidate 物化到 gitlink 路径：

```bash
git -C "$CHILD_REPO" worktree add --detach "$CHILD_BASE_WT" "$CHILD_BASE"
python3 "$SKILL_DIR/scripts/unified_sync.py" materialize-child \
  --parent-worktree "$PARENT_WT" \
  --child-repo "$CHILD_REPO" \
  --manifest "$ARTIFACT_ROOT/manifest.json" \
  --child-base-worktree "$CHILD_BASE_WT" "${WLROOTS_MATERIALIZE_ARGS[@]}" \
  --output "$ARTIFACT_ROOT/child-materialization.json"
```

该命令只在缺失/空目录创建本地 detached linked worktree；已有 checkout 仅核验，不 reset、覆盖或 fetch。R 启用时同时物化 C 候选、P 内 C 候选下的 R；C 基线已有登记才物化 R0，旧基线不注入新布局。报告核对每层 SHA、对象库、linked-worktree、clean、路径与 manifest。

## 9. 构建、安装与 package consumer

按 [Waylib 合同](references/waylib-contract.md) 建立 child base 审计 worktree；使用 `validation_record.py` 无 shell 执行并记录以下固定 ID：

```text
deckshell-configure
deckshell-build
deckshell-compositor-ctest
waylib-base-configure
waylib-base-build
waylib-base-install
waylib-base-ctest
waylib-candidate-configure
waylib-candidate-build
waylib-candidate-install
waylib-ctest
waylib-package-consumer-configure
waylib-package-consumer-build
waylib-package-consumer
```

四个必需 CMake build ID 只接受默认完整 `cmake --build`，拒绝 target 选择、原生参数及空跑；记录器和报告共用规则。可额外记录 `deckshell-top-level-ctest`；真实 0 tests 记录为 `no-tests`，报告显示 `NO_TESTS`。

R 模式另需 `wlroots-base-configure/build/test`、`wlroots-candidate-configure/build/test` 六条 Meson 记录。测试记录器注入当前 ID/attempt 的独立 `--logbase`，要求日志原先不存在；拒绝 `--list` 等非执行模式及用户覆盖日志名，不读取旧 `testlog.json`。原生零注册测试仍记 `NO_TESTS`。C 和 consumer 不允许 0 tests、Skipped 或只跑子集；CTest 使用本次 `BUILD/waylib`，无过滤 `--show-only=json-v1` 核对完整注册集合，新旧摘要均支持。

唯一例外：来源基线确无 `3rdparty/wlroots` 且 R0 的整个根树为空时，记录器自动将三个 `wlroots-base-*` 记录为 `not-applicable`，保存 Git 证明并明确未执行；调用方式不变，三个 ID 不能省略。报告独立重读 Git 对象，候选 Meson、C/P 验证和两个 R gate 均不获豁免；这不是 `NO_TESTS`。

每个固定 ID 的 `--cwd` 必须是对应 source worktree 根目录。四个 configure ID 的 `-B` 和两个 Waylib install ID 的 `--prefix` 在命令执行前必须不存在；记录器写入 `fresh_paths`，报告按命令重新解析绝对路径并要求 `existed_before=false`。记录器还保存命令执行前后 Git HEAD 与 clean 状态；报告要求 DeckShell、child baseline、child candidate 三组验证分别绑定 manifest 中的冻结提交，命令期间 HEAD 变化或 worktree 出现修改都会直接阻断。

`deckshell-configure`、`deckshell-build`、`deckshell-compositor-ctest`（以及实际运行的 `deckshell-top-level-ctest`）必须额外传入 nested checkout 身份：

```bash
PARENT_CHILD_WT="$PARENT_WT/3rdparty/waylib-shared"
python3 "$SKILL_DIR/scripts/validation_record.py" \
  --id deckshell-configure --category build --cwd "$PARENT_WT" \
  --manifest "$ARTIFACT_ROOT/manifest.json" \
  --nested-checkout "$PARENT_CHILD_WT" --nested-head "$CHILD_CANDIDATE" \
  --artifact-root "$ARTIFACT_ROOT" --bundle "$ARTIFACT_ROOT/validations.json" -- \
  cmake -S "$PARENT_WT" -B "$DECKSHELL_BUILD" -G Ninja \
    -DCMAKE_BUILD_TYPE=Release -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
```

对 parent build、compositor CTest 和可选顶层 CTest 使用相同的 `--nested-checkout/--nested-head` 参数。缺少、错误或变脏的 nested checkout 会令报告阻断。

所有验证记录推荐传 `--manifest`，R 模式必需；记录器据此绑定实际依赖，不能只用旧单层参数证明 R。C/P 配置使用 Ninja 和 `CMAKE_EXPORT_COMPILE_COMMANDS=ON`；构建后保存 codemodel、编译数据库、Ninja 命令和 compiler dependencies，核对生成头摘要。wrapper 必须出现在具体消费目标的链接库与该目标实际链接输入中；自身产物输出、仅 `add_dependencies` 或系统 wlroots 均不能代替。

base/candidate 安装及 consumer 完成后运行：

```bash
python3 "$SKILL_DIR/scripts/waylib_contract_audit.py" \
  --before "$WAYLIB_INSTALL_BASE" --after "$WAYLIB_INSTALL_CANDIDATE" \
  --source-before "$CHILD_BASE_WT" --source-after "$CHILD_WT" \
  --consumer "$ARTIFACT_ROOT/waylib-package-consumer-result.json" \
  --artifact-root "$ARTIFACT_ROOT" --output "$ARTIFACT_ROOT/waylib-contract-audit.json"
```

安装审计通过真实 CMake 加载已安装 package，比较导出公共属性；pkg-config 固定本次安装树的 .pc 路径，比较变量展开后的动态/静态参数和依赖。仅归一化安装根路径，保留顺序；查询失败不退回文本扫描，单次 consumer 通过不能豁免漂移。旧字面快照必须重建。

## 10. 生成报告

```bash
python3 "$SKILL_DIR/scripts/generate_sync_report.py" \
  --inventory "$ARTIFACT_ROOT/inventory.json" --manifest "$ARTIFACT_ROOT/manifest.json" \
  --deckshell-verify "$ARTIFACT_ROOT/deckshell-verify.json" \
  --waylib-verify "$ARTIFACT_ROOT/waylib-verify.json" \
  --gitlink-verify "$ARTIFACT_ROOT/gitlink-verify.json" \
  --protocol-tracking "$ARTIFACT_ROOT/protocol-candidates.json" \
  --contract-audit "$ARTIFACT_ROOT/waylib-contract-audit.json" \
  --child-materialization "$ARTIFACT_ROOT/child-materialization.json" \
  --wlroots-verify "$ARTIFACT_ROOT/wlroots-verify.json" \
  --nested-gitlink-verify "$ARTIFACT_ROOT/nested-gitlink-verify.json" \
  --validations "$ARTIFACT_ROOT/validations.json" \
  --artifact-root "$ARTIFACT_ROOT" --output "$ARTIFACT_ROOT/sync-report.md" \
  --summary-output "$ARTIFACT_ROOT/sync-report.json"
```

报告的 `build_scope` 仅绑定本段终点；缺任一必需门禁、构建或测试证据时只能输出 `blocked/MISSING`，不得补写历史数字或示例 PASS，也不证明其他 tag 已验收。

## 11. 显式本地 closeout

先获得独立收口授权，确认全部目标 ref 未被任何 worktree 检出。只有完整报告 `pass` 时执行；R 模式先设置条件参数：

```bash
# WLROOTS_CANDIDATE 来自 manifest.final_wlroots_head。
if test -n "${WLROOTS_REPO:-}"; then
WLROOTS_CLOSEOUT_ARGS=(--wlroots-repo "$WLROOTS_REPO" --wlroots-ref "$WLROOTS_TARGET_REF"
  --wlroots-expected-old "$WLROOTS_BASE" --wlroots-new "$WLROOTS_CANDIDATE")
fi
```

```bash
python3 "$SKILL_DIR/scripts/unified_sync.py" closeout \
  --parent-repo "$SOURCE_REPO" --child-repo "$CHILD_REPO" \
  --parent-ref "$PARENT_TARGET_REF" --child-ref "$CHILD_TARGET_REF" \
  --parent-expected-old "$PARENT_BASE" --child-expected-old "$CHILD_BASE" \
  --parent-new "$PARENT_CANDIDATE" --child-new "$CHILD_CANDIDATE" \
  --report "$ARTIFACT_ROOT/sync-report.json" \
  --journal "$ARTIFACT_ROOT/closeout-journal.json" "${WLROOTS_CLOSEOUT_ARGS[@]}"
```

closeout 按 R→C→P（R 不适用则 C→P）执行 expected-old CAS。部分成功不回滚下层 ref；保留 journal，恢复同一身份且所有 refs 仍符合预期后追加 `--resume`，只续作未完成阶段。

## 阻断条件

- 来源范围含 merge，或 base 不是 head 祖先。
- inventory 有 unknown、未批准 review-only、源目录类型漂移或路径策略哈希漂移。
- C 普通内容越出三类根和精确结构适配；R 内容不符合去前缀投影；P 内容越出规范目标路径。
- `waylib-only` parent 非 gitlink-only，或 `dual` 未更新/错误更新 gitlink。
- gitlink mode 非 `160000`、对象非 commit、child SHA 不可达、from/to 链不连续。
- child/parent 顺序不满足 journal sequence，或 message/evidence/manifest 来源映射不一致。
- adapted 缺补丁、实质说明或哈希；empty 缺等价证明；任何 silent skip。
- `applied` 与来源补丁投影不一致；`adapted` 与获批补丁内容投影不一致，或逐路径取舍缺项、未批准、证明无效。
- 任一中间 child 的源码合同审计缺失、哈希无效、与 Git 对象不符或显示漂移；不能用最终候选恢复原状抵消。
- 协议已触发但未冻结 protocol ref；候选结果被写成“确认对应”。
- parent 构建前缺少 manifest 绑定的 child materialization，或 nested checkout HEAD/common Git directory/linked 状态/clean 状态不匹配。
- child base/candidate 安装清单、public header、package config/targets、导出目标公共属性、核心 target、导出 namespace、public namespace、pkg-config 或 consumer 合同漂移。
- fresh configure/build/CTest/consumer 失败、跳过或缺日志；0 tests 被标成 PASS。
- replay/closeout 身份漂移、worktree 不 clean、目标 ref 已移动或仍被检出。
- 来源路径、run-id、refs doc 或 adaptation note 含换行/控制字符，可能破坏结构化追溯格式。
- 需要修改外层 HA-DeckShell gitlink、执行 push/tag 或扩大路径 owner，但用户未另行授权。

## 完成定义

每段须来源映射齐全、八类结构化门禁（P/C/R verify、两层 gitlink、protocol advisory、Waylib contract、递归 materialization）通过、必需日志和本段完整报告有效，并完成获准的 closeout。全部冻结关键节点均满足这些条件才可声明整组本地同步完成；普通中间提交不作可构建承诺。R 不适用须由工具核验；隔离 fixture 不代表真实产品验证，远程发布另行授权。
