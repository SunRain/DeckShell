# RootSurfaceContainer 迁移指南

## 迁移概述

基于文件差异分析，本指南提供了从 `compositor` 版本迁移到 `3rdparty/waylib-shared` 版本的详细步骤。

## 迁移策略

### 策略选择
1. **完全替换**: 直接使用 3rdparty 版本替换 compositor 版本
2. **渐进式迁移**: 分阶段逐步迁移，保持向后兼容性
3. **混合使用**: 在过渡期间同时维护两个版本

**推荐策略**: 渐进式迁移，以最小化风险并确保功能完整性。

## 详细迁移步骤

### 阶段 1: 准备工作

#### 1.1 备份当前代码
```bash
# 创建备份分支
git checkout -b migration-backup
git add .
git commit -m "Backup before RootSurfaceContainer migration"
```

#### 1.2 分析依赖关系
- 识别所有使用 RootSurfaceContainer 的文件
- 检查现有的 API 调用模式
- 评估测试覆盖率

#### 1.3 创建兼容性测试
```cpp
// 创建测试文件验证迁移前后功能一致性
void testMigrationCompatibility() {
    // 测试关键功能
    // - Surface 管理
    // - Output 处理
    // - Move/Resize 操作
    // - ZOrder 层级
}
```

### 阶段 2: 结构迁移

#### 2.1 更新包含路径
```cpp
// 从:
#include "surfacecontainer.h"

// 改为:
#include "surface/surfacecontainer.h"
```

#### 2.2 更新依赖路径
```cpp
// 从:
#include "helper.h"
#include "surfacewrapper.h"
#include "output.h"

// 改为:
#include "output/output.h"
#include "seat/helper.h"
#include "surface/surfacewrapper.h"
```

#### 2.3 同步枚举定义
```cpp
// 添加缺失的 ZOrder 值
enum ContainerZOrder {
    BackgroundZOrder = -2,
    BottomZOrder = -1,
    NormalZOrder = 0,
    MultitaskviewZOrder = 1,    // 新增
    TopZOrder = 2,              // 从 1 改为 2
    OverlayZOrder = 3,          // 从 2 改为 3
    TaskBarZOrder = 4,          // 从 3 改为 4
    MenuBarZOrder = 4,          // 从 3 改为 4
    PopupZOrder = 5,            // 从 4 改为 5
    CaptureLayerZOrder = 6,     // 新增
    LockScreenZOrder = 7,       // 新增
};
```

### 阶段 3: API 迁移

#### 3.1 方法签名更新
```cpp
// 从:
void destroyForSurface(WSurface *surface)

// 改为:
void destroyForSurface(SurfaceWrapper *wrapper)
```

#### 3.2 Helper 方法调用更新
```cpp
// 从:
Helper::instance()->activeSurface(surface)

// 改为:
Helper::instance()->activateSurface(surface)
```

#### 3.3 内存管理策略更新
```cpp
// 从:
void destroyForSurface(WSurface *surface) {
    auto wrapper = getSurface(surface);
    delete wrapper;  // 直接删除
}

// 改为:
void destroyForSurface(SurfaceWrapper *wrapper) {
    wrapper->markWrapperToRemoved();  // 标记删除
}
```

### 阶段 4: 功能增强迁移

#### 4.1 Layer Surface 处理
```cpp
void addBySubContainer(SurfaceContainer *sub, SurfaceWrapper *surface) {
    SurfaceContainer::addBySubContainer(sub, surface);

    if (surface->type() != SurfaceWrapper::Type::Layer) {
        // RootSurfaceContainer does not have control over layer surface's position and ownsOutput
        // All things are done in LayerSurfaceContainer

        // 添加现有的连接逻辑...
        connect(surface, &SurfaceWrapper::requestMove, this, [this] {
            auto surface = qobject_cast<SurfaceWrapper *>(sender());
            Q_ASSERT(surface);
            startMove(surface);
        });

        // ... 其他逻辑
    }
}
```

#### 4.2 QML 集成增强
```cpp
// 添加 Q_MOC_INCLUDE 以支持 QML
Q_MOC_INCLUDE(<wcursor.h>)
```

### 阶段 5: 测试和验证

#### 5.1 单元测试
```cpp
void testZOrderValues() {
    // 验证所有 ZOrder 值正确
    QCOMPARE(RootSurfaceContainer::BackgroundZOrder, -2);
    QCOMPARE(RootSurfaceContainer::LockScreenZOrder, 7);
}

void testMethodSignatures() {
    // 验证方法签名正确
    RootSurfaceContainer container;
    SurfaceWrapper *wrapper = nullptr;
    container.destroyForSurface(wrapper);  // 应接受 SurfaceWrapper*
}

void testHelperIntegration() {
    // 验证 Helper 方法调用正确
    SurfaceWrapper *surface = createTestSurface();
    Helper::instance()->activateSurface(surface);  // 使用新方法名
}
```

#### 5.2 集成测试
- 测试窗口管理功能
- 测试多输出支持
- 测试 Move/Resize 操作
- 测试 Layer Surface 处理

#### 5.3 性能测试
- 验证内存使用情况
- 检查渲染性能
- 评估启动时间

### 阶段 6: 清理和优化

#### 6.1 移除兼容性代码
- 删除临时兼容性包装器
- 清理废弃的 API 调用
- 更新文档和注释

#### 6.2 代码优化
- 应用新的代码风格
- 优化性能瓶颈
- 改进错误处理

## 风险评估和缓解策略

### 高风险项目
1. **API 签名变化**: 可能破坏现有代码
   - **缓解**: 创建兼容性包装器

2. **内存管理差异**: 可能导致内存泄漏或崩溃
   - **缓解**: 仔细测试内存生命周期

3. **依赖路径变化**: 可能导致编译失败
   - **缓解**: 分阶段更新包含路径

### 中风险项目
1. **ZOrder 值变化**: 可能影响窗口层级
   - **缓解**: 验证所有窗口类型正确映射

2. **Helper 方法变化**: 可能影响输入处理
   - **缓解**: 确保所有调用点都更新

## 回滚计划

### 快速回滚
```bash
# 如果迁移失败，快速回滚
git checkout migration-backup
git branch -D migration-main
```

### 渐进式回滚
1. 恢复 API 兼容性包装器
2. 逐步回滚功能增强
3. 保持向后兼容性直到完全稳定

## 成功标准

### 功能完整性
- [ ] 所有现有功能正常工作
- [ ] 新增功能正确实现
- [ ] 性能不劣化

### 代码质量
- [ ] 编译无警告
- [ ] 所有测试通过
- [ ] 代码覆盖率不降低

### 文档完整性
- [ ] API 文档更新
- [ ] 迁移指南完善
- [ ] 代码注释更新

## 总结

这次迁移涉及多个方面的变化，包括 API、依赖关系和功能增强。通过分阶段进行和充分测试，可以最小化风险并确保成功迁移。建议在开发分支上进行迁移，并在充分测试后合并到主分支。