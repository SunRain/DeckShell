// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "devicepathfixture.h"

#include <libinput.h>
#include <libudev.h>

extern "C" {
#include <wlr/backend/libinput.h>
}

#include <sys/syscall.h>

#include <QtGlobal>

#include <cstdarg>
#include <cstddef>
#include <cstring>
#include <dlfcn.h>
#include <fcntl.h>
#include <sys/types.h>
#include <unistd.h>
#include <utility>

namespace {

struct FixtureState
{
    wlr_input_device *device = nullptr;
    QByteArray physicalPath;
    QByteArray devicePath;
    QByteArray procDevicesPath;
};

// The exported symbols below intercept only the active fake device. All other calls are
// forwarded to the real shared libraries so the rest of test_multi_seat remains unchanged.
FixtureState fixture;
alignas(std::max_align_t) char fakeLibinputDevice;
alignas(std::max_align_t) char fakeUdevDevice;

libinput_device *libinputFixtureHandle()
{
    return reinterpret_cast<libinput_device *>(&fakeLibinputDevice);
}

udev_device *udevFixtureHandle()
{
    return reinterpret_cast<udev_device *>(&fakeUdevDevice);
}

template<typename Function>
Function resolveNext(const char *name)
{
    auto function = reinterpret_cast<Function>(dlsym(RTLD_NEXT, name));
    if (!function)
        qFatal("Failed to resolve test interposer dependency: %s", name);
    return function;
}

const char *redirectedPath(const char *path)
{
    if (!fixture.procDevicesPath.isEmpty() && path
        && std::strcmp(path, "/proc/bus/input/devices") == 0) {
        return fixture.procDevicesPath.constData();
    }
    return path;
}

mode_t openMode(int flags, va_list arguments)
{
    if ((flags & O_CREAT) || (flags & O_TMPFILE) == O_TMPFILE)
        return static_cast<mode_t>(va_arg(arguments, int));
    return 0;
}

int openFile(int directoryFd, const char *path, int flags, mode_t mode)
{
    return static_cast<int>(syscall(SYS_openat, directoryFd, redirectedPath(path), flags, mode));
}

} // namespace

DevicePathFixture::DevicePathFixture(wlr_input_device *device,
                                     QByteArray physicalPath,
                                     QByteArray devicePath,
                                     QByteArray procDevicesPath)
{
    Q_ASSERT(device);
    Q_ASSERT(!fixture.device);
    fixture.device = device;
    fixture.physicalPath = std::move(physicalPath);
    fixture.devicePath = std::move(devicePath);
    fixture.procDevicesPath = std::move(procDevicesPath);
}

DevicePathFixture::~DevicePathFixture()
{
    fixture = { };
}

extern "C" bool wlr_input_device_is_libinput(wlr_input_device *device)
{
    if (device == fixture.device)
        return true;

    using Function = bool (*)(wlr_input_device *);
    static const auto function = resolveNext<Function>("wlr_input_device_is_libinput");
    return function(device);
}

extern "C" libinput_device *wlr_libinput_get_device_handle(wlr_input_device *device)
{
    if (device == fixture.device)
        return libinputFixtureHandle();

    using Function = libinput_device *(*)(wlr_input_device *);
    static const auto function = resolveNext<Function>("wlr_libinput_get_device_handle");
    return function(device);
}

extern "C" udev_device *libinput_device_get_udev_device(libinput_device *device)
{
    if (device == libinputFixtureHandle())
        return udevFixtureHandle();

    using Function = udev_device *(*)(libinput_device *);
    static const auto function = resolveNext<Function>("libinput_device_get_udev_device");
    return function(device);
}

extern "C" const char *udev_device_get_property_value(udev_device *device, const char *key)
{
    if (device == udevFixtureHandle()) {
        if (std::strcmp(key, "PHYS") == 0)
            return fixture.physicalPath.isNull() ? nullptr : fixture.physicalPath.constData();
        if (std::strcmp(key, "DEVPATH") == 0)
            return fixture.devicePath.isNull() ? nullptr : fixture.devicePath.constData();
        return nullptr;
    }

    using Function = const char *(*)(udev_device *, const char *);
    static const auto function = resolveNext<Function>("udev_device_get_property_value");
    return function(device, key);
}

extern "C" udev_device *udev_device_unref(udev_device *device)
{
    if (device == udevFixtureHandle())
        return nullptr;

    using Function = udev_device *(*)(udev_device *);
    static const auto function = resolveNext<Function>("udev_device_unref");
    return function(device);
}

extern "C" int openat(int directoryFd, const char *path, int flags, ...)
{
    va_list arguments;
    va_start(arguments, flags);
    const mode_t mode = openMode(flags, arguments);
    va_end(arguments);
    return openFile(directoryFd, path, flags, mode);
}

extern "C" int open(const char *path, int flags, ...)
{
    va_list arguments;
    va_start(arguments, flags);
    const mode_t mode = openMode(flags, arguments);
    va_end(arguments);
    return openFile(AT_FDCWD, path, flags, mode);
}

extern "C" int open64(const char *path, int flags, ...)
{
    va_list arguments;
    va_start(arguments, flags);
    const mode_t mode = openMode(flags, arguments);
    va_end(arguments);
    return openFile(AT_FDCWD, path, flags, mode);
}
