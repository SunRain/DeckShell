// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <QtTest/QTest>

#include <deckshell/deckgamepad/providers/evdev/evdevprovider.h>
#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtCore/QDateTime>
#include <QtCore/QFile>
#include <QtCore/QJsonDocument>
#include <QtCore/QJsonObject>
#include <QtCore/QPointer>
#include <QtCore/QTemporaryDir>
#include <QtGui/QGuiApplication>
#include <QtGui/QKeyEvent>
#include <QtQml/QQmlComponent>
#include <QtQml/QQmlContext>
#include <QtQml/QQmlEngine>
#include <QtGui/QWindow>

#include "uinput_test_device.h"

#if defined(__linux__)
#include <fcntl.h>
#include <linux/input.h>
#include <unistd.h>
#endif

using namespace deckshell::deckgamepad;

class KeySink final : public QObject
{
    Q_OBJECT

public:
    int lastPressedKey = 0;
    int lastReleasedKey = 0;
    int pressCount = 0;
    int repeatPressCount = 0;
    int releaseCount = 0;

    Q_INVOKABLE void onPressed(int key, bool autoRepeat)
    {
        lastPressedKey = key;
        pressCount++;
        if (autoRepeat) {
            repeatPressCount++;
        }
    }

    Q_INVOKABLE void onReleased(int key)
    {
        lastReleasedKey = key;
        releaseCount++;
    }

protected:
    bool event(QEvent *e) override
    {
        if (e->type() == QEvent::KeyPress) {
            auto *ke = static_cast<QKeyEvent *>(e);
            onPressed(ke->key(), ke->isAutoRepeat());
            return true;
        }
        if (e->type() == QEvent::KeyRelease) {
            auto *ke = static_cast<QKeyEvent *>(e);
            onReleased(ke->key());
            return true;
        }
        return QObject::event(e);
    }
};

static QString writeRepeatProfile(const QDir &dir)
{
    const QString path = dir.filePath(QStringLiteral("action_mapping_profile.json"));

    QJsonObject root;
    root[QStringLiteral("version")] = QStringLiteral("1.0");

    QJsonObject repeat;
    repeat[QStringLiteral("enabled")] = true;
    repeat[QStringLiteral("delay_ms")] = 0;
    repeat[QStringLiteral("interval_ms")] = 10;
    root[QStringLiteral("repeat")] = repeat;

    root[QStringLiteral("button_bindings")] = QJsonObject{};
    root[QStringLiteral("axis_bindings")] = QJsonObject{};

    QFile file(path);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Truncate)) {
        return QString{};
    }
    file.write(QJsonDocument(root).toJson(QJsonDocument::Indented));
    file.close();

    return path;
}

class TestQmlKeyNavigationRepeatHoldE2e final : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void holdHat_generatesRepeat_releaseStops_andTargetSwitchKeepsConsistentRelease()
    {
#if !defined(__linux__)
        QSKIP("requires Linux uinput/udev");
#else
        const int probeFd = ::open("/dev/uinput", O_RDWR | O_NONBLOCK);
        if (probeFd < 0) {
            QSKIP("missing /dev/uinput access");
        }
        (void)::close(probeFd);

        QTemporaryDir dir;
        QVERIFY(dir.isValid());
        const QString profilePath = writeRepeatProfile(QDir(dir.path()));
        QVERIFY(!profilePath.isEmpty());

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
        cfg.enableLegacyDeckShellPaths = false;
        cfg.actionMappingProfilePathOverride = profilePath;

        QVERIFY(service.setRuntimeConfig(cfg));
        QVERIFY(service.start());

        const QString name = QStringLiteral("DeckGamepadRepeatHold-%1").arg(QDateTime::currentMSecsSinceEpoch());

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

        KeySink sinkA;
        KeySink sinkB;

        QQmlEngine engine;
#if defined(DECKGAMEPAD_QML_IMPORT_ROOT)
        engine.addImportPath(QStringLiteral(DECKGAMEPAD_QML_IMPORT_ROOT));
#endif
        engine.rootContext()->setContextProperty(QStringLiteral("_deckGamepadService"), &service);
        engine.rootContext()->setContextProperty(QStringLiteral("keySinkA"), &sinkA);
        engine.rootContext()->setContextProperty(QStringLiteral("keySinkB"), &sinkB);

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
        target: keySinkA
    }

    function switchTargetToB() {
        nav.target = keySinkB
    }
}
)qml").arg(deviceId);

        QQmlComponent component(&engine);
        component.setData(qml.toUtf8(), QUrl(QStringLiteral("qrc:/deckgamepad_keynav_repeat_hold_target.qml")));
        QVERIFY2(component.isReady(), qPrintable(component.errorString()));

        QPointer<QObject> obj = component.create();
        QVERIFY2(obj != nullptr, qPrintable(component.errorString()));

        QVERIFY(dev.emitAbs(ABS_HAT0Y, -1));
        QVERIFY(dev.sync());

        QTRY_VERIFY_WITH_TIMEOUT(sinkA.pressCount >= 1, 1500);
        QTRY_VERIFY_WITH_TIMEOUT(sinkA.repeatPressCount >= 1, 1500);

        QVERIFY(QMetaObject::invokeMethod(obj.data(), "switchTargetToB"));
        QTRY_VERIFY_WITH_TIMEOUT(sinkA.releaseCount >= 1, 1500);
        QTRY_VERIFY_WITH_TIMEOUT(sinkB.repeatPressCount >= 1, 1500);

        QVERIFY(dev.emitAbs(ABS_HAT0Y, 0));
        QVERIFY(dev.sync());

        QTRY_VERIFY_WITH_TIMEOUT(sinkB.releaseCount >= 1, 1500);

        const int pressCountAtRelease = sinkB.pressCount;
        const int repeatCountAtRelease = sinkB.repeatPressCount;
        QTest::qWait(200);
        QCOMPARE(sinkB.pressCount, pressCountAtRelease);
        QCOMPARE(sinkB.repeatPressCount, repeatCountAtRelease);

        dev = UinputTestDevice{};
        obj->deleteLater();
        QCoreApplication::processEvents();
        service.stop();
