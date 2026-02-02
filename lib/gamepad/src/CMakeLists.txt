# DeckShell Gamepad Core Library
# Qt-only library for Linux evdev gamepad support (optional Treeland Wayland client as upper layer)

cmake_minimum_required(VERSION 3.16)

find_package(Qt6 6.8 REQUIRED COMPONENTS Core)
find_package(Qt6 6.8 COMPONENTS DBus QUIET)
find_package(PkgConfig REQUIRED)
pkg_check_modules(UDEV REQUIRED IMPORTED_TARGET libudev)

set(CMAKE_AUTOMOC ON)

option(DECKGAMEPAD_BUILD_TREELAND_CLIENT "Build Treeland Wayland client library (optional)" OFF)

option(DECKGAMEPAD_BUILD_QML_MODULE
    "Build DeckShell.DeckGamepad QML module (optional)"
    OFF
)

# 默认 evdev 运行模式（用于 DeckGamepadService::DeckGamepadService 默认构造路径）
# - evdev-udev: 单线程调试模式（legacy 行为对照/回归排查）
# - evdev: IO 线程模式（推荐）
set(DECKGAMEPAD_DEFAULT_PROVIDER "evdev"
    CACHE STRING "Default evdev mode for DeckGamepadService (evdev-udev|evdev)"
)
set_property(CACHE DECKGAMEPAD_DEFAULT_PROVIDER PROPERTY STRINGS "evdev-udev" "evdev")

include(GNUInstallDirs)
if(NOT DEFINED CMAKE_INSTALL_QMLDIR)
    set(CMAKE_INSTALL_QMLDIR "${CMAKE_INSTALL_LIBDIR}/qt6/qml" CACHE PATH "Qt QML install directory")
endif()

set(CORE_SOURCES
    core/deckgamepaderror.h
    core/deckgamepaddiagnostic.h
    core/deckgamepadaction.h
    core/deckgamepaddeviceinfo.h
    core/deckgamepadruntimeconfig.h
    service/ideckgamepadprovider.h
    service/deckgamepadservice.h
    service/deckgamepadservice.cpp
    providers/evdev/evdevprovider.h
    providers/evdev/evdevprovider.cpp
    core/deckgamepad.h
    core/deckgamepad.cpp
    backend/deckgamepadbackend.h
    backend/deckgamepadbackend.cpp
    backend/deviceaccessbroker.h
    backend/deviceaccessbroker.cpp
    backend/sessiongate.h
    backend/sessiongate.cpp
    backend/deviceuidgenerator.h
    backend/deviceuidgenerator.cpp
    mapping/deckgamepadmapping.h
    mapping/deckgamepadsdlcontrollerdb.h
    mapping/deckgamepadsdlcontrollerdb.cpp
    mapping/deckgamepadsdlcontrollerdb_p.h
    mapping/deckgamepadcustommappingmanager.h
    mapping/deckgamepadcustommappingmanager.cpp
    mapping/deckgamepadcalibrationstore.h
    mapping/deckgamepadcalibrationstore.cpp
    extras/actionmappingprofile.h
    extras/actionmappingprofile.cpp
    extras/deckgamepadkeyboardmapping.h
    extras/deckgamepadkeyboardmapping.cpp
    extras/deckgamepadactionmapper.h
    extras/deckgamepadactionmapper.cpp
    extras/deckgamepadactionkeymapping.h
    extras/deckgamepadactionkeymapping.cpp
    extras/keyboardmappingprofile.h
    extras/keyboardmappingprofile.cpp
    extras/steaminputdetector.h
    extras/steaminputdetector.cpp
)

add_library(deckshell-gamepad ${CORE_SOURCES})

target_link_libraries(deckshell-gamepad
    PUBLIC
        Qt6::Core
        PkgConfig::UDEV
)

set(_deckgamepad_default_provider_evdev 0)
if(DECKGAMEPAD_DEFAULT_PROVIDER STREQUAL "evdev")
    set(_deckgamepad_default_provider_evdev 1)
elseif(DECKGAMEPAD_DEFAULT_PROVIDER STREQUAL "evdev-udev")
    set(_deckgamepad_default_provider_evdev 0)
else()
    message(FATAL_ERROR "Invalid DECKGAMEPAD_DEFAULT_PROVIDER=${DECKGAMEPAD_DEFAULT_PROVIDER} (expected evdev-udev or evdev)")
endif()
target_compile_definitions(deckshell-gamepad PUBLIC DECKGAMEPAD_DEFAULT_PROVIDER_EVDEV=${_deckgamepad_default_provider_evdev})
unset(_deckgamepad_default_provider_evdev)

