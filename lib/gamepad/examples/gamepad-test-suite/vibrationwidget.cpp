// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "vibrationwidget.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QGroupBox>
#include <QLabel>
#include <QThread>
#include <QHeaderView>

using namespace TreelandGamepad;

VibrationWidget::VibrationWidget(TreelandGamepadClient *client, QWidget *parent)
    : QWidget(parent)
    , m_client(client)
{
    setupPresets();
    setupUI();
}

void VibrationWidget::setupUI()
{
    auto *mainLayout = new QVBoxLayout(this);
    
    // 预设选择
    auto *presetGroup = new QGroupBox("振动预设");
    auto *presetLayout = new QHBoxLayout(presetGroup);
    
    presetLayout->addWidget(new QLabel("选择预设:"));
    m_presetCombo = new QComboBox;
    for (const auto &preset : m_presets) {
        m_presetCombo->addItem(preset.name);
    }
    connect(m_presetCombo, QOverload<int>::of(&QComboBox::currentIndexChanged),
            this, &VibrationWidget::onPresetSelected);
    presetLayout->addWidget(m_presetCombo);
    presetLayout->addStretch();
    
    mainLayout->addWidget(presetGroup);
    
    // 自定义控制
    auto *customGroup = new QGroupBox("自定义振动");
    auto *customLayout = new QGridLayout(customGroup);
    
    // 弱马达
    customLayout->addWidget(new QLabel("弱马达:"), 0, 0);
    m_weakSlider = new QSlider(Qt::Horizontal);
    m_weakSlider->setRange(0, 100);
    m_weakSlider->setValue(0);
    connect(m_weakSlider, &QSlider::valueChanged, 
            this, &VibrationWidget::onWeakSliderChanged);
    customLayout->addWidget(m_weakSlider, 0, 1);
    m_weakLabel = new QLabel("0%");
    m_weakLabel->setMinimumWidth(40);
    customLayout->addWidget(m_weakLabel, 0, 2);
    
    // 强马达
    customLayout->addWidget(new QLabel("强马达:"), 1, 0);
    m_strongSlider = new QSlider(Qt::Horizontal);
    m_strongSlider->setRange(0, 100);
    m_strongSlider->setValue(0);
    connect(m_strongSlider, &QSlider::valueChanged,
            this, &VibrationWidget::onStrongSliderChanged);
    customLayout->addWidget(m_strongSlider, 1, 1);
    m_strongLabel = new QLabel("0%");
    m_strongLabel->setMinimumWidth(40);
    customLayout->addWidget(m_strongLabel, 1, 2);
    
    // 持续时间
    customLayout->addWidget(new QLabel("持续时间:"), 2, 0);
    m_durationSpinBox = new QSpinBox;
    m_durationSpinBox->setRange(0, 10000);
    m_durationSpinBox->setValue(1000);
    m_durationSpinBox->setSuffix(" ms");
    m_durationSpinBox->setSingleStep(100);
    customLayout->addWidget(m_durationSpinBox, 2, 1);
    
    mainLayout->addWidget(customGroup);
    
    // 控制按钮
    auto *buttonLayout = new QHBoxLayout;
    m_testButton = new QPushButton("测试振动");
    m_testButton->setMinimumHeight(40);
    connect(m_testButton, &QPushButton::clicked, this, &VibrationWidget::onTestVibration);
    buttonLayout->addWidget(m_testButton);
    
    m_stopButton = new QPushButton("停止振动");
    m_stopButton->setMinimumHeight(40);
    connect(m_stopButton, &QPushButton::clicked, this, &VibrationWidget::onStopVibration);
    buttonLayout->addWidget(m_stopButton);
    
    mainLayout->addLayout(buttonLayout);
    
    // 序列编辑器
    auto *sequenceGroup = new QGroupBox("振动序列");
    auto *sequenceLayout = new QVBoxLayout(sequenceGroup);
    
    m_sequenceTable = new QTableWidget(0, 4);
    m_sequenceTable->setHorizontalHeaderLabels(QStringList() 
        << "弱马达" << "强马达" << "持续时间(ms)" << "延迟(ms)");
    m_sequenceTable->horizontalHeader()->setStretchLastSection(true);
    sequenceLayout->addWidget(m_sequenceTable);
    
    auto *sequenceButtonLayout = new QHBoxLayout;
    m_addStepButton = new QPushButton("添加步骤");
    connect(m_addStepButton, &QPushButton::clicked, this, &VibrationWidget::onAddStep);
    sequenceButtonLayout->addWidget(m_addStepButton);
    
    m_removeStepButton = new QPushButton("删除步骤");
    connect(m_removeStepButton, &QPushButton::clicked, this, &VibrationWidget::onRemoveStep);
    sequenceButtonLayout->addWidget(m_removeStepButton);
    
    m_playSequenceButton = new QPushButton("播放序列");
    connect(m_playSequenceButton, &QPushButton::clicked, this, &VibrationWidget::onPlaySequence);
    sequenceButtonLayout->addWidget(m_playSequenceButton);
    
    sequenceLayout->addLayout(sequenceButtonLayout);
    
    mainLayout->addWidget(sequenceGroup);
    mainLayout->addStretch();
}

