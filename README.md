# DeckShell

DeckShell 包含基于 Qt 6、Waylib 和配套 native wlroots 的 Wayland 合成器
`DeckCompositor`。本仓库使用 C++20、CMake 3.25 及以上版本。

默认构建消费**已经安装的 WaylibShared 开发包**，不需要物化
`3rdparty/waylib-shared`。`WITH_SUBMODULE_WAYLIB=ON` 仅用于显式内嵌开发；
没有安装包时不会自动切换到源码构建。

## 依赖与安装包准备

需要 Qt 6.8 及以上的 Core、Gui、Qml、Quick、QuickControls2、DBus、Test、
QuickTest、ShaderTools、LinguistTools、Concurrent、RemoteObjects、Network 及
对应 Private 开发文件，以及 Dtk6 Core、Declarative、SystemSettings、Tools。
其余系统依赖由 CMake/pkg-config 检查，包括 Wayland、wayland-protocols、
pixman、libinput、XCB、libsystemd 和 Xau。启用 DDM 时还需要匹配的 DDM 和 PAM。

WaylibShared 开发包必须包含 `WaylibShared::SharedServer`、
`WaylibShared::waylib-wlroots`、`WaylibShared::qtwaylandscanner`、
`waylib_generate_qtwayland_server_protocol()`、QML 模块和 wlroots 协议数据。
不要用独立系统 wlroots 替换包中配套的 native 库。Qt Private、Waylib 和 native
wlroots 的 ABI 有版本耦合，开发包与运行包必须来自相配套的构建。

已有上述包时，直接进入下一节。需要本地构建 Waylib 包时，直接配置完整的
Waylib 源码；remote-subsurface XML 随配套实现一同提供，不需要预装
`DeckCompositorProtocols`。以下命令从 DeckShell 仓库根执行，安装到用户目录，
不写系统前缀：

```sh
waylib_prefix="$PWD/_local/waylib"

# 若使用本仓库提供的 Waylib 源码，先显式初始化；也可改为独立 Waylib checkout。
git submodule update --init --recursive -- 3rdparty/waylib-shared
waylib_source="$PWD/3rdparty/waylib-shared"
cmake -S "$waylib_source" -B build-waylib -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_INSTALL_PREFIX="$waylib_prefix" \
  -DCMAKE_INSTALL_LIBDIR=lib \
  -DTREELAND_INSTALL_DEV=ON -DBUILD_WAYLIB_TESTS=ON
cmake --build build-waylib --parallel 6
ctest --test-dir build-waylib --no-tests=error --output-on-failure
cmake --install build-waylib
```

Waylib 配置只读取自身 `waylib/protocols/` 中的配套 XML，不要求 DeckShell 源树，
也不查找外部协议包；缺失库内 XML 时会明确失败，不回退到其他安装。
Waylib 自身的系统依赖及自定义安装目录说明见其
[README](3rdparty/waylib-shared/README.md)。

## 默认安装包消费

以下仍从 DeckShell 仓库根执行；`waylib_prefix` 指向上一节或发行包提供的安装前缀。
DeckShell 的仓内协议继续由 `protocols/compositor` 提供，不从旧 Treeland 安装补齐。

```sh
deckshell_prefix="$PWD/_local/deckshell"
cmake -S . -B build -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_PREFIX_PATH="$waylib_prefix" \
  -DCMAKE_INSTALL_PREFIX="$deckshell_prefix" \
  -DCMAKE_INSTALL_LIBDIR=lib
cmake --build build --parallel 6
ctest --test-dir build --no-tests=error --output-on-failure
cmake --install build
```

`WITH_SUBMODULE_WAYLIB` 默认 `OFF`；此路径不编译 Waylib/native 源码、不读取 child
helper 或头目录，也不执行 child 的安装脚本。使用多个依赖前缀时，用分号分隔
`CMAKE_PREFIX_PATH`；新前缀应在系统旧安装之前，必要时显式指定 `WaylibShared_DIR`。

测试默认保留协议、native、Glass 和安装 smoke。Wayland 测试需要真实本地 socket
权限；协议夹具需要 PATH 中可执行的 `dbus-daemon` 与 `dde-dconfig-daemon`，并启动
私有 D-Bus/DConfig 服务。XWayland 还要求 `/tmp/.X11-unix` 由 root 或运行用户拥有；
隔离环境可以使用私有目录，不能修改桌面会话的 socket。Glass 的像素断言需要可用的渲染后端。
缺少这些条件属于环境限制，不等于测试通过。

## 运行与安装所有权

DeckShell 只安装自身产物；Waylib/native DSO、QML plugin、qmldir、qmltypes
由独立 Waylib 包安装和维护。自定义非系统前缀下，DeckShell 安装产物保留选中外部
依赖的安装目录，不要求 `LD_LIBRARY_PATH` 或旧 build tree。若移动依赖安装前缀，
需要重新配置并安装 DeckShell；这不同于 Waylib 包自身的可迁移性。

QML import root 需要包含 DeckShell 与 Waylib 两份模块。例如上面显式选择 `lib`
的默认布局可使用：

```sh
QML_IMPORT_PATH="$deckshell_prefix/lib/qt6/qml:$waylib_prefix/lib/qt6/qml" \
  "$deckshell_prefix/bin/deckcompositor"
```

Waylib 的实际目录由 `WaylibShared_QML_IMPORT_DIR`、`WaylibShared_LIBDIR`、
`WaylibShared_WLROOTS_PROTOCOLS_DIR` 和 `WaylibShared_PKGCONFIG_DIR` 提供；
自定义布局不要照抄示例中的 `lib`。安装 smoke 自动使用这些元数据，在隔离目录
安装 `DeckShellQmlRuntime`，清除动态库路径覆盖后用纯 Qt QML runtime 导入
`DeckShell.Compositor`，不会修改生成的安装脚本或借用 child build 的 QML 模块。

## 显式内嵌开发

```sh
git submodule update --init --recursive -- 3rdparty/waylib-shared
cmake -S . -B build-embedded -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug -DWITH_SUBMODULE_WAYLIB=ON \
  -DDECKSHELL_TEST_WAYLIB_PREFIX="$waylib_prefix"
cmake --build build-embedded --parallel 6
ctest --test-dir build-embedded --no-tests=error --output-on-failure
```

内嵌模式沿用相同公开 target、协议 helper 和目录合同，仍只安装 DeckShell 自有
产物。`DECKSHELL_TEST_WAYLIB_PREFIX` 是安装 smoke 的配套 runtime 输入，不能指向
Waylib build tree。该选项不参与普通内嵌编译；未提供时配置和构建仍可运行，
但安装 smoke 会明确失败并说明缺少条件，不静默跳过。提供后，该测试仅把配套
已安装的两个 runtime DSO 放入临时部署树，QML 模块仍来自所选安装包。

合成器及 `treeland-debug` 的进一步使用说明见
[compositor/README.zh_CN.md](compositor/README.zh_CN.md)。
