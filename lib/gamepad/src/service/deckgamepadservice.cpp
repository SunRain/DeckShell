// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <deckshell/deckgamepad/core/deckgamepadaction.h>
#include <deckshell/deckgamepad/extras/actionmappingprofile.h>
#include <deckshell/deckgamepad/extras/deckgamepadactionmapper.h>
#include <deckshell/deckgamepad/providers/evdev/evdevprovider.h>

#include <QtCore/QDateTime>
#include <QtCore/QMetaType>

#include <algorithm>
#include <errno.h>

DECKGAMEPAD_BEGIN_NAMESPACE

#ifndef DECKGAMEPAD_DEFAULT_PROVIDER_EVDEV
#define DECKGAMEPAD_DEFAULT_PROVIDER_EVDEV 0
#endif

static void registerDeckGamepadEventMetaTypes()
{
    static bool registered = false;
    if (registered) {
        return;
    }
    registered = true;

    (void)qRegisterMetaType<DeckGamepadButtonEvent>();
    (void)qRegisterMetaType<DeckGamepadAxisEvent>();
    (void)qRegisterMetaType<DeckGamepadHatEvent>();
    (void)qRegisterMetaType<DeckGamepadActionEvent>();
    (void)qRegisterMetaType<DeckGamepadRuntimeConfig>();
    (void)qRegisterMetaType<DeckGamepadError>();
    (void)qRegisterMetaType<DeckGamepadErrorCode>();
    (void)qRegisterMetaType<DeckGamepadErrorKind>();
    (void)qRegisterMetaType<DeckGamepadDeviceAvailability>();
    (void)qRegisterMetaType<DeckGamepadDiagnostic>();
    (void)qRegisterMetaType<DeckGamepadDeviceInfo>();
    (void)qRegisterMetaType<DeckGamepadDeviceAccessMode>();
    (void)qRegisterMetaType<DeckGamepadCapturePolicy>();
    (void)qRegisterMetaType<DeckGamepadEvdevGrabMode>();
    (void)qRegisterMetaType<DeckGamepadProviderSelection>();
}

static DeckGamepadError decorateServiceError(DeckGamepadError error)
{
    if (error.isOk()) {
        return error;
    }

    // 兜底 hint：避免上层拿到“只有 code 没有可操作建议”的错误。
    if (error.hint.isEmpty()) {
        switch (error.code) {
        case DeckGamepadErrorCode::PermissionDenied:
            error.hint = QStringLiteral("check /dev/input permissions (input group or udev rules) or Treeland authorization");
            break;
        case DeckGamepadErrorCode::NotSupported:
            error.hint = QStringLiteral("try another backend or build with the required feature enabled");
            break;
        case DeckGamepadErrorCode::BackendStartFailed:
            error.hint = QStringLiteral("check runtime environment and dependencies (Wayland session/protocol, udev, etc.)");
            break;
        case DeckGamepadErrorCode::InvalidConfig:
            error.hint = QStringLiteral("stop the service before changing configuration");
            break;
        case DeckGamepadErrorCode::Io:
            error.hint = QStringLiteral("verify device availability and permissions, then retry");
            break;
        case DeckGamepadErrorCode::None:
        case DeckGamepadErrorCode::Unknown:
        default:
            break;
        }
    }

    return error;
}

static DeckGamepadProviderSelection resolveProviderSelection(const DeckGamepadRuntimeConfig &config)
{
    DeckGamepadProviderSelection selection = config.providerSelection;
    if (selection == DeckGamepadProviderSelection::Auto) {
#if DECKGAMEPAD_DEFAULT_PROVIDER_EVDEV
        selection = DeckGamepadProviderSelection::Evdev;
#else
        selection = DeckGamepadProviderSelection::EvdevUdev;
#endif
    }
    return selection;
}

static bool providerMatchesSelection(const IDeckGamepadProvider *provider, DeckGamepadProviderSelection selection)
{
    if (!provider) {
        return false;
    }

    const QString name = provider->name();
    switch (selection) {
    case DeckGamepadProviderSelection::Evdev:
    case DeckGamepadProviderSelection::EvdevUdev:
        // providerSelection 仅用于控制 EvdevProvider 的线程模式（IO vs single-thread debug），
        // provider 实体本身不再区分 evdev-udev。
        return name == QStringLiteral("evdev");
    case DeckGamepadProviderSelection::Auto:
    default:
        return false;
    }
}

static IDeckGamepadProvider *createProviderForSelection(DeckGamepadProviderSelection selection)
{
    Q_UNUSED(selection);
    return new EvdevProvider();
}

