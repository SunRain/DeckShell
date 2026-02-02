// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "treelandprovider.h"

#include "treelandgamepadclient.h"
#include "treelandgamepaddevice.h"

#include <deckshell/deckgamepad/core/deckgamepadaction.h>

#include <QtCore/QCryptographicHash>

DECKGAMEPAD_BEGIN_NAMESPACE

TreelandProvider::TreelandProvider(QObject *parent)
    : IDeckGamepadProvider(parent)
    , m_client(new TreelandGamepad::TreelandGamepadClient(this))
{
    connect(m_client, &TreelandGamepad::TreelandGamepadClient::gamepadAdded, this, [this](int deviceId, const QString &name) {
        Q_EMIT gamepadConnected(deviceId, name);
        Q_EMIT deviceAvailabilityChanged(deviceId, DeckGamepadDeviceAvailability::Available);

        if (auto *dev = m_client->gamepad(deviceId)) {
            connect(dev,
                    &TreelandGamepad::TreelandGamepadDevice::axisDeadzoneApplied,
                    this,
                    [this](uint32_t, double) { setError(DeckGamepadError{}); });
            connect(dev,
                    &TreelandGamepad::TreelandGamepadDevice::axisDeadzoneFailed,
                    this,
                    [this](uint32_t, uint32_t error) {
                        DeckGamepadError err;
                        err.code = (error == 1) ? DeckGamepadErrorCode::PermissionDenied : DeckGamepadErrorCode::Unknown;
                        err.message = QStringLiteral("Failed to set deadzone via Treeland protocol");
                        err.context = QStringLiteral("TreelandProvider::setAxisDeadzone");
                        err.recoverable = true;
                        setError(err);
                    });
        }
    });
    connect(m_client, &TreelandGamepad::TreelandGamepadClient::gamepadRemoved, this, [this](int deviceId) {
        Q_EMIT gamepadDisconnected(deviceId);
        Q_EMIT deviceAvailabilityChanged(deviceId, DeckGamepadDeviceAvailability::Removed);
    });

    connect(m_client,
            &TreelandGamepad::TreelandGamepadClient::buttonEvent,
            this,
            [this](int deviceId, DeckGamepadButtonEvent event) {
                Q_EMIT buttonEvent(deviceId, event);
            });
    connect(m_client,
            &TreelandGamepad::TreelandGamepadClient::axisEvent,
            this,
            [this](int deviceId, DeckGamepadAxisEvent event) {
                Q_EMIT axisEvent(deviceId, event);
            });
    connect(m_client,
            &TreelandGamepad::TreelandGamepadClient::hatEvent,
            this,
            [this](int deviceId, DeckGamepadHatEvent event) {
                Q_EMIT hatEvent(deviceId, event);
            });

    connect(m_client,
            &TreelandGamepad::TreelandGamepadClient::lastDiagnosticChanged,
            this,
            [this](const QString &message) {
                DeckGamepadDiagnostic diag;
                if (!message.isEmpty()) {
                    diag.key = QString::fromLatin1(DeckGamepadDiagnosticKey::WaylandFocusGated);
                    diag.details.insert(QStringLiteral("message"), message);
                    diag.suggestedActions = { QString::fromLatin1(DeckGamepadActionId::HelpFocusWindow),
                                              QString::fromLatin1(DeckGamepadActionId::HelpRequestAuthorization) };
                }
                setDiagnostic(std::move(diag));
            });
}

TreelandProvider::~TreelandProvider()
{
    stop();
}

QString TreelandProvider::name() const
{
    return QStringLiteral("treeland");
}

bool TreelandProvider::setRuntimeConfig(const DeckGamepadRuntimeConfig &config)
{
    if (m_running) {
        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::InvalidConfig;
        err.message = QStringLiteral("setRuntimeConfig is only allowed when provider is not running");
        err.context = QStringLiteral("TreelandProvider::setRuntimeConfig");
        err.recoverable = true;
        setError(err);
        return false;
    }

    m_config = config;
    return true;
}

DeckGamepadRuntimeConfig TreelandProvider::runtimeConfig() const
{
    return m_config;
}

bool TreelandProvider::start()
{
    if (m_running) {
        return true;
    }
    if (!m_client) {
        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::BackendStartFailed;
        err.message = QStringLiteral("No TreelandGamepadClient instance");
        err.context = QStringLiteral("TreelandProvider::start");
        err.recoverable = false;
        setError(err);
        return false;
    }

    setError(DeckGamepadError{});
    setDiagnostic(DeckGamepadDiagnostic{});

    const bool ok = m_client->connectToCompositor();
    if (!ok) {
        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::BackendStartFailed;
        err.message = QStringLiteral("Treeland backend unavailable (connect or protocol not ready)");
        err.context = QStringLiteral("TreelandGamepadClient::connectToCompositor");
        err.hint = QStringLiteral("ensure running in a Wayland session and compositor provides treeland_gamepad_manager_v1");
        err.recoverable = true;
        setError(err);
        return false;
    }

    m_running = true;

    // initial availability signals
    for (int id : m_client->availableGamepads()) {
        Q_EMIT deviceAvailabilityChanged(id, DeckGamepadDeviceAvailability::Available);
    }

    return true;
}

void TreelandProvider::stop()
{
    if (!m_running) {
        return;
    }
    if (m_client) {
        m_client->disconnectFromCompositor();
    }
    m_running = false;
}

