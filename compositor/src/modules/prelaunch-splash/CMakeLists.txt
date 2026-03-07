find_package(TreelandProtocols 0.5.5 REQUIRED)

local_qtwayland_server_protocol_treeland(libdeckcompositor
    PROTOCOL ${TREELAND_PROTOCOLS_DATA_DIR}/treeland-prelaunch-splash-v2.xml
    BASENAME treeland-prelaunch-splash-v2
)

impl_deckcompositor(
    NAME
        module_prelaunch_splash
    SOURCE
        prelaunchsplash.h
        prelaunchsplash.cpp
        ${CMAKE_CURRENT_BINARY_DIR}/wayland-treeland-prelaunch-splash-v2-server-protocol.c
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
    LINK
        Qt6::Core
)
