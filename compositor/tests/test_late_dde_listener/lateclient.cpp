// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "lateclient.h"

#include "treeland-dde-shell-v1-client-protocol.h"
#include "xdg-shell-client-protocol.h"

#include <wayland-client.h>

#include <algorithm>
#include <array>
#include <cerrno>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <string>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

namespace {

struct ClientSurface
{
    wl_surface *surface = nullptr;
    xdg_surface *xdgSurface = nullptr;
    xdg_toplevel *toplevel = nullptr;
    treeland_dde_shell_surface_v1 *ddeSurface = nullptr;
};

class LateDdeClient
{
public:
    ~LateDdeClient();

    bool connectTo(const char *socketPath);
    bool createSurfaces();
    bool createDdeSurface(std::size_t index);
    bool destroyXdgSurface(std::size_t index);
    int runCommandLoop();

    static void registryGlobal(void *data,
                               wl_registry *registry,
                               uint32_t name,
                               const char *interface,
                               uint32_t version);
    static void registryGlobalRemove(void *, wl_registry *, uint32_t);
    static void xdgSurfaceConfigure(void *, xdg_surface *surface, uint32_t serial);
    static void xdgWmBasePing(void *, xdg_wm_base *wmBase, uint32_t serial);

private:
    bool roundtrip() const;
    bool handleCommand(const std::string &command);
    void cleanup();

