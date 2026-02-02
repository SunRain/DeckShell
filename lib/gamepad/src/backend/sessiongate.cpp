// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "sessiongate.h"

#include <QtCore/QCoreApplication>

#if defined(DECKGAMEPAD_ENABLE_LOGIND) && DECKGAMEPAD_ENABLE_LOGIND
#include <QtDBus/QDBusInterface>
#include <QtDBus/QDBusObjectPath>
#include <QtDBus/QDBusReply>
#endif

DECKGAMEPAD_BEGIN_NAMESPACE

SessionGate::SessionGate(QObject *parent)
    : QObject(parent)
#if defined(DECKGAMEPAD_ENABLE_LOGIND) && DECKGAMEPAD_ENABLE_LOGIND
    , m_systemBus(QDBusConnection::systemBus())
#endif
{
#if defined(DECKGAMEPAD_ENABLE_LOGIND) && DECKGAMEPAD_ENABLE_LOGIND
    initLogind();
#endif
}

bool SessionGate::enabled() const
{
    return m_enabled;
}

void SessionGate::setEnabled(bool enabled)
{
    if (m_enabled == enabled) {
        return;
    }
    m_enabled = enabled;
    if (!m_enabled) {
        if (!m_active) {
            m_active = true;
            Q_EMIT activeChanged(m_active);
        }
    }
}

bool SessionGate::supported() const
{
    return m_supported;
}

bool SessionGate::isActive() const
{
    return !m_enabled ? true : m_active;
}

#if defined(DECKGAMEPAD_ENABLE_LOGIND) && DECKGAMEPAD_ENABLE_LOGIND
void SessionGate::initLogind()
{
    if (!m_systemBus.isConnected()) {
        m_supported = false;
        Q_EMIT supportedChanged(m_supported);
        return;
    }

    QDBusInterface manager(QStringLiteral("org.freedesktop.login1"),
                           QStringLiteral("/org/freedesktop/login1"),
                           QStringLiteral("org.freedesktop.login1.Manager"),
                           m_systemBus);
    if (!manager.isValid()) {
        m_supported = false;
        Q_EMIT supportedChanged(m_supported);
        return;
    }

    const uint32_t pid = static_cast<uint32_t>(QCoreApplication::applicationPid());
    QDBusReply<QDBusObjectPath> sessionReply = manager.call(QStringLiteral("GetSessionByPID"), pid);
    if (!sessionReply.isValid()) {
        m_supported = false;
        Q_EMIT supportedChanged(m_supported);
        return;
    }

    m_sessionPath = sessionReply.value().path();
    if (m_sessionPath.isEmpty()) {
        m_supported = false;
        Q_EMIT supportedChanged(m_supported);
        return;
    }

    m_supported = true;
    Q_EMIT supportedChanged(m_supported);

    // query current Active
    QDBusInterface props(QStringLiteral("org.freedesktop.login1"),
                         m_sessionPath,
                         QStringLiteral("org.freedesktop.DBus.Properties"),
                         m_systemBus);
    if (props.isValid()) {
        QDBusReply<QVariant> activeReply = props.call(QStringLiteral("Get"),
                                                      QStringLiteral("org.freedesktop.login1.Session"),
                                                      QStringLiteral("Active"));
        if (activeReply.isValid()) {
            updateActive(activeReply.value().toBool());
        }
    }

    // subscribe to PropertiesChanged
    (void)m_systemBus.connect(QStringLiteral("org.freedesktop.login1"),
                              m_sessionPath,
                              QStringLiteral("org.freedesktop.DBus.Properties"),
                              QStringLiteral("PropertiesChanged"),
                              this,
                              SLOT(handlePropertiesChanged(QString,QVariantMap,QStringList)));
}

void SessionGate::updateActive(bool active)
{
    if (m_active == active) {
        return;
    }
    m_active = active;
    Q_EMIT activeChanged(m_active);
}

void SessionGate::handlePropertiesChanged(const QString &interfaceName,
                                          const QVariantMap &changed,
                                          const QStringList &invalidated)
{
    Q_UNUSED(invalidated);
    if (!m_enabled) {
        return;
    }
    if (interfaceName != QLatin1StringView("org.freedesktop.login1.Session")) {
        return;
    }
    const auto it = changed.find(QStringLiteral("Active"));
    if (it != changed.end()) {
        updateActive(it.value().toBool());
    }
}
#endif

DECKGAMEPAD_END_NAMESPACE
