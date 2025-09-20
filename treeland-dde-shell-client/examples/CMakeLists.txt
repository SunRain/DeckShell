qt_add_executable(ddeshellclient-unified
    main.cpp
    launcher.h
    launcher.cpp
    widgetdemo.h
    widgetdemo.cpp
)

# Add QML module for the demo
qt_add_qml_module(ddeshellclient-unified
    URI "ddeshellclient.unified.demo"
    VERSION 1.0
    QML_FILES
        demo.qml
)

target_link_libraries(ddeshellclient-unified
    PRIVATE
        ddeshellclient
        Qt::Core
        Qt::Gui
        Qt::Widgets
        Qt::Quick
        Qt::Qml
        Qt::WaylandClient
        Qt::WaylandClientPrivate
)

# Include directories for accessing header files
target_include_directories(ddeshellclient-unified
    PRIVATE
        ${PROJECT_SOURCE_DIR}/src
        ${PROJECT_BINARY_DIR}/src
)

# Define QML plugin path for runtime
target_compile_definitions(ddeshellclient-unified
    PRIVATE
        QML_PLUGIN_PATH="${PROJECT_BINARY_DIR}/declarative"
)

install(TARGETS ddeshellclient-unified
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
