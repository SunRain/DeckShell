# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

find_package(Qt6 REQUIRED COMPONENTS Gui GuiPrivate)

add_executable(test_qpa_lifecycle_probe probe.cpp)

target_link_libraries(test_qpa_lifecycle_probe
    PRIVATE
        Qt::Gui
        Qt::GuiPrivate
        WaylibShared::SharedServer
)

add_test(
    NAME test_qpa_lifecycle
    COMMAND ${CMAKE_COMMAND}
        -DDECKCOMPOSITOR_MAIN=${CMAKE_SOURCE_DIR}/compositor/src/main.cpp
        -DQPA_PROBE_EXECUTABLE=$<TARGET_FILE:test_qpa_lifecycle_probe>
        -P ${CMAKE_CURRENT_SOURCE_DIR}/run.cmake
)

set_tests_properties(test_qpa_lifecycle PROPERTIES TIMEOUT 20)
