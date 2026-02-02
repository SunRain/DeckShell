// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

// ActionId -> Qt::Key 查询/信号工具：不注入事件，由应用决定是否注入到目标对象。

#pragma once

#include <QtCore/QMetaObject>
#include <QtCore/QObject>
#include <QtCore/QString>
#include <QtCore/QVector>
#include <QtQml/qqml.h>

#include "abstractgamepadactionsource.h"

class GamepadActionKeyMapper : public QObject
{
    Q_OBJECT
    QML_ELEMENT

    Q_PROPERTY(bool active READ active WRITE setActive NOTIFY activeChanged FINAL)
    Q_PROPERTY(AbstractGamepadActionSource *actionRouter READ actionRouter WRITE setActionRouter NOTIFY actionRouterChanged FINAL)

public:
    explicit GamepadActionKeyMapper(QObject *parent = nullptr);
    ~GamepadActionKeyMapper() override;

    bool active() const;
    void setActive(bool active);

    AbstractGamepadActionSource *actionRouter() const;
    void setActionRouter(AbstractGamepadActionSource *router);

    Q_INVOKABLE int qtKeyForActionId(const QString &actionId) const;
    Q_INVOKABLE int modifiersForActionId(const QString &actionId) const;

Q_SIGNALS:
    void activeChanged();
    void actionRouterChanged();

    void keyEvent(int qtKey, int modifiers, bool pressed, bool repeated, const QString &actionId);

private:
    void updateSubscriptions();
    void handleAction(const QString &actionId, bool pressed, bool repeated);

    bool m_active = false;
    AbstractGamepadActionSource *m_actionRouter = nullptr;
    QVector<QMetaObject::Connection> m_connections;
};
