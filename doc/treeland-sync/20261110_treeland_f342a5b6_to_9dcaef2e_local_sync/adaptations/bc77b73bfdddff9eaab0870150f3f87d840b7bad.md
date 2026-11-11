# P / DeckShell 适配：feat(xsettings): publish GTK IM module via Gtk/IMModule

- Treeland 来源：` 25906a2dc40cb6c2c053b735bf1dc260cf1feb9d `。
- 本仓目标：` bc77b73bfdddff9eaab0870150f3f87d840b7bad `。
- 节点：N10；action=adapted。
- [本仓总记录](../summary.md#entry-94)。

## 比较口径

比较来源唯一父提交 → 来源提交，与原目标唯一父提交 → 原目标提交的逐路径增量。
零上下文补丁对照会呈现基线位置、既有命名和本次实现差异；它不是整棵来源树与目标树的长期差异，也不声称所有显示行都是本次新增适配。
本批没有历史改写；依赖 gitlink 在总记录单列，不混进源码适配。原验收只适用于总记录列出的原节点候选。

## 已审说明

以下保留原证据文字；其中依赖 SHA 属于原运行，新依赖身份见下文与总记录。

- ` Preserve DeckShell layout, DDM guards, external-lock and late-DDE lifetime protections, installed WaylibShared package names and QML URI; integrate source deltas and only the explicitly approved XML/contract inputs. `

保留/映射路径：` compositor/misc/dconfig/org.deepin.dde.treeland.user.json `、` compositor/misc/systemd/dde-session-pre.target.wants/treeland-sd.service.in `、` compositor/src/core/waylandserver.cpp `、` compositor/src/session/session.cpp `、` compositor/src/session/session.h `、` compositor/src/xsettings/settingmanager.cpp `、` compositor/src/xsettings/settingmanager.h `。
排除路径：无。

## 逐路径取舍与实际差异

### ` compositor/misc/dconfig/org.deepin.dde.treeland.user.json ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/25906a2dc40cb6c2c053b735bf1dc260cf1feb9d/parent-review.json`。
- 来源路径：` misc/dconfig/org.deepin.dde.treeland.user.json `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 73057c6b9c1a2fa4f3d5c4be0237ea4f070d2395 ` → ` 25906a2dc40cb6c2c053b735bf1dc260cf1feb9d `。
- 原目标增量端点：` 2a8d80d5ce4cebc7f400c54387a0ee5d1e7fba06 ` → ` bc77b73bfdddff9eaab0870150f3f87d840b7bad `。
- 本次目标：` 2a8d80d5ce4cebc7f400c54387a0ee5d1e7fba06 ` → ` bc77b73bfdddff9eaab0870150f3f87d840b7bad `。
- 目标文件项（mode/type/blob）：` 100644 blob 59546f3ab3198f05e6a2d55c42c867c61170e85d ` → ` 100644 blob c87cff85e922b8d85078efea37afcb4f4e00e16b `。
- 来源文件项 ` misc/dconfig/org.deepin.dde.treeland.user.json `：` 100644 blob 59546f3ab3198f05e6a2d55c42c867c61170e85d ` → ` 100644 blob c87cff85e922b8d85078efea37afcb4f4e00e16b `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/misc/systemd/dde-session-pre.target.wants/treeland-sd.service.in ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/25906a2dc40cb6c2c053b735bf1dc260cf1feb9d/parent-review.json`。
- 来源路径：` misc/systemd/dde-session-pre.target.wants/treeland-sd.service.in `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 73057c6b9c1a2fa4f3d5c4be0237ea4f070d2395 ` → ` 25906a2dc40cb6c2c053b735bf1dc260cf1feb9d `。
- 原目标增量端点：` 2a8d80d5ce4cebc7f400c54387a0ee5d1e7fba06 ` → ` bc77b73bfdddff9eaab0870150f3f87d840b7bad `。
- 本次目标：` 2a8d80d5ce4cebc7f400c54387a0ee5d1e7fba06 ` → ` bc77b73bfdddff9eaab0870150f3f87d840b7bad `。
- 目标文件项（mode/type/blob）：` 100644 blob 2ab7c6900a1f18119d0fce6e15ba4ed767035fd9 ` → ` 100644 blob b41c5eb1069ddd711e2acf29d9df47592ba93451 `。
- 来源文件项 ` misc/systemd/dde-session-pre.target.wants/treeland-sd.service.in `：` 100644 blob 2ab7c6900a1f18119d0fce6e15ba4ed767035fd9 ` → ` 100644 blob b41c5eb1069ddd711e2acf29d9df47592ba93451 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/src/core/waylandserver.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/25906a2dc40cb6c2c053b735bf1dc260cf1feb9d/parent-review.json`。
- 来源路径：` src/core/waylandserver.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 73057c6b9c1a2fa4f3d5c4be0237ea4f070d2395 ` → ` 25906a2dc40cb6c2c053b735bf1dc260cf1feb9d `。
- 原目标增量端点：` 2a8d80d5ce4cebc7f400c54387a0ee5d1e7fba06 ` → ` bc77b73bfdddff9eaab0870150f3f87d840b7bad `。
- 本次目标：` 2a8d80d5ce4cebc7f400c54387a0ee5d1e7fba06 ` → ` bc77b73bfdddff9eaab0870150f3f87d840b7bad `。
- 目标文件项（mode/type/blob）：` 100644 blob 1295ffd00f3a676f508916b76c7a8864f91feaff ` → ` 100644 blob 829423d05ebcaaf778bfc8f52111c98b4859b8ef `。
- 来源文件项 ` src/core/waylandserver.cpp `：` 100644 blob f3f52aae1902e6328964beab9a0d3da2b3827f14 ` → ` 100644 blob e7ec183ca93734c25cf44b4c844f66d2f4056b55 `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,17 +1,17 @@
-@@ -408 +408 @@ void WaylandServer::applyCurrentUserConfig(const QString &userName,
+@@ -411 +411 @@ void WaylandServer::applyCurrentUserConfig(const QString &userName,
 -                       &SessionManager::syncActiveSessionCursorSettings);
 +                       &SessionManager::syncActiveSessionXSettings);
-@@ -412 +412,5 @@ void WaylandServer::applyCurrentUserConfig(const QString &userName,
+@@ -415 +415,5 @@ void WaylandServer::applyCurrentUserConfig(const QString &userName,
 -                       &SessionManager::syncActiveSessionCursorSettings);
 +                       &SessionManager::syncActiveSessionXSettings);
 +            disconnect(m_config,
 +                       &TreelandUserConfig::x11GtkIMModuleChanged,
 +                       m_sessionManager,
 +                       &SessionManager::syncActiveSessionXSettings);
-@@ -421 +425 @@ void WaylandServer::applyCurrentUserConfig(const QString &userName,
+@@ -424 +428 @@ void WaylandServer::applyCurrentUserConfig(const QString &userName,
 -            &SessionManager::syncActiveSessionCursorSettings,
 +            &SessionManager::syncActiveSessionXSettings,
-@@ -426 +430,6 @@ void WaylandServer::applyCurrentUserConfig(const QString &userName,
+@@ -429 +433,6 @@ void WaylandServer::applyCurrentUserConfig(const QString &userName,
 -            &SessionManager::syncActiveSessionCursorSettings,
 +            &SessionManager::syncActiveSessionXSettings,
 +            Qt::UniqueConnection);
@@ -19,6 +19,6 @@
 +            &TreelandUserConfig::x11GtkIMModuleChanged,
 +            m_sessionManager,
 +            &SessionManager::syncActiveSessionXSettings,
-@@ -441 +450 @@ void WaylandServer::applyCurrentUserConfig(const QString &userName,
+@@ -444 +453 @@ void WaylandServer::applyCurrentUserConfig(const QString &userName,
 -    m_sessionManager->syncActiveSessionCursorSettings();
 +    m_sessionManager->syncActiveSessionXSettings();
```


### ` compositor/src/session/session.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/25906a2dc40cb6c2c053b735bf1dc260cf1feb9d/parent-review.json`。
- 来源路径：` src/session/session.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 73057c6b9c1a2fa4f3d5c4be0237ea4f070d2395 ` → ` 25906a2dc40cb6c2c053b735bf1dc260cf1feb9d `。
- 原目标增量端点：` 2a8d80d5ce4cebc7f400c54387a0ee5d1e7fba06 ` → ` bc77b73bfdddff9eaab0870150f3f87d840b7bad `。
- 本次目标：` 2a8d80d5ce4cebc7f400c54387a0ee5d1e7fba06 ` → ` bc77b73bfdddff9eaab0870150f3f87d840b7bad `。
- 目标文件项（mode/type/blob）：` 100644 blob 9f42f1059ee79521646784d993df3a64f196bdfa ` → ` 100644 blob 02bd5db113f2427f47cacbef1cd595dc31074623 `。
- 来源文件项 ` src/session/session.cpp `：` 100644 blob 9f42f1059ee79521646784d993df3a64f196bdfa ` → ` 100644 blob 02bd5db113f2427f47cacbef1cd595dc31074623 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/src/session/session.h ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/25906a2dc40cb6c2c053b735bf1dc260cf1feb9d/parent-review.json`。
- 来源路径：` src/session/session.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 73057c6b9c1a2fa4f3d5c4be0237ea4f070d2395 ` → ` 25906a2dc40cb6c2c053b735bf1dc260cf1feb9d `。
- 原目标增量端点：` 2a8d80d5ce4cebc7f400c54387a0ee5d1e7fba06 ` → ` bc77b73bfdddff9eaab0870150f3f87d840b7bad `。
- 本次目标：` 2a8d80d5ce4cebc7f400c54387a0ee5d1e7fba06 ` → ` bc77b73bfdddff9eaab0870150f3f87d840b7bad `。
- 目标文件项（mode/type/blob）：` 100644 blob 4a8c02edc52906c4c4f5c2fff516a5bd099a5899 ` → ` 100644 blob 8185fa3b19ade2dfb8e66ee585ba8ca5dc01f500 `。
- 来源文件项 ` src/session/session.h `：` 100644 blob 4a8c02edc52906c4c4f5c2fff516a5bd099a5899 ` → ` 100644 blob 8185fa3b19ade2dfb8e66ee585ba8ca5dc01f500 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/src/xsettings/settingmanager.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/25906a2dc40cb6c2c053b735bf1dc260cf1feb9d/parent-review.json`。
- 来源路径：` src/xsettings/settingmanager.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 73057c6b9c1a2fa4f3d5c4be0237ea4f070d2395 ` → ` 25906a2dc40cb6c2c053b735bf1dc260cf1feb9d `。
- 原目标增量端点：` 2a8d80d5ce4cebc7f400c54387a0ee5d1e7fba06 ` → ` bc77b73bfdddff9eaab0870150f3f87d840b7bad `。
- 本次目标：` 2a8d80d5ce4cebc7f400c54387a0ee5d1e7fba06 ` → ` bc77b73bfdddff9eaab0870150f3f87d840b7bad `。
- 目标文件项（mode/type/blob）：` 100644 blob bd01ef4e8a7aa29931f4121f2af8cdb8f99309cb ` → ` 100644 blob 8df01718dd5a340fa5207d44cbdb441b079447ba `。
- 来源文件项 ` src/xsettings/settingmanager.cpp `：` 100644 blob bd01ef4e8a7aa29931f4121f2af8cdb8f99309cb ` → ` 100644 blob 8df01718dd5a340fa5207d44cbdb441b079447ba `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/src/xsettings/settingmanager.h ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/25906a2dc40cb6c2c053b735bf1dc260cf1feb9d/parent-review.json`。
- 来源路径：` src/xsettings/settingmanager.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 73057c6b9c1a2fa4f3d5c4be0237ea4f070d2395 ` → ` 25906a2dc40cb6c2c053b735bf1dc260cf1feb9d `。
- 原目标增量端点：` 2a8d80d5ce4cebc7f400c54387a0ee5d1e7fba06 ` → ` bc77b73bfdddff9eaab0870150f3f87d840b7bad `。
- 本次目标：` 2a8d80d5ce4cebc7f400c54387a0ee5d1e7fba06 ` → ` bc77b73bfdddff9eaab0870150f3f87d840b7bad `。
- 目标文件项（mode/type/blob）：` 100644 blob 6e74248b47a1f5eb0ba62642f38b4ca97647b1f0 ` → ` 100644 blob a2d428acb2ce74ef78008f2f128c2c6a5cb12757 `。
- 来源文件项 ` src/xsettings/settingmanager.h `：` 100644 blob 6e74248b47a1f5eb0ba62642f38b4ca97647b1f0 ` → ` 100644 blob a2d428acb2ce74ef78008f2f128c2c6a5cb12757 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

- 依赖 ` 3rdparty/waylib-shared `：unchanged；` a1e20b7fe6f02a54e2d689d789c84468cb1c67be ` → ` a1e20b7fe6f02a54e2d689d789c84468cb1c67be `。

## 原工件定位

- mapped_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/25906a2dc40cb6c2c053b735bf1dc260cf1feb9d/parent-mapped-source.patch`。
- root_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/25906a2dc40cb6c2c053b735bf1dc260cf1feb9d/parent-root-source.patch`。
- adaptation_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/25906a2dc40cb6c2c053b735bf1dc260cf1feb9d/parent.patch`。
- target_diff：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/25906a2dc40cb6c2c053b735bf1dc260cf1feb9d/parent-target.diff`。
