# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

foreach(required_variable IN ITEMS DECKSHELL_SOURCE_DIR DECKSHELL_BINARY_DIR)
    if(NOT DEFINED ${required_variable})
        message(FATAL_ERROR "${required_variable} is required")
    endif()
endforeach()

get_filename_component(DECKSHELL_SOURCE_DIR "${DECKSHELL_SOURCE_DIR}" REALPATH)
get_filename_component(DECKSHELL_BINARY_DIR "${DECKSHELL_BINARY_DIR}" REALPATH)

function(read_required file_path output_variable)
    if(NOT EXISTS "${file_path}")
        message(FATAL_ERROR "Required protocol contract file not found: ${file_path}")
    endif()
    file(READ "${file_path}" file_content)
    set(${output_variable} "${file_content}" PARENT_SCOPE)
endfunction()

function(require_text file_path expected_text)
    read_required("${file_path}" file_content)
    string(FIND "${file_content}" "${expected_text}" text_offset)
    if(text_offset EQUAL -1)
        message(FATAL_ERROR "${file_path} is missing protocol contract: ${expected_text}")
    endif()
endfunction()

function(require_regex file_path expected_regex description)
    read_required("${file_path}" file_content)
    string(REGEX MATCH "${expected_regex}" matched_text "${file_content}")
    if(NOT matched_text)
        message(FATAL_ERROR "${file_path} is missing ${description}")
    endif()
endfunction()

function(require_ordered_text file_path)
    read_required("${file_path}" file_content)
    set(previous_offset -1)
    foreach(expected_text IN LISTS ARGN)
        string(FIND "${file_content}" "${expected_text}" text_offset)
        if(text_offset EQUAL -1)
            message(FATAL_ERROR "${file_path} is missing generated request: ${expected_text}")
        endif()
        if(text_offset LESS_EQUAL previous_offset)
            message(FATAL_ERROR "${file_path} has an unexpected generated request order at: ${expected_text}")
        endif()
        set(previous_offset ${text_offset})
    endforeach()
endfunction()

set(dde_xml "${DECKSHELL_SOURCE_DIR}/protocols/compositor/xml/treeland-dde-shell-v1.xml")
set(personalization_xml
    "${DECKSHELL_SOURCE_DIR}/protocols/compositor/xml/treeland-personalization-manager-v1.xml")
set(virtual_output_xml
    "${DECKSHELL_SOURCE_DIR}/protocols/compositor/xml/treeland-virtual-output-manager-v1.xml")

set(dde_header
    "${DECKSHELL_SOURCE_DIR}/compositor/src/modules/dde-shell/ddeshellmanagerinterfacev1.h")
set(dde_source
    "${DECKSHELL_SOURCE_DIR}/compositor/src/modules/dde-shell/ddeshellmanagerinterfacev1.cpp")
set(dde_client_cmake
    "${DECKSHELL_SOURCE_DIR}/treeland-dde-shell-client/src/CMakeLists.txt")
set(personalization_header
    "${DECKSHELL_SOURCE_DIR}/compositor/src/modules/personalization/personalizationmanagerinterfacev1.h")
set(virtual_output_header
    "${DECKSHELL_SOURCE_DIR}/compositor/src/modules/virtual-output/virtualoutputmanagerinterfacev1.h")

foreach(protocol_xml IN ITEMS "${dde_xml}" "${personalization_xml}" "${virtual_output_xml}")
    require_regex("${protocol_xml}"
        "<interface name=\"treeland_[a-z_]+_manager_v1\" version=\"2\">"
        "a version 2 manager interface")
endforeach()

foreach(manager_header IN ITEMS
        "${dde_header}"
        "${personalization_header}"
        "${virtual_output_header}")
    require_text("${manager_header}" "static constexpr int InterfaceVersion = 2;")
endforeach()

require_regex("${dde_source}"
    "void set_xwindow_position_relative\\([^;]*\\) override;"
    "the DDE relative-position handler override")
require_text("${dde_client_cmake}" "NO_INCLUDE_CORE_ONLY")

set(generated_module_dir "${DECKSHELL_BINARY_DIR}/src/modules")
set(dde_generated
    "${generated_module_dir}/dde-shell/wayland-treeland-dde-shell-v1-server-protocol.c")
set(personalization_generated
    "${generated_module_dir}/personalization/wayland-treeland-personalization-manager-v1-server-protocol.c")
set(virtual_output_generated
    "${generated_module_dir}/virtual-output/wayland-treeland-virtual-output-manager-v1-server-protocol.c")

require_ordered_text("${dde_generated}"
    [=[{ "get_window_overlap_checker",]=]
    [=[{ "get_shell_surface",]=]
    [=[{ "get_treeland_dde_active",]=]
    [=[{ "get_treeland_multitaskview",]=]
    [=[{ "get_treeland_window_picker",]=]
    [=[{ "get_treeland_lockscreen",]=]
    [=[{ "set_xwindow_position_relative",]=]
    [=[{ "destroy", "2",]=])
require_text("${dde_generated}"
    [=["treeland_dde_shell_manager_v1", 2,]=])

get_filename_component(deckshell_build_root "${DECKSHELL_BINARY_DIR}" DIRECTORY)
set(dde_client_generated
    "${deckshell_build_root}/treeland-dde-shell-client/src/wayland-treeland-dde-shell-v1-client-protocol.h")
require_text("${dde_client_generated}" [=[#include "wayland-client.h"]=])
require_text("${dde_client_generated}" "&wl_callback_interface")

require_ordered_text("${personalization_generated}"
    [=[{ "get_window_context",]=]
    [=[{ "get_cursor_context",]=]
    [=[{ "get_font_context",]=]
    [=[{ "get_appearance_context",]=]
    [=[{ "destroy", "2",]=])
require_text("${personalization_generated}"
    [=["treeland_personalization_manager_v1", 2,]=])

require_ordered_text("${virtual_output_generated}"
    [=[{ "create_virtual_output",]=]
    [=[{ "get_virtual_output_list",]=]
    [=[{ "get_virtual_output",]=]
    [=[{ "destroy", "2",]=])
require_text("${virtual_output_generated}"
    [=["treeland_virtual_output_manager_v1", 2,]=])
