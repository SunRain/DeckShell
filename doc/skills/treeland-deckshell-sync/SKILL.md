---
name: treeland-deckshell-sync
description: 将 DeckShell 仓库远端 `treeland/master` 的显式提交区间确定性同步到 DeckShell 本地目标分支时使用；执行历史重写映射、路径白名单、`waylib/**`/`qwlroots/**` 剥离、幂等追溯、冻结 worktree、子模块、证据审计、构建测试与本地 fast-forward。适用于新同步、区间续同步和既有结果复核；不用于反向同步或远程 push。
---

# Treeland → DeckShell 区间同步

## 固定职责

把固定来源区间 `(<range_base>..<range_head>]` 按原顺序同步到一个显式本地目标分支，并满足：

- 来源固定为 remote `treeland`、branch `master`、ref `refs/remotes/treeland/master`。
- 非 dependency-only 来源提交保持 1:1 目标提交和唯一 Treeland 追溯。
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
- `adapted`：发生冲突或 DeckShell 合同适配；额外保存 `difference-report.md` 并逐项解释差异。
- `empty`：只在目标树已等价包含过滤补丁时使用；保存非空 `equivalence-proof.md`，不能把普通 apply 失败视为等价。

冲突适配只能修改当前提交批准的目标路径。禁止夹带重构、无关修复、excluded 路径或未知根路径。

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
[treeland-sync] adaptation notes:
- <说明；无则 none>

Treeland-Commit: <完整 treeland SHA>
```

不要固定写入该提交未使用的 `src/** -> compositor/src/**`。mixed 另加依赖剥离说明。每次提交后立即保存来源 → 目标 SHA。

## 8. 证据验证

生成 evidence JSON：

```json
{
  "entries": [
    {
      "source_commit": "<sha>",
      "target_commit": "<sha>",
      "action": "applied|adapted|empty",
      "mapped_patch": "<absolute path to filtered.patch>",
      "staged_diff": "<absolute path; applied/adapted>",
      "commit_diff": "<absolute path>",
      "path_audit": "<absolute path>",
      "difference_report": "<absolute path; adapted>",
      "adaptation_notes": "<non-empty; adapted>",
      "equivalence_proof": "<absolute path; empty>"
    }
  ]
}
```

在工作分支 HEAD 或 already-synced 冻结目标上重跑 traces，再验证：

```bash
python3 "<skill_dir>/scripts/sync_audit.py" verify \
  --repo "<repo_dir>" \
  --inventory "<scratch_dir>/inventory.json" \
  --traces "<scratch_dir>/traces-after.json" \
  --evidence "<scratch_dir>/evidence.json" \
  --output "<scratch_dir>/verify.json"
```

`verify` 必须证明：完整有序映射、单父提交、目标路径合法、applied 路径精确、adapted/empty 证据存在且非空。`outcome != pass` 时禁止构建收口。

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
- applied 实际路径与 inventory 不一致。
- adapted 存在未解释差异；empty 缺少等价证明。
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
6. 每个 mixed 的 drop paths；每个 adapted/empty 的证据路径。
7. verify、子模块、配置、构建和两级 CTest 结果。
8. 最终本地分支和 HEAD。
9. `remote_push: no`。
