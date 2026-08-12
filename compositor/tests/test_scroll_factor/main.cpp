// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "seat/seatsmanager.h"

#include <wcursor.h>
#include <winputdevice.h>
#include <wseat.h>
#include <wserver.h>
#include <wscoplistener.h>

#include <QGuiApplication>
#include <QTest>
#include <QVector>

#include <algorithm>
#include <cerrno>
#include <cmath>
#include <cstring>
#include <memory>
#include <sys/socket.h>

extern "C" {
#include <wayland-client.h>
#include <wayland-server-core.h>
#include <wlr/interfaces/wlr_pointer.h>
}

namespace {

constexpr double AxisDelta = 10.0;

struct ClientState
{
    wl_display *display = nullptr;
    wl_registry *registry = nullptr;
    wl_compositor *compositor = nullptr;
    wl_seat *seat = nullptr;
    wl_pointer *pointer = nullptr;
    wl_surface *surface = nullptr;
    uint32_t compositorName = 0;
    uint32_t compositorVersion = 0;
    uint32_t seatName = 0;
    uint32_t seatVersion = 0;
    bool pointerEntered = false;
    QVector<double> axisValues;
};

void pointerEnter(void *data, wl_pointer *, uint32_t, wl_surface *, wl_fixed_t, wl_fixed_t)
{
    static_cast<ClientState *>(data)->pointerEntered = true;
}

void pointerAxis(void *data, wl_pointer *, uint32_t, uint32_t, wl_fixed_t value)
{
    static_cast<ClientState *>(data)->axisValues.append(wl_fixed_to_double(value));
}

void pointerLeave(void *, wl_pointer *, uint32_t, wl_surface *) { }

void pointerMotion(void *, wl_pointer *, uint32_t, wl_fixed_t, wl_fixed_t) { }

void pointerButton(void *, wl_pointer *, uint32_t, uint32_t, uint32_t, uint32_t) { }

void pointerFrame(void *, wl_pointer *) { }

void pointerAxisSource(void *, wl_pointer *, uint32_t) { }

void pointerAxisStop(void *, wl_pointer *, uint32_t, uint32_t) { }

void pointerAxisDiscrete(void *, wl_pointer *, uint32_t, int32_t) { }

void pointerAxisValue120(void *, wl_pointer *, uint32_t, int32_t) { }

void pointerAxisRelativeDirection(void *, wl_pointer *, uint32_t, uint32_t) { }

const wl_pointer_listener PointerListener = {
    .enter = pointerEnter,
    .leave = pointerLeave,
    .motion = pointerMotion,
    .button = pointerButton,
    .axis = pointerAxis,
    .frame = pointerFrame,
    .axis_source = pointerAxisSource,
    .axis_stop = pointerAxisStop,
    .axis_discrete = pointerAxisDiscrete,
    .axis_value120 = pointerAxisValue120,
    .axis_relative_direction = pointerAxisRelativeDirection,
};

void seatCapabilities(void *data, wl_seat *seat, uint32_t capabilities)
{
    auto *state = static_cast<ClientState *>(data);
    if (!(capabilities & WL_SEAT_CAPABILITY_POINTER) || state->pointer)
        return;

    state->pointer = wl_seat_get_pointer(seat);
    wl_pointer_add_listener(state->pointer, &PointerListener, state);
}

void seatName(void *, wl_seat *, const char *) { }

const wl_seat_listener SeatListener = {
    .capabilities = seatCapabilities,
    .name = seatName,
};

void registryGlobal(void *data,
                    wl_registry *,
                    uint32_t name,
                    const char *interface,
                    uint32_t version)
{
    auto *state = static_cast<ClientState *>(data);
    if (std::strcmp(interface, wl_compositor_interface.name) == 0) {
        state->compositorName = name;
        state->compositorVersion = version;
    } else if (std::strcmp(interface, wl_seat_interface.name) == 0) {
        state->seatName = name;
        state->seatVersion = version;
    }
}

const wl_registry_listener RegistryListener = {
    .global = registryGlobal,
    .global_remove = nullptr,
};

} // namespace

