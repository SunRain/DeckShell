# P / DeckShell 适配：fix(wallpaper): use build factory in Debug

- Treeland 来源：` 252d0df3366671533b1914b55053a5ac4cbe6a3a `。
- 本仓目标：` bde8fd486752be3c8dc0d6d7ffd5a0f8e3aceaf8 `。
- 原同步目标：` 0b78f4b4bc17080372dd230c180abd9b5643ddec `；本页文件名采用整理后的完整目标 SHA。
- 节点：N5；action=adapted。
- [本仓总记录](../summary.md#entry-91)。

## 比较口径

比较来源唯一父提交 → 来源提交，与原目标唯一父提交 → 原目标提交的逐路径增量。
零上下文补丁对照会呈现基线位置、既有命名和本次实现差异；它不是整棵来源树与目标树的长期差异，也不声称所有显示行都是本次新增适配。
改写后的普通文件与原目标相同；派生 gitlink 在总记录单列，不混进源码适配。原验收只适用于总记录列出的原节点候选。

## 已审说明

以下保留原证据文字；其中依赖 SHA 属于原运行，新依赖身份见下文与总记录。

- ` 保留来源 Debug 构建树壁纸工厂选择与 Release 已安装程序选择；构建输出按嵌套 compositor 的 PROJECT_BINARY_DIR 映射，保持现有 treeland-wallpaper-factory 可执行名称。 `

保留/映射路径：` compositor/CMakeLists.txt `、` compositor/src/wallpaper/wallpaperlauncher.cpp `、` compositor/src/wallpaper/wallpaperlauncher.h `。
排除路径：无。

## 逐路径取舍与实际差异

### ` compositor/CMakeLists.txt ` / modified

- 原审核理由：` 保留来源 Debug 构建树壁纸工厂选择与 Release 已安装程序选择；构建输出按嵌套 compositor 的 PROJECT_BINARY_DIR 映射，保持现有 treeland-wallpaper-factory 可执行名称。 `。
- 路径证明：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/adaptations/252d0df3366671533b1914b55053a5ac4cbe6a3a/parent-0-proof.json`。
- 来源路径：` CMakeLists.txt `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 6ea349ac28b93b61ca3f9223ec021344141d6fce ` → ` 252d0df3366671533b1914b55053a5ac4cbe6a3a `。
- 原目标增量端点：` 7d2daba2014eabef671253fb361c372cedcfb4f0 ` → ` 0b78f4b4bc17080372dd230c180abd9b5643ddec `。
- 本次目标：` 5b04ac8e277ac6d7887bf2ffb0be358f554d4bcc ` → ` bde8fd486752be3c8dc0d6d7ffd5a0f8e3aceaf8 `。
- 目标文件项（mode/type/blob）：` 100644 blob 3a3b8a4a9e9db4d3e14f1f84e3b21baf6ff5a5fc ` → ` 100644 blob 8f759f605b1423eecba3d871ef279481b3b8bb0a `。
- 来源文件项 ` CMakeLists.txt `：` 100644 blob 7baa2e7522159cfdd7b4be945bfcb042d6f1d98b ` → ` 100644 blob fe3a1d1a1468ac60204dfcc09ad6395252240a8e `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,2 +1,3 @@
-@@ -110,0 +111 @@ add_compile_definitions("TREELAND_PLUGINS_OUTPUT_PATH=\"${TREELAND_PLUGINS_OUTPU
-+add_compile_definitions("TREELAND_WALLPAPER_FACTORY_OUTPUT_PATH=\"${CMAKE_BINARY_DIR}/wallpaper-factory/treeland-wallpaper-factory\"")
+@@ -163,0 +164,2 @@ add_compile_definitions(
++add_compile_definitions(
++    "TREELAND_WALLPAPER_FACTORY_OUTPUT_PATH=\"${PROJECT_BINARY_DIR}/wallpaper-factory/treeland-wallpaper-factory\"")
```


### ` compositor/src/wallpaper/wallpaperlauncher.cpp ` / modified

- 原审核理由：` 保留来源 Debug 构建树壁纸工厂选择与 Release 已安装程序选择；构建输出按嵌套 compositor 的 PROJECT_BINARY_DIR 映射，保持现有 treeland-wallpaper-factory 可执行名称。 `。
- 路径证明：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/adaptations/252d0df3366671533b1914b55053a5ac4cbe6a3a/parent-1-proof.json`。
- 来源路径：` src/wallpaper/wallpaperlauncher.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 6ea349ac28b93b61ca3f9223ec021344141d6fce ` → ` 252d0df3366671533b1914b55053a5ac4cbe6a3a `。
- 原目标增量端点：` 7d2daba2014eabef671253fb361c372cedcfb4f0 ` → ` 0b78f4b4bc17080372dd230c180abd9b5643ddec `。
- 本次目标：` 5b04ac8e277ac6d7887bf2ffb0be358f554d4bcc ` → ` bde8fd486752be3c8dc0d6d7ffd5a0f8e3aceaf8 `。
- 目标文件项（mode/type/blob）：` 100644 blob 54dfa6c13765a6857b0311cbe36622e48873285b ` → ` 100644 blob ff4a8866612a4694626585371534a9460e68f1bc `。
- 来源文件项 ` src/wallpaper/wallpaperlauncher.cpp `：` 100644 blob 54dfa6c13765a6857b0311cbe36622e48873285b ` → ` 100644 blob ff4a8866612a4694626585371534a9460e68f1bc `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/src/wallpaper/wallpaperlauncher.h ` / modified

- 原审核理由：` 保留来源 Debug 构建树壁纸工厂选择与 Release 已安装程序选择；构建输出按嵌套 compositor 的 PROJECT_BINARY_DIR 映射，保持现有 treeland-wallpaper-factory 可执行名称。 `。
- 路径证明：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/adaptations/252d0df3366671533b1914b55053a5ac4cbe6a3a/parent-2-proof.json`。
- 来源路径：` src/wallpaper/wallpaperlauncher.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 6ea349ac28b93b61ca3f9223ec021344141d6fce ` → ` 252d0df3366671533b1914b55053a5ac4cbe6a3a `。
- 原目标增量端点：` 7d2daba2014eabef671253fb361c372cedcfb4f0 ` → ` 0b78f4b4bc17080372dd230c180abd9b5643ddec `。
- 本次目标：` 5b04ac8e277ac6d7887bf2ffb0be358f554d4bcc ` → ` bde8fd486752be3c8dc0d6d7ffd5a0f8e3aceaf8 `。
- 目标文件项（mode/type/blob）：` 100644 blob 08dd1c9d644e437a2aceb508f1072d3648b3b858 ` → ` 100644 blob 062c9042574fcbc58991d82ea9bd98b3d05b876b `。
- 来源文件项 ` src/wallpaper/wallpaperlauncher.h `：` 100644 blob 08dd1c9d644e437a2aceb508f1072d3648b3b858 ` → ` 100644 blob 062c9042574fcbc58991d82ea9bd98b3d05b876b `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 5d193f6dccab6ad38890d453710c38dc69f53c0b ` → ` 5d193f6dccab6ad38890d453710c38dc69f53c0b `。
  原证据引用：` ed4f019301c0d3dd8434d842152f343a69e988d5 ` → ` ed4f019301c0d3dd8434d842152f343a69e988d5 `。

## 原工件定位

- mapped_source_patch：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/commits/252d0df3366671533b1914b55053a5ac4cbe6a3a/parent-mapped-source.patch`。
- root_source_patch：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/commits/252d0df3366671533b1914b55053a5ac4cbe6a3a/parent-root-source.patch`。
- adaptation_patch：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/adaptations/252d0df3366671533b1914b55053a5ac4cbe6a3a/parent.diff`。
- target_diff：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/commits/252d0df3366671533b1914b55053a5ac4cbe6a3a/parent-target.diff`。
