# find_package(TreelandProtocols REQUIRED)

# Protocol files are now generated in parent CMakeLists.txt

impl_module(
    NAME
        module_ddeshell
    MAIN_TARGET
        ${TARGET}
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellmanagerinterfacev1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellattached.h
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellmanagerinterfacev1.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellattached.cpp
        ${WAYLAND_PROTOCOLS_OUTPUTDIR}/qwayland-server-treeland-dde-shell-v1.cpp
        ${WAYLAND_PROTOCOLS_OUTPUTDIR}/wayland-treeland-dde-shell-v1-server-protocol.c
    INCLUDE
        $<BUILD_INTERFACE:${WAYLAND_PROTOCOLS_OUTPUTDIR}>
)