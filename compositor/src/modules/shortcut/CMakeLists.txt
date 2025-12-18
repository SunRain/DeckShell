find_package(DeckCompositorProtocols REQUIRED)

local_qtwayland_server_protocol_treeland(libtreeland
    PROTOCOL ${TREELAND_PROTOCOLS_DATA_DIR}/treeland-shortcut-manager-v2.xml
    BASENAME treeland-shortcut-manager-v2
)

impl_treeland(
    NAME
        module_shortcut
    SOURCE
        shortcutmanager.h
        shortcutmanager.cpp
        shortcutrunner.h
        shortcutrunner.cpp
        shortcutcontroller.h
        shortcutcontroller.cpp
    ${CMAKE_BINARY_DIR}/src/modules/shortcut/wayland-treeland-shortcut-manager-v2-server-protocol.c
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
    LINK
        PkgConfig::WLROOTS
        Waylib::SharedServer
        Qt6::Core
        Qt6::Gui
        Qt6::Quick
)
