# Treeland 架构图表

## 1. 整体架构图

```mermaid
graph TB
    subgraph "用户界面层"
        QML[QML界面文件]
        UI[用户界面组件]
    end

    subgraph "业务逻辑层"
        TREELAND[Treeland 主控制器]
        HELPER[Helper 辅助类]
        QMLENGINE[QmlEngine]
        WORKSPACE[Workspace]
    end

    subgraph "功能模块层"
        CAPTURE[Capture 模块]
        PERSONALIZATION[Personalization 模块]
        WINDOW_MGMT[Window Management 模块]
        SHORTCUT[Shortcut 模块]
        WALLPAPER[Wallpaper 模块]
        FOREIGN_TOPLEVEL[Foreign Toplevel 模块]
    end

    subgraph "插件系统"
        LOCKSCREEN[LockScreen 插件]
        MULTITASKVIEW[MultitaskView 插件]
        OTHER_PLUGINS[...其他插件]
    end

    subgraph "基础设施层"
        WAYLAND[Wayland 协议]
        DBUS[D-Bus 系统]
        QT[Qt 框架]
        WLROOTS[wlroots 库]
    end

    QML --> QMLENGINE
    QMLENGINE --> TREELAND
    TREELAND --> HELPER
    TREELAND --> WORKSPACE
    TREELAND --> CAPTURE
    TREELAND --> PERSONALIZATION
    TREELAND --> WINDOW_MGMT
    TREELAND --> SHORTCUT
    TREELAND --> WALLPAPER
    TREELAND --> FOREIGN_TOPLEVEL

    TREELAND --> LOCKSCREEN
    TREELAND --> MULTITASKVIEW
    TREELAND --> OTHER_PLUGINS

    HELPER --> WAYLAND
    CAPTURE --> WAYLAND
    PERSONALIZATION --> WAYLAND
    WINDOW_MGMT --> WAYLAND

    TREELAND --> DBUS
    HELPER --> QT
    QMLENGINE --> QT
    WAYLAND --> WLROOTS
```

## 2. 类继承关系图

```mermaid
classDiagram
    class QObject {
        +signal()
        +slot()
    }

    class QDBusContext {
        +connection()
        +message()
        +serviceUid()
    }

    class TreelandProxyInterface {
        +qmlEngine()* QmlEngine
        +workspace()* Workspace
        +rootSurfaceContainer()* RootSurfaceContainer
        +blockActivateSurface(bool)
        +isBlockActivateSurface()* bool
    }

    class BasePluginInterface {
        +~BasePluginInterface()
    }

    class PluginInterface {
        +initialize(TreelandProxyInterface*)
        +shutdown()
        +name()* QString
        +description()* QString
        +enabled()* bool
    }

    class ILockScreen {
        +createLockScreen(Output*, QQuickItem*)* QQuickItem
    }

    class IMultitaskView {
        +setStatus(Status)
        +toggleMultitaskView(ActiveReason)
        +immediatelyExit()
    }

    class Treeland {
        +debugMode()* bool
        +ActivateWayland(QDBusUnixFileDescriptor)* bool
        +XWaylandName()* QString
        -d_ptr TreelandPrivate*
    }

    class LockScreenPlugin {
        +initialize(TreelandProxyInterface*)
        +shutdown()
        +name()* QString
        +description()* QString
        +enabled()* bool
        +createLockScreen(Output*, QQuickItem*)* QQuickItem
    }

    class MultitaskViewPlugin {
        +initialize(TreelandProxyInterface*)
        +shutdown()
        +name()* QString
        +description()* QString
        +enabled()* bool
        +setStatus(Status)
        +toggleMultitaskView(ActiveReason)
        +immediatelyExit()
    }

    QObject <|-- Treeland
    QDBusContext <|-- Treeland
    TreelandProxyInterface <|-- Treeland

    BasePluginInterface <|-- PluginInterface
    PluginInterface <|-- LockScreenPlugin
    PluginInterface <|-- MultitaskViewPlugin

    BasePluginInterface <|-- ILockScreen
    BasePluginInterface <|-- IMultitaskView

    ILockScreen <|-- LockScreenPlugin
    IMultitaskView <|-- MultitaskViewPlugin
```

