// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "core/rootsurfacecontainer.h"
#include "core/treeland.h"
#include "lateclient.h"
#include "modules/dde-shell/ddeshellmanagerinterfacev1.h"
#include "seat/helper.h"
#include "session/session.h"
#include "surface/surfacewrapper.h"

#include <wrenderhelper.h>
#include <wserver.h>
#include <wsocket.h>

#include <QElapsedTimer>
#include <QFile>
#include <QGuiApplication>
#include <QPointer>
#include <QProcess>
#include <QTemporaryDir>
#include <QTest>

#include <cstring>
#include <memory>

class LateDdeListenerTest : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void initTestCase();
    void realShellHandlerTracksIndependentLateSurfacesAndDestroyedWrapper();
    void cleanupTestCase();

private:
    SurfaceWrapper *wrapperForAppId(const QString &appId) const;
    bool dispatchServer();
    void sendClientCommand(const QByteArray &command);
    QString diagnostics();

    std::unique_ptr<QTemporaryDir> m_runtimeDir;
    std::unique_ptr<Treeland::Treeland> m_treeland;
    QProcess m_client;
    QByteArray m_clientOutput;
};

SurfaceWrapper *LateDdeListenerTest::wrapperForAppId(const QString &appId) const
{
    if (!m_treeland)
        return nullptr;

    for (auto *wrapper : m_treeland->rootSurfaceContainer()->surfaces()) {
        if (wrapper->appId() == appId)
            return wrapper;
    }
    return nullptr;
}

QString LateDdeListenerTest::diagnostics()
{
    m_clientOutput.append(m_client.readAll());
    return QString::fromLocal8Bit(m_clientOutput);
}

bool LateDdeListenerTest::dispatchServer()
{
    auto *helper = Helper::instance();
    auto *ddeShell = helper ? helper->ddeShellV1() : nullptr;
    auto *server = ddeShell ? WServer::from(ddeShell) : nullptr;
    if (!server || !server->handle())
        return false;

    auto *display = server->handle();
    if (wl_event_loop_dispatch(wl_display_get_event_loop(display), 0) != 0)
        return false;
    wl_display_flush_clients(display);
    return true;
}

void LateDdeListenerTest::sendClientCommand(const QByteArray &command)
{
    const QByteArray acknowledgement = "ok " + command + '\n';
    m_clientOutput.clear();

    QCOMPARE(m_client.write(command + '\n'), command.size() + 1);
    QVERIFY2(m_client.waitForBytesWritten(1000), qPrintable(m_client.errorString()));
    QElapsedTimer commandTimer;
    commandTimer.start();
    while (!m_clientOutput.contains(acknowledgement) && commandTimer.elapsed() < 5000) {
        QVERIFY(dispatchServer());
        QCoreApplication::processEvents(QEventLoop::AllEvents, 10);
        m_client.waitForReadyRead(10);
        diagnostics();
    }
    QVERIFY2(m_clientOutput.contains(acknowledgement), qPrintable(diagnostics()));
    QCOMPARE(m_client.state(), QProcess::Running);
}

void LateDdeListenerTest::initTestCase()
{
    m_runtimeDir = std::make_unique<QTemporaryDir>();
    QVERIFY2(m_runtimeDir->isValid(), "failed to create XDG runtime directory");
    qputenv("XDG_RUNTIME_DIR", m_runtimeDir->path().toUtf8());

    WRenderHelper::setupRendererBackend();
    m_treeland = std::make_unique<Treeland::Treeland>();

    auto *helper = Helper::instance();
    QVERIFY(helper);
    const auto session = helper->sessionManager()->globalSession();
    QVERIFY(session);
    QVERIFY(session->socket());

    const QString socketPath = session->socket()->fullServerName();
    QTRY_VERIFY_WITH_TIMEOUT(!socketPath.isEmpty() && QFile::exists(socketPath), 5000);

    m_client.setProcessChannelMode(QProcess::MergedChannels);
    m_client.start(QCoreApplication::applicationFilePath(),
                   { QStringLiteral("--late-dde-client"), socketPath });
    QVERIFY2(m_client.waitForStarted(5000), qPrintable(m_client.errorString()));
    QElapsedTimer readyTimer;
    readyTimer.start();
    while (!m_clientOutput.contains("ready\n") && readyTimer.elapsed() < 5000) {
        QVERIFY(dispatchServer());
        QCoreApplication::processEvents(QEventLoop::AllEvents, 50);
        m_client.waitForReadyRead(50);
        diagnostics();
    }
    const QString readyDiagnostics = diagnostics();
    QVERIFY2(m_clientOutput.contains("ready\n"),
             qPrintable(QStringLiteral("late DDE client did not become ready; state=%1, error=%2, "
                                       "exitStatus=%3, exitCode=%4, output:\n%5")
                            .arg(m_client.state())
                            .arg(m_client.errorString())
                            .arg(m_client.exitStatus())
                            .arg(m_client.exitCode())
                            .arg(readyDiagnostics)));

    QTRY_VERIFY_WITH_TIMEOUT(wrapperForAppId(QStringLiteral("org.deepin.test.late-dde-0")), 5000);
    QTRY_VERIFY_WITH_TIMEOUT(wrapperForAppId(QStringLiteral("org.deepin.test.late-dde-1")), 5000);
    QTRY_VERIFY_WITH_TIMEOUT(wrapperForAppId(QStringLiteral("org.deepin.test.late-dde-2")), 5000);
}

