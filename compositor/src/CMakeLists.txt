if(QT_KNOWN_POLICY_QTP0001)
    qt_policy(SET QTP0001 NEW)
    # the RESOURCE_PREFIX argument for qt_add_qml_module() defaults to ":/qt/qml/"
endif()
if(POLICY CMP0071)
    # https://cmake.org/cmake/help/latest/policy/CMP0071.html
    cmake_policy(SET CMP0071 NEW)
endif()

# set(LIB_NAME libdeckcompositor)
set(BIN_NAME deckcompositor)

find_package(Dtk6 REQUIRED COMPONENTS Core Declarative SystemSettings Tools)
if (NOT DISABLE_DDM)
    find_package(DDM 0.2.0 REQUIRED COMPONENTS Common)
endif()
find_package(QT NAMES Qt6 COMPONENTS Core REQUIRED)
find_package(Qt6 CONFIG REQUIRED ShaderTools Concurrent RemoteObjects Network)
find_package(Qt6 COMPONENTS Quick QuickControls2 REQUIRED)
if(Qt6_VERSION VERSION_GREATER_EQUAL 6.10)
    find_package(Qt6 REQUIRED COMPONENTS QuickPrivate QuickTemplates2Private)
endif()
pkg_search_module(PIXMAN REQUIRED IMPORTED_TARGET pixman-1)
pkg_search_module(WAYLAND REQUIRED IMPORTED_TARGET wayland-server)
pkg_search_module(LIBINPUT REQUIRED IMPORTED_TARGET libinput)
pkg_search_module(XCB REQUIRED IMPORTED_TARGET xcb)
pkg_search_module(XCB_RANDR REQUIRED IMPORTED_TARGET xcb-randr)
if (NOT DISABLE_DDM)
    pkg_check_modules(PAM REQUIRED IMPORTED_TARGET pam)
endif()
pkg_check_modules(Systemd REQUIRED IMPORTED_TARGET libsystemd)
# qt_finalize_target will collect all executable's private dependencies that are CMake targets

configure_file("common/constants.h.in" "common/constants.h" IMMEDIATE @ONLY)
qt_add_dbus_adaptor(DBUS_ADAPTOR "${PROJECT_SOURCE_DIR}/misc/dbus/org.deepin.compositor1.xml" "core/treeland.h" Treeland::Treeland)

set_source_files_properties("${PROJECT_SOURCE_DIR}/misc/interfaces/org.freedesktop.DisplayManager.xml" PROPERTIES
    NO_NAMESPACE ON
    CLASSNAME DisplayManager
)
set_source_files_properties("${PROJECT_SOURCE_DIR}/misc/interfaces/org.freedesktop.DisplayManager.Seat.xml" PROPERTIES
    NO_NAMESPACE ON
    CLASSNAME DisplaySeat
)

set_source_files_properties("${PROJECT_SOURCE_DIR}/misc/interfaces/org.freedesktop.DisplayManager.Session.xml" PROPERTIES
    NO_NAMESPACE ON
    CLASSNAME DisplaySession
)

set_source_files_properties("${PROJECT_SOURCE_DIR}/misc/interfaces/org.freedesktop.login1.Manager.xml" PROPERTIES
   INCLUDE "${PROJECT_SOURCE_DIR}/src/utils/loginddbustypes.h"
)
set_source_files_properties("${PROJECT_SOURCE_DIR}/misc/interfaces/org.freedesktop.login1.Seat.xml" PROPERTIES
   INCLUDE "${PROJECT_SOURCE_DIR}/src/utils/loginddbustypes.h"
)

set_source_files_properties("${PROJECT_SOURCE_DIR}/misc/interfaces/org.freedesktop.login1.Session.xml" PROPERTIES
   INCLUDE "${PROJECT_SOURCE_DIR}/src/utils/loginddbustypes.h"
)

set_source_files_properties("${PROJECT_SOURCE_DIR}/misc/interfaces/org.freedesktop.login1.User.xml" PROPERTIES
   INCLUDE "${PROJECT_SOURCE_DIR}/src/utils/loginddbustypes.h"
)

