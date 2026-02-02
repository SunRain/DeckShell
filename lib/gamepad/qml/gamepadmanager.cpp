// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "gamepadmanager.h"

#include "custommappingmanager.h"
#include "gamepaddevicemodel.h"

#include <deckshell/deckgamepad/service/deckgamepadservice.h>
#include <deckshell/deckgamepad/providers/evdev/evdevprovider.h>

#include <QtCore/QDebug>
#include <QtQml/QQmlContext>

#if DECKGAMEPAD_ENABLE_TREELAND
#include <deckshell/deckgamepad/treeland/treelandprovider.h>
#endif

using deckshell::deckgamepad::DeckGamepadService;
using deckshell::deckgamepad::DeckGamepadError;
using deckshell::deckgamepad::DeckGamepadDiagnostic;
using deckshell::deckgamepad::DeckGamepadErrorKind;
using deckshell::deckgamepad::EvdevProvider;
#if DECKGAMEPAD_ENABLE_TREELAND
using deckshell::deckgamepad::TreelandProvider;
#endif

static GamepadManager::DiagnosticKind diagnosticKindFromError(const DeckGamepadError &err)
{
    switch (err.kind()) {
    case DeckGamepadErrorKind::None:
        return GamepadManager::DiagnosticKind::Ok;
    case DeckGamepadErrorKind::Denied:
        return GamepadManager::DiagnosticKind::Denied;
    case DeckGamepadErrorKind::Unsupported:
        return GamepadManager::DiagnosticKind::Unsupported;
    case DeckGamepadErrorKind::Unavailable:
        return GamepadManager::DiagnosticKind::Unavailable;
    case DeckGamepadErrorKind::InvalidConfig:
    case DeckGamepadErrorKind::Unknown:
        return GamepadManager::DiagnosticKind::Error;
    case DeckGamepadErrorKind::Io:
        return GamepadManager::DiagnosticKind::Unavailable;
    default:
        return GamepadManager::DiagnosticKind::Error;
    }
}

static GamepadManager::DiagnosticKind diagnosticKindFromDiagnosticKey(const QString &key)
{
    using namespace deckshell::deckgamepad;
    if (key.isEmpty()) {
        return GamepadManager::DiagnosticKind::Ok;
    }
    if (key == QLatin1StringView(DeckGamepadDiagnosticKey::PermissionDenied)
        || key == QLatin1StringView(DeckGamepadDiagnosticKey::WaylandNotAuthorized)) {
        return GamepadManager::DiagnosticKind::Denied;
    }
    if (key == QLatin1StringView(DeckGamepadDiagnosticKey::LogindUnavailable)) {
        return GamepadManager::DiagnosticKind::Unavailable;
    }
    if (key == QLatin1StringView(DeckGamepadDiagnosticKey::WaylandFocusGated)) {
        return GamepadManager::DiagnosticKind::Unavailable;
    }
    if (key == QLatin1StringView(DeckGamepadDiagnosticKey::SessionInactive)) {
        return GamepadManager::DiagnosticKind::Unavailable;
    }
    if (key == QLatin1StringView(DeckGamepadDiagnosticKey::DeviceBusy)
        || key == QLatin1StringView(DeckGamepadDiagnosticKey::DeviceGrabFailed)) {
        return GamepadManager::DiagnosticKind::Unavailable;
    }
    return GamepadManager::DiagnosticKind::Error;
}

GamepadManager *GamepadManager::s_instance = nullptr;

GamepadManager::GamepadManager(QObject *parent)
    : QObject(parent)
    , m_ownedService(new DeckGamepadService(nullptr, this))
    , m_deviceModel(new GamepadDeviceModel(this))
    , m_customMapping(new CustomMappingManager(this))
{
    // QML_SINGLETON 的实例可能由 QML 引擎直接构造（不走 GamepadManager::instance/create）。
    // 为避免 QML 单例与 C++ 侧 instance() 产生“双实例”而导致事件链路断开，这里统一绑定全局指针。
    if (!s_instance) {
        s_instance = this;
    }

    bindService(m_ownedService);

    refreshDeviceModel();
}

GamepadManager::~GamepadManager()
{
    if (s_instance == this) {
        s_instance = nullptr;
    }
}

GamepadManager *GamepadManager::instance()
{
    if (!s_instance) {
        s_instance = new GamepadManager();
    }
    return s_instance;
}

