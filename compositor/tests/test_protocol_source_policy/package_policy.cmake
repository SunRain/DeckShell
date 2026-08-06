# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

if(NOT DEFINED DECKSHELL_SOURCE_DIR)
    message(FATAL_ERROR "DECKSHELL_SOURCE_DIR is required")
endif()

get_filename_component(DECKSHELL_SOURCE_DIR "${DECKSHELL_SOURCE_DIR}" REALPATH)
set(protocols_dir "${DECKSHELL_SOURCE_DIR}/protocols/compositor")

function(read_required file_path output_variable)
    if(NOT EXISTS "${file_path}")
        message(FATAL_ERROR "Required package file not found: ${file_path}")
    endif()
    file(READ "${file_path}" file_content)
    set(${output_variable} "${file_content}" PARENT_SCOPE)
endfunction()

function(require_text file_path expected_text)
    read_required("${file_path}" file_content)
    string(FIND "${file_content}" "${expected_text}" text_offset)
    if(text_offset EQUAL -1)
        message(FATAL_ERROR "${file_path} is missing package policy: ${expected_text}")
    endif()
endfunction()

function(reject_text file_path rejected_text)
    read_required("${file_path}" file_content)
    string(FIND "${file_content}" "${rejected_text}" text_offset)
    if(NOT text_offset EQUAL -1)
        message(FATAL_ERROR "${file_path} still contains legacy package metadata: ${rejected_text}")
    endif()
endfunction()

set(protocols_cmake "${protocols_dir}/CMakeLists.txt")
set(package_cmake "${protocols_dir}/cmake/CMakeLists.txt")
set(config_template "${protocols_dir}/cmake/DeckCompositorProtocolsConfig.cmake.in")
set(pkgconfig_template "${protocols_dir}/cmake/deckcompositor-protocols.pc.in")

require_text("${protocols_cmake}" "project(DeckCompositorProtocols VERSION 0.5.9)")
require_text("${package_cmake}" "configure_package_config_file(")
require_text("${config_template}" "@PACKAGE_INIT@")
require_text("${config_template}" "DECKCOMPOSITOR_PROTOCOLS_DATA_DIR")
require_text("${config_template}" "DeckCompositorProtocols_VERSION")
reject_text("${config_template}" "TREELAND_PROTOCOLS_DATA_DIR")
reject_text("${config_template}" "TreelandProtocols_VERSION")
reject_text("${config_template}" "TREELAND_PROTOCOLS_VERSION")
require_text("${pkgconfig_template}" "deckcompositor_protocols_datadir=")

file(GLOB protocol_xml_files RELATIVE "${protocols_dir}"
    "${protocols_dir}/xml/*.xml")
list(LENGTH protocol_xml_files protocol_xml_count)
if(NOT protocol_xml_count EQUAL 22)
    message(FATAL_ERROR "Expected 22 protocol XML files, found ${protocol_xml_count}")
endif()

read_required("${protocols_cmake}" protocols_cmake_content)
foreach(protocol_xml IN LISTS protocol_xml_files)
    string(FIND "${protocols_cmake_content}" "${protocol_xml}" xml_offset)
    if(xml_offset EQUAL -1)
        message(FATAL_ERROR "Protocol XML is missing from the install list: ${protocol_xml}")
    endif()
endforeach()

if(DEFINED DECKCOMPOSITOR_INSTALL_PREFIX)
    get_filename_component(
        DECKCOMPOSITOR_INSTALL_PREFIX
        "${DECKCOMPOSITOR_INSTALL_PREFIX}"
        REALPATH)
    find_package(DeckCompositorProtocols 0.5.9 EXACT CONFIG REQUIRED
        PATHS "${DECKCOMPOSITOR_INSTALL_PREFIX}"
        NO_DEFAULT_PATH)

    set(expected_data_dir
        "${DECKCOMPOSITOR_INSTALL_PREFIX}/share/DeckShell/compositor-protocols")
    get_filename_component(expected_data_dir "${expected_data_dir}" REALPATH)
    get_filename_component(
        actual_data_dir
        "${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}"
        REALPATH)
    if(NOT actual_data_dir STREQUAL expected_data_dir)
        message(FATAL_ERROR
            "Installed package exported ${actual_data_dir}, expected ${expected_data_dir}")
    endif()

    file(GLOB installed_protocol_xml_files "${actual_data_dir}/*.xml")
    list(LENGTH installed_protocol_xml_files installed_protocol_xml_count)
    if(NOT installed_protocol_xml_count EQUAL 22)
        message(FATAL_ERROR
            "Installed package must contain 22 XML files, found ${installed_protocol_xml_count}")
    endif()
endif()
