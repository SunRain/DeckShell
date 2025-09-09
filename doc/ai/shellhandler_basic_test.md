# ShellHandler基本功能测试用例

## 测试概述

本测试用例用于验证ShellHandler的基本功能是否正常工作，包括：
1. ShellHandler的初始化
2. 表面管理功能
3. DDE Shell扩展支持
4. 与Helper类的集成

## 测试环境

- 操作系统: Linux
- 编译器: GCC/Clang
- 构建系统: CMake
- 依赖库: Qt6, Waylib, DDE Shell

## 测试用例

### 测试用例1: ShellHandler初始化测试

**测试目标**: 验证ShellHandler能够正确初始化

**前置条件**:
- RootSurfaceContainer已创建
- WServer已初始化

**测试步骤**:
1. 创建RootSurfaceContainer实例
2. 创建ShellHandler实例，传入rootContainer
3. 验证ShellHandler的成员变量正确初始化
4. 验证各个surface container正确创建

**预期结果**:
- ShellHandler实例创建成功
- 所有surface container (background, bottom, workspace, top, overlay, popup) 正确初始化
- Z轴顺序正确设置

**测试代码**:
```cpp
void testShellHandlerInitialization() {
    // 创建root container
    auto rootContainer = new RootSurfaceContainer(window->contentItem());

    // 创建ShellHandler
    auto shellHandler = new ShellHandler(rootContainer);

    // 验证初始化
    QVERIFY(shellHandler->workspace() != nullptr);
    QVERIFY(shellHandler->m_backgroundContainer != nullptr);
    QVERIFY(shellHandler->m_bottomContainer != nullptr);
    QVERIFY(shellHandler->m_topContainer != nullptr);
    QVERIFY(shellHandler->m_overlayContainer != nullptr);
    QVERIFY(shellHandler->m_popupContainer != nullptr);

    // 验证Z轴顺序
    QCOMPARE(shellHandler->m_backgroundContainer->z(), RootSurfaceContainer::BackgroundZOrder);
    QCOMPARE(shellHandler->m_bottomContainer->z(), RootSurfaceContainer::BottomZOrder);
    QCOMPARE(shellHandler->m_workspace->z(), RootSurfaceContainer::NormalZOrder);
    QCOMPARE(shellHandler->m_topContainer->z(), RootSurfaceContainer::TopZOrder);
    QCOMPARE(shellHandler->m_overlayContainer->z(), RootSurfaceContainer::OverlayZOrder);
    QCOMPARE(shellHandler->m_popupContainer->z(), RootSurfaceContainer::PopupZOrder);
}
```

### 测试用例2: XDG Shell初始化测试

**测试目标**: 验证ShellHandler能够正确初始化XDG Shell

**前置条件**:
- WServer已创建
- ShellHandler已初始化

**测试步骤**:
1. 创建WServer实例
2. 调用ShellHandler::initXdgShell(server)
3. 验证m_xdgShell正确设置
4. 验证信号连接正确建立

**预期结果**:
- m_xdgShell不为nullptr
- toplevelSurfaceAdded信号连接到onXdgToplevelSurfaceAdded
- toplevelSurfaceRemoved信号连接到onXdgToplevelSurfaceRemoved
- popupSurfaceAdded信号连接到onXdgPopupSurfaceAdded
- popupSurfaceRemoved信号连接到onXdgPopupSurfaceRemoved

### 测试用例3: Layer Shell初始化测试

**测试目标**: 验证ShellHandler能够正确初始化Layer Shell

**前置条件**:
- XDG Shell已初始化

**测试步骤**:
1. 调用ShellHandler::initLayerShell(server)
2. 验证m_layerShell正确设置
3. 验证信号连接正确建立

**预期结果**:
- m_layerShell不为nullptr
- surfaceAdded信号连接到onLayerSurfaceAdded
- surfaceRemoved信号连接到onLayerSurfaceRemoved

### 测试用例4: XWayland创建测试

**测试目标**: 验证ShellHandler能够正确创建XWayland

**前置条件**:
- WServer, WSeat, qw_compositor已创建

**测试步骤**:
1. 调用ShellHandler::createXWayland(server, seat, compositor, false)
2. 验证返回的WXWayland实例不为nullptr
3. 验证XWayland正确添加到m_xwaylands列表
4. 验证Seat设置正确

