find_package(Qt6 REQUIRED COMPONENTS Test)
find_package(PkgConfig REQUIRED)
pkg_search_module(WAYLAND_CLIENT REQUIRED IMPORTED_TARGET wayland-client)

add_executable(test_manager_resource_lifecycle main.cpp)

target_include_directories(test_manager_resource_lifecycle
    PRIVATE
        ${CMAKE_SOURCE_DIR}/compositor/src
)

target_link_libraries(test_manager_resource_lifecycle
    PRIVATE
        libdeckcompositor
        Qt::Test
        PkgConfig::WAYLAND_CLIENT
        WaylibShared::SharedServer
)

add_test(NAME test_manager_resource_lifecycle COMMAND test_manager_resource_lifecycle)

set_property(TEST test_manager_resource_lifecycle PROPERTY
    ENVIRONMENT "QT_QPA_PLATFORM=offscreen"
)

set_property(TEST test_manager_resource_lifecycle PROPERTY TIMEOUT 10)
