// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <deckshell/deckgamepad/backend/deckgamepadbackend.h>
#include <deckshell/deckgamepad/mapping/deckgamepadcustommappingmanager.h>
#include <deckshell/deckgamepad/mapping/deckgamepadsdlcontrollerdb.h>

#include "deckgamepadsdlmappingutils_p.h"

#include <QtCore/QDebug>
#include <QtCore/QFile>
#include <QtCore/QDir>
#include <QtCore/QMetaObject>
#include <QtCore/QStandardPaths>
#include <QtCore/QTextStream>
#include <QtCore/QThread>

extern "C" {
#include <linux/input.h>
}

DECKGAMEPAD_BEGIN_NAMESPACE

// ============================================================================
// DeckGamepadCustomMappingManager Implementation
// ============================================================================

DeckGamepadCustomMappingManager::DeckGamepadCustomMappingManager(DeckGamepadBackend *backend, QObject *parent)
    : QObject(parent)
    , m_backend(backend)
    , m_sdlDb(backend ? backend->sdlDb() : nullptr)
{
    // Set default config path
    const QString configDir = QStandardPaths::writableLocation(QStandardPaths::AppConfigLocation);
    m_configPath = QDir(configDir).filePath("custom_gamepad_mappings.txt");
    
    // Initialize preset templates
    initializePresets();

    qDebug() << "DeckGamepadCustomMappingManager initialized, default config path:" << m_configPath;
}

DeckGamepadCustomMappingManager::~DeckGamepadCustomMappingManager()
{
}

// ========== Mapping CRUD ==========

QString DeckGamepadCustomMappingManager::createCustomMapping(int deviceId)
{
    QString guid = getDeviceGuid(deviceId);
    if (guid.isEmpty()) {
        qWarning() << "Cannot create mapping: invalid device ID" << deviceId;
        return QString();
    }
    
    const QString deviceName = getDeviceName(deviceId);

    DeviceMapping mapping;
    mapping.guid = guid;
    mapping.name = deviceName;

    QHash<int, int> physicalButtons;
    QHash<int, int> physicalAxes;

    // Try to load SDL DB default mapping as starting point
    if (m_backend && m_sdlDb) {
        DeviceMapping sdlMapping;
        auto loadFromSdlDb = [&] {
            auto *device = m_backend->device(deviceId);
            if (!device) {
                return;
            }

            physicalButtons = device->physicalButtonMap();
            physicalAxes = device->physicalAxisMap();

            if (m_sdlDb->hasMapping(guid)) {
                sdlMapping = m_sdlDb->createDeviceMapping(guid, physicalButtons, physicalAxes);
            }
        };

        if (QThread::currentThread() == m_backend->thread()) {
            loadFromSdlDb();
        } else {
            QMetaObject::invokeMethod(m_backend, loadFromSdlDb, Qt::BlockingQueuedConnection);
        }

        if (!sdlMapping.isEmpty()) {
            mapping = std::move(sdlMapping);
            mapping.guid = guid;
            mapping.name = deviceName;
            qDebug() << "Created custom mapping from SDL DB for" << mapping.name;
        }
    }
    
    // If no SDL mapping, use generic template
    if (mapping.isEmpty()) {
        mapping = createGenericMapping();
        mapping.guid = guid;
        mapping.name = deviceName;
        qDebug() << "Created generic mapping for" << mapping.name;
    }

    StoredCustomMapping stored;
    stored.cachedEvdevMapping = mapping;
    stored.sdlString = deckGamepadComposeSdlMappingString(mapping, physicalButtons, physicalAxes);
    m_customMappings[guid] = stored;
    emit mappingCreated(guid);
    
    return guid;
}

bool DeckGamepadCustomMappingManager::hasCustomMapping(int deviceId) const
{
    QString guid = getDeviceGuid(deviceId);
    return hasCustomMapping(guid);
}

bool DeckGamepadCustomMappingManager::hasCustomMapping(const QString &guid) const
{
    return m_customMappings.contains(guid);
}