GamepadManager *GamepadManager::create(QQmlEngine *engine, QJSEngine *scriptEngine)
{
    Q_UNUSED(scriptEngine);
    auto *inst = GamepadManager::instance();
    if (engine) {
        engine->setObjectOwnership(inst, QQmlEngine::CppOwnership);

        // 外部 service 注入契约：
        // - 宿主进程如需复用外部 DeckGamepadService，应在加载任何 QML 之前设置：
        //   engine.rootContext()->setContextProperty("_deckGamepadService", serviceObject)
        // - 其他 QML 类型（如 Gamepad/ServiceActionRouter/GamepadKeyNavigation）可能在未显式引用 GamepadManager
        //   的情况下解析 service，因此应通过本 create() 获取 manager 以避免错过注入时机。
        const QVariant injected = engine->rootContext()->contextProperty(QStringLiteral("_deckGamepadService"));
        auto *obj = injected.value<QObject *>();
        auto *svc = qobject_cast<DeckGamepadService *>(obj);
        if (svc) {
            inst->setExternalService(svc);
        } else {
            qWarning() << "DeckShell.DeckGamepad GamepadManager: 未注入 _deckGamepadService（请在加载 QML 前设置 rootContext 属性），使用内部 service";
        }
    }
    return inst;
}

GamepadManager::BackendMode GamepadManager::backendMode() const
{
    return m_backendMode;
}

void GamepadManager::setBackendMode(BackendMode mode)
{
    if (m_backendMode == mode) {
        return;
    }

    if (hasExternalServiceInjected()) {
        m_backendMode = mode;
        Q_EMIT backendModeChanged();
        setSwitchDiagnostic(QStringLiteral("已注入外部 DeckGamepadService：backendMode 仅作显示，不会切换后端"),
                            DiagnosticKind::Unsupported);
        return;
    }

    const bool wasRunning = m_service && m_service->state() == DeckGamepadService::State::Running;
    const ActiveBackend previousActive = m_activeBackend;

    m_backendMode = mode;
    Q_EMIT backendModeChanged();

    if (!wasRunning) {
        return;
    }

    if (start()) {
        return;
    }

    const QString failedDiagnostic = m_diagnostic;
    const DiagnosticKind failedKind = m_diagnosticKind;

    bool restored = false;
    switch (previousActive) {
    case ActiveBackend::Evdev:
        restored = startEvdev();
        break;
    case ActiveBackend::Treeland:
#if DECKGAMEPAD_ENABLE_TREELAND
        restored = startTreeland();
#else
        restored = false;
#endif
        break;
    case ActiveBackend::None:
        restored = false;
        break;
    }

    if (restored) {
        setSwitchDiagnostic(QStringLiteral("后端切换失败，已恢复上一后端：") + failedDiagnostic, failedKind);
        refreshDeviceModel();
        Q_EMIT connectedCountChanged();
        updateErrorDiagnosticFromService();
        updateDiagnostic();
    }
}

GamepadManager::ProviderSelection GamepadManager::providerSelection() const
{
    return m_providerSelection;
}

void GamepadManager::setProviderSelection(ProviderSelection selection)
{
    if (m_providerSelection == selection) {
        return;
    }

    if (hasExternalServiceInjected()) {
        m_providerSelection = selection;
        Q_EMIT providerSelectionChanged();
        setSwitchDiagnostic(QStringLiteral("已注入外部 DeckGamepadService：providerSelection 仅作显示，不会切换 provider"),
                            DiagnosticKind::Unsupported);
        return;
    }

    const bool wasRunning = m_service && m_service->state() == DeckGamepadService::State::Running;
    const ProviderSelection previous = m_providerSelection;

    m_providerSelection = selection;
    Q_EMIT providerSelectionChanged();

    if (!wasRunning) {
        return;
    }

    // providerSelection 仅影响 evdev 分支；Treeland 模式下变更仅生效于下次切回 evdev。
    if (m_backendMode == BackendMode::Treeland) {
        setSwitchDiagnostic(QStringLiteral("Treeland 后端下 providerSelection 不生效（切回 evdev 后生效）"),
                            DiagnosticKind::Unsupported);
        return;
    }

    if (start()) {
        return;
    }

    const QString failedDiagnostic = m_diagnostic;
    const DiagnosticKind failedKind = m_diagnosticKind;

    // 回滚到之前的选择
    m_providerSelection = previous;
    Q_EMIT providerSelectionChanged();
    const bool restored = start();

    if (restored) {
        setSwitchDiagnostic(QStringLiteral("Provider 切换失败，已恢复上一选择：") + failedDiagnostic, failedKind);
        refreshDeviceModel();
        Q_EMIT connectedCountChanged();
        updateErrorDiagnosticFromService();
        updateDiagnostic();
    }
}

