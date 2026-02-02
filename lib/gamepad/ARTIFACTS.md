# 发布产物清单（Linux-only / core-only）

本文件用于明确 “DeckShellGamepad（core）” 在安装后应包含哪些文件，以及发行版拆包（`core/-dev`）的建议与第三方 `find_package` 消费验证方式。

> 注：`-qml` / `-treeland` 属于 P1，本次仅覆盖 core。

## 1) 对外 CMake 包信息

- 包名：`DeckShellGamepad`（CONFIG 包）
- 目标：`DeckShell::deckshell-gamepad`
- 依赖：
  - `Qt6::Core`
  - `libudev`（通过 `pkg-config`：`libudev`）
  - （可选）`Qt6::DBus`：当构建环境可用时，会启用 logind 支持并在 `DeckShellGamepadConfig.cmake` 中声明依赖

## 2) 安装布局（`CMAKE_INSTALL_PREFIX=<prefix>`）

### 2.1 core（运行时）

必需数据文件（运行时用于设备映射基线）：
- `<prefix>/share/DeckShellGamepad/gamecontrollerdb.txt`

若以共享库发布（推荐用于发行版拆 `core/-dev`）：
- `<prefix>/lib/libdeckshell-gamepad.so.1.0.0`
- `<prefix>/lib/libdeckshell-gamepad.so.1`
- （可选）`<prefix>/lib/libdeckshell-gamepad.so`（部分发行版会放在 `-dev`）

### 2.2 -dev（开发文件）

头文件（对外 API，已过滤 `*_p.h`）：
- `<prefix>/include/deckshell/deckgamepad/**/*.h`

CMake 导出（第三方 `find_package` 所需）：
- `<prefix>/lib/cmake/DeckShellGamepad/DeckShellGamepadConfig.cmake`
- `<prefix>/lib/cmake/DeckShellGamepad/DeckShellGamepadConfigVersion.cmake`
- `<prefix>/lib/cmake/DeckShellGamepad/DeckShellGamepadTargets*.cmake`

若以静态库发布（默认 `BUILD_SHARED_LIBS=OFF`）：
- `<prefix>/lib/libdeckshell-gamepad.a`

## 3) 拆包建议（发行版 / 系统包）

推荐（共享库构建，便于拆分与复用）：
- `deckshell-gamepad`（core）：共享库运行时文件（`.so.<soname>` + `.so.<major>`）+ `gamecontrollerdb.txt`
- `deckshell-gamepad-dev`：头文件 + CMake 导出 +（链接用的 `.so` symlink / 静态库 `.a`）

说明：
- 若只提供静态库（默认构建方式），`core/-dev` 的拆分收益较低；可选择不拆包，或让 `-dev` 依赖 `core` 并携带 `.a` 与开发文件。
- 本项目的 `-qml` / `-treeland` 拆分（依赖 core + Qt6::Qml/Gui / Wayland）按 P1 规划推进。

## 4) 第三方 `find_package` 消费验证（core-only）

验证目标：一个完全独立的 CMake 工程，能通过 `find_package(DeckShellGamepad CONFIG REQUIRED)` 构建并运行。

参考工程：`tests/smoke/gamepad_consumer/`。

最小步骤（静态 / 共享任选其一）：

```bash
cmake -S "DeckShellGamepad-private-work" -B "/tmp/deckgamepad-build" -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_TESTING=OFF -DDECKGAMEPAD_BUILD_TESTS=OFF \
  -DBUILD_GAMEPAD_EXAMPLES=OFF \
  -DDECKGAMEPAD_BUILD_QML_MODULE=OFF -DDECKGAMEPAD_BUILD_TREELAND_CLIENT=OFF \
  -DBUILD_SHARED_LIBS=ON \
  -DCMAKE_INSTALL_PREFIX="/tmp/deckgamepad-install"
cmake --build "/tmp/deckgamepad-build" --target install --parallel

cmake -S "DeckShellGamepad-private-work/tests/smoke/gamepad_consumer" -B "/tmp/deckgamepad-consumer" -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="/tmp/deckgamepad-install"
cmake --build "/tmp/deckgamepad-consumer" --parallel

LD_LIBRARY_PATH="/tmp/deckgamepad-install/lib:${LD_LIBRARY_PATH}" \
  "/tmp/deckgamepad-consumer/gamepad_consumer"
```

## 5) 合规提示

- `share/DeckShellGamepad/gamecontrollerdb.txt` 为第三方数据文件，来源/版本/许可追踪见 `THIRD_PARTY.md`（当前标记为 TBD）。
