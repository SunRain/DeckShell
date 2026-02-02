// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QMainWindow>
#include <QTabWidget>
#include <QComboBox>
#include <QStatusBar>
#include <QLabel>
#include <QMap>
#include <memory>

#include "../../src/treelandgamepadclient.h"

QT_BEGIN_NAMESPACE
class QTabWidget;
class QComboBox;
class QLabel;
QT_END_NAMESPACE

class MonitorWidget;
class VisualizerWidget;
class VibrationWidget;
class SimpleGameWidget;
class InputMapperWidget;

class GamepadTestSuite : public QMainWindow
{
    Q_OBJECT

public:
    explicit GamepadTestSuite(QWidget *parent = nullptr);
    ~GamepadTestSuite();
    
    void setWaylandSocket(const QString &socketName);

Q_SIGNALS:
    void currentDeviceChanged(int deviceId);

private Q_SLOTS:
    void onConnectionChanged(bool connected);
    void onGamepadAdded(int deviceId, const QString &name);
    void onGamepadRemoved(int deviceId);
    void onDeviceSelectionChanged(int index);
    void showAboutDialog();
    void refreshDevices();
    
private:
    void setupUI();
    void connectSignals();
    void updateStatusBar();
    
private:
    TreelandGamepad::TreelandGamepadClient *m_client;
    QString m_waylandSocket;
    
    // UI组件
    QTabWidget *m_tabWidget;
    QComboBox *m_deviceSelector;
    QLabel *m_connectionStatus;
    
    // 功能模块
    MonitorWidget *m_monitorWidget;
    VisualizerWidget *m_visualizerWidget;
    VibrationWidget *m_vibrationWidget;
    SimpleGameWidget *m_gameWidget;
    InputMapperWidget *m_mapperWidget;
    
    // 设备管理
    QMap<int, TreelandGamepad::TreelandGamepadDevice*> m_devices;
    int m_currentDeviceId = -1;
};
