# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

find_package(Qt6 REQUIRED COMPONENTS Core Network Test)
find_package(DDM 0.2.0 REQUIRED COMPONENTS Common)

add_executable(test_ddm_greeter_lifecycle main.cpp)

target_include_directories(test_ddm_greeter_lifecycle
    PRIVATE
        ${CMAKE_SOURCE_DIR}/compositor/src
)

target_link_libraries(test_ddm_greeter_lifecycle
    PRIVATE
        libdeckcompositor
        DDM::Common
        Qt::Core
        Qt::Network
        Qt::Test
)

add_test(NAME test_ddm_greeter_lifecycle COMMAND test_ddm_greeter_lifecycle)
set_tests_properties(test_ddm_greeter_lifecycle PROPERTIES TIMEOUT 10)
