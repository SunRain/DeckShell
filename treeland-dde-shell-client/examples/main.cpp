#include "launcher.h"
#include "widgetdemo.h"

#include <QApplication>
#include <QDebug>
#include <QQmlApplicationEngine>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    // Create launcher
    Launcher launcher;

    // Widget demo instance (created on demand)
    WidgetDemo *widgetDemo = nullptr;

    // QML engine instance (created on demand)
    QQmlApplicationEngine *qmlEngine = nullptr;

    // Handle Widget Demo request
    QObject::connect(&launcher, &Launcher::widgetDemoRequested, [&]() {
        qDebug() << "Launching Widget Demo...";

        if (!widgetDemo) {
            widgetDemo = new WidgetDemo();
        }

        widgetDemo->show();
        widgetDemo->raise();
        widgetDemo->activateWindow();
    });

    // Handle QML Demo request
    QObject::connect(&launcher, &Launcher::qmlDemoRequested, [&]() {
        qDebug() << "Launching QML Demo...";

        if (!qmlEngine) {
            qmlEngine = new QQmlApplicationEngine(&app);

            // Add QML import path
#ifdef QML_PLUGIN_PATH
            qmlEngine->addImportPath(QStringLiteral(QML_PLUGIN_PATH));
            qDebug() << "Added QML import path:" << QML_PLUGIN_PATH;
#endif

            // Load QML file
            // URI "ddeshellclient.unified.demo" is converted to path "ddeshellclient/unified/demo"
            const QUrl url(QStringLiteral("qrc:/qt/qml/ddeshellclient/unified/demo/demo.qml"));
            qmlEngine->load(url);

            if (qmlEngine->rootObjects().isEmpty()) {
                qWarning() << "Failed to load QML demo";
                delete qmlEngine;
                qmlEngine = nullptr;
            }
        }
    });

    launcher.show();

    return app.exec();
}
