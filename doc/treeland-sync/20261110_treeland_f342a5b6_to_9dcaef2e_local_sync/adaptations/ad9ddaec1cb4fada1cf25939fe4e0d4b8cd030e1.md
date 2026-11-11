# P / DeckShell 适配：fix(surface): skip unsupported edge tiling

- Treeland 来源：` c0658911f467a2923ae4c822b4e87c08506a9975 `。
- 本仓目标：` ad9ddaec1cb4fada1cf25939fe4e0d4b8cd030e1 `。
- 节点：N10；action=adapted。
- [本仓总记录](../summary.md#entry-8)。

## 比较口径

比较来源唯一父提交 → 来源提交，与原目标唯一父提交 → 原目标提交的逐路径增量。
零上下文补丁对照会呈现基线位置、既有命名和本次实现差异；它不是整棵来源树与目标树的长期差异，也不声称所有显示行都是本次新增适配。
本批没有历史改写；依赖 gitlink 在总记录单列，不混进源码适配。原验收只适用于总记录列出的原节点候选。

## 已审说明

以下保留原证据文字；其中依赖 SHA 属于原运行，新依赖身份见下文与总记录。

- ` Preserve DeckShell layout, DDM guards, external-lock and late-DDE lifetime protections, installed WaylibShared package names and QML URI; integrate source deltas and only the explicitly approved XML/contract inputs. `

保留/映射路径：` compositor/src/core/rootsurfacecontainer.cpp `、` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
排除路径：无。

## 逐路径取舍与实际差异

### ` compositor/src/core/rootsurfacecontainer.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/c0658911f467a2923ae4c822b4e87c08506a9975/parent-review.json`。
- 来源路径：` src/core/rootsurfacecontainer.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 954d0cce8bda5b34cc635c045e6449bf39e320af ` → ` c0658911f467a2923ae4c822b4e87c08506a9975 `。
- 原目标增量端点：` 9e5bc32642dbbb03cf53fa7a4ff65bb08d053dbd ` → ` ad9ddaec1cb4fada1cf25939fe4e0d4b8cd030e1 `。
- 本次目标：` 9e5bc32642dbbb03cf53fa7a4ff65bb08d053dbd ` → ` ad9ddaec1cb4fada1cf25939fe4e0d4b8cd030e1 `。
- 目标文件项（mode/type/blob）：` 100644 blob e19349afa8e97a3cf238b208dc5a64d039c6186d ` → ` 100644 blob 755b85297d11eac9197536cf388f288660e21e20 `。
- 来源文件项 ` src/core/rootsurfacecontainer.cpp `：` 100644 blob 12a17a96bba98085204c5ba5aba19db428bcb2a2 ` → ` 100644 blob 68ae61405bd327be7a8ee96bc3c3bc4768ae8833 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/src/surface/surfacewrapper.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/c0658911f467a2923ae4c822b4e87c08506a9975/parent-review.json`。
- 来源路径：` src/surface/surfacewrapper.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 954d0cce8bda5b34cc635c045e6449bf39e320af ` → ` c0658911f467a2923ae4c822b4e87c08506a9975 `。
- 原目标增量端点：` 9e5bc32642dbbb03cf53fa7a4ff65bb08d053dbd ` → ` ad9ddaec1cb4fada1cf25939fe4e0d4b8cd030e1 `。
- 本次目标：` 9e5bc32642dbbb03cf53fa7a4ff65bb08d053dbd ` → ` ad9ddaec1cb4fada1cf25939fe4e0d4b8cd030e1 `。
- 目标文件项（mode/type/blob）：` 100644 blob 755f668c7872676a1d0b12832b3a842e63b84533 ` → ` 100644 blob e3c411167379bd5f36ef7b3fdf31936a8d17f659 `。
- 来源文件项 ` src/surface/surfacewrapper.cpp `：` 100644 blob 755f668c7872676a1d0b12832b3a842e63b84533 ` → ` 100644 blob e3c411167379bd5f36ef7b3fdf31936a8d17f659 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/src/surface/surfacewrapper.h ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/c0658911f467a2923ae4c822b4e87c08506a9975/parent-review.json`。
- 来源路径：` src/surface/surfacewrapper.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 954d0cce8bda5b34cc635c045e6449bf39e320af ` → ` c0658911f467a2923ae4c822b4e87c08506a9975 `。
- 原目标增量端点：` 9e5bc32642dbbb03cf53fa7a4ff65bb08d053dbd ` → ` ad9ddaec1cb4fada1cf25939fe4e0d4b8cd030e1 `。
- 本次目标：` 9e5bc32642dbbb03cf53fa7a4ff65bb08d053dbd ` → ` ad9ddaec1cb4fada1cf25939fe4e0d4b8cd030e1 `。
- 目标文件项（mode/type/blob）：` 100644 blob 3585b8018bf7dd8d6b43b40c153e720d627150aa ` → ` 100644 blob d1c58a62416da50fd1f69dc4e1cfe0b487f2bb11 `。
- 来源文件项 ` src/surface/surfacewrapper.h `：` 100644 blob 3585b8018bf7dd8d6b43b40c153e720d627150aa ` → ` 100644 blob d1c58a62416da50fd1f69dc4e1cfe0b487f2bb11 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

- 依赖 ` 3rdparty/waylib-shared `：unchanged；` f1fe3771a9a8fa3037da1d6ab153cc538610b721 ` → ` f1fe3771a9a8fa3037da1d6ab153cc538610b721 `。

## 原工件定位

- mapped_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/c0658911f467a2923ae4c822b4e87c08506a9975/parent-mapped-source.patch`。
- root_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/c0658911f467a2923ae4c822b4e87c08506a9975/parent-root-source.patch`。
- adaptation_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/c0658911f467a2923ae4c822b4e87c08506a9975/parent.patch`。
- target_diff：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/c0658911f467a2923ae4c822b4e87c08506a9975/parent-target.diff`。