DeviceMapping DeckGamepadCustomMappingManager::getCustomMapping(int deviceId) const
{
    QString guid = getDeviceGuid(deviceId);
    if (guid.isEmpty()) {
        return {};
    }

    const auto it = m_customMappings.constFind(guid);
    if (it == m_customMappings.constEnd()) {
        return {};
    }

    const StoredCustomMapping &stored = it.value();
    if (!stored.cachedEvdevMapping.isEmpty()) {
        return stored.cachedEvdevMapping;
    }

    if (!m_backend || stored.sdlString.isEmpty()) {
        return {};
    }

    QHash<int, int> physicalButtons;
    QHash<int, int> physicalAxes;
    auto collectPhysicalMaps = [&] {
        auto *device = m_backend->device(deviceId);
        if (!device) {
            return;
        }
        physicalButtons = device->physicalButtonMap();
        physicalAxes = device->physicalAxisMap();
    };

    if (QThread::currentThread() == m_backend->thread()) {
        collectPhysicalMaps();
    } else {
        QMetaObject::invokeMethod(m_backend, collectPhysicalMaps, Qt::BlockingQueuedConnection);
    }

    DeviceMapping parsed = deckGamepadParseSdlMappingString(stored.sdlString, physicalButtons, physicalAxes);
    if (parsed.isEmpty()) {
        return {};
    }

    parsed.guid = guid;
    parsed.name = getDeviceName(deviceId);
    return parsed;
}

DeviceMapping DeckGamepadCustomMappingManager::getCustomMapping(const QString &guid) const
{
    const auto it = m_customMappings.constFind(guid);
    if (it == m_customMappings.constEnd()) {
        return {};
    }
    return it.value().cachedEvdevMapping;
}

void DeckGamepadCustomMappingManager::removeCustomMapping(int deviceId)
{
    QString guid = getDeviceGuid(deviceId);
    removeCustomMapping(guid);
}

void DeckGamepadCustomMappingManager::removeCustomMapping(const QString &guid)
{
    if (m_customMappings.remove(guid) > 0) {
        emit mappingRemoved(guid);
        qDebug() << "Removed custom mapping for GUID:" << guid;
    }
}

// ========== Mapping Editing ==========

void DeckGamepadCustomMappingManager::setButtonMapping(int deviceId, GamepadButton logicalButton, int physicalCode)
{
    QString guid = getDeviceGuid(deviceId);
    if (guid.isEmpty() || !m_customMappings.contains(guid)) {
        qWarning() << "Cannot set button mapping: no custom mapping for device" << deviceId;
        return;
    }

    QHash<int, int> physicalButtons;
    QHash<int, int> physicalAxes;
    if (m_backend) {
        auto collectPhysicalMaps = [&] {
            auto *device = m_backend->device(deviceId);
            if (!device) {
                return;
            }
            physicalButtons = device->physicalButtonMap();
            physicalAxes = device->physicalAxisMap();
        };

        if (QThread::currentThread() == m_backend->thread()) {
            collectPhysicalMaps();
        } else {
            QMetaObject::invokeMethod(m_backend, collectPhysicalMaps, Qt::BlockingQueuedConnection);
        }
    }

    StoredCustomMapping &stored = m_customMappings[guid];
    if (stored.cachedEvdevMapping.isEmpty() && !stored.sdlString.isEmpty()) {
        DeviceMapping parsed = deckGamepadParseSdlMappingString(stored.sdlString, physicalButtons, physicalAxes);
        if (parsed.isEmpty()) {
            qWarning() << "Cannot set button mapping: failed to parse stored SDL mapping for device" << deviceId;
            return;
        }
        parsed.guid = guid;
        parsed.name = getDeviceName(deviceId);
        stored.cachedEvdevMapping = parsed;
    }

    DeviceMapping &mapping = stored.cachedEvdevMapping;
    mapping.buttonMap[physicalCode] = logicalButton;
    stored.sdlString = deckGamepadComposeSdlMappingString(mapping, physicalButtons, physicalAxes);

    emit mappingChanged(guid);
    qDebug() << "Set button mapping:" << logicalButton << "->" << physicalCode;
}