DeckGamepadService::DeckGamepadService(QObject *parent)
    : QObject(parent)
{
    registerDeckGamepadEventMetaTypes();
    m_actionMappingProfile = std::make_unique<ActionMappingProfile>(ActionMappingProfile::createNavigationPreset());

    // 默认 provider：统一使用 EvdevProvider；build 默认值控制其线程模式（evdev=IO 线程；evdev-udev=单线程调试）。
    (void)setProviderInternal(createProviderForSelection(resolveProviderSelection(m_runtimeConfig)), false);

    m_axisCoalesceTimer.setSingleShot(true);
    connect(&m_axisCoalesceTimer, &QTimer::timeout, this, &DeckGamepadService::flushCoalescedAxisEvents);

    m_hatCoalesceTimer.setSingleShot(true);
    connect(&m_hatCoalesceTimer, &QTimer::timeout, this, &DeckGamepadService::flushCoalescedHatEvents);
}

DeckGamepadService::DeckGamepadService(IDeckGamepadProvider *provider, QObject *parent)
    : QObject(parent)
{
    registerDeckGamepadEventMetaTypes();
    m_actionMappingProfile = std::make_unique<ActionMappingProfile>(ActionMappingProfile::createNavigationPreset());
    (void)setProviderInternal(provider, true);

    m_axisCoalesceTimer.setSingleShot(true);
    connect(&m_axisCoalesceTimer, &QTimer::timeout, this, &DeckGamepadService::flushCoalescedAxisEvents);

    m_hatCoalesceTimer.setSingleShot(true);
    connect(&m_hatCoalesceTimer, &QTimer::timeout, this, &DeckGamepadService::flushCoalescedHatEvents);
}

DeckGamepadService::~DeckGamepadService()
{
    stop();
}

bool DeckGamepadService::reloadActionMappingProfile()
{
    ActionMappingProfile profile = ActionMappingProfile::createNavigationPreset();

    const QString profilePath = m_runtimeConfig.resolveActionMappingProfilePath();
    if (!profilePath.isEmpty()) {
        ActionMappingProfile overrides;
        QString errorMessage;
        if (!ActionMappingProfile::loadFromFile(profilePath, &overrides, &errorMessage)) {
            DeckGamepadError err;
            err.code = DeckGamepadErrorCode::InvalidConfig;
            err.message = QStringLiteral("Failed to load action mapping profile: %1").arg(errorMessage);
            err.context = QStringLiteral("DeckGamepadService::reloadActionMappingProfile");
            err.recoverable = true;
            setError(err);
            return false;
        }
        profile.applyOverridesFrom(overrides);
    }

    if (!m_actionMappingProfile) {
        m_actionMappingProfile = std::make_unique<ActionMappingProfile>(profile);
    } else {
        *m_actionMappingProfile = profile;
    }

    return true;
}

void DeckGamepadService::clearActionMappers()
{
    const auto keys = m_actionMapperByDevice.keys();
    for (int deviceId : keys) {
        DeckGamepadActionMapper *mapper = m_actionMapperByDevice.value(deviceId);
        if (!mapper) {
            continue;
        }
        mapper->reset();
        delete mapper;
    }
    m_actionMapperByDevice.clear();
    m_hat0ValueByDevice.clear();
}

DeckGamepadActionMapper *DeckGamepadService::ensureActionMapper(int deviceId)
{
    if (deviceId < 0) {
        return nullptr;
    }

    if (DeckGamepadActionMapper *existing = m_actionMapperByDevice.value(deviceId)) {
        return existing;
    }

    auto *mapper = new DeckGamepadActionMapper(this);
    mapper->setEnabled(true);

    if (m_actionMappingProfile) {
        mapper->applyActionMappingProfile(*m_actionMappingProfile);
    } else {
        mapper->applyNavigationPreset();
    }

    connect(mapper, &DeckGamepadActionMapper::actionEvent, this, [this, deviceId](DeckGamepadActionEvent event) {
        Q_EMIT actionEvent(deviceId, event);
    });
    connect(mapper, &DeckGamepadActionMapper::actionTriggered, this, [this, deviceId](const QString &actionId, bool pressed, bool repeated) {
        Q_EMIT actionTriggered(deviceId, actionId, pressed, repeated);
    });

    m_actionMapperByDevice.insert(deviceId, mapper);
    m_hat0ValueByDevice.insert(deviceId, GAMEPAD_HAT_CENTER);
    return mapper;
}

