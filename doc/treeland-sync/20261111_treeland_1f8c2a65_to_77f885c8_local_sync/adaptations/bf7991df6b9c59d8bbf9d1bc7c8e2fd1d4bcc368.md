# P / DeckShell 适配：fix(workspace): avoid focus changes from inactive workspaces

- Treeland 来源：` 26bd572c2e0565cd20fda62252fc38fced5b6021 `。
- 本仓目标：` bf7991df6b9c59d8bbf9d1bc7c8e2fd1d4bcc368 `。
- 节点：N11；action=adapted。
- [本仓总记录](../summary.md#entry-21)。

## 比较口径

比较来源唯一父提交 → 来源提交，与原目标唯一父提交 → 原目标提交的逐路径增量。
零上下文补丁对照会呈现基线位置、既有命名和本次实现差异；它不是整棵来源树与目标树的长期差异，也不声称所有显示行都是本次新增适配。
本批没有历史改写；依赖 gitlink 在总记录单列，不混进源码适配。原验收只适用于总记录列出的原节点候选。

## 已审说明

以下保留原证据文字；其中依赖 SHA 属于原运行，新依赖身份见下文与总记录。

- ` Apply the reviewed canonical source projection and necessary authorized local integration; preserve WaylibShared package identity, namespace, XML and regression semantics. `

保留/映射路径：` compositor/src/workspace/workspace.cpp `。
排除路径：无。

## 逐路径取舍与实际差异

### ` compositor/src/workspace/workspace.cpp ` / modified

- 原审核理由：` Integrate the canonical source delta, preserving nonconflicting accepted local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/inputs/26bd572c2e0565cd20fda62252fc38fced5b6021/parent-review.json`。
- 来源路径：` src/workspace/workspace.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 72d40791dab83c005c55d533b662a426be8a6eeb ` → ` 26bd572c2e0565cd20fda62252fc38fced5b6021 `。
- 原目标增量端点：` ea402759984079e80dccf03ace7c79c0055b81d8 ` → ` bf7991df6b9c59d8bbf9d1bc7c8e2fd1d4bcc368 `。
- 本次目标：` ea402759984079e80dccf03ace7c79c0055b81d8 ` → ` bf7991df6b9c59d8bbf9d1bc7c8e2fd1d4bcc368 `。
- 目标文件项（mode/type/blob）：` 100644 blob f31e2ed6d7ccfd22721b4bab04b6d5933223e15d ` → ` 100644 blob 5018ef253ee9c7ab7eaa9b5d1e2134c1dbe4065c `。
- 来源文件项 ` src/workspace/workspace.cpp `：` 100644 blob f839301311ec1483206faced71419245cb29c571 ` → ` 100644 blob 3d1e0e5edaafb3b9f762f42ab7d4012dad0e1d77 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

- 依赖 ` 3rdparty/waylib-shared `：unchanged；` b156ab2516c19c5624b90ddbd0a32cdc3b53bbb7 ` → ` b156ab2516c19c5624b90ddbd0a32cdc3b53bbb7 `。

## 原工件定位

- mapped_source_patch：外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/commits/26bd572c2e0565cd20fda62252fc38fced5b6021/parent-mapped-source.patch`。
- root_source_patch：外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/commits/26bd572c2e0565cd20fda62252fc38fced5b6021/parent-root-source.patch`。
- adaptation_patch：外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/inputs/26bd572c2e0565cd20fda62252fc38fced5b6021/parent.patch`。
- target_diff：外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/commits/26bd572c2e0565cd20fda62252fc38fced5b6021/parent-target.diff`。
