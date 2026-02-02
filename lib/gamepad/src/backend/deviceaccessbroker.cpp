// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "deviceaccessbroker.h"

#include <QtCore/QCoreApplication>

extern "C" {
#include <sys/stat.h>
#include <sys/sysmacros.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
}

#if defined(DECKGAMEPAD_ENABLE_LOGIND) && DECKGAMEPAD_ENABLE_LOGIND
#include <QtDBus/QDBusConnection>
#include <QtDBus/QDBusInterface>
#include <QtDBus/QDBusObjectPath>
#include <QtDBus/QDBusReply>
#include <QtDBus/QDBusUnixFileDescriptor>
#endif

DECKGAMEPAD_BEGIN_NAMESPACE

DeviceAccessBroker::DeviceAccessBroker(QObject *parent)
    : QObject(parent)
{
}

void DeviceAccessBroker::setRuntimeConfig(const DeckGamepadRuntimeConfig &config)
{
    m_config = config;
}

DeckGamepadRuntimeConfig DeviceAccessBroker::runtimeConfig() const
{
    return m_config;
}

DeckGamepadDeviceOpenResult DeviceAccessBroker::openDevice(const QString &devpath) const
{
    switch (m_config.deviceAccessMode) {
    case DeckGamepadDeviceAccessMode::DirectOpen:
    {
        DeckGamepadDeviceOpenResult direct = openDirect(devpath);
        if (direct.ok()) {
            return direct;
        }

        if (direct.error.sysErrno == EACCES || direct.error.sysErrno == EPERM) {
            DeckGamepadDeviceOpenResult ro = openDirectReadOnly(devpath);
            if (ro.ok()) {
                return ro;
            }
        }

        return direct;
    }
    case DeckGamepadDeviceAccessMode::LogindTakeDevice:
        return openViaLogind(devpath);
    case DeckGamepadDeviceAccessMode::Auto:
    default: {
        DeckGamepadDeviceOpenResult direct = openDirect(devpath);
        if (direct.ok()) {
            return direct;
        }

        if (direct.error.sysErrno == EACCES || direct.error.sysErrno == EPERM) {
            DeckGamepadDeviceOpenResult logind = openViaLogind(devpath);
            if (logind.ok()) {
                return logind;
            }

            // logind 不可用：允许退化为只读打开，以便至少具备输入读取能力（rumble 可能不可用）。
            DeckGamepadDeviceOpenResult ro = openDirectReadOnly(devpath);
            if (ro.ok()) {
                return ro;
            }

            // direct 被拒绝且 logind 不可用：优先返回 logind 分支以便上层给出可操作引导。
            if (!logind.error.isOk()) {
                logind.error.message = QStringLiteral("Permission denied and logind TakeDevice failed");
            }
            return logind;
        }

        return direct;
    }
    }
}

DeckGamepadDeviceOpenResult DeviceAccessBroker::openDirect(const QString &devpath) const
{
    DeckGamepadDeviceOpenResult r;
    r.method = QStringLiteral("direct");

    errno = 0;
    const int fd = ::open(devpath.toUtf8().constData(), O_RDWR | O_NONBLOCK);
    if (fd < 0) {
        const int openErrno = errno;
        r.error.sysErrno = openErrno;
        r.error.context = QStringLiteral("open(%1)").arg(devpath);
        r.error.recoverable = m_config.enableAutoRetryOpen;
        if (openErrno == EACCES || openErrno == EPERM) {
            r.error.code = DeckGamepadErrorCode::PermissionDenied;
            r.error.message = QStringLiteral("Permission denied when opening gamepad device");
        } else if (openErrno == ENOENT) {
            r.error.code = DeckGamepadErrorCode::Io;
            r.error.message = QStringLiteral("Gamepad device node not found");
            r.error.recoverable = true;
        } else {
            r.error.code = DeckGamepadErrorCode::Io;
            r.error.message = QStringLiteral("Failed to open gamepad device");
        }
        return r;
    }

    r.fd = fd;
    return r;
}

DeckGamepadDeviceOpenResult DeviceAccessBroker::openDirectReadOnly(const QString &devpath) const
{
    DeckGamepadDeviceOpenResult r;
    r.method = QStringLiteral("direct_readonly");

    errno = 0;
    const int fd = ::open(devpath.toUtf8().constData(), O_RDONLY | O_NONBLOCK);
    if (fd < 0) {
        const int openErrno = errno;
        r.error.sysErrno = openErrno;
        r.error.context = QStringLiteral("open(ro,%1)").arg(devpath);
        r.error.recoverable = m_config.enableAutoRetryOpen;
        if (openErrno == EACCES || openErrno == EPERM) {
            r.error.code = DeckGamepadErrorCode::PermissionDenied;
            r.error.message = QStringLiteral("Permission denied when opening gamepad device (read-only)");
        } else if (openErrno == ENOENT) {
            r.error.code = DeckGamepadErrorCode::Io;
            r.error.message = QStringLiteral("Gamepad device node not found");
            r.error.recoverable = true;
        } else {
            r.error.code = DeckGamepadErrorCode::Io;
            r.error.message = QStringLiteral("Failed to open gamepad device (read-only)");
        }
        return r;
    }

    r.fd = fd;
    return r;
}

