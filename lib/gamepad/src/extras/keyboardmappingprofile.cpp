// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "keyboardmappingprofile.h"

#include <QJsonObject>
#include <QJsonArray>
#include <QDebug>

DECKGAMEPAD_BEGIN_NAMESPACE

KeyboardMappingProfile::KeyboardMappingProfile()
    : createdAt(QDateTime::currentDateTime())
    , modifiedAt(QDateTime::currentDateTime())
{
}

KeyboardMappingProfile::KeyboardMappingProfile(const QString &profileName)
    : name(profileName)
    , createdAt(QDateTime::currentDateTime())
    , modifiedAt(QDateTime::currentDateTime())
{
}

QJsonObject KeyboardMappingProfile::toJson() const
{
    QJsonObject obj;
    
    obj["name"] = name;
    obj["description"] = description;
    obj["version"] = "1.0";
    obj["created_at"] = createdAt.toString(Qt::ISODate);
    obj["modified_at"] = modifiedAt.toString(Qt::ISODate);
    
    // Serialize button mappings
    QJsonObject buttonMappingsObj;
    for (auto it = buttonMappings.constBegin(); it != buttonMappings.constEnd(); ++it) {
        QString key = QString::number(static_cast<int>(it.key()));
        buttonMappingsObj[key] = it.value().toJson();
    }
    obj["button_mappings"] = buttonMappingsObj;
    
    // Serialize axis mappings
    QJsonObject axisMappingsObj;
    for (auto it = axisMappings.constBegin(); it != axisMappings.constEnd(); ++it) {
        QString key = QString::number(static_cast<int>(it.key()));
        axisMappingsObj[key] = it.value().toJson();
    }
    obj["axis_mappings"] = axisMappingsObj;
    
    return obj;
}

KeyboardMappingProfile KeyboardMappingProfile::fromJson(const QJsonObject &obj)
{
    KeyboardMappingProfile profile;
    
    profile.name = obj.value("name").toString();
    profile.description = obj.value("description").toString();
    profile.createdAt = QDateTime::fromString(obj.value("created_at").toString(), Qt::ISODate);
    profile.modifiedAt = QDateTime::fromString(obj.value("modified_at").toString(), Qt::ISODate);
    
    // Deserialize button mappings
    QJsonObject buttonMappingsObj = obj.value("button_mappings").toObject();
    for (const QString &key : buttonMappingsObj.keys()) {
        bool ok;
        int buttonInt = key.toInt(&ok);
        if (ok) {
            GamepadButton button = static_cast<GamepadButton>(buttonInt);
            KeyMapping mapping = KeyMapping::fromJson(buttonMappingsObj[key].toObject());
            profile.buttonMappings[button] = mapping;
        }
    }
    
    // Deserialize axis mappings
    QJsonObject axisMappingsObj = obj.value("axis_mappings").toObject();
    for (const QString &key : axisMappingsObj.keys()) {
        bool ok;
        int axisInt = key.toInt(&ok);
        if (ok) {
            GamepadAxis axis = static_cast<GamepadAxis>(axisInt);
            AxisKeyMapping mapping = AxisKeyMapping::fromJson(axisMappingsObj[key].toObject());
            profile.axisMappings[axis] = mapping;
        }
    }
    
    return profile;
}

void KeyboardMappingProfile::applyTo(DeckGamepadKeyboardMappingManager *manager) const
{
    if (!manager)
        return;
    
    // Clear existing mappings
    manager->clearAll();
    
    // Apply button mappings
    for (auto it = buttonMappings.constBegin(); it != buttonMappings.constEnd(); ++it) {
        manager->setButtonMapping(it.key(), it.value());
    }
    
    // Apply axis mappings
    for (auto it = axisMappings.constBegin(); it != axisMappings.constEnd(); ++it) {
        manager->setAxisMapping(it.key(), it.value());
    }
}

KeyboardMappingProfile KeyboardMappingProfile::fromManager(const QString &name, 
                                                            const DeckGamepadKeyboardMappingManager *manager)
{
    KeyboardMappingProfile profile(name);
    
    if (!manager)
        return profile;
    
    // TODO: Need to add API to DeckGamepadKeyboardMappingManager to export current mappings
    // For now, this creates an empty profile with the given name
    
    return profile;
}

// ========== Preset Templates ==========

