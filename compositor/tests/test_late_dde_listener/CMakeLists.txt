# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

find_package(Qt6 REQUIRED COMPONENTS Gui Test)
find_package(PkgConfig REQUIRED)
pkg_get_variable(WAYLAND_PROTOCOLS_DATA_DIR wayland-protocols pkgdatadir)
pkg_search_module(WAYLAND_CLIENT REQUIRED IMPORTED_TARGET wayland-client)
find_program(WAYLAND_SCANNER_EXECUTABLE wayland-scanner REQUIRED)

set(XDG_SHELL_XML
    ${WAYLAND_PROTOCOLS_DATA_DIR}/stable/xdg-shell/xdg-shell.xml
)
set(XDG_SHELL_HEADER
    ${CMAKE_CURRENT_BINARY_DIR}/xdg-shell-client-protocol.h
)
set(XDG_SHELL_CODE
    ${CMAKE_CURRENT_BINARY_DIR}/xdg-shell-protocol.c
)
set(DDE_SHELL_XML
    ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-dde-shell-v1.xml
)
set(DDE_SHELL_HEADER
    ${CMAKE_CURRENT_BINARY_DIR}/treeland-dde-shell-v1-client-protocol.h
)
set(DDE_SHELL_CODE
    ${CMAKE_CURRENT_BINARY_DIR}/treeland-dde-shell-v1-protocol.c
)

add_custom_command(
    OUTPUT ${XDG_SHELL_HEADER}
    COMMAND ${WAYLAND_SCANNER_EXECUTABLE} client-header ${XDG_SHELL_XML} ${XDG_SHELL_HEADER}
    DEPENDS ${XDG_SHELL_XML}
    VERBATIM
)

add_custom_command(
    OUTPUT ${XDG_SHELL_CODE}
    COMMAND ${WAYLAND_SCANNER_EXECUTABLE} private-code ${XDG_SHELL_XML} ${XDG_SHELL_CODE}
    DEPENDS ${XDG_SHELL_XML}
    VERBATIM
)

add_custom_command(
    OUTPUT ${DDE_SHELL_HEADER}
    COMMAND ${WAYLAND_SCANNER_EXECUTABLE} client-header ${DDE_SHELL_XML} ${DDE_SHELL_HEADER}
    DEPENDS ${DDE_SHELL_XML}
    VERBATIM
)

add_custom_command(
    OUTPUT ${DDE_SHELL_CODE}
    COMMAND ${WAYLAND_SCANNER_EXECUTABLE} private-code ${DDE_SHELL_XML} ${DDE_SHELL_CODE}
    DEPENDS ${DDE_SHELL_XML}
    VERBATIM
)

add_executable(test_late_dde_listener
    main.cpp
    lateclient.cpp
    lateclient.h
    ${XDG_SHELL_HEADER}
    ${XDG_SHELL_CODE}
    ${DDE_SHELL_HEADER}
    ${DDE_SHELL_CODE}
)

target_include_directories(test_late_dde_listener
    PRIVATE
        ${CMAKE_SOURCE_DIR}/compositor/src
        ${CMAKE_CURRENT_BINARY_DIR}
)

target_link_libraries(test_late_dde_listener
    PRIVATE
        libdeckcompositor
        Qt::Gui
        Qt::Test
        PkgConfig::WAYLAND_CLIENT
        WaylibShared::SharedServer
)

add_test(NAME test_late_dde_listener COMMAND test_late_dde_listener)
set_tests_properties(test_late_dde_listener PROPERTIES TIMEOUT 60)
