# 独立本地修复与安装包消费链

## 精确授权的本地尾部提交

来源同步完成后发现独立本地缺陷，须先取得明确授权，不得把修复伪装为来源提交。
保留原 manifest、journal、候选和失败记录；在新的 detached P/C worktree 上分别创建
一个相邻非 merge 本地提交，P 同时传播修复后的 C gitlink。R、协议 XML、配套实现路径、
provenance 及 Waylib 公共合同不变。没有授权则继续阻断。

`record_local_fix.py` 接收原 manifest、原 P/C evidence、明确列出 P/C 文件的 approval、
新 P/C/R worktree 和新 artifact root。它只生成派生 manifest 和 lane evidence，
不修改源码、创建提交、更新 refs 或补写验证结果。原来源序列、基线、range、run-id
和 protocol companion 完整保留；`local_fix` 单独记录两层 base/head、diff 和 C 源码合同。
approval 必须含非空 authorization/reason/id、approved 状态、原 manifest 摘要及相同 refs_doc。

所有 source projection、消息、协议与合同检查继续执行；报告重新核验本地修复的精确路径、
相邻提交、真实 diff、公共合同和两层 gitlink。新候选使用新构建与安装目录，旧 PASS 不能
换 manifest 摘要后复用。全部原验收及独立 closeout 授权要求不变。

## P 默认 installed-package 路线

按 C configure → 默认完整 build → 完整 unstripped install → P configure/build 的顺序，
向同一个 `validations.json` 记录命令。P 的 `WITH_SUBMODULE_WAYLIB=OFF` 不要求在
自身 codemodel 中重新编译 wrapper，而是读取当前 manifest 绑定的 C 三条记录并重验：

- C wrapper 确实编译本次 R，实际消费它的生成头及库，而不是系统 wlroots。
- 安装库来自 C codemodel 的产物与安装位置，存在于真实 install manifest；ELF 仅
  归一化 CMake 的 RPATH 安装变换后比较，其余字节不忽略。
- P 同一实际链接目标同时使用已安装 WaylibSharedServer 和 wrapper；仅依赖顺序不算。
- 该目标的真实编译依赖使用安装的 R 源头文件与生成头，逐个对应本次 C source/build。
  系统头、C 源码树/构建树头、旧包、替换产物及缺失或错绑记录均拒绝。

报告重读保存的原始 C/P 编译和链接证据，并重算当前安装产物。内嵌路线沿用原检查，
不把安装包支持作为编译失败后的自动回退。
