// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "monitorwidget.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGroupBox>
#include <QDateTime>
#include <QFileDialog>
#include <QFile>
#include <QTextStream>
#include <QMessageBox>

using namespace TreelandGamepad;
using namespace deckshell::deckgamepad;

MonitorWidget::MonitorWidget(TreelandGamepadClient *client, QWidget *parent)
    : QWidget(parent)
    , m_client(client)
{
    setupUI();
}

void MonitorWidget::setupUI()
{
    auto *mainLayout = new QVBoxLayout(this);
    
    // 控制面板
    auto *controlGroup = new QGroupBox("控制选项");
    auto *controlLayout = new QHBoxLayout(controlGroup);
    
    m_timestampCheck = new QCheckBox("显示时间戳");
    m_timestampCheck->setChecked(m_showTimestamp);
    connect(m_timestampCheck, &QCheckBox::toggled, this, &MonitorWidget::toggleTimestamp);
    controlLayout->addWidget(m_timestampCheck);
    
    m_rawDataCheck = new QCheckBox("显示原始数据");
    m_rawDataCheck->setChecked(m_showRawData);
    connect(m_rawDataCheck, &QCheckBox::toggled, this, &MonitorWidget::toggleRawData);
    controlLayout->addWidget(m_rawDataCheck);
    
    m_autoScrollCheck = new QCheckBox("自动滚动");
    m_autoScrollCheck->setChecked(true);
    controlLayout->addWidget(m_autoScrollCheck);
    
    controlLayout->addStretch();
    
    m_clearButton = new QPushButton("清空日志");
    connect(m_clearButton, &QPushButton::clicked, this, &MonitorWidget::clearLog);
    controlLayout->addWidget(m_clearButton);
    
    m_saveButton = new QPushButton("保存日志");
    connect(m_saveButton, &QPushButton::clicked, this, &MonitorWidget::saveLog);
    controlLayout->addWidget(m_saveButton);
    
    mainLayout->addWidget(controlGroup);
    
    // 统计信息
    auto *statsGroup = new QGroupBox("事件统计");
    auto *statsLayout = new QHBoxLayout(statsGroup);
    
    m_buttonCountLabel = new QLabel("按钮事件: 0");
    statsLayout->addWidget(m_buttonCountLabel);
    
    m_axisCountLabel = new QLabel("轴事件: 0");
    statsLayout->addWidget(m_axisCountLabel);
    
    m_hatCountLabel = new QLabel("方向键事件: 0");
    statsLayout->addWidget(m_hatCountLabel);
    
    statsLayout->addStretch();
    
    mainLayout->addWidget(statsGroup);
    
    // 日志显示区
    m_logDisplay = new QTextEdit;
    m_logDisplay->setReadOnly(true);
    m_logDisplay->setFont(QFont("Monospace", 9));
    m_logDisplay->setStyleSheet("QTextEdit { background-color: #1e1e1e; color: #d4d4d4; }");
    mainLayout->addWidget(m_logDisplay);
    
    // 初始提示
    appendLog("=== Treeland Gamepad Event Monitor ===");
    appendLog("等待设备连接...");
}

void MonitorWidget::setCurrentDevice(int deviceId)
{
    // 断开旧设备
    disconnectDevice();
    
    if (deviceId < 0) {
        appendLog("设备已断开");
        m_currentDevice = nullptr;
        return;
    }
    
    // 连接新设备
    m_currentDevice = m_client->gamepad(deviceId);
    if (m_currentDevice) {
        connectDevice(m_currentDevice);
        appendLog(QString("已切换到设备 ID: %1, 名称: %2")
                 .arg(deviceId)
                 .arg(m_currentDevice->name()));
    }
}

void MonitorWidget::connectDevice(TreelandGamepadDevice *device)
{
    if (!device) return;
    
    // 连接事件信号
    connect(device, &TreelandGamepadDevice::buttonEvent,
            this, &MonitorWidget::onButtonEvent);
    connect(device, &TreelandGamepadDevice::axisEvent,
            this, &MonitorWidget::onAxisEvent);
    connect(device, &TreelandGamepadDevice::hatEvent,
            this, &MonitorWidget::onHatEvent);
}

void MonitorWidget::disconnectDevice()
{
    if (!m_currentDevice) return;
    
    // 断开所有信号
    disconnect(m_currentDevice, nullptr, this, nullptr);
}

void MonitorWidget::onButtonEvent(DeckGamepadButtonEvent event)
{
    m_buttonEventCount++;
    m_buttonCountLabel->setText(QString("按钮事件: %1").arg(m_buttonEventCount));
    
    QString message;
    if (m_showRawData) {
        message = QString("[BUTTON] time=%1, button=%2, pressed=%3")
                 .arg(event.time_msec)
                 .arg(event.button)
                 .arg(event.pressed ? 1 : 0);
    } else {
        message = QString("[按钮] %1 %2")
                 .arg(buttonName(static_cast<GamepadButton>(event.button)))
                 .arg(event.pressed ? "按下" : "释放");
    }
    
    appendLog(message);
}

void MonitorWidget::onAxisEvent(DeckGamepadAxisEvent event)
{
    m_axisEventCount++;
    m_axisCountLabel->setText(QString("轴事件: %1").arg(m_axisEventCount));
    
    QString message;
    if (m_showRawData) {
        message = QString("[AXIS] time=%1, axis=%2, value=%3")
                 .arg(event.time_msec)
                 .arg(event.axis)
                 .arg(event.value, 0, 'f', 3);
    } else {
        message = QString("[轴] %1 = %2")
                 .arg(axisName(static_cast<GamepadAxis>(event.axis)))
                 .arg(event.value, 0, 'f', 3);
    }
    
    appendLog(message);
}

