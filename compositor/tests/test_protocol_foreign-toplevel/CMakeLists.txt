# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

find_package(Qt6 REQUIRED COMPONENTS Core Test)
find_package(PkgConfig REQUIRED)
pkg_search_module(WAYLAND_CLIENT REQUIRED IMPORTED_TARGET wayland-client)

add_executable(test_protocol_foreign-toplevel main.cpp)

target_compile_definitions(test_protocol_foreign-toplevel
    PRIVATE
        PROTOCOL_XML="${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-foreign-toplevel-manager-unstable-v2.xml"
)

target_include_directories(test_protocol_foreign-toplevel
    PRIVATE
        ${CMAKE_SOURCE_DIR}/compositor/src
)

target_link_libraries(test_protocol_foreign-toplevel
    PRIVATE
        libdeckcompositor
        Qt::Core
        Qt::Test
        PkgConfig::WAYLAND_CLIENT
)

add_test(NAME test_protocol_foreign-toplevel COMMAND test_protocol_foreign-toplevel)
set_tests_properties(test_protocol_foreign-toplevel PROPERTIES TIMEOUT 10)