void DeckGamepadCustomMappingManager::setAxisMapping(int deviceId, GamepadAxis logicalAxis, int physicalCode, bool inverted)
{
    QString guid = getDeviceGuid(deviceId);
    if (guid.isEmpty() || !m_customMappings.contains(guid)) {
        qWarning() << "Cannot set axis mapping: no custom mapping for device" << deviceId;
        return;
    }

    QHash<int, int> physicalButtons;
    QHash<int, int> physicalAxes;
    if (m_backend) {
        auto collectPhysicalMaps = [&] {
            auto *device = m_backend->device(deviceId);
            if (!device) {
                return;
            }
            physicalButtons = device->physicalButtonMap();
            physicalAxes = device->physicalAxisMap();
        };

        if (QThread::currentThread() == m_backend->thread()) {
            collectPhysicalMaps();
        } else {
            QMetaObject::invokeMethod(m_backend, collectPhysicalMaps, Qt::BlockingQueuedConnection);
        }
    }

    StoredCustomMapping &stored = m_customMappings[guid];
    if (stored.cachedEvdevMapping.isEmpty() && !stored.sdlString.isEmpty()) {
        DeviceMapping parsed = deckGamepadParseSdlMappingString(stored.sdlString, physicalButtons, physicalAxes);
        if (parsed.isEmpty()) {
            qWarning() << "Cannot set axis mapping: failed to parse stored SDL mapping for device" << deviceId;
            return;
        }
        parsed.guid = guid;
        parsed.name = getDeviceName(deviceId);
        stored.cachedEvdevMapping = parsed;
    }

    DeviceMapping &mapping = stored.cachedEvdevMapping;
    mapping.axisMap[physicalCode] = logicalAxis;

    if (inverted) {
        mapping.invertedAxes.insert(physicalCode);
    } else {
        mapping.invertedAxes.remove(physicalCode);
    }

    stored.sdlString = deckGamepadComposeSdlMappingString(mapping, physicalButtons, physicalAxes);

    emit mappingChanged(guid);
    qDebug() << "Set axis mapping:" << logicalAxis << "->" << physicalCode << "inverted:" << inverted;
}

void DeckGamepadCustomMappingManager::setHatMapping(int deviceId, GamepadButton logicalButton, int hatCode, int hatMask)
{
    QString guid = getDeviceGuid(deviceId);
    if (guid.isEmpty() || !m_customMappings.contains(guid)) {
        qWarning() << "Cannot set HAT mapping: no custom mapping for device" << deviceId;
        return;
    }

    QHash<int, int> physicalButtons;
    QHash<int, int> physicalAxes;
    if (m_backend) {
        auto collectPhysicalMaps = [&] {
            auto *device = m_backend->device(deviceId);
            if (!device) {
                return;
            }
            physicalButtons = device->physicalButtonMap();
            physicalAxes = device->physicalAxisMap();
        };

        if (QThread::currentThread() == m_backend->thread()) {
            collectPhysicalMaps();
        } else {
            QMetaObject::invokeMethod(m_backend, collectPhysicalMaps, Qt::BlockingQueuedConnection);
        }
    }

    StoredCustomMapping &stored = m_customMappings[guid];
    if (stored.cachedEvdevMapping.isEmpty() && !stored.sdlString.isEmpty()) {
        DeviceMapping parsed = deckGamepadParseSdlMappingString(stored.sdlString, physicalButtons, physicalAxes);
        if (parsed.isEmpty()) {
            qWarning() << "Cannot set hat mapping: failed to parse stored SDL mapping for device" << deviceId;
            return;
        }
        parsed.guid = guid;
        parsed.name = getDeviceName(deviceId);
        stored.cachedEvdevMapping = parsed;
    }

    DeviceMapping &mapping = stored.cachedEvdevMapping;

    // HAT mapping: store in hatButtonMap with combined key (hatCode << 8 | hatMask)
    int hatKey = (hatCode << 8) | hatMask;
    mapping.hatButtonMap[hatKey] = logicalButton;

    stored.sdlString = deckGamepadComposeSdlMappingString(mapping, physicalButtons, physicalAxes);

    emit mappingChanged(guid);
    qDebug() << "Set HAT mapping:" << logicalButton << "-> HAT" << hatCode << "mask" << hatMask;
}

void DeckGamepadCustomMappingManager::clearButtonMapping(int deviceId, GamepadButton logicalButton)
{
    QString guid = getDeviceGuid(deviceId);
    if (guid.isEmpty() || !m_customMappings.contains(guid)) {
        return;
    }

    QHash<int, int> physicalButtons;
    QHash<int, int> physicalAxes;
    if (m_backend) {
        auto collectPhysicalMaps = [&] {
            auto *device = m_backend->device(deviceId);
            if (!device) {
                return;
            }
            physicalButtons = device->physicalButtonMap();
            physicalAxes = device->physicalAxisMap();
        };

        if (QThread::currentThread() == m_backend->thread()) {
            collectPhysicalMaps();
        } else {
            QMetaObject::invokeMethod(m_backend, collectPhysicalMaps, Qt::BlockingQueuedConnection);
        }
    }

    StoredCustomMapping &stored = m_customMappings[guid];
    if (stored.cachedEvdevMapping.isEmpty() && !stored.sdlString.isEmpty()) {
        DeviceMapping parsed = deckGamepadParseSdlMappingString(stored.sdlString, physicalButtons, physicalAxes);
        if (!parsed.isEmpty()) {
            parsed.guid = guid;
            parsed.name = getDeviceName(deviceId);
            stored.cachedEvdevMapping = parsed;
        }
    }

    DeviceMapping &mapping = stored.cachedEvdevMapping;

    // Find and remove the mapping
    for (auto it = mapping.buttonMap.begin(); it != mapping.buttonMap.end(); ) {
        if (it.value() == logicalButton) {
            it = mapping.buttonMap.erase(it);
        } else {
            ++it;
        }
    }

    stored.sdlString = deckGamepadComposeSdlMappingString(mapping, physicalButtons, physicalAxes);
    emit mappingChanged(guid);
}

