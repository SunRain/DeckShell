# 协议测试的 DConfig 隔离运行方案

## 适用范围与实现边界

本方案用于统一同步的本地节点验收：当 parent candidate 的协议测试依赖 DConfig、宿主未安装 `dde-dconfig-daemon` 时，使用可追溯的隔离运行依赖启动私有服务，不以安装或启用系统服务为前提。依赖缺失须在 compositor 首次使用 DConfig 前明确失败，不能等到泛化的 `DConfig is invalid` 才定位环境问题。

固定的是依赖准备、隔离和失败处理合同，不是某个包版本、历史绝对路径或 helper 的内部实现。没有 DConfig 依赖的测试不套用本要求；它也不改变 C/R 的验证范围或协议 XML 来源合同。

**已有能力与待实施要求必须分开：** 固化本方案时，`compositor/tests/protocols/framework/test-dconfig-service.cpp` 已通过 `execlp` 按 `PATH` 启动真实 daemon，并创建私有 D-Bus；但父进程仅以 `fork()` 成功判断启动成功，`protocol-test-entry.cpp` 仍在 `Treeland::preInit/postInit` 后检查服务就绪。因此下面的依赖准备方式可用于现有框架，完整的“初始化前报告启动失败、确认服务就绪”仍是待实施要求，不得因保存本文而宣称已修复。每次同步须以实际候选源码复核该边界。

框架 README 当前将 DConfig helper 与 AccountsService 模拟一并描述为临时 CI 设施。这里固定的是**本地同步验收的隔离运行方式**，不固定 AccountsService mock，也不裁定所有 CI 必须保留同一 helper。后续获准修改测试框架时，应同步澄清 README 中 DConfig 的适用范围；本方案不授权自动修改候选源码或扩大 replay 路径。

## 每次验证需要提供的信息

| 输入 | 要求 |
|---|---|
| 依赖来源 | 提供 daemon 的包名、版本、架构、可信仓库或获取地址，以及已有包管理体系的签名或校验依据；不能只记录一个可执行文件名 |
| 本地运行位置 | 包与解包目录位于源码 worktree 外的持久 artifact 目录，例如 `$ARTIFACT_ROOT/runtime-dependency/`；记录实际 daemon 路径，不依赖历史方案目录必然存在 |
| 运行兼容性 | 确认宿主架构、动态库满足该包要求，`dbus-daemon` 可用，运行环境允许私有 D-Bus/Wayland 所需的本地 Unix socket；不能把 socket 权限失败误报为包缺失 |
| 当前测试身份 | 使用本段 manifest、parent candidate 和本次 build；DSG 数据及 `TREELAND_PROTOCOL_TEST_DSG_DIR` 等测试环境来自该候选的 CMake 配置，不借用旧 build 或宿主配置数据 |

在已有 `refs_doc` 或本段运行依赖记录中保存上述来源和实际使用位置，沿用 `validations.json` 与原始日志记录测试。无需新增证据 schema、通用依赖管理器或独立 gate。复用发行版已有的包校验机制；仅有自行计算的摘要不能证明包来源可信。

历史方案 `20260909_treeland_0_8_14_to_0_9_1_local_sync` 的 N7 使用过 Arch `extra/deepin-app-services 1.0.45-1`、x86_64 包，在 `runtime-dependency/dependency.json` 记录来源、仓库摘要和 `system_install: false`。这是已用过的依赖示例，不是永久版本约束、当前可下载承诺或新候选通过证明；其他发行版须选择与宿主兼容且来源明确的包。

## 依赖准备与验证入口

1. 从本段候选的测试注册和启动代码确认 DConfig 依赖，不因看到任意 DConfig 警告就扩大所有测试的前置条件。
2. 在当前授权和网络权限内准备可信包，核对包身份后仅解包到本次 artifact 目录，不执行系统安装或服务启用。可复用已核对的本地包，但要在本段记录实际使用的来源与位置；包不可用时报告缺口，不猜下载地址或静默换版本。
3. 检查实际 daemon 路径、执行权限、动态库、`dbus-daemon` 和本次 DSG 数据。包不存在、不可执行或运行环境不满足时明确停止受影响验证，不把结果写成 SKIP/PASS。
4. 仅给验证记录器及其子进程提供 daemon 路径，再运行完整 compositor CTest。保留候选 CMake 设置的 headless、renderer、DSG 等测试环境；不要关闭协议测试或删减注册集合以绕过依赖。
5. 由测试框架启动和回收私有 D-Bus、daemon 与临时运行目录，不手动启动宿主 daemon，不使用 `systemctl` 或修改登录 shell 环境。持久依赖包和验证日志保留在 artifact 目录，不作为测试临时资源清理。

