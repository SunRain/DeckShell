waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-wine-window-state-unstable-v1.xml
    BASENAME treeland-wine-window-state-unstable-v1
)

impl_deckcompositor(
    NAME
        module_wine_window_state
    SOURCE
        winewindowstate.h
        winewindowstate.cpp
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
    LINK
        Qt6::Core
)
