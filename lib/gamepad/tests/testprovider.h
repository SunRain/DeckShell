// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <deckshell/deckgamepad/service/ideckgamepadprovider.h>

#include <QtCore/QHash>

DECKGAMEPAD_BEGIN_NAMESPACE

class TestGamepadProvider final : public IDeckGamepadProvider
{
public:
    explicit TestGamepadProvider(QObject *parent = nullptr)
        : IDeckGamepadProvider(parent)
    {
    }

    QString name() const override { return QStringLiteral("TestGamepadProvider"); }

    bool setRuntimeConfig(const DeckGamepadRuntimeConfig &config) override
    {
        m_runtimeConfig = config;
        return true;
    }

    DeckGamepadRuntimeConfig runtimeConfig() const override { return m_runtimeConfig; }

    bool start() override { return m_startOk; }
    void stop() override { }

    QList<int> knownGamepads() const override { return m_known; }
    QList<int> connectedGamepads() const override { return m_connected; }

    QString deviceName(int deviceId) const override { return m_deviceName.value(deviceId); }
    QString deviceGuid(int deviceId) const override { return m_deviceGuid.value(deviceId); }
    DeckGamepadDeviceInfo deviceInfo(int deviceId) const override { return m_deviceInfo.value(deviceId); }
    QString deviceUid(int deviceId) const override { return m_deviceUid.value(deviceId); }

    DeckGamepadDeviceAvailability deviceAvailability(int deviceId) const override
    {
        return m_deviceAvailability.value(deviceId, DeckGamepadDeviceAvailability::Unavailable);
    }

    DeckGamepadError deviceLastError(int deviceId) const override { return m_deviceLastError.value(deviceId); }

    void setAxisDeadzone(int deviceId, uint32_t axis, float deadzone) override
    {
        Q_UNUSED(deviceId);
        Q_UNUSED(axis);
        Q_UNUSED(deadzone);
    }

    void setAxisSensitivity(int deviceId, uint32_t axis, float sensitivity) override
    {
        Q_UNUSED(deviceId);
        Q_UNUSED(axis);
        Q_UNUSED(sensitivity);
    }

    bool startVibration(int deviceId, float weakMagnitude, float strongMagnitude, int durationMs) override
    {
        Q_UNUSED(deviceId);
        Q_UNUSED(weakMagnitude);
        Q_UNUSED(strongMagnitude);
        Q_UNUSED(durationMs);
        return false;
    }

    void stopVibration(int deviceId) override { Q_UNUSED(deviceId); }

    DeckGamepadCustomMappingManager *customMappingManager() const override { return nullptr; }
    ICalibrationStore *calibrationStore() const override { return nullptr; }

    DeckGamepadError lastError() const override { return m_lastError; }
    DeckGamepadDiagnostic diagnostic() const override { return m_diagnostic; }

    // test controls
    void setStartOk(bool ok) { m_startOk = ok; }
    void setLastErrorValue(const DeckGamepadError &error) { m_lastError = error; }
    void setDiagnosticValue(const DeckGamepadDiagnostic &diag) { m_diagnostic = diag; }

    void emitLastErrorChanged(const DeckGamepadError &error)
    {
        m_lastError = error;
        Q_EMIT lastErrorChanged(error);
    }

    void emitDiagnosticChanged(const DeckGamepadDiagnostic &diag)
    {
        m_diagnostic = diag;
        Q_EMIT diagnosticChanged(diag);
    }

    void emitDeviceAvailabilityChanged(int deviceId, DeckGamepadDeviceAvailability availability)
    {
        if (!m_known.contains(deviceId)) {
            m_known.append(deviceId);
        }
        m_deviceAvailability.insert(deviceId, availability);
        Q_EMIT deviceAvailabilityChanged(deviceId, availability);
    }

    void emitDeviceLastErrorChanged(int deviceId, const DeckGamepadError &error)
    {
        if (!m_known.contains(deviceId)) {
            m_known.append(deviceId);
        }
        m_deviceLastError.insert(deviceId, error);
        Q_EMIT deviceLastErrorChanged(deviceId, error);
    }

    void emitButtonEvent(int deviceId, DeckGamepadButtonEvent event) { Q_EMIT buttonEvent(deviceId, event); }
    void emitAxisEvent(int deviceId, DeckGamepadAxisEvent event) { Q_EMIT axisEvent(deviceId, event); }
    void emitHatEvent(int deviceId, DeckGamepadHatEvent event) { Q_EMIT hatEvent(deviceId, event); }

    void addConnectedGamepad(int deviceId, const QString &name = QStringLiteral("Test Gamepad"))
    {
        if (!m_known.contains(deviceId)) {
            m_known.append(deviceId);
        }
        if (!m_connected.contains(deviceId)) {
            m_connected.append(deviceId);
        }
        m_deviceName.insert(deviceId, name);
        m_deviceAvailability.insert(deviceId, DeckGamepadDeviceAvailability::Available);
        Q_EMIT gamepadConnected(deviceId, name);
    }

    void removeConnectedGamepad(int deviceId)
    {
        m_connected.removeAll(deviceId);
        m_deviceAvailability.insert(deviceId, DeckGamepadDeviceAvailability::Removed);
        Q_EMIT gamepadDisconnected(deviceId);
    }

private:
    bool m_startOk = true;
    DeckGamepadRuntimeConfig m_runtimeConfig;
    DeckGamepadError m_lastError;
    DeckGamepadDiagnostic m_diagnostic;

    QList<int> m_known;
    QList<int> m_connected;
    QHash<int, QString> m_deviceName;
    QHash<int, QString> m_deviceGuid;
    QHash<int, DeckGamepadDeviceInfo> m_deviceInfo;
    QHash<int, QString> m_deviceUid;
    QHash<int, DeckGamepadDeviceAvailability> m_deviceAvailability;
    QHash<int, DeckGamepadError> m_deviceLastError;
};

DECKGAMEPAD_END_NAMESPACE
