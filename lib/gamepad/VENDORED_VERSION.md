# 版本记录（可复制为独立项目）

本目录在 DeckShell 仓库内作为 `DeckShellGamepad` 的**唯一开发入口**（`lib/gamepad`）。后续如需作为独立项目继续开发，可直接复制本目录到新仓库。

为保证可追溯，请在每次复制/同步时更新以下记录。

## 来源记录
- 来源仓库: DeckShell
- 来源路径: `lib/gamepad`
- 版本: 1.0.0
- 提交: cb3553444748c3d172f0526e0898499ba511771f
- 记录日期: 2026-01-04
- 维护方式: 人工维护

## 关键说明
- 新增 `protocols/treeland-gamepad-v1.xml`（vendored，MIT）并随 `deckshell-gamepad-treeland` 安装交付
- 自带 install+find_package smoke 测试（`tests/`）
- SDL DB 默认安装目录调整为 `share/DeckShellGamepad/`，并兼容 legacy `share/DeckShell/` 搜索路径
