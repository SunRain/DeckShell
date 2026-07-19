// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "seat/seatsmanager.h"
#include "surfaceclient.h"

#include <wbackend.h>
#include <winputdevice.h>
#include <wseat.h>
#include <wserver.h>
#include <wsurface.h>

#include <qwcompositor.h>
#include <qwdisplay.h>
#include <qwinputdevice.h>
#include <qwseat.h>

#include <QGuiApplication>
#include <QMouseEvent>
#include <QPointingDevice>
#include <QSignalSpy>
#include <QTest>

#include <memory>
#include <vector>

extern "C" {
#include <wlr/interfaces/wlr_keyboard.h>
#include <wlr/interfaces/wlr_pointer.h>
}

class MultiSeatTest : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void init();
    void assignsMigratesAndRemovesDevices();
    void removingSeatReassignsDevices();
    void keepsVideoBusKeyboardForBrightnessShortcuts();
    void keepsKeyboardAndPointerFocusPerSeat();
    void cleanup();

private:
    std::unique_ptr<WInputDevice> createPointer(wlr_pointer *pointer, const char *name);
    std::unique_ptr<WInputDevice> createKeyboard(wlr_keyboard *keyboard, const char *name);
    void detachDevices();

    std::unique_ptr<WServer> m_server;
    std::unique_ptr<SeatsManager> m_manager;
    WSeat *m_seat0 = nullptr;
    WSeat *m_seat1 = nullptr;
    wlr_pointer m_pointer0 = { };
    wlr_pointer m_pointer1 = { };
    wlr_keyboard m_keyboard0 = { };
    wlr_keyboard m_keyboard1 = { };
    wlr_keyboard m_videoBusKeyboard = { };
    std::unique_ptr<WInputDevice> m_pointerDevice0;
    std::unique_ptr<WInputDevice> m_pointerDevice1;
    std::unique_ptr<WInputDevice> m_keyboardDevice0;
    std::unique_ptr<WInputDevice> m_keyboardDevice1;
    std::unique_ptr<WInputDevice> m_videoBusDevice;
    QW_NAMESPACE::qw_compositor *m_compositor = nullptr;
    std::unique_ptr<SurfaceClient> m_client;
    std::vector<std::unique_ptr<WSurface>> m_surfaces;
};

std::unique_ptr<WInputDevice> MultiSeatTest::createPointer(wlr_pointer *pointer, const char *name)
{
    static const wlr_pointer_impl PointerImpl = {
        .name = "test-multi-seat-pointer",
    };
    wlr_pointer_init(pointer, &PointerImpl, name);
    auto *handle = QW_NAMESPACE::qw_input_device::create(&pointer->base);
    return std::make_unique<WInputDevice>(handle, true);
}

std::unique_ptr<WInputDevice> MultiSeatTest::createKeyboard(wlr_keyboard *keyboard,
                                                            const char *name)
{
    static const wlr_keyboard_impl KeyboardImpl = {
        .name = "test-multi-seat-keyboard",
    };
    wlr_keyboard_init(keyboard, &KeyboardImpl, name);
    auto *handle = QW_NAMESPACE::qw_input_device::create(&keyboard->base);
    return std::make_unique<WInputDevice>(handle, true);
}

void MultiSeatTest::init()
{
    m_server = std::make_unique<WServer>();
    m_manager = std::make_unique<SeatsManager>(m_server.get());
    m_seat0 = m_manager->createSeat(QStringLiteral("seat0"), true);
    m_seat1 = m_manager->createSeat(QStringLiteral("seat1"));
    m_server->attach(m_seat0);
    m_server->attach(m_seat1);
    m_compositor = QW_NAMESPACE::qw_compositor::create(m_server->handle()->handle(), 6, nullptr);
    QVERIFY(m_compositor);

    m_pointerDevice0 = createPointer(&m_pointer0, "seat0-pointer");
    m_pointerDevice1 = createPointer(&m_pointer1, "seat1-pointer");
    m_keyboardDevice0 = createKeyboard(&m_keyboard0, "seat0-keyboard");
    m_keyboardDevice1 = createKeyboard(&m_keyboard1, "seat1-keyboard");
    m_videoBusDevice = createKeyboard(&m_videoBusKeyboard, "Video Bus");

    m_server->start();
    m_manager->setupAllSeats(nullptr, nullptr, nullptr);
}

