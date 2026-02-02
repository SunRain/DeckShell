// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "gamepad.h"

#include "gamepadmanager.h"

#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtCore/QDateTime>
#include <QtQml/QQmlEngine>

using deckshell::deckgamepad::DeckGamepadService;
using deckshell::deckgamepad::GamepadAxis;
using deckshell::deckgamepad::GamepadButton;

Gamepad::Gamepad(QObject *parent)
    : QObject(parent)
{
    m_coalesceTimer.setSingleShot(true);
    m_coalesceTimer.setInterval(m_coalesceIntervalMs);
    connect(&m_coalesceTimer, &QTimer::timeout, this, &Gamepad::flushPendingChanges);
}

Gamepad::~Gamepad() = default;

void Gamepad::classBegin()
{
}

void Gamepad::componentComplete()
{
    ensureManagerResolved();
}

int Gamepad::deviceId() const
{
    return m_deviceId;
}

void Gamepad::setDeviceId(int deviceId)
{
    ensureManagerResolved();
    if (m_deviceId == deviceId) {
        return;
    }
    m_deviceId = deviceId;

    resetState();
    syncDeviceInfo();

    Q_EMIT deviceIdChanged();
}

bool Gamepad::connected() const
{
    return m_connected;
}

QString Gamepad::name() const
{
    return m_name;
}

int Gamepad::coalesceIntervalMs() const
{
    return m_coalesceIntervalMs;
}

void Gamepad::setCoalesceIntervalMs(int intervalMs)
{
    if (m_coalesceIntervalMs == intervalMs) {
        return;
    }

    m_coalesceIntervalMs = intervalMs;

    if (m_coalesceIntervalMs > 0) {
        m_coalesceTimer.setInterval(m_coalesceIntervalMs);
    } else {
        m_coalesceTimer.stop();
        flushPendingChanges();
    }

    Q_EMIT coalesceIntervalMsChanged();
}

quint64 Gamepad::axisRawEventCount() const
{
    return m_axisRawEventCount;
}

quint64 Gamepad::axisNotifyCount() const
{
    return m_axisNotifyCount;
}

quint64 Gamepad::axisDroppedEventCount() const
{
    return (m_axisRawEventCount > m_axisNotifyCount) ? (m_axisRawEventCount - m_axisNotifyCount) : 0;
}

quint64 Gamepad::hatRawEventCount() const
{
    return m_hatRawEventCount;
}

quint64 Gamepad::hatNotifyCount() const
{
    return m_hatNotifyCount;
}

quint64 Gamepad::hatDroppedEventCount() const
{
    return (m_hatRawEventCount > m_hatNotifyCount) ? (m_hatRawEventCount - m_hatNotifyCount) : 0;
}

int Gamepad::lastCoalesceLatencyMs() const
{
    return m_lastCoalesceLatencyMs;
}

int Gamepad::hatDirection() const
{
    return m_hatDirectionByHat[0];
}

int Gamepad::hat1Direction() const
{
    return m_hatDirectionByHat[1];
}

int Gamepad::hat2Direction() const
{
    return m_hatDirectionByHat[2];
}

int Gamepad::hat3Direction() const
{
    return m_hatDirectionByHat[3];
}

