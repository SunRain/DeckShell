// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "testprovider.h"

#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtTest/QSignalSpy>
#include <QtTest/QTest>

using namespace deckshell::deckgamepad;

class TestCoalesce : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void axisCoalesceDisabledPassThrough()
    {
        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        DeckGamepadRuntimeConfig cfg = service.runtimeConfig();
        cfg.axisCoalesceIntervalMs = 0;
        cfg.hatCoalesceIntervalMs = 0;
        QVERIFY(service.setRuntimeConfig(cfg));

        QVERIFY(service.start());

        QSignalSpy axisSpy(&service, &DeckGamepadService::axisEvent);

        DeckGamepadAxisEvent ev{ 0, 0, 0.1 };
        provider->emitAxisEvent(1, ev);
        ev.value = 0.2;
        provider->emitAxisEvent(1, ev);

        QCOMPARE(axisSpy.count(), 2);
    }

    void axisCoalesceEmitsOnlyLastValuePerAxis()
    {
        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        DeckGamepadRuntimeConfig cfg = service.runtimeConfig();
        cfg.axisCoalesceIntervalMs = 20;
        cfg.hatCoalesceIntervalMs = 0;
        QVERIFY(service.setRuntimeConfig(cfg));

        QVERIFY(service.start());

        QSignalSpy axisSpy(&service, &DeckGamepadService::axisEvent);

        DeckGamepadAxisEvent ev{ 0, 0, 0.1 };
        provider->emitAxisEvent(1, ev);
        ev.value = 0.2;
        provider->emitAxisEvent(1, ev);
        ev.value = 0.3;
        provider->emitAxisEvent(1, ev);

        QTest::qWait(40);

        QCOMPARE(axisSpy.count(), 1);
        const auto args = axisSpy.takeFirst();
        const auto out = qvariant_cast<DeckGamepadAxisEvent>(args.at(1));
        QCOMPARE(out.axis, 0u);
        QCOMPARE(out.value, 0.3);
    }

    void hatCoalesceEmitsOnlyLastValuePerHat()
    {
        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        DeckGamepadRuntimeConfig cfg = service.runtimeConfig();
        cfg.axisCoalesceIntervalMs = 0;
        cfg.hatCoalesceIntervalMs = 20;
        QVERIFY(service.setRuntimeConfig(cfg));

        QVERIFY(service.start());

        QSignalSpy hatSpy(&service, &DeckGamepadService::hatEvent);

        DeckGamepadHatEvent ev{ 0, 0, GAMEPAD_HAT_UP };
        provider->emitHatEvent(1, ev);
        ev.value = GAMEPAD_HAT_RIGHT;
        provider->emitHatEvent(1, ev);
        ev.value = GAMEPAD_HAT_LEFT;
        provider->emitHatEvent(1, ev);

        QTest::qWait(40);

        QCOMPARE(hatSpy.count(), 1);
        const auto args = hatSpy.takeFirst();
        const auto out = qvariant_cast<DeckGamepadHatEvent>(args.at(1));
        QCOMPARE(out.hat, 0u);
        QCOMPARE(out.value, static_cast<int32_t>(GAMEPAD_HAT_LEFT));
    }

    void hatCoalesceEmitsOnlyLastValuePerHatIndex()
    {
        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        DeckGamepadRuntimeConfig cfg = service.runtimeConfig();
        cfg.axisCoalesceIntervalMs = 0;
        cfg.hatCoalesceIntervalMs = 20;
        QVERIFY(service.setRuntimeConfig(cfg));

        QVERIFY(service.start());

        QSignalSpy hatSpy(&service, &DeckGamepadService::hatEvent);

        DeckGamepadHatEvent hat0{ 0, 0, GAMEPAD_HAT_UP };
        provider->emitHatEvent(1, hat0);
        hat0.value = GAMEPAD_HAT_LEFT;
        provider->emitHatEvent(1, hat0);

        DeckGamepadHatEvent hat1{ 0, 1, GAMEPAD_HAT_RIGHT };
        provider->emitHatEvent(1, hat1);
        hat1.value = GAMEPAD_HAT_DOWN;
        provider->emitHatEvent(1, hat1);

        QTest::qWait(40);

        QCOMPARE(hatSpy.count(), 2);

        QCOMPARE(hatSpy.at(0).at(0).toInt(), 1);
        const auto out0 = qvariant_cast<DeckGamepadHatEvent>(hatSpy.at(0).at(1));
        QCOMPARE(out0.hat, 0u);
        QCOMPARE(out0.value, static_cast<int32_t>(GAMEPAD_HAT_LEFT));

        QCOMPARE(hatSpy.at(1).at(0).toInt(), 1);
        const auto out1 = qvariant_cast<DeckGamepadHatEvent>(hatSpy.at(1).at(1));
        QCOMPARE(out1.hat, 1u);
        QCOMPARE(out1.value, static_cast<int32_t>(GAMEPAD_HAT_DOWN));
    }
};

QTEST_MAIN(TestCoalesce)

#include "test_coalesce.moc"
