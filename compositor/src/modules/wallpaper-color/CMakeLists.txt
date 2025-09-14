find_package(DeckCompositorProtocols REQUIRED)

ws_generate_local(server ${TREELAND_PROTOCOLS_DATA_DIR}/treeland-wallpaper-color-v1.xml treeland-wallpaper-color-protocol)

impl_treeland(
    NAME
        module_wallpapercolor
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/wallpapercolor.h
        ${CMAKE_CURRENT_SOURCE_DIR}/impl/wallpaper_color_impl.h
        ${CMAKE_CURRENT_SOURCE_DIR}/wallpapercolor.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/impl/wallpaper_color_impl.cpp
        ${WAYLAND_PROTOCOLS_OUTPUTDIR}/treeland-wallpaper-color-protocol.c
    LINK
        PkgConfig::WLROOTS
        Waylib::SharedServer
        Qt6::Core
        Qt6::Gui
        Qt6::Quick
)
