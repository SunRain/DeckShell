# DeckShellGamepad tests (standalone, no DeckShell repo dependency)

if(NOT BUILD_TESTING)
    return()
endif()

set(smoke_script_in "${CMAKE_CURRENT_SOURCE_DIR}/cmake/deckgamepad_install_find_package_smoke.cmake.in")
set(smoke_script_out "${CMAKE_CURRENT_BINARY_DIR}/deckgamepad_install_find_package_smoke.cmake")

configure_file("${smoke_script_in}" "${smoke_script_out}" @ONLY)

add_test(
    NAME deckgamepad_install_find_package_smoke
    COMMAND "${CMAKE_COMMAND}" -P "${smoke_script_out}"
)

find_package(Qt6 6.8 REQUIRED COMPONENTS Test)

add_executable(test_action_mapper
    test_action_mapper.cpp
)
set_target_properties(test_action_mapper PROPERTIES AUTOMOC ON)
target_link_libraries(test_action_mapper PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_action_mapper COMMAND test_action_mapper)

add_executable(test_action_mapper_repeat
    test_action_mapper_repeat.cpp
)
set_target_properties(test_action_mapper_repeat PROPERTIES AUTOMOC ON)
target_link_libraries(test_action_mapper_repeat PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_action_mapper_repeat COMMAND test_action_mapper_repeat)

add_executable(test_action_mapping_profile
    test_action_mapping_profile.cpp
)
set_target_properties(test_action_mapping_profile PROPERTIES AUTOMOC ON)
target_link_libraries(test_action_mapping_profile PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_action_mapping_profile COMMAND test_action_mapping_profile)

add_executable(test_service_action_mapping
    test_service_action_mapping.cpp
)
set_target_properties(test_service_action_mapping PROPERTIES AUTOMOC ON)
target_link_libraries(test_service_action_mapping PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_service_action_mapping COMMAND test_service_action_mapping)

add_executable(test_diagnostic_key
    test_diagnostic_key.cpp
)
set_target_properties(test_diagnostic_key PROPERTIES AUTOMOC ON)
target_link_libraries(test_diagnostic_key PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_diagnostic_key COMMAND test_diagnostic_key)

add_executable(test_device_uid
    test_device_uid.cpp
)
set_target_properties(test_device_uid PROPERTIES AUTOMOC ON)
target_link_libraries(test_device_uid PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_device_uid COMMAND test_device_uid)

add_executable(test_coalesce
    test_coalesce.cpp
)
set_target_properties(test_coalesce PROPERTIES AUTOMOC ON)
target_link_libraries(test_coalesce PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_coalesce COMMAND test_coalesce)

add_executable(test_sdl_controller_db_mapping
    test_sdl_controller_db_mapping.cpp
)
set_target_properties(test_sdl_controller_db_mapping PROPERTIES AUTOMOC ON)
target_link_libraries(test_sdl_controller_db_mapping PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_sdl_controller_db_mapping COMMAND test_sdl_controller_db_mapping)

add_executable(test_custom_mapping_roundtrip
    test_custom_mapping_roundtrip.cpp
)
set_target_properties(test_custom_mapping_roundtrip PROPERTIES AUTOMOC ON)
target_link_libraries(test_custom_mapping_roundtrip PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_custom_mapping_roundtrip COMMAND test_custom_mapping_roundtrip)

add_executable(test_calibration_store_json
    test_calibration_store_json.cpp
)
set_target_properties(test_calibration_store_json PROPERTIES AUTOMOC ON)
target_link_libraries(test_calibration_store_json PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_calibration_store_json COMMAND test_calibration_store_json)

add_executable(test_calibration_evdev_integration
    test_calibration_evdev_integration.cpp
    uinput_test_device.cpp
)
set_target_properties(test_calibration_evdev_integration PROPERTIES AUTOMOC ON)
target_link_libraries(test_calibration_evdev_integration PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_calibration_evdev_integration COMMAND test_calibration_evdev_integration)

add_executable(test_service_provider_selection
    test_service_provider_selection.cpp
)
set_target_properties(test_service_provider_selection PROPERTIES AUTOMOC ON)
target_link_libraries(test_service_provider_selection PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_service_provider_selection COMMAND test_service_provider_selection)

add_executable(test_player_assignment
    test_player_assignment.cpp
)
set_target_properties(test_player_assignment PROPERTIES AUTOMOC ON)
target_link_libraries(test_player_assignment PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_player_assignment COMMAND test_player_assignment)

add_executable(test_evdevprovider_spike
    test_evdevprovider_spike.cpp
)
set_target_properties(test_evdevprovider_spike PROPERTIES AUTOMOC ON)
target_link_libraries(test_evdevprovider_spike PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_evdevprovider_spike COMMAND test_evdevprovider_spike)

