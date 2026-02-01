find_package(TreelandProtocols REQUIRED)

local_qtwayland_server_protocol_treeland(libdeckcompositor
    PROTOCOL ${TREELAND_PROTOCOLS_DATA_DIR}/treeland-output-manager-v1.xml
    BASENAME treeland-output-manager-v1
)

impl_treeland(
    NAME
        module_outputmanager
    SOURCE
        outputmanagement.h
        outputmanagement.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/wayland-treeland-output-manager-v1-server-protocol.c
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
