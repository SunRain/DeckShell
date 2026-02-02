# DeckShell Gamepad Library

Linux evdev-based gamepad driver library for DeckShell Compositor.

## 🎯 对外发布定位（Linux-only / core-only）

本库对外发布定位为 **Linux-only 的 Gamepad 基础库**；本次对外发布基线为 **仅 core（C++/Qt6::Core）**。

对外承诺（本次）：
- **支持平台**：Linux（evdev + libudev），Qt 6（Core）
- **稳定入口**：`DeckGamepadService`（唯一推荐长期依赖入口）
- **覆盖能力**：设备枚举/热插拔、button/axis/hat、SDL DB 映射、自定义映射/校准、（可选）rumble（FF_RUMBLE，best-effort）
- **不支持**：Windows XInput/DirectInput、macOS、浏览器标准 Gamepad API、系统级输入注入（uinput/seat）

后续补强（P1，不纳入本次稳定承诺）：
- QML 模块（`DeckShell.DeckGamepad`）
- Treeland Wayland client
- 蓝牙/2.4G 等连接方式的真机回归矩阵

## ⚠️ 已知限制（Beta/RC）

> 说明：本节面向“对外发布（Linux-only/core-only）”的已知边界与限制；每条限制应能在回归矩阵或设计边界中找到依据。

- **rumble/振动（FF_RUMBLE）为可选能力**：需要对 `/dev/input/event*` 具备写权限（`O_RDWR` + `EVIOCSFF`/`write(EV_FF)`）。在受限环境（只读 fd、或 FF 相关 ioctl/write 被拒绝）下，输入读取仍可用，但 `startVibration()` 会失败。
- **热插拔在受限环境可能退化为“周期 rescan”**：当 udev monitor/netlink 不可用时，会退化为 periodic rescan；热插拔的发现延迟取决于重试/扫描周期（见 `enableAutoRetryOpen` 与 backoff 配置）。
- **自动化集成测试依赖 `/dev/uinput`**：uinput/udev 相关集成/E2E 测试在无权限环境会 `SKIP`；对外发布前应在具备 `/dev/uinput` 的环境补齐门禁证据（或用等价真机矩阵覆盖风险）。

## 📜 来源和版本追踪

**原始来源**：
- **仓库**：waylib-shared (qwlroots)
- **Commit**：`01adb2350ef31f5a597c255d0f56d1ab04938d72`
- **作者**：SunRain <41245110@qq.com>
- **日期**：2025-10-18 11:00:51 +0800
- **提交信息**：qwlroots gamepad support

**移植到 DeckShell**：
- **移植日期**：2025-10-18
- **移植理由**：将底层游戏手柄驱动作为独立库集成到 DeckShell 项目，便于独立维护和优化
- **命名空间**：使用 `deckshell::deckgamepad` 命名空间（通过 `DECKGAMEPAD_USE_NAMESPACE` 宏）

## 📂 目录结构

```
<repo-root>/
├── README.md                   # 本文件（版本追踪和使用说明）
├── CMakeLists.txt              # 库主构建配置
├── src/                        # 核心库源代码
├── data/                       # 数据文件（SDL gamecontrollerdb）
├── protocols/                  # vendored Wayland 协议（treeland-gamepad-v1.xml）
├── tests/                      # 独立仓库自洽的测试与 smoke
└── examples/                   # 示例程序
```

> 说明：在 DeckShell 主仓库内通常作为 vendored 目录 `lib/gamepad/` 存在；抽离为独立项目时以上述 `<repo-root>` 为准。

## ✨ 功能特性

- ✅ **完整的 Linux evdev 驱动实现**（551 行 C++）
- ✅ **设备热插拔检测**（基于 udev）
- ✅ **标准按键映射**（Xbox/SDL2 兼容）
- ✅ **（可选）力反馈/振动支持**（FF_RUMBLE；需要设备与权限支持；参考 `src/backend/deckgamepadbackend.cpp`）
- ✅ **自定义死区和灵敏度调整**（m_customDeadzones, m_axisSensitivity）
- ✅ **多手柄支持**（最多 16 个设备）
- ✅ **完整的事件系统**（按钮、摇杆、HAT/D-pad）

