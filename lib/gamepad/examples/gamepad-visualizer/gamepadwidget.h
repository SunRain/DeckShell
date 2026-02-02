// Copyright (C) 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#ifndef GAMEPADWIDGET_H
#define GAMEPADWIDGET_H

#include <QWidget>
#include <QHash>

class GamepadWidget : public QWidget
{
    Q_OBJECT

public:
    explicit GamepadWidget(QWidget *parent = nullptr);
    ~GamepadWidget() override;

    void setButtonState(uint32_t button, bool pressed);
    void setAxisValue(uint32_t axis, double value);
    void setHatValue(int32_t value);
    void reset();

protected:
    void paintEvent(QPaintEvent *event) override;

private:
    void drawBackground(QPainter &painter);
    void drawController(QPainter &painter);
    void drawButtons(QPainter &painter);
    void drawJoysticks(QPainter &painter);
    void drawDPad(QPainter &painter);
    void drawTriggers(QPainter &painter);
    void drawLabels(QPainter &painter);

    QColor buttonColor(uint32_t button) const;
    QString buttonName(uint32_t button) const;

private:
    // Button states (button code -> pressed state)
    QHash<uint32_t, bool> m_buttonStates;

    // Axis values (axis code -> value)
    QHash<uint32_t, double> m_axisValues;

    // D-pad state
    int32_t m_hatValue;
};

#endif // GAMEPADWIDGET_H
