// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/core/deckgamepadaction.h>
#include <deckshell/deckgamepad/mapping/deckgamepadcalibrationstore.h>
#include <deckshell/deckgamepad/providers/evdev/evdevprovider.h>
#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtCore/QDateTime>
#include <QtCore/QTemporaryDir>
#include <QtTest/QTest>

#include "uinput_test_device.h"

#if defined(__linux__)
#include <fcntl.h>
#include <linux/input.h>
#include <unistd.h>
#endif

using namespace deckshell::deckgamepad;

class TestCalibrationEvdevIntegration final : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void calibrationOverride_affectsAxisNormalizationAndActionThreshold()
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

        const QString calibrationPath = dir.filePath(QStringLiteral("calibration.json"));
        const QString guid = QStringLiteral("03000000341200007856000001000000");

        {
            CalibrationData data;
            DeviceCalibration dev;
            dev.name = QStringLiteral("DeckGamepadCalibrationTest");
            dev.backend = QStringLiteral("evdev");
            dev.updatedAt = QDateTime::currentDateTimeUtc();

            AxisCalibration cal;
            cal.mode = AxisCalibrationMode::MinMax;
            cal.min = -0.5f;
            cal.max = 0.5f;
            dev.axes.insert(GAMEPAD_AXIS_LEFT_X, cal);

            data.devices.insert(guid, dev);

            JsonCalibrationStore store(calibrationPath);
            QVERIFY(store.save(data));
        }

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
        cfg.calibrationPathOverride = calibrationPath;

        QVERIFY(service.setRuntimeConfig(cfg));
        QVERIFY(service.start());

        const QString name = QStringLiteral("DeckGamepadCalibrationTest-%1").arg(QDateTime::currentMSecsSinceEpoch());

        int deviceId = -1;
        QObject::connect(&service, &DeckGamepadService::gamepadConnected, &service, [&](int id, const QString &n) {
            if (n == name) {
                deviceId = id;
            }
        });

        DeckGamepadAxisEvent lastAxis{};
        bool sawAxis = false;
        QObject::connect(&service, &DeckGamepadService::axisEvent, &service, [&](int id, DeckGamepadAxisEvent ev) {
            if (id != deviceId) {
                return;
            }
            lastAxis = ev;
            sawAxis = true;
        });

        bool sawNavRightPress = false;
        bool sawNavRightRelease = false;
        QObject::connect(&service,
                         &DeckGamepadService::actionTriggered,
                         &service,
                         [&](int id, const QString &actionId, bool pressed, bool repeated) {
                             Q_UNUSED(repeated);
                             if (id != deviceId) {
                                 return;
                             }
                             if (actionId == QString::fromLatin1(DeckGamepadActionId::NavRight)) {
                                 if (pressed) {
                                     sawNavRightPress = true;
                                 } else {
                                     sawNavRightRelease = true;
                                 }
                             }
                         });

        UinputTestDevice dev = UinputTestDevice::createGamepad(name);
        if (!dev.isValid()) {
            QSKIP("failed to create uinput gamepad device");
        }

        QTRY_VERIFY_WITH_TIMEOUT(deviceId >= 0, 5000);
        QCOMPARE(service.deviceGuid(deviceId), guid);

        sawAxis = false;
        QVERIFY(dev.emitAbs(ABS_X, 8192));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sawAxis, 1500);
        QCOMPARE(static_cast<int>(lastAxis.axis), static_cast<int>(GAMEPAD_AXIS_LEFT_X));
        QVERIFY(lastAxis.value > 0.45);
        QTRY_VERIFY_WITH_TIMEOUT(sawNavRightPress, 1500);

        sawAxis = false;
        QVERIFY(dev.emitAbs(ABS_X, 0));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sawAxis, 1500);
        QTRY_VERIFY_WITH_TIMEOUT(sawNavRightRelease, 1500);

        dev = UinputTestDevice{};
        service.stop();
#endif
    }
};

QTEST_MAIN(TestCalibrationEvdevIntegration)
#include "test_calibration_evdev_integration.moc"
