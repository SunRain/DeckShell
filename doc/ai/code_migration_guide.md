# Waylib 代码迁移指南

## 概述

本文档详细说明了如何将 `3rdparty/waylib-shared/src-unused/core` 目录下的代码迁移到 `compositor` 目录，确保兼容现有架构并提升系统性能。

## 同名文件分析

### 1. qmlengine.h

**差异分析：**
- `compositor` 版本：基础 QML 组件工厂
- `3rdparty` 版本：扩展了更多组件支持

**迁移步骤：**
1. 添加缺失的私有成员：
   - `lockScreenComponent`
   - `dockPreviewComponent`
   - `minimizeAnimationComponent`
   - `launchpadAnimationComponent`
   - `launchpadCoverComponent`
   - `layershellAnimationComponent`

2. 添加对应的创建方法：
   - `createLockScreen()`
   - `createDockPreview()`
   - `createMinimizeAnimation()`
   - `createLaunchpadAnimation()`
   - `createLaunchpadCover()`
   - `createLayerShellAnimation()`

3. 更新构造函数初始化新组件

### 2. rootsurfacecontainer.h

**差异分析：**
- `compositor` 版本：基础表面容器管理
- `3rdparty` 版本：增强的表面位置管理和输出更新

**迁移步骤：**
1. 添加方法声明：
   ```cpp
   void ensureSurfaceNormalPositionValid(SurfaceWrapper *surface);
   void updateSurfaceOutputs(SurfaceWrapper *surface);
   ```

2. 确保包含必要的头文件

### 3. rootsurfacecontainer.cpp

**差异分析：**
- `compositor` 版本：基础实现
- `3rdparty` 版本：完整的表面管理和优化

**迁移步骤：**
1. 实现缺失的方法：
   - `ensureSurfaceNormalPositionValid()`
   - `updateSurfaceOutputs()`

2. 添加辅助函数：
   - `pointToRectMinDistance()`
   - `adjustRectToMakePointVisible()`

3. 更新现有方法实现

## 错误处理优化

### 1. 空指针检查
```cpp
if (!surface) {
    qCWarning(qLcRootSurfaceContainer) << "Surface is null";
    return;
}
```

### 2. 边界检查
```cpp
Q_ASSERT(geometry.isValid());
if (!geometry.isValid()) {
    qCWarning(qLcRootSurfaceContainer) << "Invalid geometry";
    return;
}
```

### 3. 资源清理
```cpp
if (m_surfaceItem) {
    m_surfaceItem->deleteLater();
    m_surfaceItem = nullptr;
}
```

## 性能提升建议

### 1. 缓存优化
```cpp
// 缓存频繁计算的值
QRectF cachedGeometry = surface->geometry();
if (cachedGeometry != m_lastGeometry) {
    updateSurfaceOutputs(surface);
    m_lastGeometry = cachedGeometry;
}
```

### 2. 批量处理
```cpp
// 批量更新多个表面
QList<SurfaceWrapper*> surfacesToUpdate;
for (auto surface : surfacesToUpdate) {
    updateSurfaceOutputs(surface);
}
emit surfacesUpdated();
```

### 3. 异步处理
```cpp
// 使用 Qt Concurrent 进行异步处理
QtConcurrent::run([this, surface]() {
    ensureSurfaceNormalPositionValid(surface);
});
```

## 测试验证方法

### 1. 单元测试
```cpp
void TestRootSurfaceContainer::testEnsureSurfaceNormalPositionValid()
{
    // 测试表面位置验证逻辑
    SurfaceWrapper *surface = createMockSurface();
    container->ensureSurfaceNormalPositionValid(surface);

    QVERIFY(surface->geometry().isValid());
}
```

### 2. 集成测试
```cpp
void TestIntegration::testSurfaceOutputUpdate()
{
    // 测试表面输出更新流程
    setupTestEnvironment();
    triggerOutputChange();

    QVERIFY(verifySurfaceOutputs());
}
```

### 3. 性能测试
```cpp
void TestPerformance::testBulkSurfaceUpdate()
{
    QBENCHMARK {
        for (int i = 0; i < 1000; ++i) {
            container->updateSurfaceOutputs(surfaces[i]);
        }
    }
}
```

## 迁移实施计划

### Phase 1: 代码迁移
1. 备份现有代码
2. 逐个文件进行迁移
3. 编译验证

### Phase 2: 功能验证
1. 运行单元测试
2. 执行集成测试
3. 性能基准测试

### Phase 3: 优化改进
1. 应用错误处理优化
2. 实施性能提升
3. 最终验证测试

## 风险评估

### 潜在风险
1. **兼容性问题**：新代码可能与现有架构冲突
2. **性能影响**：增强功能可能影响系统性能
3. **稳定性问题**：新代码可能引入bug

### 缓解措施
1. 逐步迁移，逐个验证
2. 性能监控和基准测试
3. 完整的测试覆盖

## 总结

通过本次迁移，我们将获得：
- 更丰富的 QML 组件支持
- 增强的表面管理功能
- 更好的错误处理机制
- 提升的系统性能

迁移过程需要谨慎进行，确保每个步骤都经过充分测试，以避免引入新的问题。