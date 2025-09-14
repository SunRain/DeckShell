find_package(DeckCompositorProtocols REQUIRED)

ws_generate_local(server ${TREELAND_PROTOCOLS_DATA_DIR}/treeland-ddm-v1.xml treeland-ddm-v1-protocol)

impl_treeland(
    NAME
        module_ddm
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/ddminterfacev1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/ddminterfacev1.cpp
        ${WAYLAND_PROTOCOLS_OUTPUTDIR}/treeland-ddm-v1-protocol.c
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
