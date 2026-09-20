
waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-window-transition-unstable-v1.xml
    BASENAME treeland-window-transition-unstable-v1
)

impl_deckcompositor(
    NAME
        module_window_transition
    SOURCE
        ${PROJECT_SOURCE_DIR}/src/modules/window-transition/windowtransitionmanagerinterfacev1.h
        ${PROJECT_SOURCE_DIR}/src/modules/window-transition/windowtransitionmanagerinterfacev1.cpp
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
    LINK
        Qt6::Core
)
