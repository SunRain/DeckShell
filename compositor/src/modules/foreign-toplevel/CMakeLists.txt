find_package(DeckCompositorProtocols REQUIRED)

ws_generate_local(server ${TREELAND_PROTOCOLS_DATA_DIR}/treeland-foreign-toplevel-manager-v1.xml treeland-foreign-toplevel-manager-protocol)

impl_treeland(
    NAME
        module_foreigntoplevel
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/foreigntoplevelmanagerv1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/impl/foreign_toplevel_manager_impl.h
        ${CMAKE_CURRENT_SOURCE_DIR}/foreigntoplevelmanagerv1.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/impl/foreign_toplevel_manager_impl.cpp
        ${WAYLAND_PROTOCOLS_OUTPUTDIR}/treeland-foreign-toplevel-manager-protocol.c
    INCLUDE
        $<BUILD_INTERFACE:${WAYLAND_PROTOCOLS_OUTPUTDIR}>
)
