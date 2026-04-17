
local_qtwayland_server_protocol_treeland(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-virtual-output-manager-v1.xml
    BASENAME treeland-virtual-output-manager-v1
)

impl_deckcompositor(
    NAME
        module_virtualoutput
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/virtualoutputmanagerinterfacev1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/virtualoutputmanagerinterfacev1.cpp
        ${CMAKE_CURRENT_BINARY_DIR}/wayland-treeland-virtual-output-manager-v1-server-protocol.c
    LINK
        PkgConfig::WLROOTS
        WaylibShared::SharedServer
        Qt6::Core
        Qt6::Gui
        Qt6::Quick
)
