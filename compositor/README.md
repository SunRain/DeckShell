# DeckCompositor

DeckCompositor is DeckShell's Wayland compositor built on QtQuick, WaylibShared,
and its matching native wlroots library. Build it from the DeckShell repository
root; the complete dependency, installation, and test workflow is documented in
[../README.md](../README.md).

## Dependencies

Use Qt 6.8 or newer, the matching Qt Private development files, Dtk6, and the
system dependencies checked by CMake/pkg-config. The installed WaylibShared
**development and runtime packages must match**, including native wlroots;
a separate system wlroots or the retired qwlroots package is not a substitute.

DeckShell owns its protocol XML in `protocols/compositor`. Waylib builds use the
remote-subsurface XML bundled with the matching implementation in their own
`waylib/protocols/` directory. They require neither this source tree nor an
installed `DeckCompositorProtocols` package; missing bundled XML is an error,
not a reason to fall back to an old Treeland installation.

## Building

The default `WITH_SUBMODULE_WAYLIB=OFF` uses the installed WaylibShared package.
Run from the **DeckShell root**, with `waylib_prefix` set to its installation:

```sh
cmake -S . -B build -G Ninja -DCMAKE_PREFIX_PATH="$waylib_prefix"
cmake --build build --parallel 6
ctest --test-dir build --no-tests=error --output-on-failure
```

Use `-DWITH_SUBMODULE_WAYLIB=ON` only for explicit embedded development, after
initializing `3rdparty/waylib-shared` and its wlroots submodule. Both modes use
`WaylibShared::SharedServer`, `WaylibShared::waylib-wlroots`, and the package's
protocol helper. DeckShell installs only its own files; the separately installed
Waylib runtime supplies its DSOs and QML module.

The install smoke uses that real runtime without `LD_LIBRARY_PATH`. Embedded
builds additionally need `-DDECKSHELL_TEST_WAYLIB_PREFIX="$waylib_prefix"` when
running this test; omitting it does not block ordinary configuration or builds.
See the root README for runtime import paths and environment-dependent tests.

## Packaging

A `debian` folder is provided to build the package under the *deepin* linux desktop distribution. To build the package, use the following command:

```shell
$ sudo apt build-dep . # install build dependencies
$ dpkg-buildpackage -uc -us -nc -b # build binary package(s)
```

## treeland-debug

`treeland-debug` is an adb-style command-line inspector and controller for the
running Treeland compositor. It connects to Treeland's debug Remote Object over
Qt Remote Objects and exposes subcommands for inspecting the window tree,
controlling windows, injecting input events and grabbing screenshots. Like `adb`,
it runs in two modes:

- **Non-shell (one-shot) mode** — the default: `treeland-debug <command> [args]`.
- **Shell mode** — an interactive REPL: `treeland-debug shell`.

The client builds as part of the normal Treeland build (it is on by default; pass
`-DBUILD_TREELAND_DEBUG=OFF` to skip it):

```bash
cmake -B build
cmake --build build --target treeland-debug
sudo cmake --install build --component treeland-debug
```

### Enabling the debug source

The debug Remote Object is opt-in: it is enabled by default in **Debug** builds
(so `treeland-debug` works out of the box without extra config), and in
**Release** builds it is off until you enable the `remoteDebug` DConfig option
as the `dde` user (Treeland runs as `dde` in global mode and its local socket is
owner-only). Toggling `remoteDebug` in Release builds takes effect immediately
-- the remote source is created or destroyed on the fly, no restart needed:

```bash
sudo -u dde -- dde-dconfig set \
  -a org.deepin.dde.treeland \
  -r org.deepin.dde.treeland \
  -k remoteDebug \
  -v true
```

All commands below are run as the `dde` user, e.g.
`sudo -u dde -- treeland-debug windows`.

### Socket naming and connection

Treeland publishes the debug source on a local socket whose default name is
`org.deepin.dde.treeland.debug` (placed in `QDir::tempPath()` — typically
`/tmp`, but respects `$TMPDIR` — by Qt, so a client running under any
`XDG_RUNTIME_DIR` can discover it). When that name is already taken
by another running treeland (global service, session service, local build),
a numeric suffix is appended (`org.deepin.dde.treeland.debug-1`, `-2`, …),
selected with a non-blocking advisory lock (the same approach libwayland uses
for Wayland sockets). A stale socket file left by a crashed instance is
reclaimed, and a live old-build instance (one without a lock file) is probed
and left alone.

