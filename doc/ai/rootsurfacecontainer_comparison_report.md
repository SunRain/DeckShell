# RootSurfaceContainer 文件差异分析报告

## 概述
本文档比较了 `compositor/rootsurfacecontainer.h` 与 `3rdparty/waylib-shared/src-unused/core/rootsurfacecontainer.h` 以及对应 CPP 文件的差异。

## 主要差异总结

### 1. 头文件结构差异

#### 包含路径差异
- **compositor 版本**: `#include "surfacecontainer.h"`
- **3rdparty 版本**: `#include "surface/surfacecontainer.h"`

#### ContainerZOrder 枚举差异
| ZOrder 值 | compositor | 3rdparty |
|-----------|------------|----------|
| BackgroundZOrder | -2 | -2 |
| BottomZOrder | -1 | -1 |
| NormalZOrder | 0 | 0 |
| TopZOrder | 1 | 2 |
| OverlayZOrder | 2 | 3 |
| TaskBarZOrder | 3 | 4 |
| MenuBarZOrder | 3 | 4 |
| PopupZOrder | 4 | 5 |
| **新增值** | - | MultitaskviewZOrder = 1 |
| **新增值** | - | CaptureLayerZOrder = 6 |
| **新增值** | - | LockScreenZOrder = 7 |

#### 方法签名差异
- **destroyForSurface**:
  - compositor: `void destroyForSurface(WSurface *surface)`
  - 3rdparty: `void destroyForSurface(SurfaceWrapper *wrapper)`

#### QML 相关差异
- **compositor**: 无 Q_MOC_INCLUDE
- **3rdparty**: `Q_MOC_INCLUDE(<wcursor.h>)`

#### 声明差异
- **compositor**:
  ```cpp
  Q_DECLARE_OPAQUE_POINTER(WAYLIB_SERVER_NAMESPACE::WOutputLayout*)
  Q_DECLARE_OPAQUE_POINTER(WAYLIB_SERVER_NAMESPACE::WCursor*)
  ```
- **3rdparty**:
  ```cpp
  Q_DECLARE_OPAQUE_POINTER(WAYLIB_SERVER_NAMESPACE::WOutputLayout *)
  ```

### 2. CPP 文件实现差异

#### 包含路径差异
- **compositor**:
  ```cpp
  #include "rootsurfacecontainer.h"
  #include "helper.h"
  #include "surfacewrapper.h"
  #include "output.h"
  ```
- **3rdparty**:
  ```cpp
  #include "rootsurfacecontainer.h"
  #include "output/output.h"
  #include "seat/helper.h"
  #include "surface/surfacewrapper.h"
  ```

#### destroyForSurface 实现差异
- **compositor**: `delete wrapper;`
- **3rdparty**: `wrapper->markWrapperToRemoved();`

#### Helper 方法调用差异
- **compositor**: `Helper::instance()->activeSurface(surface)`
- **3rdparty**: `Helper::instance()->activateSurface(surface)`

#### addBySubContainer 增强
3rdparty 版本在 `addBySubContainer` 中添加了额外的条件检查和注释：
```cpp
if (surface->type() != SurfaceWrapper::Type::Layer) {
    // RootSurfaceContainer does not have control over layer surface's position and ownsOutput
    // All things are done in LayerSurfaceContainer
    // ... 额外逻辑
}
```

### 3. 兼容性影响分析

#### API 兼容性问题
1. **方法签名不匹配**: `destroyForSurface` 参数类型不同
2. **依赖路径变化**: 需要更新包含路径
3. **Helper 方法差异**: 方法名从 `activeSurface` 改为 `activateSurface`

#### 功能差异影响
1. **ZOrder 扩展**: 3rdparty 版本支持更多层级，可能影响窗口管理逻辑
2. **内存管理差异**: 删除 vs 标记删除的策略不同
3. **Layer Surface 处理**: 3rdparty 版本对 Layer Surface 有特殊处理

#### 集成影响
1. **编译依赖**: 需要调整包含路径和依赖关系
2. **QML 集成**: Q_MOC_INCLUDE 可能影响 QML 绑定
3. **命名空间**: 需要确保 WAYLIB_SERVER_NAMESPACE 正确定义

## 迁移建议

### 推荐迁移策略
1. **渐进式迁移**: 先迁移头文件结构，再处理实现差异
2. **兼容层**: 为 API 变化创建兼容性包装器
3. **测试驱动**: 每个迁移步骤后进行充分测试

### 具体实施步骤
1. 更新包含路径和依赖关系
2. 调整方法签名和调用
3. 同步 ZOrder 枚举值
4. 更新 Helper 方法调用
5. 处理 Layer Surface 特殊逻辑
6. 测试和验证功能完整性

## 结论
两套文件在核心功能上相似，但存在显著的结构和实现差异。3rdparty 版本似乎是更新的实现，包含了更多的功能和更好的模块化。迁移时需要仔细处理 API 兼容性和功能完整性。