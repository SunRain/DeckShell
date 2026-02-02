// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QtCore/QString>

class UinputTestDevice final
{
public:
    static UinputTestDevice createGamepad(const QString &name);

    UinputTestDevice() = default;
    ~UinputTestDevice();

    UinputTestDevice(const UinputTestDevice &) = delete;
    UinputTestDevice &operator=(const UinputTestDevice &) = delete;

    UinputTestDevice(UinputTestDevice &&other) noexcept;
    UinputTestDevice &operator=(UinputTestDevice &&other) noexcept;

    bool isValid() const;
    QString name() const;

    bool emitKey(int code, int value);
    bool emitAbs(int code, int value);
    bool sync();

private:
    explicit UinputTestDevice(int fd, QString name, bool created);
    void reset();

    int m_fd = -1;
    QString m_name;
    bool m_created = false;
};

