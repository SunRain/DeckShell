// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QtCore/QObject>
#include <QtCore/QStringList>
#include <QtQml/qqml.h>

namespace deckshell::deckgamepad {
class DeckGamepadService;
class DeckGamepadCustomMappingManager;
} // namespace deckshell::deckgamepad

class CustomMappingManager : public QObject
{
    Q_OBJECT
    QML_ELEMENT

public:
    explicit CustomMappingManager(QObject *parent = nullptr);
    ~CustomMappingManager() override;

    void setService(deckshell::deckgamepad::DeckGamepadService *service);

    Q_PROPERTY(bool supported READ supported NOTIFY supportedChanged FINAL)
    bool supported() const;

    Q_INVOKABLE QString createCustomMapping(int deviceId);
    Q_INVOKABLE bool hasCustomMapping(int deviceId) const;
    Q_INVOKABLE QStringList availablePresets() const;
    Q_INVOKABLE bool loadPreset(int deviceId, const QString &presetName);

    Q_INVOKABLE bool saveToFile(const QString &filePath = QString());
    Q_INVOKABLE int loadFromFile(const QString &filePath = QString());

    Q_INVOKABLE bool applyMapping(int deviceId);
    Q_INVOKABLE bool resetToSdlDefault(int deviceId);

    Q_INVOKABLE bool isMappingComplete(int deviceId) const;
    Q_INVOKABLE QStringList getMissingMappings(int deviceId) const;

    Q_INVOKABLE QString exportToSdlString(int deviceId) const;
    Q_INVOKABLE bool importFromSdlString(int deviceId, const QString &sdlString);

public Q_SLOTS:
    void syncFromService();

Q_SIGNALS:
    void supportedChanged();

private:
    deckshell::deckgamepad::DeckGamepadCustomMappingManager *mappingManager() const;

    deckshell::deckgamepad::DeckGamepadService *m_service = nullptr;
    bool m_supported = false;
};