## 🔧 依赖

### 必需
- **Qt 6.8+**（Core 模块）
- **libudev**（设备热插拔）
- **Linux kernel evdev**（输入事件接口）

### 可选（示例程序）
- **Qt 6.8+ Widgets**（gamepad-visualizer）

## 🚀 使用方法

### 构建矩阵（最小说明）

- **core（必选）**：`deckshell-gamepad`（Qt6::Core + libudev）
- **treeland client（P1，可选）**：`-DDECKGAMEPAD_BUILD_TREELAND_CLIENT=ON`（需要 wayland-client + wayland-scanner；默认使用 `protocols/treeland-gamepad-v1.xml`，可用 `TREELAND_GAMEPAD_PROTOCOL_XML` 覆盖）
- **QML 模块（P1，可选）**：`-DDECKGAMEPAD_BUILD_QML_MODULE=ON`（需要 Qt6::Qml + Qt6::Gui；安装到 `${CMAKE_INSTALL_QMLDIR}/DeckShell/DeckGamepad/`，QML 侧可 `import DeckShell.DeckGamepad`）
- **examples（可选）**：`-DBUILD_GAMEPAD_EXAMPLES=ON/OFF`
- **shared/static（可选）**：`-DBUILD_SHARED_LIBS=ON/OFF`
- **tests（可选）**：`-DDECKGAMEPAD_BUILD_TESTS=ON -DBUILD_TESTING=ON`（包含 install+find_package smoke）

#### no-skip 门禁（防止“测试跳过仍显示通过”）

当环境缺少 `/dev/uinput` 权限时，部分集成/E2E 会 `QSKIP`，`ctest` 仍返回成功。
推荐使用下列统一入口，**让 SKIP 直接失败**：

```bash
# build_dir 为 CMake 构建目录
cmake --build "<build_dir>" --target ctest-no-skip

# 或直接运行脚本
bash "scripts/ctest_no_skip.sh" "<build_dir>"
```

### 快速上手（第三方应用，core-only）

> 目标：安装后可 `find_package(DeckShellGamepad CONFIG REQUIRED)` 并链接 `DeckShell::deckshell-gamepad`。

**构建与安装（core-only，发行版推荐 shared）**：

```bash
cmake -S "DeckShellGamepad-private-work" -B "build-deckgamepad" \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_GAMEPAD_EXAMPLES=OFF \
  -DDECKGAMEPAD_BUILD_TESTS=OFF \
  -DDECKGAMEPAD_BUILD_QML_MODULE=OFF \
  -DDECKGAMEPAD_BUILD_TREELAND_CLIENT=OFF
cmake --build "build-deckgamepad" -j
cmake --install "build-deckgamepad" --prefix "<prefix>"
```

**第三方 CMake 消费者（install + find_package）**：见下方“作为库使用”示例（推荐在应用侧设置 `enableLegacyDeckShellPaths=false`，避免误读 `~/.config/DeckShell/*`）。

## ✅ 稳定 API（对外推荐）

本库面向第三方应用的“稳定推荐入口”如下（优先级从高到低）：

- **C++：`DeckGamepadService`（推荐）**
  - 统一生命周期、设备枚举、事件信号、诊断与错误模型。
  - 默认使用 `EvdevProvider`（Linux `/dev/input` 直连；默认 IO 线程），无需手写 provider。
    - 调试单线程模式：运行期设置 `DeckGamepadRuntimeConfig.providerSelection = EvdevUdev`，或环境变量 `DECKGAMEPAD_EVDEV_SINGLE_THREAD=1`，或构建期 `-DDECKGAMEPAD_DEFAULT_PROVIDER=evdev-udev`。
  - 可通过注入 `IDeckGamepadProvider` 实现后端替换（例如 Treeland/WL 协议、mock/replay）。
