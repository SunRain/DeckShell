// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QtCore/QHash>
#include <QtCore/QObject>
#include <QtCore/QPointer>
#include <QtCore/QString>
#include <QtCore/QStringList>
#include <QtCore/QTimer>
#include <QtQml/qqml.h>

class GamepadManager;
namespace deckshell::deckgamepad {
class DeckGamepadCustomMappingManager;
}

class MappingEditorBridge : public QObject
{
    Q_OBJECT
    QML_ELEMENT

    Q_PROPERTY(int deviceId READ deviceId WRITE setDeviceId NOTIFY deviceIdChanged FINAL)
    Q_PROPERTY(QString deviceName READ deviceName NOTIFY deviceNameChanged FINAL)
    Q_PROPERTY(QString deviceGuid READ deviceGuid NOTIFY deviceGuidChanged FINAL)
    Q_PROPERTY(bool hasCustomMapping READ hasCustomMapping NOTIFY mappingChanged FINAL)
    Q_PROPERTY(bool isListening READ isListening NOTIFY listeningChanged FINAL)
    Q_PROPERTY(bool isMappingComplete READ isMappingComplete NOTIFY mappingChanged FINAL)

public:
    explicit MappingEditorBridge(QObject *parent = nullptr);
    ~MappingEditorBridge() override;

    int deviceId() const { return m_deviceId; }
    void setDeviceId(int deviceId);

    QString deviceName() const;
    QString deviceGuid() const;
    bool hasCustomMapping() const;
    bool isListening() const { return m_isListening; }
    bool isMappingComplete() const;

    // ========== Mapping Operations ==========
    Q_INVOKABLE void createMapping();
    Q_INVOKABLE bool saveMapping();
    Q_INVOKABLE void removeMapping();
    Q_INVOKABLE bool loadPreset(const QString &presetName);
    Q_INVOKABLE QStringList availablePresets();

    // ========== Button/Axis Mapping ==========
    Q_INVOKABLE QString getButtonMapping(int logicalButton);
    Q_INVOKABLE QString getAxisMapping(int logicalAxis);
    Q_INVOKABLE void clearButtonMapping(int logicalButton);
    Q_INVOKABLE void clearAxisMapping(int logicalAxis);

    // ========== Input Capture ==========
    Q_INVOKABLE void startCapture(const QString &inputType);
    Q_INVOKABLE void stopCapture();
    Q_INVOKABLE void setCaptureTarget(int logicalButton, int logicalAxis);

    // ========== Validation ==========
    Q_INVOKABLE QStringList getMissingMappings();

    // ========== Export/Import ==========
    Q_INVOKABLE QString exportToSdl();
    Q_INVOKABLE bool importFromSdl(const QString &sdlString);

    // ========== Clipboard Operations ==========
    Q_INVOKABLE void copyToClipboard(const QString &text);
    Q_INVOKABLE QString pasteFromClipboard();
    Q_INVOKABLE bool validateSdlString(const QString &sdlString);

Q_SIGNALS:
    void deviceIdChanged();
    void deviceNameChanged();
    void deviceGuidChanged();
    void mappingChanged();
    void listeningChanged();

    void inputCaptured(int evdevCode, const QString &inputName);
    void captureTimeout();
    void captureFailed(const QString &reason);
    void mappingSaved();
    void mappingSaveFailed(const QString &error);
    void clipboardOperationCompleted(bool success, const QString &message);

private Q_SLOTS:
    void onButtonPressed(int deviceId, int button);
    void onAxisChanged(int deviceId, int axis, double value);
    void onCaptureTimerTimeout();

private:
    deckshell::deckgamepad::DeckGamepadCustomMappingManager *mappingManager() const;
    GamepadManager *resolveManager() const;

    QString buttonCodeToName(int evdevCode) const;
    QString axisCodeToName(int evdevCode) const;
    QString logicalButtonToName(int logicalButton) const;
    QString logicalAxisToName(int logicalAxis) const;

    int resolvePhysicalButtonCode(int deviceId, int logicalButton) const;
    int resolvePhysicalAxisCode(int deviceId, int logicalAxis) const;

    int m_deviceId = -1;
    bool m_isListening = false;
    QString m_captureType; // "button" or "axis"
    int m_captureLogicalButton = -1;
    int m_captureLogicalAxis = -1;

    mutable QPointer<GamepadManager> m_manager;

    QTimer *m_captureTimer = nullptr;
    static constexpr int CAPTURE_TIMEOUT_MS = 5000;

    QHash<int, double> m_lastAxisValues;
    static constexpr double AXIS_THRESHOLD = 0.5;
};