void DeckGamepadService::handleHatAsVirtualDpadButtons(int deviceId, const DeckGamepadHatEvent &event)
{
    if (static_cast<int>(event.hat) != 0) {
        return;
    }

    DeckGamepadActionMapper *mapper = ensureActionMapper(deviceId);
    if (!mapper) {
        return;
    }

    const int prev = m_hat0ValueByDevice.value(deviceId, GAMEPAD_HAT_CENTER);
    const int next = static_cast<int>(event.value);
    if (prev == next) {
        return;
    }

    m_hat0ValueByDevice.insert(deviceId, next);

    auto update = [&](GamepadButton button, int mask) {
        const bool wasPressed = (prev & mask) != 0;
        const bool pressed = (next & mask) != 0;
        if (wasPressed == pressed) {
            return;
        }
        mapper->processButton(button, pressed, static_cast<int>(event.time_msec));
    };

    update(GAMEPAD_BUTTON_DPAD_UP, GAMEPAD_HAT_UP);
    update(GAMEPAD_BUTTON_DPAD_DOWN, GAMEPAD_HAT_DOWN);
    update(GAMEPAD_BUTTON_DPAD_LEFT, GAMEPAD_HAT_LEFT);
    update(GAMEPAD_BUTTON_DPAD_RIGHT, GAMEPAD_HAT_RIGHT);
}

DeckGamepadService::State DeckGamepadService::state() const
{
    return m_state;
}

QString DeckGamepadService::activeProviderName() const
{
    return m_provider ? m_provider->name() : QString{};
}

DeckGamepadError DeckGamepadService::lastError() const
{
    return m_lastError;
}

QString DeckGamepadService::lastErrorMessage() const
{
    return m_lastError.message;
}

int DeckGamepadService::lastErrno() const
{
    return m_lastError.sysErrno;
}

QString DeckGamepadService::lastErrorContext() const
{
    return m_lastError.context;
}

DeckGamepadDiagnostic DeckGamepadService::diagnostic() const
{
    return m_diagnostic;
}

QString DeckGamepadService::diagnosticKey() const
{
    return m_diagnostic.key;
}

QVariantMap DeckGamepadService::diagnosticDetails() const
{
    return m_diagnostic.details;
}

QStringList DeckGamepadService::suggestedActions() const
{
    return m_diagnostic.suggestedActions;
}

quint64 DeckGamepadService::totalEventCount() const
{
    return m_totalEventCount;
}

qint64 DeckGamepadService::lastEventWallclockMs() const
{
    return m_lastEventWallclockMs;
}

quint64 DeckGamepadService::axisRawEventCount() const
{
    return m_axisRawEventCount;
}

quint64 DeckGamepadService::axisEmittedEventCount() const
{
    return m_axisEmittedEventCount;
}

quint64 DeckGamepadService::axisDroppedEventCount() const
{
    return (m_axisRawEventCount >= m_axisEmittedEventCount) ? (m_axisRawEventCount - m_axisEmittedEventCount) : 0;
}

quint64 DeckGamepadService::hatRawEventCount() const
{
    return m_hatRawEventCount;
}

quint64 DeckGamepadService::hatEmittedEventCount() const
{
    return m_hatEmittedEventCount;
}

quint64 DeckGamepadService::hatDroppedEventCount() const
{
    return (m_hatRawEventCount >= m_hatEmittedEventCount) ? (m_hatRawEventCount - m_hatEmittedEventCount) : 0;
}

int DeckGamepadService::lastCoalesceLatencyMs() const
{
    return m_lastCoalesceLatencyMs;
}

bool DeckGamepadService::hasCustomMappingManager() const
{
    return customMappingManager() != nullptr;
}

bool DeckGamepadService::hasCalibrationStore() const
{
    return calibrationStore() != nullptr;
}

DeckGamepadRuntimeConfig DeckGamepadService::runtimeConfig() const
{
    return m_runtimeConfig;
}

bool DeckGamepadService::setRuntimeConfig(DeckGamepadRuntimeConfig config)
{
    if (m_state != State::Stopped) {
        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::InvalidConfig;
        err.message = QStringLiteral("setRuntimeConfig is only allowed when Stopped");
        err.context = QStringLiteral("DeckGamepadService::setRuntimeConfig");
        err.recoverable = true;
        setError(err);
        return false;
    }

    m_runtimeConfig = std::move(config);

    if (m_autoSelectProvider) {
        const DeckGamepadProviderSelection desired = resolveProviderSelection(m_runtimeConfig);
        if (!providerMatchesSelection(m_provider, desired)) {
            IDeckGamepadProvider *nextProvider = createProviderForSelection(desired);
            if (!setProviderInternal(nextProvider, false)) {
                if (nextProvider && nextProvider->parent() != this) {
                    delete nextProvider;
                }
                return false;
            }
        } else if (m_provider && !m_provider->setRuntimeConfig(m_runtimeConfig)) {
            setError(m_provider->lastError());
            return false;
        }
    } else if (m_provider && !m_provider->setRuntimeConfig(m_runtimeConfig)) {
        setError(m_provider->lastError());
        return false;
    }

    Q_EMIT runtimeConfigChanged();
    Q_EMIT capabilitiesChanged();
    return true;
}

