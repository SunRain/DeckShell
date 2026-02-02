// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "visualizerwidget.h"
#include <QPainter>
#include <QPaintEvent>
#include <cmath>

using namespace TreelandGamepad;
using namespace deckshell::deckgamepad;

VisualizerWidget::VisualizerWidget(TreelandGamepadClient *client, QWidget *parent)
    : QWidget(parent)
    , m_client(client)
    , m_updateTimer(new QTimer(this))
{
    // 设置背景
    setAutoFillBackground(true);
    QPalette pal = palette();
    pal.setColor(QPalette::Window, Qt::white);
    setPalette(pal);
    
    // 初始化状态
    for (int i = 0; i < GAMEPAD_BUTTON_MAX; ++i) {
        m_buttonStates[static_cast<GamepadButton>(i)] = false;
    }
    for (int i = 0; i < GAMEPAD_AXIS_MAX; ++i) {
        m_axisValues[static_cast<GamepadAxis>(i)] = 0.0;
    }
    
    // 设置更新定时器
    connect(m_updateTimer, &QTimer::timeout, this, &VisualizerWidget::updateDisplay);
    m_updateTimer->start(16); // ~60 FPS
}

void VisualizerWidget::setCurrentDevice(int deviceId)
{
    disconnectDevice();
    
    if (deviceId < 0) {
        m_currentDevice = nullptr;
        update();
        return;
    }
    
    m_currentDevice = m_client->gamepad(deviceId);
    if (m_currentDevice) {
        connectDevice(m_currentDevice);
    }
    update();
}

void VisualizerWidget::connectDevice(TreelandGamepadDevice *device)
{
    if (!device) return;
    
    connect(device, &TreelandGamepadDevice::buttonChanged,
            this, &VisualizerWidget::onButtonChanged);
    connect(device, &TreelandGamepadDevice::axisChanged,
            this, &VisualizerWidget::onAxisChanged);
    connect(device, &TreelandGamepadDevice::hatChanged,
            this, &VisualizerWidget::onHatChanged);
}

void VisualizerWidget::disconnectDevice()
{
    if (!m_currentDevice) return;
    disconnect(m_currentDevice, nullptr, this, nullptr);
}

void VisualizerWidget::onButtonChanged(GamepadButton button, bool pressed)
{
    m_buttonStates[button] = pressed;
}

void VisualizerWidget::onAxisChanged(GamepadAxis axis, double value)
{
    m_axisValues[axis] = value;
}

void VisualizerWidget::onHatChanged(int direction)
{
    m_hatDirection = direction;
}

void VisualizerWidget::updateDisplay()
{
    update();
}

void VisualizerWidget::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event)
    
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);
    
    drawGamepad(painter);
}

