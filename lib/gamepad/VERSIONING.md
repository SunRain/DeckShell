# 版本与兼容性策略（SemVer）

本文定义 **DeckShellGamepad（Linux-only / core-only）** 的版本号、ABI/SONAME、对外稳定 API 边界与变更日志策略。

> 发行版交付以 **shared** 为准（`BUILD_SHARED_LIBS=ON`）。

## 1) 适用范围

- 本策略适用于 **core**（C++ / `Qt6::Core` + `libudev`）。
- `-qml` / `-treeland` 属于 P1：未来可复用本策略，但**不在本次对外承诺范围**内。

## 2) 版本号规则

采用语义化版本（SemVer）：`MAJOR.MINOR.PATCH`。

- **MAJOR**：破坏性变更（Breaking Changes）。
- **MINOR**：向后兼容的功能新增（Added/Changed 但不破坏）。
- **PATCH**：向后兼容的缺陷修复（Fixed）。

## 3) 共享库 ABI/SONAME（发行版以 shared 为准）

发行版推荐构建：

```bash
cmake -S "DeckShellGamepad-private-work" -B "build" \
  -DBUILD_SHARED_LIBS=ON
```

- SONAME：`libdeckshell-gamepad.so.<SOVERSION>`
- 规则：
  - `SOVERSION` 与 `MAJOR` 对齐（ABI break → 同步 bump）。
  - 仅做向后兼容的新增/修复（MINOR/PATCH）时，保持 `SOVERSION` 不变。

> 说明：ABI “是否兼容”以发行版的 ELF/SONAME 语义为准；在相同 `Qt6` major 与兼容的 toolchain/C++ ABI 前提下，`1.x` 目标是尽量保持 ABI 稳定。

## 4) 对外 API 分层（稳定 vs internal vs legacy）

### 4.1 Stable（对外承诺稳定）

承诺：
- **同一 MAJOR 内**保持 source-level 兼容；
- 发行版共享库场景下，**同一 MAJOR 内尽量保持 ABI 兼容**（见第 3 节）。

Stable API（P0）覆盖：
- `deckshell::deckgamepad::DeckGamepadService`（公开方法与 signals）
- 错误/诊断契约：
  - `DeckGamepadError` / `DeckGamepadErrorCode` / `DeckGamepadErrorKind` / `DeckGamepadDeviceAvailability`
  - `DeckGamepadDiagnostic` + `DeckGamepadDiagnosticKey::*`（既有 key 字符串值不变）
  - `DeckGamepadDiagnostic.suggestedActions` 中的 actionId：**只增不改**（删除/重命名视为破坏性变更）
- 事件与基础枚举：
  - `DeckGamepadButtonEvent` / `DeckGamepadAxisEvent` / `DeckGamepadHatEvent`
  - `GamepadButton` / `GamepadAxis` / `GamepadHatMask`
- 运行期配置：
  - `DeckGamepadRuntimeConfig`（字段语义稳定；允许新增字段，既有字段不删除不改语义）

稳定性边界（重要）：
- `DeckGamepadDiagnostic.details` 为**可变上下文**（用于日志/排障），不作为稳定接口承诺；自动化断言应使用 `diagnostic.key`。

### 4.2 Public-but-unstable（可用但不承诺稳定）

以下内容即使被安装进 `-dev`（头文件可见），也**不建议第三方直接依赖其符号**（实现细节可能在 MINOR 版本中重构）：
- `backend/*`
- `providers/*`
- `mapping/*`、`extras/*` 中偏实现/策略细节的类型与行为

如第三方确有需要，建议优先通过 `DeckGamepadService` 的转发/配置能力达成目的，或在上游提出需求将其纳入 Stable 层。

### 4.3 Legacy / Deprecated（兼容期）

- `deckshell::gamepad` 命名空间：兼容别名（`[[deprecated("use deckshell::deckgamepad")]]`）
  - 仅用于迁移期（编译会产生 deprecation warning）
  - 移除策略：**仅在 MAJOR 升级时移除**（不会在 `1.x` 中移除）

- `DeckGamepadRuntimeConfig.enableLegacyDeckShellPaths`：兼容旧 DeckShell 路径回退开关
  - 独立第三方应用推荐显式关闭（避免误读 `~/.config/DeckShell/*`）

## 5) 破坏性变更（Breaking Change）判定规则

以下任一发生 → bump `MAJOR`（并同步 bump `SOVERSION`）：

- Stable API 删除/重命名/改签名/改变既有语义
- 稳定 enum 的既有取值语义变更（新增取值不算破坏）
- `DeckGamepadDiagnosticKey::*` 的既有 key 字符串变更
- 稳定 actionId 的重命名/删除
- install 布局导致 `find_package(DeckShellGamepad CONFIG REQUIRED)` 失效（包名/target/路径的破坏性变化）

## 6) 变更日志（Changelog）策略

- 变更日志文件：`DeckShellGamepad-private-work/CHANGELOG.md`
- 格式：Keep a Changelog（Added/Changed/Fixed/Deprecated/Removed/Security）
- 工作流：
  1. 每个 PR 在 `[Unreleased]` 下补充条目（只写对外可感知内容）
  2. 发布时：将 Unreleased 条目移动到对应版本小节并补上日期
  3. 同步更新 `CMakeLists.txt` 中的 `PROJECT_VERSION`，并打 tag

