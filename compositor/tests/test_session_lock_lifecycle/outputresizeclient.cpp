// Copyright (C) 2026 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "outputresizeclient.h"

#include <QElapsedTimer>

#include <algorithm>
#include <cerrno>
#include <cstring>
#include <poll.h>

const wl_registry_listener OutputResizeClient::RegistryListener = {
    .global = OutputResizeClient::registryGlobal,
    .global_remove = OutputResizeClient::registryGlobalRemove,
};

const zwlr_output_manager_v1_listener OutputResizeClient::ManagerListener = {
    .head = OutputResizeClient::managerHead,
    .done = OutputResizeClient::managerDone,
    .finished = OutputResizeClient::managerFinished,
};

const zwlr_output_head_v1_listener OutputResizeClient::HeadListener = {
    .name = OutputResizeClient::headName,
    .description = OutputResizeClient::headDescription,
    .physical_size = OutputResizeClient::headPhysicalSize,
    .mode = OutputResizeClient::headMode,
    .enabled = OutputResizeClient::headEnabled,
    .current_mode = OutputResizeClient::headCurrentMode,
    .position = OutputResizeClient::headPosition,
    .transform = OutputResizeClient::headTransform,
    .scale = OutputResizeClient::headScale,
    .finished = OutputResizeClient::headFinished,
};

const zwlr_output_configuration_v1_listener OutputResizeClient::ConfigurationListener = {
    .succeeded = OutputResizeClient::configurationSucceeded,
    .failed = OutputResizeClient::configurationFailed,
    .cancelled = OutputResizeClient::configurationCancelled,
};

OutputResizeClient::~OutputResizeClient()
{
    disconnect();
}

bool OutputResizeClient::connectTo(const QString &runtimeDir, QString *error)
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
    if (!m_manager)
        return fail(error, QStringLiteral("zwlr_output_manager_v1 is absent"));
    return waitFor(
        [this] {
            return !m_heads.empty() && m_configurationSerial != 0;
        },
        error);
}

bool OutputResizeClient::resizeFirstOutput(int width, int height, QString *error)
{
    if (!m_manager || width <= 0 || height <= 0)
        return fail(error, QStringLiteral("invalid output resize request"));

    auto *target = m_heads.front().get();
    auto *configuration =
        zwlr_output_manager_v1_create_configuration(m_manager, m_configurationSerial);
    if (!configuration)
        return fail(error, QStringLiteral("output configuration creation failed"));

    m_configurationState = { };
    zwlr_output_configuration_v1_add_listener(configuration,
                                              &ConfigurationListener,
                                              &m_configurationState);

    for (const auto &head : m_heads) {
        auto *headConfiguration =
            zwlr_output_configuration_v1_enable_head(configuration, head->head);
        if (!headConfiguration) {
            zwlr_output_configuration_v1_destroy(configuration);
            return fail(error, QStringLiteral("output head configuration creation failed"));
        }
        if (head.get() == target) {
            zwlr_output_configuration_head_v1_set_custom_mode(headConfiguration, width, height, 0);
        } else if (head->currentMode) {
            zwlr_output_configuration_head_v1_set_mode(headConfiguration, head->currentMode);
        }
        zwlr_output_configuration_head_v1_set_position(headConfiguration, 0, 0);
        zwlr_output_configuration_head_v1_destroy(headConfiguration);
    }

    zwlr_output_configuration_v1_apply(configuration);
    if (wl_display_flush(m_display) < 0 && errno != EAGAIN)
        return fail(error, QStringLiteral("output configuration flush failed"));

    if (!waitFor(
            [this] {
                return m_configurationState.succeeded || m_configurationState.failed
                    || m_configurationState.cancelled;
            },
            error)) {
        return false;
    }

    if (!m_configurationState.succeeded)
        return fail(error, QStringLiteral("output configuration was rejected"));
    zwlr_output_configuration_v1_destroy(configuration);
    return true;
}

