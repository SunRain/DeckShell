// Copyright (C) 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#ifndef GAMEPADVIEWER_H
#define GAMEPADVIEWER_H

#include <QMainWindow>
#include <QComboBox>
#include <QLabel>
#include <QHash>

#include <deckshell/deckgamepad/backend/deckgamepadbackend.h>

DECKGAMEPAD_USE_NAMESPACE

QT_BEGIN_NAMESPACE
class QVBoxLayout;
class QHBoxLayout;
class QPushButton;
class QSlider;
class QGroupBox;
QT_END_NAMESPACE

class GamepadWidget;

class GamepadViewer : public QMainWindow
{
    Q_OBJECT

public:
    explicit GamepadViewer(QWidget *parent = nullptr);
    ~GamepadViewer() override;

private slots:
    void onGamepadConnected(int deviceId, const QString &name);
    void onGamepadDisconnected(int deviceId);
    void onDeviceSelectionChanged(int index);
    void onButtonEvent(int deviceId, struct DeckGamepadButtonEvent event);
    void onAxisEvent(int deviceId, struct DeckGamepadAxisEvent event);
    void onHatEvent(int deviceId, struct DeckGamepadHatEvent event);

    // Advanced features slots (Task 1.5 & 1.6)
    void onLeftStickDeadzoneChanged(int value);
    void onRightStickDeadzoneChanged(int value);
    void onTriggersDeadzoneChanged(int value);
    void onLeftStickSensitivityChanged(int value);
    void onRightStickSensitivityChanged(int value);
    void onResetSettings();
    void onTestWeakVibration();
    void onTestStrongVibration();
    void onTestBothVibration();
    void onStopVibration();

private:
    void setupUi();
    void setupAdvancedControls(QVBoxLayout *mainLayout);
    void updateDeviceList();
    void updateStatusLabel();

private:
    DeckGamepadBackend *m_backend;
    GamepadWidget *m_gamepadWidget;
    QComboBox *m_deviceSelector;
    QLabel *m_statusLabel;
    QLabel *m_connectionLabel;

    // Advanced control widgets
    QGroupBox *m_advancedGroup;
    QSlider *m_leftStickDeadzoneSlider;
    QSlider *m_rightStickDeadzoneSlider;
    QSlider *m_triggersDeadzoneSlider;
    QSlider *m_leftStickSensitivitySlider;
    QSlider *m_rightStickSensitivitySlider;
    QLabel *m_leftStickDeadzoneLabel;
    QLabel *m_rightStickDeadzoneLabel;
    QLabel *m_triggersDeadzoneLabel;
    QLabel *m_leftStickSensitivityLabel;
    QLabel *m_rightStickSensitivityLabel;
    QPushButton *m_resetButton;
    QPushButton *m_weakVibButton;
    QPushButton *m_strongVibButton;
    QPushButton *m_bothVibButton;
    QPushButton *m_stopVibButton;

    int m_currentDeviceId;
    QHash<int, QString> m_connectedDevices; // deviceId -> name
};

#endif // GAMEPADVIEWER_H