bool DeckGamepadService::start()
{
    if (m_state == State::Running) {
        return true;
    }

    clearError();

    if (!m_provider) {
        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::InvalidConfig;
        err.message = QStringLiteral("No provider configured");
        err.context = QStringLiteral("DeckGamepadService::start");
        err.recoverable = true;
        setError(err);
        setState(State::Failed);
        return false;
    }

    if (!reloadActionMappingProfile()) {
        setState(State::Failed);
        return false;
    }

    // 确保 Provider 连接已建立，避免 connect-after-start 漏掉“已连接设备”的信号。
    ensureProviderConnections();

    if (!m_provider->setRuntimeConfig(m_runtimeConfig)) {
        setError(m_provider->lastError());
        setState(State::Failed);
        return false;
    }

    const bool ok = m_provider->start();
    if (!ok) {
        DeckGamepadError err = m_provider->lastError();
        if (err.isOk()) {
            err.code = DeckGamepadErrorCode::BackendStartFailed;
            err.message = QStringLiteral("Provider start failed");
            err.context = m_provider->name();
            err.recoverable = true;
        }
        setError(err);
        setState(State::Failed);
        return false;
    }

    setState(State::Running);
    Q_EMIT capabilitiesChanged();
    return true;
}

void DeckGamepadService::stop()
{
    if (m_state == State::Stopped) {
        return;
    }

    flushCoalescedAxisHatEvents();

    if (m_provider) {
        m_provider->stop();
    }

    clearActionMappers();
    clearPlayerAssignments();
    setState(State::Stopped);
    Q_EMIT capabilitiesChanged();
}

bool DeckGamepadService::setProvider(IDeckGamepadProvider *provider)
{
    return setProviderInternal(provider, true);
}

bool DeckGamepadService::setProviderInternal(IDeckGamepadProvider *provider, bool disableAutoSelect)
{
    if (m_state != State::Stopped) {
        DeckGamepadError err;
        err.code = DeckGamepadErrorCode::InvalidConfig;
        err.message = QStringLiteral("setProvider is only allowed when Stopped");
        err.context = QStringLiteral("DeckGamepadService::setProvider");
        err.recoverable = true;
        setError(err);
        return false;
    }

    if (provider == m_provider) {
        return true;
    }

    if (provider && !provider->setRuntimeConfig(m_runtimeConfig)) {
        setError(provider->lastError());
        return false;
    }

    if (disableAutoSelect) {
        m_autoSelectProvider = false;
    }

    IDeckGamepadProvider *previousProvider = m_provider;

    clearPlayerAssignments();
    clearActionMappers();
    clearProviderConnections();
    m_deviceAvailabilityCache.clear();
    m_deviceErrorCache.clear();

    m_provider = provider;
    if (m_provider && m_provider->parent() != this) {
        m_provider->setParent(this);
    }

    ensureProviderConnections();

    Q_EMIT providerChanged();
    Q_EMIT capabilitiesChanged();
    updateDiagnostic();

    if (previousProvider && previousProvider != m_provider && previousProvider->parent() == this) {
        delete previousProvider;
    }
    return true;
}

IDeckGamepadProvider *DeckGamepadService::provider() const
{
    return m_provider;
}

int DeckGamepadService::assignPlayer(int deviceId)
{
    if (deviceId < 0) {
        return -1;
    }

    const int existing = m_playerIndexByDevice.value(deviceId, -1);
    if (existing >= 0) {
        return existing;
    }

    // 仅允许为已连接设备分配（避免对已移除设备留下脏状态）。
    if (!connectedGamepads().contains(deviceId)) {
        return -1;
    }

    int slot = -1;
    for (int i = 0; i < kMaxPlayerSlots; ++i) {
        if (m_playerAssignments[static_cast<size_t>(i)] < 0) {
            slot = i;
            break;
        }
    }

    if (slot < 0) {
        return -1;
    }

    m_playerAssignments[static_cast<size_t>(slot)] = deviceId;
    m_playerIndexByDevice.insert(deviceId, slot);
    Q_EMIT playerAssigned(deviceId, slot);
    return slot;
}

void DeckGamepadService::unassignPlayer(int deviceId)
{
    if (deviceId < 0) {
        return;
    }

    auto it = m_playerIndexByDevice.find(deviceId);
    if (it == m_playerIndexByDevice.end()) {
        return;
    }

    const int slot = it.value();
    m_playerIndexByDevice.erase(it);

    if (slot >= 0 && slot < kMaxPlayerSlots && m_playerAssignments[static_cast<size_t>(slot)] == deviceId) {
        m_playerAssignments[static_cast<size_t>(slot)] = -1;
    } else {
        for (int i = 0; i < kMaxPlayerSlots; ++i) {
            if (m_playerAssignments[static_cast<size_t>(i)] == deviceId) {
                m_playerAssignments[static_cast<size_t>(i)] = -1;
                break;
            }
        }
    }

    Q_EMIT playerUnassigned(deviceId);
}