set(_deckgamepad_enable_logind 0)
if(TARGET Qt6::DBus)
    set(_deckgamepad_enable_logind 1)
    target_link_libraries(deckshell-gamepad PUBLIC Qt6::DBus)
endif()
set(DECKSHELL_GAMEPAD_ENABLE_LOGIND ${_deckgamepad_enable_logind})
target_compile_definitions(deckshell-gamepad PUBLIC DECKGAMEPAD_ENABLE_LOGIND=${_deckgamepad_enable_logind})
unset(_deckgamepad_enable_logind)

target_compile_definitions(deckshell-gamepad
    PRIVATE
        $<$<BOOL:${BUILD_SHARED_LIBS}>:DECKGAMEPAD_EXPORT=Q_DECL_EXPORT>
        $<$<NOT:$<BOOL:${BUILD_SHARED_LIBS}>>:DECKGAMEPAD_EXPORT=>
)

set_target_properties(deckshell-gamepad PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION 1
    OUTPUT_NAME "deckshell-gamepad"
    POSITION_INDEPENDENT_CODE ON
)

set(DECKGAMEPAD_BUILD_INCLUDE_DIR "${CMAKE_CURRENT_BINARY_DIR}/include")
set(DECKGAMEPAD_BUILD_INCLUDE_ROOT "${DECKGAMEPAD_BUILD_INCLUDE_DIR}/deckshell/deckgamepad")

file(MAKE_DIRECTORY "${DECKGAMEPAD_BUILD_INCLUDE_ROOT}")

set(DECKGAMEPAD_PUBLIC_DOMAINS
    core
    service
    backend
    mapping
    extras
    providers
    treeland
)

foreach(domain IN LISTS DECKGAMEPAD_PUBLIC_DOMAINS)
    set(src "${CMAKE_CURRENT_SOURCE_DIR}/${domain}")
    set(dst "${DECKGAMEPAD_BUILD_INCLUDE_ROOT}/${domain}")

    if(NOT EXISTS "${dst}")
        file(CREATE_LINK "${src}" "${dst}" SYMBOLIC)
    endif()
endforeach()

target_include_directories(deckshell-gamepad
    PUBLIC
        $<BUILD_INTERFACE:${DECKGAMEPAD_BUILD_INCLUDE_DIR}>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

target_compile_features(deckshell-gamepad PUBLIC cxx_std_17)

install(DIRECTORY
    core
    service
    backend
    mapping
    extras
    providers
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/deckshell/deckgamepad
    FILES_MATCHING PATTERN "*.h" PATTERN "*_p.h" EXCLUDE
)

install(TARGETS deckshell-gamepad
    EXPORT DeckShellGamepadTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

install(EXPORT DeckShellGamepadTargets
    FILE DeckShellGamepadTargets.cmake
    NAMESPACE DeckShell::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/DeckShellGamepad
)

include(CMakePackageConfigHelpers)

set(DECKSHELL_GAMEPAD_CMAKE_INSTALL_DIR "${CMAKE_INSTALL_LIBDIR}/cmake/DeckShellGamepad")

configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/DeckShellGamepadConfig.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/DeckShellGamepadConfig.cmake"
    INSTALL_DESTINATION "${DECKSHELL_GAMEPAD_CMAKE_INSTALL_DIR}"
)

write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/DeckShellGamepadConfigVersion.cmake"
    VERSION "${PROJECT_VERSION}"
    COMPATIBILITY SameMajorVersion
)

install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/DeckShellGamepadConfig.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/DeckShellGamepadConfigVersion.cmake"
    DESTINATION "${DECKSHELL_GAMEPAD_CMAKE_INSTALL_DIR}"
)

install(FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/../data/gamecontrollerdb.txt
    DESTINATION ${CMAKE_INSTALL_DATADIR}/DeckShellGamepad
)

