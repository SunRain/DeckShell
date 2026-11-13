# protocol-companion：chore(protocol): 同步 remote-subsurface 配套快照

- 类型：protocol-companion；不属于普通 Treeland 来源映射。
- 原直接父提交：` 9927c8830e7118ddc0c23a9fcf09a99c48ec2917 `；原目标：` ac8f4b1928105fdcfc809c8cf11cbe65c12ecccd `。
- 本仓直接父提交：` 9927c8830e7118ddc0c23a9fcf09a99c48ec2917 `；本仓目标：` ac8f4b1928105fdcfc809c8cf11cbe65c12ecccd `。
- [本仓总记录](../summary.md#entry-66)。

## 原依据与取舍

- ` 协议来源 578263755cb80b56f2e13fde34da1c294418e608:wine/treeland-remote-subsurface-unstable-v1.xml `
- ` 配对实现来源 77f885c8dbeb0e0e0bebdafdee02eadb1d150439 `
- ` 按原协议配对更新受控快照/配对元数据及依赖引用；不计为普通来源回放。 `
- 外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/manifest.json#protocol_update`
- 外层历史资料：`.helloagents/plans/20261111_treeland_1f8c2a65_to_77f885c8_local_sync/evidence/N11-local-fix-3/protocol/parent-target.diff`

原授权说明适用于其列出的修复范围；下列逐路径增量来自原 Git 对象；整理后的普通文件不变，派生 gitlink 按映射核对。

## ` 3rdparty/waylib-shared `

- mode/type/blob：` 160000 commit 8b304b873e688cd6f72554503df165b7a809de6f ` → ` 160000 commit a0f86a62a8cf3038e306ce191f5ded1a09b58fed `。

```diff
diff --git a/3rdparty/waylib-shared b/3rdparty/waylib-shared
index 8b304b873..a0f86a62a 160000
--- a/3rdparty/waylib-shared
+++ b/3rdparty/waylib-shared
@@ -1 +1 @@
-Subproject commit 8b304b873e688cd6f72554503df165b7a809de6f
+Subproject commit a0f86a62a8cf3038e306ce191f5ded1a09b58fed
```


原记录不等于本次重新构建/测试；未把后续补档提交作为已接受产品候选。
