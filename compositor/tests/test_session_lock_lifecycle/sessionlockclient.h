// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include "ext-session-lock-v1-client-protocol.h"

#include <QString>
#include <QTemporaryFile>

#include <functional>
#include <memory>
#include <vector>

class SessionLockClient
{
public:
    ~SessionLockClient();

    bool connectTo(const QString &runtimeDir, QString *error);
    bool lock(QString *error);
    bool requestLock(QString *error);
    bool createAndCommitLockSurfaces(QString *error);
    bool unlock(QString *error);
    void disconnectAbruptly();
    bool waitForReconfigure(QString *error);

    bool isLocked() const;
    bool isFinished() const;
    int outputCount() const;
    int renderedLockSurfaceCount() const;

private:
    struct RegistryState
    {
        uint32_t managerName = 0;
        uint32_t managerVersion = 0;
    };

    struct LockState
    {
        bool locked = false;
        bool finished = false;
    };

    struct LockSurface
    {
        wl_surface *surface = nullptr;
        ext_session_lock_surface_v1 *lockSurface = nullptr;
        uint32_t configureSerial = 0;
        int width = 0;
        int height = 0;
        int configureCount = 0;
        bool configured = false;
        wl_buffer *buffer = nullptr;
        std::unique_ptr<QTemporaryFile> bufferFile;
    };

    static const wl_registry_listener RegistryListener;
    static const ext_session_lock_v1_listener SessionLockListener;
    static const ext_session_lock_surface_v1_listener LockSurfaceListener;

    static void registryGlobal(void *data,
                               wl_registry *registry,
                               uint32_t name,
                               const char *interface,
                               uint32_t version);
    static void registryGlobalRemove(void *data, wl_registry *registry, uint32_t name);
    static void sessionLocked(void *data, ext_session_lock_v1 *lock);
    static void sessionFinished(void *data, ext_session_lock_v1 *lock);
    static void lockSurfaceConfigure(void *data,
                                     ext_session_lock_surface_v1 *lockSurface,
                                     uint32_t serial,
                                     uint32_t width,
                                     uint32_t height);

    bool waitFor(const std::function<bool()> &condition, QString *error);
    bool createLockSurface(wl_output *output, QString *error);
    bool commitLockSurface(LockSurface &surface, QString *error);
    void disconnect();
    bool fail(QString *error, const QString &message) const;

    wl_display *m_display = nullptr;
    wl_registry *m_registry = nullptr;
    wl_compositor *m_compositor = nullptr;
    wl_shm *m_shm = nullptr;
    ext_session_lock_manager_v1 *m_manager = nullptr;
    ext_session_lock_v1 *m_lock = nullptr;
    RegistryState m_registryState;
    LockState m_lockState;
    std::vector<wl_output *> m_outputs;
    std::vector<LockSurface> m_lockSurfaces;
};
