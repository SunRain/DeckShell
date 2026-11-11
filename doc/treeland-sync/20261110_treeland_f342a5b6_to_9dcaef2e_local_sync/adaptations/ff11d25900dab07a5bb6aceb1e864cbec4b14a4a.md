# P / DeckShell 适配：chore: remove deprecated window picker and multitaskview code

- Treeland 来源：` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 本仓目标：` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 节点：N10；action=adapted。
- [本仓总记录](../summary.md#entry-4)。

## 比较口径

比较来源唯一父提交 → 来源提交，与原目标唯一父提交 → 原目标提交的逐路径增量。
零上下文补丁对照会呈现基线位置、既有命名和本次实现差异；它不是整棵来源树与目标树的长期差异，也不声称所有显示行都是本次新增适配。
本批没有历史改写；依赖 gitlink 在总记录单列，不混进源码适配。原验收只适用于总记录列出的原节点候选。

## 已审说明

以下保留原证据文字；其中依赖 SHA 属于原运行，新依赖身份见下文与总记录。

- ` Preserve DeckShell layout, DDM guards, external-lock and late-DDE lifetime protections, installed WaylibShared package names and QML URI; integrate source deltas and only the explicitly approved XML/contract inputs. `

保留/映射路径：` compositor/examples/CMakeLists.txt `、` compositor/examples/test_multitaskview/CMakeLists.txt `、` compositor/examples/test_multitaskview/Main.qml `、` compositor/examples/test_multitaskview/ddeshell.cpp `、` compositor/examples/test_multitaskview/ddeshell.h `、` compositor/examples/test_multitaskview/main.cpp `、` compositor/examples/test_window_picker/CMakeLists.txt `、` compositor/examples/test_window_picker/Main.qml `、` compositor/examples/test_window_picker/ddeshell.cpp `、` compositor/examples/test_window_picker/ddeshell.h `、` compositor/examples/test_window_picker/main.cpp `、` compositor/src/CMakeLists.txt `、` compositor/src/core/qml/WindowPickerLayer.qml `、` compositor/src/core/qmlengine.cpp `、` compositor/src/core/qmlengine.h `、` compositor/src/core/windowpicker.cpp `、` compositor/src/core/windowpicker.h `、` compositor/src/modules/dde-shell/ddeshellmanagerinterfacev1.cpp `、` compositor/src/modules/dde-shell/ddeshellmanagerinterfacev1.h `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/tests/protocols/CMakeLists.txt `、` compositor/tests/protocols/INDEX.md `、` compositor/tests/protocols/treeland-dde-shell-picker-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-dde-shell-picker-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-dde-shell-picker-desktop-v1/treeland-dde-shell-picker-desktop-v1.c `、` compositor/tests/protocols/treeland-dde-shell-picker-desktop-v1/treeland-dde-shell-picker-desktop-v1.h `、` compositor/tests/protocols/treeland-dde-shell-v1/README.md `、` compositor/tests/protocols/treeland-dde-shell-v1/setup.cpp `、` compositor/tests/protocols/treeland-dde-shell-v1/treeland-dde-shell-v1.c `、` compositor/tests/protocols/treeland-dde-shell-v1/treeland-dde-shell-v1.h `、` compositor/tests/test_window_picker/CMakeLists.txt `、` compositor/tests/test_window_picker/Main.qml `、` compositor/tests/test_window_picker/ddeshell.cpp `、` compositor/tests/test_window_picker/ddeshell.h `、` compositor/tests/test_window_picker/main.cpp `。
排除路径：无。

## 逐路径取舍与实际差异

### ` compositor/examples/CMakeLists.txt ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` examples/CMakeLists.txt `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 4db57e30d8c0a88051db364b57a145338a6aa3ff ` → ` 100644 blob a134fe72f32ec2e3404085735b5bc5ccdbfc2eb7 `。
- 来源文件项 ` examples/CMakeLists.txt `：` 100644 blob 4db57e30d8c0a88051db364b57a145338a6aa3ff ` → ` 100644 blob a134fe72f32ec2e3404085735b5bc5ccdbfc2eb7 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/examples/test_multitaskview/CMakeLists.txt ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` examples/test_multitaskview/CMakeLists.txt `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 0593d4ec2f456e91c897c9b18b1bb96d25e7d238 ` → ` None `。
- 来源文件项 ` examples/test_multitaskview/CMakeLists.txt `：` 100644 blob 32f7937ac8f0522d5f974e2e5580ca7e21c53105 ` → ` None `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,10 +1,9 @@
 deleted file mode 100644
-@@ -1,39 +0,0 @@
+@@ -1,38 +0,0 @@
 -find_package(Qt6 REQUIRED COMPONENTS Gui Quick WaylandClient)
 -if(Qt6_VERSION VERSION_GREATER_EQUAL 6.10)
 -    find_package(Qt6 REQUIRED COMPONENTS WaylandClientPrivate)
 -endif()
--find_package(TreelandProtocols REQUIRED)
 -
 -set(BIN_NAME test-multitaskview)
 -
@@ -27,7 +26,7 @@
 -qt_generate_wayland_protocol_client_sources(${BIN_NAME}
 -    NO_INCLUDE_CORE_ONLY
 -    FILES
--        ${TREELAND_PROTOCOLS_DATA_DIR}/treeland-dde-shell-v1.xml
+-        ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-dde-shell-v1.xml
 -)
 -
 -target_link_libraries(${BIN_NAME}
```


### ` compositor/examples/test_multitaskview/Main.qml ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` examples/test_multitaskview/Main.qml `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob cee7467a6592aa2479cd99f8dc7fcc73a4222574 ` → ` None `。
- 来源文件项 ` examples/test_multitaskview/Main.qml `：` 100644 blob cee7467a6592aa2479cd99f8dc7fcc73a4222574 ` → ` None `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/examples/test_multitaskview/ddeshell.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` examples/test_multitaskview/ddeshell.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob b728acbf9518f279a278be9351f969869433af0a ` → ` None `。
- 来源文件项 ` examples/test_multitaskview/ddeshell.cpp `：` 100644 blob b728acbf9518f279a278be9351f969869433af0a ` → ` None `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/examples/test_multitaskview/ddeshell.h ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` examples/test_multitaskview/ddeshell.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 3e42738af78e0e473befd8e32585b947defd80d0 ` → ` None `。
- 来源文件项 ` examples/test_multitaskview/ddeshell.h `：` 100644 blob 3e42738af78e0e473befd8e32585b947defd80d0 ` → ` None `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/examples/test_multitaskview/main.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` examples/test_multitaskview/main.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob e37e67f93941e1891c938634c091d5a1a3c9b504 ` → ` None `。
- 来源文件项 ` examples/test_multitaskview/main.cpp `：` 100644 blob e37e67f93941e1891c938634c091d5a1a3c9b504 ` → ` None `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/examples/test_window_picker/CMakeLists.txt ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` examples/test_window_picker/CMakeLists.txt `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob dca5839bacf16e1702e8af5ba5e308337b6f3693 ` → ` None `。
- 来源文件项 ` examples/test_window_picker/CMakeLists.txt `：` 100644 blob 8f6e2b5aabe61a58fe5e8d434f5917d6c408063d ` → ` None `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,10 +1,9 @@
 deleted file mode 100644
-@@ -1,39 +0,0 @@
+@@ -1,38 +0,0 @@
 -find_package(Qt6 REQUIRED COMPONENTS Gui Quick WaylandClient)
 -if(Qt6_VERSION VERSION_GREATER_EQUAL 6.10)
 -    find_package(Qt6 REQUIRED COMPONENTS WaylandClientPrivate)
 -endif()
--find_package(TreelandProtocols REQUIRED)
 -
 -set(BIN_NAME test-window-picker)
 -
@@ -27,7 +26,7 @@
 -qt_generate_wayland_protocol_client_sources(${BIN_NAME}
 -    NO_INCLUDE_CORE_ONLY
 -    FILES
--        ${TREELAND_PROTOCOLS_DATA_DIR}/treeland-dde-shell-v1.xml
+-        ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-dde-shell-v1.xml
 -)
 -
 -target_link_libraries(${BIN_NAME}
```


### ` compositor/examples/test_window_picker/Main.qml ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` examples/test_window_picker/Main.qml `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob f88dcf589bf57aa9195858818974d1e33ba412e1 ` → ` None `。
- 来源文件项 ` examples/test_window_picker/Main.qml `：` 100644 blob f88dcf589bf57aa9195858818974d1e33ba412e1 ` → ` None `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/examples/test_window_picker/ddeshell.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` examples/test_window_picker/ddeshell.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 01c384deab43e8682c314477f7af9a1eb66a4993 ` → ` None `。
- 来源文件项 ` examples/test_window_picker/ddeshell.cpp `：` 100644 blob 01c384deab43e8682c314477f7af9a1eb66a4993 ` → ` None `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/examples/test_window_picker/ddeshell.h ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` examples/test_window_picker/ddeshell.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 9ee7b2be5aab5252add9459e9ae004f6f069991c ` → ` None `。
- 来源文件项 ` examples/test_window_picker/ddeshell.h `：` 100644 blob 9ee7b2be5aab5252add9459e9ae004f6f069991c ` → ` None `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/examples/test_window_picker/main.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` examples/test_window_picker/main.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 6874f451d1ecfdc8a22a7b6ed7b76409e9b01606 ` → ` None `。
- 来源文件项 ` examples/test_window_picker/main.cpp `：` 100644 blob 6874f451d1ecfdc8a22a7b6ed7b76409e9b01606 ` → ` None `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/src/CMakeLists.txt ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` src/CMakeLists.txt `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob cf884aefa0de1dafa608edcd5df6ed521bf78336 ` → ` 100644 blob 1098e175f3af0cc64869d5b48e356c055154f492 `。
- 来源文件项 ` src/CMakeLists.txt `：` 100644 blob 78c154044ffd762e55b7a024482e21452840904e ` → ` 100644 blob 2e7b88f9e255107d90b395b4ee972eabb18d5074 `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,5 +1,5 @@
-@@ -151,2 +150,0 @@ qt_add_qml_module(libtreeland
+@@ -154,2 +153,0 @@ qt_add_qml_module(libdeckcompositor
 -        core/windowpicker.cpp
 -        core/windowpicker.h
-@@ -274 +271,0 @@ qt_add_qml_module(libtreeland
+@@ -278 +275,0 @@ qt_add_qml_module(libdeckcompositor
 -        core/qml/WindowPickerLayer.qml
```


### ` compositor/src/core/qml/WindowPickerLayer.qml ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` src/core/qml/WindowPickerLayer.qml `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob c666d91d5630fe65d0f44a2d30cf7ce9ca4db212 ` → ` None `。
- 来源文件项 ` src/core/qml/WindowPickerLayer.qml `：` 100644 blob d24e40b7089ddccf568dee55f647154dc0a7f9dc ` → ` None `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -4,7 +4,7 @@
 -// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
 -
 -import QtQuick
--import Treeland
+-import DeckShell.Compositor
 -
 -WindowPicker {
 -    anchors.fill: parent
```


### ` compositor/src/core/qmlengine.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` src/core/qmlengine.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob dbc4e6afe247e64686647b1b1558f23367a58c86 ` → ` 100644 blob f0a2644ebd15eafb846dc1941d3bbcddabe30505 `。
- 来源文件项 ` src/core/qmlengine.cpp `：` 100644 blob 3ddf1dbd93e8d433366b9d0e940fb39ae28ecd27 ` → ` 100644 blob 0a5d00148114bdb997849afeb3796fa691387a4e `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,5 +1,5 @@
 @@ -56 +55,0 @@ QmlEngine::QmlEngine(QObject *parent)
--    , windowPickerComponent(this, "Treeland", "WindowPickerLayer")
+-    , windowPickerComponent(this, "DeckShell.Compositor", "WindowPickerLayer")
 @@ -262,5 +260,0 @@ QQuickItem *QmlEngine::createCaptureSelector(QQuickItem *parent, CaptureManagerV
 -QQuickItem *QmlEngine::createWindowPicker(QQuickItem *parent)
 -{
```


### ` compositor/src/core/qmlengine.h ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` src/core/qmlengine.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 3492c14660fb1cb422383771c0a7bbfc1169472b ` → ` 100644 blob 3c031eaf3890c3a36c6b67f5a67861ba2072cba3 `。
- 来源文件项 ` src/core/qmlengine.h `：` 100644 blob 3492c14660fb1cb422383771c0a7bbfc1169472b ` → ` 100644 blob 3c031eaf3890c3a36c6b67f5a67861ba2072cba3 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/src/core/windowpicker.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` src/core/windowpicker.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob d099d43ac4c307cd33d50db5558e296e87c153f8 ` → ` None `。
- 来源文件项 ` src/core/windowpicker.cpp `：` 100644 blob d099d43ac4c307cd33d50db5558e296e87c153f8 ` → ` None `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/src/core/windowpicker.h ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` src/core/windowpicker.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 08c1be66c35997433c74fd234722ed748c117c9c ` → ` None `。
- 来源文件项 ` src/core/windowpicker.h `：` 100644 blob 08c1be66c35997433c74fd234722ed748c117c9c ` → ` None `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/src/modules/dde-shell/ddeshellmanagerinterfacev1.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` src/modules/dde-shell/ddeshellmanagerinterfacev1.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 6fc1b966ae89175f9b1862959d55723402f2b3f8 ` → ` 100644 blob 9ae679945a8d7376bca0a2986718f99810e6f6b1 `。
- 来源文件项 ` src/modules/dde-shell/ddeshellmanagerinterfacev1.cpp `：` 100644 blob e9f37bcae603aca3b57067886497d9a5ae4c760c ` → ` 100644 blob d5e565ee970443f83a5add3b63900e8d0d028427 `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,8 +1,8 @@
 @@ -25 +24,0 @@ static QList<MultiTaskViewInterface *> s_multiTaskViews;
 -static QList<WindowPickerInterface *> s_windowPickers;
-@@ -42 +40,0 @@ protected:
+@@ -43 +41,0 @@ protected:
 -    void get_treeland_window_picker(Resource *resource, uint32_t id) override;
-@@ -207,26 +204,0 @@ void DDEShellManagerInterfaceV1Private::get_treeland_multitaskview(Resource *res
+@@ -213,26 +210,0 @@ void DDEShellManagerInterfaceV1Private::get_treeland_multitaskview(Resource *res
 -void DDEShellManagerInterfaceV1Private::get_treeland_window_picker(Resource *resource,
 -                                                                   uint32_t id)
 -{
@@ -29,7 +29,7 @@
 -    Q_EMIT q->PickerCreated(windowPicker);
 -}
 -
-@@ -747,49 +718,0 @@ MultiTaskViewInterface::MultiTaskViewInterface(wl_resource *resource)
+@@ -753,49 +724,0 @@ MultiTaskViewInterface::MultiTaskViewInterface(wl_resource *resource)
 -class WindowPickerInterfacePrivate : public QtWaylandServer::treeland_window_picker_v1
 -{
 -public:
```


### ` compositor/src/modules/dde-shell/ddeshellmanagerinterfacev1.h ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` src/modules/dde-shell/ddeshellmanagerinterfacev1.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 9828faf3a5525079d2c7d26776554007fd91dbe2 ` → ` 100644 blob 72cd7488cb2134f34213834445fb0eba7ef6d2e4 `。
- 来源文件项 ` src/modules/dde-shell/ddeshellmanagerinterfacev1.h `：` 100644 blob 68ab69398c50546e9121962c3abf219f89165a0f ` → ` 100644 blob 099710fdbddaf206511bc9d81b4c91c6ebbc259b `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/src/seat/helper.cpp ` / modified

- 原审核理由：` Reviewed three-way resolution preserving local package, runtime and regression integration. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` src/seat/helper.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 826b1e9b7439cc0c1473673f5e1b556f107dab15 ` → ` 100644 blob 9c1c89f1f7a6c0351f343b146e24da689e887dda `。
- 来源文件项 ` src/seat/helper.cpp `：` 100644 blob 66dc15f57eddad0b2fb6e027176fff801e724b7c ` → ` 100644 blob 58e7330f7bec526063b76dac2af2800c6e2573ff `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,11 +1,11 @@
 @@ -33 +32,0 @@
 -#include "core/windowpicker.h"
-@@ -912,4 +910,0 @@ void Helper::init(Treeland::Treeland *treeland)
+@@ -968,4 +966,0 @@ void Helper::init(Treeland::Treeland *treeland)
 -    connect(m_ddeShellV1,
 -            &DDEShellManagerInterfaceV1::PickerCreated,
 -            this,
 -            &Helper::handleWindowPicker);
-@@ -2115,24 +2109,0 @@ QString Helper::currentLockScreenWallpaper(WOutput *output)
+@@ -2234,24 +2228,0 @@ QString Helper::currentLockScreenWallpaper(WOutput *output)
 -void Helper::handleWindowPicker(WindowPickerInterface *picker)
 -{
 -    connect(picker, &WindowPickerInterface::pick, this, [this, picker](const QString &hint) {
```


### ` compositor/src/seat/helper.h ` / modified

- 原审核理由：` Reviewed three-way resolution preserving local package, runtime and regression integration. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` src/seat/helper.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 418f50d883aa5c38ec181f932a88c255512351d7 ` → ` 100644 blob 85ad71505d3828d44c305fecb994d3cacb3f4dec `。
- 来源文件项 ` src/seat/helper.h `：` 100644 blob 4359e9278255d7249d6d0aaffb87eb24cccf5adb ` → ` 100644 blob 50ec6f57f13187d32254092cfca085a5722771ac `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,5 +1,5 @@
-@@ -126 +125,0 @@ class ShowDesktopInterfaceV1;
+@@ -133 +132,0 @@ class ShowDesktopInterfaceV1;
 -class WindowPickerInterface;
-@@ -224,2 +222,0 @@ public:
+@@ -233,2 +231,0 @@ public:
 -    void handleWindowPicker(WindowPickerInterface *picker);
 -
```


### ` compositor/tests/protocols/CMakeLists.txt ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` tests/protocols/CMakeLists.txt `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 58a8bb09aaf9e42e9d2c7d5b64327011eb6ea6b4 ` → ` 100644 blob d60e9cc1c78aa7a941d031f904e9581510c7ebad `。
- 来源文件项 ` tests/protocols/CMakeLists.txt `：` 100644 blob 2076ae5263ecc9f0f5d0089105de441425c63315 ` → ` 100644 blob 6693143c3ef673d5373518f55c0c2236e0b1a753 `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,2 +1,2 @@
-@@ -42 +41,0 @@ add_subdirectory(treeland-dde-shell-multitask-desktop-v1)
+@@ -44 +43,0 @@ add_subdirectory(treeland-dde-shell-multitask-desktop-v1)
 -add_subdirectory(treeland-dde-shell-picker-desktop-v1)
```


### ` compositor/tests/protocols/INDEX.md ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` tests/protocols/INDEX.md `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 81108f93d6f5bfe63eb18110e37b0776e8698810 ` → ` 100644 blob a824bd0a65fea618e4cbca64318b85c159ae9981 `。
- 来源文件项 ` tests/protocols/INDEX.md `：` 100644 blob 81108f93d6f5bfe63eb18110e37b0776e8698810 ` → ` 100644 blob a824bd0a65fea618e4cbca64318b85c159ae9981 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/tests/protocols/treeland-dde-shell-picker-desktop-v1/CMakeLists.txt ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` tests/protocols/treeland-dde-shell-picker-desktop-v1/CMakeLists.txt `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 5ec5463b1507602908e5121e1a7e9fa3afacfe3d ` → ` None `。
- 来源文件项 ` tests/protocols/treeland-dde-shell-picker-desktop-v1/CMakeLists.txt `：` 100644 blob d02c86b978c92ad27b3e85860a9025e29f795233 ` → ` None `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -3,7 +3,7 @@
 -
 -treeland_add_protocol_test(
 -    NAME treeland_dde_shell_picker_desktop_v1
--    XML "${TREELAND_PROTOCOLS_DATA_DIR}/treeland-dde-shell-v1.xml"
+-    XML "${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-dde-shell-v1.xml"
 -    SETUP "${CMAKE_CURRENT_SOURCE_DIR}/setup.cpp"
 -    CLIENT "${CMAKE_CURRENT_SOURCE_DIR}/treeland-dde-shell-picker-desktop-v1.c"
 -)
```


### ` compositor/tests/protocols/treeland-dde-shell-picker-desktop-v1/setup.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` tests/protocols/treeland-dde-shell-picker-desktop-v1/setup.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob de614f3298617b614a6eec02e01965cce3786725 ` → ` None `。
- 来源文件项 ` tests/protocols/treeland-dde-shell-picker-desktop-v1/setup.cpp `：` 100644 blob de614f3298617b614a6eec02e01965cce3786725 ` → ` None `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/tests/protocols/treeland-dde-shell-picker-desktop-v1/treeland-dde-shell-picker-desktop-v1.c ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` tests/protocols/treeland-dde-shell-picker-desktop-v1/treeland-dde-shell-picker-desktop-v1.c `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 3c08365a9b4a1e4bd138c3532d7f5eabdd448264 ` → ` None `。
- 来源文件项 ` tests/protocols/treeland-dde-shell-picker-desktop-v1/treeland-dde-shell-picker-desktop-v1.c `：` 100644 blob 3c08365a9b4a1e4bd138c3532d7f5eabdd448264 ` → ` None `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/tests/protocols/treeland-dde-shell-picker-desktop-v1/treeland-dde-shell-picker-desktop-v1.h ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` tests/protocols/treeland-dde-shell-picker-desktop-v1/treeland-dde-shell-picker-desktop-v1.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 9348ab6da36accf552c1216287375c27903af606 ` → ` None `。
- 来源文件项 ` tests/protocols/treeland-dde-shell-picker-desktop-v1/treeland-dde-shell-picker-desktop-v1.h `：` 100644 blob 9348ab6da36accf552c1216287375c27903af606 ` → ` None `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/tests/protocols/treeland-dde-shell-v1/README.md ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` tests/protocols/treeland-dde-shell-v1/README.md `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 7294bd64a28c7395858eb9783e2cb241f8d664d6 ` → ` 100644 blob 94072f1f7b2c6fc0c27f20d58f95024303d5ed03 `。
- 来源文件项 ` tests/protocols/treeland-dde-shell-v1/README.md `：` 100644 blob 7294bd64a28c7395858eb9783e2cb241f8d664d6 ` → ` 100644 blob 94072f1f7b2c6fc0c27f20d58f95024303d5ed03 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/tests/protocols/treeland-dde-shell-v1/setup.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` tests/protocols/treeland-dde-shell-v1/setup.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 7deb91902ed76de4ba53b92a60faed09d85405b8 ` → ` 100644 blob 63bdd24138dc57397543d9bd3c384e48e46555f7 `。
- 来源文件项 ` tests/protocols/treeland-dde-shell-v1/setup.cpp `：` 100644 blob 7deb91902ed76de4ba53b92a60faed09d85405b8 ` → ` 100644 blob 63bdd24138dc57397543d9bd3c384e48e46555f7 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/tests/protocols/treeland-dde-shell-v1/treeland-dde-shell-v1.c ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` tests/protocols/treeland-dde-shell-v1/treeland-dde-shell-v1.c `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 099fbf22c988b8140261787d01cf925f03692413 ` → ` 100644 blob 9b39e31539ccd5d458c1109d75e284a00d16df10 `。
- 来源文件项 ` tests/protocols/treeland-dde-shell-v1/treeland-dde-shell-v1.c `：` 100644 blob 099fbf22c988b8140261787d01cf925f03692413 ` → ` 100644 blob 9b39e31539ccd5d458c1109d75e284a00d16df10 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/tests/protocols/treeland-dde-shell-v1/treeland-dde-shell-v1.h ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` tests/protocols/treeland-dde-shell-v1/treeland-dde-shell-v1.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 7b66b59e79a9624b57bc09d76dbc47cd02cdfa68 ` → ` 100644 blob c4d66628efffe15665058bd9039e0d3f9947a5d9 `。
- 来源文件项 ` tests/protocols/treeland-dde-shell-v1/treeland-dde-shell-v1.h `：` 100644 blob 7b66b59e79a9624b57bc09d76dbc47cd02cdfa68 ` → ` 100644 blob c4d66628efffe15665058bd9039e0d3f9947a5d9 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/tests/test_window_picker/CMakeLists.txt ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` tests/test_window_picker/CMakeLists.txt `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 5d2a8508fcbc107af23fd750464987e566aa3d10 ` → ` None `。
- 来源文件项 ` tests/test_window_picker/CMakeLists.txt `：` 100644 blob 3f2664592ba517cc1c298b2f9c9995ce13bd803a ` → ` None `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,10 +1,9 @@
 deleted file mode 100644
-@@ -1,38 +0,0 @@
+@@ -1,37 +0,0 @@
 -find_package(Qt6 REQUIRED COMPONENTS WaylandClient Quick)
 -if(Qt6_VERSION VERSION_GREATER_EQUAL 6.10)
 -    find_package(Qt6 REQUIRED COMPONENTS WaylandClientPrivate)
 -endif()
--find_package(TreelandProtocols REQUIRED)
 -
 -set(BIN_NAME test-window-picker)
 -
@@ -27,7 +26,7 @@
 -qt_generate_wayland_protocol_client_sources(${BIN_NAME}
 -    NO_INCLUDE_CORE_ONLY
 -    FILES
--        ${TREELAND_PROTOCOLS_DATA_DIR}/treeland-dde-shell-v1.xml
+-        ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-dde-shell-v1.xml
 -)
 -
 -target_link_libraries(${BIN_NAME}
```


### ` compositor/tests/test_window_picker/Main.qml ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` tests/test_window_picker/Main.qml `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob f88dcf589bf57aa9195858818974d1e33ba412e1 ` → ` None `。
- 来源文件项 ` tests/test_window_picker/Main.qml `：` 100644 blob f88dcf589bf57aa9195858818974d1e33ba412e1 ` → ` None `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/tests/test_window_picker/ddeshell.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` tests/test_window_picker/ddeshell.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 01c384deab43e8682c314477f7af9a1eb66a4993 ` → ` None `。
- 来源文件项 ` tests/test_window_picker/ddeshell.cpp `：` 100644 blob 01c384deab43e8682c314477f7af9a1eb66a4993 ` → ` None `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/tests/test_window_picker/ddeshell.h ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` tests/test_window_picker/ddeshell.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 9ee7b2be5aab5252add9459e9ae004f6f069991c ` → ` None `。
- 来源文件项 ` tests/test_window_picker/ddeshell.h `：` 100644 blob 9ee7b2be5aab5252add9459e9ae004f6f069991c ` → ` None `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/tests/test_window_picker/main.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-review.json`。
- 来源路径：` tests/test_window_picker/main.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 53cd448e72b0ca07909d83326758416fafa64e31 ` → ` bf7ef355ad069a8fd27ff6ed7799649620851dcf `。
- 原目标增量端点：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 本次目标：` 5a5042c23ce2c6e63840454db144c026ed651f1d ` → ` ff11d25900dab07a5bb6aceb1e864cbec4b14a4a `。
- 目标文件项（mode/type/blob）：` 100644 blob 6874f451d1ecfdc8a22a7b6ed7b76409e9b01606 ` → ` None `。
- 来源文件项 ` tests/test_window_picker/main.cpp `：` 100644 blob 6874f451d1ecfdc8a22a7b6ed7b76409e9b01606 ` → ` None `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

- 依赖 ` 3rdparty/waylib-shared `：unchanged；` f1fe3771a9a8fa3037da1d6ab153cc538610b721 ` → ` f1fe3771a9a8fa3037da1d6ab153cc538610b721 `。

## 原工件定位

- mapped_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-mapped-source.patch`。
- root_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-root-source.patch`。
- adaptation_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent.patch`。
- target_diff：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/bf7ef355ad069a8fd27ff6ed7799649620851dcf/parent-target.diff`。
