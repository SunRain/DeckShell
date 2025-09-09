# ShellHandler 移植实现指南

## 概述

本文档提供了将 ShellHandler 功能移植到 Compositor 项目的具体实现步骤和代码示例。

## 移植后的架构

### 增强的 Helper 类

移植后，Helper 类将包含以下新增功能：

```cpp
class Helper : public WSeatEventFilter {
    // ... 现有成员

private:
    // 新增的 ShellHandler 功能
    void handleDdeShellSurfaceAdded(WSurface *surface, SurfaceWrapper *wrapper);
    void setResourceManagerAtom(WXWayland *xwayland, const QByteArray &value);
    void setupSurfaceActiveWatcher(SurfaceWrapper *wrapper);

    // 新增的成员变量
    QList<WXWayland *> m_xwaylands;
    QObject *m_windowMenu = nullptr;
};
```

## 具体实现

### 1. DDE Shell 协议支持

#### 头文件修改 (helper.h)

```cpp
// 添加必要的包含
#include <xcb/xcb.h>

// 在 private 部分添加新方法声明
private:
    void handleDdeShellSurfaceAdded(WAYLIB_SERVER_NAMESPACE::WSurface *surface,
                                    SurfaceWrapper *wrapper);
    void setResourceManagerAtom(WAYLIB_SERVER_NAMESPACE::WXWayland *xwayland,
                                const QByteArray &value);
    void setupSurfaceActiveWatcher(SurfaceWrapper *wrapper);

    // 新增成员变量
    QList<WAYLIB_SERVER_NAMESPACE::WXWayland *> m_xwaylands;
    QObject *m_windowMenu = nullptr;
```

#### 实现文件修改 (helper.cpp)

```cpp
// 在构造函数中初始化新成员
Helper::Helper(QObject *parent)
    : WSeatEventFilter(parent)
    // ... 现有初始化
    , m_windowMenu(nullptr)
{
    // ... 现有代码
}

// 在 init() 方法中添加 DDE Shell 支持
void Helper::init()
{
    // ... 现有代码

    // 在 XDG 表面添加处理中添加 DDE 检查
    connect(xdgShell, &WXdgShell::toplevelSurfaceAdded, this, [this] (WXdgToplevelSurface *surface) {
        auto wrapper = new SurfaceWrapper(qmlEngine(), surface, SurfaceWrapper::Type::XdgToplevel);

        // 添加 DDE Shell 支持
        if (DDEShellSurfaceInterface::get(surface->surface())) {
            handleDdeShellSurfaceAdded(surface->surface(), wrapper);
        }

        // ... 现有代码
    });

    // 在 XWayland 创建后添加资源管理器设置
    connect(m_xwayland, &WXWayland::ready, this, [this] {
        setResourceManagerAtom(m_xwayland, QString("Xft.dpi:\t%1")
            .arg(96 * m_surfaceContainer->window()->effectiveDevicePixelRatio())
            .toUtf8());
    });

    // ... 现有代码
}
```

### 2. DDE Shell 表面处理实现

```cpp
void Helper::handleDdeShellSurfaceAdded(WSurface *surface, SurfaceWrapper *wrapper)
{
    wrapper->setIsDDEShellSurface(true);
    auto ddeShellSurface = DDEShellSurfaceInterface::get(surface);
    Q_ASSERT(ddeShellSurface);

    auto updateLayer = [ddeShellSurface, wrapper] {
        if (ddeShellSurface->role().value() == DDEShellSurfaceInterface::OVERLAY)
            wrapper->setSurfaceRole(SurfaceWrapper::SurfaceRole::Overlay);
    };

    if (ddeShellSurface->role().has_value())
        updateLayer();

    connect(ddeShellSurface, &DDEShellSurfaceInterface::roleChanged, this, [updateLayer] {
        updateLayer();
    });

    if (ddeShellSurface->yOffset().has_value())
        wrapper->setAutoPlaceYOffset(ddeShellSurface->yOffset().value());

    connect(ddeShellSurface, &DDEShellSurfaceInterface::yOffsetChanged, this,
            [wrapper](uint32_t offset) {
        wrapper->setAutoPlaceYOffset(offset);
    });

    if (ddeShellSurface->surfacePos().has_value())
        wrapper->setClientRequstPos(ddeShellSurface->surfacePos().value());

    connect(ddeShellSurface, &DDEShellSurfaceInterface::positionChanged, this,
            [wrapper](QPoint pos) {
        wrapper->setClientRequstPos(pos);
    });

    if (ddeShellSurface->skipSwitcher().has_value())
        wrapper->setSkipSwitcher(ddeShellSurface->skipSwitcher().value());

    if (ddeShellSurface->skipDockPreView().has_value())
        wrapper->setSkipDockPreView(ddeShellSurface->skipDockPreView().value());

    if (ddeShellSurface->skipMutiTaskView().has_value())
        wrapper->setSkipMutiTaskView(ddeShellSurface->skipMutiTaskView().value());

    wrapper->setAcceptKeyboardFocus(ddeShellSurface->acceptKeyboardFocus());

    connect(ddeShellSurface, &DDEShellSurfaceInterface::skipSwitcherChanged, this,
            [wrapper](bool skip) {
        wrapper->setSkipSwitcher(skip);
    });
    connect(ddeShellSurface, &DDEShellSurfaceInterface::skipDockPreViewChanged, this,
            [wrapper](bool skip) {
        wrapper->setSkipDockPreView(skip);
    });
    connect(ddeShellSurface, &DDEShellSurfaceInterface::skipMutiTaskViewChanged, this,
            [wrapper](bool skip) {
        wrapper->setSkipMutiTaskView(skip);
    });
    connect(ddeShellSurface, &DDEShellSurfaceInterface::acceptKeyboardFocusChanged, this,
            [wrapper](bool accept) {
        wrapper->setAcceptKeyboardFocus(accept);
    });
}
```

