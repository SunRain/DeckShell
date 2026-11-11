# P / DeckShell 适配：test(protocols): add window transition protocol test

- Treeland 来源：` 66d93a08ff5bf55fd5af7da2f5076d77c849abbe `。
- 本仓目标：` d7b660ab8cd6e8abd2ce76fc6dccf1422444cc9e `。
- 节点：N10；action=adapted。
- [本仓总记录](../summary.md#entry-20)。

## 比较口径

比较来源唯一父提交 → 来源提交，与原目标唯一父提交 → 原目标提交的逐路径增量。
零上下文补丁对照会呈现基线位置、既有命名和本次实现差异；它不是整棵来源树与目标树的长期差异，也不声称所有显示行都是本次新增适配。
本批没有历史改写；依赖 gitlink 在总记录单列，不混进源码适配。原验收只适用于总记录列出的原节点候选。

## 已审说明

以下保留原证据文字；其中依赖 SHA 属于原运行，新依赖身份见下文与总记录。

- ` Preserve DeckShell layout, DDM guards, external-lock and late-DDE lifetime protections, installed WaylibShared package names and QML URI; integrate source deltas and only the explicitly approved XML/contract inputs. `

保留/映射路径：` compositor/tests/protocols/CMakeLists.txt `、` compositor/tests/protocols/INDEX.md `、` compositor/tests/protocols/treeland-window-transition-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-window-transition-unstable-v1/README.md `、` compositor/tests/protocols/treeland-window-transition-unstable-v1/setup.cpp `、` compositor/tests/protocols/treeland-window-transition-unstable-v1/treeland-window-transition-unstable-v1.c `、` compositor/tests/protocols/treeland-window-transition-unstable-v1/treeland-window-transition-unstable-v1.h `。
排除路径：无。

## 逐路径取舍与实际差异

### ` compositor/tests/protocols/CMakeLists.txt ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/66d93a08ff5bf55fd5af7da2f5076d77c849abbe/parent-review.json`。
- 来源路径：` tests/protocols/CMakeLists.txt `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 4f21a5854ee34371dc086d504b93ffb354a8255f ` → ` 66d93a08ff5bf55fd5af7da2f5076d77c849abbe `。
- 原目标增量端点：` c9df25de02ba26a6777afee7ade81add35fb7b88 ` → ` d7b660ab8cd6e8abd2ce76fc6dccf1422444cc9e `。
- 本次目标：` c9df25de02ba26a6777afee7ade81add35fb7b88 ` → ` d7b660ab8cd6e8abd2ce76fc6dccf1422444cc9e `。
- 目标文件项（mode/type/blob）：` 100644 blob d60e9cc1c78aa7a941d031f904e9581510c7ebad ` → ` 100644 blob 405bf8c994973f0389c576d264ced2e0acb9065b `。
- 来源文件项 ` tests/protocols/CMakeLists.txt `：` 100644 blob 6693143c3ef673d5373518f55c0c2236e0b1a753 ` → ` 100644 blob b313acd35dbb86e2c99b691b8a64ee52e39d3801 `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,2 +1,2 @@
-@@ -69,0 +70 @@ add_subdirectory(treeland-show-desktop-desktop-v1)
+@@ -71,0 +72 @@ add_subdirectory(treeland-show-desktop-desktop-v1)
 +add_subdirectory(treeland-window-transition-unstable-v1)
```


### ` compositor/tests/protocols/INDEX.md ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/66d93a08ff5bf55fd5af7da2f5076d77c849abbe/parent-review.json`。
- 来源路径：` tests/protocols/INDEX.md `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 4f21a5854ee34371dc086d504b93ffb354a8255f ` → ` 66d93a08ff5bf55fd5af7da2f5076d77c849abbe `。
- 原目标增量端点：` c9df25de02ba26a6777afee7ade81add35fb7b88 ` → ` d7b660ab8cd6e8abd2ce76fc6dccf1422444cc9e `。
- 本次目标：` c9df25de02ba26a6777afee7ade81add35fb7b88 ` → ` d7b660ab8cd6e8abd2ce76fc6dccf1422444cc9e `。
- 目标文件项（mode/type/blob）：` 100644 blob 3d672d88a939d38d32a6b7da6bd96d20656b6821 ` → ` 100644 blob 517692540aed262d8e5cfd6068bf59dceadf2713 `。
- 来源文件项 ` tests/protocols/INDEX.md `：` 100644 blob 3d672d88a939d38d32a6b7da6bd96d20656b6821 ` → ` 100644 blob 517692540aed262d8e5cfd6068bf59dceadf2713 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/tests/protocols/treeland-window-transition-unstable-v1/CMakeLists.txt ` / materialized

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/66d93a08ff5bf55fd5af7da2f5076d77c849abbe/parent-review.json`。
- 来源路径：` tests/protocols/treeland-window-transition-unstable-v1/CMakeLists.txt `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 4f21a5854ee34371dc086d504b93ffb354a8255f ` → ` 66d93a08ff5bf55fd5af7da2f5076d77c849abbe `。
- 原目标增量端点：` c9df25de02ba26a6777afee7ade81add35fb7b88 ` → ` d7b660ab8cd6e8abd2ce76fc6dccf1422444cc9e `。
- 本次目标：` c9df25de02ba26a6777afee7ade81add35fb7b88 ` → ` d7b660ab8cd6e8abd2ce76fc6dccf1422444cc9e `。
- 目标文件项（mode/type/blob）：` None ` → ` 100644 blob 9ffca7e0247045eeb2c5f4151a57bff7c654ee2c `。
- 来源文件项 ` tests/protocols/treeland-window-transition-unstable-v1/CMakeLists.txt `：` None ` → ` 100644 blob 3324c22d6a024a0fa88606aa40e0c4cfbe7ededb `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -3,7 +3,7 @@
 +# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
 +treeland_add_protocol_test(
 +    NAME treeland_window_transition_unstable_v1
-+    XML "${TREELAND_PROTOCOLS_DATA_DIR}/treeland-window-transition-unstable-v1.xml"
++    XML "${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-window-transition-unstable-v1.xml"
 +    SETUP "${CMAKE_CURRENT_SOURCE_DIR}/setup.cpp"
 +    CLIENT "${CMAKE_CURRENT_SOURCE_DIR}/treeland-window-transition-unstable-v1.c"
 +    EXTRA_XMLS "${WAYLAND_PROTOCOLS_DATADIR}/staging/xdg-activation/xdg-activation-v1.xml"
```


### ` compositor/tests/protocols/treeland-window-transition-unstable-v1/README.md ` / materialized

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/66d93a08ff5bf55fd5af7da2f5076d77c849abbe/parent-review.json`。
- 来源路径：` tests/protocols/treeland-window-transition-unstable-v1/README.md `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 4f21a5854ee34371dc086d504b93ffb354a8255f ` → ` 66d93a08ff5bf55fd5af7da2f5076d77c849abbe `。
- 原目标增量端点：` c9df25de02ba26a6777afee7ade81add35fb7b88 ` → ` d7b660ab8cd6e8abd2ce76fc6dccf1422444cc9e `。
- 本次目标：` c9df25de02ba26a6777afee7ade81add35fb7b88 ` → ` d7b660ab8cd6e8abd2ce76fc6dccf1422444cc9e `。
- 目标文件项（mode/type/blob）：` None ` → ` 100644 blob c2d8716164f42a1eb8807410865ece27a11e57ff `。
- 来源文件项 ` tests/protocols/treeland-window-transition-unstable-v1/README.md `：` None ` → ` 100644 blob c2d8716164f42a1eb8807410865ece27a11e57ff `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/tests/protocols/treeland-window-transition-unstable-v1/setup.cpp ` / materialized

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/66d93a08ff5bf55fd5af7da2f5076d77c849abbe/parent-review.json`。
- 来源路径：` tests/protocols/treeland-window-transition-unstable-v1/setup.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 4f21a5854ee34371dc086d504b93ffb354a8255f ` → ` 66d93a08ff5bf55fd5af7da2f5076d77c849abbe `。
- 原目标增量端点：` c9df25de02ba26a6777afee7ade81add35fb7b88 ` → ` d7b660ab8cd6e8abd2ce76fc6dccf1422444cc9e `。
- 本次目标：` c9df25de02ba26a6777afee7ade81add35fb7b88 ` → ` d7b660ab8cd6e8abd2ce76fc6dccf1422444cc9e `。
- 目标文件项（mode/type/blob）：` None ` → ` 100644 blob a468ec107bbd32923d497f7411259014ab4ba620 `。
- 来源文件项 ` tests/protocols/treeland-window-transition-unstable-v1/setup.cpp `：` None ` → ` 100644 blob a468ec107bbd32923d497f7411259014ab4ba620 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/tests/protocols/treeland-window-transition-unstable-v1/treeland-window-transition-unstable-v1.c ` / materialized

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/66d93a08ff5bf55fd5af7da2f5076d77c849abbe/parent-review.json`。
- 来源路径：` tests/protocols/treeland-window-transition-unstable-v1/treeland-window-transition-unstable-v1.c `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 4f21a5854ee34371dc086d504b93ffb354a8255f ` → ` 66d93a08ff5bf55fd5af7da2f5076d77c849abbe `。
- 原目标增量端点：` c9df25de02ba26a6777afee7ade81add35fb7b88 ` → ` d7b660ab8cd6e8abd2ce76fc6dccf1422444cc9e `。
- 本次目标：` c9df25de02ba26a6777afee7ade81add35fb7b88 ` → ` d7b660ab8cd6e8abd2ce76fc6dccf1422444cc9e `。
- 目标文件项（mode/type/blob）：` None ` → ` 100644 blob 8a16d668c514970accfaa3f5fa17902b87558421 `。
- 来源文件项 ` tests/protocols/treeland-window-transition-unstable-v1/treeland-window-transition-unstable-v1.c `：` None ` → ` 100644 blob 8a16d668c514970accfaa3f5fa17902b87558421 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/tests/protocols/treeland-window-transition-unstable-v1/treeland-window-transition-unstable-v1.h ` / materialized

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/66d93a08ff5bf55fd5af7da2f5076d77c849abbe/parent-review.json`。
- 来源路径：` tests/protocols/treeland-window-transition-unstable-v1/treeland-window-transition-unstable-v1.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 4f21a5854ee34371dc086d504b93ffb354a8255f ` → ` 66d93a08ff5bf55fd5af7da2f5076d77c849abbe `。
- 原目标增量端点：` c9df25de02ba26a6777afee7ade81add35fb7b88 ` → ` d7b660ab8cd6e8abd2ce76fc6dccf1422444cc9e `。
- 本次目标：` c9df25de02ba26a6777afee7ade81add35fb7b88 ` → ` d7b660ab8cd6e8abd2ce76fc6dccf1422444cc9e `。
- 目标文件项（mode/type/blob）：` None ` → ` 100644 blob 045fe0f07a0cb797ee274ae8ecea664f28ed2c33 `。
- 来源文件项 ` tests/protocols/treeland-window-transition-unstable-v1/treeland-window-transition-unstable-v1.h `：` None ` → ` 100644 blob 045fe0f07a0cb797ee274ae8ecea664f28ed2c33 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

- 依赖 ` 3rdparty/waylib-shared `：unchanged；` ff770ab35961c04737758a94cb2360336cd8e96a ` → ` ff770ab35961c04737758a94cb2360336cd8e96a `。

## 原工件定位

- mapped_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/66d93a08ff5bf55fd5af7da2f5076d77c849abbe/parent-mapped-source.patch`。
- root_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/66d93a08ff5bf55fd5af7da2f5076d77c849abbe/parent-root-source.patch`。
- adaptation_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/66d93a08ff5bf55fd5af7da2f5076d77c849abbe/parent.patch`。
- target_diff：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/66d93a08ff5bf55fd5af7da2f5076d77c849abbe/parent-target.diff`。
