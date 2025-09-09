# CMake Include方法详解

本文档详细介绍了CMake中用于设置代码include的各种方法，按功能分类整理。

## 1. 模块包含方法

### 1.1 include() 命令
`include()` 命令用于包含CMake模块或脚本文件。

**语法：**
```cmake
include(<file|module> [OPTIONAL] [RESULT_VARIABLE <var>] [NO_POLICY_SCOPE])
```

**参数说明：**
- `<file|module>`: 要包含的文件路径或模块名
- `OPTIONAL`: 可选，如果文件不存在不会报错
- `RESULT_VARIABLE`: 可选，存储包含结果的变量
- `NO_POLICY_SCOPE`: 可选，不继承策略设置

**示例：**
```cmake
# 包含标准CMake模块
include(GNUInstallDirs)
include(FeatureSummary)

# 包含自定义模块（需要设置CMAKE_MODULE_PATH）
include(WaylandScannerHelpers)

# 包含文件路径
include(cmake/DefineImplModule.cmake)

# 可选包含
include(MyOptionalModule OPTIONAL)
```

### 1.2 CMAKE_MODULE_PATH 变量
设置CMake模块的搜索路径。

**示例：**
```cmake
# 设置模块搜索路径
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")
list(APPEND CMAKE_MODULE_PATH "/usr/share/cmake/Modules")
```

## 2. 目录包含方法

### 2.1 CMAKE_INCLUDE_CURRENT_DIR 变量
自动将当前源目录和构建目录添加到include路径中。

**示例：**
```cmake
set(CMAKE_INCLUDE_CURRENT_DIR ON)
# 这等价于：
# include_directories(${CMAKE_CURRENT_SOURCE_DIR})
# include_directories(${CMAKE_CURRENT_BINARY_DIR})
```

### 2.2 include_directories() 命令
设置全局的include搜索路径。

**语法：**
```cmake
include_directories([AFTER|BEFORE] [SYSTEM] <dir1> [<dir2> ...])
```

**参数说明：**
- `AFTER|BEFORE`: 添加到现有路径的后面或前面
- `SYSTEM`: 将目录标记为系统目录（编译器可能给予特殊处理）
- `<dir1> [<dir2> ...]`: 要添加的目录列表

**示例：**
```cmake
# 添加include目录
include_directories(include)
include_directories(${CMAKE_BINARY_DIR}/generated)

# 系统include目录
include_directories(SYSTEM /usr/local/include)

# 在前面添加
include_directories(BEFORE src)
```

### 2.3 target_include_directories() 命令
为特定目标设置include路径，这是推荐的方法。

**语法：**
```cmake
target_include_directories(<target>
  <INTERFACE|PUBLIC|PRIVATE> [items1...]
  [<INTERFACE|PUBLIC|PRIVATE> [items2...] ...])
```

**可见性说明：**
- `PRIVATE`: 只对目标本身可见
- `PUBLIC`: 对目标本身和依赖它的目标可见
- `INTERFACE`: 只对依赖目标可见，不对目标本身可见

**示例：**
```cmake
target_include_directories(my_target
  PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_BINARY_DIR}
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
  INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/api>
)

# 使用生成器表达式
target_include_directories(my_target
  PRIVATE
    $<BUILD_INTERFACE:${CMAKE_BINARY_DIR}/protocols>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_BINDIR}>
)
```

## 3. 包搜索路径方法

### 3.1 CMAKE_PREFIX_PATH 变量
设置find_package()搜索包的根路径。

**示例：**
```cmake
# 设置包搜索路径
set(CMAKE_PREFIX_PATH "/usr/local;/opt/local;/home/user/local")

# 或使用list追加
list(APPEND CMAKE_PREFIX_PATH "/custom/install/path")
```

### 3.2 CMAKE_INCLUDE_PATH 变量
设置find_path()和find_file()搜索头文件的路径。