add_executable(test_backend_provider_regression
    test_backend_provider_regression.cpp
)
set_target_properties(test_backend_provider_regression PROPERTIES AUTOMOC ON)
target_link_libraries(test_backend_provider_regression PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_backend_provider_regression COMMAND test_backend_provider_regression)

add_executable(test_uinput_udev_integration
    test_uinput_udev_integration.cpp
    uinput_test_device.cpp
)
set_target_properties(test_uinput_udev_integration PROPERTIES AUTOMOC ON)
target_link_libraries(test_uinput_udev_integration PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_uinput_udev_integration COMMAND test_uinput_udev_integration)

add_executable(test_sdl_db_override_evdev_integration
    test_sdl_db_override_evdev_integration.cpp
    uinput_test_device.cpp
)
set_target_properties(test_sdl_db_override_evdev_integration PROPERTIES AUTOMOC ON)
target_link_libraries(test_sdl_db_override_evdev_integration PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_sdl_db_override_evdev_integration COMMAND test_sdl_db_override_evdev_integration)

add_executable(test_multi_device_hotplug_stress
    test_multi_device_hotplug_stress.cpp
    uinput_test_device.cpp
)
set_target_properties(test_multi_device_hotplug_stress PROPERTIES AUTOMOC ON)
target_link_libraries(test_multi_device_hotplug_stress PRIVATE Qt6::Core Qt6::Test deckshell-gamepad)
add_test(NAME deckgamepad_multi_device_hotplug_stress COMMAND test_multi_device_hotplug_stress)

