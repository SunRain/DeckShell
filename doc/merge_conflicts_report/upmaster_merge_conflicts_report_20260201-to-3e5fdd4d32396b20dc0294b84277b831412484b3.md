# up-master (f6af3a5..3e5fdd4] → master-merge 冲突/差异点报告（v2）

生成方法：对比「上游提交 diff（按路径映射 src→compositor/src，且 mixed commit 剥离 waylib/qwlroots 后）」与「master-merge 对应提交 diff」。


## feat: Add per-user XWayland session management

- upstream: `6547558cc729b2f85d65b007d2926f66bd50ed2f`
- master-merge: `c4d3f0db12bf3b4eda22134048fd62e20f510df4`
- mixed commit (需剥离 waylib/qwlroots): `True`
- files changed: `3`; files differ vs upstream(mapped): `3`

### compositor/src/core/treeland.cpp

```diff
@@ -1,8 +1,8 @@
@@ -12,10 +12,10 @@
-@@ -278,7 +278,11 @@ Treeland::Treeland()
+@@ -293,7 +293,11 @@ Treeland::Treeland()
-                 envs.insert("XDG_SESSION_DESKTOP", "Treeland");
+                 envs.insert("XDG_SESSION_DESKTOP", "DeckShell");
-@@ -407,17 +411,23 @@ QString Treeland::XWaylandName()
+@@ -426,17 +430,23 @@ QString Treeland::XWaylandName()
-index 4e1278a2..09ca0fe5 100644
+index f80cb660..33e9b00b 100644
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -10,7 +10,7 @@
@@ -44,7 +44,7 @@
@@ -66,18 +66,27 @@
@@ -97,10 +106,10 @@
@@ -141,7 +150,7 @@
-index 3ffb05ba..df687358 100644
+index e0b18851..1db2b779 100644
-@@ -110,6 +110,7 @@
+@@ -111,6 +111,7 @@
-@@ -778,21 +779,24 @@ void Helper::onSurfaceWrapperAdded(SurfaceWrapper *wrapper)
+@@ -780,21 +781,24 @@ void Helper::onSurfaceWrapperAdded(SurfaceWrapper *wrapper)
-@@ -801,13 +805,15 @@ void Helper::onSurfaceWrapperAdded(SurfaceWrapper *wrapper)
+@@ -803,13 +807,15 @@ void Helper::onSurfaceWrapperAdded(SurfaceWrapper *wrapper)
-@@ -853,15 +859,26 @@ void Helper::onSurfaceWrapperAboutToRemove(SurfaceWrapper *wrapper)
+@@ -855,16 +861,35 @@ void Helper::onSurfaceWrapperAboutToRemove(SurfaceWrapper *wrapper)
--    auto credentials = WClient::getCredentials(wrapper->surface()->waylandClient()->handle());
-     auto user = m_userModel->currentUser();
+-#ifndef DISABLE_DDM
+     auto credentials = WClient::getCredentials(wrapper->surface()->waylandClient()->handle());
+-    auto user = m_userModel->currentUser();
--        return credentials->uid == user->UID() || credentials->uid == puid;
++    if (!credentials)
++        return false;
++
++    if (user)
+         return credentials->uid == user->UID() || credentials->uid == puid;
++    return credentials->uid == puid;
++#ifndef DISABLE_DDM
++    auto user = m_userModel->currentUser();
...
```

### compositor/src/seat/helper.h

```diff
@@ -1,8 +1,8 @@
@@ -10,7 +10,7 @@
@@ -25,9 +25,9 @@
-index 1b8156b5..eea22fdc 100644
+index 071c3f95..d4f004f3 100644
-@@ -179,6 +179,7 @@ public:
+@@ -187,6 +187,7 @@ public:
-@@ -314,6 +315,14 @@ private:
+@@ -331,6 +332,14 @@ private:
-@@ -387,9 +396,12 @@ private:
-     IMultitaskView *m_multitaskView{ nullptr };
+@@ -412,9 +421,12 @@ private:
+ #endif
```


## feat: Manage per-user Wayland/XWayland sessions via Helper::Session

- upstream: `b2661a3d863ce856f376114163945e9ad46098e6`
- master-merge: `12a9a039940fd7e36e0de4474366103b95e667ad`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `6`; files differ vs upstream(mapped): `3`

### compositor/src/plugins/multitaskview/multitaskview.cpp

```diff
@@ -1,5 +1,5 @@
@@ -11,7 +11,7 @@
-index 650e7b00..ce65adb9 100644
+index 7256d2be..39e30854 100644
-@@ -495,7 +495,7 @@ void MultitaskviewSurfaceModel::handleSurfaceMappedChanged()
+@@ -517,7 +517,7 @@ void MultitaskviewSurfaceModel::handleSurfaceSkipMutiTaskViewChanged()
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -23,7 +23,7 @@
@@ -40,7 +40,7 @@
@@ -48,6 +48,15 @@
@@ -68,13 +77,17 @@
@@ -130,7 +143,7 @@
-index df687358..f104d6e8 100644
+index 1db2b779..10a84f32 100644
-@@ -276,6 +276,20 @@ Helper::Helper(QObject *parent)
+@@ -278,6 +278,20 @@ Helper::Helper(QObject *parent)
-@@ -783,7 +797,15 @@ void Helper::onSurfaceWrapperAdded(SurfaceWrapper *wrapper)
+@@ -785,7 +799,15 @@ void Helper::onSurfaceWrapperAdded(SurfaceWrapper *wrapper)
-@@ -856,29 +878,11 @@ void Helper::onSurfaceWrapperAboutToRemove(SurfaceWrapper *wrapper)
+@@ -858,42 +880,11 @@ void Helper::onSurfaceWrapperAboutToRemove(SurfaceWrapper *wrapper)
+-    auto credentials = WClient::getCredentials(wrapper->surface()->waylandClient()->handle());
+-    if (!credentials)
+-        return false;
+-
+-    if (user)
+-        return credentials->uid == user->UID() || credentials->uid == puid;
+-    return credentials->uid == puid;
+-#ifndef DISABLE_DDM
+-#else
+-    // When DISABLE_DDM is defined, only check against current process uid
+-    return puid == getuid();
+-#endif
-@@ -1103,50 +1107,24 @@ void Helper::init()
+@@ -1127,50 +1118,24 @@ void Helper::init()
-@@ -1202,19 +1180,19 @@ void Helper::init()
+@@ -1226,19 +1191,19 @@ void Helper::init()
...
```

### compositor/src/seat/helper.h

```diff
@@ -1,8 +1,8 @@
@@ -11,7 +11,7 @@
@@ -26,7 +26,7 @@
@@ -34,7 +34,7 @@
@@ -43,7 +43,7 @@
@@ -63,7 +63,7 @@
-index eea22fdc..750d5723 100644
+index d4f004f3..00d26898 100644
-@@ -16,6 +16,8 @@
+@@ -22,6 +22,8 @@
-@@ -105,6 +107,14 @@ QW_BEGIN_NAMESPACE
+@@ -113,6 +115,14 @@ QW_BEGIN_NAMESPACE
-@@ -180,6 +190,7 @@ public:
+@@ -188,6 +198,7 @@ public:
-@@ -230,7 +241,7 @@ public Q_SLOTS:
+@@ -245,7 +256,7 @@ public Q_SLOTS:
-@@ -315,13 +326,16 @@ private:
+@@ -332,13 +343,16 @@ private:
-@@ -329,6 +343,9 @@ private:
+@@ -346,6 +360,9 @@ private:
-@@ -341,7 +358,6 @@ private:
+@@ -358,7 +375,6 @@ private:
-@@ -399,9 +415,4 @@ private:
+@@ -424,9 +440,4 @@ private:
```


## refactor: implement atomic multi-output configuration

- upstream: `f50669edc6647bce9783613db217413c018c0a40`
- master-merge: `ca75e355efd81bb6a4d34d6a2c018c8387957a06`
- mixed commit (需剥离 waylib/qwlroots): `True`
- files changed: `3`; files differ vs upstream(mapped): `3`

### .gitignore

```diff
@@ -1,12 +1,12 @@
+ .qmlls.ini
+ *.qmlproject.user
-index 54bc87b0..97587130 100644
+index f1dca30e..2135829c 100644
-@@ -1,6 +1,7 @@
- .vscode/
- .cache/
- build*/
+@@ -45,6 +45,7 @@ Makefile*
+ # IDE 和编辑器文件 (IDE and Editor Files)
+ # =============================================================================
+ # Qt Creator
- 
- *.user
+ *.autosave
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -10,7 +10,7 @@
-index 082e67a6..1accb9f5 100644
+index cd84487c..55b2ecab 100644
-@@ -50,6 +50,7 @@
+@@ -51,6 +51,7 @@
-@@ -495,55 +496,206 @@ void Helper::setGamma(struct wlr_gamma_control_manager_v1_set_gamma_event *event
+@@ -497,55 +498,206 @@ void Helper::setGamma(struct wlr_gamma_control_manager_v1_set_gamma_event *event
```

### compositor/src/seat/helper.h

```diff
@@ -1,8 +1,8 @@
@@ -10,7 +10,7 @@
@@ -18,7 +18,7 @@
-index f40024f3..0e54f74f 100644
+index 636fe60b..11381559 100644
-@@ -15,6 +15,7 @@
+@@ -21,6 +21,7 @@
-@@ -292,7 +293,6 @@ private:
+@@ -309,7 +310,6 @@ private:
-@@ -410,4 +410,14 @@ private:
+@@ -435,4 +435,14 @@ private:
```


## chore: update find_package calls for Qt private modules for building with Qt 6.10

- upstream: `25b930d59b1d5423ba6b3316b2d7965fa81cf245`
- master-merge: `9a51cd71b459651f53556a6d8804cdfa94310a66`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `9`; files differ vs upstream(mapped): `9`

### compositor/examples/test_capture/CMakeLists.txt

```diff
@@ -1,11 +1,14 @@
- find_package(TreelandProtocols REQUIRED)
- pkg_check_modules(EGL REQUIRED IMPORTED_TARGET egl gl)
+ find_package(DeckCompositorProtocols REQUIRED)
+ pkg_check_modules(EGL REQUIRED IMPORTED_TARGET egl gl glesv2)
-index 354ff6ac..737dd848 100644
+index e6508290..ddcdc3ba 100644
-@@ -1,5 +1,6 @@
+@@ -1,8 +1,8 @@
+-
+     main.cpp
+ )
```

### compositor/examples/test_show_desktop/CMakeLists.txt

```diff
@@ -1,10 +1,10 @@
- find_package(TreelandProtocols REQUIRED)
+ find_package(DeckCompositorProtocols REQUIRED)
-index 40622024..e80d972f 100644
+index c7831720..6ce51e94 100644
```

### compositor/examples/test_super_overlay_surface/CMakeLists.txt

```diff
@@ -1,10 +1,15 @@
- find_package(TreelandProtocols REQUIRED)
+ find_package(DeckCompositorProtocols REQUIRED)
-index 3a81bed3..f0b844b3 100644
+index a0f4c0f9..4fa50ec7 100644
+@@ -23,4 +24,3 @@ target_link_libraries(${BIN_NAME}
+ )
+ 
+ install(TARGETS ${BIN_NAME} RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}")
+-
```

