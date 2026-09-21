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

set(DECKSHELL_TEST_WAYLIB_PREFIX "" CACHE PATH
    "Installed WaylibShared runtime used by the embedded-development install smoke test")

# 仅从显式安装包读取 runtime 目录，不替换内嵌模式已经存在的公开 target。
function(_deckshell_test_installed_waylib_runtime)
    set(WaylibShared_DIR "WaylibShared_DIR-NOTFOUND")
    find_package(WaylibShared CONFIG REQUIRED COMPONENTS SharedServer
        PATHS "${DECKSHELL_TEST_WAYLIB_PREFIX}" NO_DEFAULT_PATH)
    set(_deckshell_test_waylib_qml_dir "${WaylibShared_QML_IMPORT_DIR}" PARENT_SCOPE)
    set(_deckshell_test_waylib_libdir "${WaylibShared_LIBDIR}" PARENT_SCOPE)
endfunction()

set(_deckshell_test_waylib_qml_dir "${WaylibShared_QML_IMPORT_DIR}")
set(_deckshell_test_waylib_libdir "${WaylibShared_LIBDIR}")
if(WITH_SUBMODULE_WAYLIB)
    set(_deckshell_test_waylib_qml_dir "")
    set(_deckshell_test_waylib_libdir "")
    if(DECKSHELL_TEST_WAYLIB_PREFIX)
        _deckshell_test_installed_waylib_runtime()
    endif()
endif()

execute_process(
    COMMAND "${CMAKE_COMMAND}" -E env QT_QPA_PLATFORM=offscreen
        "${QML6_EXECUTABLE}" --version
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
        DECKSHELL_SOURCE_DIRECTORY="${CMAKE_SOURCE_DIR}"
        DECKSHELL_QML_INSTALL_DIRECTORY="${DECKSHELL_QML_INSTALL_DIR}"
        DECKSHELL_LIBRARY_INSTALL_DIRECTORY="${CMAKE_INSTALL_LIBDIR}"
        DECKSHELL_QML_PLUGIN_FILENAME="$<TARGET_FILE_NAME:libdeckcompositorplugin>"
        WAYLIB_RUNTIME_QML_IMPORT_DIRECTORY="${_deckshell_test_waylib_qml_dir}"
        WAYLIB_RUNTIME_LIBRARY_DIRECTORY="${_deckshell_test_waylib_libdir}"
        WAYLIB_RUNTIME_LIBRARY_FILENAME="$<TARGET_SONAME_FILE_NAME:WaylibShared::SharedServer>"
        WAYLIB_NATIVE_LIBRARY_FILENAME="$<TARGET_SONAME_FILE_NAME:WaylibShared::waylib-wlroots>"
        EMBEDDED_WAYLIB_BUILD=$<BOOL:${WITH_SUBMODULE_WAYLIB}>
        QML_EXECUTABLE_PATH="${QML6_EXECUTABLE}"
        READELF_EXECUTABLE_PATH="${READELF_EXECUTABLE}"
)

target_link_libraries(test_qml_install_smoke
    PRIVATE
        Qt::Core
        Qt::Test
)
add_dependencies(test_qml_install_smoke libdeckcompositorplugin capture)

add_test(NAME test_qml_install_smoke COMMAND test_qml_install_smoke)
set_tests_properties(test_qml_install_smoke PROPERTIES TIMEOUT 60)