- **QML：`DeckShell.DeckGamepad`（P1，可选扩展）**
  - 不纳入本次 core-only 对外发布基线与稳定承诺；如需使用请自行启用构建选项与安装验证。

刻意不做（稳定边界）：
- **不提供系统级输入注入**（`uinput`/seat 注入属于更高权限与安全边界，应由上层/宿主实现并明确授权）。

## ⚠️ 高级/legacy API（不承诺稳定）

以下能力可用，但不建议第三方应用直接依赖为长期契约（可能在后续版本做破坏性调整）：
- `DeckGamepadBackend`（单例，legacy 实现细节，主要用于 provider 适配/调试/历史兼容）
- `treeland/*`（Wayland 协议链路受 compositor 策略影响，如 focused gating/授权语义）

## 🧩 QML 模块（DeckShell.DeckGamepad）

> ⚠️ P1（可选扩展）：本次对外发布为 core-only，不承诺 QML 模块的稳定性与兼容性；如需使用请自行启用 `-DDECKGAMEPAD_BUILD_QML_MODULE=ON` 并进行安装+导入验证。

该模块面向“纯 Qt/QML 应用”提供开箱即用的接入方式（无需额外手柄相关 C++ glue），核心导出：
- `GamepadManager`（QML_SINGLETON）：后端选择/诊断/设备列表/配置入口
- `Gamepad`：每设备对象（全量按钮/轴/hat 状态 + raw event）
- `GamepadActionRouter`：输出稳定 actionId（不注入 KeyEvent）
- `GamepadKeyNavigation`：可选 Key Navigation 适配器（Action→KeyEvent，带门控）
- `CustomMappingManager`：自定义映射包装（仅 evdev 生效）

刻意不做（对外契约约束）：
- **不对 QML 暴露 SDL DB 元信息**（例如条目列表、匹配详情、DB 版本/数量等），避免形成不可控外部契约。

### “开箱即用”定义（对外分发）

对第三方纯 QML 应用而言，“开箱即用”指：
- **无需额外 C++ glue**：不需要手写 `qmlRegisterType/qmlRegisterSingletonType` 或自定义插件加载代码
- **默认安装路径可被找到**：模块安装到 `${CMAKE_INSTALL_QMLDIR}/DeckShell/DeckGamepad/`，并交付 `qmldir` + 插件库 + typeinfo（`*.qmltypes`，例如 `DeckShellGamepadQmlPlugin.qmltypes`）
- **安装后可验证**：建议使用“build → install → clean env import”类 smoke 测试固化（避免只在源码树可用）

运行期搜索路径约定：
- 若安装到 Qt 的默认 QML 目录（同前缀），通常无需额外配置即可 `import DeckShell.DeckGamepad`
- 若安装到自定义前缀或非标准路径，可设置 `QML2_IMPORT_PATH=<prefix>/${CMAKE_INSTALL_QMLDIR}`，或在应用侧调用 `QQmlEngine::addImportPath()`

### QML 最小使用示例（推荐）

```qml
import QtQuick
import QtQuick.Controls
import DeckShell.DeckGamepad 1.0

ApplicationWindow {
    visible: true

    Component.onCompleted: GamepadManager.start()

    Gamepad { id: gp; deviceId: -1 } // 通过 deviceModel 选择后赋值
    GamepadActionRouter { id: router; active: true; gamepad: gp }
    GamepadKeyNavigation { active: true; actionRouter: router; target: keySink }

    Rectangle { id: keySink; focus: true; Keys.onPressed: (e) => e.accepted = true }
}
```

### 拆包建议（避免 core 强拉 QtQml 依赖）

