set(virtual_keyboard_xml "${WaylibShared_WLROOTS_PROTOCOLS_DIR}/virtual-keyboard-unstable-v1.xml")
if(NOT EXISTS "${virtual_keyboard_xml}")
    message(FATAL_ERROR "WaylibShared development package is missing ${virtual_keyboard_xml}")
endif()

treeland_add_protocol_test(
    NAME treeland_shortcut_manager_desktop_v2
    XML "${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-shortcut-manager-v2.xml"
    EXTRA_XMLS "${virtual_keyboard_xml}"
    EXTRA_LIBRARIES PkgConfig::XKBCOMMON
    SETUP "${CMAKE_CURRENT_SOURCE_DIR}/setup.cpp"
    CLIENT "${CMAKE_CURRENT_SOURCE_DIR}/treeland-shortcut-manager-desktop-v2.c"
)
