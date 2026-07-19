---
name: treeland-deckshell-sync
description: 将 DeckShell 仓库远端 `treeland/master` 的显式提交区间确定性同步到 DeckShell 本地目标分支时使用；执行历史重写映射、路径白名单、`waylib/**`/`qwlroots/**` 剥离、幂等追溯、冻结 worktree、子模块、证据审计、构建测试与本地 fast-forward。适用于新同步、区间续同步和既有结果复核；不用于反向同步或远程 push。
---

# Treeland → DeckShell 区间同步

## 固定职责

把固定来源区间 `(<range_base>..<range_head>]` 按原顺序同步到一个显式本地目标分支，并满足：

- 来源固定为 remote `treeland`、branch `master`、ref `refs/remotes/treeland/master`。
- 非 dependency-only 来源提交保持 1:1 目标提交和唯一 Treeland 追溯。
- 每个 retained 来源路径只对应 path policy 计算出的唯一规范目标路径；不存在隐式兄弟文件、一对多实现路径或由目标提交自授权的额外路径。
- 路径只能命中 `mapped`、`root-owned`、`excluded` 或已批准的 `review-only`；`unknown` 必须阻断。
- `waylib`、`waylib/**`、`qwlroots`、`qwlroots/**` 不进入目标提交。
- 所有审计和构建使用冻结 SHA 的隔离 worktree。
- 只收口到本地 fast-forward，固定输出 `remote_push: no`。

开始前读取：

- [`references/path-policy.md`](references/path-policy.md)：路径策略唯一事实来源。
- `scripts/sync_audit.py --help`：inventory、traces、verify 的确定性命令接口。

## 输入契约

执行前必须得到：

```yaml
repo_dir: <DeckShell Git 根目录的绝对路径>
source_snapshot_mode: live|existing-ref
range_base: <不包含的来源 commit>
range_head: <包含的来源 commit>
target_branch: <已存在的本地分支>
work_branch: sync/treeland-<short-base>-<short-head>
worktree_dir: <new-sync 隔离工作树绝对路径>
audit_worktree: <already-synced 独立审计工作树绝对路径>
scratch_dir: <所有 Git worktree 之外的绝对路径>
build_dir: <位于冻结审计工作树内或 scratch_dir 的全新目录>
history_gate_doc: <发生历史重写时的门禁文档>
sync_report: <最终同步报告>
review_approvals: []
```

缺少范围、目标分支或任一隔离路径时停止。不得猜测 `range_head`，不得把远端分支作为本地目标分支。

## 1. 预检与来源冻结

确认仓库、来源 remote 和目标本地分支：

```bash
git -C "<repo_dir>" rev-parse --show-toplevel
git -C "<repo_dir>" remote get-url "treeland"
git -C "<repo_dir>" show-ref --verify "refs/heads/<target_branch>"
git -C "<repo_dir>" worktree list --porcelain
```

必须证明：

- `repo_dir` 等于 `rev-parse --show-toplevel` 的规范化绝对路径。
- `scratch_dir`、`worktree_dir`、`audit_worktree`、`build_dir` 互不覆盖。
- `scratch_dir` 不位于任何 Git worktree 内。
- 目标主工作树可以有用户修改，但不得在其中应用补丁、初始化构建或生成审计证据。

`live` 模式先记录旧来源 SHA，再刷新固定 remote-tracking ref：

```bash
git -C "<repo_dir>" rev-parse "refs/remotes/treeland/master^{commit}"
git -C "<repo_dir>" fetch "treeland" "+refs/heads/master:refs/remotes/treeland/master"
```

`existing-ref` 模式不 fetch，并在报告中写明“仅验证本地快照”。随后解析并冻结：

```bash
git -C "<repo_dir>" rev-parse "<range_base>^{commit}"
git -C "<repo_dir>" rev-parse "<range_head>^{commit}"
git -C "<repo_dir>" rev-parse "refs/remotes/treeland/master^{commit}"
git -C "<repo_dir>" rev-parse "refs/heads/<target_branch>^{commit}"
```

后续只使用完整 SHA，不再使用移动 ref。

## 2. 历史映射门禁

验证规范化范围属于冻结来源历史：

