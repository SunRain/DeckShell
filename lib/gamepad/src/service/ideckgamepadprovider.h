// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

// 统一的手柄后端提供者接口：封装设备枚举/热插拔/输入事件/基础控制，并为上层提供稳定抽象边界。
// 本接口采用 Qt signals/slots 风格，供 DeckGamepadService 聚合并作为上层唯一推荐入口。

#pragma once

#include <deckshell/deckgamepad/core/deckgamepad.h>
#include <deckshell/deckgamepad/core/deckgamepaddiagnostic.h>
#include <deckshell/deckgamepad/core/deckgamepaderror.h>
#include <deckshell/deckgamepad/core/deckgamepaddeviceinfo.h>
#include <deckshell/deckgamepad/core/deckgamepadruntimeconfig.h>

#include <QtCore/QList>
#include <QtCore/QObject>
#include <QtCore/QString>

DECKGAMEPAD_BEGIN_NAMESPACE

class DeckGamepadCustomMappingManager;
class ICalibrationStore;

/**
 * @brief 统一的手柄 Provider 抽象（Qt 信号风格）
 *
 * 关键契约（阶段1）：
 * - start/stop 必须幂等；start 失败不得留下半初始化资源。
 * - Provider 依赖 Qt 事件循环（如使用 QSocketNotifier），要求在有 event loop 的线程运行。
 * - 信号发射线程语义必须明确：默认与 Provider 所在线程一致；不承诺跨线程 direct connection 安全。
 * - connectedGamepads() 必须与 gamepadConnected/gamepadDisconnected 保持一致性：
 *   - 发出 gamepadConnected 后，connectedGamepads() 必须可查询到该 deviceId。
 *   - 发出 gamepadDisconnected 后，connectedGamepads() 不应再包含该 deviceId。
 */
class DECKGAMEPAD_EXPORT IDeckGamepadProvider : public QObject
{
    Q_OBJECT

public:
    explicit IDeckGamepadProvider(QObject *parent = nullptr)
        : QObject(parent)
    {
    }
    ~IDeckGamepadProvider() override = default;

    virtual QString name() const = 0;

    // 运行期配置：仅约束“可被调用”，不强制 Provider 立即生效（推荐 start 前设置）。
    virtual bool setRuntimeConfig(const DeckGamepadRuntimeConfig &config) = 0;
    virtual DeckGamepadRuntimeConfig runtimeConfig() const = 0;

    virtual bool start() = 0;
    virtual void stop() = 0;

    // 设备集合：known 包含已发现但不可用设备；connected 仅包含可用（可收事件）设备。
    virtual QList<int> knownGamepads() const = 0;
    virtual QList<int> connectedGamepads() const = 0;
    virtual QString deviceName(int deviceId) const = 0;
    virtual QString deviceGuid(int deviceId) const = 0;
    virtual DeckGamepadDeviceInfo deviceInfo(int deviceId) const = 0;
    // 可选：用于上层持久化/排障（如无法提供稳定 uid，可返回空并在 deviceInfo 中退化）。
    virtual QString deviceUid(int deviceId) const = 0;

    virtual DeckGamepadDeviceAvailability deviceAvailability(int deviceId) const = 0;
    virtual DeckGamepadError deviceLastError(int deviceId) const = 0;

    virtual void setAxisDeadzone(int deviceId, uint32_t axis, float deadzone) = 0;
    virtual void setAxisSensitivity(int deviceId, uint32_t axis, float sensitivity) = 0;

    virtual bool startVibration(int deviceId,
                                float weakMagnitude,
                                float strongMagnitude,
                                int durationMs) = 0;
    virtual void stopVibration(int deviceId) = 0;

    // 可选能力端口：不可用时返回 nullptr；端口对象生命周期必须清晰（推荐与 Service 绑定）。
    virtual DeckGamepadCustomMappingManager *customMappingManager() const = 0;
    virtual ICalibrationStore *calibrationStore() const = 0;

    // Provider 级别错误（例如 start 失败、后端崩溃/异常等）
    virtual DeckGamepadError lastError() const = 0;
    // Provider 级别诊断（例如 focused gating/授权语义等非错误态提示）
    virtual DeckGamepadDiagnostic diagnostic() const = 0;

Q_SIGNALS:
    void lastErrorChanged(DeckGamepadError error);
    void diagnosticChanged(DeckGamepadDiagnostic diagnostic);
    void deviceAvailabilityChanged(int deviceId, DeckGamepadDeviceAvailability availability);
    void deviceLastErrorChanged(int deviceId, DeckGamepadError error);

    void gamepadConnected(int deviceId, const QString &name);
    void gamepadDisconnected(int deviceId);
    void buttonEvent(int deviceId, DeckGamepadButtonEvent event);
    void axisEvent(int deviceId, DeckGamepadAxisEvent event);
    void hatEvent(int deviceId, DeckGamepadHatEvent event);
};

DECKGAMEPAD_END_NAMESPACE
