# up-master → master-merge 全量文件级差异归因（src/** → compositor/src/**）

- 对比基准：`up-master@3e5fdd4d32396b20dc0294b84277b831412484b3:src/**`
- 对比目标：`master-merge:compositor/src/**`（工作区内容）
- 生成时间：2026-02-01

## 0) 统计摘要

- 上游文件数：334
- 完全一致：256
- 存在差异：78
- 目标缺失文件：0
- 目标额外文件：2

目标额外文件（up-master 无对应映射）：
- `compositor/src/config/treelandconfig.cpp`
- `compositor/src/config/treelandconfig.hpp`

## 1) 归因维度定义（用于逐项标注）

为避免把“工程差异/产品差异”误判为“Waylib workaround”，本报告按以下维度对每个偏离项做标注：

- **A. QML 命名空间/模块名差异**：`Treeland` → `DeckShell.Compositor`（属于产品命名空间差异，非 Waylib API workaround）
- **B. WaylibShared QML import 差异**：`Waylib.QuickSharedServer` ↔ `WaylibShared.QuickSharedServer`（属于 WaylibShared 打包/命名调整，通常是必要适配，非“旧 waylib-shared 兼容 workaround”）
- **C. WaylibShared CMake target 差异**：`Waylib::SharedServer` ↔ `WaylibShared::SharedServer`（同上，属于必要适配）
- **D. 协议生成/target 整理**：`TreelandProtocols`、`local_qtwayland_server_protocol_treeland()` 等（属于构建/协议组织差异）
- **E. 编译开关差异**：`DISABLE_DDM` / `EXT_SESSION_LOCK_V1` 等（属于可选特性裁剪/构建差异）
- **F. 业务功能差异**：与 WaylibShared 版本无关的功能补丁（例如 DDE Shell surface 延迟创建处理等）

## 2) “仅为旧 waylib-shared 兼容”的分叉点筛选结果

结论：**在当前 `master-merge` HEAD 上，未发现仍残留的“仅为旧 waylib-shared 兼容”的分叉点。**

说明：
- 本轮扫描的判定口径是：偏离项是否引入了仅为兼容旧 WaylibShared API 的替代路径（例如 `pidfd` 获取绕行、输出提交绕过 `WOutputHelper` 管线、以及不必要的 session/socket 反查等），且在更新后的 `3rdparty/waylib-shared` 下可直接回退到 up-master 原始实现而不影响现有功能/构建。
- 已确认并回退的旧 workaround（不再体现在差异清单中）：
  - `pidfd` 获取绕行（已回退为 `pidFD()`）
  - 输出配置/亮度色温提交绕过 `WOutputHelper`（已回退为 `WOutputHelper::ExtraState + scheduleCommitJob()`）
  - XWayland 标题栏判定的 `WClient/WSocket` 绕行（已回退为 `xwaylandSurface->xwayland()` + `sessionForXWayland()`）

## 3) 差异项逐条归因（commit → 文件级）

> 注：本节按“文件路径”逐项列出偏离并标注归因维度（A-F）。如同一文件同时命中多个维度，则并列标注。

### 3.1 构建/协议相关

- `compositor/src/CMakeLists.txt`：C、D、E
- `compositor/src/modules/CMakeLists.txt`：D
- `compositor/src/modules/app-id-resolver/CMakeLists.txt`：D
- `compositor/src/modules/capture/CMakeLists.txt`：C、D
- `compositor/src/modules/dde-shell/CMakeLists.txt`：D
- `compositor/src/modules/ddm/CMakeLists.txt`：E
- `compositor/src/modules/foreign-toplevel/CMakeLists.txt`：D
- `compositor/src/modules/item-selector/CMakeLists.txt`：D
- `compositor/src/modules/keystate/CMakeLists.txt`：D
- `compositor/src/modules/output-manager/CMakeLists.txt`：D
- `compositor/src/modules/personalization/CMakeLists.txt`：D
- `compositor/src/modules/prelaunch-splash/CMakeLists.txt`：D
- `compositor/src/modules/screensaver/CMakeLists.txt`：D
- `compositor/src/modules/shortcut/CMakeLists.txt`：C、D
- `compositor/src/modules/tools/CMakeLists.txt`：D
- `compositor/src/modules/virtual-output/CMakeLists.txt`：C、D
- `compositor/src/modules/wallpaper-color/CMakeLists.txt`：C、D
- `compositor/src/modules/window-management/CMakeLists.txt`：C、D
- `compositor/src/plugins/lockscreen/CMakeLists.txt`：D、E
- `compositor/src/plugins/multitaskview/CMakeLists.txt`：D
- `compositor/src/treeland-shortcut/CMakeLists.txt`：D

### 3.2 核心 C++ 逻辑（非 WaylibShared workaround）

