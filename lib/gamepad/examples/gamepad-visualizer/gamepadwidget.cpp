// Copyright (C) 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "gamepadwidget.h"
#include <deckshell/deckgamepad/core/deckgamepad.h>

#include <QPainter>
#include <QPaintEvent>
#include <QDebug>

DECKGAMEPAD_USE_NAMESPACE

GamepadWidget::GamepadWidget(QWidget *parent)
    : QWidget(parent)
    , m_hatValue(GAMEPAD_HAT_CENTER)
{
    setMinimumSize(600, 400);
    reset();
}

GamepadWidget::~GamepadWidget()
{
}

void GamepadWidget::setButtonState(uint32_t button, bool pressed)
{
    m_buttonStates[button] = pressed;
    update();
}

void GamepadWidget::setAxisValue(uint32_t axis, double value)
{
    m_axisValues[axis] = value;
    update();
}

void GamepadWidget::setHatValue(int32_t value)
{
    m_hatValue = value;
    update();
}

void GamepadWidget::reset()
{
    m_buttonStates.clear();
    m_axisValues.clear();
    m_hatValue = GAMEPAD_HAT_CENTER;
    update();
}

void GamepadWidget::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event);

    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    drawBackground(painter);
    drawController(painter);
    drawTriggers(painter);
    drawButtons(painter);
    drawJoysticks(painter);
    drawDPad(painter);
    drawLabels(painter);
}

void GamepadWidget::drawBackground(QPainter &painter)
{
    painter.fillRect(rect(), QColor(240, 240, 245));
}

void GamepadWidget::drawController(QPainter &painter)
{
    int w = width();
    int h = height();

    // Draw controller body outline
    painter.setPen(QPen(QColor(80, 80, 100), 3));
    painter.setBrush(QColor(200, 200, 210));

    // Main body
    QRect body(w * 0.15, h * 0.3, w * 0.7, h * 0.5);
    painter.drawRoundedRect(body, 20, 20);

    // Left grip
    QRect leftGrip(w * 0.1, h * 0.5, w * 0.15, h * 0.3);
    painter.drawRoundedRect(leftGrip, 15, 15);

    // Right grip
    QRect rightGrip(w * 0.75, h * 0.5, w * 0.15, h * 0.3);
    painter.drawRoundedRect(rightGrip, 15, 15);
}

void GamepadWidget::drawButtons(QPainter &painter)
{
    int w = width();
    int h = height();

    // Face buttons (A, B, X, Y) - Xbox layout
    struct ButtonInfo {
        uint32_t code;
        QPointF center;
        QString label;
        QColor color;
    };

    QVector<ButtonInfo> faceButtons = {
        {GAMEPAD_BUTTON_A, QPointF(w * 0.75, h * 0.50), "A", QColor(100, 200, 100)},  // Bottom
        {GAMEPAD_BUTTON_B, QPointF(w * 0.80, h * 0.45), "B", QColor(200, 100, 100)},  // Right
        {GAMEPAD_BUTTON_X, QPointF(w * 0.70, h * 0.45), "X", QColor(100, 150, 255)},  // Left
        {GAMEPAD_BUTTON_Y, QPointF(w * 0.75, h * 0.40), "Y", QColor(255, 200, 100)},  // Top
    };

    for (const auto &btn : faceButtons) {
        bool pressed = m_buttonStates.value(btn.code, false);

        painter.setPen(QPen(QColor(60, 60, 80), 2));
        painter.setBrush(pressed ? btn.color : btn.color.lighter(150));

        painter.drawEllipse(btn.center, 20, 20);

        painter.setPen(Qt::black);
        painter.setFont(QFont("Arial", 10, QFont::Bold));
        painter.drawText(QRectF(btn.center.x() - 20, btn.center.y() - 20, 40, 40),
                        Qt::AlignCenter, btn.label);
    }

    // Shoulder buttons
    QVector<ButtonInfo> shoulderButtons = {
        {GAMEPAD_BUTTON_L1, QPointF(w * 0.25, h * 0.25), "L1", QColor(180, 180, 180)},
        {GAMEPAD_BUTTON_R1, QPointF(w * 0.75, h * 0.25), "R1", QColor(180, 180, 180)},
    };

    for (const auto &btn : shoulderButtons) {
        bool pressed = m_buttonStates.value(btn.code, false);

        painter.setPen(QPen(QColor(60, 60, 80), 2));
        painter.setBrush(pressed ? QColor(100, 255, 100) : btn.color);

        QRectF rect(btn.center.x() - 30, btn.center.y() - 10, 60, 20);
        painter.drawRoundedRect(rect, 5, 5);

        painter.setPen(Qt::black);
        painter.setFont(QFont("Arial", 9, QFont::Bold));
        painter.drawText(rect, Qt::AlignCenter, btn.label);
    }

    // Center buttons (Select, Start, Guide)
    QVector<ButtonInfo> centerButtons = {
        {GAMEPAD_BUTTON_SELECT, QPointF(w * 0.43, h * 0.38), "◀", QColor(200, 200, 200)},
        {GAMEPAD_BUTTON_START,  QPointF(w * 0.57, h * 0.38), "▶", QColor(200, 200, 200)},
        {GAMEPAD_BUTTON_GUIDE,  QPointF(w * 0.50, h * 0.42), "⌂", QColor(220, 220, 100)},
    };

    for (const auto &btn : centerButtons) {
        bool pressed = m_buttonStates.value(btn.code, false);

        painter.setPen(QPen(QColor(60, 60, 80), 2));
        painter.setBrush(pressed ? QColor(100, 255, 100) : btn.color);

        painter.drawEllipse(btn.center, 12, 12);

        painter.setPen(Qt::black);
        painter.setFont(QFont("Arial", 10, QFont::Bold));
        painter.drawText(QRectF(btn.center.x() - 12, btn.center.y() - 12, 24, 24),
                        Qt::AlignCenter, btn.label);
    }
}

