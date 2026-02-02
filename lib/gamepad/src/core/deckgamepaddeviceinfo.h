// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

// 设备身份与最小信息：用于 compositor 转发/配置持久化/排障（deviceUid 脱敏）。

#pragma once

#include <deckshell/deckgamepad/core/deckgamepad.h>

#include <QtCore/QMetaType>
#include <QtCore/QString>

DECKGAMEPAD_BEGIN_NAMESPACE

struct DeckGamepadDeviceInfo {
    QString deviceUid; // 稳定身份键（脱敏，适合作为持久化 key）
    QString guid;      // SDL GUID（兼容字段）
    QString name;
    uint16_t vendorId = 0;
    uint16_t productId = 0;
    QString transport; // e.g. usb/bluetooth/unknown
    bool supportsRumble = false;

    bool isValid() const { return !deviceUid.isEmpty() || !guid.isEmpty() || !name.isEmpty(); }
};

DECKGAMEPAD_END_NAMESPACE

Q_DECLARE_METATYPE(deckshell::deckgamepad::DeckGamepadDeviceInfo)

