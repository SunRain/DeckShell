// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/core/deckgamepadaction.h>
#include <deckshell/deckgamepad/extras/actionmappingprofile.h>

#include <QtTest/QTest>

using namespace deckshell::deckgamepad;

class TestActionMappingProfile : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void navigationPresetContainsExpectedBindings()
    {
        const ActionMappingProfile profile = ActionMappingProfile::createNavigationPreset();

        QVERIFY(profile.hasNavigationPriority);
        QCOMPARE(profile.navigationPriority, ActionMappingProfile::NavigationPriority::DpadOverLeftStick);

        QCOMPARE(profile.buttonBindings.value(GAMEPAD_BUTTON_DPAD_UP).actionId, QString::fromLatin1(DeckGamepadActionId::NavUp));
        QCOMPARE(profile.buttonBindings.value(GAMEPAD_BUTTON_DPAD_DOWN).actionId, QString::fromLatin1(DeckGamepadActionId::NavDown));
        QCOMPARE(profile.buttonBindings.value(GAMEPAD_BUTTON_DPAD_LEFT).actionId, QString::fromLatin1(DeckGamepadActionId::NavLeft));
        QCOMPARE(profile.buttonBindings.value(GAMEPAD_BUTTON_DPAD_RIGHT).actionId, QString::fromLatin1(DeckGamepadActionId::NavRight));

        QCOMPARE(profile.buttonBindings.value(GAMEPAD_BUTTON_A).actionId, QString::fromLatin1(DeckGamepadActionId::NavAccept));
        QCOMPARE(profile.buttonBindings.value(GAMEPAD_BUTTON_B).actionId, QString::fromLatin1(DeckGamepadActionId::NavBack));
        QCOMPARE(profile.buttonBindings.value(GAMEPAD_BUTTON_START).actionId, QString::fromLatin1(DeckGamepadActionId::NavMenu));
        QCOMPARE(profile.buttonBindings.value(GAMEPAD_BUTTON_L1).actionId, QString::fromLatin1(DeckGamepadActionId::NavTabPrev));
        QCOMPARE(profile.buttonBindings.value(GAMEPAD_BUTTON_R1).actionId, QString::fromLatin1(DeckGamepadActionId::NavTabNext));

        QVERIFY(profile.axisBindings.contains(GAMEPAD_AXIS_LEFT_X));
        const DeckGamepadAxisActionBinding x = profile.axisBindings.value(GAMEPAD_AXIS_LEFT_X);
        QVERIFY(x.hasNegative);
        QVERIFY(x.hasPositive);
        QCOMPARE(x.negative.actionId, QString::fromLatin1(DeckGamepadActionId::NavLeft));
        QCOMPARE(x.positive.actionId, QString::fromLatin1(DeckGamepadActionId::NavRight));

        QVERIFY(profile.axisBindings.contains(GAMEPAD_AXIS_LEFT_Y));
        const DeckGamepadAxisActionBinding y = profile.axisBindings.value(GAMEPAD_AXIS_LEFT_Y);
        QVERIFY(y.hasNegative);
        QVERIFY(y.hasPositive);
        QCOMPARE(y.negative.actionId, QString::fromLatin1(DeckGamepadActionId::NavUp));
        QCOMPARE(y.positive.actionId, QString::fromLatin1(DeckGamepadActionId::NavDown));
    }

    void jsonRoundTripKeepsBindingsAndRepeat()
    {
        ActionMappingProfile profile = ActionMappingProfile::createNavigationPreset();
        profile.hasRepeatConfig = true;
        profile.repeat.enabled = true;
        profile.repeat.delayMs = 120;
        profile.repeat.intervalMs = 45;
        profile.hasNavigationPriority = true;
        profile.navigationPriority = ActionMappingProfile::NavigationPriority::LeftStickOverDpad;

        const QJsonObject json = profile.toJson();
        const ActionMappingProfile roundtrip = ActionMappingProfile::fromJson(json);

        QVERIFY(roundtrip.hasNavigationPriority);
        QCOMPARE(roundtrip.navigationPriority, ActionMappingProfile::NavigationPriority::LeftStickOverDpad);

        QVERIFY(roundtrip.hasRepeatConfig);
        QCOMPARE(roundtrip.repeat.enabled, true);
        QCOMPARE(roundtrip.repeat.delayMs, 120);
        QCOMPARE(roundtrip.repeat.intervalMs, 45);

        QCOMPARE(roundtrip.buttonBindings.value(GAMEPAD_BUTTON_A).actionId, QString::fromLatin1(DeckGamepadActionId::NavAccept));
        QCOMPARE(roundtrip.axisBindings.value(GAMEPAD_AXIS_LEFT_X).negative.actionId, QString::fromLatin1(DeckGamepadActionId::NavLeft));
    }
};

QTEST_MAIN(TestActionMappingProfile)

#include "test_action_mapping_profile.moc"

