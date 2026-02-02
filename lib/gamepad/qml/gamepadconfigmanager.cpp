// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "gamepadconfigmanager.h"
#include "gamepadmanager.h"

#include <deckshell/deckgamepad/extras/keyboardmappingprofile.h>
#include <deckshell/deckgamepad/service/deckgamepadservice.h>

#include <QFile>
#include <QSaveFile>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QStandardPaths>
#include <QDir>
#include <QFileInfo>
#include <QDateTime>
#include <QTimer>
#include <QtQml/QQmlContext>

using namespace deckshell::deckgamepad;

namespace {

bool ensureParentDirExists(const QString &filePath, QString *errorMessage)
{
    const QFileInfo fileInfo(filePath);
    QDir dir = fileInfo.dir();
    if (dir.exists()) {
        return true;
    }

    if (dir.mkpath(".")) {
        return true;
    }

    if (errorMessage) {
        *errorMessage = QStringLiteral("Failed to create directory: %1").arg(dir.path());
    }
    return false;
}

bool backupExistingFile(const QString &filePath, QString *errorMessage)
{
    if (!QFile::exists(filePath)) {
        return true;
    }

    const QString backupPath = filePath + QStringLiteral(".bak");
    if (QFile::exists(backupPath) && !QFile::remove(backupPath)) {
        if (errorMessage) {
            *errorMessage = QStringLiteral("Failed to remove existing backup: %1").arg(backupPath);
        }
        return false;
    }

    if (!QFile::copy(filePath, backupPath)) {
        if (errorMessage) {
            *errorMessage = QStringLiteral("Failed to create backup: %1").arg(backupPath);
        }
        return false;
    }

    return true;
}

bool writeJsonAtomically(const QString &filePath, const QJsonObject &json, QString *errorMessage)
{
    QSaveFile file(filePath);
    if (!file.open(QIODevice::WriteOnly)) {
        if (errorMessage) {
            *errorMessage = file.errorString();
        }
        return false;
    }

    const QJsonDocument doc(json);
    if (file.write(doc.toJson(QJsonDocument::Indented)) == -1) {
        if (errorMessage) {
            *errorMessage = file.errorString();
        }
        file.cancelWriting();
        return false;
    }

    if (!file.commit()) {
        if (errorMessage) {
            *errorMessage = file.errorString();
        }
        return false;
    }

    return true;
}

bool writeJsonWithBackupAtomic(const QString &filePath, const QJsonObject &json, QString *errorMessage)
{
    if (!ensureParentDirExists(filePath, errorMessage)) {
        return false;
    }

    if (!backupExistingFile(filePath, errorMessage)) {
        return false;
    }

    return writeJsonAtomically(filePath, json, errorMessage);
}

} // namespace

GamepadConfigManager *GamepadConfigManager::m_instance = nullptr;

GamepadConfigManager::GamepadConfigManager(QObject *parent)
    : QObject(parent)
    , m_hotReloadEnabled(false)
    , m_fileWatcher(new QFileSystemWatcher(this))
    , m_deadzoneTrialTimer(new QTimer(this))
    , m_autoAssignPlayer(true)
    , m_defaultDeadzone(0.15f)
    , m_defaultSensitivity(1.0f)
    , m_vibrationEnabled(true)
    , m_keyboardMappingEnabled(false)
    , m_configDirOverride(qEnvironmentVariable("DECKSHELL_GAMEPAD_CONFIG_DIR").trimmed())
{
    connect(m_fileWatcher, &QFileSystemWatcher::fileChanged,
            this, &GamepadConfigManager::onFileChanged);

    if (m_deadzoneTrialTimer) {
        m_deadzoneTrialTimer->setSingleShot(true);
        connect(m_deadzoneTrialTimer, &QTimer::timeout, this, [this] {
            cancelDeadzoneTrial();
        });
    }

    // Try to load config from default path
    QString defaultPath = getDefaultConfigPath();
    if (QFile::exists(defaultPath)) {
        loadConfig(defaultPath);
    } else {
        // First run: load defaults and save to file (Stage 3.1)
        qInfo() << "First run detected, creating default gamepad config at:" << defaultPath;
        loadDefaultConfig();
        
        // Save default config to file
        if (saveConfig(defaultPath)) {
            qInfo() << "Default gamepad config file created successfully";
        } else {
            qWarning() << "Failed to create default gamepad config file";
        }
    }
}

QString GamepadConfigManager::configDir() const
{
    if (!m_configDirOverride.isEmpty()) {
        return m_configDirOverride;
    }
    return QStandardPaths::writableLocation(QStandardPaths::AppConfigLocation);
}

GamepadConfigManager::~GamepadConfigManager()
{
    m_instance = nullptr;
}

GamepadConfigManager* GamepadConfigManager::instance()
{
    if (!m_instance) {
        m_instance = new GamepadConfigManager();
    }
    return m_instance;
}