```bash
git -C "<repo_dir>" merge-base --is-ancestor "<range_base_sha>" "<range_head_sha>"
git -C "<repo_dir>" merge-base --is-ancestor "<range_head_sha>" "<source_head_sha>"
git -C "<repo_dir>" reflog show "refs/remotes/treeland/master"
```

边界不在当前来源历史或本次 fetch 发生 forced-update 时，先使用 `range-diff`、稳定 patch-id、二进制/模式变化审计建立旧线 → 新线的唯一映射。`history_gate_doc` 必须记录：

- 原始和规范化边界；
- 旧、新提交映射；
- 非等价项的范围决策；
- 重新计算的数量、顺序和路径分类；
- PASS 或 BLOCKED。

不能唯一映射、只能按 subject 猜测或旧范围异常膨胀时停止；不得创建工作分支。

## 3. 生成路径 inventory

在创建分支前运行：

```bash
python3 "<skill_dir>/scripts/sync_audit.py" inventory \
  --repo "<repo_dir>" \
  --base "<normalized_base_sha>" \
  --head "<normalized_head_sha>" \
  --output "<scratch_dir>/inventory.json"
```

对每个已批准的 review-only policy key 追加：

```text
--approve-review <policy-key>
```

inventory 使用 NUL 分隔解析普通文件、rename 和 copy，并输出：

- 有序来源 SHA、SHA-256、merge commit；
- dependency-only、mixed、other 数量；
- 每个 old/new path 的分类和目标路径；
- `mapped_source_paths`、`root_source_paths`、drop paths、target paths；
- `target_paths` 是该来源提交可触达的唯一规范目标路径集合；
- review-only/unknown 阻断原因。

`outcome != pass`、存在 merge commit、unknown 或未批准 review-only 时停止。

## 4. 幂等追溯门禁

对冻结目标 SHA 运行：

```bash
python3 "<skill_dir>/scripts/sync_audit.py" traces \
  --repo "<repo_dir>" \
  --target "<target_base_sha>" \
  --inventory "<scratch_dir>/inventory.json" \
  --output "<scratch_dir>/traces-before.json"
```

脚本必须按以下规则解析：

1. 优先使用唯一的完整 `Treeland-Commit:`。
2. 没有新 trailer 时，只在 legacy cherry-pick trailer 中匹配 inventory SHA。
3. 相同 SHA 去重；中间 DeckShell SHA 不参与来源映射。
4. 重复、错序、非前缀缺口或 dependency-only 映射进入 `blocked`。

状态处理：

- `new-sync`：允许创建同步分支。
- `already-synced`：禁止回放，直接创建 detached 审计 worktree。
- `partial-prefix`：停止并输出剩余来源边界；只有新的显式方案批准后才能续同步。
- `blocked`：停止，不自动改写历史。

## 5. 创建冻结工作树并初始化子模块

### new-sync

```bash
git -C "<repo_dir>" branch "<work_branch>" "<target_base_sha>"
git -C "<repo_dir>" worktree add "<worktree_dir>" "<work_branch>"
git -C "<worktree_dir>" rev-parse "HEAD^{commit}"
```

### already-synced

```bash
git -C "<repo_dir>" worktree add --detach "<audit_worktree>" "<target_base_sha>"
git -C "<audit_worktree>" rev-parse "HEAD^{commit}"
```

在实际用于构建的冻结 worktree 中执行：

```bash
git -C "<frozen_worktree>" submodule sync --recursive
git -C "<frozen_worktree>" submodule update --init --recursive
git -C "<frozen_worktree>" submodule status --recursive
```

不得使用 `--remote`。固定 gitlink 无法取得时 BLOCKED。不要持久化修改共享 `rerere` 配置；需要时仅在相关 Git 命令使用临时 `-c rerere.enabled=true -c rerere.autoupdate=true`。

## 6. new-sync 逐提交回放

严格按 inventory 顺序处理：

- dependency-only：记录 `skipped-dependency-only`，不创建提交。
- mixed/other：从 `<source_commit>^` 到 `<source_commit>` 生成两个限域补丁。

补丁构造规则：

