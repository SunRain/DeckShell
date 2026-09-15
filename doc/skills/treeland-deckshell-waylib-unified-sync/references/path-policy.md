# DeckShell 路径策略引用

统一工具不复制或整体放宽 DeckShell 路径表。运行时读取指定 DeckShell 仓库中的 `doc/skills/treeland-deckshell-sync/references/path-policy.md` 第一个 fenced JSON，并冻结其绝对路径和 SHA-256；replay 重新核对该文件及源码 inventory，漂移阻断。

本统一模型仅有以下显式 owner 扩展：

- `qwlroots/**`、`waylib/**`、`wlroots/**` 进入 C 普通文件，保持路径；对 P 仍排除。
- `3rdparty/wlroots/**` 进入独立 R，去前缀；C 只记录固定同名 gitlink。
- C `.gitmodules`/R gitlink 是可复算的派生路径；C 根 `CMakeLists.txt` 仅接受显式结构适配，不成为普通 source owner。

P 的 mapped/root-owned/review-only 规则不变；review-only 按 policy_key 批准，unknown 继续阻断。两种 wlroots 根若变成文件、symlink 或来源 gitlink，不能猜测迁移；C `wlroots/` 必须普通目录。

明确授权的公共合同迁移可通过 `contract_migration` 逐文件批准必要的本地包配置、consumer 和 P 测试调用方及现有 `compositor/src/CMakeLists.txt` 运行时安装入口，以及已授权 scanner/协议迁移的 P 根 `CMakeLists.txt`、`qtwaylandscanner/CMakeLists.txt`、`qtwaylandscanner/qtwaylandscanner.cpp`、`protocols/compositor/CMakeLists.txt` 和 `protocols/compositor/xml/treeland-remote-subsurface-unstable-v1.xml`；具体范围及证明见 [迁移 schema](evidence-schema.md#显式公共合同迁移)。这些集成路径不改写来源 inventory，不变成普通 owner，也不允许把规范来源实现挪入兄弟文件；默认路径规则及 R 去前缀投影不变。

调用者另行批准 QML 导入修正时，仅允许把既有 `compositor/src/core/qml/PrelaunchSplash.qml` 精确加入对应来源的迁移集成路径，导入既定的 `WaylibShared.QuickSharedServer 1.0`；其他 QML 文件仍不获授权，普通 inventory 与目录所有权不变。

rename 两侧参与 owner 和审批；copy 只把 new 作为实际变更，old 保留关系。跨 owner 的删除/新增分别回放，不把 unchanged copy source 写成必需目标路径。

来源 `protocols/**/*.xml` 和实际 P `protocols/compositor/**/*.xml` 分别触发协议候选；信号不决定所有权，不授权扩展目标路径或自动替换 XML。完整矩阵见 [统一合同](unified-contract.md)。