GamepadConfigManager* GamepadConfigManager::create(QQmlEngine *engine, QJSEngine *scriptEngine)
{
    Q_UNUSED(scriptEngine);

    auto *instance = GamepadConfigManager::instance();
    if (engine) {
        engine->setObjectOwnership(instance, QQmlEngine::CppOwnership);

        const QVariant injected = engine->rootContext()->contextProperty(QStringLiteral("_deckGamepadService"));
        auto *obj = injected.value<QObject *>();
        auto *svc = qobject_cast<DeckGamepadService *>(obj);
        if (svc) {
            instance->setService(svc);
        } else {
            // 统一走 QML 单例工厂：避免绕过注入契约导致 service 在不同入口被创建两次。
            GamepadManager *mgr = engine->singletonInstance<GamepadManager *>(QStringLiteral("DeckShell.DeckGamepad"),
                                                                              QStringLiteral("GamepadManager"));
            if (!mgr) {
                mgr = GamepadManager::create(engine, nullptr);
            }
            instance->setService(mgr ? mgr->service() : nullptr);
        }
    }
    return instance;
}

void GamepadConfigManager::setService(DeckGamepadService *service)
{
    if (m_service == service) {
        return;
    }

    if (m_service) {
        disconnect(m_service, nullptr, this, nullptr);
    }

    m_service = service;
    if (!m_service) {
        return;
    }

    connect(m_service, &DeckGamepadService::gamepadConnected,
            this, &GamepadConfigManager::onGamepadConnected);

    // 同步已连接设备（避免注入发生在 service 已启动之后时漏应用配置）
    const auto deviceIds = m_service->connectedGamepads();
    for (int deviceId : deviceIds) {
        applyDeviceConfig(deviceId);
    }
}

QString GamepadConfigManager::getDefaultConfigPath() const
{
    return QDir(configDir()).filePath("gamepad-config.json");
}

QString GamepadConfigManager::getDeviceKey(int deviceId) const
{
    if (deviceId < 0) {
        return QString();
    }

    if (!m_service)
        return QString::number(deviceId);

    const QString guid = m_service->deviceGuid(deviceId).trimmed();
    if (!guid.isEmpty()) {
        return guid;
    }

    const QString legacyKey = getLegacyDeviceKey(deviceId);
    if (!legacyKey.isEmpty()) {
        return legacyKey;
    }

    return QString::number(deviceId);
}

QString GamepadConfigManager::getLegacyDeviceKey(int deviceId) const
{
    if (!m_service)
        return QString();

    QString name = m_service->deviceName(deviceId);
    if (name.isEmpty()) {
        return QString();
    }

    return name.replace(' ', '_');
}

QString GamepadConfigManager::getDeviceKeyForRead(int deviceId) const
{
    const QString preferredKey = getDeviceKey(deviceId);
    if (preferredKey.isEmpty()) {
        return QString();
    }

    const QJsonObject devices = m_config["devices"].toObject();
    if (devices.contains(preferredKey)) {
        return preferredKey;
    }

    const QString legacyKey = getLegacyDeviceKey(deviceId);
    if (!legacyKey.isEmpty() && devices.contains(legacyKey)) {
        return legacyKey;
    }

    // Fall back to preferred key (caller will treat missing entry as defaults)
    return preferredKey;
}

bool GamepadConfigManager::loadConfig(const QString &filePath)
{
    const QString preferredPath = getDefaultConfigPath();
    const QString legacyPath =
        QDir(QStandardPaths::writableLocation(QStandardPaths::ConfigLocation))
            .filePath("DeckShell/gamepad-config.json");

    QString pathToLoad = filePath.isEmpty() ? m_configFilePath : filePath;
    if (pathToLoad.isEmpty()) {
        pathToLoad = preferredPath;
    }

    if (filePath.isEmpty() && m_configFilePath.isEmpty() && m_configDirOverride.isEmpty()
        && !QFile::exists(pathToLoad) && QFile::exists(legacyPath)) {
        qInfo() << "Loading gamepad config from legacy path:" << legacyPath;
        pathToLoad = legacyPath;
    }

    QFile file(pathToLoad);
    if (!file.open(QIODevice::ReadOnly)) {
        qWarning() << "Failed to open gamepad config file:" << pathToLoad;
        loadDefaultConfig();
        return false;
    }

    QByteArray data = file.readAll();
    file.close();

    QJsonDocument doc = QJsonDocument::fromJson(data);
    if (doc.isNull() || !doc.isObject()) {
        qWarning() << "Invalid gamepad config JSON:" << pathToLoad;
        loadDefaultConfig();
        return false;
    }

    if (!fromJson(doc.object())) {
        qWarning() << "Failed to parse gamepad config:" << pathToLoad;
        loadDefaultConfig();
        return false;
    }

    clearDeadzoneTrialState();

    m_configFilePath = filePath.isEmpty() ? preferredPath : pathToLoad;
    applyConfig();

    qInfo() << "Loaded gamepad config from:" << pathToLoad;
    Q_EMIT configLoaded();

    return true;
}