void LateDdeListenerTest::realShellHandlerTracksIndependentLateSurfacesAndDestroyedWrapper()
{
    QPointer first = wrapperForAppId(QStringLiteral("org.deepin.test.late-dde-0"));
    QPointer second = wrapperForAppId(QStringLiteral("org.deepin.test.late-dde-1"));
    QPointer third = wrapperForAppId(QStringLiteral("org.deepin.test.late-dde-2"));
    QVERIFY(first);
    QVERIFY(second);
    QVERIFY(third);
    QVERIFY(!first->isDDEShellSurface());
    QVERIFY(!second->isDDEShellSurface());
    QVERIFY(!third->isDDEShellSurface());

    sendClientCommand("dde 0");
    QTRY_VERIFY(first->isDDEShellSurface());
    QTRY_VERIFY(first->skipSwitcher());
    QVERIFY(!second->isDDEShellSurface());

    sendClientCommand("dde 1");
    QTRY_VERIFY(second->isDDEShellSurface());
    QTRY_VERIFY(second->skipSwitcher());

    QPointer<WSurface> thirdSurface = third->surface();
    QVERIFY(thirdSurface);
    sendClientCommand("destroy-xdg 2");
    QTRY_VERIFY(third.isNull());
    QTRY_VERIFY(thirdSurface.isNull());
    QCOMPARE(wrapperForAppId(QStringLiteral("org.deepin.test.late-dde-2")), nullptr);

    QPointer<DDEShellSurfaceInterface> orphanDdeSurface;
    const auto connection = connect(Helper::instance()->ddeShellV1(),
                                    &DDEShellManagerInterfaceV1::surfaceCreated,
                                    this,
                                    [&orphanDdeSurface](DDEShellSurfaceInterface *surface) {
                                        orphanDdeSurface = surface;
                                    });
    sendClientCommand("dde 2");
    disconnect(connection);
    QVERIFY(orphanDdeSurface);
    QCOMPARE(orphanDdeSurface->wSurface(), nullptr);
    QCOMPARE(wrapperForAppId(QStringLiteral("org.deepin.test.late-dde-2")), nullptr);
}

void LateDdeListenerTest::cleanupTestCase()
{
    if (m_client.state() == QProcess::Running) {
        m_client.write("quit\n");
        m_client.waitForBytesWritten(1000);
        if (!m_client.waitForFinished(5000)) {
            m_client.terminate();
            if (!m_client.waitForFinished(2000)) {
                m_client.kill();
                m_client.waitForFinished(2000);
            }
        }
    }

    if (m_treeland)
        dispatchServer();

    // Treeland owns process-wide QML singletons and normally lives until process exit.
    // Explicit fixture destruction exercises an unrelated QObject child-order teardown bug.
    m_treeland.release();
    m_runtimeDir.reset();
}

int main(int argc, char *argv[])
{
    if (argc == 3 && std::strcmp(argv[1], "--late-dde-client") == 0)
        return runLateDdeClient(argv[2]);

    qputenv("WLR_BACKENDS", "headless");
    qputenv("WLR_HEADLESS_OUTPUTS", "1");
    qputenv("WLR_RENDERER", "pixman");
    qputenv("WLR_LIBINPUT_NO_DEVICES", "1");
    qunsetenv("QT_QPA_PLATFORM");

    WServer::initializeQPA();
    QGuiApplication::setQuitOnLastWindowClosed(false);

    int applicationArgc = 1;
    char *applicationArgv[] = { argv[0], nullptr };
    QGuiApplication app(applicationArgc, applicationArgv);
    app.setOrganizationName(QStringLiteral("deepin"));
    app.setApplicationName(QStringLiteral("test-late-dde-listener"));

    LateDdeListenerTest test;
    return QTest::qExec(&test, argc, argv);
}

#include "main.moc"
