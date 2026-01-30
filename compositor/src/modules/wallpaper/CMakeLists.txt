find_package(TreelandProtocols REQUIRED)

local_qtwayland_server_protocol_treeland(libdeckcompositor
    PROTOCOL ${TREELAND_PROTOCOLS_DATA_DIR}/treeland-wallpaper-manager-unstable-v1.xml
    BASENAME treeland-wallpaper-manager-unstable-v1
)

local_qtwayland_server_protocol_treeland(libdeckcompositor
    PROTOCOL ${TREELAND_PROTOCOLS_DATA_DIR}/treeland-wallpaper-shell-unstable-v1.xml
    BASENAME treeland-wallpaper-shell-unstable-v1
)

impl_deckcompositor(
    NAME
        module_wallpaper
    SOURCE
        wallpapermanagerinterfacev1.h
        wallpapermanagerinterfacev1.cpp
        wallpapershellinterfacev1.h
        wallpapershellinterfacev1.cpp
        wallpapernotifierinterfacev1.h
        wallpapernotifierinterfacev1.cpp
        ${CMAKE_CURRENT_BINARY_DIR}/wayland-treeland-wallpaper-manager-unstable-v1-server-protocol.c
        ${CMAKE_CURRENT_BINARY_DIR}/wayland-treeland-wallpaper-shell-unstable-v1-server-protocol.c
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
