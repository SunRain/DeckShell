find_package(DeckCompositorProtocols REQUIRED)

local_qtwayland_server_protocol_treeland(libdeckcompositor
    PROTOCOL ${TREELAND_PROTOCOLS_DATA_DIR}/treeland-dde-shell-v1.xml
    BASENAME treeland-dde-shell-v1
)

impl_treeland(
    NAME
        module_ddeshell
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellmanagerinterfacev1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellattached.h
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellmanagerinterfacev1.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellattached.cpp
        ${CMAKE_CURRENT_BINARY_DIR}/wayland-treeland-dde-shell-v1-server-protocol.c
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
