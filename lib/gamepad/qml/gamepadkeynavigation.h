// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QtCore/QHash>
#include <QtCore/QObject>
#include <QtCore/QMetaObject>
#include <QtCore/QPointer>
#include <QtCore/QVector>
#include <QtQml/QQmlParserStatus>
#include <QtQml/qqml.h>

#include <deckshell/deckgamepad/extras/deckgamepadactionmapper.h>

#include "abstractgamepadactionsource.h"

class Gamepad;
class GamepadActionRouter;

class GamepadKeyNavigation : public QObject, public QQmlParserStatus
{
    Q_OBJECT
    Q_INTERFACES(QQmlParserStatus)
	    QML_ELEMENT

	    Q_PROPERTY(bool active READ active WRITE setActive NOTIFY activeChanged FINAL)
	    Q_PROPERTY(Gamepad *gamepad READ gamepad WRITE setGamepad NOTIFY gamepadChanged FINAL)
	    Q_PROPERTY(AbstractGamepadActionSource *actionSource READ actionSource WRITE setActionSource NOTIFY actionSourceChanged FINAL)
	    Q_PROPERTY(GamepadActionRouter *actionRouter READ actionRouter WRITE setActionRouter NOTIFY actionRouterChanged FINAL)
	    Q_PROPERTY(bool useLegacyMapper READ useLegacyMapper WRITE setUseLegacyMapper NOTIFY useLegacyMapperChanged FINAL)
	    Q_PROPERTY(QObject *target READ target WRITE setTarget NOTIFY targetChanged FINAL)
	    Q_PROPERTY(QString suppressionReason READ suppressionReason NOTIFY suppressionReasonChanged FINAL)

public:
    explicit GamepadKeyNavigation(QObject *parent = nullptr);
    ~GamepadKeyNavigation() override;

    void classBegin() override;
    void componentComplete() override;

    bool active() const;
    void setActive(bool active);

    Gamepad *gamepad() const;
    void setGamepad(Gamepad *gamepad);

	    GamepadActionRouter *actionRouter() const;
	    void setActionRouter(GamepadActionRouter *router);

	    AbstractGamepadActionSource *actionSource() const;
	    void setActionSource(AbstractGamepadActionSource *source);

    bool useLegacyMapper() const;
    void setUseLegacyMapper(bool enabled);

    QObject *target() const;
    void setTarget(QObject *target);

    QString suppressionReason() const;

Q_SIGNALS:
    void activeChanged();
    void gamepadChanged();
    void actionSourceChanged();
    void actionRouterChanged();
    void useLegacyMapperChanged();
    void targetChanged();
    void suppressionReasonChanged();

private Q_SLOTS:
    void onActionTriggered(const QString &actionId, bool pressed, bool repeated);

private:
    static quint64 keyCombo(int qtKey, int modifiers);

    void updateSubscriptions();
    void releaseAll();
    void handleAction(const QString &actionId, bool pressed, bool repeated);
    QObject *resolveTarget() const;
    bool shouldSuppress(QObject *resolvedTarget, QString *reason) const;
	    void updateSuppressionReason(const QString &reason);

	    bool m_active = false;
	    Gamepad *m_gamepad = nullptr;
	    AbstractGamepadActionSource *m_actionSource = nullptr;
	    GamepadActionRouter *m_actionRouter = nullptr;
	    bool m_useLegacyMapper = false;
    QPointer<QObject> m_target;

    deckshell::deckgamepad::DeckGamepadActionMapper m_mapper;
    QHash<quint64, QPointer<QObject>> m_pressedTargets;
    QVector<QMetaObject::Connection> m_connections;
    QString m_suppressionReason;
};
