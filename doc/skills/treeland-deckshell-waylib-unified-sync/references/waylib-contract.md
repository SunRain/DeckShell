# waylib-shared 构建、安装与 package 合同

## 受保护合同

C 普通内容位于 `qwlroots/**`、`waylib/**`、`wlroots/**`；R 位于 C 的 `3rdparty/wlroots` 子模块。精确登记和获批的 C 根 CMake 接入不等于放宽 package 合同。默认阻断：

- installed file/public header 路径新增、删除、移动；
- package `*Config.cmake`、`*Targets.cmake` 文件路径变化；
- exported target 或 `WaylibShared::*` namespace 变化；
- 已安装 target 的公共属性值变化，包括 `INTERFACE_*`、导入配置的 location/soname/链接接口、配置映射和兼容性属性；
- installed public header 的 namespace 集合变化；
- pkg-config Name/Version/Requires/Libs/Cflags 变化；
- 源码中的非测试核心 CMake target、`install(...)`、package 生成、PUBLIC/INTERFACE include、export namespace 变化；
- `qwlroots/**` 或 `waylib/**` 内 `CMakePresets.json`，以及 `EXPORT_NAME`、`OUTPUT_NAME`、`PUBLIC_HEADER` target 属性变化；
- 受保护源码表达式所引用的 `set/option` 定义变化，包括传递引用；不能只比较 `${TARGET}` 这类未展开的名称；
- 已有 package consumer configure/build 失败。

PRIVATE 依赖、PRIVATE include、测试 target 或 private 实现可变化，但在每个所选关键节点仍须通过 fresh build/install 与 consumer。源码扫描会忽略 `tests/**`、`examples/**` 目标；安装快照是该节点的 package 边界权威。普通中间提交不要求完整构建，不豁免下述逐提交源码合同检查。

## 逐提交源码预检

每次 C commit 后、对应 P commit 前，replay 从相邻 Git 树生成 `waylib-source-contract-audit`。比较非测试核心 target、install/package/PUBLIC/INTERFACE include/export namespace、受保护属性、CMakePresets 和变量依赖；同时记录公共调用与相关 set/option/unset 定义的条件、作用域、顺序、函数调用和 include/add_subdirectory/return 等入口。未改变调用文字不代表执行合同不变。公共头的命名空间宏保留 include、条件与 undef 后展开，无法求值则阻断。工件位于 `commits/<source-sha>/child-source-contract-audit.json`。

未经精确批准的中间节点漂移都阻断，即使范围末尾会恢复。例如 `Core → BrokenCore → Core` 在第一次变化处停止，parent gitlink 不会指向 BrokenCore。保留 child commit 和 journal；同身份 resume 和 child verifier 必须重算审计并验证工件哈希，不能改 JSON 放行。