void DeckGamepadCustomMappingManager::clearAxisMapping(int deviceId, GamepadAxis logicalAxis)
{
    QString guid = getDeviceGuid(deviceId);
    if (guid.isEmpty() || !m_customMappings.contains(guid)) {
        return;
    }

    QHash<int, int> physicalButtons;
    QHash<int, int> physicalAxes;
    if (m_backend) {
        auto collectPhysicalMaps = [&] {
            auto *device = m_backend->device(deviceId);
            if (!device) {
                return;
            }
            physicalButtons = device->physicalButtonMap();
            physicalAxes = device->physicalAxisMap();
        };

        if (QThread::currentThread() == m_backend->thread()) {
            collectPhysicalMaps();
        } else {
            QMetaObject::invokeMethod(m_backend, collectPhysicalMaps, Qt::BlockingQueuedConnection);
        }
    }

    StoredCustomMapping &stored = m_customMappings[guid];
    if (stored.cachedEvdevMapping.isEmpty() && !stored.sdlString.isEmpty()) {
        DeviceMapping parsed = deckGamepadParseSdlMappingString(stored.sdlString, physicalButtons, physicalAxes);
        if (!parsed.isEmpty()) {
            parsed.guid = guid;
            parsed.name = getDeviceName(deviceId);
            stored.cachedEvdevMapping = parsed;
        }
    }

    DeviceMapping &mapping = stored.cachedEvdevMapping;

    // Find and remove the mapping
    for (auto it = mapping.axisMap.begin(); it != mapping.axisMap.end(); ) {
        if (it.value() == logicalAxis) {
            int code = it.key();
            it = mapping.axisMap.erase(it);
            mapping.invertedAxes.remove(code);
        } else {
            ++it;
        }
    }

    stored.sdlString = deckGamepadComposeSdlMappingString(mapping, physicalButtons, physicalAxes);
    emit mappingChanged(guid);
}

// ========== Preset Templates ==========

bool DeckGamepadCustomMappingManager::loadPreset(int deviceId, const QString &presetName)
{
    if (!m_presetTemplates.contains(presetName)) {
        qWarning() << "Unknown preset:" << presetName;
        return false;
    }
    
    QString guid = getDeviceGuid(deviceId);
    if (guid.isEmpty()) {
        return false;
    }

    const QString deviceName = getDeviceName(deviceId);

    QHash<int, int> physicalButtons;
    QHash<int, int> physicalAxes;
    if (m_backend) {
        auto collectPhysicalMaps = [&] {
            auto *device = m_backend->device(deviceId);
            if (!device) {
                return;
            }
            physicalButtons = device->physicalButtonMap();
            physicalAxes = device->physicalAxisMap();
        };

        if (QThread::currentThread() == m_backend->thread()) {
            collectPhysicalMaps();
        } else {
            QMetaObject::invokeMethod(m_backend, collectPhysicalMaps, Qt::BlockingQueuedConnection);
        }
    }

    const QString rawPreset = m_presetTemplates[presetName];
    QStringList parts = rawPreset.split(QLatin1Char(','), Qt::KeepEmptyParts);
    if (parts.size() < 3) {
        qWarning() << "Failed to parse preset (invalid SDL mapping string):" << presetName;
        return false;
    }

    parts[0] = guid;
    parts[1] = deviceName;
    const QString normalizedSdlString = parts.join(QLatin1Char(','));

    DeviceMapping mapping = deckGamepadParseSdlMappingString(normalizedSdlString, physicalButtons, physicalAxes);
    if (mapping.isEmpty()) {
        qWarning() << "Failed to parse preset:" << presetName;
        return false;
    }

    mapping.guid = guid;
    mapping.name = deviceName;

    StoredCustomMapping stored;
    stored.cachedEvdevMapping = mapping;
    stored.sdlString = deckGamepadComposeSdlMappingString(mapping, physicalButtons, physicalAxes);
    m_customMappings[guid] = stored;
    emit mappingChanged(guid);
    
    qDebug() << "Loaded preset" << presetName << "for device" << deviceId;
    return true;
}