void GamepadWidget::drawJoysticks(QPainter &painter)
{
    int w = width();
    int h = height();

    struct StickInfo {
        uint32_t axisX;
        uint32_t axisY;
        uint32_t button;
        QPointF center;
        QString label;
    };

    QVector<StickInfo> sticks = {
        {GAMEPAD_AXIS_LEFT_X, GAMEPAD_AXIS_LEFT_Y, GAMEPAD_BUTTON_L3,
         QPointF(w * 0.30, h * 0.55), "L3"},
        {GAMEPAD_AXIS_RIGHT_X, GAMEPAD_AXIS_RIGHT_Y, GAMEPAD_BUTTON_R3,
         QPointF(w * 0.60, h * 0.65), "R3"},
    };

    for (const auto &stick : sticks) {
        bool pressed = m_buttonStates.value(stick.button, false);
        double valueX = m_axisValues.value(stick.axisX, 0.0);
        double valueY = m_axisValues.value(stick.axisY, 0.0);

        // Stick base
        painter.setPen(QPen(QColor(60, 60, 80), 2));
        painter.setBrush(QColor(150, 150, 160));
        painter.drawEllipse(stick.center, 35, 35);

        // Stick position indicator
        QPointF stickPos(
            stick.center.x() + valueX * 25,
            stick.center.y() + valueY * 25
        );

        painter.setBrush(pressed ? QColor(100, 255, 100) : QColor(100, 100, 120));
        painter.drawEllipse(stickPos, 15, 15);

        // Label
        painter.setPen(Qt::white);
        painter.setFont(QFont("Arial", 8, QFont::Bold));
        painter.drawText(QRectF(stick.center.x() - 35, stick.center.y() + 40, 70, 20),
                        Qt::AlignCenter, stick.label);
    }
}

