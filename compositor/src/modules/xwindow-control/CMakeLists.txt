
waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-xwindow-control-unstable-v1.xml
    BASENAME treeland-xwindow-control-unstable-v1
)

impl_deckcompositor(
    NAME
        module_xwindow_control
    SOURCE
        ${PROJECT_SOURCE_DIR}/src/modules/xwindow-control/xwindowcontrolinterfacev1.h
        ${PROJECT_SOURCE_DIR}/src/modules/xwindow-control/xwindowcontrolinterfacev1.cpp
    LINK
        WaylibShared::waylib-wlroots
        WaylibShared::SharedServer
        Qt6::Core
        Qt6::Gui
        Qt6::Quick
)
