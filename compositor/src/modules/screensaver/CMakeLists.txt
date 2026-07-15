
ws_generate_local(server ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-screensaver-v1.xml treeland-screensaver-v1-protocol)

impl_deckcompositor(
    NAME
        module_screensaver
    SOURCE
        screensaverinterfacev1.h
        screensaverinterfacev1.cpp
        ${WAYLAND_PROTOCOLS_OUTPUTDIR}/treeland-screensaver-v1-protocol.c
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
