// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QObject>
#include <QString>
#include <QStringList>
#include <QJsonObject>
#include <QFileSystemWatcher>
#include <QQmlEngine>
#include <QMap>

#include <deckshell/deckgamepad/extras/keyboardmappingprofile.h>

class QTimer;

namespace deckshell {
namespace deckgamepad {
class DeckGamepadService;
class DeckGamepadKeyboardMappingManager;
}
}

class GamepadConfigManager : public QObject
{
    Q_OBJECT
    QML_ELEMENT
    QML_SINGLETON

    Q_PROPERTY(bool autoAssignPlayer READ autoAssignPlayer WRITE setAutoAssignPlayer NOTIFY configChanged FINAL)
    Q_PROPERTY(float defaultDeadzone READ defaultDeadzone WRITE setDefaultDeadzone NOTIFY configChanged FINAL)
    Q_PROPERTY(float defaultSensitivity READ defaultSensitivity WRITE setDefaultSensitivity NOTIFY configChanged FINAL)
    Q_PROPERTY(bool vibrationEnabled READ vibrationEnabled WRITE setVibrationEnabled NOTIFY configChanged FINAL)
    Q_PROPERTY(bool keyboardMappingEnabled READ keyboardMappingEnabled WRITE setKeyboardMappingEnabled
            NOTIFY keyboardMappingEnabledChanged FINAL)

public:
    static GamepadConfigManager* instance();
    static GamepadConfigManager* create(QQmlEngine *engine, QJSEngine *scriptEngine);

    explicit GamepadConfigManager(QObject *parent = nullptr);
    ~GamepadConfigManager() override;

    // 配置加载/保存
    Q_INVOKABLE bool loadConfig(const QString &filePath = QString());
    Q_INVOKABLE bool saveConfig(const QString &filePath = QString());
    Q_INVOKABLE void loadDefaultConfig();

    // 热更新
    Q_INVOKABLE void enableHotReload(bool enable);
    bool isHotReloadEnabled() const { return m_hotReloadEnabled; }

    // 全局设置
    bool autoAssignPlayer() const;
    void setAutoAssignPlayer(bool enable);

    float defaultDeadzone() const;
    void setDefaultDeadzone(float deadzone);

    float defaultSensitivity() const;
    void setDefaultSensitivity(float sensitivity);

    bool vibrationEnabled() const;
    void setVibrationEnabled(bool enabled);

    // 按策略执行振动：先检查配置开关，再转发到 DeckGamepadService。
    bool startVibrationWithPolicy(int deviceId, float weak, float strong, int durationMs = 1000);

    // Deadzone trial：默认临时生效，显式提交，超时自动回滚。
    Q_INVOKABLE bool beginDeadzoneTrialGlobal(float deadzone, int ttlMs = 0);
    Q_INVOKABLE bool beginDeadzoneTrialDeviceAxis(int deviceId, uint32_t axis, float deadzone, int ttlMs = 0);
    Q_INVOKABLE bool commitDeadzoneTrial();
    Q_INVOKABLE bool cancelDeadzoneTrial();
    Q_INVOKABLE bool hasDeadzoneTrial() const;
    Q_INVOKABLE int deadzoneTrialRemainingMs() const;

    // 键盘映射
    bool keyboardMappingEnabled() const;
    void setKeyboardMappingEnabled(bool enabled);

    // ========== Profile Management ==========
    
    // Profile 列表
    QStringList listProfiles() const;
    QString currentProfile() const;
    
    // Profile 增删改查
    bool createProfile(const QString &name, const QString &description = QString());
    bool switchProfile(const QString &name);
    bool deleteProfile(const QString &name);
    bool renameProfile(const QString &oldName, const QString &newName);
    
    // Profile 数据
    deckshell::deckgamepad::KeyboardMappingProfile getProfile(const QString &name) const;
    bool saveProfile(const deckshell::deckgamepad::KeyboardMappingProfile &profile);
    
