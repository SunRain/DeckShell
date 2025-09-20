# layer-shell-qt QML 支持实现方式分析

> 分析对象：`layer-shell-qt/src/declarative/` 目录
>
> 分析日期：2025-10-10

## 概述

layer-shell-qt 使用 Qt 的 **Attached Properties（附加属性）** 机制实现 QML 集成，而不是创建独立的 QML 类型。这是一种非常优雅且侵入性低的实现方式。

---

## 1. 核心架构：Attached Properties 模式

### 1.1 关键代码

**文件：** `layer-shell-qt/src/declarative/types.h:10-19`

```cpp
QML_DECLARE_TYPEINFO(LayerShellQt::Window, QML_HAS_ATTACHED_PROPERTIES)

class WindowForeign
{
    Q_GADGET
    QML_NAMED_ELEMENT(Window)           // QML 中的名称
    QML_FOREIGN(LayerShellQt::Window)   // 绑定到 C++ 类
    QML_UNCREATABLE("")                 // 不能直接创建实例
    QML_ATTACHED(LayerShellQt::Window)  // 作为附加属性使用
};
```

### 1.2 设计要点

- **`QML_FOREIGN`**：将现有的 C++ 类（`LayerShellQt::Window`）暴露给 QML，无需修改原始类
- **`QML_UNCREATABLE`**：防止在 QML 中直接 `Window {}` 创建实例
- **`QML_ATTACHED`**：声明这个类型作为附加属性使用
- **`Q_GADGET`**：轻量级元对象系统，不继承 QObject

---

## 2. QML 使用方式

### 2.1 导入模块

```qml
import org.kde.layershell 1.0
```

### 2.2 使用示例

```qml
import QtQuick
import org.kde.layershell 1.0

Window {
    visible: true
    width: 400
    height: 300

    // 通过附加属性配置 layer-shell
    LayerShell.Window.layer: LayerShell.Window.LayerOverlay
    LayerShell.Window.anchors: LayerShell.Window.AnchorTop | LayerShell.Window.AnchorLeft
    LayerShell.Window.margins: Qt.margins(10, 10, 10, 10)
    LayerShell.Window.exclusionZone: 40
    LayerShell.Window.keyboardInteractivity: LayerShell.Window.KeyboardInteractivityOnDemand
    LayerShell.Window.scope: "my-panel"
}
```

### 2.3 特点

- **非侵入性**：使用标准 QML `Window`，通过 `LayerShell.Window.*` 附加属性扩展
- **语义清晰**：一眼就能看出哪些是 layer-shell 特有的属性
- **可选使用**：不用 layer-shell 时，去掉附加属性即可，窗口仍正常工作

---

## 3. 实现机制详解

### 3.1 QML 模块定义

**文件：** `layer-shell-qt/src/declarative/CMakeLists.txt:4-11`

```cmake
ecm_add_qml_module(LayerShellQtQml
                  URI "org.kde.layershell"
                  VERSION 1.0
                  SOURCES types.h types.cpp
                  GENERATE_PLUGIN_SOURCE)
target_link_libraries(LayerShellQtQml PRIVATE Qt::Qml LayerShellQtInterface)

ecm_finalize_qml_module(LayerShellQtQml DESTINATION ${KDE_INSTALL_QMLDIR})
```

**关键点：**
- 使用 KDE 的 `ecm_add_qml_module` 宏简化 QML 模块创建
- `GENERATE_PLUGIN_SOURCE` 自动生成插件代码
- 只需 `types.h/cpp` 两个文件即可完成 QML 绑定

### 3.2 C++ 类实现

**文件：** `layer-shell-qt/src/interfaces/window.h:21-153`

#### 3.2.1 类定义

