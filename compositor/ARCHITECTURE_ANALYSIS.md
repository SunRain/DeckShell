# TinyWL 架构分析报告

## 项目概述

TinyWL 是基于 Wayland 协议的 Qt Quick 合成器示例实现，展示了 C++/QML 混合架构在现代桌面环境中的应用。

## 程序架构

### 核心组件层次结构

```
TinyWL (Qt Quick Wayland Compositor)
├── C++ 层 (Backend & Logic)
│   ├── Helper - 系统管理与初始化
│   ├── QmlEngine - QML 组件工厂
│   ├── SurfaceWrapper - 窗口包装器
│   ├── Output - 输出设备管理
│   └── Workspace - 工作区管理
│
└── QML 层 (UI & Visual)
    ├── PrimaryOutput.qml - 主输出显示
    ├── Decoration.qml - 窗口装饰
    ├── TitleBar.qml - 标题栏
    ├── SurfaceContent.qml - 窗口内容
    └── 其他 UI 组件
```

## 启动流程分析

### 1. 程序入口 (main.cpp)

```cpp
int main(int argc, char *argv[]) {
    // 1. 初始化渲染后端
    WRenderHelper::setupRendererBackend();

    // 2. 创建 QML 引擎
    QmlEngine qmlEngine;

    // 3. 获取 Helper 单例并初始化
    Helper *helper = qmlEngine.singletonInstance<Helper*>("Tinywl", "Helper");
    helper->init();

    // 4. 启动事件循环
    return app.exec();
}
```

### 2. 系统初始化 (Helper::init())

```cpp
void Helper::init() {
    // 1. 设置 QML 上下文
    m_surfaceContainer->setQmlEngine(engine);

    // 2. 初始化服务器组件
    m_server->start();
    m_renderer = WRenderHelper::createRenderer(m_backend->handle());

    // 3. 设置输出设备监听
    connect(m_backend, &WBackend::outputAdded, this, [this] (WOutput *output) {
        Output *o = Output::createPrimary(output, qmlEngine(), this);
        m_outputList.append(o);
    });

    // 4. 设置 Wayland 协议处理
    auto *xdgShell = m_server->attach<WXdgShell>(5);
    connect(xdgShell, &WXdgShell::toplevelSurfaceAdded, this, [this] (WXdgToplevelSurface *surface) {
        auto wrapper = new SurfaceWrapper(qmlEngine(), surface, SurfaceWrapper::Type::XdgToplevel);
        m_workspace->addSurface(wrapper);
    });
}
```

## QML 组件创建机制

### QmlEngine 类分析

QmlEngine 作为 QML 组件的统一工厂，预注册了所有可用的 QML 组件：

```cpp
QmlEngine::QmlEngine(QObject *parent)
    : QQmlApplicationEngine(parent)
    , titleBarComponent(this, "Tinywl", "TitleBar")
    , decorationComponent(this, "Tinywl", "Decoration")
    , windowMenuComponent(this, "Tinywl", "WindowMenu")
    , taskBarComponent(this, "Tinywl", "TaskBar")
    , surfaceContent(this, "Tinywl", "SurfaceContent")
    // ... 其他组件
{
}
```

### 组件创建方法

```cpp
QQuickItem *QmlEngine::createTitleBar(SurfaceWrapper *surface, QQuickItem *parent) {
    auto context = qmlContext(parent);
    auto obj = titleBarComponent.beginCreate(context);
    titleBarComponent.setInitialProperties(obj, {
        {"surface", QVariant::fromValue(surface)}
    });
    auto item = qobject_cast<QQuickItem*>(obj);
    item->setParent(parent);
    item->setParentItem(parent);
    titleBarComponent.completeCreate();
    return item;
}
```

## QML 文件调用关系详解

### 1. PrimaryOutput.qml

**调用路径:**
```
Helper::init() → WBackend::outputAdded → Output::createPrimary() → QQmlComponent("Tinywl", "PrimaryOutput")
```

**功能:**
- 主输出显示区域管理
- 光标渲染 (Cursor.qml)
- 壁纸显示 (Wallpaper.qml)
- 输出视口控制 (OutputViewport)