int DeckGamepadService::playerIndex(int deviceId) const
{
    return m_playerIndexByDevice.value(deviceId, -1);
}

QList<int> DeckGamepadService::knownGamepads() const
{
    return m_provider ? m_provider->knownGamepads() : QList<int>{};
}

QList<int> DeckGamepadService::connectedGamepads() const
{
    return m_provider ? m_provider->connectedGamepads() : QList<int>{};
}

QString DeckGamepadService::deviceName(int deviceId) const
{
    return m_provider ? m_provider->deviceName(deviceId) : QString{};
}

QString DeckGamepadService::deviceGuid(int deviceId) const
{
    return m_provider ? m_provider->deviceGuid(deviceId) : QString{};
}

DeckGamepadDeviceInfo DeckGamepadService::deviceInfo(int deviceId) const
{
    return m_provider ? m_provider->deviceInfo(deviceId) : DeckGamepadDeviceInfo{};
}

QString DeckGamepadService::deviceUid(int deviceId) const
{
    return m_provider ? m_provider->deviceUid(deviceId) : QString{};
}

DeckGamepadDeviceAvailability DeckGamepadService::deviceAvailability(int deviceId) const
{
    return m_provider ? m_provider->deviceAvailability(deviceId) : DeckGamepadDeviceAvailability::Removed;
}

DeckGamepadError DeckGamepadService::deviceLastError(int deviceId) const
{
    return m_provider ? m_provider->deviceLastError(deviceId) : DeckGamepadError{};
}

void DeckGamepadService::setAxisDeadzone(int deviceId, uint32_t axis, float deadzone)
{
    if (!m_provider) {
        return;
    }
    m_provider->setAxisDeadzone(deviceId, axis, deadzone);
}

void DeckGamepadService::setAxisSensitivity(int deviceId, uint32_t axis, float sensitivity)
{
    if (!m_provider) {
        return;
    }
    m_provider->setAxisSensitivity(deviceId, axis, sensitivity);
}

bool DeckGamepadService::startVibration(int deviceId, float weakMagnitude, float strongMagnitude, int durationMs)
{
    if (!m_provider) {
        return false;
    }
    return m_provider->startVibration(deviceId, weakMagnitude, strongMagnitude, durationMs);
}

void DeckGamepadService::stopVibration(int deviceId)
{
    if (!m_provider) {
        return;
    }
    m_provider->stopVibration(deviceId);
}

DeckGamepadCustomMappingManager *DeckGamepadService::customMappingManager() const
{
    return m_provider ? m_provider->customMappingManager() : nullptr;
}

ICalibrationStore *DeckGamepadService::calibrationStore() const
{
    return m_provider ? m_provider->calibrationStore() : nullptr;
}

