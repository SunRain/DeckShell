// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "gamepadtestsuite.h"
#include "monitorwidget.h"
#include "visualizerwidget.h"
#include "vibrationwidget.h"
#include "simplegamewidget.h"
#include "inputmapperwidget.h"

#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QMenuBar>
#include <QMenu>
#include <QMessageBox>
#include <QTimer>
#include <QPushButton>
#include <QApplication>
#include <QDebug>

GamepadTestSuite::GamepadTestSuite(QWidget *parent)
    : QMainWindow(parent)
    , m_client(new TreelandGamepad::TreelandGamepadClient(this))
{
    setupUI();
    connectSignals();
}

GamepadTestSuite::~GamepadTestSuite()
{
    m_client->disconnectFromCompositor();
}

void GamepadTestSuite::setWaylandSocket(const QString &socketName)
{
    m_waylandSocket = socketName;
}

void GamepadTestSuite::setupUI()
{
    // 创建中心部件
    auto *centralWidget = new QWidget(this);
    setCentralWidget(centralWidget);
    
    // 主布局
    auto *mainLayout = new QVBoxLayout(centralWidget);
    
    // 设备选择器栏
    auto *deviceBar = new QWidget;
    auto *deviceLayout = new QHBoxLayout(deviceBar);
    deviceLayout->setContentsMargins(5, 5, 5, 5);
    
    deviceLayout->addWidget(new QLabel("当前设备:"));
    m_deviceSelector = new QComboBox;
    m_deviceSelector->setMinimumWidth(200);
    m_deviceSelector->addItem("无设备", -1);
    deviceLayout->addWidget(m_deviceSelector);
    
    m_connectionStatus = new QLabel("未连接");
    m_connectionStatus->setStyleSheet("QLabel { color: red; font-weight: bold; }");
    deviceLayout->addWidget(m_connectionStatus);
    
    deviceLayout->addStretch();
    
    auto *refreshButton = new QPushButton("刷新设备");
    connect(refreshButton, &QPushButton::clicked, this, &GamepadTestSuite::refreshDevices);
    deviceLayout->addWidget(refreshButton);
    
    mainLayout->addWidget(deviceBar);
    
    // 创建标签页
    m_tabWidget = new QTabWidget;
    
    // 添加各个功能模块
    m_monitorWidget = new MonitorWidget(m_client);
    m_tabWidget->addTab(m_monitorWidget, "事件监视器");
    
    m_visualizerWidget = new VisualizerWidget(m_client);
    m_tabWidget->addTab(m_visualizerWidget, "可视化");
    
    m_vibrationWidget = new VibrationWidget(m_client);
    m_tabWidget->addTab(m_vibrationWidget, "振动测试");
    
    m_gameWidget = new SimpleGameWidget(m_client);
    m_tabWidget->addTab(m_gameWidget, "示例游戏");
    
    m_mapperWidget = new InputMapperWidget(m_client);
    m_tabWidget->addTab(m_mapperWidget, "输入映射");
    
    mainLayout->addWidget(m_tabWidget);
    
    // 创建菜单栏
    auto *menuBar = this->menuBar();
    
    // 文件菜单
    auto *fileMenu = menuBar->addMenu("文件(&F)");
    auto *exitAction = fileMenu->addAction("退出(&X)");
    connect(exitAction, &QAction::triggered, this, &QWidget::close);
    
    // 设备菜单
    auto *deviceMenu = menuBar->addMenu("设备(&D)");
    auto *connectAction = deviceMenu->addAction("连接到Compositor(&C)");
    connect(connectAction, &QAction::triggered, [this]() {
        if (!m_client->isConnected()) {
            if (!m_client->connectToCompositor(m_waylandSocket)) {
                QMessageBox::warning(this, "连接失败", 
                    "无法连接到Wayland compositor。\n"
                    "请确保compositor支持treeland-gamepad-v1协议。");
            }
        }
    });
    
    auto *disconnectAction = deviceMenu->addAction("断开连接(&D)");
    connect(disconnectAction, &QAction::triggered, [this]() {
        m_client->disconnectFromCompositor();
    });
    
    deviceMenu->addSeparator();
    auto *refreshAction = deviceMenu->addAction("刷新设备列表(&R)");
    refreshAction->setShortcut(QKeySequence::Refresh);
    connect(refreshAction, &QAction::triggered, this, &GamepadTestSuite::refreshDevices);
    
    // 帮助菜单
    auto *helpMenu = menuBar->addMenu("帮助(&H)");
    auto *aboutAction = helpMenu->addAction("关于(&A)");
    connect(aboutAction, &QAction::triggered, this, &GamepadTestSuite::showAboutDialog);
    
    auto *aboutQtAction = helpMenu->addAction("关于Qt(&Q)");
    connect(aboutQtAction, &QAction::triggered, qApp, &QApplication::aboutQt);
    
    // 状态栏
    statusBar()->showMessage("等待连接到Wayland compositor...");
    
    // 窗口设置
    setWindowTitle("Treeland Gamepad Test Suite");
    resize(1200, 800);
    
    // 尝试自动连接
    QTimer::singleShot(100, [this]() {
        if (!m_client->connectToCompositor(m_waylandSocket)) {
            qWarning() << "自动连接失败，请手动连接";
        }
    });
}