bool GamepadConfigManager::saveConfig(const QString &filePath)
{
    QString path = filePath.isEmpty() ? m_configFilePath : filePath;
    if (path.isEmpty()) {
        path = getDefaultConfigPath();
    }

    QString errorMessage;
    if (!writeJsonWithBackupAtomic(path, toJson(), &errorMessage)) {
        qWarning() << "Failed to save gamepad config file:" << path << errorMessage;
        return false;
    }

    m_configFilePath = path;
    qInfo() << "Saved gamepad config to:" << path;

    return true;
}

void GamepadConfigManager::loadDefaultConfig()
{
    // Embedded default config
    QJsonObject config;
    config["version"] = "1.0";

    QJsonObject global;
    global["autoAssignPlayer"] = true;
    global["defaultDeadzone"] = 0.15;
    global["defaultSensitivity"] = 1.0;
    global["enableVibration"] = true;
    config["global"] = global;

    QJsonObject shortcuts;
    QJsonObject guideButton;
    guideButton["enabled"] = true;
    
    QJsonArray combinations;
    QJsonObject comboA;
    comboA["button"] = "A";
    comboA["action"] = "showMultitaskView";
    combinations.append(comboA);
    
    QJsonObject comboB;
    comboB["button"] = "B";
    comboB["action"] = "showDesktop";
    combinations.append(comboB);
    
    guideButton["combinations"] = combinations;
    shortcuts["guideButton"] = guideButton;
    config["shortcuts"] = shortcuts;

    config["devices"] = QJsonObject();

    fromJson(config);

    clearDeadzoneTrialState();
    applyConfig();

    qInfo() << "Loaded default gamepad config";
}

void GamepadConfigManager::enableHotReload(bool enable)
{
    if (m_hotReloadEnabled == enable)
        return;

    m_hotReloadEnabled = enable;

    if (enable && !m_configFilePath.isEmpty()) {
        m_fileWatcher->addPath(m_configFilePath);
        qInfo() << "Enabled hot reload for gamepad config:" << m_configFilePath;
    } else {
        m_fileWatcher->removePath(m_configFilePath);
        qInfo() << "Disabled hot reload for gamepad config";
    }
}

void GamepadConfigManager::onFileChanged(const QString &path)
{
    if (path != m_configFilePath)
        return;

    qInfo() << "Gamepad config file changed, reloading...";

    // Re-add the watch (it's automatically removed after the file is modified)
    m_fileWatcher->addPath(m_configFilePath);

    // Reload configuration
    if (loadConfig(m_configFilePath)) {
        Q_EMIT hotReloadTriggered();
    }
}

void GamepadConfigManager::onGamepadConnected(int deviceId, const QString &name)
{
    Q_UNUSED(name);

    // Apply device-specific configuration if available
    applyDeviceConfig(deviceId);

    // Auto-assign player if enabled
    if (m_autoAssignPlayer && m_service) {
        int playerIndex = m_service->playerIndex(deviceId);
        if (playerIndex == -1) {
            m_service->assignPlayer(deviceId);
        }
    }
}

bool GamepadConfigManager::autoAssignPlayer() const
{
    return m_autoAssignPlayer;
}

void GamepadConfigManager::setAutoAssignPlayer(bool enable)
{
    if (m_autoAssignPlayer == enable)
        return;

    m_autoAssignPlayer = enable;

    QJsonObject global = m_config["global"].toObject();
    global["autoAssignPlayer"] = enable;
    m_config["global"] = global;

    Q_EMIT configChanged();
}

float GamepadConfigManager::defaultDeadzone() const
{
    if (m_deadzoneTrialHasGlobalDefault) {
        return m_deadzoneTrialGlobalDefault;
    }
    return m_defaultDeadzone;
}

void GamepadConfigManager::setDefaultDeadzone(float deadzone)
{
    if (qFuzzyCompare(m_defaultDeadzone, deadzone))
        return;

    m_defaultDeadzone = qBound(0.0f, deadzone, 1.0f);

    QJsonObject global = m_config["global"].toObject();
    global["defaultDeadzone"] = m_defaultDeadzone;
    m_config["global"] = global;

    Q_EMIT configChanged();
}

float GamepadConfigManager::defaultSensitivity() const
{
    return m_defaultSensitivity;
}

void GamepadConfigManager::setDefaultSensitivity(float sensitivity)
{
    if (qFuzzyCompare(m_defaultSensitivity, sensitivity))
        return;

    m_defaultSensitivity = qBound(0.1f, sensitivity, 5.0f);

    QJsonObject global = m_config["global"].toObject();
    global["defaultSensitivity"] = m_defaultSensitivity;
    m_config["global"] = global;

    Q_EMIT configChanged();
}

bool GamepadConfigManager::vibrationEnabled() const
{
    return m_vibrationEnabled;
}

void GamepadConfigManager::setVibrationEnabled(bool enabled)
{
    if (m_vibrationEnabled == enabled)
        return;

    m_vibrationEnabled = enabled;

    QJsonObject global = m_config["global"].toObject();
    global["enableVibration"] = enabled;
    m_config["global"] = global;

    if (!enabled && m_service) {
        const auto deviceIds = m_service->connectedGamepads();
        for (int deviceId : deviceIds) {
            m_service->stopVibration(deviceId);
        }
    }

    Q_EMIT configChanged();
}

