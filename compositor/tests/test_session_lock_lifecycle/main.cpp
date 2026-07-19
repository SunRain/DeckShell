// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "outputresizeclient.h"
#include "sessionlockclient.h"

#include <QElapsedTimer>
#include <QFile>
#include <QProcess>
#include <QProcessEnvironment>
#include <QTemporaryDir>
#include <QTest>
#include <QThread>

#include <memory>

class SessionLockLifecycleTest : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void init();
    void externalClientLocksAndUnlocksTwice();
    void lockSurfacesAcknowledgeConfigureAndCommitForEveryOutput();
    void activeLockRejectsConcurrentClient();
    void outputResizeReconfiguresLockSurfaces();
    void abandonedClientPreservesConfiguredRecoveryAuthority();
    void cleanup();

private:
    bool waitForSocket();
    QString diagnostics();
    void stopCompositor();

    std::unique_ptr<QTemporaryDir> m_runtimeDir;
    QProcess m_compositor;
    QByteArray m_output;
};

bool SessionLockLifecycleTest::waitForSocket()
{
    const QString socketPath = m_runtimeDir->filePath(QStringLiteral("wayland-0"));
    QElapsedTimer timer;
    timer.start();

    while (!QFile::exists(socketPath) && timer.elapsed() < 10000) {
        if (m_compositor.state() == QProcess::NotRunning)
            return false;
        m_compositor.waitForReadyRead(50);
        m_output.append(m_compositor.readAll());
        QThread::msleep(20);
    }
    return QFile::exists(socketPath);
}

QString SessionLockLifecycleTest::diagnostics()
{
    m_output.append(m_compositor.readAll());
    return QString::fromLocal8Bit(m_output);
}

void SessionLockLifecycleTest::init()
{
    m_runtimeDir = std::make_unique<QTemporaryDir>();
    QVERIFY2(m_runtimeDir->isValid(), "failed to create runtime directory");

    auto environment = QProcessEnvironment::systemEnvironment();
    environment.insert(QStringLiteral("XDG_RUNTIME_DIR"), m_runtimeDir->path());
    environment.insert(QStringLiteral("WLR_BACKENDS"), QStringLiteral("headless"));
    environment.insert(QStringLiteral("WLR_HEADLESS_OUTPUTS"), QStringLiteral("2"));
    environment.insert(QStringLiteral("WLR_RENDERER"), QStringLiteral("pixman"));

    m_compositor.setProcessEnvironment(environment);
    m_compositor.setProcessChannelMode(QProcess::MergedChannels);
    m_compositor.start(QString::fromUtf8(DECKCOMPOSITOR_EXECUTABLE), { });

    QVERIFY2(m_compositor.waitForStarted(5000), qPrintable(m_compositor.errorString()));
    QVERIFY2(waitForSocket(), qPrintable(diagnostics()));
}

void SessionLockLifecycleTest::externalClientLocksAndUnlocksTwice()
{
    for (int attempt = 1; attempt <= 2; ++attempt) {
        SessionLockClient client;
        QString error;
        QVERIFY2(client.connectTo(m_runtimeDir->path(), &error),
                 qPrintable(error + u'\n' + diagnostics()));
        QVERIFY2(client.lock(&error), qPrintable(error + u'\n' + diagnostics()));
        QVERIFY2(client.unlock(&error), qPrintable(error + u'\n' + diagnostics()));
        QTest::qWait(100);
        QCOMPARE(m_compositor.state(), QProcess::Running);
    }
}

void SessionLockLifecycleTest::lockSurfacesAcknowledgeConfigureAndCommitForEveryOutput()
{
    SessionLockClient client;
    QString error;
    QVERIFY2(client.connectTo(m_runtimeDir->path(), &error),
             qPrintable(error + u'\n' + diagnostics()));
    QCOMPARE(client.outputCount(), 2);
    QVERIFY2(client.lock(&error), qPrintable(error + u'\n' + diagnostics()));
    QVERIFY2(client.createAndCommitLockSurfaces(&error), qPrintable(error + u'\n' + diagnostics()));
    QCOMPARE(client.renderedLockSurfaceCount(), client.outputCount());
    QVERIFY2(client.unlock(&error), qPrintable(error + u'\n' + diagnostics()));
    QCOMPARE(m_compositor.state(), QProcess::Running);
}