bool Gamepad::buttonA() const { return buttonState(deckshell::deckgamepad::GAMEPAD_BUTTON_A); }
bool Gamepad::buttonB() const { return buttonState(deckshell::deckgamepad::GAMEPAD_BUTTON_B); }
bool Gamepad::buttonX() const { return buttonState(deckshell::deckgamepad::GAMEPAD_BUTTON_X); }
bool Gamepad::buttonY() const { return buttonState(deckshell::deckgamepad::GAMEPAD_BUTTON_Y); }
bool Gamepad::buttonL1() const { return buttonState(deckshell::deckgamepad::GAMEPAD_BUTTON_L1); }
bool Gamepad::buttonR1() const { return buttonState(deckshell::deckgamepad::GAMEPAD_BUTTON_R1); }
bool Gamepad::buttonL2() const { return buttonState(deckshell::deckgamepad::GAMEPAD_BUTTON_L2); }
bool Gamepad::buttonR2() const { return buttonState(deckshell::deckgamepad::GAMEPAD_BUTTON_R2); }
bool Gamepad::buttonSelect() const { return buttonState(deckshell::deckgamepad::GAMEPAD_BUTTON_SELECT); }
bool Gamepad::buttonStart() const { return buttonState(deckshell::deckgamepad::GAMEPAD_BUTTON_START); }
bool Gamepad::buttonL3() const { return buttonState(deckshell::deckgamepad::GAMEPAD_BUTTON_L3); }
bool Gamepad::buttonR3() const { return buttonState(deckshell::deckgamepad::GAMEPAD_BUTTON_R3); }
bool Gamepad::buttonGuide() const { return buttonState(deckshell::deckgamepad::GAMEPAD_BUTTON_GUIDE); }
bool Gamepad::buttonDpadUp() const { return buttonState(deckshell::deckgamepad::GAMEPAD_BUTTON_DPAD_UP); }
bool Gamepad::buttonDpadDown() const { return buttonState(deckshell::deckgamepad::GAMEPAD_BUTTON_DPAD_DOWN); }
bool Gamepad::buttonDpadLeft() const { return buttonState(deckshell::deckgamepad::GAMEPAD_BUTTON_DPAD_LEFT); }
bool Gamepad::buttonDpadRight() const { return buttonState(deckshell::deckgamepad::GAMEPAD_BUTTON_DPAD_RIGHT); }

double Gamepad::axisLeftX() const { return axisValue(deckshell::deckgamepad::GAMEPAD_AXIS_LEFT_X); }
double Gamepad::axisLeftY() const { return axisValue(deckshell::deckgamepad::GAMEPAD_AXIS_LEFT_Y); }
double Gamepad::axisRightX() const { return axisValue(deckshell::deckgamepad::GAMEPAD_AXIS_RIGHT_X); }
double Gamepad::axisRightY() const { return axisValue(deckshell::deckgamepad::GAMEPAD_AXIS_RIGHT_Y); }
double Gamepad::axisTriggerLeft() const { return axisValue(deckshell::deckgamepad::GAMEPAD_AXIS_TRIGGER_LEFT); }
double Gamepad::axisTriggerRight() const { return axisValue(deckshell::deckgamepad::GAMEPAD_AXIS_TRIGGER_RIGHT); }

void Gamepad::handleDeviceConnected(int deviceId)
{
    if (deviceId != m_deviceId) {
        return;
    }
    if (!m_connected) {
        m_connected = true;
        Q_EMIT connectedChanged();
    }

    syncDeviceInfo();
}

void Gamepad::handleDeviceDisconnected(int deviceId)
{
    if (deviceId != m_deviceId) {
        return;
    }
    if (m_connected) {
        m_connected = false;
        Q_EMIT connectedChanged();
    }

    resetState();
}

void Gamepad::handleButtonEvent(deckshell::deckgamepad::DeckGamepadButtonEvent event)
{
    const int button = static_cast<int>(event.button);
    const bool pressed = event.pressed;

    Q_EMIT buttonEvent(button, pressed, static_cast<int>(event.time_msec));

    if (button < 0 || button >= deckshell::deckgamepad::GAMEPAD_BUTTON_MAX) {
        return;
    }

    const auto enumButton = static_cast<GamepadButton>(button);
    if (buttonState(enumButton) == pressed) {
        return;
    }

    setButtonState(enumButton, pressed);
}