QList<int> TreelandProvider::knownGamepads() const
{
    return m_client ? m_client->availableGamepads() : QList<int>{};
}

QList<int> TreelandProvider::connectedGamepads() const
{
    return m_client ? m_client->availableGamepads() : QList<int>{};
}

QString TreelandProvider::deviceName(int deviceId) const
{
    if (!m_client) {
        return {};
    }
    auto *dev = m_client->gamepad(deviceId);
    return dev ? dev->name() : QString{};
}

QString TreelandProvider::deviceGuid(int deviceId) const
{
    if (!m_client) {
        return {};
    }
    auto *dev = m_client->gamepad(deviceId);
    return dev ? dev->guid() : QString{};
}

DeckGamepadDeviceInfo TreelandProvider::deviceInfo(int deviceId) const
{
    DeckGamepadDeviceInfo info;
    if (!m_client) {
        return info;
    }

    auto *dev = m_client->gamepad(deviceId);
    if (!dev) {
        return info;
    }

    info.name = dev->name();
    info.guid = dev->guid();
    info.transport = QStringLiteral("wayland");
    info.supportsRumble = true; // 协议层对外暴露振动能力；实际可用性由 compositor 决定

    // treeland 侧暂无 udev 信息：用 guid/name 脱敏 hash 作为稳定 uid（同进程/同协议实例稳定）。
    const QByteArray seed = (info.guid + QLatin1Char('|') + info.name).toUtf8();
    const QByteArray digest = QCryptographicHash::hash(seed, QCryptographicHash::Sha256).toHex();
    info.deviceUid = QStringLiteral("treeland:") + QString::fromLatin1(digest.left(32));

    return info;
}

QString TreelandProvider::deviceUid(int deviceId) const
{
    return deviceInfo(deviceId).deviceUid;
}

DeckGamepadDeviceAvailability TreelandProvider::deviceAvailability(int deviceId) const
{
    if (!m_client || !m_client->gamepad(deviceId)) {
        return DeckGamepadDeviceAvailability::Removed;
    }
    return DeckGamepadDeviceAvailability::Available;
}

DeckGamepadError TreelandProvider::deviceLastError(int deviceId) const
{
    Q_UNUSED(deviceId);
    return {};
}

void TreelandProvider::setAxisDeadzone(int deviceId, uint32_t axis, float deadzone)
{
    if (!m_client || !m_client->gamepad(deviceId)) {
        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::Io;
        err.message = QStringLiteral("Gamepad not available");
        err.context = QStringLiteral("TreelandProvider::setAxisDeadzone");
        err.recoverable = true;
        setError(err);
        return;
    }

    if (!m_client->hasCapability(0x4 /* write_deadzone */)) {
        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::PermissionDenied;
        err.message = QStringLiteral("Not authorized: missing write-deadzone capability");
        err.context = QStringLiteral("TreelandProvider::setAxisDeadzone");
        err.hint = QStringLiteral("request token via system D-Bus + polkit, then call treeland_gamepad_manager_v1.authorize(token)");
        err.recoverable = true;
        setError(err);
        return;
    }

    setError(DeckGamepadError{});
    m_client->gamepad(deviceId)->setAxisDeadzone(axis, deadzone);
}

void TreelandProvider::setAxisSensitivity(int deviceId, uint32_t axis, float sensitivity)
{
    Q_UNUSED(deviceId);
    Q_UNUSED(axis);
    Q_UNUSED(sensitivity);

    DeckGamepadError err;
    err.code = DeckGamepadErrorCode::NotSupported;
    err.message = QStringLiteral("Axis sensitivity is not supported by Treeland backend");
    err.context = QStringLiteral("TreelandProvider::setAxisSensitivity");
    err.recoverable = true;
    setError(err);
}

bool TreelandProvider::startVibration(int deviceId, float weakMagnitude, float strongMagnitude, int durationMs)
{
    if (!m_client || !m_client->gamepad(deviceId)) {
        return false;
    }
    m_client->setVibration(deviceId, weakMagnitude, strongMagnitude, durationMs);
    return true;
}

void TreelandProvider::stopVibration(int deviceId)
{
    if (!m_client || !m_client->gamepad(deviceId)) {
        return;
    }
    m_client->stopVibration(deviceId);
}

DeckGamepadCustomMappingManager *TreelandProvider::customMappingManager() const
{
    return nullptr;
}

ICalibrationStore *TreelandProvider::calibrationStore() const
{
    return nullptr;
}

DeckGamepadError TreelandProvider::lastError() const
{
    return m_lastError;
}

DeckGamepadDiagnostic TreelandProvider::diagnostic() const
{
    return m_diagnostic;
}

void TreelandProvider::setError(DeckGamepadError error)
{
    m_lastError = std::move(error);
    Q_EMIT lastErrorChanged(m_lastError);
}

void TreelandProvider::setDiagnostic(DeckGamepadDiagnostic diagnostic)
{
    if (m_diagnostic.key == diagnostic.key && m_diagnostic.details == diagnostic.details
        && m_diagnostic.suggestedActions == diagnostic.suggestedActions) {
        return;
    }
    m_diagnostic = std::move(diagnostic);
    Q_EMIT diagnosticChanged(m_diagnostic);
}

DECKGAMEPAD_END_NAMESPACE
