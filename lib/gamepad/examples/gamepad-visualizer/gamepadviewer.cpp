// Copyright (C) 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "gamepadviewer.h"
#include "gamepadwidget.h"

#include <deckshell/deckgamepad/backend/deckgamepadbackend.h>

#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGroupBox>
#include <QMessageBox>
#include <QPushButton>
#include <QSlider>
#include <QGridLayout>

DECKGAMEPAD_USE_NAMESPACE

GamepadViewer::GamepadViewer(QWidget *parent)
    : QMainWindow(parent)
    , m_backend(nullptr)
    , m_gamepadWidget(nullptr)
    , m_deviceSelector(nullptr)
    , m_statusLabel(nullptr)
    , m_connectionLabel(nullptr)
    , m_currentDeviceId(-1)
{
    setupUi();

    // Initialize backend
    m_backend = DeckGamepadBackend::instance();

    // Connect backend signals
    connect(m_backend, &DeckGamepadBackend::gamepadConnected,
            this, &GamepadViewer::onGamepadConnected);
    connect(m_backend, &DeckGamepadBackend::gamepadDisconnected,
            this, &GamepadViewer::onGamepadDisconnected);
    connect(m_backend, &DeckGamepadBackend::buttonEvent,
            this, &GamepadViewer::onButtonEvent);
    connect(m_backend, &DeckGamepadBackend::axisEvent,
            this, &GamepadViewer::onAxisEvent);
    connect(m_backend, &DeckGamepadBackend::hatEvent,
            this, &GamepadViewer::onHatEvent);

    // Start backend
    if (!m_backend->start()) {
        QMessageBox::critical(this, tr("Error"),
                            tr("Failed to start gamepad backend.\n"
                               "Make sure you have permission to access /dev/input devices."));
    }

    // Update device list with already connected devices
    updateDeviceList();
}

GamepadViewer::~GamepadViewer()
{
}

void GamepadViewer::setupUi()
{
    setWindowTitle(tr("Gamepad Visualizer"));

    QWidget *centralWidget = new QWidget(this);
    setCentralWidget(centralWidget);

    QVBoxLayout *mainLayout = new QVBoxLayout(centralWidget);

    // Device selection group
    QGroupBox *deviceGroup = new QGroupBox(tr("Device Selection"), this);
    QHBoxLayout *deviceLayout = new QHBoxLayout(deviceGroup);

    QLabel *deviceLabel = new QLabel(tr("Gamepad:"), this);
    m_deviceSelector = new QComboBox(this);
    m_deviceSelector->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Preferred);
    connect(m_deviceSelector, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &GamepadViewer::onDeviceSelectionChanged);

    deviceLayout->addWidget(deviceLabel);
    deviceLayout->addWidget(m_deviceSelector);

    mainLayout->addWidget(deviceGroup);

    // Connection status
    m_connectionLabel = new QLabel(tr("No gamepad connected"), this);
    m_connectionLabel->setStyleSheet("QLabel { color: red; font-weight: bold; }");
    m_connectionLabel->setAlignment(Qt::AlignCenter);
    mainLayout->addWidget(m_connectionLabel);

    // Gamepad visualization widget
    m_gamepadWidget = new GamepadWidget(this);
    m_gamepadWidget->setMinimumSize(600, 400);
    mainLayout->addWidget(m_gamepadWidget, 1);

    // Status label
    m_statusLabel = new QLabel(tr("Waiting for gamepad input..."), this);
    m_statusLabel->setAlignment(Qt::AlignCenter);
    mainLayout->addWidget(m_statusLabel);

    // Advanced controls
    setupAdvancedControls(mainLayout);
}

void GamepadViewer::onGamepadConnected(int deviceId, const QString &name)
{
    m_connectedDevices[deviceId] = name;
    updateDeviceList();
    updateStatusLabel();
}

