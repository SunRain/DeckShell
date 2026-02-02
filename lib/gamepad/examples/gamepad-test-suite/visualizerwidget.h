// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#pragma once

#include <QWidget>
#include <QTimer>
#include <QMap>
#include "../../src/treelandgamepadclient.h"
#include "../../src/treelandgamepaddevice.h"

class VisualizerWidget : public QWidget
{
    Q_OBJECT
    
public:
    explicit VisualizerWidget(TreelandGamepad::TreelandGamepadClient *client,
                             QWidget *parent = nullptr);
    
public Q_SLOTS:
    void setCurrentDevice(int deviceId);
    
protected:
    void paintEvent(QPaintEvent *event) override;
    
private Q_SLOTS:
    void onButtonChanged(TreelandGamepad::GamepadButton button, bool pressed);
    void onAxisChanged(TreelandGamepad::GamepadAxis axis, double value);
    void onHatChanged(int direction);
    void updateDisplay();
    
private:
    void drawGamepad(QPainter &painter);
    void drawButton(QPainter &painter, const QRectF &rect, 
                   const QString &label, bool pressed);
    void drawStick(QPainter &painter, const QPointF &center, 
                  double x, double y, const QString &label);
    void drawTrigger(QPainter &painter, const QRectF &rect, 
                    double value, const QString &label);
    void drawDPad(QPainter &painter, const QPointF &center, int direction);
    void connectDevice(TreelandGamepad::TreelandGamepadDevice *device);
    void disconnectDevice();
    
private:
    TreelandGamepad::TreelandGamepadClient *m_client;
    TreelandGamepad::TreelandGamepadDevice *m_currentDevice = nullptr;
    
    // 缓存状态
    QMap<TreelandGamepad::GamepadButton, bool> m_buttonStates;
    QMap<TreelandGamepad::GamepadAxis, double> m_axisValues;
    int m_hatDirection = 0;
    
    // 更新定时器
    QTimer *m_updateTimer;
};
