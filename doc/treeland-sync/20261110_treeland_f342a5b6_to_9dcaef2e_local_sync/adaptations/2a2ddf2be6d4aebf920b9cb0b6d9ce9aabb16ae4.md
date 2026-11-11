# P / DeckShell 适配：feat(dock-preview): rebuild the preview strip out of slot instances

- Treeland 来源：` 55a277af889842e450ae5958409eb3163268525d `。
- 本仓目标：` 2a2ddf2be6d4aebf920b9cb0b6d9ce9aabb16ae4 `。
- 节点：N10；action=adapted。
- [本仓总记录](../summary.md#entry-106)。

## 比较口径

比较来源唯一父提交 → 来源提交，与原目标唯一父提交 → 原目标提交的逐路径增量。
零上下文补丁对照会呈现基线位置、既有命名和本次实现差异；它不是整棵来源树与目标树的长期差异，也不声称所有显示行都是本次新增适配。
本批没有历史改写；依赖 gitlink 在总记录单列，不混进源码适配。原验收只适用于总记录列出的原节点候选。

## 已审说明

以下保留原证据文字；其中依赖 SHA 属于原运行，新依赖身份见下文与总记录。

- ` Preserve DeckShell layout, DDM guards, external-lock and late-DDE lifetime protections, installed WaylibShared package names and QML URI; integrate source deltas and only the explicitly approved XML/contract inputs. `

保留/映射路径：` compositor/src/core/qml/DockPreview.qml `。
排除路径：无。

## 逐路径取舍与实际差异

### ` compositor/src/core/qml/DockPreview.qml ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/55a277af889842e450ae5958409eb3163268525d/parent-review.json`。
- 来源路径：` src/core/qml/DockPreview.qml `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` ec6b4fd1267be817be99162dd4aa5a6ee1d76cd7 ` → ` 55a277af889842e450ae5958409eb3163268525d `。
- 原目标增量端点：` 9e9943d0277b9b53768ddd9165361a3bab2d5d8c ` → ` 2a2ddf2be6d4aebf920b9cb0b6d9ce9aabb16ae4 `。
- 本次目标：` 9e9943d0277b9b53768ddd9165361a3bab2d5d8c ` → ` 2a2ddf2be6d4aebf920b9cb0b6d9ce9aabb16ae4 `。
- 目标文件项（mode/type/blob）：` 100644 blob 8a55d56a69c78ff63959ec9c6346e1a0a7ae8c1b ` → ` 100644 blob 3bbac865e0a639915c02de421b63b14850136a1b `。
- 来源文件项 ` src/core/qml/DockPreview.qml `：` 100644 blob aedca30cb7f600e5aa10db1c1861d4cff42267f8 ` → ` 100644 blob c5e6cfa3a5570a28a487e0660dcfc4c08bb2e911 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

- 依赖 ` 3rdparty/waylib-shared `：unchanged；` a1e20b7fe6f02a54e2d689d789c84468cb1c67be ` → ` a1e20b7fe6f02a54e2d689d789c84468cb1c67be `。

## 原工件定位

- mapped_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/55a277af889842e450ae5958409eb3163268525d/parent-mapped-source.patch`。
- root_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/55a277af889842e450ae5958409eb3163268525d/parent-root-source.patch`。
- adaptation_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/55a277af889842e450ae5958409eb3163268525d/parent.patch`。
- target_diff：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/55a277af889842e450ae5958409eb3163268525d/parent-target.diff`。