void GamepadViewer::onGamepadDisconnected(int deviceId)
{
    m_connectedDevices.remove(deviceId);

    if (m_currentDeviceId == deviceId) {
        m_currentDeviceId = -1;
        m_gamepadWidget->reset();
    }

    updateDeviceList();
    updateStatusLabel();
}

void GamepadViewer::onDeviceSelectionChanged(int index)
{
    if (index < 0) {
        m_currentDeviceId = -1;
        m_gamepadWidget->reset();
        return;
    }

    m_currentDeviceId = m_deviceSelector->itemData(index).toInt();
    m_gamepadWidget->reset();
    updateStatusLabel();
}

void GamepadViewer::onButtonEvent(int deviceId, DeckGamepadButtonEvent event)
{
    if (deviceId != m_currentDeviceId)
        return;

    m_gamepadWidget->setButtonState(event.button, event.pressed);
    m_statusLabel->setText(tr("Button %1 %2")
                          .arg(event.button)
                          .arg(event.pressed ? tr("pressed") : tr("released")));
}

void GamepadViewer::onAxisEvent(int deviceId, DeckGamepadAxisEvent event)
{
    if (deviceId != m_currentDeviceId)
        return;

    m_gamepadWidget->setAxisValue(event.axis, event.value);
    m_statusLabel->setText(tr("Axis %1 = %2")
                          .arg(event.axis)
                          .arg(event.value, 0, 'f', 3));
}

void GamepadViewer::onHatEvent(int deviceId, DeckGamepadHatEvent event)
{
    if (deviceId != m_currentDeviceId)
        return;

    m_gamepadWidget->setHatValue(event.value);
    m_statusLabel->setText(tr("D-pad: 0x%1")
                          .arg(event.value, 2, 16, QChar('0')));
}

void GamepadViewer::updateDeviceList()
{
    m_deviceSelector->clear();

    if (m_connectedDevices.isEmpty()) {
        m_deviceSelector->addItem(tr("No gamepad connected"));
        m_deviceSelector->setEnabled(false);
        m_currentDeviceId = -1;
        return;
    }

    m_deviceSelector->setEnabled(true);

    for (auto it = m_connectedDevices.constBegin();
         it != m_connectedDevices.constEnd(); ++it) {
        m_deviceSelector->addItem(QString("[%1] %2").arg(it.key()).arg(it.value()),
                                 it.key());
    }

    // Auto-select first device if none selected
    if (m_currentDeviceId == -1 && m_deviceSelector->count() > 0) {
        m_currentDeviceId = m_deviceSelector->itemData(0).toInt();
    }
}

void GamepadViewer::updateStatusLabel()
{
    if (m_connectedDevices.isEmpty()) {
        m_connectionLabel->setText(tr("No gamepad connected"));
        m_connectionLabel->setStyleSheet("QLabel { color: red; font-weight: bold; }");
    } else if (m_currentDeviceId >= 0) {
        m_connectionLabel->setText(tr("Connected: %1")
                                  .arg(m_connectedDevices.value(m_currentDeviceId)));
        m_connectionLabel->setStyleSheet("QLabel { color: green; font-weight: bold; }");
    } else {
        m_connectionLabel->setText(tr("Please select a gamepad"));
        m_connectionLabel->setStyleSheet("QLabel { color: orange; font-weight: bold; }");
    }
}

// ============================================================================
// Advanced Features UI Setup (Task 1.5 & 1.6)
// ============================================================================

