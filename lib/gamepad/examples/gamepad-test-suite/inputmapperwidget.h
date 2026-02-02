// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QWidget>
#include <QTableWidget>
#include <QCheckBox>
#include <QPushButton>
#include "../../src/treelandgamepadclient.h"
#include "../../src/treelandgamepaddevice.h"

class InputMapperWidget : public QWidget
{
    Q_OBJECT
    
public:
    explicit InputMapperWidget(TreelandGamepad::TreelandGamepadClient *client,
                               QWidget *parent = nullptr);
    
public Q_SLOTS:
    void setCurrentDevice(int deviceId);
    
private Q_SLOTS:
    void onEnableMapping(bool enable);
    void onAddMapping();
    void onRemoveMapping();
    void onClearMappings();
    
private:
    void setupUI();
    void setupDefaultMappings();
    
private:
    TreelandGamepad::TreelandGamepadClient *m_client;
    TreelandGamepad::TreelandGamepadDevice *m_currentDevice = nullptr;
    
    QTableWidget *m_mappingTable;
    QCheckBox *m_enableCheck;
    QPushButton *m_addButton;
    QPushButton *m_removeButton;
    QPushButton *m_clearButton;
    
    bool m_mappingEnabled = false;
};