### compositor/examples/test_virtual_output/CMakeLists.txt

```diff
@@ -1,10 +1,15 @@
- find_package(TreelandProtocols REQUIRED)
+ find_package(DeckCompositorProtocols REQUIRED)
-index 7b3e5dce..553142ab 100644
+index ebc10110..be8a0223 100644
+@@ -22,4 +23,3 @@ target_link_libraries(${BIN_NAME}
+ )
+ 
+ install(TARGETS ${BIN_NAME} RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}")
+-
```

### compositor/examples/test_window_bg/CMakeLists.txt

```diff
@@ -1,10 +1,10 @@
- find_package(TreelandProtocols REQUIRED)
+ find_package(DeckCompositorProtocols REQUIRED)
-index f59d46fc..a6d1eda9 100644
+index ad60cd52..2b361448 100644
```

### compositor/examples/test_window_overlapped/CMakeLists.txt

```diff
@@ -1,10 +1,15 @@
- find_package(TreelandProtocols REQUIRED)
+ find_package(DeckCompositorProtocols REQUIRED)
-index d4ac27ab..33456e89 100644
+index 3901ff56..68be04f3 100644
+@@ -24,4 +25,3 @@ target_link_libraries(${BIN_NAME}
+ )
+ 
+ install(TARGETS ${BIN_NAME} RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}")
+-
```

### compositor/examples/test_window_picker/CMakeLists.txt

```diff
@@ -1,10 +1,10 @@
- find_package(TreelandProtocols REQUIRED)
+ find_package(DeckCompositorProtocols REQUIRED)
-index ca1c0289..6a1fc651 100644
+index 3d7690c1..5ac45d3f 100644
```

### compositor/src/modules/capture/CMakeLists.txt

```diff
@@ -1,11 +1,11 @@
- find_package(TreelandProtocols REQUIRED)
+ find_package(DeckCompositorProtocols REQUIRED)
-index b86bc999..7977bc1e 100644
+index a864ed33..c267b7bb 100644
```

### compositor/tests/test_window_picker/CMakeLists.txt

```diff
@@ -1,10 +1,10 @@
- find_package(TreelandProtocols REQUIRED)
+ find_package(DeckCompositorProtocols REQUIRED)
-index ca1c0289..6a1fc651 100644
+index 3d7690c1..5ac45d3f 100644
```


## feat: support setting brightness & color temperature through treeland-output-manager-v1

- upstream: `cfaea209066868c9fba4bb8ac7f34093665d22fe`
- master-merge: `76cf419bb3637c4a39c3aeb26eee42a0f5dd4ad6`
- mixed commit (需剥离 waylib/qwlroots): `True`
- files changed: `22`; files differ vs upstream(mapped): `6`

### compositor/src/CMakeLists.txt

```diff
@@ -1,10 +1,10 @@
@@ -13,10 +13,10 @@
@@ -24,7 +24,7 @@
-     CLASS_NAME "TreelandConfig"
+ #     CLASS_NAME "TreelandConfig"
-@@ -89,6 +96,7 @@ qt_add_qml_module(libtreeland
+@@ -89,6 +96,7 @@ qt_add_qml_module(libdeckcompositor
-@@ -133,6 +141,8 @@ qt_add_qml_module(libtreeland
+@@ -135,6 +143,8 @@ qt_add_qml_module(libdeckcompositor
-index b85994d9..f6b402d4 100644
+index aa5fecb1..bf478679 100644
-@@ -72,6 +72,13 @@ dtk_add_config_to_cpp(
- )
+@@ -72,6 +72,13 @@ qt_add_dbus_interface(DBUS_INTERFACE   "${PROJECT_SOURCE_DIR}/misc/interfaces/or
+ # )
- qt_add_library(libtreeland SHARED)
+ qt_add_library(libdeckcompositor SHARED)
- set_target_properties(libtreeland PROPERTIES
+ set_target_properties(libdeckcompositor PROPERTIES
```

### compositor/src/modules/CMakeLists.txt

```diff
@@ -1,5 +1,5 @@
-index ecf5493b..eeae4371 100644
+index cff75b33..35f6330f 100644
```

### compositor/src/modules/output-manager/CMakeLists.txt

```diff
@@ -1,21 +1,4 @@
-similarity index 65%
+similarity index 100%
-index 3e06132e..e1afe344 100644
-+++ b/compositor/src/modules/output-manager/CMakeLists.txt
-@@ -10,9 +10,9 @@ impl_treeland(
-     NAME
-         module_primaryoutput
-     SOURCE
--        ${CMAKE_SOURCE_DIR}/src/modules/primary-output/outputmanagement.h
--        ${CMAKE_SOURCE_DIR}/src/modules/primary-output/impl/output_manager_impl.h
--        ${CMAKE_SOURCE_DIR}/src/modules/primary-output/outputmanagement.cpp
--        ${CMAKE_SOURCE_DIR}/src/modules/primary-output/impl/output_manager_impl.cpp
-+        ${CMAKE_SOURCE_DIR}/src/modules/output-manager/outputmanagement.h
-+        ${CMAKE_SOURCE_DIR}/src/modules/output-manager/impl/output_manager_impl.h
-+        ${CMAKE_SOURCE_DIR}/src/modules/output-manager/outputmanagement.cpp
-+        ${CMAKE_SOURCE_DIR}/src/modules/output-manager/impl/output_manager_impl.cpp
-         ${WAYLAND_PROTOCOLS_OUTPUTDIR}/treeland-output-management-protocol.c
- )
```

### compositor/src/output/output.cpp

```diff
@@ -1,5 +1,5 @@
@@ -32,7 +32,7 @@
@@ -47,7 +47,7 @@
-index 565fb56d..adb76841 100644
+index 7904e552..2cc1998d 100644
-@@ -136,8 +142,14 @@ Output::Output(WOutputItem *output, QObject *parent)
+@@ -132,8 +138,14 @@ Output::Output(WOutputItem *output, QObject *parent)
-@@ -886,3 +898,130 @@ QRectF Output::validGeometry() const
+@@ -882,3 +894,130 @@ QRectF Output::validGeometry() const
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -11,7 +11,7 @@
@@ -20,7 +20,7 @@
@@ -31,12 +31,12 @@
-index 1accb9f5..2d1b1669 100644
+index 55b2ecab..bfeb65b4 100644
-@@ -23,7 +23,7 @@
+@@ -24,7 +24,7 @@
-@@ -1132,7 +1132,7 @@ void Helper::init()
+@@ -1140,7 +1140,7 @@ void Helper::init()
-@@ -1193,8 +1193,8 @@ void Helper::init()
+@@ -1202,8 +1202,8 @@ void Helper::init()
-@@ -1206,7 +1206,7 @@ void Helper::init()
+@@ -1215,7 +1215,7 @@ void Helper::init()
+ #ifndef DISABLE_DDM
-                 m_lockScreen->setPrimaryOutputName(m_rootSurfaceContainer->primaryOutput()->output()->name());
```

### compositor/src/seat/helper.h

```diff
@@ -1,8 +1,8 @@
@@ -11,12 +11,12 @@
-index 0e54f74f..6345ecfc 100644
+index 11381559..70bdcb08 100644
-@@ -90,7 +90,7 @@ class DDEShellManagerInterfaceV1;
+@@ -96,7 +96,7 @@ class DDEShellManagerInterfaceV1;
-@@ -378,7 +378,7 @@ private:
+@@ -395,7 +395,7 @@ private:
+ #ifndef DISABLE_DDM
- #ifdef EXT_SESSION_LOCK_V1
-     WSessionLockManager *m_sessionLockManager = nullptr;
+ #endif
```


## feat: Add logout cleanup

- upstream: `0afe407a3b387a2f730807d56cd46b1475711128`
- master-merge: `5148740f9d74562249b987da49e4fa4547ae7654`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `9`; files differ vs upstream(mapped): `4`

### compositor/src/core/shellhandler.cpp

```diff
@@ -1,5 +1,5 @@
-index 105bb4f6..db227e46 100644
+index c28d1f68..caa84e6f 100644
```

### compositor/src/core/treeland.cpp

```diff
@@ -1,13 +1,13 @@
-         connect(qmlEngine, &QQmlEngine::quit, q, &Treeland::quit, Qt::QueuedConnection);
-         helper = qmlEngine->singletonInstance<Helper *>("Treeland", "Helper");
-         connect(helper, &Helper::requestQuit, q, &Treeland::quit, Qt::QueuedConnection);
+     connect(qmlEngine, &QQmlEngine::quit, q, &Treeland::quit, Qt::QueuedConnection);
+     helper = qmlEngine->singletonInstance<Helper *>("DeckShell.Compositor", "Helper");
+     connect(helper, &Helper::requestQuit, q, &Treeland::quit, Qt::QueuedConnection);
-         auto userModel = qmlEngine->singletonInstance<UserModel *>("Treeland", "UserModel");
+     auto userModel = qmlEngine->singletonInstance<UserModel *>("DeckShell.Compositor", "UserModel");
-index 09ca0fe5..597b9244 100644
+index 33e9b00b..88736e61 100644
-@@ -79,7 +79,7 @@ public:
--        helper->init();
-+        helper->init(q);
+@@ -94,7 +94,7 @@ void init()
+-    helper->init();
++    helper->init(q);
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -11,7 +11,7 @@
@@ -28,7 +28,7 @@
@@ -40,7 +40,7 @@
@@ -49,9 +49,9 @@
@@ -67,7 +67,7 @@
-     m_userModel = engine->singletonInstance<UserModel *>("Treeland", "UserModel");
+     m_userModel = engine->singletonInstance<UserModel *>("DeckShell.Compositor", "UserModel");
-index 2d1b1669..e58fe400 100644
+index bfeb65b4..96a37a88 100644
-@@ -38,6 +38,8 @@
+@@ -39,6 +39,8 @@
-@@ -169,6 +171,16 @@ static QByteArray readWindowProperty(xcb_connection_t *connection,
+@@ -170,6 +172,16 @@ static QByteArray readWindowProperty(xcb_connection_t *connection,
-@@ -892,6 +904,11 @@ void Helper::onSurfaceWrapperAdded(SurfaceWrapper *wrapper)
+@@ -894,6 +906,11 @@ void Helper::onSurfaceWrapperAdded(SurfaceWrapper *wrapper)
-@@ -1044,8 +1061,9 @@ void Helper::deleteTaskSwitch()
+@@ -1046,8 +1063,9 @@ void Helper::deleteTaskSwitch()
- 
-@@ -1263,13 +1281,8 @@ void Helper::init()
+ #ifndef DISABLE_DDM
+@@ -1274,13 +1292,8 @@ void Helper::init()
-@@ -2175,6 +2188,42 @@ std::shared_ptr<Session> Helper::sessionForSocket(WSocket *socket) const
+@@ -2204,6 +2217,42 @@ std::shared_ptr<Session> Helper::sessionForSocket(WSocket *socket) const
-@@ -2223,10 +2272,6 @@ std::shared_ptr<Session> Helper::ensureSession(uid_t uid)
+@@ -2252,10 +2301,6 @@ std::shared_ptr<Session> Helper::ensureSession(uid_t uid)
-@@ -2253,44 +2298,27 @@ std::shared_ptr<Session> Helper::ensureSession(uid_t uid)
+@@ -2282,44 +2327,27 @@ std::shared_ptr<Session> Helper::ensureSession(uid_t uid)
-@@ -2348,16 +2376,16 @@ WXWayland *Helper::defaultXWaylandSocket() const
+@@ -2377,16 +2405,16 @@ WXWayland *Helper::defaultXWaylandSocket() const
...
```

