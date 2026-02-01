local_qtwayland_server_protocol_treeland(libdeckcompositor
    PROTOCOL ${CMAKE_SOURCE_DIR}/protocols/kde-keystate.xml
    BASENAME keystate
)

impl_treeland(
    NAME
        module_keystate
    SOURCE
        keystate.h
        keystate.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/wayland-keystate-server-protocol.c
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
    LINK
        Qt6::Core
)
