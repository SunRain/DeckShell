// SPDX-FileCopyrightText: 2024 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <deckshell/deckgamepad/core/deckgamepad.h>
#include <deckshell/deckgamepad/mapping/deckgamepadmapping.h>

#include <QtCore/QObject>
#include <QtCore/QString>
#include <QtCore/QHash>
#include <QtCore/QStringList>

DECKGAMEPAD_BEGIN_NAMESPACE

class DeckGamepadSdlControllerDb;
class DeckGamepadBackend;

/// 自定义映射管理器（SDL mapping 格式，优先于 SDL DB）。
/// 负责加载/保存映射文件，并可将映射应用到运行中设备。
class DECKGAMEPAD_EXPORT DeckGamepadCustomMappingManager : public QObject
{
    Q_OBJECT

public:
    explicit DeckGamepadCustomMappingManager(DeckGamepadBackend *backend, QObject *parent = nullptr);
    ~DeckGamepadCustomMappingManager() override;

    // 映射 CRUD

    // 创建指定设备的自定义映射；优先以 SDL DB 映射为基线。
    QString createCustomMapping(int deviceId);

    bool hasCustomMapping(int deviceId) const;
    bool hasCustomMapping(const QString &guid) const;

    DeviceMapping getCustomMapping(int deviceId) const;
    DeviceMapping getCustomMapping(const QString &guid) const;

    void removeCustomMapping(int deviceId);
    void removeCustomMapping(const QString &guid);

    // 映射编辑

    void setButtonMapping(int deviceId, GamepadButton logicalButton, int physicalCode);

    void setAxisMapping(int deviceId, GamepadAxis logicalAxis, int physicalCode, bool inverted = false);

    void setHatMapping(int deviceId, GamepadButton logicalButton, int hatCode, int hatMask);

    void clearButtonMapping(int deviceId, GamepadButton logicalButton);
    void clearAxisMapping(int deviceId, GamepadAxis logicalAxis);

    // 预设模板

    bool loadPreset(int deviceId, const QString &presetName);

    QStringList availablePresets() const;

    // 持久化

    // filePath 为空时写入 defaultConfigPath()；文件格式兼容 SDL DB。
    bool saveToFile(const QString &filePath = QString());

    int loadFromFile(const QString &filePath = QString());

    QString defaultConfigPath() const;

    // 仅影响 filePath 为空时的默认读写路径，不改变文件格式。
    void setDefaultConfigPath(const QString &filePath);

    // 启用后会在 legacy 路径回退读取（兼容旧版本）。
    void setLegacyFallbackEnabled(bool enabled);
    bool legacyFallbackEnabled() const;

    // legacy 目录名（默认 "DeckShell"）。
    void setLegacyDirName(const QString &dirName);
    QString legacyDirName() const;

    // 应用/重置

    bool applyMapping(int deviceId);

    bool resetToSdlDefault(int deviceId);

    // 校验

    bool isMappingComplete(int deviceId) const;

    QStringList getMissingMappings(int deviceId) const;

    // 导入/导出（SDL mapping string）

    QString exportToSdlString(int deviceId) const;

    bool importFromSdlString(int deviceId, const QString &sdlString);

Q_SIGNALS:
    void mappingCreated(const QString &guid);
    void mappingChanged(const QString &guid);
    void mappingRemoved(const QString &guid);
    void mappingSaved(const QString &filePath);
    void mappingApplied(int deviceId);

private:
    QString getDeviceGuid(int deviceId) const;
    QString getDeviceName(int deviceId) const;
    DeviceMapping createGenericMapping() const;
    void initializePresets();

    struct StoredCustomMapping {
        QString sdlString;
        DeviceMapping cachedEvdevMapping;
    };
    
    DeckGamepadBackend *m_backend;
    DeckGamepadSdlControllerDb *m_sdlDb;

    // 自定义映射：GUID -> SDL mapping string（并在需要时按 device physical map 物化为 DeviceMapping）
    QHash<QString, StoredCustomMapping> m_customMappings;

    // 预设模板：presetName -> SDL mapping string
    QHash<QString, QString> m_presetTemplates;

    QString m_configPath;

    bool m_enableLegacyFallback = true;
    QString m_legacyDirName = QStringLiteral("DeckShell");
};

DECKGAMEPAD_END_NAMESPACE
