> 仓内参考副本；权威原文：`.helloagents/plans/20261106_treeland_0_10_0_to_0_11_0_local_sync/plan.md`。
> 保留原同步方案的历史时点与验收边界；其中历史命令不是本次补档的执行指令。

# Treeland 0.10.0 → 0.11.0 实施方案

本方案实施已批准的 [PRD](prd.md)。整批标识 `20261106_treeland_0_10_0_to_0_11_0_local_sync`，仅有一个关键节点 N9，来源 `(3a100f265970cb6acf9addf07e5c297aab9e9839..f342a5b6debd028ed9bc4bc3e806118efbcae8f2]`。source tip 冻结为 `87485fdeccc93e134e897d479439db03e5730465`。XML 固定为协议 0.7.0 / `49e985e0fb0b55fd2299349f08bac14c4e09f2b3`，已于本轮明确批准。

## 基线和隔离目录

- 初始 P：`36208f1f600bd64ee6b0047e112b26b4aea9f2ba`；目标 `refs/heads/master-merge-to-0-11-0`。
- C：`7f93d719aa33605b3c0de9684471698016d06b1a`；新目标 `refs/heads/waylibshared-merge-to-0-11-0`。
- R：`c844d3549136a250231d3abb2fc5f6832ff05c4e`；新目标 `refs/heads/master-merge-treeland-to-0-11-0`。
- 每个 linked worktree 位于本方案 `worktrees/` 下；证据、预览补丁和源码外构建位于同级 `evidence/` 下，不位于 worktree 内，不使用旧 attempt。
- 工具适配先在 `worktrees/tooling` 完成并单独提交；此提交作为 N9 的实际 P replay 基线，初始用户目标 ref 暂不移动。完整验证后先核对并接受这项已授权工具维护，再由 closeout 从真实 replay 基线接受产品结果。任何前置快进均用 expected-old CAS，并保留事实记录，不改写 manifest 基线。
- 正式 replay 的 run-id 绑定具体 attempt；冲突现场不 reset、abort 或删 journal，需补适配时使用独立新 attempt。

## 实施步骤

1. 精确扩展 `contract_migration.PARENT_INTEGRATION_FILES` 的 12 个已批准 XML 文件；同步说明，使用现有迁移 round-trip 测试验证已批准路径可回放/独立核验、未批准路径继续拒绝。
2. 在独立预览工作树逐来源审核三方补丁，生成有序逐路径适配证明。保留本地包名、安装布局、DISABLE_DDM 等配置；不恢复系统 TreelandProtocols 依赖。协议 XML 在首次相关实现节点按固定来源加入，remote-subsurface 由 journal 配套阶段管理。
3. 运行统一 R→C→P replay。范围内每个来源只对应本次一条映射，C-only 同步创建 P gitlink 提交。R 无来源内容变化，保留真实 R 基线，并完整证明两处继承差异。
4. 运行 P/C/R 内容投影、两层 gitlink、协议 advisory、protocol pairing、source/install contract 和依赖物化验证。C/R base 和 candidate 以及 P candidate 都实际 fresh build/test，构建并行数依据当前可用内存保守设置。
5. 生成 N9 完整报告，通过后将目标 refs 安排为未检出，按 R→C→P expected-old CAS 收口。失败保留现场与已完成层，不自动回滚。
6. 按整体范围执行 `unified_sync.py finish --task sync`，输出 P/C 仓内记录；不自动提交这些文档、push、tag 或改外层 index。日常 P master、C waylibshared、R master-merge-treeland 保留。

## 验证入口与接受条件

工具验证：`python3 -m unittest discover -s <tooling>/doc/skills/treeland-deckshell-waylib-unified-sync/tests -p test_contract_migration.py`，以及受影响回放/迁移验证测试。源码以 `git diff --check` 检查。

产品验证全部使用该技能的 `validation_record.py --manifest ...`：C base/candidate configure/build/install/CTest、package consumer 三步；R base/candidate Meson setup/compile/test；P configure/build/compositor CTest。P 默认安装包路线仅消费本批 C 安装树，CTest 运行依赖按 `protocol-test-runtime.md` 准备。真实失败和 SKIP 原样保留。用户于本轮明确授权跳过当前 DRM 阻塞：仅允许 N9 完整、未过滤 CTest 中 `test_drm` 的真实 SKIP 不阻断接受；不覆盖任何 FAIL、其它 SKIP、缺测或过滤测试，不证明 DRM/GPU 行为已通过。最终授权记录绑定本次 manifest、验证 attempt、原始日志和完整发现集合，原阻断报告保留，另生成限定授权后的接受报告。

冻结 C 基线的 Qt 私有接口不兼容宿主 Qt 6.12；从 N9-attempt-2 起使用发行版签名验证后的 Qt 6.11.2、Dtk 6.7.49 及配套依赖，在 Bubblewrap 的只读 `/usr` overlay 中统一构建基线与候选。包来源/签名记录位于 `evidence/toolchain-qt611/toolchain.json`，新增调试工具依赖的 Qt HTTP Server/WebSockets 6.11.2 补充记录位于同目录 `http-modules/toolchain.json`。DConfig 复用 `evidence/N9-attempt-2/runtime-dependency/` 的隔离 `deepin-app-services 1.0.45-1`；XDG cache/config/data/state 仅指向沙箱内私有可写目录。每次重新执行构建与加载检查，不安装系统包、不修改冻结 SHA，保留失败记录。

上游新增协议测试的公共头引用适配为本地扁平安装路径；安全上下文及 text-input v1/v3 测试仅从同一候选 SHA 的已物化子模块读取未导出的私有声明，仍链接本批安装库，其余公共头和 R 头继续来自本批安装树。不得为测试新增私有头导出或硬编码上游 namespace。

本地回归测试随相关来源同步：生命周期测试复用已有私有 DConfig/Accounts 设施并等待异步就绪；socket 检查保留全局排除要求并匹配新增的空指针保护；协议包检查按已批准新增清单严格要求 32 个 XML 及完整安装条目。原有交互、安全和安装断言不删减。

最终接受仅依据 `generate_sync_report.py` 九项 gate 和全部必需日志，以及实际 closeout 和 finish 结果；预检、工具测试或快照编译不能替代完整产品验收。
