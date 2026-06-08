# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

if(NOT EXISTS "${QPA_PROBE_EXECUTABLE}")
    message(FATAL_ERROR "QPA lifecycle probe not found: ${QPA_PROBE_EXECUTABLE}")
endif()

file(READ "${DECKCOMPOSITOR_MAIN}" main_source)

string(FIND "${main_source}" "QGuiApplicationPrivate::platform_theme" platform_theme_offset)
if(NOT platform_theme_offset EQUAL -1)
    message(FATAL_ERROR "main.cpp still mutates QGuiApplicationPrivate::platform_theme")
endif()

string(FIND "${main_source}" "private/qguiapplication_p.h" private_header_offset)
if(NOT private_header_offset EQUAL -1)
    message(FATAL_ERROR "main.cpp still includes qguiapplication_p.h")
endif()

string(FIND "${main_source}" "WServer::initializeQPA(" qpa_call_offset)
string(FIND "${main_source}" "[](const QString &)" qpa_callback_offset)
if(qpa_call_offset EQUAL -1 OR qpa_callback_offset EQUAL -1)
    message(FATAL_ERROR "main.cpp does not initialize QPA with the Waylib theme callback")
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
