// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "gamepaddevicemodel.h"

#include "gamepadmanager.h"

#include <deckshell/deckgamepad/service/deckgamepadservice.h>

using deckshell::deckgamepad::DeckGamepadService;

GamepadDeviceModel::GamepadDeviceModel(QObject *parent)
    : QAbstractListModel(parent)
{
}

int GamepadDeviceModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid()) {
        return 0;
    }
    return m_devices.size();
}

QVariant GamepadDeviceModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || index.row() < 0 || index.row() >= m_devices.size()) {
        return {};
    }

    const auto &dev = m_devices.at(index.row());
    switch (role) {
    case DeviceIdRole:
        return dev.deviceId;
    case DeviceNameRole:
        return dev.deviceName;
    case IsConnectedRole:
        return dev.isConnected;
    case PlayerIndexRole:
        return dev.playerIndex;
    default:
        return {};
    }
}

QHash<int, QByteArray> GamepadDeviceModel::roleNames() const
{
    QHash<int, QByteArray> roles;
    roles[DeviceIdRole] = "deviceId";
    roles[DeviceNameRole] = "deviceName";
    roles[IsConnectedRole] = "isConnected";
    roles[PlayerIndexRole] = "playerIndex";
    return roles;
}

void GamepadDeviceModel::refresh()
{
    beginResetModel();

    m_devices.clear();

    // 避免在这里调用 GamepadManager::instance()，否则在 GamepadManager 构造期间会递归创建单例并导致崩溃。
    auto *mgr = qobject_cast<GamepadManager *>(parent());
    if (mgr && mgr->service()) {
        const auto deviceIds = mgr->service()->connectedGamepads();
        for (int id : deviceIds) {
            DeviceInfo info;
            info.deviceId = id;
            info.deviceName = mgr->service()->deviceName(id);
            info.isConnected = true;
            info.playerIndex = mgr->service()->playerIndex(id);
            m_devices.append(std::move(info));
        }
    }

    endResetModel();
}
