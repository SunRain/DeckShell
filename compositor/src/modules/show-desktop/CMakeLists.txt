
waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-show-desktop-unstable-v1.xml
    BASENAME treeland-show-desktop-unstable-v1
)

impl_deckcompositor(
    NAME
        module_showdesktop
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/showdesktopinterfacev1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/showdesktopinterfacev1.cpp
    LINK
        WaylibShared::waylib-wlroots
        WaylibShared::SharedServer
        Qt6::Core
        Qt6::Gui
        Qt6::Quick
)