### 3. XWayland 资源管理器设置

```cpp
void Helper::setResourceManagerAtom(WXWayland *xwayland, const QByteArray &value)
{
    auto xcb_conn = xwayland->xcbConnection();
    auto root = xwayland->xcbScreen()->root;
    xcb_change_property(xcb_conn,
                        XCB_PROP_MODE_REPLACE,
                        root,
                        xwayland->atom("RESOURCE_MANAGER"),
                        XCB_ATOM_STRING,
                        8,
                        value.size(),
                        value.constData());
    xcb_flush(xcb_conn);
}
```

### 4. 增强的表面激活逻辑

```cpp
void Helper::setupSurfaceActiveWatcher(SurfaceWrapper *wrapper)
{
    Q_ASSERT_X(wrapper->container(), Q_FUNC_INFO, "Must setContainer at first!");

    if (wrapper->type() == SurfaceWrapper::Type::XdgPopup) {
        connect(wrapper, &SurfaceWrapper::requestActive, this, [this, wrapper]() {
            auto parent = wrapper->parentSurface();
            while (parent->type() == SurfaceWrapper::Type::XdgPopup) {
                parent = parent->parentSurface();
            }
            if (!parent) {
                qCCritical(qLcShellHandler) << "A new popup without toplevel parent!";
                return;
            }
            if (!parent->showOnWorkspace(m_workspace->current()->id())) {
                qCWarning(qLcShellHandler) << "A popup active, but it's parent not in current workspace!";
                return;
            }
            activeSurface(parent);
        });
    } else if (wrapper->type() == SurfaceWrapper::Type::Layer) {
        connect(wrapper, &SurfaceWrapper::requestActive, this, [this, wrapper]() {
            auto layerSurface = qobject_cast<WLayerSurface *>(wrapper->shellSurface());
            if (layerSurface->keyboardInteractivity() == WLayerSurface::KeyboardInteractivity::None)
                return;

            if (layerSurface->layer() == WLayerSurface::LayerType::Overlay
                || layerSurface->keyboardInteractivity() == WLayerSurface::KeyboardInteractivity::Exclusive)
                activeSurface(wrapper);
        });
    } else { // Xdgtoplevel or X11
        connect(wrapper, &SurfaceWrapper::requestActive, this, [this, wrapper]() {
            if (wrapper->showOnWorkspace(m_workspace->current()->id()))
                activeSurface(wrapper);
            else
                m_workspace->pushActivedSurface(wrapper);
        });

        connect(wrapper, &SurfaceWrapper::requestInactive, this, [this, wrapper]() {
            m_workspace->removeActivedSurface(wrapper);
            activeSurface(m_workspace->current()->latestActiveSurface());
        });
    }
}
```

## CMakeLists.txt 修改

### 添加 XCB 依赖

```cmake
# 在 find_package 部分添加
find_package(PkgConfig REQUIRED)
pkg_search_module(XCB REQUIRED IMPORTED_TARGET xcb)

# 在 target_link_libraries 中添加
target_link_libraries(${TARGET}
    PRIVATE
    # ... 现有库
    PkgConfig::XCB
)
```

## 集成步骤

### 步骤 1: 依赖准备
1. 确保系统中安装了 XCB 开发库
2. 复制必要的 DDE Shell 接口文件到项目中

### 步骤 2: 代码集成
1. 将新增的方法添加到 Helper 类
2. 在 init() 方法中集成新的信号连接
3. 更新现有的表面处理逻辑

### 步骤 3: 编译和测试
1. 重新编译项目
2. 测试 DDE Shell 协议支持
3. 测试 XWayland 资源管理器功能
4. 验证表面激活逻辑

## 测试建议

### 功能测试
1. **DDE Shell 测试**
   - 创建支持 DDE Shell 协议的客户端
   - 验证 skipSwitcher, skipDockPreView 等属性正确设置
   - 测试 OVERLAY 角色处理

2. **XWayland 测试**
   - 启动 X11 应用程序
   - 验证 DPI 设置正确
   - 检查 XSETTINGS 同步

3. **表面激活测试**
   - 测试弹窗激活父窗口
   - 验证 Layer Surface 键盘焦点处理
   - 检查工作区切换时的激活逻辑

### 性能测试
1. 内存使用监控
2. 启动时间测量
3. 表面切换性能测试

## 故障排除

### 常见问题
1. **XCB 依赖缺失**: 确保安装了 libxcb 开发包
2. **DDE Shell 接口缺失**: 需要从 waylib-shared 复制相关接口文件
3. **编译错误**: 检查包含路径和命名空间

### 调试建议
1. 添加详细的日志输出
2. 使用 Wayland 调试工具
3. 监控 XCB 连接状态

---

*实现时间: 2025-09-10*
*实现策略: 增量集成*
*测试状态: 待验证*