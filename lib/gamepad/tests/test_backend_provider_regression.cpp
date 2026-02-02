// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/backend/deckgamepadbackend.h>

#include <QtCore/QFile>
#include <QtCore/QTemporaryDir>
#include <QtTest/QSignalSpy>
#include <QtTest/QTest>

#include <errno.h>

using namespace deckshell::deckgamepad;

namespace deckshell::deckgamepad {
class DeckGamepadBackendTestHooks
{
public:
    static void addKnownDevice(DeckGamepadBackend &backend,
                              int deviceId,
                              const QString &devpath,
                              DeckGamepadDeviceAvailability availability = DeckGamepadDeviceAvailability::Unavailable)
    {
        DeckGamepadBackend::KnownDevice known;
        known.devpath = devpath;
        known.availability = availability;
        backend.m_knownDevices.insert(deviceId, known);
    }

    static void addConnectedDevice(DeckGamepadBackend &backend, int deviceId, DeckGamepadDevice *device)
    {
        backend.m_devices.insert(deviceId, device);
    }

    static void setRunning(DeckGamepadBackend &backend, bool running) { backend.m_running = running; }

    static bool tryOpenGamepad(DeckGamepadBackend &backend, int deviceId, const QString &devpath)
    {
        return backend.tryOpenGamepad(deviceId, devpath);
    }

    static void closeGamepad(DeckGamepadBackend &backend, int deviceId) { backend.closeGamepad(deviceId); }

    static void handleSessionGateActiveChanged(DeckGamepadBackend &backend, bool active)
    {
        backend.handleSessionGateActiveChanged(active);
    }
};
}

class TestBackendProviderRegression : public QObject
{
    Q_OBJECT

private:
    static QString createFileWithPermissions(const QTemporaryDir &dir, const QString &name, QFileDevice::Permissions perm)
    {
        const QString path = dir.filePath(name);
        QFile file(path);
        if (!file.open(QIODevice::WriteOnly)) {
            return QString{};
        }
        (void)file.write("x");
        file.close();

        if (!QFile::setPermissions(path, perm)) {
            return QString{};
        }
        return path;
    }

private Q_SLOTS:
    void permissionDenied_openIsReportedAndDeviceRemainsKnown()
    {
        QTemporaryDir dir;
        QVERIFY(dir.isValid());

        const QString devpath = createFileWithPermissions(dir, QStringLiteral("no-permission"), QFileDevice::Permissions{});
        QVERIFY(!devpath.isEmpty());

        DeckGamepadBackend backend;

        DeckGamepadRuntimeConfig cfg = backend.runtimeConfig();
        cfg.deviceAccessMode = DeckGamepadDeviceAccessMode::DirectOpen;
        cfg.enableAutoRetryOpen = false;
        cfg.grabMode = DeckGamepadEvdevGrabMode::Shared;
        backend.setRuntimeConfig(cfg);

        DeckGamepadBackendTestHooks::addKnownDevice(backend, 1, devpath);

        QSignalSpy errSpy(&backend, &DeckGamepadBackend::deviceErrorChanged);

        QVERIFY(!DeckGamepadBackendTestHooks::tryOpenGamepad(backend, 1, devpath));

        QVERIFY(errSpy.count() >= 1);
        QCOMPARE(errSpy.last().at(0).toInt(), 1);
        const auto err = qvariant_cast<DeckGamepadError>(errSpy.last().at(1));
        QCOMPARE(err.code, DeckGamepadErrorCode::PermissionDenied);
        QVERIFY(err.sysErrno == EACCES || err.sysErrno == EPERM);
        QVERIFY(err.context.startsWith(QStringLiteral("open(")));

        QVERIFY(backend.knownGamepads().contains(1));
        QCOMPARE(backend.deviceAvailability(1), DeckGamepadDeviceAvailability::Unavailable);
        QCOMPARE(backend.deviceLastError(1).code, DeckGamepadErrorCode::PermissionDenied);
    }

    void evdevGrabFailure_isReportedAsRecoverableIoError()
    {
        QTemporaryDir dir;
        QVERIFY(dir.isValid());

        const QString devpath = createFileWithPermissions(dir,
                                                          QStringLiteral("regular-file"),
                                                          QFileDevice::ReadOwner | QFileDevice::WriteOwner);
        QVERIFY(!devpath.isEmpty());

        DeckGamepadBackend backend;

        DeckGamepadRuntimeConfig cfg = backend.runtimeConfig();
        cfg.deviceAccessMode = DeckGamepadDeviceAccessMode::DirectOpen;
        cfg.enableAutoRetryOpen = true;
        cfg.grabMode = DeckGamepadEvdevGrabMode::Exclusive;
        backend.setRuntimeConfig(cfg);

        DeckGamepadBackendTestHooks::addKnownDevice(backend, 2, devpath);

        QVERIFY(!DeckGamepadBackendTestHooks::tryOpenGamepad(backend, 2, devpath));

        const DeckGamepadError err = backend.deviceLastError(2);
        QCOMPARE(err.code, DeckGamepadErrorCode::Io);
        QCOMPARE(err.context, QStringLiteral("EVIOCGRAB"));
        QVERIFY(err.sysErrno != 0);
        QVERIFY(err.recoverable);
    }