void OutputResizeClient::registryGlobal(void *data,
                                        wl_registry *registry,
                                        uint32_t name,
                                        const char *interface,
                                        uint32_t version)
{
    auto *client = static_cast<OutputResizeClient *>(data);
    if (std::strcmp(interface, zwlr_output_manager_v1_interface.name) != 0)
        return;

    const uint32_t bindVersion = std::min(version, 1U);
    client->m_manager = static_cast<zwlr_output_manager_v1 *>(
        wl_registry_bind(registry, name, &zwlr_output_manager_v1_interface, bindVersion));
    zwlr_output_manager_v1_add_listener(client->m_manager, &ManagerListener, client);
}

void OutputResizeClient::registryGlobalRemove(void *, wl_registry *, uint32_t) { }

void OutputResizeClient::managerHead(void *data,
                                     zwlr_output_manager_v1 *,
                                     zwlr_output_head_v1 *head)
{
    auto *client = static_cast<OutputResizeClient *>(data);
    auto state = std::make_unique<HeadState>();
    state->head = head;
    auto *statePtr = state.get();
    client->m_heads.push_back(std::move(state));
    zwlr_output_head_v1_add_listener(head, &HeadListener, statePtr);
}

void OutputResizeClient::managerDone(void *data, zwlr_output_manager_v1 *, uint32_t serial)
{
    auto *client = static_cast<OutputResizeClient *>(data);
    client->m_configurationSerial = serial;
}

void OutputResizeClient::managerFinished(void *, zwlr_output_manager_v1 *) { }

void OutputResizeClient::headName(void *data, zwlr_output_head_v1 *head, const char *name)
{
    Q_UNUSED(head);
    static_cast<HeadState *>(data)->name = QString::fromUtf8(name);
}

void OutputResizeClient::headDescription(void *, zwlr_output_head_v1 *, const char *) { }

void OutputResizeClient::headPhysicalSize(void *, zwlr_output_head_v1 *, int32_t, int32_t) { }

void OutputResizeClient::headMode(void *, zwlr_output_head_v1 *, zwlr_output_mode_v1 *) { }

void OutputResizeClient::headCurrentMode(void *data,
                                         zwlr_output_head_v1 *head,
                                         zwlr_output_mode_v1 *mode)
{
    Q_UNUSED(head);
    static_cast<HeadState *>(data)->currentMode = mode;
}

void OutputResizeClient::headEnabled(void *data, zwlr_output_head_v1 *head, int32_t enabled)
{
    Q_UNUSED(head);
    static_cast<HeadState *>(data)->enabled = enabled != 0;
}

void OutputResizeClient::headPosition(void *, zwlr_output_head_v1 *, int32_t, int32_t) { }

void OutputResizeClient::headTransform(void *, zwlr_output_head_v1 *, int32_t) { }

void OutputResizeClient::headScale(void *, zwlr_output_head_v1 *, wl_fixed_t) { }

void OutputResizeClient::headFinished(void *data, zwlr_output_head_v1 *head)
{
    Q_UNUSED(head);
    static_cast<HeadState *>(data)->enabled = false;
}

void OutputResizeClient::configurationSucceeded(void *data, zwlr_output_configuration_v1 *)
{
    static_cast<ConfigurationState *>(data)->succeeded = true;
}

void OutputResizeClient::configurationFailed(void *data, zwlr_output_configuration_v1 *)
{
    static_cast<ConfigurationState *>(data)->failed = true;
}

void OutputResizeClient::configurationCancelled(void *data, zwlr_output_configuration_v1 *)
{
    static_cast<ConfigurationState *>(data)->cancelled = true;
}

bool OutputResizeClient::waitFor(const std::function<bool()> &condition, QString *error)
{
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
    return condition() || fail(error, QStringLiteral("timed out waiting for output configuration"));
}

OutputResizeClient::HeadState *OutputResizeClient::findHead(zwlr_output_head_v1 *head) const
{
    const auto it = std::find_if(m_heads.cbegin(), m_heads.cend(), [head](const auto &state) {
        return state->head == head;
    });
    return it == m_heads.cend() ? nullptr : it->get();
}

void OutputResizeClient::disconnect()
{
    if (m_display)
        wl_display_disconnect(m_display);
    m_display = nullptr;
    m_registry = nullptr;
    m_manager = nullptr;
    m_heads.clear();
    m_configurationSerial = 0;
}

bool OutputResizeClient::fail(QString *error, const QString &message) const
{
    if (error)
        *error = message;
    return false;
}