#endif
    }

    void pressedTargetDestroyed_releaseFallsBackToCurrentTarget()
    {
#if !defined(__linux__)
        QSKIP("requires Linux uinput/udev");
#else
        const int probeFd = ::open("/dev/uinput", O_RDWR | O_NONBLOCK);
        if (probeFd < 0) {
            QSKIP("missing /dev/uinput access");
        }
        (void)::close(probeFd);

        QTemporaryDir dir;
        QVERIFY(dir.isValid());
        const QString profilePath = writeRepeatProfile(QDir(dir.path()));
        QVERIFY(!profilePath.isEmpty());

        auto *provider = new EvdevProvider();
        DeckGamepadService service(provider);

        DeckGamepadRuntimeConfig cfg = service.runtimeConfig();
        cfg.providerSelection = DeckGamepadProviderSelection::EvdevUdev;
        cfg.deviceAccessMode = DeckGamepadDeviceAccessMode::DirectOpen;
        cfg.capturePolicy = DeckGamepadCapturePolicy::Always;
        cfg.grabMode = DeckGamepadEvdevGrabMode::Shared;
        cfg.enableAutoRetryOpen = false;
        cfg.enableLegacyDeckShellPaths = false;
        cfg.actionMappingProfilePathOverride = profilePath;

        QVERIFY(service.setRuntimeConfig(cfg));
        QVERIFY(service.start());

        const QString name = QStringLiteral("DeckGamepadRepeatHoldDestroy-%1").arg(QDateTime::currentMSecsSinceEpoch());

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

        KeySink sinkB;
        auto *sinkA = new KeySink();

        QQmlEngine engine;
#if defined(DECKGAMEPAD_QML_IMPORT_ROOT)
        engine.addImportPath(QStringLiteral(DECKGAMEPAD_QML_IMPORT_ROOT));
#endif
        engine.rootContext()->setContextProperty(QStringLiteral("_deckGamepadService"), &service);
        engine.rootContext()->setContextProperty(QStringLiteral("keySinkA"), sinkA);
        engine.rootContext()->setContextProperty(QStringLiteral("keySinkB"), &sinkB);

        const QString qml = QStringLiteral(R"qml(
import QtQuick
import QtQuick.Window
import DeckShell.DeckGamepad 1.0

Window {
    id: win
    width: 160
    height: 90
    visible: true
    Component.onCompleted: b.forceActiveFocus()

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
        target: keySinkA
    }

    Item {
        id: b
        anchors.fill: parent
        focus: true
        Keys.enabled: true
        Keys.onPressed: (event) => {
            if (event.key === Qt.Key_Up) {
                keySinkB.onPressed(event.key, event.isAutoRepeat)
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
}
)qml").arg(deviceId);

        QQmlComponent component(&engine);
        component.setData(qml.toUtf8(), QUrl(QStringLiteral("qrc:/deckgamepad_keynav_repeat_hold_destroy.qml")));
        QVERIFY2(component.isReady(), qPrintable(component.errorString()));

        QPointer<QObject> obj = component.create();
        QVERIFY2(obj != nullptr, qPrintable(component.errorString()));

        auto *window = qobject_cast<QWindow *>(obj.data());
        QVERIFY(window != nullptr);
        window->requestActivate();
        QTest::qWait(20);

        QObject *navObj = obj->property("nav").value<QObject *>();
        QVERIFY(navObj != nullptr);

        const QString suppression = navObj->property("suppressionReason").toString();
        if (!suppression.isEmpty()) {
            QSKIP(qPrintable(QStringLiteral("suppressed: %1").arg(suppression)));
        }

        QVERIFY(dev.emitAbs(ABS_HAT0Y, -1));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sinkA->repeatPressCount >= 1, 1500);

        delete sinkA;
        sinkA = nullptr;

        QTRY_VERIFY_WITH_TIMEOUT(sinkB.repeatPressCount >= 1, 1500);

        QVERIFY(dev.emitAbs(ABS_HAT0Y, 0));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sinkB.releaseCount >= 1, 1500);

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
    TestQmlKeyNavigationRepeatHoldE2e tc;
    return QTest::qExec(&tc, argc, argv);
}

#include "test_qml_keynavigation_repeat_hold_e2e.moc"
