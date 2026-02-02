cmake_minimum_required(VERSION 3.16)
project(gamepad-test-suite VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

# Find Qt6
find_package(Qt6 6.8 REQUIRED COMPONENTS Core Widgets)

# Sources
set(SOURCES
    main.cpp
    gamepadtestsuite.h
    gamepadtestsuite.cpp
    monitorwidget.h
    monitorwidget.cpp
    visualizerwidget.h
    visualizerwidget.cpp
    vibrationwidget.h
    vibrationwidget.cpp
    simplegamewidget.h
    simplegamewidget.cpp
    inputmapperwidget.h
    inputmapperwidget.cpp
)

# Executable
add_executable(gamepad-test-suite ${SOURCES})

# Include directories
target_include_directories(gamepad-test-suite PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/../../src
)

# Link libraries
target_link_libraries(gamepad-test-suite PRIVATE
    Qt6::Core
    Qt6::Widgets
    deckshell-gamepad-treeland
)

# Install
install(TARGETS gamepad-test-suite
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

message(STATUS "Gamepad Test Suite configuration:")
message(STATUS "  Qt6 version: ${Qt6_VERSION}")
message(STATUS "  C++ standard: ${CMAKE_CXX_STANDARD}")