**预期结果**:
- 返回有效的WXWayland实例
- XWayland实例在m_xwaylands列表中
- Seat正确设置

### 测试用例5: 输入法Helper初始化测试

**测试目标**: 验证ShellHandler能够正确初始化输入法Helper

**前置条件**:
- WServer, WSeat已创建

**测试步骤**:
1. 调用ShellHandler::initInputMethodHelper(server, seat)
2. 验证m_inputMethodHelper正确设置
3. 验证信号连接正确建立

**预期结果**:
- m_inputMethodHelper不为nullptr
- inputPopupSurfaceV2Added信号连接到onInputPopupSurfaceV2Added
- inputPopupSurfaceV2Removed信号连接到onInputPopupSurfaceV2Removed

### 测试用例6: DDE Shell表面处理测试

**测试目标**: 验证ShellHandler能够正确处理DDE Shell表面

**前置条件**:
- SurfaceWrapper已创建
- DDE Shell表面接口可用

**测试步骤**:
1. 创建SurfaceWrapper实例
2. 调用ShellHandler::handleDdeShellSurfaceAdded(surface, wrapper)
3. 验证DDE Shell属性正确设置
4. 验证信号连接正确建立

**预期结果**:
- wrapper标记为DDE Shell表面
- 角色变化信号正确连接
- Y偏移变化信号正确连接
- 位置变化信号正确连接
- 跳过属性变化信号正确连接

### 测试用例7: 表面激活监控测试

**测试目标**: 验证ShellHandler能够正确设置表面激活监控

**前置条件**:
- SurfaceWrapper已创建并设置容器

**测试步骤**:
1. 创建SurfaceWrapper实例
2. 设置其容器
3. 调用ShellHandler::setupSurfaceActiveWatcher(wrapper)
4. 验证requestActive信号连接正确
5. 验证requestInactive信号连接正确

**预期结果**:
- 根据表面类型正确设置激活行为
- Layer表面设置alwaysOnTop属性
- XDG/Popup表面连接到Helper的激活方法

### 测试用例8: 窗口菜单设置测试

**测试目标**: 验证ShellHandler能够正确设置窗口菜单

**前置条件**:
- SurfaceWrapper已创建
- 窗口菜单已创建

**测试步骤**:
1. 创建SurfaceWrapper实例
2. 调用ShellHandler::setupSurfaceWindowMenu(wrapper)
3. 触发requestShowWindowMenu信号
4. 验证窗口菜单显示方法被调用

**预期结果**:
- requestShowWindowMenu信号正确连接到窗口菜单
- 窗口菜单能够正确显示

## 测试执行

### 自动化测试

使用Qt Test框架创建自动化测试：

```cpp
#include <QtTest>
#include <QSignalSpy>

class TestShellHandler : public QObject {
    Q_OBJECT

private slots:
    void initTestCase();
    void cleanupTestCase();

    void testInitialization();
    void testXdgShellInit();
    void testLayerShellInit();
    void testXWaylandCreation();
    void testInputMethodInit();
    void testDdeShellHandling();
    void testSurfaceActiveWatcher();
    void testWindowMenuSetup();
};
```

### 手动测试

1. 编译项目确保无错误
2. 运行自动化测试套件
3. 检查测试覆盖率
4. 验证所有测试用例通过

## 测试结果记录

| 测试用例 | 状态 | 结果 | 备注 |
|---------|------|------|------|
| 初始化测试 | ⏳ | 待执行 | - |
| XDG Shell初始化 | ⏳ | 待执行 | - |
| Layer Shell初始化 | ⏳ | 待执行 | - |
| XWayland创建 | ⏳ | 待执行 | - |
| 输入法Helper初始化 | ⏳ | 待执行 | - |
| DDE Shell表面处理 | ⏳ | 待执行 | - |
| 表面激活监控 | ⏳ | 待执行 | - |
| 窗口菜单设置 | ⏳ | 待执行 | - |

## 问题记录

如果测试中发现问题，请记录在此处：

1. **问题描述**:
   - 发现时间:
   - 影响范围:
   - 解决建议:

2. **问题描述**:
   - 发现时间:
   - 影响范围:
   - 解决建议:

---

**测试用例创建时间**: 2025-09-12
**测试状态**: 📝 已创建，待执行