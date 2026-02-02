// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/core/deckgamepadaction.h>
#include <deckshell/deckgamepad/providers/evdev/evdevprovider.h>
#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtCore/QDateTime>
#include <QtTest/QTest>

#include "uinput_test_device.h"

#if defined(__linux__)
#include <fcntl.h>
#include <unistd.h>
#include <linux/input.h>
#endif

using namespace deckshell::deckgamepad;

class TestUinputUdevIntegration final : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void hotplugAndEvents_areObserved()
    {
#if !defined(__linux__)
        QSKIP("requires Linux uinput/udev");
#else
        const int probeFd = ::open("/dev/uinput", O_RDWR | O_NONBLOCK);
        if (probeFd < 0) {
            QSKIP("missing /dev/uinput access");
        }
        (void)::close(probeFd);

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

        QVERIFY(service.setRuntimeConfig(cfg));
        QVERIFY(service.start());

        const QString name = QStringLiteral("DeckGamepadTest-%1").arg(QDateTime::currentMSecsSinceEpoch());

        int deviceId = -1;
        QObject::connect(&service, &DeckGamepadService::gamepadConnected, &service, [&](int id, const QString &n) {
            if (n == name) {
                deviceId = id;
            }
        });

        bool sawDisconnected = false;
        QObject::connect(&service, &DeckGamepadService::gamepadDisconnected, &service, [&](int id) {
            if (id == deviceId) {
                sawDisconnected = true;
            }
        });

        DeckGamepadButtonEvent lastButton{};
        bool sawButton = false;
        QObject::connect(&service, &DeckGamepadService::buttonEvent, &service, [&](int id, DeckGamepadButtonEvent ev) {
            if (id == deviceId) {
                lastButton = ev;
                sawButton = true;
            }
        });

        DeckGamepadAxisEvent lastAxis{};
        bool sawAxis = false;
        QObject::connect(&service, &DeckGamepadService::axisEvent, &service, [&](int id, DeckGamepadAxisEvent ev) {
            if (id == deviceId) {
                lastAxis = ev;
                sawAxis = true;
            }
        });

        DeckGamepadHatEvent lastHat{};
        bool sawHat = false;
        QObject::connect(&service, &DeckGamepadService::hatEvent, &service, [&](int id, DeckGamepadHatEvent ev) {
            if (id == deviceId) {
                lastHat = ev;
                sawHat = true;
            }
        });

        QString lastActionId;
        bool lastActionPressed = false;
        bool sawNavUpPress = false;
        bool sawNavUpRelease = false;
        QObject::connect(&service,
                         &DeckGamepadService::actionTriggered,
                         &service,
                         [&](int id, const QString &actionId, bool pressed, bool repeated) {
                             Q_UNUSED(repeated);
                             if (id != deviceId) {
                                 return;
                             }
                             lastActionId = actionId;
                             lastActionPressed = pressed;
                             if (actionId == QString::fromLatin1(DeckGamepadActionId::NavUp)) {
                                 if (pressed) {
                                     sawNavUpPress = true;
                                 } else {
                                     sawNavUpRelease = true;
                                 }
                             }
                         });

        UinputTestDevice dev = UinputTestDevice::createGamepad(name);
        if (!dev.isValid()) {
            QSKIP("failed to create uinput gamepad device");
        }

        QTRY_VERIFY_WITH_TIMEOUT(deviceId >= 0, 5000);

        QVERIFY(dev.emitKey(BTN_SOUTH, 1));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sawButton, 1500);
        QCOMPARE(static_cast<int>(lastButton.button), static_cast<int>(GAMEPAD_BUTTON_A));
        QVERIFY(lastButton.pressed);

        sawButton = false;
        QVERIFY(dev.emitAbs(ABS_X, 32767));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sawAxis, 1500);
        QCOMPARE(static_cast<int>(lastAxis.axis), static_cast<int>(GAMEPAD_AXIS_LEFT_X));
        QVERIFY(lastAxis.value > 0.9);

        // Reset the axis back to neutral before asserting on hat-driven navigation.
        // Otherwise, a held NavRight action (including repeats) can race with the NavUp assertion.
        sawAxis = false;
        QVERIFY(dev.emitAbs(ABS_X, 0));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sawAxis, 1500);
        lastActionId.clear();
        lastActionPressed = false;

        QVERIFY(dev.emitAbs(ABS_HAT0Y, -1));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sawHat, 1500);
        QVERIFY((lastHat.value & GAMEPAD_HAT_UP) != 0);
        QTRY_VERIFY_WITH_TIMEOUT(sawNavUpPress, 1500);
        QCOMPARE(lastActionId, QString::fromLatin1(DeckGamepadActionId::NavUp));
        QVERIFY(lastActionPressed);

        QVERIFY(dev.emitAbs(ABS_HAT0Y, 0));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sawNavUpRelease, 1500);

        dev = UinputTestDevice{};
        QTRY_VERIFY_WITH_TIMEOUT(sawDisconnected, 5000);

        service.stop();
#endif
    }
};

QTEST_MAIN(TestUinputUdevIntegration)
#include "test_uinput_udev_integration.moc"