bool GamepadConfigManager::startVibrationWithPolicy(int deviceId, float weak, float strong, int durationMs)
{
    if (!m_service) {
        return false;
    }

    if (!m_vibrationEnabled || !deviceVibrationEnabled(deviceId)) {
        return false;
    }

    return m_service->startVibration(deviceId, weak, strong, durationMs);
}

bool GamepadConfigManager::keyboardMappingEnabled() const
{
    return m_keyboardMappingEnabled;
}

void GamepadConfigManager::setKeyboardMappingEnabled(bool enabled)
{
    if (m_keyboardMappingEnabled == enabled)
        return;

    m_keyboardMappingEnabled = enabled;

    QJsonObject keyboardMapping = m_config["keyboard_mapping"].toObject();
    keyboardMapping["enabled"] = enabled;
    m_config["keyboard_mapping"] = keyboardMapping;

    Q_EMIT keyboardMappingEnabledChanged(enabled);
    Q_EMIT configChanged();
    
    // Auto-save configuration
    saveConfig();
}

float GamepadConfigManager::deviceDeadzone(int deviceId, uint32_t axis) const
{
    QString deviceKey = getDeviceKeyForRead(deviceId);
    if (deviceKey.isEmpty())
        return defaultDeadzone();

    const QString trialDeviceKey = getDeviceKey(deviceId);
    const auto deviceTrialIt = m_deadzoneTrialDeviceAxis.constFind(trialDeviceKey);
    if (deviceTrialIt != m_deadzoneTrialDeviceAxis.cend()) {
        const auto axisTrialIt = deviceTrialIt->constFind(axis);
        if (axisTrialIt != deviceTrialIt->cend()) {
            return axisTrialIt->value;
        }
    }

    QJsonObject devices = m_config["devices"].toObject();
    QJsonObject device = devices[deviceKey].toObject();
    QJsonObject deadzones = device["deadzone"].toObject();

    QString axisKey = QString::number(axis);
    if (deadzones.contains(axisKey)) {
        return deadzones[axisKey].toDouble(defaultDeadzone());
    }

    return defaultDeadzone();
}

void GamepadConfigManager::setDeviceDeadzone(int deviceId, uint32_t axis, float deadzone)
{
    deadzone = qBound(0.0f, deadzone, 1.0f);

    if (m_service) {
        m_service->setAxisDeadzone(deviceId, axis, deadzone);
    }
}

float GamepadConfigManager::persistedDeviceDeadzone(int deviceId, uint32_t axis) const
{
    QString deviceKey = getDeviceKeyForRead(deviceId);
    if (deviceKey.isEmpty()) {
        return m_defaultDeadzone;
    }

    const QJsonObject devices = m_config["devices"].toObject();
    const QJsonObject device = devices.value(deviceKey).toObject();
    const QJsonObject deadzones = device.value("deadzone").toObject();

    const QString axisKey = QString::number(axis);
    if (deadzones.contains(axisKey)) {
        return static_cast<float>(deadzones.value(axisKey).toDouble(m_defaultDeadzone));
    }

    return m_defaultDeadzone;
}

void GamepadConfigManager::clearDeadzoneTrialState()
{
    if (m_deadzoneTrialTimer) {
        m_deadzoneTrialTimer->stop();
    }

    m_deadzoneTrialHasGlobalDefault = false;
    m_deadzoneTrialDeviceAxis.clear();
}

void GamepadConfigManager::refreshDeadzoneTrialTimer(int ttlMs)
{
    if (!m_deadzoneTrialTimer) {
        return;
    }

    const int safeTtlMs = ttlMs > 0 ? ttlMs : kDefaultDeadzoneTrialTtlMs;
    m_deadzoneTrialTimer->start(safeTtlMs);
}

bool GamepadConfigManager::beginDeadzoneTrialGlobal(float deadzone, int ttlMs)
{
    deadzone = qBound(0.0f, deadzone, 1.0f);

    if (!hasDeadzoneTrial()) {
        m_deadzoneTrialBaselineGlobalDefault = m_defaultDeadzone;
    }

    m_deadzoneTrialHasGlobalDefault = true;
    m_deadzoneTrialGlobalDefault = deadzone;

    refreshDeadzoneTrialTimer(ttlMs);
    applyConfig();
    Q_EMIT configChanged();
    return true;
}

bool GamepadConfigManager::beginDeadzoneTrialDeviceAxis(int deviceId,
                                                        uint32_t axis,
                                                        float deadzone,
                                                        int ttlMs)
{
    deadzone = qBound(0.0f, deadzone, 1.0f);

    const QString deviceKey = getDeviceKey(deviceId);
    if (deviceKey.isEmpty()) {
        return false;
    }

    if (!hasDeadzoneTrial()) {
        m_deadzoneTrialBaselineGlobalDefault = m_defaultDeadzone;
    }

    auto &axisMap = m_deadzoneTrialDeviceAxis[deviceKey];
    auto it = axisMap.find(axis);
    if (it == axisMap.end()) {
        DeadzoneTrialAxisEntry entry;
        entry.baseline = persistedDeviceDeadzone(deviceId, axis);
        entry.value = deadzone;
        axisMap.insert(axis, entry);
    } else {
        it->value = deadzone;
    }

    refreshDeadzoneTrialTimer(ttlMs);

    if (m_service) {
        m_service->setAxisDeadzone(deviceId, axis, deadzone);
    }

    Q_EMIT configChanged();
    return true;
}

