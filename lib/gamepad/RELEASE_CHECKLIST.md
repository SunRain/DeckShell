# Release checklist（shared / 发行版发布步骤）

本文用于固化 **DeckShellGamepad（Linux-only / core-only）** 在发行版以 **shared** 形式发布时的检查清单与回滚策略。

适用范围：
- ✅ core（C++ / `Qt6::Core` + `libudev`）
- ❌ `-qml` / `-treeland`（P1，不在本次发布承诺内）

参考文档：
- 产物清单：`ARTIFACTS.md`
- 版本与兼容性：`VERSIONING.md`
- 对外变更日志：`CHANGELOG.md`
- 已知限制：`README.md`（“⚠️ 已知限制（Beta/RC）”）

---

## 0) 发布前结论（Gate）

发布前必须给出结论（建议写入 release notes 或 PR 描述）：
- [ ] 发布目标：Beta/RC（Linux-only / core-only）
- [ ] 连接方式基线：USB（蓝牙/2.4G 作为 P1）
- [ ] 基线手柄：≥2 台（deviceId/证据日志已落盘）

---

## 1) 版本号与 ABI（shared）

- [ ] 选择新版本号 `MAJOR.MINOR.PATCH`（规则见 `VERSIONING.md`）
- [ ] 更新 `CMakeLists.txt` 中 `project(DeckShellGamepad VERSION x.y.z ...)`
- [ ] 检查 `src/CMakeLists.txt` 中 `SOVERSION` 是否与 `MAJOR` 对齐（ABI break → bump `MAJOR` + bump `SOVERSION`）
- [ ] 如存在对外破坏性变更：在 `VERSIONING.md` 的 Breaking Change 规则下逐条对照确认

---

## 2) Changelog（对外可感知变更）

- [ ] 更新 `CHANGELOG.md` 的 `[Unreleased]`：
  - 只写对外可感知内容（API/行为/依赖/已知限制变化）
  - 不写纯重构细节（除非影响可观察行为）
- [ ] 发布时将 `[Unreleased]` 条目移动到新版本小节并写入发布日期

---

## 3) 合规与第三方（Release blocker）

> ⛔ 对外发布前，合规项不允许处于 “TBD” 状态。

- [ ] `THIRD_PARTY.md` 中 `data/gamecontrollerdb.txt` 的来源版本从 `TBD` 补齐到可追溯版本（commit/tag/date）
- [ ] `LICENSE` / `NOTICE` / `THIRD_PARTY.md` 三者一致且可审计
- [ ] 确认发行版拆包时携带必要的许可证文本（尤其是第三方数据文件）

---

## 4) 构建与安装（shared / staging）

推荐用 staging 前缀验证安装产物，不污染系统：

```bash
cmake -S "DeckShellGamepad-private-work" -B "build-release" -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTING=OFF -DDECKGAMEPAD_BUILD_TESTS=OFF \
  -DBUILD_GAMEPAD_EXAMPLES=OFF \
  -DDECKGAMEPAD_BUILD_QML_MODULE=OFF \
  -DDECKGAMEPAD_BUILD_TREELAND_CLIENT=OFF \
  -DCMAKE_INSTALL_PREFIX="/tmp/deckgamepad-install"
cmake --build "build-release" --parallel
cmake --install "build-release"
```

- [ ] 构建参数确认：`BUILD_SHARED_LIBS=ON`（发行版以 shared 为准）
- [ ] 产物安装到 staging 前缀（例如 `/tmp/deckgamepad-install`）

---

## 5) 产物校验（对照 `ARTIFACTS.md`）

- [ ] `libdeckshell-gamepad.so.*` 存在且 SONAME 正确（`readelf -d` 可核对 `SONAME`）
- [ ] `lib/cmake/DeckShellGamepad/*` 存在（`DeckShellGamepadConfig.cmake`、`DeckShellGamepadTargets*.cmake` 等）
- [ ] `share/DeckShellGamepad/gamecontrollerdb.txt` 已安装
- [ ] 头文件已安装且不包含 `*_p.h`（内部头不对外发布）

---

## 6) 第三方消费验证（install + find_package）

