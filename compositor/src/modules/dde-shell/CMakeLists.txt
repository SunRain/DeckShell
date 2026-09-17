
# --- Deprecated v1 protocol (kept for transition until dde-shell migrates) ---
# TODO: Remove the v1 protocol and its module sources
# (ddeshellmanagerinterfacev1.*, ddeshellattached.*) in a future release
# once dde-shell has migrated to treeland-dde-shell-unstable-v2.
waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-dde-shell-v1.xml
    BASENAME treeland-dde-shell-v1
)

waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-dde-shell-unstable-v2.xml
    BASENAME treeland-dde-shell-unstable-v2
)

impl_deckcompositor(
    NAME
        module_ddeshell
    SOURCE
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellmanagerinterfacev1.h
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellattached.h
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellmanagerinterfacev1.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellattached.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellmanagerinterfacev2.h
        ${CMAKE_CURRENT_SOURCE_DIR}/ddeshellmanagerinterfacev2.cpp
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
