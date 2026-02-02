// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/service/deckgamepadservice.h>
#include <deckshell/deckgamepad/providers/evdev/evdevprovider.h>
#include <deckshell/deckgamepad/mapping/deckgamepadcustommappingmanager.h>

#include <QtCore/QThread>
#include <QtTest/QTest>

using namespace deckshell::deckgamepad;

namespace {
bool isSingleThreadForcedByEnv()
{
    const QByteArray raw = qgetenv("DECKGAMEPAD_EVDEV_SINGLE_THREAD");
    if (raw.isEmpty()) {
        return false;
    }

    const QByteArray normalized = raw.trimmed().toLower();
    if (normalized.isEmpty()) {
        return true;
    }
    if (normalized == QByteArrayLiteral("0")
        || normalized == QByteArrayLiteral("false")
        || normalized == QByteArrayLiteral("no")
        || normalized == QByteArrayLiteral("off")) {
        return false;
    }
    return true;
}
}

class TestServiceProviderSelection : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void providerSelection_canSwitch_andRollbackToAuto()
    {
        DeckGamepadService service;

        auto *provider = qobject_cast<EvdevProvider *>(service.provider());
        QVERIFY2(provider, "DeckGamepadService should use EvdevProvider");

        DeckGamepadRuntimeConfig cfg = service.runtimeConfig();

        cfg.providerSelection = DeckGamepadProviderSelection::Evdev;
        QVERIFY(service.setRuntimeConfig(cfg));
        QCOMPARE(service.activeProviderName(), QStringLiteral("evdev"));
        auto *mgr = service.customMappingManager();
        QVERIFY(mgr);
        auto *ioThread = provider->findChild<QThread *>(QStringLiteral("DeckGamepadEvdevProviderIO"));
        if (isSingleThreadForcedByEnv()) {
            QVERIFY2(!ioThread, "EvdevProvider should not create an IO thread in single-thread mode");
            QCOMPARE(mgr->thread(), QThread::currentThread());
        } else {
            QVERIFY(mgr->thread() != QThread::currentThread());
            QVERIFY(ioThread && ioThread->isRunning());
            QCOMPARE(mgr->thread(), ioThread);
        }

        cfg.providerSelection = DeckGamepadProviderSelection::EvdevUdev;
        QVERIFY(service.setRuntimeConfig(cfg));
        QCOMPARE(service.activeProviderName(), QStringLiteral("evdev"));
        mgr = service.customMappingManager();
        QVERIFY(mgr);
        QCOMPARE(mgr->thread(), QThread::currentThread());

        cfg.providerSelection = DeckGamepadProviderSelection::Auto;
        QVERIFY(service.setRuntimeConfig(cfg));
        QCOMPARE(service.activeProviderName(), QStringLiteral("evdev"));
    }
};

QTEST_MAIN(TestServiceProviderSelection)
#include "test_service_provider_selection.moc"
