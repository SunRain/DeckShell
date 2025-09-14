find_package(DeckCompositorProtocols REQUIRED)

ws_generate_local(server ${TREELAND_PROTOCOLS_DATA_DIR}/treeland-window-management-v1.xml treeland-window-management-protocol)

impl_treeland(
    NAME
        module_windowmanagement
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/windowmanagement.h
        ${CMAKE_CURRENT_SOURCE_DIR}/impl/window_management_impl.h
        ${CMAKE_CURRENT_SOURCE_DIR}/windowmanagement.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/impl/window_management_impl.cpp
        ${WAYLAND_PROTOCOLS_OUTPUTDIR}/treeland-window-management-protocol.c
    LINK
        PkgConfig::WLROOTS
        Waylib::SharedServer
        Qt6::Core
        Qt6::Gui
        Qt6::Quick
)
