waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-output-manager-v1.xml
    BASENAME treeland-output-manager-v1
)

impl_deckcompositor(
    NAME
        module_outputmanager
    SOURCE
        outputmanagement.h
        outputmanagement.cpp
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
