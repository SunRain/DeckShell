// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "gamepadactionrouter.h"

#include "gamepad.h"

GamepadActionRouter::GamepadActionRouter(QObject *parent)
    : AbstractGamepadActionSource(parent)
    , m_mapper(this)
{
    m_mapper.setEnabled(true);
    m_mapper.applyNavigationPreset();

    connect(&m_mapper,
            &deckshell::deckgamepad::DeckGamepadActionMapper::actionTriggered,
            this,
            &AbstractGamepadActionSource::actionTriggered);
}

GamepadActionRouter::~GamepadActionRouter() = default;

bool GamepadActionRouter::active() const
{
    return m_active;
}

void GamepadActionRouter::setActive(bool active)
{
    if (m_active == active) {
        return;
    }
    m_active = active;
    updateSubscriptions();
    Q_EMIT activeChanged();
}

Gamepad *GamepadActionRouter::gamepad() const
{
    return m_gamepad;
}

void GamepadActionRouter::setGamepad(Gamepad *gamepad)
{
    if (m_gamepad == gamepad) {
        return;
    }
    m_gamepad = gamepad;
    updateSubscriptions();
    Q_EMIT gamepadChanged();
}

double GamepadActionRouter::deadzone() const
{
    return m_mapper.deadzone();
}

void GamepadActionRouter::setDeadzone(double deadzone)
{
    m_mapper.setDeadzone(deadzone);
    Q_EMIT mappingConfigChanged();
}

double GamepadActionRouter::hysteresis() const
{
    return m_mapper.hysteresis();
}

void GamepadActionRouter::setHysteresis(double hysteresis)
{
    m_mapper.setHysteresis(hysteresis);
    Q_EMIT mappingConfigChanged();
}

deckshell::deckgamepad::DeckGamepadActionMapper::DiagonalPolicy GamepadActionRouter::diagonalPolicy() const
{
    return m_mapper.diagonalPolicy();
}

void GamepadActionRouter::setDiagonalPolicy(deckshell::deckgamepad::DeckGamepadActionMapper::DiagonalPolicy policy)
{
    m_mapper.setDiagonalPolicy(policy);
    Q_EMIT mappingConfigChanged();
}

bool GamepadActionRouter::releaseOnCenter() const
{
    return m_mapper.releaseOnCenter();
}

void GamepadActionRouter::setReleaseOnCenter(bool enabled)
{
    m_mapper.setReleaseOnCenter(enabled);
    Q_EMIT mappingConfigChanged();
}

bool GamepadActionRouter::repeatEnabled() const
{
    return m_mapper.repeatEnabled();
}

void GamepadActionRouter::setRepeatEnabled(bool enabled)
{
    m_mapper.setRepeatEnabled(enabled);
    Q_EMIT mappingConfigChanged();
}

int GamepadActionRouter::repeatDelayMs() const
{
    return m_mapper.repeatDelayMs();
}

void GamepadActionRouter::setRepeatDelayMs(int delayMs)
{
    m_mapper.setRepeatDelayMs(delayMs);
    Q_EMIT mappingConfigChanged();
}

int GamepadActionRouter::repeatIntervalMs() const
{
    return m_mapper.repeatIntervalMs();
}

void GamepadActionRouter::setRepeatIntervalMs(int intervalMs)
{
    m_mapper.setRepeatIntervalMs(intervalMs);
    Q_EMIT mappingConfigChanged();
}

void GamepadActionRouter::updateSubscriptions()
{
    for (const auto &c : m_connections) {
        disconnect(c);
    }
    m_connections.clear();

    if (!m_active || !m_gamepad) {
        m_mapper.setEnabled(false);
        m_mapper.reset();
        return;
    }

    m_mapper.setEnabled(true);

    m_connections.append(connect(m_gamepad, &QObject::destroyed, this, [this]() {
        m_gamepad = nullptr;
        updateSubscriptions();
    }));

    m_connections.append(connect(m_gamepad, &Gamepad::deviceIdChanged, this, [this]() {
        m_mapper.reset();
    }));

    m_connections.append(connect(m_gamepad, &Gamepad::connectedChanged, this, [this]() {
        if (m_gamepad && !m_gamepad->connected()) {
            m_mapper.reset();
        }
    }));

    m_connections.append(connect(m_gamepad, &Gamepad::buttonChanged, this, [this](int button, bool pressed) {
        if (!m_active) {
            return;
        }
        if (button < 0 || button >= deckshell::deckgamepad::GAMEPAD_BUTTON_MAX) {
            return;
        }
        m_mapper.processButton(static_cast<deckshell::deckgamepad::GamepadButton>(button), pressed);
    }));

    m_connections.append(connect(m_gamepad, &Gamepad::axisChanged, this, [this](int axis, double value) {
        if (!m_active) {
            return;
        }
        if (axis < 0 || axis >= deckshell::deckgamepad::GAMEPAD_AXIS_MAX) {
            return;
        }
        m_mapper.processAxis(static_cast<deckshell::deckgamepad::GamepadAxis>(axis), value);
    }));
}
