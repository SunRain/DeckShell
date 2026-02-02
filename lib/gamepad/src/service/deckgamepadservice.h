// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

// 手柄统一入口（Service）：聚合 Provider，向上层暴露稳定 API 与输入事件信号，并提供最小可观测面。

#pragma once

#include "ideckgamepadprovider.h"

#include <deckshell/deckgamepad/core/deckgamepadaction.h>
#include <deckshell/deckgamepad/core/deckgamepaddiagnostic.h>
#include <array>
#include <memory>
#include <QtCore/QHash>
#include <QtCore/QObject>
#include <QtCore/QString>
#include <QtCore/QStringList>
#include <QtCore/QTimer>
#include <QtCore/QVariantMap>

DECKGAMEPAD_BEGIN_NAMESPACE

class DeckGamepadCustomMappingManager;
class ICalibrationStore;
class DeckGamepadActionMapper;
struct ActionMappingProfile;

class DECKGAMEPAD_EXPORT DeckGamepadService final : public QObject
{
    Q_OBJECT

public:
    enum class State {
        Stopped,
        Running,
        Failed,
    };
    Q_ENUM(State)

    explicit DeckGamepadService(QObject *parent = nullptr);
    explicit DeckGamepadService(IDeckGamepadProvider *provider, QObject *parent = nullptr);
    ~DeckGamepadService() override;

    // ========== 可观测面 ==========
    State state() const;
    QString activeProviderName() const;

    DeckGamepadError lastError() const;
    QString lastErrorMessage() const;
    int lastErrno() const;
    QString lastErrorContext() const;

    // 诊断契约（稳定 key + 可选 details + 建议动作）
    DeckGamepadDiagnostic diagnostic() const;
    QString diagnosticKey() const;
    QVariantMap diagnosticDetails() const;
    QStringList suggestedActions() const;

    quint64 totalEventCount() const;
    qint64 lastEventWallclockMs() const;

    // axis/hat coalesce 统计（仅统计 Service 输出侧）
    quint64 axisRawEventCount() const;
    quint64 axisEmittedEventCount() const;
    quint64 axisDroppedEventCount() const;
    quint64 hatRawEventCount() const;
    quint64 hatEmittedEventCount() const;
    quint64 hatDroppedEventCount() const;
    int lastCoalesceLatencyMs() const;

    bool hasCustomMappingManager() const;
    bool hasCalibrationStore() const;

    // ========== 生命周期 ==========
    bool start();
    void stop();

    DeckGamepadRuntimeConfig runtimeConfig() const;
    // 运行中禁止变更配置（避免“半生效”）；如需切换请 stop → setRuntimeConfig → start。
    bool setRuntimeConfig(DeckGamepadRuntimeConfig config);

    // Provider 注入/替换：仅允许在 Stopped 状态替换；运行中替换会失败并保留原 provider。
    bool setProvider(IDeckGamepadProvider *provider);
    IDeckGamepadProvider *provider() const;

    // ========== 统一 API（薄转发）==========
    QList<int> knownGamepads() const;
    QList<int> connectedGamepads() const;
    QString deviceName(int deviceId) const;
    QString deviceGuid(int deviceId) const;
    DeckGamepadDeviceInfo deviceInfo(int deviceId) const;
    QString deviceUid(int deviceId) const;
    DeckGamepadDeviceAvailability deviceAvailability(int deviceId) const;
    DeckGamepadError deviceLastError(int deviceId) const;

    void setAxisDeadzone(int deviceId, uint32_t axis, float deadzone);
    void setAxisSensitivity(int deviceId, uint32_t axis, float sensitivity);

    bool startVibration(int deviceId, float weakMagnitude, float strongMagnitude, int durationMs = 1000);
    void stopVibration(int deviceId);

    DeckGamepadCustomMappingManager *customMappingManager() const;
    ICalibrationStore *calibrationStore() const;

