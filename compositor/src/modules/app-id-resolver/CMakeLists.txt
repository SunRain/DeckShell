waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-app-id-resolver-v1.xml
    BASENAME treeland-app-id-resolver-v1
)

impl_deckcompositor(
    NAME
        module_app_id_resolver
    SOURCE
        appidresolver.h
        appidresolver.cpp
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
    LINK
        Qt6::Core
)
