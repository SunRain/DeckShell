# N11 独立修复：最后一个快捷键 action 解绑后清理空 key

本提交仅修复 `ShortcutController::registerKey()` 安装的解绑回调：移除指定 action 后，只有该 key 的 action 集合已空时才删除外层 key。同 key 的其它 action 不受影响；原 Session-isolation 测试断言不变。

## 原因和真实失败

N11 的 65 个来源提交已完成逐提交回放；此前独立判空修复让完整 `test_session_isolation` 越过 socket-owned `ownsClient(nullptr)` 的原崩溃后，两种配置都停在：

```text
FAIL: inactive upsert followed by unbind leaves no stale binding
Actual (m_context.result): 1
Expected (0): 0
```

测试向后台 B 的 F10 绑定发送改名 upsert，然后解绑新名称，要求 A 的 F9 仍匹配、B 的 F10 不再匹配。原 deleter 只移除内层 action，留下空外层 key；`matchesShortcut()` 按外层 key 的存在性判断，因此空 key 仍吞掉输入。

修复前的生产实现和 C 客户端断言与冻结来源 head 的对应文件字节一致；本提交后的原客户端断言继续保持该字节一致。该归因不等于独立运行或复现了纯 Treeland 的 CI 环境。

## 明确批准的窄修

用户批准按 PRD §9 **另作独立修复提交**，仅清理最后一个 action 解绑后的空 key，保留同 key 的其它 action和原测试断言，不改写此前已冻结判空提交。

生产增量只有下面三行，位置在既有 action 删除后、既有 `m_actionCombinedMap.remove(action)` 前：

```cpp
if (m_keyMap[combined].isEmpty()) {
    m_keyMap.remove(combined);
}
```

不改 `matchesShortcut()`、dispatch、upsert、名称路由、action-to-key 规则、手势、协议请求/事件、XML、C/R 内容或两层 gitlink。

## 与已有来源和修复的关系

- 来源范围：`(1f8c2a658b4b4e868e0650f9890c5e752fd1b839..77f885c8dbeb0e0e0bebdafdee02eadb1d150439]`，65 项来源映射不变。
- 直接父 P：`da94bafea5d130bdee98e2c7854e2b352c7d5224`，原判空传播提交保持原样。
- 保留 C：`780ae6e53d52483d17f14d40fa44c8d67d5874fc`，原判空源码与独立说明的提交保持原样。
- 保留 R：`b79b9b38a473ca57f5b54892280dfad4f25f8e42`。
- 独立修复标识：`N11-shortcut-last-action-unbind-1`；不带来源或协议 companion trailer。

这是一个相邻非 merge **P-only** 修复。为避免原记录工具仅支持一次 P/C 修复而迫使伪造 C 提交，本批私有工具显式记录 `parent_tail_repair`，保留原 `local_fix` 对象、approval 和 manifest；新报告、源码/消息/gitlink检查及 `finish` 都重新核验该尾部。

## 验证依据与验收边界

提交前用原候选的真实 `libdeckcompositor.so` 构建并运行 artifact-only 控制器 probe，五个边界用例均真实失败在解绑或 clear 后仍匹配空 key：最后 action、同 key 多 action 的最后解绑、改名 upsert 后解绑、重复/未知解绑、clear。原日志及源码保留，不计为新候选 PASS。

新候选将以相同公共 API 和断言验证修复，并运行正常/关闭 XWayland 的完整未过滤 Session-isolation 和 compositor CTest，以及 fresh C 默认完整 build/install、真实消费链、协议和 runtime 检查。所有结果绑定新候选，旧 PASS 不重新绑定。

完整结果保存在外层方案的 `evidence/N11-local-fix-2/`；本说明记录提交时的原因、批准范围和验收要求，不预先宣称整批接受。除原已批准的真实 `test_drm` 环境不足 SKIP 外，任何失败、额外 SKIP、过滤或未执行都继续阻断；只有接受后才执行专用 refs CAS 和整批 `finish`。

外层方案标识：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/plan.md`。
