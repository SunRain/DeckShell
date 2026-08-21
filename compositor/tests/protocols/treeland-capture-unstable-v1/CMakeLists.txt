treeland_add_protocol_test(
    NAME treeland_capture_unstable_v1
    XML "${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-capture-unstable-v1.xml"
    SETUP "${CMAKE_CURRENT_SOURCE_DIR}/setup.cpp"
    CLIENT "${CMAKE_CURRENT_SOURCE_DIR}/treeland-capture-unstable-v1.c"
)

# CaptureManagerV1 lives in the DeckShell.Compositor.Capture QML module library, which
# libdeckcompositor links privately (impl_deckcompositor), so link it explicitly here.
target_link_libraries(test_treeland_capture_unstable_v1 PRIVATE capture)
target_compile_definitions(test_treeland_capture_unstable_v1 PRIVATE WLR_USE_UNSTABLE)