qt_add_dbus_interface(DDM_DBUS_SOURCES "${PROJECT_SOURCE_DIR}/misc/interfaces/org.freedesktop.DisplayManager.xml"          DisplayManager)
qt_add_dbus_interface(DDM_DBUS_SOURCES "${PROJECT_SOURCE_DIR}/misc/interfaces/org.freedesktop.DisplayManager.Seat.xml"     DisplayManagerSeat)
qt_add_dbus_interface(DDM_DBUS_SOURCES "${PROJECT_SOURCE_DIR}/misc/interfaces/org.freedesktop.DisplayManager.Session.xml"  DisplayManagerSession)
qt_add_dbus_interface(DDM_DBUS_SOURCES "${PROJECT_SOURCE_DIR}/misc/interfaces/org.deepin.DisplayManager.xml"               DDMDisplayManager)
qt_add_dbus_interface(DBUS_INTERFACE   "${PROJECT_SOURCE_DIR}/misc/interfaces/org.freedesktop.login1.Manager.xml"          Login1Manager)
qt_add_dbus_interface(DBUS_INTERFACE   "${PROJECT_SOURCE_DIR}/misc/interfaces/org.freedesktop.login1.Seat.xml"             Login1Seat)
qt_add_dbus_interface(DBUS_INTERFACE   "${PROJECT_SOURCE_DIR}/misc/interfaces/org.freedesktop.login1.Session.xml"          Login1Session)
qt_add_dbus_interface(DBUS_INTERFACE   "${PROJECT_SOURCE_DIR}/misc/interfaces/org.freedesktop.login1.User.xml"             Login1User)

dtk_add_config_to_cpp(
    TREELAND_CONFIG
    "${PROJECT_SOURCE_DIR}/misc/dconfig/org.deepin.dde.treeland.json"
    OUTPUT_FILE_NAME "treelandconfig.hpp"
    CLASS_NAME "TreelandConfig"
)

dtk_add_config_to_cpp(
    TREELAND_USER_CONFIG
    "${PROJECT_SOURCE_DIR}/misc/dconfig/org.deepin.dde.treeland.user.json"
    OUTPUT_FILE_NAME "treelanduserconfig.hpp"
    CLASS_NAME "TreelandUserConfig"
)

dtk_add_config_to_cpp(
    OUTPUT_CONFIG
    "${PROJECT_SOURCE_DIR}/misc/dconfig/org.deepin.dde.treeland.output.json"
    OUTPUT_FILE_NAME "outputconfig.hpp"
    CLASS_NAME "OutputConfig"
)

dtk_add_config_to_cpp(
    SEAT_USER_CONFIG
    "${PROJECT_SOURCE_DIR}/misc/dconfig/org.deepin.dde.treeland.user.seat.json"
    OUTPUT_FILE_NAME "seatuserconfig.hpp"
    CLASS_NAME "SeatUserDConfig"
)

dtk_add_config_to_cpp(
    APP_CONFIG
    "${PROJECT_SOURCE_DIR}/misc/dconfig/org.deepin.dde.treeland.app.json"
    OUTPUT_FILE_NAME "appconfig.hpp"
    CLASS_NAME "AppConfig"
)

qt_add_library(libdeckcompositor SHARED)

set_target_properties(libdeckcompositor PROPERTIES
    OUTPUT_NAME "deckcompositor"
    VERSION ${CMAKE_PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR}
)

