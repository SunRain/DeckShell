
waylib_generate_qtwayland_server_protocol(libdeckcompositor
    PROTOCOL ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-output-group-manager-unstable-v1.xml
    BASENAME treeland-output-group-manager-unstable-v1
)

impl_deckcompositor(
    NAME
        module_outputgroup
    SOURCE
        ${PROJECT_SOURCE_DIR}/src/modules/output-group/outputgroupmanagerinterfacev1.h
        ${PROJECT_SOURCE_DIR}/src/modules/output-group/outputgroupmanagerinterfacev1.cpp
    LINK
        WaylibShared::waylib-wlroots
        WaylibShared::SharedServer
        Qt6::Core
        Qt6::Gui
        Qt6::Quick
)