- 使用 `mapped_source_paths` 生成 mapped patch，以 `--directory=compositor` 应用。
- 使用 `root_source_paths` 生成 root-owned patch，直接应用。
- 以参数数组传递 JSON 中的路径，不拼接或 `eval` shell 字符串。
- 空路径列表不生成、不应用补丁。
- 不先应用完整提交再回退 excluded 路径。

### 目标路径权威门禁

每个来源提交的 inventory `target_paths` 是该提交唯一的目标路径权威：

- 目标提交的所有 old/new 实际路径都必须属于 `target_paths`；额外路径统一报告 `target-path-expansion` 并 BLOCKED。
- `adaptation_paths` 只能解释 `target_paths` 内的 `modified`、`omitted`、`materialized`，不能用目标提交刚触达的兄弟文件反向扩大授权范围。
- 规范目标路径在目标父树中不存在时，可以在同一规范路径使用 `materialized`；“规范路径缺失”本身不等于结构漂移。
- DeckShell 本地独有的测试客户端、fixture、辅助类和适配器可以继续独立存在，但本次同步提交不得触达它们，也不得把 mapped 上游实现责任迁入其中。
- 具有上游对应路径的生产文件和测试文件都受本门禁约束，不能按“测试辅助文件”豁免。

如果 mapped 补丁只能通过修改兄弟文件、把规范路径标记为 omitted/empty 或继续维护一对多实现才能落地，则人工判定为 `target-structure-drift`，立即停止当前回放，不创建该来源提交。恢复流程固定为：

1. 在本次冻结同步工作树之外，准备独立的 DeckShell 结构对齐变更。
2. 恢复上游规范文件形状，同时保留已经确认的行为修复和测试覆盖。
3. 完成产品构建、测试和差异审计，并将结构对齐结果形成干净的新目标基线。
4. 从新目标基线重新生成 inventory、traces 和冻结 worktree，再重新回放来源区间。

不得把结构对齐夹入 Treeland 1:1 映射提交，不得用 `adapted` 或 `empty` 隐藏目标结构漂移。

应用前后保存到 `scratch_dir/<source_sha>/`：

```text
mapped.patch
root.patch
filtered.patch
apply.log
staged.diff
commit.diff
path-audit.txt
```

动作分类：

- `applied`：两个补丁无冲突应用，且没有人工修改；实际目标路径必须等于 inventory target paths。
- `adapted`：发生冲突或 DeckShell 合同适配；实际目标路径必须是 inventory target paths 的子集，额外保存 `difference-report.md` 并逐项解释差异。
- `empty`：只在目标树已等价包含过滤补丁时使用；保存非空 `equivalence-proof.md`，不能把普通 apply 失败、兄弟文件存在相似代码或实现已迁移到未映射路径视为等价。

`equivalence-proof.md` 必须采用一种明确证明路线：精确补丁等价记录冻结 SHA、mapped filtered patch 哈希及 `git apply --reverse --check` 命令和结果；适配后行为等价记录来源 hunk 到规范目标实现的逐项映射、无法精确 reverse-check 的原因，以及针对性测试命令和结果。两种路线都不得引用 inventory 外路径承担等价实现。

冲突适配只能修改当前提交 inventory 批准的目标路径。禁止夹带重构、无关修复、excluded 路径、未知根路径或本地独有文件。

## 7. 创建规范追溯提交

保留来源 subject/body、author 和 author date。先移除或隔离来源正文中的同步 trailer，再追加唯一规范块：

```text
(cherry picked from commit <完整 treeland SHA>)

[treeland-sync] classification: mixed|other
[treeland-sync] action: applied|adapted|empty
[treeland-sync] drop files:
- <实际 drop path；无则 none>
[treeland-sync] path mapping:
- <该提交实际使用的映射；无则 none>
[treeland-sync] adaptation paths:
- modified|omitted|materialized: <目标仓库相对路径；可多行；无则 none>
[treeland-sync] adaptation notes:
- <说明；无则 none>

Treeland-Commit: <完整 treeland SHA>
```

不要固定写入该提交未使用的 `src/** -> compositor/src/**`。mixed 的依赖剥离只由 `drop files` 表达；只有 `action=adapted` 才在 adaptation notes 解释 DeckShell 合同适配。每次提交后立即保存来源 → 目标 SHA。

