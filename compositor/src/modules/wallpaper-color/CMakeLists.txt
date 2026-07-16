local_qtwayland_server_protocol_treeland(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-wallpaper-color-v1.xml
    BASENAME treeland-wallpaper-color-v1
)

impl_deckcompositor(
    NAME
        module_wallpapercolor
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/wallpapercolorinterfacev1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/wallpapercolorinterfacev1.cpp
        ${CMAKE_CURRENT_BINARY_DIR}/wayland-treeland-wallpaper-color-v1-server-protocol.c
    LINK
        Wlroots::wlroots
        WaylibShared::SharedServer
        Qt6::Core
        Qt6::Gui
        Qt6::Quick
)
