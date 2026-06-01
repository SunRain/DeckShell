local_qtwayland_server_protocol_treeland(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-keyboard-state-notify-unstable-v1.xml
    BASENAME treeland-keyboard-state-notify-unstable-v1
)

impl_deckcompositor(
    NAME
        module_keyboard_state_notify
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/keyboardstatenotifymanagerinterfacev1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/keyboardstatenotifymanagerinterfacev1.cpp
        ${CMAKE_CURRENT_BINARY_DIR}/wayland-treeland-keyboard-state-notify-unstable-v1-server-protocol.c
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