qt_add_qml_module(libdeckcompositor
    URI DeckShell.Compositor
    VERSION "2.0"
    IMPORTS WaylibShared.QuickSharedServer

    SOURCES
        ${DDM_DBUS_SOURCES}
        ${DBUS_INTERFACE}
        ${TREELAND_CONFIG}
        ${TREELAND_USER_CONFIG}
        ${OUTPUT_CONFIG}
        ${APP_CONFIG}
        ${SEAT_USER_CONFIG}
        common/treelandlogging.cpp
        common/treelandlogging.h
        core/layersurfacecontainer.cpp
        core/layersurfacecontainer.h
        core/qmlengine.cpp
        core/qmlengine.h
        core/rootsurfacecontainer.cpp
        core/rootsurfacecontainer.h
        core/imcandidatepanelmanager.cpp
        core/imcandidatepanelmanager.h
        core/shellhandler.cpp
        core/shellhandler.h
        core/treelandinit.cpp
        core/treeland.cpp
        core/treeland.h
        core/windowpicker.cpp
        core/windowpicker.h
        core/windowconfigstore.cpp
        core/windowconfigstore.h
        effects/tquickradiuseffect.cpp
        effects/tquickradiuseffect.h
        effects/tquickradiuseffect_p.h
        effects/tsgradiusimagenode.cpp
        effects/tsgradiusimagenode.h
        $<$<OR:$<NOT:$<BOOL:${DISABLE_DDM}>>,$<BOOL:${EXT_SESSION_LOCK_V1}>>:core/lockscreen.h>
        $<$<OR:$<NOT:$<BOOL:${DISABLE_DDM}>>,$<BOOL:${EXT_SESSION_LOCK_V1}>>:core/lockscreen.cpp>
        $<$<NOT:$<BOOL:${DISABLE_DDM}>>:greeter/greeterproxy.cpp>
        $<$<NOT:$<BOOL:${DISABLE_DDM}>>:greeter/greeterproxy.h>
        $<$<NOT:$<BOOL:${DISABLE_DDM}>>:greeter/sessionmodel.cpp>
        $<$<NOT:$<BOOL:${DISABLE_DDM}>>:greeter/sessionmodel.h>
        $<$<NOT:$<BOOL:${DISABLE_DDM}>>:greeter/user.cpp>
        $<$<NOT:$<BOOL:${DISABLE_DDM}>>:greeter/user.h>
        $<$<NOT:$<BOOL:${DISABLE_DDM}>>:greeter/usermodel.cpp>
        $<$<NOT:$<BOOL:${DISABLE_DDM}>>:greeter/usermodel.h>
        input/gestures.cpp
        input/gestures.h
        input/inputdevice.cpp
        input/inputdevice.h
        input/togglablegesture.cpp
        input/togglablegesture.h
        input/inputmanager.cpp
        input/inputmanager.h
        interfaces/baseplugininterface.h
        interfaces/lockscreeninterface.h
        interfaces/multitaskviewinterface.h
        interfaces/plugininterface.h
        interfaces/proxyinterface.h
        modules/resource/treelandremotesource.cpp
        modules/resource/treelandremotesource.h
        output/output.cpp
        output/output.h
        output/backlight.h
        output/backlight.cpp
        output/outputmanager.cpp
        output/outputmanager.h
        seat/helper.cpp
        seat/helper.h
        seat/pointerconstraintsmanager.cpp
        seat/pointerconstraintsmanager.h
        seat/seatsmanager.cpp
        seat/seatsmanager.h
        session/session.cpp
        session/session.h
        surface/surfacecontainer.cpp
        surface/surfacecontainer.h
        surface/seatsurfacemanager.cpp
        surface/seatsurfacemanager.h
        surface/surfacefilterproxymodel.cpp
        surface/surfacefilterproxymodel.h
        surface/surfaceproxy.cpp
        surface/surfaceproxy.h
        surface/surfacewrapper.cpp
        surface/surfacewrapper.h
        utils/cmdline.cpp
        utils/cmdline.h
        utils/propertymonitor.cpp
        utils/propertymonitor.h
        utils/singlematchconnection.h
        utils/loginddbustypes.h
        utils/loginddbustypes.cpp
        utils/fpsdisplaymanager.cpp
        utils/fpsdisplaymanager.h
        utils/scriptrunner.cpp
        utils/scriptrunner.h
        wallpaper/wallpapersurface.h
        wallpaper/wallpapersurface.cpp
        wallpaper/wallpaperitem.cpp
        wallpaper/wallpaperitem.h
        wallpaper/wallpapermanager.cpp
        wallpaper/wallpapermanager.h
        wallpaper/wallpaperconfig.h
        wallpaper/wallpaperconfig.cpp
        wallpaper/wallpaperlauncher.h
        wallpaper/wallpaperlauncher.cpp
        wallpaper/wallpaperswitcheritem.cpp
        wallpaper/wallpaperswitcheritem.h
        workspace/workspace.cpp
        workspace/workspace.h
        workspace/workspaceanimationcontroller.cpp
        workspace/workspaceanimationcontroller.h
        workspace/workspacemodel.cpp
        workspace/workspacemodel.h
        xsettings/abstractsettings.h
        xsettings/abstractsettings.cpp
        xsettings/xsettings.h
        xsettings/xsettings.cpp
        xsettings/xresource.h
        xsettings/xresource.cpp
        xsettings/settingmanager.h
        xsettings/settingmanager.cpp

    QML_FILES
        core/qml/SourceOutput.qml
        core/qml/MirrorOutput.qml
        core/qml/TitleBar.qml
        core/qml/Decoration.qml
        core/qml/WindowMenu.qml
        core/qml/TaskBar.qml
        core/qml/SurfaceContent.qml
        core/qml/XdgShadow.qml
        core/qml/Border.qml
        core/qml/OutputMenuBar.qml
        core/qml/WorkspaceSwitcher.qml
        core/qml/WorkspaceProxy.qml
        core/qml/FpsDisplay.qml
        core/qml/Animations/GeometryAnimation.qml
        core/qml/Animations/NewAnimation.qml
        core/qml/Animations/MinimizeAnimation.qml
        core/qml/Animations/ShowDesktopAnimation.qml
        core/qml/Animations/LaunchpadAnimation.qml
        core/qml/Animations/LayerShellAnimation.qml
        core/qml/Effects/Blur.qml
        core/qml/Effects/+vulkan/Blur.qml
        core/qml/Effects/GlassEffect.qml
        core/qml/Effects/LaunchpadCover.qml
        core/qml/TaskSwitcher.qml
        core/qml/TaskWindowPreview.qml
        core/qml/SwitchViewDelegate.qml
        core/qml/SwitchViewHighlightDelegate.qml
        core/qml/DockPreview.qml
        core/qml/FadeBehavior.qml
        core/qml/CaptureSelectorLayer.qml
        core/qml/WindowPickerLayer.qml
        core/qml/EdgeTilePreview.qml
        core/qml/LockScreenFallback.qml
        core/qml/PrelaunchSplash.qml
    RESOURCE_PREFIX
        /qt/qml
    OUTPUT_DIRECTORY
        ${PROJECT_BINARY_DIR}/qt/qml/DeckShell/Compositor
)

