// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "testprovider.h"

#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtTest/QSignalSpy>
#include <QtTest/QTest>

using namespace deckshell::deckgamepad;

class TestPlayerAssignment : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void assignAndUnassign()
    {
        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        QVERIFY(service.start());

        provider->addConnectedGamepad(1, QStringLiteral("Pad-1"));

        QSignalSpy assignedSpy(&service, &DeckGamepadService::playerAssigned);
        QSignalSpy unassignedSpy(&service, &DeckGamepadService::playerUnassigned);

        QCOMPARE(service.assignPlayer(1), 0);
        QCOMPARE(service.playerIndex(1), 0);
        QCOMPARE(assignedSpy.count(), 1);
        QCOMPARE(unassignedSpy.count(), 0);

        service.unassignPlayer(1);
        QCOMPARE(service.playerIndex(1), -1);
        QCOMPARE(assignedSpy.count(), 1);
        QCOMPARE(unassignedSpy.count(), 1);
    }

    void noDuplicateAssignSignal()
    {
        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        QVERIFY(service.start());

        provider->addConnectedGamepad(1, QStringLiteral("Pad-1"));

        QSignalSpy assignedSpy(&service, &DeckGamepadService::playerAssigned);

        QCOMPARE(service.assignPlayer(1), 0);
        QCOMPARE(service.assignPlayer(1), 0);
        QCOMPARE(assignedSpy.count(), 1);
    }

    void fullSlotsReturnMinusOne()
    {
        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        QVERIFY(service.start());

        for (int id = 1; id <= 5; ++id) {
            provider->addConnectedGamepad(id, QStringLiteral("Pad-%1").arg(id));
        }

        QSignalSpy assignedSpy(&service, &DeckGamepadService::playerAssigned);

        QCOMPARE(service.assignPlayer(1), 0);
        QCOMPARE(service.assignPlayer(2), 1);
        QCOMPARE(service.assignPlayer(3), 2);
        QCOMPARE(service.assignPlayer(4), 3);
        QCOMPARE(service.assignPlayer(5), -1);

        QCOMPARE(assignedSpy.count(), 4);
    }

    void disconnectClearsAssignment()
    {
        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        QVERIFY(service.start());

        provider->addConnectedGamepad(1, QStringLiteral("Pad-1"));

        QSignalSpy unassignedSpy(&service, &DeckGamepadService::playerUnassigned);

        QCOMPARE(service.assignPlayer(1), 0);
        QCOMPARE(service.playerIndex(1), 0);

        provider->removeConnectedGamepad(1);

        QCOMPARE(service.playerIndex(1), -1);
        QCOMPARE(unassignedSpy.count(), 1);
    }
};

QTEST_MAIN(TestPlayerAssignment)

#include "test_player_assignment.moc"

