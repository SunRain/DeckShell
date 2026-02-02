// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <QtTest/QTest>

#include <deckshell/deckgamepad/core/deckgamepadaction.h>
#include <deckshell/deckgamepad/mapping/deckgamepadcustommappingmanager.h>
#include <deckshell/deckgamepad/providers/evdev/evdevprovider.h>
#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QtCore/QDateTime>
#include <QtCore/QFile>
#include <QtCore/QPointer>
#include <QtCore/QTemporaryDir>
#include <QtGui/QGuiApplication>
#include <QtGui/QKeyEvent>
#include <QtQml/QQmlComponent>
#include <QtQml/QQmlContext>
#include <QtQml/QQmlEngine>

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

class TestCustomMappingEvdevE2e final : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void customMappingOverridesDefaultMapping()
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

        // UinputTestDevice uses vendor=0x1234, product=0x5678, bus=USB, version=1 (see uinput_test_device.cpp).
        static const QString guid = QStringLiteral("03000000341200007856000001000000");
        const QString mappingFile = dir.filePath(QStringLiteral("custom_gamepad_mappings.txt"));

        QFile file(mappingFile);
        QVERIFY(file.open(QIODevice::WriteOnly | QIODevice::Truncate | QIODevice::Text));
        file.write(
            (guid
             + QStringLiteral(
                 ",DeckGamepad Test,a:b1,b:b0,x:b2,y:b3,dpup:h0.1,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,platform:Linux\n"))
                .toUtf8());
        file.close();

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
        cfg.customMappingPathOverride = mappingFile;

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

        const QString qml = QStringLiteral(R"qml(
import QtQml
import DeckShell.DeckGamepad 1.0

QtObject {
    property int selectedDeviceId: %1

    property Gamepad gp: Gamepad { deviceId: selectedDeviceId }

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
        component.setData(qml.toUtf8(), QUrl(QStringLiteral("qrc:/deckgamepad_custom_mapping_evdev_e2e.qml")));
        QVERIFY2(component.isReady(), qPrintable(component.errorString()));

        QPointer<QObject> obj = component.create();
        QVERIFY2(obj != nullptr, qPrintable(component.errorString()));

        QString lastActionId;
        bool lastActionPressed = false;
        QObject::connect(&service,
                         &DeckGamepadService::actionTriggered,
                         obj,
                         [&](int id, const QString &actionId, bool pressed, bool repeated) {
                             Q_UNUSED(repeated);
                             if (id != deviceId) {
                                 return;
                             }
                             lastActionId = actionId;
                             lastActionPressed = pressed;
                         });

        auto resetTracking = [&] {
            lastActionId.clear();
            lastActionPressed = false;
            sink.lastPressedKey = 0;
            sink.lastReleasedKey = 0;
            sink.pressCount = 0;
            sink.releaseCount = 0;
        };

        // Baseline: default mapping should map BTN_SOUTH to NavAccept → Qt::Key_Return.
        resetTracking();
        QVERIFY(dev.emitKey(BTN_SOUTH, 1));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sink.pressCount >= 1, 1500);
        QCOMPARE(sink.lastPressedKey, static_cast<int>(Qt::Key_Return));
        QTRY_VERIFY_WITH_TIMEOUT(!lastActionId.isEmpty(), 1500);
        QCOMPARE(lastActionId, QString::fromLatin1(DeckGamepadActionId::NavAccept));
        QVERIFY(lastActionPressed);

        QVERIFY(dev.emitKey(BTN_SOUTH, 0));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sink.releaseCount >= 1, 1500);
        QCOMPARE(sink.lastReleasedKey, static_cast<int>(Qt::Key_Return));

        // Apply custom mapping from file: swap A/B so BTN_SOUTH becomes NavBack → Qt::Key_Escape.
        auto *mgr = service.customMappingManager();
        QVERIFY(mgr != nullptr);
        QTRY_VERIFY_WITH_TIMEOUT(mgr->hasCustomMapping(deviceId), 1500);
        QVERIFY(mgr->applyMapping(deviceId));
        QTest::qWait(50);

        resetTracking();
        QVERIFY(dev.emitKey(BTN_SOUTH, 1));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sink.pressCount >= 1, 1500);
        QCOMPARE(sink.lastPressedKey, static_cast<int>(Qt::Key_Escape));
        QTRY_VERIFY_WITH_TIMEOUT(!lastActionId.isEmpty(), 1500);
        QCOMPARE(lastActionId, QString::fromLatin1(DeckGamepadActionId::NavBack));
        QVERIFY(lastActionPressed);

        QVERIFY(dev.emitKey(BTN_SOUTH, 0));
        QVERIFY(dev.sync());
        QTRY_VERIFY_WITH_TIMEOUT(sink.releaseCount >= 1, 1500);
        QCOMPARE(sink.lastReleasedKey, static_cast<int>(Qt::Key_Escape));

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
    TestCustomMappingEvdevE2e tc;
    return QTest::qExec(&tc, argc, argv);
}

#include "test_custom_mapping_evdev_e2e.moc"
