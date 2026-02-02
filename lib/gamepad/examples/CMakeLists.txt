# DeckShell Gamepad Examples
# Console monitor and GUI visualizer tools

cmake_minimum_required(VERSION 3.25)

# Add example subdirectories
if(DECKGAMEPAD_BUILD_TREELAND_CLIENT)
    add_subdirectory(gamepad-wayland-monitor)
    add_subdirectory(gamepad-test-suite)
else()
    add_subdirectory(gamepad-monitor)
    add_subdirectory(gamepad-visualizer)
endif()

# CLI configuration tool (always built)
add_subdirectory(gamepad-cli)

# Minimal consumer demo (core/service only, internal reuse baseline)
add_subdirectory(gamepad-consumer-minimal)

if(DECKGAMEPAD_BUILD_QML_MODULE)
    add_subdirectory(qml-gamepad-demo)
endif()

message(STATUS "Gamepad examples configured:")
message(STATUS "  - gamepad-monitor (console event monitor, evdev)")
message(STATUS "  - gamepad-visualizer (Qt Widgets visualizer, evdev)")
message(STATUS "  - gamepad-config (CLI configuration tool)")
message(STATUS "  - gamepad-consumer-minimal (core/service only consumer demo)")
message(STATUS "  - qml-gamepad-demo (Qt Quick demo for DeckShell.DeckGamepad)")
