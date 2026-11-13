# P / DeckShell 适配：feat(session): retain the owning user configuration

- Treeland 来源：` c7d4b1226c0450e0257b1447515c271b837e1512 `。
- 本仓目标：` 1b4df41c0be46b58b20adcc2ccfba9e8aa95ea70 `。
- 节点：N11；action=adapted。
- [本仓总记录](../summary.md#entry-50)。

## 比较口径

比较来源唯一父提交 → 来源提交，与原目标唯一父提交 → 原目标提交的逐路径增量。
零上下文补丁对照会呈现基线位置、既有命名和本次实现差异；它不是整棵来源树与目标树的长期差异，也不声称所有显示行都是本次新增适配。
本批没有历史改写；依赖 gitlink 在总记录单列，不混进源码适配。原验收只适用于总记录列出的原节点候选。

## 已审说明

以下保留原证据文字；其中依赖 SHA 属于原运行，新依赖身份见下文与总记录。

- ` Apply the reviewed canonical source projection and necessary authorized local integration; preserve WaylibShared package identity, namespace, XML and regression semantics. `

保留/映射路径：` compositor/src/session/session.cpp `、` compositor/src/session/session.h `。
排除路径：无。

## 逐路径取舍与实际差异

### ` compositor/src/session/session.cpp ` / modified

- 原审核理由：` Integrate the canonical source delta, preserving nonconflicting accepted local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/inputs/c7d4b1226c0450e0257b1447515c271b837e1512/parent-review.json`。
- 来源路径：` src/session/session.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 9dfc7417d918731f3961a908ff95d20b4c7a0f5a ` → ` c7d4b1226c0450e0257b1447515c271b837e1512 `。
- 原目标增量端点：` 81a169a1935fff877cb665e85d12e348946a6574 ` → ` 1b4df41c0be46b58b20adcc2ccfba9e8aa95ea70 `。
- 本次目标：` 81a169a1935fff877cb665e85d12e348946a6574 ` → ` 1b4df41c0be46b58b20adcc2ccfba9e8aa95ea70 `。
- 目标文件项（mode/type/blob）：` 100644 blob 93eaf4c0d1a005a2adbb0ac711cc3f55a54554c4 ` → ` 100644 blob 2934650c8041e5acb13f79bb3ab19a62af037075 `。
- 来源文件项 ` src/session/session.cpp `：` 100644 blob 93eaf4c0d1a005a2adbb0ac711cc3f55a54554c4 ` → ` 100644 blob 2934650c8041e5acb13f79bb3ab19a62af037075 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/src/session/session.h ` / modified

- 原审核理由：` Integrate the canonical source delta, preserving nonconflicting accepted local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/inputs/c7d4b1226c0450e0257b1447515c271b837e1512/parent-review.json`。
- 来源路径：` src/session/session.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 9dfc7417d918731f3961a908ff95d20b4c7a0f5a ` → ` c7d4b1226c0450e0257b1447515c271b837e1512 `。
- 原目标增量端点：` 81a169a1935fff877cb665e85d12e348946a6574 ` → ` 1b4df41c0be46b58b20adcc2ccfba9e8aa95ea70 `。
- 本次目标：` 81a169a1935fff877cb665e85d12e348946a6574 ` → ` 1b4df41c0be46b58b20adcc2ccfba9e8aa95ea70 `。
- 目标文件项（mode/type/blob）：` 100644 blob e37dbdf097800be7dcff821628f4f73a0dbfcaf5 ` → ` 100644 blob 4e168448d2423705737a223e475621157bf1f3e8 `。
- 来源文件项 ` src/session/session.h `：` 100644 blob e37dbdf097800be7dcff821628f4f73a0dbfcaf5 ` → ` 100644 blob 4e168448d2423705737a223e475621157bf1f3e8 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

- 依赖 ` 3rdparty/waylib-shared `：unchanged；` d2fd6828913037cc12954a29f1442f47de0a695f ` → ` d2fd6828913037cc12954a29f1442f47de0a695f `。

## 原工件定位

- mapped_source_patch：外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/commits/c7d4b1226c0450e0257b1447515c271b837e1512/parent-mapped-source.patch`。
- root_source_patch：外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/commits/c7d4b1226c0450e0257b1447515c271b837e1512/parent-root-source.patch`。
- adaptation_patch：外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/inputs/c7d4b1226c0450e0257b1447515c271b837e1512/parent.patch`。
- target_diff：外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/commits/c7d4b1226c0450e0257b1447515c271b837e1512/parent-target.diff`。