KeyboardMappingProfile KeyboardMappingProfile::createWASDPreset()
{
    KeyboardMappingProfile profile("WASD");
    profile.description = "WASD movement + Space jump + Shift sprint";
    
    // Left stick: WASD
    AxisKeyMapping leftStickX;
    leftStickX.negative = KeyMapping(Qt::Key_A, 0, "A - Move Left");
    leftStickX.positive = KeyMapping(Qt::Key_D, 0, "D - Move Right");
    leftStickX.threshold = 0.3f;
    profile.axisMappings[GAMEPAD_AXIS_LEFT_X] = leftStickX;
    
    AxisKeyMapping leftStickY;
    leftStickY.negative = KeyMapping(Qt::Key_W, 0, "W - Move Forward");
    leftStickY.positive = KeyMapping(Qt::Key_S, 0, "S - Move Backward");
    leftStickY.threshold = 0.3f;
    profile.axisMappings[GAMEPAD_AXIS_LEFT_Y] = leftStickY;
    
    // Buttons
    profile.buttonMappings[GAMEPAD_BUTTON_A] = KeyMapping(Qt::Key_Space, 0, "Space - Jump");
    profile.buttonMappings[GAMEPAD_BUTTON_B] = KeyMapping(Qt::Key_Shift, 0, "Shift - Sprint");
    profile.buttonMappings[GAMEPAD_BUTTON_X] = KeyMapping(Qt::Key_E, 0, "E - Interact");
    profile.buttonMappings[GAMEPAD_BUTTON_Y] = KeyMapping(Qt::Key_R, 0, "R - Reload");
    
    return profile;
}

KeyboardMappingProfile KeyboardMappingProfile::createArrowKeysPreset()
{
    KeyboardMappingProfile profile("Arrow Keys");
    profile.description = "Arrow keys + Enter/Ctrl for retro games";
    
    // DPad: Arrow Keys (using Left Stick)
    AxisKeyMapping leftStickX;
    leftStickX.negative = KeyMapping(Qt::Key_Left, 0, "Left Arrow");
    leftStickX.positive = KeyMapping(Qt::Key_Right, 0, "Right Arrow");
    leftStickX.threshold = 0.3f;
    profile.axisMappings[GAMEPAD_AXIS_LEFT_X] = leftStickX;
    
    AxisKeyMapping leftStickY;
    leftStickY.negative = KeyMapping(Qt::Key_Up, 0, "Up Arrow");
    leftStickY.positive = KeyMapping(Qt::Key_Down, 0, "Down Arrow");
    leftStickY.threshold = 0.3f;
    profile.axisMappings[GAMEPAD_AXIS_LEFT_Y] = leftStickY;
    
    // Buttons
    profile.buttonMappings[GAMEPAD_BUTTON_A] = KeyMapping(Qt::Key_Return, 0, "Enter");
    profile.buttonMappings[GAMEPAD_BUTTON_B] = KeyMapping(Qt::Key_Control, 0, "Ctrl");
    profile.buttonMappings[GAMEPAD_BUTTON_X] = KeyMapping(Qt::Key_Alt, 0, "Alt");
    profile.buttonMappings[GAMEPAD_BUTTON_Y] = KeyMapping(Qt::Key_Escape, 0, "Esc");
    
    return profile;
}

KeyboardMappingProfile KeyboardMappingProfile::createNumpadPreset()
{
    KeyboardMappingProfile profile("Numpad");
    profile.description = "Numpad layout for fighting games";
    
    // Right stick: Numpad 8246
    AxisKeyMapping rightStickX;
    rightStickX.negative = KeyMapping(Qt::Key_4, 0, "Numpad 4");
    rightStickX.positive = KeyMapping(Qt::Key_6, 0, "Numpad 6");
    rightStickX.threshold = 0.3f;
    profile.axisMappings[GAMEPAD_AXIS_RIGHT_X] = rightStickX;
    
    AxisKeyMapping rightStickY;
    rightStickY.negative = KeyMapping(Qt::Key_8, 0, "Numpad 8");
    rightStickY.positive = KeyMapping(Qt::Key_2, 0, "Numpad 2");
    rightStickY.threshold = 0.3f;
    profile.axisMappings[GAMEPAD_AXIS_RIGHT_Y] = rightStickY;
    
    // Buttons: Numpad numbers
    profile.buttonMappings[GAMEPAD_BUTTON_A] = KeyMapping(Qt::Key_1, 0, "Numpad 1");
    profile.buttonMappings[GAMEPAD_BUTTON_B] = KeyMapping(Qt::Key_3, 0, "Numpad 3");
    profile.buttonMappings[GAMEPAD_BUTTON_X] = KeyMapping(Qt::Key_7, 0, "Numpad 7");
    profile.buttonMappings[GAMEPAD_BUTTON_Y] = KeyMapping(Qt::Key_9, 0, "Numpad 9");
    profile.buttonMappings[GAMEPAD_BUTTON_L1] = KeyMapping(Qt::Key_5, 0, "Numpad 5");
    profile.buttonMappings[GAMEPAD_BUTTON_R1] = KeyMapping(Qt::Key_0, 0, "Numpad 0");
    
    return profile;
}

DECKGAMEPAD_END_NAMESPACE
