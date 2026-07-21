# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

if(NOT DEFINED DECKSHELL_SOURCE_DIR)
    message(FATAL_ERROR "DECKSHELL_SOURCE_DIR is required")
endif()

get_filename_component(DECKSHELL_SOURCE_DIR "${DECKSHELL_SOURCE_DIR}" REALPATH)

function(read_required file_path output_variable)
    if(NOT EXISTS "${file_path}")
        message(FATAL_ERROR "Required CMake file not found: ${file_path}")
    endif()
    file(READ "${file_path}" file_content)
    set(${output_variable} "${file_content}" PARENT_SCOPE)
endfunction()

function(require_text file_path expected_text)
    read_required("${file_path}" file_content)
    string(FIND "${file_content}" "${expected_text}" text_offset)
    if(text_offset EQUAL -1)
        message(FATAL_ERROR "${file_path} is missing required protocol source policy: ${expected_text}")
    endif()
endfunction()

set(protocols_cmake "${DECKSHELL_SOURCE_DIR}/protocols/compositor/CMakeLists.txt")
set(compositor_cmake "${DECKSHELL_SOURCE_DIR}/compositor/CMakeLists.txt")
set(client_cmake "${DECKSHELL_SOURCE_DIR}/treeland-dde-shell-client/CMakeLists.txt")

require_text("${protocols_cmake}"
    [=[set(DECKCOMPOSITOR_PROTOCOLS_DATA_DIR "${CMAKE_CURRENT_SOURCE_DIR}/xml")]=])
require_text("${protocols_cmake}"
    "if(NOT CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)")
require_text("${protocols_cmake}"
    [=[set(DECKCOMPOSITOR_PROTOCOLS_DATA_DIR "${CMAKE_CURRENT_SOURCE_DIR}/xml" PARENT_SCOPE)]=])
require_text("${compositor_cmake}"
    "if(NOT DEFINED DECKCOMPOSITOR_PROTOCOLS_DATA_DIR)")
require_text("${compositor_cmake}"
    "find_package(DeckCompositorProtocols 0.5.9 REQUIRED)")
require_text("${client_cmake}"
    "if(NOT DEFINED DECKCOMPOSITOR_PROTOCOLS_DATA_DIR)")
require_text("${client_cmake}"
    "find_package(DeckCompositorProtocols 0.5.9 REQUIRED)")

file(GLOB_RECURSE protocol_consumer_files LIST_DIRECTORIES false
    "${DECKSHELL_SOURCE_DIR}/compositor/src/CMakeLists.txt"
    "${DECKSHELL_SOURCE_DIR}/compositor/src/*.cmake"
    "${DECKSHELL_SOURCE_DIR}/compositor/tests/CMakeLists.txt"
    "${DECKSHELL_SOURCE_DIR}/compositor/tests/*.cmake"
    "${DECKSHELL_SOURCE_DIR}/compositor/examples/CMakeLists.txt"
    "${DECKSHELL_SOURCE_DIR}/compositor/examples/*.cmake"
    "${DECKSHELL_SOURCE_DIR}/compositor/tools/CMakeLists.txt"
    "${DECKSHELL_SOURCE_DIR}/compositor/tools/*.cmake"
    "${DECKSHELL_SOURCE_DIR}/compositor/wallpaper-factory/CMakeLists.txt"
    "${DECKSHELL_SOURCE_DIR}/treeland-dde-shell-client/src/CMakeLists.txt"
    "${DECKSHELL_SOURCE_DIR}/treeland-dde-shell-client/src/*.cmake"
)

foreach(consumer_file IN LISTS protocol_consumer_files)
    if(consumer_file MATCHES "/test_protocol_source_policy/")
        continue()
    endif()

    read_required("${consumer_file}" consumer_content)

    string(REGEX MATCH
        "find_package\\((DeckCompositorProtocols|TreelandProtocols)"
        package_lookup "${consumer_content}")
    if(package_lookup)
        message(FATAL_ERROR
            "Protocol consumer must inherit the canonical source instead of looking up a package: ${consumer_file}")
    endif()

    string(FIND "${consumer_content}" "TREELAND_PROTOCOLS_DATA_DIR" legacy_offset)
    if(NOT legacy_offset EQUAL -1)
        message(FATAL_ERROR
            "Protocol consumer still uses TREELAND_PROTOCOLS_DATA_DIR: ${consumer_file}")
    endif()

    string(FIND "${consumer_content}"
        "\${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}treeland-"
        missing_separator_offset)
    if(NOT missing_separator_offset EQUAL -1)
        message(FATAL_ERROR
            "Protocol source path is missing a separator after the canonical directory: ${consumer_file}")
    endif()
endforeach()
