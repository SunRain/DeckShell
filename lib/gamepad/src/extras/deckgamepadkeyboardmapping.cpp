// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/extras/deckgamepadkeyboardmapping.h>

#include <QDebug>
#include <QFile>
#include <QJsonArray>
#include <QJsonDocument>

#include <Qt>

DECKGAMEPAD_BEGIN_NAMESPACE

QJsonObject KeyMapping::toJson() const
{
    QJsonObject obj;
    obj["key"] = qtKey;
    obj["modifiers"] = modifiers;
    obj["description"] = description;
    return obj;
}

KeyMapping KeyMapping::fromJson(const QJsonObject &obj)
{
    KeyMapping mapping;
    mapping.qtKey = obj["key"].toInt();
    mapping.modifiers = obj["modifiers"].toInt();
    mapping.description = obj["description"].toString();
    return mapping;
}

QJsonObject AxisKeyMapping::toJson() const
{
    QJsonObject obj;
    obj["negative"] = negative.toJson();
    obj["positive"] = positive.toJson();
    obj["threshold"] = threshold;
    return obj;
}

AxisKeyMapping AxisKeyMapping::fromJson(const QJsonObject &obj)
{
    AxisKeyMapping mapping;
    mapping.negative = KeyMapping::fromJson(obj["negative"].toObject());
    mapping.positive = KeyMapping::fromJson(obj["positive"].toObject());
    mapping.threshold = static_cast<float>(obj["threshold"].toDouble(0.5));
    return mapping;
}

DeckGamepadKeyboardMappingManager::DeckGamepadKeyboardMappingManager(QObject *parent)
    : QObject(parent)
    , m_enabled(false)
{
    qDebug() << "DeckGamepadKeyboardMappingManager created";
}

DeckGamepadKeyboardMappingManager::~DeckGamepadKeyboardMappingManager()
{
    qDebug() << "DeckGamepadKeyboardMappingManager destroyed";
}

void DeckGamepadKeyboardMappingManager::setEnabled(bool enabled)
{
    if (m_enabled == enabled) {
        return;
    }

    m_enabled = enabled;

    if (!enabled) {
        m_axisStates.clear();
    }

    emit enabledChanged(enabled);
    qDebug() << "Keyboard mapping" << (enabled ? "enabled" : "disabled");
}

void DeckGamepadKeyboardMappingManager::setButtonMapping(GamepadButton button, const KeyMapping &key)
{
    m_buttonMappings[button] = key;
    emit mappingChanged();

    qDebug() << "Button" << buttonToString(button) << "mapped to key" << key.qtKey;
}

KeyMapping DeckGamepadKeyboardMappingManager::buttonMapping(GamepadButton button) const
{
    return m_buttonMappings.value(button);
}

void DeckGamepadKeyboardMappingManager::clearButtonMapping(GamepadButton button)
{
    m_buttonMappings.remove(button);
    emit mappingChanged();
}

void DeckGamepadKeyboardMappingManager::setAxisMapping(GamepadAxis axis, const AxisKeyMapping &keys)
{
    m_axisMappings[axis] = keys;
    emit mappingChanged();

    qDebug() << "Axis" << axisToString(axis) << "mapped to keys" << keys.negative.qtKey << "/"
             << keys.positive.qtKey;
}

AxisKeyMapping DeckGamepadKeyboardMappingManager::axisMapping(GamepadAxis axis) const
{
    return m_axisMappings.value(axis);
}

void DeckGamepadKeyboardMappingManager::clearAxisMapping(GamepadAxis axis)
{
    m_axisMappings.remove(axis);
    m_axisStates.remove(axis);
    emit mappingChanged();
}

void DeckGamepadKeyboardMappingManager::processButton(GamepadButton button, bool pressed)
{
    if (!m_enabled) {
        return;
    }

    KeyMapping mapping = m_buttonMappings.value(button);
    if (!mapping.isValid()) {
        return;
    }

    emitKeyEvent(mapping, pressed);
}

void DeckGamepadKeyboardMappingManager::processAxis(GamepadAxis axis, float value)
{
    if (!m_enabled) {
        return;
    }

    AxisKeyMapping mapping = m_axisMappings.value(axis);
    if (!mapping.negative.isValid() && !mapping.positive.isValid()) {
        return;
    }

    AxisState &state = m_axisStates[axis];

    bool shouldNegative = value < -mapping.threshold;
    bool shouldPositive = value > mapping.threshold;

    if (shouldNegative != state.negativeActive) {
        state.negativeActive = shouldNegative;
        if (mapping.negative.isValid()) {
            emitKeyEvent(mapping.negative, shouldNegative);
        }
    }

    if (shouldPositive != state.positiveActive) {
        state.positiveActive = shouldPositive;
        if (mapping.positive.isValid()) {
            emitKeyEvent(mapping.positive, shouldPositive);
        }
    }
}