void SessionLockLifecycleTest::activeLockRejectsConcurrentClient()
{
    SessionLockClient owner;
    QString error;
    QVERIFY2(owner.connectTo(m_runtimeDir->path(), &error),
             qPrintable(error + u'\n' + diagnostics()));
    QVERIFY2(owner.lock(&error), qPrintable(error + u'\n' + diagnostics()));
    QVERIFY2(owner.createAndCommitLockSurfaces(&error), qPrintable(error + u'\n' + diagnostics()));

    SessionLockClient contender;
    QVERIFY2(contender.connectTo(m_runtimeDir->path(), &error),
             qPrintable(error + u'\n' + diagnostics()));
    QVERIFY2(contender.requestLock(&error), qPrintable(error + u'\n' + diagnostics()));
    QVERIFY(contender.isFinished());
    QVERIFY(!contender.isLocked());

    QVERIFY2(owner.unlock(&error), qPrintable(error + u'\n' + diagnostics()));
    QCOMPARE(m_compositor.state(), QProcess::Running);
}

void SessionLockLifecycleTest::outputResizeReconfiguresLockSurfaces()
{
    SessionLockClient owner;
    QString error;
    QVERIFY2(owner.connectTo(m_runtimeDir->path(), &error),
             qPrintable(error + u'\n' + diagnostics()));
    QVERIFY2(owner.lock(&error), qPrintable(error + u'\n' + diagnostics()));
    QVERIFY2(owner.createAndCommitLockSurfaces(&error), qPrintable(error + u'\n' + diagnostics()));

    OutputResizeClient outputClient;
    QVERIFY2(outputClient.connectTo(m_runtimeDir->path(), &error),
             qPrintable(error + u'\n' + diagnostics()));
    QVERIFY2(outputClient.resizeFirstOutput(640, 480, &error),
             qPrintable(error + u'\n' + diagnostics()));
    QVERIFY2(owner.waitForReconfigure(&error), qPrintable(error + u'\n' + diagnostics()));
    QVERIFY2(owner.unlock(&error), qPrintable(error + u'\n' + diagnostics()));
    QCOMPARE(m_compositor.state(), QProcess::Running);
}

void SessionLockLifecycleTest::abandonedClientPreservesConfiguredRecoveryAuthority()
{
    {
        SessionLockClient abandoned;
        QString error;
        QVERIFY2(abandoned.connectTo(m_runtimeDir->path(), &error),
                 qPrintable(error + u'\n' + diagnostics()));
        QVERIFY2(abandoned.lock(&error), qPrintable(error + u'\n' + diagnostics()));
        QVERIFY2(abandoned.createAndCommitLockSurfaces(&error),
                 qPrintable(error + u'\n' + diagnostics()));
        abandoned.disconnectAbruptly();
    }

    QTest::qWait(200);
    QCOMPARE(m_compositor.state(), QProcess::Running);

    SessionLockClient recovery;
    QString error;
    QVERIFY2(recovery.connectTo(m_runtimeDir->path(), &error),
             qPrintable(error + u'\n' + diagnostics()));
#ifdef SESSION_LOCK_WITH_DDM
    // Once DDM owns recovery, an unprivileged external client must not be able
    // to replace the trusted greeter and then unlock the session.
    QVERIFY2(recovery.requestLock(&error), qPrintable(error + u'\n' + diagnostics()));
    QVERIFY(recovery.isFinished());
    QVERIFY(!recovery.isLocked());
#else
    QVERIFY2(recovery.lock(&error), qPrintable(error + u'\n' + diagnostics()));
    QVERIFY2(recovery.createAndCommitLockSurfaces(&error),
             qPrintable(error + u'\n' + diagnostics()));
    QVERIFY2(recovery.unlock(&error), qPrintable(error + u'\n' + diagnostics()));
#endif
    QCOMPARE(m_compositor.state(), QProcess::Running);
}

void SessionLockLifecycleTest::stopCompositor()
{
    if (m_compositor.state() == QProcess::NotRunning)
        return;

    m_compositor.terminate();
    if (!m_compositor.waitForFinished(3000)) {
        m_compositor.kill();
        m_compositor.waitForFinished(3000);
    }
    m_output.append(m_compositor.readAll());
}

void SessionLockLifecycleTest::cleanup()
{
    stopCompositor();
    m_runtimeDir.reset();
}

QTEST_GUILESS_MAIN(SessionLockLifecycleTest)
#include "main.moc"
