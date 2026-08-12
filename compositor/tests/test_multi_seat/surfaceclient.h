// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <wglobal.h>

#include <wscoplistener.h>
#include <QVector>

#include <cstdint>

struct wl_compositor;
struct wl_display;
struct wl_client;
struct wl_registry;
struct wl_seat;
struct wl_surface;
struct wlr_surface;

struct wlr_compositor;

WAYLIB_SERVER_BEGIN_NAMESPACE
class WServer;
WAYLIB_SERVER_END_NAMESPACE

class SurfaceClient
{
public:
    SurfaceClient() = default;
    ~SurfaceClient();

    bool connectTo(WAYLIB_SERVER_NAMESPACE::WServer *server,
                   wlr_compositor *compositor,
                   QString *error);
    bool createSurfaces(int count, QString *error);
    const QVector<wlr_surface *> &nativeSurfaces() const;
    void disconnect();

    static void registryGlobal(void *data,
                               wl_registry *registry,
                               uint32_t name,
                               const char *interface,
                               uint32_t version);
    static void registryGlobalRemove(void *data, wl_registry *registry, uint32_t name);

private:
    bool dispatchServer(QString *error);
    bool dispatchClient(QString *error);

    WAYLIB_SERVER_NAMESPACE::WServer *m_server = nullptr;
    wl_display *m_display = nullptr;
    wl_client *m_serverClient = nullptr;
    wl_registry *m_registry = nullptr;
    wl_compositor *m_compositor = nullptr;
    QVector<wl_seat *> m_seats;
    QVector<wl_surface *> m_surfaces;
    QVector<wlr_surface *> m_nativeSurfaces;
    QVector<QPair<uint32_t, uint32_t>> m_seatGlobals;
    uint32_t m_compositorName = 0;
    uint32_t m_compositorVersion = 0;
    WAYLIB_SERVER_NAMESPACE::WScopedListener m_surfaceListener;
};