`adaptation paths` 是机器可核验的路径清单，不得把路径混入普通说明：

- `modified`：路径出现在目标提交实际 diff 中，且内容因 DeckShell 合同适配而不同。
- `omitted`：路径属于 inventory 的预期目标路径，但因适配没有出现在目标提交实际 diff 中。
- `materialized`：路径出现在目标提交实际 diff 中，且目标侧没有可直接沿用的既有基线，由适配显式创建。
- 同一路径只能出现一次，不能同时声明为多个 kind；路径必须属于 inventory 预期目标路径。
- `adapted` 必须至少列出一项；`applied`、`empty` 固定写 `- none`。
- `adaptation notes` 只解释“为什么这样适配”，不重复承担文件清单职责；`applied`、`empty` 固定写 `- none`。

## 8. 证据验证

生成 evidence JSON：

```json
{
  "schema_version": 2,
  "entries": [
    {
      "source_commit": "<sha>",
      "target_commit": "<sha>",
      "action": "applied|adapted|empty",
      "mapped_patch": {"path": "<relative path>", "size": 1, "sha256": "<64 hex>"},
      "staged_diff": {"path": "<relative path; applied/adapted>", "size": 1, "sha256": "<64 hex>"},
      "commit_diff": {"path": "<relative path>", "size": 1, "sha256": "<64 hex>"},
      "path_audit": {"path": "<relative path>", "size": 1, "sha256": "<64 hex>"},
      "difference_report": {"path": "<relative path; adapted>", "size": 1, "sha256": "<64 hex>"},
      "adaptation_paths": [
        {
          "kind": "modified|omitted|materialized",
          "path": "<DeckShell 目标仓库相对路径>",
          "target_status": "A|M|D|R|C|omitted",
          "source_status": "A|M|D|R|C",
          "parent_exists": false,
          "proof": [{"path": "<relative path>", "size": 1, "sha256": "<64 hex>"}],
          "review_state": "approved"
        }
      ],
      "adaptation_notes": "<non-empty; adapted>",
      "equivalence_proof": {"path": "<relative path; empty>", "size": 1, "sha256": "<64 hex>"}
    }
  ]
}
```

evidence 兼容规则：

- 缺少 `schema_version` 或值为 `1` 时仅可按旧规则复核已经完成的同步历史，不得作为迁移完成证据。
- `schema_version: 2` 时，`adapted` 必须提供非空 `adaptation_paths` 和非空 `adaptation_notes`。
- `schema_version: 2` 的 `applied`、`empty` 不得携带非空 `adaptation_paths`；`adaptation_notes` 使用 `none` 或留空，并与提交消息中的 `- none` 对齐。
- 所有 adaptation path 必须属于 inventory 预期目标路径；目标提交实际路径超出该集合时，无论 evidence 如何声明都以 `target-path-expansion` BLOCKED。
- `modified`、`materialized` 路径必须同时属于 inventory 预期目标路径并出现在目标提交实际路径中。
- `omitted` 路径必须属于 inventory 预期目标路径，且不得出现在目标提交实际路径中。
- 提交消息中的 `adaptation paths`、`adaptation notes` 必须与 evidence 的结构化值顺序一致；缺失、重复、非法 kind、重复路径或不一致均 BLOCKED。
- 迁移验证必须显式传入 `--require-evidence-schema 2 --evidence-root <root>`；相对 artifact 必须位于 root 内，是普通文件，且大小和 SHA-256 匹配。
- strict v2 的每条 adaptation path 必须带 target/source status、真实 parent-tree 事实、非空 proof 和 `review_state=approved`；`materialized` 只允许目标状态 `A` 且父树不存在。
- 路径顺序固定为 `omitted`、`materialized`、`modified`，同 kind 按 UTF-8 字节序排列；paths 字段必须位于 notes 字段之前。
- strict v2 只机器验证 `equivalence_proof` 的路径、文件类型、大小和 SHA-256；证明正文是否完成精确 reverse-check 或行为等价映射仍必须逐项复核，不能把工件存在误报为语义等价。
- 当前 evidence schema v2 不提供一对多 relocation 授权。未来确需保留永久目标实现迁移时，必须显式升级 schema、声明来源到目标关系和独立批准证据，不得复用普通 `adapted` 绕过本门禁。