GamepadManager::ActiveBackend GamepadManager::activeBackend() const
{
    return m_activeBackend;
}

QString GamepadManager::activeProviderName() const
{
    return m_service ? m_service->activeProviderName() : QString{};
}

int GamepadManager::connectedCount() const
{
    return m_service ? m_service->connectedGamepads().size() : 0;
}

GamepadDeviceModel *GamepadManager::deviceModel() const
{
    return m_deviceModel;
}

CustomMappingManager *GamepadManager::customMapping() const
{
    return m_customMapping;
}

QString GamepadManager::diagnostic() const
{
    return m_diagnostic;
}

QString GamepadManager::diagnosticKey() const
{
    return m_diagnosticKey;
}

QStringList GamepadManager::suggestedActions() const
{
    return m_suggestedActions;
}

GamepadManager::DiagnosticKind GamepadManager::diagnosticKind() const
{
    return m_diagnosticKind;
}

bool GamepadManager::start()
{
    if (!m_service) {
        return false;
    }

    if (hasExternalServiceInjected()) {
        refreshDeviceModel();
        Q_EMIT connectedCountChanged();
        updateErrorDiagnosticFromService();
        updateDiagnostic();
        return m_service->state() == DeckGamepadService::State::Running;
    }

    setSwitchDiagnostic(QString{}, DiagnosticKind::Ok);
    setProviderDiagnostic(QString{});

    bool ok = false;
    switch (m_backendMode) {
    case BackendMode::Auto:
        ok = startAuto();
        break;
    case BackendMode::Evdev:
        ok = startEvdev();
        break;
    case BackendMode::Treeland:
        ok = startTreeland();
        break;
    }

    refreshDeviceModel();
    Q_EMIT connectedCountChanged();
    updateErrorDiagnosticFromService();
    updateDiagnostic();
    return ok;
}

void GamepadManager::stop()
{
    if (!m_service) {
        return;
    }

    if (hasExternalServiceInjected()) {
        return;
    }

    m_service->stop();
    setActiveBackend(ActiveBackend::None);
    refreshDeviceModel();
    Q_EMIT connectedCountChanged();
    updateErrorDiagnosticFromService();
    setSwitchDiagnostic(QString{}, DiagnosticKind::Ok);
    setProviderDiagnostic(QString{});
    updateDiagnostic();
}

void GamepadManager::setAxisDeadzone(int deviceId, int axis, double deadzone)
{
    if (!m_service) {
        return;
    }
    m_service->setAxisDeadzone(deviceId, static_cast<uint32_t>(axis), static_cast<float>(deadzone));
}

void GamepadManager::setAxisSensitivity(int deviceId, int axis, double sensitivity)
{
    if (!m_service) {
        return;
    }
    m_service->setAxisSensitivity(deviceId, static_cast<uint32_t>(axis), static_cast<float>(sensitivity));
}

bool GamepadManager::startVibration(int deviceId, double weak, double strong, int durationMs)
{
    if (!m_service) {
        return false;
    }
    return m_service->startVibration(deviceId,
                                     static_cast<float>(weak),
                                     static_cast<float>(strong),
                                     durationMs);
}

void GamepadManager::stopVibration(int deviceId)
{
    if (!m_service) {
        return;
    }
    m_service->stopVibration(deviceId);
}

QVariantList GamepadManager::connectedGamepads() const
{
    QVariantList result;
    if (!m_service) {
        return result;
    }

    const auto deviceIds = m_service->connectedGamepads();
    result.reserve(deviceIds.size());
    for (int id : deviceIds) {
        QVariantMap deviceInfo;
        deviceInfo.insert(QStringLiteral("deviceId"), id);
        deviceInfo.insert(QStringLiteral("name"), m_service->deviceName(id));
        deviceInfo.insert(QStringLiteral("playerIndex"), m_service->playerIndex(id));
        result.append(deviceInfo);
    }
    return result;
}