void GamepadViewer::setupAdvancedControls(QVBoxLayout *mainLayout)
{
    m_advancedGroup = new QGroupBox(tr("Advanced Settings"), this);
    QGridLayout *advLayout = new QGridLayout(m_advancedGroup);

    int row = 0;

    // === Deadzone Controls (Task 1.5) ===
    QLabel *deadzoneTitle = new QLabel(tr("<b>Deadzone Settings</b>"), this);
    advLayout->addWidget(deadzoneTitle, row++, 0, 1, 3);

    // Left stick deadzone
    advLayout->addWidget(new QLabel(tr("Left Stick:"), this), row, 0);
    m_leftStickDeadzoneSlider = new QSlider(Qt::Horizontal, this);
    m_leftStickDeadzoneSlider->setRange(0, 50);  // 0-50% deadzone
    m_leftStickDeadzoneSlider->setValue(0);
    advLayout->addWidget(m_leftStickDeadzoneSlider, row, 1);
    m_leftStickDeadzoneLabel = new QLabel(tr("0%"), this);
    advLayout->addWidget(m_leftStickDeadzoneLabel, row++, 2);
    connect(m_leftStickDeadzoneSlider, &QSlider::valueChanged,
            this, &GamepadViewer::onLeftStickDeadzoneChanged);

    // Right stick deadzone
    advLayout->addWidget(new QLabel(tr("Right Stick:"), this), row, 0);
    m_rightStickDeadzoneSlider = new QSlider(Qt::Horizontal, this);
    m_rightStickDeadzoneSlider->setRange(0, 50);
    m_rightStickDeadzoneSlider->setValue(0);
    advLayout->addWidget(m_rightStickDeadzoneSlider, row, 1);
    m_rightStickDeadzoneLabel = new QLabel(tr("0%"), this);
    advLayout->addWidget(m_rightStickDeadzoneLabel, row++, 2);
    connect(m_rightStickDeadzoneSlider, &QSlider::valueChanged,
            this, &GamepadViewer::onRightStickDeadzoneChanged);

    // Triggers deadzone
    advLayout->addWidget(new QLabel(tr("Triggers:"), this), row, 0);
    m_triggersDeadzoneSlider = new QSlider(Qt::Horizontal, this);
    m_triggersDeadzoneSlider->setRange(0, 50);
    m_triggersDeadzoneSlider->setValue(0);
    advLayout->addWidget(m_triggersDeadzoneSlider, row, 1);
    m_triggersDeadzoneLabel = new QLabel(tr("0%"), this);
    advLayout->addWidget(m_triggersDeadzoneLabel, row++, 2);
    connect(m_triggersDeadzoneSlider, &QSlider::valueChanged,
            this, &GamepadViewer::onTriggersDeadzoneChanged);

    // === Sensitivity Controls (Task 1.5) ===
    QLabel *sensitivityTitle = new QLabel(tr("<b>Sensitivity Settings</b>"), this);
    advLayout->addWidget(sensitivityTitle, row++, 0, 1, 3);

    // Left stick sensitivity
    advLayout->addWidget(new QLabel(tr("Left Stick:"), this), row, 0);
    m_leftStickSensitivitySlider = new QSlider(Qt::Horizontal, this);
    m_leftStickSensitivitySlider->setRange(50, 200);  // 0.5x to 2.0x
    m_leftStickSensitivitySlider->setValue(100);  // 1.0x
    advLayout->addWidget(m_leftStickSensitivitySlider, row, 1);
    m_leftStickSensitivityLabel = new QLabel(tr("1.0x"), this);
    advLayout->addWidget(m_leftStickSensitivityLabel, row++, 2);
    connect(m_leftStickSensitivitySlider, &QSlider::valueChanged,
            this, &GamepadViewer::onLeftStickSensitivityChanged);

    // Right stick sensitivity
    advLayout->addWidget(new QLabel(tr("Right Stick:"), this), row, 0);
    m_rightStickSensitivitySlider = new QSlider(Qt::Horizontal, this);
    m_rightStickSensitivitySlider->setRange(50, 200);
    m_rightStickSensitivitySlider->setValue(100);
    advLayout->addWidget(m_rightStickSensitivitySlider, row, 1);
    m_rightStickSensitivityLabel = new QLabel(tr("1.0x"), this);
    advLayout->addWidget(m_rightStickSensitivityLabel, row++, 2);
    connect(m_rightStickSensitivitySlider, &QSlider::valueChanged,
            this, &GamepadViewer::onRightStickSensitivityChanged);

    // Reset button
    m_resetButton = new QPushButton(tr("Reset All Settings"), this);
    advLayout->addWidget(m_resetButton, row++, 0, 1, 3);
    connect(m_resetButton, &QPushButton::clicked,
            this, &GamepadViewer::onResetSettings);

    // === Vibration Controls (Task 1.6) ===
    QLabel *vibrationTitle = new QLabel(tr("<b>Vibration Test</b>"), this);
    advLayout->addWidget(vibrationTitle, row++, 0, 1, 3);

    QHBoxLayout *vibLayout = new QHBoxLayout();
    m_weakVibButton = new QPushButton(tr("Weak"), this);
    m_strongVibButton = new QPushButton(tr("Strong"), this);
    m_bothVibButton = new QPushButton(tr("Both"), this);
    m_stopVibButton = new QPushButton(tr("Stop"), this);

    vibLayout->addWidget(m_weakVibButton);
    vibLayout->addWidget(m_strongVibButton);
    vibLayout->addWidget(m_bothVibButton);
    vibLayout->addWidget(m_stopVibButton);

    advLayout->addLayout(vibLayout, row++, 0, 1, 3);

    connect(m_weakVibButton, &QPushButton::clicked,
            this, &GamepadViewer::onTestWeakVibration);
    connect(m_strongVibButton, &QPushButton::clicked,
            this, &GamepadViewer::onTestStrongVibration);
    connect(m_bothVibButton, &QPushButton::clicked,
            this, &GamepadViewer::onTestBothVibration);
    connect(m_stopVibButton, &QPushButton::clicked,
            this, &GamepadViewer::onStopVibration);

    mainLayout->addWidget(m_advancedGroup);
}