在工作分支 HEAD 或 already-synced 冻结目标上重跑 traces，再验证：

```bash
python3 "<skill_dir>/scripts/sync_audit.py" verify \
  --repo "<repo_dir>" \
  --inventory "<scratch_dir>/inventory.json" \
  --traces "<scratch_dir>/traces-after.json" \
  --evidence "<scratch_dir>/evidence.json" \
  --evidence-root "<persistent_evidence_root>" \
  --require-evidence-schema 2 \
  --output "<scratch_dir>/verify.json"
```

`verify` 必须分别报告 `report_schema_version`、`evidence_schema_version`、`strict_evidence_schema_required`、`target_path_authority` 和 `target_path_expansions`，并证明完整有序映射、单父提交、目标路径合法、applied 路径精确、adapted 无目标路径扩张、adapted/empty 证据完整，以及 schema v2 的 adaptation 路径语义和提交消息一致性。`outcome != pass` 或 `target_path_authority != pass` 时禁止构建收口。

## 9. 冻结构建与测试

确保 `build_dir` 为全新目录，然后执行：

```bash
cmake -S "<frozen_worktree>" -B "<build_dir>" -G "Ninja" -DCMAKE_BUILD_TYPE="Debug"
cmake --build "<build_dir>"
ctest --test-dir "<build_dir>/compositor" --output-on-failure
ctest --test-dir "<build_dir>" --output-on-failure
```

分别记录配置、构建、compositor CTest 和顶层 CTest。0 tests 必须原样报告，不能表述为完整覆盖。失败且不能证明与当前同步无关时 BLOCKED。

## 10. 本地 fast-forward 与复验

只对 `new-sync` 执行。确认目标主工作树：

```bash
git -C "<target_worktree>" branch --show-current
git -C "<target_worktree>" status --short
git -C "<target_worktree>" rev-parse "HEAD^{commit}"
git -C "<target_worktree>" merge --ff-only "<work_branch>"
```

前三条必须分别证明当前分支等于目标分支、工作树干净、HEAD 等于冻结基线。目标已移动时停止，不 rebase、不覆盖。合入后在新目标 HEAD 上重新执行 traces、verify、子模块状态、构建和 CTest。

技能到此结束；不得执行任何远程 push。

## 阻断条件

出现任一情况立即停止：

- 来源边界不能唯一归一化，或范围包含未定义 merge commit。
- inventory 存在 unknown、未批准 review-only 或摘要不一致。
- 幂等状态为 partial-prefix/blocked，或 dependency-only 已有目标映射。
- worktree、scratch、build 路径重叠或冻结 HEAD 不匹配。
- 子模块为空、gitlink 不匹配或固定对象不可取得。
- 目标提交触达 excluded/unknown 路径。
- 目标提交实际 old/new 路径超出 inventory target paths，或 evidence adaptation path 试图引用该额外路径。
- mapped 实现责任已迁入兄弟文件或本地独有文件，形成 `target-structure-drift`。
- applied 实际路径与 inventory 不一致。
- adapted 存在未解释差异、缺少 adaptation paths/notes、路径语义非法或提交消息与 evidence 不一致；empty 缺少等价证明。
- trace 重复、错序或一个目标提交匹配多个 inventory 来源。
- 构建或测试回归。
- fast-forward 前目标分支移动或目标工作树不干净。

## 输出要求

最终 `sync_report` 必须包含：

1. 原始/规范化范围、source head、target base 和快照模式。
2. history gate PASS/BLOCKED 及旧线 → 新线映射。
3. inventory 数量、顺序 SHA-256、review approvals 和跳过清单。
4. new-sync/already-synced/partial-prefix/blocked 状态。
5. 完整来源 → 目标映射、new/legacy trace。
6. 每个 mixed 的 drop paths；每个 adapted 的 adaptation paths/notes；每个 adapted/empty 的证据路径。
7. `target_path_authority`、完整 `target_path_expansions` 和发现结构漂移时采用的新基线恢复记录。
8. verify、子模块、配置、构建和两级 CTest 结果。
9. 最终本地分支和 HEAD。
10. `remote_push: no`。
