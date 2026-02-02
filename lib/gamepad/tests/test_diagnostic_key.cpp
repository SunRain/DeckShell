// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "testprovider.h"

#include <deckshell/deckgamepad/core/deckgamepadaction.h>
#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtTest/QSignalSpy>
#include <QtTest/QTest>

#include <errno.h>

using namespace deckshell::deckgamepad;

class TestDiagnosticKey : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void permissionDeniedMapsToStableKey()
    {
        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        QSignalSpy spy(&service, &DeckGamepadService::diagnosticChanged);

        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::PermissionDenied;
        err.message = QStringLiteral("permission denied");
        err.sysErrno = EACCES;
        err.context = QStringLiteral("evdev open");

        provider->emitLastErrorChanged(err);

        QVERIFY(spy.count() >= 1);
        QCOMPARE(service.diagnosticKey(), QString::fromLatin1(DeckGamepadDiagnosticKey::PermissionDenied));
        QVERIFY(service.suggestedActions().contains(QString::fromLatin1(DeckGamepadActionId::HelpCheckPermissions)));
    }

    void devicePermissionDeniedIsVisibleAsDiagnostic()
    {
        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        QSignalSpy spy(&service, &DeckGamepadService::diagnosticChanged);

        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::PermissionDenied;
        err.message = QStringLiteral("permission denied");
        err.sysErrno = EACCES;
        err.context = QStringLiteral("open(/dev/input/event99)");

        provider->emitDeviceAvailabilityChanged(1, DeckGamepadDeviceAvailability::Unavailable);
        provider->emitDeviceLastErrorChanged(1, err);

        QVERIFY(spy.count() >= 1);
        QCOMPARE(service.diagnosticKey(), QString::fromLatin1(DeckGamepadDiagnosticKey::PermissionDenied));
        QCOMPARE(service.diagnosticDetails().value(QStringLiteral("deviceId")).toInt(), 1);
    }

    void sessionInactiveMapsToStableKey()
    {
        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        QSignalSpy spy(&service, &DeckGamepadService::diagnosticChanged);

        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::Io;
        err.message = QStringLiteral("inactive session");
        err.context = QStringLiteral("SessionGate: inactive");

        provider->emitLastErrorChanged(err);

        QVERIFY(spy.count() >= 1);
        QCOMPARE(service.diagnosticKey(), QString::fromLatin1(DeckGamepadDiagnosticKey::SessionInactive));
        QVERIFY(service.suggestedActions().contains(QString::fromLatin1(DeckGamepadActionId::HelpSwitchToActiveSession)));
    }

    void deviceBusyMapsToStableKey()
    {
        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        QSignalSpy spy(&service, &DeckGamepadService::diagnosticChanged);

        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::Io;
        err.message = QStringLiteral("device busy");
        err.sysErrno = EBUSY;
        err.context = QStringLiteral("evdev open");

        provider->emitLastErrorChanged(err);

        QVERIFY(spy.count() >= 1);
        QCOMPARE(service.diagnosticKey(), QString::fromLatin1(DeckGamepadDiagnosticKey::DeviceBusy));
        QVERIFY(service.suggestedActions().contains(QString::fromLatin1(DeckGamepadActionId::HelpDisableGrab)));
    }

    void providerDiagnosticOverridesError()
    {
        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);

        QSignalSpy spy(&service, &DeckGamepadService::diagnosticChanged);

        DeckGamepadDiagnostic diag;
        diag.key = QString::fromLatin1(DeckGamepadDiagnosticKey::WaylandFocusGated);
        diag.suggestedActions = QStringList{ QString::fromLatin1(DeckGamepadActionId::HelpFocusWindow) };
        provider->emitDiagnosticChanged(diag);

        QVERIFY(spy.count() >= 1);
        QCOMPARE(service.diagnosticKey(), QString::fromLatin1(DeckGamepadDiagnosticKey::WaylandFocusGated));
    }
};

QTEST_MAIN(TestDiagnosticKey)

#include "test_diagnostic_key.moc"