class ScrollFactorTest : public QObject
{
    Q_OBJECT

private Q_SLOTS:
    void initTestCase();
    void axisDeltaUsesConfiguredFactor_data();
    void axisDeltaUsesConfiguredFactor();
    void cleanupTestCase();

private:
    void dispatchServerRequests();
    void dispatchClientEvents();
    void bindClientGlobals();
    void destroyClient();

    std::unique_ptr<WAYLIB_SERVER_NAMESPACE::WServer> m_server;
    std::unique_ptr<SeatsManager> m_seatsManager;
    std::unique_ptr<WAYLIB_SERVER_NAMESPACE::WInputDevice> m_inputDevice;
    WAYLIB_SERVER_NAMESPACE::WSeat *m_seat = nullptr;
    WAYLIB_SERVER_NAMESPACE::WCursor *m_cursor = nullptr;
    wlr_compositor *m_compositor = nullptr;
    WAYLIB_SERVER_NAMESPACE::WScopedListener m_surfaceListener;
    wlr_surface *m_nativeSurface = nullptr;
    wlr_pointer m_nativePointer = { };
    wl_client *m_serverClient = nullptr;
    ClientState m_client;
};

void ScrollFactorTest::dispatchServerRequests()
{
    QVERIFY(wl_display_flush(m_client.display) >= 0);
    QCOMPARE(wl_event_loop_dispatch(wl_display_get_event_loop(m_server->handle()), 0), 0);
    wl_display_flush_clients(m_server->handle());
}

void ScrollFactorTest::dispatchClientEvents()
{
    QVERIFY(wl_display_dispatch(m_client.display) >= 0);
}

void ScrollFactorTest::bindClientGlobals()
{
    QVERIFY(m_client.compositorName != 0);
    QVERIFY(m_client.seatName != 0);

    m_client.compositor =
        static_cast<wl_compositor *>(wl_registry_bind(m_client.registry,
                                                      m_client.compositorName,
                                                      &wl_compositor_interface,
                                                      std::min(m_client.compositorVersion, 6U)));
    m_client.seat = static_cast<wl_seat *>(wl_registry_bind(m_client.registry,
                                                            m_client.seatName,
                                                            &wl_seat_interface,
                                                            std::min(m_client.seatVersion, 9U)));
    wl_seat_add_listener(m_client.seat, &SeatListener, &m_client);

    dispatchServerRequests();
    dispatchClientEvents();
    QVERIFY(m_client.pointer != nullptr);
}

void ScrollFactorTest::initTestCase()
{
    static const wlr_pointer_impl PointerImpl = {
        .name = "test-scroll-factor-pointer",
    };

    m_server = std::make_unique<WAYLIB_SERVER_NAMESPACE::WServer>();
    m_seatsManager = std::make_unique<SeatsManager>(m_server.get());
    m_seat = m_seatsManager->createSeat(QStringLiteral("seat0"), true);
    m_server->attach(m_seat);

    wlr_pointer_init(&m_nativePointer, &PointerImpl, "test-scroll-factor-pointer");
    m_inputDevice = std::make_unique<WAYLIB_SERVER_NAMESPACE::WInputDevice>(&m_nativePointer.base, true);
    QCOMPARE(m_inputDevice->handle(), &m_nativePointer.base);
    m_seat->attachInputDevice(m_inputDevice.get());

    m_compositor = wlr_compositor_create(m_server->handle(), 6, nullptr);
    QVERIFY(m_compositor != nullptr);
    m_surfaceListener.init(&m_compositor->events.new_surface, [this](wlr_surface *surface) {
        m_nativeSurface = surface;
    });

    m_server->start();
    m_seatsManager->setupAllSeats(nullptr, nullptr, nullptr);
    m_cursor = m_seat->cursor();
    QVERIFY(m_cursor != nullptr);

    int sockets[2] = { -1, -1 };
    QCOMPARE(::socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, sockets), 0);
    m_serverClient = wl_client_create(m_server->handle(), sockets[0]);
    QVERIFY2(m_serverClient != nullptr, std::strerror(errno));
    m_client.display = wl_display_connect_to_fd(sockets[1]);
    QVERIFY(m_client.display != nullptr);

    m_client.registry = wl_display_get_registry(m_client.display);
    wl_registry_add_listener(m_client.registry, &RegistryListener, &m_client);
    dispatchServerRequests();
    dispatchClientEvents();
    bindClientGlobals();

    m_client.surface = wl_compositor_create_surface(m_client.compositor);
    dispatchServerRequests();
    QVERIFY(m_nativeSurface != nullptr);

    wlr_seat_pointer_notify_enter(m_seat->handle(), m_nativeSurface, 0.0, 0.0);
    wl_display_flush_clients(m_server->handle());
    dispatchClientEvents();
    QVERIFY(m_client.pointerEntered);
}

