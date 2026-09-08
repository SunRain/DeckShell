find_package(Qt6 REQUIRED COMPONENTS Test)

add_executable(test_protocol_show-desktop main.cpp)

target_include_directories(test_protocol_show-desktop
    PRIVATE
        ${CMAKE_SOURCE_DIR}/compositor/src
)

target_link_libraries(test_protocol_show-desktop
    PRIVATE
        libdeckcompositor
        Qt::Test
)

add_test(NAME test_protocol_show-desktop COMMAND test_protocol_show-desktop)

set_property(TEST test_protocol_show-desktop PROPERTY
    ENVIRONMENT "QT_QPA_PLATFORM=offscreen"
)

set_property(TEST test_protocol_show-desktop PROPERTY
    TIMEOUT 3
)
