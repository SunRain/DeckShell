waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-screensaver-v1.xml
    BASENAME treeland-screensaver-v1
)

impl_deckcompositor(
    NAME
        module_screensaver
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/screensaverinterfacev1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/screensaverinterfacev1.cpp
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
