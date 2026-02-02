# Gamepad Test Suite - 综合测试工具

一个功能完整的Treeland Gamepad Wayland协议客户端示例程序，集成了监控、可视化、振动测试、示例游戏和输入映射等多种功能。

## 功能模块

### 1. 事件监视器 (Event Monitor)
- 实时显示所有手柄输入事件
- 支持时间戳和原始数据显示
- 事件统计（按钮、轴、方向键事件计数）
- 日志保存功能

### 2. 可视化 (Visualizer)
- 图形化显示手柄布局
- 实时显示按钮状态（按下/释放）
- 摇杆位置可视化
- 扳机键进度条
- 方向键8方向指示

### 3. 振动测试 (Vibration Test)
- 预设振动模式（轻触、中等、强烈等）
- 自定义振动参数（强度、持续时间）
- 振动序列编辑器
- 双马达独立控制

### 4. 示例游戏 (Simple Game)
- 2D射击游戏演示
- 左摇杆控制移动
- 右扳机或A键射击
- 碰撞振动反馈
- 得分和生命系统

### 5. 输入映射 (Input Mapper)
- 手柄按钮到键盘按键映射
- 预设映射配置
- 自定义映射规则
- 映射启用/禁用控制

## 编译

```bash
cd /home/wangguojian/Project/sde-project/DeckShell/build
make gamepad-test-suite
```

## 运行

### 基本运行
```bash
./lib/gamepad/examples/gamepad-test-suite/gamepad-test-suite
```

### 带参数运行
```bash
# 启用调试输出
./gamepad-test-suite --debug

# 指定Wayland socket
./gamepad-test-suite --socket wayland-1

# 查看帮助
./gamepad-test-suite --help
```

## 使用说明

### 连接手柄
1. 程序启动后会自动尝试连接到Wayland compositor
2. 如果自动连接失败，使用菜单"设备 > 连接到Compositor"手动连接
3. 连接成功后，顶部会显示"已连接"状态

### 设备选择
- 使用顶部的设备选择下拉框切换当前活动设备
- 支持多个手柄同时连接
- 设备热插拔自动检测

### 功能切换
- 使用标签页切换不同功能模块
- 每个模块独立运行，可同时使用多个功能

### 快捷键
- F5: 刷新设备列表
- Ctrl+Q: 退出程序

## 代码结构

```
gamepad-test-suite/
├── main.cpp                  # 程序入口
├── gamepadtestsuite.h/cpp   # 主窗口类
├── monitorwidget.h/cpp      # 事件监视器模块
├── visualizerwidget.h/cpp   # 可视化模块
├── vibrationwidget.h/cpp    # 振动测试模块
├── simplegamewidget.h/cpp   # 示例游戏模块
├── inputmapperwidget.h/cpp  # 输入映射模块
└── CMakeLists.txt           # 构建配置
```

## API使用示例

### 初始化客户端
```cpp
TreelandGamepad::TreelandGamepadClient *client = 
    new TreelandGamepad::TreelandGamepadClient(this);

if (!client->connectToCompositor()) {
    qWarning() << "Failed to connect";
}
```

### 处理设备事件
```cpp
connect(client, &TreelandGamepadClient::gamepadAdded,
    [](int deviceId, const QString &name) {
        qDebug() << "Device added:" << name;
    });
```

### 获取设备状态
```cpp
TreelandGamepadDevice *device = client->gamepad(deviceId);
if (device) {
    bool aPressed = device->isButtonPressed(Button_A);
    double leftX = device->axisValue(Axis_LeftX);
}
```

### 控制振动
```cpp
// 设置振动（弱马达50%，强马达100%，持续1秒）
device->setVibration(0.5, 1.0, 1000);

// 停止振动
device->stopVibration();
```

## 扩展开发

这个示例程序展示了如何：
1. 连接到Wayland compositor
2. 管理多个手柄设备
3. 处理各种输入事件
4. 实现振动反馈
5. 创建游戏应用
6. 映射输入到其他操作

可以基于此代码进行扩展，开发更复杂的应用程序。

## 故障排除

### 无法连接到compositor
- 确保compositor支持`treeland-gamepad-v1`协议
- 检查是否有权限访问Wayland socket
- 尝试指定socket名称：`--socket wayland-0`

### 设备未检测到
- 确保手柄已正确连接到系统
- 检查`/dev/input/`下是否有对应的设备节点
- 确认compositor已正确识别设备

### 振动不工作
- 并非所有手柄都支持振动
- 检查手柄驱动是否支持force feedback
- 确认compositor已启用振动支持

## 许可证

Copyright (C) 2025 UnionTech Software Technology Co., Ltd.

Licensed under Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