### compositor/src/seat/helper.h

```diff
@@ -1,8 +1,8 @@
@@ -31,7 +31,7 @@
@@ -40,7 +40,7 @@
@@ -54,7 +54,7 @@
-index 6345ecfc..a83af367 100644
+index 70bdcb08..40c53be3 100644
-@@ -104,16 +104,27 @@ struct wlr_idle_inhibitor_v1;
+@@ -112,16 +112,27 @@ struct wlr_idle_inhibitor_v1;
-@@ -162,7 +173,7 @@ public:
+@@ -170,7 +181,7 @@ public:
-@@ -189,8 +200,13 @@ public:
+@@ -197,8 +208,13 @@ public:
-@@ -325,15 +341,13 @@ private:
+@@ -342,15 +358,13 @@ private:
```


## fix: Display issues with scaling and resolution switching in copy mode

- upstream: `0205097b0389d212b5be149b2549d4726cee3bfc`
- master-merge: `8c52f93d761686ac45dcd5129ea61ba37e05f847`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `4`; files differ vs upstream(mapped): `4`

### compositor/src/core/qml/CopyOutput.qml

```diff
@@ -1,5 +1,5 @@
@@ -87,8 +87,8 @@
-index 2b557b49..ddf96be6 100644
+index ecb836f6..ee3de4e7 100644
-     }
-@@ -41,7 +83,7 @@ OutputItem {
+ 
+@@ -48,7 +90,7 @@ OutputItem {
```

### compositor/src/core/qml/SurfaceContent.qml

```diff
@@ -1,5 +1,5 @@
-index 26deed02..31299de7 100644
+index ff9aece5..8122f97e 100644
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -11,7 +11,7 @@
@@ -22,7 +22,7 @@
-index 4522dec2..256eb307 100644
+index 12c06131..2f4cfe14 100644
-@@ -512,7 +512,7 @@ void Helper::onOutputTestOrApply(qw_output_configuration_v1 *config, bool onlyTe
+@@ -514,7 +514,7 @@ void Helper::onOutputTestOrApply(qw_output_configuration_v1 *config, bool onlyTe
-@@ -553,9 +553,8 @@ void Helper::onOutputTestOrApply(qw_output_configuration_v1 *config, bool onlyTe
+@@ -555,9 +555,8 @@ void Helper::onOutputTestOrApply(qw_output_configuration_v1 *config, bool onlyTe
-@@ -1808,6 +1807,25 @@ Output *Helper::createCopyOutput(WOutput *output, Output *proxy)
+@@ -1833,6 +1832,25 @@ Output *Helper::createCopyOutput(WOutput *output, Output *proxy)
```

### compositor/src/seat/helper.h

```diff
@@ -1,8 +1,8 @@
-index b10ab23e..767b5393 100644
+index d47c0277..e3b69063 100644
-@@ -332,6 +332,7 @@ private:
+@@ -349,6 +349,7 @@ private:
```


## fix: fix crash on logout & hiding of wayland surface on user switch

- upstream: `f334727fb696be21553cfba4ad1418e468d3dccc`
- master-merge: `ec5529add5795b6c5592d4f21b68f96c2864f228`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `4`; files differ vs upstream(mapped): `4`

### compositor/src/core/shellhandler.cpp

```diff
@@ -1,8 +1,8 @@
-index db227e46..a4a37feb 100644
+index caa84e6f..17f08fc1 100644
-@@ -192,6 +192,8 @@ void ShellHandler::onXdgToplevelSurfaceRemoved(WXdgToplevelSurface *surface)
+@@ -209,6 +209,8 @@ void ShellHandler::onXdgToplevelSurfaceRemoved(WXdgToplevelSurface *surface)
```

### compositor/src/core/treeland.cpp

```diff
@@ -1,8 +1,8 @@
@@ -14,4 +14,4 @@
-@@ -379,7 +379,11 @@ bool Treeland::ActivateWayland(QDBusUnixFileDescriptor _fd)
+@@ -394,7 +394,11 @@ bool Treeland::ActivateWayland(QDBusUnixFileDescriptor _fd)
-index 597b9244..dc8f41f7 100644
+index 88736e61..67520a1a 100644
-     auto userModel =
+ #ifndef DISABLE_DDM
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -28,7 +28,7 @@
@@ -44,7 +44,7 @@
-index 256eb307..6ffa61d9 100644
+index 2f4cfe14..9bf18f0c 100644
-@@ -2255,20 +2255,17 @@ std::shared_ptr<Session> Helper::ensureSession(int id, uid_t uid)
+@@ -2284,20 +2284,17 @@ std::shared_ptr<Session> Helper::ensureSession(int id, uid_t uid)
-@@ -2407,11 +2404,12 @@ void Helper::updateActiveUserSession(const QString &username, int id)
+@@ -2436,11 +2433,12 @@ void Helper::updateActiveUserSession(const QString &username, int id)
-@@ -2419,19 +2417,8 @@ void Helper::updateActiveUserSession(const QString &username, int id)
+@@ -2448,19 +2446,8 @@ void Helper::updateActiveUserSession(const QString &username, int id)
```

### compositor/src/seat/helper.h

```diff
@@ -1,8 +1,8 @@
-index 767b5393..700c0da6 100644
+index e3b69063..c33d343f 100644
-@@ -120,7 +120,6 @@ public:
+@@ -128,7 +128,6 @@ public:
```


## feat: Support org.freedesktop.ScreenSaver specification

- upstream: `d2b1d9e638efa5b139346d7075fe18b01105b718`
- master-merge: `e9d16f79c625dee2ff380e3a8bfed2764ee50e31`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `11`; files differ vs upstream(mapped): `4`

### compositor/src/CMakeLists.txt

```diff
@@ -1,12 +1,12 @@
-index f6b402d4..d4e316a3 100644
+index bf478679..c2801963 100644
-@@ -304,6 +304,7 @@ target_link_libraries(libtreeland
+@@ -321,6 +321,7 @@ target_link_libraries(libdeckcompositor
- set(BIN_NAME treeland)
- 
+ qt_add_executable(${BIN_NAME}
+     main.cpp
```

### compositor/src/modules/CMakeLists.txt

```diff
@@ -1,9 +1,9 @@
-index eeae4371..dde1c213 100644
+index 35f6330f..b59538b3 100644
-@@ -32,3 +32,4 @@ add_subdirectory(dde-shell)
- add_subdirectory(capture)
- add_subdirectory(item-selector)
- add_subdirectory(ddm)
+@@ -34,3 +34,4 @@ add_subdirectory(item-selector)
+ if(NOT DISABLE_DDM)
+     add_subdirectory(ddm)
+ endif()
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -10,7 +10,7 @@
@@ -21,7 +21,7 @@
-@@ -1330,6 +1335,8 @@ void Helper::init(Treeland::Treeland *treeland)
+@@ -1341,6 +1346,8 @@ void Helper::init(Treeland::Treeland *treeland)
-index 6ffa61d9..7b63fad9 100644
+index 9bf18f0c..d8e393cc 100644
-@@ -40,6 +40,7 @@
+@@ -41,6 +41,7 @@
-@@ -759,6 +760,10 @@ void Helper::onNewIdleInhibitor(wlr_idle_inhibitor_v1 *wlr_inhibitor)
+@@ -761,6 +762,10 @@ void Helper::onNewIdleInhibitor(wlr_idle_inhibitor_v1 *wlr_inhibitor)
```

### compositor/src/seat/helper.h

```diff
@@ -1,16 +1,16 @@
@@ -19,7 +19,7 @@
@@ -27,10 +27,11 @@
-index 700c0da6..1770d7a3 100644
+index c33d343f..d099fc1f 100644
-@@ -100,6 +100,7 @@ class UserModel;
- class DDMInterfaceV1;
+@@ -108,6 +108,7 @@ class DDMInterfaceV1;
+ #endif
-@@ -252,6 +253,8 @@ public:
+@@ -267,6 +268,8 @@ public:
-@@ -339,7 +342,6 @@ private:
+@@ -356,7 +359,6 @@ private:
-@@ -395,6 +397,7 @@ private:
-     VirtualOutputV1 *m_virtualOutput = nullptr;
-     OutputManagerV1 *m_outputManagerV1 = nullptr;
+@@ -414,7 +416,7 @@ private:
+ #ifndef DISABLE_DDM
+-
```


## feat: Support Xauthority access control for Xwayland

- upstream: `b24d20a77215acac625d9305368d3d52e446723c`
- master-merge: `6e82408fe93eb69f8d4cb544e903946dde279c5d`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `7`; files differ vs upstream(mapped): `2`

### compositor/src/CMakeLists.txt

```diff
@@ -1,17 +1,16 @@
@@ -19,7 +18,7 @@
--qt_add_dbus_adaptor(DBUS_ADAPTOR "${CMAKE_SOURCE_DIR}/misc/dbus/org.deepin.compositor1.xml" "core/treeland.h" Treeland::Treeland)
+ qt_add_dbus_adaptor(DBUS_ADAPTOR "${PROJECT_SOURCE_DIR}/misc/dbus/org.deepin.compositor1.xml" "core/treeland.h" Treeland::Treeland)
-@@ -92,7 +92,6 @@ qt_add_qml_module(libtreeland
+@@ -92,7 +93,6 @@ qt_add_qml_module(libdeckcompositor
-index 16bcf3f7..a6c4900b 100644
+index 1d41b120..ade35df4 100644
-@@ -25,7 +25,7 @@ pkg_search_module(XCB REQUIRED IMPORTED_TARGET xcb)
+@@ -25,6 +25,7 @@ pkg_search_module(XCB REQUIRED IMPORTED_TARGET xcb)
- set_source_files_properties("${CMAKE_SOURCE_DIR}/misc/interfaces/org.freedesktop.DisplayManager.xml" PROPERTIES
-     NO_NAMESPACE ON
+ set_source_files_properties("${PROJECT_SOURCE_DIR}/misc/interfaces/org.freedesktop.DisplayManager.xml" PROPERTIES
-@@ -348,3 +347,19 @@ target_link_libraries(treeland-sd
+@@ -363,3 +363,19 @@ target_link_libraries(treeland-sd
```

### compositor/src/core/treeland.cpp

