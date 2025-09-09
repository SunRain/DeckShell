# RootSurfaceContainer 详细对比分析

## 文件对比清单

### 1. rootsurfacecontainer.h 对比

#### 头文件包含差异
| 差异类型 | compositor版本 | 3rdparty版本 |
|---------|---------------|-------------|
| 包含路径 | `#include "surfacecontainer.h"` | `#include "surface/surfacecontainer.h"` |
| MOC声明 | 无 `Q_MOC_INCLUDE(<wcursor.h>)` | 有 `Q_MOC_INCLUDE(<wcursor.h>)` |
| 指针声明 | 无 `Q_DECLARE_OPAQUE_POINTER` | 有 `Q_DECLARE_OPAQUE_POINTER(WAYLIB_SERVER_NAMESPACE::WCursor *)` |

#### ContainerZOrder 枚举对比
| ZOrder级别 | compositor值 | 3rdparty值 | 差异 |
|-----------|-------------|-----------|------|
| BackgroundZOrder | -2 | -2 | 无差异 |
| BottomZOrder | -1 | -1 | 无差异 |
| NormalZOrder | 0 | 0 | 无差异 |
| MultitaskviewZOrder | - | 1 | 3rdparty新增 |
| TopZOrder | 1 | 2 | 值不同 |
| OverlayZOrder | 2 | 3 | 值不同 |
| TaskBarZOrder | 3 | 4 | 值不同 |
| MenuBarZOrder | 3 | 4 | 值不同 |
| PopupZOrder | 4 | 5 | 值不同 |
| CaptureLayerZOrder | - | 6 | 3rdparty新增 |
| LockScreenZOrder | - | 7 | 3rdparty新增 |

#### 方法签名差异
| 方法 | compositor签名 | 3rdparty签名 | 差异说明 |
|------|---------------|-------------|----------|
| destroyForSurface | `void destroyForSurface(WSurface *surface)` | `void destroyForSurface(SurfaceWrapper *wrapper)` | 参数类型不同 |

### 2. rootsurfacecontainer.cpp 对比

#### 销毁机制差异
**compositor版本:**
```cpp
void RootSurfaceContainer::destroyForSurface(WSurface *surface)
{
    auto wrapper = getSurface(surface);
    if (wrapper == moveResizeState.surface)
        endMoveResize();

    delete wrapper;
}
```

**3rdparty版本:**
```cpp
void RootSurfaceContainer::destroyForSurface(SurfaceWrapper *wrapper)
{
    if (wrapper == moveResizeState.surface)
        endMoveResize();

    wrapper->markWrapperToRemoved();
}
```

**差异分析:**
- compositor: 直接删除wrapper对象
- 3rdparty: 调用`markWrapperToRemoved()`标记删除，由其他机制处理

#### Layer Surface 处理差异
**compositor版本 (addBySubContainer):**
```cpp
void RootSurfaceContainer::addBySubContainer(SurfaceContainer *sub, SurfaceWrapper *surface)
{
    SurfaceContainer::addBySubContainer(sub, surface);
    // ... 连接信号
    if (!surface->ownsOutput()) {
        // ... 设置输出逻辑
    }
    // ... 更新输出
    if (surface->shellSurface()->surface()->mapped())
        Helper::instance()->activeSurface(surface, Qt::OtherFocusReason);
}
```

**3rdparty版本 (addBySubContainer):**
```cpp
void RootSurfaceContainer::addBySubContainer(SurfaceContainer *sub, SurfaceWrapper *surface)
{
    SurfaceContainer::addBySubContainer(sub, surface);

    if (surface->type() != SurfaceWrapper::Type::Layer) {
        // RootSurfaceContainer does not have control over layer surface's position and ownsOutput
        // All things are done in LayerSurfaceContainer
        // ... 连接信号和处理逻辑
    }
}
```

**差异分析:**
- compositor: 统一处理所有surface类型，包括最后的激活调用
- 3rdparty: 明确区分Layer surface和其他类型，有详细注释说明职责分离

#### 激活逻辑差异
**compositor版本 (startMove):**
```cpp
void RootSurfaceContainer::startMove(SurfaceWrapper *surface)
{
    endMoveResize();
    beginMoveResize(surface, Qt::Edges{0});

    Helper::instance()->activeSurface(surface);
}
```

**3rdparty版本 (startMove):**
```cpp
void RootSurfaceContainer::startMove(SurfaceWrapper *surface)
{
    endMoveResize();
    beginMoveResize(surface, Qt::Edges{ 0 });

    Helper::instance()->activateSurface(surface);
}
```

**差异分析:**
- compositor: `activeSurface(surface)`
- 3rdparty: `activateSurface(surface)`
- 方法名不同，可能有不同的实现逻辑

