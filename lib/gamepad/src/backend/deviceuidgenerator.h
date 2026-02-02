// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

// deviceUid 生成：基于 udev 属性组合，并对敏感字段做 hash（不泄露 serial/path 原文）。

#pragma once

#include <deckshell/deckgamepad/core/deckgamepad.h>

#include <QtCore/QHash>
#include <QtCore/QString>

DECKGAMEPAD_BEGIN_NAMESPACE

class DeckGamepadDeviceUidGenerator
{
public:
    static QString generateFromUdevProperties(const QHash<QString, QString> &props);
};

DECKGAMEPAD_END_NAMESPACE