## 3. 模块架构图

```mermaid
graph TB
    subgraph "Capture 模块"
        CAPTURE_MGR[CaptureManagerV1]
        CAPTURE_CTX[CaptureContextV1]
        CAPTURE_SRC[CaptureSource]
        CAPTURE_SRC_OUTPUT[CaptureSourceOutput]
        CAPTURE_SRC_WINDOW[CaptureSourceSurface]
        CAPTURE_SRC_REGION[CaptureSourceRegion]
        CAPTURE_SELECTOR[CaptureSourceSelector]
    end

    subgraph "Personalization 模块"
        PERS_MGR[PersonalizationManager]
        APPEARANCE_IMPL[AppearanceImpl]
        FONT_IMPL[FontImpl]
        PERS_MGR_IMPL[PersonalizationManagerImpl]
    end

    subgraph "Window Management 模块"
        WIN_MGR[WindowManagement]
        WIN_MGR_IMPL[WindowManagementImpl]
    end

    CAPTURE_MGR --> CAPTURE_CTX
    CAPTURE_CTX --> CAPTURE_SRC
    CAPTURE_SRC --> CAPTURE_SRC_OUTPUT
    CAPTURE_SRC --> CAPTURE_SRC_WINDOW
    CAPTURE_SRC --> CAPTURE_SRC_REGION
    CAPTURE_MGR --> CAPTURE_SELECTOR

    PERS_MGR --> APPEARANCE_IMPL
    PERS_MGR --> FONT_IMPL
    PERS_MGR --> PERS_MGR_IMPL

    WIN_MGR --> WIN_MGR_IMPL
```

## 4. 数据流图

```mermaid
flowchart TD
    A[用户输入] --> B[Input 模块]
    B --> C[Seat 模块]
    C --> D[Helper 类]

    D --> E[Treeland 主控制器]
    E --> F{功能分发}

    F --> G[Capture 模块]
    F --> H[Personalization 模块]
    F --> I[Window Management 模块]
    F --> J[其他模块]

    G --> K[Wayland 协议处理]
    H --> K
    I --> K
    J --> K

    E --> L[QmlEngine]
    L --> M[QML 界面渲染]

    E --> N[插件系统]
    N --> O[LockScreen 插件]
    N --> P[MultitaskView 插件]

    E --> Q[D-Bus 接口]
    Q --> R[系统服务调用]

    K --> S[wlroots 后端]
    S --> T[硬件渲染]

    M --> U[显示输出]
    T --> U
```

## 5. 插件加载流程图

```mermaid
flowchart TD
    A[启动 Treeland] --> B[扫描插件目录]
    B --> C{找到插件文件?}

    C -->|是| D[创建 QPluginLoader]
    C -->|否| F[完成加载]

    D --> E{加载成功?}
    E -->|是| G[创建插件实例]
    E -->|否| H[记录错误]

    G --> I{实现 PluginInterface?}
    I -->|是| J[调用 initialize()]
    I -->|否| K[记录错误]

    J --> L{是 LockScreen 插件?}
    L -->|是| M[注册 ILockScreen]
    L -->|否| N{是 MultitaskView 插件?}

    N -->|是| O[注册 IMultitaskView]
    N -->|否| P[注册为通用插件]

    M --> Q[连接插件信号]
    O --> Q
    P --> Q

    Q --> R[设置插件翻译]
    R --> S[添加到插件列表]
    S --> B

    H --> B
    K --> B
```

## 6. 组件依赖图

