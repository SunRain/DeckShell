# DDE Shell Unified Demo

这是一个统一的 DDE Shell 演示示例，展示了两种使用 DDE Shell 的方式。

## 功能特性

### 启动界面 (Launcher)
- 欢迎界面，包含两个选项按钮
- 选择 Widget Demo 或 QML Demo

### Widget Demo
- **实现方式**: 传统 C++ Qt Widgets
- **特点**:
  - 命令式编程风格
  - 使用 Window::get() 获取 DDE Shell 实例
  - 通过按钮动态控制各种属性
  - 监听初始化信号

- **功能**:
  - Toggle Skip Multitask View
  - Toggle Skip Switcher
  - Toggle Skip Dock Preview
  - Toggle Accept Keyboard Focus
  - Set Surface Position

### QML Demo
- **实现方式**: 声明式 QML
- **特点**:
  - 声明式编程风格
  - 使用附加属性 (layer-shell-qt 风格)
  - 属性通过 QML 绑定自动更新
  - 无需手动管理状态

- **功能**:
  - CheckBox 实时控制所有 DDE Shell 属性
  - 属性变化通过绑定自动应用

## 编译

```bash
cmake -S . -B build
cmake --build build --target ddeshell-unified
```

## 运行

```bash
./build/examples/test_skip_multitaskview_window/examples/unified/ddeshell-unified
```

## 文件结构

```
unified/
├── CMakeLists.txt      # 构建配置
├── main.cpp            # 程序入口
├── launcher.h/cpp      # 启动界面
├── widgetdemo.h/cpp    # Widget 演示
└── demo.qml            # QML 演示
```

## 技术对比

| 特性 | Widget Demo | QML Demo |
|------|-------------|----------|
| 编程风格 | 命令式 | 声明式 |
| API 风格 | C++ 方法调用 | QML 附加属性 |
| 状态管理 | 手动管理 | 自动绑定 |
| UI 更新 | 手动更新标签 | 自动响应 |
| 代码量 | 较多 | 较少 |
| 类型安全 | 编译时检查 | 运行时检查 |

## 适用场景

### 使用 Widget Demo (C++ API)
- 需要精细控制的复杂应用
- 已有大量 C++ Widget 代码
- 需要与 C++ 后端紧密集成
- 性能关键应用

### 使用 QML Demo (QML 附加属性)
- 快速原型开发
- UI 为主的应用
- 需要动态 UI 效果
- 团队熟悉 QML

## 协议支持

两种实现方式都完整支持 `treeland_dde_shell_surface_v1` 协议的所有功能：
- skipMultitaskview
- skipSwitcher
- skipDockPreview
- acceptKeyboardFocus
- role
- surfacePosition
- autoPlacement
