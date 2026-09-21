// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QProcess>
#include <QProcessEnvironment>
#include <QTemporaryDir>
#include <QTest>

namespace {

QString runProcess(const QString &program,
                   const QStringList &arguments,
                   const QProcessEnvironment &environment,
                   int timeout,
                   QString *output = nullptr)
{
    QProcess process;
    process.setProcessEnvironment(environment);
    process.setProcessChannelMode(QProcess::MergedChannels);
    process.start(program, arguments);
    if (!process.waitForStarted(timeout))
        return process.errorString();
    if (!process.waitForFinished(timeout)) {
        process.kill();
        process.waitForFinished();
        return QStringLiteral("process timed out: ") + program;
    }
    const QString processOutput = QString::fromLocal8Bit(process.readAll());
    if (output)
        *output = processOutput;
    if (process.exitStatus() != QProcess::NormalExit || process.exitCode() != 0) {
        return QStringLiteral("%1 failed (exit %2, status %3):\n%4")
            .arg(program)
            .arg(process.exitCode())
            .arg(process.exitStatus())
            .arg(processOutput.right(12000));
    }
    return { };
}

QProcessEnvironment cleanEnvironment()
{
    auto environment = QProcessEnvironment::systemEnvironment();
    for (const char *name : { "LD_LIBRARY_PATH",
                              "LD_PRELOAD",
                              "LD_AUDIT",
                              "QML_IMPORT_PATH",
                              "QML2_IMPORT_PATH",
                              "QT_QML_IMPORT_PATH" }) {
        environment.remove(QString::fromLatin1(name));
    }
    return environment;
}

QString stagedInstallPath(const QString &stage, const QString &installDirectory)
{
    const QString destination = QDir::isAbsolutePath(installDirectory)
        ? installDirectory
        : QDir(QStringLiteral("/usr/local")).filePath(installDirectory);
    return QDir(stage).filePath(destination.mid(1));
}

QString stageEmbeddedRuntime(const QString &stage)
{
#if EMBEDDED_WAYLIB_BUILD
    // 内嵌库没有外部包的链接目录；测试仅将配套已安装的两个 DSO 放入隔离部署树。
    // 不执行 child 安装、不复制开发文件，正式外部包测试不需要此准备步骤。
    const QDir source(QString::fromUtf8(WAYLIB_RUNTIME_LIBRARY_DIRECTORY));
    const QString destination =
        stagedInstallPath(stage, QString::fromUtf8(DECKSHELL_LIBRARY_INSTALL_DIRECTORY));
    if (!QDir().mkpath(destination))
        return QStringLiteral("cannot create runtime staging directory: ") + destination;
    for (const char *name : { WAYLIB_RUNTIME_LIBRARY_FILENAME, WAYLIB_NATIVE_LIBRARY_FILENAME }) {
        QFile library(source.filePath(QString::fromUtf8(name)));
        if (!library.copy(QDir(destination).filePath(QString::fromUtf8(name))))
            return library.fileName() + QStringLiteral(": ") + library.errorString();
    }
#else
    Q_UNUSED(stage)
#endif
    return { };
}

} // namespace

class QmlInstallSmokeTest : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void initTestCase();
    void stagedModuleIncludesItsPluginAndQml();
    void stagedPluginHasNoSourceOrBuildRpath();
    void stagedInstallLoadsDeckShellCompositorWithoutBuildTreeImports();

private:
    QTemporaryDir m_stage;
    QString m_qmlRoot;
    QString m_moduleDirectory;
    QString m_pluginPath;
};

