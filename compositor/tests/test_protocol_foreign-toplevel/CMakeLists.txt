# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

find_package(Qt6 REQUIRED COMPONENTS DBus Gui Test)
find_package(PkgConfig REQUIRED)
pkg_search_module(WAYLAND_CLIENT REQUIRED IMPORTED_TARGET wayland-client)

add_executable(test_protocol_foreign-toplevel
    main.cpp
    ../protocols/framework/test-dconfig-service.cpp
    ../protocols/framework/test-accounts-service.cpp
)

target_compile_definitions(test_protocol_foreign-toplevel
    PRIVATE
        PROTOCOL_XML="${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-foreign-toplevel-manager-unstable-v3.xml"
)

target_include_directories(test_protocol_foreign-toplevel
    PRIVATE
        ${CMAKE_SOURCE_DIR}/compositor/src
        ${CMAKE_CURRENT_SOURCE_DIR}/../protocols/framework
)

target_link_libraries(test_protocol_foreign-toplevel
    PRIVATE
        libdeckcompositor
        Qt::DBus
        Qt::Gui
        Qt::Test
        PkgConfig::WAYLAND_CLIENT
)

add_test(NAME test_protocol_foreign-toplevel COMMAND test_protocol_foreign-toplevel)
set_tests_properties(test_protocol_foreign-toplevel PROPERTIES
    TIMEOUT 30
    ENVIRONMENT "WLR_BACKENDS=headless;WLR_RENDERER=pixman;DSG_DATA_DIRS=${CMAKE_BINARY_DIR}/compositor/tests/protocols/dsg:/usr/share/dsg;TREELAND_PROTOCOL_TEST_DSG_DIR=${CMAKE_BINARY_DIR}/compositor/tests/protocols/dsg"
)
if(NOT DISABLE_XWAYLAND)
    set_property(TEST test_protocol_foreign-toplevel APPEND PROPERTY ENVIRONMENT
        "WLR_XWAYLAND=$<TARGET_FILE:treeland-xwayland>")
    add_dependencies(test_protocol_foreign-toplevel treeland-xwayland)
endif()
add_dependencies(test_protocol_foreign-toplevel multitaskview)
if(NOT DISABLE_DDM)
    add_dependencies(test_protocol_foreign-toplevel lockscreen)
endif()