```diff
@@ -1,5 +1,5 @@
@@ -9,8 +9,8 @@
@@ -18,7 +18,7 @@
@@ -28,16 +28,15 @@
@@ -56,9 +55,9 @@
@@ -67,7 +66,7 @@
-         connect(qmlEngine, &QQmlEngine::quit, q, &Treeland::quit, Qt::QueuedConnection);
-         helper = qmlEngine->singletonInstance<Helper *>("Treeland", "Helper");
-         connect(helper, &Helper::requestQuit, q, &Treeland::quit, Qt::QueuedConnection);
+     connect(qmlEngine, &QQmlEngine::quit, q, &Treeland::quit, Qt::QueuedConnection);
+     helper = qmlEngine->singletonInstance<Helper *>("DeckShell.Compositor", "Helper");
+     connect(helper, &Helper::requestQuit, q, &Treeland::quit, Qt::QueuedConnection);
-@@ -305,14 +310,16 @@ Treeland::Treeland()
+@@ -320,14 +324,16 @@ Treeland::Treeland()
-@@ -409,7 +416,7 @@ bool Treeland::ActivateWayland(QDBusUnixFileDescriptor _fd)
+@@ -428,7 +434,7 @@ bool Treeland::ActivateWayland(QDBusUnixFileDescriptor _fd)
-@@ -428,43 +435,20 @@ QString Treeland::XWaylandName()
+@@ -447,43 +453,20 @@ QString Treeland::XWaylandName()
-index dc8f41f7..a6742f69 100644
+index 67520a1a..094751e1 100644
- #include "greeter/usermodel.h"
-@@ -12,6 +11,7 @@
+ #include <qcontainerfwd.h>
+@@ -16,6 +15,7 @@
-@@ -34,6 +34,9 @@ using namespace DDM;
+@@ -38,6 +38,9 @@ using namespace DDM;
-@@ -79,6 +82,8 @@ public:
-+
-+        qputenv("WLR_XWAYLAND", QByteArray(LIBEXEC_DIR) + "/treeland-xwayland");
-         helper->init(q);
...
```


## feat: introduce ShortcutManagerV2 and refactor shortcut handling

- upstream: `160e721a2a6a452a22ef2d43fa2c776075e190c8`
- master-merge: `7446270bdf892171a3381c82e933e6d8133b4b57`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `56`; files differ vs upstream(mapped): `7`

### compositor/src/modules/shortcut/CMakeLists.txt

```diff
@@ -1,27 +1,23 @@
- find_package(TreelandProtocols REQUIRED)
+ find_package(DeckCompositorProtocols REQUIRED)
-index 2eceabe0..1a2ba45b 100644
+index e155572b..c1c4095c 100644
-@@ -1,15 +1,19 @@
+@@ -1,6 +1,6 @@
-         module_shortcut
-     SOURCE
--        ${CMAKE_SOURCE_DIR}/src/modules/shortcut/shortcutmanager.h
-         ${CMAKE_SOURCE_DIR}/src/modules/shortcut/impl/shortcut_manager_impl.h
--        ${CMAKE_SOURCE_DIR}/src/modules/shortcut/shortcutmanager.cpp
-         ${CMAKE_SOURCE_DIR}/src/modules/shortcut/impl/shortcut_manager_impl.cpp
-+        ${CMAKE_SOURCE_DIR}/src/modules/shortcut/shortcutmanager.h
-+        ${CMAKE_SOURCE_DIR}/src/modules/shortcut/shortcutmanager.cpp
-+        ${CMAKE_SOURCE_DIR}/src/modules/shortcut/shortcutrunner.h
-+        ${CMAKE_SOURCE_DIR}/src/modules/shortcut/shortcutrunner.cpp
-+        ${CMAKE_SOURCE_DIR}/src/modules/shortcut/shortcutcontroller.h
-+        ${CMAKE_SOURCE_DIR}/src/modules/shortcut/shortcutcontroller.cpp
+@@ -10,6 +10,10 @@ impl_treeland(
+         ${CMAKE_CURRENT_SOURCE_DIR}/impl/shortcut_manager_impl.h
+         ${CMAKE_CURRENT_SOURCE_DIR}/shortcutmanager.cpp
+         ${CMAKE_CURRENT_SOURCE_DIR}/impl/shortcut_manager_impl.cpp
++        ${CMAKE_CURRENT_SOURCE_DIR}/shortcutrunner.h
++        ${CMAKE_CURRENT_SOURCE_DIR}/shortcutrunner.cpp
...
```

### compositor/src/plugins/multitaskview/multitaskview.cpp

```diff
@@ -1,5 +1,5 @@
-index ce65adb9..26d5e81b 100644
+index 39e30854..ee62eff4 100644
```

### compositor/src/plugins/multitaskview/multitaskview.h

```diff
@@ -1,5 +1,5 @@
-index a0892c79..551308cb 100644
+index 1cb44938..5c57cfda 100644
```

### compositor/src/plugins/multitaskview/qml/MultitaskviewProxy.qml

```diff
@@ -1,5 +1,5 @@
-index 654f73cd..4f2b1480 100644
+index d35e6d94..d743d67b 100644
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -13,7 +13,7 @@
@@ -23,7 +23,7 @@
@@ -32,7 +32,7 @@
@@ -72,7 +72,7 @@
@@ -91,7 +91,7 @@
-@@ -1164,17 +1130,7 @@ void Helper::init(Treeland::Treeland *treeland)
+@@ -1168,17 +1134,7 @@ void Helper::init(Treeland::Treeland *treeland)
-@@ -1234,7 +1190,7 @@ void Helper::init(Treeland::Treeland *treeland)
+@@ -1242,7 +1198,7 @@ void Helper::init(Treeland::Treeland *treeland)
-@@ -1426,6 +1382,27 @@ void Helper::init(Treeland::Treeland *treeland)
+@@ -1437,6 +1393,27 @@ void Helper::init(Treeland::Treeland *treeland)
-index 0831e0c6..a33b612c 100644
+index c0576b0d..b539977b 100644
-@@ -28,10 +28,8 @@
+@@ -29,10 +29,8 @@
-@@ -42,6 +40,9 @@
+@@ -43,6 +41,9 @@
-@@ -201,8 +202,6 @@ Helper::Helper(QObject *parent)
+@@ -202,8 +203,6 @@ Helper::Helper(QObject *parent)
-@@ -240,39 +239,6 @@ Helper::Helper(QObject *parent)
+@@ -242,39 +241,6 @@ Helper::Helper(QObject *parent)
-@@ -1568,156 +1545,9 @@ bool Helper::beforeDisposeEvent(WSeat *seat, QWindow *, QInputEvent *event)
+@@ -1583,161 +1560,9 @@ bool Helper::beforeDisposeEvent(WSeat *seat, QWindow *, QInputEvent *event)
+-#if !defined(DISABLE_DDM) || defined(EXT_SESSION_LOCK_V1)
+-#endif
+-
+-            }
--            } else if (m_lockScreen && m_lockScreen->available() && kevent->key() == Qt::Key_L) {
+-            else if (m_lockScreen && m_lockScreen->available() && kevent->key() == Qt::Key_L) {
...
```

### compositor/src/seat/helper.h

```diff
@@ -1,17 +1,16 @@
@@ -21,7 +20,7 @@
@@ -36,7 +35,7 @@
@@ -53,7 +52,7 @@
@@ -62,7 +61,7 @@
@@ -71,9 +70,9 @@
- #include "core/qmlengine.h"
-index e03bf156..6cd187a3 100644
+index ec122acd..dbec2935 100644
-@@ -5,7 +5,7 @@
- 
- #include "modules/foreign-toplevel/foreigntoplevelmanagerv1.h"
--#include "input/togglablegesture.h"
+@@ -10,6 +10,7 @@
+ #include "core/lockscreen.h"
+ #endif
+ #include "input/togglablegesture.h"
-@@ -81,7 +81,8 @@ class SurfaceContainer;
+@@ -87,7 +88,8 @@ class SurfaceContainer;
-@@ -135,13 +136,12 @@ Q_SIGNALS:
+@@ -143,13 +145,12 @@ Q_SIGNALS:
-@@ -180,16 +180,6 @@ public:
+@@ -188,16 +189,6 @@ public:
-@@ -372,8 +362,6 @@ private:
+@@ -389,8 +380,6 @@ private:
-@@ -392,7 +380,7 @@ private:
+@@ -409,7 +398,7 @@ private:
-@@ -415,8 +403,6 @@ private:
-     SurfaceWrapper *m_activatedSurface = nullptr;
+@@ -437,8 +426,6 @@ private:
...
```

### compositor/src/treeland-shortcut/CMakeLists.txt

```diff
@@ -1,5 +1,5 @@
-index acf53b32..466442a8 100644
+index 86512883..2e5f2268 100644
```


## fix: fix dde-session not started after ddm restart or crash recover

- upstream: `723ac6a7c71e0f33a5b0726939f6d4665767fd2b`
- master-merge: `7ad64778fc832ab8ca72739ff80a815f3497f9a0`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `4`; files differ vs upstream(mapped): `1`

### compositor/src/core/treeland.cpp

```diff
@@ -1,8 +1,8 @@
@@ -10,7 +10,7 @@
@@ -61,7 +61,7 @@
@@ -80,5 +80,5 @@
-@@ -310,16 +355,14 @@ Treeland::Treeland()
+@@ -324,16 +369,14 @@ Treeland::Treeland()
-index a6742f69..b6ea02d8 100644
+index 094751e1..c4c648bb 100644
-@@ -34,6 +34,7 @@ using namespace DDM;
+@@ -38,6 +38,7 @@ using namespace DDM;
-@@ -265,6 +266,50 @@ private:
+@@ -279,6 +280,50 @@ private:
- #ifdef QT_DEBUG
+ #ifdef COMPOSITOR_PLUGINS_ADD_BUILD_PATH
```


## chore: Implement splash screen

- upstream: `3af058665f417743bef8256aa2cdc3df19b5044d`
- master-merge: `1fe34958bc58078db385f4b5b83ed6f34d671bec`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `26`; files differ vs upstream(mapped): `9`

### a

```diff
@@ -1,46 +0,0 @@
-+diff --git a/src/core/qml/DockPreview.qml b/src/core/qml/DockPreview.qml
-+--- a/src/core/qml/DockPreview.qml
-++++ b/src/core/qml/DockPreview.qml
-diff --git a/a b/a
-new file mode 100644
-index 00000000..c668db78
-+++ b/a
-@@ -0,0 +1,40 @@
-+index 9845615..b0a4df7 100644
-+@@ -13,7 +13,7 @@ import org.deepin.dtk 1.0 as D
-+ 
-+ Item {
-+     id: root
-+-    property int aniDuration: 0
-++    property int aniDuration: 200
-+     // whether animations are enabled; default to true when aniDuration > 0
-+     property bool enableAnimation: aniDuration > 0
-+     property alias spacing: listview.spacing
-+@@ -408,7 +408,7 @@ Item {
-+         highlightFollowsCurrentItem: true
-+         implicitHeight: root.implicitHeight - headLayout.implicitHeight
-+         implicitWidth: root.implicitWidth - listview.spacing * 2
-+-        highlightMoveDuration: root.enableAnimation ? 200 : 0
-++        highlightMoveDuration: root.enableAnimation ? root.aniDuration/2 : 0
...
```

### compositor/CMakeLists.txt

