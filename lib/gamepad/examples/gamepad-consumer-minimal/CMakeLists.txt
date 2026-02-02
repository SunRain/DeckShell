# Minimal DeckGamepad consumer demo (internal reuse baseline: core/service only)

cmake_minimum_required(VERSION 3.25)

project(gamepad-consumer-minimal VERSION 1.0.0 LANGUAGES CXX)

find_package(Qt6 6.8 REQUIRED COMPONENTS Core)

set(_deckgamepad_target deckshell-gamepad)
if(NOT TARGET ${_deckgamepad_target})
    find_package(DeckShellGamepad CONFIG REQUIRED)
    set(_deckgamepad_target DeckShell::deckshell-gamepad)
endif()

add_executable(gamepad-consumer-minimal
    main.cpp
)

target_link_libraries(gamepad-consumer-minimal
    PRIVATE
        Qt6::Core
        ${_deckgamepad_target}
)

target_compile_features(gamepad-consumer-minimal PRIVATE cxx_std_17)

install(TARGETS gamepad-consumer-minimal
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

message(STATUS "Gamepad consumer minimal demo configured:")
message(STATUS "  - Executable: gamepad-consumer-minimal")
message(STATUS "  - Target: ${_deckgamepad_target}")
message(STATUS "  - Qt6 version: ${Qt6_VERSION}")

