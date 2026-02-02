// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <deckshell/deckgamepad/mapping/deckgamepadmapping.h>
#include <QtCore/QHash>
#include <QtCore/QString>

DECKGAMEPAD_BEGIN_NAMESPACE

/**
 * @brief SDL input binding type
 * 
 * Describes how a logical button/axis is mapped to a physical input
 * in SDL format (e.g., "b0", "a1", "+a2", "h0.1")
 */
struct SdlInputBinding {
    enum Type {
        Button,       ///< b0, b1, b2 (physical button index)
        Axis,         ///< a0, a1, a2 (full axis)
        HalfAxisPos,  ///< +a0 (positive half of axis, acts as button)
        HalfAxisNeg,  ///< -a0 (negative half of axis, acts as button)
        Hat           ///< h0.1, h0.2, h0.4, h0.8 (HAT direction)
    };
    
    Type type;
    int index;        ///< SDL button/axis index (NOT evdev code!)
    int hatMask;      ///< for Hat type: 1=up, 2=right, 4=down, 8=left
    bool inverted;    ///< for Axis type: whether to invert the value (e.g. ~a0)
    
    SdlInputBinding() 
        : type(Button)
        , index(-1)
        , hatMask(0)
        , inverted(false)
    {}
    
    bool isValid() const { return index >= 0; }
};

/**
 * @brief SDL raw mapping (parsed from database)
 * 
 * This is the intermediate representation after parsing an SDL mapping line.
 * It maps logical buttons/axes to SDL input bindings (which use SDL indices,
 * not evdev codes).
 */
struct SdlRawMapping {
    QString guid;         ///< Device GUID
    QString name;         ///< Device name
    QString platform;     ///< Platform identifier (e.g., "Linux")
    
    // Logical button/axis → SDL input binding
    QHash<GamepadButton, SdlInputBinding> buttons;
    QHash<GamepadAxis, SdlInputBinding> axes;
    
    SdlRawMapping() {}
    
    bool isValid() const { 
        return !guid.isEmpty() && (!buttons.isEmpty() || !axes.isEmpty());
    }
};

/**
 * @brief Private data for DeckGamepadSdlControllerDb
 */
class DeckGamepadSdlControllerDbPrivate
{
public:
    DeckGamepadSdlControllerDbPrivate() : loadedCount(0) {}
    
    // Database storage: GUID → raw mapping
    QHash<QString, SdlRawMapping> mappings;
    
    // Metadata
    QString databasePath;
    int loadedCount;
    
    // Parsing helpers
    bool parseMappingLine(const QString &line, SdlRawMapping &out);
    SdlInputBinding parseInputBinding(const QString &value);
    
    // Conversion helper
    DeviceMapping convertToDeviceMapping(
        const SdlRawMapping &rawMapping,
        const QHash<int, int> &physicalButtonMap,
        const QHash<int, int> &physicalAxisMap
    ) const;
};

DECKGAMEPAD_END_NAMESPACE
