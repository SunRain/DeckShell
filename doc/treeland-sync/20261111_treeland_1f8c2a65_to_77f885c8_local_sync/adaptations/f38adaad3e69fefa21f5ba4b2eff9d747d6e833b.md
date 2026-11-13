# P / DeckShell 适配：refactor(output): keep configuration replies with their requesting protocol

- Treeland 来源：` 34012ca473c6c590e0aca32c68ea58837d9b7a97 `。
- 本仓目标：` f38adaad3e69fefa21f5ba4b2eff9d747d6e833b `。
- 节点：N11；action=adapted。
- [本仓总记录](../summary.md#entry-53)。

## 比较口径

比较来源唯一父提交 → 来源提交，与原目标唯一父提交 → 原目标提交的逐路径增量。
零上下文补丁对照会呈现基线位置、既有命名和本次实现差异；它不是整棵来源树与目标树的长期差异，也不声称所有显示行都是本次新增适配。
本批没有历史改写；依赖 gitlink 在总记录单列，不混进源码适配。原验收只适用于总记录列出的原节点候选。

## 已审说明

以下保留原证据文字；其中依赖 SHA 属于原运行，新依赖身份见下文与总记录。

- ` Apply the reviewed canonical source projection and necessary authorized local integration; preserve WaylibShared package identity, namespace, XML and regression semantics. `

保留/映射路径：` compositor/src/output/outputmanager.cpp `、` compositor/src/output/outputmanager.h `。
排除路径：无。

## 逐路径取舍与实际差异

### ` compositor/src/output/outputmanager.cpp ` / modified

- 原审核理由：` Integrate the canonical source delta, preserving nonconflicting accepted local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/inputs/34012ca473c6c590e0aca32c68ea58837d9b7a97/parent-review.json`。
- 来源路径：` src/output/outputmanager.cpp `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 6f3ee9dab17a0bb8edc406a20ea04a26726f8f05 ` → ` 34012ca473c6c590e0aca32c68ea58837d9b7a97 `。
- 原目标增量端点：` 380393d038ffef803dc086ffcd3f90fd1342d071 ` → ` f38adaad3e69fefa21f5ba4b2eff9d747d6e833b `。
- 本次目标：` 380393d038ffef803dc086ffcd3f90fd1342d071 ` → ` f38adaad3e69fefa21f5ba4b2eff9d747d6e833b `。
- 目标文件项（mode/type/blob）：` 100644 blob 0f1dee8b94be696c4b0d580e546317eb0accc734 ` → ` 100644 blob 9b96dcaef8d6b9031402945b547990b02afecdeb `。
- 来源文件项 ` src/output/outputmanager.cpp `：` 100644 blob 5554cbd88a1fb27d068a08cac4194a8ab9b98ae0 ` → ` 100644 blob 3e1f7984af5f695d5ec73334fcde3004121c9217 `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -1,4 +1,4 @@
-@@ -135,4 +135,4 @@ void OutputManager::setOutputManagementProtocol(WOutputManagerV1 *manager)
+@@ -136,4 +136,4 @@ void OutputManager::setOutputManagementProtocol(WOutputManagerV1 *manager)
 -    connect(m_outputManagementProtocol,
 -            &WOutputManagerV1::requestTestOrApply,
 -            this,
@@ -7,51 +7,51 @@
 +            [this, manager](wlr_output_configuration_v1 *config, bool onlyTest) {
 +                testOrApplyConfiguration(manager, config, onlyTest);
 +            });
-@@ -1353 +1353,2 @@ void OutputManager::setPowerMode(wlr_output_power_v1_set_mode_event *event)
+@@ -1365 +1365,2 @@ void OutputManager::setPowerMode(wlr_output_power_v1_set_mode_event *event)
 -void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config,
 +void OutputManager::testOrApplyConfiguration(WOutputManagerV1 *protocol,
 +                                             wlr_output_configuration_v1 *config,
-@@ -1356 +1357 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
+@@ -1368 +1369 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
 -    QList<WOutputState> states = m_outputManagementProtocol->stateListPending(config);
 +    QList<WOutputState> states = protocol->stateListPending(config);
-@@ -1448 +1449 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
+@@ -1460 +1461 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
 -        m_outputManagementProtocol->sendResult(config, ok);
 +        protocol->sendTestResult(config, ok);
-@@ -1453 +1454,2 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
+@@ -1465 +1466,2 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
 -        m_outputManagementProtocol->sendResult(m_pendingOutputConfig.config, false);
 +        if (m_pendingOutputConfig.protocol)
 +            m_pendingOutputConfig.protocol->sendResult(m_pendingOutputConfig.config, false);
-@@ -1456,0 +1459 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
+@@ -1468,0 +1471 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
 +    m_pendingOutputConfig.protocol = protocol;
-@@ -1465 +1468 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
+@@ -1477 +1480 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
 -    const auto answerOnce = [this, config](bool ok) {
 +    const auto answerOnce = [this, config, protocol](bool ok) {
-@@ -1470 +1473 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
+@@ -1482 +1485 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
 -        m_outputManagementProtocol->sendResult(config, ok);
 +        protocol->sendResult(config, ok);
-@@ -1581,0 +1585 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
+@@ -1593,0 +1597 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
 +        const auto generation = m_sessionGeneration;
-@@ -1587,0 +1592 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
+@@ -1599,0 +1604 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
 +             generation,
-@@ -1594 +1599 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
+@@ -1606 +1611 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
 -                if (!self) {
 +                if (!self)
-@@ -1596,2 +1601,4 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
+@@ -1608,2 +1613,4 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
 -                }
 -
 +                const bool currentRequest = self->m_sessionGeneration == generation
 +                    && self->m_pendingOutputConfig.config == pendingConfig;
 +                // Hardware commits still finish when their requesting Session
 +                // changes; always retire the shared output-group bookkeeping.
-@@ -1609 +1616,2 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
+@@ -1621 +1628,2 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
 -                    self->onOutputCommitFinished(pendingConfig, success);
 +                    if (currentRequest)
 +                        self->onOutputCommitFinished(pendingConfig, success);
-@@ -1628 +1636,2 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
+@@ -1640 +1648,2 @@ void OutputManager::testOrApplyConfiguration(wlr_output_configuration_v1 *config
 -                    self->onOutputCommitFinished(pendingConfig, false);
 +                    if (currentRequest)
 +                        self->onOutputCommitFinished(pendingConfig, false);
-@@ -1713 +1722,2 @@ void OutputManager::onOutputCommitFinished(wlr_output_configuration_v1 *config,
+@@ -1725 +1734,2 @@ void OutputManager::onOutputCommitFinished(wlr_output_configuration_v1 *config,
 -    m_outputManagementProtocol->sendResult(config, ok, m_pendingOutputConfig.states);
 +    if (m_pendingOutputConfig.protocol)
 +        m_pendingOutputConfig.protocol->sendResult(config, ok, m_pendingOutputConfig.states);
```


### ` compositor/src/output/outputmanager.h ` / modified

- 原审核理由：` Integrate the canonical source delta, preserving nonconflicting accepted local changes. `。
- 路径证明：外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/inputs/34012ca473c6c590e0aca32c68ea58837d9b7a97/parent-review.json`。
- 来源路径：` src/output/outputmanager.h `；无来源路径表示本地集成，不冒充上游修改。
- 来源增量端点：` 6f3ee9dab17a0bb8edc406a20ea04a26726f8f05 ` → ` 34012ca473c6c590e0aca32c68ea58837d9b7a97 `。
- 原目标增量端点：` 380393d038ffef803dc086ffcd3f90fd1342d071 ` → ` f38adaad3e69fefa21f5ba4b2eff9d747d6e833b `。
- 本次目标：` 380393d038ffef803dc086ffcd3f90fd1342d071 ` → ` f38adaad3e69fefa21f5ba4b2eff9d747d6e833b `。
- 目标文件项（mode/type/blob）：` 100644 blob 6c6e80a8e047b0195d3633685c061668487cc9a7 ` → ` 100644 blob 6bdd142988997947bd4d073d8c415c130736ff34 `。
- 来源文件项 ` src/output/outputmanager.h `：` 100644 blob 1cabaeeb9c2a9bf3abf2c769c012498a0a403a79 ` → ` 100644 blob 6f5579ff6a70bac9db746d320ce93e17c5e6af4a `。

两侧零上下文增量的文本对照（保留 hunk 位置；尾空格/Tab 显示为 ␠/⇥；不是可直接应用的纯适配补丁）：

```diff
--- 来源的本次增量
+++ 本仓的本次增量
@@ -6,5 +6,5 @@
 +                                  wlr_output_configuration_v1 *config, bool onlyTest);
 @@ -153,0 +156 @@ private:
 +    quint64 m_sessionGeneration = 0;
-@@ -177,0 +181 @@ private:
+@@ -178,0 +182 @@ private:
 +        QPointer<WAYLIB_SERVER_NAMESPACE::WOutputManagerV1> protocol;
```


- 依赖 ` 3rdparty/waylib-shared `：unchanged；` d2fd6828913037cc12954a29f1442f47de0a695f ` → ` d2fd6828913037cc12954a29f1442f47de0a695f `。

## 原工件定位

- mapped_source_patch：外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/commits/34012ca473c6c590e0aca32c68ea58837d9b7a97/parent-mapped-source.patch`。
- root_source_patch：外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/commits/34012ca473c6c590e0aca32c68ea58837d9b7a97/parent-root-source.patch`。
- adaptation_patch：外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/inputs/34012ca473c6c590e0aca32c68ea58837d9b7a97/parent.patch`。
- target_diff：外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/commits/34012ca473c6c590e0aca32c68ea58837d9b7a97/parent-target.diff`。