QStringList DeckGamepadCustomMappingManager::availablePresets() const
{
    return m_presetTemplates.keys();
}

// ========== Persistence ==========

bool DeckGamepadCustomMappingManager::saveToFile(const QString &filePath)
{
    QString path = filePath.isEmpty() ? m_configPath : filePath;
    
    // Ensure directory exists
    QFileInfo fileInfo(path);
    QDir dir = fileInfo.dir();
    if (!dir.exists()) {
        if (!dir.mkpath(".")) {
            qWarning() << "Failed to create directory:" << dir.path();
            return false;
        }
    }
    
    QFile file(path);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        qWarning() << "Failed to open file for writing:" << path << file.errorString();
        return false;
    }
    
    QTextStream out(&file);
    out << "# DeckShell Custom Gamepad Mappings\n";
    out << "# Format: SDL GameController DB compatible\n";
    out << "# Generated: " << QDateTime::currentDateTime().toString(Qt::ISODate) << "\n\n";
    
    int count = 0;
    for (auto it = m_customMappings.constBegin(); it != m_customMappings.constEnd(); ++it) {
        const QString sdlString = it.value().sdlString.trimmed();
        if (!sdlString.isEmpty()) {
            out << sdlString << "\n";
            count++;
        }
    }
    
    file.close();
    emit mappingSaved(path);
    
    qDebug() << "Saved" << count << "custom mappings to" << path;
    return true;
}

int DeckGamepadCustomMappingManager::loadFromFile(const QString &filePath)
{
    QString path = filePath.isEmpty() ? m_configPath : filePath;
    
    QFile file(path);
    if (!file.exists()) {
        if (filePath.isEmpty() && m_enableLegacyFallback) {
            const QString legacyPath =
                QDir(QStandardPaths::writableLocation(QStandardPaths::ConfigLocation))
                    .filePath(QString("%1/custom_gamepad_mappings.txt").arg(m_legacyDirName));

            if (legacyPath != path && QFile::exists(legacyPath)) {
                qInfo() << "Custom mapping file found in legacy location:" << legacyPath;
                path = legacyPath;
                file.setFileName(path);
            }
        }

        if (!file.exists()) {
            qDebug() << "Custom mapping file does not exist:" << path;
            return 0;
        }
    }
    
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qWarning() << "Failed to open file for reading:" << path << file.errorString();
        return -1;
    }
    
    int count = 0;
    QTextStream in(&file);
    
    while (!in.atEnd()) {
        QString line = in.readLine().trimmed();
        
        // Skip comments and empty lines
        if (line.isEmpty() || line.startsWith('#')) {
            continue;
        }

        const QStringList parts = line.split(QLatin1Char(','), Qt::KeepEmptyParts);
        if (parts.size() < 3) {
            continue;
        }

        const QString guid = parts[0].trimmed().toLower();
        if (guid.isEmpty()) {
            continue;
        }

        StoredCustomMapping stored;
        stored.sdlString = line;
        m_customMappings[guid] = stored;
        count++;
    }
    
    file.close();
    
    qDebug() << "Loaded" << count << "custom mappings from" << path;
    return count;
}

QString DeckGamepadCustomMappingManager::defaultConfigPath() const
{
    return m_configPath;
}

void DeckGamepadCustomMappingManager::setDefaultConfigPath(const QString &filePath)
{
    if (filePath.isEmpty()) {
        const QString configDir = QStandardPaths::writableLocation(QStandardPaths::AppConfigLocation);
        m_configPath = QDir(configDir).filePath("custom_gamepad_mappings.txt");
        return;
    }

    m_configPath = filePath;
}

void DeckGamepadCustomMappingManager::setLegacyFallbackEnabled(bool enabled)
{
    m_enableLegacyFallback = enabled;
}

bool DeckGamepadCustomMappingManager::legacyFallbackEnabled() const
{
    return m_enableLegacyFallback;
}

void DeckGamepadCustomMappingManager::setLegacyDirName(const QString &dirName)
{
    if (!dirName.isEmpty()) {
        m_legacyDirName = dirName;
    }
}

QString DeckGamepadCustomMappingManager::legacyDirName() const
{
    return m_legacyDirName;
}

// ========== Apply Mapping ==========