目标：第三方工程在“仅给 prefix”的前提下可配置/构建/运行。

参考工程：`tests/smoke/gamepad_consumer/`

```bash
cmake -S "DeckShellGamepad-private-work/tests/smoke/gamepad_consumer" -B "/tmp/deckgamepad-consumer" -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="/tmp/deckgamepad-install"
cmake --build "/tmp/deckgamepad-consumer" --parallel

LD_LIBRARY_PATH="/tmp/deckgamepad-install/lib:${LD_LIBRARY_PATH}" \
  "/tmp/deckgamepad-consumer/gamepad_consumer"
```

- [ ] `find_package(DeckShellGamepad CONFIG REQUIRED)` 成功
- [ ] `DeckShell::deckshell-gamepad` 可链接
- [ ] 可执行文件运行成功（最小 smoke）

---

## 7) 测试门禁（发布前必须可复现）

### 7.1 常规环境（无特权）

- [ ] `ctest` 基础用例通过（允许“依赖 uinput 的用例”被 SKIP，但必须可见并记录原因）

### 7.2 特权/专机环境（推荐 nightly 与发布前强门禁）

> 目标：关键 uinput/udev 集成/E2E **不允许 SKIP**。

- [ ] 在具备 `/dev/uinput` 权限的环境跑全量 `ctest`（no-skip 门禁）
  - 推荐入口：`cmake --build <build_dir> --target ctest-no-skip`
  - 或直接执行：`bash scripts/ctest_no_skip.sh <build_dir>`
- [ ] Sanitizer（ASan/UBSan）全量通过（no-skip 门禁）
- [ ] 若出现 `missing /dev/uinput access` 但权限位看起来正常：优先排查容器/sandbox 的 device cgroup 限制；需要使用 privileged runner/专机执行

证据要求（建议作为 release artifact 保存）：
- [ ] `LastTest.log`（包含完整测试列表与是否 SKIP）

---

## 8) 真机回归矩阵与已知限制（对外声明）

- [ ] 回归矩阵已更新并可追溯证据（USB 基线 ≥2 台）：
  - `helloagents/plan/202601271626_deckshell-gamepad-linux-release/regression-matrix.md`
  - `helloagents/plan/202601271626_deckshell-gamepad-linux-release/evidence/*`
- [ ] `README.md` 的 “⚠️ 已知限制（Beta/RC）” 已同步最新风险与边界
- [ ] 对外声明明确“支持范围/不支持项/已知限制/规避建议”

---

## 9) Git tag（建议）与发布记录

建议 tag 命名（避免多项目仓库歧义）：
- `deckshell-gamepad-vX.Y.Z`

最小步骤：
- [ ] 提交版本号与 changelog 更新
- [ ] 创建 tag（建议 annotated tag）
- [ ] 记录发布产物校验与回归矩阵结论（可作为 CI artifact / release notes 附件）

---

## 10) 回滚策略（Rollback）

### 10.1 原则

- **不建议删除已公开 tag**：优先通过“发布新 PATCH hotfix”修复。
- 回滚目标是“恢复可用 + 可追溯”，避免在消费方造成不可解释的版本漂移。

### 10.2 典型场景与动作

**A. 发现严重问题但尚未被发行版广泛分发**
- [ ] 停止发布（不要继续推进下游打包）
- [ ] 在主线修复后发布 `X.Y.(Z+1)`（hotfix）
- [ ] `CHANGELOG.md` 记录问题与修复版本

**B. 发行版已分发（shared）且需要紧急回滚**
- [ ] 下游包回滚到上一版 `X.Y.(Z-1)`（或上一可用版本）
- [ ] 同步发布 `X.Y.(Z+1)` 修复版，并在发行说明中标注“回滚建议/影响范围”

**C. ABI 破坏（误判导致同 MAJOR 内 break）**
- [ ] 立即冻结继续发布
- [ ] 选项 1：回退破坏性变更并发布 PATCH（保持 ABI）
- [ ] 选项 2：正确 bump `MAJOR` + bump `SOVERSION`，并在发行版拆包层面并行提供旧 MAJOR