QString GamepadManager::gamepadName(int deviceId) const
{
    return m_service ? m_service->deviceName(deviceId) : QString{};
}

int GamepadManager::playerIndex(int deviceId) const
{
    return m_service ? m_service->playerIndex(deviceId) : -1;
}

int GamepadManager::assignPlayer(int deviceId)
{
    return m_service ? m_service->assignPlayer(deviceId) : -1;
}

void GamepadManager::unassignPlayer(int deviceId)
{
    if (m_service) {
        m_service->unassignPlayer(deviceId);
    }
}

void GamepadManager::setExternalService(DeckGamepadService *service)
{
    if (!service) {
        return;
    }

    if (m_service == service && m_externalServiceInjected) {
        return;
    }

    m_externalServiceInjected = true;

    if (m_ownedService && m_ownedService != service) {
        m_ownedService->stop();
    }

    bindService(service);
    setActiveBackend(ActiveBackend::None);

    refreshDeviceModel();
    Q_EMIT connectedCountChanged();
    updateErrorDiagnosticFromService();
    updateDiagnostic();
}

DeckGamepadService *GamepadManager::service() const
{
    return m_service;
}

void GamepadManager::refreshDeviceModel()
{
    if (m_deviceModel) {
        m_deviceModel->refresh();
    }
}

void GamepadManager::bindService(DeckGamepadService *service)
{
    if (m_service == service) {
        return;
    }

    if (m_service) {
        disconnect(m_service, nullptr, this, nullptr);
        if (m_customMapping) {
            disconnect(m_service, nullptr, m_customMapping, nullptr);
        }
    }

    m_service = service;

    if (m_customMapping) {
        m_customMapping->setService(m_service);
    }

    if (!m_service) {
        refreshDeviceModel();
        Q_EMIT connectedCountChanged();
        Q_EMIT activeProviderNameChanged();
        updateErrorDiagnosticFromService();
        updateDiagnostic();
        return;
    }

    connect(m_service, &DeckGamepadService::gamepadConnected, this, [this](int deviceId, const QString &name) {
        refreshDeviceModel();
        Q_EMIT connectedCountChanged();
        Q_EMIT gamepadConnected(deviceId, name);
    });
    connect(m_service, &DeckGamepadService::gamepadDisconnected, this, [this](int deviceId) {
        refreshDeviceModel();
        Q_EMIT connectedCountChanged();
        Q_EMIT gamepadDisconnected(deviceId);
    });

    connect(m_service, &DeckGamepadService::playerAssigned, this, [this](int deviceId, int index) {
        refreshDeviceModel();
        Q_EMIT playerAssigned(deviceId, index);
    });
    connect(m_service, &DeckGamepadService::playerUnassigned, this, [this](int deviceId) {
        refreshDeviceModel();
        Q_EMIT playerUnassigned(deviceId);
    });

    connect(m_service,
            &DeckGamepadService::buttonEvent,
            this,
            [this](int deviceId, deckshell::deckgamepad::DeckGamepadButtonEvent event) {
                const int button = static_cast<int>(event.button);
                Q_EMIT buttonEvent(deviceId, button, event.pressed);
                if (event.pressed) {
                    Q_EMIT buttonPressed(deviceId, button);
                } else {
                    Q_EMIT buttonReleased(deviceId, button);
                }
            });
    connect(m_service,
            &DeckGamepadService::axisEvent,
            this,
            [this](int deviceId, deckshell::deckgamepad::DeckGamepadAxisEvent event) {
                const int axis = static_cast<int>(event.axis);
                Q_EMIT axisEvent(deviceId, axis, event.value);
                Q_EMIT axisChanged(deviceId, axis, event.value);
            });
    connect(m_service,
            &DeckGamepadService::hatEvent,
            this,
            [this](int deviceId, deckshell::deckgamepad::DeckGamepadHatEvent event) {
                const int hat = static_cast<int>(event.hat);
                Q_EMIT hatEvent(deviceId, hat, event.value);
                Q_EMIT hatChanged(deviceId, hat, event.value);
            });

    connect(m_service, &DeckGamepadService::lastErrorChanged, this, [this]() {
        updateErrorDiagnosticFromService();
    });
    connect(m_service, &DeckGamepadService::stateChanged, this, [this]() {
        updateErrorDiagnosticFromService();
    });
    connect(m_service, &DeckGamepadService::diagnosticChanged, this, [this](DeckGamepadDiagnostic) {
        updateErrorDiagnosticFromService();
    });

    connect(m_service, &DeckGamepadService::providerChanged, this, [this]() {
        Q_EMIT activeProviderNameChanged();
        refreshDeviceModel();
        Q_EMIT connectedCountChanged();
        updateErrorDiagnosticFromService();
        updateDiagnostic();
    });

    if (m_customMapping) {
        connect(m_service, &DeckGamepadService::capabilitiesChanged, m_customMapping, &CustomMappingManager::syncFromService);
    }

    refreshDeviceModel();
    updateErrorDiagnosticFromService();
    updateDiagnostic();
    Q_EMIT activeProviderNameChanged();
}