bool GamepadConfigManager::commitDeadzoneTrial()
{
    if (!hasDeadzoneTrial()) {
        return false;
    }

    const QJsonObject oldConfig = m_config;
    const float oldDefaultDeadzone = m_defaultDeadzone;

    QJsonObject newConfig = oldConfig;

    if (m_deadzoneTrialHasGlobalDefault) {
        QJsonObject global = newConfig.value("global").toObject();
        global["defaultDeadzone"] = m_deadzoneTrialGlobalDefault;
        newConfig["global"] = global;
    }

    if (!m_deadzoneTrialDeviceAxis.isEmpty()) {
        QJsonObject devices = newConfig.value("devices").toObject();
        for (auto deviceIt = m_deadzoneTrialDeviceAxis.cbegin();
             deviceIt != m_deadzoneTrialDeviceAxis.cend();
             ++deviceIt) {
            QJsonObject device = devices.value(deviceIt.key()).toObject();
            QJsonObject deadzones = device.value("deadzone").toObject();

            const auto &axes = deviceIt.value();
            for (auto axisIt = axes.cbegin(); axisIt != axes.cend(); ++axisIt) {
                deadzones[QString::number(axisIt.key())] = axisIt->value;
            }

            device["deadzone"] = deadzones;
            devices[deviceIt.key()] = device;
        }
        newConfig["devices"] = devices;
    }

    m_config = newConfig;
    if (m_deadzoneTrialHasGlobalDefault) {
        m_defaultDeadzone = m_deadzoneTrialGlobalDefault;
    }

    const bool saved = saveConfig();
    if (!saved) {
        m_config = oldConfig;
        m_defaultDeadzone = oldDefaultDeadzone;
        return false;
    }

    clearDeadzoneTrialState();
    applyConfig();
    Q_EMIT configChanged();
    return true;
}

bool GamepadConfigManager::cancelDeadzoneTrial()
{
    if (!hasDeadzoneTrial()) {
        return false;
    }

    clearDeadzoneTrialState();
    applyConfig();
    Q_EMIT configChanged();
    return true;
}

bool GamepadConfigManager::hasDeadzoneTrial() const
{
    return m_deadzoneTrialHasGlobalDefault || !m_deadzoneTrialDeviceAxis.isEmpty();
}

int GamepadConfigManager::deadzoneTrialRemainingMs() const
{
    if (!hasDeadzoneTrial() || !m_deadzoneTrialTimer) {
        return 0;
    }
    return qMax(0, m_deadzoneTrialTimer->remainingTime());
}

float GamepadConfigManager::deviceSensitivity(int deviceId, uint32_t axis) const
{
    QString deviceKey = getDeviceKeyForRead(deviceId);
    if (deviceKey.isEmpty())
        return m_defaultSensitivity;

    QJsonObject devices = m_config["devices"].toObject();
    QJsonObject device = devices[deviceKey].toObject();
    QJsonObject sensitivities = device["sensitivity"].toObject();

    QString axisKey = QString::number(axis);
    if (sensitivities.contains(axisKey)) {
        return sensitivities[axisKey].toDouble(m_defaultSensitivity);
    }

    return m_defaultSensitivity;
}

void GamepadConfigManager::setDeviceSensitivity(int deviceId, uint32_t axis, float sensitivity)
{
    QString deviceKey = getDeviceKey(deviceId);
    if (deviceKey.isEmpty())
        return;

    sensitivity = qBound(0.1f, sensitivity, 5.0f);

    QJsonObject devices = m_config["devices"].toObject();
    QJsonObject device = devices[deviceKey].toObject();
    QJsonObject sensitivities = device["sensitivity"].toObject();

    QString axisKey = QString::number(axis);
    sensitivities[axisKey] = sensitivity;
    device["sensitivity"] = sensitivities;
    devices[deviceKey] = device;
    m_config["devices"] = devices;

    if (m_service) {
        m_service->setAxisSensitivity(deviceId, axis, sensitivity);
    }

    Q_EMIT configChanged();
}

bool GamepadConfigManager::deviceVibrationEnabled(int deviceId) const
{
    QString deviceKey = getDeviceKeyForRead(deviceId);
    if (deviceKey.isEmpty())
        return m_vibrationEnabled;

    QJsonObject devices = m_config["devices"].toObject();
    QJsonObject device = devices[deviceKey].toObject();
    QJsonObject vibration = device["vibration"].toObject();

    return vibration.value("enabled").toBool(m_vibrationEnabled);
}

