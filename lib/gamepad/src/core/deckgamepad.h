// Copyright (C) 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QtCore/QMetaType>
#include <QtCore/qglobal.h>

#include <stdint.h>

// 导出宏：通常由 CMake 提供；为单独编译提供兜底定义。
#ifndef DECKGAMEPAD_EXPORT
#  if defined(BUILD_SHARED_LIBS)
#    define DECKGAMEPAD_EXPORT Q_DECL_EXPORT
#  else
#    define DECKGAMEPAD_EXPORT
#  endif
#endif

// 命名空间宏：通常由 CMake 提供；为单独编译提供兜底定义。
#ifndef DECKGAMEPAD_BEGIN_NAMESPACE
#  define DECKGAMEPAD_BEGIN_NAMESPACE namespace deckshell { namespace deckgamepad {
#  define DECKGAMEPAD_END_NAMESPACE }}
#  define DECKGAMEPAD_USE_NAMESPACE using namespace deckshell::deckgamepad;
#endif

DECKGAMEPAD_BEGIN_NAMESPACE

// 按键事件（button 为 GamepadButton）。
struct DeckGamepadButtonEvent {
    uint32_t time_msec;
    uint32_t button; // GamepadButton
    bool pressed;
};

// 轴事件（axis 为 GamepadAxis；value 归一化到 [-1, 1]）。
struct DeckGamepadAxisEvent {
    uint32_t time_msec;
    uint32_t axis; // GamepadAxis
    double value;
};

// Hat/D-pad 事件（value 为 GamepadHatMask 位或）。
struct DeckGamepadHatEvent {
    uint32_t time_msec;
    uint32_t hat; // Hat 索引（通常为 0）
    int32_t value;
};

// 按键枚举（对齐 SDL2/Xbox 常用布局）。
enum GamepadButton {
    GAMEPAD_BUTTON_INVALID = -1,
    GAMEPAD_BUTTON_A = 0, // BTN_SOUTH / BTN_A
    GAMEPAD_BUTTON_B,     // BTN_EAST / BTN_B
    GAMEPAD_BUTTON_X,     // BTN_NORTH / BTN_X
    GAMEPAD_BUTTON_Y,     // BTN_WEST / BTN_Y
    GAMEPAD_BUTTON_L1,    // BTN_TL
    GAMEPAD_BUTTON_R1,    // BTN_TR
    GAMEPAD_BUTTON_L2,    // BTN_TL2
    GAMEPAD_BUTTON_R2,    // BTN_TR2
    GAMEPAD_BUTTON_SELECT, // BTN_SELECT / Back
    GAMEPAD_BUTTON_START,  // BTN_START
    GAMEPAD_BUTTON_L3,     // BTN_THUMBL
    GAMEPAD_BUTTON_R3,     // BTN_THUMBR
    GAMEPAD_BUTTON_GUIDE,  // BTN_MODE / Home
    GAMEPAD_BUTTON_DPAD_UP, // 由 hat 映射生成
    GAMEPAD_BUTTON_DPAD_DOWN,
    GAMEPAD_BUTTON_DPAD_LEFT,
    GAMEPAD_BUTTON_DPAD_RIGHT,
    GAMEPAD_BUTTON_MAX
};

// 轴枚举（evdev：ABS_*）。
enum GamepadAxis {
    GAMEPAD_AXIS_INVALID = -1,
    GAMEPAD_AXIS_LEFT_X = 0, // ABS_X
    GAMEPAD_AXIS_LEFT_Y,     // ABS_Y
    GAMEPAD_AXIS_RIGHT_X,    // ABS_RX
    GAMEPAD_AXIS_RIGHT_Y,    // ABS_RY
    GAMEPAD_AXIS_TRIGGER_LEFT, // ABS_Z
    GAMEPAD_AXIS_TRIGGER_RIGHT, // ABS_RZ
    GAMEPAD_AXIS_MAX
};

// Hat 方向位掩码（可位或组合）。
enum GamepadHatMask {
    GAMEPAD_HAT_CENTER = 0,
    GAMEPAD_HAT_UP = 1,
    GAMEPAD_HAT_RIGHT = 2,
    GAMEPAD_HAT_DOWN = 4,
    GAMEPAD_HAT_LEFT = 8
};

DECKGAMEPAD_END_NAMESPACE

namespace deckshell {
#if defined(Q_MOC_RUN)
namespace gamepad {
#else
namespace [[deprecated("use deckshell::deckgamepad")]] gamepad {
#endif
using namespace deckgamepad;
} // namespace gamepad
} // namespace deckshell

Q_DECLARE_METATYPE(deckshell::deckgamepad::DeckGamepadButtonEvent)
Q_DECLARE_METATYPE(deckshell::deckgamepad::DeckGamepadAxisEvent)
Q_DECLARE_METATYPE(deckshell::deckgamepad::DeckGamepadHatEvent)
