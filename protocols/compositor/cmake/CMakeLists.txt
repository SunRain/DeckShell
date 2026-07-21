include(CMakePackageConfigHelpers)

configure_package_config_file(
    DeckCompositorProtocolsConfig.cmake.in
    DeckCompositorProtocolsConfig.cmake
    INSTALL_DESTINATION "${DECKCOMPOSITOR_PROTOCOLS_INSTALL_CMAKEDIR}"
)
configure_file(DeckCompositorProtocolsConfigVersion.cmake.in DeckCompositorProtocolsConfigVersion.cmake @ONLY)
configure_file(deckcompositor-protocols.pc.in deckcompositor-protocols.pc @ONLY)

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/DeckCompositorProtocolsConfig.cmake
              ${CMAKE_CURRENT_BINARY_DIR}/DeckCompositorProtocolsConfigVersion.cmake
    DESTINATION "${DECKCOMPOSITOR_PROTOCOLS_INSTALL_CMAKEDIR}")

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/deckcompositor-protocols.pc
    DESTINATION ${CMAKE_INSTALL_DATADIR}/pkgconfig)
