# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

find_package(Qt6 REQUIRED COMPONENTS Gui Test)
find_package(PkgConfig REQUIRED)
pkg_search_module(WAYLAND_CLIENT REQUIRED IMPORTED_TARGET wayland-client)

add_executable(test_multi_seat
    devicepathfixture.cpp
    devicepathfixture.h
    main.cpp
    surfaceclient.cpp
    surfaceclient.h
)

target_compile_definitions(test_multi_seat PRIVATE WLR_USE_UNSTABLE)
set_target_properties(test_multi_seat PROPERTIES ENABLE_EXPORTS ON)

target_include_directories(test_multi_seat
    PRIVATE
        ${CMAKE_SOURCE_DIR}/compositor/src
)

target_link_libraries(test_multi_seat
    PRIVATE
        libdeckcompositor
        Qt::Gui
        Qt::Test
        WaylibShared::SharedServer
        PkgConfig::WAYLAND_CLIENT
        WaylibShared::waylib-wlroots
        ${CMAKE_DL_LIBS}
)

add_test(NAME test_multi_seat COMMAND test_multi_seat)
set_tests_properties(test_multi_seat PROPERTIES TIMEOUT 15)
