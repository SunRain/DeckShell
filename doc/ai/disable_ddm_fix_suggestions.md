# DISABLE_DDM 缺失依赖修复建议报告

## 概述

在分析 `compositor` 目录的 C++ 代码后，发现了多个缺失 `DISABLE_DDM` 宏保护的代码块。这些缺失的保护会导致在启用 `DISABLE_DDM` 选项时编译失败。

## 发现的问题

### 1. CMake 级别问题

#### 问题：DDM 模块未条件编译
**文件**: `compositor/src/modules/CMakeLists.txt` (第34行)
```cmake
add_subdirectory(ddm)  # 缺少条件编译保护
```

**影响**: 当 `DISABLE_DDM=ON` 时，DDM 模块仍然会被编译，导致依赖错误。

**修复建议**:
```cmake
if(NOT DISABLE_DDM)
    add_subdirectory(ddm)
endif()
```

### 2. C++ 代码级别问题

#### 问题1：wallpaperimage.cpp 中未保护的 UserModel 使用
**文件**: `compositor/src/wallpaper/wallpaperimage.cpp` (第24-25行)
```cpp
connect(Helper::instance()->qmlEngine()->singletonInstance<UserModel *>("Treeland",
                                                                        "UserModel"),
        &UserModel::currentUserNameChanged,
        this,
        &WallpaperImage::updateSource);
```

**影响**: 当 `DISABLE_DDM=ON` 时，UserModel 类不存在，导致编译错误。

**修复建议**:
```cpp
#ifndef DISABLE_DDM
connect(Helper::instance()->qmlEngine()->singletonInstance<UserModel *>("Treeland",
                                                                        "UserModel"),
        &UserModel::currentUserNameChanged,
        this,
        &WallpaperImage::updateSource);
#endif
```

#### 问题2：cmdline.cpp 中未保护的锁屏选项
**文件**: `compositor/src/utils/cmdline.cpp` (第143-145行)
```cpp
bool CmdLine::useLockScreen() const
{
    return m_parser->isSet(*m_lockScreen.get());
}
```

**影响**: 虽然这个方法本身不会导致编译错误，但当 `DISABLE_DDM=ON` 时，锁屏功能不可用，这个选项应该被禁用。

**修复建议**:
```cpp
bool CmdLine::useLockScreen() const
{
#ifndef DISABLE_DDM
    return m_parser->isSet(*m_lockScreen.get());
#else
    return false;
#endif
}
```

#### 问题3：ddminterfacev1.cpp 完全未保护
**文件**: `compositor/src/modules/ddm/ddminterfacev1.cpp`
**问题**: 整个文件都是 DDM 相关的，但没有宏保护。

**影响**: 当 `DISABLE_DDM=ON` 时，这个文件仍然会被编译，但依赖的 DDM 功能不存在。

**修复建议**: 在文件开头添加宏保护：
```cpp
#ifndef DISABLE_DDM

// 整个文件内容

#endif // DISABLE_DDM
```

或者更好的方案：在 `modules/ddm/CMakeLists.txt` 中添加条件编译保护。

### 3. 间接依赖问题

#### 问题：surfacewrapper.cpp 中的锁屏相关功能
**文件**: `compositor/src/surface/surfacewrapper.cpp`
**问题**: 虽然有 `setHideByLockScreen` 方法，但可能在某些调用点缺少保护。

**建议**: 检查所有调用 `setHideByLockScreen` 的地方，确保在 `DISABLE_DDM=ON` 时不会被调用。

## 修复优先级

### 高优先级（必须修复）
1. **DDM 模块条件编译** - `modules/CMakeLists.txt`
2. **ddminterfacev1.cpp 文件保护** - 添加宏保护或条件编译
3. **wallpaperimage.cpp UserModel 使用** - 添加宏保护

### 中优先级（建议修复）
4. **cmdline.cpp 锁屏选项处理** - 添加条件返回
5. **surfacewrapper.cpp 锁屏调用检查** - 验证调用点保护

## 修复方案

### 方案1：宏保护法
在相关文件中添加 `#ifndef DISABLE_DDM` 宏保护。

### 方案2：条件编译法
在 CMakeLists.txt 中使用条件编译完全排除相关文件。

### 方案3：运行时检查法
在代码中添加运行时检查，当 DDM 功能不可用时优雅降级。

## 推荐修复顺序

1. 修复 CMake 级别的 DDM 模块条件编译
2. 修复 ddminterfacev1.cpp 的保护
3. 修复 wallpaperimage.cpp 中的 UserModel 使用
4. 修复 cmdline.cpp 中的锁屏选项
5. 验证所有修复后进行编译测试

## 验证方法

修复完成后，应该能够成功执行：
```bash
cd compositor
mkdir build
cd build
cmake -B . -S .. -DDISABLE_DDM=ON
cmake --build build -j$(nproc)
```

---
*分析时间: 2025-09-16*
*分析工具: Kilo Code Architect Mode*
*修复建议版本: 1.0*
