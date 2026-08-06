pkg_get_variable(WAYLAND_PROTOCOLS_DATADIR wayland-protocols pkgdatadir)

waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${WAYLAND_PROTOCOLS_DATADIR}/staging/xdg-activation/xdg-activation-v1.xml
    BASENAME xdg-activation-v1
)

impl_deckcompositor(
    NAME
        module_activation
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/activationmanagerinterfacev1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/activationmanagerinterfacev1.cpp
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
