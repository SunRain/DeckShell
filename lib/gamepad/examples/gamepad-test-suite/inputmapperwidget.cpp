// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "inputmapperwidget.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGroupBox>
#include <QLabel>
#include <QHeaderView>

using namespace TreelandGamepad;

InputMapperWidget::InputMapperWidget(TreelandGamepadClient *client, QWidget *parent)
    : QWidget(parent)
    , m_client(client)
{
    setupUI();
    setupDefaultMappings();
}

void InputMapperWidget::setupUI()
{
    auto *mainLayout = new QVBoxLayout(this);
    
    // 启用/禁用映射
    auto *controlGroup = new QGroupBox("映射控制");
    auto *controlLayout = new QHBoxLayout(controlGroup);
    
    m_enableCheck = new QCheckBox("启用输入映射");
    connect(m_enableCheck, &QCheckBox::toggled, this, &InputMapperWidget::onEnableMapping);
    controlLayout->addWidget(m_enableCheck);
    
    controlLayout->addStretch();
    
    mainLayout->addWidget(controlGroup);
    
    // 映射表
    auto *mappingGroup = new QGroupBox("映射配置");
    auto *mappingLayout = new QVBoxLayout(mappingGroup);
    
    m_mappingTable = new QTableWidget(0, 3);
    m_mappingTable->setHorizontalHeaderLabels(QStringList() 
        << "手柄按钮" << "映射到" << "描述");
    m_mappingTable->horizontalHeader()->setStretchLastSection(true);
    m_mappingTable->setSelectionBehavior(QAbstractItemView::SelectRows);
    mappingLayout->addWidget(m_mappingTable);
    
    // 按钮栏
    auto *buttonLayout = new QHBoxLayout;
    
    m_addButton = new QPushButton("添加映射");
    connect(m_addButton, &QPushButton::clicked, this, &InputMapperWidget::onAddMapping);
    buttonLayout->addWidget(m_addButton);
    
    m_removeButton = new QPushButton("删除映射");
    connect(m_removeButton, &QPushButton::clicked, this, &InputMapperWidget::onRemoveMapping);
    buttonLayout->addWidget(m_removeButton);
    
    m_clearButton = new QPushButton("清空全部");
    connect(m_clearButton, &QPushButton::clicked, this, &InputMapperWidget::onClearMappings);
    buttonLayout->addWidget(m_clearButton);
    
    buttonLayout->addStretch();
    
    mappingLayout->addLayout(buttonLayout);
    
    mainLayout->addWidget(mappingGroup);
    
    // 说明
    auto *infoLabel = new QLabel(
        "输入映射功能允许将手柄按钮映射到键盘按键或鼠标操作。\n"
        "注意：此功能仅作为演示，实际映射需要系统级权限。");
    infoLabel->setWordWrap(true);
    infoLabel->setStyleSheet("QLabel { color: gray; }");
    mainLayout->addWidget(infoLabel);
    
    mainLayout->addStretch();
}

void InputMapperWidget::setupDefaultMappings()
{
    // 添加一些默认映射示例
    struct DefaultMapping {
        QString button;
        QString target;
        QString description;
    };
    
    QList<DefaultMapping> defaults = {
        {"A", "Space", "跳跃"},
        {"B", "Escape", "取消/返回"},
        {"X", "E", "互动"},
        {"Y", "I", "物品栏"},
        {"Start", "Enter", "确认/暂停"},
        {"Select", "Tab", "地图/菜单"},
        {"LB", "Q", "技能1"},
        {"RB", "R", "技能2"},
        {"DPad-Up", "W", "向前移动"},
        {"DPad-Down", "S", "向后移动"},
        {"DPad-Left", "A", "向左移动"},
        {"DPad-Right", "D", "向右移动"},
    };
    
    for (const auto &mapping : defaults) {
        int row = m_mappingTable->rowCount();
        m_mappingTable->insertRow(row);
        m_mappingTable->setItem(row, 0, new QTableWidgetItem(mapping.button));
        m_mappingTable->setItem(row, 1, new QTableWidgetItem(mapping.target));
        m_mappingTable->setItem(row, 2, new QTableWidgetItem(mapping.description));
    }
}

void InputMapperWidget::setCurrentDevice(int deviceId)
{
    if (deviceId < 0) {
        m_currentDevice = nullptr;
        m_enableCheck->setEnabled(false);
        m_enableCheck->setChecked(false);
    } else {
        m_currentDevice = m_client->gamepad(deviceId);
        m_enableCheck->setEnabled(m_currentDevice != nullptr);
    }
}

void InputMapperWidget::onEnableMapping(bool enable)
{
    m_mappingEnabled = enable;
    m_addButton->setEnabled(!enable);
    m_removeButton->setEnabled(!enable);
    m_clearButton->setEnabled(!enable);
    
    if (enable) {
        // 这里应该实现实际的映射逻辑
        // 但由于需要系统权限，这里只是演示
    }
}

void InputMapperWidget::onAddMapping()
{
    int row = m_mappingTable->rowCount();
    m_mappingTable->insertRow(row);
    m_mappingTable->setItem(row, 0, new QTableWidgetItem("Button"));
    m_mappingTable->setItem(row, 1, new QTableWidgetItem("Key"));
    m_mappingTable->setItem(row, 2, new QTableWidgetItem("自定义"));
}

void InputMapperWidget::onRemoveMapping()
{
    int row = m_mappingTable->currentRow();
    if (row >= 0) {
        m_mappingTable->removeRow(row);
    }
}

void InputMapperWidget::onClearMappings()
{
    m_mappingTable->setRowCount(0);
}
