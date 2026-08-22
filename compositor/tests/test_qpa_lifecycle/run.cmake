# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

if(NOT EXISTS "${QPA_PROBE_EXECUTABLE}")
    message(FATAL_ERROR "QPA lifecycle probe not found: ${QPA_PROBE_EXECUTABLE}")
endif()

file(READ "${DECKCOMPOSITOR_MAIN}" main_source)
get_filename_component(main_directory "${DECKCOMPOSITOR_MAIN}" DIRECTORY)
file(READ "${main_directory}/core/treelandinit.cpp" initialization_source)
set(startup_source "${main_source}\n${initialization_source}")

string(FIND "${startup_source}" "QGuiApplicationPrivate::platform_theme" platform_theme_offset)
if(NOT platform_theme_offset EQUAL -1)
    message(FATAL_ERROR "Startup code still mutates QGuiApplicationPrivate::platform_theme")
endif()

string(FIND "${startup_source}" "private/qguiapplication_p.h" private_header_offset)
if(NOT private_header_offset EQUAL -1)
    message(FATAL_ERROR "Startup code still includes qguiapplication_p.h")
endif()

string(FIND "${main_source}" "Treeland::preInit(" pre_init_offset)
string(FIND "${initialization_source}" "WServer::initializeQPA(" qpa_call_offset)
string(FIND "${initialization_source}" "[](const QString &)" qpa_callback_offset)
string(FIND "${initialization_source}" "std::make_unique<QGuiApplication>" application_offset)
if(pre_init_offset EQUAL -1 OR qpa_call_offset EQUAL -1 OR qpa_callback_offset EQUAL -1
        OR application_offset EQUAL -1 OR NOT qpa_call_offset LESS application_offset)
    message(FATAL_ERROR "Startup must initialize QPA with the Waylib theme callback before QGuiApplication")
endif()

foreach(attempt RANGE 1 2)
    execute_process(
        COMMAND ${CMAKE_COMMAND} -E env
            WLR_BACKENDS=headless
            WLR_RENDERER=pixman
            "${QPA_PROBE_EXECUTABLE}"
        RESULT_VARIABLE result
        OUTPUT_VARIABLE output
        ERROR_VARIABLE error
        TIMEOUT 8
    )

    if(NOT result EQUAL 0)
        message(FATAL_ERROR
            "QPA lifecycle attempt ${attempt} failed with ${result}\n"
            "stdout:\n${output}\n"
            "stderr:\n${error}"
        )
    endif()
endforeach()