if(DECKGAMEPAD_BUILD_TREELAND_CLIENT)
    pkg_check_modules(WAYLAND_CLIENT REQUIRED IMPORTED_TARGET wayland-client)

    pkg_get_variable(WAYLAND_SCANNER wayland-scanner wayland_scanner)
    if(NOT WAYLAND_SCANNER)
        message(FATAL_ERROR "wayland-scanner not found")
    endif()

    set(TREELAND_GAMEPAD_PROTOCOL_XML "${CMAKE_CURRENT_SOURCE_DIR}/../protocols/treeland-gamepad-v1.xml"
        CACHE FILEPATH "Path to treeland-gamepad-v1.xml (Treeland client only)")

    if(NOT EXISTS "${TREELAND_GAMEPAD_PROTOCOL_XML}" AND DEFINED TREELAND_PROTOCOLS_DATA_DIR)
        if(EXISTS "${TREELAND_PROTOCOLS_DATA_DIR}/treeland-gamepad-v1.xml")
            set(TREELAND_GAMEPAD_PROTOCOL_XML "${TREELAND_PROTOCOLS_DATA_DIR}/treeland-gamepad-v1.xml")
        endif()
    endif()

    if(NOT EXISTS "${TREELAND_GAMEPAD_PROTOCOL_XML}")
        message(FATAL_ERROR "TREELAND_GAMEPAD_PROTOCOL_XML not found. Set -DTREELAND_GAMEPAD_PROTOCOL_XML=/path/to/treeland-gamepad-v1.xml (or ensure vendored protocols/treeland-gamepad-v1.xml exists) to build Treeland client.")
    endif()

    set(PROTOCOL_HEADER "${CMAKE_CURRENT_BINARY_DIR}/treeland-gamepad-v1-client-protocol.h")
    set(PROTOCOL_SOURCE "${CMAKE_CURRENT_BINARY_DIR}/treeland-gamepad-v1-client-protocol.c")

    add_custom_command(
        OUTPUT ${PROTOCOL_HEADER}
        COMMAND ${WAYLAND_SCANNER} client-header ${TREELAND_GAMEPAD_PROTOCOL_XML} ${PROTOCOL_HEADER}
        DEPENDS ${TREELAND_GAMEPAD_PROTOCOL_XML}
        COMMENT "Generating Treeland gamepad protocol header"
    )

    add_custom_command(
        OUTPUT ${PROTOCOL_SOURCE}
        COMMAND ${WAYLAND_SCANNER} private-code ${TREELAND_GAMEPAD_PROTOCOL_XML} ${PROTOCOL_SOURCE}
        DEPENDS ${TREELAND_GAMEPAD_PROTOCOL_XML}
        COMMENT "Generating Treeland gamepad protocol source"
    )

    set(TREELAND_SOURCES
        treeland/treelandgamepadglobal.h
        treeland/treelandgamepadclient.h
        treeland/treelandgamepadclient.cpp
        treeland/treelandgamepaddevice.h
        treeland/treelandgamepaddevice.cpp
        treeland/treelandgamepadmanager.h
        treeland/treelandgamepadmanager.cpp
        treeland/treelandprovider.h
        treeland/treelandprovider.cpp
        ${PROTOCOL_HEADER}
        ${PROTOCOL_SOURCE}
    )

    add_library(deckshell-gamepad-treeland ${TREELAND_SOURCES})

    target_include_directories(deckshell-gamepad-treeland
        PRIVATE
            ${CMAKE_CURRENT_BINARY_DIR}
    )

    target_link_libraries(deckshell-gamepad-treeland
        PUBLIC
            Qt6::Core
            deckshell-gamepad
            PkgConfig::WAYLAND_CLIENT
    )

    target_compile_definitions(deckshell-gamepad-treeland
        PRIVATE
            TREELAND_GAMEPAD_LIBRARY
    )

    set_target_properties(deckshell-gamepad-treeland PROPERTIES
        VERSION ${PROJECT_VERSION}
        SOVERSION 1
        OUTPUT_NAME "deckshell-gamepad-treeland"
        POSITION_INDEPENDENT_CODE ON
    )

    target_compile_features(deckshell-gamepad-treeland PUBLIC cxx_std_17)

    install(DIRECTORY
        treeland
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/deckshell/deckgamepad
        FILES_MATCHING PATTERN "*.h"
    )

    install(TARGETS deckshell-gamepad-treeland
        EXPORT DeckShellGamepadTargets
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    )

    install(FILES
        "${TREELAND_GAMEPAD_PROTOCOL_XML}"
        DESTINATION ${CMAKE_INSTALL_DATADIR}/DeckShellGamepad/protocols
    )
endif()

message(STATUS "Core library configured:")
message(STATUS "  - Library type: ${BUILD_SHARED_LIBS}")
message(STATUS "  - Qt version: ${Qt6_VERSION}")
message(STATUS "  - Install prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "  - SDL DB file: ${CMAKE_CURRENT_SOURCE_DIR}/../data/gamecontrollerdb.txt")
message(STATUS "  - Treeland client: ${DECKGAMEPAD_BUILD_TREELAND_CLIENT}")
