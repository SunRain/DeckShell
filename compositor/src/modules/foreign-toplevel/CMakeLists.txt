
local_qtwayland_server_protocol_treeland(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-foreign-toplevel-manager-v1.xml
    BASENAME treeland-foreign-toplevel-manager-v1
)

impl_deckcompositor(
    NAME
        module_foreigntoplevel
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/dockpreviewcontextv1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/foreigntoplevelhandlev1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/foreigntoplevelmanagerv1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/foreigntoplevelmanagerv1.cpp
        ${CMAKE_CURRENT_BINARY_DIR}/wayland-treeland-foreign-toplevel-manager-v1-server-protocol.c
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
