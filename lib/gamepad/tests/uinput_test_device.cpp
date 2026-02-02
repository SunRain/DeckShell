// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "uinput_test_device.h"

#if defined(__linux__)
#include <linux/input.h>
#include <linux/uinput.h>

#include <errno.h>
#include <fcntl.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/time.h>
#include <unistd.h>
#endif

UinputTestDevice::UinputTestDevice(int fd, QString name, bool created)
    : m_fd(fd)
    , m_name(std::move(name))
    , m_created(created)
{
}

UinputTestDevice::~UinputTestDevice()
{
    reset();
}

UinputTestDevice::UinputTestDevice(UinputTestDevice &&other) noexcept
{
    *this = std::move(other);
}

UinputTestDevice &UinputTestDevice::operator=(UinputTestDevice &&other) noexcept
{
    if (this == &other) {
        return *this;
    }

    reset();
    m_fd = other.m_fd;
    m_name = std::move(other.m_name);
    m_created = other.m_created;

    other.m_fd = -1;
    other.m_created = false;
    other.m_name.clear();
    return *this;
}

bool UinputTestDevice::isValid() const
{
    return m_fd >= 0 && m_created;
}

QString UinputTestDevice::name() const
{
    return m_name;
}

void UinputTestDevice::reset()
{
#if defined(__linux__)
    if (m_fd >= 0) {
        if (m_created) {
            (void)ioctl(m_fd, UI_DEV_DESTROY);
        }
        (void)::close(m_fd);
    }
#endif
    m_fd = -1;
    m_created = false;
    m_name.clear();
}

UinputTestDevice UinputTestDevice::createGamepad(const QString &name)
{
#if !defined(__linux__)
    Q_UNUSED(name);
    return UinputTestDevice{};
#else
    const int fd = ::open("/dev/uinput", O_RDWR | O_NONBLOCK);
    if (fd < 0) {
        return UinputTestDevice{};
    }

    auto fail = [&] {
        (void)::close(fd);
        return UinputTestDevice{};
    };

    // Enable event types
    if (ioctl(fd, UI_SET_EVBIT, EV_KEY) < 0) {
        return fail();
    }
    if (ioctl(fd, UI_SET_EVBIT, EV_ABS) < 0) {
        return fail();
    }
    if (ioctl(fd, UI_SET_EVBIT, EV_SYN) < 0) {
        return fail();
    }

    // Buttons
    const int keys[] = {
        BTN_SOUTH,
        BTN_EAST,
        BTN_NORTH,
        BTN_WEST,
        BTN_TL,
        BTN_TR,
        BTN_SELECT,
        BTN_START,
    };
    for (int code : keys) {
        if (ioctl(fd, UI_SET_KEYBIT, code) < 0) {
            return fail();
        }
    }

    // Axes + hats
    const int absCodes[] = {
        ABS_X,
        ABS_Y,
        ABS_HAT0X,
        ABS_HAT0Y,
    };
    for (int code : absCodes) {
        if (ioctl(fd, UI_SET_ABSBIT, code) < 0) {
            return fail();
        }
    }

    struct uinput_user_dev uidev = {};
    const QByteArray utf8Name = name.toUtf8();
    (void)snprintf(uidev.name, sizeof(uidev.name), "%s", utf8Name.constData());
    uidev.id.bustype = BUS_USB;
    uidev.id.vendor = 0x1234;
    uidev.id.product = 0x5678;
    uidev.id.version = 1;

    // ABS ranges
    uidev.absmin[ABS_X] = -32768;
    uidev.absmax[ABS_X] = 32767;
    uidev.absmin[ABS_Y] = -32768;
    uidev.absmax[ABS_Y] = 32767;
    uidev.absmin[ABS_HAT0X] = -1;
    uidev.absmax[ABS_HAT0X] = 1;
    uidev.absmin[ABS_HAT0Y] = -1;
    uidev.absmax[ABS_HAT0Y] = 1;

    const ssize_t wrote = ::write(fd, &uidev, sizeof(uidev));
    if (wrote != static_cast<ssize_t>(sizeof(uidev))) {
        return fail();
    }

    if (ioctl(fd, UI_DEV_CREATE) < 0) {
        return fail();
    }

    return UinputTestDevice(fd, name, true);
#endif
}

bool UinputTestDevice::emitKey(int code, int value)
{
#if !defined(__linux__)
    Q_UNUSED(code);
    Q_UNUSED(value);
    return false;
#else
    if (!isValid()) {
        return false;
    }

    struct input_event ev = {};
    (void)gettimeofday(&ev.time, nullptr);
    ev.type = EV_KEY;
    ev.code = static_cast<__u16>(code);
    ev.value = value;

    const ssize_t wrote = ::write(m_fd, &ev, sizeof(ev));
    return wrote == static_cast<ssize_t>(sizeof(ev));
#endif
}

bool UinputTestDevice::emitAbs(int code, int value)
{
#if !defined(__linux__)
    Q_UNUSED(code);
    Q_UNUSED(value);
    return false;
#else
    if (!isValid()) {
        return false;
    }

    struct input_event ev = {};
    (void)gettimeofday(&ev.time, nullptr);
    ev.type = EV_ABS;
    ev.code = static_cast<__u16>(code);
    ev.value = value;

    const ssize_t wrote = ::write(m_fd, &ev, sizeof(ev));
    return wrote == static_cast<ssize_t>(sizeof(ev));
#endif
}

bool UinputTestDevice::sync()
{
#if !defined(__linux__)
    return false;
#else
    if (!isValid()) {
        return false;
    }

    struct input_event ev = {};
    (void)gettimeofday(&ev.time, nullptr);
    ev.type = EV_SYN;
    ev.code = SYN_REPORT;
    ev.value = 0;

    const ssize_t wrote = ::write(m_fd, &ev, sizeof(ev));
    return wrote == static_cast<ssize_t>(sizeof(ev));
#endif
}
