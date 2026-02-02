// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <deckshell/deckgamepad/core/deckgamepad.h>
#include <QtCore/QHash>
#include <QtCore/QSet>
#include <QtCore/QString>

DECKGAMEPAD_BEGIN_NAMESPACE

/**
 * @brief Physical input type from evdev
 */
enum class PhysicalInputType {
    Button,      ///< evdev EV_KEY event
    Axis,        ///< evdev EV_ABS event (full range)
    Hat          ///< evdev ABS_HAT0X/Y event
};

/**
 * @brief Physical input descriptor
 * 
 * Describes a physical input from the device (evdev code)
 */
struct PhysicalInput {
    PhysicalInputType type;
    int code;        ///< evdev code (BTN_SOUTH, ABS_X, etc.)
    int hatMask;     ///< for HAT: 1=up, 2=right, 4=down, 8=left
    bool inverted;   ///< for axes: whether to invert the value
    
    PhysicalInput() 
        : type(PhysicalInputType::Button)
        , code(-1)
        , hatMask(0)
        , inverted(false)
    {}
    
    bool isValid() const { return code >= 0; }
};

/**
 * @brief Precomputed device mapping for optimal performance
 * 
 * This structure maps physical inputs (evdev codes) to logical outputs
 * (GamepadButton/GamepadAxis). It's precomputed when a device is connected
 * to make the event processing path O(1).
 */
struct DeviceMapping {
    QString guid;         ///< SDL GUID of the device
    QString name;         ///< Device name
    
    // Precomputed lookup tables: evdev code → logical button/axis
    QHash<int, GamepadButton> buttonMap;      ///< evdev button code → GamepadButton
    QHash<int, GamepadAxis> axisMap;          ///< evdev axis code → GamepadAxis
    // Hat mapping key: (hatIndex << 8) | hatMask (hatMask: 1=up,2=right,4=down,8=left)
    QHash<int, GamepadButton> hatButtonMap;   ///< hatKey → D-pad button

    // Half-axis mapping: evdev axis code → button (pressed when value crosses threshold)
    QHash<int, GamepadButton> halfAxisPosButtonMap; ///< +aX → button
    QHash<int, GamepadButton> halfAxisNegButtonMap; ///< -aX → button
    
    // Axis inversion flags
    QSet<int> invertedAxes;  ///< evdev axis codes that should be inverted
    
    DeviceMapping() {}
    
    bool isEmpty() const { 
        return buttonMap.isEmpty() && axisMap.isEmpty() && hatButtonMap.isEmpty()
            && halfAxisPosButtonMap.isEmpty() && halfAxisNegButtonMap.isEmpty();
    }
    
    bool isValid() const {
        return !guid.isEmpty() && !isEmpty();
    }
};

DECKGAMEPAD_END_NAMESPACE
