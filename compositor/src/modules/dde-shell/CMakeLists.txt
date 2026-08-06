waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-dde-shell-v1.xml
    BASENAME treeland-dde-shell-v1
)

impl_deckcompositor(
    NAME
        module_ddeshell
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellmanagerinterfacev1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellattached.h
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellmanagerinterfacev1.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellattached.cpp
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
