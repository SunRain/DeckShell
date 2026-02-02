// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

// 设备访问策略层：direct-open + 可选 logind TakeDevice（seatd 预留为后续扩展）。

#pragma once

#include <deckshell/deckgamepad/core/deckgamepaderror.h>
#include <deckshell/deckgamepad/core/deckgamepadruntimeconfig.h>

#include <QtCore/QObject>
#include <QtCore/QString>

#include <functional>

DECKGAMEPAD_BEGIN_NAMESPACE

struct DeckGamepadDeviceOpenResult {
    int fd = -1;
    QString method; // "direct" | "logind"
    DeckGamepadError error;
    std::function<void()> releaseDevice; // logind ReleaseDevice（如有）

    bool ok() const { return fd >= 0; }
};

class DeviceAccessBroker final : public QObject
{
    Q_OBJECT

public:
    explicit DeviceAccessBroker(QObject *parent = nullptr);

    void setRuntimeConfig(const DeckGamepadRuntimeConfig &config);
    DeckGamepadRuntimeConfig runtimeConfig() const;

    DeckGamepadDeviceOpenResult openDevice(const QString &devpath) const;

private:
    DeckGamepadDeviceOpenResult openDirect(const QString &devpath) const;
    DeckGamepadDeviceOpenResult openDirectReadOnly(const QString &devpath) const;
    DeckGamepadDeviceOpenResult openViaLogind(const QString &devpath) const;

    DeckGamepadRuntimeConfig m_config;
};

DECKGAMEPAD_END_NAMESPACE
