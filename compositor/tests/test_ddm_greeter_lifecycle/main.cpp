// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "greeter/greeterproxy.h"

#include <Messages.h>

#include <QCoreApplication>
#include <QDataStream>
#include <QLocalServer>
#include <QLocalSocket>
#include <QSignalSpy>
#include <QTest>

#include <memory>

using namespace DDM;

class TestGreeterProxy final : public GreeterProxy
{
public:
    TestGreeterProxy(const QString &authSocket, const QString &waylandSocket)
        : GreeterProxy(authSocket, waylandSocket, nullptr)
    {
    }
};

class DdmGreeterLifecycleTest : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void constructsWithoutDdmSocket();
    void exchangesHandshakeAndDaemonState();
};

void DdmGreeterLifecycleTest::constructsWithoutDdmSocket()
{
    TestGreeterProxy proxy(QString(), QStringLiteral("wayland-test"));

    QVERIFY(!proxy.isConnected());
    QCOMPARE(proxy.hostName(), QString());
    QCOMPARE(proxy.failedAttempts(), 0);
}

void DdmGreeterLifecycleTest::exchangesHandshakeAndDaemonState()
{
    QLocalServer server;
    const QString socketName =
        QStringLiteral("deckshell-ddm-test-%1").arg(QCoreApplication::applicationPid());
    QLocalServer::removeServer(socketName);
    server.setSocketOptions(QLocalServer::UserAccessOption);
    QVERIFY2(server.listen(socketName), qPrintable(server.errorString()));

    TestGreeterProxy proxy(server.fullServerName(), QStringLiteral("wayland-test"));
    QSignalSpy disconnectedSpy(&proxy, &GreeterProxy::socketDisconnected);
    QSignalSpy hostNameSpy(&proxy, &GreeterProxy::hostNameChanged);
    QSignalSpy powerOffSpy(&proxy, &GreeterProxy::canPowerOffChanged);
    QSignalSpy rebootSpy(&proxy, &GreeterProxy::canRebootChanged);
    QSignalSpy suspendSpy(&proxy, &GreeterProxy::canSuspendChanged);
    QSignalSpy hibernateSpy(&proxy, &GreeterProxy::canHibernateChanged);
    QSignalSpy hybridSleepSpy(&proxy, &GreeterProxy::canHybridSleepChanged);
    QSignalSpy failedAttemptsSpy(&proxy, &GreeterProxy::failedAttemptsChanged);

    QTRY_VERIFY(proxy.isConnected());
    QTRY_VERIFY(server.hasPendingConnections());
    std::unique_ptr<QLocalSocket> peer(server.nextPendingConnection());
    QVERIFY(peer);

    QDataStream handshake(peer.get());
    quint32 message = 0;
    QString waylandSocket;
    QTRY_VERIFY(peer->bytesAvailable() > 0);
    handshake.startTransaction();
    handshake >> message >> waylandSocket;
    QVERIFY(handshake.commitTransaction());
    QCOMPARE(message, quint32(GreeterMessages::Connect));
    QCOMPARE(waylandSocket, QStringLiteral("wayland-test"));

    QByteArray response;
    QDataStream output(&response, QIODevice::WriteOnly);
    const quint32 capabilities =
        Capability::PowerOff | Capability::Suspend | Capability::HybridSleep;
    output << quint32(DaemonMessages::Capabilities) << capabilities
           << quint32(DaemonMessages::HostName) << QStringLiteral("deck-test")
           << quint32(DaemonMessages::LoginFailed) << QStringLiteral("alice");
    QCOMPARE(peer->write(response), qint64(response.size()));
    QVERIFY(peer->flush());

    QTRY_COMPARE(proxy.hostName(), QStringLiteral("deck-test"));
    QTRY_COMPARE(proxy.failedAttempts(), 1);
    QVERIFY(proxy.canPowerOff());
    QVERIFY(!proxy.canReboot());
    QVERIFY(proxy.canSuspend());
    QVERIFY(!proxy.canHibernate());
    QVERIFY(proxy.canHybridSleep());

    QCOMPARE(hostNameSpy.count(), 1);
    QCOMPARE(powerOffSpy.count(), 1);
    QCOMPARE(rebootSpy.count(), 1);
    QCOMPARE(suspendSpy.count(), 1);
    QCOMPARE(hibernateSpy.count(), 1);
    QCOMPARE(hybridSleepSpy.count(), 1);
    QCOMPARE(failedAttemptsSpy.count(), 1);

    peer->disconnectFromServer();
    QTRY_COMPARE(disconnectedSpy.count(), 1);
    QVERIFY(!proxy.isConnected());
}

QTEST_GUILESS_MAIN(DdmGreeterLifecycleTest)
#include "main.moc"
