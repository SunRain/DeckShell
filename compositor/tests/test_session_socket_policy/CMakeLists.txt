# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

add_test(
    NAME test_session_socket_policy
    COMMAND ${CMAKE_COMMAND}
        -DSESSION_SOURCE=${CMAKE_SOURCE_DIR}/compositor/src/session/session.cpp
        -P ${CMAKE_CURRENT_SOURCE_DIR}/run.cmake
)

set_tests_properties(test_session_socket_policy PROPERTIES TIMEOUT 10)