void Gamepad::handleAxisEvent(deckshell::deckgamepad::DeckGamepadAxisEvent event)
{
    const int axis = static_cast<int>(event.axis);
    Q_EMIT axisEvent(axis, event.value, static_cast<int>(event.time_msec));

    if (axis < 0 || axis >= deckshell::deckgamepad::GAMEPAD_AXIS_MAX) {
        return;
    }

    const auto enumAxis = static_cast<GamepadAxis>(axis);
    setAxisValue(enumAxis, event.value);

    m_axisRawEventCount++;

    if (m_coalesceIntervalMs <= 0) {
        emitAxisNotify(enumAxis);
        Q_EMIT axisChanged(axis, axisValue(enumAxis));
        m_axisNotifyCount++;
        Q_EMIT statsChanged();
        return;
    }

    m_pendingAxisMask |= (1u << static_cast<uint32_t>(axis));

    if (!m_coalesceTimer.isActive()) {
        m_pendingCoalesceStartWallclockMs = QDateTime::currentMSecsSinceEpoch();
        m_coalesceTimer.start();
    }
}

void Gamepad::handleHatEvent(deckshell::deckgamepad::DeckGamepadHatEvent event)
{
    const int hat = static_cast<int>(event.hat);
    const int value = event.value;

    Q_EMIT hatEvent(hat, value, static_cast<int>(event.time_msec));

    m_hatRawEventCount++;

    if (hat < 0 || hat >= 4) {
        return;
    }

    if (m_coalesceIntervalMs <= 0) {
        if (m_hatDirectionByHat[static_cast<size_t>(hat)] == value) {
            return;
        }

        m_hatDirectionByHat[static_cast<size_t>(hat)] = value;
        switch (hat) {
        case 0:
            Q_EMIT hatDirectionChanged();
            break;
        case 1:
            Q_EMIT hat1DirectionChanged();
            break;
        case 2:
            Q_EMIT hat2DirectionChanged();
            break;
        case 3:
            Q_EMIT hat3DirectionChanged();
            break;
        default:
            break;
        }

        Q_EMIT hatChanged(hat, value);

        if (hat == 0) {
            // Derive virtual DPad buttons from hat0 mask.
            setButtonState(deckshell::deckgamepad::GAMEPAD_BUTTON_DPAD_UP,
                           (value & deckshell::deckgamepad::GAMEPAD_HAT_UP) != 0);
            setButtonState(deckshell::deckgamepad::GAMEPAD_BUTTON_DPAD_DOWN,
                           (value & deckshell::deckgamepad::GAMEPAD_HAT_DOWN) != 0);
            setButtonState(deckshell::deckgamepad::GAMEPAD_BUTTON_DPAD_LEFT,
                           (value & deckshell::deckgamepad::GAMEPAD_HAT_LEFT) != 0);
            setButtonState(deckshell::deckgamepad::GAMEPAD_BUTTON_DPAD_RIGHT,
                           (value & deckshell::deckgamepad::GAMEPAD_HAT_RIGHT) != 0);
        }

        m_hatNotifyCount++;
        Q_EMIT statsChanged();
        return;
    }

    m_pendingHatMask |= static_cast<uint8_t>(1u << static_cast<uint32_t>(hat));
    m_pendingHatDirectionByHat[static_cast<size_t>(hat)] = value;

    if (!m_coalesceTimer.isActive()) {
        m_pendingCoalesceStartWallclockMs = QDateTime::currentMSecsSinceEpoch();
        m_coalesceTimer.start();
    }
}