公共迁移须有调用者明确授权，并使用 [contract_migration 审批](evidence-schema.md#显式公共合同迁移) 精确绑定来源、前后快照、实际差异和必要本地调用方；不自动移除旧包或变更命名空间。源码和安装分别审批，旧 wrapper-only 批准不能豁免删除/替换。保留的合同、新 API 和候选实际安装包仍完整验收，报告显示批准的真实变化而不是 `drift={}`。

源码预检采用保守规则，不是任意 CMake 求值器：受保护执行上下文改变就阻断；应通过目标适配保留原合同，不能靠说明豁免。仅新增 wrapper 时可精确批准根部 `add_subdirectory(wlroots)` 及 wrapper 新增项，已有上下文变化仍拒绝。已知私有调用的变更不纳入公共门禁。安装后的 public header、namespace、导出属性与真实 consumer 仍须按下述流程验证，不能由静态扫描代替。

## 基线与 candidate

使用 SKILL.md 物化步骤从冻结 `CHILD_BASE` 建立的 `CHILD_BASE_WT`，candidate 使用 replay child worktree。不得以主工作树或旧构建代替。

build、install、consumer 目录可放在持久 artifact root 下，但必须与源码 worktree 分离。base 与 candidate source worktree 必须 clean；合同审计在读取源码前再次检查。对两者都执行 fresh configure/build/install；每个 configure 的 `-B` 和 install 的 `--prefix` 必须在命令执行前不存在，并由 validation evidence 与最终报告复验，不能复用旧 CMake cache 或安装树。

此处 base/candidate 属于当前关键节点分段，接续规则见 [关键节点分段验收](key-node-validation.md)。四个必需 CMake build ID 使用默认完整构建，只允许配置、并行数、详细输出和 `--clean-first`；目标选择、原生 `-- ...` 参数、帮助和空跑不能充当验收。

C candidate 必须在 P 的固定 gitlink 路径物化。R 模式用 `materialize-child --wlroots-repo ... --child-base-worktree ...` 同时处理 C/P 所需的两层依赖；C0 未登记 R 时不往基线注入目录。所有记录传 `--manifest`，据此在命令前后重查源及各依赖 SHA/common Git directory/linked/clean。旧单层 `--nested-checkout/--nested-head` 不能单独证明 R。

示例调用统一使用 `validation_record.py`：

```bash
python3 "$SKILL_DIR/scripts/validation_record.py" \
  --id waylib-base-configure --category build --cwd "$CHILD_BASE_WT" \
  --manifest "$ARTIFACT_ROOT/manifest.json" \
  --artifact-root "$ARTIFACT_ROOT" --bundle "$ARTIFACT_ROOT/validations.json" -- \
  cmake -S "$CHILD_BASE_WT" -B "$WAYLIB_BUILD_BASE" -G Ninja -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DBUILD_WAYLIB_TESTS=ON -DBUILD_QWLROOTS_TESTS=ON

python3 "$SKILL_DIR/scripts/validation_record.py" \
  --id waylib-base-build --category build --cwd "$CHILD_BASE_WT" \
  --manifest "$ARTIFACT_ROOT/manifest.json" \
  --artifact-root "$ARTIFACT_ROOT" --bundle "$ARTIFACT_ROOT/validations.json" -- \
  cmake --build "$WAYLIB_BUILD_BASE"

python3 "$SKILL_DIR/scripts/validation_record.py" \
  --id waylib-base-install --category build --cwd "$CHILD_BASE_WT" \
  --manifest "$ARTIFACT_ROOT/manifest.json" \
  --artifact-root "$ARTIFACT_ROOT" --bundle "$ARTIFACT_ROOT/validations.json" -- \
  cmake --install "$WAYLIB_BUILD_BASE" --prefix "$WAYLIB_INSTALL_BASE"
```

candidate 对应 ID 为 `waylib-candidate-configure`、`waylib-candidate-build`、`waylib-candidate-install`，参数改为 candidate worktree/build/install。两侧都必须测试：

```bash
python3 "$SKILL_DIR/scripts/validation_record.py" \
  --id waylib-base-ctest --category test --cwd "$CHILD_BASE_WT" \
  --manifest "$ARTIFACT_ROOT/manifest.json" \
  --artifact-root "$ARTIFACT_ROOT" --bundle "$ARTIFACT_ROOT/validations.json" -- \
  ctest --test-dir "$WAYLIB_BUILD_BASE/waylib" --output-on-failure --no-tests=error

python3 "$SKILL_DIR/scripts/validation_record.py" \
  --id waylib-ctest --category test --cwd "$CHILD_WT" \
  --manifest "$ARTIFACT_ROOT/manifest.json" \
  --artifact-root "$ARTIFACT_ROOT" --bundle "$ARTIFACT_ROOT/validations.json" -- \
  ctest --test-dir "$WAYLIB_BUILD_CANDIDATE/waylib" --output-on-failure --no-tests=error
```

记录器先执行无过滤 `--show-only=json-v1`，保存发现结果并要求实际测试完整覆盖；空顶层、别的 build、只跑可通过的子集均不能替代 `BUILD/waylib`。新旧 CTest 摘要都支持；0 tests、failed、Not Run、Skipped 和无法解析均不能满足必需测试。

## 已有 package consumer

使用 waylib-shared 自带 `test_project/`，不要编造新的伪 consumer。configure、build 和 CTest 三步都必须是独立的必需验证；consumer build 目录必须 fresh，且只连接 candidate install：

```bash
python3 "$SKILL_DIR/scripts/validation_record.py" \
  --id waylib-package-consumer-configure --category build --cwd "$CHILD_WT" \
  --manifest "$ARTIFACT_ROOT/manifest.json" \
  --artifact-root "$ARTIFACT_ROOT" --bundle "$ARTIFACT_ROOT/validations.json" -- \
  cmake -S "$CHILD_WT/test_project" -B "$WAYLIB_CONSUMER_BUILD" -G Ninja \
    -DCMAKE_PREFIX_PATH="$WAYLIB_INSTALL_CANDIDATE" -DBUILD_TESTING=ON

python3 "$SKILL_DIR/scripts/validation_record.py" \
  --id waylib-package-consumer-build --category build --cwd "$CHILD_WT" \
  --manifest "$ARTIFACT_ROOT/manifest.json" \
  --artifact-root "$ARTIFACT_ROOT" --bundle "$ARTIFACT_ROOT/validations.json" -- \
  cmake --build "$WAYLIB_CONSUMER_BUILD"

python3 "$SKILL_DIR/scripts/validation_record.py" \
  --id waylib-package-consumer --category consumer --cwd "$CHILD_WT" \
  --manifest "$ARTIFACT_ROOT/manifest.json" \
  --artifact-root "$ARTIFACT_ROOT" --bundle "$ARTIFACT_ROOT/validations.json" -- \
  ctest --test-dir "$WAYLIB_CONSUMER_BUILD" \
    --output-on-failure --no-tests=error
```

三个固定 ID 缺一不可。最后一条命令必须使用 `--no-tests=error`，因此未注册测试不能冒充 consumer 成功；`validation_record.py --category consumer` 同时生成合同审计所需的 `waylib-package-consumer-result.json`。

独立审计重读已哈希日志及测试发现工件，要求 total/passed/failed/skipped 与 JSON 一致且非零全通过；全部或部分 skipped 的 exit 0 仍失败。最终报告复用相同结论，不只信 outcome 字段。

## R 原生构建与 wrapper 接入

R 原始工程用 Meson；C 的 `wlroots/CMakeLists.txt` 是被 C/P 顶层包含的包装层，不当独立 CMake 工程。R0 与 R candidate 各自使用 clean linked worktree 和独立 fresh build，例如 R0 工作树尚未创建时：

```bash
git -C "$WLROOTS_REPO" worktree add --detach "$WLROOTS_BASE_WT" "$WLROOTS_BASE"
```

base/candidate 分别以对应的 `--cwd`、build 和 `wlroots-base-*` / `wlroots-candidate-*` ID 执行以下三个命令体，均由 `validation_record.py --manifest ...` 记录：

```bash
meson setup "$WLROOTS_BUILD" "$WLROOTS_WT" --buildtype=release --wrap-mode=nodownload
meson compile -C "$WLROOTS_BUILD"
meson test -C "$WLROOTS_BUILD" --print-errorlogs
```

空 R 基线不添加跳过参数：仍按上述方式调用三个 `wlroots-base-*` ID。记录器从 manifest 首个来源节点的唯一父提交解析冻结的 `range_base`，重新读取该提交的 `3rdparty/wlroots` 以及真实 R0 commit 的整个根树。仅“来源子树不存在且 R0 为空树”成立时，不启动 Meson、不创建构建目录，自动写出三个 `not-applicable` 记录和内容寻址的 Git 证明。报告独立重读对象；仅有 `source_base_tree: null`、缺少 `meson.build` 或已批准的基线差异都不能代替这两个事实。

三个基线记录仍缺一不可，保留 clean linked worktree 与 manifest 绑定；结果明确 `executed: false`、`exit_code: null`，不填写测试计数，也不伪造执行成功或 NO_TESTS。R candidate 即使仍为空也必须实际执行 Meson；C/P 构建、安装消费链以及两个 R 内容/gitlink gate 均维持原要求。

对应后缀为 configure（build 类）、build（build 类）、test（test 类）。记录器自动运行 Meson introspect --tests，并注入 `--logbase=treeland-<id>-attempt-<N>`，要求对应 JSON 日志执行前不存在。`--list`、`--help`、`--benchmark`、关闭日志及用户指定 logbase 均拒绝；不再读取默认旧 `testlog.json`。报告重查命令、ID/attempt、日志路径和 freshness 证据。结果必须覆盖完整发现集合；零注册测试为 NO_TESTS，不替代构建。持久测试证据仅保留 name/result/returncode，不复制进程环境。

C/P 的 R 模式配置必须是 Ninja、`CMAKE_EXPORT_COMPILE_COMMANDS=ON`；构建证据保存 codemodel/compile_commands/Ninja 命令、实际编译依赖和生成头摘要。wrapper 产物必须同时属于具体消费目标的 codemodel 链接库，以及产生该目标的真实链接命令输入；按完整路径比较，排除 wrapper 自身输出与纯 `add_dependencies`。只放置未使用的生成头或回退系统 wlroots 均不能放行；报告重新读取工件执行同一检查。

已独立验收的原生 Meson 包装层使用 CMake `waylib_wlroots_native` 入口定位同目录的 `native/` 构建，不伪装成 CMake 编译目标。记录器额外保存 Meson 目标来源、真实编译数据库与 Ninja 依赖；必须证明库由当前 R 源码编译、生成头确实被 R 及 C/P 使用、具体 C/P 目标链接该库的完整路径。仅构建 native 库、借用另一源码树或系统库仍阻断；此规则同样适用于分段基线，不复用前一节点的 PASS。

新增 wrapper target/安装产物需精确批准，格式见 [证据格式](evidence-schema.md)。wrapper-only 批准只接受 wrapper 新增项，不能修改旧核心 target、public header、导出与安装合同。qwlroots 0.19 与来源 wlroots 0.20 的 API 兼容不能由目录映射推定；需要公共迁移时必须另有上述明确授权和精确审批，不因依赖目录变化自动放行。

当 C 已登记 R 且对应来源树包含 `wlroots/update-from-upstream.sh`，或 C 已保留该脚本时，目标必须继续保留该路径；来源后来删除脚本也不能自动撤销目标保留规则。来源与目标均无该脚本的旧场景不凭空创建文件。脚本必须是 mode 为 `100644` 或 `100755` 的普通 blob，不能是 symlink、目录或 gitlink，并在原脚本内容前加入固定拒绝前缀：

```bash
#!/usr/bin/env bash
printf '%s\n' 'waylib-shared uses a wlroots submodule; use unified sync to update it.' >&2
exit 64
```

该前缀由 `wlroots.UPDATER_GUARD` 核验；必须在任何 fetch/subtree/写 ref 之前退出。普通 `omitted`/`empty` 或适配证明不得豁免文件存在性、类型与拒绝前缀。暂存树、提交后、恢复和独立 Waylib 验证共用 `updater_guard_errors`，从 Git 对象读取，而非以工作目录中的文件存在性为准。UPSTREAM 只作为数据读取，保留 SOURCE_URL/REF/COMMIT/VERSION 的纯上游信息，并追加 submodule 布局说明，不以目标 SHA 覆盖上游 pin。

## 快照比较

`waylib_contract_audit.py` 同时读取 base/candidate install root 和 source root。快照记录完整安装相对路径与内容 hash；比较使用 package-facing 语义，不因普通头文件内容或注释变化直接阻断。

pkg-config 将被查 .pc 的目录置于搜索首位，按包名查询并核验 `pcfiledir` 的实际绝对路径；不能回退到系统同名包。本安装树的依赖优先，其他依赖使用工具的系统搜索目录。清除继承的 `PKG_CONFIG_*` 覆盖，避免其他安装树或 sysroot 冒充本次结果；保留系统 include/lib 参数以便比较。原生查询提供 Version、Requires/Requires.private、Cflags/Libs 及 `--static` 参数，Name 变量也由原生查询展开。命令参数按 shell 转义解码后只归一化安装根，不排序，不因 consumer 通过豁免变化。工具缺失、包无效或依赖查询失败直接失败，不退回字面字段；包名查询避免 pkg-config 把含空格的绝对文件名拆成多个包表达式。

快照的每个 pkg-config 项必须包含实际求值的 `Cflags.static`、`Libs.static` 等字段；旧字面快照和依赖其生成的报告必须重建，不能仅补字段或修改摘要。

导出属性通过临时 CMake 工程加载已安装 Config 入口获取；没有 Config 时加载 Targets 入口。读取每个 imported target 的实际属性，不再用正则推测变量展开。`exported_target_properties` 保存 `target -> property -> value`；本次 install root 统一替换为 `<install-root>`，列表顺序、生成器表达式和配置专属属性保留。CMake 配置失败直接返回 `fail`，不降级成文本结果。该探测随本 skill 使用 CMake 3.27+、C/C++ 编译器和被审包的配置依赖，不构建产品。

```bash
python3 "$SKILL_DIR/scripts/waylib_contract_audit.py" \
  --before "$WAYLIB_INSTALL_BASE" --after "$WAYLIB_INSTALL_CANDIDATE" \
  --source-before "$CHILD_BASE_WT" --source-after "$CHILD_WT" \
  --consumer "$ARTIFACT_ROOT/waylib-package-consumer-result.json" \
  --artifact-root "$ARTIFACT_ROOT" \
  --output "$ARTIFACT_ROOT/waylib-contract-audit.json"
```

缺任一 install root、只构建 candidate、缺 consumer CTest 日志或 log hash 不符时，结果只能是 `fail/blocked`。审计器记录两个 source worktree 的实际 HEAD；最终报告要求它们分别等于 manifest 的 child base/candidate，并独立要求上述 configure/build/CTest 三个 validation ID。合同审计中的 consumer 记录还必须与 validation bundle 的 `waylib-package-consumer` 当前 attempt 一致。

审计器另生成固定写出基线完整 namespace 的编译探针（例如 `::Waylib::Server`），通过候选安装包配置编译；不使用候选 SERVER_NAMESPACE 宏自适应。探针失败、快照绑定不同或源码工件被替换都会阻断。

每个基线公共头分别在独立翻译单元中检查其固定命名空间，完整构建覆盖全部这些单元；不把所有公共头合并编译，避免基线头之间的重复定义干扰命名空间检查，也防止其他头补齐候选中实际缺失的命名空间。

安装命名空间投影使用真实导出属性中的安装树 include 根定位同名协议头；多个有效根仍有歧义时阻断，不按文件内容相同或排序任取其一。仅与命名空间有关的条件及其错误指令进入投影，已剥离条件内的错误指令不能提升到外层；外部头的实际编译约束仍由逐头安装探针验证。

报告还会从两份快照重算合同差异，而非直接相信审计的 `pass`。缺少 `exported_target_properties` 的旧快照必须重新生成；不能只补字段或改 hash。consumer 通过只能证明该 consumer 的使用路径，不能豁免其他公共属性漂移。
