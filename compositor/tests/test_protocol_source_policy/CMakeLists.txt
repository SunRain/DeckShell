# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

add_test(
    NAME test_protocol_source_policy
    COMMAND ${CMAKE_COMMAND}
        -DDECKSHELL_SOURCE_DIR=${CMAKE_SOURCE_DIR}
        -P ${CMAKE_CURRENT_SOURCE_DIR}/source_policy.cmake
)

add_test(
    NAME test_protocol_package_policy
    COMMAND ${CMAKE_COMMAND}
        -DDECKSHELL_SOURCE_DIR=${CMAKE_SOURCE_DIR}
        -P ${CMAKE_CURRENT_SOURCE_DIR}/package_policy.cmake
)

add_test(
    NAME test_protocol_generated_contract
    COMMAND ${CMAKE_COMMAND}
        -DDECKSHELL_SOURCE_DIR=${CMAKE_SOURCE_DIR}
        -DDECKSHELL_BINARY_DIR=${CMAKE_BINARY_DIR}/compositor
        -P ${CMAKE_CURRENT_SOURCE_DIR}/generated_contract.cmake
)

add_test(
    NAME test_build_compatibility_policy
    COMMAND ${CMAKE_COMMAND}
        -DDECKSHELL_SOURCE_DIR=${CMAKE_SOURCE_DIR}
        -P ${CMAKE_CURRENT_SOURCE_DIR}/compatibility_policy.cmake
)

set_tests_properties(
    test_protocol_source_policy
    test_protocol_package_policy
    test_protocol_generated_contract
    test_build_compatibility_policy
    PROPERTIES TIMEOUT 10
)
