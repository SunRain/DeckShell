// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QWidget>
#include <QTextEdit>
#include <QPushButton>
#include <QCheckBox>
#include <QLabel>
#include "../../src/treelandgamepadclient.h"
#include "../../src/treelandgamepaddevice.h"

class MonitorWidget : public QWidget
{
    Q_OBJECT
    
public:
    explicit MonitorWidget(TreelandGamepad::TreelandGamepadClient *client, 
                          QWidget *parent = nullptr);
    
public Q_SLOTS:
    void setCurrentDevice(int deviceId);
    
private Q_SLOTS:
    void onButtonEvent(TreelandGamepad::DeckGamepadButtonEvent event);
    void onAxisEvent(TreelandGamepad::DeckGamepadAxisEvent event);
    void onHatEvent(TreelandGamepad::DeckGamepadHatEvent event);
    void clearLog();
    void saveLog();
    void toggleTimestamp(bool enable);
    void toggleRawData(bool enable);
    
private:
    void appendLog(const QString &message);
    QString buttonName(TreelandGamepad::GamepadButton button) const;
    QString axisName(TreelandGamepad::GamepadAxis axis) const;
    QString hatDirectionName(int direction) const;
    void setupUI();
    void connectDevice(TreelandGamepad::TreelandGamepadDevice *device);
    void disconnectDevice();
    
private:
    TreelandGamepad::TreelandGamepadClient *m_client;
    TreelandGamepad::TreelandGamepadDevice *m_currentDevice = nullptr;
    
    // UI控件
    QTextEdit *m_logDisplay;
    QPushButton *m_clearButton;
    QPushButton *m_saveButton;
    QCheckBox *m_timestampCheck;
    QCheckBox *m_rawDataCheck;
    QCheckBox *m_autoScrollCheck;
    
    // 统计信息
    QLabel *m_buttonCountLabel;
    QLabel *m_axisCountLabel;
    QLabel *m_hatCountLabel;
    int m_buttonEventCount = 0;
    int m_axisEventCount = 0;
    int m_hatEventCount = 0;
    
    // 选项
    bool m_showTimestamp = true;
    bool m_showRawData = false;
};
