local_qtwayland_server_protocol_treeland(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-ddm-v1.xml
    BASENAME treeland-ddm-v1
)

impl_deckcompositor(
    NAME
        module_ddm
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/ddminterfacev1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/ddminterfacev1.cpp
        ${CMAKE_CURRENT_BINARY_DIR}/wayland-treeland-ddm-v1-server-protocol.c
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