**示例：**
```cmake
set(CMAKE_INCLUDE_PATH "/custom/include;/opt/include")
```

### 3.3 CMAKE_SYSTEM_INCLUDE_PATH 变量
系统级include路径，通常由CMake自动设置。

**示例：**
```cmake
# 查看系统include路径
message("System include paths: ${CMAKE_SYSTEM_INCLUDE_PATH}")
```

## 4. 高级用法和最佳实践

### 4.1 条件包含
```cmake
# 根据条件包含
if(BUILD_TESTS)
  include(CTest)
  include_directories(test/include)
endif()

# 根据平台包含
if(UNIX)
  include_directories(/usr/local/include)
elseif(WIN32)
  include_directories("C:/Program Files/MyLib/include")
endif()
```

### 4.2 使用生成器表达式
```cmake
target_include_directories(my_target
  PRIVATE
    # 只在构建时包含
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>
    # 只在安装时包含
    $<INSTALL_INTERFACE:include>
    # 条件包含
    $<$<PLATFORM_ID:Linux>:${LINUX_INCLUDE_DIR}>
)
```

### 4.3 包含顺序管理
```cmake
# 使用AFTER/BEFORE控制包含顺序
include_directories(BEFORE ${CMAKE_BINARY_DIR})  # 优先使用构建目录
include_directories(AFTER /usr/include)          # 最后使用系统目录
```

### 4.4 调试include路径
```cmake
# 打印所有include路径
get_property(dirs DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY INCLUDE_DIRECTORIES)
foreach(dir ${dirs})
  message(STATUS "Include dir: ${dir}")
endforeach()

# 检查特定目标的include路径
get_target_property(inc_dirs my_target INCLUDE_DIRECTORIES)
message("Target include dirs: ${inc_dirs}")
```

## 5. 常见模式和示例

### 5.1 项目结构include设置
```cmake
# 典型的项目结构
project(MyProject)

# 设置模块路径
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

# 自动包含当前目录
set(CMAKE_INCLUDE_CURRENT_DIR ON)

# 包含标准模块
include(GNUInstallDirs)
include(FeatureSummary)

# 添加子目录
add_subdirectory(src)
add_subdirectory(include)

# 在子目录中使用
# src/CMakeLists.txt
target_include_directories(my_lib
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../include>
    $<INSTALL_INTERFACE:include>
)
```

### 5.2 第三方库集成
```cmake
# 查找包
find_package(Qt6 REQUIRED COMPONENTS Core)

# 使用包的include路径
target_include_directories(my_target
  PRIVATE ${Qt6Core_PRIVATE_INCLUDE_DIRS}
)

# 或让find_package自动处理
target_link_libraries(my_target Qt6::Core)
```

## 6. 注意事项

1. **优先使用target_include_directories()**: 这是现代CMake推荐的方法，提供更好的封装性。

2. **避免全局include_directories()**: 除非确实需要全局包含，否则使用target-specific方法。

3. **使用生成器表达式**: 对于条件包含和构建/安装时的不同路径。

4. **包含顺序**: 使用AFTER/BEFORE参数控制搜索顺序。

5. **调试**: 使用get_property()和message()调试include路径问题。

6. **跨平台兼容性**: 使用CMAKE_SYSTEM_INCLUDE_PATH等变量确保跨平台兼容。

## 7. 实际项目示例

基于当前项目的CMakeLists.txt分析：

```cmake
# 根CMakeLists.txt中的include设置
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/")
include(WaylandScannerHelpers)
include(cmake/WaylandScannerHelpers.cmake)
include(cmake/DefineImplModule.cmake)

# compositor/CMakeLists.txt中的include设置
set(CMAKE_INCLUDE_CURRENT_DIR ON)
target_include_directories(${TARGET}
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_BINARY_DIR}/protocols>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_BINDIR}>
  PRIVATE ${Qt6Gui_PRIVATE_INCLUDE_DIRS}
)
```

这些设置展示了实际项目中include方法的综合应用。