bool DeckGamepadCustomMappingManager::applyMapping(int deviceId)
{
    QString guid = getDeviceGuid(deviceId);
    const auto it = m_customMappings.find(guid);
    if (it == m_customMappings.end()) {
        qWarning() << "No custom mapping to apply for device" << deviceId;
        return false;
    }

    StoredCustomMapping &stored = it.value();

    QString sdlString = stored.sdlString.trimmed();
    if (sdlString.isEmpty() && !stored.cachedEvdevMapping.isEmpty()) {
        QHash<int, int> physicalButtons;
        QHash<int, int> physicalAxes;
        if (m_backend) {
            auto collectPhysicalMaps = [&] {
                auto *device = m_backend->device(deviceId);
                if (!device) {
                    return;
                }
                physicalButtons = device->physicalButtonMap();
                physicalAxes = device->physicalAxisMap();
            };

            if (QThread::currentThread() == m_backend->thread()) {
                collectPhysicalMaps();
            } else {
                QMetaObject::invokeMethod(m_backend, collectPhysicalMaps, Qt::BlockingQueuedConnection);
            }
        }

        sdlString = deckGamepadComposeSdlMappingString(stored.cachedEvdevMapping, physicalButtons, physicalAxes);
    }

    if (sdlString.isEmpty()) {
        qWarning() << "Failed to apply mapping: empty SDL mapping string";
        return false;
    }

    {
        QStringList parts = sdlString.split(QLatin1Char(','), Qt::KeepEmptyParts);
        if (parts.size() >= 3) {
            parts[0] = guid;
            parts[1] = getDeviceName(deviceId);
            sdlString = parts.join(QLatin1Char(','));
        }
        stored.sdlString = sdlString;
    }

    if (!m_backend) {
        return false;
    }

    bool ok = false;
    auto applyToDevice = [&] {
        if (!m_sdlDb || !m_sdlDb->addMapping(sdlString)) {
            return;
        }

        auto *device = m_backend->device(deviceId);
        if (!device) {
            return;
        }

        device->reloadMapping();
        ok = true;
    };

    if (QThread::currentThread() == m_backend->thread()) {
        applyToDevice();
    } else {
        QMetaObject::invokeMethod(m_backend, applyToDevice, Qt::BlockingQueuedConnection);
    }

    if (!ok) {
        qWarning() << "Failed to apply mapping to device" << deviceId;
        return false;
    }

    emit mappingApplied(deviceId);
    qDebug() << "Applied custom mapping to device" << deviceId;
    return true;
}

bool DeckGamepadCustomMappingManager::resetToSdlDefault(int deviceId)
{
    QString guid = getDeviceGuid(deviceId);
    
    // Remove custom mapping
    removeCustomMapping(guid);
    
    // Reload device mapping (will use SDL DB default)
    if (!m_backend) {
        return false;
    }

    bool ok = false;
    auto reloadDevice = [&] {
        if (m_sdlDb) {
            m_sdlDb->removeMapping(guid);
        }

        auto *device = m_backend->device(deviceId);
        if (!device) {
            return;
        }

        device->reloadMapping();
        ok = true;
    };

    if (QThread::currentThread() == m_backend->thread()) {
        reloadDevice();
    } else {
        QMetaObject::invokeMethod(m_backend, reloadDevice, Qt::BlockingQueuedConnection);
    }

    if (!ok) {
        return false;
    }

    qDebug() << "Reset device" << deviceId << "to SDL DB default";
    return true;
}

// ========== Validation ==========

bool DeckGamepadCustomMappingManager::isMappingComplete(int deviceId) const
{
    return getMissingMappings(deviceId).isEmpty();
}

QStringList DeckGamepadCustomMappingManager::getMissingMappings(int deviceId) const
{
    QString guid = getDeviceGuid(deviceId);
    if (!m_customMappings.contains(guid)) {
        return QStringList() << "No custom mapping exists";
    }

    const DeviceMapping mapping = getCustomMapping(deviceId);
    QStringList missing;
    
    // Check essential buttons
    QList<GamepadButton> essentialButtons = {
        GAMEPAD_BUTTON_A, GAMEPAD_BUTTON_B, GAMEPAD_BUTTON_X, GAMEPAD_BUTTON_Y,
        GAMEPAD_BUTTON_L1, GAMEPAD_BUTTON_R1,
        GAMEPAD_BUTTON_SELECT, GAMEPAD_BUTTON_START
    };
    
    for (GamepadButton button : essentialButtons) {
        bool found = false;
        for (auto it = mapping.buttonMap.constBegin(); it != mapping.buttonMap.constEnd(); ++it) {
            if (it.value() == button) {
                found = true;
                break;
            }
        }
        if (!found) {
            missing << QString("Button %1").arg(button);
        }
    }
    
    // Check essential axes
    QList<GamepadAxis> essentialAxes = {
        GAMEPAD_AXIS_LEFT_X, GAMEPAD_AXIS_LEFT_Y,
        GAMEPAD_AXIS_RIGHT_X, GAMEPAD_AXIS_RIGHT_Y
    };
    
    for (GamepadAxis axis : essentialAxes) {
        bool found = false;
        for (auto it = mapping.axisMap.constBegin(); it != mapping.axisMap.constEnd(); ++it) {
            if (it.value() == axis) {
                found = true;
                break;
            }
        }
        if (!found) {
            missing << QString("Axis %1").arg(axis);
        }
    }
    
    return missing;
}

