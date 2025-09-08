cmake_minimum_required(VERSION 3.16)

project(DeckCompositor
        VERSION 0.1
        LANGUAGES C CXX
        DESCRIPTION "Deck Shell Compositor")

set(TARGET deckcompositor)

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

qt_standard_project_setup(REQUIRES 6.8)

if(QT_KNOWN_POLICY_QTP0001) # this policy was introduced in Qt 6.5
    qt_policy(SET QTP0001 NEW)
    # the RESOURCE_PREFIX argument for qt_add_qml_module() defaults to ":/qt/qml/"
endif()
if(POLICY CMP0071)
    # https://cmake.org/cmake/help/latest/policy/CMP0071.html
    cmake_policy(SET CMP0071 NEW)
endif()


# Standard installation paths
include(GNUInstallDirs)
# Macros
include(FeatureSummary)

# include(cmake/DefineTarget.cmake)

option(START_DEMO "Start demo when boot" ON)

# set(QT_QML_GENERATE_QMLLS_INI ON)

set(LOCAL_QML_IMPORT_PATH "${QML_IMPORT_PATH}")
list(APPEND LOCAL_QML_IMPORT_PATH "${PROJECT_BINARY_DIR}")

set(QML_IMPORT_PATH "${LOCAL_QML_IMPORT_PATH}" CACHE STRING "For LSP" FORCE)

find_package(Qt6 COMPONENTS REQUIRED Core Quick QuickControls2 )
# Find Waylib
# Waylib is built as a submodule, so we don't need to find it
# find_package(Waylib REQUIRED COMPONENTS SharedServer)

find_package(PkgConfig REQUIRED)
pkg_search_module(PIXMAN REQUIRED IMPORTED_TARGET pixman-1)
pkg_search_module(WAYLAND REQUIRED IMPORTED_TARGET wayland-server)

# Waylib is built as a submodule, so we link directly to the target
# The Waylib::SharedServer target should be available from the waylib submodule

add_executable(${TARGET}
    main.cpp
)

qt_add_qml_module(${TARGET}
    URI DeckShell.Compositor
    VERSION "2.0"

    SOURCES helper.h helper.cpp
    SOURCES surfacewrapper.h surfacewrapper.cpp
    SOURCES workspace.h workspace.cpp
    SOURCES output.h output.cpp
    SOURCES qmlengine.h qmlengine.cpp
    SOURCES surfacecontainer.h surfacecontainer.cpp
    SOURCES layersurfacecontainer.h layersurfacecontainer.cpp
    SOURCES rootsurfacecontainer.h rootsurfacecontainer.cpp
    SOURCES surfaceproxy.h surfaceproxy.cpp
    SOURCES wallpaperprovider.h wallpaperprovider.cpp
    SOURCES wallpaperimage.h wallpaperimage.cpp
    SOURCES workspacemodel.h workspacemodel.cpp

    QML_FILES PrimaryOutput.qml
    QML_FILES CopyOutput.qml
    QML_FILES TitleBar.qml
    QML_FILES Decoration.qml
    QML_FILES TaskBar.qml
    QML_FILES RoundedClipEffect.qml
    QML_FILES SurfaceContent.qml
    QML_FILES Shadow.qml
    QML_FILES Border.qml
    QML_FILES GeometryAnimation.qml
    QML_FILES OutputMenuBar.qml
    QML_FILES WorkspaceSwitcher.qml
    QML_FILES WorkspaceProxy.qml
    QML_FILES WindowMenu.qml

    RESOURCES
    "res/xx.jpg"
)

target_compile_definitions(${TARGET}
    PRIVATE
    SOURCE_DIR="${CMAKE_CURRENT_SOURCE_DIR}"
    PROJECT_BINARY_DIR="${PROJECT_BINARY_DIR}"
    $<$<BOOL:${START_DEMO}>:START_DEMO>
)

target_include_directories(
    ${TARGET}
    PUBLIC 
    $<BUILD_INTERFACE:${CMAKE_BINARY_DIR}/protocols>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_BINDIR}>
    PRIVATE ${Qt6Gui_PRIVATE_INCLUDE_DIRS} ${Qt6Quick_PRIVATE_INCLUDE_DIRS}
    ${Qt6EglSupport_PRIVATE_INCLUDE_DIRS}
    ${Qt6InputSupport_PRIVATE_INCLUDE_DIRS}
)

target_link_libraries(${TARGET}
    PRIVATE
    Qt6::Quick
    Qt6::QuickControls2
    Qt6::QuickPrivate
    Waylib::SharedServer
    PkgConfig::PIXMAN
    PkgConfig::WAYLAND
)

install(TARGETS ${TARGET} DESTINATION ${CMAKE_INSTALL_BINDIR})

