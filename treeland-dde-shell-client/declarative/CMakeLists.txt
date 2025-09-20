# QML 插件模块
# URI: DeckShell.ddeshellclient
# 安装路径: DeckShell/ddeshellclient/
qt_add_qml_module(DShellClientQmlPlugin
    URI "DeckShell.ddeshellclient"
    VERSION 1.0
    PLUGIN_TARGET DShellClientQmlPlugin
    OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/DeckShell/ddeshellclient"
    SOURCES
        types.h
        types.cpp
)

# 链接到共享库（不再直接编译 window.cpp）
target_link_libraries(DShellClientQmlPlugin
    PRIVATE
        ddeshellclient          # 链接到共享库
        Qt::Core
        Qt::Gui
        Qt::Qml
        Qt::Quick
        Qt::WaylandClient
        Qt::WaylandClientPrivate
)

# 包含目录（从共享库获取）
target_include_directories(DShellClientQmlPlugin
    PRIVATE
        ${PROJECT_SOURCE_DIR}/src  # 访问 window.h
        ${PROJECT_BINARY_DIR}/src  # 访问生成的 Wayland 协议头文件
)

# 安装插件到 QML 模块路径
# 路径：${CMAKE_INSTALL_QMLDIR}/DeckShell/ddeshellclient/
install(TARGETS DShellClientQmlPlugin
    LIBRARY DESTINATION ${CMAKE_INSTALL_QMLDIR}/DeckShell/ddeshellclient
)

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/DeckShell/ddeshellclient/qmldir
    DESTINATION ${CMAKE_INSTALL_QMLDIR}/DeckShell/ddeshellclient
)