void DeckGamepadService::ensureProviderConnections()
{
    if (!m_provider || m_providerConnectionsReady) {
        return;
    }

    m_providerConnectionsReady = true;

	    connect(m_provider,
	            &IDeckGamepadProvider::lastErrorChanged,
	            this,
	            [this](DeckGamepadError error) {
	                setError(std::move(error));
	            });
	    connect(m_provider,
	            &IDeckGamepadProvider::diagnosticChanged,
	            this,
	            [this](DeckGamepadDiagnostic diagnostic) {
	                if (!m_provider || m_provider != sender()) {
	                    return;
	                }
	                if (!diagnostic.isOk()) {
	                    // provider 级诊断优先于 error（例如 focused gating / authorize 语义）
	                    if (m_diagnostic.key == diagnostic.key && m_diagnostic.details == diagnostic.details
	                        && m_diagnostic.suggestedActions == diagnostic.suggestedActions) {
	                        return;
	                    }
	                    m_diagnostic = std::move(diagnostic);
	                    Q_EMIT diagnosticChanged(m_diagnostic);
	                    return;
	                }
	                updateDiagnostic();
	            });
	    connect(m_provider,
	            &IDeckGamepadProvider::deviceAvailabilityChanged,
	            this,
	            [this](int deviceId, DeckGamepadDeviceAvailability availability) {
	                m_deviceAvailabilityCache.insert(deviceId, availability);
	                Q_EMIT deviceAvailabilityChanged(deviceId, availability);
	                updateDiagnostic();
	            });
	    connect(m_provider,
	            &IDeckGamepadProvider::deviceLastErrorChanged,
	            this,
	            [this](int deviceId, DeckGamepadError error) {
	                m_deviceErrorCache.insert(deviceId, error);
	                Q_EMIT deviceLastErrorChanged(deviceId, error);
	                updateDiagnostic();
	            });

	    connect(m_provider,
	            &IDeckGamepadProvider::gamepadConnected,
	            this,
	            &DeckGamepadService::gamepadConnected);
	    connect(m_provider,
	            &IDeckGamepadProvider::gamepadDisconnected,
	            this,
	            [this](int deviceId) {
	                if (DeckGamepadActionMapper *mapper = m_actionMapperByDevice.take(deviceId)) {
	                    mapper->reset();
	                    delete mapper;
	                }
	                m_hat0ValueByDevice.remove(deviceId);
	                m_deviceAvailabilityCache.remove(deviceId);
	                m_deviceErrorCache.remove(deviceId);
	                unassignPlayer(deviceId);
	                Q_EMIT gamepadDisconnected(deviceId);
	                updateDiagnostic();
	            });

    connect(m_provider,
            &IDeckGamepadProvider::buttonEvent,
            this,
            [this](int deviceId, DeckGamepadButtonEvent event) {
                m_totalEventCount++;
                m_lastEventWallclockMs = QDateTime::currentMSecsSinceEpoch();
                Q_EMIT buttonEvent(deviceId, event);

                if (event.button < static_cast<uint32_t>(GAMEPAD_BUTTON_MAX)) {
                    if (DeckGamepadActionMapper *mapper = ensureActionMapper(deviceId)) {
                        mapper->processButton(static_cast<GamepadButton>(event.button),
                                              event.pressed,
                                              static_cast<int>(event.time_msec));
                    }
                }
            });
	    connect(m_provider,
	            &IDeckGamepadProvider::axisEvent,
	            this,
	            [this](int deviceId, DeckGamepadAxisEvent event) {
	                m_totalEventCount++;
	                m_lastEventWallclockMs = QDateTime::currentMSecsSinceEpoch();
	                m_axisRawEventCount++;

	                const int intervalMs = m_runtimeConfig.axisCoalesceIntervalMs;
	                if (intervalMs <= 0) {
	                    m_axisEmittedEventCount++;
	                    Q_EMIT axisEvent(deviceId, event);

	                    if (event.axis < static_cast<uint32_t>(GAMEPAD_AXIS_MAX)) {
	                        if (DeckGamepadActionMapper *mapper = ensureActionMapper(deviceId)) {
	                            mapper->processAxis(static_cast<GamepadAxis>(event.axis),
	                                                event.value,
	                                                static_cast<int>(event.time_msec));
	                        }
	                    }
	                    return;
	                }

	                const quint64 key = (static_cast<quint64>(static_cast<uint32_t>(deviceId)) << 32)
	                    | static_cast<quint64>(event.axis);
	                m_pendingAxisEvents.insert(key, event);

	                if (!m_axisCoalesceTimer.isActive()) {
	                    m_axisCoalesceStartWallclockMs = QDateTime::currentMSecsSinceEpoch();
	                    m_axisCoalesceTimer.start(intervalMs);
	                }
	            });
	    connect(m_provider,
	            &IDeckGamepadProvider::hatEvent,
	            this,
	            [this](int deviceId, DeckGamepadHatEvent event) {
	                m_totalEventCount++;
	                m_lastEventWallclockMs = QDateTime::currentMSecsSinceEpoch();
	                m_hatRawEventCount++;

	                const int intervalMs = m_runtimeConfig.hatCoalesceIntervalMs;
	                if (intervalMs <= 0) {
	                    m_hatEmittedEventCount++;
	                    Q_EMIT hatEvent(deviceId, event);
	                    handleHatAsVirtualDpadButtons(deviceId, event);
	                    return;
	                }

	                const quint64 key = (static_cast<quint64>(static_cast<uint32_t>(deviceId)) << 32)
	                    | static_cast<quint64>(event.hat);
	                m_pendingHatEvents.insert(key, event);

	                if (!m_hatCoalesceTimer.isActive()) {
	                    m_hatCoalesceStartWallclockMs = QDateTime::currentMSecsSinceEpoch();
	                    m_hatCoalesceTimer.start(intervalMs);
	                }
	            });
}

void DeckGamepadService::clearPlayerAssignments()
{
    for (int slot = 0; slot < kMaxPlayerSlots; ++slot) {
        const int deviceId = m_playerAssignments[static_cast<size_t>(slot)];
        if (deviceId < 0) {
            continue;
        }
        m_playerAssignments[static_cast<size_t>(slot)] = -1;
        m_playerIndexByDevice.remove(deviceId);
        Q_EMIT playerUnassigned(deviceId);
    }
}

