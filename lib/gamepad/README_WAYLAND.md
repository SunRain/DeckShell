# Treeland Gamepad Wayland Protocol Client Library

A Qt6/C++ client library implementing the `treeland-gamepad-v1` Wayland protocol for gamepad input handling and vibration control.

## Features

- Complete implementation of `treeland-gamepad-v1` protocol
- Qt6 signals and slots for event handling
- Automatic gamepad detection and lifecycle management
- Button, axis, and HAT/D-pad input events
- Dual-motor vibration control
- Thread-safe operation with Qt event loop integration

## Building

### Requirements
- Qt6 (>= 6.0)
- CMake (>= 3.16)
- Wayland client libraries
- wayland-scanner tool

### Build Instructions
```bash
mkdir build && cd build
cmake -DDECKGAMEPAD_BUILD_TREELAND_CLIENT=ON ..
cmake --build .
```

默认使用仓库内 vendored 协议文件：
- `protocols/treeland-gamepad-v1.xml`

如需覆盖协议文件路径，可显式指定：
```bash
cmake -DDECKGAMEPAD_BUILD_TREELAND_CLIENT=ON -DTREELAND_GAMEPAD_PROTOCOL_XML=/path/to/treeland-gamepad-v1.xml ..
```

## Usage Example

```cpp
#include <treelandgamepadclient.h>
using namespace TreelandGamepad;

// Create and connect client
TreelandGamepadClient client;
client.connectToCompositor();

// Handle gamepad events
QObject::connect(&client, &TreelandGamepadClient::gamepadAdded,
    [&](int deviceId, const QString &name) {
        qDebug() << "Gamepad connected:" << name;
    });

// Set vibration
client.setVibration(deviceId, 0.5, 1.0, 1000);
```

## Button Mapping (Xbox/SDL2 Standard)
- 0-3: A/B/X/Y
- 4-7: LB/RB/LT/RT
- 8-9: Select/Start
- 10-11: L3/R3
- 12: Guide
- 13-16: D-pad directions

## Axis Mapping
- 0-1: Left stick X/Y
- 2-3: Right stick X/Y
- 4-5: Left/Right triggers

## License
Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
