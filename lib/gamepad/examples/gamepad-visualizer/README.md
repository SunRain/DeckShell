# Gamepad Visualizer

A graphical Qt Widgets application for visualizing gamepad/joystick input in real-time using the qwlroots gamepad backend.

## Features

- **Visual Gamepad Display**: Real-time graphical representation of an Xbox-style gamepad controller
- **Button Visualization**: All buttons (A/B/X/Y, L1/R1/L2/R2, L3/R3, D-pad, Start/Select/Guide) light up when pressed
- **Analog Stick Tracking**: Visual representation of left and right analog stick positions
- **Trigger Indicators**: Progress bars showing trigger (L2/R2) pressure levels
- **Multi-Device Support**: Dropdown selector for switching between multiple connected gamepads
- **Hotplug Detection**: Automatically detects when gamepads are connected or disconnected
- **Status Display**: Real-time event information showing current button/axis/D-pad state

## Supported Gamepads

This application works with any gamepad that uses the standard Linux evdev interface, including:

- Xbox 360/One/Series controllers (wired and wireless)
- PlayStation 4/5 DualShock/DualSense controllers
- Nintendo Switch Pro Controller
- Steam Deck built-in controls
- Generic USB/Bluetooth gamepads

## User Interface

The application window contains:

1. **Device Selector**: Dropdown menu to choose which connected gamepad to visualize
2. **Connection Status**: Shows current connection state (green when connected)
3. **Visual Gamepad Widget**:
   - Face buttons (A, B, X, Y) on the right side
   - D-pad on the left side
   - Two analog sticks showing real-time position
   - Shoulder buttons (L1/R1) at the top
   - Trigger indicators (L2/R2) with fill bars
   - Center buttons (Select, Start, Guide)
4. **Event Status**: Text label showing the latest input event

## Building

### Prerequisites

- Qt 6.x (Core, Gui, Widgets modules)
- qwlroots library with gamepad support
- libudev

### Build Instructions

```bash
# From the qwlroots build directory
cmake -B build -S /path/to/qwlroots
cmake --build build --target gamepad-visualizer

# Or use make
cd build
make gamepad-visualizer
```

### Standalone Build

```bash
cd qwlroots/examples/gamepad-visualizer
cmake -B build
cmake --build build
```

The executable will be located at:
- Main build: `build/examples/gamepad-visualizer/gamepad-visualizer`
- Standalone: `build/gamepad-visualizer`

## Running

```bash
./gamepad-visualizer
```

**Note**: You may need to run with proper permissions to access `/dev/input/event*` devices. Options:

1. **Add user to `input` group** (recommended):
   ```bash
   sudo usermod -a -G input $USER
   # Log out and log back in for changes to take effect
   ```

2. **Run with sudo** (not recommended for regular use):
   ```bash
   sudo ./gamepad-visualizer
   ```

3. **Set udev rules** (advanced):
   Create `/etc/udev/rules.d/99-gamepad.rules`:
   ```
   SUBSYSTEM=="input", MODE="0666", GROUP="input"
   ```

## Usage

1. **Connect a Gamepad**: Plug in your gamepad via USB or pair it via Bluetooth
2. **Select Device**: If multiple gamepads are connected, choose the one you want to visualize from the dropdown
3. **Test Inputs**:
   - Press buttons - they will light up in the visualization
   - Move analog sticks - the stick indicators will move accordingly
   - Press triggers - the progress bars will fill based on pressure
   - Use D-pad - the directional buttons will highlight

## Visual Guide

### Button Colors

- **A Button**: Green (bottom position)
- **B Button**: Red (right position)
- **X Button**: Blue (left position)
- **Y Button**: Yellow (top position)
- **Guide Button**: Yellow (center)
- **All Others**: Gray when released, bright green when pressed

### Analog Sticks

- **Base Circle**: Gray background showing range of motion
- **Position Indicator**: Dark circle that moves based on stick position
- Fully deflected stick moves the indicator to the edge of the base circle

### Triggers (L2/R2)

- Progress bars at the top of the controller
- Empty when not pressed
- Fill from left to right based on trigger pressure
- Turn green when pressed or when pressure > 10%

## Comparison with gamepad-monitor

| Feature | gamepad-monitor | gamepad-visualizer |
|---------|----------------|-------------------|
| Interface | Console/Terminal | Graphical (Qt Widgets) |
| Output | Text event logs | Visual controller display |
| Button Feedback | Text messages | Visual highlighting |
| Analog Sticks | Numeric values | Position visualization |
| Triggers | Numeric values | Progress bars |
| Multi-Device | Yes | Yes (with selector) |
| Best For | Debugging, testing | End-user visualization, demos |

## Troubleshooting

### No gamepads detected

1. **Check device connection**:
   ```bash
   ls -l /dev/input/event*
   ```

2. **Verify gamepad is recognized**:
   ```bash
   cat /proc/bus/input/devices
   ```
   Look for entries with "joystick" or your controller name.

3. **Test with evtest**:
   ```bash
   sudo evtest /dev/input/eventX
   ```
   (where X is your gamepad event number)

4. **Check permissions**:
   ```bash
   groups  # Should include 'input'
   ```

### Application shows error on startup

- **"Failed to start gamepad backend"**: You don't have permission to access `/dev/input/` devices. See the "Running" section above for solutions.

### Visual display not updating

- Make sure the correct gamepad is selected in the dropdown
- Try disconnecting and reconnecting the gamepad
- Check if `gamepad-monitor` can detect events from the same device

### Controller-specific issues

- **PS4/PS5**: May require pairing in Bluetooth settings first
- **Switch Pro**: Use the "Pair" button (small button near USB-C port)
- **Xbox Wireless**: Requires Bluetooth adapter or wireless dongle

## Technical Details

The visualizer uses:
- **DeckGamepadBackend**: Singleton backend for gamepad device management
- **QPainter**: Custom painting for all visual elements
- **Qt Signals/Slots**: Event propagation from backend to UI
- **evdev**: Direct reading from Linux input event interface

All drawing is done in the `GamepadWidget::paintEvent()` method using QPainter, providing smooth real-time updates at the widget's refresh rate.

## See Also

- [gamepad-monitor](../gamepad-monitor/README.md) - Console version for event monitoring
- [qwlroots Gamepad Backend](../../src/types/deckgamepadbackend.h)
- [Linux Kernel Joystick API](https://www.kernel.org/doc/html/latest/input/joydev/index.html)

## License

Copyright (C) 2024 UnionTech Software Technology Co., Ltd.

This example is licensed under Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only.