面向发行版/系统包的常见拆分方式：
- `core`：`deckshell-gamepad`（Qt6::Core + libudev）
- `-dev`：头文件 + `DeckShellGamepadConfig.cmake` 等开发文件
- `-qml`：`DeckShell.DeckGamepad` QML 模块（依赖 core + Qt6::Qml/Gui）
- `-treeland`（可选）：Treeland client 支持（如启用 `DECKGAMEPAD_BUILD_TREELAND_CLIENT=ON`）

具体安装产物（`core/-dev`）与第三方 `find_package` 验证步骤见：`ARTIFACTS.md`。
版本与兼容性承诺（SemVer/ABI/破坏性变更规则）与变更日志策略见：`VERSIONING.md`、`CHANGELOG.md`。
shared 发行版发布步骤（tag/产物校验/回归矩阵/回滚策略）见：`RELEASE_CHECKLIST.md`。

### 作为库使用

### 第三方 CMake 消费者（install + find_package）

本库已导出 CMake 包 `DeckShellGamepad` 与目标 `DeckShell::deckshell-gamepad`，推荐第三方应用使用 install 产物接入：

```cmake
find_package(DeckShellGamepad CONFIG REQUIRED)

add_executable(app main.cpp)
target_link_libraries(app PRIVATE DeckShell::deckshell-gamepad Qt6::Core)
```

提示：
- 若安装到非系统前缀，可设置 `CMAKE_PREFIX_PATH=<prefix>` 或 `DeckShellGamepad_DIR=<prefix>/lib/cmake/DeckShellGamepad`
- 可参考 `tests/smoke/gamepad_consumer/`（install+find_package smoke consumer）

```cpp
#include <deckshell/deckgamepad/service/deckgamepadservice.h>

using deckshell::deckgamepad::DeckGamepadService;
using deckshell::deckgamepad::DeckGamepadRuntimeConfig;

DeckGamepadService service;

// 可选：独立应用建议关闭 legacy DeckShell 路径回退（避免误读 ~/.config/DeckShell/*）
DeckGamepadRuntimeConfig config;
config.enableLegacyDeckShellPaths = false;
service.setRuntimeConfig(config); // 需在 start() 前设置

QObject::connect(&service, &DeckGamepadService::diagnosticChanged, [](auto diag) {
    if (!diag.isOk()) {
        qInfo() << "gamepad diagnosticKey=" << diag.key << "actions=" << diag.suggestedActions;
    }
});

QObject::connect(&service, &DeckGamepadService::gamepadConnected, [](int deviceId, const QString &name) {
    qInfo() << "Gamepad connected:" << deviceId << name;
});

QObject::connect(&service, &DeckGamepadService::buttonEvent, [](int deviceId, auto event) {
    qInfo() << "Button" << event.button << (event.pressed ? "pressed" : "released") << "device" << deviceId;
});

if (!service.start()) {
    qWarning() << "Failed to start gamepad service:" << service.lastErrorMessage();
}
```

### 编译库

```bash
cd <repo-root>
cmake -B build -DBUILD_GAMEPAD_EXAMPLES=OFF
cmake --build build

# 默认构建为静态库（BUILD_SHARED_LIBS=OFF）
ls build/src/libdeckshell-gamepad.a

# 发行版建议构建共享库（BUILD_SHARED_LIBS=ON）
cmake -B build-shared -DBUILD_GAMEPAD_EXAMPLES=OFF -DBUILD_SHARED_LIBS=ON
cmake --build build-shared
ls build-shared/src/libdeckshell-gamepad.so*
```

### 编译示例程序

```bash
cd <repo-root>
cmake -B build -DBUILD_GAMEPAD_EXAMPLES=ON
cmake --build build

# 运行监控工具
./build/examples/gamepad-monitor/gamepad-monitor

# 运行可视化工具
./build/examples/gamepad-visualizer/gamepad-visualizer
```

## 🛠️ 集成到 DeckShell Compositor

在 `compositor/src/seat/helper.cpp` 中：