bool GamepadManager::hasExternalServiceInjected() const
{
    return m_externalServiceInjected && m_service && m_service != m_ownedService;
}

bool GamepadManager::startAuto()
{
    setSwitchDiagnostic(QString{}, DiagnosticKind::Ok);

#if DECKGAMEPAD_ENABLE_TREELAND
    if (!m_service) {
        setActiveBackend(ActiveBackend::None);
        return false;
    }

    const bool treelandOk = startWithProvider(new TreelandProvider());
    if (treelandOk) {
        setActiveBackend(ActiveBackend::Treeland);
        setProviderDiagnostic(QString{});
        return true;
    }

    const auto err = m_service->lastError();
    QString reason = err.message;
    if (!err.hint.isEmpty()) {
        reason = reason + QStringLiteral(" (") + err.hint + QStringLiteral(")");
    }

    const bool evdevOk = startEvdev();
    if (evdevOk) {
        setSwitchDiagnostic(QStringLiteral("Auto: Treeland 不可用，已降级为 ")
                                + activeProviderName()
                                + QStringLiteral("：")
                                + reason,
                            diagnosticKindFromError(err));
        return true;
    }

    setSwitchDiagnostic(QStringLiteral("Auto: Treeland 与 evdev provider 均启动失败"), DiagnosticKind::Error);
    return false;
#else
    const bool evdevOk = startEvdev();
    if (evdevOk) {
        setSwitchDiagnostic(QStringLiteral("Auto: Treeland 后端未编译（DECKGAMEPAD_BUILD_TREELAND_CLIENT=OFF），使用 ")
                                + activeProviderName(),
                            DiagnosticKind::Unsupported);
    }
    return evdevOk;
#endif
}

bool GamepadManager::startEvdev()
{
    if (!m_service) {
        setActiveBackend(ActiveBackend::None);
        return false;
    }

    // 统一使用 EvdevProvider：providerSelection 仅用于控制其线程模式（IO vs single-thread debug）。
    deckshell::deckgamepad::DeckGamepadRuntimeConfig cfg = m_service->runtimeConfig();
    switch (m_providerSelection) {
    case ProviderSelection::EvdevUdev:
        cfg.providerSelection = deckshell::deckgamepad::DeckGamepadProviderSelection::EvdevUdev;
        break;
    case ProviderSelection::Evdev:
        cfg.providerSelection = deckshell::deckgamepad::DeckGamepadProviderSelection::Evdev;
        break;
    case ProviderSelection::Auto:
    default:
        cfg.providerSelection = deckshell::deckgamepad::DeckGamepadProviderSelection::Auto;
        break;
    }

    m_service->stop();
    (void)m_service->setRuntimeConfig(cfg);

    const bool ok = startWithProvider(new EvdevProvider());
    setActiveBackend(ok ? ActiveBackend::Evdev : ActiveBackend::None);
    setProviderDiagnostic(QString{});
    return ok;
}

bool GamepadManager::startTreeland()
{
#if DECKGAMEPAD_ENABLE_TREELAND
    if (!m_service) {
        setActiveBackend(ActiveBackend::None);
        return false;
    }

    const bool ok = startWithProvider(new TreelandProvider());
    setActiveBackend(ok ? ActiveBackend::Treeland : ActiveBackend::None);
    setProviderDiagnostic(QString{});
    return ok;
#else
    setActiveBackend(ActiveBackend::None);
    setSwitchDiagnostic(QStringLiteral("Treeland 后端未编译（DECKGAMEPAD_BUILD_TREELAND_CLIENT=OFF）"),
                        DiagnosticKind::Unsupported);
    return false;
#endif
}

