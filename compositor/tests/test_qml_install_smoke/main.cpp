// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QHash>
#include <QProcess>
#include <QProcessEnvironment>
#include <QRegularExpression>
#include <QSaveFile>
#include <QTemporaryDir>
#include <QTest>

#include <utility>

namespace {

QString runProcess(const QString &program,
                   const QStringList &arguments,
                   const QProcessEnvironment &environment,
                   int timeout)
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
        return QStringLiteral("process timed out");
    }
    if (process.exitStatus() != QProcess::NormalExit || process.exitCode() != 0) {
        const QString output = QString::fromLocal8Bit(process.readAll());
        constexpr qsizetype maximumErrorLength = 12000;
        if (output.size() > maximumErrorLength)
            return QStringLiteral("... install output truncated ...\n")
                + output.right(maximumErrorLength);
        return output;
    }
    return { };
}

QStringList runtimeInstallScripts()
{
    const QDir buildDirectory(QString::fromUtf8(DECKSHELL_BUILD_DIRECTORY));
    return {
        buildDirectory.filePath(
            QStringLiteral("3rdparty/waylib-shared/waylib/src/server/cmake_install.cmake")),
        buildDirectory.filePath(
            QStringLiteral("compositor/src/modules/capture/cmake_install.cmake")),
        buildDirectory.filePath(QStringLiteral("compositor/src/cmake_install.cmake")),
    };
}

QString runRuntimeInstall(const QStringList &installScripts,
                          const QProcessEnvironment &environment,
                          int timeout)
{
    for (const QString &installScript : installScripts) {
        const QString error =
            runProcess(QString::fromUtf8(CMAKE_EXECUTABLE_PATH),
                       { QStringLiteral("-DCMAKE_INSTALL_PREFIX=/usr/local"),
                         QStringLiteral("-DCMAKE_INSTALL_COMPONENT=DeckShellQmlRuntime"),
                         QStringLiteral("-DCMAKE_INSTALL_LOCAL_ONLY=TRUE"),
                         QStringLiteral("-P"),
                         installScript },
                       environment,
                       timeout);
        if (!error.isEmpty())
            return error;
    }
    return { };
}

class InstallScriptRpathCompatibilityPatch
{
public:
    explicit InstallScriptRpathCompatibilityPatch(QStringList installScripts)
        : m_installScripts(std::move(installScripts))
    {
    }

    ~InstallScriptRpathCompatibilityPatch()
    {
        QString ignoredError;
        restore(&ignoredError);
    }

