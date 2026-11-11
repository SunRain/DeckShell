# P / DeckShell 适配：feat(wlroots): add XCB Shape dependency

- Treeland 来源：` 4258d3fd990988da31d8bb41b563b36b98535878 `。
- 本仓目标：` 215fff3d05d5104de2e3d3ceb69fccbd98bdc48d `。
- 节点：N10；action=adapted。
- [本仓总记录](../summary.md#entry-113)。

## 比较口径

比较来源唯一父提交 → 来源提交，与原目标唯一父提交 → 原目标提交的逐路径增量。
零上下文补丁对照会呈现基线位置、既有命名和本次实现差异；它不是整棵来源树与目标树的长期差异，也不声称所有显示行都是本次新增适配。
本批没有历史改写；依赖 gitlink 在总记录单列，不混进源码适配。原验收只适用于总记录列出的原节点候选。

## 已审说明

以下保留原证据文字；其中依赖 SHA 属于原运行，新依赖身份见下文与总记录。

- ` Preserve DeckShell layout, DDM guards, external-lock and late-DDE lifetime protections, installed WaylibShared package names and QML URI; integrate source deltas and only the explicitly approved XML/contract inputs. `
- ` Includes waylib-shared update to 9d70c7d8a0923f892e22b0edabb25a7660e10fd5. `
- ` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `

保留/映射路径：` compositor/debian/control `。
排除路径：` wlroots/CMakeLists.txt `。

## 逐路径取舍与实际差异

### ` compositor/debian/control ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/4258d3fd990988da31d8bb41b563b36b98535878/parent-review.json`。
- 来源路径：` debian/control `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 8e7f5d53418ac8b7cd79ea17c882469d116ed654 ` → ` 4258d3fd990988da31d8bb41b563b36b98535878 `。
- 原目标增量端点：` 1435406eec1699fc7ab1b4b8bef1d8cbe224361e ` → ` 215fff3d05d5104de2e3d3ceb69fccbd98bdc48d `。
- 本次目标：` 1435406eec1699fc7ab1b4b8bef1d8cbe224361e ` → ` 215fff3d05d5104de2e3d3ceb69fccbd98bdc48d `。
- 目标文件项（mode/type/blob）：` 100644 blob 20b2b1e3e38b1a013e2f53c793c7c176b59abd45 ` → ` 100644 blob 4c5213d633ed23a05398c4f892a89c6bdb85fcad `。
- 来源文件项 ` debian/control `：` 100644 blob 20b2b1e3e38b1a013e2f53c793c7c176b59abd45 ` → ` 100644 blob 4c5213d633ed23a05398c4f892a89c6bdb85fcad `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

- 依赖 ` 3rdparty/waylib-shared `：updated；` b429ece329a8bfc5b0c5bbc2dc749565ae1e8ee2 ` → ` 9d70c7d8a0923f892e22b0edabb25a7660e10fd5 `。

## 原工件定位

- mapped_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/4258d3fd990988da31d8bb41b563b36b98535878/parent-mapped-source.patch`。
- root_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/4258d3fd990988da31d8bb41b563b36b98535878/parent-root-source.patch`。
- adaptation_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/4258d3fd990988da31d8bb41b563b36b98535878/parent.patch`。
- target_diff：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/4258d3fd990988da31d8bb41b563b36b98535878/parent-target.diff`。