bool GamepadManager::startWithProvider(deckshell::deckgamepad::IDeckGamepadProvider *provider)
{
    if (hasExternalServiceInjected()) {
        setActiveBackend(ActiveBackend::None);
        setSwitchDiagnostic(QStringLiteral("已注入外部 DeckGamepadService：不支持在 QML 中切换后端"), DiagnosticKind::Unsupported);
        return false;
    }

    if (!m_service || !provider) {
        return false;
    }

    m_service->stop();
    if (!m_service->setProvider(provider)) {
        if (provider->parent() != m_service) {
            delete provider;
        }
        return false;
    }
    return m_service->start();
}

void GamepadManager::setActiveBackend(ActiveBackend backend)
{
    if (m_activeBackend == backend) {
        return;
    }
    m_activeBackend = backend;
    Q_EMIT activeBackendChanged();
}

void GamepadManager::setSwitchDiagnostic(QString message, DiagnosticKind kind)
{
    const DiagnosticKind normalizedKind = message.isEmpty() ? DiagnosticKind::Ok : kind;
    if (m_switchDiagnostic == message && m_switchKind == normalizedKind) {
        return;
    }
    m_switchDiagnostic = std::move(message);
    m_switchKind = normalizedKind;
    updateDiagnostic();
}

void GamepadManager::setProviderDiagnostic(QString message)
{
    if (m_providerDiagnostic == message) {
        return;
    }
    m_providerDiagnostic = std::move(message);
    updateDiagnostic();
}

void GamepadManager::updateErrorDiagnosticFromService()
{
    QString next;
    QString nextKey;
    QStringList nextActions;
    DiagnosticKind nextKind = DiagnosticKind::Ok;
    if (m_service) {
        const auto diag = m_service->diagnostic();
        nextKey = diag.key;
        nextActions = diag.suggestedActions;

        const auto err = m_service->lastError();
        if (!err.isOk()) {
            next = err.message;
            if (!err.hint.isEmpty()) {
                next = next + QStringLiteral(" (") + err.hint + QStringLiteral(")");
            }
            nextKind = diagnosticKindFromError(err);
        } else if (!diag.isOk()) {
            const QVariant msgVar = diag.details.value(QStringLiteral("message"));
            next = msgVar.isValid() ? msgVar.toString() : QString{};
            if (next.isEmpty()) {
                next = diag.key;
            }
            nextKind = diagnosticKindFromDiagnosticKey(diag.key);
        }
    }

    if (m_errorDiagnostic == next && m_errorKind == nextKind) {
        // 继续检查 key/actions 变更（避免“文本不变但 key 变了”被吞掉）
    } else {
        m_errorDiagnostic = std::move(next);
        m_errorKind = nextKind;
        updateDiagnostic();
    }

    if (m_diagnosticKey != nextKey) {
        m_diagnosticKey = std::move(nextKey);
        Q_EMIT diagnosticKeyChanged();
    }

    if (m_suggestedActions != nextActions) {
        m_suggestedActions = std::move(nextActions);
        Q_EMIT suggestedActionsChanged();
    }
}

void GamepadManager::updateDiagnostic()
{
    QStringList parts;
    if (!m_errorDiagnostic.isEmpty()) {
        parts.append(m_errorDiagnostic);
    }
    if (!m_switchDiagnostic.isEmpty()) {
        parts.append(m_switchDiagnostic);
    }
    if (!m_providerDiagnostic.isEmpty()) {
        parts.append(m_providerDiagnostic);
    }

    const QString next = parts.join(QLatin1Char('\n'));
    if (m_diagnostic == next) {
        return;
    }
    m_diagnostic = next;
    Q_EMIT diagnosticChanged();

    updateDiagnosticKind();
}

void GamepadManager::updateDiagnosticKind()
{
    DiagnosticKind next = DiagnosticKind::Ok;
    if (m_errorKind != DiagnosticKind::Ok) {
        next = m_errorKind;
    } else if (m_switchKind != DiagnosticKind::Ok) {
        next = m_switchKind;
    }

    if (m_diagnosticKind == next) {
        return;
    }

    m_diagnosticKind = next;
    Q_EMIT diagnosticKindChanged();
}
