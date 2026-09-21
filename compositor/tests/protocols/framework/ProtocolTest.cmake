include_guard(GLOBAL)

set(TREELAND_PROTOCOL_TEST_FRAMEWORK_DIR "${CMAKE_CURRENT_LIST_DIR}")

pkg_get_variable(WAYLAND_PROTOCOLS_DATADIR wayland-protocols pkgdatadir)
set(TREELAND_PROTOCOL_TEST_FRAMEWORK_BINARY_DIR
    "${CMAKE_CURRENT_BINARY_DIR}/framework")
file(MAKE_DIRECTORY "${TREELAND_PROTOCOL_TEST_FRAMEWORK_BINARY_DIR}")
set(xdg_shell_xml "${WAYLAND_PROTOCOLS_DATADIR}/stable/xdg-shell/xdg-shell.xml")
set(xdg_shell_header
    "${TREELAND_PROTOCOL_TEST_FRAMEWORK_BINARY_DIR}/xdg-shell-client-protocol.h")
set(xdg_shell_code
    "${TREELAND_PROTOCOL_TEST_FRAMEWORK_BINARY_DIR}/xdg-shell-client-protocol.c")
add_custom_command(
    OUTPUT "${xdg_shell_header}"
    COMMAND wayland-scanner client-header "${xdg_shell_xml}" "${xdg_shell_header}"
    DEPENDS "${xdg_shell_xml}"
    VERBATIM
)
add_custom_command(
    OUTPUT "${xdg_shell_code}"
    COMMAND wayland-scanner private-code "${xdg_shell_xml}" "${xdg_shell_code}"
    DEPENDS "${xdg_shell_xml}" "${xdg_shell_header}"
    VERBATIM
)

add_library(treeland_protocol_test_framework STATIC
    "${TREELAND_PROTOCOL_TEST_FRAMEWORK_DIR}/protocol-test-entry.cpp"
    "${TREELAND_PROTOCOL_TEST_FRAMEWORK_DIR}/test-accounts-service.cpp"
    "${TREELAND_PROTOCOL_TEST_FRAMEWORK_DIR}/test-accounts-service.h"
    "${TREELAND_PROTOCOL_TEST_FRAMEWORK_DIR}/client-connection.c"
    "${TREELAND_PROTOCOL_TEST_FRAMEWORK_DIR}/test-dconfig-service.cpp"
    "${TREELAND_PROTOCOL_TEST_FRAMEWORK_DIR}/test-dconfig-service.h"
    "${TREELAND_PROTOCOL_TEST_FRAMEWORK_DIR}/server-bridge.cpp"
    "${TREELAND_PROTOCOL_TEST_FRAMEWORK_DIR}/server-bridge-api.h"
    "${TREELAND_PROTOCOL_TEST_FRAMEWORK_DIR}/xdg-toplevel-client.c"
    "${TREELAND_PROTOCOL_TEST_FRAMEWORK_DIR}/xdg-toplevel-client.h"
    "${xdg_shell_header}"
    "${xdg_shell_code}"
)
target_include_directories(treeland_protocol_test_framework
    PUBLIC
        "${TREELAND_PROTOCOL_TEST_FRAMEWORK_DIR}"
        "${TREELAND_PROTOCOL_TEST_FRAMEWORK_BINARY_DIR}"
    PRIVATE
        "${CMAKE_SOURCE_DIR}/compositor/src"
)
target_link_libraries(treeland_protocol_test_framework
    PUBLIC
        libdeckcompositor
        WaylibShared::SharedServer
        PkgConfig::WAYLAND_CLIENT
        Qt6::Core
        Qt6::DBus
        Qt6::Gui
        Qt6::Test
)
set_target_properties(treeland_protocol_test_framework PROPERTIES C_STANDARD 11)

# 生成测试客户端的协议代码，并通过输出变量返回参与构建的文件。
function(_treeland_protocol_test_client xml output_sources)
    get_filename_component(protocol_basename "${xml}" NAME_WE)
    set(protocol_header "${CMAKE_CURRENT_BINARY_DIR}/${protocol_basename}-client-protocol.h")
    set(protocol_code "${CMAKE_CURRENT_BINARY_DIR}/${protocol_basename}-client-protocol.c")
    add_custom_command(
        OUTPUT "${protocol_header}"
        COMMAND wayland-scanner client-header "${xml}" "${protocol_header}"
        DEPENDS "${xml}"
        VERBATIM
    )
    add_custom_command(
        OUTPUT "${protocol_code}"
        COMMAND wayland-scanner private-code "${xml}" "${protocol_code}"
        DEPENDS "${xml}" "${protocol_header}"
        VERBATIM
    )
    set(${output_sources} "${protocol_header}" "${protocol_code}" PARENT_SCOPE)
endfunction()

# 注册协议测试，复用公共 Waylib target 的头文件及链接要求。
function(treeland_add_protocol_test)
    set(oneValueArgs NAME XML SETUP CLIENT)
    set(multiValueArgs EXTRA_XMLS EXTRA_LIBRARIES)
    cmake_parse_arguments(ARGS "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})
    foreach(required NAME SETUP CLIENT)
        if(NOT ARGS_${required})
            message(FATAL_ERROR "treeland_add_protocol_test requires ${required}")
        endif()
    endforeach()

    string(REPLACE "-" "_" target_suffix "${ARGS_NAME}")
    set(target "test_${target_suffix}")
    set(protocol_client_sources)
    foreach(xml IN LISTS ARGS_XML ARGS_EXTRA_XMLS)
        _treeland_protocol_test_client("${xml}" generated_sources)
        list(APPEND protocol_client_sources ${generated_sources})
    endforeach()
    add_executable(${target}
        "${ARGS_SETUP}"
        "${ARGS_CLIENT}"
        ${protocol_client_sources}
    )
    target_include_directories(${target} PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}"
        "${CMAKE_CURRENT_BINARY_DIR}"
        "${TREELAND_PROTOCOL_TEST_FRAMEWORK_DIR}"
        "${CMAKE_SOURCE_DIR}/compositor/src"
    )
    target_link_libraries(${target} PRIVATE
        "$<LINK_LIBRARY:WHOLE_ARCHIVE,treeland_protocol_test_framework>"
        ${ARGS_EXTRA_LIBRARIES}
    )
    # Q_OBJECT users live in treeland_protocol_test_framework.  Per-protocol
    # fixtures and C clients do not need an autogen pass of their own.
    set_target_properties(${target} PROPERTIES
        AUTOMOC OFF
        AUTOUIC OFF
        AUTORCC OFF
        C_STANDARD 11
    )
    add_dependencies(${target} multitaskview)
    if(NOT DISABLE_DDM)
        add_dependencies(${target} lockscreen)
    endif()
    add_test(NAME ${target} COMMAND ${target})
    set_tests_properties(${target} PROPERTIES
        ENVIRONMENT "WLR_BACKENDS=headless;WLR_RENDERER=pixman;DSG_DATA_DIRS=${TREELAND_PROTOCOL_TEST_DSG_DATA_DIRS};TREELAND_PROTOCOL_TEST_DSG_DIR=${TREELAND_PROTOCOL_TEST_DSG_DATA_DIR}"
        LABELS "protocols"
        SKIP_REGULAR_EXPRESSION "SKIP   :"
        SKIP_RETURN_CODE 77
        TIMEOUT 30
    )
endfunction()