**关键属性:**
```qml
OutputItem {
    cursorDelegate: Cursor { ... }
    OutputViewport { id: outputViewport }
    Wallpaper { id: wallpaper }
}
```

### 2. CopyOutput.qml

**调用路径:**
```
Helper::init() → WBackend::outputAdded → Output::createCopy() → QQmlComponent("Tinywl", "CopyOutput")
```

**功能:**
- 副屏幕输出显示
- 主屏幕内容复制显示
- 支持旋转和缩放变换

### 3. Decoration.qml

**调用路径:**
```
SurfaceWrapper::setNoDecoration() → QmlEngine::createDecoration() → QQmlComponent("Tinywl", "Decoration")
```

**功能:**
- 窗口装饰管理
- 鼠标事件处理（调整大小）
- 阴影效果 (Shadow.qml)
- 边框效果 (Border.qml)

**关键代码:**
```qml
Item {
    MouseArea {
        onPressed: function (event) {
            if (edges) surface.requestResize(edges)
        }
    }

    Shadow { id: shadow }
    Border { visible: surface.visibleDecoration }
}
```

### 4. TitleBar.qml

**调用路径:**
```
SurfaceWrapper::updateTitleBar() → QmlEngine::createTitleBar() → QQmlComponent("Tinywl", "TitleBar")
```

**功能:**
- 窗口标题栏
- 窗口控制按钮（最小化/最大化/关闭）
- 悬停和点击事件处理

**关键组件:**
```qml
Control {
    HoverHandler { ... }
    TapHandler { ... }

    Row {
        ToolButton { text: "🗗"; onClicked: surface.requestMinimize() }
        ToolButton { text: "🗗"; onClicked: surface.requestMaximize() }
        ToolButton { text: "✕"; onClicked: surface.requestClose() }
    }
}
```

### 5. SurfaceContent.qml

**调用路径:**
```
SurfaceWrapper 构造函数 → surfaceItem->setDelegate() → QQmlComponent("Tinywl", "SurfaceContent")
```

**功能:**
- 窗口内容渲染
- 透明度控制
- 圆角裁剪效果 (RoundedClipEffect.qml)

### 6. TaskBar.qml

**调用路径:**
```
Output::createPrimary() → QmlEngine::createTaskBar() → QQmlComponent("Tinywl", "TaskBar")
```

**功能:**
- 任务栏显示
- 最小化窗口缩略图
- 窗口切换功能

### 7. WindowMenu.qml

**调用路径:**
```
Helper::init() → QmlEngine::createWindowMenu() → QQmlComponent("Tinywl", "WindowMenu")
```

**功能:**
- 窗口右键菜单
- 窗口操作选项（移动/调整大小/关闭等）

### 8. WorkspaceSwitcher.qml

**调用路径:**
```
Workspace::switchTo() → QmlEngine::createWorkspaceSwitcher() → QQmlComponent("Tinywl", "WorkspaceSwitcher")
```

**功能:**
- 工作区切换动画
- 工作区预览显示

### 9. GeometryAnimation.qml

**调用路径:**
```
SurfaceWrapper::startStateChangeAnimation() → QmlEngine::createGeometryAnimation() → QQmlComponent("Tinywl", "GeometryAnimation")
```

**功能:**
- 窗口几何变化动画
- 状态切换过渡效果

### 10. OutputMenuBar.qml

**调用路径:**
```
Output::createPrimary() → QmlEngine::createMenuBar() → QQmlComponent("Tinywl", "OutputMenuBar")
```

**功能:**
- 输出控制菜单
- 缩放、旋转、工作区管理

## SurfaceWrapper 类详解

SurfaceWrapper 是 C++ 和 QML 之间的核心桥梁：

### 构造函数分析

