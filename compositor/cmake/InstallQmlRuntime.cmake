# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

set(_deckshell_qml_module_dir "${DECKSHELL_QML_INSTALL_DIR}/DeckShell/Compositor")
get_filename_component(_deckshell_qml_module_full_dir "${_deckshell_qml_module_dir}"
    ABSOLUTE BASE_DIR "${CMAKE_INSTALL_PREFIX}")
file(RELATIVE_PATH _deckshell_qml_to_lib
    "${_deckshell_qml_module_full_dir}" "${CMAKE_INSTALL_FULL_LIBDIR}")
file(RELATIVE_PATH _deckshell_bin_to_lib
    "${CMAKE_INSTALL_FULL_BINDIR}" "${CMAKE_INSTALL_FULL_LIBDIR}")

# 自有库从同级目录发现彼此；外部包的固定安装目录由真实链接依赖传播。
set_target_properties(libdeckcompositor capture PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    INSTALL_RPATH_USE_LINK_PATH TRUE
)
set_target_properties(libdeckcompositorplugin PROPERTIES
    INSTALL_RPATH "$ORIGIN/${_deckshell_qml_to_lib}"
    INSTALL_RPATH_USE_LINK_PATH TRUE
)
set_target_properties(${BIN_NAME} PROPERTIES
    INSTALL_RPATH "$ORIGIN/${_deckshell_bin_to_lib}"
    INSTALL_RPATH_USE_LINK_PATH TRUE
)

install(DIRECTORY "${PROJECT_BINARY_DIR}/qt/qml/DeckShell/Compositor/"
    DESTINATION "${_deckshell_qml_module_dir}"
    COMPONENT DeckShellQmlRuntime
    FILES_MATCHING
        PATTERN "*.qml"
        PATTERN "*.qmltypes"
        PATTERN "qmldir"
)
install(TARGETS libdeckcompositorplugin
    LIBRARY DESTINATION "${_deckshell_qml_module_dir}"
    COMPONENT DeckShellQmlRuntime
)
install(TARGETS libdeckcompositor
    LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    NAMELINK_SKIP
    COMPONENT DeckShellQmlRuntime
)
if(TREELAND_INSTALL_DEV)
    install(TARGETS libdeckcompositor
        LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
        NAMELINK_ONLY
    )
endif()

unset(_deckshell_qml_module_dir)
unset(_deckshell_qml_module_full_dir)
unset(_deckshell_qml_to_lib)
unset(_deckshell_bin_to_lib)
