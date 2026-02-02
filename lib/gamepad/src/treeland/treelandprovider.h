// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

// Treeland Provider：将 TreelandGamepadClient 适配为 IDeckGamepadProvider，供上层统一入口使用。

#pragma once

#include <deckshell/deckgamepad/service/ideckgamepadprovider.h>

#include <QtCore/QString>

namespace TreelandGamepad {
class TreelandGamepadClient;
} // namespace TreelandGamepad

DECKGAMEPAD_BEGIN_NAMESPACE

class TreelandProvider final : public IDeckGamepadProvider
{
    Q_OBJECT

public:
    explicit TreelandProvider(QObject *parent = nullptr);
    ~TreelandProvider() override;

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

private:
    void setError(DeckGamepadError error);
    void setDiagnostic(DeckGamepadDiagnostic diagnostic);

    TreelandGamepad::TreelandGamepadClient *m_client = nullptr;
    bool m_running = false;
    DeckGamepadRuntimeConfig m_config;
    DeckGamepadError m_lastError;
    DeckGamepadDiagnostic m_diagnostic;
};

DECKGAMEPAD_END_NAMESPACE