```cpp
SurfaceWrapper::SurfaceWrapper(QmlEngine *qmlEngine, WToplevelSurface *shellSurface, Type type, QQuickItem *parent)
    : QQuickItem(parent)
    , m_engine(qmlEngine)
    , m_shellSurface(shellSurface)
    , m_type(type)
{
    // 1. 创建对应的 SurfaceItem
    switch (type) {
    case Type::XdgToplevel:
        m_surfaceItem = new WXdgToplevelSurfaceItem(this);
        break;
    // ... 其他类型
    }

    // 2. 设置 QML 上下文
    QQmlEngine::setContextForObject(this, qmlEngine->rootContext());
    QQmlEngine::setContextForObject(m_surfaceItem, qmlEngine->rootContext());

    // 3. 设置 SurfaceContent 作为 delegate
    m_surfaceItem->setDelegate(qmlEngine->surfaceContentComponent());

    // 4. 连接信号
    shellSurface->safeConnect(&WToplevelSurface::requestMaximize, this, &SurfaceWrapper::requestMaximize);
    // ... 其他信号连接
}
```

### QML 组件管理

```cpp
void SurfaceWrapper::setNoDecoration(bool newNoDecoration) {
    if (m_noDecoration == newNoDecoration)
        return;

    m_noDecoration = newNoDecoration;
    if (m_noDecoration) {
        // 销毁装饰组件
        if (m_decoration) {
            m_decoration->deleteLater();
            m_decoration = nullptr;
        }
    } else {
        // 创建装饰组件
        m_decoration = m_engine->createDecoration(this, this);
        m_decoration->stackBefore(m_surfaceItem);
    }
}
```

## 调用关系图

```mermaid
graph TD
    A[main.cpp] --> B[QmlEngine 创建]
    B --> C[Helper 单例获取]
    C --> D[Helper::init()]

    D --> E[输出设备监听]
    E --> F[Output::createPrimary()]
    F --> G[PrimaryOutput.qml]
    F --> H[TaskBar.qml]
    F --> I[OutputMenuBar.qml]

    D --> J[Wayland 协议处理]
    J --> K[XDG 表面添加]
    K --> L[SurfaceWrapper 创建]
    L --> M[SurfaceContent.qml]
    L --> N[Decoration.qml]
    L --> O[TitleBar.qml]

    N --> P[Shadow.qml]
    N --> Q[Border.qml]
    M --> R[RoundedClipEffect.qml]

    L --> S[GeometryAnimation.qml]
    D --> T[WindowMenu.qml]
    D --> U[WorkspaceSwitcher.qml]
```

## 设计特点总结

### 1. 模块化架构
- **C++ 层**: 处理 Wayland 协议、窗口管理、系统集成
- **QML 层**: 处理用户界面、视觉效果、动画

### 2. 动态组件创建
- 根据需要动态创建 QML 组件
- 支持组件的生命周期管理
- 提高内存使用效率

### 3. 统一组件管理
- QmlEngine 作为组件工厂
- 标准化组件创建接口
- 简化组件管理逻辑

### 4. 信号槽通信
- C++ 和 QML 通过信号槽机制通信
- 支持双向数据绑定
- 保持松耦合设计

### 5. 灵活的输出管理
- 支持主屏幕和副本屏幕模式
- 动态输出设备检测
- 硬件加速支持

## 关键集成点

| 组件 | 职责 | 集成方式 |
|------|------|----------|
| Helper | 系统初始化、服务器管理 | 单例模式，QML 单例注册 |
| QmlEngine | QML 组件工厂 | 预注册组件，统一创建接口 |
| SurfaceWrapper | 窗口包装器 | C++/QML 桥梁，组件生命周期管理 |
| Output | 输出设备管理 | 动态组件创建，硬件层集成 |

## 性能优化策略

1. **延迟加载**: QML 组件按需创建
2. **对象池**: 复用常用组件实例
3. **硬件加速**: 利用 GPU 渲染能力
4. **异步处理**: 非阻塞的组件创建和销毁

## 扩展性设计

1. **插件架构**: 支持动态加载新的 QML 组件
2. **协议扩展**: 易于添加新的 Wayland 协议支持
3. **主题系统**: 支持自定义视觉主题
4. **配置系统**: 运行时配置调整

---

*分析时间: 2025-09-04*
*分析工具: Kilo Code Architect Mode*
*项目版本: waylib/examples/tinywl*
