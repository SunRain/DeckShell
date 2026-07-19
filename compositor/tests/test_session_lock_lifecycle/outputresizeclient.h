// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include "wlr-output-management-unstable-v1-client-protocol.h"

#include <QString>

#include <functional>
#include <memory>
#include <vector>

class OutputResizeClient
{
public:
    ~OutputResizeClient();

    bool connectTo(const QString &runtimeDir, QString *error);
    bool resizeFirstOutput(int width, int height, QString *error);

private:
    struct HeadState
    {
        zwlr_output_head_v1 *head = nullptr;
        zwlr_output_mode_v1 *currentMode = nullptr;
        QString name;
        bool enabled = true;
    };

    struct ConfigurationState
    {
        bool succeeded = false;
        bool failed = false;
        bool cancelled = false;
    };

    static const wl_registry_listener RegistryListener;
    static const zwlr_output_manager_v1_listener ManagerListener;
    static const zwlr_output_head_v1_listener HeadListener;
    static const zwlr_output_configuration_v1_listener ConfigurationListener;

    static void registryGlobal(void *data,
                               wl_registry *registry,
                               uint32_t name,
                               const char *interface,
                               uint32_t version);
    static void registryGlobalRemove(void *data, wl_registry *registry, uint32_t name);
    static void managerHead(void *data, zwlr_output_manager_v1 *manager, zwlr_output_head_v1 *head);
    static void managerDone(void *data, zwlr_output_manager_v1 *manager, uint32_t serial);
    static void managerFinished(void *data, zwlr_output_manager_v1 *manager);
    static void headName(void *data, zwlr_output_head_v1 *head, const char *name);
    static void headDescription(void *data, zwlr_output_head_v1 *head, const char *description);
    static void headPhysicalSize(void *data,
                                 zwlr_output_head_v1 *head,
                                 int32_t width,
                                 int32_t height);
    static void headMode(void *data, zwlr_output_head_v1 *head, zwlr_output_mode_v1 *mode);
    static void headCurrentMode(void *data, zwlr_output_head_v1 *head, zwlr_output_mode_v1 *mode);
    static void headEnabled(void *data, zwlr_output_head_v1 *head, int32_t enabled);
    static void headPosition(void *data, zwlr_output_head_v1 *head, int32_t x, int32_t y);
    static void headTransform(void *data, zwlr_output_head_v1 *head, int32_t transform);
    static void headScale(void *data, zwlr_output_head_v1 *head, wl_fixed_t scale);
    static void headFinished(void *data, zwlr_output_head_v1 *head);
    static void configurationSucceeded(void *data, zwlr_output_configuration_v1 *configuration);
    static void configurationFailed(void *data, zwlr_output_configuration_v1 *configuration);
    static void configurationCancelled(void *data, zwlr_output_configuration_v1 *configuration);

    bool waitFor(const std::function<bool()> &condition, QString *error);
    HeadState *findHead(zwlr_output_head_v1 *head) const;
    bool fail(QString *error, const QString &message) const;
    void disconnect();

    wl_display *m_display = nullptr;
    wl_registry *m_registry = nullptr;
    zwlr_output_manager_v1 *m_manager = nullptr;
    uint32_t m_configurationSerial = 0;
    std::vector<std::unique_ptr<HeadState>> m_heads;
    ConfigurationState m_configurationState;
};
