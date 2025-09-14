find_package(DeckCompositorProtocols REQUIRED)

ws_generate_local(server ${TREELAND_PROTOCOLS_DATA_DIR}/treeland-personalization-manager-v1.xml treeland-personalization-manager-protocol)

find_package(Dtk6Core REQUIRED)

set(PUBLIC_HEADERS
    ${CMAKE_CURRENT_SOURCE_DIR}/personalizationmanager.h
    ${CMAKE_CURRENT_SOURCE_DIR}/impl/personalization_manager_impl.h
    ${CMAKE_CURRENT_SOURCE_DIR}/impl/appearance_impl.h
    ${CMAKE_CURRENT_SOURCE_DIR}/impl/types.h
    ${CMAKE_CURRENT_SOURCE_DIR}/impl/font_impl.h
)

set(SRCS
    ${CMAKE_CURRENT_SOURCE_DIR}/personalizationmanager.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/impl/personalization_manager_impl.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/impl/appearance_impl.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/impl/font_impl.cpp
    ${WAYLAND_PROTOCOLS_OUTPUTDIR}/treeland-personalization-manager-protocol.c
)

impl_treeland(
    NAME
        module_personalization
    SOURCE
        ${PUBLIC_HEADERS}
        ${SRCS}
)

qt_add_resources(libdeckcompositor "default_background"
    PREFIX "/"
    FILES
        desktop.webp
)

install(FILES ${PUBLIC_HEADERS} DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/treeland/modules/personalization")
