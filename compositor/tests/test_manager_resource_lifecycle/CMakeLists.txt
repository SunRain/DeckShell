find_package(Qt6 REQUIRED COMPONENTS DBus Gui Test)
find_package(PkgConfig REQUIRED)
pkg_search_module(WAYLAND_CLIENT REQUIRED IMPORTED_TARGET wayland-client)

add_executable(test_manager_resource_lifecycle
    main.cpp
    ../protocols/framework/test-dconfig-service.cpp
    ../protocols/framework/test-accounts-service.cpp
)

target_include_directories(test_manager_resource_lifecycle
    PRIVATE
        ${CMAKE_SOURCE_DIR}/compositor/src
        ${CMAKE_CURRENT_SOURCE_DIR}/../protocols/framework
)

target_link_libraries(test_manager_resource_lifecycle
    PRIVATE
        libdeckcompositor
        Qt::DBus
        Qt::Gui
        Qt::Test
        PkgConfig::WAYLAND_CLIENT
        WaylibShared::SharedServer
)

add_test(NAME test_manager_resource_lifecycle COMMAND test_manager_resource_lifecycle)

set_tests_properties(test_manager_resource_lifecycle PROPERTIES
    TIMEOUT 30
    ENVIRONMENT "WLR_BACKENDS=headless;WLR_RENDERER=pixman;DSG_DATA_DIRS=${CMAKE_BINARY_DIR}/compositor/tests/protocols/dsg:/usr/share/dsg;TREELAND_PROTOCOL_TEST_DSG_DIR=${CMAKE_BINARY_DIR}/compositor/tests/protocols/dsg"
)
if(NOT DISABLE_XWAYLAND)
    set_property(TEST test_manager_resource_lifecycle APPEND PROPERTY ENVIRONMENT
        "WLR_XWAYLAND=$<TARGET_FILE:treeland-xwayland>")
    add_dependencies(test_manager_resource_lifecycle treeland-xwayland)
endif()
add_dependencies(test_manager_resource_lifecycle multitaskview)
if(NOT DISABLE_DDM)
    add_dependencies(test_manager_resource_lifecycle lockscreen)
endif()