    // 导入/导出
    bool exportProfile(const QString &name, const QString &filePath);
    bool importProfile(const QString &filePath);
    
    // 应用到键盘映射管理器
    void applyProfileToManager(const QString &name, deckshell::deckgamepad::DeckGamepadKeyboardMappingManager *manager);

    // Per-device settings
    float deviceDeadzone(int deviceId, uint32_t axis) const;
    void setDeviceDeadzone(int deviceId, uint32_t axis, float deadzone);

    float deviceSensitivity(int deviceId, uint32_t axis) const;
    void setDeviceSensitivity(int deviceId, uint32_t axis, float sensitivity);

    bool deviceVibrationEnabled(int deviceId) const;
    void setDeviceVibrationEnabled(int deviceId, bool enabled);

    // 应用到 DeckGamepadService
    Q_INVOKABLE void applyConfig();

    void setService(deckshell::deckgamepad::DeckGamepadService *service);
    deckshell::deckgamepad::DeckGamepadService *service() const { return m_service; }

    // 导出
    QString configFilePath() const { return m_configFilePath; }
    QJsonObject toJson() const;
    bool fromJson(const QJsonObject &json);

Q_SIGNALS:
    void configLoaded();
    void configChanged();
    void hotReloadTriggered();
    void keyboardMappingEnabledChanged(bool enabled);
    
    // Profile 信号
    void currentProfileChanged(const QString &name);
    void profileListChanged();

private Q_SLOTS:
    void onFileChanged(const QString &path);
    void onGamepadConnected(int deviceId, const QString &name);

private:
    QString configDir() const;
    QString getDefaultConfigPath() const;
    QString getDeviceKey(int deviceId) const;
    QString getLegacyDeviceKey(int deviceId) const;
    QString getDeviceKeyForRead(int deviceId) const;
    void applyDeviceConfig(int deviceId);
    float persistedDeviceDeadzone(int deviceId, uint32_t axis) const;
    void clearDeadzoneTrialState();
    void refreshDeadzoneTrialTimer(int ttlMs);
    
    // Profile 路径与兼容处理
    QString getProfilesDir() const;
    QString getLegacyProfilesDir() const;
    QString getProfilePath(const QString &name) const;
    QString getLegacyProfilePath(const QString &name) const;
    QString resolveExistingProfilePath(const QString &name) const;
    QString resolveProfilePathForWrite(const QString &name) const;
    bool loadProfile(const QString &name);
    void ensureProfilesDir();

    static GamepadConfigManager *m_instance;

    deckshell::deckgamepad::DeckGamepadService *m_service = nullptr;

    // 配置数据
    QJsonObject m_config;
    QString m_configFilePath;

    // 热更新
    bool m_hotReloadEnabled;
    QFileSystemWatcher *m_fileWatcher;

    struct DeadzoneTrialAxisEntry {
        float baseline = 0.0f;
        float value = 0.0f;
    };

    static constexpr int kDefaultDeadzoneTrialTtlMs = 30000;

    // Deadzone trial 状态（不可写入 m_config）
    bool m_deadzoneTrialHasGlobalDefault = false;
    float m_deadzoneTrialGlobalDefault = 0.0f;
    float m_deadzoneTrialBaselineGlobalDefault = 0.0f;
    QMap<QString, QMap<uint32_t, DeadzoneTrialAxisEntry>> m_deadzoneTrialDeviceAxis;
    QTimer *m_deadzoneTrialTimer = nullptr;

    // 缓存的全局设置
    bool m_autoAssignPlayer;
    float m_defaultDeadzone;
    float m_defaultSensitivity;
    bool m_vibrationEnabled;
    bool m_keyboardMappingEnabled;
    
    // Profile 管理
    QString m_currentProfile;
    QMap<QString, deckshell::deckgamepad::KeyboardMappingProfile> m_profileCache;

    // 测试/覆盖
    QString m_configDirOverride;
};