Debug builds use a distinct base name (`org.deepin.dde.treeland.debug-dev`)
so a debug-compiled treeland can run alongside a release one. A debug-built
treeland-debug client automatically prefers the debug instance and falls back
to the release instance when the debug one is unreachable; a release-built
client uses the release instance. An explicit `--url` always overrides this
with no implicit processing.

### Global options

| Option | Default | Description |
| --- | --- | --- |
| `--url <url>` | auto: debug socket (debug build) with release fallback, else release socket | Remote object host URL. |
| `--name <name>` | `WindowTree` | Remote object name. |
| `--timeout-ms <n>` | `30000` | Request timeout in ms (non-negative integer). |
| `--json` | off | Emit machine-readable JSON for `tree`/`cursor`/`windows`/`clients`. |
| `--preview` | auto | Force inline image preview in terminal (auto-detected by default). |
| `--no-preview` | off | Disable inline image preview. |
| `-h, --help` | — | Show help. |
| `-v, --version` | — | Show version. |
| `--tree` / `--cursor` | — | Backward-compatible aliases for the `tree` / `cursor` commands. |

### Command reference

Window-control commands accept a target given by **numeric `id`** (printed by
`windows` / `clients` / `top`) or by **`appId`** (the first matching window is
used).

#### Inspection

| Command | Arguments | Output |
| --- | --- | --- |
| `tree` | _(none, default)_ | Layout tree (human-readable; `--json` for JSON). |
| `cursor` | _(none)_ | Cursor position `x=… y=…` (`--json` for `{"x","y"}`). |
| `windows` | _(none)_ | Window table; `--json` for a JSON array. |
| `clients` | _(none)_ | Client + window table; `--json` for a JSON array. |
| `top` | `[interval-ms]` (default 1000) | Live, `top`-like refreshing client view (Ctrl+C to quit). |

#### Window control

| Command | Arguments | Output |
| --- | --- | --- |
| `activate` | `<id>` | `ok` / `failed`. |
| `close` | `<id>` | `ok` / `failed`. |
| `minimize` | `<id>` | `ok` / `failed`. |
| `maximize` | `<id>` | `ok` / `failed` (toggles maximized). |
| `fullscreen` | `<id>` | `ok` / `failed` (toggles fullscreen). |
| `move` | `<id> <x> <y>` | `ok` / `failed`. |
| `resize` | `<id> <w> <h>` | `ok` / `failed`. |
| `workspace` | `<id> <ws-id>` | `ok` / `failed` (move window to a workspace). |

#### Input / event injection

| Command | Arguments | Output |
| --- | --- | --- |
| `move-cursor` | `<x> <y>` | `ok` / `failed`. |
| `event motion` | `<x> <y>` | `ok` / `failed`. |
| `event button` | `<left\|right\|middle\|code> [press\|release\|click]` | `ok` / `failed` (default `click`). |
| `event key` | `<name\|evdev-code> [press\|release\|tap]` | `ok` / `failed` (default `tap`). |

Pointer buttons use Linux input codes (`left`=0x110, `right`=0x111,
`middle`=0x112, or a numeric code). Keyboard keys use Linux evdev keycodes;
common names are recognised (`esc`, `enter`, `space`, `tab`, `a`–`z`, `0`–`9`,
arrow keys, `f1`–`f12`, `home`/`end`/`pageup`/`pagedown`/`insert`/`del`, …) or a
raw code may be passed. Keys are delivered to the keyboard-focused surface —
`activate` a window first to target it; pointer buttons go to the surface under
the cursor.

#### Image capture

Screenshots are rendered server-side and returned to the `treeland-debug`
client as PNG bytes; the client writes them to a file and prints the path.
The compositor itself never touches the filesystem. If `file` is omitted a
path under `/tmp` is generated.

| Command | Arguments | Output |
| --- | --- | --- |
| `screenshot output` | `[name] [file]` | PNG file path (stdout). |
| `screenshot window` | `<id> [file]` | PNG file path (stdout). |

#### Interactive

| Command | Arguments | Output |
| --- | --- | --- |
| `shell` | _(none)_ | REPL (`treeland>`) accepting all commands plus `help`/`exit`. |
| `help` | _(none)_ | Full help text. |