# Qt's generated install rules do not copy this module when the backing
# library is installed separately. Keep the module relocatable for staged
# installs and package builds instead of using an absolute system QML path.
set(_DECKSHELL_QML_INSTALL_DIR "${QT6_INSTALL_QML}")
if(NOT _DECKSHELL_QML_INSTALL_DIR OR IS_ABSOLUTE "${_DECKSHELL_QML_INSTALL_DIR}")
    set(_DECKSHELL_QML_INSTALL_DIR "${CMAKE_INSTALL_LIBDIR}/qt6/qml")
endif()
install(
    DIRECTORY "${PROJECT_BINARY_DIR}/qt/qml/DeckShell/Compositor/"
    DESTINATION "${_DECKSHELL_QML_INSTALL_DIR}/DeckShell/Compositor"
    COMPONENT DeckShellQmlRuntime
    FILES_MATCHING
        PATTERN "*.qml"
        PATTERN "*.qmltypes"
        PATTERN "qmldir"
)
set_target_properties(libdeckcompositorplugin PROPERTIES
    INSTALL_RPATH "$ORIGIN/../../../.."
)
# Qt's generated plugin install rule is kept for the default package
# component. The dedicated runtime component uses a file install so its
# component boundary remains explicit across Qt versions.
install(
    FILES "$<TARGET_FILE:libdeckcompositorplugin>"
    DESTINATION "${_DECKSHELL_QML_INSTALL_DIR}/DeckShell/Compositor"
    COMPONENT DeckShellQmlRuntime
)
install(
    CODE
        "file(RPATH_SET FILE \"\$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/${_DECKSHELL_QML_INSTALL_DIR}/DeckShell/Compositor/$<TARGET_FILE_NAME:libdeckcompositorplugin>\" NEW_RPATH \"\$ORIGIN/../../../..\")"
    COMPONENT DeckShellQmlRuntime
)
unset(_DECKSHELL_QML_INSTALL_DIR)

qt_add_repc_sources(libdeckcompositor
    modules/resource/treelandwindowtree.rep
)

set_property(TARGET libdeckcompositor APPEND PROPERTY AUTOMOC_MOC_OPTIONS
    "-b;${CMAKE_CURRENT_BINARY_DIR}/outputconfig.hpp"
)

