cmake_minimum_required(VERSION 3.25.0)

project(
  DeckShell
  VERSION 0.1
  LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

# Standard installation paths
include(GNUInstallDirs)
# Macros
include(FeatureSummary)


find_package(Qt6 REQUIRED COMPONENTS Core)

qt_standard_project_setup(REQUIRES 6.8)

set(PROJECT_SOURCES # Place your source files here
)

set(BUILD_TREELAND_EXAMPLES OFF)
set(BUILD_WAYLIB_TESTS OFF)
set(BUILD_WAYLIB_EXAMPLES OFF)
set(BUILD_QWLROOTS_TESTS OFF)
set(BUILD_QWLROOTS_EXAMPLES OFF)

# add_executable(DeckShell ${PROJECT_SOURCES}) target_link_libraries(DeckShell
# Qt${QT_VERSION_MAJOR}::Core)

# set(QT_QML_GENERATE_QMLLS_INI ON)

add_subdirectory(3rdparty/waylib-shared)
add_subdirectory(compositor)