```mermaid
graph TD
    subgraph "核心依赖"
        TREELAND_CORE[Treeland 核心]
        QML_ENGINE[QmlEngine]
        HELPER_CORE[Helper]
        WORKSPACE_CORE[Workspace]
    end

    subgraph "界面组件"
        QML_COMPONENTS[QML 组件]
        SURFACE_CONTAINERS[表面容器]
        WINDOW_PICKER[窗口选择器]
    end

    subgraph "功能模块"
        CAPTURE_MOD[Capture]
        PERS_MOD[Personalization]
        WIN_MOD[Window Management]
        SHORTCUT_MOD[Shortcut]
        WALLPAPER_MOD[Wallpaper]
    end

    subgraph "系统集成"
        DBUS_INTEGRATION[D-Bus]
        WAYLAND_INTEGRATION[Wayland]
        X11_INTEGRATION[X11 兼容]
    end

    subgraph "外部库"
        QT_FRAMEWORK[Qt 框架]
        WLROOTS_LIB[wlroots]
        SYSTEM_LIBS[系统库]
    end

    TREELAND_CORE --> QML_ENGINE
    TREELAND_CORE --> HELPER_CORE
    TREELAND_CORE --> WORKSPACE_CORE

    QML_ENGINE --> QML_COMPONENTS
    HELPER_CORE --> SURFACE_CONTAINERS
    HELPER_CORE --> WINDOW_PICKER

    TREELAND_CORE --> CAPTURE_MOD
    TREELAND_CORE --> PERS_MOD
    TREELAND_CORE --> WIN_MOD
    TREELAND_CORE --> SHORTCUT_MOD
    TREELAND_CORE --> WALLPAPER_MOD

    TREELAND_CORE --> DBUS_INTEGRATION
    HELPER_CORE --> WAYLAND_INTEGRATION
    HELPER_CORE --> X11_INTEGRATION

    QML_ENGINE --> QT_FRAMEWORK
    WAYLAND_INTEGRATION --> WLROOTS_LIB
    DBUS_INTEGRATION --> QT_FRAMEWORK
    TREELAND_CORE --> SYSTEM_LIBS
```

## 7. 生命周期图

```mermaid
stateDiagram-v2
    [*] --> 初始化
    初始化 --> 加载配置
    加载配置 --> 创建QmlEngine
    创建QmlEngine --> 初始化Helper
    初始化Helper --> 注册DBus服务
    注册DBus服务 --> 加载插件
    加载插件 --> 运行主循环

    运行主循环 --> 处理事件
    处理事件 --> 运行主循环

    运行主循环 --> 接收关闭信号
    接收关闭信号 --> 清理插件
    清理插件 --> 销毁Helper
    销毁Helper --> 销毁QmlEngine
    销毁QmlEngine --> [*]
```

## 8. 通信模式图

```mermaid
graph TD
    subgraph "同步通信"
        SIGNAL_SLOT[信号槽机制]
        DIRECT_CALL[直接方法调用]
        PROPERTY_BINDING[属性绑定]
    end

    subgraph "异步通信"
        DBUS_MESSAGE[D-Bus 消息]
        WAYLAND_PROTOCOL[Wayland 协议]
        QPROCESS[进程间通信]
    end

    subgraph "事件驱动"
        WAYLAND_EVENTS[Wayland 事件]
        QT_EVENTS[Qt 事件]
        TIMER_EVENTS[定时器事件]
    end

    SIGNAL_SLOT --> TREELAND[Treeland]
    DIRECT_CALL --> TREELAND
    PROPERTY_BINDING --> QML_ENGINE[QmlEngine]

    DBUS_MESSAGE --> TREELAND
    WAYLAND_PROTOCOL --> MODULES[功能模块]
    QPROCESS --> HELPER[Helper]

    WAYLAND_EVENTS --> INPUT_MODULE[Input 模块]
    QT_EVENTS --> UI_COMPONENTS[UI 组件]
    TIMER_EVENTS --> ANIMATION_SYSTEM[动画系统]
```

---

*图表说明：以上图表基于代码分析绘制，展示了Treeland项目的整体架构、类关系、数据流和通信模式。实际实现可能因运行时条件而有所不同。*