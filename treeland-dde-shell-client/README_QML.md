# DDE Shell QML Support - 使用说明

本项目已完整实现了 `treeland_dde_shell_surface_v1` 协议的 QML 支持，采用 **layer-shell-qt 风格的 Attached Properties** 模式。

## ✨ 特性

- ✅ **标准 Qt 对象管理**：使用 parent-child 机制，无需手动管理内存
- ✅ **Attached Properties**：与 layer-shell-qt 一致的 QML 使用方式
- ✅ **属性绑定支持**：所有属性支持 QML 双向绑定
- ✅ **实时更新**：属性变化自动同步到 Wayland compositor
- ✅ **异步初始化**：自动处理延迟初始化和操作队列

## 📦 构建

```bash
mkdir build && cd build
cmake ..
make
```

## 🚀 QML 使用方式

### 基本示例

```qml
import QtQuick
import QtQuick.Window
import DShellTest 1.0

Window {
    width: 400
    height: 300
    visible: true

    // 使用 Attached Properties 配置 DDE Shell
    DShellSurface.skipMultitaskview: true
    DShellSurface.skipSwitcher: true
    DShellSurface.skipDockPreview: false
    DShellSurface.acceptKeyboardFocus: false
    DShellSurface.role: ShellSurface.Role.Overlay

    Rectangle {
        anchors.fill: parent
        color: "lightblue"

        Text {
            anchors.centerIn: parent
            text: "DDE Shell QML Window"
        }
    }
}
```

### 运行 QML 示例

```bash
# 方式 1: 使用 qml 工具运行
qml test.qml

# 方式 2: 使用 qmlscene
qmlscene test.qml

# 注意：需要确保 DShellTest QML 模块已安装或在模块搜索路径中
```

### 动态属性绑定

```qml
Window {
    DShellSurface.skipMultitaskview: myCheckbox.checked

    CheckBox {
        id: myCheckbox
        text: "Skip Multitask View"
        checked: true
    }

    Component.onCompleted: {
        // 读取当前属性值
        console.log("Current skipMultitaskview:", DShellSurface.skipMultitaskview)
    }
}
```

## 🎯 可用属性

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `skipMultitaskview` | bool | false | 是否跳过多任务视图 |
| `skipSwitcher` | bool | false | 是否跳过窗口切换器 |
| `skipDockPreview` | bool | false | 是否跳过任务栏预览 |
| `acceptKeyboardFocus` | bool | true | 是否接受键盘焦点 |
| `role` | enum | Overlay | 窗口角色（当前仅支持 Overlay） |

## 🏗️ C++ 使用方式（保持兼容）

```cpp
#include "window.h"

// 方式 1: 使用 QWindow
QWindow *qwindow = new QWindow();
Window *ddeWindow = Window::get(qwindow);
ddeWindow->setSkipMultitaskview(true);

// 方式 2: 使用 QMainWindow
QMainWindow *mainWindow = new QMainWindow();
Window *ddeWindow = Window::get(mainWindow);
ddeWindow->setSkipSwitcher(true);
```

## 🔧 实现架构

```
┌─────────────────────────────────────────┐
│  QML 层                                  │
│  import DShellTest 1.0                  │
│  Window { DShellSurface.xxx: ... }     │
└────────────┬────────────────────────────┘
             │ Attached Properties
             │ Qt 自动调用 qmlAttachedProperties()
┌────────────▼────────────────────────────┐
│  declarative/types.h                    │
│  QML_FOREIGN(Window)                    │
│  QML_ATTACHED(Window)                   │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│  window.h/cpp                           │
│  - Q_PROPERTY 声明                       │
│  - qmlAttachedProperties() 实现          │
│  - parent-child 生命周期管理             │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│  shellsurface.h/cpp                     │
│  Wayland 协议包装                        │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│  treeland_dde_shell_surface_v1          │
│  Wayland 协议实现                        │
└─────────────────────────────────────────┘
```

## 📚 与 layer-shell-qt 对比

| 特性 | layer-shell-qt | DeckShell (本项目) |
|------|----------------|-------------------|
| QML 集成方式 | Attached Properties | ✅ Attached Properties |
| 使用语法 | `LayerShell.Window.xxx` | `DShellSurface.xxx` |
| 生命周期管理 | parent-child | ✅ parent-child |
| 属性绑定 | 支持 | ✅ 支持 |
| C++ API | 独立使用 | ✅ 独立使用 |

## ⚠️ 重要说明

1. **生命周期管理**：Window 对象由 QWindow 作为 parent 自动管理，无需手动 delete
2. **线程安全**：所有操作必须在主线程中进行
3. **异步初始化**：属性设置会自动排队，初始化完成后执行
4. **QML 模块路径**：确保 `DShellTest` 模块在 QML 搜索路径中

## 🐛 故障排除

### 问题：QML 提示 "module not found"

**解决方案**：
```bash
# 检查模块是否已生成
ls build/declarative/DShellTest/

# 设置 QML 模块路径
export QML_IMPORT_PATH=/path/to/build/declarative
qml test.qml
```

### 问题：属性设置无效

**解决方案**：
- 检查 Window 是否已初始化：`Window::initialized` 信号
- 查看日志中的排队操作执行情况
- 确认 Wayland compositor 支持 `treeland_dde_shell_v1` 协议

## 📖 参考资源

- [Qt QML Attached Properties](https://doc.qt.io/qt-6/qtqml-syntax-objectattributes.html)
- [layer-shell-qt 项目](https://github.com/KDE/layer-shell-qt)
- [treeland-dde-shell-v1 协议](./treeland-dde-shell-v1.xml)

---

**生成时间**：2025-10-15
**Qt 版本要求**：Qt 6.5+
**协议版本**：treeland_dde_shell_v1 version 1
