// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/core/deckgamepadaction.h>
#include <deckshell/deckgamepad/providers/evdev/evdevprovider.h>
#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtCore/QDateTime>
#include <QtCore/QFile>
#include <QtCore/QTemporaryDir>
#include <QtTest/QTest>

#include "uinput_test_device.h"

#if defined(__linux__)
#include <fcntl.h>
#include <linux/input.h>
#include <unistd.h>
#endif

using namespace deckshell::deckgamepad;

class TestSdlDbOverrideEvdevIntegration final : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void sdlDbOverride_isAppliedToEvdevChain()
    {
#if !defined(__linux__)
        QSKIP("requires Linux uinput/udev");
#else
        const int probeFd = ::open("/dev/uinput", O_RDWR | O_NONBLOCK);
        if (probeFd < 0) {
            QSKIP("missing /dev/uinput access");
        }
        (void)::close(probeFd);

        QTemporaryDir dir;
        QVERIFY(dir.isValid());

        // UinputTestDevice uses vendor=0x1234, product=0x5678, bus=USB, version=1 (see uinput_test_device.cpp).
        // SDL GUID is composed as: bustype/vendor/product/version (16-bit LE words with padding).
        static const QString guid = QStringLiteral("03000000341200007856000001000000");

        const QString dbFile = dir.filePath(QStringLiteral("gamecontrollerdb.txt"));
        QFile file(dbFile);
        QVERIFY(file.open(QIODevice::WriteOnly | QIODevice::Truncate | QIODevice::Text));

        // Cover: inverted axis (~a1) and half-axis mapping (-a0/+a0) as D-pad buttons.
        file.write(
            (guid
             + QStringLiteral(",DeckGamepad Test,lefty:~a1,dpup:-a0,dpdown:+a0,platform:Linux\n"))
                .toUtf8());
        file.close();

        // DeckGamepadService 会接管 provider 的 QObject 生命周期（setParent(this) + 析构时 delete），
        // 因此这里必须使用堆对象，避免栈对象被 delete 导致崩溃。
        auto *provider = new EvdevProvider();
        DeckGamepadService service(provider);

        DeckGamepadRuntimeConfig cfg = service.runtimeConfig();
        cfg.providerSelection = DeckGamepadProviderSelection::EvdevUdev;
        cfg.deviceAccessMode = DeckGamepadDeviceAccessMode::DirectOpen;
        cfg.capturePolicy = DeckGamepadCapturePolicy::Always;
        cfg.grabMode = DeckGamepadEvdevGrabMode::Shared;
        cfg.enableAutoRetryOpen = false;
        cfg.enableLegacyDeckShellPaths = false;
        cfg.sdlDbPathOverride = dbFile;

        QVERIFY(service.setRuntimeConfig(cfg));
        QVERIFY(service.start());

        const QString name = QStringLiteral("DeckGamepadTest-%1").arg(QDateTime::currentMSecsSinceEpoch());

        int deviceId = -1;
        QObject::connect(&service, &DeckGamepadService::gamepadConnected, &service, [&](int id, const QString &n) {
            if (n == name) {
                deviceId = id;
            }
        });

        UinputTestDevice dev = UinputTestDevice::createGamepad(name);
        if (!dev.isValid()) {
            QSKIP("failed to create uinput gamepad device");
        }

        QTRY_VERIFY_WITH_TIMEOUT(deviceId >= 0, 5000);

        DeckGamepadAxisEvent lastAxis{};
        bool sawAxis = false;
        QObject::connect(&service, &DeckGamepadService::axisEvent, &service, [&](int id, DeckGamepadAxisEvent ev) {
            if (id == deviceId) {
                lastAxis = ev;
                sawAxis = true;
            }
        });

        bool sawNavUpPress = false;
        bool sawNavUpRelease = false;
        bool sawNavDownPress = false;
        bool sawNavDownRelease = false;
        QObject::connect(&service,
                         &DeckGamepadService::actionTriggered,
                         &service,
                         [&](int id, const QString &actionId, bool pressed, bool repeated) {
                             Q_UNUSED(repeated);
                             if (id != deviceId) {
                                 return;
                             }
                             if (actionId == QString::fromLatin1(DeckGamepadActionId::NavUp)) {
                                 if (pressed) {
                                     sawNavUpPress = true;
                                 } else {
                                     sawNavUpRelease = true;
                                 }
                             }
                             if (actionId == QString::fromLatin1(DeckGamepadActionId::NavDown)) {
                                 if (pressed) {
                                     sawNavDownPress = true;
                                 } else {
                                     sawNavDownRelease = true;
                                 }
                             }
                         });

        // Inverted axis: ABS_Y max should become ~-1.0.
        sawAxis = false;
        QVERIFY(dev.emitAbs(ABS_Y, 32767));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sawAxis, 1500);
        QCOMPARE(static_cast<int>(lastAxis.axis), static_cast<int>(GAMEPAD_AXIS_LEFT_Y));
        QVERIFY(lastAxis.value < -0.9);

        // Reset the axis back to neutral before validating half-axis-driven buttons.
        // Otherwise the navigation preset may keep NavUp pressed due to LEFT_Y being held.
        sawAxis = false;
        QVERIFY(dev.emitAbs(ABS_Y, 0));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sawAxis, 1500);
        QTest::qWait(30);

        // Reset action tracking for the half-axis assertions.
        sawNavUpPress = false;
        sawNavUpRelease = false;
        sawNavDownPress = false;
        sawNavDownRelease = false;

        // Half-axis as buttons: ABS_X negative/positive should trigger NavUp/NavDown.
        QVERIFY(dev.emitAbs(ABS_X, -32768));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sawNavUpPress, 1500);

        QVERIFY(dev.emitAbs(ABS_X, 0));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sawNavUpRelease, 1500);

        QVERIFY(dev.emitAbs(ABS_X, 32767));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sawNavDownPress, 1500);

        QVERIFY(dev.emitAbs(ABS_X, 0));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sawNavDownRelease, 1500);

        dev = UinputTestDevice{};
        service.stop();
#endif
    }
};

QTEST_MAIN(TestSdlDbOverrideEvdevIntegration)
#include "test_sdl_db_override_evdev_integration.moc"
