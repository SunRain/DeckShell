local_qtwayland_server_protocol_treeland(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-wine-window-state-unstable-v1.xml
    BASENAME treeland-wine-window-state-v1
)

impl_deckcompositor(
    NAME
        module_wine_window_state
    SOURCE
        winewindowstate.h
        winewindowstate.cpp
        ${CMAKE_CURRENT_BINARY_DIR}/wayland-treeland-wine-window-state-v1-server-protocol.c
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
    LINK
        Qt6::Core
)
