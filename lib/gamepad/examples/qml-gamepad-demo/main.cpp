// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQuickStyle>

int main(int argc, char *argv[])
{
    if (qEnvironmentVariableIsEmpty("QT_QUICK_CONTROLS_STYLE")) {
        QQuickStyle::setStyle(QStringLiteral("Basic"));
    }

    QGuiApplication app(argc, argv);

    QQmlApplicationEngine engine;
#if defined(DECKSHELL_GAMEPAD_QML_IMPORT_ROOT)
    engine.addImportPath(QStringLiteral(DECKSHELL_GAMEPAD_QML_IMPORT_ROOT));
#endif
    const QByteArray extraImportRoot = qgetenv("DECKSHELL_GAMEPAD_QML_IMPORT_ROOT");
    if (!extraImportRoot.isEmpty()) {
        engine.addImportPath(QString::fromUtf8(extraImportRoot));
    }

    QObject::connect(
        &engine,
        &QQmlApplicationEngine::objectCreationFailed,
        &app,
        []() {
            QCoreApplication::exit(-1);
        },
        Qt::QueuedConnection);

    engine.loadFromModule("deckshell.gamepad.demo", "Main");

    return app.exec();
}
