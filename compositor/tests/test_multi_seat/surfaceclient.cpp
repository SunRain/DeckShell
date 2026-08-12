// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "surfaceclient.h"

#include <wserver.h>

#include <algorithm>
#include <cerrno>
#include <cstring>
#include <sys/socket.h>
#include <unistd.h>

extern "C" {
#include <wayland-client.h>
#include <wayland-server-core.h>
}

namespace {

const wl_registry_listener RegistryListener = {
    .global = SurfaceClient::registryGlobal,
    .global_remove = SurfaceClient::registryGlobalRemove,
};

void setError(QString *error, const QString &message)
{
    if (error)
        *error = message;
}

} // namespace

SurfaceClient::~SurfaceClient()
{
    disconnect();
}

bool SurfaceClient::connectTo(WAYLIB_SERVER_NAMESPACE::WServer *server,
                              wlr_compositor *compositor,
                              QString *error)
{
    m_server = server;
    m_surfaceListener.init(&compositor->events.new_surface, [this](wlr_surface *surface) {
        m_nativeSurfaces.append(surface);
    });

    int sockets[2] = { -1, -1 };
    if (::socketpair(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0, sockets) != 0) {
        setError(error, QString::fromLocal8Bit(std::strerror(errno)));
        return false;
    }

    m_serverClient = wl_client_create(server->handle(), sockets[0]);
    if (!m_serverClient) {
        ::close(sockets[0]);
        ::close(sockets[1]);
        setError(error, QStringLiteral("wl_client_create failed"));
        return false;
    }

    m_display = wl_display_connect_to_fd(sockets[1]);
    if (!m_display) {
        ::close(sockets[1]);
        setError(error, QStringLiteral("wl_display_connect_to_fd failed"));
        return false;
    }

    m_registry = wl_display_get_registry(m_display);
    wl_registry_add_listener(m_registry, &RegistryListener, this);
    if (!dispatchServer(error) || !dispatchClient(error))
        return false;

    if (!m_compositorName || m_seatGlobals.size() < 2) {
        setError(error, QStringLiteral("required compositor or seat globals are missing"));
        return false;
    }

    m_compositor =
        static_cast<wl_compositor *>(wl_registry_bind(m_registry,
                                                      m_compositorName,
                                                      &wl_compositor_interface,
                                                      std::min(m_compositorVersion, 6U)));
    for (const auto &[name, version] : std::as_const(m_seatGlobals)) {
        m_seats.append(static_cast<wl_seat *>(
            wl_registry_bind(m_registry, name, &wl_seat_interface, std::min(version, 9U))));
    }

    return dispatchServer(error) && dispatchClient(error);
}

bool SurfaceClient::createSurfaces(int count, QString *error)
{
    for (int i = 0; i < count; ++i)
        m_surfaces.append(wl_compositor_create_surface(m_compositor));

    if (!dispatchServer(error))
        return false;
    if (m_nativeSurfaces.size() != count) {
        setError(error, QStringLiteral("unexpected native surface count"));
        return false;
    }
    return true;
}

const QVector<wlr_surface *> &SurfaceClient::nativeSurfaces() const
{
    return m_nativeSurfaces;
}

void SurfaceClient::disconnect()
{
    m_surfaceListener.disconnect();

    if (!m_display)
        return;

    for (auto *surface : std::as_const(m_surfaces))
        wl_surface_destroy(surface);
    for (auto *seat : std::as_const(m_seats))
        wl_seat_release(seat);
    if (m_compositor)
        wl_compositor_destroy(m_compositor);
    if (m_registry)
        wl_registry_destroy(m_registry);

    wl_display_flush(m_display);
    wl_display_disconnect(m_display);
    m_display = nullptr;
    m_registry = nullptr;
    m_compositor = nullptr;
    m_surfaces.clear();
    m_seats.clear();
    m_nativeSurfaces.clear();
    m_seatGlobals.clear();
    m_compositorName = 0;
    m_compositorVersion = 0;

    if (m_server) {
        wl_event_loop_dispatch(wl_display_get_event_loop(m_server->handle()), 0);
        m_serverClient = nullptr;
    }
}

void SurfaceClient::registryGlobal(void *data,
                                   wl_registry *,
                                   uint32_t name,
                                   const char *interface,
                                   uint32_t version)
{
    auto *client = static_cast<SurfaceClient *>(data);
    if (std::strcmp(interface, wl_compositor_interface.name) == 0) {
        client->m_compositorName = name;
        client->m_compositorVersion = version;
    } else if (std::strcmp(interface, wl_seat_interface.name) == 0) {
        client->m_seatGlobals.append({ name, version });
    }
}

void SurfaceClient::registryGlobalRemove(void *, wl_registry *, uint32_t) { }

bool SurfaceClient::dispatchServer(QString *error)
{
    if (wl_display_flush(m_display) < 0) {
        setError(error, QStringLiteral("failed to flush Wayland client"));
        return false;
    }
    if (wl_event_loop_dispatch(wl_display_get_event_loop(m_server->handle()), 0) != 0) {
        setError(error, QStringLiteral("failed to dispatch Wayland server"));
        return false;
    }
    wl_display_flush_clients(m_server->handle());
    return true;
}

bool SurfaceClient::dispatchClient(QString *error)
{
    if (wl_display_dispatch(m_display) >= 0)
        return true;

    setError(error, QStringLiteral("failed to dispatch Wayland client"));
    return false;
}
