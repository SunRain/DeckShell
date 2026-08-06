waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-shortcut-manager-v2.xml
    BASENAME treeland-shortcut-manager-v2
)

impl_deckcompositor(
    NAME
        module_shortcut
    SOURCE
        shortcutmanager.h
        shortcutmanager.cpp
        shortcutrunner.h
        shortcutrunner.cpp
        shortcutcontroller.h
        shortcutcontroller.cpp
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
    LINK
        Wlroots::wlroots
        WaylibShared::SharedServer
        Qt6::Core
        Qt6::Gui
        Qt6::Quick
)
