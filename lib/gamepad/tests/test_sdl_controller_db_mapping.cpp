// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/mapping/deckgamepadsdlcontrollerdb.h>

#include <QtTest/QTest>

#include <linux/input.h>

using namespace deckshell::deckgamepad;

class TestSdlControllerDbMapping final : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void invertedAxis_isRecorded()
    {
        static const QString guid = QStringLiteral("03000000deadbeef0000000000000000");

        DeckGamepadSdlControllerDb db;
        QVERIFY(db.addMapping(guid + QStringLiteral(",Test Pad,leftx:~a0,lefty:a1,platform:Linux")));

        QHash<int, int> physicalButtons;
        QHash<int, int> physicalAxes;
        physicalAxes.insert(ABS_X, 0);
        physicalAxes.insert(ABS_Y, 1);

        const DeviceMapping mapping = db.createDeviceMapping(guid, physicalButtons, physicalAxes);
        QVERIFY(mapping.isValid());
        QVERIFY(mapping.axisMap.contains(ABS_X));
        QCOMPARE(mapping.axisMap.value(ABS_X), GAMEPAD_AXIS_LEFT_X);
        QVERIFY(mapping.invertedAxes.contains(ABS_X));
        QVERIFY(!mapping.invertedAxes.contains(ABS_Y));
    }

    void hatMapping_isConverted()
    {
        static const QString guid = QStringLiteral("03000000deadbeef0000000000000000");

        DeckGamepadSdlControllerDb db;
        QVERIFY(db.addMapping(guid
                              + QStringLiteral(
                                  ",Test Pad,dpup:h0.1,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,platform:Linux")));

        const DeviceMapping mapping = db.createDeviceMapping(guid, {}, {});
        QVERIFY(mapping.isValid());

        QCOMPARE(mapping.hatButtonMap.value((0 << 8) | GAMEPAD_HAT_UP, GAMEPAD_BUTTON_INVALID), GAMEPAD_BUTTON_DPAD_UP);
        QCOMPARE(mapping.hatButtonMap.value((0 << 8) | GAMEPAD_HAT_DOWN, GAMEPAD_BUTTON_INVALID),
                 GAMEPAD_BUTTON_DPAD_DOWN);
        QCOMPARE(mapping.hatButtonMap.value((0 << 8) | GAMEPAD_HAT_LEFT, GAMEPAD_BUTTON_INVALID),
                 GAMEPAD_BUTTON_DPAD_LEFT);
        QCOMPARE(mapping.hatButtonMap.value((0 << 8) | GAMEPAD_HAT_RIGHT, GAMEPAD_BUTTON_INVALID),
                 GAMEPAD_BUTTON_DPAD_RIGHT);
    }

    void halfAxisMapping_isConverted()
    {
        static const QString guid = QStringLiteral("03000000deadbeef0000000000000000");

        DeckGamepadSdlControllerDb db;
        QVERIFY(db.addMapping(guid
                              + QStringLiteral(",Test Pad,dpup:-a0,dpdown:+a0,dpleft:-a1,dpright:+a1,platform:Linux")));

        QHash<int, int> physicalAxes;
        physicalAxes.insert(ABS_X, 0);
        physicalAxes.insert(ABS_Y, 1);

        const DeviceMapping mapping = db.createDeviceMapping(guid, {}, physicalAxes);
        QVERIFY(mapping.isValid());

        QCOMPARE(mapping.halfAxisNegButtonMap.value(ABS_X, GAMEPAD_BUTTON_INVALID), GAMEPAD_BUTTON_DPAD_UP);
        QCOMPARE(mapping.halfAxisPosButtonMap.value(ABS_X, GAMEPAD_BUTTON_INVALID), GAMEPAD_BUTTON_DPAD_DOWN);
        QCOMPARE(mapping.halfAxisNegButtonMap.value(ABS_Y, GAMEPAD_BUTTON_INVALID), GAMEPAD_BUTTON_DPAD_LEFT);
        QCOMPARE(mapping.halfAxisPosButtonMap.value(ABS_Y, GAMEPAD_BUTTON_INVALID), GAMEPAD_BUTTON_DPAD_RIGHT);
    }
};

QTEST_MAIN(TestSdlControllerDbMapping)
#include "test_sdl_controller_db_mapping.moc"