void QmlInstallSmokeTest::initTestCase()
{
    QVERIFY2(m_stage.isValid(), "failed to create install staging directory");
    const QString waylibQmlRoot = QString::fromUtf8(WAYLIB_RUNTIME_QML_IMPORT_DIRECTORY);
    QVERIFY2(
        !waylibQmlRoot.isEmpty(),
        "embedded builds require DECKSHELL_TEST_WAYLIB_PREFIX pointing to a matching installed "
        "WaylibShared runtime; installed-only builds use their selected package");
    QVERIFY2(
        QFileInfo::exists(
            QDir(waylibQmlRoot).filePath(QStringLiteral("WaylibShared/QuickSharedServer/qmldir"))),
        "the selected WaylibShared runtime has no installed QML module");

    auto installEnvironment = cleanEnvironment();
    installEnvironment.insert(QStringLiteral("DESTDIR"), m_stage.path());
    const QString installError = runProcess(QString::fromUtf8(CMAKE_EXECUTABLE_PATH),
                                            { QStringLiteral("--install"),
                                              QString::fromUtf8(DECKSHELL_BUILD_DIRECTORY),
                                              QStringLiteral("--prefix"),
                                              QStringLiteral("/usr/local"),
                                              QStringLiteral("--component"),
                                              QStringLiteral("DeckShellQmlRuntime") },
                                            installEnvironment,
                                            30000);
    QVERIFY2(installError.isEmpty(), qPrintable(installError));
    const QString runtimeError = stageEmbeddedRuntime(m_stage.path());
    QVERIFY2(runtimeError.isEmpty(), qPrintable(runtimeError));

    m_qmlRoot =
        stagedInstallPath(m_stage.path(), QString::fromUtf8(DECKSHELL_QML_INSTALL_DIRECTORY));
    m_moduleDirectory = QDir(m_qmlRoot).filePath(QStringLiteral("DeckShell/Compositor"));
    m_pluginPath =
        QDir(m_moduleDirectory).filePath(QString::fromUtf8(DECKSHELL_QML_PLUGIN_FILENAME));
}

void QmlInstallSmokeTest::stagedModuleIncludesItsPluginAndQml()
{
    QVERIFY2(QFileInfo::exists(m_moduleDirectory + QStringLiteral("/qmldir")),
             "installed qmldir is missing");
    QVERIFY2(QFileInfo::exists(m_moduleDirectory + QStringLiteral("/core/qml/PrelaunchSplash.qml")),
             "installed QML implementation is missing");
    QVERIFY2(QFileInfo::exists(m_pluginPath), "installed QML plugin is missing");
}

void QmlInstallSmokeTest::stagedPluginHasNoSourceOrBuildRpath()
{
    QString dynamicSection;
    const QString error = runProcess(QString::fromUtf8(READELF_EXECUTABLE_PATH),
                                     { QStringLiteral("-d"), m_pluginPath },
                                     cleanEnvironment(),
                                     10000,
                                     &dynamicSection);
    QVERIFY2(error.isEmpty(), qPrintable(error));
    QVERIFY2(!dynamicSection.contains(QString::fromUtf8(DECKSHELL_BUILD_DIRECTORY)),
             qPrintable(dynamicSection));
    QVERIFY2(!dynamicSection.contains(QString::fromUtf8(DECKSHELL_SOURCE_DIRECTORY)),
             qPrintable(dynamicSection));
}

void QmlInstallSmokeTest::stagedInstallLoadsDeckShellCompositorWithoutBuildTreeImports()
{
    const QString sourcePath = QDir(m_stage.path()).filePath(QStringLiteral("ImportSmoke.qml"));
    QFile source(sourcePath);
    QVERIFY2(source.open(QIODevice::WriteOnly | QIODevice::Truncate),
             qPrintable(source.errorString()));
    const QByteArray contents = "import QtQuick\n"
                                "import QtQml 2.15\n"
                                "import DeckShell.Compositor 2.0\n"
                                "Item {\n"
                                "    width: 1\n"
                                "    height: 1\n"
                                "    Border { anchors.fill: parent }\n"
                                "    Component.onCompleted: Qt.quit()\n"
                                "}\n";
    QCOMPARE(source.write(contents), contents.size());
    source.close();

    auto environment = cleanEnvironment();
    const QString importPaths =
        m_qmlRoot + QDir::listSeparator() + QString::fromUtf8(WAYLIB_RUNTIME_QML_IMPORT_DIRECTORY);
    environment.insert(QStringLiteral("QML_IMPORT_PATH"), importPaths);
    environment.insert(QStringLiteral("QT_QPA_PLATFORM"), QStringLiteral("offscreen"));
    const QString error =
        runProcess(QString::fromUtf8(QML_EXECUTABLE_PATH), { sourcePath }, environment, 15000);
    QVERIFY2(error.isEmpty(), qPrintable(error));
}

QTEST_GUILESS_MAIN(QmlInstallSmokeTest)
#include "main.moc"