void Gamepad::flushPendingChanges()
{
    const uint32_t pendingAxis = m_pendingAxisMask;
    const uint8_t pendingHats = m_pendingHatMask;
    if (pendingAxis == 0 && pendingHats == 0) {
        return;
    }

    const qint64 nowMs = QDateTime::currentMSecsSinceEpoch();
    if (m_pendingCoalesceStartWallclockMs >= 0) {
        m_lastCoalesceLatencyMs = static_cast<int>(qMax<qint64>(0, nowMs - m_pendingCoalesceStartWallclockMs));
    }
    m_pendingCoalesceStartWallclockMs = -1;

    if (pendingHats != 0) {
        m_pendingHatMask = 0;
        for (int hat = 0; hat < 4; ++hat) {
            if (!(pendingHats & static_cast<uint8_t>(1u << static_cast<uint32_t>(hat)))) {
                continue;
            }

            const int value = m_pendingHatDirectionByHat[static_cast<size_t>(hat)];
            if (m_hatDirectionByHat[static_cast<size_t>(hat)] == value) {
                continue;
            }

            m_hatDirectionByHat[static_cast<size_t>(hat)] = value;
            switch (hat) {
            case 0:
                Q_EMIT hatDirectionChanged();
                break;
            case 1:
                Q_EMIT hat1DirectionChanged();
                break;
            case 2:
                Q_EMIT hat2DirectionChanged();
                break;
            case 3:
                Q_EMIT hat3DirectionChanged();
                break;
            default:
                break;
            }

            Q_EMIT hatChanged(hat, value);

            if (hat == 0) {
                // Derive virtual DPad buttons from hat0 mask.
                setButtonState(deckshell::deckgamepad::GAMEPAD_BUTTON_DPAD_UP,
                               (value & deckshell::deckgamepad::GAMEPAD_HAT_UP) != 0);
                setButtonState(deckshell::deckgamepad::GAMEPAD_BUTTON_DPAD_DOWN,
                               (value & deckshell::deckgamepad::GAMEPAD_HAT_DOWN) != 0);
                setButtonState(deckshell::deckgamepad::GAMEPAD_BUTTON_DPAD_LEFT,
                               (value & deckshell::deckgamepad::GAMEPAD_HAT_LEFT) != 0);
                setButtonState(deckshell::deckgamepad::GAMEPAD_BUTTON_DPAD_RIGHT,
                               (value & deckshell::deckgamepad::GAMEPAD_HAT_RIGHT) != 0);
            }

            m_hatNotifyCount++;
        }
    }

    m_pendingAxisMask = 0;
    for (int axis = 0; axis < deckshell::deckgamepad::GAMEPAD_AXIS_MAX; ++axis) {
        if (!(pendingAxis & (1u << static_cast<uint32_t>(axis)))) {
            continue;
        }

        const auto enumAxis = static_cast<GamepadAxis>(axis);
        emitAxisNotify(enumAxis);
        Q_EMIT axisChanged(axis, axisValue(enumAxis));
        m_axisNotifyCount++;
    }

    Q_EMIT statsChanged();
}

bool Gamepad::buttonState(GamepadButton button) const
{
    const int idx = static_cast<int>(button);
    if (idx < 0 || idx >= static_cast<int>(m_buttonStates.size())) {
        return false;
    }
    return m_buttonStates[static_cast<size_t>(idx)];
}

void Gamepad::setButtonState(GamepadButton button, bool pressed)
{
    const int idx = static_cast<int>(button);
    if (idx < 0 || idx >= static_cast<int>(m_buttonStates.size())) {
        return;
    }
    if (m_buttonStates[static_cast<size_t>(idx)] == pressed) {
        return;
    }
    m_buttonStates[static_cast<size_t>(idx)] = pressed;
    emitButtonNotify(button);
    Q_EMIT buttonChanged(idx, pressed);
}

