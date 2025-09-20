cmake_minimum_required(VERSION 3.16)
project(DDEShellClient VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Qt6 packages
find_package(Qt6 REQUIRED COMPONENTS
    Core
    Gui
    Widgets
    Qml
    Quick
    WaylandClient
    WaylandClientPrivate
)

# 标准项目设置
qt_standard_project_setup(REQUIRES 6.5)

# 安装路径
include(GNUInstallDirs)
set(CMAKE_INSTALL_QMLDIR "${CMAKE_INSTALL_LIBDIR}/qt6/qml")

# 构建顺序
add_subdirectory(src)          # 共享库优先
add_subdirectory(declarative)  # QML plugin 依赖共享库
add_subdirectory(examples)     # 示例依赖共享库

# 导出 CMake 配置
install(EXPORT DDEShellClientTargets
    FILE DDEShellClientTargets.cmake
    NAMESPACE DDEShellClient::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/DDEShellClient
)

# 生成配置文件
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/DDEShellClientConfigVersion.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY AnyNewerVersion
)

configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/DDEShellClientConfig.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/DDEShellClientConfig.cmake"
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/DDEShellClient
)

install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/DDEShellClientConfig.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/DDEShellClientConfigVersion.cmake"
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/DDEShellClient
)