// ========== Export/Import ==========

QString DeckGamepadCustomMappingManager::exportToSdlString(int deviceId) const
{
    QString guid = getDeviceGuid(deviceId);
    const auto it = m_customMappings.constFind(guid);
    if (it == m_customMappings.constEnd()) {
        return {};
    }

    const StoredCustomMapping &stored = it.value();
    const QString sdlString = stored.sdlString.trimmed();
    if (!sdlString.isEmpty()) {
        return sdlString;
    }

    if (!m_backend || stored.cachedEvdevMapping.isEmpty()) {
        return {};
    }

    QHash<int, int> physicalButtons;
    QHash<int, int> physicalAxes;
    auto collectPhysicalMaps = [&] {
        auto *device = m_backend->device(deviceId);
        if (!device) {
            return;
        }
        physicalButtons = device->physicalButtonMap();
        physicalAxes = device->physicalAxisMap();
    };

    if (QThread::currentThread() == m_backend->thread()) {
        collectPhysicalMaps();
    } else {
        QMetaObject::invokeMethod(m_backend, collectPhysicalMaps, Qt::BlockingQueuedConnection);
    }

    return deckGamepadComposeSdlMappingString(stored.cachedEvdevMapping, physicalButtons, physicalAxes);
}

bool DeckGamepadCustomMappingManager::importFromSdlString(int deviceId, const QString &sdlString)
{
    const QString guid = getDeviceGuid(deviceId);
    if (guid.isEmpty()) {
        return false;
    }

    const QString deviceName = getDeviceName(deviceId);

    QStringList parts = sdlString.split(QLatin1Char(','), Qt::KeepEmptyParts);
    if (parts.size() < 3) {
        return false;
    }

    parts[0] = guid;
    parts[1] = deviceName;
    const QString normalizedSdlString = parts.join(QLatin1Char(','));

    QHash<int, int> physicalButtons;
    QHash<int, int> physicalAxes;
    if (m_backend) {
        auto collectPhysicalMaps = [&] {
            auto *device = m_backend->device(deviceId);
            if (!device) {
                return;
            }
            physicalButtons = device->physicalButtonMap();
            physicalAxes = device->physicalAxisMap();
        };

        if (QThread::currentThread() == m_backend->thread()) {
            collectPhysicalMaps();
        } else {
            QMetaObject::invokeMethod(m_backend, collectPhysicalMaps, Qt::BlockingQueuedConnection);
        }
    }

    DeviceMapping mapping = deckGamepadParseSdlMappingString(normalizedSdlString, physicalButtons, physicalAxes);
    if (mapping.isEmpty()) {
        return false;
    }

    mapping.guid = guid;
    mapping.name = deviceName;

    StoredCustomMapping stored;
    stored.cachedEvdevMapping = mapping;
    stored.sdlString = deckGamepadComposeSdlMappingString(mapping, physicalButtons, physicalAxes);
    m_customMappings[guid] = stored;
    emit mappingChanged(guid);
    
    return true;
}

// ========== Private Helper Methods ==========

QString DeckGamepadCustomMappingManager::getDeviceGuid(int deviceId) const
{
    if (!m_backend) {
        return QString();
    }

    if (QThread::currentThread() == m_backend->thread()) {
        auto *device = m_backend->device(deviceId);
        return device ? device->guid() : QString();
    }

    QString guid;
    QMetaObject::invokeMethod(m_backend, [&] {
        auto *device = m_backend->device(deviceId);
        guid = device ? device->guid() : QString();
    }, Qt::BlockingQueuedConnection);
    return guid;
}

QString DeckGamepadCustomMappingManager::getDeviceName(int deviceId) const
{
    if (!m_backend) {
        return QString();
    }

    if (QThread::currentThread() == m_backend->thread()) {
        auto *device = m_backend->device(deviceId);
        return device ? device->name() : QString();
    }

    QString name;
    QMetaObject::invokeMethod(m_backend, [&] {
        auto *device = m_backend->device(deviceId);
        name = device ? device->name() : QString();
    }, Qt::BlockingQueuedConnection);
    return name;
}

