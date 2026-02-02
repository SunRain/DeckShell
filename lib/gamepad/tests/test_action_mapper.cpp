// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/extras/deckgamepadactionmapper.h>

#include <QtTest/QSignalSpy>
#include <QtTest/QTest>

using namespace deckshell::deckgamepad;

class TestActionMapper : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void defaultRepeatDisabled()
    {
        DeckGamepadActionMapper mapper;
        QSignalSpy spy(&mapper, &DeckGamepadActionMapper::actionTriggered);

        mapper.processButton(GAMEPAD_BUTTON_A, true, 1);
        QCOMPARE(spy.count(), 1);
        QCOMPARE(spy.takeFirst().at(0).toString(), QString::fromLatin1(DeckGamepadActionId::NavAccept));

        mapper.processButton(GAMEPAD_BUTTON_A, true, 2);
        QCOMPARE(spy.count(), 0);

        mapper.processButton(GAMEPAD_BUTTON_A, false, 3);
        QCOMPARE(spy.count(), 1);
        const auto args = spy.takeFirst();
        QCOMPARE(args.at(0).toString(), QString::fromLatin1(DeckGamepadActionId::NavAccept));
        QCOMPARE(args.at(1).toBool(), false);
        QCOMPARE(args.at(2).toBool(), false); // repeated
    }

    void axisThresholdHysteresisAndReleaseOnCenter()
    {
        DeckGamepadActionMapper mapper;
        mapper.applyNavigationPreset();
        QSignalSpy spy(&mapper, &DeckGamepadActionMapper::actionTriggered);

        // 默认 deadzone=0.25 hysteresis=0.05 => press=0.30 release=0.25
        mapper.processAxis(GAMEPAD_AXIS_LEFT_X, 0.29, 0);
        QCOMPARE(spy.count(), 0);

        mapper.processAxis(GAMEPAD_AXIS_LEFT_X, 0.31, 1);
        QCOMPARE(spy.count(), 1);
        QCOMPARE(spy.takeFirst().at(0).toString(), QString::fromLatin1(DeckGamepadActionId::NavRight));

        mapper.processAxis(GAMEPAD_AXIS_LEFT_X, 0.26, 2);
        QCOMPARE(spy.count(), 0);

        mapper.processAxis(GAMEPAD_AXIS_LEFT_X, 0.24, 3);
        QCOMPARE(spy.count(), 1);
        const auto args = spy.takeFirst();
        QCOMPARE(args.at(0).toString(), QString::fromLatin1(DeckGamepadActionId::NavRight));
        QCOMPARE(args.at(1).toBool(), false);
    }

    void diagonalPolicyPreferCardinalLocks()
    {
        DeckGamepadActionMapper mapper;
        QSignalSpy spy(&mapper, &DeckGamepadActionMapper::actionTriggered);

        mapper.processAxis(GAMEPAD_AXIS_LEFT_X, 0.8, 0);
        mapper.processAxis(GAMEPAD_AXIS_LEFT_Y, 0.9, 0); // Down is positive
        QVERIFY(spy.count() >= 1);

        bool sawDown = false;
        bool sawRight = false;
        for (const auto &row : spy) {
            if (row.at(0).toString() == QString::fromLatin1(DeckGamepadActionId::NavDown) && row.at(1).toBool()) {
                sawDown = true;
            }
            if (row.at(0).toString() == QString::fromLatin1(DeckGamepadActionId::NavRight) && row.at(1).toBool()) {
                sawRight = true;
            }
        }
        // PreferCardinal：先触发的轴获得 lock，后续另一个轴不会形成斜向输出。
        QVERIFY(!sawDown);
        QVERIFY(sawRight);
    }

    void diagonalPolicyAllowDiagonal()
    {
        DeckGamepadActionMapper mapper;
        mapper.setDiagonalPolicy(DeckGamepadActionMapper::DiagonalPolicy::AllowDiagonal);
        QSignalSpy spy(&mapper, &DeckGamepadActionMapper::actionTriggered);

        mapper.processAxis(GAMEPAD_AXIS_LEFT_X, 0.8, 0);
        mapper.processAxis(GAMEPAD_AXIS_LEFT_Y, 0.9, 0);

        bool sawDown = false;
        bool sawRight = false;
        for (const auto &row : spy) {
            if (row.at(0).toString() == QString::fromLatin1(DeckGamepadActionId::NavDown) && row.at(1).toBool()) {
                sawDown = true;
            }
            if (row.at(0).toString() == QString::fromLatin1(DeckGamepadActionId::NavRight) && row.at(1).toBool()) {
                sawRight = true;
            }
        }
        QVERIFY(sawDown);
        QVERIFY(sawRight);

        spy.clear();

        mapper.processAxis(GAMEPAD_AXIS_LEFT_X, 0.0, 1);
        mapper.processAxis(GAMEPAD_AXIS_LEFT_Y, 0.0, 1);
        QVERIFY(spy.count() >= 2);
    }
};

QTEST_MAIN(TestActionMapper)

#include "test_action_mapper.moc"