void VisualizerWidget::drawGamepad(QPainter &painter)
{
    if (!m_currentDevice) {
        painter.setPen(Qt::black);
        painter.setFont(QFont("Arial", 16));
        painter.drawText(rect(), Qt::AlignCenter, "无设备连接");
        return;
    }
    
    // 计算缩放
    const int baseWidth = 800;
    const int baseHeight = 600;
    const qreal scale = qMin(width() / qreal(baseWidth), 
                             height() / qreal(baseHeight));
    
    painter.save();
    painter.translate(width() / 2, height() / 2);
    painter.scale(scale, scale);
    painter.translate(-baseWidth / 2, -baseHeight / 2);
    
    // 绘制手柄主体
    painter.setPen(QPen(Qt::darkGray, 3));
    painter.setBrush(QColor(240, 240, 240));
    
    // 左侧手柄部分
    QRectF leftBody(50, 200, 250, 250);
    painter.drawEllipse(leftBody);
    
    // 右侧手柄部分
    QRectF rightBody(500, 200, 250, 250);
    painter.drawEllipse(rightBody);
    
    // 中间连接部分
    QRectF centerBody(250, 250, 300, 150);
    painter.drawRoundedRect(centerBody, 20, 20);
    
    // 绘制左摇杆
    QPointF leftStickPos(175, 325);
    double leftX = m_axisValues.value(GAMEPAD_AXIS_LEFT_X, 0.0);
    double leftY = m_axisValues.value(GAMEPAD_AXIS_LEFT_Y, 0.0);
    drawStick(painter, leftStickPos, leftX, leftY, "L");
    
    // 绘制右摇杆
    QPointF rightStickPos(625, 325);
    double rightX = m_axisValues.value(GAMEPAD_AXIS_RIGHT_X, 0.0);
    double rightY = m_axisValues.value(GAMEPAD_AXIS_RIGHT_Y, 0.0);
    drawStick(painter, rightStickPos, rightX, rightY, "R");
    
    // 绘制ABXY按钮
    const int buttonSize = 40;
    drawButton(painter, QRectF(625, 225, buttonSize, buttonSize), "Y", 
              m_buttonStates.value(GAMEPAD_BUTTON_Y));
    drawButton(painter, QRectF(675, 275, buttonSize, buttonSize), "B", 
              m_buttonStates.value(GAMEPAD_BUTTON_B));
    drawButton(painter, QRectF(625, 325, buttonSize, buttonSize), "A", 
              m_buttonStates.value(GAMEPAD_BUTTON_A));
    drawButton(painter, QRectF(575, 275, buttonSize, buttonSize), "X", 
              m_buttonStates.value(GAMEPAD_BUTTON_X));
    
    // 绘制肩键
    drawButton(painter, QRectF(150, 150, 80, 30), "LB", 
              m_buttonStates.value(GAMEPAD_BUTTON_L1));
    drawButton(painter, QRectF(570, 150, 80, 30), "RB", 
              m_buttonStates.value(GAMEPAD_BUTTON_R1));
    
    // LT/RT按钮
    if (m_buttonStates.value(GAMEPAD_BUTTON_L2)) {
        drawButton(painter, QRectF(150, 110, 80, 30), "LT", true);
    }
    if (m_buttonStates.value(GAMEPAD_BUTTON_R2)) {
        drawButton(painter, QRectF(570, 110, 80, 30), "RT", true);
    }
    
    // 绘制扳机进度
    double ltValue = m_axisValues.value(GAMEPAD_AXIS_TRIGGER_LEFT, 0.0);
    double rtValue = m_axisValues.value(GAMEPAD_AXIS_TRIGGER_RIGHT, 0.0);
    drawTrigger(painter, QRectF(100, 90, 30, 100), ltValue, "LT");
    drawTrigger(painter, QRectF(670, 90, 30, 100), rtValue, "RT");
    
    // 绘制方向键
    drawDPad(painter, QPointF(175, 250), m_hatDirection);
    
    // 绘制功能键
    drawButton(painter, QRectF(320, 300, 60, 30), "SELECT", 
              m_buttonStates.value(GAMEPAD_BUTTON_SELECT));
    drawButton(painter, QRectF(420, 300, 60, 30), "START", 
              m_buttonStates.value(GAMEPAD_BUTTON_START));
    drawButton(painter, QRectF(370, 250, 60, 40), "GUIDE", 
              m_buttonStates.value(GAMEPAD_BUTTON_GUIDE));
    
    // L3/R3状态
    if (m_buttonStates.value(GAMEPAD_BUTTON_L3)) {
        painter.setPen(QPen(Qt::red, 3));
        painter.drawEllipse(leftStickPos, 50, 50);
    }
    if (m_buttonStates.value(GAMEPAD_BUTTON_R3)) {
        painter.setPen(QPen(Qt::red, 3));
        painter.drawEllipse(rightStickPos, 50, 50);
    }
    
    // 绘制设备信息
    painter.setPen(Qt::black);
    painter.setFont(QFont("Arial", 12));
    painter.drawText(QRectF(50, 50, 700, 30), Qt::AlignCenter, 
                    QString("设备: %1 (ID: %2)")
                    .arg(m_currentDevice->name())
                    .arg(m_currentDevice->deviceId()));
    
    painter.restore();
}