void GamepadWidget::drawDPad(QPainter &painter)
{
    int w = width();
    int h = height();

    QPointF center(w * 0.30, h * 0.42);
    int size = 15;
    int gap = 5;

    bool up    = m_hatValue & GAMEPAD_HAT_UP;
    bool down  = m_hatValue & GAMEPAD_HAT_DOWN;
    bool left  = m_hatValue & GAMEPAD_HAT_LEFT;
    bool right = m_hatValue & GAMEPAD_HAT_RIGHT;

    painter.setPen(QPen(QColor(60, 60, 80), 2));

    // Up
    painter.setBrush(up ? QColor(100, 255, 100) : QColor(180, 180, 180));
    QRectF upRect(center.x() - size/2, center.y() - size - gap, size, size);
    painter.drawRect(upRect);

    // Down
    painter.setBrush(down ? QColor(100, 255, 100) : QColor(180, 180, 180));
    QRectF downRect(center.x() - size/2, center.y() + gap, size, size);
    painter.drawRect(downRect);

    // Left
    painter.setBrush(left ? QColor(100, 255, 100) : QColor(180, 180, 180));
    QRectF leftRect(center.x() - size - gap, center.y() - size/2, size, size);
    painter.drawRect(leftRect);

    // Right
    painter.setBrush(right ? QColor(100, 255, 100) : QColor(180, 180, 180));
    QRectF rightRect(center.x() + gap, center.y() - size/2, size, size);
    painter.drawRect(rightRect);

    // Center
    painter.setBrush(QColor(160, 160, 160));
    painter.drawEllipse(center, size/3, size/3);

    // Label
    painter.setPen(Qt::black);
    painter.setFont(QFont("Arial", 8, QFont::Bold));
    painter.drawText(QRectF(center.x() - 30, center.y() + 25, 60, 20),
                    Qt::AlignCenter, "D-Pad");
}

void GamepadWidget::drawTriggers(QPainter &painter)
{
    int w = width();
    int h = height();

    struct TriggerInfo {
        uint32_t axis;
        uint32_t button;
        QPointF pos;
        QString label;
    };

    QVector<TriggerInfo> triggers = {
        {GAMEPAD_AXIS_TRIGGER_LEFT, GAMEPAD_BUTTON_L2, QPointF(w * 0.25, h * 0.15), "L2"},
        {GAMEPAD_AXIS_TRIGGER_RIGHT, GAMEPAD_BUTTON_R2, QPointF(w * 0.75, h * 0.15), "R2"},
    };

    for (const auto &trigger : triggers) {
        bool pressed = m_buttonStates.value(trigger.button, false);
        double value = m_axisValues.value(trigger.axis, 0.0);

        // Normalize trigger value (usually -1 to 1, but triggers are 0 to 1)
        double normalized = (value + 1.0) / 2.0;
        normalized = qBound(0.0, normalized, 1.0);

        // Background
        painter.setPen(QPen(QColor(60, 60, 80), 2));
        painter.setBrush(QColor(220, 220, 220));
        QRectF bgRect(trigger.pos.x() - 30, trigger.pos.y(), 60, 15);
        painter.drawRect(bgRect);

        // Fill level
        painter.setBrush(pressed || normalized > 0.1 ? QColor(100, 255, 100) : QColor(150, 150, 150));
        QRectF fillRect(trigger.pos.x() - 30, trigger.pos.y(), 60 * normalized, 15);
        painter.drawRect(fillRect);

        // Label
        painter.setPen(Qt::black);
        painter.setFont(QFont("Arial", 9, QFont::Bold));
        painter.drawText(QRectF(trigger.pos.x() - 30, trigger.pos.y() - 15, 60, 15),
                        Qt::AlignCenter, trigger.label);
    }
}

void GamepadWidget::drawLabels(QPainter &painter)
{
    painter.setPen(QColor(80, 80, 100));
    painter.setFont(QFont("Arial", 10, QFont::Bold));

    painter.drawText(QRectF(0, height() - 25, width(), 20),
                    Qt::AlignCenter,
                    "Press any button or move any stick/trigger");
}

QColor GamepadWidget::buttonColor(uint32_t button) const
{
    Q_UNUSED(button);
    return QColor(100, 200, 255);
}

QString GamepadWidget::buttonName(uint32_t button) const
{
    switch (button) {
    case GAMEPAD_BUTTON_A: return "A";
    case GAMEPAD_BUTTON_B: return "B";
    case GAMEPAD_BUTTON_X: return "X";
    case GAMEPAD_BUTTON_Y: return "Y";
    case GAMEPAD_BUTTON_L1: return "L1";
    case GAMEPAD_BUTTON_R1: return "R1";
    case GAMEPAD_BUTTON_L2: return "L2";
    case GAMEPAD_BUTTON_R2: return "R2";
    case GAMEPAD_BUTTON_L3: return "L3";
    case GAMEPAD_BUTTON_R3: return "R3";
    case GAMEPAD_BUTTON_SELECT: return "Select";
    case GAMEPAD_BUTTON_START: return "Start";
    case GAMEPAD_BUTTON_GUIDE: return "Guide";
    default: return QString("Button %1").arg(button);
    }
}
