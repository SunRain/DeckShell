# DISABLE_DDM 宏依赖分析报告

## 概述

本报告分析了 `compositor` 目录中所有依赖 DISABLE_DDM 功能的文件、函数和代码块。DISABLE_DDM 是一个 CMake 选项，当启用时会添加编译定义 "DISABLE_DDM"，用于禁用 DDM（Display Display Manager）和问候功能。

## CMake 配置

### 主 CMakeLists.txt
- **文件**: `compositor/CMakeLists.txt`
- **行号**: 43-47
- **代码**:
  ```cmake
  option(DISABLE_DDM "Disable DDM and greeter" OFF)

  if(DISABLE_DDM)
      add_compile_definitions("DISABLE_DDM")
  endif()
  ```
- **说明**: 定义 DISABLE_DDM 选项，当启用时添加编译宏定义。

### 源代码 CMakeLists.txt
- **文件**: `compositor/src/CMakeLists.txt`
- **行号**: 14, 112-121, 298-300
- **代码**:
  ```cmake
  if (NOT DISABLE_DDM)
      find_package(DDM 0.2.0 REQUIRED COMPONENTS Auth Common)
  endif()

  $<$<NOT:$<BOOL:${DISABLE_DDM}>>:core/lockscreen.h>
  $<$<NOT:$<BOOL:${DISABLE_DDM}>>:core/lockscreen.cpp>
  $<$<NOT:$<BOOL:${DISABLE_DDM}>>:greeter/greeterproxy.cpp>
  $<$<NOT:$<BOOL:${DISABLE_DDM}>>:greeter/greeterproxy.h>
  $<$<NOT:$<BOOL:${DISABLE_DDM}>>:greeter/sessionmodel.cpp>
  $<$<NOT:$<BOOL:${DISABLE_DDM}>>:greeter/sessionmodel.h>
  $<$<NOT:$<BOOL:${DISABLE_DDM}>>:greeter/user.cpp>
  $<$<NOT:$<BOOL:${DISABLE_DDM}>>:greeter/user.h>
  $<$<NOT:$<BOOL:${DISABLE_DDM}>>:greeter/usermodel.cpp>
  $<$<NOT:$<BOOL:${DISABLE_DDM}>>:greeter/usermodel.h>

  $<$<NOT:$<BOOL:${DISABLE_DDM}>>:DDM::Auth>
  $<$<NOT:$<BOOL:${DISABLE_DDM}>>:DDM::Common>
  $<$<NOT:$<BOOL:${DISABLE_DDM}>>:PkgConfig::PAM>
  ```
- **说明**: 条件编译锁屏和问候相关的文件，以及条件链接 DDM 库。

## 源代码依赖

### 1. Helper 类 (compositor/src/seat/helper.h & helper.cpp)

#### 头文件声明
- **文件**: `compositor/src/seat/helper.h`
- **行号**: 95-97, 213-215, 383
- **代码**:
  ```cpp
  #ifndef DISABLE_DDM
  class UserModel;
  class DDMInterfaceV1;
  #endif

  #ifndef DISABLE_DDM
      UserModel *userModel() const;
      DDMInterfaceV1 *ddmInterfaceV1() const;
  #endif

  #ifndef DISABLE_DDM
      UserModel *m_userModel{ nullptr };
  #endif
  ```
- **说明**: 条件声明 UserModel 和 DDMInterfaceV1 类，以及相关成员变量和函数。

#### 实现文件
- **文件**: `compositor/src/seat/helper.cpp`
- **行号**: 16-18, 855-857, 972-974, 1021-1025, 1296-1304, 1774-1799, 1810-1822, 2013-2041, 2055-2085, 2215-2229
- **依赖说明**:
  1. **行16-18**: 条件包含锁屏头文件
  2. **行855-857**: 条件初始化用户模型
  3. **行972-974**: 条件连接用户模型信号
  4. **行1021-1025**: 条件设置锁屏主输出名称
  5. **行1296-1304**: 条件处理锁屏快捷键
  6. **行1774-1799**: 条件实现锁屏处理函数
  7. **行1810-1822**: 条件实现会话锁/解锁处理
  8. **行2013-2041**: 条件实现锁屏设置
  9. **行2055-2085**: 条件实现锁屏显示
  10. **行2215-2229**: 条件实现用户模型访问函数