void DeckGamepadService::clearProviderConnections()
{
    if (!m_provider) {
        return;
    }
    disconnect(m_provider, nullptr, this, nullptr);
    m_providerConnectionsReady = false;
}

void DeckGamepadService::flushCoalescedAxisHatEvents()
{
    flushCoalescedAxisEvents();
    flushCoalescedHatEvents();
}

void DeckGamepadService::flushCoalescedAxisEvents()
{
    if (m_pendingAxisEvents.isEmpty()) {
        return;
    }

    const qint64 nowMs = QDateTime::currentMSecsSinceEpoch();
    if (m_axisCoalesceStartWallclockMs >= 0) {
        m_lastAxisCoalesceLatencyMs = static_cast<int>(qMax<qint64>(0, nowMs - m_axisCoalesceStartWallclockMs));
    }
    m_axisCoalesceStartWallclockMs = -1;

    // flush axis（按 key 排序，避免 QHash 迭代顺序导致测试不稳定）
    QList<quint64> keys = m_pendingAxisEvents.keys();
    std::sort(keys.begin(), keys.end());
    for (const quint64 key : keys) {
        const int deviceId = static_cast<int>((key >> 32) & 0xffffffffu);
        m_axisEmittedEventCount++;
        const DeckGamepadAxisEvent event = m_pendingAxisEvents.value(key);
        Q_EMIT axisEvent(deviceId, event);

        if (event.axis < static_cast<uint32_t>(GAMEPAD_AXIS_MAX)) {
            if (DeckGamepadActionMapper *mapper = ensureActionMapper(deviceId)) {
                mapper->processAxis(static_cast<GamepadAxis>(event.axis),
                                    event.value,
                                    static_cast<int>(event.time_msec));
            }
        }
    }
    m_pendingAxisEvents.clear();

    m_lastCoalesceLatencyMs = qMax(m_lastAxisCoalesceLatencyMs, m_lastHatCoalesceLatencyMs);
}

void DeckGamepadService::flushCoalescedHatEvents()
{
    if (m_pendingHatEvents.isEmpty()) {
        return;
    }

    const qint64 nowMs = QDateTime::currentMSecsSinceEpoch();
    if (m_hatCoalesceStartWallclockMs >= 0) {
        m_lastHatCoalesceLatencyMs = static_cast<int>(qMax<qint64>(0, nowMs - m_hatCoalesceStartWallclockMs));
    }
    m_hatCoalesceStartWallclockMs = -1;

    // flush hat（按 key 排序，避免 QHash 迭代顺序导致测试不稳定）
    QList<quint64> keys = m_pendingHatEvents.keys();
    std::sort(keys.begin(), keys.end());
    for (const quint64 key : keys) {
        const int deviceId = static_cast<int>((key >> 32) & 0xffffffffu);
        m_hatEmittedEventCount++;
        const DeckGamepadHatEvent event = m_pendingHatEvents.value(key);
        Q_EMIT hatEvent(deviceId, event);
        handleHatAsVirtualDpadButtons(deviceId, event);
    }
    m_pendingHatEvents.clear();

    m_lastCoalesceLatencyMs = qMax(m_lastAxisCoalesceLatencyMs, m_lastHatCoalesceLatencyMs);
}

void DeckGamepadService::clearError()
{
    m_lastError = DeckGamepadError{};
    Q_EMIT lastErrorChanged();
    updateDiagnostic();
}

void DeckGamepadService::setError(DeckGamepadError error)
{
    m_lastError = decorateServiceError(std::move(error));
    Q_EMIT lastErrorChanged();
    updateDiagnostic();
}

void DeckGamepadService::setState(State state)
{
    if (m_state == state) {
        return;
    }
    m_state = state;
    Q_EMIT stateChanged(m_state);
}

void DeckGamepadService::updateDiagnostic()
{
    DeckGamepadDiagnostic next;

    if (m_provider) {
        next = m_provider->diagnostic();
    }

    if (next.isOk()) {
        next = diagnosticFromError(m_lastError);
    }

    if (next.isOk()) {
        // 兜底：从 device 级错误中选择一个可操作的诊断（优先 Unavailable）。
        int selectedDeviceId = -1;
        DeckGamepadError selectedError;

        for (auto it = m_deviceAvailabilityCache.constBegin(); it != m_deviceAvailabilityCache.constEnd(); ++it) {
            if (it.value() != DeckGamepadDeviceAvailability::Unavailable) {
                continue;
            }
            const auto errIt = m_deviceErrorCache.constFind(it.key());
            if (errIt == m_deviceErrorCache.constEnd() || errIt.value().isOk()) {
                continue;
            }
            selectedDeviceId = it.key();
            selectedError = errIt.value();
            break;
        }

        if (selectedDeviceId >= 0) {
            next = diagnosticFromError(selectedError);
            next.details.insert(QStringLiteral("deviceId"), selectedDeviceId);
        }
    }

    if (m_diagnostic.key == next.key && m_diagnostic.details == next.details
        && m_diagnostic.suggestedActions == next.suggestedActions) {
        return;
    }

    m_diagnostic = std::move(next);
    Q_EMIT diagnosticChanged(m_diagnostic);
}

