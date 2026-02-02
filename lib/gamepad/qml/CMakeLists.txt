# DeckShell Gamepad QML module
# URI: DeckShell.DeckGamepad

cmake_minimum_required(VERSION 3.25)

find_package(Qt6 6.8 REQUIRED COMPONENTS Core Gui Qml)

set(CMAKE_AUTOMOC ON)

	set(QML_GAMEPAD_SOURCES
	    abstractgamepadactionsource.h
	    gamepadconfigmanager.h
	    gamepadconfigmanager.cpp
	    gamepadmanager.h
	    gamepadmanager.cpp
    gamepaddevicemodel.h
    gamepaddevicemodel.cpp
    mappingeditorbridge.h
    mappingeditorbridge.cpp
    gamepad.h
    gamepad.cpp
    gamepadactionrouter.h
    gamepadactionrouter.cpp
    gamepadactionkeymapper.h
    gamepadactionkeymapper.cpp
    gamepadkeynavigation.h
    gamepadkeynavigation.cpp
    serviceactionrouter.h
    serviceactionrouter.cpp
    custommappingmanager.h
    custommappingmanager.cpp
)

qt_add_library(DeckShellGamepadQmlPlugin SHARED)

qt_add_qml_module(DeckShellGamepadQmlPlugin
    URI "DeckShell.DeckGamepad"
    VERSION 1.0
    CLASS_NAME GamepadQmlPlugin
    OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/DeckShell/DeckGamepad"
    SOURCES
        ${QML_GAMEPAD_SOURCES}
)

target_link_libraries(DeckShellGamepadQmlPlugin
    PRIVATE
        Qt6::Core
        Qt6::Gui
        Qt6::Qml
        deckshell-gamepad
)

if(TARGET deckshell-gamepad-treeland)
    target_link_libraries(DeckShellGamepadQmlPlugin PRIVATE deckshell-gamepad-treeland)
    target_compile_definitions(DeckShellGamepadQmlPlugin PRIVATE DECKGAMEPAD_ENABLE_TREELAND=1)
endif()

install(TARGETS DeckShellGamepadQmlPlugin DeckShellGamepadQmlPluginplugin
    LIBRARY DESTINATION ${CMAKE_INSTALL_QMLDIR}/DeckShell/DeckGamepad
)

install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/DeckShell/DeckGamepad/qmldir"
    "${CMAKE_CURRENT_BINARY_DIR}/DeckShell/DeckGamepad/DeckShellGamepadQmlPlugin.qmltypes"
    DESTINATION ${CMAKE_INSTALL_QMLDIR}/DeckShell/DeckGamepad
)
