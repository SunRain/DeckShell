# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

if(NOT DEFINED DECKSHELL_SOURCE_DIR)
    message(FATAL_ERROR "DECKSHELL_SOURCE_DIR is required")
endif()

get_filename_component(DECKSHELL_SOURCE_DIR "${DECKSHELL_SOURCE_DIR}" REALPATH)

function(read_required file_path output_variable)
    if(NOT EXISTS "${file_path}")
        message(FATAL_ERROR "Required compatibility file not found: ${file_path}")
    endif()
    file(READ "${file_path}" file_content)
    set(${output_variable} "${file_content}" PARENT_SCOPE)
endfunction()

function(reject_text file_path rejected_text)
    read_required("${file_path}" file_content)
    string(FIND "${file_content}" "${rejected_text}" text_offset)
    if(NOT text_offset EQUAL -1)
        message(FATAL_ERROR "${file_path} still exposes removed compatibility wrapper: ${rejected_text}")
    endif()
endfunction()

set(define_target "${DECKSHELL_SOURCE_DIR}/compositor/cmake/DefineTarget.cmake")
set(compositor_sources "${DECKSHELL_SOURCE_DIR}/compositor/src/CMakeLists.txt")
set(misc_sources "${DECKSHELL_SOURCE_DIR}/compositor/misc/CMakeLists.txt")

reject_text("${define_target}" "function(impl_treeland)")
reject_text("${compositor_sources}" "libtreeland")
reject_text("${misc_sources}" "add_subdirectory(cmake)")

set(legacy_config_dir "${DECKSHELL_SOURCE_DIR}/compositor/misc/cmake")
if(EXISTS "${legacy_config_dir}/CMakeLists.txt" OR EXISTS "${legacy_config_dir}/TreelandConfig.cmake.in")
    message(FATAL_ERROR "The inactive TreelandConfig package wrapper must be removed: ${legacy_config_dir}")
endif()

file(GLOB_RECURSE active_cmake_files LIST_DIRECTORIES false
    "${DECKSHELL_SOURCE_DIR}/compositor/*.cmake"
    "${DECKSHELL_SOURCE_DIR}/compositor/CMakeLists.txt"
    "${DECKSHELL_SOURCE_DIR}/treeland-dde-shell-client/*.cmake"
    "${DECKSHELL_SOURCE_DIR}/treeland-dde-shell-client/CMakeLists.txt")
foreach(cmake_file IN LISTS active_cmake_files)
    if(cmake_file MATCHES "/test_protocol_source_policy/compatibility_policy\.cmake$")
        continue()
    endif()
    reject_text("${cmake_file}" "impl_treeland(")
    reject_text("${cmake_file}" "libtreeland")
endforeach()