DeckGamepadDiagnostic DeckGamepadService::diagnosticFromError(const DeckGamepadError &error)
{
    DeckGamepadDiagnostic diag;
    if (error.isOk()) {
        return diag;
    }

    diag.details.insert(QStringLiteral("code"), static_cast<int>(error.code));
    if (error.sysErrno != 0) {
        diag.details.insert(QStringLiteral("errno"), error.sysErrno);
    }
    if (!error.context.isEmpty()) {
        diag.details.insert(QStringLiteral("context"), error.context);
    }
    if (!error.message.isEmpty()) {
        diag.details.insert(QStringLiteral("message"), error.message);
    }
    if (!error.hint.isEmpty()) {
        diag.details.insert(QStringLiteral("hint"), error.hint);
    }

    // special cases (优先级最高)
    if (error.context.startsWith(QStringLiteral("SessionGate"))) {
        diag.key = QString::fromLatin1(DeckGamepadDiagnosticKey::SessionInactive);
        diag.suggestedActions = { QString::fromLatin1(DeckGamepadActionId::HelpSwitchToActiveSession) };
        return diag;
    }
    if (error.sysErrno == EBUSY) {
        diag.key = QString::fromLatin1(DeckGamepadDiagnosticKey::DeviceBusy);
        diag.suggestedActions = { QString::fromLatin1(DeckGamepadActionId::HelpDisableGrab),
                                  QString::fromLatin1(DeckGamepadActionId::HelpRetry) };
        return diag;
    }
    if (error.context.contains(QStringLiteral("EVIOCGRAB"))) {
        diag.key = QString::fromLatin1(DeckGamepadDiagnosticKey::DeviceGrabFailed);
        diag.suggestedActions = { QString::fromLatin1(DeckGamepadActionId::HelpDisableGrab),
                                  QString::fromLatin1(DeckGamepadActionId::HelpRetry) };
        return diag;
    }
    if (error.context.contains(QStringLiteral("logind"), Qt::CaseInsensitive)) {
        diag.key = QString::fromLatin1(DeckGamepadDiagnosticKey::LogindUnavailable);
        diag.suggestedActions = { QString::fromLatin1(DeckGamepadActionId::HelpCheckPermissions),
                                  QString::fromLatin1(DeckGamepadActionId::HelpRetry) };
        return diag;
    }

    switch (error.code) {
    case DeckGamepadErrorCode::PermissionDenied:
        diag.key = QString::fromLatin1(DeckGamepadDiagnosticKey::PermissionDenied);
        diag.suggestedActions = { QString::fromLatin1(DeckGamepadActionId::HelpCheckPermissions),
                                  QString::fromLatin1(DeckGamepadActionId::HelpRequestAuthorization) };
        break;
    case DeckGamepadErrorCode::InvalidConfig:
        diag.key = QStringLiteral("deckgamepad.invalid_config");
        diag.suggestedActions = { QString::fromLatin1(DeckGamepadActionId::HelpRetry) };
        break;
    case DeckGamepadErrorCode::NotSupported:
        diag.key = QStringLiteral("deckgamepad.not_supported");
        diag.suggestedActions = { QString::fromLatin1(DeckGamepadActionId::HelpRetry) };
        break;
    case DeckGamepadErrorCode::BackendStartFailed:
        diag.key = QStringLiteral("deckgamepad.backend.unavailable");
        diag.suggestedActions = { QString::fromLatin1(DeckGamepadActionId::HelpRetry) };
        break;
    case DeckGamepadErrorCode::Io:
        diag.key = QStringLiteral("deckgamepad.io_error");
        diag.suggestedActions = { QString::fromLatin1(DeckGamepadActionId::HelpRetry) };
        break;
    case DeckGamepadErrorCode::None:
        diag.key.clear();
        break;
    case DeckGamepadErrorCode::Unknown:
    default:
        diag.key = QStringLiteral("deckgamepad.unknown");
        diag.suggestedActions = { QString::fromLatin1(DeckGamepadActionId::HelpRetry) };
        break;
    }

    return diag;
}

DECKGAMEPAD_END_NAMESPACE
