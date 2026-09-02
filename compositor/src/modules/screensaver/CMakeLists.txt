waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-screensaver-unstable-v2.xml
    BASENAME treeland-screensaver-unstable-v2
)

impl_deckcompositor(
    NAME
        module_screensaver
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/screensaverinterfacev2.h
        ${CMAKE_CURRENT_SOURCE_DIR}/screensaverinterfacev2.cpp
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
