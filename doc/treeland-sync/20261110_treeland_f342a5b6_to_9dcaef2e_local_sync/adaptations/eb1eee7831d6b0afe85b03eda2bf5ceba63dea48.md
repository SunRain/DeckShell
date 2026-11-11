# P / DeckShell 适配：feat(greeter): take session dirs and the last login from DDM

- Treeland 来源：` 87e63ff43cd5dec5e56d9402572c4a2f807c8244 `。
- 本仓目标：` eb1eee7831d6b0afe85b03eda2bf5ceba63dea48 `。
- 节点：N10；action=adapted。
- [本仓总记录](../summary.md#entry-31)。

## 比较口径

比较来源唯一父提交 → 来源提交，与原目标唯一父提交 → 原目标提交的逐路径增量。
零上下文补丁对照会呈现基线位置、既有命名和本次实现差异；它不是整棵来源树与目标树的长期差异，也不声称所有显示行都是本次新增适配。
本批没有历史改写；依赖 gitlink 在总记录单列，不混进源码适配。原验收只适用于总记录列出的原节点候选。

## 已审说明

以下保留原证据文字；其中依赖 SHA 属于原运行，新依赖身份见下文与总记录。

- ` Preserve DeckShell layout, DDM guards, external-lock and late-DDE lifetime protections, installed WaylibShared package names and QML URI; integrate source deltas and only the explicitly approved XML/contract inputs. `

保留/映射路径：` compositor/src/greeter/greeterproxy.cpp `、` compositor/src/greeter/sessionmodel.cpp `、` compositor/src/greeter/sessionmodel.h `、` compositor/src/greeter/usermodel.cpp `、` compositor/src/greeter/usermodel.h `、` compositor/src/plugins/lockscreen/qml/SessionList.qml `。
排除路径：无。

## 逐路径取舍与实际差异

### ` compositor/src/greeter/greeterproxy.cpp ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/87e63ff43cd5dec5e56d9402572c4a2f807c8244/parent-review.json`。
- 来源路径：` src/greeter/greeterproxy.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 30ff777fafd7f99dd9939bb70361560617a7978c ` → ` 87e63ff43cd5dec5e56d9402572c4a2f807c8244 `。
- 原目标增量端点：` e658967b3e54597e94fd47aa2e595746a3d71536 ` → ` eb1eee7831d6b0afe85b03eda2bf5ceba63dea48 `。
- 本次目标：` e658967b3e54597e94fd47aa2e595746a3d71536 ` → ` eb1eee7831d6b0afe85b03eda2bf5ceba63dea48 `。
- 目标文件项（mode/type/blob）：` 100644 blob 848356bba0e6a19bba2b9f8ea2f29c7b3f652a1b ` → ` 100644 blob 482ebf5550357a637fec898f8e106dde33818fce `。
- 来源文件项 ` src/greeter/greeterproxy.cpp `：` 100644 blob 40eb8a19efcf507dd62b0e5531921b58e9366df4 ` → ` 100644 blob b56e357d3dd8466056e62b0d5b33f08fa6a10af8 `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,28 +1,28 @@
-@@ -246,2 +245,0 @@ void GreeterProxy::login(const QString &user, const QString &password, const int
+@@ -262,2 +261,0 @@ void GreeterProxy::login(const QString &user, const QString &password, const int
 -    DDM::Session::Type type =
 -        static_cast<DDM::Session::Type>(sessionModel()->data(index, SessionModel::TypeRole).toInt());
-@@ -249,3 +247,2 @@ void GreeterProxy::login(const QString &user, const QString &password, const int
+@@ -265,3 +263,2 @@ void GreeterProxy::login(const QString &user, const QString &password, const int
 -    qCInfo(lcTlGreeter) << "Logging user" << user << "in with" << type << "session" << name;
 -    DDM::Session session(type, name);
 -    SocketWriter(m_socket) << quint32(GreeterMessages::Login) << user << password << session;
 +    qCInfo(lcTlGreeter) << "Logging user" << user << "in with session" << name;
 +    SocketWriter(m_socket) << quint32(GreeterMessages::Login) << user << password << name;
-@@ -468,0 +466,2 @@ void GreeterProxy::readyRead()
+@@ -485,0 +483,2 @@ void GreeterProxy::readyRead()
 +        input.startTransaction();
 +
-@@ -470 +469 @@ void GreeterProxy::readyRead()
+@@ -487 +486 @@ void GreeterProxy::readyRead()
 -        quint32 message;
 +        quint32 message = 0;
-@@ -479 +478 @@ void GreeterProxy::readyRead()
+@@ -496 +495 @@ void GreeterProxy::readyRead()
 -            quint32 capabilities;
 +            quint32 capabilities = 0;
-@@ -480,0 +480,2 @@ void GreeterProxy::readyRead()
+@@ -497,0 +497,2 @@ void GreeterProxy::readyRead()
 +            if (!input.commitTransaction())
 +                return;
-@@ -500,0 +502,2 @@ void GreeterProxy::readyRead()
+@@ -517,0 +519,2 @@ void GreeterProxy::readyRead()
 +            if (!input.commitTransaction())
 +                return;
-@@ -504,0 +508,22 @@ void GreeterProxy::readyRead()
+@@ -521,0 +525,22 @@ void GreeterProxy::readyRead()
 +        case DaemonMessages::LastLogin: {
 +            qCDebug(lcTlGreeter) << "Message received from daemon: LastLogin";
 +
@@ -45,28 +45,28 @@
 +
 +            sessionModel()->setSessionDirs(waylandSessionDirs, x11SessionDirs);
 +        } break;
-@@ -507,0 +533,2 @@ void GreeterProxy::readyRead()
+@@ -524,0 +550,2 @@ void GreeterProxy::readyRead()
 +            if (!input.commitTransaction())
 +                return;
-@@ -515,0 +543,2 @@ void GreeterProxy::readyRead()
+@@ -532,0 +560,2 @@ void GreeterProxy::readyRead()
 +            if (!input.commitTransaction())
 +                return;
-@@ -520,0 +550,3 @@ void GreeterProxy::readyRead()
+@@ -537,0 +567,3 @@ void GreeterProxy::readyRead()
 +            if (!input.commitTransaction())
 +                return;
 +
-@@ -525,0 +558,3 @@ void GreeterProxy::readyRead()
+@@ -542,0 +575,3 @@ void GreeterProxy::readyRead()
 +            if (!input.commitTransaction())
 +                return;
 +
-@@ -535,0 +571,2 @@ void GreeterProxy::readyRead()
+@@ -552,0 +588,2 @@ void GreeterProxy::readyRead()
 +            if (!input.commitTransaction())
 +                return;
-@@ -568,0 +606,2 @@ void GreeterProxy::readyRead()
+@@ -585,0 +623,2 @@ void GreeterProxy::readyRead()
 +            if (!input.commitTransaction())
 +                return;
-@@ -618,0 +658,2 @@ void GreeterProxy::readyRead()
+@@ -635,0 +675,2 @@ void GreeterProxy::readyRead()
 +            if (!input.commitTransaction())
 +                return;
-@@ -619,0 +661 @@ void GreeterProxy::readyRead()
+@@ -636,0 +678 @@ void GreeterProxy::readyRead()
 +            return;
```


### ` compositor/src/greeter/sessionmodel.cpp ` / modified

- 原审核理由：` Reviewed three-way resolution preserving local package, runtime and regression integration. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/87e63ff43cd5dec5e56d9402572c4a2f807c8244/parent-review.json`。
- 来源路径：` src/greeter/sessionmodel.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 30ff777fafd7f99dd9939bb70361560617a7978c ` → ` 87e63ff43cd5dec5e56d9402572c4a2f807c8244 `。
- 原目标增量端点：` e658967b3e54597e94fd47aa2e595746a3d71536 ` → ` eb1eee7831d6b0afe85b03eda2bf5ceba63dea48 `。
- 本次目标：` e658967b3e54597e94fd47aa2e595746a3d71536 ` → ` eb1eee7831d6b0afe85b03eda2bf5ceba63dea48 `。
- 目标文件项（mode/type/blob）：` 100644 blob a32c928aab1aed7bea53b1781ad848b5ec0acd10 ` → ` 100644 blob c33966cc97d3be707cebf3305351d1792f0f37a0 `。
- 来源文件项 ` src/greeter/sessionmodel.cpp `：` 100644 blob dfb88bbd61748e397d921cce5153c929452c8411 ` → ` 100644 blob c33966cc97d3be707cebf3305351d1792f0f37a0 `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,5 +1,5 @@
 @@ -24 +24 @@
--#include <Configuration.h>
+-#include <ddm/common/Configuration.h>
 +#include <DDesktopEntry>
 @@ -25,0 +26 @@
 +#include <QDir>
```


### ` compositor/src/greeter/sessionmodel.h ` / modified

- 原审核理由：` Reviewed three-way resolution preserving local package, runtime and regression integration. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/87e63ff43cd5dec5e56d9402572c4a2f807c8244/parent-review.json`。
- 来源路径：` src/greeter/sessionmodel.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 30ff777fafd7f99dd9939bb70361560617a7978c ` → ` 87e63ff43cd5dec5e56d9402572c4a2f807c8244 `。
- 原目标增量端点：` e658967b3e54597e94fd47aa2e595746a3d71536 ` → ` eb1eee7831d6b0afe85b03eda2bf5ceba63dea48 `。
- 本次目标：` e658967b3e54597e94fd47aa2e595746a3d71536 ` → ` eb1eee7831d6b0afe85b03eda2bf5ceba63dea48 `。
- 目标文件项（mode/type/blob）：` 100644 blob b4c6c0cf3a11f25dc24a1240c125c0e6050fb88d ` → ` 100644 blob 11703582d950a063b77d3646506e6b101583ecb7 `。
- 来源文件项 ` src/greeter/sessionmodel.h `：` 100644 blob c992b1ccd5f80bffdfa4861f8ff8c3f61f5b24dc ` → ` 100644 blob 11703582d950a063b77d3646506e6b101583ecb7 `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,5 +1,5 @@
 @@ -24,2 +23,0 @@
--#include <Session.h>
+-#include <ddm/common/Session.h>
 -
 @@ -29,0 +28,2 @@
 +class QFileSystemWatcher;
```


### ` compositor/src/greeter/usermodel.cpp ` / modified

- 原审核理由：` Reviewed three-way resolution preserving local package, runtime and regression integration. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/87e63ff43cd5dec5e56d9402572c4a2f807c8244/parent-review.json`。
- 来源路径：` src/greeter/usermodel.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 30ff777fafd7f99dd9939bb70361560617a7978c ` → ` 87e63ff43cd5dec5e56d9402572c4a2f807c8244 `。
- 原目标增量端点：` e658967b3e54597e94fd47aa2e595746a3d71536 ` → ` eb1eee7831d6b0afe85b03eda2bf5ceba63dea48 `。
- 本次目标：` e658967b3e54597e94fd47aa2e595746a3d71536 ` → ` eb1eee7831d6b0afe85b03eda2bf5ceba63dea48 `。
- 目标文件项（mode/type/blob）：` 100644 blob 69c14501662866eb8576e6b052e5e46580d21fff ` → ` 100644 blob 7ba837e479dc02d0d4ded94aeaf9ca3241ba9f7c `。
- 来源文件项 ` src/greeter/usermodel.cpp `：` 100644 blob 10b0ff1a49ef960eedbcf9bc5d30bba43148cd49 ` → ` 100644 blob 7ba837e479dc02d0d4ded94aeaf9ca3241ba9f7c `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,5 +1,5 @@
 @@ -27,2 +26,0 @@
--#include <Configuration.h>
+-#include <ddm/common/Configuration.h>
 -
 @@ -45 +42,0 @@
 -using namespace DDM;
```


### ` compositor/src/greeter/usermodel.h ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/87e63ff43cd5dec5e56d9402572c4a2f807c8244/parent-review.json`。
- 来源路径：` src/greeter/usermodel.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 30ff777fafd7f99dd9939bb70361560617a7978c ` → ` 87e63ff43cd5dec5e56d9402572c4a2f807c8244 `。
- 原目标增量端点：` e658967b3e54597e94fd47aa2e595746a3d71536 ` → ` eb1eee7831d6b0afe85b03eda2bf5ceba63dea48 `。
- 本次目标：` e658967b3e54597e94fd47aa2e595746a3d71536 ` → ` eb1eee7831d6b0afe85b03eda2bf5ceba63dea48 `。
- 目标文件项（mode/type/blob）：` 100644 blob 194d76799fa2f94a172a09f8710b82d02ded6dab ` → ` 100644 blob 22da5211480b93302d5ab0010d0363c43c08ee81 `。
- 来源文件项 ` src/greeter/usermodel.h `：` 100644 blob 194d76799fa2f94a172a09f8710b82d02ded6dab ` → ` 100644 blob 22da5211480b93302d5ab0010d0363c43c08ee81 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

### ` compositor/src/plugins/lockscreen/qml/SessionList.qml ` / modified

- 原审核理由：` Apply the exact source delta at its canonical path, preserving nonconflicting local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/87e63ff43cd5dec5e56d9402572c4a2f807c8244/parent-review.json`。
- 来源路径：` src/plugins/lockscreen/qml/SessionList.qml `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 30ff777fafd7f99dd9939bb70361560617a7978c ` → ` 87e63ff43cd5dec5e56d9402572c4a2f807c8244 `。
- 原目标增量端点：` e658967b3e54597e94fd47aa2e595746a3d71536 ` → ` eb1eee7831d6b0afe85b03eda2bf5ceba63dea48 `。
- 本次目标：` e658967b3e54597e94fd47aa2e595746a3d71536 ` → ` eb1eee7831d6b0afe85b03eda2bf5ceba63dea48 `。
- 目标文件项（mode/type/blob）：` 100644 blob 68db8cada8d8e4a7832b387a3d04cd0076606751 ` → ` 100644 blob 4cf242cbe7eb62ff2e13a3994eb408307a58957f `。
- 来源文件项 ` src/plugins/lockscreen/qml/SessionList.qml `：` 100644 blob 4efc871463dd5d89cb2c726613f176531aa84616 ` → ` 100644 blob a876ff2c9852973bd39ee59434812bed068ebe68 `。
- 两侧本次增量相同；既有本地差异的保留不被计作本次新增 delta。文件身份与审核理由仍如上。

- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 3b05a9d59d14beded8475ae755ff2b7c9c7f9d36 ` → ` 3b05a9d59d14beded8475ae755ff2b7c9c7f9d36 `。

## 原工件定位

- mapped_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/87e63ff43cd5dec5e56d9402572c4a2f807c8244/parent-mapped-source.patch`。
- root_source_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/87e63ff43cd5dec5e56d9402572c4a2f807c8244/parent-root-source.patch`。
- adaptation_patch：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/inputs/87e63ff43cd5dec5e56d9402572c4a2f807c8244/parent.patch`。
- target_diff：外层历史资料：`.helloagents/plans/20261110_treeland_f342a5b6_to_9dcaef2e_local_sync/evidence/N10-attempt-7/commits/87e63ff43cd5dec5e56d9402572c4a2f807c8244/parent-target.diff`。
