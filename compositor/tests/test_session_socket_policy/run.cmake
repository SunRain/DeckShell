# Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

if(NOT EXISTS "${SESSION_SOURCE}")
    message(FATAL_ERROR "SessionManager source not found: ${SESSION_SOURCE}")
endif()

file(READ "${SESSION_SOURCE}" session_source)

set(expected_active
    "ptr->m_socket->setEnabled(newEnabled, globalSession()->socket());")
set(expected_previous
    "previous->m_socket->setEnabled(false, globalSession()->socket());")

foreach(expected_call IN ITEMS expected_active expected_previous)
    string(FIND "${session_source}" "${${expected_call}}" call_offset)
    if(call_offset EQUAL -1)
        message(FATAL_ERROR
            "SessionManager is missing the global Socket exclusion call: ${${expected_call}}")
    endif()
endforeach()

string(FIND "${session_source}"
       "ptr->m_socket->setEnabled(newEnabled);"
       legacy_active_offset)
if(NOT legacy_active_offset EQUAL -1)
    message(FATAL_ERROR "Legacy single-argument active Socket call is still present")
endif()

string(FIND "${session_source}"
       "previous->m_socket->setEnabled(false);"
       legacy_previous_offset)
if(NOT legacy_previous_offset EQUAL -1)
    message(FATAL_ERROR "Legacy single-argument previous Socket call is still present")
endif()
