// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

// Active session 门控：在锁屏/切 VT/多会话下自动停止采集，并在恢复后触发重连。

#pragma once

#include <deckshell/deckgamepad/core/deckgamepad.h>

#include <QtCore/QObject>

#if defined(DECKGAMEPAD_ENABLE_LOGIND) && DECKGAMEPAD_ENABLE_LOGIND
#include <QtCore/QVariantMap>
#include <QtDBus/QDBusConnection>
#endif

DECKGAMEPAD_BEGIN_NAMESPACE

class SessionGate final : public QObject
{
    Q_OBJECT

public:
    explicit SessionGate(QObject *parent = nullptr);

    bool enabled() const;
    void setEnabled(bool enabled);

    bool supported() const;
    bool isActive() const;

Q_SIGNALS:
    void activeChanged(bool active);
    void supportedChanged(bool supported);

private:
#if defined(DECKGAMEPAD_ENABLE_LOGIND) && DECKGAMEPAD_ENABLE_LOGIND
    void initLogind();
    void updateActive(bool active);

private Q_SLOTS:
    void handlePropertiesChanged(const QString &interfaceName, const QVariantMap &changed, const QStringList &invalidated);
private:
#endif

    bool m_enabled = true;
    bool m_supported = false;
    bool m_active = true;

#if defined(DECKGAMEPAD_ENABLE_LOGIND) && DECKGAMEPAD_ENABLE_LOGIND
    QDBusConnection m_systemBus;
    QString m_sessionPath;
#endif
};

DECKGAMEPAD_END_NAMESPACE
