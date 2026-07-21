// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QByteArray>

struct wlr_input_device;

class DevicePathFixture final
{
public:
    DevicePathFixture(wlr_input_device *device,
                      QByteArray physicalPath,
                      QByteArray devicePath,
                      QByteArray procDevicesPath);
    ~DevicePathFixture();

    DevicePathFixture(const DevicePathFixture &) = delete;
    DevicePathFixture &operator=(const DevicePathFixture &) = delete;
};