```cpp
#include <deckshell/deckgamepad/service/deckgamepadservice.h>

void Helper::init()
{
    // ... 其他初始化代码

    // Helper 持有单实例 Service，并注入 compositor 业务侧 GamepadManager 等模块
    m_gamepadService = new deckshell::deckgamepad::DeckGamepadService(this);

    // 先连接信号，再 start()，避免“已连接设备”丢事件
    connect(m_gamepadService, &deckshell::deckgamepad::DeckGamepadService::gamepadConnected,
            this, &Helper::onGamepadConnected);
    connect(m_gamepadService, &deckshell::deckgamepad::DeckGamepadService::buttonEvent,
            this, &Helper::onGamepadButton);

    if (!m_gamepadService->start()) {
        qWarning() << "Failed to start gamepad service:" << m_gamepadService->lastErrorMessage();
    }
}
```

## 📖 API 参考

### DeckGamepadService（推荐，稳定入口）

**方法（节选）**：
- `bool start()` / `void stop()` - 启停
- `DeckGamepadRuntimeConfig runtimeConfig() const` / `bool setRuntimeConfig(DeckGamepadRuntimeConfig)` - 运行期配置（运行中禁止修改）
- `QString activeProviderName() const` - 当前 provider
- `DeckGamepadError lastError() const` / `DeckGamepadDiagnostic diagnostic() const` - 错误与诊断
- `QList<int> connectedGamepads() const` / `DeckGamepadDeviceInfo deviceInfo(int)` - 设备枚举与信息
- `bool startVibration(int, float, float, int)` / `void stopVibration(int)` - 振动

**信号（节选）**：
- `gamepadConnected(int deviceId, const QString &name)`
- `buttonEvent(int deviceId, DeckGamepadButtonEvent event)`
- `deviceAvailabilityChanged(int deviceId, DeckGamepadDeviceAvailability availability)`
- `diagnosticChanged(DeckGamepadDiagnostic diagnostic)`

### IDeckGamepadProvider（扩展点）

用于自定义后端（evdev/treeland/mock/replay），由 `DeckGamepadService` 聚合并对上层提供统一信号风格。

### DeckGamepadBackend（高级/legacy，单例）

**方法**：
- `static DeckGamepadBackend* instance()` - 获取单例
- `bool start()` - 启动后端（初始化 udev，扫描设备）
- `void stop()` - 停止后端并关闭所有设备
- `QList<int> connectedGamepads() const` - 获取已连接设备 ID 列表
- `DeckGamepadDevice* device(int id) const` - 获取设备对象
- `void setAxisDeadzone(int deviceId, uint32_t axis, float deadzone)` - 设置轴死区（0.0-1.0）
- `void setAxisSensitivity(int deviceId, uint32_t axis, float sensitivity)` - 设置轴灵敏度（0.1-5.0）
- `bool startVibration(int deviceId, float weak, float strong, int duration_ms = 1000)` - 启动振动
- `void stopVibration(int deviceId)` - 停止振动

**信号**：
- `gamepadConnected(int deviceId, const QString &name)` - 设备连接
- `gamepadDisconnected(int deviceId)` - 设备断开
- `buttonEvent(int deviceId, DeckGamepadButtonEvent event)` - 按钮事件
- `axisEvent(int deviceId, DeckGamepadAxisEvent event)` - 摇杆/扳机事件
- `hatEvent(int deviceId, DeckGamepadHatEvent event)` - 方向键事件

### 数据结构

