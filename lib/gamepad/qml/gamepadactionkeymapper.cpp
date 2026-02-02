// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "gamepadactionkeymapper.h"

#include <deckshell/deckgamepad/extras/deckgamepadactionkeymapping.h>

GamepadActionKeyMapper::GamepadActionKeyMapper(QObject *parent)
    : QObject(parent)
{
}

GamepadActionKeyMapper::~GamepadActionKeyMapper() = default;

bool GamepadActionKeyMapper::active() const
{
    return m_active;
}

void GamepadActionKeyMapper::setActive(bool active)
{
    if (m_active == active) {
        return;
    }
    m_active = active;
    updateSubscriptions();
    Q_EMIT activeChanged();
}

AbstractGamepadActionSource *GamepadActionKeyMapper::actionRouter() const
{
    return m_actionRouter;
}

void GamepadActionKeyMapper::setActionRouter(AbstractGamepadActionSource *router)
{
    if (m_actionRouter == router) {
        return;
    }
    m_actionRouter = router;
    updateSubscriptions();
    Q_EMIT actionRouterChanged();
}

int GamepadActionKeyMapper::qtKeyForActionId(const QString &actionId) const
{
    const auto mapping = deckshell::deckgamepad::deckGamepadQtKeyMappingForActionId(actionId);
    return mapping.qtKey;
}

int GamepadActionKeyMapper::modifiersForActionId(const QString &actionId) const
{
    const auto mapping = deckshell::deckgamepad::deckGamepadQtKeyMappingForActionId(actionId);
    return mapping.modifiers;
}

void GamepadActionKeyMapper::updateSubscriptions()
{
    for (const auto &c : m_connections) {
        disconnect(c);
    }
    m_connections.clear();

    if (!m_active) {
        return;
    }

    if (!m_actionRouter) {
        return;
    }

    m_connections.append(connect(m_actionRouter, &QObject::destroyed, this, [this]() {
        m_actionRouter = nullptr;
        updateSubscriptions();
    }));

	    m_connections.append(connect(m_actionRouter,
	                                 &AbstractGamepadActionSource::actionTriggered,
	                                 this,
	                                 &GamepadActionKeyMapper::handleAction));
}

void GamepadActionKeyMapper::handleAction(const QString &actionId, bool pressed, bool repeated)
{
    if (!m_active) {
        return;
    }

    const auto mapping = deckshell::deckgamepad::deckGamepadQtKeyMappingForActionId(actionId);
    if (!mapping.isValid()) {
        return;
    }

    Q_EMIT keyEvent(mapping.qtKey, mapping.modifiers, pressed, repeated, actionId);
}
