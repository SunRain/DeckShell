// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <deckshell/deckgamepad/extras/deckgamepadactionmapper.h>

#include "abstractgamepadactionsource.h"

#include <QtCore/QObject>
#include <QtCore/QVector>
#include <QtQml/qqml.h>

class Gamepad;

class GamepadActionRouter : public AbstractGamepadActionSource
{
    Q_OBJECT
    QML_ELEMENT

    Q_PROPERTY(bool active READ active WRITE setActive NOTIFY activeChanged FINAL)
    Q_PROPERTY(Gamepad *gamepad READ gamepad WRITE setGamepad NOTIFY gamepadChanged FINAL)

    Q_PROPERTY(double deadzone READ deadzone WRITE setDeadzone NOTIFY mappingConfigChanged FINAL)
    Q_PROPERTY(double hysteresis READ hysteresis WRITE setHysteresis NOTIFY mappingConfigChanged FINAL)
    Q_PROPERTY(deckshell::deckgamepad::DeckGamepadActionMapper::DiagonalPolicy diagonalPolicy READ diagonalPolicy WRITE setDiagonalPolicy NOTIFY mappingConfigChanged FINAL)
    Q_PROPERTY(bool releaseOnCenter READ releaseOnCenter WRITE setReleaseOnCenter NOTIFY mappingConfigChanged FINAL)
    Q_PROPERTY(bool repeatEnabled READ repeatEnabled WRITE setRepeatEnabled NOTIFY mappingConfigChanged FINAL)
    Q_PROPERTY(int repeatDelayMs READ repeatDelayMs WRITE setRepeatDelayMs NOTIFY mappingConfigChanged FINAL)
    Q_PROPERTY(int repeatIntervalMs READ repeatIntervalMs WRITE setRepeatIntervalMs NOTIFY mappingConfigChanged FINAL)

public:
    explicit GamepadActionRouter(QObject *parent = nullptr);
    ~GamepadActionRouter() override;

    bool active() const;
    void setActive(bool active);

    Gamepad *gamepad() const;
    void setGamepad(Gamepad *gamepad);

    double deadzone() const;
    void setDeadzone(double deadzone);

    double hysteresis() const;
    void setHysteresis(double hysteresis);

    deckshell::deckgamepad::DeckGamepadActionMapper::DiagonalPolicy diagonalPolicy() const;
    void setDiagonalPolicy(deckshell::deckgamepad::DeckGamepadActionMapper::DiagonalPolicy policy);

    bool releaseOnCenter() const;
    void setReleaseOnCenter(bool enabled);

    bool repeatEnabled() const;
    void setRepeatEnabled(bool enabled);

    int repeatDelayMs() const;
    void setRepeatDelayMs(int delayMs);

    int repeatIntervalMs() const;
    void setRepeatIntervalMs(int intervalMs);

Q_SIGNALS:
    void activeChanged();
    void gamepadChanged();
    void mappingConfigChanged();

private:
    void updateSubscriptions();

    bool m_active = true;
    Gamepad *m_gamepad = nullptr;
    QVector<QMetaObject::Connection> m_connections;

    deckshell::deckgamepad::DeckGamepadActionMapper m_mapper;
};
