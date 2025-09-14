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

find_package(Qt6 REQUIRED COMPONENTS Core)
if(Qt6_VERSION VERSION_GREATER_EQUAL 6.8)
    qt_standard_project_setup(REQUIRES 6.8)
else()
    set(CMAKE_AUTOMOC ON)
    set(CMAKE_AUTORCC ON)
    set(CMAKE_AUTOUIC ON)
endif()

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

find_package(Qt6 COMPONENTS REQUIRED Core Quick QuickControls2 WaylandCompositor Network DBus)
# Find DTK
find_package(Dtk6 REQUIRED COMPONENTS Core Declarative SystemSettings)

# Find Waylib
# Waylib is built as a submodule, so we don't need to find it
find_package(Waylib REQUIRED COMPONENTS SharedServer)

find_package(PkgConfig REQUIRED)
pkg_search_module(PIXMAN REQUIRED IMPORTED_TARGET pixman-1)
pkg_search_module(WAYLAND REQUIRED IMPORTED_TARGET wayland-server)
pkg_search_module(XCB REQUIRED IMPORTED_TARGET xcb)
# pkg_search_module(LIBINPUT REQUIRED IMPORTED_TARGET libinput)


# Waylib is built as a submodule, so we link directly to the target
# The Waylib::SharedServer target should be available from the waylib submodule


ws_generate(
    server
    wayland-protocols
    staging/color-management/color-management-v1.xml
    color-management-v1-protocol
)

add_executable(${TARGET}
    main.cpp
)

qt6_generate_wayland_protocol_server_sources(${TARGET}
    FILES
        ${CMAKE_CURRENT_SOURCE_DIR}/protocols/deckcompositor-shortcut-manager-v1.xml
        #${CMAKE_CURRENT_SOURCE_DIR}/protocols/treeland-dde-shell-v1.xml
)

qt_add_qml_module(${TARGET}
    URI DeckShell.Compositor
    VERSION "2.0"

    SOURCES treelandlogging.h treelandlogging.cpp
    SOURCES treelandconfig.h treelandconfig.cpp
    SOURCES helper.h helper.cpp
    SOURCES utils/cmdline.h utils/cmdline.cpp
    SOURCES surface/surfacewrapper.h surface/surfacewrapper.cpp
    SOURCES output.h output.cpp
    SOURCES qmlengine.h qmlengine.cpp
    SOURCES surface/surfacecontainer.h surface/surfacecontainer.cpp
    SOURCES layersurfacecontainer.h layersurfacecontainer.cpp
    SOURCES rootsurfacecontainer.h rootsurfacecontainer.cpp
    SOURCES surface/surfaceproxy.h surface/surfaceproxy.cpp
    SOURCES surface/surfacefilterproxymodel.h surface/surfacefilterproxymodel.cpp
    SOURCES wallpaperprovider.h wallpaperprovider.cpp
    SOURCES wallpaperimage.h wallpaperimage.cpp
    SOURCES workspace/workspace.h workspace/workspace.cpp
    SOURCES workspace/workspaceanimationcontroller.h workspace/workspaceanimationcontroller.cpp
    SOURCES workspace/workspacemodel.h workspace/workspacemodel.cpp
    # SOURCES shellmanager.h shellmanager.cpp # ShellManager files not found in target directory
    SOURCES shellhandler.h shellhandler.cpp
    SOURCES popupsurfacecontainer.h popupsurfacecontainer.cpp
    SOURCES interfaces/proxyinterface.h

    # Ensure QML types are properly registered
    DEPENDENCIES
        QtQuick
        QtQuick.Controls
        Waylib.QuickSharedServer

    QML_FILES qml/Border.qml
    QML_FILES qml/CopyOutput.qml
    QML_FILES qml/Decoration.qml
    QML_FILES qml/DockPreview.qml
    QML_FILES qml/FadeBehavior.qml
    QML_FILES qml/LockScreen.qml
    QML_FILES qml/OutputMenuBar.qml
    QML_FILES qml/PrimaryOutput.qml
    QML_FILES qml/RoundedClipEffect.qml
    QML_FILES qml/SurfaceContent.qml
    QML_FILES qml/SwitchViewDelegate.qml
    QML_FILES qml/SwitchViewHighlightDelegate.qml
    QML_FILES qml/TaskBar.qml
    QML_FILES qml/TaskSwitcher.qml
    QML_FILES qml/TaskWindowPreview.qml
    QML_FILES qml/TitleBar.qml
    QML_FILES qml/WindowMenu.qml
    QML_FILES qml/WindowPickerLayer.qml
    QML_FILES qml/WorkSpaceMask.qml
    QML_FILES qml/WorkspaceProxy.qml
    QML_FILES qml/WorkspaceSwitcher.qml
    QML_FILES qml/XdgShadow.qml
    QML_FILES qml/Animations/GeometryAnimation.qml
    QML_FILES qml/Animations/LaunchpadAnimation.qml
    QML_FILES qml/Animations/LayerShellAnimation.qml
    QML_FILES qml/Animations/MinimizeAnimation.qml
    QML_FILES qml/Animations/NewAnimation.qml
    QML_FILES qml/Animations/ShowDesktopAnimation.qml
    QML_FILES qml/Effects/Blur.qml
    QML_FILES qml/Effects/LaunchpadCover.qml

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
    Qt6::Network
    Dtk6::Core
    Qt6::DBus
    Dtk6::Declarative
    Dtk6::SystemSettings
    Waylib::SharedServer
    PkgConfig::PIXMAN
    PkgConfig::WAYLAND
    PkgConfig::XCB
)

install(TARGETS ${TARGET} DESTINATION ${CMAKE_INSTALL_BINDIR})

# Generate protocol files before adding dde-shell subdirectory
local_qtwayland_server_protocol_treeland(${TARGET}
    PROTOCOL ${CMAKE_CURRENT_SOURCE_DIR}/protocols/treeland-dde-shell-v1.xml
    BASENAME treeland-dde-shell-v1
)

add_subdirectory(dde-shell)

