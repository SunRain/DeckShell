project(qtwaylandscanner_deckshell CXX)

if (PROJECT_IS_TOP_LEVEL)
    cmake_minimum_required(VERSION 3.16)
    set(CMAKE_CXX_STANDARD 20)
    find_package(Qt6 CONFIG REQUIRED Core)
endif()

# Define the function before building targets so it can be used during configuration
function(local_qtwayland_server_protocol_treeland target)
    # Parse arguments
    set(options PRIVATE_CODE)
    set(oneValueArgs PROTOCOL BASENAME PREFIX)
    cmake_parse_arguments(ARGS "${options}" "${oneValueArgs}" "" ${ARGN})

    if(ARGS_UNPARSED_ARGUMENTS)
        message(FATAL_ERROR "Unknown keywords given to local_qtwayland_server_protocol_treeland(): \"${ARGS_UNPARSED_ARGUMENTS}\"")
    endif()

    set(_prefix "${ARGS_PREFIX}")

    find_package(PkgConfig REQUIRED)
    get_filename_component(_infile ${ARGS_PROTOCOL} ABSOLUTE)
    pkg_get_variable(WAYLAND_SCANNER wayland-scanner wayland_scanner)

    if(NOT WAYLAND_SCANNER)
        message(FATAL_ERROR "wayland-scanner not found. Please install wayland development tools.")
    endif()
    set(server_header "${WAYLAND_PROTOCOLS_OUTPUTDIR}/wayland-${ARGS_BASENAME}-server-protocol.h")
    set(server_code "${WAYLAND_PROTOCOLS_OUTPUTDIR}/wayland-${ARGS_BASENAME}-server-protocol.c")
    execute_process(COMMAND ${WAYLAND_SCANNER} "server-header" ${_infile} ${server_header})
    execute_process(COMMAND ${WAYLAND_SCANNER} "private-code" ${_infile} ${server_code})

    set(_header "${WAYLAND_PROTOCOLS_OUTPUTDIR}/qwayland-server-${ARGS_BASENAME}.h")
    set(_code "${WAYLAND_PROTOCOLS_OUTPUTDIR}/qwayland-server-${ARGS_BASENAME}.cpp")

    set_source_files_properties(${_header} ${_code} GENERATED)

    add_custom_command(OUTPUT "${_header}"
        COMMAND qtwaylandscanner_deckshell server-header ${_infile} "" ${_prefix} > ${_header}
        DEPENDS ${_infile} qtwaylandscanner_deckshell VERBATIM)

    add_custom_command(OUTPUT "${_code}"
        COMMAND qtwaylandscanner_deckshell server-code ${_infile} "" ${_prefix} > ${_code}
        DEPENDS ${_infile} ${_header} qtwaylandscanner_deckshell VERBATIM)

    set_property(SOURCE ${_header} ${_code} PROPERTY SKIP_AUTOMOC ON)

    target_sources(${target} PRIVATE "${_code}")
    target_include_directories(${target} PRIVATE "${WAYLAND_PROTOCOLS_OUTPUTDIR}")

    add_custom_target(generate_protocols_${ARGS_BASENAME} ALL
                      DEPENDS ${_header} ${_code}
    )
    add_dependencies(${target} generate_protocols_${ARGS_BASENAME})

endfunction()

# Now define the build targets after the function
if(CMAKE_CROSSCOMPILING AND qtwaylandscanner_deckshell_EXECUTABLE)
    add_executable(qtwaylandscanner_deckshell IMPORTED GLOBAL)
    set_target_properties(qtwaylandscanner_deckshell PROPERTIES IMPORTED_LOCATION ${qtwaylandscanner_deckshell_EXECUTABLE})
elseif(CMAKE_CROSSCOMPILING)
    # search native tooling prefix
    set(NATIVE_PREFIX "" CACHE STRING "CMAKE_PREFIX_PATH for native Qt libraries")
    if (NOT NATIVE_PREFIX)
        # Try to find native Qt installation
        find_program(QMAKE_EXECUTABLE NAMES qmake qmake6 PATHS /usr/bin /usr/local/bin)
        if(QMAKE_EXECUTABLE)
            execute_process(COMMAND ${QMAKE_EXECUTABLE} -query QT_INSTALL_PREFIX
                           OUTPUT_VARIABLE QT_INSTALL_PREFIX
                           OUTPUT_STRIP_TRAILING_WHITESPACE)
            set(NATIVE_PREFIX ${QT_INSTALL_PREFIX})
        endif()
    endif()

    message(STATUS "Building qtwaylandscanner_deckshell against ${NATIVE_PREFIX}")

    include(ExternalProject)
    ExternalProject_Add(native_qtwaylandscanner_deckshell
            SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}
            CMAKE_ARGS -DCMAKE_PREFIX_PATH=${NATIVE_PREFIX}
            -DCMAKE_INSTALL_PREFIX=${CMAKE_CURRENT_BINARY_DIR}
            -DQT_MAJOR_VERSION=6
            INSTALL_COMMAND ""
            BUILD_BYPRODUCTS ${CMAKE_CURRENT_BINARY_DIR}/native_qtwaylandscanner_deckshell-prefix/src/native_qtwaylandscanner_deckshell-build/qtwaylandscanner_deckshell
            )
    add_executable(qtwaylandscanner_deckshell IMPORTED GLOBAL)
    add_dependencies(qtwaylandscanner_deckshell native_qtwaylandscanner_deckshell)
    set_target_properties(qtwaylandscanner_deckshell PROPERTIES IMPORTED_LOCATION
            ${CMAKE_CURRENT_BINARY_DIR}/native_qtwaylandscanner_deckshell-prefix/src/native_qtwaylandscanner_deckshell-build/qtwaylandscanner_deckshell)
else()
    # host build
    remove_definitions(-DQT_NO_CAST_FROM_ASCII)
    add_executable(qtwaylandscanner_deckshell ${CMAKE_CURRENT_SOURCE_DIR}/qtwaylandscanner.cpp)
    target_link_libraries(qtwaylandscanner_deckshell Qt::Core)
endif()
