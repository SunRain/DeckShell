// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <deckshell/deckgamepad/mapping/deckgamepadmapping.h>
#include <deckshell/deckgamepad/mapping/deckgamepadsdlcontrollerdb.h>

#include <QtCore/QMap>

DECKGAMEPAD_BEGIN_NAMESPACE

inline DeviceMapping deckGamepadParseSdlMappingString(
    const QString &mappingString,
    const QHash<int, int> &physicalButtonMap,
    const QHash<int, int> &physicalAxisMap)
{
    const QStringList parts = mappingString.split(QLatin1Char(','), Qt::KeepEmptyParts);
    if (parts.size() < 3) {
        return {};
    }

    const QString guid = parts[0].trimmed();
    if (guid.isEmpty()) {
        return {};
    }

    DeckGamepadSdlControllerDb db;
    if (!db.addMapping(mappingString)) {
        return {};
    }

    return db.createDeviceMapping(guid, physicalButtonMap, physicalAxisMap);
}

inline QString deckGamepadComposeSdlMappingString(
    const DeviceMapping &mapping,
    const QHash<int, int> &physicalButtonMap,
    const QHash<int, int> &physicalAxisMap)
{
    if (mapping.guid.isEmpty()) {
        return {};
    }

    auto sdlKeyForButton = [](GamepadButton button) -> QString {
        switch (button) {
        case GAMEPAD_BUTTON_A:
            return QStringLiteral("a");
        case GAMEPAD_BUTTON_B:
            return QStringLiteral("b");
        case GAMEPAD_BUTTON_X:
            return QStringLiteral("x");
        case GAMEPAD_BUTTON_Y:
            return QStringLiteral("y");
        case GAMEPAD_BUTTON_L1:
            return QStringLiteral("leftshoulder");
        case GAMEPAD_BUTTON_R1:
            return QStringLiteral("rightshoulder");
        case GAMEPAD_BUTTON_SELECT:
            return QStringLiteral("back");
        case GAMEPAD_BUTTON_START:
            return QStringLiteral("start");
        case GAMEPAD_BUTTON_GUIDE:
            return QStringLiteral("guide");
        case GAMEPAD_BUTTON_L3:
            return QStringLiteral("leftstick");
        case GAMEPAD_BUTTON_R3:
            return QStringLiteral("rightstick");
        case GAMEPAD_BUTTON_DPAD_UP:
            return QStringLiteral("dpup");
        case GAMEPAD_BUTTON_DPAD_DOWN:
            return QStringLiteral("dpdown");
        case GAMEPAD_BUTTON_DPAD_LEFT:
            return QStringLiteral("dpleft");
        case GAMEPAD_BUTTON_DPAD_RIGHT:
            return QStringLiteral("dpright");
        default:
            return {};
        }
    };

    auto sdlKeyForAxis = [](GamepadAxis axis) -> QString {
        switch (axis) {
        case GAMEPAD_AXIS_LEFT_X:
            return QStringLiteral("leftx");
        case GAMEPAD_AXIS_LEFT_Y:
            return QStringLiteral("lefty");
        case GAMEPAD_AXIS_RIGHT_X:
            return QStringLiteral("rightx");
        case GAMEPAD_AXIS_RIGHT_Y:
            return QStringLiteral("righty");
        case GAMEPAD_AXIS_TRIGGER_LEFT:
            return QStringLiteral("lefttrigger");
        case GAMEPAD_AXIS_TRIGGER_RIGHT:
            return QStringLiteral("righttrigger");
        default:
            return {};
        }
    };

    QMap<QString, QString> items;

    for (auto it = mapping.buttonMap.constBegin(); it != mapping.buttonMap.constEnd(); ++it) {
        const QString sdlKey = sdlKeyForButton(it.value());
        if (sdlKey.isEmpty()) {
            continue;
        }

        const int buttonIndex = physicalButtonMap.value(it.key(), -1);
        if (buttonIndex < 0) {
            continue;
        }

        items.insert(sdlKey, QStringLiteral("b%1").arg(buttonIndex));
    }

    for (auto it = mapping.halfAxisPosButtonMap.constBegin(); it != mapping.halfAxisPosButtonMap.constEnd(); ++it) {
        const QString sdlKey = sdlKeyForButton(it.value());
        if (sdlKey.isEmpty()) {
            continue;
        }

        const int axisIndex = physicalAxisMap.value(it.key(), -1);
        if (axisIndex < 0) {
            continue;
        }

        items.insert(sdlKey, QStringLiteral("+a%1").arg(axisIndex));
    }

    for (auto it = mapping.halfAxisNegButtonMap.constBegin(); it != mapping.halfAxisNegButtonMap.constEnd(); ++it) {
        const QString sdlKey = sdlKeyForButton(it.value());
        if (sdlKey.isEmpty()) {
            continue;
        }

        const int axisIndex = physicalAxisMap.value(it.key(), -1);
        if (axisIndex < 0) {
            continue;
        }

        items.insert(sdlKey, QStringLiteral("-a%1").arg(axisIndex));
    }

    for (auto it = mapping.axisMap.constBegin(); it != mapping.axisMap.constEnd(); ++it) {
        const QString sdlKey = sdlKeyForAxis(it.value());
        if (sdlKey.isEmpty()) {
            continue;
        }

        const int axisIndex = physicalAxisMap.value(it.key(), -1);
        if (axisIndex < 0) {
            continue;
        }

        const bool inverted = mapping.invertedAxes.contains(it.key());
        items.insert(sdlKey, QStringLiteral("%1a%2").arg(inverted ? QStringLiteral("~") : QString{}, QString::number(axisIndex)));
    }

    for (auto it = mapping.hatButtonMap.constBegin(); it != mapping.hatButtonMap.constEnd(); ++it) {
        const QString sdlKey = sdlKeyForButton(it.value());
        if (sdlKey.isEmpty()) {
            continue;
        }

        const int hatKey = it.key();
        const int hatIndex = (hatKey >> 8) & 0xFF;
        const int hatMask = hatKey & 0xFF;
        items.insert(sdlKey, QStringLiteral("h%1.%2").arg(hatIndex).arg(hatMask));
    }

    QStringList partsOut;
    partsOut << mapping.guid;
    partsOut << (mapping.name.isEmpty() ? QStringLiteral("Unknown Gamepad") : mapping.name);
    for (auto it = items.constBegin(); it != items.constEnd(); ++it) {
        partsOut << QStringLiteral("%1:%2").arg(it.key(), it.value());
    }
    partsOut << QStringLiteral("platform:Linux");

    return partsOut.join(QLatin1Char(','));
}

DECKGAMEPAD_END_NAMESPACE

