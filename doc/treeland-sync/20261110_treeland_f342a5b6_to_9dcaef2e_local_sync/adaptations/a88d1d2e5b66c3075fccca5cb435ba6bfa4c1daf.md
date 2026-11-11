# P / DeckShell 适配：feat(surface): opt non-toplevel surfaces into SSD via decoration protocol

- Treeland 来源：` 7d3ec5b27566a7d02d195ef42bdda35012faec2a `。
- 本仓目标：` a88d1d2e5b66c3075fccca5cb435ba6bfa4c1daf `。
- 节点：N10；action=adapted。
- [本仓总记录](../summary.md#entry-122)。

## 比较口径

比较来源唯一父提交 → 来源提交，与原目标唯一父提交 → 原目标提交的逐路径增量。
零上下文补丁对照会呈现基线位置、既有命名和本次实现差异；它不是整棵来源树与目标树的长期差异，也不声称所有显示行都是本次新增适配。
本批没有历史改写；依赖 gitlink 在总记录单列，不混进源码适配。原验收只适用于总记录列出的原节点候选。

## 已审说明

以下保留原证据文字；其中依赖 SHA 属于原运行，新依赖身份见下文与总记录。

- ` Preserve DeckShell layout, DDM guards, external-lock and late-DDE lifetime protections, installed WaylibShared package names and QML URI; integrate source deltas and only the explicitly approved XML/contract inputs. `

保留/映射路径：` compositor/docs/window-decoration-matrix.md `、` compositor/src/core/surfaceprotocolcontroller.cpp `、` compositor/src/modules/decoration/decorationmanagerinterfacev1.cpp `。
排除路径：无。

## 逐路径取舍与实际差异

### ` compositor/docs/window-decoration-matrix.md ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/7d3ec5b27566a7d02d195ef42bdda35012faec2a/parent-review.json`。
- 来源路径：` docs/window-decoration-matrix.md `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` cbebfc9e74b4766b16b3a2f3487d9d895e09e10a ` → ` 7d3ec5b27566a7d02d195ef42bdda35012faec2a `。
- 原目标增量端点：` f8b6bc3cb2f21fc52db555ca1b0821fecf090bfa ` → ` a88d1d2e5b66c3075fccca5cb435ba6bfa4c1daf `。
- 本次目标：` f8b6bc3cb2f21fc52db555ca1b0821fecf090bfa ` → ` a88d1d2e5b66c3075fccca5cb435ba6bfa4c1daf `。
- 目标文件项（mode/type/blob）：` 100644 blob d3a0f51d2a52ab44179c8f7b844a2db0b188f89e ` → ` 100644 blob d2f5b1ebb4aad4cc85c9d50b29aeeaad45d3c0d9 `。
- 来源文件项 ` docs/window-decoration-matrix.md `：` 100644 blob d3a0f51d2a52ab44179c8f7b844a2db0b188f89e ` → ` 100644 blob d2f5b1ebb4aad4cc85c9d50b29aeeaad45d3c0d9 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/src/core/surfaceprotocolcontroller.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/7d3ec5b27566a7d02d195ef42bdda35012faec2a/parent-review.json`。
- 来源路径：` src/core/surfaceprotocolcontroller.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` cbebfc9e74b4766b16b3a2f3487d9d895e09e10a ` → ` 7d3ec5b27566a7d02d195ef42bdda35012faec2a `。
- 原目标增量端点：` f8b6bc3cb2f21fc52db555ca1b0821fecf090bfa ` → ` a88d1d2e5b66c3075fccca5cb435ba6bfa4c1daf `。
- 本次目标：` f8b6bc3cb2f21fc52db555ca1b0821fecf090bfa ` → ` a88d1d2e5b66c3075fccca5cb435ba6bfa4c1daf `。
- 目标文件项（mode/type/blob）：` 100644 blob bdf16034c6ccdaa84c50d9c790f364c5469a9541 ` → ` 100644 blob a835620a7bae40174e45159ce1a037dac59a097f `。
- 来源文件项 ` src/core/surfaceprotocolcontroller.cpp `：` 100644 blob bdf16034c6ccdaa84c50d9c790f364c5469a9541 ` → ` 100644 blob a835620a7bae40174e45159ce1a037dac59a097f `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/src/modules/decoration/decorationmanagerinterfacev1.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/7d3ec5b27566a7d02d195ef42bdda35012faec2a/parent-review.json`。
- 来源路径：` src/modules/decoration/decorationmanagerinterfacev1.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` cbebfc9e74b4766b16b3a2f3487d9d895e09e10a ` → ` 7d3ec5b27566a7d02d195ef42bdda35012faec2a `。
- 原目标增量端点：` f8b6bc3cb2f21fc52db555ca1b0821fecf090bfa ` → ` a88d1d2e5b66c3075fccca5cb435ba6bfa4c1daf `。
- 本次目标：` f8b6bc3cb2f21fc52db555ca1b0821fecf090bfa ` → ` a88d1d2e5b66c3075fccca5cb435ba6bfa4c1daf `。
- 目标文件项（mode/type/blob）：` 100644 blob 9583653c73227cfa67307c1f5c41a5c9d3ecdc61 ` → ` 100644 blob 01ea421135a6915f0d88ad6d7338df01591da26c `。
- 来源文件项 ` src/modules/decoration/decorationmanagerinterfacev1.cpp `：` 100644 blob 9583653c73227cfa67307c1f5c41a5c9d3ecdc61 ` → ` 100644 blob 01ea421135a6915f0d88ad6d7338df01591da26c `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 357fcfa31dc2a67ad874daecc2bd392263d32370 ` → ` 357fcfa31dc2a67ad874daecc2bd392263d32370 `。

## 原工件定位

- mapped_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/7d3ec5b27566a7d02d195ef42bdda35012faec2a/parent-mapped-source.patch`。
- root_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/7d3ec5b27566a7d02d195ef42bdda35012faec2a/parent-root-source.patch`。
- adaptation_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/7d3ec5b27566a7d02d195ef42bdda35012faec2a/parent.patch`。
- target_diff：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/7d3ec5b27566a7d02d195ef42bdda35012faec2a/parent-target.diff`。