    wl_display *m_display = nullptr;
    wl_registry *m_registry = nullptr;
    wl_compositor *m_compositor = nullptr;
    xdg_wm_base *m_wmBase = nullptr;
    treeland_dde_shell_manager_v1 *m_ddeManager = nullptr;
    std::array<ClientSurface, 3> m_surfaces;
};

constexpr wl_registry_listener RegistryListener = {
    .global = LateDdeClient::registryGlobal,
    .global_remove = LateDdeClient::registryGlobalRemove,
};

constexpr xdg_surface_listener XdgSurfaceListener = {
    .configure = LateDdeClient::xdgSurfaceConfigure,
};

constexpr xdg_wm_base_listener XdgWmBaseListener = {
    .ping = LateDdeClient::xdgWmBasePing,
};

int connectUnixSocket(const char *socketPath)
{
    if (!socketPath || std::strlen(socketPath) >= sizeof(sockaddr_un::sun_path))
        return -1;

    const int fd = ::socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (fd < 0)
        return -1;

    sockaddr_un address{ .sun_family = AF_UNIX };
    std::strcpy(address.sun_path, socketPath);
    if (::connect(fd, reinterpret_cast<const sockaddr *>(&address), sizeof(address)) == 0)
        return fd;

    ::close(fd);
    return -1;
}

LateDdeClient::~LateDdeClient()
{
    cleanup();
}

void LateDdeClient::registryGlobal(void *data,
                                   wl_registry *registry,
                                   uint32_t name,
                                   const char *interface,
                                   uint32_t version)
{
    auto *client = static_cast<LateDdeClient *>(data);
    if (std::strcmp(interface, wl_compositor_interface.name) == 0) {
        client->m_compositor = static_cast<wl_compositor *>(
            wl_registry_bind(registry, name, &wl_compositor_interface, std::min(version, 6U)));
    } else if (std::strcmp(interface, xdg_wm_base_interface.name) == 0) {
        client->m_wmBase = static_cast<xdg_wm_base *>(
            wl_registry_bind(registry, name, &xdg_wm_base_interface, std::min(version, 5U)));
        xdg_wm_base_add_listener(client->m_wmBase, &XdgWmBaseListener, client);
    } else if (std::strcmp(interface, treeland_dde_shell_manager_v1_interface.name) == 0) {
        client->m_ddeManager = static_cast<treeland_dde_shell_manager_v1 *>(
            wl_registry_bind(registry,
                             name,
                             &treeland_dde_shell_manager_v1_interface,
                             std::min(version, 2U)));
    }
}

void LateDdeClient::registryGlobalRemove(void *, wl_registry *, uint32_t) { }

void LateDdeClient::xdgSurfaceConfigure(void *, xdg_surface *surface, uint32_t serial)
{
    xdg_surface_ack_configure(surface, serial);
}

void LateDdeClient::xdgWmBasePing(void *, xdg_wm_base *wmBase, uint32_t serial)
{
    xdg_wm_base_pong(wmBase, serial);
}

bool LateDdeClient::roundtrip() const
{
    return m_display && wl_display_roundtrip(m_display) >= 0;
}

bool LateDdeClient::connectTo(const char *socketPath)
{
    std::fprintf(stderr, "connect: %s\n", socketPath ? socketPath : "<null>");
    const int fd = connectUnixSocket(socketPath);
    if (fd < 0) {
        std::fprintf(stderr, "failed to connect to %s: %s\n", socketPath, std::strerror(errno));
        return false;
    }
    std::fprintf(stderr, "connect: fd=%d\n", fd);

    m_display = wl_display_connect_to_fd(fd);
    if (!m_display) {
        std::fprintf(stderr, "wl_display_connect_to_fd failed: %s\n", std::strerror(errno));
        ::close(fd);
        return false;
    }
    std::fprintf(stderr, "display connected\n");

    m_registry = wl_display_get_registry(m_display);
    wl_registry_add_listener(m_registry, &RegistryListener, this);
    if (!roundtrip()) {
        std::fprintf(stderr, "registry roundtrip failed: %s\n", std::strerror(errno));
        return false;
    }
    std::fprintf(stderr,
                 "registry: compositor=%p xdg_wm_base=%p dde_manager=%p\n",
                 static_cast<void *>(m_compositor),
                 static_cast<void *>(m_wmBase),
                 static_cast<void *>(m_ddeManager));
    if (!m_compositor || !m_wmBase || !m_ddeManager) {
        std::fprintf(stderr, "required globals are missing\n");
        return false;
    }
    return true;
}

bool LateDdeClient::createSurfaces()
{
    for (std::size_t index = 0; index < m_surfaces.size(); ++index) {
        auto &entry = m_surfaces[index];
        entry.surface = wl_compositor_create_surface(m_compositor);
        if (!entry.surface) {
            std::fprintf(stderr, "surface %zu: wl_compositor_create_surface failed\n", index);
            return false;
        }
        entry.xdgSurface = xdg_wm_base_get_xdg_surface(m_wmBase, entry.surface);
        if (!entry.xdgSurface) {
            std::fprintf(stderr, "surface %zu: xdg_wm_base_get_xdg_surface failed\n", index);
            return false;
        }
        xdg_surface_add_listener(entry.xdgSurface, &XdgSurfaceListener, nullptr);
        entry.toplevel = xdg_surface_get_toplevel(entry.xdgSurface);
        if (!entry.toplevel) {
            std::fprintf(stderr, "surface %zu: xdg_surface_get_toplevel failed\n", index);
            return false;
        }

        const std::string appId = "org.deepin.test.late-dde-" + std::to_string(index);
        xdg_toplevel_set_app_id(entry.toplevel, appId.c_str());
        wl_surface_commit(entry.surface);
        std::fprintf(stderr, "surface %zu: committed app_id=%s\n", index, appId.c_str());
    }
    const bool result = roundtrip();
    std::fprintf(stderr, "surface roundtrip: %s\n", result ? "ok" : "failed");
    return result;
}

bool LateDdeClient::createDdeSurface(std::size_t index)
{
    if (index >= m_surfaces.size() || m_surfaces[index].ddeSurface)
        return false;

    auto &entry = m_surfaces[index];
    entry.ddeSurface = treeland_dde_shell_manager_v1_get_shell_surface(m_ddeManager, entry.surface);
    treeland_dde_shell_surface_v1_set_skip_switcher(entry.ddeSurface, 1);
    return roundtrip();
}

bool LateDdeClient::destroyXdgSurface(std::size_t index)
{
    if (index >= m_surfaces.size() || !m_surfaces[index].xdgSurface)
        return false;

    auto &entry = m_surfaces[index];
    xdg_toplevel_destroy(entry.toplevel);
    xdg_surface_destroy(entry.xdgSurface);
    entry.toplevel = nullptr;
    entry.xdgSurface = nullptr;
    return roundtrip();
}

bool LateDdeClient::handleCommand(const std::string &command)
{
    std::size_t index = 0;
    if (std::sscanf(command.c_str(), "dde %zu", &index) == 1)
        return createDdeSurface(index);
    if (std::sscanf(command.c_str(), "destroy-xdg %zu", &index) == 1)
        return destroyXdgSurface(index);
    return false;
}

int LateDdeClient::runCommandLoop()
{
    std::puts("ready");
    std::fflush(stdout);

    std::string command;
    while (std::getline(std::cin, command)) {
        if (command == "quit")
            return 0;
        if (!handleCommand(command)) {
            std::fprintf(stderr, "error %s\n", command.c_str());
            return 1;
        }
        std::printf("ok %s\n", command.c_str());
        std::fflush(stdout);
    }
    return 0;
}

void LateDdeClient::cleanup()
{
    if (!m_display)
        return;

    for (auto &entry : m_surfaces) {
        if (entry.ddeSurface)
            treeland_dde_shell_surface_v1_destroy(entry.ddeSurface);
        if (entry.toplevel)
            xdg_toplevel_destroy(entry.toplevel);
        if (entry.xdgSurface)
            xdg_surface_destroy(entry.xdgSurface);
        if (entry.surface)
            wl_surface_destroy(entry.surface);
    }
    if (m_ddeManager)
        treeland_dde_shell_manager_v1_destroy(m_ddeManager);
    if (m_wmBase)
        xdg_wm_base_destroy(m_wmBase);
    if (m_compositor)
        wl_compositor_destroy(m_compositor);
    if (m_registry)
        wl_registry_destroy(m_registry);

    wl_display_flush(m_display);
    wl_display_disconnect(m_display);
    m_display = nullptr;
}

} // namespace

int runLateDdeClient(const char *socketPath)
{
    LateDdeClient client;
    if (!client.connectTo(socketPath) || !client.createSurfaces())
        return 1;
    return client.runCommandLoop();
}
