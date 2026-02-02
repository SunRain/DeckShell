# Gamepad Configuration CLI Tool

Command-line tool for testing, configuring, and debugging gamepads in DeckShell.

## Features

- 📋 **List Devices**: Show all connected gamepads
- 🔍 **Device Info**: Display detailed device information including SDL mapping status
- 🎮 **Input Testing**: Real-time button/axis/HAT event monitoring
- 📳 **Vibration Testing**: Test force feedback/rumble
- 🗄️ **SDL DB Query**: Query SDL GameController Database
- 💾 **Export Config**: Export current configuration to JSON

## Installation

The tool is built as part of the gamepad examples:

```bash
cd build
cmake --build . --target gamepad-config
```

The executable will be at: `build/lib/gamepad/examples/gamepad-cli/gamepad-config`

## Usage

### List All Connected Gamepads

```bash
gamepad-config --list
```

**Output Example**:
```
Connected Gamepads (1):
----------------------------------------
Device ID: 0
  Name: Xbox 360 Controller
  Path: /dev/input/event5
  GUID: 030000005e040000a102000001000000
  SDL Mapping: ✓ Xbox 360 Controller
```

### Show Device Information

```bash
gamepad-config --device 0 --info
```

**Output Example**:
```
Device Information:
==================
Device ID: 0
Name: Xbox 360 Controller
Path: /dev/input/event5
GUID: 030000005e040000a102000001000000
Connected: Yes
SDL Mapping: ✓ Found
  Mapping Name: Xbox 360 Controller

SDL Database Status:
  Total Mappings: 2052
```

### Test Input (Real-time Events)

```bash
# Test all devices
gamepad-config --test-input

# Test specific device
gamepad-config --device 0 --test-input
```

**Output Example**:
```
Testing input from device 0 (Xbox 360 Controller)
Press Ctrl+C to stop
----------------------------------------
[BUTTON] Device 0: A PRESSED
[BUTTON] Device 0: A RELEASED
[AXIS] Device 0: LEFT_X = 0.523
[AXIS] Device 0: LEFT_Y = -0.782
[BUTTON] Device 0: L1 PRESSED
[HAT] Device 0: UP
[HAT] Device 0: CENTER
```

### Test Vibration

```bash
gamepad-config --device 0 --vibrate 0.5,0.8,1000
```

Parameters: `weak_magnitude,strong_magnitude,duration_ms`
- Magnitudes: 0.0-1.0
- Duration: milliseconds
注意：
- 需要对对应的 `/dev/input/event*` 具备写权限（能 `O_RDWR` 打开并写入 `EV_FF`）。
- 若运行环境只能 `O_RDONLY`（常见于 ACL 限制写），将提示 “Failed to start vibration”。

**Output Example**:
```
Testing vibration on device 0...
  Weak: 0.5
  Strong: 0.8
  Duration: 1000 ms
Vibration started successfully!
```

### Query SDL Database

#### Show DB Statistics

```bash
gamepad-config --sdl-db
```

**Output Example**:
```
SDL GameController Database:
=============================
Total Mappings: 2052

Connected Devices:
  Xbox 360 Controller
    GUID: 030000005e040000a102000001000000
    Mapped: Yes
```

#### Query Specific GUID

```bash
gamepad-config --query-guid 030000005e040000a102000001000000
```

**Output Example**:
```
Querying GUID: 030000005e040000a102000001000000
----------------------------------------
✓ Mapping found!
  Device Name: Xbox 360 Controller
```

### Export Configuration

```bash
gamepad-config --export config.json
```

Exports current gamepad configuration to a JSON file.

**Output JSON Example**:
```json
{
  "devices": [
    {
      "id": 0,
      "name": "Xbox 360 Controller",
      "path": "/dev/input/event5",
      "guid": "030000005e040000a102000001000000",
      "has_sdl_mapping": true,
      "mapping_name": "Xbox 360 Controller"
    }
  ],
  "sdl_db_mappings": 2052,
  "export_timestamp": "2025-10-27T15:30:00"
}
```

## Command Reference

### General Options

| Option | Short | Description |
|--------|-------|-------------|
| `--help` | `-h` | Show help message |
| `--version` | `-V` | Show version |

### Device Commands

| Option | Short | Arguments | Description |
|--------|-------|-----------|-------------|
| `--list` | `-l` | - | List all connected gamepads |
| `--device` | `-d` | `id` | Specify device ID for other commands |
| `--info` | - | - | Show device information (requires `--device`) |

### Testing Commands

| Option | Short | Arguments | Description |
|--------|-------|-----------|-------------|
| `--test-input` | `-t` | - | Test input events (optional `--device`) |
| `--vibrate` | - | `weak,strong,ms` | Test vibration (requires `--device`) |

### SDL Database Commands

| Option | Arguments | Description |
|--------|-----------|-------------|
| `--sdl-db` | - | Show SDL DB information |
| `--query-guid` | `guid` | Query mapping for specific GUID |

### Configuration Commands

| Option | Short | Arguments | Description |
|--------|-------|-----------|-------------|
| `--export` | `-e` | `filename` | Export configuration to JSON |

## Examples

### Common Workflows

#### 1. Quick Device Check
```bash
# Check what's connected
gamepad-config --list

# Get details
gamepad-config --device 0 --info
```

#### 2. Test New Controller
```bash
# Test all buttons and axes
gamepad-config --device 0 --test-input

# Test vibration
gamepad-config --device 0 --vibrate 0.7,0.7,500
```

#### 3. Check SDL Mapping
```bash
# See if device has mapping
gamepad-config --sdl-db

# Query specific GUID
gamepad-config --query-guid <guid>
```

#### 4. Export for Debugging
```bash
# Export current state
gamepad-config --export debug-$(date +%Y%m%d).json
```

## Troubleshooting

### No Gamepads Detected

1. Check permissions:
   ```bash
   ls -l /dev/input/event*
   # Should be readable by your user
   ```

2. Check udev rules:
   ```bash
   sudo udevadm info /dev/input/event5
   ```

3. Try with sudo (not recommended for regular use):
   ```bash
   sudo gamepad-config --list
   ```

### SDL Mapping Not Found

If a device shows "SDL Mapping: ✗", it means:
- Device GUID not in SDL GameController DB
- Device will use generic Xbox layout
- You can contribute the mapping to SDL DB

To get the GUID for contribution:
```bash
gamepad-config --device 0 --info | grep GUID
```

### Vibration Not Working

- Not all gamepads support vibration
- Check if device has force feedback capability:
  ```bash
  cat /sys/class/input/event*/device/capabilities/ff
  # Non-zero means vibration supported
  ```

## Development

### Building from Source

```bash
cd DeckShell
mkdir build && cd build
cmake ..
cmake --build . --target gamepad-config
```

### Running Without Install

```bash
./build/lib/gamepad/examples/gamepad-cli/gamepad-config --list
```

## See Also

- [SDL GameController DB](https://github.com/gabomdq/SDL_GameControllerDB)
- [DeckShell Gamepad Documentation](../../README.md)
- [Stage 4 Implementation Plan](../../../../doc/STAGE4_TASK_CHECKLIST.md)

## License

Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