void ScrollFactorTest::axisDeltaUsesConfiguredFactor_data()
{
    QTest::addColumn<double>("factor");
    QTest::addColumn<uint32_t>("source");
    QTest::addColumn<double>("expectedDelta");

    QTest::newRow("mouse-default") << 1.0 << uint32_t(WL_POINTER_AXIS_SOURCE_WHEEL) << 10.0;
    QTest::newRow("mouse-slower") << 0.5 << uint32_t(WL_POINTER_AXIS_SOURCE_WHEEL) << 5.0;
    QTest::newRow("mouse-faster") << 2.0 << uint32_t(WL_POINTER_AXIS_SOURCE_WHEEL) << 20.0;
    QTest::newRow("touchpad-slower") << 0.5 << uint32_t(WL_POINTER_AXIS_SOURCE_FINGER) << 5.0;
    QTest::newRow("touchpad-faster") << 2.0 << uint32_t(WL_POINTER_AXIS_SOURCE_FINGER) << 20.0;
}

void ScrollFactorTest::axisDeltaUsesConfiguredFactor()
{
    QFETCH(double, factor);
    QFETCH(uint32_t, source);
    QFETCH(double, expectedDelta);

    m_cursor->setScrollFactor(factor);
    m_client.axisValues.clear();

    wlr_pointer_axis_event event = {
        .pointer = &m_nativePointer,
        .time_msec = 42,
        .source = static_cast<wl_pointer_axis_source>(source),
        .orientation = WL_POINTER_AXIS_VERTICAL_SCROLL,
        .relative_direction = WL_POINTER_AXIS_RELATIVE_DIRECTION_IDENTICAL,
        .delta = AxisDelta,
        .delta_discrete = WLR_POINTER_AXIS_DISCRETE_STEP,
    };
    wl_signal_emit_mutable(&m_nativePointer.events.axis, &event);
    wl_signal_emit_mutable(&m_nativePointer.events.frame, &m_nativePointer);
    wl_display_flush_clients(m_server->handle());
    dispatchClientEvents();

    QCOMPARE(m_client.axisValues.size(), 1);
    QVERIFY(std::abs(m_client.axisValues.constFirst() - expectedDelta) < 0.001);
}

void ScrollFactorTest::destroyClient()
{
    if (!m_client.display)
        return;

    if (m_client.pointer)
        wl_pointer_release(m_client.pointer);
    if (m_client.surface)
        wl_surface_destroy(m_client.surface);
    if (m_client.seat)
        wl_seat_release(m_client.seat);
    if (m_client.compositor)
        wl_compositor_destroy(m_client.compositor);
    if (m_client.registry)
        wl_registry_destroy(m_client.registry);
    wl_display_flush(m_client.display);
    wl_display_disconnect(m_client.display);
    m_client = { };

    wl_event_loop_dispatch(wl_display_get_event_loop(m_server->handle()), 0);
    m_serverClient = nullptr;
}

void ScrollFactorTest::cleanupTestCase()
{
    m_surfaceListener.disconnect();
    destroyClient();

    if (m_seat && m_inputDevice)
        m_seat->detachInputDevice(m_inputDevice.get());
    m_inputDevice.reset();
    m_seatsManager.reset();
    m_seat = nullptr;
    m_cursor = nullptr;
    m_server->stop();
    m_server.reset();
    wlr_pointer_finish(&m_nativePointer);
}

int main(int argc, char *argv[])
{
    WAYLIB_SERVER_NAMESPACE::WServer::initializeQPA();
    QGuiApplication app(argc, argv);
    ScrollFactorTest test;
    return QTest::qExec(&test, argc, argv);
}

#include "main.moc"
