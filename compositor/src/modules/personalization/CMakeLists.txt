waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-personalization-manager-v1.xml
    BASENAME treeland-personalization-manager-v1
)

find_package(Dtk6Core REQUIRED)

set(PUBLIC_HEADERS
    ${CMAKE_CURRENT_SOURCE_DIR}/personalizationmanagerinterfacev1.h
)

set(SRCS
    ${CMAKE_CURRENT_SOURCE_DIR}/personalizationmanagerinterfacev1.cpp
)

impl_deckcompositor(
    NAME
        module_personalization
    SOURCE
        ${PUBLIC_HEADERS}
        ${SRCS}
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)

qt_add_resources(libdeckcompositor "default_background"
    PREFIX "/"
    FILES
        desktop.webp
)

install(FILES ${PUBLIC_HEADERS} DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/treeland/modules/personalization")