DeckGamepadDeviceOpenResult DeviceAccessBroker::openViaLogind(const QString &devpath) const
{
    DeckGamepadDeviceOpenResult r;
    r.method = QStringLiteral("logind");

#if defined(DECKGAMEPAD_ENABLE_LOGIND) && DECKGAMEPAD_ENABLE_LOGIND
    struct stat st { };
    if (::stat(devpath.toUtf8().constData(), &st) != 0) {
        r.error.code = DeckGamepadErrorCode::Io;
        r.error.sysErrno = errno;
        r.error.message = QStringLiteral("stat() failed for device node");
        r.error.context = QStringLiteral("logind.stat(%1)").arg(devpath);
        r.error.recoverable = m_config.enableAutoRetryOpen;
        return r;
    }

    const uint32_t majorNum = static_cast<uint32_t>(major(st.st_rdev));
    const uint32_t minorNum = static_cast<uint32_t>(minor(st.st_rdev));

    QDBusConnection bus = QDBusConnection::systemBus();
    if (!bus.isConnected()) {
        r.error.code = DeckGamepadErrorCode::NotSupported;
        r.error.message = QStringLiteral("System D-Bus not available");
        r.error.context = QStringLiteral("logind.systemBus");
        r.error.recoverable = true;
        return r;
    }

    QDBusInterface manager(QStringLiteral("org.freedesktop.login1"),
                           QStringLiteral("/org/freedesktop/login1"),
                           QStringLiteral("org.freedesktop.login1.Manager"),
                           bus);
    if (!manager.isValid()) {
        r.error.code = DeckGamepadErrorCode::NotSupported;
        r.error.message = QStringLiteral("logind manager not available");
        r.error.context = QStringLiteral("logind.Manager");
        r.error.recoverable = true;
        return r;
    }

    const uint32_t pid = static_cast<uint32_t>(QCoreApplication::applicationPid());
    QDBusReply<QDBusObjectPath> sessionReply = manager.call(QStringLiteral("GetSessionByPID"), pid);
    if (!sessionReply.isValid()) {
        r.error.code = DeckGamepadErrorCode::NotSupported;
        r.error.message = QStringLiteral("logind session not available");
        r.error.context = QStringLiteral("logind.GetSessionByPID");
        r.error.recoverable = true;
        return r;
    }

    const QString sessionPath = sessionReply.value().path();
    if (sessionPath.isEmpty()) {
        r.error.code = DeckGamepadErrorCode::NotSupported;
        r.error.message = QStringLiteral("logind session path is empty");
        r.error.context = QStringLiteral("logind.sessionPath");
        r.error.recoverable = true;
        return r;
    }

    QDBusInterface session(QStringLiteral("org.freedesktop.login1"),
                           sessionPath,
                           QStringLiteral("org.freedesktop.login1.Session"),
                           bus);
    if (!session.isValid()) {
        r.error.code = DeckGamepadErrorCode::NotSupported;
        r.error.message = QStringLiteral("logind session interface not available");
        r.error.context = QStringLiteral("logind.Session");
        r.error.recoverable = true;
        return r;
    }

    QDBusReply<QDBusUnixFileDescriptor> fdReply = session.call(QStringLiteral("TakeDevice"), majorNum, minorNum);
    if (!fdReply.isValid()) {
        r.error.code = DeckGamepadErrorCode::PermissionDenied;
        r.error.message = QStringLiteral("logind TakeDevice failed");
        r.error.context = QStringLiteral("logind.TakeDevice");
        r.error.recoverable = true;
        return r;
    }

    QDBusUnixFileDescriptor fd = fdReply.value();
    const int rawFd = fd.takeFileDescriptor();
    if (rawFd < 0) {
        r.error.code = DeckGamepadErrorCode::Io;
        r.error.message = QStringLiteral("logind returned invalid fd");
        r.error.context = QStringLiteral("logind.TakeDevice.fd");
        r.error.recoverable = true;
        return r;
    }

    // ensure non-blocking
    const int flags = ::fcntl(rawFd, F_GETFL);
    if (flags >= 0) {
        (void)::fcntl(rawFd, F_SETFL, flags | O_NONBLOCK);
    }

    r.fd = rawFd;
    r.releaseDevice = [bus, sessionPath, majorNum, minorNum]() mutable {
        QDBusInterface session(QStringLiteral("org.freedesktop.login1"),
                               sessionPath,
                               QStringLiteral("org.freedesktop.login1.Session"),
                               bus);
        if (session.isValid()) {
            (void)session.call(QStringLiteral("ReleaseDevice"), majorNum, minorNum);
        }
    };
    return r;
#else
    r.error.code = DeckGamepadErrorCode::NotSupported;
    r.error.message = QStringLiteral("logind support is not built (Qt6::DBus missing)");
    r.error.context = QStringLiteral("logind");
    r.error.recoverable = true;
    Q_UNUSED(devpath);
    return r;
#endif
}

DECKGAMEPAD_END_NAMESPACE
