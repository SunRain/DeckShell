# P / DeckShell 适配：fix: connect dock rectangle handler before splash handover

- Treeland 来源：` 4f1bd38f0fbd17d96c893250bec8e2a00b676d35 `。
- 本仓目标：` 1cb34fec99ea8b68df2abed8a626df491afa61d2 `。
- 节点：N8b；action=adapted。
- [本仓总记录](../summary.md#entry-40)。

## 比较口径

比较来源唯一父提交 → 来源提交，与原目标唯一父提交 → 原目标提交的逐路径增量。
零上下文补丁对照会呈现基线位置、既有命名和本次实现差异；它不是整棵来源树与目标树的长期差异，也不声称所有显示行都是本次新增适配。
本批没有历史改写；依赖 gitlink 在总记录单列，不混进源码适配。原验收只适用于总记录列出的原节点候选。

## 已审说明

以下保留原证据文字；其中依赖 SHA 属于原运行，新依赖身份见下文与总记录。

- ` 按来源差异进行三方合并，保留相邻本地树的构建名、受控协议目录及已有条件；新增/移动文件使用规范映射路径。协议额外路径仅按 PRD §5.3.1 精确迁移。 `

保留/映射路径：` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv1.cpp `。
排除路径：无。

## 逐路径取舍与实际差异

### ` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv1.cpp ` / modified

- 原审核理由：` 按来源差异进行三方合并，保留相邻本地树的构建名、受控协议目录及已有条件；新增/移动文件使用规范映射路径。协议额外路径仅按 PRD §5.3.1 精确迁移。 `。
- 路径证明：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/decisions/4f1bd38f0fbd17d96c893250bec8e2a00b676d35-parent.patch`。
- 来源路径：` src/modules/foreign-toplevel/foreigntoplevelmanagerv1.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` cb038ef766940545fd05d0a22578c7e9fbaa7324 ` → ` 4f1bd38f0fbd17d96c893250bec8e2a00b676d35 `。
- 原目标增量端点：` d806f87a8f58ff03d447deace2d78c206f6a2d3f ` → ` 1cb34fec99ea8b68df2abed8a626df491afa61d2 `。
- 本次目标：` d806f87a8f58ff03d447deace2d78c206f6a2d3f ` → ` 1cb34fec99ea8b68df2abed8a626df491afa61d2 `。
- 目标文件项（mode/type/blob）：` 100644 blob 75d91c73064cd5ef6892f66c6849884e3fa4a2a6 ` → ` 100644 blob 381079ef9912467e29ac88a738b40073977e36cc `。
- 来源文件项 ` src/modules/foreign-toplevel/foreigntoplevelmanagerv1.cpp `：` 100644 blob e036ee273f208efa1f53a500e6fab262cb0d3228 ` → ` 100644 blob fd668613141f64d28a51a2075c73a28bfc733124 `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,4 +1,4 @@
-@@ -237,0 +238,27 @@ void ForeignToplevelManagerInterfaceV1Private::setupHandleForWrapper(SurfaceEntr
+@@ -244,0 +245,27 @@ void ForeignToplevelManagerInterfaceV1Private::setupHandleForWrapper(SurfaceEntr
 +    // The rectangle handler only depends on the wrapper, so connect it here for
 +    // both splash and normal handles: a splash is exposed to clients immediately
 +    // and a set_rectangle sent during the splash phase must not be dropped.
@@ -26,7 +26,7 @@
 +                         wrapper->setIconGeometry(iconGeometry);
 +                     });
 +
-@@ -494,13 +520,0 @@ void ForeignToplevelManagerInterfaceV1::initializeToplevelHandle(SurfaceWrapper
+@@ -502,13 +528,0 @@ void ForeignToplevelManagerInterfaceV1::initializeToplevelHandle(SurfaceWrapper
 -    connect(handle,
 -            &ForeignToplevelHandleV1::rectangleChanged,
 -            wrapper,
```


- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 1f37c019972da79aa624947a1cdcc3c97f625559 ` → ` 1f37c019972da79aa624947a1cdcc3c97f625559 `。

## 原工件定位

- mapped_source_patch：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/commits/4f1bd38f0fbd17d96c893250bec8e2a00b676d35/parent-mapped-source.patch`。
- root_source_patch：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/commits/4f1bd38f0fbd17d96c893250bec8e2a00b676d35/parent-root-source.patch`。
- adaptation_patch：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/decisions/4f1bd38f0fbd17d96c893250bec8e2a00b676d35-parent.patch`。
- target_diff：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/commits/4f1bd38f0fbd17d96c893250bec8e2a00b676d35/parent-target.diff`。