**按钮枚举**（deckgamepad.h）：
```cpp
enum GamepadButton {
    GAMEPAD_BUTTON_A = 0,      // 南键（Xbox A, PS Cross）
    GAMEPAD_BUTTON_B,          // 东键（Xbox B, PS Circle）
    GAMEPAD_BUTTON_X,          // 西键（Xbox X, PS Square）
    GAMEPAD_BUTTON_Y,          // 北键（Xbox Y, PS Triangle）
    GAMEPAD_BUTTON_L1,         // 左肩键
    GAMEPAD_BUTTON_R1,         // 右肩键
    GAMEPAD_BUTTON_L2,         // 左扳机（按钮）
    GAMEPAD_BUTTON_R2,         // 右扳机（按钮）
    GAMEPAD_BUTTON_SELECT,     // 选择键（Xbox Back, PS Share）
    GAMEPAD_BUTTON_START,      // 开始键（Xbox Start, PS Options）
    GAMEPAD_BUTTON_L3,         // 左摇杆按下
    GAMEPAD_BUTTON_R3,         // 右摇杆按下
    GAMEPAD_BUTTON_GUIDE,      // 主页键（Xbox Guide, PS Home）
    // ... 方向键虚拟按钮
};
```

**摇杆枚举**（deckgamepad.h）：
```cpp
enum GamepadAxis {
    GAMEPAD_AXIS_LEFT_X = 0,       // 左摇杆 X 轴（-1.0 到 1.0）
    GAMEPAD_AXIS_LEFT_Y,           // 左摇杆 Y 轴
    GAMEPAD_AXIS_RIGHT_X,          // 右摇杆 X 轴
    GAMEPAD_AXIS_RIGHT_Y,          // 右摇杆 Y 轴
    GAMEPAD_AXIS_TRIGGER_LEFT,     // 左扳机（模拟）
    GAMEPAD_AXIS_TRIGGER_RIGHT,    // 右扳机（模拟）
};
```

## 🔍 调试

### 诊断与排障（建议先看 `diagnosticKey` / `lastError`）

对第三方应用而言，推荐优先通过 `DeckGamepadService` 的**结构化诊断/错误**来做 UI 提示与降级，而不是依赖日志字符串：
- `DeckGamepadService::diagnosticKey()` / `diagnosticDetails()` / `suggestedActions()`
- `DeckGamepadService::lastError()` / `lastErrno()` / `lastErrorMessage()` / `lastErrorContext()`

常见诊断 key 对照（`src/core/deckgamepaddiagnostic.h`）：

| diagnosticKey | 典型含义 | 推荐处理动作（最小集） |
|---|---|---|
| `deckgamepad.permission.denied` | 无法读取/打开 `/dev/input/event*`（权限不足） | 配置 udev 规则/加入 `input` 组；或将 `deviceAccessMode=LogindTakeDevice`（需 logind/Qt DBus 支持）；仅调试时可用 root 复现 |
| `deckgamepad.session.inactive` | 当前会话非 active，按 `capturePolicy=ActiveSessionOnly` 门控 | 解锁/切回 active session；或将 `capturePolicy=Always`（kiosk/daemon 场景） |
| `deckgamepad.logind.unavailable` | 期望 logind 但运行环境不具备 | 切换 `deviceAccessMode=DirectOpen` 并配置权限；或确保运行在 systemd/logind 环境并启用 Qt DBus |
| `deckgamepad.device.busy` | 设备被占用/不可用（例如被其它进程独占） | 关闭占用进程；或使用 `grabMode=Shared`/`Auto` 降级共享采集 |
| `deckgamepad.device.grab_failed` | `EVIOCGRAB` 失败（独占抓取失败） | 推荐使用 `grabMode=Auto`（失败会自动降级 shared 并保留提示）；若必须独占则改用 `grabMode=Exclusive` 并允许失败退出 |
| `deckgamepad.wayland.focus_gated` |（P1/treeland）Wayland focus gating 导致事件被门控 | 确认 compositor 策略/窗口焦点；或改用 evdev provider |
| `deckgamepad.wayland.not_authorized` |（P1/treeland）Wayland 授权不足 | 由 compositor/宿主侧完成授权；或改用 evdev provider |

