// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

// Evdev Provider（P0 spike）：持有并管理 evdev/udev 逻辑（阶段1：内部封装 backend 实例，去单例依赖）。

#pragma once

#include <deckshell/deckgamepad/service/ideckgamepadprovider.h>

#include <QtCore/QHash>
#include <QtCore/QSet>

#include <memory>

class QThread;

DECKGAMEPAD_BEGIN_NAMESPACE

class DeckGamepadBackend;
class DeckGamepadCustomMappingManager;
class JsonCalibrationStore;
class EvdevProviderWorker;

class EvdevProvider final : public IDeckGamepadProvider
{
    Q_OBJECT

public:
    explicit EvdevProvider(QObject *parent = nullptr);
    ~EvdevProvider() override;

    QString name() const override;

    bool setRuntimeConfig(const DeckGamepadRuntimeConfig &config) override;
    DeckGamepadRuntimeConfig runtimeConfig() const override;

    bool start() override;
    void stop() override;

    QList<int> knownGamepads() const override;
    QList<int> connectedGamepads() const override;
    QString deviceName(int deviceId) const override;
    QString deviceGuid(int deviceId) const override;
    DeckGamepadDeviceInfo deviceInfo(int deviceId) const override;
    QString deviceUid(int deviceId) const override;

    DeckGamepadDeviceAvailability deviceAvailability(int deviceId) const override;
    DeckGamepadError deviceLastError(int deviceId) const override;

    void setAxisDeadzone(int deviceId, uint32_t axis, float deadzone) override;
    void setAxisSensitivity(int deviceId, uint32_t axis, float sensitivity) override;

    bool startVibration(int deviceId, float weakMagnitude, float strongMagnitude, int durationMs) override;
    void stopVibration(int deviceId) override;

    DeckGamepadCustomMappingManager *customMappingManager() const override;
    ICalibrationStore *calibrationStore() const override;
    DeckGamepadError lastError() const override;
    DeckGamepadDiagnostic diagnostic() const override;

private Q_SLOTS:
    void handleBackendLastErrorChanged(DeckGamepadError error);
    void handleBackendDeviceInfoChanged(int deviceId, DeckGamepadDeviceInfo info);
    void handleBackendDeviceAvailabilityChanged(int deviceId, DeckGamepadDeviceAvailability availability);
    void handleBackendDeviceErrorChanged(int deviceId, DeckGamepadError error);
    void handleBackendGamepadConnected(int deviceId, const QString &name);
    void handleBackendGamepadDisconnected(int deviceId);

private:
    enum class BackendMode {
        IoThread,
        SingleThreadDebug,
    };

    void ensureBackendConnections();
    void ensureCalibrationStore();
    bool wantsIoThread(const DeckGamepadRuntimeConfig &config) const;
    bool ensureBackendForConfig(const DeckGamepadRuntimeConfig &config);
    void destroyBackend();
    QList<int> sortedDeviceIds(const QSet<int> &ids) const;
    void clearCaches();
    void syncSnapshotFromBackend();
    void setError(DeckGamepadError error);

    BackendMode m_backendMode = BackendMode::IoThread;
    bool m_backendConnectionsReady = false;

    QThread *m_ioThread = nullptr;
    EvdevProviderWorker *m_worker = nullptr;
    std::unique_ptr<DeckGamepadBackend> m_singleThreadBackend;
    DeckGamepadBackend *m_backend = nullptr; // lives in IO thread, owned by worker
    DeckGamepadCustomMappingManager *m_customMappingManager = nullptr;
    bool m_running = false;

    DeckGamepadRuntimeConfig m_config;
    DeckGamepadError m_lastError;
    std::unique_ptr<JsonCalibrationStore> m_calibrationStore;

    QSet<int> m_knownIds;
    QSet<int> m_connectedIds;
    QHash<int, DeckGamepadDeviceInfo> m_deviceInfoCache;
    QHash<int, DeckGamepadDeviceAvailability> m_deviceAvailabilityCache;
    QHash<int, DeckGamepadError> m_deviceLastErrorCache;
};

DECKGAMEPAD_END_NAMESPACE
