// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <QtTest/QTest>

#include <QtGui/QGuiApplication>
#include <QtQml/QQmlComponent>
#include <QtQml/QQmlEngine>

class QmlImportTest final : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void importDeckShellGamepadModule()
    {
        QQmlEngine engine;
#if defined(DECKGAMEPAD_QML_IMPORT_ROOT)
        engine.addImportPath(QStringLiteral(DECKGAMEPAD_QML_IMPORT_ROOT));
#endif

	        static const char qml[] = R"qml(
	import QtQml
	import DeckShell.DeckGamepad 1.0

		QtObject {
		    property int connectedCount: GamepadManager.connectedCount
		    property string diagnostic: GamepadManager.diagnostic
		    property string diagnosticKey: GamepadManager.diagnosticKey
		    property bool customMappingSupported: GamepadManager.customMapping.supported

		    property Gamepad gp: Gamepad {
		        deviceId: -1
		    }

		    property int hat0Direction: gp.hatDirection
		    property int hat1Direction: gp.hat1Direction
		    property int hat2Direction: gp.hat2Direction
		    property int hat3Direction: gp.hat3Direction

		    property GamepadActionRouter router: GamepadActionRouter {
		        active: false
		        gamepad: gp
		    }

	    property GamepadActionKeyMapper keyMapper: GamepadActionKeyMapper {
	        active: false
	        actionRouter: router
	    }

	    property ServiceActionRouter serviceRouter: ServiceActionRouter {
	        active: false
	        gamepad: gp
	    }

	    property GamepadKeyNavigation nav: GamepadKeyNavigation {
	        active: false
	        actionSource: serviceRouter
	    }
	}
	)qml";

        QQmlComponent component(&engine);
        component.setData(qml, QUrl(QStringLiteral("qrc:/deckgamepad_test.qml")));
        QVERIFY2(component.isReady(), qPrintable(component.errorString()));

        QObject *obj = component.create();
        QVERIFY2(obj != nullptr, qPrintable(component.errorString()));
        delete obj;
    }
};

int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);
    QmlImportTest tc;
    return QTest::qExec(&tc, argc, argv);
}

#include "test_qml_import.moc"
