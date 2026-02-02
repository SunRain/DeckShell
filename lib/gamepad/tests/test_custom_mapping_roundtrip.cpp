// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/mapping/deckgamepadsdlmappingutils_p.h>

#include <QtTest/QTest>

#include <linux/input.h>

using namespace deckshell::deckgamepad;

class TestCustomMappingRoundtrip final : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void parseAndCompose_roundtripPreservesSemantics()
    {
        static const QString guid = QStringLiteral("03000000deadbeef0000000000000000");

        // Cover: hat, inverted axis, half-axis (+a/-a) as button.
        const QString input = guid
            + QStringLiteral(",Test Pad,a:+a2,b:-a5,lefty:~a1,dpup:h0.1,platform:Linux");

        QHash<int, int> physicalButtons;
        QHash<int, int> physicalAxes;
        physicalAxes.insert(ABS_X, 0);
        physicalAxes.insert(ABS_Y, 1);
        physicalAxes.insert(ABS_Z, 2);
        physicalAxes.insert(ABS_RZ, 5);

        const DeviceMapping parsed = deckGamepadParseSdlMappingString(input, physicalButtons, physicalAxes);
        QVERIFY(parsed.isValid());

        const QString composed = deckGamepadComposeSdlMappingString(parsed, physicalButtons, physicalAxes);
        QVERIFY(!composed.isEmpty());

        const DeviceMapping reparsed = deckGamepadParseSdlMappingString(composed, physicalButtons, physicalAxes);
        QVERIFY(reparsed.isValid());

        QCOMPARE(reparsed.hatButtonMap, parsed.hatButtonMap);
        QCOMPARE(reparsed.axisMap, parsed.axisMap);
        QCOMPARE(reparsed.invertedAxes, parsed.invertedAxes);
        QCOMPARE(reparsed.halfAxisPosButtonMap, parsed.halfAxisPosButtonMap);
        QCOMPARE(reparsed.halfAxisNegButtonMap, parsed.halfAxisNegButtonMap);
        QCOMPARE(reparsed.buttonMap, parsed.buttonMap);
    }
};

QTEST_MAIN(TestCustomMappingRoundtrip)
#include "test_custom_mapping_roundtrip.moc"

