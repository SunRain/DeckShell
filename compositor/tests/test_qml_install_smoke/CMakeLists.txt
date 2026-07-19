# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

find_package(Qt6 REQUIRED COMPONENTS Core Test)
if(NOT DISABLE_DDM)
    find_package(DDM 0.2.0 REQUIRED COMPONENTS Common)
endif()
find_program(QML6_EXECUTABLE NAMES qml6)
if(NOT QML6_EXECUTABLE)
    find_program(QML6_EXECUTABLE NAMES qml REQUIRED)
endif()
find_program(READELF_EXECUTABLE NAMES readelf REQUIRED)

execute_process(
    COMMAND "${QML6_EXECUTABLE}" --version
    OUTPUT_VARIABLE QML_VERSION_OUTPUT
    ERROR_VARIABLE QML_VERSION_OUTPUT
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
if(NOT QML_VERSION_OUTPUT MATCHES "Qml Runtime 6\\.")
    message(FATAL_ERROR
        "test_qml_install_smoke requires a Qt 6 QML runtime; found '${QML6_EXECUTABLE}': "
        "${QML_VERSION_OUTPUT}"
    )
endif()

add_executable(test_qml_install_smoke
    main.cpp
)

target_compile_definitions(test_qml_install_smoke
    PRIVATE
        CMAKE_EXECUTABLE_PATH="${CMAKE_COMMAND}"
        DECKSHELL_BUILD_DIRECTORY="${CMAKE_BINARY_DIR}"
        QML_EXECUTABLE_PATH="${QML6_EXECUTABLE}"
        READELF_EXECUTABLE_PATH="${READELF_EXECUTABLE}"
)

if(TARGET DDM::Common)
    target_compile_definitions(test_qml_install_smoke
        PRIVATE
            EXTERNAL_RUNTIME_LIBRARY_DIRECTORY="$<TARGET_FILE_DIR:DDM::Common>"
    )
endif()

target_link_libraries(test_qml_install_smoke
    PRIVATE
        Qt::Core
        Qt::Test
)

add_test(NAME test_qml_install_smoke COMMAND test_qml_install_smoke)
set_tests_properties(test_qml_install_smoke PROPERTIES TIMEOUT 60)