if(DECKGAMEPAD_BUILD_QML_MODULE)
    find_package(Qt6 6.8 REQUIRED COMPONENTS Gui Qml)

    add_executable(test_qml_import
        test_qml_import.cpp
    )

    set_target_properties(test_qml_import PROPERTIES
        AUTOMOC ON
    )

    target_link_libraries(test_qml_import
        PRIVATE
            Qt6::Core
            Qt6::Gui
            Qt6::Qml
            Qt6::Test
    )

    add_executable(test_qml_keynavigation_service_action
        test_qml_keynavigation_service_action.cpp
    )

    set_target_properties(test_qml_keynavigation_service_action PROPERTIES
        AUTOMOC ON
    )

    target_link_libraries(test_qml_keynavigation_service_action
        PRIVATE
            Qt6::Core
            Qt6::Gui
            Qt6::Qml
            Qt6::Test
            deckshell-gamepad
    )

    add_executable(test_qml_keynavigation_evdev_e2e
        test_qml_keynavigation_evdev_e2e.cpp
        uinput_test_device.cpp
    )

    set_target_properties(test_qml_keynavigation_evdev_e2e PROPERTIES
        AUTOMOC ON
    )

    target_link_libraries(test_qml_keynavigation_evdev_e2e
        PRIVATE
            Qt6::Core
            Qt6::Gui
            Qt6::Qml
            Qt6::Test
            deckshell-gamepad
    )

    add_executable(test_qml_keynavigation_repeat_hold_e2e
        test_qml_keynavigation_repeat_hold_e2e.cpp
        uinput_test_device.cpp
    )

    set_target_properties(test_qml_keynavigation_repeat_hold_e2e PROPERTIES
        AUTOMOC ON
    )

    target_link_libraries(test_qml_keynavigation_repeat_hold_e2e
        PRIVATE
            Qt6::Core
            Qt6::Gui
            Qt6::Qml
            Qt6::Test
            deckshell-gamepad
    )

    add_executable(test_custom_mapping_evdev_e2e
        test_custom_mapping_evdev_e2e.cpp
        uinput_test_device.cpp
    )

    set_target_properties(test_custom_mapping_evdev_e2e PROPERTIES
        AUTOMOC ON
    )

    target_link_libraries(test_custom_mapping_evdev_e2e
        PRIVATE
            Qt6::Core
            Qt6::Gui
            Qt6::Qml
            Qt6::Test
            deckshell-gamepad
    )

    if(TARGET DeckShellGamepadQmlPlugin)
        get_target_property(_qml_module_dir DeckShellGamepadQmlPlugin QT_QML_MODULE_OUTPUT_DIRECTORY)
        if(_qml_module_dir)
            get_filename_component(_qml_deckshell_dir "${_qml_module_dir}" DIRECTORY) # .../DeckShell
            get_filename_component(_qml_import_root "${_qml_deckshell_dir}" DIRECTORY) # parent of DeckShell
            target_compile_definitions(test_qml_import
                PRIVATE
                    DECKGAMEPAD_QML_IMPORT_ROOT="${_qml_import_root}"
            )
            target_compile_definitions(test_qml_keynavigation_service_action
                PRIVATE
                    DECKGAMEPAD_QML_IMPORT_ROOT="${_qml_import_root}"
            )
            target_compile_definitions(test_qml_keynavigation_evdev_e2e
                PRIVATE
                    DECKGAMEPAD_QML_IMPORT_ROOT="${_qml_import_root}"
            )
            target_compile_definitions(test_qml_keynavigation_repeat_hold_e2e
                PRIVATE
                    DECKGAMEPAD_QML_IMPORT_ROOT="${_qml_import_root}"
            )
            target_compile_definitions(test_custom_mapping_evdev_e2e
                PRIVATE
                    DECKGAMEPAD_QML_IMPORT_ROOT="${_qml_import_root}"
            )
        endif()
    endif()

    add_test(
        NAME deckgamepad_qml_import_smoke
        COMMAND test_qml_import
    )

    set_tests_properties(deckgamepad_qml_import_smoke PROPERTIES
        ENVIRONMENT "QT_QPA_PLATFORM=offscreen"
    )

    add_test(
        NAME deckgamepad_qml_keynavigation_service_action
        COMMAND test_qml_keynavigation_service_action
    )

    set_tests_properties(deckgamepad_qml_keynavigation_service_action PROPERTIES
        ENVIRONMENT "QT_QPA_PLATFORM=offscreen"
    )

    add_executable(test_qml_keynavigation_release_target
        test_qml_keynavigation_release_target.cpp
    )

    set_target_properties(test_qml_keynavigation_release_target PROPERTIES
        AUTOMOC ON
    )

    target_link_libraries(test_qml_keynavigation_release_target
        PRIVATE
            Qt6::Core
            Qt6::Gui
            Qt6::Qml
            Qt6::Test
            deckshell-gamepad
    )

    if(TARGET DeckShellGamepadQmlPlugin)
        get_target_property(_qml_module_dir DeckShellGamepadQmlPlugin QT_QML_MODULE_OUTPUT_DIRECTORY)
        if(_qml_module_dir)
            get_filename_component(_qml_deckshell_dir "${_qml_module_dir}" DIRECTORY) # .../DeckShell
            get_filename_component(_qml_import_root "${_qml_deckshell_dir}" DIRECTORY) # parent of DeckShell
            target_compile_definitions(test_qml_keynavigation_release_target
                PRIVATE
                    DECKGAMEPAD_QML_IMPORT_ROOT="${_qml_import_root}"
            )
        endif()
    endif()

    add_test(
        NAME deckgamepad_qml_keynavigation_release_target
        COMMAND test_qml_keynavigation_release_target
    )

    set_tests_properties(deckgamepad_qml_keynavigation_release_target PROPERTIES
        ENVIRONMENT "QT_QPA_PLATFORM=offscreen"
    )

    add_test(
        NAME deckgamepad_qml_keynavigation_evdev_e2e
        COMMAND test_qml_keynavigation_evdev_e2e
    )

    set_tests_properties(deckgamepad_qml_keynavigation_evdev_e2e PROPERTIES
        ENVIRONMENT "QT_QPA_PLATFORM=offscreen"
    )

    add_test(
        NAME deckgamepad_qml_keynavigation_repeat_hold_e2e
        COMMAND test_qml_keynavigation_repeat_hold_e2e
    )

    set_tests_properties(deckgamepad_qml_keynavigation_repeat_hold_e2e PROPERTIES
        ENVIRONMENT "QT_QPA_PLATFORM=offscreen"
    )

    add_test(
        NAME deckgamepad_custom_mapping_evdev_e2e
        COMMAND test_custom_mapping_evdev_e2e
    )

    set_tests_properties(deckgamepad_custom_mapping_evdev_e2e PROPERTIES
        ENVIRONMENT "QT_QPA_PLATFORM=offscreen"
    )
endif()

set(_deckgamepad_test_targets
    test_action_mapper
    test_action_mapper_repeat
    test_action_mapping_profile
    test_service_action_mapping
    test_diagnostic_key
    test_device_uid
    test_coalesce
    test_sdl_controller_db_mapping
    test_custom_mapping_roundtrip
    test_calibration_store_json
    test_calibration_evdev_integration
    test_service_provider_selection
    test_player_assignment
    test_evdevprovider_spike
    test_backend_provider_regression
    test_uinput_udev_integration
    test_sdl_db_override_evdev_integration
    test_multi_device_hotplug_stress
)

if(DECKGAMEPAD_BUILD_QML_MODULE)
    list(APPEND _deckgamepad_test_targets
        test_qml_import
        test_qml_keynavigation_service_action
        test_qml_keynavigation_evdev_e2e
        test_qml_keynavigation_repeat_hold_e2e
        test_custom_mapping_evdev_e2e
        test_qml_keynavigation_release_target
    )
endif()

add_custom_target(deckgamepad-tests
    DEPENDS ${_deckgamepad_test_targets}
)
