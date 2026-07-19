// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "sessionlockclient.h"

#include <QElapsedTimer>

#include <algorithm>
#include <cerrno>
#include <cstring>
#include <limits>
#include <poll.h>

const wl_registry_listener SessionLockClient::RegistryListener = {
    .global = SessionLockClient::registryGlobal,
    .global_remove = SessionLockClient::registryGlobalRemove,
};

const ext_session_lock_v1_listener SessionLockClient::SessionLockListener = {
    .locked = SessionLockClient::sessionLocked,
    .finished = SessionLockClient::sessionFinished,
};

const ext_session_lock_surface_v1_listener SessionLockClient::LockSurfaceListener = {
    .configure = SessionLockClient::lockSurfaceConfigure,
};

SessionLockClient::~SessionLockClient()
{
    disconnect();
}

bool SessionLockClient::connectTo(const QString &runtimeDir, QString *error)
{
    qputenv("XDG_RUNTIME_DIR", runtimeDir.toLocal8Bit());
    qputenv("WAYLAND_DISPLAY", "wayland-0");

    m_display = wl_display_connect(nullptr);
    if (!m_display)
        return fail(error, QStringLiteral("wl_display_connect failed"));

    m_registry = wl_display_get_registry(m_display);
    wl_registry_add_listener(m_registry, &RegistryListener, this);
    if (wl_display_roundtrip(m_display) < 0)
        return fail(error, QStringLiteral("registry roundtrip failed"));

    if (!m_registryState.managerName)
        return fail(error, QStringLiteral("ext_session_lock_manager_v1 is absent"));
    if (!m_compositor)
        return fail(error, QStringLiteral("wl_compositor is absent"));
    if (!m_shm)
        return fail(error, QStringLiteral("wl_shm is absent"));
    if (m_outputs.empty())
        return fail(error, QStringLiteral("no wl_output global is available"));

    const uint32_t version = std::min(m_registryState.managerVersion, 1U);
    m_manager = static_cast<ext_session_lock_manager_v1 *>(
        wl_registry_bind(m_registry,
                         m_registryState.managerName,
                         &ext_session_lock_manager_v1_interface,
                         version));
    return m_manager || fail(error, QStringLiteral("manager bind failed"));
}

bool SessionLockClient::requestLock(QString *error)
{
    if (!m_manager)
        return fail(error, QStringLiteral("lock requested before manager bind"));
    if (m_lock)
        return fail(error, QStringLiteral("lock requested more than once"));

    m_lock = ext_session_lock_manager_v1_lock(m_manager);
    if (!m_lock)
        return fail(error, QStringLiteral("lock request creation failed"));

    ext_session_lock_v1_add_listener(m_lock, &SessionLockListener, this);
    if (wl_display_flush(m_display) < 0 && errno != EAGAIN)
        return fail(error, QStringLiteral("lock request flush failed"));

    return waitFor(
        [this] {
            return m_lockState.locked || m_lockState.finished;
        },
        error);
}

bool SessionLockClient::lock(QString *error)
{
    if (!requestLock(error))
        return false;
    if (m_lockState.finished)
        return fail(error, QStringLiteral("compositor denied session lock"));
    return true;
}

bool SessionLockClient::createAndCommitLockSurfaces(QString *error)
{
    if (!m_lockState.locked)
        return fail(error, QStringLiteral("lock surface requested before locked event"));
    if (!m_lockSurfaces.empty())
        return fail(error, QStringLiteral("lock surfaces were already created"));

    m_lockSurfaces.reserve(m_outputs.size());
    for (auto *output : m_outputs) {
        if (!createLockSurface(output, error))
            return false;
    }

    if (wl_display_flush(m_display) < 0 && errno != EAGAIN)
        return fail(error, QStringLiteral("lock surface request flush failed"));

    for (const auto &surface : m_lockSurfaces) {
        if (!waitFor(
                [&surface] {
                    return surface.configured;
                },
                error))
            return false;
    }

    for (auto &surface : m_lockSurfaces) {
        if (!commitLockSurface(surface, error))
            return false;
    }

    if (wl_display_roundtrip(m_display) < 0)
        return fail(error, QStringLiteral("lock surface commit roundtrip failed"));
    return true;
}

