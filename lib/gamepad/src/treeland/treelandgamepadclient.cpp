// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "treelandgamepadclient.h"

#include "treelandgamepaddevice.h"
#include "treelandgamepadmanager.h"

#include <wayland-client.h>

#include <QDebug>
#include <QPointer>
#include <QSocketNotifier>
#include <QTimer>

#include <cstring>

namespace TreelandGamepad {

struct TreelandGamepadClient::Private
{
    TreelandGamepadClient *q = nullptr;

    wl_display *display = nullptr;
    wl_registry *registry = nullptr;
    QSocketNotifier *socketNotifier = nullptr;

    QPointer<TreelandGamepadManager> manager;
    QHash<int, TreelandGamepadDevice *> devices;
    bool protocolReady = false;

    quint64 totalEventCount = 0;
    QString lastDiagnostic;
    bool focusDiagnosticEmitted = false;
    bool focusDiagnosticScheduled = false;
    uint32_t grantedCapabilities = 0;

    // 注册表监听器
    static const struct wl_registry_listener registryListener;

    static void registryGlobal(void *data,
                               wl_registry *registry,
                               uint32_t name,
                               const char *interface,
                               uint32_t version)
    {
        auto *d = static_cast<Private *>(data);

        if (strcmp(interface, "treeland_gamepad_manager_v1") != 0) {
            return;
        }

        if (d->manager) {
            return;
        }

        d->manager = new TreelandGamepadManager(d->q);
        if (d->manager->bind(registry, name, version)) {
            d->protocolReady = true;
            QObject::connect(d->manager,
                             &TreelandGamepadManager::gamepadAdded,
                             d->q,
                             &TreelandGamepadClient::handleGamepadAdded);
            QObject::connect(d->manager,
                             &TreelandGamepadManager::gamepadRemoved,
                             d->q,
                             &TreelandGamepadClient::handleGamepadRemoved);
            QObject::connect(d->manager,
                             &TreelandGamepadManager::authorized,
                             d->q,
                             [d](uint32_t capabilities) {
                                 d->grantedCapabilities = capabilities;
                                 Q_EMIT d->q->grantedCapabilitiesChanged(capabilities);
                                 Q_EMIT d->q->authorized(capabilities);
                             });
            QObject::connect(d->manager,
                             &TreelandGamepadManager::authorizationFailed,
                             d->q,
                             [d](uint32_t error) {
                                 Q_EMIT d->q->authorizationFailed(error);
                             });
        }
    }