#### 调整大小函数差异
**compositor版本 (startResize):**
```cpp
void RootSurfaceContainer::startResize(SurfaceWrapper *surface, Qt::Edges edges)
{
    endMoveResize();
    Q_ASSERT(edges != 0);

    beginMoveResize(surface, edges);
    surface->shellSurface()->setResizeing(true);
    Helper::instance()->activeSurface(surface);
}
```

**3rdparty版本 (startResize):**
```cpp
void RootSurfaceContainer::startResize(SurfaceWrapper *surface, Qt::Edges edges)
{
    endMoveResize();
    Q_ASSERT(edges != 0);

    beginMoveResize(surface, edges);
    surface->shellSurface()->setResizeing(true);
    Helper::instance()->activateSurface(surface);
}
```

**差异分析:**
- 同样是方法名差异：`activeSurface` vs `activateSurface`

#### 几何过滤差异
**compositor版本 (filterSurfaceStateChange):**
```cpp
bool RootSurfaceContainer::filterSurfaceStateChange(SurfaceWrapper *surface, SurfaceWrapper::State newState, SurfaceWrapper::State oldState)
{
    Q_UNUSED(oldState);
    Q_UNUSED(newState);
    return surface == moveResizeState.surface;
}
```

**3rdparty版本 (filterSurfaceStateChange):**
```cpp
bool RootSurfaceContainer::filterSurfaceStateChange(SurfaceWrapper *surface,
                                                     [[maybe_unused]] SurfaceWrapper::State newState,
                                                     [[maybe_unused]] SurfaceWrapper::State oldState)
{
    return surface == moveResizeState.surface;
}
```

**差异分析:**
- 3rdparty版本使用了`[[maybe_unused]]`属性来避免未使用参数的警告

#### 静态函数差异
**compositor版本:**
```cpp
static qreal pointToRectMinDistance(const QPointF &pos, const QRectF &rect) {
    if (rect.contains(pos))
        return 0;
    return std::min({std::abs(rect.x() - pos.x()), std::abs(rect.y() - pos.y()),
                     std::abs(rect.right() - pos.x()), std::abs(rect.bottom() - pos.y())});
}
```

**3rdparty版本:**
```cpp
static qreal pointToRectMinDistance(const QPointF &pos, const QRectF &rect)
{
    if (rect.contains(pos))
        return 0;
    return std::min({ std::abs(rect.x() - pos.x()),
                      std::abs(rect.y() - pos.y()),
                      std::abs(rect.right() - pos.x()),
                      std::abs(rect.bottom() - pos.y()) });
}
```

**差异分析:**
- 代码格式不同：compositor使用单行，3rdparty使用多行

## 架构影响分析

### 1. ZOrder 值差异的影响
- **渲染顺序**: 不同的ZOrder值会影响窗口的渲染层级
- **用户体验**: 可能导致窗口层级显示异常
- **兼容性**: 需要确保所有相关组件都使用一致的ZOrder值

### 2. 销毁机制差异的影响
- **内存管理**: 直接删除 vs 标记删除的策略不同
- **生命周期**: 可能影响对象的生命周期管理
- **性能**: 标记删除可能有更好的性能，但复杂度更高

### 3. Layer Surface 处理差异的影响
- **职责分离**: 3rdparty版本更明确地区分了Layer surface的处理职责
- **代码组织**: compositor版本的处理更统一
- **维护性**: 3rdparty版本的注释更详细，便于理解

### 4. 方法命名差异的影响
- **API一致性**: `activeSurface` vs `activateSurface` 的命名不一致
- **调用兼容性**: 需要检查所有调用点是否需要更新

## 迁移建议

### 高优先级修改
1. **统一ZOrder值**: 选择一个版本的标准并统一所有相关文件
2. **统一方法签名**: 选择参数类型并更新所有调用点
3. **统一方法命名**: 选择 `activeSurface` 或 `activateSurface` 并保持一致

### 中优先级修改
1. **统一销毁机制**: 决定使用直接删除还是标记删除策略
2. **统一Layer处理**: 决定是否需要明确的职责分离
3. **代码格式统一**: 统一代码风格和格式

### 低优先级修改
1. **添加MOC声明**: 根据需要添加或移除MOC相关声明
2. **优化静态函数**: 统一静态函数的格式
3. **完善注释**: 添加必要的代码注释

## 测试建议

### 回归测试
1. **窗口创建和销毁测试**: 验证surface的生命周期管理
2. **窗口层级测试**: 验证ZOrder值的正确性
3. **窗口移动和调整大小测试**: 验证move/resize功能
4. **Layer surface测试**: 验证特殊surface类型的处理

### 性能测试
1. **内存使用测试**: 监控内存泄漏和使用情况
2. **渲染性能测试**: 验证窗口渲染的流畅性
3. **响应时间测试**: 验证用户操作的响应速度

---

*对比分析时间: 2025-09-09*
*分析工具: Kilo Code Architect Mode*