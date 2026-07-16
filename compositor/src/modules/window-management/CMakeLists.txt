local_qtwayland_server_protocol_treeland(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-window-management-v1.xml
    BASENAME treeland-window-management-v1
)

impl_deckcompositor(
    NAME
        module_windowmanagement
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/windowmanagementinterfacev1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/windowmanagementinterfacev1.cpp
        ${CMAKE_CURRENT_BINARY_DIR}/wayland-treeland-window-management-v1-server-protocol.c
    LINK
        Wlroots::wlroots
        WaylibShared::SharedServer
        Qt6::Core
        Qt6::Gui
        Qt6::Quick
)
