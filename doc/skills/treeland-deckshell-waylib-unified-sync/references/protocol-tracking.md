# treeland-protocols advisory 候选

## 触发边界

协议追踪有两个独立触发信号：

1. Treeland 来源提交实际修改 `protocols/**/*.xml`；
2. replay 后的 parent candidate 实际修改 `protocols/compositor/**/*.xml`。

任一信号成立就查询协议仓库。来源或 parent 触达其他非 XML `protocols/**` 不自动扩大查询范围。

未触发时 `protocol_tracker.py` 不要求协议仓库，输出：

```json
{
  "schema_version": 2,
  "kind": "treeland-unified-protocol-candidates",
  "outcome": "pass",
  "advisory": true,
  "status": "not-triggered",
  "entries": []
}
```

## 冻结与搜索

触发后把调用者提供的 `protocol_ref`（CLI 中对应 `--protocol-head`）解析为完整 `protocol_head`。它可以是本地分支、任意 remote-tracking ref、tag 或完整 SHA；不要求名称为 `treeland-protocols`，不要求存在该 remote，也不从 URL 推断身份。工具只扫描该 commit 及祖先中触达六类协议目录的提交，不读取后续移动 HEAD。

对每个来源 commit：

1. 从 inventory 读取来源协议路径，并从 parent manifest 读取实际目标协议路径；
2. 提取来源和候选 commit 的无上下文 added/removed 行，归一化空白；识别 rename，使仅 mode 或纯 XML 重命名得到空内容差异；
3. 仅保留作者时间位于来源前 `days_before` 到后 `days_after` 的候选；
4. 任一侧标准化差异为空时 comparison_status=not-comparable、similarity=null，不调用 SequenceMatcher；其余使用确定性比率；
5. 保留 `similarity >= threshold` 的全部候选；
6. 按相似度降序、时间距离升序、SHA 升序排序。

默认阈值 `0.7`、窗口 `30/7` 天。参数、冻结 head、搜索路径、触发来源、候选 author/date/subject、相似度和时间距离全部写入 JSON。

## 状态语义

- `no-candidate`：没有达到阈值的候选；不阻断内容同步，但报告必须保留事实。
- `single-candidate`：只有一个候选；仍不是确认映射。
- `ambiguous-candidates`：多个候选；全部保留，不择优冒充唯一结果，也不因启发式歧义阻断内容同步。
- `not-comparable`：已触发但来源标准化内容差异为空，不等同于 not-triggered；空差异候选保留在 not_comparable 诊断数组，不进入阈值候选，即使 threshold=0。

任何状态都不得生成 `confirmed_commit` 字段。需要确认协议来源时，应在同步范围外进行人工/项目级语义审查，并作为独立证据记录。候选 JSON 必须保留 `source_paths`、`target_paths` 和 `trigger_sources`，以便区分两种触发路径。

完整报告要求 tracker 同时读取 --parent-repo 与 --manifest，即使最终 not-triggered 也绑定 manifest_sha256、parent_context_used=true；不能用仅观察来源的结果替代实际 P 目标检查。
