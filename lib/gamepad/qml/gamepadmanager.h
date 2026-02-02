// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QtCore/QObject>
#include <QtCore/QString>
#include <QtCore/QStringList>
#include <QtCore/QVariant>
#include <QtQml/QQmlEngine>
#include <QtQml/qqml.h>

namespace deckshell::deckgamepad {
class DeckGamepadService;
class IDeckGamepadProvider;
}

class CustomMappingManager;
class GamepadDeviceModel;

class GamepadManager : public QObject
{
    Q_OBJECT
    QML_ELEMENT
    QML_SINGLETON

    Q_PROPERTY(BackendMode backendMode READ backendMode WRITE setBackendMode NOTIFY backendModeChanged FINAL)
    Q_PROPERTY(ProviderSelection providerSelection READ providerSelection WRITE setProviderSelection NOTIFY providerSelectionChanged FINAL)
    Q_PROPERTY(ActiveBackend activeBackend READ activeBackend NOTIFY activeBackendChanged FINAL)
    Q_PROPERTY(QString activeProviderName READ activeProviderName NOTIFY activeProviderNameChanged FINAL)
    Q_PROPERTY(int connectedCount READ connectedCount NOTIFY connectedCountChanged FINAL)
    Q_PROPERTY(GamepadDeviceModel *deviceModel READ deviceModel CONSTANT FINAL)
    Q_PROPERTY(CustomMappingManager *customMapping READ customMapping CONSTANT FINAL)
    Q_PROPERTY(QString diagnostic READ diagnostic NOTIFY diagnosticChanged FINAL)
    Q_PROPERTY(QString diagnosticKey READ diagnosticKey NOTIFY diagnosticKeyChanged FINAL)
    Q_PROPERTY(QStringList suggestedActions READ suggestedActions NOTIFY suggestedActionsChanged FINAL)
    Q_PROPERTY(DiagnosticKind diagnosticKind READ diagnosticKind NOTIFY diagnosticKindChanged FINAL)

public:
    enum class BackendMode {
        Auto = 0,
        Evdev,
        Treeland,
    };
    Q_ENUM(BackendMode)

    enum class ProviderSelection {
        Auto = 0,
        EvdevUdev,
        Evdev,
    };
    Q_ENUM(ProviderSelection)

    enum class ActiveBackend {
        None = 0,
        Evdev,
        Treeland,
    };
    Q_ENUM(ActiveBackend)

    enum class DiagnosticKind {
        Ok = 0,
        Unsupported,
        Denied,
        Unavailable,
        Error,
    };
    Q_ENUM(DiagnosticKind)

    static GamepadManager *instance();
    static GamepadManager *create(QQmlEngine *engine, QJSEngine *scriptEngine);

    explicit GamepadManager(QObject *parent = nullptr);
    ~GamepadManager() override;

    BackendMode backendMode() const;
    void setBackendMode(BackendMode mode);

    ProviderSelection providerSelection() const;
    void setProviderSelection(ProviderSelection selection);

    ActiveBackend activeBackend() const;
    QString activeProviderName() const;

    int connectedCount() const;
    GamepadDeviceModel *deviceModel() const;
    CustomMappingManager *customMapping() const;

    QString diagnostic() const;
    QString diagnosticKey() const;
    QStringList suggestedActions() const;
    DiagnosticKind diagnosticKind() const;

    Q_INVOKABLE bool start();
    Q_INVOKABLE void stop();

    Q_INVOKABLE void setAxisDeadzone(int deviceId, int axis, double deadzone);
    Q_INVOKABLE void setAxisSensitivity(int deviceId, int axis, double sensitivity);
    Q_INVOKABLE bool startVibration(int deviceId, double weak, double strong, int durationMs = 1000);
    Q_INVOKABLE void stopVibration(int deviceId);

    // ========== compositor 兼容 API ==========
    Q_INVOKABLE QVariantList connectedGamepads() const;
    Q_INVOKABLE QString gamepadName(int deviceId) const;
    Q_INVOKABLE int playerIndex(int deviceId) const;
    Q_INVOKABLE int assignPlayer(int deviceId);
    Q_INVOKABLE void unassignPlayer(int deviceId);

    // 外部 Service 注入：用于 compositor 进程复用 Helper 创建的单例，避免重复打开设备。
    void setExternalService(deckshell::deckgamepad::DeckGamepadService *service);

    deckshell::deckgamepad::DeckGamepadService *service() const;

Q_SIGNALS:
    void backendModeChanged();
    void providerSelectionChanged();
    void activeBackendChanged();
    void activeProviderNameChanged();
    void connectedCountChanged();
    void diagnosticChanged();
    void diagnosticKeyChanged();
    void suggestedActionsChanged();
    void diagnosticKindChanged();

    void gamepadConnected(int deviceId, const QString &name);
    void gamepadDisconnected(int deviceId);
    void buttonEvent(int deviceId, int button, bool pressed);
    void axisEvent(int deviceId, int axis, double value);
    void hatEvent(int deviceId, int hat, int value);

    // compositor 兼容信号
    void playerAssigned(int deviceId, int playerIndex);
    void playerUnassigned(int deviceId);
    void buttonPressed(int deviceId, int button);
    void buttonReleased(int deviceId, int button);
    void axisChanged(int deviceId, int axis, double value);
    void hatChanged(int deviceId, int hat, int direction);

private:
    static GamepadManager *s_instance;

    void refreshDeviceModel();
    void bindService(deckshell::deckgamepad::DeckGamepadService *service);
    bool hasExternalServiceInjected() const;
    bool startAuto();
    bool startEvdev();
    bool startTreeland();
    bool startWithProvider(deckshell::deckgamepad::IDeckGamepadProvider *provider);

    void setActiveBackend(ActiveBackend backend);
    void setSwitchDiagnostic(QString message, DiagnosticKind kind = DiagnosticKind::Ok);
    void setProviderDiagnostic(QString message);
    void updateErrorDiagnosticFromService();
    void updateDiagnostic();
    void updateDiagnosticKind();

    deckshell::deckgamepad::DeckGamepadService *m_ownedService = nullptr;
    deckshell::deckgamepad::DeckGamepadService *m_service = nullptr;
    GamepadDeviceModel *m_deviceModel = nullptr;
    CustomMappingManager *m_customMapping = nullptr;

    BackendMode m_backendMode = BackendMode::Auto;
    ProviderSelection m_providerSelection = ProviderSelection::Auto;
    ActiveBackend m_activeBackend = ActiveBackend::None;

    QString m_switchDiagnostic;
    DiagnosticKind m_switchKind = DiagnosticKind::Ok;
    QString m_providerDiagnostic;
    QString m_errorDiagnostic;
    QString m_diagnostic;
    QString m_diagnosticKey;
    QStringList m_suggestedActions;
    DiagnosticKind m_errorKind = DiagnosticKind::Ok;
    DiagnosticKind m_diagnosticKind = DiagnosticKind::Ok;

    bool m_externalServiceInjected = false;
};