```diff
@@ -1,13 +1,13 @@
-index a5ce11b9..45be3e9a 100644
+index 5633d77e..58681ec0 100644
-@@ -22,7 +22,7 @@ add_feature_info(submodule_waylib WITH_SUBMODULE_WAYLIB "Use waylib from submodu
- option(ADDRESS_SANITIZER "Enable address sanitizer" OFF)
- add_feature_info(ASanSupport ADDRESS_SANITIZER "https://github.com/google/sanitizers/wiki/AddressSanitizer")
+@@ -37,7 +37,7 @@ option(ADDRESS_SANITIZER "Enable address sanitizer" OFF)
+ add_feature_info(ASanSupport ADDRESS_SANITIZER
+     "https://github.com/google/sanitizers/wiki/AddressSanitizer")
- option(DISABLE_DDM "Disable DDM and greeter" OFF)
+ option(DISABLE_DDM "Disable DDM and greeter" ON)
```

### compositor/a

```diff
@@ -0,0 +1,46 @@
++diff --git a/src/core/qml/DockPreview.qml b/src/core/qml/DockPreview.qml
++--- a/src/core/qml/DockPreview.qml
+diff --git a/compositor/a b/compositor/a
+new file mode 100644
+index 00000000..c668db78
+--- /dev/null
+@@ -0,0 +1,40 @@
++index 9845615..b0a4df7 100644
++@@ -13,7 +13,7 @@ import org.deepin.dtk 1.0 as D
++ 
++ Item {
++     id: root
++-    property int aniDuration: 0
++     // whether animations are enabled; default to true when aniDuration > 0
++     property bool enableAnimation: aniDuration > 0
++     property alias spacing: listview.spacing
++@@ -408,7 +408,7 @@ Item {
++         highlightFollowsCurrentItem: true
++         implicitHeight: root.implicitHeight - headLayout.implicitHeight
++         implicitWidth: root.implicitWidth - listview.spacing * 2
++-        highlightMoveDuration: root.enableAnimation ? 200 : 0
++         spacing: 5
++         highlight: Control {
++             objectName: "highlight"
...
```

### compositor/src/CMakeLists.txt

```diff
@@ -1,16 +1,16 @@
-@@ -112,6 +112,7 @@ qt_add_qml_module(libtreeland
+@@ -113,6 +113,7 @@ qt_add_qml_module(libdeckcompositor
-@@ -212,6 +213,7 @@ qt_add_qml_module(libtreeland
+@@ -215,6 +216,7 @@ qt_add_qml_module(libdeckcompositor
-index a6c4900b..d672c345 100644
+index ade35df4..9ce9ea4a 100644
+         config/treelandconfig.cpp
+         config/treelandconfig.hpp
-         effects/tquickradiuseffect.h
-         effects/tquickradiuseffect_p.h
```

### compositor/src/core/qmlengine.cpp

```diff
@@ -1,12 +1,12 @@
-     , layershellAnimationComponent(this, "Treeland", "LayerShellAnimation")
-     , lockScreenFallbackComponent(this, "Treeland", "LockScreenFallback")
-     , fpsDisplayComponent(this, "Treeland", "FpsDisplay")
-+    , prelaunchSplashComponent(this, "Treeland", "PrelaunchSplash")
+     , layershellAnimationComponent(this, "DeckShell.Compositor", "LayerShellAnimation")
+     , lockScreenFallbackComponent(this, "DeckShell.Compositor", "LockScreenFallback")
+     , fpsDisplayComponent(this, "DeckShell.Compositor", "FpsDisplay")
++    , prelaunchSplashComponent(this, "DeckShell.Compositor", "PrelaunchSplash")
-index 24afe885..0fd823bb 100644
+index d5e9f5b7..bdc89774 100644
```

### compositor/src/core/shellhandler.cpp

```diff
@@ -1,5 +1,5 @@
@@ -108,7 +108,7 @@
@@ -183,6 +183,10 @@
@@ -232,7 +236,7 @@
@@ -241,7 +245,7 @@
@@ -389,7 +393,7 @@
-index 22f49a35..bae70ce3 100644
+index 629f6d16..db0a837a 100644
-@@ -135,40 +195,107 @@ void ShellHandler::initInputMethodHelper(WServer *server, WSeat *seat)
+@@ -135,10 +195,72 @@ void ShellHandler::initInputMethodHelper(WServer *server, WSeat *seat)
+     } else {
+@@ -159,33 +281,38 @@ void ShellHandler::onXdgToplevelSurfaceAdded(WXdgToplevelSurface *surface)
+             wrapper->setProperty("ddeShellConnection", QVariant::fromValue(connection));
+         }
-@@ -180,8 +307,6 @@ void ShellHandler::onXdgToplevelSurfaceRemoved(WXdgToplevelSurface *surface)
+@@ -197,8 +324,6 @@ void ShellHandler::onXdgToplevelSurfaceRemoved(WXdgToplevelSurface *surface)
-@@ -232,48 +357,116 @@ void ShellHandler::onXdgPopupSurfaceRemoved(WXdgPopupSurface *surface)
+@@ -249,48 +374,116 @@ void ShellHandler::onXdgPopupSurfaceRemoved(WXdgPopupSurface *surface)
-@@ -522,3 +715,5 @@ void ShellHandler::setResourceManagerAtom(WAYLIB_SERVER_NAMESPACE::WXWayland *xw
+@@ -539,3 +732,5 @@ void ShellHandler::setResourceManagerAtom(WAYLIB_SERVER_NAMESPACE::WXWayland *xw
```

### compositor/src/modules/CMakeLists.txt

```diff
@@ -1,10 +1,10 @@
-index dde1c213..410c3a52 100644
+index b59538b3..60586fdc 100644
-@@ -33,3 +33,5 @@ add_subdirectory(capture)
- add_subdirectory(item-selector)
- add_subdirectory(ddm)
+@@ -35,3 +35,5 @@ if(NOT DISABLE_DDM)
+     add_subdirectory(ddm)
+ endif()
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -11,7 +11,7 @@
@@ -26,8 +26,8 @@
-@@ -1144,6 +1146,14 @@ void Helper::init(Treeland::Treeland *treeland)
+@@ -1150,6 +1152,14 @@ void Helper::init(Treeland::Treeland *treeland)
-@@ -1288,6 +1298,11 @@ void Helper::init(Treeland::Treeland *treeland)
-     qmlRegisterType<CaptureSourceSelector>("Treeland.Protocols", 1, 0, "CaptureSourceSelector");
+@@ -1299,6 +1309,11 @@ void Helper::init(Treeland::Treeland *treeland)
+     qmlRegisterType<CaptureSourceSelector>("DeckShell.Compositor.Protocols", 1, 0, "CaptureSourceSelector");
-index 563760c5..5cb01c93 100644
+index 5febac70..8cca5b9a 100644
-@@ -43,6 +43,8 @@
+@@ -44,6 +44,8 @@
```

### compositor/src/seat/helper.h

```diff
@@ -1,8 +1,8 @@
@@ -12,7 +12,7 @@
@@ -20,11 +20,11 @@
-index 6cd187a3..c9e39538 100644
+index dbec2935..d1b70e30 100644
-@@ -19,6 +19,9 @@
+@@ -26,6 +26,9 @@
-@@ -88,6 +91,7 @@ class WallpaperColorV1;
+@@ -95,6 +98,7 @@ class WallpaperColorV1;
-@@ -387,6 +391,7 @@ private:
+@@ -405,6 +409,7 @@ private:
-     DDMInterfaceV1 *m_ddmInterfaceV1 = nullptr;
+ #ifndef DISABLE_DDM
```


## refactor: extract common surface container update logic

- upstream: `40f1ea4a41463de5ef4669a5bc49cdb4b59c2128`
- master-merge: `a52bff83ab6288541ca785eb120c25a9179dda09`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `2`; files differ vs upstream(mapped): `1`

### compositor/src/core/shellhandler.cpp

```diff
@@ -1,5 +1,5 @@
@@ -41,8 +41,8 @@
@@ -74,7 +74,7 @@
-index 046d951d..df1f1bb3 100644
+index 3c24da01..bdbae4cb 100644
-@@ -258,31 +290,7 @@ void ShellHandler::initXdgWrapperCommon(WXdgToplevelSurface *surface, SurfaceWra
-         handleDdeShellSurfaceAdded(surface->surface(), wrapper);
+@@ -275,31 +307,7 @@ void ShellHandler::initXdgWrapperCommon(WXdgToplevelSurface *surface, SurfaceWra
+         }
-@@ -456,36 +464,9 @@ SurfaceWrapper *ShellHandler::matchOrCreateXwaylandWrapper(WXWaylandSurface *sur
+@@ -473,36 +481,9 @@ SurfaceWrapper *ShellHandler::matchOrCreateXwaylandWrapper(WXWaylandSurface *sur
```


## fix: handle undetermined surface type in session checks

- upstream: `7a8bdef0af2b50d52b232100f1d7bd85385599db`
- master-merge: `76618c09f3ec8a2175afa82481435525b41b3b89`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `4`; files differ vs upstream(mapped): `3`

### a

```diff
@@ -1,46 +0,0 @@
--diff --git a/src/core/qml/DockPreview.qml b/src/core/qml/DockPreview.qml
--+++ b/src/core/qml/DockPreview.qml
-diff --git a/a b/a
-deleted file mode 100644
-index c668db78..00000000
-+++ /dev/null
-@@ -1,40 +0,0 @@
--index 9845615..b0a4df7 100644
--@@ -13,7 +13,7 @@ import org.deepin.dtk 1.0 as D
-- 
-- Item {
--     id: root
--+    property int aniDuration: 200
--     // whether animations are enabled; default to true when aniDuration > 0
--     property bool enableAnimation: aniDuration > 0
--     property alias spacing: listview.spacing
--@@ -408,7 +408,7 @@ Item {
--         highlightFollowsCurrentItem: true
--         implicitHeight: root.implicitHeight - headLayout.implicitHeight
--         implicitWidth: root.implicitWidth - listview.spacing * 2
--+        highlightMoveDuration: root.enableAnimation ? root.aniDuration/2 : 0
--         spacing: 5
--         highlight: Control {
--             objectName: "highlight"
...
```

### compositor/a

```diff
@@ -0,0 +1,46 @@
+-diff --git a/src/core/qml/DockPreview.qml b/src/core/qml/DockPreview.qml
+---- a/src/core/qml/DockPreview.qml
+-+++ b/src/core/qml/DockPreview.qml
+diff --git a/compositor/a b/compositor/a
+deleted file mode 100644
+index c668db78..00000000
+--- a/compositor/a
+@@ -1,40 +0,0 @@
+-index 9845615..b0a4df7 100644
+-@@ -13,7 +13,7 @@ import org.deepin.dtk 1.0 as D
+- 
+- Item {
+-     id: root
+--    property int aniDuration: 0
+-+    property int aniDuration: 200
+-     // whether animations are enabled; default to true when aniDuration > 0
+-     property bool enableAnimation: aniDuration > 0
+-     property alias spacing: listview.spacing
+-@@ -408,7 +408,7 @@ Item {
+-         highlightFollowsCurrentItem: true
+-         implicitHeight: root.implicitHeight - headLayout.implicitHeight
+-         implicitWidth: root.implicitWidth - listview.spacing * 2
+--        highlightMoveDuration: root.enableAnimation ? 200 : 0
+-+        highlightMoveDuration: root.enableAnimation ? root.aniDuration/2 : 0
...
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
-index f32d9963..cc4afd3a 100644
+index 05b6fe1b..5f839253 100644
-@@ -1096,6 +1096,10 @@ void Helper::onSurfaceWrapperAboutToRemove(SurfaceWrapper *wrapper)
+@@ -1098,6 +1098,10 @@ void Helper::onSurfaceWrapperAboutToRemove(SurfaceWrapper *wrapper)
```


