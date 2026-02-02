# 第三方与依赖说明

本仓库自身包含/引用的第三方内容与依赖项说明如下（用于合规追溯；详情以对应上游为准）：

## 1. vendored 协议文件

- `protocols/treeland-gamepad-v1.xml`
  - 许可证：MIT（以文件内 SPDX 为准）
  - 说明：仅在构建 `deckshell-gamepad-treeland`（P1，可选）时使用/安装

## 2. 数据文件

- `data/gamecontrollerdb.txt`
  - 来源：SDL GameController DB
    - 上游仓库：https://github.com/gabomdq/SDL_GameControllerDB
    - 上游版本：TBD（发布前需补齐 commit/tag/date）
  - 许可证：TBD（发布前需补齐；以 SDL_GameControllerDB 上游声明为准）
  - 本仓库用途：用于 evdev 设备的“标准化映射”（仅加载/使用 Linux platform 条目）
  - 打包/分发注意：
    - 本文件会被安装到 `${CMAKE_INSTALL_DATADIR}/DeckShellGamepad/gamecontrollerdb.txt`
    - 对外发布前建议把“上游版本 + 许可文本/引用方式”落盘到本文件（避免合规追溯困难）

## 3. 构建/运行依赖（未 vendoring）

- Qt6（Core；示例可能依赖 Widgets）
- libudev（Linux 设备枚举/热插拔）
- wayland-client / wayland-scanner（仅在构建 `deckshell-gamepad-treeland` 时需要）