    static void registryGlobalRemove(void *data, wl_registry *registry, uint32_t name)
    {
        Q_UNUSED(data)
        Q_UNUSED(registry)
        Q_UNUSED(name)
        // 如需处理移除
    }
};

const struct wl_registry_listener TreelandGamepadClient::Private::registryListener = {
    &TreelandGamepadClient::Private::registryGlobal,
    &TreelandGamepadClient::Private::registryGlobalRemove
};

TreelandGamepadClient::TreelandGamepadClient(QObject *parent)
    : QObject(parent)
    , d(std::make_unique<Private>())
{
    d->q = this;

    (void)qRegisterMetaType<DeckGamepadButtonEvent>();
    (void)qRegisterMetaType<DeckGamepadAxisEvent>();
    (void)qRegisterMetaType<DeckGamepadHatEvent>();
}

TreelandGamepadClient::~TreelandGamepadClient()
{
    disconnectFromCompositor();
}

bool TreelandGamepadClient::connectToCompositor(const QString &socketName)
{
    if (d->display) {
        qWarning() << "Already connected to compositor";
        return false;
    }

    // 连接 Wayland display
    if (socketName.isEmpty()) {
        d->display = wl_display_connect(nullptr);
    } else {
        d->display = wl_display_connect(socketName.toUtf8().constData());
    }

    if (!d->display) {
        qWarning() << "Failed to connect to Wayland display" << socketName;
        return false;
    }

    setupRegistry();

    // 接入 Qt 事件循环
    int fd = wl_display_get_fd(d->display);
    d->socketNotifier = new QSocketNotifier(fd, QSocketNotifier::Read, this);
    connect(d->socketNotifier,
            &QSocketNotifier::activated,
            this,
            &TreelandGamepadClient::handleWaylandEvents);

    // 首次 roundtrip 获取 globals
    wl_display_roundtrip(d->display);

    if (!d->protocolReady) {
        qWarning() << "treeland_gamepad_manager_v1 protocol is not available on this compositor";
        disconnectFromCompositor();
        return false;
    }

    // 二次 roundtrip 处理即时设备
    wl_display_roundtrip(d->display);
    wl_display_dispatch_pending(d->display);

    Q_EMIT connectedChanged(true);
    return true;
}

void TreelandGamepadClient::disconnectFromCompositor()
{
    if (!d->display) {
        return;
    }

    // 清理设备
    for (auto it = d->devices.cbegin(); it != d->devices.cend(); ++it) {
        if (it.value()) {
            it.value()->deleteLater();
        }
    }
    d->devices.clear();

    // 清理管理器
    if (d->manager) {
        d->manager->unbind();
        d->manager->deleteLater();
        d->manager = nullptr;
    }

    // 清理 registry
    teardownRegistry();

    // 清理 socket notifier
    if (d->socketNotifier) {
        d->socketNotifier->setEnabled(false);
        d->socketNotifier->deleteLater();
        d->socketNotifier = nullptr;
    }

    // 断开 display 连接
    wl_display_disconnect(d->display);
    d->display = nullptr;
    d->protocolReady = false;

    if (d->totalEventCount != 0) {
        d->totalEventCount = 0;
        Q_EMIT totalEventCountChanged(0);
    }

    if (!d->lastDiagnostic.isEmpty()) {
        d->lastDiagnostic.clear();
        Q_EMIT lastDiagnosticChanged(d->lastDiagnostic);
    }

    if (d->grantedCapabilities != 0) {
        d->grantedCapabilities = 0;
        Q_EMIT grantedCapabilitiesChanged(0);
    }

    d->focusDiagnosticEmitted = false;
    d->focusDiagnosticScheduled = false;

    Q_EMIT connectedChanged(false);
}

bool TreelandGamepadClient::isConnected() const
{
    return d->display != nullptr;
}

quint64 TreelandGamepadClient::totalEventCount() const
{
    return d->totalEventCount;
}

QString TreelandGamepadClient::lastDiagnostic() const
{
    return d->lastDiagnostic;
}

uint32_t TreelandGamepadClient::grantedCapabilities() const
{
    return d->grantedCapabilities;
}

QList<int> TreelandGamepadClient::availableGamepads() const
{
    return d->devices.keys();
}

TreelandGamepadDevice *TreelandGamepadClient::gamepad(int deviceId) const
{
    return d->devices.value(deviceId, nullptr);
}

void TreelandGamepadClient::setVibration(int deviceId,
                                         double weakMagnitude,
                                         double strongMagnitude,
                                         int durationMs)
{
    if (auto *device = gamepad(deviceId)) {
        device->setVibration(weakMagnitude, strongMagnitude, durationMs);
    }
}

void TreelandGamepadClient::stopVibration(int deviceId)
{
    if (auto *device = gamepad(deviceId)) {
        device->stopVibration();
    }
}

void TreelandGamepadClient::stopAllVibration()
{
    for (const auto &device : d->devices) {
        device->stopVibration();
    }
}

bool TreelandGamepadClient::authorize(const QString &token)
{
    if (!d->display || !d->manager || !d->manager->isBound()) {
        return false;
    }
    if (!d->manager->authorize(token)) {
        return false;
    }
    wl_display_flush(d->display);
    return true;
}

bool TreelandGamepadClient::hasCapability(uint32_t capability) const
{
    return (d->grantedCapabilities & capability) != 0;
}

void TreelandGamepadClient::handleWaylandEvents()
{
    if (!d->display) {
        return;
    }

    // 准备读取事件
    while (wl_display_prepare_read(d->display) != 0) {
        wl_display_dispatch_pending(d->display);
    }

    // 刷新待处理请求
    wl_display_flush(d->display);

    // 从 socket 读取事件
    wl_display_read_events(d->display);

    // 分发事件
    wl_display_dispatch_pending(d->display);
}

void TreelandGamepadClient::setupRegistry()
{
    d->registry = wl_display_get_registry(d->display);
    wl_registry_add_listener(d->registry, &Private::registryListener, d.get());
}

void TreelandGamepadClient::teardownRegistry()
{
    if (d->registry) {
        wl_registry_destroy(d->registry);
        d->registry = nullptr;
    }
}

void TreelandGamepadClient::handleGamepadAdded(int deviceId, const QString &name)
{
    if (!d->manager) {
        return;
    }

    // 创建设备包装对象
    auto device = new TreelandGamepadDevice(this, deviceId, name);

    // 连接设备信号到全局信号
    connect(device,
            &TreelandGamepadDevice::buttonEvent,
            this,
            [this, deviceId](DeckGamepadButtonEvent event) {
                if (d->totalEventCount == 0 && !d->lastDiagnostic.isEmpty()) {
                    d->lastDiagnostic.clear();
                    Q_EMIT lastDiagnosticChanged(d->lastDiagnostic);
                }
                d->totalEventCount++;
                Q_EMIT totalEventCountChanged(d->totalEventCount);
                Q_EMIT buttonEvent(deviceId, event);
            });
    connect(device,
            &TreelandGamepadDevice::axisEvent,
            this,
            [this, deviceId](DeckGamepadAxisEvent event) {
                if (d->totalEventCount == 0 && !d->lastDiagnostic.isEmpty()) {
                    d->lastDiagnostic.clear();
                    Q_EMIT lastDiagnosticChanged(d->lastDiagnostic);
                }
                d->totalEventCount++;
                Q_EMIT totalEventCountChanged(d->totalEventCount);
                Q_EMIT axisEvent(deviceId, event);
            });
    connect(device,
            &TreelandGamepadDevice::hatEvent,
            this,
            [this, deviceId](DeckGamepadHatEvent event) {
                if (d->totalEventCount == 0 && !d->lastDiagnostic.isEmpty()) {
                    d->lastDiagnostic.clear();
                    Q_EMIT lastDiagnosticChanged(d->lastDiagnostic);
                }
                d->totalEventCount++;
                Q_EMIT totalEventCountChanged(d->totalEventCount);
                Q_EMIT hatEvent(deviceId, event);
            });

    d->devices[deviceId] = device;

    // 创建 Wayland gamepad 对象
    if (d->manager) {
        d->manager->createGamepad(deviceId);
    }

    if (!d->focusDiagnosticScheduled) {
        d->focusDiagnosticScheduled = true;
        QTimer::singleShot(1000, this, [this]() {
            d->focusDiagnosticScheduled = false;
            if (!d->display || d->devices.isEmpty() || d->totalEventCount > 0
                || d->focusDiagnosticEmitted) {
                return;
            }

            d->focusDiagnosticEmitted = true;
            d->lastDiagnostic = QStringLiteral(
                "Treeland gamepad: 已连接且发现设备，但未收到事件。该协议默认存在 focused "
                "gating：仅向键盘焦点所属客户端发送事件；请确保窗口获得键盘焦点。若需要后台收事件（"
                "用于校准/诊断），需先通过系统授权获取 token 并调用 authorize(token) 申请 "
                "listen_background 能力。");
            Q_EMIT lastDiagnosticChanged(d->lastDiagnostic);
        });
    }

    Q_EMIT gamepadAdded(deviceId, name);
}

void TreelandGamepadClient::handleGamepadRemoved(int deviceId)
{
    auto *device = d->devices.take(deviceId);
    if (!device) {
        return;
    }

    // 销毁 Wayland gamepad 对象
    if (d->manager) {
        d->manager->destroyGamepad(deviceId);
    }

    // 延迟释放设备对象
    device->deleteLater();

    Q_EMIT gamepadRemoved(deviceId);
}

} // namespace TreelandGamepad