void VisualizerWidget::drawButton(QPainter &painter, const QRectF &rect, 
                                  const QString &label, bool pressed)
{
    painter.save();
    
    if (pressed) {
        painter.setPen(QPen(Qt::darkRed, 2));
        painter.setBrush(QColor(255, 100, 100));
    } else {
        painter.setPen(QPen(Qt::darkGray, 2));
        painter.setBrush(Qt::white);
    }
    
    painter.drawEllipse(rect);
    
    painter.setPen(pressed ? Qt::white : Qt::black);
    painter.setFont(QFont("Arial", 10, QFont::Bold));
    painter.drawText(rect, Qt::AlignCenter, label);
    
    painter.restore();
}

void VisualizerWidget::drawStick(QPainter &painter, const QPointF &center, 
                                 double x, double y, const QString &label)
{
    painter.save();
    
    // 外圈
    painter.setPen(QPen(Qt::black, 2));
    painter.setBrush(QColor(200, 200, 200));
    painter.drawEllipse(center, 50, 50);
    
    // 摇杆位置
    QPointF stickPos = center + QPointF(x * 30, y * 30);
    
    painter.setPen(QPen(Qt::darkBlue, 2));
    painter.setBrush(QColor(100, 150, 255));
    painter.drawEllipse(stickPos, 20, 20);
    
    // 标签
    painter.setPen(Qt::white);
    painter.setFont(QFont("Arial", 10, QFont::Bold));
    painter.drawText(QRectF(stickPos.x() - 20, stickPos.y() - 10, 40, 20), 
                    Qt::AlignCenter, label);
    
    painter.restore();
}

void VisualizerWidget::drawTrigger(QPainter &painter, const QRectF &rect, 
                                   double value, const QString &label)
{
    painter.save();
    
    // 背景
    painter.setPen(QPen(Qt::black, 2));
    painter.setBrush(Qt::lightGray);
    painter.drawRect(rect);
    
    // 进度
    if (value > 0) {
        QRectF fillRect = rect;
        fillRect.setHeight(rect.height() * std::abs(value));
        fillRect.moveTop(rect.bottom() - fillRect.height());
        
        painter.setBrush(QColor(100, 255, 100));
        painter.drawRect(fillRect);
    }
    
    // 标签
    painter.setPen(Qt::black);
    painter.setFont(QFont("Arial", 8));
    painter.drawText(rect, Qt::AlignCenter, label);
    
    // 数值
    painter.drawText(rect.adjusted(0, rect.height() - 20, 0, 0), 
                    Qt::AlignCenter, 
                    QString::number(value, 'f', 2));
    
    painter.restore();
}

void VisualizerWidget::drawDPad(QPainter &painter, const QPointF &center, int direction)
{
    painter.save();
    
    const int size = 30;
    
    // 上
    QPolygonF upArrow;
    upArrow << center + QPointF(0, -size)
            << center + QPointF(-10, -size + 10)
            << center + QPointF(10, -size + 10);
    painter.setPen(QPen(Qt::black, 2));
    painter.setBrush((direction & GAMEPAD_HAT_UP) ? Qt::red : Qt::lightGray);
    painter.drawPolygon(upArrow);
    
    // 下
    QPolygonF downArrow;
    downArrow << center + QPointF(0, size)
              << center + QPointF(-10, size - 10)
              << center + QPointF(10, size - 10);
    painter.setBrush((direction & GAMEPAD_HAT_DOWN) ? Qt::red : Qt::lightGray);
    painter.drawPolygon(downArrow);
    
    // 左
    QPolygonF leftArrow;
    leftArrow << center + QPointF(-size, 0)
              << center + QPointF(-size + 10, -10)
              << center + QPointF(-size + 10, 10);
    painter.setBrush((direction & GAMEPAD_HAT_LEFT) ? Qt::red : Qt::lightGray);
    painter.drawPolygon(leftArrow);
    
    // 右
    QPolygonF rightArrow;
    rightArrow << center + QPointF(size, 0)
               << center + QPointF(size - 10, -10)
               << center + QPointF(size - 10, 10);
    painter.setBrush((direction & GAMEPAD_HAT_RIGHT) ? Qt::red : Qt::lightGray);
    painter.drawPolygon(rightArrow);
    
    // 中心圆
    painter.setBrush(Qt::darkGray);
    painter.drawEllipse(center, 10, 10);
    
    painter.restore();
}