void MonitorWidget::onHatEvent(DeckGamepadHatEvent event)
{
    m_hatEventCount++;
    m_hatCountLabel->setText(QString("方向键事件: %1").arg(m_hatEventCount));
    
    QString message;
    if (m_showRawData) {
        message = QString("[HAT] time=%1, hat=%2, direction=%3")
                 .arg(event.time_msec)
                 .arg(event.hat)
                 .arg(event.value);
    } else {
        message = QString("[方向键] %1")
                 .arg(hatDirectionName(event.value));
    }
    
    appendLog(message);
}

void MonitorWidget::appendLog(const QString &message)
{
    QString logLine;
    
    if (m_showTimestamp) {
        logLine = QString("[%1] %2")
                 .arg(QDateTime::currentDateTime().toString("hh:mm:ss.zzz"))
                 .arg(message);
    } else {
        logLine = message;
    }
    
    m_logDisplay->append(logLine);
    
    if (m_autoScrollCheck->isChecked()) {
        m_logDisplay->moveCursor(QTextCursor::End);
    }
}

void MonitorWidget::clearLog()
{
    m_logDisplay->clear();
    m_buttonEventCount = 0;
    m_axisEventCount = 0;
    m_hatEventCount = 0;
    m_buttonCountLabel->setText("按钮事件: 0");
    m_axisCountLabel->setText("轴事件: 0");
    m_hatCountLabel->setText("方向键事件: 0");
    
    appendLog("=== 日志已清空 ===");
}

void MonitorWidget::saveLog()
{
    QString fileName = QFileDialog::getSaveFileName(this, 
        "保存日志", 
        QString("gamepad_log_%1.txt").arg(QDateTime::currentDateTime().toString("yyyyMMdd_hhmmss")),
        "文本文件 (*.txt);;所有文件 (*)");
    
    if (fileName.isEmpty()) return;
    
    QFile file(fileName);
    if (file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        QTextStream stream(&file);
        stream << m_logDisplay->toPlainText();
        file.close();
        
        QMessageBox::information(this, "保存成功", 
            QString("日志已保存到: %1").arg(fileName));
    } else {
        QMessageBox::warning(this, "保存失败", 
            QString("无法保存文件: %1").arg(fileName));
    }
}

void MonitorWidget::toggleTimestamp(bool enable)
{
    m_showTimestamp = enable;
}

void MonitorWidget::toggleRawData(bool enable)
{
    m_showRawData = enable;
}

QString MonitorWidget::buttonName(GamepadButton button) const
{
    switch (button) {
    case GAMEPAD_BUTTON_A: return "A";
    case GAMEPAD_BUTTON_B: return "B";
    case GAMEPAD_BUTTON_X: return "X";
    case GAMEPAD_BUTTON_Y: return "Y";
    case GAMEPAD_BUTTON_L1: return "LB";
    case GAMEPAD_BUTTON_R1: return "RB";
    case GAMEPAD_BUTTON_L2: return "LT";
    case GAMEPAD_BUTTON_R2: return "RT";
    case GAMEPAD_BUTTON_SELECT: return "Select/Back";
    case GAMEPAD_BUTTON_START: return "Start";
    case GAMEPAD_BUTTON_L3: return "L3";
    case GAMEPAD_BUTTON_R3: return "R3";
    case GAMEPAD_BUTTON_GUIDE: return "Guide/Home";
    case GAMEPAD_BUTTON_DPAD_UP: return "DPad-Up";
    case GAMEPAD_BUTTON_DPAD_DOWN: return "DPad-Down";
    case GAMEPAD_BUTTON_DPAD_LEFT: return "DPad-Left";
    case GAMEPAD_BUTTON_DPAD_RIGHT: return "DPad-Right";
    default: return QString("Unknown(%1)").arg(static_cast<int>(button));
    }
}

QString MonitorWidget::axisName(GamepadAxis axis) const
{
    switch (axis) {
    case GAMEPAD_AXIS_LEFT_X: return "Left-X";
    case GAMEPAD_AXIS_LEFT_Y: return "Left-Y";
    case GAMEPAD_AXIS_RIGHT_X: return "Right-X";
    case GAMEPAD_AXIS_RIGHT_Y: return "Right-Y";
    case GAMEPAD_AXIS_TRIGGER_LEFT: return "Trigger-Left";
    case GAMEPAD_AXIS_TRIGGER_RIGHT: return "Trigger-Right";
    default: return QString("Unknown(%1)").arg(static_cast<int>(axis));
    }
}

QString MonitorWidget::hatDirectionName(int direction) const
{
    switch (direction) {
    case GAMEPAD_HAT_CENTER: return "Center";
    case GAMEPAD_HAT_UP: return "Up";
    case GAMEPAD_HAT_RIGHT: return "Right";
    case GAMEPAD_HAT_DOWN: return "Down";
    case GAMEPAD_HAT_LEFT: return "Left";
    case GAMEPAD_HAT_UP | GAMEPAD_HAT_RIGHT: return "Up-Right";
    case GAMEPAD_HAT_DOWN | GAMEPAD_HAT_RIGHT: return "Down-Right";
    case GAMEPAD_HAT_DOWN | GAMEPAD_HAT_LEFT: return "Down-Left";
    case GAMEPAD_HAT_UP | GAMEPAD_HAT_LEFT: return "Up-Left";
    default: return QString("Unknown(%1)").arg(direction);
    }
}