## feat: add global configuration for prelaunch splash feature

- upstream: `5a67e8d2a18e6e2a019a7c36c12a45b5107a2cfa`
- master-merge: `2fdc9639b48780feace796edf9b9e2e26f63fefb`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `7`; files differ vs upstream(mapped): `5`

### compositor/src/CMakeLists.txt

```diff
@@ -1,10 +1,10 @@
-     CLASS_NAME "TreelandConfig"
+ #     CLASS_NAME "TreelandConfig"
-index d672c345..f60d0d05 100644
+index 9ce9ea4a..05dd640d 100644
-@@ -72,6 +72,13 @@ dtk_add_config_to_cpp(
- )
+@@ -73,6 +73,13 @@ qt_add_dbus_interface(DBUS_INTERFACE   "${PROJECT_SOURCE_DIR}/misc/interfaces/or
+ # )
```

### compositor/src/core/shellhandler.cpp

```diff
@@ -1,5 +1,5 @@
-index 7c9df7a0..350cea6f 100644
+index c74c1238..3e6d10f5 100644
```

### compositor/src/output/output.cpp

```diff
@@ -1,8 +1,8 @@
-index adb76841..cd8637af 100644
+index 2cc1998d..a10a9624 100644
-@@ -149,7 +149,7 @@ Output::Output(WOutputItem *output, QObject *parent)
+@@ -145,7 +145,7 @@ Output::Output(WOutputItem *output, QObject *parent)
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -10,13 +10,14 @@
@@ -25,7 +26,7 @@
@@ -39,22 +40,19 @@
--    m_config = TreelandConfig::createByName("org.deepin.treeland",
+-    // m_config = TreelandConfig::createByName("org.deepin.treeland",
+-    m_config = &TreelandConfig::ref();
-@@ -1119,8 +1127,6 @@ void Helper::init(Treeland::Treeland *treeland)
-     auto engine = qmlEngine();
-     m_userModel = engine->singletonInstance<UserModel *>("Treeland", "UserModel");
+@@ -1123,8 +1130,6 @@ void Helper::init(Treeland::Treeland *treeland)
+     m_userModel = engine->singletonInstance<UserModel *>("DeckShell.Compositor", "UserModel");
-@@ -1224,9 +1230,9 @@ void Helper::init(Treeland::Treeland *treeland)
+@@ -1233,6 +1238,9 @@ void Helper::init(Treeland::Treeland *treeland)
--        m_config = TreelandConfig::createByName("org.deepin.treeland",
-index cc4afd3a..9bb8e6d9 100644
+index 5f839253..b942c15b 100644
-@@ -36,6 +36,7 @@
+@@ -37,6 +37,7 @@
-@@ -209,9 +210,11 @@ Helper::Helper(QObject *parent)
+@@ -210,10 +211,11 @@ Helper::Helper(QObject *parent)
--                                            "org.deepin.treeland",
--                                            QString());
+-    //                                         "org.deepin.treeland",
+-    //                                         QString());
-@@ -301,7 +304,12 @@ Helper *Helper::instance()
+@@ -303,7 +305,12 @@ Helper *Helper::instance()
+ #endif
...
```

### compositor/src/seat/helper.h

```diff
@@ -1,8 +1,8 @@
@@ -10,15 +10,15 @@
@@ -26,7 +26,7 @@
@@ -34,7 +34,7 @@
-index c9e39538..9e996179 100644
+index d1b70e30..872c6ebb 100644
-@@ -33,6 +33,7 @@ Q_MOC_INCLUDE("modules/capture/capture.h")
+@@ -40,6 +40,7 @@ Q_MOC_INCLUDE("modules/capture/capture.h")
-@@ -104,6 +105,7 @@ class ILockScreen;
- class UserModel;
+@@ -113,6 +114,7 @@ class UserModel;
+ #endif
-@@ -149,6 +151,7 @@ class Helper : public WSeatEventFilter
+@@ -158,6 +160,7 @@ class Helper : public WSeatEventFilter
-@@ -176,6 +179,7 @@ public:
+@@ -185,6 +188,7 @@ public:
-@@ -348,7 +352,8 @@ private:
+@@ -366,7 +370,8 @@ private:
```


## chore: cleanup build configuration and xwayland code

- upstream: `36a0753d404160cd497a72f1d6dee2fc1dd397eb`
- master-merge: `6cc9788ec0df87455269974ce0863dd0540c074c`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `5`; files differ vs upstream(mapped): `2`

### compositor/CMakeLists.txt

```diff
@@ -1,13 +1,13 @@
-index 7826d4d1..9269ab54 100644
+index 72998a1e..71b972f6 100644
-@@ -22,7 +22,7 @@ add_feature_info(submodule_waylib WITH_SUBMODULE_WAYLIB "Use waylib from submodu
- option(ADDRESS_SANITIZER "Enable address sanitizer" OFF)
- add_feature_info(ASanSupport ADDRESS_SANITIZER "https://github.com/google/sanitizers/wiki/AddressSanitizer")
+@@ -37,7 +37,7 @@ option(ADDRESS_SANITIZER "Enable address sanitizer" OFF)
+ add_feature_info(ASanSupport ADDRESS_SANITIZER
+     "https://github.com/google/sanitizers/wiki/AddressSanitizer")
- option(DISABLE_DDM "Disable DDM and greeter" OFF)
+ option(DISABLE_DDM "Disable DDM and greeter" ON)
```

### compositor/src/core/shellhandler.cpp

```diff
@@ -1,5 +1,5 @@
-index 56a4c9f9..496dc07c 100644
+index d00e039f..8e0a851a 100644
```


## refactor: reorganize dconfig file structure

- upstream: `0cd74fbb1089139cc845ec83fce0e787b8f37b2e`
- master-merge: `02e12851ca3347f2ae6ac067fb78210e69660de3`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `14`; files differ vs upstream(mapped): `6`

### compositor/src/CMakeLists.txt

```diff
@@ -1,16 +1,23 @@
@@ -30,7 +37,7 @@
+-#     CLASS_NAME "TreelandConfig"
-     CLASS_NAME "TreelandConfig"
++    CLASS_NAME "TreelandConfig"
-@@ -102,6 +102,7 @@ qt_add_qml_module(libtreeland
+@@ -103,6 +103,7 @@ qt_add_qml_module(libdeckcompositor
-index f60d0d05..7f32e566 100644
+index 05dd640d..dfa48341 100644
-@@ -67,21 +67,21 @@ qt_add_dbus_interface(DBUS_INTERFACE   "${CMAKE_SOURCE_DIR}/misc/interfaces/org.
+@@ -66,23 +66,23 @@ qt_add_dbus_interface(DBUS_INTERFACE   "${PROJECT_SOURCE_DIR}/misc/interfaces/or
+ qt_add_dbus_interface(DBUS_INTERFACE   "${PROJECT_SOURCE_DIR}/misc/interfaces/org.freedesktop.login1.Session.xml"          Login1Session)
+ qt_add_dbus_interface(DBUS_INTERFACE   "${PROJECT_SOURCE_DIR}/misc/interfaces/org.freedesktop.login1.User.xml"             Login1User)
- dtk_add_config_to_cpp(
-     TREELAND_CONFIG
--    "${PROJECT_SOURCE_DIR}/misc/dconfig/org.deepin.treeland.json"
+-# dtk_add_config_to_cpp(
+-#     TREELAND_CONFIG
+-#     "${PROJECT_SOURCE_DIR}/misc/dconfig/org.deepin.treeland.json"
+-#     OUTPUT_FILE_NAME "treelandconfig.hpp"
+-# )
++dtk_add_config_to_cpp(
++    TREELAND_CONFIG
-     OUTPUT_FILE_NAME "treelandconfig.hpp"
- )
++    OUTPUT_FILE_NAME "treelandconfig.hpp"
...
```

### compositor/src/core/shellhandler.cpp

```diff
@@ -1,5 +1,5 @@
-index a2d75908..289dcf79 100644
+index bdbbaf05..975685e6 100644
```

### compositor/src/output/output.cpp

```diff
@@ -1,5 +1,5 @@
@@ -17,7 +17,7 @@
@@ -28,7 +28,7 @@
-     QQmlComponent delegate(engine, "Treeland", "PrimaryOutput");
+     QQmlComponent delegate(engine, "DeckShell.Compositor", "PrimaryOutput");
-index cd8637af..6f977379 100644
+index a10a9624..7cce0e47 100644
-@@ -149,7 +150,7 @@ Output::Output(WOutputItem *output, QObject *parent)
+@@ -145,7 +146,7 @@ Output::Output(WOutputItem *output, QObject *parent)
```

### compositor/src/plugins/multitaskview/multitaskview.cpp

```diff
@@ -1,5 +1,5 @@
-index 8d79da74..666dda37 100644
+index 9d77f7e4..3b891222 100644
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -11,7 +11,7 @@
@@ -25,7 +25,7 @@
@@ -40,9 +40,9 @@
-@@ -1230,8 +1230,8 @@ void Helper::init(Treeland::Treeland *treeland)
+@@ -1238,8 +1238,8 @@ void Helper::init(Treeland::Treeland *treeland)
-index 69a3020a..9deeac70 100644
+index 643c5e95..b7616356 100644
-@@ -36,7 +36,7 @@
+@@ -37,7 +37,7 @@
-@@ -210,10 +210,10 @@ Helper::Helper(QObject *parent)
+@@ -211,10 +211,10 @@ Helper::Helper(QObject *parent)
-@@ -302,12 +302,12 @@ Helper *Helper::instance()
+@@ -303,12 +303,12 @@ Helper *Helper::instance()
-     m_personalization = m_server->attach<PersonalizationV1>();
+ #ifndef DISABLE_DDM
```

### compositor/src/seat/helper.h

```diff
@@ -1,8 +1,8 @@
@@ -11,16 +11,16 @@
@@ -31,7 +31,7 @@
@@ -42,7 +42,7 @@
-index 9e996179..30c8ad21 100644
+index 872c6ebb..29212025 100644
-@@ -33,7 +33,7 @@ Q_MOC_INCLUDE("modules/capture/capture.h")
+@@ -40,7 +40,7 @@ Q_MOC_INCLUDE("modules/capture/capture.h")
-@@ -105,7 +105,7 @@ class ILockScreen;
- class UserModel;
+@@ -114,7 +114,7 @@ class UserModel;
+ #endif
-@@ -150,8 +150,8 @@ class Helper : public WSeatEventFilter
+@@ -159,8 +159,8 @@ class Helper : public WSeatEventFilter
-@@ -178,8 +178,8 @@ public:
+@@ -187,8 +187,8 @@ public:
-@@ -352,8 +352,8 @@ private:
+@@ -370,8 +370,8 @@ private:
```