void MultiSeatTest::assignsMigratesAndRemovesDevices()
{
    m_manager->addDeviceRule(QStringLiteral("seat1"), QStringLiteral("^2:seat1-pointer$"));

    QCOMPARE(m_manager->autoAssignDevice(m_pointerDevice0.get()), m_seat0);
    QCOMPARE(m_manager->autoAssignDevice(m_pointerDevice1.get()), m_seat1);
    QCOMPARE(m_pointerDevice0->seat(), m_seat0);
    QCOMPARE(m_pointerDevice1->seat(), m_seat1);
    QVERIFY(m_seat0->deviceList().contains(m_pointerDevice0.get()));
    QVERIFY(m_seat1->deviceList().contains(m_pointerDevice1.get()));

    auto *qtPointer0 = m_pointerDevice0->qtDevice<QPointingDevice>();
    auto *qtPointer1 = m_pointerDevice1->qtDevice<QPointingDevice>();
    QVERIFY(qtPointer0);
    QVERIFY(qtPointer1);
    QMouseEvent event0(QEvent::MouseButtonPress,
                       QPointF(1, 1),
                       QPointF(1, 1),
                       Qt::LeftButton,
                       Qt::LeftButton,
                       Qt::NoModifier,
                       qtPointer0);
    QMouseEvent event1(QEvent::MouseButtonPress,
                       QPointF(1, 1),
                       QPointF(1, 1),
                       Qt::LeftButton,
                       Qt::LeftButton,
                       Qt::NoModifier,
                       qtPointer1);
    QCOMPARE(m_manager->getSeatForEvent(&event0), m_seat0);
    QCOMPARE(m_manager->getSeatForEvent(&event1), m_seat1);

    QSignalSpy reassignedSpy(m_manager.get(), &SeatsManager::deviceReassigned);
    m_manager->assignDeviceToSeat(m_pointerDevice1.get(), QStringLiteral("seat0"));
    QCOMPARE(m_pointerDevice1->seat(), m_seat0);
    QVERIFY(!m_seat1->deviceList().contains(m_pointerDevice1.get()));
    QVERIFY(m_seat0->deviceList().contains(m_pointerDevice1.get()));
    QCOMPARE(reassignedSpy.count(), 1);
    QCOMPARE(qvariant_cast<WInputDevice *>(reassignedSpy.at(0).at(0)), m_pointerDevice1.get());
    QCOMPARE(qvariant_cast<WSeat *>(reassignedSpy.at(0).at(1)), m_seat1);
    QCOMPARE(qvariant_cast<WSeat *>(reassignedSpy.at(0).at(2)), m_seat0);

    WBackend backend;
    m_manager->connectBackendSignals(&backend);
    QSignalSpy addedSpy(m_manager.get(), &SeatsManager::deviceAdded);
    QSignalSpy removedSpy(m_manager.get(), &SeatsManager::deviceRemoved);
    Q_EMIT backend.inputAdded(m_pointerDevice1.get());
    QCOMPARE(addedSpy.count(), 1);
    Q_EMIT backend.inputRemoved(m_pointerDevice1.get());
    QCOMPARE(removedSpy.count(), 1);
    QCOMPARE(m_pointerDevice1->seat(), nullptr);
    QVERIFY(!m_seat0->deviceList().contains(m_pointerDevice1.get()));
    QVERIFY(!m_manager->devicesForSeat(m_seat0).contains(m_pointerDevice1.get()));
}

void MultiSeatTest::removingSeatReassignsDevices()
{
    m_manager->assignDeviceToSeat(m_pointerDevice1.get(), QStringLiteral("seat1"));
    QCOMPARE(m_pointerDevice1->seat(), m_seat1);

    QSignalSpy reassignedSpy(m_manager.get(), &SeatsManager::deviceReassigned);
    WSeat *removedSeat = m_seat1;
    m_manager->removeSeat(QStringLiteral("seat1"));
    m_seat1 = nullptr;

    QCOMPARE(m_manager->getSeat(QStringLiteral("seat1")), nullptr);
    QCOMPARE(m_manager->fallbackSeat(), m_seat0);
    QCOMPARE(m_pointerDevice1->seat(), m_seat0);
    QCOMPARE(reassignedSpy.count(), 1);
    QCOMPARE(qvariant_cast<WSeat *>(reassignedSpy.at(0).at(1)), removedSeat);
    QCOMPARE(qvariant_cast<WSeat *>(reassignedSpy.at(0).at(2)), m_seat0);
}

