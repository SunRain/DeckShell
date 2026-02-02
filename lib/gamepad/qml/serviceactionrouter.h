// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include "abstractgamepadactionsource.h"

#include <QtCore/QObject>
#include <QtCore/QString>
#include <QtCore/QVector>
#include <QtQml/QQmlParserStatus>
#include <QtQml/qqml.h>

class Gamepad;
class GamepadManager;

class ServiceActionRouter : public AbstractGamepadActionSource, public QQmlParserStatus
{
    Q_OBJECT
    Q_INTERFACES(QQmlParserStatus)
    QML_ELEMENT

    Q_PROPERTY(bool active READ active WRITE setActive NOTIFY activeChanged FINAL)
    Q_PROPERTY(Gamepad *gamepad READ gamepad WRITE setGamepad NOTIFY gamepadChanged FINAL)
    Q_PROPERTY(QObject *service READ service WRITE setService NOTIFY serviceChanged FINAL)

public:
    explicit ServiceActionRouter(QObject *parent = nullptr);
    ~ServiceActionRouter() override;

    void classBegin() override;
    void componentComplete() override;

    bool active() const;
    void setActive(bool active);

    Gamepad *gamepad() const;
    void setGamepad(Gamepad *gamepad);

    QObject *service() const;
    void setService(QObject *service);

Q_SIGNALS:
    void activeChanged();
    void gamepadChanged();
    void serviceChanged();

private Q_SLOTS:
    void onServiceActionTriggered(int deviceId, const QString &actionId, bool pressed, bool repeated);

private:
    void updateSubscriptions();
    GamepadManager *resolveManager() const;

    bool m_active = true;
    Gamepad *m_gamepad = nullptr;
    QObject *m_service = nullptr;
    QVector<QMetaObject::Connection> m_connections;
};