void DeckGamepadKeyboardMappingManager::applyWASDPreset()
{
    qDebug() << "Applying WASD preset";

    clearAll();

    AxisKeyMapping leftStick;
    leftStick.negative = KeyMapping(Qt::Key_A, 0, "A");
    leftStick.positive = KeyMapping(Qt::Key_D, 0, "D");
    leftStick.threshold = 0.3f;
    setAxisMapping(GAMEPAD_AXIS_LEFT_X, leftStick);
    
    AxisKeyMapping leftStickY;
    leftStickY.negative = KeyMapping(Qt::Key_W, 0, "W");
    leftStickY.positive = KeyMapping(Qt::Key_S, 0, "S");
    leftStickY.threshold = 0.3f;
    setAxisMapping(GAMEPAD_AXIS_LEFT_Y, leftStickY);

    setButtonMapping(GAMEPAD_BUTTON_A, KeyMapping(Qt::Key_Space, 0, "Space"));
    setButtonMapping(GAMEPAD_BUTTON_B, KeyMapping(Qt::Key_Shift, 0, "Shift"));
    setButtonMapping(GAMEPAD_BUTTON_X, KeyMapping(Qt::Key_E, 0, "E"));
    setButtonMapping(GAMEPAD_BUTTON_Y, KeyMapping(Qt::Key_Q, 0, "Q"));

    setButtonMapping(GAMEPAD_BUTTON_L1, KeyMapping(Qt::Key_Tab, 0, "Tab"));
    setButtonMapping(GAMEPAD_BUTTON_R1, KeyMapping(Qt::Key_R, 0, "R"));

    emit mappingChanged();
}

void DeckGamepadKeyboardMappingManager::applyArrowPreset()
{
    qDebug() << "Applying Arrow Keys preset";

    clearAll();

    setButtonMapping(GAMEPAD_BUTTON_DPAD_UP, KeyMapping(Qt::Key_Up, 0, "Up"));
    setButtonMapping(GAMEPAD_BUTTON_DPAD_DOWN, KeyMapping(Qt::Key_Down, 0, "Down"));
    setButtonMapping(GAMEPAD_BUTTON_DPAD_LEFT, KeyMapping(Qt::Key_Left, 0, "Left"));
    setButtonMapping(GAMEPAD_BUTTON_DPAD_RIGHT, KeyMapping(Qt::Key_Right, 0, "Right"));

    setButtonMapping(GAMEPAD_BUTTON_A, KeyMapping(Qt::Key_Return, 0, "Enter"));
    setButtonMapping(GAMEPAD_BUTTON_B, KeyMapping(Qt::Key_Back, 0, "Back"));
    setButtonMapping(GAMEPAD_BUTTON_X, KeyMapping(Qt::Key_Alt, 0, "Alt"));
    setButtonMapping(GAMEPAD_BUTTON_Y, KeyMapping(Qt::Key_Escape, 0, "Esc"));

    emit mappingChanged();
}

void DeckGamepadKeyboardMappingManager::applyNumpadPreset()
{
    qDebug() << "Applying Numpad preset";

    clearAll();

    AxisKeyMapping rightStickX;
    rightStickX.negative = KeyMapping(Qt::Key_4, 0, "Numpad 4");
    rightStickX.positive = KeyMapping(Qt::Key_6, 0, "Numpad 6");
    rightStickX.threshold = 0.3f;
    setAxisMapping(GAMEPAD_AXIS_RIGHT_X, rightStickX);
    
    AxisKeyMapping rightStickY;
    rightStickY.negative = KeyMapping(Qt::Key_8, 0, "Numpad 8");
    rightStickY.positive = KeyMapping(Qt::Key_2, 0, "Numpad 2");
    rightStickY.threshold = 0.3f;
    setAxisMapping(GAMEPAD_AXIS_RIGHT_Y, rightStickY);

    setButtonMapping(GAMEPAD_BUTTON_A, KeyMapping(Qt::Key_0, 0, "Numpad 0"));
    setButtonMapping(GAMEPAD_BUTTON_B, KeyMapping(Qt::Key_1, 0, "Numpad 1"));
    setButtonMapping(GAMEPAD_BUTTON_X, KeyMapping(Qt::Key_3, 0, "Numpad 3"));
    setButtonMapping(GAMEPAD_BUTTON_Y, KeyMapping(Qt::Key_5, 0, "Numpad 5"));

    emit mappingChanged();
}

void DeckGamepadKeyboardMappingManager::clearAll()
{
    m_buttonMappings.clear();
    m_axisMappings.clear();
    m_axisStates.clear();
    emit mappingChanged();

    qDebug() << "All keyboard mappings cleared";
}

