# Treeland → DeckShell 路径策略

本文件是同步路径分类的唯一事实来源。`scripts/sync_audit.py` 读取下方 JSON；修改路径合同后必须同步运行脚本测试和 dry-run。

```json
{
  "version": 1,
  "mapped": {
    "directories": {
      ".agents": "compositor/.agents",
      ".tx": "compositor/.tx",
      "LICENSES": "compositor/LICENSES",
      "cmake": "compositor/cmake",
      "debian": "compositor/debian",
      "docs": "compositor/docs",
      "examples": "compositor/examples",
      "misc": "compositor/misc",
      "nix": "compositor/nix",
      "scripts": "compositor/scripts",
      "src": "compositor/src",
      "tests": "compositor/tests",
      "tools": "compositor/tools",
      "translations": "compositor/translations",
      "wallpaper-factory": "compositor/wallpaper-factory"
    },
    "files": {
      ".envrc": "compositor/.envrc",
      "AGENTS.md": "compositor/AGENTS.md",
      "CMakeLists.txt": "compositor/CMakeLists.txt",
      "CMakePresets.json": "compositor/CMakePresets.json",
      "README.md": "compositor/README.md",
      "README.zh_CN.md": "compositor/README.zh_CN.md",
      "REUSE.toml": "compositor/REUSE.toml",
      "default.nix": "compositor/default.nix",
      "flake.lock": "compositor/flake.lock",
      "flake.nix": "compositor/flake.nix",
      "garnix.yaml": "compositor/garnix.yaml",
      "renovate.json": "compositor/renovate.json"
    }
  },
  "root_owned": {
    "directories": {
      "protocols": "protocols"
    },
    "files": {
      ".clang-format": ".clang-format",
      ".editorconfig": ".editorconfig",
      ".gitignore": ".gitignore"
    }
  },
  "excluded": {
    "directories": [
      "qwlroots",
      "waylib"
    ],
    "files": []
  },
  "review_only": {
    "directories": {
      ".github": ".github"
    },
    "files": {
      ".gitmodules": ".gitmodules"
    }
  }
}
```

## 分类语义

- `mapped`：转换到 `compositor/` 下的固定目标路径。
- `root_owned`：明确允许保留在 DeckShell 根项目中的路径。
- `excluded`：dependency-only 时跳过，mixed 时剥离。
- `review_only`：必须通过 `--approve-review <policy-key>` 显式批准；批准后按声明的目标路径同步。
- 未命中以上分类的路径为 `unknown`，inventory 必须判定为 `BLOCKED`。

## 规范目标路径权威

- 每个 retained 来源路径只映射到本策略计算出的一个规范目标路径。目录映射只替换声明的目录前缀，不产生隐式兄弟文件或一对多实现路径。
- 每个来源提交的 inventory `target_paths` 是该提交可触达的唯一目标路径集合；目标提交的任一 old/new 实际路径超出该集合时，`verify` 必须报告 `target-path-expansion` 并阻断。
- evidence 只能解释 inventory 已授权路径，不能因目标提交触达了额外文件就把该文件声明为 `modified` 或 `materialized`。
- 规范目标路径在目标父树中不存在时，允许在同一规范路径 `materialized`；不得改在兄弟路径创建或维护上游实现。
- DeckShell 本地独有文件可以独立存在且可以按本地职责拆分，但不得在 Treeland 1:1 映射提交中吸收 mapped 上游实现责任。具有上游对应路径的测试文件不属于本地独有文件。
- 如果同步只能通过修改兄弟文件、以 omitted/empty 跳过规范路径或继续维护一对多实现才能完成，则标记 `target-structure-drift` 并停止；先在同步任务外恢复规范文件形状，再从新的干净目标基线重跑完整门禁。

## Rename / copy

旧路径和新路径分别分类，不 blanket block 跨分类 rename/copy：

- excluded → mapped：丢弃旧侧，保留映射后的新侧。
- mapped → excluded：保留映射后的删除侧，丢弃新侧。
- mapped/root-owned 之间移动：分别转换旧、新目标路径。
- 任一侧为 `unknown` 或未批准的 `review_only`：阻断。

Git 不持久化 rename 元数据；过滤后表现为 delete/add 是合法结果，但 inventory 必须保留原始 rename/copy 关系供审计。retained rename/copy 的旧、新规范目标路径都属于该提交的 `target_paths`，因此不会被误报为目标路径扩张。