void MultiSeatTest::keepsVideoBusKeyboardForBrightnessShortcuts()
{
    m_manager->assignDevice(m_videoBusDevice.get(), nullptr, nullptr, m_seat0);

    QCOMPARE(m_videoBusDevice->seat(), m_seat0);
    QVERIFY(m_seat0->deviceList().contains(m_videoBusDevice.get()));
}

void MultiSeatTest::keepsKeyboardAndPointerFocusPerSeat()
{
    m_manager->assignDeviceToSeat(m_pointerDevice0.get(), QStringLiteral("seat0"));
    m_manager->assignDeviceToSeat(m_keyboardDevice0.get(), QStringLiteral("seat0"));
    m_manager->assignDeviceToSeat(m_pointerDevice1.get(), QStringLiteral("seat1"));
    m_manager->assignDeviceToSeat(m_keyboardDevice1.get(), QStringLiteral("seat1"));

    m_client = std::make_unique<SurfaceClient>();
    QString error;
    QVERIFY2(m_client->connectTo(m_server.get(), m_compositor, &error), qPrintable(error));
    QVERIFY2(m_client->createSurfaces(2, &error), qPrintable(error));
    for (auto *nativeSurface : m_client->nativeSurfaces()) {
        auto *handle = QW_NAMESPACE::qw_surface::from(nativeSurface);
        QVERIFY(handle);
        m_surfaces.push_back(std::make_unique<WSurface>(handle));
    }

    m_seat0->setKeyboardFocusSurface(m_surfaces[0].get());
    m_seat1->setKeyboardFocusSurface(m_surfaces[1].get());
    m_seat0->handle()->pointer_notify_enter(m_client->nativeSurfaces()[0], 1.0, 1.0);
    m_seat1->handle()->pointer_notify_enter(m_client->nativeSurfaces()[1], 2.0, 2.0);

    QCOMPARE(m_seat0->keyboardFocusSurface(), m_surfaces[0].get());
    QCOMPARE(m_seat1->keyboardFocusSurface(), m_surfaces[1].get());
    QCOMPARE(m_seat0->pointerFocusSurface(), m_surfaces[0].get());
    QCOMPARE(m_seat1->pointerFocusSurface(), m_surfaces[1].get());

    m_seat0->setKeyboardFocusSurface(m_surfaces[1].get());
    m_seat0->handle()->pointer_notify_enter(m_client->nativeSurfaces()[1], 3.0, 3.0);
    QCOMPARE(m_seat0->keyboardFocusSurface(), m_surfaces[1].get());
    QCOMPARE(m_seat1->keyboardFocusSurface(), m_surfaces[1].get());
    QCOMPARE(m_seat0->pointerFocusSurface(), m_surfaces[1].get());
    QCOMPARE(m_seat1->pointerFocusSurface(), m_surfaces[1].get());
}

void MultiSeatTest::detachDevices()
{
    if (!m_manager)
        return;

    for (auto *seat : m_manager->seats()) {
        const auto devices = seat->deviceList();
        for (auto *device : devices)
            seat->detachInputDevice(device);
    }
}

void MultiSeatTest::cleanup()
{
    if (m_seat0 && m_seat0->isValid()) {
        m_seat0->setKeyboardFocusSurface(nullptr);
        m_seat0->handle()->pointer_notify_clear_focus();
    }
    if (m_seat1 && m_seat1->isValid()) {
        m_seat1->setKeyboardFocusSurface(nullptr);
        m_seat1->handle()->pointer_notify_clear_focus();
    }
    m_surfaces.clear();
    m_client.reset();

    detachDevices();
    m_pointerDevice0.reset();
    m_pointerDevice1.reset();
    m_keyboardDevice0.reset();
    m_keyboardDevice1.reset();
    m_videoBusDevice.reset();
    m_manager.reset();
    m_seat0 = nullptr;
    m_seat1 = nullptr;
    if (m_server->isRunning())
        m_server->stop();
    m_server.reset();

    wlr_pointer_finish(&m_pointer0);
    wlr_pointer_finish(&m_pointer1);
    wlr_keyboard_finish(&m_keyboard0);
    wlr_keyboard_finish(&m_keyboard1);
    wlr_keyboard_finish(&m_videoBusKeyboard);
    m_compositor = nullptr;
}

int main(int argc, char *argv[])
{
    WServer::initializeQPA();
    QGuiApplication app(argc, argv);
    MultiSeatTest test;
    return QTest::qExec(&test, argc, argv);
}

#include "main.moc"
