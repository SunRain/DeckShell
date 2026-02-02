# Gamepad Monitor

A simple console application to monitor gamepad/joystick events using the qwlroots gamepad backend.

## Features

- **Device Detection**: Automatically detects connected gamepads and lists their information
- **Hotplug Support**: Monitors gamepad connection and disconnection events
- **Button Events**: Displays button press and release events with button names
- **Axis Events**: Shows analog stick and trigger values in real-time
- **D-Pad (HAT) Events**: Monitors directional pad input with combined directions

## Supported Gamepads

This example works with any gamepad that uses the standard Linux evdev interface, including:

- Xbox 360/One/Series controllers (wired and wireless)
- PlayStation 4/5 DualShock/DualSense controllers
- Nintendo Switch Pro Controller
- Steam Deck built-in controls
- Generic USB/Bluetooth gamepads

## Building

### Prerequisites

- Qt 6.x
- qwlroots library
- libudev

### Build Instructions

```bash
# From the qwlroots build directory
cmake -B build -S /path/to/qwlroots
cmake --build build --target gamepad-monitor

# Or use make
cd build
make gamepad-monitor
```

### Standalone Build

```bash
cd qwlroots/examples/gamepad-monitor
cmake -B build
cmake --build build
```

## Running

```bash
./gamepad-monitor
```

**Note**: You may need to run with proper permissions to access `/dev/input/event*` devices. Options:

1. **Add user to `input` group** (recommended):
   ```bash
   sudo usermod -a -G input $USER
   # Log out and log back in for changes to take effect
   ```

2. **Run with sudo** (not recommended for regular use):
   ```bash
   sudo ./gamepad-monitor
   ```

3. **Set udev rules** (advanced):
   Create `/etc/udev/rules.d/99-gamepad.rules`:
   ```
   SUBSYSTEM=="input", MODE="0666", GROUP="input"
   ```

## Example Output

```
========================================
   Gamepad Monitor - Press Ctrl+C to exit
========================================

Detected 1 gamepad(s):
  [0] Xbox Wireless Controller
      Path: /dev/input/event12

Monitoring gamepad events... Press Ctrl+C to quit.

[0] Button A        pressed  (code: 0)
[0] Axis Left Stick X  =  -0.350
[0] Axis Left Stick Y  =   0.820
[0] D-pad: Up                    (value: 0x01)
[0] Button A        released (code: 0)
[1] Gamepad connected: PlayStation 4 Controller
    Name: Sony Interactive Entertainment Wireless Controller
    Path: /dev/input/event15
```

## Button Mapping

Standard Xbox controller layout:

| Button   | Description         |
|----------|---------------------|
| A        | South button        |
| B        | East button         |
| X        | West button         |
| Y        | North button        |
| LB (L1)  | Left shoulder       |
| RB (R1)  | Right shoulder      |
| LT (L2)  | Left trigger button |
| RT (R2)  | Right trigger button|
| L3       | Left stick press    |
| R3       | Right stick press   |
| Start    | Start/Options       |
| Select   | Select/Share/Back   |
| Guide    | Home/Guide/PS button|

## Axis Mapping

| Axis           | Description       | Range      |
|----------------|-------------------|------------|
| Left Stick X   | Left analog X     | -1.0 ~ 1.0 |
| Left Stick Y   | Left analog Y     | -1.0 ~ 1.0 |
| Right Stick X  | Right analog X    | -1.0 ~ 1.0 |
| Right Stick Y  | Right analog Y    | -1.0 ~ 1.0 |
| Left Trigger   | Analog LT/L2      | -1.0 ~ 1.0 |
| Right Trigger  | Analog RT/R2      | -1.0 ~ 1.0 |

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

### Events not showing up

- Some gamepads may have a deadzone. Try moving sticks further from center.
- Axis events with values less than 0.05 are filtered out to reduce noise.

### Controller-specific issues

- **PS4/PS5**: May require pairing in Bluetooth settings first
- **Switch Pro**: Use the "Pair" button (small button near USB-C port)
- **Xbox Wireless**: Requires Bluetooth adapter or wireless dongle

## See Also

- [qwlroots Gamepad Backend](../../../qwlroots/src/types/deckgamepadbackend.h)
- [Linux Kernel Joystick API](https://www.kernel.org/doc/html/latest/input/joydev/index.html)
- [evdev Documentation](https://www.freedesktop.org/wiki/Software/libevdev/)

## License

Copyright (C) 2024 UnionTech Software Technology Co., Ltd.

This example is licensed under Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only.