    bool apply(QString *error)
    {
        for (const QString &path : m_installScripts) {
            QFile file(path);
            if (!file.open(QIODevice::ReadOnly)) {
                *error = file.errorString();
                return false;
            }

            const QByteArray original = file.readAll();
            const QByteArray patched = removeNormalizedRpathPadding(original);
            if (patched == original)
                continue;

            if (!writeFile(path, patched, error))
                return false;
            m_originals.insert(path, original);
        }

        if (m_originals.isEmpty()) {
            *error = QStringLiteral("no generated install RPATH entries were found");
            return false;
        }
        return true;
    }

private:
    static QByteArray removeNormalizedRpathPadding(const QByteArray &contents)
    {
        static const QRegularExpression expression(QStringLiteral(R"(OLD_RPATH "([^"]*):")"));

        QString patched = QString::fromUtf8(contents);

        struct Replacement
        {
            qsizetype offset;
            qsizetype length;
            QString text;
        };

        QList<Replacement> replacements;

        auto matchIterator = expression.globalMatch(patched);
        while (matchIterator.hasNext()) {
            const QRegularExpressionMatch match = matchIterator.next();
            QString oldRpath = match.captured(1);
            if (QString(oldRpath).remove(QLatin1Char(':')).isEmpty())
                oldRpath.clear();
            replacements.append(
                { match.capturedStart(),
                  match.capturedLength(),
                  QStringLiteral("OLD_RPATH \"") + oldRpath + QStringLiteral("\"") });
        }

        for (auto iterator = replacements.crbegin(); iterator != replacements.crend(); ++iterator)
            patched.replace(iterator->offset, iterator->length, iterator->text);
        return patched.toUtf8();
    }

    static bool writeFile(const QString &path, const QByteArray &contents, QString *error)
    {
        QSaveFile file(path);
        if (!file.open(QIODevice::WriteOnly)) {
            *error = file.errorString();
            return false;
        }
        if (file.write(contents) != contents.size()) {
            *error = file.errorString();
            file.cancelWriting();
            return false;
        }
        if (!file.commit()) {
            *error = file.errorString();
            return false;
        }
        return true;
    }

    void restore(QString *error)
    {
        for (auto iterator = m_originals.cbegin(); iterator != m_originals.cend(); ++iterator) {
            if (!writeFile(iterator.key(), iterator.value(), error))
                return;
        }
        m_originals.clear();
    }

    QStringList m_installScripts;
    QHash<QString, QByteArray> m_originals;
};

} // namespace

class QmlInstallSmokeTest : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void stagedInstallLoadsDeckShellCompositorWithoutBuildTreeImports();
};

void QmlInstallSmokeTest::stagedInstallLoadsDeckShellCompositorWithoutBuildTreeImports()
{
    QTemporaryDir stage;
    QVERIFY2(stage.isValid(), "failed to create install staging directory");
    QTemporaryDir compatibilityStage;

    auto installEnvironment = QProcessEnvironment::systemEnvironment();
    installEnvironment.insert(QStringLiteral("DESTDIR"), stage.path());
    const QStringList installScripts = runtimeInstallScripts();
    QString installError = runRuntimeInstall(installScripts, installEnvironment, 30000);

    QString activeStagePath = stage.path();
    if (!installError.isEmpty()) {
        QVERIFY2(
            installError.contains(QStringLiteral("file RPATH_CHANGE could not write new RPATH")),
            qPrintable(installError));
        QVERIFY2(compatibilityStage.isValid(), "failed to create compatibility staging directory");

        InstallScriptRpathCompatibilityPatch compatibilityPatch(installScripts);
        QString patchError;
        QVERIFY2(compatibilityPatch.apply(&patchError), qPrintable(patchError));

        qWarning().noquote()
            << "CMake generated a normalized ELF RUNPATH mismatch; retrying the staged install"
            << "with transactionally patched generated install scripts.";
        installEnvironment.insert(QStringLiteral("DESTDIR"), compatibilityStage.path());
        installError = runRuntimeInstall(installScripts, installEnvironment, 30000);
        activeStagePath = compatibilityStage.path();
    }
    if (!installError.isEmpty())
        qWarning().noquote() << installError;
    QVERIFY2(installError.isEmpty(), qPrintable(installError));

    const QString prefix = QDir(activeStagePath).filePath(QStringLiteral("usr/local"));
    const QString qmlRoot = prefix + QStringLiteral("/lib/qt6/qml");
    const QString moduleDir = qmlRoot + QStringLiteral("/DeckShell/Compositor");
    const QString pluginPath = moduleDir + QStringLiteral("/liblibdeckcompositorplugin.so");

    QVERIFY2(QFileInfo::exists(moduleDir + QStringLiteral("/qmldir")),
             "installed qmldir is missing");
    QVERIFY2(QFileInfo::exists(moduleDir + QStringLiteral("/core/qml/PrelaunchSplash.qml")),
             "installed QML implementation is missing");
    QVERIFY2(QFileInfo::exists(pluginPath), "installed QML plugin is missing");

    const auto cleanEnvironment = [] {
        auto environment = QProcessEnvironment::systemEnvironment();
        environment.remove(QStringLiteral("LD_LIBRARY_PATH"));
        environment.remove(QStringLiteral("QML_IMPORT_PATH"));
        environment.remove(QStringLiteral("QML2_IMPORT_PATH"));
        return environment;
    };

    const QString readelfError = runProcess(QString::fromUtf8(READELF_EXECUTABLE_PATH),
                                            { QStringLiteral("-d"), pluginPath },
                                            cleanEnvironment(),
                                            10000);
    QVERIFY2(readelfError.isEmpty(), qPrintable(readelfError));

    QProcess readelf;
    readelf.setProcessEnvironment(cleanEnvironment());
    readelf.setProcessChannelMode(QProcess::MergedChannels);
    readelf.start(QString::fromUtf8(READELF_EXECUTABLE_PATH), { QStringLiteral("-d"), pluginPath });
    QVERIFY2(readelf.waitForFinished(10000), qPrintable(readelf.errorString()));
    const QString dynamicSection = QString::fromLocal8Bit(readelf.readAll());
    QVERIFY2(!dynamicSection.contains(QString::fromUtf8(DECKSHELL_BUILD_DIRECTORY)),
             qPrintable(dynamicSection));

    const QString sourcePath = QDir(activeStagePath).filePath(QStringLiteral("ImportSmoke.qml"));
    QFile source(sourcePath);
    QVERIFY2(source.open(QIODevice::WriteOnly | QIODevice::Truncate),
             qPrintable(source.errorString()));
    source.write("import QtQuick\n"
                 "import QtQml 2.15\n"
                 "import DeckShell.Compositor 2.0\n"
                 "Item {\n"
                 "    width: 1\n"
                 "    height: 1\n"
                 "    Border { anchors.fill: parent }\n"
                 "    Component.onCompleted: Qt.quit()\n"
                 "}\n");
    source.close();

    auto qmlEnvironment = cleanEnvironment();
#ifdef EXTERNAL_RUNTIME_LIBRARY_DIRECTORY
    // DDM is a separately packaged runtime dependency. The staged DeckShell
    // install must not copy or claim ownership of it, but the loader still
    // needs the directory of the DDM installation used for this build.
    qmlEnvironment.insert(QStringLiteral("LD_LIBRARY_PATH"),
                          QString::fromUtf8(EXTERNAL_RUNTIME_LIBRARY_DIRECTORY));
#endif
    qmlEnvironment.insert(QStringLiteral("QML_IMPORT_PATH"), qmlRoot);
    qmlEnvironment.insert(QStringLiteral("QML2_IMPORT_PATH"), qmlRoot);
    qmlEnvironment.insert(QStringLiteral("QT_QPA_PLATFORM"), QStringLiteral("offscreen"));
    const QString qmlError = runProcess(QString::fromUtf8(QML_EXECUTABLE_PATH),
                                        { QStringLiteral("-I"), qmlRoot, sourcePath },
                                        qmlEnvironment,
                                        15000);
    QVERIFY2(qmlError.isEmpty(), qPrintable(qmlError));
}

QTEST_GUILESS_MAIN(QmlInstallSmokeTest)
#include "main.moc"
