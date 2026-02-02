// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include "treelandgamepadglobal.h"
#include <QObject>
#include <memory>
#include <cstdint>

struct treeland_gamepad_v1;

namespace TreelandGamepad {

class TreelandGamepadClient;

class TREELAND_GAMEPAD_EXPORT TreelandGamepadDevice : public QObject
{
    Q_OBJECT
    Q_PROPERTY(int deviceId READ deviceId CONSTANT)
    Q_PROPERTY(QString name READ name CONSTANT)
    Q_PROPERTY(QString guid READ guid NOTIFY guidChanged)
    Q_PROPERTY(bool connected READ isConnected NOTIFY connectedChanged)

public:
    ~TreelandGamepadDevice();

    // Properties
    int deviceId() const;
    QString name() const;
    QString guid() const;
    bool isConnected() const;

    // Vibration control
    void setVibration(double weakMagnitude, double strongMagnitude, int durationMs = 0);
    void stopVibration();

    // Global tuning (compositor-side; requires authorization)
    void setAxisDeadzone(uint32_t axis, double deadzone);

    // Button state queries
    bool isButtonPressed(GamepadButton button) const;
    double axisValue(GamepadAxis axis) const;
    int hatDirection() const;

Q_SIGNALS:
    void connectedChanged(bool connected);
    void guidChanged(const QString &guid);
    
    // Button events
    void buttonPressed(GamepadButton button);
    void buttonReleased(GamepadButton button);
    void buttonChanged(GamepadButton button, bool pressed);
    
    // Axis events
    void axisChanged(GamepadAxis axis, double value);
    
    // Hat events
    void hatChanged(int direction);
    
    // Raw events (with timestamps)
    void buttonEvent(DeckGamepadButtonEvent event);
    void axisEvent(DeckGamepadAxisEvent event);
    void hatEvent(DeckGamepadHatEvent event);

    // Tuning results (protocol v2)
    void axisDeadzoneApplied(uint32_t axis, double deadzone);
    void axisDeadzoneFailed(uint32_t axis, uint32_t error);

private:
    explicit TreelandGamepadDevice(TreelandGamepadClient *client, int deviceId, const QString &name);
    
    void handleButton(uint32_t time, uint32_t button, uint32_t state);
    void handleAxis(uint32_t time, uint32_t axis, double value);
    void handleHat(uint32_t time, uint32_t hat, int32_t value);
    void setConnected(bool connected);
    void setGamepadHandle(struct treeland_gamepad_v1 *gamepad);
    void setGuid(const QString &guid);
    void handleAxisDeadzoneApplied(uint32_t axis, double deadzone);
    void handleAxisDeadzoneFailed(uint32_t axis, uint32_t error);

    friend class TreelandGamepadClient;
    friend class TreelandGamepadManager;

    struct Private;
    std::unique_ptr<Private> d;
};

} // namespace TreelandGamepad
