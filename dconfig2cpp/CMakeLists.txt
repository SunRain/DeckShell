project(dconfig2cpp CXX)

if(PROJECT_IS_TOP_LEVEL)
    cmake_minimum_required(VERSION 3.16)
    set(CMAKE_CXX_STANDARD 20)
    find_package(Qt6 CONFIG REQUIRED Core)
endif()

include(MacroAddFileDependencies)
include(CMakeParseArguments)

set(TARGET_NAME dconfig2cpp)

# Define the helper function
# Define the function before building targets so it can be used during configuration
function(dtk_add_config_to_cpp OUTPUT_VAR JSON_FILE)
    if(NOT EXISTS ${JSON_FILE})
        message(FATAL_ERROR "JSON file ${JSON_FILE} does not exist.")
    endif()

    cmake_parse_arguments("arg" "" "OUTPUT_FILE_NAME;CLASS_NAME" "" ${ARGN})

    # Generate the output header file name
    get_filename_component(FILE_NAME_WLE ${JSON_FILE} NAME_WLE)
    if(DEFINED arg_OUTPUT_FILE_NAME)
        set(OUTPUT_HEADER "${CMAKE_CURRENT_BINARY_DIR}/${arg_OUTPUT_FILE_NAME}")
    else()
        set(OUTPUT_HEADER
            "${CMAKE_CURRENT_BINARY_DIR}/dconfig_${FILE_NAME_WLE}.hpp")
    endif()

    # Check if CLASS_NAME is set
    if(DEFINED arg_CLASS_NAME)
        set(CLASS_NAME_ARG -c ${arg_CLASS_NAME})
    else()
        set(CLASS_NAME_ARG "")
    endif()

    # Add a custom command to run dconfig2cpp
    add_custom_command(
        OUTPUT ${OUTPUT_HEADER}
        COMMAND ${TARGET_NAME} -o ${OUTPUT_HEADER} ${CLASS_NAME_ARG}
        ${JSON_FILE}
        DEPENDS ${JSON_FILE} ${DTK_XML2CPP}
        COMMENT "Generating ${OUTPUT_HEADER} from ${JSON_FILE}"
        VERBATIM)

    # Add the generated header to the specified output variable
    set(${OUTPUT_VAR}
        ${${OUTPUT_VAR}} ${OUTPUT_HEADER}
        PARENT_SCOPE)
endfunction()

# Now define the build targets after the function

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
find_package(Qt6 CONFIG REQUIRED COMPONENTS Core)

add_executable(${TARGET_NAME} main.cpp)

target_link_libraries(${TARGET_NAME} PRIVATE Qt6::Core)

# set_target_properties(${TARGET_NAME} PROPERTIES OUTPUT_NAME ${TARGET_NAME}
#     EXPORT_NAME DConfig2Cpp)

# install(
#     TARGETS ${TARGET_NAME}
#     EXPORT Dtk${DTK_VERSION_MAJOR}ToolsTargets
#     DESTINATION ${TOOL_INSTALL_DIR})

