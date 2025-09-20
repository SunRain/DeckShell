# DDE Shell Library

Qt6 shared library for Deepin Desktop Environment shell integration with Wayland.

## 功能特性

- ✅ C++ API：完整的 DDE shell surface 管理
- ✅ QML Plugin：声明式 UI 集成（Attached Properties）
- ✅ Wayland 协议：treeland_dde_shell_v1 支持
- ✅ 异步初始化：自动处理延迟初始化和操作队列

## 构建和安装

```bash
# 构建
cmake -B build -DCMAKE_INSTALL_PREFIX=/usr
cmake --build build

# 安装
sudo cmake --install build
```

### 安装结果

```
/usr/lib/libddeshellclient.so                              # 共享库
/usr/include/DeckShell/ddeshellclient/window.h             # 公共头文件
/usr/include/DeckShell/ddeshellclient/shellsurface.h
/usr/include/DeckShell/ddeshellclient/waylandmanager.h
/usr/include/DeckShell/ddeshellclient/ddeshellclient_export.h
/usr/lib/qt6/qml/DeckShell/ddeshellclient/                 # QML 插件
    ├── libDShellClientQmlPlugin.so
    └── qmldir
/usr/lib/cmake/DDEShellClient/DDEShellClientConfig.cmake        # CMake 配置
/usr/bin/ddeshellclient-simple                             # 示例程序
/usr/bin/ddeshellclient-mainwindow
/usr/bin/ddeshellclient-qml
```

## 使用方法

### C++ API

```cpp
#include <DeckShell/ddeshellclient/window.h>
#include <DeckShell/ddeshellclient/shellsurface.h>

Window *ddeWindow = Window::get(qwindow);
ddeWindow->setSkipMultitaskview(true);
ddeWindow->setSkipSwitcher(true);
ddeWindow->setRole(ShellSurface::Role::Overlay);
```

### CMake 集成

```cmake
find_package(DDEShellClient REQUIRED)
target_link_libraries(myapp DDEShellClient::ddeshellclient)
```

### QML 集成

```qml
import QtQuick
import QtQuick.Window
import DeckShell.ddeshellclient 1.0

Window {
    DShellClientSurface.skipMultitaskview: true
    DShellClientSurface.skipSwitcher: true
    DShellClientSurface.acceptKeyboardFocus: false
    DShellClientSurface.role: ShellSurface.Role.Overlay
}
```

## 示例程序

- `ddeshellclient-simple`: 纯 C++ 最小示例
- `ddeshellclient-mainwindow`: 完整的 MainWindow 示例（带 UI）
- `ddeshellclient-qml`: QML Attached Properties 示例

运行示例：
```bash
ddeshellclient-simple
ddeshellclient-mainwindow
ddeshellclient-qml
```

## 架构设计

参考 KDE layer-shell-qt 项目架构：
- 共享库与 QML plugin 分离
- 使用 Qt parent-child 生命周期管理
- QML Attached Properties 模式

详见：[layer-shell-qt-qml-analysis.md](./layer-shell-qt-qml-analysis.md)

## 许可证

[待添加]