target_compile_definitions(libdeckcompositor
    PRIVATE
    WLR_USE_UNSTABLE
    PROJECT_COMPILE_QML_DIR="${PROJECT_BINARY_DIR}/qt/qml/DeckShell/Compositor"

    "TREELAND_SYSCONFDIR=\"${TREELAND_SYSCONFDIR}\""
)

if (USE_BUILD_TREE_WALLPAPER_FACTORY)
    target_compile_definitions(libdeckcompositor
        PRIVATE
        TREELAND_USE_BUILD_TREE_WALLPAPER_FACTORY
        "TREELAND_WALLPAPER_FACTORY_OUTPUT_PATH=\"${PROJECT_BINARY_DIR}/wallpaper-factory/treeland-wallpaper-factory\""
    )
endif()

qt_add_shaders(libdeckcompositor "deckcompositor_shaders_ng"
    BATCHABLE
    PRECOMPILE
    PREFIX
        "/shaders"
    BASE
        ${PROJECT_RESOURCES_DIR}/shaders
    FILES
        ${PROJECT_RESOURCES_DIR}/shaders/radiussmoothtexture.vert
        ${PROJECT_RESOURCES_DIR}/shaders/radiussmoothtexture.frag
)

# Liquid Glass shaders are used with ShaderEffect, not custom QSGGeometry,
# so BATCHABLE is unnecessary (it only adds an unused batchable variant).
qt_add_shaders(libdeckcompositor "deckcompositor_liquidglass_shaders"
    PRECOMPILE
    OPTIMIZED
    PREFIX
        "/shaders"
    BASE
        ${PROJECT_RESOURCES_DIR}/shaders
    FILES
        ${PROJECT_RESOURCES_DIR}/shaders/liquidglass.vert
        ${PROJECT_RESOURCES_DIR}/shaders/liquidglass.frag
)

set_source_files_properties(core/qml/overridable/InWindowBlur.qml
    PROPERTIES
        QT_RESOURCE_ALIAS "+treeland/InWindowBlur.qml"
)
qt_add_resources(libdeckcompositor "override_dtkdeclarative_qml"
    PREFIX "/dtk/declarative/qml/overridable"
    FILES
        core/qml/overridable/InWindowBlur.qml
)

qt_add_resources(libdeckcompositor "deckcompositor_assets"
    PREFIX "/dsg/icons"
    BASE ${PROJECT_RESOURCES_DIR}/icons
    FILES
        ${PROJECT_RESOURCES_DIR}/icons/close.dci
        ${PROJECT_RESOURCES_DIR}/icons/add.dci
        ${PROJECT_RESOURCES_DIR}/icons/select_output.dci
        ${PROJECT_RESOURCES_DIR}/icons/select_window.dci
        ${PROJECT_RESOURCES_DIR}/icons/select_region.dci
        ${PROJECT_RESOURCES_DIR}/icons/login_capslock.dci
        ${PROJECT_RESOURCES_DIR}/icons/login_display_password.dci
        ${PROJECT_RESOURCES_DIR}/icons/login_hidden_password.dci
        ${PROJECT_RESOURCES_DIR}/icons/login_keyboard.dci
        ${PROJECT_RESOURCES_DIR}/icons/login_lock.dci
        ${PROJECT_RESOURCES_DIR}/icons/login_open.dci
        ${PROJECT_RESOURCES_DIR}/icons/login_power.dci
        ${PROJECT_RESOURCES_DIR}/icons/login_reboot.dci
        ${PROJECT_RESOURCES_DIR}/icons/login_hibernate.dci
        ${PROJECT_RESOURCES_DIR}/icons/login_user.dci
        ${PROJECT_RESOURCES_DIR}/icons/login_hint.dci
        ${PROJECT_RESOURCES_DIR}/icons/login_logout.dci
        ${PROJECT_RESOURCES_DIR}/icons/login_shutdown.dci
        ${PROJECT_RESOURCES_DIR}/icons/login_suspend.dci
        ${PROJECT_RESOURCES_DIR}/icons/login_switchuser.dci
        ${PROJECT_RESOURCES_DIR}/icons/login_update_reboot.dci
        ${PROJECT_RESOURCES_DIR}/icons/login_update_shutdown.dci
        ${PROJECT_RESOURCES_DIR}/icons/backToLightdm.dci
        ${PROJECT_RESOURCES_DIR}/icons/logo.svg
)

