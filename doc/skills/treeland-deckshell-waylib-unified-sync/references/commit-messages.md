# 提交消息合同

所有同步提交保留来源 author name/email/date。来源完整 message 放在缩进块中，防止来源正文里的同名 trailer 被误解析为本次追溯字段。

## 引用基准与旧证据

新提交的唯一 `Refs:` 保存外层工作区相对方案标识，例如 `.helloagents/plans/<batch>/plan.md`；普通 P/C/R 与协议 companion 共用同一值。路径使用 `/`，不允许绝对路径、盘符、`..`、反斜杠、`~`、控制字符或 `./` 等非规范形式。它是历史资料定位，不是相对 P/C/R 仓库的 Markdown 链接。

运行参数仍由现有路径解析器取得 canonical repo、common Git directory、worktree 和工件路径；实际环境身份、安装路径和原始日志保持原语义。迁移审批中的 `refs_doc` 必须与本次相对值完全一致。历史 manifest、报告和日志中的绝对路径只读兼容，不能批量替换或重算旧证据后声称新 SHA 已验收。

已获授权的消息整理只改顶层 `Refs:` 及生成的下层依赖 SHA，保留来源缩进块、来源 trailer、作者和提交者元数据。协议 companion 保留 `Protocol-Implementation-Commit` / `Treeland-Protocols-Commit`，不制造普通 `Treeland-Commit`。对应内容/拓扑检查见 [旧新映射](repo-records.md#可选旧新映射)。

## child commit

```text
<原始 subject>

Original treeland commit:
    <原始 message，每行缩进>

[treeland-unified-sync] classification: waylib-only|dual
[treeland-unified-sync] action: applied|adapted|empty|gitlink-only
[treeland-unified-sync] lane: child
[treeland-unified-sync] content action: applied|adapted|empty|not-applicable
[treeland-unified-sync] nested gitlink: <null 或 status/from/to/url/gitmodules_before/gitmodules_after 的单行 JSON>
[treeland-unified-sync] drop files:
- <实际非 child 路径；无则 none>
[treeland-unified-sync] adaptation paths:
- <modified|omitted|materialized>: <目标路径；非 adapted 则整行写 none>
[treeland-unified-sync] adaptation notes:
- <说明；无则 none>
[treeland-unified-sync] parent association: manifest-only
[treeland-unified-sync] run-id: <run-id>

Refs: <持久 refs_doc>
Treeland-Commit: <完整来源 SHA>
```

child message 不得出现未来 parent SHA。`parent association: manifest-only` 是固定声明，不是“稍后 amend”的占位。

R 使用同一消息结构但 `lane: wlroots`，nested gitlink 为 null，action 仅 applied/adapted/empty，drop files 为非 R 来源变更。R 不引用未来 C SHA。C 包含 R 更新时追加其完整 SHA；首次登记还明确备注“.gitmodules 是显式结构适配，不是纯 gitlink 变更”。C 的 overall action 和 content action 必须与普通内容/派生路径一致。

## waylib-only parent

```text
<原始 subject>

Original treeland commit:
    <原始 message>

[treeland-unified-sync] classification: waylib-only
[treeland-unified-sync] action: gitlink-only
[treeland-unified-sync] drop files:
- qwlroots/<...>|waylib/<...>|wlroots/<...>|3rdparty/wlroots/<...>
[treeland-unified-sync] path mapping:
- none
[treeland-unified-sync] adaptation paths:
- none
[treeland-unified-sync] adaptation notes:
- DeckShell contains only the gitlink update.
- 这是一个单纯的 gitlink 变更。
- Includes waylib-shared update to <child SHA>.
- 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。
[treeland-unified-sync] waylib-shared sync:
- commit: <child SHA>
- action: synced
- gitlink: updated
[treeland-unified-sync] run-id: <run-id>

Refs: <持久 refs_doc>
Treeland-Commit: <完整来源 SHA>
```

实际 diff 必须只包含 `3rdparty/waylib-shared`。

## dual parent

与 parent 模板相同，但：

- classification 为 `dual`；
- action 是 parent 内容 action `applied|adapted|empty`；
- path mapping 列出 inventory 的来源 → 规范目标；
- commit 同时包含 child gitlink；
- adaptation notes 固定追加 `Includes waylib-shared update to <child SHA>.` 和“此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新”。

## deckshell-only parent

- classification 为 `deckshell-only`；
- action 为 `applied|adapted|empty`；
- `waylib-shared sync` 写 `action: not-applicable` 与 `gitlink: unchanged`；
- 实际 commit 不得触达 gitlink。

## 验证

每个目标 commit 的 `Treeland-Commit`、classification、action、drop list、adaptation paths 和 notes 必须唯一且与 inventory/manifest/evidence 一致。C/R 的 lane、content action、nested gitlink 也须一致。adaptation paths 在消息中保存 kind/path，理由与哈希证明在 evidence；P/C/R verifier 都核对真实 Git 对象，不靠 subject 或相似度猜映射。

旧 `(cherry picked from commit <完整 SHA>)` 仅用于冻结基线中的重叠阻断；新提交仍只生成上述统一追溯格式，不引入旧状态机或双格式写入。