```cpp
class LAYERSHELLQT_EXPORT Window : public QObject
{
    Q_OBJECT
    Q_PROPERTY(Anchors anchors READ anchors WRITE setAnchors NOTIFY anchorsChanged)
    Q_PROPERTY(QString scope READ scope WRITE setScope)
    Q_PROPERTY(QMargins margins READ margins WRITE setMargins NOTIFY marginsChanged)
    Q_PROPERTY(qint32 exclusionZone READ exclusionZone WRITE setExclusiveZone NOTIFY exclusionZoneChanged)
    Q_PROPERTY(Layer layer READ layer WRITE setLayer NOTIFY layerChanged)
    Q_PROPERTY(KeyboardInteractivity keyboardInteractivity READ keyboardInteractivity WRITE setKeyboardInteractivity NOTIFY keyboardInteractivityChanged)
    Q_PROPERTY(ScreenConfiguration screenConfiguration READ screenConfiguration WRITE setScreenConfiguration)
    Q_PROPERTY(bool activateOnShow READ activateOnShow WRITE setActivateOnShow)

public:
    ~Window() override;

    // 枚举定义
    enum Anchor {
        AnchorNone = 0,
        AnchorTop = 1,
        AnchorBottom = 2,
        AnchorLeft = 4,
        AnchorRight = 8,
    };
    Q_DECLARE_FLAGS(Anchors, Anchor)
    Q_FLAG(Anchors)

    enum Layer {
        LayerBackground = 0,
        LayerBottom = 1,
        LayerTop = 2,
        LayerOverlay = 3,
    };
    Q_ENUM(Layer)

    enum KeyboardInteractivity {
        KeyboardInteractivityNone = 0,
        KeyboardInteractivityExclusive = 1,
        KeyboardInteractivityOnDemand = 2,
    };
    Q_ENUM(KeyboardInteractivity)

    // ... getter/setter 方法 ...

    // 关键：获取或创建 Window 对象
    static Window *get(QWindow *window);

    // 关键：QML Attached Properties 接口
    static Window *qmlAttachedProperties(QObject *object);

Q_SIGNALS:
    void anchorsChanged();
    void exclusionZoneChanged();
    void marginsChanged();
    void layerChanged();
    // ...

private:
    Window(QWindow *window);
    QScopedPointer<WindowPrivate> d;
};
```

#### 3.2.2 关键方法

**`qmlAttachedProperties` 方法** (`window.cpp:225-228`):

```cpp
Window *Window::qmlAttachedProperties(QObject *object)
{
    return get(qobject_cast<QWindow *>(object));
}
```

这是实现 Attached Properties 的核心。当 QML 中使用 `LayerShell.Window.xxx` 时，Qt 会调用这个静态方法。

### 3.3 单例模式管理

**文件：** `layer-shell-qt/src/interfaces/window.cpp:41, 212-223`

```cpp
// 全局映射：QWindow -> Window
static QMap<QWindow *, Window *> s_map;

Window *Window::get(QWindow *window)
{
    if (!window) {
        return nullptr;
    }

    auto layerShellWindow = s_map.value(window);
    if (layerShellWindow) {
        return layerShellWindow;  // 已存在，直接返回
    }
    return new Window(window);  // 懒加载创建
}
```

**设计要点：**
- 每个 `QWindow` 只对应一个 `Window` 对象
- 懒加载：只在需要时创建
- 通过静态 map 全局管理生命周期

### 3.4 与 Wayland 集成

**文件：** `layer-shell-qt/src/interfaces/window.cpp:184-210`

```cpp
Window::Window(QWindow *window)
    : QObject(window)
    , d(new WindowPrivate(window))
{
    s_map.insert(d->parentWindow, this);

    window->create();  // 确保平台窗口已创建

    auto waylandWindow = dynamic_cast<QtWaylandClient::QWaylandWindow *>(window->handle());
    if (!waylandWindow) {
        qCWarning(LAYERSHELLQT) << window << "is not a wayland window";
        return;
    }

    static QWaylandLayerShellIntegration *shellIntegration = nullptr;
    if (!shellIntegration) {
        shellIntegration = new QWaylandLayerShellIntegration();
        if (!shellIntegration->initialize(waylandWindow->display())) {
            delete shellIntegration;
            shellIntegration = nullptr;
            qCWarning(LAYERSHELLQT) << "Failed to initialize layer-shell integration";
            return;
        }
    }

    waylandWindow->setShellIntegration(shellIntegration);
}
```

**关键点：**
- 在构造函数中自动设置 Wayland Shell Integration
- 单例模式管理 `shellIntegration`
- 错误处理完善

---

## 4. Qt 6.8+ 兼容性处理

**文件：** `layer-shell-qt/src/declarative/types.h:22-55`

为 Qt 6.8.1 以下版本提供 `QMargins` 的 QML 值类型支持：

```cpp
#if QT_VERSION < QT_VERSION_CHECK(6, 8, 1)
struct Q_QML_EXPORT QQmlMarginsValueType {
    QMargins m;
    Q_PROPERTY(int left READ left WRITE setLeft FINAL)
    Q_PROPERTY(int right READ right WRITE setRight FINAL)
    Q_PROPERTY(int top READ top WRITE setTop FINAL)
    Q_PROPERTY(int bottom READ bottom WRITE setBottom FINAL)
    Q_GADGET
    QML_ANONYMOUS
    QML_FOREIGN(QMargins)
    QML_EXTENDED(QQmlMarginsValueType)
    QML_STRUCTURED_VALUE

public:
    QQmlMarginsValueType() = default;
    Q_INVOKABLE QQmlMarginsValueType(const QMarginsF &margins)
        : m(margins.toMargins())
    {
    }
    int left() const;
    int right() const;
    int top() const;
    int bottom() const;
    void setLeft(int);
    void setRight(int);
    void setTop(int);
    void setBottom(int);

    operator QMargins() const
    {
        return m;
    }
};
#endif
```