DeviceMapping DeckGamepadCustomMappingManager::createGenericMapping() const
{
    DeviceMapping mapping;
    
    // Generic Xbox-style button mapping
    mapping.buttonMap[BTN_SOUTH] = GAMEPAD_BUTTON_A;      // BTN_A
    mapping.buttonMap[BTN_EAST] = GAMEPAD_BUTTON_B;       // BTN_B
    mapping.buttonMap[BTN_NORTH] = GAMEPAD_BUTTON_X;      // BTN_X
    mapping.buttonMap[BTN_WEST] = GAMEPAD_BUTTON_Y;       // BTN_Y
    mapping.buttonMap[BTN_TL] = GAMEPAD_BUTTON_L1;        // LB
    mapping.buttonMap[BTN_TR] = GAMEPAD_BUTTON_R1;        // RB
    mapping.buttonMap[BTN_SELECT] = GAMEPAD_BUTTON_SELECT;
    mapping.buttonMap[BTN_START] = GAMEPAD_BUTTON_START;
    mapping.buttonMap[BTN_MODE] = GAMEPAD_BUTTON_GUIDE;
    mapping.buttonMap[BTN_THUMBL] = GAMEPAD_BUTTON_L3;
    mapping.buttonMap[BTN_THUMBR] = GAMEPAD_BUTTON_R3;
    
    // Generic axis mapping
    mapping.axisMap[ABS_X] = GAMEPAD_AXIS_LEFT_X;
    mapping.axisMap[ABS_Y] = GAMEPAD_AXIS_LEFT_Y;
    mapping.axisMap[ABS_RX] = GAMEPAD_AXIS_RIGHT_X;
    mapping.axisMap[ABS_RY] = GAMEPAD_AXIS_RIGHT_Y;
    mapping.axisMap[ABS_Z] = GAMEPAD_AXIS_TRIGGER_LEFT;
    mapping.axisMap[ABS_RZ] = GAMEPAD_AXIS_TRIGGER_RIGHT;
    
    // HAT/D-pad mapping
    mapping.hatButtonMap[GAMEPAD_HAT_UP] = GAMEPAD_BUTTON_DPAD_UP;
    mapping.hatButtonMap[GAMEPAD_HAT_DOWN] = GAMEPAD_BUTTON_DPAD_DOWN;
    mapping.hatButtonMap[GAMEPAD_HAT_LEFT] = GAMEPAD_BUTTON_DPAD_LEFT;
    mapping.hatButtonMap[GAMEPAD_HAT_RIGHT] = GAMEPAD_BUTTON_DPAD_RIGHT;
    
    return mapping;
}

void DeckGamepadCustomMappingManager::initializePresets()
{
    // Xbox preset
    m_presetTemplates["xbox"] = "xinput,Xbox Controller,a:b0,b:b1,x:b2,y:b3,"
        "back:b6,start:b7,guide:b8,leftshoulder:b4,rightshoulder:b5,"
        "leftstick:b9,rightstick:b10,leftx:a0,lefty:a1,rightx:a3,righty:a4,"
        "lefttrigger:a2,righttrigger:a5,dpup:h0.1,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,"
        "platform:Linux";
    
    // PlayStation preset
    m_presetTemplates["playstation"] = "ps,PlayStation Controller,a:b0,b:b1,x:b2,y:b3,"
        "back:b8,start:b9,guide:b10,leftshoulder:b4,rightshoulder:b5,"
        "leftstick:b11,rightstick:b12,leftx:a0,lefty:a1,rightx:a3,righty:a4,"
        "lefttrigger:a2,righttrigger:a5,dpup:h0.1,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,"
        "platform:Linux";
    
    // Nintendo preset
    m_presetTemplates["nintendo"] = "nintendo,Nintendo Controller,a:b1,b:b0,x:b3,y:b2,"
        "back:b6,start:b7,guide:b8,leftshoulder:b4,rightshoulder:b5,"
        "leftstick:b9,rightstick:b10,leftx:a0,lefty:a1,rightx:a3,righty:a4,"
        "lefttrigger:a2,righttrigger:a5,dpup:h0.1,dpdown:h0.4,dpleft:h0.8,dpright:h0.2,"
        "platform:Linux";
    
    // Generic preset (same as Xbox)
    m_presetTemplates["generic"] = m_presetTemplates["xbox"];
}

DECKGAMEPAD_END_NAMESPACE