降级策略建议（面向“基本可用/基本稳定”）：
- **权限/短暂 I/O**：保持 `enableAutoRetryOpen=true`（默认）并配置合理 backoff（避免 busy loop）。
- **抓取**：默认 `grabMode=Shared`；如需优先独占但不阻断，使用 `grabMode=Auto`。
- **会话门控**：桌面环境推荐 `ActiveSessionOnly`；kiosk/daemon 可用 `Always`（需自行评估安全边界）。
- **振动（FF_RUMBLE）**：需要对 `/dev/input/event*` 具备写权限（`O_RDWR` + `EVIOCSFF`/`write(EV_FF)`）。若运行环境只能 `O_RDONLY`（例如 ACL 限制写），本库仍可读取输入，但 `startVibration()` 会失败；建议通过 udev 规则/组权限或 `deviceAccessMode=LogindTakeDevice` 获取可写 fd。

### 查看输入设备

```bash
# 列出所有输入设备
cat /proc/bus/input/devices

# 测试原始事件
sudo evtest /dev/input/eventX
```

### 权限配置

如果遇到权限问题，创建 udev 规则：

```bash
# /etc/udev/rules.d/99-gamepad.rules
SUBSYSTEM=="input", ATTRS{name}=="*Controller*", MODE="0660", GROUP="input"
SUBSYSTEM=="input", ATTRS{name}=="*Gamepad*", MODE="0660", GROUP="input"
KERNEL=="event*", SUBSYSTEM=="input", MODE="0660", GROUP="input"
```

应用规则：
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
sudo usermod -a -G input $USER  # 添加用户到 input 组
# 注销并重新登录
```

## 📝 维护说明

### 同步上游更新

如需同步 qwlroots 的更新：

```bash
cd 3rdparty/waylib-shared
git log qwlroots/src/types/qwgamepad* --oneline --since="2025-10-18"

# 如有新提交，手动应用 patch 或重新复制
```

### 本地修改记录

所有本地修改应记录在本文件的"变更历史"部分。

## 📋 变更历史

### v1.0.1 (2025-10-18)
- **命名空间调整**：将命名空间从 `DeckShell::Gamepad` 改为 `deckshell::gamepad`（全小写）
  - 更新 deckgamepad.h 中的默认宏定义
  - 更新 CMakeLists.txt 中的编译定义
  - 使用 `DECKGAMEPAD_USE_NAMESPACE` 宏

### v1.0.0 (2025-10-18)
- **初始移植**：从 qwlroots commit `01adb235` 移植完整代码
- **保持原始结构**：代码和接口保持不变
- **添加独立构建**：创建 CMakeLists.txt，编译为静态库
- **包含示例程序**：gamepad-monitor 和 gamepad-visualizer
- **版本追踪**：创建本 README.md 记录完整来源信息

## 📄 许可证

本项目源码文件普遍使用 SPDX 标识许可（多数文件为多重许可）：
- `Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only`

对外分发注意事项（简要）：
- 请以**每个源码文件头部**的 SPDX 声明为准（不同文件可能存在不同许可表达式）。
- `data/gamecontrollerdb.txt` 属于第三方数据文件，许可/版本追踪见 `THIRD_PARTY.md`（本仓库当前标记为 TBD，发布前需补齐）。
- 更多说明见 `LICENSE` 与 `NOTICE`。

版权归属：
- Copyright (C) 2024 UnionTech Software Technology Co., Ltd.
- 基于 qtgamepad 和 Godot Engine v4.0 代码

## 🔗 相关链接

- **qwlroots 仓库**：[waylib-shared](https://github.com/vioken/waylib)
- **原始 commit**：`01adb2350ef31f5a597c255d0f56d1ab04938d72`
- **参考实现**：
  - qtgamepad: https://code.qt.io/cgit/qt/qtgamepad.git/
  - Godot Engine: https://github.com/godotengine/godot
- **Linux 输入子系统文档**：https://www.kernel.org/doc/html/latest/input/

## 📮 反馈

如有问题或建议，请在 DeckShell 项目中提交 Issue。
