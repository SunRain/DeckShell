
waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-foreign-toplevel-manager-unstable-v3.xml
    BASENAME treeland-foreign-toplevel-manager-unstable-v3
)

impl_deckcompositor(
    NAME
        module_foreigntoplevel
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/dockpreviewcontextv3.h
        ${CMAKE_CURRENT_SOURCE_DIR}/foreigntoplevelhandlev3.h
        ${CMAKE_CURRENT_SOURCE_DIR}/foreigntoplevelmanagerv3.h
        ${CMAKE_CURRENT_SOURCE_DIR}/foreigntoplevelmanagerv3.cpp
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
