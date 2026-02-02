// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

// ActionId -> Qt::Key 映射工具：将稳定 actionId 映射为 Qt 键值与修饰键（不负责注入）。

#pragma once

#include <deckshell/deckgamepad/core/deckgamepadaction.h>
#include <deckshell/deckgamepad/core/deckgamepad.h>

#include <QtCore/QString>

DECKGAMEPAD_BEGIN_NAMESPACE

struct DeckGamepadQtKeyMapping final {
    int qtKey = 0; // Qt::Key_*
    int modifiers = 0; // Qt::KeyboardModifier bitmask

    bool isValid() const { return qtKey != 0; }
};

DECKGAMEPAD_EXPORT DeckGamepadQtKeyMapping deckGamepadQtKeyMappingForActionId(const QString &actionId);

DECKGAMEPAD_END_NAMESPACE

