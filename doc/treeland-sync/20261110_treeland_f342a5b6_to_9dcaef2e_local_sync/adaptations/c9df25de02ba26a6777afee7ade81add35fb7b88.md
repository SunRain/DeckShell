# P / DeckShell 适配：feat(examples): add window transition test client

- Treeland 来源：` 4f21a5854ee34371dc086d504b93ffb354a8255f `。
- 本仓目标：` c9df25de02ba26a6777afee7ade81add35fb7b88 `。
- 节点：N10；action=adapted。
- [本仓总记录](../summary.md#entry-19)。

## 比较口径

比较来源唯一父提交 → 来源提交，与原目标唯一父提交 → 原目标提交的逐路径增量。
零上下文补丁对照会呈现基线位置、既有命名和本次实现差异；它不是整棵来源树与目标树的长期差异，也不声称所有显示行都是本次新增适配。
本批没有历史改写；依赖 gitlink 在总记录单列，不混进源码适配。原验收只适用于总记录列出的原节点候选。

## 已审说明

以下保留原证据文字；其中依赖 SHA 属于原运行，新依赖身份见下文与总记录。

- ` Preserve DeckShell layout, DDM guards, external-lock and late-DDE lifetime protections, installed WaylibShared package names and QML URI; integrate source deltas and only the explicitly approved XML/contract inputs. `

保留/映射路径：` compositor/examples/CMakeLists.txt `、` compositor/examples/test-window-transition/CMakeLists.txt `、` compositor/examples/test-window-transition/main.cpp `。
排除路径：无。

## 逐路径取舍与实际差异

### ` compositor/examples/CMakeLists.txt ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/4f21a5854ee34371dc086d504b93ffb354a8255f/parent-review.json`。
- 来源路径：` examples/CMakeLists.txt `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` b63b97c1694526829dbd067d8843882a107b9291 ` → ` 4f21a5854ee34371dc086d504b93ffb354a8255f `。
- 原目标增量端点：` 38048b02ec2aefd5cbd9af09e45d64f69a62683b ` → ` c9df25de02ba26a6777afee7ade81add35fb7b88 `。
- 本次目标：` 38048b02ec2aefd5cbd9af09e45d64f69a62683b ` → ` c9df25de02ba26a6777afee7ade81add35fb7b88 `。
- 目标文件项（mode/type/blob）：` 100644 blob a134fe72f32ec2e3404085735b5bc5ccdbfc2eb7 ` → ` 100644 blob efa6a9fcf00b3656fd252041a19ab1a315be4b2d `。
- 来源文件项 ` examples/CMakeLists.txt `：` 100644 blob a134fe72f32ec2e3404085735b5bc5ccdbfc2eb7 ` → ` 100644 blob efa6a9fcf00b3656fd252041a19ab1a315be4b2d `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/examples/test-window-transition/CMakeLists.txt ` / materialized

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/4f21a5854ee34371dc086d504b93ffb354a8255f/parent-review.json`。
- 来源路径：` examples/test-window-transition/CMakeLists.txt `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` b63b97c1694526829dbd067d8843882a107b9291 ` → ` 4f21a5854ee34371dc086d504b93ffb354a8255f `。
- 原目标增量端点：` 38048b02ec2aefd5cbd9af09e45d64f69a62683b ` → ` c9df25de02ba26a6777afee7ade81add35fb7b88 `。
- 本次目标：` 38048b02ec2aefd5cbd9af09e45d64f69a62683b ` → ` c9df25de02ba26a6777afee7ade81add35fb7b88 `。
- 目标文件项（mode/type/blob）：` None ` → ` 100644 blob 38a655fbd432e940d98af2fe2869d870b72786fb `。
- 来源文件项 ` examples/test-window-transition/CMakeLists.txt `：` None ` → ` 100644 blob 39b51fbbbd75138d120413cac8471aa6cdc02d65 `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,12 +1,11 @@
 new file mode 100644
-@@ -0,0 +1,30 @@
+@@ -0,0 +1,29 @@
 +find_package(Qt6 REQUIRED COMPONENTS Gui WaylandClient Widgets)
 +if(Qt6_VERSION VERSION_GREATER_EQUAL 6.10)
 +    find_package(Qt6 REQUIRED COMPONENTS GuiPrivate WaylandClientPrivate)
 +endif()
 +find_package(PkgConfig REQUIRED)
 +pkg_get_variable(WAYLAND_PROTOCOLS_DATADIR wayland-protocols pkgdatadir)
-+find_package(TreelandProtocols REQUIRED)
 +
 +set(BIN_NAME test-window-transition)
 +
@@ -17,7 +16,7 @@
 +qt_generate_wayland_protocol_client_sources(${BIN_NAME}
 +    FILES
 +        ${WAYLAND_PROTOCOLS_DATADIR}/staging/xdg-activation/xdg-activation-v1.xml
-+        ${TREELAND_PROTOCOLS_DATA_DIR}/treeland-window-transition-unstable-v1.xml
++        ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-window-transition-unstable-v1.xml
 +)
 +
 +target_link_libraries(${BIN_NAME}
```


### ` compositor/examples/test-window-transition/main.cpp ` / materialized

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/4f21a5854ee34371dc086d504b93ffb354a8255f/parent-review.json`。
- 来源路径：` examples/test-window-transition/main.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` b63b97c1694526829dbd067d8843882a107b9291 ` → ` 4f21a5854ee34371dc086d504b93ffb354a8255f `。
- 原目标增量端点：` 38048b02ec2aefd5cbd9af09e45d64f69a62683b ` → ` c9df25de02ba26a6777afee7ade81add35fb7b88 `。
- 本次目标：` 38048b02ec2aefd5cbd9af09e45d64f69a62683b ` → ` c9df25de02ba26a6777afee7ade81add35fb7b88 `。
- 目标文件项（mode/type/blob）：` None ` → ` 100644 blob 51da4cc9fe565977313e9feb947679ca92469bda `。
- 来源文件项 ` examples/test-window-transition/main.cpp `：` None ` → ` 100644 blob 51da4cc9fe565977313e9feb947679ca92469bda `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

- 依赖 ` 3rdparty/waylib-shared `：unchanged；` ff770ab35961c04737758a94cb2360336cd8e96a ` → ` ff770ab35961c04737758a94cb2360336cd8e96a `。

## 原工件定位

- mapped_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/4f21a5854ee34371dc086d504b93ffb354a8255f/parent-mapped-source.patch`。
- root_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/4f21a5854ee34371dc086d504b93ffb354a8255f/parent-root-source.patch`。
- adaptation_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/4f21a5854ee34371dc086d504b93ffb354a8255f/parent.patch`。
- target_diff：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/4f21a5854ee34371dc086d504b93ffb354a8255f/parent-target.diff`。