## feat: optimize prelaunch splash handling and logging

- upstream: `8afacc53dd6df34d5e906475f6fc0598f17e5daf`
- master-merge: `a01e0f9db1a56a13008e09c11e9d18e5d31528e1`
- mixed commit (需剥离 waylib/qwlroots): `True`
- files changed: `5`; files differ vs upstream(mapped): `2`

### compositor/src/core/shellhandler.cpp

```diff
@@ -1,5 +1,5 @@
-index 289dcf79..e8576299 100644
+index 975685e6..fba32511 100644
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -13,7 +13,7 @@
@@ -22,9 +22,9 @@
-@@ -1163,7 +1163,7 @@ void Helper::init(Treeland::Treeland *treeland)
+@@ -1168,7 +1168,7 @@ void Helper::init(Treeland::Treeland *treeland)
-@@ -1230,8 +1230,8 @@ void Helper::init(Treeland::Treeland *treeland)
+@@ -1238,8 +1238,8 @@ void Helper::init(Treeland::Treeland *treeland)
-index 9deeac70..98ed0e1f 100644
+index b7616356..0db080b7 100644
-@@ -210,8 +210,8 @@ Helper::Helper(QObject *parent)
+@@ -211,8 +211,8 @@ Helper::Helper(QObject *parent)
-     m_personalization = m_server->attach<PersonalizationV1>();
+ #ifndef DISABLE_DDM
```


## fix: resolve code review issues

- upstream: `811594cadc42d98ee64a651e85e12e60f4b9da74`
- master-merge: `5a3fc11390e966bc351a86d8ac197648eef0b4c1`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `7`; files differ vs upstream(mapped): `3`

### compositor/src/core/shellhandler.cpp

```diff
@@ -1,8 +1,8 @@
-index e8576299..ef7e9d3c 100644
+index fba32511..b3b71af8 100644
-@@ -322,18 +322,19 @@ void ShellHandler::onXdgToplevelSurfaceRemoved(WXdgToplevelSurface *surface)
+@@ -339,18 +339,19 @@ void ShellHandler::onXdgToplevelSurfaceRemoved(WXdgToplevelSurface *surface)
```

### compositor/src/output/output.cpp

```diff
@@ -1,8 +1,8 @@
@@ -13,7 +13,7 @@
-index 6a719dd8..7d18ac9a 100644
+index 36798d82..4c88d1e8 100644
-@@ -150,7 +150,9 @@ Output::Output(WOutputItem *output, QObject *parent)
+@@ -146,7 +146,9 @@ Output::Output(WOutputItem *output, QObject *parent)
-@@ -233,7 +235,6 @@ void Output::placeCentered(SurfaceWrapper *surface)
+@@ -229,7 +231,6 @@ void Output::placeCentered(SurfaceWrapper *surface)
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -11,8 +11,8 @@
-@@ -1231,7 +1231,7 @@ void Helper::init(Treeland::Treeland *treeland)
+@@ -1239,7 +1239,7 @@ void Helper::init(Treeland::Treeland *treeland)
-index c01c8e3e..3a11d249 100644
+index 90cb9f96..cab21e69 100644
-@@ -211,7 +211,7 @@ Helper::Helper(QObject *parent)
+@@ -212,7 +212,7 @@ Helper::Helper(QObject *parent)
- 
+ #ifndef DISABLE_DDM
```


## feat: Add display mode recording and automatic restoration system

- upstream: `72da3e3f1eedaf6007ef4c2ce18e85dbea7ccba3`
- master-merge: `16938104fb7d15b7cbc209b02863a76da1ad5eff`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `10`; files differ vs upstream(mapped): `4`

### compositor/src/CMakeLists.txt

```diff
@@ -1,8 +1,8 @@
-@@ -151,6 +151,10 @@ qt_add_qml_module(libtreeland
+@@ -154,6 +154,10 @@ qt_add_qml_module(libdeckcompositor
-index 7f32e566..0a7e8b96 100644
+index dfa48341..a84d11b7 100644
```

### compositor/src/output/output.cpp

```diff
@@ -1,8 +1,8 @@
@@ -11,7 +11,7 @@
-index 7d18ac9a..39185811 100644
+index 4c88d1e8..7a36f203 100644
-@@ -131,7 +131,7 @@ Output *Output::createCopy(WOutput *output, Output *proxy, QQmlEngine *engine, Q
+@@ -127,7 +127,7 @@ Output *Output::createCopy(WOutput *output, Output *proxy, QQmlEngine *engine, Q
-@@ -388,7 +388,7 @@ void Output::enable()
+@@ -384,7 +384,7 @@ void Output::enable()
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -11,7 +11,7 @@
@@ -22,7 +22,7 @@
@@ -59,7 +59,7 @@
@@ -137,7 +137,7 @@
@@ -148,7 +148,7 @@
-index 3a11d249..b04fd374 100644
+index cab21e69..5660a80a 100644
-@@ -23,6 +23,8 @@
+@@ -24,6 +24,8 @@
-@@ -224,6 +226,10 @@ Helper::Helper(QObject *parent)
+@@ -225,6 +227,10 @@ Helper::Helper(QObject *parent)
-@@ -387,12 +393,35 @@ void Helper::onOutputAdded(WOutput *output)
+@@ -388,12 +394,35 @@ void Helper::onOutputAdded(WOutput *output)
-@@ -439,26 +468,62 @@ void Helper::onOutputRemoved(WOutput *output)
+@@ -440,26 +469,62 @@ void Helper::onOutputRemoved(WOutput *output)
-@@ -502,6 +567,10 @@ void Helper::handleCopyModeOutputDisable(Output *affectedOutput)
+@@ -503,6 +568,10 @@ void Helper::handleCopyModeOutputDisable(Output *affectedOutput)
-@@ -533,7 +602,6 @@ void Helper::handleCopyModeOutputDisable(Output *affectedOutput)
+@@ -534,7 +603,6 @@ void Helper::handleCopyModeOutputDisable(Output *affectedOutput)
-@@ -594,6 +662,29 @@ void Helper::onOutputTestOrApply(qw_output_configuration_v1 *config, bool onlyTe
+@@ -595,6 +663,29 @@ void Helper::onOutputTestOrApply(qw_output_configuration_v1 *config, bool onlyTe
-@@ -1782,32 +1873,7 @@ void Helper::moveSurfacesToOutput(const QList<SurfaceWrapper *> &surfaces,
+@@ -1799,32 +1890,7 @@ void Helper::moveSurfacesToOutput(const QList<SurfaceWrapper *> &surfaces,
-@@ -2746,6 +2812,7 @@ void Helper::setNoAnimation(bool noAnimation) {
+@@ -2786,6 +2852,7 @@ void Helper::setNoAnimation(bool noAnimation) {
-@@ -2756,3 +2823,47 @@ void Helper::toggleFpsDisplay()
+@@ -2796,3 +2863,47 @@ void Helper::toggleFpsDisplay()
```

### compositor/src/seat/helper.h

```diff
@@ -1,17 +1,17 @@
@@ -20,8 +20,8 @@
- class TreelandUserConfig;
-index 30c8ad21..e5ae5a63 100644
+index 29212025..100bcf35 100644
-@@ -103,6 +103,8 @@ class IMultitaskView;
- class LockScreenInterface;
+@@ -111,6 +111,8 @@ class LockScreenInterface;
+ #ifndef DISABLE_DDM
+ #endif
-@@ -342,6 +344,8 @@ private:
+@@ -360,6 +362,8 @@ private:
-@@ -407,6 +411,8 @@ private:
- #endif
+@@ -428,6 +432,8 @@ private:
+ 
```


## refactor: use qtwayland scanner for treeland-shortcut-manager-v2 protocol implementation

- upstream: `39888b579f5241f7242da9edf5fc3cbcb2b58517`
- master-merge: `bfa60cd9dfb763836dec33b92122171573794bf5`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `6`; files differ vs upstream(mapped): `1`

### compositor/src/modules/shortcut/CMakeLists.txt

```diff
@@ -1,9 +1,9 @@
@@ -15,18 +15,24 @@
- find_package(TreelandProtocols REQUIRED)
+ find_package(DeckCompositorProtocols REQUIRED)
-index 1a2ba45b..c184fe0f 100644
+index c1c4095c..85085ea9 100644
--        ${CMAKE_SOURCE_DIR}/src/modules/shortcut/impl/shortcut_manager_impl.h
--        ${CMAKE_SOURCE_DIR}/src/modules/shortcut/impl/shortcut_manager_impl.cpp
-         ${CMAKE_SOURCE_DIR}/src/modules/shortcut/shortcutmanager.h
-         ${CMAKE_SOURCE_DIR}/src/modules/shortcut/shortcutmanager.cpp
-         ${CMAKE_SOURCE_DIR}/src/modules/shortcut/shortcutrunner.h
-         ${CMAKE_SOURCE_DIR}/src/modules/shortcut/shortcutrunner.cpp
-         ${CMAKE_SOURCE_DIR}/src/modules/shortcut/shortcutcontroller.h
-         ${CMAKE_SOURCE_DIR}/src/modules/shortcut/shortcutcontroller.cpp
+-        ${CMAKE_CURRENT_SOURCE_DIR}/shortcutmanager.h
+-        ${CMAKE_CURRENT_SOURCE_DIR}/impl/shortcut_manager_impl.h
+-        ${CMAKE_CURRENT_SOURCE_DIR}/shortcutmanager.cpp
+-        ${CMAKE_CURRENT_SOURCE_DIR}/impl/shortcut_manager_impl.cpp
+-        ${CMAKE_CURRENT_SOURCE_DIR}/shortcutrunner.h
+-        ${CMAKE_CURRENT_SOURCE_DIR}/shortcutrunner.cpp
+-        ${CMAKE_CURRENT_SOURCE_DIR}/shortcutcontroller.h
+-        ${CMAKE_CURRENT_SOURCE_DIR}/shortcutcontroller.cpp
-+        ${CMAKE_BINARY_DIR}/src/modules/shortcut/wayland-treeland-shortcut-manager-v2-server-protocol.c
++        shortcutmanager.h
++        shortcutmanager.cpp
++        shortcutrunner.h
...
```


## Remove unused module

- upstream: `566c2439c7af12dd046aaed36e90d5c1a3f94026`
- master-merge: `a2e0e39d0cc0d26b54daf8c1482b09da2a89b763`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `1`; files differ vs upstream(mapped): `1`

### compositor/src/CMakeLists.txt

