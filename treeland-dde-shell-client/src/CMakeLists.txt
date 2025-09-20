# 创建共享库
qt_add_library(ddeshellclient SHARED
    window.h
    window.cpp
    shellsurface.h
    shellsurface.cpp
    waylandmanager.h
    waylandmanager.cpp
    ddeshellclient_export.h
)

# 生成 Wayland 协议客户端代码
qt_generate_wayland_protocol_client_sources(ddeshellclient
    FILES ${TREELAND_PROTOCOLS_DATA_DIR}/treeland-dde-shell-v1.xml
)

# 显式添加生成的 C 协议文件到库源文件
# qt_generate_wayland_protocol_client_sources 生成两个文件:
# 1. qwayland-treeland-dde-shell-v1.cpp (C++ 包装类)
# 2. wayland-treeland-dde-shell-v1-protocol.c (C 协议定义)
# 需要显式添加 .c 文件以确保协议接口符号被编译进库
set(PROTOCOL_C_FILE "${CMAKE_CURRENT_BINARY_DIR}/wayland-treeland-dde-shell-v1-protocol.c")
set_source_files_properties(${PROTOCOL_C_FILE} PROPERTIES
    GENERATED TRUE
    LANGUAGE C
)
target_sources(ddeshellclient PRIVATE ${PROTOCOL_C_FILE})

# 确保项目启用 C 语言支持
enable_language(C)

# 定义导出宏
target_compile_definitions(ddeshellclient PRIVATE DDESHELLCLIENT_LIBRARY)

# 设置符号可见性
set_target_properties(ddeshellclient PROPERTIES
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN ON
)

# 链接依赖
target_link_libraries(ddeshellclient
    PUBLIC
        Qt::Core
        Qt::Gui
        Qt::Qml
    PRIVATE
        Qt::Widgets
        Qt::WaylandClient
        Qt::WaylandClientPrivate
)

# 包含目录
# 安装后的头文件路径: include/DeckShell/ddeshellclient/window.h
target_include_directories(ddeshellclient
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include/DeckShell/ddeshellclient>
    PRIVATE
        ${CMAKE_CURRENT_BINARY_DIR}  # 生成的 Wayland 头文件
)

# 安装规则
install(TARGETS ddeshellclient
    EXPORT DDEShellClientTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

# 安装头文件到 include/DeckShell/ddeshellclient/
install(FILES
    window.h
    shellsurface.h
    waylandmanager.h
    ddeshellclient_export.h
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/DeckShell/ddeshellclient
)