void GamepadTestSuite::connectSignals()
{
    // 客户端信号
    connect(m_client, &TreelandGamepad::TreelandGamepadClient::connectedChanged,
            this, &GamepadTestSuite::onConnectionChanged);
    connect(m_client, &TreelandGamepad::TreelandGamepadClient::gamepadAdded,
            this, &GamepadTestSuite::onGamepadAdded);
    connect(m_client, &TreelandGamepad::TreelandGamepadClient::gamepadRemoved,
            this, &GamepadTestSuite::onGamepadRemoved);
    
    // 设备选择器信号
    connect(m_deviceSelector, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &GamepadTestSuite::onDeviceSelectionChanged);
    
    // 传递当前设备改变信号到各个模块
    connect(this, &GamepadTestSuite::currentDeviceChanged,
            m_monitorWidget, &MonitorWidget::setCurrentDevice);
    connect(this, &GamepadTestSuite::currentDeviceChanged,
            m_visualizerWidget, &VisualizerWidget::setCurrentDevice);
    connect(this, &GamepadTestSuite::currentDeviceChanged,
            m_vibrationWidget, &VibrationWidget::setCurrentDevice);
    connect(this, &GamepadTestSuite::currentDeviceChanged,
            m_gameWidget, &SimpleGameWidget::setCurrentDevice);
    connect(this, &GamepadTestSuite::currentDeviceChanged,
            m_mapperWidget, &InputMapperWidget::setCurrentDevice);
}

void GamepadTestSuite::onConnectionChanged(bool connected)
{
    if (connected) {
        m_connectionStatus->setText("已连接");
        m_connectionStatus->setStyleSheet("QLabel { color: green; font-weight: bold; }");
        statusBar()->showMessage("已连接到Wayland compositor");
    } else {
        m_connectionStatus->setText("未连接");
        m_connectionStatus->setStyleSheet("QLabel { color: red; font-weight: bold; }");
        statusBar()->showMessage("未连接到Wayland compositor");
        
        // 清空设备列表
        m_deviceSelector->clear();
        m_deviceSelector->addItem("无设备", -1);
        m_devices.clear();
        m_currentDeviceId = -1;
    }
    
    updateStatusBar();
}

void GamepadTestSuite::onGamepadAdded(int deviceId, const QString &name)
{
    qDebug() << "Gamepad added:" << deviceId << name;
    
    // 获取设备对象
    auto *device = m_client->gamepad(deviceId);
    if (!device) {
        qWarning() << "Failed to get device object for" << deviceId;
        return;
    }
    
    // 保存设备
    m_devices[deviceId] = device;
    
    // 添加到选择器
    m_deviceSelector->addItem(QString("%1 (ID: %2)").arg(name).arg(deviceId), deviceId);
    
    // 如果是第一个设备，自动选中
    if (m_devices.size() == 1) {
        m_deviceSelector->setCurrentIndex(1); // 跳过"无设备"项
    }
    
    updateStatusBar();
    statusBar()->showMessage(QString("设备已连接: %1").arg(name), 3000);
}

