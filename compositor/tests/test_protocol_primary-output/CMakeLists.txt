find_package(Qt6 REQUIRED COMPONENTS Test)

add_executable(test_protocol_primary-output main.cpp)

target_include_directories(test_protocol_primary-output
    PRIVATE
        ${CMAKE_SOURCE_DIR}/compositor/src
)

target_link_libraries(test_protocol_primary-output
    PRIVATE
        libdeckcompositor
        Qt::Test
        Qt::Gui
        Qt::Qml
        Waylib::SharedServer
)

add_test(NAME test_protocol_primary-output COMMAND test_protocol_primary-output)

set_property(TEST test_protocol_primary-output PROPERTY
    ENVIRONMENT "QT_QPA_PLATFORM=offscreen"
)

set_property(TEST test_protocol_primary-output PROPERTY
    TIMEOUT 3
)
