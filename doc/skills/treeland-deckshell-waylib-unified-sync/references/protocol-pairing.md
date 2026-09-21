# 每轮 remote-subsurface 配套检查

该检查每轮必需，包括 XML/实现分别变化、双方变化或均无变化。原有
`protocol_tracker.py` 仍只提供 advisory 候选；它的触发条件、退出 0 和
`not-triggered` 都不替代配套结论。普通 Waylib 构建仅使用库内 XML，不运行维护工具。

## 来源与回放

C 基线须携带 `waylib/protocols/remote-subsurface.json`，分别记录已接受实现与
XML 的仓库、精确提交、路径。本段 implementation base 必须等于该记录；XML
base 也必须等于已接受提交。对象须已在本地，不自动 fetch。分支/tag 会解析为
精确提交；浅历史、对象缺失、文件删除或不明确的移动均报告“尚未适配”。

`protocol-update.json` 的最小输入：

```json
{
  "selection": {
    "repo": "/absolute/local/treeland-protocols",
    "base": "<last accepted XML commit>",
    "head": "<selected XML commit or ref>",
    "path": "xml/treeland-remote-subsurface-unstable-v1.xml"
  }
}
```

`path` 在唯一 rename 链可推导时可省略；大幅改写或删除后重建须显式指定新路径。
`selection.implementation_paths` 可增加本轮新实现文件。检查保留区间中每个提交的
相关 diff，包含中间修改后回退，不能只看两个端点或版本号。

```sh
python3 "$SKILL_DIR/scripts/unified_sync.py" protocol-inspect \
  --source-repo "$SOURCE_REPO" --child-repo "$CHILD_REPO" \
  --child-base "$CHILD_BASE" --inventory "$ARTIFACT_ROOT/inventory.json" \
  --selection "$ARTIFACT_ROOT/protocol-selection.json" \
  --output "$ARTIFACT_ROOT/protocol-inspection.json"
```

这里 `protocol-selection.json` 是上例中 `selection` 对象本身。检查通过只表示
`inspected-not-accepted`。随后给现有 `replay` 命令添加
`--protocol-update "$ARTIFACT_ROOT/protocol-update.json"`。普通来源回放结束后，
同一 journal 内执行 C→P 配套步骤：更新 C 的 XML/来源记录、P 的同协议 XML 和
C gitlink。没有实际变化不创建空提交。配套提交独立于来源映射，不伪造 Treeland
来源提交；其内容和源码合同仍经原有验证器检查。

需要补充本地适配时，输入可增加 `child`、`parent` 对象，每个对象包含 `paths`
（精确文件列表）、`reason` 和已有工件格式的 `adaptation_patch`。C 仅允许已检查
实现路径和 `waylib/tests/`、`test_project/`；P 仅允许 `compositor/` 与
`treeland-dde-shell-client/`。这些路径权限不替代当轮用户授权。XML、来源记录和
内部 gitlink 由配套步骤管理。补丁应包含必要客户端/测试更新，不手改生成代码。

## 验证与接受

运行既有 base/candidate 构建、安装、消费及 P/R 检查；使用
`validation_record.py --manifest ...` 记录真实执行。配套审查 JSON 包含：

- `implementation`: `disposition` 为 `updated` 或 `unchanged`，以及具体 `reason`。
- `wire_review`、`behavior_review`、`client_upgrade`：逐项说明签名/顺序/枚举、
  描述语义与客户端升级影响。`breaking` 为布尔值；wire 变化须明确标记破坏性影响。
- `compatibility`: 固定 `direct-switch`，不接受旧接口别名、双协议或运行时回退。
- `clients`: 列出基线和候选中所有引用旧/新协议接口的受影响源码，记录 `lane`、
  `path`、`disposition`、`reason`。自动发现扫描 C/P 的 C++、头文件和 QML；
  审查还须判断间接调用和其他语言的客户端。标记 updated 的文件必须确有 Git 变化。
- `validations`: `build` 使用 `waylib-candidate-build`；`consumer` 与 `interaction`
  指向真实、非零且通过的 CTest 记录，命令包含 `--no-tests=error`。
- `expectations`: 每条含 `source`（精确 `XML_COMMIT:path`）、`case`（已通过的
  CTest 名）、`kind: interaction` 和独立合同依据 `assertion`。至少覆盖真实行为，
  不能只填 registry、编译结果或同一 XML 生成的两端一致。

```sh
python3 "$SKILL_DIR/scripts/unified_sync.py" protocol-verify \
  --inventory "$ARTIFACT_ROOT/inventory.json" --manifest "$ARTIFACT_ROOT/manifest.json" \
  --review "$ARTIFACT_ROOT/protocol-review.json" --validations "$ARTIFACT_ROOT/validations.json" \
  --artifact-root "$ARTIFACT_ROOT" --output "$ARTIFACT_ROOT/protocol-pairing.json"
```

给 `generate_sync_report.py` 添加
`--protocol-pairing "$ARTIFACT_ROOT/protocol-pairing.json"`。完整报告要求九项 gate；
配套失败、缺失结论、必要测试无法运行时报告“尚未适配”，保留目标范围、最后已接受
配对、失败阶段/原因、未完成项和已有验证。`closeout` 在任何 ref 写入前拒绝该报告，
并核对来源记录与报告配对。失败候选可保留，上一已接受配对不变；不是运行时回退。

每段通过后仍须在已授权仓库按原有 R→C→P expected-old CAS 接受；报告通过本身
不等于同步完成。部分更新失败保留 journal、报告已完成阶段，不自动回滚。
