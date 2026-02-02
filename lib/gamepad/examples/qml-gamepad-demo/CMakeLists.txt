# DeckShell.DeckGamepad QML demo

cmake_minimum_required(VERSION 3.25)

find_package(Qt6 6.8 REQUIRED COMPONENTS Core Gui Qml Quick QuickControls2)

qt_add_executable(qml-gamepad-demo
    main.cpp
)
set_target_properties(qml-gamepad-demo PROPERTIES AUTOMOC ON)

qt_add_qml_module(qml-gamepad-demo
    URI "deckshell.gamepad.demo"
    VERSION 1.0
    QML_FILES
        qml/Main.qml
)

target_link_libraries(qml-gamepad-demo
    PRIVATE
        Qt6::Core
        Qt6::Gui
        Qt6::Qml
        Qt6::Quick
        Qt6::QuickControls2
)

if(TARGET DeckShellGamepadQmlPlugin)
    get_target_property(_qml_module_dir DeckShellGamepadQmlPlugin QT_QML_MODULE_OUTPUT_DIRECTORY)
    if(_qml_module_dir)
        get_filename_component(_qml_deckshell_dir "${_qml_module_dir}" DIRECTORY) # .../DeckShell
        get_filename_component(_qml_import_root "${_qml_deckshell_dir}" DIRECTORY) # parent of DeckShell
        target_compile_definitions(qml-gamepad-demo
            PRIVATE
                DECKSHELL_GAMEPAD_QML_IMPORT_ROOT="${_qml_import_root}"
        )
    endif()
endif()

install(TARGETS qml-gamepad-demo
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
