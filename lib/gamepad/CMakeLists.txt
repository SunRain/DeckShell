# DeckShell Gamepad Library
# Ported from qwlroots commit 01adb2350ef31f5a597c255d0f56d1ab04938d72
# Original Author: SunRain <41245110@qq.com>
# License: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

cmake_minimum_required(VERSION 3.16)

project(DeckShellGamepad
    VERSION 1.0.0
    LANGUAGES C CXX
    DESCRIPTION "Linux evdev-based gamepad driver library for DeckShell"
)

include(CTest)

set(_deckgamepad_is_top_level OFF)
if(CMAKE_SOURCE_DIR STREQUAL PROJECT_SOURCE_DIR)
    set(_deckgamepad_is_top_level ON)
endif()

# Build options（子项目默认仅构建 core，避免拖入 examples/QML/tests）
set(_deckgamepad_build_examples_default ON)
set(_deckgamepad_build_tests_default ON)
if(NOT _deckgamepad_is_top_level)
    set(_deckgamepad_build_examples_default OFF)
    set(_deckgamepad_build_tests_default OFF)
endif()

option(BUILD_GAMEPAD_EXAMPLES "Build gamepad examples (monitor and visualizer)" ${_deckgamepad_build_examples_default})
option(DECKGAMEPAD_BUILD_TESTS "Build DeckShellGamepad tests (standalone only by default)" ${_deckgamepad_build_tests_default})
option(BUILD_SHARED_LIBS "Build shared library instead of static" OFF)
unset(_deckgamepad_build_examples_default)
unset(_deckgamepad_build_tests_default)
unset(_deckgamepad_is_top_level)

# Add core library
add_subdirectory(src)

# Add QML module (optional)
if(DECKGAMEPAD_BUILD_QML_MODULE)
    add_subdirectory(qml)
endif()

# Add examples (optional)
if(BUILD_GAMEPAD_EXAMPLES)
    message(STATUS "Building gamepad examples")
    add_subdirectory(examples)
else()
    message(STATUS "Skipping gamepad examples (BUILD_GAMEPAD_EXAMPLES=OFF)")
endif()

if(DECKGAMEPAD_BUILD_TESTS)
    add_subdirectory(tests)

    add_custom_target(ctest-no-skip
        COMMAND "${CMAKE_COMMAND}" -E env "CTEST_OUTPUT_ON_FAILURE=1" "bash"
            "${CMAKE_CURRENT_SOURCE_DIR}/scripts/ctest_no_skip.sh"
            "${CMAKE_BINARY_DIR}"
        DEPENDS deckgamepad-tests
        WORKING_DIRECTORY "${CMAKE_BINARY_DIR}"
        COMMENT "Run ctest and fail on SKIP/Not Run"
        USES_TERMINAL
    )
endif()

# Display summary
message(STATUS "================================")
message(STATUS "DeckShell Gamepad Library v${PROJECT_VERSION}")
message(STATUS "Source: qwlroots commit 01adb235")
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "Library type: ${BUILD_SHARED_LIBS}")
message(STATUS "Build examples: ${BUILD_GAMEPAD_EXAMPLES}")
message(STATUS "================================")
