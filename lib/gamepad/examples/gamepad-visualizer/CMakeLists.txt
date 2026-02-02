# Gamepad Visualizer - Qt Widgets visualization tool for gamepad testing
# Ported from qwlroots commit 01adb2350ef31f5a597c255d0f56d1ab04938d72

cmake_minimum_required(VERSION 3.25)

project(gamepad-visualizer
    VERSION 1.0.0
    LANGUAGES CXX
    DESCRIPTION "Qt Widgets gamepad visualizer using DeckShell Gamepad library"
)

# C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Qt settings
set(CMAKE_AUTOMOC ON)

# Find Qt
find_package(Qt6 6.8 REQUIRED COMPONENTS Core Gui Widgets)

# Source files
set(SOURCES
    main.cpp
    gamepadviewer.h
    gamepadviewer.cpp
    gamepadwidget.h
    gamepadwidget.cpp
)

# Create executable
add_executable(gamepad-visualizer ${SOURCES})

# Link libraries
target_link_libraries(gamepad-visualizer
    PRIVATE
        deckshell-gamepad
        Qt6::Core
        Qt6::Gui
        Qt6::Widgets
)

# Display configuration
message(STATUS "gamepad-visualizer configured")
message(STATUS "  - Linked to deckshell-gamepad library")
message(STATUS "  - Qt version: ${Qt6_VERSION}")