**说明：**
- Qt 6.8.1+ 原生支持 `QMargins` 作为 QML 值类型
- 对于低版本，手动提供支持
- 使用 `QML_STRUCTURED_VALUE` 实现结构化值类型

---

## 5. 对比：layer-shell-qt vs DeckShell 当前实现

| 特性 | layer-shell-qt | DeckShell 当前方式 |
|------|----------------|-------------------|
| **QML 集成方式** | Attached Properties | 独立 QML 类型 |
| **代码侵入性** | 低（通过附加属性扩展） | 高（需要包装类） |
| **使用便利性** | 高（直接用 `Window`） | 中（需要自定义组件） |
| **暴露的类型数量** | 1 个（`Window`） | 多个包装类 |
| **维护成本** | 低（只有 `types.h/cpp`） | 高（多个文件） |
| **与 Qt 集成度** | 完美（原生 `QWindow`） | 一般（需要额外类型） |
| **可选性** | 高（去掉附加属性即可） | 低（耦合紧密） |
| **学习曲线** | 低（标准 QML 语法） | 中（需要理解自定义类型） |

---

## 6. 适用于 DeckShell 的启示

### 6.1 推荐的 QML 使用方式

```qml
import org.deepin.deckshell 1.0

Window {
    visible: true

    // DeckShell 附加属性
    DeckShell.Surface.skipMultitaskView: true
    DeckShell.Surface.skipSwitcher: true
    DeckShell.Surface.skipTaskbar: false
    DeckShell.Surface.windowType: DeckShell.Surface.TypePanel
}
```

### 6.2 实现步骤

#### 步骤 1：创建 `declarative` 目录

```
examples/test_skip_multitaskview_window/
├── declarative/
│   ├── CMakeLists.txt
│   ├── types.h
│   └── types.cpp
```

#### 步骤 2：定义 QML 类型绑定

**`types.h`**:
```cpp
#ifndef DECKSHELL_QML_TYPES_H
#define DECKSHELL_QML_TYPES_H

#include "../dshellsurface.h"
#include <qqml.h>

QML_DECLARE_TYPEINFO(DShellSurface, QML_HAS_ATTACHED_PROPERTIES)

class DShellSurfaceForeign
{
    Q_GADGET
    QML_NAMED_ELEMENT(Surface)
    QML_FOREIGN(DShellSurface)
    QML_UNCREATABLE("")
    QML_ATTACHED(DShellSurface)
};

#endif
```

**`types.cpp`**:
```cpp
#include "types.h"
// 实现文件可以为空，或者包含额外的辅助函数
```

#### 步骤 3：修改 `DShellSurface` 类

在 `dshellsurface.h` 中添加：

```cpp
class DShellSurface : public QObject
{
    Q_OBJECT
    Q_PROPERTY(bool skipMultitaskView READ skipMultitaskView WRITE setSkipMultitaskView NOTIFY skipMultitaskViewChanged)
    // ... 其他属性 ...

public:
    // ... 现有方法 ...

    // 关键：QML Attached Properties 接口
    static DShellSurface *qmlAttachedProperties(QObject *object);

Q_SIGNALS:
    void skipMultitaskViewChanged();
    // ... 其他信号 ...
};
```

在 `dshellsurface.cpp` 中实现：

```cpp
DShellSurface *DShellSurface::qmlAttachedProperties(QObject *object)
{
    QWindow *window = qobject_cast<QWindow *>(object);
    if (!window) {
        return nullptr;
    }
    return get(window);  // 使用现有的 get 方法
}
```

#### 步骤 4：配置 CMake

**`declarative/CMakeLists.txt`**:
```cmake
ecm_add_qml_module(DeckShellQml
                  URI "org.deepin.deckshell"
                  VERSION 1.0
                  SOURCES types.h types.cpp
                  GENERATE_PLUGIN_SOURCE)
target_link_libraries(DeckShellQml PRIVATE Qt::Qml DShellSurfaceLib)

ecm_finalize_qml_module(DeckShellQml DESTINATION ${KDE_INSTALL_QMLDIR})
```

### 6.3 关键改造点

1. **保持 C++ API 不变**：`DShellSurface` 继续作为独立的 C++ 类使用
2. **添加 QML 绑定层**：通过 `declarative/types.h` 暴露给 QML
3. **实现 `qmlAttachedProperties`**：连接 QML 和 C++ 的桥梁
4. **使用单例模式**：确保每个 `QWindow` 只有一个 `DShellSurface` 对象

---

## 7. 实现架构图

