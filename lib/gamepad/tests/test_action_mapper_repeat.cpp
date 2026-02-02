// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/extras/deckgamepadactionmapper.h>

#include <QtTest/QSignalSpy>
#include <QtTest/QTest>

using namespace deckshell::deckgamepad;

class TestActionMapperRepeat : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void delayIntervalRepeat()
    {
        DeckGamepadActionMapper mapper;
        mapper.setRepeatEnabled(true);
        mapper.setRepeatDelayMs(80);
        mapper.setRepeatIntervalMs(30);

        QSignalSpy spy(&mapper, &DeckGamepadActionMapper::actionTriggered);

        mapper.processButton(GAMEPAD_BUTTON_DPAD_RIGHT, true, 1);
        QCOMPARE(spy.count(), 1);
        QCOMPARE(spy.first().at(0).toString(), QString::fromLatin1(DeckGamepadActionId::NavRight));
        QCOMPARE(spy.first().at(1).toBool(), true);
        QCOMPARE(spy.first().at(2).toBool(), false); // repeated

        spy.clear();

        QTest::qWait(40);
        QCOMPARE(spy.count(), 0); // repeatDelay 未到，不能提前输出 repeated

        QTRY_VERIFY_WITH_TIMEOUT(spy.count() >= 1, 500);
        QVERIFY(spy.first().at(2).toBool()); // repeated=true
        QCOMPARE(spy.first().at(0).toString(), QString::fromLatin1(DeckGamepadActionId::NavRight));
        QCOMPARE(spy.first().at(1).toBool(), true);
    }

    void repeatStopsAfterRelease()
    {
        DeckGamepadActionMapper mapper;
        mapper.setRepeatEnabled(true);
        mapper.setRepeatDelayMs(60);
        mapper.setRepeatIntervalMs(25);

        QSignalSpy spy(&mapper, &DeckGamepadActionMapper::actionTriggered);

        mapper.processButton(GAMEPAD_BUTTON_DPAD_UP, true, 1);
        QTRY_VERIFY_WITH_TIMEOUT(spy.count() >= 2, 500); // pressed + repeated（至少一次）

        spy.clear();
        mapper.processButton(GAMEPAD_BUTTON_DPAD_UP, false, 2);
        QTRY_VERIFY_WITH_TIMEOUT(spy.count() >= 1, 200); // release
        QCOMPARE(spy.last().at(0).toString(), QString::fromLatin1(DeckGamepadActionId::NavUp));
        QCOMPARE(spy.last().at(1).toBool(), false);

        spy.clear();
        QTest::qWait(120);
        QCOMPARE(spy.count(), 0); // 已释放，不应再输出 repeated
    }

    void directionSwitchResetsRepeatTiming()
    {
        DeckGamepadActionMapper mapper;
        mapper.setRepeatEnabled(true);
        mapper.setRepeatDelayMs(80);
        mapper.setRepeatIntervalMs(30);

        QSignalSpy spy(&mapper, &DeckGamepadActionMapper::actionTriggered);

        mapper.processAxis(GAMEPAD_AXIS_LEFT_X, 0.9, 1); // Right
        QTRY_VERIFY_WITH_TIMEOUT(spy.count() >= 1, 200);
        QCOMPARE(spy.last().at(0).toString(), QString::fromLatin1(DeckGamepadActionId::NavRight));
        QCOMPARE(spy.last().at(1).toBool(), true);
        QCOMPARE(spy.last().at(2).toBool(), false);

        spy.clear();

        // 方向切换：Right -> Left（不回中，直接翻转）
        mapper.processAxis(GAMEPAD_AXIS_LEFT_X, -0.9, 2);
        QTRY_VERIFY_WITH_TIMEOUT(spy.count() >= 2, 200); // Right release + Left press

        bool sawLeftPress = false;
        for (const auto &row : spy) {
            if (row.at(0).toString() == QString::fromLatin1(DeckGamepadActionId::NavLeft) &&
                row.at(1).toBool() && !row.at(2).toBool()) {
                sawLeftPress = true;
            }
        }
        QVERIFY(sawLeftPress);

        spy.clear();
        QTest::qWait(40);
        QCOMPARE(spy.count(), 0); // repeatDelay 重置后未到，不应输出 repeated

        QTRY_VERIFY_WITH_TIMEOUT(spy.count() >= 1, 500);
        QCOMPARE(spy.first().at(0).toString(), QString::fromLatin1(DeckGamepadActionId::NavLeft));
        QCOMPARE(spy.first().at(1).toBool(), true);
        QVERIFY(spy.first().at(2).toBool());
    }

    void dpadHasPriorityOverStick()
    {
        DeckGamepadActionMapper mapper;
        QSignalSpy spy(&mapper, &DeckGamepadActionMapper::actionTriggered);

        // 先由 stick 输出 Right
        mapper.processAxis(GAMEPAD_AXIS_LEFT_X, 0.9, 1);
        QTRY_VERIFY_WITH_TIMEOUT(spy.count() >= 1, 200);

        bool sawRightPress = false;
        for (const auto &row : spy) {
            if (row.at(0).toString() == QString::fromLatin1(DeckGamepadActionId::NavRight) &&
                row.at(1).toBool()) {
                sawRightPress = true;
            }
        }
        QVERIFY(sawRightPress);

        spy.clear();

        // 再按 D-pad Left：应切换为 Left（并释放 Right），stick 不得互相打断
        mapper.processButton(GAMEPAD_BUTTON_DPAD_LEFT, true, 2);
        QTRY_VERIFY_WITH_TIMEOUT(spy.count() >= 2, 200);

        bool sawLeftPress = false;
        bool sawRightRelease = false;
        for (const auto &row : spy) {
            if (row.at(0).toString() == QString::fromLatin1(DeckGamepadActionId::NavLeft) &&
                row.at(1).toBool()) {
                sawLeftPress = true;
            }
            if (row.at(0).toString() == QString::fromLatin1(DeckGamepadActionId::NavRight) &&
                !row.at(1).toBool()) {
                sawRightRelease = true;
            }
        }
        QVERIFY(sawLeftPress);
        QVERIFY(sawRightRelease);

        spy.clear();
        mapper.processAxis(GAMEPAD_AXIS_LEFT_X, -0.9, 3); // stick 变化应被忽略（D-pad 优先）
        mapper.processAxis(GAMEPAD_AXIS_LEFT_X, 0.9, 4);
        QCOMPARE(spy.count(), 0);

        // 松开 D-pad：此时应回到 stick 输出 Right
        mapper.processButton(GAMEPAD_BUTTON_DPAD_LEFT, false, 5);
        QTRY_VERIFY_WITH_TIMEOUT(spy.count() >= 2, 200); // Left release + Right press

        bool sawLeftRelease = false;
        sawRightPress = false;
        for (const auto &row : spy) {
            if (row.at(0).toString() == QString::fromLatin1(DeckGamepadActionId::NavLeft) &&
                !row.at(1).toBool()) {
                sawLeftRelease = true;
            }
            if (row.at(0).toString() == QString::fromLatin1(DeckGamepadActionId::NavRight) &&
                row.at(1).toBool()) {
                sawRightPress = true;
            }
        }
        QVERIFY(sawLeftRelease);
        QVERIFY(sawRightPress);
    }
};

QTEST_MAIN(TestActionMapperRepeat)

#include "test_action_mapper_repeat.moc"

