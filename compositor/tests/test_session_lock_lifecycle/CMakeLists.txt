# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

find_package(Qt6 REQUIRED COMPONENTS Core Test)
find_package(PkgConfig REQUIRED)
pkg_search_module(WAYLAND_CLIENT REQUIRED IMPORTED_TARGET wayland-client)
pkg_get_variable(WLR_PROTOCOLS_DATA_DIR wlr-protocols pkgdatadir)
pkg_get_variable(WAYLAND_PROTOCOLS_DATA_DIR wayland-protocols pkgdatadir)
find_program(WAYLAND_SCANNER_EXECUTABLE wayland-scanner REQUIRED)

set(PROTOCOL_XML
    ${WAYLAND_PROTOCOLS_DATA_DIR}/staging/ext-session-lock/ext-session-lock-v1.xml
)
set(PROTOCOL_HEADER
    ${CMAKE_CURRENT_BINARY_DIR}/ext-session-lock-v1-client-protocol.h
)
set(PROTOCOL_CODE
    ${CMAKE_CURRENT_BINARY_DIR}/ext-session-lock-v1-protocol.c
)

set(OUTPUT_MANAGEMENT_XML
    ${WLR_PROTOCOLS_DATA_DIR}/unstable/wlr-output-management-unstable-v1.xml
)
set(OUTPUT_MANAGEMENT_HEADER
    ${CMAKE_CURRENT_BINARY_DIR}/wlr-output-management-unstable-v1-client-protocol.h
)
set(OUTPUT_MANAGEMENT_CODE
    ${CMAKE_CURRENT_BINARY_DIR}/wlr-output-management-unstable-v1-protocol.c
)

add_custom_command(
    OUTPUT ${PROTOCOL_HEADER}
    COMMAND ${WAYLAND_SCANNER_EXECUTABLE} client-header ${PROTOCOL_XML} ${PROTOCOL_HEADER}
    DEPENDS ${PROTOCOL_XML}
    VERBATIM
)

add_custom_command(
    OUTPUT ${PROTOCOL_CODE}
    COMMAND ${WAYLAND_SCANNER_EXECUTABLE} private-code ${PROTOCOL_XML} ${PROTOCOL_CODE}
    DEPENDS ${PROTOCOL_XML}
    VERBATIM
)

add_custom_command(
    OUTPUT ${OUTPUT_MANAGEMENT_HEADER}
    COMMAND ${WAYLAND_SCANNER_EXECUTABLE} client-header ${OUTPUT_MANAGEMENT_XML} ${OUTPUT_MANAGEMENT_HEADER}
    DEPENDS ${OUTPUT_MANAGEMENT_XML}
    VERBATIM
)

add_custom_command(
    OUTPUT ${OUTPUT_MANAGEMENT_CODE}
    COMMAND ${WAYLAND_SCANNER_EXECUTABLE} private-code ${OUTPUT_MANAGEMENT_XML} ${OUTPUT_MANAGEMENT_CODE}
    DEPENDS ${OUTPUT_MANAGEMENT_XML}
    VERBATIM
)

add_executable(test_session_lock_lifecycle
    main.cpp
    sessionlockclient.cpp
    sessionlockclient.h
    outputresizeclient.cpp
    outputresizeclient.h
    ${PROTOCOL_HEADER}
    ${PROTOCOL_CODE}
    ${OUTPUT_MANAGEMENT_HEADER}
    ${OUTPUT_MANAGEMENT_CODE}
)

target_compile_definitions(test_session_lock_lifecycle
    PRIVATE
        DECKCOMPOSITOR_EXECUTABLE="$<TARGET_FILE:deckcompositor>"
)

if(NOT DISABLE_DDM)
    target_compile_definitions(test_session_lock_lifecycle
        PRIVATE
            SESSION_LOCK_WITH_DDM=1
    )
endif()

target_include_directories(test_session_lock_lifecycle
    PRIVATE
        ${CMAKE_CURRENT_BINARY_DIR}
)

target_link_libraries(test_session_lock_lifecycle
    PRIVATE
        Qt::Core
        Qt::Test
        PkgConfig::WAYLAND_CLIENT
)

add_dependencies(test_session_lock_lifecycle deckcompositor)

add_test(NAME test_session_lock_lifecycle COMMAND test_session_lock_lifecycle)
set_tests_properties(test_session_lock_lifecycle PROPERTIES TIMEOUT 60)
