// Copyright (C) 2025 UnionTech Software Technology Co., Ltd.
// SPDX-License-Identifier: Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include <QCoreApplication>
#include <QTimer>
#include <QDebug>
#include <QSocketNotifier>
#include <iostream>
#include <iomanip>

#include "../../src/treelandgamepadclient.h"
#include "../../src/treelandgamepaddevice.h"
#include "../../src/treelandgamepadglobal.h"

using namespace TreelandGamepad;
using namespace deckshell::deckgamepad;

class GamepadMonitor : public QObject
{
    Q_OBJECT

public:
    TreelandGamepadClient *client() const { return m_client; }
    
    GamepadMonitor(QObject *parent = nullptr) : QObject(parent)
    {
        // Create client
        m_client = new TreelandGamepadClient(this);
        
        // Connect signals
        connect(m_client, &TreelandGamepadClient::connectedChanged,
                this, &GamepadMonitor::onConnectedChanged);
        connect(m_client, &TreelandGamepadClient::gamepadAdded,
                this, &GamepadMonitor::onGamepadAdded);
        connect(m_client, &TreelandGamepadClient::gamepadRemoved,
                this, &GamepadMonitor::onGamepadRemoved);
        
        // Try to connect
        if (!m_client->connectToCompositor()) {
            qCritical() << "Failed to connect to Wayland compositor";
            QCoreApplication::exit(1);
        }
    }

private slots:
    void onConnectedChanged(bool connected)
    {
        std::cout << "Wayland connection: " << (connected ? "CONNECTED" : "DISCONNECTED") << std::endl;
    }
    
    void onGamepadAdded(int deviceId, const QString &name)
    {
        std::cout << "Gamepad ADDED: ID=" << deviceId 
                  << " Name=\"" << name.toStdString() << "\"" << std::endl;
        
        // Get the device and connect to its signals
        if (auto *device = m_client->gamepad(deviceId)) {
            connectDevice(device);
        }
    }
    
    void onGamepadRemoved(int deviceId)
    {
        std::cout << "Gamepad REMOVED: ID=" << deviceId << std::endl;
    }
    
    void onButtonPressed(GamepadButton button)
    {
        std::cout << "Button PRESSED: " << buttonName(button)
                  << " (" << static_cast<int>(button) << ")" << std::endl;
    }
    
    void onButtonReleased(GamepadButton button)
    {
        std::cout << "Button RELEASED: " << buttonName(button)
                  << " (" << static_cast<int>(button) << ")" << std::endl;
    }
    
    void onAxisChanged(GamepadAxis axis, double value)
    {
        std::cout << "Axis CHANGED: " << axisName(axis)
                  << " = " << std::fixed << std::setprecision(3) << value << std::endl;
    }
    
    void onHatChanged(int direction)
    {
        std::cout << "Hat CHANGED: " << hatDirectionName(direction) << std::endl;
    }

private:
    void connectDevice(TreelandGamepadDevice *device)
    {
        connect(device, &TreelandGamepadDevice::buttonPressed,
                this, &GamepadMonitor::onButtonPressed);
        connect(device, &TreelandGamepadDevice::buttonReleased,
                this, &GamepadMonitor::onButtonReleased);
        connect(device, &TreelandGamepadDevice::axisChanged,
                this, &GamepadMonitor::onAxisChanged);
        connect(device, &TreelandGamepadDevice::hatChanged,
                this, &GamepadMonitor::onHatChanged);
        
        std::cout << "Connected to device " << device->deviceId() << std::endl;
    }
    
    const char* buttonName(GamepadButton button) const
    {
        switch (button) {
        case GAMEPAD_BUTTON_A: return "A";
        case GAMEPAD_BUTTON_B: return "B";
        case GAMEPAD_BUTTON_X: return "X";
        case GAMEPAD_BUTTON_Y: return "Y";
        case GAMEPAD_BUTTON_L1: return "L1/LB";
        case GAMEPAD_BUTTON_R1: return "R1/RB";
        case GAMEPAD_BUTTON_L2: return "L2/LT";
        case GAMEPAD_BUTTON_R2: return "R2/RT";
        case GAMEPAD_BUTTON_SELECT: return "Select/Back";
        case GAMEPAD_BUTTON_START: return "Start";
        case GAMEPAD_BUTTON_L3: return "L3";
        case GAMEPAD_BUTTON_R3: return "R3";
        case GAMEPAD_BUTTON_GUIDE: return "Guide/Home";
        case GAMEPAD_BUTTON_DPAD_UP: return "DPad-Up";
        case GAMEPAD_BUTTON_DPAD_DOWN: return "DPad-Down";
        case GAMEPAD_BUTTON_DPAD_LEFT: return "DPad-Left";
        case GAMEPAD_BUTTON_DPAD_RIGHT: return "DPad-Right";
        default: return "Unknown";
        }
    }
    
    const char* axisName(GamepadAxis axis) const
    {
        switch (axis) {
        case GAMEPAD_AXIS_LEFT_X: return "Left-X";
        case GAMEPAD_AXIS_LEFT_Y: return "Left-Y";
        case GAMEPAD_AXIS_RIGHT_X: return "Right-X";
        case GAMEPAD_AXIS_RIGHT_Y: return "Right-Y";
        case GAMEPAD_AXIS_TRIGGER_LEFT: return "Trigger-Left";
        case GAMEPAD_AXIS_TRIGGER_RIGHT: return "Trigger-Right";
        default: return "Unknown";
        }
    }
    
    const char* hatDirectionName(int direction) const
    {
        switch (direction) {
        case GAMEPAD_HAT_CENTER: return "Center";
        case GAMEPAD_HAT_UP: return "Up";
        case GAMEPAD_HAT_RIGHT: return "Right";
        case GAMEPAD_HAT_DOWN: return "Down";
        case GAMEPAD_HAT_LEFT: return "Left";
        case GAMEPAD_HAT_UP | GAMEPAD_HAT_RIGHT: return "Up-Right";
        case GAMEPAD_HAT_DOWN | GAMEPAD_HAT_RIGHT: return "Down-Right";
        case GAMEPAD_HAT_DOWN | GAMEPAD_HAT_LEFT: return "Down-Left";
        case GAMEPAD_HAT_UP | GAMEPAD_HAT_LEFT: return "Up-Left";
        default: return "Unknown";
        }
    }

private:
    TreelandGamepadClient *m_client = nullptr;
};

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    app.setApplicationName("gamepad-wayland-monitor");
    app.setApplicationVersion("1.0.0");
    
    std::cout << "==================================" << std::endl;
    std::cout << "Treeland Gamepad Monitor v1.0.0" << std::endl;
    std::cout << "Press Ctrl+C to exit" << std::endl;
    std::cout << "==================================" << std::endl;
    
    GamepadMonitor monitor;
    
    // Add vibration test command (press 'v' + Enter to test)
    QTimer::singleShot(2000, [&]() {
        std::cout << "\nType 'v' and press Enter to test vibration on all gamepads" << std::endl;
    });
    
    // Simple stdin reader for vibration test
    QSocketNotifier stdinNotifier(fileno(stdin), QSocketNotifier::Read);
    QObject::connect(&stdinNotifier, &QSocketNotifier::activated, [&monitor]() {
        std::string line;
        std::getline(std::cin, line);
        
        if (line == "v" || line == "V") {
            std::cout << "Testing vibration..." << std::endl;
            auto gamepads = monitor.client()->availableGamepads();
            for (int id : gamepads) {
                monitor.client()->setVibration(id, 0.5, 1.0, 1000);
            }
        }
    });
    
    return app.exec();
}

#include "main.moc"
