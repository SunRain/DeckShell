# P / DeckShell 适配：fix(lockscreen): give lock surface the keyboard focus

- Treeland 来源：` e40794df6f15e5bdd12cb2afad5ac54fc3a05d68 `。
- 本仓目标：` 37bbe086d0dcbefd43ea5d6b4b1055ece58eafc3 `。
- 节点：N10；action=adapted。
- [本仓总记录](../summary.md#entry-120)。

## 比较口径

比较来源唯一父提交 → 来源提交，与原目标唯一父提交 → 原目标提交的逐路径增量。
零上下文补丁对照会呈现基线位置、既有命名和本次实现差异；它不是整棵来源树与目标树的长期差异，也不声称所有显示行都是本次新增适配。
本批没有历史改写；依赖 gitlink 在总记录单列，不混进源码适配。原验收只适用于总记录列出的原节点候选。

## 已审说明

以下保留原证据文字；其中依赖 SHA 属于原运行，新依赖身份见下文与总记录。

- ` Preserve DeckShell layout, DDM guards, external-lock and late-DDE lifetime protections, installed WaylibShared package names and QML URI; integrate source deltas and only the explicitly approved XML/contract inputs. `

保留/映射路径：` compositor/src/lockscreen/lockscreen.cpp `、` compositor/src/lockscreen/lockscreen.h `。
排除路径：无。

## 逐路径取舍与实际差异

### ` compositor/src/lockscreen/lockscreen.cpp ` / modified

- 原审核理由：` Reviewed three-way resolution preserving local package, runtime and regression integration. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/e40794df6f15e5bdd12cb2afad5ac54fc3a05d68/parent-review.json`。
- 来源路径：` src/lockscreen/lockscreen.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` d8a1757a94ab5fdf16c93c79f62ff212816fcbf6 ` → ` e40794df6f15e5bdd12cb2afad5ac54fc3a05d68 `。
- 原目标增量端点：` a91f88476cf473a4febd1a64c55485eec4517369 ` → ` 37bbe086d0dcbefd43ea5d6b4b1055ece58eafc3 `。
- 本次目标：` a91f88476cf473a4febd1a64c55485eec4517369 ` → ` 37bbe086d0dcbefd43ea5d6b4b1055ece58eafc3 `。
- 目标文件项（mode/type/blob）：` 100644 blob ec83c399b7e17805f7ab21b44e75d367ed8af5c3 ` → ` 100644 blob 7b1142202f4cefe2fcfb5d86ace7bcb6812f9639 `。
- 来源文件项 ` src/lockscreen/lockscreen.cpp `：` 100644 blob dd9b948eec197992ab157c4a1e98025d6f78c411 ` → ` 100644 blob 225b15d0b9c37eda09ccf0ec63da717dc3f6c141 `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,6 +1,6 @@
-@@ -17,0 +18 @@
+@@ -19,0 +20 @@
 +#include "workspace/workspace.h"
-@@ -309,2 +310,6 @@ void LockScreen::onLockSurfaceAdded(WSessionLockSurface *surface)
+@@ -344,2 +345,6 @@ void LockScreen::onLockSurfaceAdded(WSessionLockSurface *surface)
 -    connect(wrapper, &SurfaceWrapper::activationRequested, this, [wrapper] {
 -        WaylandServer::instance()->activateSurface(wrapper);
 +    // Lock surfaces have no Activate capability, so ask for focus directly
@@ -9,14 +9,13 @@
 +    connect(wrapper, &SurfaceWrapper::hasFocusCapabilityChanged, this, [wrapper] {
 +        if (wrapper->hasFocusCapability())
 +            WaylandServer::instance()->requestKeyboardFocus(wrapper);
-@@ -371,0 +377,6 @@ void LockScreen::onExternalLock(WSessionLock *lock)
-+
+@@ -413,0 +419,5 @@ void LockScreen::onExternalLock(WSessionLock *lock)
 +    // Snapshot the focused surface and clear focus until the lock surface maps.
 +    // primary seat only, upgrade when lock surfaces become per-seat.
 +    auto *server = WaylandServer::instance();
 +    m_lockFocusRestoreSurface = server->activatedSurface();
 +    server->requestKeyboardFocus(nullptr);
-@@ -385,0 +397,17 @@ void LockScreen::onExternalUnlock() {
+@@ -428,0 +439,17 @@ void LockScreen::onExternalUnlock() {
 +    // After finishLockScreenTransition() so the snapshot wins over its generic restore.
 +    restoreLockedSessionFocus();
 +}
```


### ` compositor/src/lockscreen/lockscreen.h ` / modified

- 原审核理由：` Reviewed three-way resolution preserving local package, runtime and regression integration. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/e40794df6f15e5bdd12cb2afad5ac54fc3a05d68/parent-review.json`。
- 来源路径：` src/lockscreen/lockscreen.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` d8a1757a94ab5fdf16c93c79f62ff212816fcbf6 ` → ` e40794df6f15e5bdd12cb2afad5ac54fc3a05d68 `。
- 原目标增量端点：` a91f88476cf473a4febd1a64c55485eec4517369 ` → ` 37bbe086d0dcbefd43ea5d6b4b1055ece58eafc3 `。
- 本次目标：` a91f88476cf473a4febd1a64c55485eec4517369 ` → ` 37bbe086d0dcbefd43ea5d6b4b1055ece58eafc3 `。
- 目标文件项（mode/type/blob）：` 100644 blob 02e0fa174c3932af530fbbae5cab3c2ec44b42f4 ` → ` 100644 blob 352333f60df7871ac50c7679cd377f676b79d5bd `。
- 来源文件项 ` src/lockscreen/lockscreen.h `：` 100644 blob 943698c91192547ced16c7280401b510201b42be ` → ` 100644 blob b9fb9432a8b8e6dd5b1e224a6da0ccfb21d78e26 `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,7 +1,7 @@
 @@ -7,0 +8 @@
 +#include <QPointer>
-@@ -66,0 +68 @@ private:
+@@ -69,0 +71 @@ private:
 +    void restoreLockedSessionFocus();
-@@ -93,0 +96,2 @@ private:
+@@ -97,0 +100,2 @@ private:
 +    // The surface focused when the session was locked, restored on unlock.
 +    QPointer<SurfaceWrapper> m_lockFocusRestoreSurface;
```


- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 357fcfa31dc2a67ad874daecc2bd392263d32370 ` → ` 357fcfa31dc2a67ad874daecc2bd392263d32370 `。

## 原工件定位

- mapped_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/e40794df6f15e5bdd12cb2afad5ac54fc3a05d68/parent-mapped-source.patch`。
- root_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/e40794df6f15e5bdd12cb2afad5ac54fc3a05d68/parent-root-source.patch`。
- adaptation_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/e40794df6f15e5bdd12cb2afad5ac54fc3a05d68/parent.patch`。
- target_diff：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/e40794df6f15e5bdd12cb2afad5ac54fc3a05d68/parent-target.diff`。
