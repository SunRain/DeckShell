// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/providers/evdev/evdevprovider.h>
#include <deckshell/deckgamepad/core/deckgamepadaction.h>
#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtCore/QDateTime>
#include <QtCore/QFile>
#include <QtCore/QJsonDocument>
#include <QtCore/QJsonObject>
#include <QtCore/QSet>
#include <QtCore/QTemporaryDir>
#include <QtTest/QTest>

#include <vector>

#include "uinput_test_device.h"

#if defined(__linux__)
#include <fcntl.h>
#include <linux/input.h>
#include <unistd.h>
#endif

using namespace deckshell::deckgamepad;

class TestMultiDeviceHotplugStress final : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void addRemove_multipleDevices_keepsStateConsistent()
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

        QTemporaryDir dir;
        QVERIFY(dir.isValid());

        const QString profilePath = dir.filePath(QStringLiteral("action_mapping_profile.json"));
        {
            QJsonObject root;
            root[QStringLiteral("version")] = QStringLiteral("1.0");

            QJsonObject repeat;
            repeat[QStringLiteral("enabled")] = true;
            repeat[QStringLiteral("delay_ms")] = 0;
            repeat[QStringLiteral("interval_ms")] = 10;
            root[QStringLiteral("repeat")] = repeat;

            root[QStringLiteral("button_bindings")] = QJsonObject{};
            root[QStringLiteral("axis_bindings")] = QJsonObject{};

            QFile file(profilePath);
            QVERIFY(file.open(QIODevice::WriteOnly | QIODevice::Truncate));
            file.write(QJsonDocument(root).toJson(QJsonDocument::Indented));
            file.close();
        }

        DeckGamepadRuntimeConfig cfg = service.runtimeConfig();
        cfg.providerSelection = DeckGamepadProviderSelection::EvdevUdev;
        cfg.deviceAccessMode = DeckGamepadDeviceAccessMode::DirectOpen;
        cfg.capturePolicy = DeckGamepadCapturePolicy::Always;
        cfg.grabMode = DeckGamepadEvdevGrabMode::Shared;
        cfg.enableAutoRetryOpen = false;
        cfg.enableLegacyDeckShellPaths = false;
        cfg.actionMappingProfilePathOverride = profilePath;

        QVERIFY(service.setRuntimeConfig(cfg));
        QVERIFY(service.start());

        auto toSet = [](const QList<int> &values) {
            QSet<int> out;
            for (int v : values) {
                out.insert(v);
            }
            return out;
        };

        const QSet<int> baselineKnown = toSet(service.knownGamepads());
        const QSet<int> baselineConnected = toSet(service.connectedGamepads());

        QHash<QString, int> idByName;
        QObject::connect(&service, &DeckGamepadService::gamepadConnected, &service, [&](int id, const QString &name) {
            idByName.insert(name, id);
        });

        QSet<int> disconnectedIds;
        QObject::connect(&service, &DeckGamepadService::gamepadDisconnected, &service, [&](int id) {
            disconnectedIds.insert(id);
        });

        QHash<int, int> navUpRepeatCountById;
        QObject::connect(&service,
                         &DeckGamepadService::actionTriggered,
                         &service,
                         [&](int id, const QString &actionId, bool pressed, bool repeated) {
                             Q_UNUSED(pressed);
                             if (!repeated) {
                                 return;
                             }
                             if (actionId == QString::fromLatin1(DeckGamepadActionId::NavUp)) {
                                 navUpRepeatCountById[id]++;
                             }
                         });

        static constexpr int kIterations = 3;
        static constexpr int kDevicesPerIteration = 2;

        for (int iter = 0; iter < kIterations; ++iter) {
            std::vector<UinputTestDevice> devices;
            devices.reserve(kDevicesPerIteration);
            QStringList names;
            QSet<int> idsThisRound;

            for (int i = 0; i < kDevicesPerIteration; ++i) {
                const QString name = QStringLiteral("DeckGamepadHotplug-%1-%2-%3")
                                         .arg(iter)
                                         .arg(i)
                                         .arg(QDateTime::currentMSecsSinceEpoch());
                names << name;
                UinputTestDevice dev = UinputTestDevice::createGamepad(name);
                if (!dev.isValid()) {
                    QSKIP("failed to create uinput gamepad device");
                }
                devices.push_back(std::move(dev));
            }

            for (const QString &name : names) {
                QTRY_VERIFY_WITH_TIMEOUT(idByName.contains(name), 5000);
                idsThisRound.insert(idByName.value(name));
            }

            for (int i = 0; i < kDevicesPerIteration; ++i) {
                const int id = idByName.value(names.at(i), -1);
                QVERIFY(id >= 0);

                // Press/hold hat-up to start repeat; then remove device without releasing to verify cleanup.
                QVERIFY(devices.at(i).emitAbs(ABS_HAT0Y, -1));
                QVERIFY(devices.at(i).sync());
                QTRY_VERIFY_WITH_TIMEOUT(navUpRepeatCountById.value(id, 0) >= 1, 1500);
            }

            const QSet<int> knownNow = toSet(service.knownGamepads());
            const QSet<int> connectedNow = toSet(service.connectedGamepads());

            QVERIFY(connectedNow.size() >= baselineConnected.size() + idsThisRound.size());
            for (int id : idsThisRound) {
                QVERIFY(knownNow.contains(id));
                QVERIFY(connectedNow.contains(id));
            }

            // Destroy devices and wait for disconnect notifications.
            devices.clear();
            for (int id : idsThisRound) {
                QTRY_VERIFY_WITH_TIMEOUT(disconnectedIds.contains(id), 5000);
            }

            for (int id : idsThisRound) {
                const int repeatCountAtDisconnect = navUpRepeatCountById.value(id, 0);
                QTRY_VERIFY_WITH_TIMEOUT(!toSet(service.connectedGamepads()).contains(id), 5000);
                QTest::qWait(200);
                QCOMPARE(navUpRepeatCountById.value(id, 0), repeatCountAtDisconnect);
            }

            QTRY_VERIFY_WITH_TIMEOUT([&] {
                const QSet<int> knownAfter = toSet(service.knownGamepads());
                for (int id : idsThisRound) {
                    if (knownAfter.contains(id)) {
                        return false;
                    }
                }
                return true;
            }(),
                                     5000);
        }

        const QSet<int> finalKnown = toSet(service.knownGamepads());
        const QSet<int> finalConnected = toSet(service.connectedGamepads());

        // After stress iterations, at minimum we must not retain the transient uinput devices.
        QVERIFY(finalConnected == baselineConnected);
        QVERIFY(finalKnown == baselineKnown);

        service.stop();
#endif
    }
};

QTEST_MAIN(TestMultiDeviceHotplugStress)
#include "test_multi_device_hotplug_stress.moc"
