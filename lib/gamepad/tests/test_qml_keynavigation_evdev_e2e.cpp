// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <QtTest/QTest>
#include <QtTest/QSignalSpy>

#include <deckshell/deckgamepad/core/deckgamepadaction.h>
#include <deckshell/deckgamepad/providers/evdev/evdevprovider.h>
#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtCore/QDateTime>
#include <QtCore/QPointer>
#include <QtGui/QGuiApplication>
#include <QtGui/QKeyEvent>
#include <QtQml/QQmlComponent>
#include <QtQml/QQmlContext>
#include <QtQml/QQmlEngine>

#include "uinput_test_device.h"

#if defined(__linux__)
#include <fcntl.h>
#include <unistd.h>
#include <linux/input.h>
#endif

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

class TestQmlKeyNavigationEvdevE2e final : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void hatUpInjectsQtKeyUp()
    {
#if !defined(__linux__)
        QSKIP("requires Linux uinput/udev");
#else
        const int probeFd = ::open("/dev/uinput", O_RDWR | O_NONBLOCK);
        if (probeFd < 0) {
            QSKIP("missing /dev/uinput access");
        }
        (void)::close(probeFd);

        // DeckGamepadService 会接管 provider 的 QObject 生命周期（setParent(this) + 析构时 delete），
        // 因此这里必须使用堆对象，避免栈对象被 delete 导致崩溃。
        auto *provider = new EvdevProvider();
        DeckGamepadService service(provider);

        DeckGamepadRuntimeConfig cfg = service.runtimeConfig();
        cfg.providerSelection = DeckGamepadProviderSelection::EvdevUdev;
        cfg.deviceAccessMode = DeckGamepadDeviceAccessMode::DirectOpen;
        cfg.capturePolicy = DeckGamepadCapturePolicy::Always;
        cfg.grabMode = DeckGamepadEvdevGrabMode::Shared;
        cfg.enableAutoRetryOpen = false;

        QVERIFY(service.setRuntimeConfig(cfg));
        QVERIFY(service.start());

        const QString name = QStringLiteral("DeckGamepadTest-%1").arg(QDateTime::currentMSecsSinceEpoch());

        int deviceId = -1;
        QObject::connect(&service, &DeckGamepadService::gamepadConnected, &service, [&](int id, const QString &n) {
            if (n == name) {
                deviceId = id;
            }
        });

        UinputTestDevice dev = UinputTestDevice::createGamepad(name);
        if (!dev.isValid()) {
            QSKIP("failed to create uinput gamepad device");
        }

        QTRY_VERIFY_WITH_TIMEOUT(deviceId >= 0, 5000);

        KeySink sink;

        QQmlEngine engine;
#if defined(DECKGAMEPAD_QML_IMPORT_ROOT)
        engine.addImportPath(QStringLiteral(DECKGAMEPAD_QML_IMPORT_ROOT));
#endif
        engine.rootContext()->setContextProperty(QStringLiteral("_deckGamepadService"), &service);
        engine.rootContext()->setContextProperty(QStringLiteral("keySink"), &sink);

        {
            const QVariant injected = engine.rootContext()->contextProperty(QStringLiteral("_deckGamepadService"));
            QObject *objSvc = injected.value<QObject *>();
            QVERIFY(objSvc == &service);
            QVERIFY(qobject_cast<DeckGamepadService *>(objSvc) != nullptr);
        }

        const QString qml = QStringLiteral(R"qml(
import QtQml
import DeckShell.DeckGamepad 1.0

QtObject {
    property int selectedDeviceId: %1

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
)qml").arg(deviceId);

        QQmlComponent component(&engine);
        component.setData(qml.toUtf8(), QUrl(QStringLiteral("qrc:/deckgamepad_keynav_evdev_e2e.qml")));
        QVERIFY2(component.isReady(), qPrintable(component.errorString()));

        QPointer<QObject> obj = component.create();
        QVERIFY2(obj != nullptr, qPrintable(component.errorString()));

        QObject *routerObj = obj->property("router").value<QObject *>();
        QVERIFY(routerObj != nullptr);
        QCOMPARE(qmlEngine(routerObj), &engine);
        QCOMPARE(routerObj->property("service").value<QObject *>(), &service);

        QSignalSpy routerSpy(routerObj, SIGNAL(actionTriggered(QString,bool,bool)));
        QVERIFY(routerSpy.isValid());

        QString lastActionId;
        bool sawNavUpPress = false;
        bool sawNavUpRelease = false;
        QObject::connect(&service,
                         &DeckGamepadService::actionTriggered,
                         obj,
                         [&](int id, const QString &actionId, bool pressed, bool repeated) {
                             Q_UNUSED(repeated);
                             if (id != deviceId) {
                                 return;
                             }
                             lastActionId = actionId;
                             if (actionId == QString::fromLatin1(DeckGamepadActionId::NavUp)) {
                                 if (pressed) {
                                     sawNavUpPress = true;
                                 } else {
                                     sawNavUpRelease = true;
                                 }
                             }
                         });

        auto routerSaw = [&](const QString &actionId, bool pressed) {
            for (int i = 0; i < routerSpy.count(); ++i) {
                const auto args = routerSpy.at(i);
                if (args.size() < 3) {
                    continue;
                }
                if (args.at(0).toString() == actionId && args.at(1).toBool() == pressed) {
                    return true;
                }
            }
            return false;
        };

        routerSpy.clear();
        QVERIFY(dev.emitAbs(ABS_HAT0Y, -1));
        QVERIFY(dev.sync());

        QTRY_VERIFY_WITH_TIMEOUT(routerSpy.count() >= 1, 1500);
        QVERIFY(routerSaw(QString::fromLatin1(DeckGamepadActionId::NavUp), true));

        QTRY_VERIFY_WITH_TIMEOUT(sawNavUpPress, 1500);
        QCOMPARE(lastActionId, QString::fromLatin1(DeckGamepadActionId::NavUp));

        QTRY_VERIFY_WITH_TIMEOUT(sink.pressCount >= 1, 1500);
        QCOMPARE(sink.lastPressedKey, static_cast<int>(Qt::Key_Up));

        routerSpy.clear();
        QVERIFY(dev.emitAbs(ABS_HAT0Y, 0));
        QVERIFY(dev.sync());

        QTRY_VERIFY_WITH_TIMEOUT(routerSpy.count() >= 1, 1500);
        QVERIFY(routerSaw(QString::fromLatin1(DeckGamepadActionId::NavUp), false));

        QTRY_VERIFY_WITH_TIMEOUT(sawNavUpRelease, 1500);
        QTRY_VERIFY_WITH_TIMEOUT(sink.releaseCount >= 1, 1500);
        QCOMPARE(sink.lastReleasedKey, static_cast<int>(Qt::Key_Up));

        dev = UinputTestDevice{};
        obj->deleteLater();
        QCoreApplication::processEvents();

        service.stop();
#endif
    }
};

int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);
    TestQmlKeyNavigationEvdevE2e tc;
    return QTest::qExec(&tc, argc, argv);
}

#include "test_qml_keynavigation_evdev_e2e.moc"