QJsonObject DeckGamepadKeyboardMappingManager::toJson() const
{
    QJsonObject root;
    root["enabled"] = m_enabled;

    QJsonArray buttons;
    for (auto it = m_buttonMappings.constBegin(); it != m_buttonMappings.constEnd(); ++it) {
        QJsonObject entry;
        entry["button"] = static_cast<int>(it.key());
        entry["mapping"] = it.value().toJson();
        buttons.append(entry);
    }
    root["buttons"] = buttons;

    QJsonArray axes;
    for (auto it = m_axisMappings.constBegin(); it != m_axisMappings.constEnd(); ++it) {
        QJsonObject entry;
        entry["axis"] = static_cast<int>(it.key());
        entry["mapping"] = it.value().toJson();
        axes.append(entry);
    }
    root["axes"] = axes;

    return root;
}

bool DeckGamepadKeyboardMappingManager::fromJson(const QJsonObject &obj)
{
    clearAll();

    m_enabled = obj["enabled"].toBool(false);

    QJsonArray buttons = obj["buttons"].toArray();
    for (const QJsonValue &val : buttons) {
        QJsonObject entry = val.toObject();
        GamepadButton button = static_cast<GamepadButton>(entry["button"].toInt());
        KeyMapping mapping = KeyMapping::fromJson(entry["mapping"].toObject());
        m_buttonMappings[button] = mapping;
    }

    QJsonArray axes = obj["axes"].toArray();
    for (const QJsonValue &val : axes) {
        QJsonObject entry = val.toObject();
        GamepadAxis axis = static_cast<GamepadAxis>(entry["axis"].toInt());
        AxisKeyMapping mapping = AxisKeyMapping::fromJson(entry["mapping"].toObject());
        m_axisMappings[axis] = mapping;
    }

    emit mappingChanged();
    return true;
}

bool DeckGamepadKeyboardMappingManager::saveToFile(const QString &path) const
{
    QFile file(path);
    if (!file.open(QIODevice::WriteOnly)) {
        qWarning() << "Failed to open file for writing:" << path;
        return false;
    }

    QJsonDocument doc(toJson());
    file.write(doc.toJson(QJsonDocument::Indented));
    file.close();

    qDebug() << "Keyboard mapping saved to:" << path;
    return true;
}

bool DeckGamepadKeyboardMappingManager::loadFromFile(const QString &path)
{
    QFile file(path);
    if (!file.open(QIODevice::ReadOnly)) {
        qWarning() << "Failed to open file for reading:" << path;
        return false;
    }

    QByteArray data = file.readAll();
    file.close();

    QJsonDocument doc = QJsonDocument::fromJson(data);
    if (!doc.isObject()) {
        qWarning() << "Invalid JSON format in:" << path;
        return false;
    }

    fromJson(doc.object());
    qDebug() << "Keyboard mapping loaded from:" << path;
    return true;
}

void DeckGamepadKeyboardMappingManager::emitKeyEvent(const KeyMapping &mapping, bool pressed)
{
    emit keyEvent(mapping.qtKey, mapping.modifiers, pressed);

    qDebug() << "Key event:" << mapping.description << (pressed ? "pressed" : "released");
}

QString DeckGamepadKeyboardMappingManager::buttonToString(GamepadButton button) const
{
    switch (button) {
        case GAMEPAD_BUTTON_A: return "A";
        case GAMEPAD_BUTTON_B: return "B";
        case GAMEPAD_BUTTON_X: return "X";
        case GAMEPAD_BUTTON_Y: return "Y";
        case GAMEPAD_BUTTON_SELECT: return "Back";
        case GAMEPAD_BUTTON_GUIDE: return "Guide";
        case GAMEPAD_BUTTON_START: return "Start";
        case GAMEPAD_BUTTON_L3: return "LeftStick";
        case GAMEPAD_BUTTON_R3: return "RightStick";
        case GAMEPAD_BUTTON_L1: return "LeftShoulder";
        case GAMEPAD_BUTTON_R1: return "RightShoulder";
        case GAMEPAD_BUTTON_DPAD_UP: return "DPadUp";
        case GAMEPAD_BUTTON_DPAD_DOWN: return "DPadDown";
        case GAMEPAD_BUTTON_DPAD_LEFT: return "DPadLeft";
        case GAMEPAD_BUTTON_DPAD_RIGHT: return "DPadRight";
        default: return QString("Button%1").arg(static_cast<int>(button));
    }
}

QString DeckGamepadKeyboardMappingManager::axisToString(GamepadAxis axis) const
{
    switch (axis) {
        case GAMEPAD_AXIS_LEFT_X: return "LeftX";
        case GAMEPAD_AXIS_LEFT_Y: return "LeftY";
        case GAMEPAD_AXIS_RIGHT_X: return "RightX";
        case GAMEPAD_AXIS_RIGHT_Y: return "RightY";
        case GAMEPAD_AXIS_TRIGGER_LEFT: return "LeftTrigger";
        case GAMEPAD_AXIS_TRIGGER_RIGHT: return "RightTrigger";
        default: return QString("Axis%1").arg(static_cast<int>(axis));
    }
}

DECKGAMEPAD_END_NAMESPACE
