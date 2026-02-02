// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QtCore/QAbstractListModel>
#include <QtCore/QList>
#include <QtCore/QString>
#include <QtQml/qqml.h>

class GamepadDeviceModel : public QAbstractListModel
{
    Q_OBJECT
    QML_ELEMENT

public:
    enum Roles {
        DeviceIdRole = Qt::UserRole + 1,
        DeviceNameRole,
        IsConnectedRole,
        PlayerIndexRole,
    };

    explicit GamepadDeviceModel(QObject *parent = nullptr);
    ~GamepadDeviceModel() override = default;

    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;
    QHash<int, QByteArray> roleNames() const override;

public Q_SLOTS:
    void refresh();

private:
    struct DeviceInfo {
        int deviceId = -1;
        QString deviceName;
        bool isConnected = false;
        int playerIndex = -1;
    };

    QList<DeviceInfo> m_devices;
};
