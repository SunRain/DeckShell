// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QWidget>
#include <QSlider>
#include <QSpinBox>
#include <QComboBox>
#include <QPushButton>
#include <QTableWidget>
#include <QLabel>
#include "../../src/treelandgamepadclient.h"
#include "../../src/treelandgamepaddevice.h"

class VibrationWidget : public QWidget
{
    Q_OBJECT
    
public:
    explicit VibrationWidget(TreelandGamepad::TreelandGamepadClient *client,
                            QWidget *parent = nullptr);
    
public Q_SLOTS:
    void setCurrentDevice(int deviceId);
    
private Q_SLOTS:
    void onTestVibration();
    void onStopVibration();
    void onPresetSelected(int index);
    void onPlaySequence();
    void onAddStep();
    void onRemoveStep();
    void onWeakSliderChanged(int value);
    void onStrongSliderChanged(int value);
    
private:
    void setupUI();
    void setupPresets();
    
    struct VibrationPreset {
        QString name;
        double weak;
        double strong;
        int duration;
    };
    
    struct VibrationStep {
        double weak;
        double strong;
        int duration;
        int delay;
    };
    
private:
    TreelandGamepad::TreelandGamepadClient *m_client;
    TreelandGamepad::TreelandGamepadDevice *m_currentDevice = nullptr;
    
    // UI控件
    QSlider *m_weakSlider;
    QSlider *m_strongSlider;
    QLabel *m_weakLabel;
    QLabel *m_strongLabel;
    QSpinBox *m_durationSpinBox;
    QComboBox *m_presetCombo;
    QPushButton *m_testButton;
    QPushButton *m_stopButton;
    
    // 序列编辑器
    QTableWidget *m_sequenceTable;
    QPushButton *m_playSequenceButton;
    QPushButton *m_addStepButton;
    QPushButton *m_removeStepButton;
    
    // 预设列表
    QList<VibrationPreset> m_presets;
};