bool SessionLockClient::unlock(QString *error)
{
    if (!m_lockState.locked || !m_lock)
        return fail(error, QStringLiteral("unlock requested before locked event"));

    ext_session_lock_v1_unlock_and_destroy(m_lock);
    m_lock = nullptr;

    for (auto &surface : m_lockSurfaces) {
        if (surface.lockSurface)
            ext_session_lock_surface_v1_destroy(surface.lockSurface);
        if (surface.buffer)
            wl_buffer_destroy(surface.buffer);
        if (surface.surface)
            wl_surface_destroy(surface.surface);
    }
    m_lockSurfaces.clear();

    ext_session_lock_manager_v1_destroy(m_manager);
    m_manager = nullptr;

    if (wl_display_roundtrip(m_display) < 0)
        return fail(error, QStringLiteral("unlock roundtrip failed"));

    disconnect();
    return true;
}

void SessionLockClient::disconnectAbruptly()
{
    disconnect();
}

bool SessionLockClient::waitForReconfigure(QString *error)
{
    return waitFor(
        [this] {
            return std::any_of(m_lockSurfaces.cbegin(),
                               m_lockSurfaces.cend(),
                               [](const LockSurface &surface) {
                                   return surface.configureCount >= 2;
                               });
        },
        error);
}

bool SessionLockClient::isLocked() const
{
    return m_lockState.locked;
}

bool SessionLockClient::isFinished() const
{
    return m_lockState.finished;
}

int SessionLockClient::outputCount() const
{
    return static_cast<int>(m_outputs.size());
}

int SessionLockClient::renderedLockSurfaceCount() const
{
    return static_cast<int>(m_lockSurfaces.size());
}

void SessionLockClient::registryGlobal(void *data,
                                       wl_registry *registry,
                                       uint32_t name,
                                       const char *interface,
                                       uint32_t version)
{
    auto *client = static_cast<SessionLockClient *>(data);
    if (std::strcmp(interface, ext_session_lock_manager_v1_interface.name) == 0) {
        client->m_registryState.managerName = name;
        client->m_registryState.managerVersion = version;
        return;
    }

    if (std::strcmp(interface, wl_compositor_interface.name) == 0) {
        const uint32_t bindVersion = std::min(version, 4U);
        client->m_compositor = static_cast<wl_compositor *>(
            wl_registry_bind(registry, name, &wl_compositor_interface, bindVersion));
        return;
    }

    if (std::strcmp(interface, wl_shm_interface.name) == 0) {
        client->m_shm =
            static_cast<wl_shm *>(wl_registry_bind(registry, name, &wl_shm_interface, 1));
        return;
    }

    if (std::strcmp(interface, wl_output_interface.name) == 0) {
        const uint32_t bindVersion = std::min(version, 4U);
        auto *output = static_cast<wl_output *>(
            wl_registry_bind(registry, name, &wl_output_interface, bindVersion));
        client->m_outputs.push_back(output);
    }
}

void SessionLockClient::registryGlobalRemove(void *, wl_registry *, uint32_t) { }

void SessionLockClient::sessionLocked(void *data, ext_session_lock_v1 *)
{
    static_cast<SessionLockClient *>(data)->m_lockState.locked = true;
}

void SessionLockClient::sessionFinished(void *data, ext_session_lock_v1 *)
{
    static_cast<SessionLockClient *>(data)->m_lockState.finished = true;
}

void SessionLockClient::lockSurfaceConfigure(void *data,
                                             ext_session_lock_surface_v1 *,
                                             uint32_t serial,
                                             uint32_t width,
                                             uint32_t height)
{
    auto *surface = static_cast<LockSurface *>(data);
    surface->configureSerial = serial;
    surface->width = static_cast<int>(width);
    surface->height = static_cast<int>(height);
    ++surface->configureCount;
    surface->configured = true;
}

