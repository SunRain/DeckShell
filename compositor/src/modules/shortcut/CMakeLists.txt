find_package(DeckCompositorProtocols REQUIRED)

ws_generate_local(server ${TREELAND_PROTOCOLS_DATA_DIR}/treeland-shortcut-manager-v1.xml treeland-shortcut-manager-protocol)

impl_treeland(
    NAME
        module_shortcut
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/shortcutmanager.h
        ${CMAKE_CURRENT_SOURCE_DIR}/impl/shortcut_manager_impl.h
        ${CMAKE_CURRENT_SOURCE_DIR}/shortcutmanager.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/impl/shortcut_manager_impl.cpp
        ${WAYLAND_PROTOCOLS_OUTPUTDIR}/treeland-shortcut-manager-protocol.c
    LINK
        PkgConfig::WLROOTS
        Waylib::SharedServer
        Qt6::Core
        Qt6::Gui
        Qt6::Quick
)
