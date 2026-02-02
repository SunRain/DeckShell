// Copyright (C) 2024 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <QCoreApplication>
#include <QDebug>
#include <QTimer>
#include <QTextStream>

#include <deckshell/deckgamepad/backend/deckgamepadbackend.h>

DECKGAMEPAD_USE_NAMESPACE

class GamepadMonitor : public QObject
{
    Q_OBJECT

public:
    GamepadMonitor(QObject *parent = nullptr)
        : QObject(parent)
    {
        backend = DeckGamepadBackend::instance();

        // Connect signals
        connect(backend, &DeckGamepadBackend::gamepadConnected,
                this, &GamepadMonitor::onGamepadConnected);
        connect(backend, &DeckGamepadBackend::gamepadDisconnected,
                this, &GamepadMonitor::onGamepadDisconnected);
        connect(backend, &DeckGamepadBackend::buttonEvent,
                this, &GamepadMonitor::onButtonEvent);
        connect(backend, &DeckGamepadBackend::axisEvent,
                this, &GamepadMonitor::onAxisEvent);
        connect(backend, &DeckGamepadBackend::hatEvent,
                this, &GamepadMonitor::onHatEvent);
    }

    bool start()
    {
        if (!backend->start()) {
            qCritical() << "Failed to start gamepad backend";
            return false;
        }

        printHeader();
        printConnectedGamepads();
        return true;
    }

private slots:
    void onGamepadConnected(int deviceId, const QString &name)
    {
        qInfo() << "[" << deviceId << "] Gamepad connected:" << name;

        auto device = backend->device(deviceId);
        if (device) {
            qInfo() << "    Name:" << device->name();
            qInfo() << "    Path:" << device->devicePath();
        }
    }

    void onGamepadDisconnected(int deviceId)
    {
        qInfo() << "[" << deviceId << "] Gamepad disconnected";
    }

    void onButtonEvent(int deviceId, DeckGamepadButtonEvent event)
    {
        QString buttonName = getButtonName(event.button);
        QString state = event.pressed ? "pressed " : "released";

        qInfo().noquote() << QString("[%1] Button %2 %3 (code: %4)")
                   .arg(deviceId)
                   .arg(buttonName, -10)
                   .arg(state)
                   .arg(event.button);
    }

    void onAxisEvent(int deviceId, DeckGamepadAxisEvent event)
    {
        QString axisName = getAxisName(event.axis);

        // Only print significant axis changes (to reduce spam)
        if (qAbs(event.value) < 0.05) {
            return; // Ignore near-zero values (noise)
        }

        qInfo().noquote() << QString("[%1] Axis %2 = %3")
                   .arg(deviceId)
                   .arg(axisName, -12)
                   .arg(event.value, 6, 'f', 3);
    }

    void onHatEvent(int deviceId, DeckGamepadHatEvent event)
    {
        QString direction = getHatDirection(event.value);

        qInfo().noquote() << QString("[%1] D-pad: %2 (value: 0x%3)")
                   .arg(deviceId)
                   .arg(direction, -20)
                   .arg(event.value, 2, 16, QChar('0'));
    }

private:
    void printHeader()
    {
        qInfo() << "========================================";
        qInfo() << "   Gamepad Monitor - Press Ctrl+C to exit";
        qInfo() << "========================================";
        qInfo() << "";
    }

    void printConnectedGamepads()
    {
        QList<int> gamepads = backend->connectedGamepads();

        if (gamepads.isEmpty()) {
            qInfo() << "No gamepads detected.";
            qInfo() << "Waiting for gamepad connection...";
        } else {
            qInfo() << "Detected" << gamepads.size() << "gamepad(s):";
            for (int id : gamepads) {
                auto device = backend->device(id);
                if (device) {
                    qInfo() << "  [" << id << "]" << device->name();
                    qInfo() << "      Path:" << device->devicePath();
                }
            }
        }
        qInfo() << "";
    }

    QString getButtonName(uint32_t button)
    {
        switch (button) {
        case GAMEPAD_BUTTON_A:       return "A";
        case GAMEPAD_BUTTON_B:       return "B";
        case GAMEPAD_BUTTON_X:       return "X";
        case GAMEPAD_BUTTON_Y:       return "Y";
        case GAMEPAD_BUTTON_L1:      return "L1 (LB)";
        case GAMEPAD_BUTTON_R1:      return "R1 (RB)";
        case GAMEPAD_BUTTON_L2:      return "L2 (LT)";
        case GAMEPAD_BUTTON_R2:      return "R2 (RT)";
        case GAMEPAD_BUTTON_SELECT:  return "Select";
        case GAMEPAD_BUTTON_START:   return "Start";
        case GAMEPAD_BUTTON_L3:      return "L3";
        case GAMEPAD_BUTTON_R3:      return "R3";
        case GAMEPAD_BUTTON_GUIDE:   return "Guide";
        default:                     return QString("Unknown(%1)").arg(button);
        }
    }

    QString getAxisName(uint32_t axis)
    {
        switch (axis) {
        case GAMEPAD_AXIS_LEFT_X:       return "Left Stick X";
        case GAMEPAD_AXIS_LEFT_Y:       return "Left Stick Y";
        case GAMEPAD_AXIS_RIGHT_X:      return "Right Stick X";
        case GAMEPAD_AXIS_RIGHT_Y:      return "Right Stick Y";
        case GAMEPAD_AXIS_TRIGGER_LEFT: return "Left Trigger";
        case GAMEPAD_AXIS_TRIGGER_RIGHT:return "Right Trigger";
        default:                        return QString("Unknown(%1)").arg(axis);
        }
    }

    QString getHatDirection(int32_t value)
    {
        QStringList directions;

        if (value == GAMEPAD_HAT_CENTER) {
            return "Center";
        }

        if (value & GAMEPAD_HAT_UP)    directions << "Up";
        if (value & GAMEPAD_HAT_DOWN)  directions << "Down";
        if (value & GAMEPAD_HAT_LEFT)  directions << "Left";
        if (value & GAMEPAD_HAT_RIGHT) directions << "Right";

        return directions.join(" + ");
    }

    DeckGamepadBackend *backend;
};

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    app.setApplicationName("gamepad-monitor");
    app.setApplicationVersion("1.0.0");

    // Create and start monitor
    GamepadMonitor monitor;
    if (!monitor.start()) {
        return 1;
    }

    qInfo() << "Monitoring gamepad events... Press Ctrl+C to quit.";
    qInfo() << "";

    return app.exec();
}

#include "main.moc"