void GamepadConfigManager::setDeviceVibrationEnabled(int deviceId, bool enabled)
{
    QString deviceKey = getDeviceKey(deviceId);
    if (deviceKey.isEmpty())
        return;

    QJsonObject devices = m_config["devices"].toObject();
    QJsonObject device = devices[deviceKey].toObject();
    QJsonObject vibration = device["vibration"].toObject();

    vibration["enabled"] = enabled;
    device["vibration"] = vibration;
    devices[deviceKey] = device;
    m_config["devices"] = devices;

    if (!enabled && m_service) {
        m_service->stopVibration(deviceId);
    }

    Q_EMIT configChanged();
}

void GamepadConfigManager::applyConfig()
{
    if (!m_service)
        return;

    // Apply global defaults to all connected devices
    auto deviceIds = m_service->connectedGamepads();
    for (int deviceId : deviceIds) {
        applyDeviceConfig(deviceId);
    }

    qInfo() << "Applied gamepad configuration to" << deviceIds.count() << "device(s)";
}

void GamepadConfigManager::applyDeviceConfig(int deviceId)
{
    if (!m_service)
        return;

    // For now, apply default deadzone and sensitivity to all axes
    // In the future, this could be more sophisticated with per-axis config
    const int NUM_AXES = 6;  // Typical gamepad has 6 axes (LX, LY, RX, RY, LT, RT)

    for (int axis = 0; axis < NUM_AXES; ++axis) {
        float deadzone = deviceDeadzone(deviceId, axis);
        float sensitivity = deviceSensitivity(deviceId, axis);

        m_service->setAxisDeadzone(deviceId, axis, deadzone);
        m_service->setAxisSensitivity(deviceId, axis, sensitivity);
    }

    qDebug() << "Applied config for gamepad" << deviceId
                           << "deadzone:" << m_defaultDeadzone
                           << "sensitivity:" << m_defaultSensitivity;
}

QJsonObject GamepadConfigManager::toJson() const
{
    return m_config;
}

bool GamepadConfigManager::fromJson(const QJsonObject &json)
{
    m_config = json;

    // Parse global settings
    QJsonObject global = json["global"].toObject();
    m_autoAssignPlayer = global.value("autoAssignPlayer").toBool(true);
    m_defaultDeadzone = global.value("defaultDeadzone").toDouble(0.15);
    m_defaultSensitivity = global.value("defaultSensitivity").toDouble(1.0);
    m_vibrationEnabled = global.value("enableVibration").toBool(true);

    // Parse keyboard mapping settings
    if (json.contains("keyboard_mapping")) {
        QJsonObject keyboardMapping = json["keyboard_mapping"].toObject();
        m_keyboardMappingEnabled = keyboardMapping.value("enabled").toBool(false);
        m_currentProfile = keyboardMapping.value("current_profile").toString("default");
    } else {
        m_keyboardMappingEnabled = false;  // Default
        m_currentProfile = "default";
    }

    return true;
}

// ========== Profile Management Implementation ==========

QStringList GamepadConfigManager::listProfiles() const
{
    QStringList profiles;

    const auto collectFromDir = [&profiles](const QString &dirPath) {
        QDir dir(dirPath);
        if (!dir.exists()) {
            return;
        }
        QFileInfoList files = dir.entryInfoList({"*.json"}, QDir::Files);
        for (const QFileInfo &info : files) {
            profiles << info.baseName();
        }
    };

    collectFromDir(getProfilesDir());
    if (m_configDirOverride.isEmpty()) {
        collectFromDir(getLegacyProfilesDir());
    }

    profiles.removeDuplicates();
    profiles.sort(Qt::CaseInsensitive);

    if (!profiles.contains("default")) {
        profiles.prepend("default");
    }

    return profiles;
}

QString GamepadConfigManager::currentProfile() const
{
    return m_currentProfile.isEmpty() ? "default" : m_currentProfile;
}

bool GamepadConfigManager::createProfile(const QString &name, const QString &description)
{
    if (name.isEmpty()) {
        qWarning() << "Cannot create profile with empty name";
        return false;
    }
    
    // Check if profile already exists
    if (!resolveExistingProfilePath(name).isEmpty()) {
        qWarning() << "Profile already exists:" << name;
        return false;
    }
    
    // Create new profile
    KeyboardMappingProfile profile(name);
    profile.description = description;
    profile.createdAt = QDateTime::currentDateTime();
    profile.modifiedAt = profile.createdAt;
    
    if (!saveProfile(profile)) {
        return false;
    }
    
    qInfo() << "Created keyboard mapping profile:" << name;
    emit profileListChanged();
    return true;
}

bool GamepadConfigManager::switchProfile(const QString &name)
{
    if (m_currentProfile == name) {
        return true;  // Already on this profile
    }
    
    // Verify profile exists
    if (name != "default" && resolveExistingProfilePath(name).isEmpty()) {
        qWarning() << "Profile not found:" << name;
        return false;
    }
    
    QString oldProfile = m_currentProfile;
    m_currentProfile = name;
    
    // Update main config
    QJsonObject km = m_config["keyboard_mapping"].toObject();
    km["current_profile"] = name;
    m_config["keyboard_mapping"] = km;
    
    if (!saveConfig()) {
        // Rollback on failure
        m_currentProfile = oldProfile;
        return false;
    }
    
    qInfo() << "Switched keyboard mapping profile from" << oldProfile << "to" << name;
    emit currentProfileChanged(name);
    return true;
}

