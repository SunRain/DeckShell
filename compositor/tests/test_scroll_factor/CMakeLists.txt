# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

find_package(Qt6 REQUIRED COMPONENTS Gui Test)
find_package(PkgConfig REQUIRED)
pkg_search_module(WAYLAND_CLIENT REQUIRED IMPORTED_TARGET wayland-client)

add_executable(test_scroll_factor main.cpp)

target_compile_definitions(test_scroll_factor
    PRIVATE
        WLR_USE_UNSTABLE
)

target_include_directories(test_scroll_factor
    PRIVATE
        ${CMAKE_SOURCE_DIR}/compositor/src
)

target_link_libraries(test_scroll_factor
    PRIVATE
        libdeckcompositor
        Qt::Gui
        Qt::Test
        WaylibShared::SharedServer
        PkgConfig::WAYLAND_CLIENT
        WaylibShared::waylib-wlroots
)

add_test(NAME test_scroll_factor COMMAND test_scroll_factor)
set_tests_properties(test_scroll_factor PROPERTIES TIMEOUT 10)