    // ========== Player 分配（SSOT）==========
    // 约定：最多 4 个玩家槽（0-3），返回 -1 表示失败/无可用槽位。
    int assignPlayer(int deviceId);
    void unassignPlayer(int deviceId);
    int playerIndex(int deviceId) const;

Q_SIGNALS:
    void stateChanged(DeckGamepadService::State state);
    void lastErrorChanged();
    void diagnosticChanged(DeckGamepadDiagnostic diagnostic);
    void providerChanged();
    void capabilitiesChanged();
    void runtimeConfigChanged();

    void deviceAvailabilityChanged(int deviceId, DeckGamepadDeviceAvailability availability);
    void deviceLastErrorChanged(int deviceId, DeckGamepadError error);

    void gamepadConnected(int deviceId, const QString &name);
    void gamepadDisconnected(int deviceId);
    void playerAssigned(int deviceId, int playerIndex);
    void playerUnassigned(int deviceId);
    void buttonEvent(int deviceId, DeckGamepadButtonEvent event);
    void axisEvent(int deviceId, DeckGamepadAxisEvent event);
    void hatEvent(int deviceId, DeckGamepadHatEvent event);

    // ========== Action layer ==========
    // 直接输出稳定 actionId（可配置 mapping profile），避免上层重复实现 mapper/priority/repeat。
    void actionEvent(int deviceId, DeckGamepadActionEvent event);
    void actionTriggered(int deviceId, const QString &actionId, bool pressed, bool repeated);

private:
    bool setProviderInternal(IDeckGamepadProvider *provider, bool disableAutoSelect);
    void ensureProviderConnections();
    void clearProviderConnections();
    void updateDiagnostic();
    static DeckGamepadDiagnostic diagnosticFromError(const DeckGamepadError &error);
    void flushCoalescedAxisHatEvents();
    void flushCoalescedAxisEvents();
    void flushCoalescedHatEvents();

    void clearPlayerAssignments();

    bool reloadActionMappingProfile();
    void clearActionMappers();
    DeckGamepadActionMapper *ensureActionMapper(int deviceId);
    void handleHatAsVirtualDpadButtons(int deviceId, const DeckGamepadHatEvent &event);

    void clearError();
    void setError(DeckGamepadError error);
    void setState(State state);

    IDeckGamepadProvider *m_provider = nullptr; // QObject 生命周期由 parent 关系管理；不使用时为 nullptr
    bool m_autoSelectProvider = true; // true: setRuntimeConfig() 可根据 providerSelection 自动切换 provider
    State m_state = State::Stopped;

    DeckGamepadRuntimeConfig m_runtimeConfig;
    DeckGamepadError m_lastError;
    DeckGamepadDiagnostic m_diagnostic;

    QHash<int, DeckGamepadDeviceAvailability> m_deviceAvailabilityCache;
    QHash<int, DeckGamepadError> m_deviceErrorCache;

    quint64 m_totalEventCount = 0;
    qint64 m_lastEventWallclockMs = -1;

    bool m_providerConnectionsReady = false;

    QTimer m_axisCoalesceTimer;
    qint64 m_axisCoalesceStartWallclockMs = -1;
    QHash<quint64, DeckGamepadAxisEvent> m_pendingAxisEvents;

    QTimer m_hatCoalesceTimer;
    qint64 m_hatCoalesceStartWallclockMs = -1;
    QHash<quint64, DeckGamepadHatEvent> m_pendingHatEvents;

    std::unique_ptr<ActionMappingProfile> m_actionMappingProfile;
    QHash<int, DeckGamepadActionMapper *> m_actionMapperByDevice;
    QHash<int, int> m_hat0ValueByDevice;

    static constexpr int kMaxPlayerSlots = 4;
    std::array<int, kMaxPlayerSlots> m_playerAssignments{ { -1, -1, -1, -1 } }; // playerIndex -> deviceId
    QHash<int, int> m_playerIndexByDevice; // deviceId -> playerIndex

    quint64 m_axisRawEventCount = 0;
    quint64 m_axisEmittedEventCount = 0;
    quint64 m_hatRawEventCount = 0;
    quint64 m_hatEmittedEventCount = 0;
    int m_lastAxisCoalesceLatencyMs = 0;
    int m_lastHatCoalesceLatencyMs = 0;
    int m_lastCoalesceLatencyMs = 0;
};

DECKGAMEPAD_END_NAMESPACE