    void evdevGrabFailure_autoMode_fallsBackToShared()
    {
        QTemporaryDir dir;
        QVERIFY(dir.isValid());

        const QString devpath = createFileWithPermissions(dir,
                                                          QStringLiteral("regular-file-auto"),
                                                          QFileDevice::ReadOwner | QFileDevice::WriteOwner);
        QVERIFY(!devpath.isEmpty());

        DeckGamepadBackend backend;

        DeckGamepadRuntimeConfig cfg = backend.runtimeConfig();
        cfg.deviceAccessMode = DeckGamepadDeviceAccessMode::DirectOpen;
        cfg.enableAutoRetryOpen = false;
        cfg.grabMode = DeckGamepadEvdevGrabMode::Auto;
        backend.setRuntimeConfig(cfg);

        DeckGamepadBackendTestHooks::addKnownDevice(backend, 5, devpath);

        QVERIFY(DeckGamepadBackendTestHooks::tryOpenGamepad(backend, 5, devpath));
        QVERIFY(backend.connectedGamepads().contains(5));
        QCOMPARE(backend.deviceAvailability(5), DeckGamepadDeviceAvailability::Available);

        const DeckGamepadError err = backend.deviceLastError(5);
        QCOMPARE(err.code, DeckGamepadErrorCode::Io);
        QCOMPARE(err.context, QStringLiteral("EVIOCGRAB"));
        QVERIFY(err.sysErrno != 0);
    }

    void sessionGateInactive_closesDevicesAndMarksUnavailable()
    {
        DeckGamepadBackend backend;
        const QString devpath = QStringLiteral("/dev/input/event999");

        DeckGamepadBackendTestHooks::addKnownDevice(backend,
                                                    3,
                                                    devpath,
                                                    DeckGamepadDeviceAvailability::Available);

        auto *device = new DeckGamepadDevice(3, devpath, backend.sdlDb(), &backend);
        DeckGamepadBackendTestHooks::addConnectedDevice(backend, 3, device);

        DeckGamepadBackendTestHooks::setRunning(backend, true);

        QSignalSpy disconnectedSpy(&backend, &DeckGamepadBackend::gamepadDisconnected);
        QSignalSpy availSpy(&backend, &DeckGamepadBackend::deviceAvailabilityChanged);
        QSignalSpy errSpy(&backend, &DeckGamepadBackend::deviceErrorChanged);

        DeckGamepadBackendTestHooks::handleSessionGateActiveChanged(backend, false);

        QVERIFY(disconnectedSpy.count() >= 1);
        QCOMPARE(disconnectedSpy.last().at(0).toInt(), 3);

        QVERIFY(!backend.connectedGamepads().contains(3));
        QCOMPARE(backend.deviceAvailability(3), DeckGamepadDeviceAvailability::Unavailable);

        QVERIFY(availSpy.count() >= 1);
        QCOMPARE(availSpy.last().at(0).toInt(), 3);
        QCOMPARE(static_cast<DeckGamepadDeviceAvailability>(availSpy.last().at(1).toInt()),
                 DeckGamepadDeviceAvailability::Unavailable);

        QVERIFY(errSpy.count() >= 1);
        const auto err = qvariant_cast<DeckGamepadError>(errSpy.last().at(1));
        QCOMPARE(err.code, DeckGamepadErrorCode::Io);
        QCOMPARE(err.context, QStringLiteral("SessionGate"));
    }

    void hotUnplug_closeGamepadEmitsDisconnected()
    {
        DeckGamepadBackend backend;
        const QString devpath = QStringLiteral("/dev/input/event998");

        DeckGamepadBackendTestHooks::addKnownDevice(backend, 4, devpath, DeckGamepadDeviceAvailability::Available);

        auto *device = new DeckGamepadDevice(4, devpath, backend.sdlDb(), &backend);
        DeckGamepadBackendTestHooks::addConnectedDevice(backend, 4, device);

        QSignalSpy disconnectedSpy(&backend, &DeckGamepadBackend::gamepadDisconnected);

        DeckGamepadBackendTestHooks::closeGamepad(backend, 4);

        QVERIFY(disconnectedSpy.count() >= 1);
        QCOMPARE(disconnectedSpy.last().at(0).toInt(), 4);
        QVERIFY(!backend.connectedGamepads().contains(4));
    }
};

QTEST_MAIN(TestBackendProviderRegression)
#include "test_backend_provider_regression.moc"
