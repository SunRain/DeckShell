// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include "treelandgamepadglobal.h"
#include <QObject>
#include <memory>
#include <cstdint>

struct wl_registry;
struct treeland_gamepad_manager_v1;
struct treeland_gamepad_v1;

// Forward declare wl_fixed_t from wayland-util.h
typedef int32_t wl_fixed_t;

namespace TreelandGamepad {

class TreelandGamepadClient;
class TreelandGamepadDevice;

class TreelandGamepadManager : public QObject
{
    Q_OBJECT

public:
    explicit TreelandGamepadManager(TreelandGamepadClient *client);
    ~TreelandGamepadManager();

    bool bind(wl_registry *registry, uint32_t name, uint32_t version);
    void unbind();
    bool isBound() const;
    uint32_t protocolVersion() const;

    bool authorize(const QString &token);

    TreelandGamepadDevice* createGamepad(int deviceId);
    void destroyGamepad(int deviceId);

Q_SIGNALS:
    void gamepadAdded(int deviceId, const QString &name);
    void gamepadRemoved(int deviceId);
    void authorized(uint32_t capabilities);
    void authorizationFailed(uint32_t error);

private:
    // Wayland callbacks
    static void handleAuthorized(void *data,
                                 struct treeland_gamepad_manager_v1 *manager,
                                 uint32_t capabilities);
    static void handleAuthorizationFailed(void *data,
                                          struct treeland_gamepad_manager_v1 *manager,
                                          uint32_t error);
    static void handleGamepadAdded(void *data,
                                  struct treeland_gamepad_manager_v1 *manager,
                                  int32_t device_id,
                                  const char *name);
    static void handleGamepadRemoved(void *data,
                                    struct treeland_gamepad_manager_v1 *manager,
                                    int32_t device_id);

    // Gamepad callbacks
    static void handleButton(void *data,
                            struct treeland_gamepad_v1 *gamepad,
                            uint32_t time,
                            uint32_t button,
                            uint32_t state);
    static void handleAxis(void *data,
                         struct treeland_gamepad_v1 *gamepad,
                         uint32_t time,
                         uint32_t axis,
                         wl_fixed_t value);
    static void handleHat(void *data,
                        struct treeland_gamepad_v1 *gamepad,
                        uint32_t time,
                        uint32_t hat,
                        int32_t value);

    static void handleDeviceInfo(void *data,
                                 struct treeland_gamepad_v1 *gamepad,
                                 const char *guid);
    static void handleAxisDeadzoneApplied(void *data,
                                          struct treeland_gamepad_v1 *gamepad,
                                          uint32_t axis,
                                          wl_fixed_t deadzone);
    static void handleAxisDeadzoneFailed(void *data,
                                         struct treeland_gamepad_v1 *gamepad,
                                         uint32_t axis,
                                         uint32_t error);

    struct Private;
    std::unique_ptr<Private> d;
};

} // namespace TreelandGamepad