- `compositor/src/core/qmlengine.cpp`：E
- `compositor/src/core/shellhandler.cpp`：F（DDE Shell surface 延迟创建处理）
- `compositor/src/core/treeland.cpp`：E
- `compositor/src/main.cpp`：F
- `compositor/src/output/output.cpp`：A（QML 模块名）、E（若涉及编译开关）
- `compositor/src/seat/helper.cpp`：A、D、E、F
- `compositor/src/seat/helper.h`：E、F
- `compositor/src/modules/ddm/ddminterfacev1.cpp`：E
- `compositor/src/utils/cmdline.cpp`：F
- `compositor/src/wallpaper/wallpaperimage.cpp`：F

### 3.3 Greeter 相关

- `compositor/src/greeter/greeterproxy.cpp`：A、F
- `compositor/src/greeter/sessionmodel.cpp`：A、F
- `compositor/src/greeter/sessionmodel.h`：A、F
- `compositor/src/greeter/usermodel.cpp`：A、F

### 3.4 QML（命名空间与 WaylibShared import 适配为主）

#### core/qml/Animations
- `compositor/src/core/qml/Animations/GeometryAnimation.qml`：A、B
- `compositor/src/core/qml/Animations/LaunchpadAnimation.qml`：A
- `compositor/src/core/qml/Animations/LayerShellAnimation.qml`：B
- `compositor/src/core/qml/Animations/MinimizeAnimation.qml`：A
- `compositor/src/core/qml/Animations/NewAnimation.qml`：A、B
- `compositor/src/core/qml/Animations/ShowDesktopAnimation.qml`：A

#### core/qml（主界面）
- `compositor/src/core/qml/CaptureSelectorLayer.qml`：A、B
- `compositor/src/core/qml/CopyOutput.qml`：B
- `compositor/src/core/qml/Decoration.qml`：A、B
- `compositor/src/core/qml/DockPreview.qml`：A、B
- `compositor/src/core/qml/Effects/Blur.qml`：A、B
- `compositor/src/core/qml/Effects/LaunchpadCover.qml`：A、B
- `compositor/src/core/qml/OutputMenuBar.qml`：A、B
- `compositor/src/core/qml/PrimaryOutput.qml`：A、B
- `compositor/src/core/qml/SurfaceContent.qml`：A、B
- `compositor/src/core/qml/SwitchViewDelegate.qml`：A
- `compositor/src/core/qml/TaskBar.qml`：A、B
- `compositor/src/core/qml/TaskSwitcher.qml`：A、B
- `compositor/src/core/qml/TaskWindowPreview.qml`：A
- `compositor/src/core/qml/TitleBar.qml`：A、B
- `compositor/src/core/qml/WindowMenu.qml`：A、B
- `compositor/src/core/qml/WindowPickerLayer.qml`：A
- `compositor/src/core/qml/WorkspaceProxy.qml`：A
- `compositor/src/core/qml/WorkspaceSwitcher.qml`：A

#### plugins/multitaskview/qml
- `compositor/src/plugins/multitaskview/qml/MultitaskviewProxy.qml`：B
- `compositor/src/plugins/multitaskview/qml/WindowSelectionGrid.qml`：B
- `compositor/src/plugins/multitaskview/qml/WorkspaceSelectionList.qml`：A

#### plugins/lockscreen/qml
- `compositor/src/plugins/lockscreen/qml/ControlAction.qml`：A
- `compositor/src/plugins/lockscreen/qml/Greeter.qml`：A
- `compositor/src/plugins/lockscreen/qml/GreeterModel.qml`：A
- `compositor/src/plugins/lockscreen/qml/HintLabel.qml`：A
- `compositor/src/plugins/lockscreen/qml/LockView.qml`：A
- `compositor/src/plugins/lockscreen/qml/PowerList.qml`：A
- `compositor/src/plugins/lockscreen/qml/QuickAction.qml`：A
- `compositor/src/plugins/lockscreen/qml/RoundBlur.qml`：A
- `compositor/src/plugins/lockscreen/qml/SessionList.qml`：A
- `compositor/src/plugins/lockscreen/qml/ShutdownButton.qml`：A
- `compositor/src/plugins/lockscreen/qml/ShutdownView.qml`：A
- `compositor/src/plugins/lockscreen/qml/TimeDateWidget.qml`：A
- `compositor/src/plugins/lockscreen/qml/UserInput.qml`：A
- `compositor/src/plugins/lockscreen/qml/UserList.qml`：A

## 4) 建议的后续动作（可选）

- 若要进一步收敛差异（非 WaylibShared workaround 范畴）：需要单独按功能/产品差异逐项评估是否应保持本地分叉（例如 DDE Shell surface 延迟创建处理、QML 命名空间替换等）。
- 若仅关注 WaylibShared：目前无需额外回退；后续变更建议继续以 `3rdparty/waylib-shared` 的导出 target/QML module 为准，避免引入新的兼容性分支。

