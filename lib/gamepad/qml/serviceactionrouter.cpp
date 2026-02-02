// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "serviceactionrouter.h"

#include "gamepad.h"
#include "gamepadmanager.h"

#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtQml/QQmlEngine>

ServiceActionRouter::ServiceActionRouter(QObject *parent)
    : AbstractGamepadActionSource(parent)
{
}

ServiceActionRouter::~ServiceActionRouter() = default;

void ServiceActionRouter::classBegin()
{
}

void ServiceActionRouter::componentComplete()
{
    updateSubscriptions();
}

bool ServiceActionRouter::active() const
{
    return m_active;
}

void ServiceActionRouter::setActive(bool active)
{
    if (m_active == active) {
        return;
    }
    m_active = active;
    updateSubscriptions();
    Q_EMIT activeChanged();
}

Gamepad *ServiceActionRouter::gamepad() const
{
    return m_gamepad;
}

void ServiceActionRouter::setGamepad(Gamepad *gamepad)
{
    if (m_gamepad == gamepad) {
        return;
    }
    m_gamepad = gamepad;
    updateSubscriptions();
    Q_EMIT gamepadChanged();
}

QObject *ServiceActionRouter::service() const
{
    return m_service;
}

void ServiceActionRouter::setService(QObject *service)
{
    if (m_service == service) {
        return;
    }
    m_service = service;
    updateSubscriptions();
    Q_EMIT serviceChanged();
}

GamepadManager *ServiceActionRouter::resolveManager() const
{
    auto *engine = qmlEngine(this);
    if (!engine) {
        // QML 引擎尚未关联：避免抢先创建全局单例，防止错过 _deckGamepadService 注入并产生“双实例”。
        return nullptr;
    }

    if (auto *mgr = engine->singletonInstance<GamepadManager *>(QStringLiteral("DeckShell.DeckGamepad"),
                                                                QStringLiteral("GamepadManager"))) {
        return mgr;
    }

    return GamepadManager::create(engine, nullptr);
}

void ServiceActionRouter::onServiceActionTriggered(int deviceId, const QString &actionId, bool pressed, bool repeated)
{
    if (!m_active || !m_gamepad) {
        return;
    }
    if (deviceId != m_gamepad->deviceId()) {
        return;
    }
    Q_EMIT actionTriggered(actionId, pressed, repeated);
}

void ServiceActionRouter::updateSubscriptions()
{
    for (const auto &c : m_connections) {
        disconnect(c);
    }
    m_connections.clear();

    if (!m_active || !m_gamepad) {
        return;
    }

    m_connections.append(connect(m_gamepad, &QObject::destroyed, this, [this]() {
        m_gamepad = nullptr;
        updateSubscriptions();
    }));

    QObject *svc = m_service;
    if (!svc) {
        auto *mgr = resolveManager();
        svc = mgr ? mgr->service() : nullptr;
    }
    if (!svc) {
        return;
    }

    m_connections.append(connect(svc, &QObject::destroyed, this, [this]() {
        updateSubscriptions();
    }));

    m_connections.append(connect(svc,
                                 SIGNAL(actionTriggered(int,QString,bool,bool)),
                                 this,
                                 SLOT(onServiceActionTriggered(int,QString,bool,bool))));
}
