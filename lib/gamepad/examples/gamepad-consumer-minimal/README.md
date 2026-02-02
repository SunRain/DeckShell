# gamepad-consumer-minimal

最小 consumer demo：仅使用 `core/` + `service/`（`DeckGamepadService`），用于公司内部复用接入基线验证。

## 1) 在本仓库内构建（推荐）

在 `libs/` 目录执行：

```bash
cmake -S DeckShellGamepad-private-work -B DeckShellGamepad-private-work/build -DBUILD_GAMEPAD_EXAMPLES=ON
cmake --build DeckShellGamepad-private-work/build -j
./DeckShellGamepad-private-work/build/examples/gamepad-consumer-minimal/gamepad-consumer-minimal --help
```

## 2) 作为独立 consumer 构建（install + find_package）

先安装库到本地前缀：

```bash
cmake -S DeckShellGamepad-private-work -B build-deckgamepad -DCMAKE_INSTALL_PREFIX="$PWD/_install" -DBUILD_GAMEPAD_EXAMPLES=OFF -DBUILD_TESTING=OFF
cmake --build build-deckgamepad -j
cmake --install build-deckgamepad
```

再构建本 demo：

```bash
cmake -S DeckShellGamepad-private-work/examples/gamepad-consumer-minimal -B build-consumer -DCMAKE_PREFIX_PATH="$PWD/_install"
cmake --build build-consumer -j
./build-consumer/gamepad-consumer-minimal --help
```

## 3) 运行与排障

- 默认会设置 `enableLegacyDeckShellPaths=false`（内部复用基线）。
- 如果 `start()` 失败或无事件，观察输出中的：
  - `lastErrorMessage`
  - `diagnosticKey` + `suggestedActions`

常见原因：
- `/dev/input/event*` 权限不足
- 非活动会话导致门控（默认 `ActiveSessionOnly`）