bool GamepadConfigManager::deleteProfile(const QString &name)
{
    // Cannot delete default profile
    if (name == "default") {
        qWarning() << "Cannot delete default profile";
        return false;
    }
    
    // Cannot delete current profile
    if (name == m_currentProfile) {
        qWarning() << "Cannot delete current profile. Switch to another profile first.";
        return false;
    }
    
    const QString preferredPath = getProfilePath(name);
    const QString legacyPath = getLegacyProfilePath(name);

    bool removedAny = false;

    if (QFile::exists(preferredPath)) {
        removedAny = true;
        if (!QFile::remove(preferredPath)) {
            qWarning() << "Failed to delete profile file:" << preferredPath;
            return false;
        }
    }

    if (m_configDirOverride.isEmpty() && QFile::exists(legacyPath)) {
        removedAny = true;
        if (!QFile::remove(legacyPath)) {
            qWarning() << "Failed to delete legacy profile file:" << legacyPath;
            return false;
        }
    }

    if (!removedAny) {
        qWarning() << "Profile not found:" << name;
        return false;
    }
    
    // Remove from cache
    m_profileCache.remove(name);
    
    qInfo() << "Deleted keyboard mapping profile:" << name;
    emit profileListChanged();
    return true;
}

bool GamepadConfigManager::renameProfile(const QString &oldName, const QString &newName)
{
    if (oldName.isEmpty() || newName.isEmpty()) {
        qWarning() << "Cannot rename with empty name";
        return false;
    }
    
    if (oldName == "default") {
        qWarning() << "Cannot rename default profile";
        return false;
    }
    
    const QString oldPreferredPath = getProfilePath(oldName);
    const QString oldLegacyPath = getLegacyProfilePath(oldName);
    const QString newPreferredPath = getProfilePath(newName);
    const QString newLegacyPath = getLegacyProfilePath(newName);

    const bool hasPreferredOld = QFile::exists(oldPreferredPath);
    const bool hasLegacyOld = m_configDirOverride.isEmpty() && QFile::exists(oldLegacyPath);
    if (!hasPreferredOld && !hasLegacyOld) {
        qWarning() << "Profile not found:" << oldName;
        return false;
    }

    if (QFile::exists(newPreferredPath) || (m_configDirOverride.isEmpty() && QFile::exists(newLegacyPath))) {
        qWarning() << "Profile already exists:" << newName;
        return false;
    }
    
    // Load profile and update name
    KeyboardMappingProfile profile = getProfile(oldName);
    if (!profile.isValid()) {
        return false;
    }
    
    profile.name = newName;
    profile.modifiedAt = QDateTime::currentDateTime();
    
    // Save with new name and delete old
    if (!saveProfile(profile)) {
        return false;
    }

    if (hasPreferredOld) {
        QFile::remove(oldPreferredPath);
    }
    if (hasLegacyOld) {
        QFile::remove(oldLegacyPath);
    }
    m_profileCache.remove(oldName);
    
    // Update current profile if needed
    if (m_currentProfile == oldName) {
        m_currentProfile = newName;
        QJsonObject km = m_config["keyboard_mapping"].toObject();
        km["current_profile"] = newName;
        m_config["keyboard_mapping"] = km;
        saveConfig();
        emit currentProfileChanged(newName);
    }
    
    qInfo() << "Renamed profile from" << oldName << "to" << newName;
    emit profileListChanged();
    return true;
}

KeyboardMappingProfile GamepadConfigManager::getProfile(const QString &name) const
{
    // Check cache first
    if (m_profileCache.contains(name)) {
        return m_profileCache[name];
    }
    
    // Load from file
    const QString profilePath = resolveExistingProfilePath(name);
    if (profilePath.isEmpty()) {
        if (name == "default") {
            KeyboardMappingProfile profile("default");
            const_cast<GamepadConfigManager*>(this)->m_profileCache[name] = profile;
            return profile;
        }

        qWarning() << "Profile not found:" << name;
        return KeyboardMappingProfile();
    }
    
    QFile file(profilePath);
    if (!file.open(QIODevice::ReadOnly)) {
        qWarning() << "Failed to open profile:" << profilePath;
        return KeyboardMappingProfile();
    }
    
    QJsonDocument doc = QJsonDocument::fromJson(file.readAll());
    KeyboardMappingProfile profile = KeyboardMappingProfile::fromJson(doc.object());
    
    // Cache it
    const_cast<GamepadConfigManager*>(this)->m_profileCache[name] = profile;
    
    return profile;
}