### Output formats

`tree` and `cursor` print a human-readable format by default; pass `--json` for
machine-readable JSON. `windows` and `clients` also default to human-readable
tables and use `--json` for JSON.
Window JSON object (`WindowInfo`):

| Field | Type | Notes |
| --- | --- | --- |
| `id` | integer | Stable window id (the wl_surface wl_resource pointer); globally unique, accepted by control commands. |
| `appId` | string | Application id. |
| `title` | string | Window title. |
| `output` | string | Output name. |
| `container` | string | Container name. |
| `workspace` | integer | Workspace id. |
| `layer` | integer | Layer id. |
| `z` | integer | Z order. |
| `type` | integer | Window type. |
| `state` | integer | `0` Normal, `1` Maximized, `2` Minimized, `3` Fullscreen, `4` Tiling. |
| `visible` | boolean | Visibility. |
| `active` | boolean | Active / focused flag. |
| `geometry` | object | `{"x","y","width","height"}`. |
| `titlebarGeometry` | object | Same shape. |
| `boundingRect` | object | Same shape. |
| `iconGeometry` | object | Same shape. |
| `position` | object | `{"x","y"}`. |
| `frames` | integer | Number of committed frames (from `wlr_surface`). |
| `damage` | object | Last committed buffer-damage rectangle `{"x","y","width","height"}`. |

Client JSON object (`ClientInfo`): `id` (integer), `appId` (string), `pid`
(integer, `0` when unavailable), `executable` (string), `windows` (array of
`WindowInfo`).

The `tree` JSON is
`{"currentMode": str, "layers": [{"name", "layer", "windows": [WindowInfo], "workspaces": [{"id", "isActive", "windows": [WindowInfo]}]}]}`.

### Exit codes

`0` on success; `1` on connection failure, RPC failure, an unknown command, or a
control command that returns `failed`.

### Usage examples

All commands run as the `dde` user:

```bash
# Inspect the window tree (human-readable, default command)
sudo -u dde -- treeland-debug tree

# Cursor position
sudo -u dde -- treeland-debug cursor
# → x=960 y=540

# List windows
sudo -u dde -- treeland-debug windows

# List clients and their windows
sudo -u dde -- treeland-debug clients

# Live refreshing top view (1 s interval)
sudo -u dde -- treeland-debug top
# (Ctrl+C to quit)

# Activate a window by id
sudo -u dde -- treeland-debug activate 1407374883553280

# Activate a window by appId
sudo -u dde -- treeland-debug activate dde-file-manager

# Move a window
sudo -u dde -- treeland-debug move 1407374883553280 100 200

# Resize a window
sudo -u dde -- treeland-debug resize 1407374883553280 800 600

# Move a window to workspace 2
sudo -u dde -- treeland-debug workspace 1407374883553280 2

# Move cursor
sudo -u dde -- treeland-debug move-cursor 960 540

# Send a pointer click
sudo -u dde -- treeland-debug event button left click

# Send a key tap
sudo -u dde -- treeland-debug event key enter tap

# Screenshot the primary output to a file
sudo -u dde -- treeland-debug screenshot output /tmp/ss.png

# Screenshot a window (with terminal preview if supported)
sudo -u dde -- treeland-debug screenshot window 1407374883553280

# Interactive shell mode
sudo -u dde -- treeland-debug shell
treeland> help
treeland> windows
treeland> exit

# Machine-readable JSON output
sudo -u dde -- treeland-debug --json windows
sudo -u dde -- treeland-debug --json cursor
```

The `top` view refreshes every `interval-ms` (default 1000 ms) using a QTimer.
Each cycle calls `getClients()` via Qt Remote Objects, clears the terminal
(`\033[2J\033[H`), and re-prints a header with the current timestamp and
client count, followed by the client + window table. Press Ctrl+C to stop.
## GitHub Actions / CI

This project uses GitHub Actions for continuous integration. The following workflows are configured:

- **waylib builds**: Triggered when `waylib/**` files are modified
- **treeland builds**: Main project builds

## Getting Involved

- [Code contribution via GitHub](https://github.com/linuxdeepin/treeland/)
- [Submit bug or suggestions to GitHub Issues or GitHub Discussions](https://github.com/linuxdeepin/developer-center/issues/new/choose)

## License

treeland is licensed under Apache-2.0 OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only.
