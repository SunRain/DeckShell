// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/extras/deckgamepadactionkeymapping.h>

#include <QtCore/QLatin1StringView>
#include <Qt>

DECKGAMEPAD_BEGIN_NAMESPACE

DeckGamepadQtKeyMapping deckGamepadQtKeyMappingForActionId(const QString &actionId)
{
    if (actionId == QLatin1StringView(DeckGamepadActionId::NavUp)) {
        return {Qt::Key_Up, 0};
    }
    if (actionId == QLatin1StringView(DeckGamepadActionId::NavDown)) {
        return {Qt::Key_Down, 0};
    }
    if (actionId == QLatin1StringView(DeckGamepadActionId::NavLeft)) {
        return {Qt::Key_Left, 0};
    }
    if (actionId == QLatin1StringView(DeckGamepadActionId::NavRight)) {
        return {Qt::Key_Right, 0};
    }
    if (actionId == QLatin1StringView(DeckGamepadActionId::NavAccept)) {
        return {Qt::Key_Return, 0};
    }
    if (actionId == QLatin1StringView(DeckGamepadActionId::NavBack)) {
        return {Qt::Key_Escape, 0};
    }
    if (actionId == QLatin1StringView(DeckGamepadActionId::NavMenu)) {
        return {Qt::Key_Menu, 0};
    }
    if (actionId == QLatin1StringView(DeckGamepadActionId::NavTabNext)) {
        return {Qt::Key_Tab, 0};
    }
    if (actionId == QLatin1StringView(DeckGamepadActionId::NavTabPrev)) {
        return {Qt::Key_Backtab, 0};
    }

    // 迁移期别名：保留 `nav.page.*` 的映射，但语义按 Tab 处理。
    if (actionId == QLatin1StringView(DeckGamepadActionId::NavPageNext)) {
        return {Qt::Key_Tab, 0};
    }
    if (actionId == QLatin1StringView(DeckGamepadActionId::NavPagePrev)) {
        return {Qt::Key_Backtab, 0};
    }

    return {};
}

DECKGAMEPAD_END_NAMESPACE
