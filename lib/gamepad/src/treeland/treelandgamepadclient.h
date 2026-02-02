// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include "treelandgamepadglobal.h"
#include <QObject>
#include <QHash>
#include <memory>
#include <cstdint>

QT_BEGIN_NAMESPACE
class QSocketNotifier;
QT_END_NAMESPACE

struct wl_display;
struct wl_registry;
struct treeland_gamepad_manager_v1;

namespace TreelandGamepad {

class TreelandGamepadDevice;
class TreelandGamepadManager;

class TREELAND_GAMEPAD_EXPORT TreelandGamepadClient : public QObject
{
    Q_OBJECT
    Q_PROPERTY(bool connected READ isConnected NOTIFY connectedChanged)
    Q_PROPERTY(quint64 totalEventCount READ totalEventCount NOTIFY totalEventCountChanged)
    Q_PROPERTY(QString lastDiagnostic READ lastDiagnostic NOTIFY lastDiagnosticChanged)
    Q_PROPERTY(uint32_t grantedCapabilities READ grantedCapabilities NOTIFY grantedCapabilitiesChanged)

public:
    explicit TreelandGamepadClient(QObject *parent = nullptr);
    ~TreelandGamepadClient();

    // Connection management
    bool connectToCompositor(const QString &socketName = QString());
    void disconnectFromCompositor();
    bool isConnected() const;

    // Diagnostics / observability
    quint64 totalEventCount() const;
    QString lastDiagnostic() const;
    uint32_t grantedCapabilities() const;

    // Device access
    QList<int> availableGamepads() const;
    TreelandGamepadDevice* gamepad(int deviceId) const;

    // Global vibration control (convenience methods)
    void setVibration(int deviceId, double weakMagnitude, double strongMagnitude, int durationMs = 0);
    void stopVibration(int deviceId);
    void stopAllVibration();

    // Authorization (protocol v2)
    bool authorize(const QString &token);
    bool hasCapability(uint32_t capability) const;

Q_SIGNALS:
    void connectedChanged(bool connected);
    void totalEventCountChanged(quint64 count);
    void lastDiagnosticChanged(const QString &message);
    void grantedCapabilitiesChanged(uint32_t capabilities);
    void gamepadAdded(int deviceId, const QString &name);
    void gamepadRemoved(int deviceId);

    void authorized(uint32_t capabilities);
    void authorizationFailed(uint32_t error);
    
    // Global event signals (for convenience)
    void buttonEvent(int deviceId, DeckGamepadButtonEvent event);
    void axisEvent(int deviceId, DeckGamepadAxisEvent event);
    void hatEvent(int deviceId, DeckGamepadHatEvent event);

private Q_SLOTS:
    void handleWaylandEvents();

private:
    void setupRegistry();
    void teardownRegistry();
    void handleGamepadAdded(int deviceId, const QString &name);
    void handleGamepadRemoved(int deviceId);

    friend class TreelandGamepadManager;
    friend class TreelandGamepadDevice;

    struct Private;
    std::unique_ptr<Private> d;
};

} // namespace TreelandGamepad