```diff
@@ -1,21 +1,27 @@
-index 0a7e8b96..557cb859 100644
+index a84d11b7..93215393 100644
-@@ -12,7 +12,7 @@ include(${CMAKE_SOURCE_DIR}/cmake/TranslationUtils.cmake)
+@@ -11,8 +11,8 @@ endif()
+ set(BIN_NAME deckcompositor)
- if (NOT DISABLE_DDM)
+-if (NOT DISABLE_DDM OR EXT_SESSION_LOCK_V1)
++if (NOT DISABLE_DDM)
-@@ -317,7 +317,6 @@ target_link_libraries(libtreeland
+@@ -335,9 +335,8 @@ target_link_libraries(libdeckcompositor
--        $<$<NOT:$<BOOL:${DISABLE_DDM}>>:DDM::Auth>
-         $<$<NOT:$<BOOL:${DISABLE_DDM}>>:DDM::Common>
-         $<$<NOT:$<BOOL:${DISABLE_DDM}>>:PkgConfig::PAM>
+-        $<$<OR:$<NOT:$<BOOL:${DISABLE_DDM}>>,$<BOOL:${EXT_SESSION_LOCK_V1}>>:DDM::Auth>
+-        $<$<OR:$<NOT:$<BOOL:${DISABLE_DDM}>>,$<BOOL:${EXT_SESSION_LOCK_V1}>>:DDM::Common>
+-        $<$<OR:$<NOT:$<BOOL:${DISABLE_DDM}>>,$<BOOL:${EXT_SESSION_LOCK_V1}>>:PkgConfig::PAM>
++        $<$<NOT:$<BOOL:${DISABLE_DDM}>>:DDM::Common>
++        $<$<NOT:$<BOOL:${DISABLE_DDM}>>:PkgConfig::PAM>
+ 
+ add_subdirectory(plugins)
```


## refactor: use qtwayland scanner for treeland-output-manager-v1 protocol

- upstream: `0002358cb98168a1038d55b7dafe03997ef3ce05`
- master-merge: `6b0aa2f64eb322ccae966be9708398f9d1dba19c`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `9`; files differ vs upstream(mapped): `3`

### compositor/src/modules/output-manager/CMakeLists.txt

```diff
@@ -1,9 +1,9 @@
@@ -19,12 +19,14 @@
- find_package(TreelandProtocols REQUIRED)
+ find_package(DeckCompositorProtocols REQUIRED)
-index e1afe344..fdc01223 100644
+index d7541e89..f848d72d 100644
-         ${CMAKE_SOURCE_DIR}/src/modules/output-manager/outputmanagement.h
--        ${CMAKE_SOURCE_DIR}/src/modules/output-manager/impl/output_manager_impl.h
-         ${CMAKE_SOURCE_DIR}/src/modules/output-manager/outputmanagement.cpp
--        ${CMAKE_SOURCE_DIR}/src/modules/output-manager/impl/output_manager_impl.cpp
+-        ${CMAKE_CURRENT_SOURCE_DIR}/outputmanagement.h
+-        ${CMAKE_CURRENT_SOURCE_DIR}/impl/output_manager_impl.h
+-        ${CMAKE_CURRENT_SOURCE_DIR}/outputmanagement.cpp
+-        ${CMAKE_CURRENT_SOURCE_DIR}/impl/output_manager_impl.cpp
-+        ${CMAKE_BINARY_DIR}/src/modules/output-manager/wayland-treeland-output-manager-v1-server-protocol.c
++        outputmanagement.h
++        outputmanagement.cpp
++    ${CMAKE_BINARY_DIR}/src/modules/output-manager/wayland-treeland-output-manager-v1-server-protocol.c
```

### compositor/src/output/output.cpp

```diff
@@ -1,5 +1,5 @@
@@ -10,7 +10,7 @@
@@ -21,7 +21,7 @@
@@ -36,7 +36,7 @@
@@ -45,7 +45,7 @@
-index 8211622b..ce8f567b 100644
+index 6bc1a418..c2516f93 100644
-@@ -959,7 +958,9 @@ static inline void generateGammaLUT(uint32_t colorTemperature,
+@@ -955,7 +954,9 @@ static inline void generateGammaLUT(uint32_t colorTemperature,
-@@ -977,12 +978,9 @@ void Output::setOutputColor(qreal brightness, uint32_t colorTemperature)
+@@ -973,12 +974,9 @@ void Output::setOutputColor(qreal brightness, uint32_t colorTemperature)
-@@ -998,7 +996,7 @@ void Output::setOutputColor(qreal brightness, uint32_t colorTemperature)
+@@ -994,7 +992,7 @@ void Output::setOutputColor(qreal brightness, uint32_t colorTemperature)
-@@ -1006,14 +1004,14 @@ void Output::setOutputColor(qreal brightness, uint32_t colorTemperature)
+@@ -1002,14 +1000,14 @@ void Output::setOutputColor(qreal brightness, uint32_t colorTemperature)
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -13,7 +13,7 @@
@@ -32,6 +32,7 @@
-@@ -1299,6 +1299,10 @@ void Helper::init(Treeland::Treeland *treeland)
+@@ -1306,6 +1306,10 @@ void Helper::init(Treeland::Treeland *treeland)
-@@ -1359,21 +1363,8 @@ void Helper::init(Treeland::Treeland *treeland)
+@@ -1370,21 +1374,9 @@ void Helper::init(Treeland::Treeland *treeland)
-index 12f97e4d..a0c27f52 100644
+index b9f7609f..048fef4d 100644
++            m_outputManagerV1->onPrimaryOutputChanged();
+ #ifndef DISABLE_DDM
-             }
```


## fix: improve surface proxy handling for splash screens

- upstream: `3000f828e7c8ff115ba099ce600ca821c93951d9`
- master-merge: `6ea6a852bc3307f2c749a84178b3cf03070e6400`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `6`; files differ vs upstream(mapped): `3`

### compositor/src/core/qml/SwitchViewDelegate.qml

```diff
@@ -1,5 +1,5 @@
-index 4312bb61..a65691bb 100644
+index b3994639..560dc4d4 100644
```

### compositor/src/plugins/multitaskview/multitaskview.cpp

```diff
@@ -1,12 +1,15 @@
-index 666dda37..81053147 100644
+index 3b891222..e83ad9ba 100644
-@@ -644,7 +644,13 @@ void MultitaskviewSurfaceModel::monitorUnreadySurface(SurfaceWrapper *surface)
+@@ -671,7 +671,16 @@ void MultitaskviewSurfaceModel::monitorUnreadySurface(SurfaceWrapper *surface)
--    return surface->surface()->mapped() && surfaceGeometry(surface).isValid();
+-    return surface->surface()->mapped() && surfaceGeometry(surface).isValid() && !surface->skipMutiTaskView();
++    if (surface->skipMutiTaskView()) {
++        return false;
++    }
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
-index 87af2cba..dd508756 100644
+index 21d41328..f3ecef7d 100644
-@@ -1193,8 +1193,10 @@ void Helper::onSurfaceWrapperAboutToRemove(SurfaceWrapper *wrapper)
+@@ -1194,8 +1194,10 @@ void Helper::onSurfaceWrapperAboutToRemove(SurfaceWrapper *wrapper)
```


## fix: fix crash on logout

- upstream: `4acd34f7071ae2d37f1ab31e716732a200c45539`
- master-merge: `92ba6b40cb0e14a6d5d18321af4644af7810e339`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `4`; files differ vs upstream(mapped): `3`

### compositor/src/core/treeland.cpp

```diff
@@ -1,8 +1,8 @@
@@ -14,8 +14,8 @@
-@@ -327,10 +327,10 @@ Treeland::Treeland()
+@@ -341,10 +341,10 @@ Treeland::Treeland()
-                 envs.insert("XDG_SESSION_DESKTOP", "Treeland");
-@@ -348,7 +348,7 @@ Treeland::Treeland()
+                 envs.insert("XDG_SESSION_DESKTOP", "DeckShell");
+@@ -362,7 +362,7 @@ Treeland::Treeland()
-index ddff2c5f..89afd2be 100644
+index e0c3aa8e..bbcafe89 100644
```

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -11,7 +11,7 @@
-index dd508756..c7b38860 100644
+index f3ecef7d..35a8fb60 100644
-@@ -2353,7 +2353,7 @@ std::shared_ptr<Session> Helper::ensureSession(int id, uid_t uid)
+@@ -2375,7 +2375,7 @@ std::shared_ptr<Session> Helper::ensureSession(int id, uid_t uid)
-@@ -2365,36 +2365,32 @@ WXWayland *Helper::xwaylandForUid(uid_t uid)
+@@ -2387,36 +2387,32 @@ WXWayland *Helper::xwaylandForUid(uid_t uid)
```

### compositor/src/seat/helper.h

```diff
@@ -1,8 +1,8 @@
-index e5ae5a63..073914d3 100644
+index 100bcf35..481e9bf6 100644
-@@ -206,15 +206,15 @@ public:
+@@ -215,15 +215,15 @@ public:
```


## chore: temporary disable TreelandUserConfig smart pointer

- upstream: `779832f52af2156517da777bcac1d4c69a3a1373`
- master-merge: `3659db161d4b8a597aab2bb331461c019e183953`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `2`; files differ vs upstream(mapped): `2`

### compositor/src/seat/helper.cpp

```diff
@@ -1,8 +1,8 @@
@@ -14,7 +14,7 @@
@@ -23,9 +23,9 @@
-@@ -1324,9 +1324,9 @@ void Helper::init(Treeland::Treeland *treeland)
+@@ -1332,9 +1332,9 @@ void Helper::init(Treeland::Treeland *treeland)
-index c7b38860..f2fb45bc 100644
+index 35a8fb60..df7f8662 100644
-@@ -212,9 +212,9 @@ Helper::Helper(QObject *parent)
+@@ -213,9 +213,9 @@ Helper::Helper(QObject *parent)
-@@ -310,7 +310,7 @@ Helper *Helper::instance()
+@@ -311,7 +311,7 @@ Helper *Helper::instance()
-     m_personalization = m_server->attach<PersonalizationV1>();
+ #ifndef DISABLE_DDM
```

### compositor/src/seat/helper.h

```diff
@@ -1,8 +1,8 @@
-index 073914d3..7ab2d8cf 100644
+index 481e9bf6..ab5562f1 100644
-@@ -356,7 +356,7 @@ private:
+@@ -374,7 +374,7 @@ private:
```


## chore(debian): update version to 0.8.1

- upstream: `4e6aa7a6c3b28b71e49223586435f2004262a35c`
- master-merge: `703b7dc12b8f93b0262b9dc0d6415fb114e9811a`
- mixed commit (需剥离 waylib/qwlroots): `False`
- files changed: `3`; files differ vs upstream(mapped): `1`

### compositor/CMakeLists.txt

```diff
@@ -1,13 +1,13 @@
- project(Treeland
+ project(
-index a7bb8ca4..28c1f84a 100644
+index f214e9a9..38f85c22 100644
-@@ -1,7 +1,7 @@
- cmake_minimum_required(VERSION 3.25.0)
+@@ -2,7 +2,7 @@ cmake_minimum_required(VERSION 3.25.0)
+     DeckCompositor
-     LANGUAGES CXX C)
- 
- set(CMAKE_INCLUDE_CURRENT_DIR ON)
+     LANGUAGES CXX C
+     DESCRIPTION "Deck Shell Compositor"
+ )
```

