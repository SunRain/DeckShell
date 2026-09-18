
waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-region-watch-unstable-v1.xml
    BASENAME treeland-region-watch-unstable-v1
)

impl_deckcompositor(
    NAME
        module_region_watch
    SOURCE
        ${PROJECT_SOURCE_DIR}/src/modules/region-watch/regionwatchmanagerinterfacev1.h
        ${PROJECT_SOURCE_DIR}/src/modules/region-watch/regionwatchmanagerinterfacev1.cpp
    LINK
        WaylibShared::waylib-wlroots
        WaylibShared::SharedServer
        Qt6::Core
        Qt6::Gui
        Qt6::Quick
)
