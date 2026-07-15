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

## Rename / copy

旧路径和新路径分别分类，不 blanket block 跨分类 rename/copy：

- excluded → mapped：丢弃旧侧，保留映射后的新侧。
- mapped → excluded：保留映射后的删除侧，丢弃新侧。
- mapped/root-owned 之间移动：分别转换旧、新目标路径。
- 任一侧为 `unknown` 或未批准的 `review_only`：阻断。

Git 不持久化 rename 元数据；过滤后表现为 delete/add 是合法结果，但 inventory 必须保留原始 rename/copy 关系供审计。
