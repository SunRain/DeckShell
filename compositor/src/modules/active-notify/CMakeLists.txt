
waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-active-notify-unstable-v1.xml
    BASENAME treeland-active-notify-unstable-v1
)

impl_deckcompositor(
    NAME
        module_active_notify
    SOURCE
        ${PROJECT_SOURCE_DIR}/src/modules/active-notify/activenotifymanagerinterfacev1.h
        ${PROJECT_SOURCE_DIR}/src/modules/active-notify/activenotifymanagerinterfacev1.cpp
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