bool SessionLockClient::waitFor(const std::function<bool()> &condition, QString *error)
{
    if (!m_display)
        return fail(error, QStringLiteral("Wayland display is unavailable"));

    QElapsedTimer timer;
    timer.start();

    while (!condition() && timer.elapsed() < 5000) {
        if (wl_display_dispatch_pending(m_display) < 0)
            return fail(error, QStringLiteral("Wayland pending dispatch failed"));
        if (condition())
            break;

        if (wl_display_flush(m_display) < 0 && errno != EAGAIN)
            return fail(error, QStringLiteral("Wayland flush failed"));

        pollfd descriptor{ wl_display_get_fd(m_display), POLLIN, 0 };
        const int ready = ::poll(&descriptor, 1, 100);
        if (ready < 0 && errno == EINTR)
            continue;
        if (ready < 0)
            return fail(error, QStringLiteral("Wayland poll failed"));
        if (ready == 0)
            continue;
        if (descriptor.revents & (POLLERR | POLLHUP))
            return fail(error, QStringLiteral("Wayland connection closed"));
        if ((descriptor.revents & POLLIN) && wl_display_dispatch(m_display) < 0)
            return fail(error, QStringLiteral("Wayland dispatch failed"));
    }

    if (!condition())
        return fail(error, QStringLiteral("timed out waiting for Wayland response"));
    return true;
}

bool SessionLockClient::createLockSurface(wl_output *output, QString *error)
{
    auto *surface = wl_compositor_create_surface(m_compositor);
    if (!surface)
        return fail(error, QStringLiteral("wl_surface creation failed"));

    m_lockSurfaces.emplace_back();
    auto &lockSurface = m_lockSurfaces.back();
    lockSurface.surface = surface;
    lockSurface.lockSurface = ext_session_lock_v1_get_lock_surface(m_lock, surface, output);
    if (!lockSurface.lockSurface)
        return fail(error, QStringLiteral("ext-session-lock surface creation failed"));

    ext_session_lock_surface_v1_add_listener(lockSurface.lockSurface,
                                             &LockSurfaceListener,
                                             &lockSurface);
    return true;
}

bool SessionLockClient::commitLockSurface(LockSurface &surface, QString *error)
{
    if (surface.width <= 0 || surface.height <= 0)
        return fail(error, QStringLiteral("lock surface configure has invalid dimensions"));

    const qsizetype stride = static_cast<qsizetype>(surface.width) * 4;
    const qsizetype byteCount = stride * surface.height;
    if (byteCount <= 0 || byteCount > std::numeric_limits<int>::max())
        return fail(error, QStringLiteral("lock surface buffer dimensions are invalid"));

    surface.bufferFile = std::make_unique<QTemporaryFile>();
    if (!surface.bufferFile->open() || !surface.bufferFile->resize(byteCount))
        return fail(error, QStringLiteral("lock surface buffer file creation failed"));

    uchar *mapped = surface.bufferFile->map(0, byteCount);
    if (!mapped)
        return fail(error, QStringLiteral("lock surface buffer mapping failed"));
    std::fill_n(reinterpret_cast<uint32_t *>(mapped),
                static_cast<qsizetype>(surface.width) * surface.height,
                0xff202020U);
    surface.bufferFile->unmap(mapped);

    wl_shm_pool *pool =
        wl_shm_create_pool(m_shm, surface.bufferFile->handle(), static_cast<int>(byteCount));
    if (!pool)
        return fail(error, QStringLiteral("wl_shm pool creation failed"));

    surface.buffer = wl_shm_pool_create_buffer(pool,
                                               0,
                                               surface.width,
                                               surface.height,
                                               static_cast<int>(stride),
                                               WL_SHM_FORMAT_ARGB8888);
    wl_shm_pool_destroy(pool);
    if (!surface.buffer)
        return fail(error, QStringLiteral("wl_shm buffer creation failed"));

    ext_session_lock_surface_v1_ack_configure(surface.lockSurface, surface.configureSerial);
    wl_surface_attach(surface.surface, surface.buffer, 0, 0);
    wl_surface_damage_buffer(surface.surface, 0, 0, surface.width, surface.height);
    wl_surface_commit(surface.surface);
    return true;
}

void SessionLockClient::disconnect()
{
    if (m_display)
        wl_display_disconnect(m_display);

    m_display = nullptr;
    m_registry = nullptr;
    m_compositor = nullptr;
    m_shm = nullptr;
    m_manager = nullptr;
    m_lock = nullptr;
    m_outputs.clear();
    m_lockSurfaces.clear();
}

bool SessionLockClient::fail(QString *error, const QString &message) const
{
    if (error)
        *error = message;
    return false;
}