void Gamepad::emitButtonNotify(GamepadButton button)
{
    switch (button) {
    case deckshell::deckgamepad::GAMEPAD_BUTTON_A:
        Q_EMIT buttonAChanged();
        break;
    case deckshell::deckgamepad::GAMEPAD_BUTTON_B:
        Q_EMIT buttonBChanged();
        break;
    case deckshell::deckgamepad::GAMEPAD_BUTTON_X:
        Q_EMIT buttonXChanged();
        break;
    case deckshell::deckgamepad::GAMEPAD_BUTTON_Y:
        Q_EMIT buttonYChanged();
        break;
    case deckshell::deckgamepad::GAMEPAD_BUTTON_L1:
        Q_EMIT buttonL1Changed();
        break;
    case deckshell::deckgamepad::GAMEPAD_BUTTON_R1:
        Q_EMIT buttonR1Changed();
        break;
    case deckshell::deckgamepad::GAMEPAD_BUTTON_L2:
        Q_EMIT buttonL2Changed();
        break;
    case deckshell::deckgamepad::GAMEPAD_BUTTON_R2:
        Q_EMIT buttonR2Changed();
        break;
    case deckshell::deckgamepad::GAMEPAD_BUTTON_SELECT:
        Q_EMIT buttonSelectChanged();
        break;
    case deckshell::deckgamepad::GAMEPAD_BUTTON_START:
        Q_EMIT buttonStartChanged();
        break;
    case deckshell::deckgamepad::GAMEPAD_BUTTON_L3:
        Q_EMIT buttonL3Changed();
        break;
    case deckshell::deckgamepad::GAMEPAD_BUTTON_R3:
        Q_EMIT buttonR3Changed();
        break;
    case deckshell::deckgamepad::GAMEPAD_BUTTON_GUIDE:
        Q_EMIT buttonGuideChanged();
        break;
    case deckshell::deckgamepad::GAMEPAD_BUTTON_DPAD_UP:
        Q_EMIT buttonDpadUpChanged();
        break;
    case deckshell::deckgamepad::GAMEPAD_BUTTON_DPAD_DOWN:
        Q_EMIT buttonDpadDownChanged();
        break;
    case deckshell::deckgamepad::GAMEPAD_BUTTON_DPAD_LEFT:
        Q_EMIT buttonDpadLeftChanged();
        break;
    case deckshell::deckgamepad::GAMEPAD_BUTTON_DPAD_RIGHT:
        Q_EMIT buttonDpadRightChanged();
        break;
    default:
        break;
    }
}

double Gamepad::axisValue(GamepadAxis axis) const
{
    const int idx = static_cast<int>(axis);
    if (idx < 0 || idx >= static_cast<int>(m_axisValues.size())) {
        return 0.0;
    }
    return m_axisValues[static_cast<size_t>(idx)];
}

void Gamepad::setAxisValue(GamepadAxis axis, double value)
{
    const int idx = static_cast<int>(axis);
    if (idx < 0 || idx >= static_cast<int>(m_axisValues.size())) {
        return;
    }
    m_axisValues[static_cast<size_t>(idx)] = value;
}

void Gamepad::emitAxisNotify(GamepadAxis axis)
{
    switch (axis) {
    case deckshell::deckgamepad::GAMEPAD_AXIS_LEFT_X:
        Q_EMIT axisLeftXChanged();
        break;
    case deckshell::deckgamepad::GAMEPAD_AXIS_LEFT_Y:
        Q_EMIT axisLeftYChanged();
        break;
    case deckshell::deckgamepad::GAMEPAD_AXIS_RIGHT_X:
        Q_EMIT axisRightXChanged();
        break;
    case deckshell::deckgamepad::GAMEPAD_AXIS_RIGHT_Y:
        Q_EMIT axisRightYChanged();
        break;
    case deckshell::deckgamepad::GAMEPAD_AXIS_TRIGGER_LEFT:
        Q_EMIT axisTriggerLeftChanged();
        break;
    case deckshell::deckgamepad::GAMEPAD_AXIS_TRIGGER_RIGHT:
        Q_EMIT axisTriggerRightChanged();
        break;
    default:
        break;
    }
}

