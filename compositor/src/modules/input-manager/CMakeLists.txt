local_qtwayland_server_protocol_treeland(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-input-manager-unstable-v1.xml
    BASENAME treeland-input-manager-unstable-v1
)

impl_deckcompositor(
    NAME
        module_input_manager
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/inputmanagerinterfacev1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/inputmanagerinterfacev1.cpp
        ${CMAKE_CURRENT_BINARY_DIR}/wayland-treeland-input-manager-unstable-v1-server-protocol.c
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
