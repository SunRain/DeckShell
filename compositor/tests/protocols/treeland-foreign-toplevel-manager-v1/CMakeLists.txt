treeland_add_protocol_test(
    NAME treeland_foreign_toplevel_manager_v1
    XML "${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-foreign-toplevel-manager-v1.xml"
    SETUP "${CMAKE_CURRENT_SOURCE_DIR}/setup.cpp"
    CLIENT "${CMAKE_CURRENT_SOURCE_DIR}/treeland-foreign-toplevel-manager-v1.c"
)
