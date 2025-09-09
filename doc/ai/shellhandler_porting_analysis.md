# ShellHandler 移植分析报告

## 项目概述

本文档分析了 `3rdparty/waylib-shared/src-unused/core/shellhandler.h` 和 `shellhandler.cpp` 的功能，并评估将其移植到 `compositor` 项目的可行性和策略。

## ShellHandler 功能分析

### 核心功能

ShellHandler 类是 Wayland 合成器的核心组件，负责：

1. **协议管理**
   - XDG Shell 协议处理
   - Layer Shell 协议处理
   - XWayland 集成
   - 输入法助手管理

2. **表面管理**
   - 表面包装器 (SurfaceWrapper) 创建和管理
   - 表面容器管理 (LayerSurfaceContainer, PopupSurfaceContainer)
   - 工作区管理 (Workspace)

3. **平台特定功能**
   - X11/XWayland 资源管理器设置
   - DDE Shell 协议扩展支持

### 类结构

```cpp
class ShellHandler : public QObject {
public:
    // 初始化方法
    void initXdgShell(WServer *server);
    void initLayerShell(WServer *server);
    WXWayland *createXWayland(WServer *server, WSeat *seat, qw_compositor *compositor, bool lazy);
    void initInputMethodHelper(WServer *server, WSeat *seat);

    // 表面管理
    void onXdgToplevelSurfaceAdded(WXdgToplevelSurface *surface);
    void onLayerSurfaceAdded(WLayerSurface *surface);
    void onXWaylandSurfaceAdded(WXWaylandSurface *surface);

private:
    // 成员变量
    WXdgShell *m_xdgShell = nullptr;
    WLayerShell *m_layerShell = nullptr;
    WInputMethodHelper *m_inputMethodHelper = nullptr;
    QList<WXWayland *> m_xwaylands;
    RootSurfaceContainer *m_rootSurfaceContainer = nullptr;
    Workspace *m_workspace = nullptr;
    // ... 其他容器
};
```

## 与 Compositor 的比较

### 功能重叠分析

| 功能模块 | ShellHandler | Compositor (Helper) | 状态 |
|---------|-------------|-------------------|------|
| XDG Shell 初始化 | ✓ | ✓ | 重叠 |
| Layer Shell 初始化 | ✓ | ✓ | 重叠 |
| XWayland 创建 | ✓ | ✓ | 重叠 |
| 输入法助手 | ✓ | ✓ | 重叠 |
| 表面添加处理 | ✓ | ✓ | 重叠 |
| 容器管理 | ✓ | ✓ | 重叠 |
| 工作区管理 | ✓ | ✓ | 重叠 |

### 独特功能识别

ShellHandler 中有以下独特功能：

1. **DDE Shell 协议支持**
   - `handleDdeShellSurfaceAdded()` 方法
   - DDE 特定的表面角色处理
   - 跳过任务栏/切换器等属性

2. **XWayland 资源管理器设置**
   - `setResourceManagerAtom()` 方法
   - DPI 设置和 XSETTINGS 同步

3. **特定的表面激活逻辑**
   - 弹窗激活时的父窗口激活
   - Layer Surface 的键盘焦点处理

## 移植策略

### 策略选择

鉴于 Compositor 项目已经实现了大部分 ShellHandler 功能，建议采用**增量移植策略**：

1. **不完全替换**: 不将整个 ShellHandler 类移植
2. **功能增强**: 将 ShellHandler 中的独特功能集成到现有的 Helper 类中
3. **模块化移植**: 逐个移植独特功能模块

### 移植计划

#### 阶段 1: DDE Shell 协议支持

**目标**: 将 DDE Shell 协议处理功能移植到 Compositor

**涉及文件**:
- `handleDdeShellSurfaceAdded()` 方法
- DDE Shell 相关的信号连接
- 表面属性设置 (skipSwitcher, skipDockPreView 等)

**移植位置**: 集成到 `Helper::init()` 方法中的 XDG 表面处理部分

#### 阶段 2: XWayland 资源管理器

**目标**: 移植 XWayland 资源管理器设置功能

**涉及文件**:
- `setResourceManagerAtom()` 方法
- XWayland ready 信号处理
- DPI 和 XSETTINGS 设置

**移植位置**: 集成到 `Helper::init()` 方法中的 XWayland 创建部分

#### 阶段 3: 增强的表面激活逻辑

**目标**: 移植 ShellHandler 中更精细的表面激活逻辑

**涉及文件**:
- `setupSurfaceActiveWatcher()` 方法
- 弹窗和 Layer Surface 的特殊激活处理

**移植位置**: 增强现有的 `Helper::activeSurface()` 方法

## 架构适配

### 依赖关系适配

| 原依赖 | Compositor 等价物 | 适配策略 |
|-------|----------------|----------|
| `wglobal.h` | 已通过 Waylib::SharedServer 提供 | 无需修改 |
| `qwglobal.h` | 已通过 Waylib::SharedServer 提供 | 无需修改 |
| `xcb/xcb.h` | 需要添加 XCB 依赖 | 在 CMakeLists.txt 中添加 |
| `DDEShellSurfaceInterface` | 需要移植 DDE Shell 接口 | 从 waylib-shared 复制 |

### 包含路径调整

需要调整的包含路径：
```cmake
# 在 CMakeLists.txt 中添加
find_package(PkgConfig REQUIRED)
pkg_search_module(XCB REQUIRED IMPORTED_TARGET xcb)
target_link_libraries(${TARGET} PRIVATE PkgConfig::XCB)
```

### 类接口适配

Helper 类需要添加以下方法：
```cpp
private:
    void handleDdeShellSurfaceAdded(WSurface *surface, SurfaceWrapper *wrapper);
    void setResourceManagerAtom(WXWayland *xwayland, const QByteArray &value);
    void setupSurfaceActiveWatcher(SurfaceWrapper *wrapper);
```

## 实现步骤

### 步骤 1: 依赖准备
1. 在 CMakeLists.txt 中添加 XCB 依赖
2. 复制必要的 DDE Shell 接口文件
3. 更新包含路径

### 步骤 2: 核心功能移植
1. 将 `handleDdeShellSurfaceAdded()` 方法移植到 Helper 类
2. 将 `setResourceManagerAtom()` 方法移植到 Helper 类
3. 增强 `activeSurface()` 方法以支持 ShellHandler 的激活逻辑

### 步骤 3: 信号连接更新
1. 在 XDG 表面添加处理中添加 DDE Shell 检查
2. 在 XWayland 创建后添加资源管理器设置
3. 更新表面激活信号处理

### 步骤 4: 测试和验证
1. 编译检查
2. 功能测试
3. 性能测试

## 风险评估

### 技术风险
1. **依赖冲突**: XCB 和现有依赖的兼容性
2. **API 变更**: Waylib 版本差异导致的 API 不兼容
3. **性能影响**: 新增功能对性能的影响

### 缓解措施
1. 仔细检查依赖版本兼容性
2. 在移植过程中保持向后兼容
3. 添加性能监控和测试

## 预期收益

1. **功能增强**: 获得 DDE Shell 协议支持
2. **X11 兼容性**: 更好的 XWayland 集成
3. **用户体验**: 更精细的窗口管理

## 结论

通过增量移植策略，可以安全地将 ShellHandler 中的独特功能集成到 Compositor 项目中，同时避免大规模重构的风险。建议按阶段逐步实施，确保每个阶段的功能稳定后再进行下一阶段。

---

*分析时间: 2025-09-10*
*分析工具: Kilo Code Architect Mode*
*移植策略: 增量移植*