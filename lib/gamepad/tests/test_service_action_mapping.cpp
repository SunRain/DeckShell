// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/core/deckgamepadaction.h>
#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtCore/QFile>
#include <QtCore/QJsonDocument>
#include <QtCore/QJsonObject>
#include <QtCore/QTemporaryDir>
#include <QtTest/QSignalSpy>
#include <QtTest/QTest>

#include "testprovider.h"

using namespace deckshell::deckgamepad;

class TestServiceActionMapping : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void defaultMappingButtonAEmitsNavAccept()
    {
        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        QVERIFY(service.start());

        QSignalSpy spy(&service, &DeckGamepadService::actionTriggered);

        DeckGamepadButtonEvent ev;
        ev.time_msec = 1;
        ev.button = static_cast<uint32_t>(GAMEPAD_BUTTON_A);
        ev.pressed = true;
        provider->emitButtonEvent(1, ev);

        QTRY_VERIFY_WITH_TIMEOUT(spy.count() >= 1, 200);
        const auto args = spy.takeFirst();
        QCOMPARE(args.at(0).toInt(), 1);
        QCOMPARE(args.at(1).toString(), QString::fromLatin1(DeckGamepadActionId::NavAccept));
        QCOMPARE(args.at(2).toBool(), true);
        QCOMPARE(args.at(3).toBool(), false);
    }

    void hatDerivesVirtualDpadButtons()
    {
        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        QVERIFY(service.start());

        QSignalSpy spy(&service, &DeckGamepadService::actionTriggered);

        DeckGamepadHatEvent hat;
        hat.time_msec = 1;
        hat.hat = 0;
        hat.value = GAMEPAD_HAT_UP;
        provider->emitHatEvent(2, hat);

        QTRY_VERIFY_WITH_TIMEOUT(spy.count() >= 1, 200);

        bool sawUpPress = false;
        for (const auto &row : spy) {
            if (row.at(0).toInt() == 2
                && row.at(1).toString() == QString::fromLatin1(DeckGamepadActionId::NavUp)
                && row.at(2).toBool()) {
                sawUpPress = true;
            }
        }
        QVERIFY(sawUpPress);
    }

    void hat1DoesNotDeriveVirtualDpadButtons()
    {
        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        QVERIFY(service.start());

        QSignalSpy spy(&service, &DeckGamepadService::actionTriggered);

        DeckGamepadHatEvent hat;
        hat.time_msec = 1;
        hat.hat = 1;
        hat.value = GAMEPAD_HAT_UP;
        provider->emitHatEvent(2, hat);

        QTest::qWait(50);
        QCOMPARE(spy.count(), 0);

        hat.time_msec = 2;
        hat.hat = 0;
        provider->emitHatEvent(2, hat);

        QTRY_VERIFY_WITH_TIMEOUT(spy.count() >= 1, 200);
    }

    void profileOverridesButtonBinding()
    {
        QTemporaryDir dir;
        QVERIFY(dir.isValid());

        const QString path = dir.filePath(QStringLiteral("action_mapping_profile.json"));
        {
            QJsonObject root;
            root[QStringLiteral("version")] = QStringLiteral("1.0");

            QJsonObject buttonBindings;
            buttonBindings[QString::number(static_cast<int>(GAMEPAD_BUTTON_A))] = QStringLiteral("nav.menu");
            root[QStringLiteral("button_bindings")] = buttonBindings;

            root[QStringLiteral("axis_bindings")] = QJsonObject{};

            QFile file(path);
            QVERIFY(file.open(QIODevice::WriteOnly | QIODevice::Truncate));
            file.write(QJsonDocument(root).toJson(QJsonDocument::Indented));
            file.close();
        }

        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        DeckGamepadRuntimeConfig cfg;
        cfg.actionMappingProfilePathOverride = path;
        QVERIFY(service.setRuntimeConfig(cfg));
        QVERIFY(service.start());

        QSignalSpy spy(&service, &DeckGamepadService::actionTriggered);

        DeckGamepadButtonEvent ev;
        ev.time_msec = 1;
        ev.button = static_cast<uint32_t>(GAMEPAD_BUTTON_A);
        ev.pressed = true;
        provider->emitButtonEvent(1, ev);

        QTRY_VERIFY_WITH_TIMEOUT(spy.count() >= 1, 200);
        QCOMPARE(spy.last().at(1).toString(), QStringLiteral("nav.menu"));
        QCOMPARE(spy.last().at(2).toBool(), true);
    }

    void navigationPriorityLeftStickOverDpad()
    {
        QTemporaryDir dir;
        QVERIFY(dir.isValid());

        const QString path = dir.filePath(QStringLiteral("action_mapping_profile.json"));
        {
            QJsonObject root;
            root[QStringLiteral("version")] = QStringLiteral("1.0");
            root[QStringLiteral("navigation_priority")] = QStringLiteral("left_stick_over_dpad");
            root[QStringLiteral("button_bindings")] = QJsonObject{};
            root[QStringLiteral("axis_bindings")] = QJsonObject{};

            QFile file(path);
            QVERIFY(file.open(QIODevice::WriteOnly | QIODevice::Truncate));
            file.write(QJsonDocument(root).toJson(QJsonDocument::Indented));
            file.close();
        }

        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        DeckGamepadRuntimeConfig cfg;
        cfg.actionMappingProfilePathOverride = path;
        QVERIFY(service.setRuntimeConfig(cfg));
        QVERIFY(service.start());

        QSignalSpy spy(&service, &DeckGamepadService::actionTriggered);

        DeckGamepadAxisEvent axis;
        axis.time_msec = 1;
        axis.axis = static_cast<uint32_t>(GAMEPAD_AXIS_LEFT_X);
        axis.value = 0.9;
        provider->emitAxisEvent(1, axis);

        QTRY_VERIFY_WITH_TIMEOUT(spy.count() >= 1, 200);

        bool sawRightPress = false;
        for (const auto &row : spy) {
            if (row.at(0).toInt() == 1
                && row.at(1).toString() == QString::fromLatin1(DeckGamepadActionId::NavRight)
                && row.at(2).toBool()) {
                sawRightPress = true;
            }
        }
        QVERIFY(sawRightPress);

        spy.clear();

        DeckGamepadHatEvent hat;
        hat.time_msec = 2;
        hat.hat = 0;
        hat.value = GAMEPAD_HAT_LEFT;
        provider->emitHatEvent(1, hat);

        QTest::qWait(50);
        QCOMPARE(spy.count(), 0);
    }

    void repeatConfigEmitsRepeatedForHeldDirection()
    {
        QTemporaryDir dir;
        QVERIFY(dir.isValid());

        const QString path = dir.filePath(QStringLiteral("action_mapping_profile.json"));
        {
            QJsonObject root;
            root[QStringLiteral("version")] = QStringLiteral("1.0");

            QJsonObject repeat;
            repeat[QStringLiteral("enabled")] = true;
            repeat[QStringLiteral("delay_ms")] = 0;
            repeat[QStringLiteral("interval_ms")] = 5;
            root[QStringLiteral("repeat")] = repeat;

            root[QStringLiteral("button_bindings")] = QJsonObject{};
            root[QStringLiteral("axis_bindings")] = QJsonObject{};

            QFile file(path);
            QVERIFY(file.open(QIODevice::WriteOnly | QIODevice::Truncate));
            file.write(QJsonDocument(root).toJson(QJsonDocument::Indented));
            file.close();
        }

        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        DeckGamepadRuntimeConfig cfg;
        cfg.actionMappingProfilePathOverride = path;
        QVERIFY(service.setRuntimeConfig(cfg));
        QVERIFY(service.start());

        QSignalSpy spy(&service, &DeckGamepadService::actionTriggered);

        DeckGamepadHatEvent hat;
        hat.time_msec = 1;
        hat.hat = 0;
        hat.value = GAMEPAD_HAT_UP;
        provider->emitHatEvent(3, hat);

        QTRY_VERIFY_WITH_TIMEOUT(spy.count() >= 2, 300);

        bool sawUpRepeat = false;
        for (const auto &row : spy) {
            if (row.at(0).toInt() == 3
                && row.at(1).toString() == QString::fromLatin1(DeckGamepadActionId::NavUp)
                && row.at(2).toBool()
                && row.at(3).toBool()) {
                sawUpRepeat = true;
                break;
            }
        }
        QVERIFY(sawUpRepeat);
    }
};

QTEST_MAIN(TestServiceActionMapping)

#include "test_service_action_mapping.moc"
