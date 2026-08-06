waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-prelaunch-splash-v2.xml
    BASENAME treeland-prelaunch-splash-v2
)

impl_deckcompositor(
    NAME
        module_prelaunch_splash
    SOURCE
        prelaunchsplash.h
        prelaunchsplash.cpp
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
    LINK
        Qt6::Core
)
