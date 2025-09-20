cmake_minimum_required(VERSION 3.25.0)

project(
  DeckShell
  VERSION 0.1
  LANGUAGES CXX C)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/")
include(WaylandScannerHelpers)

# Standard installation paths
include(GNUInstallDirs)
# Macros
include(FeatureSummary)

include(cmake/WaylandScannerHelpers.cmake)
include(cmake/DefineImplModule.cmake)

find_package(Qt6 REQUIRED COMPONENTS Core)

qt_standard_project_setup(REQUIRES 6.8)

set(PROJECT_SOURCES # Place your source files here
)

set(BUILD_TREELAND_EXAMPLES OFF)
set(BUILD_WAYLIB_TESTS OFF)
set(BUILD_WAYLIB_EXAMPLES OFF)
set(BUILD_QWLROOTS_TESTS OFF)
set(BUILD_QWLROOTS_EXAMPLES OFF)


option(ENABLE_QT_DEBUG "Enable Qt debug features" OFF)
if(ENABLE_QT_DEBUG)
    add_compile_definitions("QT_DEBUG")
    set(COMPOSITOR_PLUGINS_ADD_BUILD_PATH ON)
    set(COMPOSITOR_ENABLE_CONSOLE_DEBUG_OUTPUT ON)
endif()


# add_executable(DeckShell ${PROJECT_SOURCES}) target_link_libraries(DeckShell
# Qt${QT_VERSION_MAJOR}::Core)

# set(QT_QML_GENERATE_QMLLS_INI ON)

# add_subdirectory(3rdparty/waylib-shared)
add_subdirectory(qtwaylandscanner)
add_subdirectory(dconfig2cpp)
add_subdirectory(protocols/compositor)
add_subdirectory(compositor)
