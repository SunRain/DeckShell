// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <QtTest/QTest>
#include <QtTest/QSignalSpy>

#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtGui/QGuiApplication>
#include <QtGui/QKeyEvent>
#include <QtQml/QQmlComponent>
#include <QtQml/QQmlContext>
#include <QtQml/QQmlEngine>
#include <QtQml/qqml.h>

#include "testprovider.h"

using namespace deckshell::deckgamepad;

class KeySink final : public QObject
{
    Q_OBJECT

public:
    int lastPressedKey = 0;
    int lastReleasedKey = 0;
    int pressCount = 0;
    int releaseCount = 0;

protected:
    bool event(QEvent *e) override
    {
        if (e->type() == QEvent::KeyPress) {
            auto *ke = static_cast<QKeyEvent *>(e);
            lastPressedKey = ke->key();
            pressCount++;
            return true;
        }
        if (e->type() == QEvent::KeyRelease) {
            auto *ke = static_cast<QKeyEvent *>(e);
            lastReleasedKey = ke->key();
            releaseCount++;
            return true;
        }
        return QObject::event(e);
    }
};

class TestQmlKeyNavigationServiceAction final : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void hatUpInjectsQtKeyUp()
    {
        auto *provider = new TestGamepadProvider();
        DeckGamepadService service(provider);
        QVERIFY(service.start());

        KeySink sink;
        QSignalSpy serviceSpy(&service, SIGNAL(actionTriggered(int,QString,bool,bool)));

        QQmlEngine engine;
#if defined(DECKGAMEPAD_QML_IMPORT_ROOT)
        engine.addImportPath(QStringLiteral(DECKGAMEPAD_QML_IMPORT_ROOT));
#endif
        engine.rootContext()->setContextProperty(QStringLiteral("_deckGamepadService"), &service);
        engine.rootContext()->setContextProperty(QStringLiteral("keySink"), &sink);

        {
            const QVariant injected = engine.rootContext()->contextProperty(QStringLiteral("_deckGamepadService"));
            QObject *obj = injected.value<QObject *>();
            QVERIFY(obj == &service);
            QVERIFY(qobject_cast<DeckGamepadService *>(obj) != nullptr);
        }

        static const char qml[] = R"qml(
import QtQml
import DeckShell.DeckGamepad 1.0

QtObject {
    property int selectedDeviceId: 1

    property Gamepad gp: Gamepad {
        deviceId: selectedDeviceId
    }

    property ServiceActionRouter router: ServiceActionRouter {
        active: true
        gamepad: gp
        service: _deckGamepadService
    }

    property GamepadKeyNavigation nav: GamepadKeyNavigation {
        active: true
        gamepad: gp
        actionSource: router
        target: keySink
    }
}
)qml";

        QQmlComponent component(&engine);
        component.setData(qml, QUrl(QStringLiteral("qrc:/deckgamepad_keynav_service_action.qml")));
        QVERIFY2(component.isReady(), qPrintable(component.errorString()));

        QObject *obj = component.create();
        QVERIFY2(obj != nullptr, qPrintable(component.errorString()));

        QObject *gpObj = obj->property("gp").value<QObject *>();
        QVERIFY(gpObj != nullptr);
        QCOMPARE(qmlEngine(gpObj), &engine);
        QCOMPARE(gpObj->property("deviceId").toInt(), 1);

        QObject *routerObj = obj->property("router").value<QObject *>();
        QVERIFY(routerObj != nullptr);
        QCOMPARE(qmlEngine(routerObj), &engine);
        QVERIFY(routerObj->property("active").toBool());
        QSignalSpy routerSpy(routerObj, SIGNAL(actionTriggered(QString,bool,bool)));

        QObject *navObj = obj->property("nav").value<QObject *>();
        QVERIFY(navObj != nullptr);
        QCOMPARE(qmlEngine(navObj), &engine);

        DeckGamepadHatEvent hat;
        hat.time_msec = 1;
        hat.hat = 0;
        hat.value = GAMEPAD_HAT_UP;
        provider->emitHatEvent(1, hat);

        QTRY_VERIFY_WITH_TIMEOUT(serviceSpy.count() >= 1, 200);
        QTRY_VERIFY_WITH_TIMEOUT(routerSpy.count() >= 1, 200);
        QTRY_VERIFY_WITH_TIMEOUT(sink.pressCount >= 1, 200);
        QCOMPARE(sink.lastPressedKey, static_cast<int>(Qt::Key_Up));

        hat.time_msec = 2;
        hat.value = GAMEPAD_HAT_CENTER;
        provider->emitHatEvent(1, hat);

        QTRY_VERIFY_WITH_TIMEOUT(sink.releaseCount >= 1, 200);
        QCOMPARE(sink.lastReleasedKey, static_cast<int>(Qt::Key_Up));

        delete obj;
    }
};

int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);
    TestQmlKeyNavigationServiceAction tc;
    return QTest::qExec(&tc, argc, argv);
}

#include "test_qml_keynavigation_service_action.moc"
