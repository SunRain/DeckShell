pkg_get_variable(WLR_PROTOCOLS_DATA_DIR wlr-protocols pkgdatadir)

treeland_add_protocol_test(
    NAME treeland_output_group_manager_v1
    XML "${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-output-group-manager-unstable-v1.xml"
    SETUP "${CMAKE_CURRENT_SOURCE_DIR}/setup.cpp"
    CLIENT "${CMAKE_CURRENT_SOURCE_DIR}/treeland-output-group-manager-v1.c"
    EXTRA_XMLS
        "${WLR_PROTOCOLS_DATA_DIR}/unstable/wlr-output-management-unstable-v1.xml"
)