// ============================================================================
// Advanced Features Slots (Task 1.5)
// ============================================================================

void GamepadViewer::onLeftStickDeadzoneChanged(int value)
{
    float deadzone = value / 100.0f;  // Convert to 0.0-0.5
    m_leftStickDeadzoneLabel->setText(QString("%1%").arg(value));

    if (m_currentDeviceId >= 0) {
        m_backend->setAxisDeadzone(m_currentDeviceId, GAMEPAD_AXIS_LEFT_X, deadzone);
        m_backend->setAxisDeadzone(m_currentDeviceId, GAMEPAD_AXIS_LEFT_Y, deadzone);
    }
}

void GamepadViewer::onRightStickDeadzoneChanged(int value)
{
    float deadzone = value / 100.0f;
    m_rightStickDeadzoneLabel->setText(QString("%1%").arg(value));

    if (m_currentDeviceId >= 0) {
        m_backend->setAxisDeadzone(m_currentDeviceId, GAMEPAD_AXIS_RIGHT_X, deadzone);
        m_backend->setAxisDeadzone(m_currentDeviceId, GAMEPAD_AXIS_RIGHT_Y, deadzone);
    }
}

void GamepadViewer::onTriggersDeadzoneChanged(int value)
{
    float deadzone = value / 100.0f;
    m_triggersDeadzoneLabel->setText(QString("%1%").arg(value));

    if (m_currentDeviceId >= 0) {
        m_backend->setAxisDeadzone(m_currentDeviceId, GAMEPAD_AXIS_TRIGGER_LEFT, deadzone);
        m_backend->setAxisDeadzone(m_currentDeviceId, GAMEPAD_AXIS_TRIGGER_RIGHT, deadzone);
    }
}

