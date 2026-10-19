
waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-output-uuid-unstable-v1.xml
    BASENAME treeland-output-uuid-unstable-v1
)

pkg_get_variable(WLR_PROTOCOLS_DATA_DIR wlr-protocols pkgdatadir)

# treeland-output-uuid-head-unstable-v1 takes a zwlr_output_head_v1 argument, so
# its generated code needs zwlr_output_head_v1_interface. waylib-wlroots only
# exports wlr_*/waylib_* (see 3rdparty/wlroots/wlroots.syms), which hides that
# symbol, so generate the wlr-output-management protocol into libdeckcompositor too.
waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${WLR_PROTOCOLS_DATA_DIR}/unstable/wlr-output-management-unstable-v1.xml
    BASENAME wlr-output-management-unstable-v1
)

waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-output-uuid-head-unstable-v1.xml
    BASENAME treeland-output-uuid-head-unstable-v1
)

impl_deckcompositor(
    NAME
        module_output_uuid
    SOURCE
        ${PROJECT_SOURCE_DIR}/src/modules/output-uuid/outputuuidmanagerinterfacev1.h
        ${PROJECT_SOURCE_DIR}/src/modules/output-uuid/outputuuidmanagerinterfacev1.cpp
    INCLUDE
        $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
)