### 2. QmlEngine 类 (compositor/src/core/qmlengine.h & qmlengine.cpp)

#### 头文件声明
- **文件**: `compositor/src/core/qmlengine.h`
- **行号**: 85-86
- **代码**:
  ```cpp
  #ifndef DISABLE_DDM
      QQmlComponent lockScreenComponent;
  #endif
  ```
- **说明**: 条件声明锁屏组件成员。

#### 实现文件
- **文件**: `compositor/src/core/qmlengine.cpp`
- **行号**: 33-34, 196-197
- **代码**:
  ```cpp
  #ifndef DISABLE_DDM
      , lockScreenComponent(this, "Treeland", "Greeter")
  #endif

  #ifndef DISABLE_DDM
      return createComponent(lockScreenComponent,
  ```
- **说明**: 条件初始化和创建锁屏组件。

### 3. Treeland 类 (compositor/src/core/treeland.cpp)

- **文件**: `compositor/src/core/treeland.cpp`
- **行号**: 9, 77-87, 106-136, 140-166, 209-218, 228-236, 374-392
- **依赖说明**:
  1. **行9**: 条件包含用户模型头文件
  2. **行77-87**: 条件获取和连接用户模型
  3. **行106-136**: 条件实现用户更改处理
  4. **行140-166**: 条件实现插件翻译更新
  5. **行209-218**: 条件连接用户模型到插件
  6. **行228-236**: 条件创建锁屏插件实例
  7. **行374-392**: 条件处理 Wayland 套接字和用户模型

### 4. WallpaperImage 类 (compositor/src/wallpaper/wallpaperimage.cpp)

- **文件**: `compositor/src/wallpaper/wallpaperimage.cpp`
- **行号**: 9, 24-30
- **代码**:
  ```cpp
  #ifndef DISABLE_DDM
  #include "greeter/usermodel.h"
  #endif

  #ifndef DISABLE_DDM
      connect(Helper::instance()->qmlEngine()->singletonInstance<UserModel *>("Treeland",
                                                                              "UserModel"),
              &UserModel::currentUserNameChanged,
              this,
              &WallpaperImage::updateSource);
  #endif
  ```
- **说明**: 条件包含用户模型头文件并连接用户更改信号。

## 受影响的文件列表

### 条件编译的文件
当 DISABLE_DDM 被定义时，以下文件不会被编译：
- `compositor/src/core/lockscreen.h`
- `compositor/src/core/lockscreen.cpp`
- `compositor/src/greeter/greeterproxy.h`
- `compositor/src/greeter/greeterproxy.cpp`
- `compositor/src/greeter/sessionmodel.h`
- `compositor/src/greeter/sessionmodel.cpp`
- `compositor/src/greeter/user.h`
- `compositor/src/greeter/user.cpp`
- `compositor/src/greeter/usermodel.h`
- `compositor/src/greeter/usermodel.cpp`

### 条件链接的库
当 DISABLE_DDM 被定义时，以下库不会被链接：
- DDM::Auth
- DDM::Common
- PkgConfig::PAM

## 功能影响

当启用 DISABLE_DDM 时，以下功能将被禁用：
1. **锁屏功能**: LockScreen 类的所有功能
2. **用户管理**: UserModel 类的所有功能
3. **问候界面**: Greeter 相关的所有组件
4. **会话管理**: 会话锁/解锁功能
5. **DDM 集成**: 与 Display Display Manager 的所有集成

## 编译验证

经过修复条件编译问题后，项目成功编译，所有依赖关系正确处理。编译输出显示：
- Exit code: 0 (成功)
- 所有目标文件成功构建
- 库文件成功链接
- 可执行文件成功生成

## 结论

DISABLE_DDM 宏在代码库中被广泛使用，主要用于条件编译与 DDM（Display Display Manager）和问候功能相关的代码。通过适当的条件编译保护，所有依赖关系都已正确处理，确保代码在启用和禁用该功能时都能正常编译。