void Gamepad::resetState()
{
    m_coalesceTimer.stop();
    m_buttonStates.fill(false);
    m_axisValues.fill(0.0);
    m_hatDirectionByHat.fill(deckshell::deckgamepad::GAMEPAD_HAT_CENTER);
    m_pendingAxisMask = 0;
    m_pendingHatMask = 0;
    m_pendingHatDirectionByHat.fill(deckshell::deckgamepad::GAMEPAD_HAT_CENTER);
    m_pendingCoalesceStartWallclockMs = -1;

    m_axisRawEventCount = 0;
    m_axisNotifyCount = 0;
    m_hatRawEventCount = 0;
    m_hatNotifyCount = 0;
    m_lastCoalesceLatencyMs = 0;

    Q_EMIT hatDirectionChanged();
    Q_EMIT hat1DirectionChanged();
    Q_EMIT hat2DirectionChanged();
    Q_EMIT hat3DirectionChanged();
    Q_EMIT statsChanged();

    Q_EMIT buttonAChanged();
    Q_EMIT buttonBChanged();
    Q_EMIT buttonXChanged();
    Q_EMIT buttonYChanged();
    Q_EMIT buttonL1Changed();
    Q_EMIT buttonR1Changed();
    Q_EMIT buttonL2Changed();
    Q_EMIT buttonR2Changed();
    Q_EMIT buttonSelectChanged();
    Q_EMIT buttonStartChanged();
    Q_EMIT buttonL3Changed();
    Q_EMIT buttonR3Changed();
    Q_EMIT buttonGuideChanged();
    Q_EMIT buttonDpadUpChanged();
    Q_EMIT buttonDpadDownChanged();
    Q_EMIT buttonDpadLeftChanged();
    Q_EMIT buttonDpadRightChanged();

    Q_EMIT axisLeftXChanged();
    Q_EMIT axisLeftYChanged();
    Q_EMIT axisRightXChanged();
    Q_EMIT axisRightYChanged();
    Q_EMIT axisTriggerLeftChanged();
    Q_EMIT axisTriggerRightChanged();
}

void Gamepad::syncDeviceInfo()
{
    auto *svc = m_manager ? m_manager->service() : nullptr;
    if (!svc) {
        return;
    }

    const bool nextConnected = svc->connectedGamepads().contains(m_deviceId);
    if (m_connected != nextConnected) {
        m_connected = nextConnected;
        Q_EMIT connectedChanged();
    }

    const QString nextName = svc->deviceName(m_deviceId);
    if (m_name != nextName) {
        m_name = nextName;
        Q_EMIT nameChanged();
    }
}

void Gamepad::ensureManagerResolved()
{
    if (m_manager) {
        return;
    }

    GamepadManager *mgr = nullptr;
    auto *engine = qmlEngine(this);
    if (!engine) {
        // QML 引擎尚未关联（property 绑定早于 componentComplete 的场景），避免在这里抢先创建全局单例，
        // 以免与引擎侧 singletonInstance 产生“双实例”并导致事件链路断开。
        return;
    }

    mgr = engine->singletonInstance<GamepadManager *>(QStringLiteral("DeckShell.DeckGamepad"),
                                                      QStringLiteral("GamepadManager"));
    if (!mgr) {
        mgr = GamepadManager::create(engine, nullptr);
    }

    rebuildSubscriptions(mgr);
}

void Gamepad::rebuildSubscriptions(GamepadManager *mgr)
{
    if (!mgr || m_manager == mgr) {
        return;
    }

    if (m_manager) {
        disconnect(m_manager, nullptr, this, nullptr);
    }

    if (auto *prevSvc = m_manager ? m_manager->service() : nullptr) {
        disconnect(prevSvc, nullptr, this, nullptr);
    }

    m_manager = mgr;

    connect(m_manager, &GamepadManager::gamepadConnected, this, &Gamepad::handleDeviceConnected);
    connect(m_manager, &GamepadManager::gamepadDisconnected, this, &Gamepad::handleDeviceDisconnected);

    if (auto *svc = m_manager->service()) {
        connect(svc,
                &DeckGamepadService::buttonEvent,
                this,
                [this](int deviceId, deckshell::deckgamepad::DeckGamepadButtonEvent event) {
                    if (deviceId == m_deviceId) {
                        handleButtonEvent(event);
                    }
                });
        connect(svc,
                &DeckGamepadService::axisEvent,
                this,
                [this](int deviceId, deckshell::deckgamepad::DeckGamepadAxisEvent event) {
                    if (deviceId == m_deviceId) {
                        handleAxisEvent(event);
                    }
                });
        connect(svc,
                &DeckGamepadService::hatEvent,
                this,
                [this](int deviceId, deckshell::deckgamepad::DeckGamepadHatEvent event) {
                    if (deviceId == m_deviceId) {
                        handleHatEvent(event);
                    }
                });
    }

    syncDeviceInfo();
}