# Use translation utilities to setup main translations
setup_main_translations(libdeckcompositor)

target_include_directories(libdeckcompositor
    PUBLIC
        # $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/compositor/src>
        # $<BUILD_INTERFACE:${CMAKE_BINARY_DIR}/src>
        # $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/compositor/src/config>
        # $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/compositor/src/core>
        # $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/compositor/src/effects>
        # $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/compositor/src/greeter>
        # $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/compositor/src/input>
        # $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/compositor/src/interfaces>
        # $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/compositor/src/output>
        # $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/compositor/src/seat>
        # $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/compositor/src/surface>
        # $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/compositor/src/workspace>
        # $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/compositor/src/utils>
        # $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/compositor/src/wallpaper>
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/config>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/core>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/effects>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/greeter>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/input>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/interfaces>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/output>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/seat>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/session>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/surface>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/workspace>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/utils>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/wallpaper>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/deckcompositor>
)

target_link_libraries(libdeckcompositor
    PUBLIC
        Dtk6::Core
        Dtk6::Declarative
        Dtk6::SystemSettings
        WaylibShared::SharedServer
    PRIVATE
        Qt6::GuiPrivate
        Qt6::Quick
        Qt6::QuickControls2
        Qt6::QuickPrivate
        Qt6::QuickTemplates2Private
        Qt6::DBus
        Qt6::Concurrent
        Qt6::RemoteObjects
        Qt6::Network
        PkgConfig::PIXMAN
        PkgConfig::WAYLAND
        PkgConfig::LIBINPUT
        PkgConfig::XCB
        PkgConfig::XCB_RANDR
        $<$<NOT:$<BOOL:${DISABLE_DDM}>>:DDM::Common>
        $<$<NOT:$<BOOL:${DISABLE_DDM}>>:PkgConfig::PAM>
        $<$<NOT:$<BOOL:${DISABLE_DDM}>>:PkgConfig::Systemd>
)

add_subdirectory(plugins)
add_subdirectory(modules)
add_subdirectory(treeland-screensaver)

# Keep the staged QML smoke test self-contained without pulling in unrelated
# compositor executables and helpers from the default install component.
if(TARGET WaylibSharedServer)
    install(
        TARGETS WaylibSharedServer
        LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
        NAMELINK_SKIP
        COMPONENT DeckShellQmlRuntime
    )
endif()
if(TARGET capture)
    install(
        TARGETS capture
        LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
        NAMELINK_SKIP
        COMPONENT DeckShellQmlRuntime
    )
endif()

if(TARGET waylib_wlroots_native_library)
    install(
        TARGETS waylib_wlroots_native_library
        LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
        NAMELINK_SKIP
        COMPONENT DeckShellQmlRuntime
    )
endif()

qt_add_executable(${BIN_NAME}
    main.cpp
)

target_include_directories(${BIN_NAME} PRIVATE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/core/>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/interfaces/>
)

target_link_libraries(${BIN_NAME} PRIVATE
    libdeckcompositor
    Qt6::GuiPrivate
    Qt6::QuickControls2
)

install(TARGETS ${BIN_NAME} RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}")
install(PROGRAMS treeland.sh DESTINATION "${CMAKE_INSTALL_BINDIR}")
install(TARGETS libdeckcompositor
    LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    NAMELINK_SKIP
    COMPONENT DeckShellQmlRuntime
)
if(TREELAND_INSTALL_DEV)
    install(TARGETS libdeckcompositor
        LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
        NAMELINK_ONLY
    )
endif()

## systemd socket

qt_add_executable(treeland-sd
    systemd-socket.cpp
)

target_link_libraries(treeland-sd
    PRIVATE
        Qt6::DBus
        PkgConfig::Systemd
)

install(TARGETS treeland-sd RUNTIME DESTINATION "${CMAKE_INSTALL_LIBEXECDIR}")

## XWayland wrapper

pkg_check_modules(LIBXAU REQUIRED IMPORTED_TARGET "xau")

qt_add_executable(treeland-xwayland
    xwayland.cpp
)

target_link_libraries(treeland-xwayland
    PRIVATE
        Qt6::Core
        PkgConfig::LIBXAU
)

install(TARGETS treeland-xwayland RUNTIME DESTINATION "${CMAKE_INSTALL_LIBEXECDIR}")
