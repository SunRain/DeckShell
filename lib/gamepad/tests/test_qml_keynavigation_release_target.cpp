// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <QtTest/QTest>

#include <QtCore/QPointer>
#include <QtGui/QGuiApplication>
#include <QtQml/QQmlComponent>
#include <QtQml/QQmlContext>
#include <QtQml/QQmlEngine>

class KeySink final : public QObject
{
    Q_OBJECT

public:
    int pressCount = 0;
    int releaseCount = 0;

    Q_INVOKABLE void onPressed(int key)
    {
        Q_UNUSED(key);
        pressCount++;
    }

    Q_INVOKABLE void onReleased(int key)
    {
        Q_UNUSED(key);
        releaseCount++;
    }
};

class TestQmlKeyNavigationReleaseTarget final : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void releaseAll_deliversToPressedTarget_evenIfFocusChanges()
    {
        KeySink sinkA;
        KeySink sinkB;

        QQmlEngine engine;
#if defined(DECKGAMEPAD_QML_IMPORT_ROOT)
        engine.addImportPath(QStringLiteral(DECKGAMEPAD_QML_IMPORT_ROOT));
#endif
        engine.rootContext()->setContextProperty(QStringLiteral("keySinkA"), &sinkA);
        engine.rootContext()->setContextProperty(QStringLiteral("keySinkB"), &sinkB);

        static const char qml[] = R"qml(
import QtQuick
import QtQuick.Window
import DeckShell.DeckGamepad 1.0

Window {
    id: win
    width: 160
    height: 90
    visible: true
    Component.onCompleted: a.forceActiveFocus()

    property int selectedDeviceId: 1

    Item {
        id: a
        anchors.fill: parent
        focus: true
        Keys.enabled: true
        Keys.onPressed: (event) => {
            if (event.key === Qt.Key_Up) {
                keySinkA.onPressed(event.key)
                event.accepted = true
            }
        }
        Keys.onReleased: (event) => {
            if (event.key === Qt.Key_Up) {
                keySinkA.onReleased(event.key)
                event.accepted = true
            }
        }
    }

    Item {
        id: b
        anchors.fill: parent
        Keys.enabled: true
        Keys.onPressed: (event) => {
            if (event.key === Qt.Key_Up) {
                keySinkB.onPressed(event.key)
                event.accepted = true
            }
        }
        Keys.onReleased: (event) => {
            if (event.key === Qt.Key_Up) {
                keySinkB.onReleased(event.key)
                event.accepted = true
            }
        }
    }

    function focusB() {
        b.forceActiveFocus()
    }

    property GamepadKeyNavigation nav: GamepadKeyNavigation {
        active: true
    }
}
)qml";

        QQmlComponent component(&engine);
        component.setData(qml, QUrl(QStringLiteral("qrc:/deckgamepad_keynav_release_target.qml")));
        QVERIFY2(component.isReady(), qPrintable(component.errorString()));

        QPointer<QObject> obj = component.create();
        QVERIFY2(obj != nullptr, qPrintable(component.errorString()));

        auto *window = qobject_cast<QWindow *>(obj.data());
        QVERIFY(window != nullptr);
        window->requestActivate();
        QTest::qWait(20);

        QObject *navObj = obj->property("nav").value<QObject *>();
        QVERIFY(navObj != nullptr);

        QVERIFY(QMetaObject::invokeMethod(navObj,
                                          "onActionTriggered",
                                          Q_ARG(QString, QStringLiteral("nav.up")),
                                          Q_ARG(bool, true),
                                          Q_ARG(bool, false)));

        const QString suppression = navObj->property("suppressionReason").toString();
        if (!suppression.isEmpty()) {
            QSKIP(qPrintable(QStringLiteral("suppressed: %1").arg(suppression)));
        }

        QTRY_VERIFY_WITH_TIMEOUT(sinkA.pressCount >= 1, 200);
        QCOMPARE(sinkB.pressCount, 0);
        QCOMPARE(sinkA.releaseCount, 0);

        QVERIFY(QMetaObject::invokeMethod(obj, "focusB"));

        navObj->setProperty("active", false);

        QTRY_VERIFY_WITH_TIMEOUT(sinkA.releaseCount >= 1, 200);
        QCOMPARE(sinkB.releaseCount, 0);

        obj->deleteLater();
    }
};

int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);
    TestQmlKeyNavigationReleaseTarget tc;
    return QTest::qExec(&tc, argc, argv);
}

#include "test_qml_keynavigation_release_target.moc"