void GamepadViewer::onLeftStickSensitivityChanged(int value)
{
    float sensitivity = value / 100.0f;  // Convert to 0.5-2.0
    m_leftStickSensitivityLabel->setText(QString("%1x").arg(sensitivity, 0, 'f', 1));

    if (m_currentDeviceId >= 0) {
        m_backend->setAxisSensitivity(m_currentDeviceId, GAMEPAD_AXIS_LEFT_X, sensitivity);
        m_backend->setAxisSensitivity(m_currentDeviceId, GAMEPAD_AXIS_LEFT_Y, sensitivity);
    }
}

void GamepadViewer::onRightStickSensitivityChanged(int value)
{
    float sensitivity = value / 100.0f;
    m_rightStickSensitivityLabel->setText(QString("%1x").arg(sensitivity, 0, 'f', 1));

    if (m_currentDeviceId >= 0) {
        m_backend->setAxisSensitivity(m_currentDeviceId, GAMEPAD_AXIS_RIGHT_X, sensitivity);
        m_backend->setAxisSensitivity(m_currentDeviceId, GAMEPAD_AXIS_RIGHT_Y, sensitivity);
    }
}

void GamepadViewer::onResetSettings()
{
    // Reset sliders
    m_leftStickDeadzoneSlider->setValue(0);
    m_rightStickDeadzoneSlider->setValue(0);
    m_triggersDeadzoneSlider->setValue(0);
    m_leftStickSensitivitySlider->setValue(100);
    m_rightStickSensitivitySlider->setValue(100);

    // Reset backend settings
    if (m_currentDeviceId >= 0) {
        m_backend->resetAxisSettings(m_currentDeviceId, GAMEPAD_AXIS_LEFT_X);
        m_backend->resetAxisSettings(m_currentDeviceId, GAMEPAD_AXIS_LEFT_Y);
        m_backend->resetAxisSettings(m_currentDeviceId, GAMEPAD_AXIS_RIGHT_X);
        m_backend->resetAxisSettings(m_currentDeviceId, GAMEPAD_AXIS_RIGHT_Y);
        m_backend->resetAxisSettings(m_currentDeviceId, GAMEPAD_AXIS_TRIGGER_LEFT);
        m_backend->resetAxisSettings(m_currentDeviceId, GAMEPAD_AXIS_TRIGGER_RIGHT);
    }

    m_statusLabel->setText(tr("All settings reset to default"));
}

// ============================================================================
// Vibration Test Slots (Task 1.6)
// ============================================================================

void GamepadViewer::onTestWeakVibration()
{
    if (m_currentDeviceId < 0) {
        m_statusLabel->setText(tr("No gamepad selected"));
        return;
    }

    if (m_backend->startVibration(m_currentDeviceId, 0.8f, 0.0f, 500)) {
        m_statusLabel->setText(tr("Testing weak vibration (500ms)"));
    } else {
        m_statusLabel->setText(tr("Vibration not supported or failed"));
    }
}

void GamepadViewer::onTestStrongVibration()
{
    if (m_currentDeviceId < 0) {
        m_statusLabel->setText(tr("No gamepad selected"));
        return;
    }

    if (m_backend->startVibration(m_currentDeviceId, 0.0f, 0.8f, 500)) {
        m_statusLabel->setText(tr("Testing strong vibration (500ms)"));
    } else {
        m_statusLabel->setText(tr("Vibration not supported or failed"));
    }
}

void GamepadViewer::onTestBothVibration()
{
    if (m_currentDeviceId < 0) {
        m_statusLabel->setText(tr("No gamepad selected"));
        return;
    }

    if (m_backend->startVibration(m_currentDeviceId, 0.6f, 0.6f, 1000)) {
        m_statusLabel->setText(tr("Testing both motors (1000ms)"));
    } else {
        m_statusLabel->setText(tr("Vibration not supported or failed"));
    }
}

void GamepadViewer::onStopVibration()
{
    if (m_currentDeviceId < 0) {
        m_statusLabel->setText(tr("No gamepad selected"));
        return;
    }

    m_backend->stopVibration(m_currentDeviceId);
    m_statusLabel->setText(tr("Vibration stopped"));
}