bool GamepadConfigManager::saveProfile(const KeyboardMappingProfile &profile)
{
    if (!profile.isValid()) {
        qWarning() << "Cannot save invalid profile";
        return false;
    }
    
    QString profilePath = resolveProfilePathForWrite(profile.name);
    if (profilePath.isEmpty()) {
        qWarning() << "Failed to resolve profile path for write:" << profile.name;
        return false;
    }

    // Update modified time
    KeyboardMappingProfile updatedProfile = profile;
    updatedProfile.modifiedAt = QDateTime::currentDateTime();
    
    QString errorMessage;
    if (!writeJsonWithBackupAtomic(profilePath, updatedProfile.toJson(), &errorMessage)) {
        qWarning() << "Failed to save profile:" << profilePath << errorMessage;
        return false;
    }
    
    // Update cache
    m_profileCache[profile.name] = updatedProfile;
    
    qInfo() << "Saved keyboard mapping profile:" << profile.name;
    return true;
}

bool GamepadConfigManager::exportProfile(const QString &name, const QString &filePath)
{
    KeyboardMappingProfile profile = getProfile(name);
    if (!profile.isValid()) {
        qWarning() << "Cannot export invalid profile:" << name;
        return false;
    }
    
    QFile file(filePath);
    if (!file.open(QIODevice::WriteOnly)) {
        qWarning() << "Failed to open export file:" << filePath;
        return false;
    }
    
    QJsonDocument doc(profile.toJson());
    file.write(doc.toJson(QJsonDocument::Indented));
    
    qInfo() << "Exported profile" << name << "to" << filePath;
    return true;
}

bool GamepadConfigManager::importProfile(const QString &filePath)
{
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly)) {
        qWarning() << "Failed to open import file:" << filePath;
        return false;
    }
    
    QJsonDocument doc = QJsonDocument::fromJson(file.readAll());
    KeyboardMappingProfile profile = KeyboardMappingProfile::fromJson(doc.object());
    
    if (!profile.isValid()) {
        qWarning() << "Invalid profile format:" << filePath;
        return false;
    }
    
    // Check for name conflicts
    QStringList existing = listProfiles();
    if (existing.contains(profile.name)) {
        // Auto-rename
        int i = 1;
        QString newName;
        do {
            newName = QString("%1 (%2)").arg(profile.name).arg(i++);
        } while (existing.contains(newName));
        
        qInfo() << "Renamed imported profile from" << profile.name << "to" << newName;
        profile.name = newName;
    }
    
    if (!saveProfile(profile)) {
        return false;
    }
    
    qInfo() << "Imported profile:" << profile.name << "from" << filePath;
    emit profileListChanged();
    return true;
}

void GamepadConfigManager::applyProfileToManager(const QString &name, DeckGamepadKeyboardMappingManager *manager)
{
    if (!manager) {
        qWarning() << "Cannot apply profile to null manager";
        return;
    }
    
    KeyboardMappingProfile profile = getProfile(name);
    if (!profile.isValid()) {
        qWarning() << "Cannot apply invalid profile:" << name;
        return;
    }
    
    profile.applyTo(manager);
    qInfo() << "Applied keyboard mapping profile" << name << "to manager";
}

// ========== Profile Management Helpers ==========

QString GamepadConfigManager::getProfilesDir() const
{
    return QDir(configDir()).filePath("profiles");
}

QString GamepadConfigManager::getLegacyProfilesDir() const
{
    return QDir(QStandardPaths::writableLocation(QStandardPaths::ConfigLocation))
        .filePath("DeckShell/profiles");
}

QString GamepadConfigManager::getProfilePath(const QString &name) const
{
    return QDir(getProfilesDir()).filePath(name + ".json");
}

QString GamepadConfigManager::getLegacyProfilePath(const QString &name) const
{
    return QDir(getLegacyProfilesDir()).filePath(name + ".json");
}

QString GamepadConfigManager::resolveExistingProfilePath(const QString &name) const
{
    const QString preferredPath = getProfilePath(name);
    if (QFile::exists(preferredPath)) {
        return preferredPath;
    }

    if (m_configDirOverride.isEmpty()) {
        const QString legacyPath = getLegacyProfilePath(name);
        if (QFile::exists(legacyPath)) {
            return legacyPath;
        }
    }

    return {};
}

QString GamepadConfigManager::resolveProfilePathForWrite(const QString &name) const
{
    const QString preferredPath = getProfilePath(name);
    if (QFile::exists(preferredPath)) {
        return preferredPath;
    }

    if (m_configDirOverride.isEmpty()) {
        const QString legacyPath = getLegacyProfilePath(name);
        if (QFile::exists(legacyPath)) {
            return legacyPath;
        }
    }

    return preferredPath;
}

bool GamepadConfigManager::loadProfile(const QString &name)
{
    KeyboardMappingProfile profile = getProfile(name);
    if (!profile.isValid()) {
        return false;
    }
    
    // Profile is now in cache
    return true;
}

void GamepadConfigManager::ensureProfilesDir()
{
    QString profilesDir = getProfilesDir();
    QDir dir;
    if (!dir.exists(profilesDir)) {
        if (dir.mkpath(profilesDir)) {
            qInfo() << "Created profiles directory:" << profilesDir;
        } else {
            qWarning() << "Failed to create profiles directory:" << profilesDir;
        }
    }
}