void VibrationWidget::setupPresets()
{
    m_presets.append({"无振动", 0.0, 0.0, 0});
    m_presets.append({"轻触", 0.3, 0.0, 50});
    m_presets.append({"中等", 0.5, 0.5, 200});
    m_presets.append({"强烈", 0.7, 1.0, 500});
    m_presets.append({"脉冲", 0.0, 1.0, 100});
    m_presets.append({"渐进", 0.3, 0.7, 1000});
    m_presets.append({"双重", 1.0, 1.0, 300});
    m_presets.append({"仅弱马达", 1.0, 0.0, 500});
    m_presets.append({"仅强马达", 0.0, 1.0, 500});
}

void VibrationWidget::setCurrentDevice(int deviceId)
{
    if (deviceId < 0) {
        m_currentDevice = nullptr;
        m_testButton->setEnabled(false);
        m_stopButton->setEnabled(false);
        m_playSequenceButton->setEnabled(false);
        return;
    }
    
    m_currentDevice = m_client->gamepad(deviceId);
    bool enabled = (m_currentDevice != nullptr);
    m_testButton->setEnabled(enabled);
    m_stopButton->setEnabled(enabled);
    m_playSequenceButton->setEnabled(enabled);
}

void VibrationWidget::onTestVibration()
{
    if (!m_currentDevice) return;
    
    double weak = m_weakSlider->value() / 100.0;
    double strong = m_strongSlider->value() / 100.0;
    int duration = m_durationSpinBox->value();
    
    m_currentDevice->setVibration(weak, strong, duration);
}

void VibrationWidget::onStopVibration()
{
    if (!m_currentDevice) return;
    m_currentDevice->stopVibration();
}

void VibrationWidget::onPresetSelected(int index)
{
    if (index < 0 || index >= m_presets.size()) return;
    
    const auto &preset = m_presets[index];
    m_weakSlider->setValue(preset.weak * 100);
    m_strongSlider->setValue(preset.strong * 100);
    m_durationSpinBox->setValue(preset.duration);
}

void VibrationWidget::onPlaySequence()
{
    if (!m_currentDevice) return;
    
    // 播放序列中的每个步骤
    for (int i = 0; i < m_sequenceTable->rowCount(); ++i) {
        double weak = m_sequenceTable->item(i, 0)->text().toDouble();
        double strong = m_sequenceTable->item(i, 1)->text().toDouble();
        int duration = m_sequenceTable->item(i, 2)->text().toInt();
        int delay = m_sequenceTable->item(i, 3)->text().toInt();
        
        m_currentDevice->setVibration(weak, strong, duration);
        QThread::msleep(duration + delay);
    }
}

void VibrationWidget::onAddStep()
{
    int row = m_sequenceTable->rowCount();
    m_sequenceTable->insertRow(row);
    
    m_sequenceTable->setItem(row, 0, new QTableWidgetItem(QString::number(m_weakSlider->value() / 100.0)));
    m_sequenceTable->setItem(row, 1, new QTableWidgetItem(QString::number(m_strongSlider->value() / 100.0)));
    m_sequenceTable->setItem(row, 2, new QTableWidgetItem(QString::number(m_durationSpinBox->value())));
    m_sequenceTable->setItem(row, 3, new QTableWidgetItem("100"));
}

void VibrationWidget::onRemoveStep()
{
    int row = m_sequenceTable->currentRow();
    if (row >= 0) {
        m_sequenceTable->removeRow(row);
    }
}

void VibrationWidget::onWeakSliderChanged(int value)
{
    m_weakLabel->setText(QString("%1%").arg(value));
}

void VibrationWidget::onStrongSliderChanged(int value)
{
    m_strongLabel->setText(QString("%1%").arg(value));
}
