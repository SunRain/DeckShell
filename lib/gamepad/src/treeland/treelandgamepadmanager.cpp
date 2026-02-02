// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "treelandgamepadmanager.h"
#include "treelandgamepadclient.h"
#include "treelandgamepaddevice.h"

#include <QDebug>
#include <wayland-client.h>
#include "treeland-gamepad-v1-client-protocol.h"

namespace TreelandGamepad {

struct TreelandGamepadManager::Private
{
    TreelandGamepadClient *client = nullptr;
    treeland_gamepad_manager_v1 *manager = nullptr;
    uint32_t name = 0;
    uint32_t version = 0;
    
    // Map device ID to Wayland gamepad object
    QHash<int, treeland_gamepad_v1*> gamepads;
    
    // Manager listener
    static const struct treeland_gamepad_manager_v1_listener managerListener;
    
    // Gamepad listener
    static const struct treeland_gamepad_v1_listener gamepadListener;
};

const struct treeland_gamepad_manager_v1_listener TreelandGamepadManager::Private::managerListener = {
    .gamepad_added = &TreelandGamepadManager::handleGamepadAdded,
    .gamepad_removed = &TreelandGamepadManager::handleGamepadRemoved,
    .authorized = &TreelandGamepadManager::handleAuthorized,
    .authorization_failed = &TreelandGamepadManager::handleAuthorizationFailed,
};

const struct treeland_gamepad_v1_listener TreelandGamepadManager::Private::gamepadListener = {
    .button = &TreelandGamepadManager::handleButton,
    .axis = &TreelandGamepadManager::handleAxis,
    .hat = &TreelandGamepadManager::handleHat,
    .device_info = &TreelandGamepadManager::handleDeviceInfo,
    .axis_deadzone_applied = &TreelandGamepadManager::handleAxisDeadzoneApplied,
    .axis_deadzone_failed = &TreelandGamepadManager::handleAxisDeadzoneFailed,
};

TreelandGamepadManager::TreelandGamepadManager(TreelandGamepadClient *client)
    : QObject(client)
    , d(std::make_unique<Private>())
{
    d->client = client;
}

TreelandGamepadManager::~TreelandGamepadManager()
{
    unbind();
}

bool TreelandGamepadManager::bind(wl_registry *registry, uint32_t name, uint32_t version)
{
    if (d->manager) {
        qWarning() << "Manager already bound";
        return false;
    }
    
    d->name = name;
    d->version = qMin(version, 2u);
    d->manager = static_cast<treeland_gamepad_manager_v1*>(
        wl_registry_bind(registry, name, &treeland_gamepad_manager_v1_interface, d->version)
    );
    
    if (!d->manager) {
        qWarning() << "Failed to bind treeland_gamepad_manager_v1";
        return false;
    }
    
    treeland_gamepad_manager_v1_add_listener(d->manager, &Private::managerListener, this);
    
    return true;
}

uint32_t TreelandGamepadManager::protocolVersion() const
{
    return d->version;
}

bool TreelandGamepadManager::authorize(const QString &token)
{
    if (!d->manager) {
        return false;
    }

    if (d->version < 2 || wl_proxy_get_version(reinterpret_cast<wl_proxy *>(d->manager)) < 2) {
        return false;
    }

    const QByteArray tokenBytes = token.toUtf8();
    treeland_gamepad_manager_v1_authorize(d->manager, tokenBytes.constData());
    return true;
}

void TreelandGamepadManager::unbind()
{
    // Destroy all gamepad objects
    for (auto it = d->gamepads.begin(); it != d->gamepads.end(); ++it) {
        treeland_gamepad_v1_release(it.value());
    }
    d->gamepads.clear();
    
    // Destroy manager
    if (d->manager) {
        treeland_gamepad_manager_v1_destroy(d->manager);
        d->manager = nullptr;
    }
    
    d->name = 0;
    d->version = 0;
}

bool TreelandGamepadManager::isBound() const
{
    return d->manager != nullptr;
}

TreelandGamepadDevice* TreelandGamepadManager::createGamepad(int deviceId)
{
    if (!d->manager) {
        qWarning() << "Manager not bound";
        return nullptr;
    }
    
    if (d->gamepads.contains(deviceId)) {
        qWarning() << "Gamepad already exists for device" << deviceId;
        return nullptr;
    }
    
    // Get the device from client
    TreelandGamepadDevice *device = d->client->gamepad(deviceId);
    if (!device) {
        qWarning() << "Device not found" << deviceId;
        return nullptr;
    }
    
    // Create Wayland gamepad object
    treeland_gamepad_v1 *gamepad = treeland_gamepad_manager_v1_get_gamepad(d->manager, deviceId);
    if (!gamepad) {
        qWarning() << "Failed to create gamepad for device" << deviceId;
        return nullptr;
    }
    
    // Set up listener with device as user data
    treeland_gamepad_v1_add_listener(gamepad, &Private::gamepadListener, device);
    
    // Store gamepad object
    d->gamepads[deviceId] = gamepad;
    
    // Store in device private data
    device->setGamepadHandle(gamepad);
    
    return device;
}

void TreelandGamepadManager::destroyGamepad(int deviceId)
{
    auto it = d->gamepads.find(deviceId);
    if (it == d->gamepads.end()) {
        return;
    }
    
    // Get the device from client
    if (TreelandGamepadDevice *device = d->client->gamepad(deviceId)) {
        device->setGamepadHandle(nullptr);
    }
    
    // Release the Wayland object
    treeland_gamepad_v1_release(it.value());
    d->gamepads.erase(it);
}

void TreelandGamepadManager::handleGamepadAdded(void *data,
                                                treeland_gamepad_manager_v1 *manager,
                                                int32_t device_id,
                                                const char *name)
{
    Q_UNUSED(manager)
    
    auto *self = static_cast<TreelandGamepadManager*>(data);
    Q_EMIT self->gamepadAdded(device_id, QString::fromUtf8(name));
}

void TreelandGamepadManager::handleAuthorized(void *data,
                                              treeland_gamepad_manager_v1 *manager,
                                              uint32_t capabilities)
{
    Q_UNUSED(manager)

    auto *self = static_cast<TreelandGamepadManager*>(data);
    Q_EMIT self->authorized(capabilities);
}

void TreelandGamepadManager::handleAuthorizationFailed(void *data,
                                                       treeland_gamepad_manager_v1 *manager,
                                                       uint32_t error)
{
    Q_UNUSED(manager)

    auto *self = static_cast<TreelandGamepadManager*>(data);
    Q_EMIT self->authorizationFailed(error);
}

void TreelandGamepadManager::handleGamepadRemoved(void *data,
                                                 treeland_gamepad_manager_v1 *manager,
                                                 int32_t device_id)
{
    Q_UNUSED(manager)
    
    auto *self = static_cast<TreelandGamepadManager*>(data);
    Q_EMIT self->gamepadRemoved(device_id);
}

void TreelandGamepadManager::handleButton(void *data,
                                         treeland_gamepad_v1 *gamepad,
                                         uint32_t time,
                                         uint32_t button,
                                         uint32_t state)
{
    Q_UNUSED(gamepad)
    
    auto *device = static_cast<TreelandGamepadDevice*>(data);
    device->handleButton(time, button, state);
}

void TreelandGamepadManager::handleAxis(void *data,
                                       treeland_gamepad_v1 *gamepad,
                                       uint32_t time,
                                       uint32_t axis,
                                       wl_fixed_t value)
{
    Q_UNUSED(gamepad)
    
    auto *device = static_cast<TreelandGamepadDevice*>(data);
    double doubleValue = wl_fixed_to_double(value);
    device->handleAxis(time, axis, doubleValue);
}

void TreelandGamepadManager::handleHat(void *data,
                                      treeland_gamepad_v1 *gamepad,
                                      uint32_t time,
                                      uint32_t hat,
                                      int32_t value)
{
    Q_UNUSED(gamepad)
    
    auto *device = static_cast<TreelandGamepadDevice*>(data);
    device->handleHat(time, hat, value);
}

void TreelandGamepadManager::handleDeviceInfo(void *data,
                                              treeland_gamepad_v1 *gamepad,
                                              const char *guid)
{
    Q_UNUSED(gamepad)

    auto *device = static_cast<TreelandGamepadDevice*>(data);
    device->setGuid(QString::fromUtf8(guid));
}

void TreelandGamepadManager::handleAxisDeadzoneApplied(void *data,
                                                       treeland_gamepad_v1 *gamepad,
                                                       uint32_t axis,
                                                       wl_fixed_t deadzone)
{
    Q_UNUSED(gamepad)

    auto *device = static_cast<TreelandGamepadDevice*>(data);
    device->handleAxisDeadzoneApplied(axis, wl_fixed_to_double(deadzone));
}

void TreelandGamepadManager::handleAxisDeadzoneFailed(void *data,
                                                      treeland_gamepad_v1 *gamepad,
                                                      uint32_t axis,
                                                      uint32_t error)
{
    Q_UNUSED(gamepad)

    auto *device = static_cast<TreelandGamepadDevice*>(data);
    device->handleAxisDeadzoneFailed(axis, error);
}

} // namespace TreelandGamepad
