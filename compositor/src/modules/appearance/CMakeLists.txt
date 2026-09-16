
# --- New protocols (treeland-protocols 0.6.0) ---
waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-appearance-unstable-v1.xml
    BASENAME treeland-appearance-unstable-v1
)

waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-appearance-manager-unstable-v1.xml
    BASENAME treeland-appearance-manager-unstable-v1
)

set(PUBLIC_HEADERS
    ${PROJECT_SOURCE_DIR}/src/modules/appearance/appearanceinterfacev1.h
    ${PROJECT_SOURCE_DIR}/src/modules/appearance/appearancemanagerinterfacev1.h
)

set(SRCS
    ${PROJECT_SOURCE_DIR}/src/modules/appearance/appearanceinterfacev1.cpp
    ${PROJECT_SOURCE_DIR}/src/modules/appearance/appearancemanagerinterfacev1.cpp
)

impl_deckcompositor(
    NAME
        module_appearance
    SOURCE
        ${PUBLIC_HEADERS}
        ${SRCS}
    INCLUDE
        $<BUILD_INTERFACE:${WAYLAND_PROTOCOLS_OUTPUTDIR}>
)

if(TREELAND_INSTALL_DEV)
    install(FILES ${PUBLIC_HEADERS} DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/treeland/modules/appearance")
endif()
