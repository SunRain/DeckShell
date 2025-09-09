# DeckShell Compositor 迁移方案

## 概述

本方案旨在将 `3rdparty/waylib-shared/src-unused/core` 中的高级功能迁移到 `compositor/` 目录，确保完全兼容现有架构。

## 主要差异分析

### 1. QmlEngine 差异

| 特性 | compositor版本 | 3rdparty版本 | 迁移建议 |
|------|---------------|-------------|----------|
| URI | "DeckShell.Compositor" | "Treeland" | 保持现有URI |
| 方法数量 | 基础方法 | 扩展方法 | 选择性迁移 |
| 组件创建 | 专用方法 | 通用createComponent | 采用通用方法 |

### 2. RootSurfaceContainer 差异

| 特性 | compositor版本 | 3rdparty版本 | 迁移建议 |
|------|---------------|-------------|----------|
| ZOrder枚举 | 基础值 | 扩展值 | 添加扩展值 |
| 销毁机制 | 直接delete | markWrapperToRemoved | 采用标记机制 |
| 类型过滤 | 无 | Layer类型过滤 | 添加类型过滤 |

### 3. LayerSurfaceContainer 差异

| 特性 | compositor版本 | 3rdparty版本 | 迁移建议 |
|------|---------------|-------------|----------|
| 日志支持 | 无 | Q_LOGGING_CATEGORY | 添加日志支持 |
| 错误处理 | 基础 | 增强空值检查 | 改进错误处理 |
| 状态管理 | 无 | setHasInitializeContainer | 添加状态管理 |

## 迁移方案

### 阶段1：核心架构迁移

#### 1.1 QmlEngine 增强
- 添加 `createComponent` 通用方法
- 选择性添加高级组件创建方法：
  - `createXdgShadow`
  - `createTaskSwitcher`
  - `createLockScreen`
  - `createMinimizeAnimation`

#### 1.2 RootSurfaceContainer 优化
- 扩展 ZOrder 枚举值
- 改进 `destroyForSurface` 方法
- 添加 Layer 类型过滤逻辑

#### 1.3 LayerSurfaceContainer 改进
- 添加日志支持
- 增强错误处理机制
- 实现状态管理功能

### 阶段2：接口适配

#### 2.1 函数签名统一
```cpp
// 建议的统一接口
QQuickItem* QmlEngine::createComponent(QQmlComponent &component,
                                     QQuickItem *parent,
                                     const QVariantMap &properties = QVariantMap());
```

#### 2.2 回调机制优化
- 统一信号槽连接模式
- 改进错误回调处理
- 添加状态变更通知

### 阶段3：依赖管理

#### 3.1 头文件包含优化
```cpp
// compositor/qmlengine.h
#include <QLoggingCategory>  // 添加日志支持
#include <QVariantMap>       // 通用属性支持
```

#### 3.2 库链接检查
- 确保所有必要依赖已包含
- 检查 Waylib 版本兼容性
- 验证 Qt 组件可用性

### 阶段4：错误处理增强

#### 4.1 异常捕获
```cpp
try {
    // 核心逻辑
} catch (const std::exception &e) {
    qCWarning(qLcCompositor) << "Exception in component creation:" << e.what();
}
```

#### 4.2 日志记录
```cpp
Q_LOGGING_CATEGORY(qLcCompositor, "deckshell.compositor")
Q_LOGGING_CATEGORY(qLcLayer, "deckshell.layer")
```

#### 4.3 边界检查
- 添加空指针检查
- 验证几何参数有效性
- 检查输出设备状态

### 阶段5：性能优化

#### 5.1 内存管理
- 实现对象池模式
- 优化组件生命周期
- 减少不必要的内存分配

#### 5.2 多线程改进
- 异步组件创建
- 后台资源加载
- 并发处理优化

#### 5.3 算法效率
- 优化表面查找算法
- 改进几何计算
- 缓存常用组件

## 测试验证方案

### 6.1 单元测试
```cpp
// test_qmlengine.cpp
TEST_F(QmlEngineTest, CreateComponent_WithValidProperties) {
    // 测试组件创建
}

TEST_F(QmlEngineTest, HandleInvalidComponent) {
    // 测试错误处理
}
```

### 6.2 集成测试
- 组件间交互测试
- 表面管理集成测试
- 输出设备切换测试

### 6.3 回归测试
- 现有功能兼容性测试
- 性能基准测试
- 内存泄漏检测

### 6.4 性能基准测试
```cpp
// benchmark_surface_creation.cpp
BENCHMARK(BM_SurfaceCreation) {
    // 测量表面创建性能
}
```

## 实施计划

### 阶段时间表

| 阶段 | 持续时间 | 主要任务 |
|------|----------|----------|
| 准备 | 1天 | 环境设置、备份 |
| 核心迁移 | 3天 | QmlEngine、容器类迁移 |
| 接口适配 | 2天 | 函数签名、回调机制 |
| 测试验证 | 2天 | 单元测试、集成测试 |
| 性能优化 | 1天 | 内存、多线程优化 |
| 文档更新 | 1天 | 迁移文档、同行评审 |

### 风险评估

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| API不兼容 | 中 | 高 | 充分测试、渐进迁移 |
| 性能下降 | 低 | 中 | 性能基准测试 |
| 内存泄漏 | 中 | 高 | 内存分析工具 |
| 功能缺失 | 低 | 中 | 功能对比验证 |

## 版本控制策略

### 分支管理
```
main (稳定分支)
├── feature/migration-qmlengine
├── feature/migration-containers
├── feature/migration-interfaces
└── feature/migration-testing
```

### 提交规范
- `[MIGRATION]` 迁移相关提交
- `[FIX]` 修复提交
- `[TEST]` 测试相关提交
- `[DOC]` 文档更新

## 监控和回滚计划

### 监控指标
- 编译成功率
- 测试通过率
- 性能基准分数
- 内存使用情况

### 回滚策略
1. 保留原代码备份
2. 按功能模块回滚
3. 渐进式部署验证
4. 自动化回滚脚本

---

*迁移方案制定时间: 2025-09-09*
*制定者: Kilo Code Architect Mode*
*预计完成时间: 10个工作日*