void GamepadTestSuite::onGamepadRemoved(int deviceId)
{
    qDebug() << "Gamepad removed:" << deviceId;
    
    // 从选择器中移除
    for (int i = 0; i < m_deviceSelector->count(); ++i) {
        if (m_deviceSelector->itemData(i).toInt() == deviceId) {
            m_deviceSelector->removeItem(i);
            break;
        }
    }
    
    // 移除设备
    m_devices.remove(deviceId);
    
    // 如果是当前设备，重置
    if (deviceId == m_currentDeviceId) {
        m_currentDeviceId = -1;
        if (m_devices.isEmpty()) {
            m_deviceSelector->setCurrentIndex(0); // 选择"无设备"
        } else {
            m_deviceSelector->setCurrentIndex(1); // 选择第一个可用设备
        }
    }
    
    updateStatusBar();
    statusBar()->showMessage("设备已断开", 3000);
}

void GamepadTestSuite::onDeviceSelectionChanged(int index)
{
    if (index < 0) return;
    
    int deviceId = m_deviceSelector->itemData(index).toInt();
    m_currentDeviceId = deviceId;
    
    qDebug() << "Current device changed to:" << deviceId;
    Q_EMIT currentDeviceChanged(deviceId);
    
    updateStatusBar();
}

void GamepadTestSuite::showAboutDialog()
{
    QMessageBox::about(this, "关于 Gamepad Test Suite",
        "<h2>Treeland Gamepad Test Suite</h2>"
        "<p>版本: 1.0.0</p>"
        "<p>一个用于测试和演示Treeland Gamepad Wayland协议的综合工具。</p>"
        "<p>功能包括:</p>"
        "<ul>"
        "<li>事件监视器 - 实时显示所有输入事件</li>"
        "<li>可视化 - 图形化展示手柄状态</li>"
        "<li>振动测试 - 测试振动反馈效果</li>"
        "<li>示例游戏 - 演示游戏中的应用</li>"
        "<li>输入映射 - 将手柄映射到键盘/鼠标</li>"
        "</ul>"
        "<p>Copyright (C) 2025 UnionTech Software Technology Co., Ltd.</p>");
}

void GamepadTestSuite::refreshDevices()
{
    const auto deviceIds = m_client->availableGamepads();

    // Build an updated device map
    QMap<int, TreelandGamepad::TreelandGamepadDevice*> newDevices;
    for (int deviceId : deviceIds) {
        if (auto *device = m_client->gamepad(deviceId)) {
            newDevices.insert(deviceId, device);
        }
    }

    // Rebuild selector contents
    m_deviceSelector->blockSignals(true);
    m_deviceSelector->clear();
    m_deviceSelector->addItem("无设备", -1);
    for (auto it = newDevices.cbegin(); it != newDevices.cend(); ++it) {
        const int deviceId = it.key();
        const QString name = it.value()->name();
        m_deviceSelector->addItem(QString("%1 (ID: %2)").arg(name).arg(deviceId), deviceId);
    }
    m_deviceSelector->blockSignals(false);

    m_devices = newDevices;

    // Select appropriate device
    int targetIndex = 0; // "无设备"
    if (!newDevices.isEmpty()) {
        int existingIndex = m_deviceSelector->findData(m_currentDeviceId);
        if (existingIndex > 0) {
            targetIndex = existingIndex;
        } else {
            targetIndex = 1; // first real device
        }
    }

    m_deviceSelector->setCurrentIndex(targetIndex);

    statusBar()->showMessage(QString("发现 %1 个设备").arg(deviceIds.size()), 2000);
    updateStatusBar();
}

void GamepadTestSuite::updateStatusBar()
{
    QString statusText = QString("连接状态: %1 | 设备数: %2")
        .arg(m_client->isConnected() ? "已连接" : "未连接")
        .arg(m_devices.size());
    
    if (m_currentDeviceId >= 0) {
        statusText += QString(" | 当前设备ID: %1").arg(m_currentDeviceId);
    }
    
    statusBar()->showMessage(statusText);
}