```
┌─────────────────────────────────────────────────────────────┐
│  QML 层                                                      │
│  import org.kde.layershell                                  │
│  Window { LayerShell.Window.layer: LayerOverlay }          │
└────────────────────────┬────────────────────────────────────┘
                         │ Attached Properties 机制
                         │ Qt 调用 qmlAttachedProperties()
┌────────────────────────▼────────────────────────────────────┐
│  declarative/types.h                                        │
│  ┌────────────────────────────────────────────────────┐    │
│  │ class WindowForeign {                              │    │
│  │     Q_GADGET                                       │    │
│  │     QML_NAMED_ELEMENT(Window)                      │    │
│  │     QML_FOREIGN(LayerShellQt::Window)              │    │
│  │     QML_UNCREATABLE("")                            │    │
│  │     QML_ATTACHED(LayerShellQt::Window)             │    │
│  │ };                                                 │    │
│  └────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │ 调用 Window::qmlAttachedProperties()
┌────────────────────────▼────────────────────────────────────┐
│  interfaces/window.h/cpp                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │ class Window : public QObject {                    │    │
│  │     Q_OBJECT                                       │    │
│  │     Q_PROPERTY(...)                                │    │
│  │     Q_ENUM(Layer)                                  │    │
│  │     Q_FLAG(Anchors)                                │    │
│  │                                                     │    │
│  │     static Window *get(QWindow *);                 │    │
│  │     static Window *qmlAttachedProperties(...);     │    │
│  │ };                                                 │    │
│  │                                                     │    │
│  │ static QMap<QWindow *, Window *> s_map;            │    │
│  └────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │ 设置 Shell Integration
                         │ waylandWindow->setShellIntegration()
┌────────────────────────▼────────────────────────────────────┐
│  qwaylandlayershellintegration.cpp                          │
│  底层 Wayland 协议实现                                      │
│  - zwlr_layer_shell_v1                                      │
│  - zwlr_layer_surface_v1                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. 关键技术点总结

### 8.1 Qt QML 机制

1. **`QML_FOREIGN`**：暴露现有 C++ 类给 QML，无需修改原类
2. **`QML_ATTACHED`**：声明类型作为附加属性使用
3. **`QML_UNCREATABLE`**：防止直接创建实例
4. **`qmlAttachedProperties(QObject *)`**：静态方法，返回附加属性对象

### 8.2 设计模式

1. **Facade 模式**：`Window` 类封装底层 Wayland 交互
2. **Singleton 模式**：全局 map 管理 `Window` 对象
3. **Lazy Initialization**：只在需要时创建 `Window` 对象

### 8.3 最佳实践

1. **最小化暴露**：只需 `types.h/cpp` 两个文件
2. **保持分离**：QML 支持作为可选模块，不影响 C++ API
3. **版本兼容**：条件编译支持不同 Qt 版本
4. **错误处理**：完善的日志和错误检查

---

## 9. 代码文件清单

| 文件路径 | 作用 | 代码行数 |
|---------|------|---------|
| `declarative/types.h` | QML 类型绑定定义 | 56 |
| `declarative/types.cpp` | QML 类型实现（仅兼容代码） | 50 |
| `declarative/CMakeLists.txt` | QML 模块构建配置 | 12 |
| `interfaces/window.h` | 核心 Window 类定义 | 158 |
| `interfaces/window.cpp` | 核心 Window 类实现 | 229 |
| **总计** | | **505** |

仅用约 500 行代码即可实现完整的 QML 支持！

---

## 10. 参考资源

1. **Qt 文档**：
   - [QML Object Attributes](https://doc.qt.io/qt-6/qtqml-syntax-objectattributes.html)
   - [Defining QML Types from C++](https://doc.qt.io/qt-6/qtqml-cppintegration-definetypes.html)
   - [QML_ATTACHED](https://doc.qt.io/qt-6/qqmlengine.html#QML_ATTACHED)

2. **layer-shell-qt 项目**：
   - [GitHub Repository](https://github.com/KDE/layer-shell-qt)
   - [API Documentation](https://api.kde.org/layer-shell-qt/html/)

3. **相关协议**：
   - [wlr-layer-shell-unstable-v1](https://wayland.app/protocols/wlr-layer-shell-unstable-v1)

---

## 11. 结论

layer-shell-qt 的 QML 实现展示了一种优雅、低侵入性的设计模式，通过 Qt 的 Attached Properties 机制实现了：

1. ✅ **非侵入性集成**：不修改原有 C++ 类结构
2. ✅ **最小化代码**：只需少量文件即可实现 QML 支持
3. ✅ **保持灵活性**：C++ 和 QML 可独立使用
4. ✅ **易于维护**：清晰的职责分离
5. ✅ **符合 Qt 最佳实践**：使用标准 Qt 机制

**这种实现方式非常适合 DeckShell 项目采用，建议参考其设计进行重构。**

---

*本文档由 Claude Code 生成，基于对 layer-shell-qt 项目的源码分析。*
