// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "treelandgamepaddevice.h"
#include "treelandgamepadclient.h"
#include "treelandgamepadmanager.h"

#include <wayland-util.h>
#include "treeland-gamepad-v1-client-protocol.h"

namespace TreelandGamepad {

struct TreelandGamepadDevice::Private
{
    TreelandGamepadClient *client = nullptr;
    treeland_gamepad_v1 *gamepad = nullptr;
    
    int deviceId = -1;
    QString name;
    QString guid;
    bool connected = false;
    
    // Current state
    QHash<GamepadButton, bool> buttonStates;
    QHash<GamepadAxis, double> axisValues;
    int hatDirection = deckshell::deckgamepad::GAMEPAD_HAT_CENTER;
    
    // Convert fixed-point to double
    static double fixedToDouble(wl_fixed_t value) {
        return wl_fixed_to_double(value);
    }
    
    // Convert double to fixed-point
    static wl_fixed_t doubleToFixed(double value) {
        return wl_fixed_from_double(value);
    }
};

TreelandGamepadDevice::TreelandGamepadDevice(TreelandGamepadClient *client, int deviceId, const QString &name)
    : QObject(client)
    , d(std::make_unique<Private>())
{
    d->client = client;
    d->deviceId = deviceId;
    d->name = name;
    d->connected = true;
    
    // Initialize axis values to 0
    for (int i = 0; i < deckshell::deckgamepad::GAMEPAD_AXIS_MAX; ++i) {
        d->axisValues[static_cast<GamepadAxis>(i)] = 0.0;
    }
}

TreelandGamepadDevice::~TreelandGamepadDevice()
{
    if (d->gamepad) {
        treeland_gamepad_v1_release(d->gamepad);
    }
}

int TreelandGamepadDevice::deviceId() const
{
    return d->deviceId;
}

QString TreelandGamepadDevice::name() const
{
    return d->name;
}

QString TreelandGamepadDevice::guid() const
{
    return d->guid;
}

bool TreelandGamepadDevice::isConnected() const
{
    return d->connected;
}

void TreelandGamepadDevice::setVibration(double weakMagnitude, double strongMagnitude, int durationMs)
{
    if (!d->gamepad) {
        return;
    }
    
    // Clamp values to [0.0, 1.0]
    weakMagnitude = qBound(0.0, weakMagnitude, 1.0);
    strongMagnitude = qBound(0.0, strongMagnitude, 1.0);
    durationMs = qMax(0, durationMs);
    
    treeland_gamepad_v1_set_vibration(
        d->gamepad,
        Private::doubleToFixed(weakMagnitude),
        Private::doubleToFixed(strongMagnitude),
        durationMs
    );
}

void TreelandGamepadDevice::stopVibration()
{
    if (!d->gamepad) {
        return;
    }
    
    treeland_gamepad_v1_stop_vibration(d->gamepad);
}

void TreelandGamepadDevice::setAxisDeadzone(uint32_t axis, double deadzone)
{
    if (!d->gamepad) {
        return;
    }

    if (wl_proxy_get_version(reinterpret_cast<wl_proxy *>(d->gamepad)) < 2) {
        return;
    }

    deadzone = qBound(0.0, deadzone, 1.0);
    treeland_gamepad_v1_set_axis_deadzone(d->gamepad, axis, Private::doubleToFixed(deadzone));
}

bool TreelandGamepadDevice::isButtonPressed(GamepadButton button) const
{
    return d->buttonStates.value(button, false);
}

double TreelandGamepadDevice::axisValue(GamepadAxis axis) const
{
    return d->axisValues.value(axis, 0.0);
}

int TreelandGamepadDevice::hatDirection() const
{
    return d->hatDirection;
}

void TreelandGamepadDevice::handleButton(uint32_t time, uint32_t button, uint32_t state)
{
    if (button >= static_cast<uint32_t>(deckshell::deckgamepad::GAMEPAD_BUTTON_MAX)) {
        return;
    }
    
    GamepadButton mappedButton = static_cast<GamepadButton>(button);
    bool pressed = (state != 0);
    bool wasPressed = d->buttonStates.value(mappedButton, false);
    
    d->buttonStates[mappedButton] = pressed;
    
    // Emit raw event
    DeckGamepadButtonEvent event;
    event.time_msec = time;
    event.button = button;
    event.pressed = pressed;
    Q_EMIT buttonEvent(event);
    
    // Emit convenience signals
    if (pressed != wasPressed) {
        Q_EMIT buttonChanged(mappedButton, pressed);
        
        if (pressed) {
            Q_EMIT buttonPressed(mappedButton);
        } else {
            Q_EMIT buttonReleased(mappedButton);
        }
    }
}

void TreelandGamepadDevice::handleAxis(uint32_t time, uint32_t axis, double value)
{
    if (axis >= static_cast<uint32_t>(deckshell::deckgamepad::GAMEPAD_AXIS_MAX)) {
        return;
    }
    
    // Clamp value to [-1.0, 1.0]
    value = qBound(-1.0, value, 1.0);
    
    GamepadAxis mappedAxis = static_cast<GamepadAxis>(axis);
    double oldValue = d->axisValues.value(mappedAxis, 0.0);
    d->axisValues[mappedAxis] = value;
    
    // Emit raw event
    DeckGamepadAxisEvent event;
    event.time_msec = time;
    event.axis = axis;
    event.value = value;
    Q_EMIT axisEvent(event);
    
    // Emit convenience signal if value changed
    if (!qFuzzyCompare(value, oldValue)) {
        Q_EMIT axisChanged(mappedAxis, value);
    }
}

void TreelandGamepadDevice::handleHat(uint32_t time, uint32_t hat, int32_t value)
{
    Q_UNUSED(hat) // Usually only one hat/D-pad
    
    int oldDirection = d->hatDirection;
    d->hatDirection = value;
    
    // Emit raw event
    DeckGamepadHatEvent event;
    event.time_msec = time;
    event.hat = hat;
    event.value = value;
    Q_EMIT hatEvent(event);
    
    // Emit convenience signal if direction changed
    if (value != oldDirection) {
        Q_EMIT hatChanged(value);
    }
}

void TreelandGamepadDevice::setConnected(bool connected)
{
    if (d->connected != connected) {
        d->connected = connected;
        Q_EMIT connectedChanged(connected);
    }
}

void TreelandGamepadDevice::setGamepadHandle(treeland_gamepad_v1 *gamepad)
{
    d->gamepad = gamepad;
}

void TreelandGamepadDevice::setGuid(const QString &guid)
{
    if (d->guid == guid) {
        return;
    }
    d->guid = guid;
    Q_EMIT guidChanged(d->guid);
}

void TreelandGamepadDevice::handleAxisDeadzoneApplied(uint32_t axis, double deadzone)
{
    Q_EMIT axisDeadzoneApplied(axis, deadzone);
}

void TreelandGamepadDevice::handleAxisDeadzoneFailed(uint32_t axis, uint32_t error)
{
    Q_EMIT axisDeadzoneFailed(axis, error);
}

} // namespace TreelandGamepad