以下 Bash 示例仅演示**已核对并解包依赖后的接入**。包在 `root/usr/bin` 提供 daemon；其他布局应使用其实际目录。`SKILL_DIR`、`PARENT_WT`、`CHILD_CANDIDATE`、`ARTIFACT_ROOT` 和 `DECKSHELL_BUILD` 沿用 [主流程](../SKILL.md) 中本段已确认的绝对路径或 SHA。示例中的文件检查不替代动态加载或服务就绪验证。

```bash
(
    DCONFIG_BIN_DIR="$ARTIFACT_ROOT/runtime-dependency/root/usr/bin"
    if ! test -x "$DCONFIG_BIN_DIR/dde-dconfig-daemon"; then
        printf 'DConfig runtime missing or not executable: %s\n' \
            "$DCONFIG_BIN_DIR/dde-dconfig-daemon" >&2
        exit 1
    fi
    if ! command -v dbus-daemon >/dev/null 2>&1; then
        printf 'DConfig runtime requires dbus-daemon on PATH\n' >&2
        exit 1
    fi
    PATH="$DCONFIG_BIN_DIR:$PATH" \
        python3 "$SKILL_DIR/scripts/validation_record.py" \
        --id deckshell-compositor-ctest --category test --cwd "$PARENT_WT" \
        --manifest "$ARTIFACT_ROOT/manifest.json" \
        --nested-checkout "$PARENT_WT/3rdparty/waylib-shared" \
        --nested-head "$CHILD_CANDIDATE" \
        --artifact-root "$ARTIFACT_ROOT" --bundle "$ARTIFACT_ROOT/validations.json" -- \
        ctest --test-dir "$DECKSHELL_BUILD/compositor" --output-on-failure
)
```

`PATH` 设置在记录器外层；它收到的命令仍以 `ctest` 开头。当前 [validation_record.py](../scripts/validation_record.py) 依赖这个首程序名采集完整 CTest 发现集合，因此不能改成 `-- env PATH=... ctest ...` 或 `-- bash -c ...`。需要运行可选顶层 CTest 时沿用相同环境接入方式和既有验证 ID，不以过滤后的协议子集替代正式全量记录。

测试框架应把 `DBUS_SYSTEM_BUS_ADDRESS`、`DBUS_SESSION_BUS_ADDRESS` 指向本测试的私有总线，并用本候选 DSG 数据设置临时 DConfig 前缀。环境变量只影响测试进程树；不预先连接宿主总线，也不要求真实桌面会话提供服务。若实际候选不具备该隔离能力，先报告框架缺口，不能用宿主系统服务静默替代。

## 启动与失败诊断的待实施合同

下面约束测试框架的可观察行为，不规定私有类、进程启动 API 或容器类型。落实到源码前须取得对应范围的授权，并按既有来源映射和适配证据流程处理。

- 在首次创建或使用 DConfig 的 compositor 初始化之前，确认所选 daemon 可执行、进程真正启动，并在有界等待内确认私有总线上 `org.desktopspec.ConfigManager` 就绪；`fork()` 返回 PID 或仅等待固定时长都不等于就绪。
- 找不到程序、执行权限不足、动态加载失败、进程提前退出、总线启动失败或服务注册超时，应非零退出并给出具体失败阶段、所选可执行路径及可取得的系统错误或子进程诊断；不能只输出泛化 DConfig 初始化错误，也不能继续初始化 compositor。
- 启动失败和正常结束都应回收本测试拥有的 daemon、私有 D-Bus 与临时目录，不触碰宿主服务或持久依赖记录。清理异常要可见，不能因退出路径绕过清理而声称隔离完整。

## 验收与结果边界

| 场景 | 可观察的验收结果 |
|---|---|
| 宿主未安装 daemon，隔离包可用 | 日志能确认使用本次隔离依赖和私有服务，实际进入协议断言；包准备成功或服务启动成功本身不等于测试通过 |
| 隔离 daemon 缺失或不可执行 | 在 compositor 初始化前明确失败并指出路径；不能命中框架的 skip 返回码、写入 PASS 或退回宿主 daemon |
| daemon 无法加载、提前退出或服务未就绪 | 在有界时间内指出具体启动失败，compositor 不进入依赖 DConfig 的初始化；此项需框架完成上述待实施合同后实测 |
| 环境禁止本地 Unix socket | 独立报告运行权限限制，保留原始错误；不归因为协议实现回归，也不自动扩大执行权限 |
| 正常结束或启动失败 | 私有进程与临时资源被回收，宿主服务及持久验证材料不受影响 |
| DConfig 正常后仍有协议断言失败 | 按实际协议及断言单独记录；例如 screencopy 未收到 `ready` 不能继续算作 daemon 缺失 |

验收证据绑定当前候选和本次完整测试结果，仍服从既有 `NO_TESTS`、Skipped/Not Run 和失败判定。历史 N7/N8a 运行记录只能说明方案来源，不能替代本段执行。若本次仅落实 skill 文档，交付必须明确“方案已固化，框架启动诊断仍待实施”，不得声明上述全部运行场景已通过。
