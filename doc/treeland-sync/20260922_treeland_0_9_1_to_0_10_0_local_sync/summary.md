# P / DeckShell 同步记录：20260922_treeland_0_9_1_to_0_10_0_local_sync

这是按仓归属生成的同步事实记录，不是新的产品验收报告。
原节点结果只绑定下文列出的原候选与原环境；本次生成未执行同步、构建、测试、收口或远端发布。

- 来源范围（左开右闭）：` fd573cf44fb06ee1eebcdd8c39716d1c797b64d4 ` → ` 3a100f265970cb6acf9addf07e5c297aab9e9839 `。
- 本仓内容基线：` 9d14efb18d1d2413376e4369461a3e11f7d44689 `。
- 本仓内容终点：` bee3531566e9d325e8d89db1ad124759033d7bc2 `；不含后继文档、URL/gitlink 或工具维护提交。
- 本仓普通目标：**41**；独立初始化：**0**；特殊目标：**4**；合计 **45**。
- 普通 action：{'applied': 15, 'adapted': 19, 'gitlink-only': 7}。
- 特殊目标分类：{'protocol-companion': 2, 'local-fix': 1, 'structural-repair': 1}。
- 整批普通 Treeland 来源：**41**；本仓未归属的来源不制造目标提交。
- 主分支归并承接上述已接受内容终点，不构成另一批同步；是否包含由正常完成入口核对。日常分支为 P `master` / C `waylibshared`，后继文档与工具提交不改变原候选验收身份。
- 本批次未提供历史改写映射，仅记录真实来源 → 目标，不虚构原目标列。
- 原需求与实施记录：[PRD](prd.md)、[plan](plan.md)。
- 外层历史资料仅用标识和相对定位列出，不是本仓链接；记录不包含完整日志、构建树或安装树。
- R 的短 Refs 是 P/C 共同方案标识，不承诺 R 仓内存在方案副本。

## 有序提交映射

| 序号 / 节点 | Treeland 来源 | 本仓目标 | action（C 另列 content_action） | 归属 |
|---|---|---|---|---|
| 1 / N8a | ` bac6470ac7932b30cf3cfc3a0bdb1fc9c9f31c34 ` | ` e7988fbedb1dd7e3a5a7ff42e1d4ca030d846a06 ` [条目](#entry-1) | applied | deckshell-only |
| 2 / N8a | ` f912abff4ef8e52208b5ebe97a8328ac8169c044 ` | ` 90a7fe038559336a6d3f65f118d73ae11c087caa ` [条目](#entry-2) | applied | deckshell-only |
| 3 / N8a | ` d83984336e4770d0d27b8eb05b68cebc395fde10 ` | ` 07edb5cb3271245ff276c72def5c51c08424a2e1 ` [适配详情](adaptations/07edb5cb3271245ff276c72def5c51c08424a2e1.md) | adapted | deckshell-only |
| 4 / N8a | ` 3cb4cbe2404ba766ad0430a2a20f7303febfdcf8 ` | ` 62b04567463080c6050c042382a5381abc139695 ` [适配详情](adaptations/62b04567463080c6050c042382a5381abc139695.md) | adapted | deckshell-only |
| 5 / N8a | ` d3cdd8644710cbb55e56feccf039729eb307fe3f ` | ` c655ce1ec9020d7b179a099890812a8230652105 ` [条目](#entry-5) | applied | dual |
| 6 / N8a | ` 8bfa446c589f06d4f427a39b93a585a2406f5cdb ` | ` b4a5826fa61f080b39e5ef4e989bd77da5cf47b2 ` [适配详情](adaptations/b4a5826fa61f080b39e5ef4e989bd77da5cf47b2.md) | adapted | dual |
| 7 / N8a | ` 007f3653c7942690f76db0c06ea55991efc59dc0 ` | ` c2b72c0970b54440970a394ba7770860ed3955c7 ` [条目](#entry-7) | gitlink-only | waylib-only |
| 8 / N8a | ` bd2c6995dd49b309abf76af13688b317fe31244e ` | ` 5a0f19288ac068187854fe9773dd3de269ea0265 ` [条目](#entry-8) | gitlink-only | waylib-only |
| 9 / N8a | ` b71d4af56f3c90d4a8bd5cf6b421bbc9028ac145 ` | ` c38a625edb9567ff40633ccc6db0eb95fdb9f01d ` [适配详情](adaptations/c38a625edb9567ff40633ccc6db0eb95fdb9f01d.md) | adapted | dual |
| 10 / N8a | ` 1a457fedc3cbb7784a3d6e9165c7dc531d0067f1 ` | ` 72cb6636921d8aa2c4feb5f90e996e3b2f44f9ee ` [条目](#entry-10) | applied | deckshell-only |
| 11 / N8a | ` 591cf2a73fdd6329693c5b452cf70f076d902f16 ` | ` 07020c5faa428631c154c8372958c7936be81d82 ` [条目](#entry-11) | applied | deckshell-only |
| 12 / N8a | ` 809017a78e5ab8558ff32e3752a5d91112d9db14 ` | ` acac4338c0fe5087166a74d799978fb6aa963a65 ` [条目](#entry-12) | applied | deckshell-only |
| 13 / N8a | ` 266f951f730967c76958692bb0c957717f89cb4a ` | ` 725d2448d9ba894aebda1ee8383b5fac46725054 ` [条目](#entry-13) | applied | deckshell-only |
| 14 / N8a | ` 8caa8dd8a42193efef23736132958333e7bc1e4c ` | ` ed16740f163c19f14d1bb794acdf042433727781 ` [条目](#entry-14) | applied | deckshell-only |
| 15 / N8a | ` 4485b04b478f921cb1491e69e9c9e33293f9affa ` | ` 7f5b13c7588921c3e8732bd6926538eb25a60b22 ` [条目](#entry-15) | applied | deckshell-only |
| 16 / N8a | ` 3357de71a728b3f486a010bb9fe0c630314912dd ` | ` e536b2e32c626ccb0cfb6545a1aa514646a89a9b ` [条目](#entry-16) | applied | deckshell-only |
| 17 / N8a | ` e5e52083e1aa69ac66070098ec44ae47752ef759 ` | ` 596d2b55f7991fc972fff7fe03cfca600a1542ca ` [条目](#entry-17) | applied | dual |
| 18 / N8a | ` 773388598efa732aa581d489f55921bf57e4dbdb ` | ` e3199b03d8ed16fd14d86b622104bd145765a3ac ` [适配详情](adaptations/e3199b03d8ed16fd14d86b622104bd145765a3ac.md) | adapted | deckshell-only |
| 19 / N8a | ` b727a8209385c064fbe96d9a3a74a00f27121b13 ` | ` c7b1809d7908184b4a983cdbeb1c9cc80085c530 ` [条目](#entry-19) | gitlink-only | waylib-only |
| 20 / N8a | ` df7b59b32de4f3982c968416cf92b3319daa7f20 ` | ` 384af637fa17312a903de9ddca52272c072b119c ` [条目](#entry-20) | gitlink-only | waylib-only |
| 21 / N8a | ` b3208c08a3599590ece69c3a68773e07584969bb ` | ` f00e4f7942285f127dcd111157cfb711fa77c340 ` [条目](#entry-21) | gitlink-only | waylib-only |
| 22 / N8a | ` af2e2bbe5bd7763c47cf8ca42c49fdd90776f167 ` | ` c0a0b0230f624b553bdf2038a6eed9dae1339eb7 ` [条目](#entry-22) | applied | deckshell-only |
| 23 / N8a | ` 1173d14965daef4048b5633676a1b873f8e6815a ` | ` 9972226d67568d58c17caf0656a9601206b0dcbc ` [条目](#entry-23) | applied | deckshell-only |
| 24 / N8a | ` 98071bd1d0039beb02a4397a91aa6c0abd6488ae ` | ` 1d732b58d831f614a60ae8fc12e13c0bd31b0738 ` [条目](#entry-24) | applied | deckshell-only |
| 25 / N8a | ` b4935634e511fd85d90cd8a9543364e68825f8c7 ` | ` d0a8390e2d0a05a3e8c5c879f8e1d0ed6e1b8a1f ` [条目](#entry-25) | applied | deckshell-only |
| 26 / N8a | ` a5656ab80ae11a0068d507659f35bb999b6d815d ` | ` f8772b17a0ad4e942ddaf9cf1fae2148518ca5cd ` [适配详情](adaptations/f8772b17a0ad4e942ddaf9cf1fae2148518ca5cd.md) | adapted | dual |
| 27 / N8a | 无（独立提交） | ` 0ba8ee8fb414e5711e4299d1142dc7d8276ed75c ` [适配详情](adaptations/0ba8ee8fb414e5711e4299d1142dc7d8276ed75c.md) | protocol-companion | protocol-companion |
| 28 / N8a | 无（独立提交） | ` cb9c6bf6bbc4a53bc50212204f34ad0cd5308ffb ` [适配详情](adaptations/cb9c6bf6bbc4a53bc50212204f34ad0cd5308ffb.md) | local-fix | local-fix |
| 29 / N8a → N8b | 无（独立提交） | ` 38ca30d3e220e99a119dca7465d1acb887e7f186 ` [适配详情](adaptations/38ca30d3e220e99a119dca7465d1acb887e7f186.md) | structural-repair | structural-repair |
| 30 / N8b | ` c0917aed288d209d0a27ccb4539d1de3e10eb7b6 ` | ` 155da93a88228842f41a1bea407d0bb49a009f5c ` [适配详情](adaptations/155da93a88228842f41a1bea407d0bb49a009f5c.md) | adapted | deckshell-only |
| 31 / N8b | ` 24e1c7a4ea8a5eeaedff24dee3df27e10f02c496 ` | ` c54dbcbfbb7100390bf64546a370ecc3e42ad094 ` [适配详情](adaptations/c54dbcbfbb7100390bf64546a370ecc3e42ad094.md) | adapted | dual |
| 32 / N8b | ` b3a357d44569f7d0e32bd6a40ffda74edec83750 ` | ` 134a681a992521213b4f0a4a6bb0aef2be5c85dd ` [适配详情](adaptations/134a681a992521213b4f0a4a6bb0aef2be5c85dd.md) | adapted | deckshell-only |
| 33 / N8b | ` 17bca039766adb868c318fa7b7d69e7f428f64ac ` | ` 9b2b8faff286e3010edeac795ea67f12ff5ac543 ` [适配详情](adaptations/9b2b8faff286e3010edeac795ea67f12ff5ac543.md) | adapted | deckshell-only |
| 34 / N8b | ` f645b104475c30e150930a1ed0d84c70be039b01 ` | ` 31d80cbdfb053b7ad106d655e4acf6456f5513ce ` [适配详情](adaptations/31d80cbdfb053b7ad106d655e4acf6456f5513ce.md) | adapted | deckshell-only |
| 35 / N8b | ` ba4f63aec9a6acccfe9deef00d6c8002b2074af3 ` | ` 1f1cb4eb7ab60a3b68f5e2a821c14a6312bd0c09 ` [适配详情](adaptations/1f1cb4eb7ab60a3b68f5e2a821c14a6312bd0c09.md) | adapted | deckshell-only |
| 36 / N8b | ` 4b1c552b70160992e7f418847ca9acf43f4d0279 ` | ` 433b5e19a8c8228acf234f94e633cfe2b76cac21 ` [适配详情](adaptations/433b5e19a8c8228acf234f94e633cfe2b76cac21.md) | adapted | deckshell-only |
| 37 / N8b | ` d9efe405ab5b91daaa1a4ae5ee237cf076064910 ` | ` 27e08f983493c74e42cad21aacbc9694b3232fb4 ` [适配详情](adaptations/27e08f983493c74e42cad21aacbc9694b3232fb4.md) | adapted | dual |
| 38 / N8b | ` 423b2ad15cf2d6153aa3c6a00e7bef7dbec01aa0 ` | ` 54edd9a5c45480b917fe5a9cdebdf59acb3e0098 ` [条目](#entry-38) | gitlink-only | waylib-only |
| 39 / N8b | ` cb038ef766940545fd05d0a22578c7e9fbaa7324 ` | ` d806f87a8f58ff03d447deace2d78c206f6a2d3f ` [适配详情](adaptations/d806f87a8f58ff03d447deace2d78c206f6a2d3f.md) | adapted | deckshell-only |
| 40 / N8b | ` 4f1bd38f0fbd17d96c893250bec8e2a00b676d35 ` | ` 1cb34fec99ea8b68df2abed8a626df491afa61d2 ` [适配详情](adaptations/1cb34fec99ea8b68df2abed8a626df491afa61d2.md) | adapted | deckshell-only |
| 41 / N8b | ` 5023ac25718db141361d66018746e66bd8e56bc6 ` | ` 1663c425c3c639f8a3f98bf3808670f9c4ef40d8 ` [适配详情](adaptations/1663c425c3c639f8a3f98bf3808670f9c4ef40d8.md) | adapted | deckshell-only |
| 42 / N8b | ` 2f5bb78f3e8b5fc73b7cf1f4a8ea09c38a946339 ` | ` ee6b6472609d03d754d76f699006209260ec6aaf ` [适配详情](adaptations/ee6b6472609d03d754d76f699006209260ec6aaf.md) | adapted | deckshell-only |
| 43 / N8b | ` b9759c0c68ac278ed1f7c6444e59f14e7743abb4 ` | ` 0060010150ceb7dbe6331f52156b446bc82862eb ` [条目](#entry-43) | gitlink-only | waylib-only |
| 44 / N8b | ` 3a100f265970cb6acf9addf07e5c297aab9e9839 ` | ` 375e1bb98daef4d3b50b0a4a40d8127bd761a73a ` [适配详情](adaptations/375e1bb98daef4d3b50b0a4a40d8127bd761a73a.md) | adapted | deckshell-only |
| 45 / N8b | 无（独立提交） | ` bee3531566e9d325e8d89db1ad124759033d7bc2 ` [适配详情](adaptations/bee3531566e9d325e8d89db1ad124759033d7bc2.md) | protocol-companion | protocol-companion |

## 逐项归属、路径与依赖

<a id="entry-1"></a>
### 1. N8a / ` fix(surface): keep restore position when switching output during animation `

- 本仓内容路径：` compositor/src/surface/surfacewrapper.cpp `。
- 实际改变：` compositor/src/surface/surfacewrapper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` f14d7cdf718307945f492eb1c6d7608413e83c29 ` → ` f14d7cdf718307945f492eb1c6d7608413e83c29 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` bac6470ac7932b30cf3cfc3a0bdb1fc9c9f31c34 ` 和原目标 ` e7988fbedb1dd7e3a5a7ff42e1d4ca030d846a06 ` 查询。

<a id="entry-2"></a>
### 2. N8a / ` fix(greeter): don't enter greeter when --lockscreen is absent `

- 本仓内容路径：` compositor/src/greeter/greeterproxy.cpp `。
- 实际改变：` compositor/src/greeter/greeterproxy.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` f14d7cdf718307945f492eb1c6d7608413e83c29 ` → ` f14d7cdf718307945f492eb1c6d7608413e83c29 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` f912abff4ef8e52208b5ebe97a8328ac8169c044 ` 和原目标 ` 90a7fe038559336a6d3f65f118d73ae11c087caa ` 查询。

<a id="entry-3"></a>
### 3. N8a / ` fix(build): gate treeland-debug source to Debug builds only `

- 本仓内容路径：` compositor/CMakeLists.txt `、` compositor/README.md `、` compositor/README.zh_CN.md `、` compositor/src/seat/helper.cpp `。
- 实际改变：` compositor/CMakeLists.txt `、` compositor/README.md `、` compositor/README.zh_CN.md `、` compositor/src/seat/helper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` f14d7cdf718307945f492eb1c6d7608413e83c29 ` → ` f14d7cdf718307945f492eb1c6d7608413e83c29 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` d83984336e4770d0d27b8eb05b68cebc395fde10 ` 和原目标 ` 07edb5cb3271245ff276c72def5c51c08424a2e1 ` 查询。
- 原审核说明：` 保留 DeckShell 已有安装包、ASan 和构建布局；只将来源的 Debug 默认启用条件、Release 动态 DConfig 更新及对应说明移植到规范目标路径。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/07edb5cb3271245ff276c72def5c51c08424a2e1.md)。

<a id="entry-4"></a>
### 4. N8a / ` fix(debug): avoid debug socket conflicts across run modes `

- 本仓内容路径：` compositor/CMakeLists.txt `、` compositor/README.md `、` compositor/README.zh_CN.md `、` compositor/src/CMakeLists.txt `、` compositor/src/common/treelandlogging.cpp `、` compositor/src/common/treelandlogging.h `、` compositor/src/modules/resource/treelanddebugsocket.cpp `、` compositor/src/modules/resource/treelanddebugsocket.h `、` compositor/src/modules/resource/treelandremotesource.cpp `、` compositor/src/modules/resource/treelandremotesource.h `、` compositor/tests/test_treeland_debug/CMakeLists.txt `、` compositor/tests/test_treeland_debug/main.cpp `、` compositor/tools/treeland-debug/CMakeLists.txt `、` compositor/tools/treeland-debug/debugserver.cpp `、` compositor/tools/treeland-debug/debugserver.h `、` compositor/tools/treeland-debug/debugsession.cpp `、` compositor/tools/treeland-debug/debugsession.h `、` compositor/tools/treeland-debug/main.cpp `。
- 实际改变：` compositor/CMakeLists.txt `、` compositor/README.md `、` compositor/README.zh_CN.md `、` compositor/src/CMakeLists.txt `、` compositor/src/common/treelandlogging.cpp `、` compositor/src/common/treelandlogging.h `、` compositor/src/modules/resource/treelanddebugsocket.cpp `、` compositor/src/modules/resource/treelanddebugsocket.h `、` compositor/src/modules/resource/treelandremotesource.cpp `、` compositor/src/modules/resource/treelandremotesource.h `、` compositor/tests/test_treeland_debug/CMakeLists.txt `、` compositor/tests/test_treeland_debug/main.cpp `、` compositor/tools/treeland-debug/CMakeLists.txt `、` compositor/tools/treeland-debug/debugserver.cpp `、` compositor/tools/treeland-debug/debugserver.h `、` compositor/tools/treeland-debug/debugsession.cpp `、` compositor/tools/treeland-debug/debugsession.h `、` compositor/tools/treeland-debug/main.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` f14d7cdf718307945f492eb1c6d7608413e83c29 ` → ` f14d7cdf718307945f492eb1c6d7608413e83c29 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` 3cb4cbe2404ba766ad0430a2a20f7303febfdcf8 ` 和原目标 ` 62b04567463080c6050c042382a5381abc139695 ` 查询。
- 原审核说明：` 保留 DeckShell 的 libdeckcompositor 构建名称和本地集成；完整引入来源 socket 生命周期、服务端和客户端更新；日志冲突只来自文件末尾空行，追加新的集中日志分类，不恢复已退休的上游构建入口。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/62b04567463080c6050c042382a5381abc139695.md)。

<a id="entry-5"></a>
### 5. N8a / ` fix(xwayland): keep modal dialogs above parent windows `

- 本仓内容路径：` compositor/src/core/shellhandler.cpp `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/core/shellhandler.cpp `。
- 排除的来源路径：` waylib/src/server/protocols/private/wxwaylandsurface_p.h `、` waylib/src/server/protocols/wxwaylandsurface.cpp `、` waylib/src/server/protocols/wxwaylandsurface.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` f14d7cdf718307945f492eb1c6d7608413e83c29 ` → ` e05868343441276dd43b2cc0c9c41d96dae1cd1c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` d3cdd8644710cbb55e56feccf039729eb307fe3f ` 和原目标 ` c655ce1ec9020d7b179a099890812a8230652105 ` 查询。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 同一 Treeland 来源的 C / waylib-shared 目标：` e05868343441276dd43b2cc0c9c41d96dae1cd1c `；跨仓定位 ` docs/treeland-sync/20260922_treeland_0_9_1_to_0_10_0_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-6"></a>
### 6. N8a / ` test(protocols): add wlroots protocol coverage `

- 本仓内容路径：` compositor/tests/protocols/CMakeLists.txt `、` compositor/tests/protocols/INDEX.md `、` compositor/tests/protocols/drm/CMakeLists.txt `、` compositor/tests/protocols/drm/README.md `、` compositor/tests/protocols/drm/drm.c `、` compositor/tests/protocols/drm/drm.h `、` compositor/tests/protocols/drm/setup.cpp `、` compositor/tests/protocols/framework/protocol-test-entry.cpp `、` compositor/tests/protocols/input-method-unstable-v2/CMakeLists.txt `、` compositor/tests/protocols/input-method-unstable-v2/README.md `、` compositor/tests/protocols/input-method-unstable-v2/input-method-unstable-v2.c `、` compositor/tests/protocols/input-method-unstable-v2/input-method-unstable-v2.h `、` compositor/tests/protocols/input-method-unstable-v2/setup.cpp `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-shortcut-manager-desktop-v2/treeland-shortcut-manager-desktop-v2.c `、` compositor/tests/protocols/virtual-keyboard-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/virtual-keyboard-unstable-v1/README.md `、` compositor/tests/protocols/virtual-keyboard-unstable-v1/setup.cpp `、` compositor/tests/protocols/virtual-keyboard-unstable-v1/virtual-keyboard-unstable-v1.c `、` compositor/tests/protocols/wlr-data-control-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/wlr-data-control-unstable-v1/README.md `、` compositor/tests/protocols/wlr-data-control-unstable-v1/setup.cpp `、` compositor/tests/protocols/wlr-data-control-unstable-v1/wlr-data-control-unstable-v1.c `、` compositor/tests/protocols/wlr-export-dmabuf-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/wlr-export-dmabuf-unstable-v1/README.md `、` compositor/tests/protocols/wlr-export-dmabuf-unstable-v1/setup.cpp `、` compositor/tests/protocols/wlr-export-dmabuf-unstable-v1/wlr-export-dmabuf-unstable-v1.c `、` compositor/tests/protocols/wlr-foreign-toplevel-management-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/wlr-foreign-toplevel-management-unstable-v1/README.md `、` compositor/tests/protocols/wlr-foreign-toplevel-management-unstable-v1/setup.cpp `、` compositor/tests/protocols/wlr-foreign-toplevel-management-unstable-v1/wlr-foreign-toplevel-management-unstable-v1.c `、` compositor/tests/protocols/wlr-foreign-toplevel-management-unstable-v1/wlr-foreign-toplevel-management-unstable-v1.h `、` compositor/tests/protocols/wlr-gamma-control-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/wlr-gamma-control-unstable-v1/README.md `、` compositor/tests/protocols/wlr-gamma-control-unstable-v1/setup.cpp `、` compositor/tests/protocols/wlr-gamma-control-unstable-v1/wlr-gamma-control-unstable-v1.c `、` compositor/tests/protocols/wlr-layer-shell-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/wlr-layer-shell-unstable-v1/README.md `、` compositor/tests/protocols/wlr-layer-shell-unstable-v1/setup.cpp `、` compositor/tests/protocols/wlr-layer-shell-unstable-v1/wlr-layer-shell-unstable-v1.c `、` compositor/tests/protocols/wlr-layer-shell-unstable-v1/wlr-layer-shell-unstable-v1.h `、` compositor/tests/protocols/wlr-output-management-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/wlr-output-management-unstable-v1/README.md `、` compositor/tests/protocols/wlr-output-management-unstable-v1/setup.cpp `、` compositor/tests/protocols/wlr-output-management-unstable-v1/wlr-output-management-unstable-v1.c `、` compositor/tests/protocols/wlr-output-management-unstable-v1/wlr-output-management-unstable-v1.h `、` compositor/tests/protocols/wlr-output-power-management-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/wlr-output-power-management-unstable-v1/README.md `、` compositor/tests/protocols/wlr-output-power-management-unstable-v1/setup.cpp `、` compositor/tests/protocols/wlr-output-power-management-unstable-v1/wlr-output-power-management-unstable-v1.c `、` compositor/tests/protocols/wlr-output-power-management-unstable-v1/wlr-output-power-management-unstable-v1.h `、` compositor/tests/protocols/wlr-screencopy-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/wlr-screencopy-unstable-v1/README.md `、` compositor/tests/protocols/wlr-screencopy-unstable-v1/setup.cpp `、` compositor/tests/protocols/wlr-screencopy-unstable-v1/wlr-screencopy-unstable-v1.c `、` compositor/tests/protocols/wlr-virtual-pointer-unstable-v1/README.md `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/tests/protocols/CMakeLists.txt `、` compositor/tests/protocols/INDEX.md `、` compositor/tests/protocols/drm/CMakeLists.txt `、` compositor/tests/protocols/drm/README.md `、` compositor/tests/protocols/drm/drm.c `、` compositor/tests/protocols/drm/drm.h `、` compositor/tests/protocols/drm/setup.cpp `、` compositor/tests/protocols/framework/protocol-test-entry.cpp `、` compositor/tests/protocols/input-method-unstable-v2/CMakeLists.txt `、` compositor/tests/protocols/input-method-unstable-v2/README.md `、` compositor/tests/protocols/input-method-unstable-v2/input-method-unstable-v2.c `、` compositor/tests/protocols/input-method-unstable-v2/input-method-unstable-v2.h `、` compositor/tests/protocols/input-method-unstable-v2/setup.cpp `、` compositor/tests/protocols/treeland-shortcut-manager-desktop-v2/treeland-shortcut-manager-desktop-v2.c `、` compositor/tests/protocols/virtual-keyboard-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/virtual-keyboard-unstable-v1/README.md `、` compositor/tests/protocols/virtual-keyboard-unstable-v1/setup.cpp `、` compositor/tests/protocols/virtual-keyboard-unstable-v1/virtual-keyboard-unstable-v1.c `、` compositor/tests/protocols/wlr-data-control-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/wlr-data-control-unstable-v1/README.md `、` compositor/tests/protocols/wlr-data-control-unstable-v1/setup.cpp `、` compositor/tests/protocols/wlr-data-control-unstable-v1/wlr-data-control-unstable-v1.c `、` compositor/tests/protocols/wlr-export-dmabuf-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/wlr-export-dmabuf-unstable-v1/README.md `、` compositor/tests/protocols/wlr-export-dmabuf-unstable-v1/setup.cpp `、` compositor/tests/protocols/wlr-export-dmabuf-unstable-v1/wlr-export-dmabuf-unstable-v1.c `、` compositor/tests/protocols/wlr-foreign-toplevel-management-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/wlr-foreign-toplevel-management-unstable-v1/README.md `、` compositor/tests/protocols/wlr-foreign-toplevel-management-unstable-v1/setup.cpp `、` compositor/tests/protocols/wlr-foreign-toplevel-management-unstable-v1/wlr-foreign-toplevel-management-unstable-v1.c `、` compositor/tests/protocols/wlr-foreign-toplevel-management-unstable-v1/wlr-foreign-toplevel-management-unstable-v1.h `、` compositor/tests/protocols/wlr-gamma-control-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/wlr-gamma-control-unstable-v1/README.md `、` compositor/tests/protocols/wlr-gamma-control-unstable-v1/setup.cpp `、` compositor/tests/protocols/wlr-gamma-control-unstable-v1/wlr-gamma-control-unstable-v1.c `、` compositor/tests/protocols/wlr-layer-shell-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/wlr-layer-shell-unstable-v1/README.md `、` compositor/tests/protocols/wlr-layer-shell-unstable-v1/setup.cpp `、` compositor/tests/protocols/wlr-layer-shell-unstable-v1/wlr-layer-shell-unstable-v1.c `、` compositor/tests/protocols/wlr-layer-shell-unstable-v1/wlr-layer-shell-unstable-v1.h `、` compositor/tests/protocols/wlr-output-management-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/wlr-output-management-unstable-v1/README.md `、` compositor/tests/protocols/wlr-output-management-unstable-v1/setup.cpp `、` compositor/tests/protocols/wlr-output-management-unstable-v1/wlr-output-management-unstable-v1.c `、` compositor/tests/protocols/wlr-output-management-unstable-v1/wlr-output-management-unstable-v1.h `、` compositor/tests/protocols/wlr-output-power-management-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/wlr-output-power-management-unstable-v1/README.md `、` compositor/tests/protocols/wlr-output-power-management-unstable-v1/setup.cpp `、` compositor/tests/protocols/wlr-output-power-management-unstable-v1/wlr-output-power-management-unstable-v1.c `、` compositor/tests/protocols/wlr-output-power-management-unstable-v1/wlr-output-power-management-unstable-v1.h `、` compositor/tests/protocols/wlr-screencopy-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/wlr-screencopy-unstable-v1/README.md `、` compositor/tests/protocols/wlr-screencopy-unstable-v1/setup.cpp `、` compositor/tests/protocols/wlr-screencopy-unstable-v1/wlr-screencopy-unstable-v1.c `、` compositor/tests/protocols/wlr-virtual-pointer-unstable-v1/README.md `。
- 排除的来源路径：` waylib/src/server/protocols/private/wtextinputv2.cpp `、` waylib/src/server/protocols/wlayershell.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` e05868343441276dd43b2cc0c9c41d96dae1cd1c ` → ` 91d126f4ed4836ba83174efa00f8b2e26d7708bd `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` 8bfa446c589f06d4f427a39b93a585a2406f5cdb ` 和原目标 ` b4a5826fa61f080b39e5ef4e989bd77da5cf47b2 ` 查询。
- 原审核说明：` 完整引入来源原生协议交互测试，保留本地协议框架与包边界；R XML 指向物化的 3rdparty/waylib-shared/3rdparty/wlroots/protocol，input-method 的 text-input-v2 XML 指向同一 C 候选内的 waylib/src/server/protocols/private，不使用不存在的上游源码布局。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/b4a5826fa61f080b39e5ef4e989bd77da5cf47b2.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 91d126f4ed4836ba83174efa00f8b2e26d7708bd `；跨仓定位 ` docs/treeland-sync/20260922_treeland_0_9_1_to_0_10_0_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-7"></a>
### 7. N8a / ` fix(export-dmabuf): expose the wlroots manager declaration `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/kernel/wlr_all.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 91d126f4ed4836ba83174efa00f8b2e26d7708bd ` → ` fe754deebcc47a0dbcd8492c946625b8b26aa8f2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` 007f3653c7942690f76db0c06ea55991efc59dc0 ` 和原目标 ` c2b72c0970b54440970a394ba7770860ed3955c7 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` fe754deebcc47a0dbcd8492c946625b8b26aa8f2 `；跨仓定位 ` docs/treeland-sync/20260922_treeland_0_9_1_to_0_10_0_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-8"></a>
### 8. N8a / ` fix(input-method): preserve text input focus during keyboard updates `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/protocols/winputmethodhelper.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` fe754deebcc47a0dbcd8492c946625b8b26aa8f2 ` → ` 0cce46d7be0f3faaba6118b7a279616b494aa2d8 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` bd2c6995dd49b309abf76af13688b317fe31244e ` 和原目标 ` 5a0f19288ac068187854fe9773dd3de269ea0265 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 0cce46d7be0f3faaba6118b7a279616b494aa2d8 `；跨仓定位 ` docs/treeland-sync/20260922_treeland_0_9_1_to_0_10_0_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-9"></a>
### 9. N8a / ` fix(output-management): publish current output state to new clients `

- 本仓内容路径：` compositor/src/seat/helper.cpp `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/seat/helper.cpp `。
- 排除的来源路径：` waylib/src/server/kernel/woutput.cpp `、` waylib/src/server/kernel/woutput.h `、` waylib/src/server/kernel/woutputlayout.cpp `、` waylib/src/server/protocols/woutputmanagerv1.cpp `、` waylib/src/server/protocols/woutputmanagerv1.h `、` waylib/src/server/qtquick/woutputrenderwindow.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 0cce46d7be0f3faaba6118b7a279616b494aa2d8 ` → ` cb6a911a19b06405d22ee92a4fee0907792a7ac6 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` b71d4af56f3c90d4a8bd5cf6b421bbc9028ac145 ` 和原目标 ` c38a625edb9567ff40633ccc6db0eb95fdb9f01d ` 查询。
- 原审核说明：` 按来源将 output-management 的 newOutput 提前到输出进入 compositor 时，解除 DConfig 异步恢复依赖；保留本地 wallpaper 初始化单次保护与失败日志，删除原 lambda 内重复的 newOutput，调整日志不再声称此时才发布输出。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/c38a625edb9567ff40633ccc6db0eb95fdb9f01d.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` cb6a911a19b06405d22ee92a4fee0907792a7ac6 `；跨仓定位 ` docs/treeland-sync/20260922_treeland_0_9_1_to_0_10_0_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-10"></a>
### 10. N8a / ` fix(foreign-toplevel): handle management requests `

- 本仓内容路径：` compositor/src/seat/helper.cpp `。
- 实际改变：` compositor/src/seat/helper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` cb6a911a19b06405d22ee92a4fee0907792a7ac6 ` → ` cb6a911a19b06405d22ee92a4fee0907792a7ac6 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` 1a457fedc3cbb7784a3d6e9165c7dc531d0067f1 ` 和原目标 ` 72cb6636921d8aa2c4feb5f90e996e3b2f44f9ee ` 查询。

<a id="entry-11"></a>
### 11. N8a / ` fix(surface): retarget pending state animations `

- 本仓内容路径：` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 实际改变：` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` cb6a911a19b06405d22ee92a4fee0907792a7ac6 ` → ` cb6a911a19b06405d22ee92a4fee0907792a7ac6 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` 591cf2a73fdd6329693c5b452cf70f076d902f16 ` 和原目标 ` 07020c5faa428631c154c8372958c7936be81d82 ` 查询。

<a id="entry-12"></a>
### 12. N8a / ` fix(surface): commit pending state after animations `

- 本仓内容路径：` compositor/src/surface/surfacewrapper.cpp `。
- 实际改变：` compositor/src/surface/surfacewrapper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` cb6a911a19b06405d22ee92a4fee0907792a7ac6 ` → ` cb6a911a19b06405d22ee92a4fee0907792a7ac6 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` 809017a78e5ab8558ff32e3752a5d91112d9db14 ` 和原目标 ` acac4338c0fe5087166a74d799978fb6aa963a65 ` 查询。

<a id="entry-13"></a>
### 13. N8a / ` feat(treeland-debug): add native MCP-over-HTTP server `

- 本仓内容路径：` compositor/tools/treeland-debug/README.md `、` compositor/tools/treeland-debug/debugserver.cpp `、` compositor/tools/treeland-debug/debugserver.h `。
- 实际改变：` compositor/tools/treeland-debug/README.md `、` compositor/tools/treeland-debug/debugserver.cpp `、` compositor/tools/treeland-debug/debugserver.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` cb6a911a19b06405d22ee92a4fee0907792a7ac6 ` → ` cb6a911a19b06405d22ee92a4fee0907792a7ac6 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` 266f951f730967c76958692bb0c957717f89cb4a ` 和原目标 ` 725d2448d9ba894aebda1ee8383b5fac46725054 ` 查询。

<a id="entry-14"></a>
### 14. N8a / ` feat(skills): add treeland-debug skill for AI debugging `

- 本仓内容路径：` compositor/.agents/skills/treeland-debug/SKILL.md `。
- 实际改变：` compositor/.agents/skills/treeland-debug/SKILL.md `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` cb6a911a19b06405d22ee92a4fee0907792a7ac6 ` → ` cb6a911a19b06405d22ee92a4fee0907792a7ac6 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` 8caa8dd8a42193efef23736132958333e7bc1e4c ` 和原目标 ` ed16740f163c19f14d1bb794acdf042433727781 ` 查询。

<a id="entry-15"></a>
### 15. N8a / ` fix(treeland-debug): use m_urls.join for screenshot errors `

- 本仓内容路径：` compositor/tools/treeland-debug/debugserver.cpp `。
- 实际改变：` compositor/tools/treeland-debug/debugserver.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` cb6a911a19b06405d22ee92a4fee0907792a7ac6 ` → ` cb6a911a19b06405d22ee92a4fee0907792a7ac6 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` 4485b04b478f921cb1491e69e9c9e33293f9affa ` 和原目标 ` 7f5b13c7588921c3e8732bd6926538eb25a60b22 ` 查询。

<a id="entry-16"></a>
### 16. N8a / ` fix(treeland-debug): rename dconfig option debugSource to remoteDebug `

- 本仓内容路径：` compositor/.agents/skills/treeland-debug/SKILL.md `、` compositor/CMakeLists.txt `、` compositor/README.md `、` compositor/README.zh_CN.md `、` compositor/misc/dconfig/org.deepin.dde.treeland.json `、` compositor/src/seat/helper.cpp `、` compositor/tools/treeland-debug/README.md `。
- 实际改变：` compositor/.agents/skills/treeland-debug/SKILL.md `、` compositor/CMakeLists.txt `、` compositor/README.md `、` compositor/README.zh_CN.md `、` compositor/misc/dconfig/org.deepin.dde.treeland.json `、` compositor/src/seat/helper.cpp `、` compositor/tools/treeland-debug/README.md `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` cb6a911a19b06405d22ee92a4fee0907792a7ac6 ` → ` cb6a911a19b06405d22ee92a4fee0907792a7ac6 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` 3357de71a728b3f486a010bb9fe0c630314912dd ` 和原目标 ` e536b2e32c626ccb0cfb6545a1aa514646a89a9b ` 查询。

<a id="entry-17"></a>
### 17. N8a / ` fix(surface): avoid null shell surface on XWayland teardown `

- 本仓内容路径：` compositor/src/core/shellhandler.cpp `、` compositor/src/core/shellhandler.h `、` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/core/shellhandler.cpp `、` compositor/src/core/shellhandler.h `、` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 排除的来源路径：` waylib/src/server/qtquick/wxwaylandsurfaceitem.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` cb6a911a19b06405d22ee92a4fee0907792a7ac6 ` → ` d6e6e6bc9b6bceee9997ae6a39b5c07137671619 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` e5e52083e1aa69ac66070098ec44ae47752ef759 ` 和原目标 ` 596d2b55f7991fc972fff7fe03cfca600a1542ca ` 查询。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 同一 Treeland 来源的 C / waylib-shared 目标：` d6e6e6bc9b6bceee9997ae6a39b5c07137671619 `；跨仓定位 ` docs/treeland-sync/20260922_treeland_0_9_1_to_0_10_0_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-18"></a>
### 18. N8a / ` feat(treeland-debug): restrict access by build type and add polkit escalation `

- 本仓内容路径：` compositor/.agents/skills/treeland-debug/SKILL.md `、` compositor/debian/treeland.install `、` compositor/misc/CMakeLists.txt `、` compositor/misc/polkit/CMakeLists.txt `、` compositor/misc/polkit/org.deepin.dde.treeland-debug.policy.in `、` compositor/src/modules/resource/treelandremotesource.cpp `、` compositor/tools/treeland-debug/README.md `、` compositor/tools/treeland-debug/main.cpp `。
- 实际改变：` compositor/.agents/skills/treeland-debug/SKILL.md `、` compositor/debian/treeland.install `、` compositor/misc/CMakeLists.txt `、` compositor/misc/polkit/CMakeLists.txt `、` compositor/misc/polkit/org.deepin.dde.treeland-debug.policy.in `、` compositor/src/modules/resource/treelandremotesource.cpp `、` compositor/tools/treeland-debug/README.md `、` compositor/tools/treeland-debug/main.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` d6e6e6bc9b6bceee9997ae6a39b5c07137671619 ` → ` d6e6e6bc9b6bceee9997ae6a39b5c07137671619 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` 773388598efa732aa581d489f55921bf57e4dbdb ` 和原目标 ` e3199b03d8ed16fd14d86b622104bd145765a3ac ` 查询。
- 原审核说明：` 完整引入来源 Debug 构建访问限制和 polkit 提权路径；misc 仅增加 polkit 子目录，不恢复本地已删除的 cmake 子目录。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/e3199b03d8ed16fd14d86b622104bd145765a3ac.md)。

<a id="entry-19"></a>
### 19. N8a / ` fix(xwayland): preserve compositor-controlled resize geometry `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/qtquick/wxwaylandsurfaceitem.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` d6e6e6bc9b6bceee9997ae6a39b5c07137671619 ` → ` dc036fba991d5218fd744730bd50f51485eeed87 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` b727a8209385c064fbe96d9a3a74a00f27121b13 ` 和原目标 ` c7b1809d7908184b4a983cdbeb1c9cc80085c530 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` dc036fba991d5218fd744730bd50f51485eeed87 `；跨仓定位 ` docs/treeland-sync/20260922_treeland_0_9_1_to_0_10_0_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-20"></a>
### 20. N8a / ` fix: track exported surface lifetime natively to prevent bad object crash `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/protocols/wremotesubsurfacemanagerv1.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` dc036fba991d5218fd744730bd50f51485eeed87 ` → ` 520d62836f73c1f156f38382e4c3f96797d14f91 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` df7b59b32de4f3982c968416cf92b3319daa7f20 ` 和原目标 ` 384af637fa17312a903de9ddca52272c072b119c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 520d62836f73c1f156f38382e4c3f96797d14f91 `；跨仓定位 ` docs/treeland-sync/20260922_treeland_0_9_1_to_0_10_0_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-21"></a>
### 21. N8a / ` fix: send frame done to remote subsurfaces `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/kernel/wsurface.cpp `、` waylib/src/server/protocols/wremotesubsurfacemanagerv1.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 520d62836f73c1f156f38382e4c3f96797d14f91 ` → ` 6979d0dff844a26bfe1bf8afbbd01cc0966ee553 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` b3208c08a3599590ece69c3a68773e07584969bb ` 和原目标 ` f00e4f7942285f127dcd111157cfb711fa77c340 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 6979d0dff844a26bfe1bf8afbbd01cc0966ee553 `；跨仓定位 ` docs/treeland-sync/20260922_treeland_0_9_1_to_0_10_0_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-22"></a>
### 22. N8a / ` fix(greeter): keep unlock animation on manual session activate `

- 本仓内容路径：` compositor/src/greeter/greeterproxy.cpp `。
- 实际改变：` compositor/src/greeter/greeterproxy.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 6979d0dff844a26bfe1bf8afbbd01cc0966ee553 ` → ` 6979d0dff844a26bfe1bf8afbbd01cc0966ee553 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` af2e2bbe5bd7763c47cf8ca42c49fdd90776f167 ` 和原目标 ` c0a0b0230f624b553bdf2038a6eed9dae1339eb7 ` 查询。

<a id="entry-23"></a>
### 23. N8a / ` fix(treeland-debug): silence unused noEscalate warning in dev builds `

- 本仓内容路径：` compositor/tools/treeland-debug/main.cpp `。
- 实际改变：` compositor/tools/treeland-debug/main.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 6979d0dff844a26bfe1bf8afbbd01cc0966ee553 ` → ` 6979d0dff844a26bfe1bf8afbbd01cc0966ee553 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` 1173d14965daef4048b5633676a1b873f8e6815a ` 和原目标 ` 9972226d67568d58c17caf0656a9601206b0dcbc ` 查询。

<a id="entry-24"></a>
### 24. N8a / ` fix(xwayland): synchronize transient window stacking `

- 本仓内容路径：` compositor/src/core/shellhandler.cpp `。
- 实际改变：` compositor/src/core/shellhandler.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 6979d0dff844a26bfe1bf8afbbd01cc0966ee553 ` → ` 6979d0dff844a26bfe1bf8afbbd01cc0966ee553 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` 98071bd1d0039beb02a4397a91aa6c0abd6488ae ` 和原目标 ` 1d732b58d831f614a60ae8fc12e13c0bd31b0738 ` 查询。

<a id="entry-25"></a>
### 25. N8a / ` fix(xwayland): skip restacking override-redirect windows `

- 本仓内容路径：` compositor/src/core/shellhandler.cpp `。
- 实际改变：` compositor/src/core/shellhandler.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 6979d0dff844a26bfe1bf8afbbd01cc0966ee553 ` → ` 6979d0dff844a26bfe1bf8afbbd01cc0966ee553 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` b4935634e511fd85d90cd8a9543364e68825f8c7 ` 和原目标 ` d0a8390e2d0a05a3e8c5c879f8e1d0ed6e1b8a1f ` 查询。

<a id="entry-26"></a>
### 26. N8a / ` refactor: adapt to treeland-protocols unstable-v2 and wine naming `

- 本仓内容路径：` compositor/.agents/skills/treeland-private-wayland-protocol/SKILL.md `、` compositor/src/modules/app-id-resolver/CMakeLists.txt `、` compositor/src/modules/app-id-resolver/appidresolver.cpp `、` compositor/src/modules/prelaunch-splash/CMakeLists.txt `、` compositor/src/modules/prelaunch-splash/prelaunchsplash.cpp `、` compositor/src/modules/screensaver/CMakeLists.txt `、` compositor/src/modules/screensaver/screensaverinterfacev1.cpp `、` compositor/src/modules/screensaver/screensaverinterfacev2.cpp `、` compositor/src/modules/screensaver/screensaverinterfacev1.h `、` compositor/src/modules/screensaver/screensaverinterfacev2.h `、` compositor/src/modules/wallpaper/wallpapershellinterfacev1.h `、` compositor/src/modules/wine-window-management/CMakeLists.txt `、` compositor/src/modules/wine-window-management/winewindowmanagement.cpp `、` compositor/src/modules/wine-window-state/CMakeLists.txt `、` compositor/src/modules/wine-window-state/winewindowstate.cpp `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/src/treeland-screensaver/CMakeLists.txt `、` compositor/src/treeland-screensaver/screensaver.cpp `、` compositor/tests/protocols/CMakeLists.txt `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v2/setup.cpp `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v1/treeland-app-id-resolver-desktop-v1.c `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v2/treeland-app-id-resolver-desktop-v2.c `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v1/treeland-app-id-resolver-desktop-v1.h `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v2/treeland-app-id-resolver-desktop-v2.h `、` compositor/tests/protocols/treeland-app-id-resolver-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-app-id-resolver-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-app-id-resolver-v1/README.md `、` compositor/tests/protocols/treeland-app-id-resolver-v2/README.md `、` compositor/tests/protocols/treeland-app-id-resolver-v1/setup.cpp `、` compositor/tests/protocols/treeland-app-id-resolver-v2/setup.cpp `、` compositor/tests/protocols/treeland-app-id-resolver-v1/treeland-app-id-resolver-v1.c `、` compositor/tests/protocols/treeland-app-id-resolver-v2/treeland-app-id-resolver-v2.c `、` compositor/tests/protocols/treeland-app-id-resolver-v1/treeland-app-id-resolver-v1.h `、` compositor/tests/protocols/treeland-app-id-resolver-v2/treeland-app-id-resolver-v2.h `、` compositor/tests/protocols/treeland-prelaunch-splash-desktop-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-prelaunch-splash-desktop-v2/treeland-prelaunch-splash-desktop-v2.c `、` compositor/tests/protocols/treeland-prelaunch-splash-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-prelaunch-splash-v2/treeland-prelaunch-splash-v2.c `、` compositor/tests/protocols/treeland-screensaver-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-screensaver-desktop-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-screensaver-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-screensaver-desktop-v2/setup.cpp `、` compositor/tests/protocols/treeland-screensaver-desktop-v1/treeland-screensaver-desktop-v1.c `、` compositor/tests/protocols/treeland-screensaver-desktop-v2/treeland-screensaver-desktop-v2.c `、` compositor/tests/protocols/treeland-screensaver-desktop-v1/treeland-screensaver-desktop-v1.h `、` compositor/tests/protocols/treeland-screensaver-desktop-v2/treeland-screensaver-desktop-v2.h `、` compositor/tests/protocols/treeland-screensaver-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-screensaver-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-screensaver-v1/README.md `、` compositor/tests/protocols/treeland-screensaver-v2/README.md `、` compositor/tests/protocols/treeland-screensaver-v1/setup.cpp `、` compositor/tests/protocols/treeland-screensaver-v2/setup.cpp `、` compositor/tests/protocols/treeland-screensaver-v1/treeland-screensaver-v1.c `、` compositor/tests/protocols/treeland-screensaver-v2/treeland-screensaver-v2.c `、` compositor/tests/protocols/treeland-screensaver-v1/treeland-screensaver-v1.h `、` compositor/tests/protocols/treeland-screensaver-v2/treeland-screensaver-v2.h `、` compositor/tests/protocols/treeland-wallpaper-desktop-v1/treeland-wallpaper-desktop-v1.c `、` compositor/tests/protocols/treeland-wallpaper-shell-unstable-v1/treeland-wallpaper-shell-unstable-v1.c `、` compositor/tools/treeland-session-helper/CMakeLists.txt `、` compositor/tools/treeland-session-helper/main.cpp `、` compositor/wallpaper-factory/qwaylandwallpapershellintegration.cpp `、` compositor/wallpaper-factory/qwaylandwallpapersurface.cpp `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/.agents/skills/treeland-private-wayland-protocol/SKILL.md `、` compositor/src/modules/app-id-resolver/CMakeLists.txt `、` compositor/src/modules/app-id-resolver/appidresolver.cpp `、` compositor/src/modules/prelaunch-splash/CMakeLists.txt `、` compositor/src/modules/prelaunch-splash/prelaunchsplash.cpp `、` compositor/src/modules/screensaver/CMakeLists.txt `、` compositor/src/modules/screensaver/screensaverinterfacev1.cpp `、` compositor/src/modules/screensaver/screensaverinterfacev1.h `、` compositor/src/modules/screensaver/screensaverinterfacev2.cpp `、` compositor/src/modules/screensaver/screensaverinterfacev2.h `、` compositor/src/modules/wallpaper/wallpapershellinterfacev1.h `、` compositor/src/modules/wine-window-management/CMakeLists.txt `、` compositor/src/modules/wine-window-management/winewindowmanagement.cpp `、` compositor/src/modules/wine-window-state/CMakeLists.txt `、` compositor/src/modules/wine-window-state/winewindowstate.cpp `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/src/treeland-screensaver/CMakeLists.txt `、` compositor/src/treeland-screensaver/screensaver.cpp `、` compositor/tests/protocols/CMakeLists.txt `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v1/treeland-app-id-resolver-desktop-v1.c `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v1/treeland-app-id-resolver-desktop-v1.h `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v2/setup.cpp `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v2/treeland-app-id-resolver-desktop-v2.c `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v2/treeland-app-id-resolver-desktop-v2.h `、` compositor/tests/protocols/treeland-app-id-resolver-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-app-id-resolver-v1/README.md `、` compositor/tests/protocols/treeland-app-id-resolver-v1/setup.cpp `、` compositor/tests/protocols/treeland-app-id-resolver-v1/treeland-app-id-resolver-v1.c `、` compositor/tests/protocols/treeland-app-id-resolver-v1/treeland-app-id-resolver-v1.h `、` compositor/tests/protocols/treeland-app-id-resolver-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-app-id-resolver-v2/README.md `、` compositor/tests/protocols/treeland-app-id-resolver-v2/setup.cpp `、` compositor/tests/protocols/treeland-app-id-resolver-v2/treeland-app-id-resolver-v2.c `、` compositor/tests/protocols/treeland-app-id-resolver-v2/treeland-app-id-resolver-v2.h `、` compositor/tests/protocols/treeland-prelaunch-splash-desktop-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-prelaunch-splash-desktop-v2/treeland-prelaunch-splash-desktop-v2.c `、` compositor/tests/protocols/treeland-prelaunch-splash-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-prelaunch-splash-v2/treeland-prelaunch-splash-v2.c `、` compositor/tests/protocols/treeland-screensaver-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-screensaver-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-screensaver-desktop-v1/treeland-screensaver-desktop-v1.c `、` compositor/tests/protocols/treeland-screensaver-desktop-v1/treeland-screensaver-desktop-v1.h `、` compositor/tests/protocols/treeland-screensaver-desktop-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-screensaver-desktop-v2/setup.cpp `、` compositor/tests/protocols/treeland-screensaver-desktop-v2/treeland-screensaver-desktop-v2.c `、` compositor/tests/protocols/treeland-screensaver-desktop-v2/treeland-screensaver-desktop-v2.h `、` compositor/tests/protocols/treeland-screensaver-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-screensaver-v1/README.md `、` compositor/tests/protocols/treeland-screensaver-v1/setup.cpp `、` compositor/tests/protocols/treeland-screensaver-v1/treeland-screensaver-v1.c `、` compositor/tests/protocols/treeland-screensaver-v1/treeland-screensaver-v1.h `、` compositor/tests/protocols/treeland-screensaver-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-screensaver-v2/README.md `、` compositor/tests/protocols/treeland-screensaver-v2/setup.cpp `、` compositor/tests/protocols/treeland-screensaver-v2/treeland-screensaver-v2.c `、` compositor/tests/protocols/treeland-screensaver-v2/treeland-screensaver-v2.h `、` compositor/tests/protocols/treeland-wallpaper-desktop-v1/treeland-wallpaper-desktop-v1.c `、` compositor/tests/protocols/treeland-wallpaper-shell-unstable-v1/treeland-wallpaper-shell-unstable-v1.c `、` compositor/tools/treeland-session-helper/CMakeLists.txt `、` compositor/tools/treeland-session-helper/main.cpp `、` compositor/wallpaper-factory/qwaylandwallpapershellintegration.cpp `、` compositor/wallpaper-factory/qwaylandwallpapersurface.cpp `、` protocols/compositor/CMakeLists.txt `、` protocols/compositor/xml/treeland-app-id-resolver-unstable-v2.xml `、` protocols/compositor/xml/treeland-app-id-resolver-v1.xml `、` protocols/compositor/xml/treeland-prelaunch-splash-unstable-v2.xml `、` protocols/compositor/xml/treeland-prelaunch-splash-v2.xml `、` protocols/compositor/xml/treeland-screensaver-unstable-v2.xml `、` protocols/compositor/xml/treeland-screensaver-v1.xml `、` protocols/compositor/xml/treeland-wallpaper-shell-unstable-v1.xml `、` protocols/compositor/xml/treeland-wine-window-management-unstable-v1.xml `、` protocols/compositor/xml/treeland-wine-window-state-unstable-v1.xml `。
- 排除的来源路径：` waylib/src/server/protocols/wremotesubsurfacemanagerv1.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 6979d0dff844a26bfe1bf8afbbd01cc0966ee553 ` → ` df72756d20356894c584b2a69376eaa1a4600bed `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/parent-evidence.json`；以来源 ` a5656ab80ae11a0068d507659f35bb999b6d815d ` 和原目标 ` f8772b17a0ad4e942ddaf9cf1fae2148518ca5cd ` 查询。
- 原审核说明：` 仅实施 PRD 5.3.1 精确批准的 unstable-v2/Wine 协议迁移；以相邻 DeckShell 目标树为基础保留 Helper 的既有接口、DISABLE_DDM 条件、初始化及锁屏语义，只移植 screensaver v2 名称；保留受控协议入口、模块相对路径和本地构建名。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/f8772b17a0ad4e942ddaf9cf1fae2148518ca5cd.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` df72756d20356894c584b2a69376eaa1a4600bed `；跨仓定位 ` docs/treeland-sync/20260922_treeland_0_9_1_to_0_10_0_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-27"></a>
### 27. N8a / chore(protocol): 同步 remote-subsurface 配套快照

- 独立类型：protocol-companion；不计为普通来源回放。
- [逐路径增量及原依据](adaptations/0ba8ee8fb414e5711e4299d1142dc7d8276ed75c.md)。

<a id="entry-28"></a>
### 28. N8a / fix(sync): 核验已安装 Waylib 消费链并记录独立本地修复

- 独立类型：local-fix；不计为普通来源回放。
- [逐路径增量及原依据](adaptations/cb9c6bf6bbc4a53bc50212204f34ad0cd5308ffb.md)。

<a id="entry-29"></a>
### 29. N8a → N8b / fix(sync): 收敛 foreign-toplevel 状态编码至规范实现

- 独立类型：structural-repair；不计为普通来源回放。
- [逐路径增量及原依据](adaptations/38ca30d3e220e99a119dca7465d1acb887e7f186.md)。

<a id="entry-30"></a>
### 30. N8b / ` fix(screensaver): release inhibit silently in destroy `

- 本仓内容路径：` compositor/src/modules/screensaver/screensaverinterfacev2.cpp `、` compositor/src/modules/screensaver/screensaverinterfacev2.h `。
- 实际改变：` compositor/src/modules/screensaver/screensaverinterfacev2.cpp `、` compositor/src/modules/screensaver/screensaverinterfacev2.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` a2b1c5752afca1581a95a8bd8ac6d3dbe115b8e4 ` → ` a2b1c5752afca1581a95a8bd8ac6d3dbe115b8e4 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/parent-evidence.json`；以来源 ` c0917aed288d209d0a27ccb4539d1de3e10eb7b6 ` 和原目标 ` 155da93a88228842f41a1bea407d0bb49a009f5c ` 查询。
- 原审核说明：` 按来源差异进行三方合并，保留相邻本地树的构建名、受控协议目录及已有条件；新增/移动文件使用规范映射路径。协议额外路径仅按 PRD §5.3.1 精确迁移。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/155da93a88228842f41a1bea407d0bb49a009f5c.md)。

<a id="entry-31"></a>
### 31. N8b / ` refactor: rename qwBuffer to wlrBuffer for naming consistency `

- 本仓内容路径：` compositor/src/modules/capture/capture.cpp `、` compositor/src/modules/capture/impl/capturev1impl.cpp `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/modules/capture/capture.cpp `、` compositor/src/modules/capture/impl/capturev1impl.cpp `。
- 排除的来源路径：` waylib/src/server/qtquick/private/wbufferrenderer.cpp `、` waylib/src/server/qtquick/wquickcursor.cpp `、` waylib/src/server/qtquick/wsgtextureprovider.cpp `、` waylib/src/server/qtquick/wsgtextureprovider.h `、` waylib/src/server/utils/wextimagecapturesourcev1impl.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` a2b1c5752afca1581a95a8bd8ac6d3dbe115b8e4 ` → ` 93bc34f05f23d7daa66f941539b377f8601dab6d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/parent-evidence.json`；以来源 ` 24e1c7a4ea8a5eeaedff24dee3df27e10f02c496 ` 和原目标 ` c54dbcbfbb7100390bf64546a370ecc3e42ad094 ` 查询。
- 原审核说明：` 按来源差异进行三方合并，保留相邻本地树的构建名、受控协议目录及已有条件；新增/移动文件使用规范映射路径。协议额外路径仅按 PRD §5.3.1 精确迁移。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/c54dbcbfbb7100390bf64546a370ecc3e42ad094.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 93bc34f05f23d7daa66f941539b377f8601dab6d `；跨仓定位 ` docs/treeland-sync/20260922_treeland_0_9_1_to_0_10_0_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-32"></a>
### 32. N8b / ` fix(show-desktop): cancel show-desktop when opening interactive layer-shell windows `

- 本仓内容路径：` compositor/src/core/shellhandler.cpp `。
- 实际改变：` compositor/src/core/shellhandler.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 93bc34f05f23d7daa66f941539b377f8601dab6d ` → ` 93bc34f05f23d7daa66f941539b377f8601dab6d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/parent-evidence.json`；以来源 ` b3a357d44569f7d0e32bd6a40ffda74edec83750 ` 和原目标 ` 134a681a992521213b4f0a4a6bb0aef2be5c85dd ` 查询。
- 原审核说明：` 按来源差异进行三方合并，保留相邻本地树的构建名、受控协议目录及已有条件；新增/移动文件使用规范映射路径。协议额外路径仅按 PRD §5.3.1 精确迁移。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/134a681a992521213b4f0a4a6bb0aef2be5c85dd.md)。

<a id="entry-33"></a>
### 33. N8b / ` fix(xwayland): allow cross-UID MIT-SHM via AmbientCapabilities=CAP_IPC_OWNER `

- 本仓内容路径：` compositor/misc/systemd/treeland.service.in `。
- 实际改变：` compositor/misc/systemd/treeland.service.in `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 93bc34f05f23d7daa66f941539b377f8601dab6d ` → ` 93bc34f05f23d7daa66f941539b377f8601dab6d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/parent-evidence.json`；以来源 ` 17bca039766adb868c318fa7b7d69e7f428f64ac ` 和原目标 ` 9b2b8faff286e3010edeac795ea67f12ff5ac543 ` 查询。
- 原审核说明：` 按来源差异进行三方合并，保留相邻本地树的构建名、受控协议目录及已有条件；新增/移动文件使用规范映射路径。协议额外路径仅按 PRD §5.3.1 精确迁移。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/9b2b8faff286e3010edeac795ea67f12ff5ac543.md)。

<a id="entry-34"></a>
### 34. N8b / ` fix(shell): keep close animation in place on activation transfer `

- 本仓内容路径：` compositor/src/core/shellhandler.cpp `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/src/surface/surfacewrapper.cpp `。
- 实际改变：` compositor/src/core/shellhandler.cpp `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/src/surface/surfacewrapper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 93bc34f05f23d7daa66f941539b377f8601dab6d ` → ` 93bc34f05f23d7daa66f941539b377f8601dab6d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/parent-evidence.json`；以来源 ` f645b104475c30e150930a1ed0d84c70be039b01 ` 和原目标 ` 31d80cbdfb053b7ad106d655e4acf6456f5513ce ` 查询。
- 原审核说明：` 按来源差异进行三方合并，保留相邻本地树的构建名、受控协议目录及已有条件；新增/移动文件使用规范映射路径。协议额外路径仅按 PRD §5.3.1 精确迁移。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/31d80cbdfb053b7ad106d655e4acf6456f5513ce.md)。

<a id="entry-35"></a>
### 35. N8b / ` fix(lockscreen): make login view global and follow cursor output `

- 本仓内容路径：` compositor/src/core/lockscreen.cpp `、` compositor/src/core/lockscreen.h `、` compositor/src/interfaces/lockscreeninterface.h `、` compositor/src/plugins/lockscreen/CMakeLists.txt `、` compositor/src/plugins/lockscreen/lockscreenplugin.cpp `、` compositor/src/plugins/lockscreen/lockscreenplugin.h `、` compositor/src/plugins/lockscreen/qml/Greeter.qml `、` compositor/src/plugins/lockscreen/qml/LoginView.qml `、` compositor/src/seat/helper.cpp `。
- 实际改变：` compositor/src/core/lockscreen.cpp `、` compositor/src/core/lockscreen.h `、` compositor/src/interfaces/lockscreeninterface.h `、` compositor/src/plugins/lockscreen/CMakeLists.txt `、` compositor/src/plugins/lockscreen/lockscreenplugin.cpp `、` compositor/src/plugins/lockscreen/lockscreenplugin.h `、` compositor/src/plugins/lockscreen/qml/Greeter.qml `、` compositor/src/plugins/lockscreen/qml/LoginView.qml `、` compositor/src/seat/helper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 93bc34f05f23d7daa66f941539b377f8601dab6d ` → ` 93bc34f05f23d7daa66f941539b377f8601dab6d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/parent-evidence.json`；以来源 ` ba4f63aec9a6acccfe9deef00d6c8002b2074af3 ` 和原目标 ` 1f1cb4eb7ab60a3b68f5e2a821c14a6312bd0c09 ` 查询。
- 原审核说明：` 按来源差异进行三方合并，保留相邻本地树的构建名、受控协议目录及已有条件；新增/移动文件使用规范映射路径。协议额外路径仅按 PRD §5.3.1 精确迁移。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/1f1cb4eb7ab60a3b68f5e2a821c14a6312bd0c09.md)。

<a id="entry-36"></a>
### 36. N8b / ` fix(lockscreen): restore white window text color in login view `

- 本仓内容路径：` compositor/src/plugins/lockscreen/qml/LoginView.qml `。
- 实际改变：` compositor/src/plugins/lockscreen/qml/LoginView.qml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 93bc34f05f23d7daa66f941539b377f8601dab6d ` → ` 93bc34f05f23d7daa66f941539b377f8601dab6d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/parent-evidence.json`；以来源 ` 4b1c552b70160992e7f418847ca9acf43f4d0279 ` 和原目标 ` 433b5e19a8c8228acf234f94e633cfe2b76cac21 ` 查询。
- 原审核说明：` 按来源差异进行三方合并，保留相邻本地树的构建名、受控协议目录及已有条件；新增/移动文件使用规范映射路径。协议额外路径仅按 PRD §5.3.1 精确迁移。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/433b5e19a8c8228acf234f94e633cfe2b76cac21.md)。

<a id="entry-37"></a>
### 37. N8b / ` fix(xwayland): honor above and below window states `

- 本仓内容路径：` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 排除的来源路径：` waylib/src/server/protocols/wxwaylandsurface.cpp `、` waylib/src/server/protocols/wxwaylandsurface.h `、` waylib/tests/unit_tests/test_native_handles/main.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 93bc34f05f23d7daa66f941539b377f8601dab6d ` → ` 25d3d2b92a5aa7b4a087927092865172cd1c4330 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/parent-evidence.json`；以来源 ` d9efe405ab5b91daaa1a4ae5ee237cf076064910 ` 和原目标 ` 27e08f983493c74e42cad21aacbc9694b3232fb4 ` 查询。
- 原审核说明：` 按来源差异进行三方合并，保留相邻本地树的构建名、受控协议目录及已有条件；新增/移动文件使用规范映射路径。协议额外路径仅按 PRD §5.3.1 精确迁移。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/27e08f983493c74e42cad21aacbc9694b3232fb4.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 25d3d2b92a5aa7b4a087927092865172cd1c4330 `；跨仓定位 ` docs/treeland-sync/20260922_treeland_0_9_1_to_0_10_0_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-38"></a>
### 38. N8b / ` fix(remote-subsurface): reattach child subsurface when ancestor is recreated `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/protocols/wremotesubsurfacemanagerv1.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 25d3d2b92a5aa7b4a087927092865172cd1c4330 ` → ` 1f37c019972da79aa624947a1cdcc3c97f625559 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/parent-evidence.json`；以来源 ` 423b2ad15cf2d6153aa3c6a00e7bef7dbec01aa0 ` 和原目标 ` 54edd9a5c45480b917fe5a9cdebdf59acb3e0098 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 1f37c019972da79aa624947a1cdcc3c97f625559 `；跨仓定位 ` docs/treeland-sync/20260922_treeland_0_9_1_to_0_10_0_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-39"></a>
### 39. N8b / ` fix(surface): keep modal window animation above parent `

- 本仓内容路径：` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 实际改变：` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 1f37c019972da79aa624947a1cdcc3c97f625559 ` → ` 1f37c019972da79aa624947a1cdcc3c97f625559 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/parent-evidence.json`；以来源 ` cb038ef766940545fd05d0a22578c7e9fbaa7324 ` 和原目标 ` d806f87a8f58ff03d447deace2d78c206f6a2d3f ` 查询。
- 原审核说明：` 按来源差异进行三方合并，保留相邻本地树的构建名、受控协议目录及已有条件；新增/移动文件使用规范映射路径。协议额外路径仅按 PRD §5.3.1 精确迁移。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/d806f87a8f58ff03d447deace2d78c206f6a2d3f.md)。

<a id="entry-40"></a>
### 40. N8b / ` fix: connect dock rectangle handler before splash handover `

- 本仓内容路径：` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv1.cpp `。
- 实际改变：` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv1.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 1f37c019972da79aa624947a1cdcc3c97f625559 ` → ` 1f37c019972da79aa624947a1cdcc3c97f625559 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/parent-evidence.json`；以来源 ` 4f1bd38f0fbd17d96c893250bec8e2a00b676d35 ` 和原目标 ` 1cb34fec99ea8b68df2abed8a626df491afa61d2 ` 查询。
- 原审核说明：` 按来源差异进行三方合并，保留相邻本地树的构建名、受控协议目录及已有条件；新增/移动文件使用规范映射路径。协议额外路径仅按 PRD §5.3.1 精确迁移。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/1cb34fec99ea8b68df2abed8a626df491afa61d2.md)。

<a id="entry-41"></a>
### 41. N8b / ` refactor: adapt window-management to treeland-show-desktop-v1 protocol `

- 本仓内容路径：` compositor/.agents/skills/treeland-debug/SKILL.md `、` compositor/examples/test_show_desktop/CMakeLists.txt `、` compositor/examples/test_show_desktop/main.cpp `、` compositor/src/core/shellhandler.cpp `、` compositor/src/modules/CMakeLists.txt `、` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv1.cpp `、` compositor/src/modules/shortcut/shortcutrunner.cpp `、` compositor/src/modules/show-desktop/CMakeLists.txt `、` compositor/src/modules/show-desktop/showdesktopinterfacev1.cpp `、` compositor/src/modules/window-management/windowmanagementinterfacev1.h `、` compositor/src/modules/show-desktop/showdesktopinterfacev1.h `、` compositor/src/modules/window-management/CMakeLists.txt `、` compositor/src/modules/window-management/windowmanagementinterfacev1.cpp `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/tests/CMakeLists.txt `、` compositor/tests/protocols/CMakeLists.txt `、` compositor/tests/protocols/INDEX.md `、` compositor/tests/protocols/treeland-show-desktop-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-window-management-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-show-desktop-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-window-management-desktop-v1/treeland-window-management-desktop-v1.c `、` compositor/tests/protocols/treeland-show-desktop-desktop-v1/treeland-show-desktop-desktop-v1.c `、` compositor/tests/protocols/treeland-window-management-desktop-v1/treeland-window-management-desktop-v1.h `、` compositor/tests/protocols/treeland-show-desktop-desktop-v1/treeland-show-desktop-desktop-v1.h `、` compositor/tests/protocols/treeland-show-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-window-management-v1/README.md `、` compositor/tests/protocols/treeland-show-desktop-v1/README.md `、` compositor/tests/protocols/treeland-show-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-window-management-v1/treeland-window-management-v1.c `、` compositor/tests/protocols/treeland-show-desktop-v1/treeland-show-desktop-v1.c `、` compositor/tests/protocols/treeland-window-management-v1/treeland-window-management-v1.h `、` compositor/tests/protocols/treeland-show-desktop-v1/treeland-show-desktop-v1.h `、` compositor/tests/protocols/treeland-window-management-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-window-management-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-window-management-v1/setup.cpp `、` compositor/tests/test_protocol_show-desktop/CMakeLists.txt `、` compositor/tests/test_protocol_window-management/main.cpp `、` compositor/tests/test_protocol_show-desktop/main.cpp `、` compositor/tests/test_protocol_window-management/CMakeLists.txt `。
- 实际改变：` compositor/.agents/skills/treeland-debug/SKILL.md `、` compositor/examples/test_show_desktop/CMakeLists.txt `、` compositor/examples/test_show_desktop/main.cpp `、` compositor/src/core/shellhandler.cpp `、` compositor/src/modules/CMakeLists.txt `、` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv1.cpp `、` compositor/src/modules/shortcut/shortcutrunner.cpp `、` compositor/src/modules/show-desktop/CMakeLists.txt `、` compositor/src/modules/show-desktop/showdesktopinterfacev1.cpp `、` compositor/src/modules/show-desktop/showdesktopinterfacev1.h `、` compositor/src/modules/window-management/CMakeLists.txt `、` compositor/src/modules/window-management/windowmanagementinterfacev1.cpp `、` compositor/src/modules/window-management/windowmanagementinterfacev1.h `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/tests/CMakeLists.txt `、` compositor/tests/protocols/CMakeLists.txt `、` compositor/tests/protocols/INDEX.md `、` compositor/tests/protocols/treeland-show-desktop-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-show-desktop-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-show-desktop-desktop-v1/treeland-show-desktop-desktop-v1.c `、` compositor/tests/protocols/treeland-show-desktop-desktop-v1/treeland-show-desktop-desktop-v1.h `、` compositor/tests/protocols/treeland-show-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-show-desktop-v1/README.md `、` compositor/tests/protocols/treeland-show-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-show-desktop-v1/treeland-show-desktop-v1.c `、` compositor/tests/protocols/treeland-show-desktop-v1/treeland-show-desktop-v1.h `、` compositor/tests/protocols/treeland-window-management-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-window-management-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-window-management-desktop-v1/treeland-window-management-desktop-v1.c `、` compositor/tests/protocols/treeland-window-management-desktop-v1/treeland-window-management-desktop-v1.h `、` compositor/tests/protocols/treeland-window-management-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-window-management-v1/README.md `、` compositor/tests/protocols/treeland-window-management-v1/setup.cpp `、` compositor/tests/protocols/treeland-window-management-v1/treeland-window-management-v1.c `、` compositor/tests/protocols/treeland-window-management-v1/treeland-window-management-v1.h `、` compositor/tests/test_protocol_show-desktop/CMakeLists.txt `、` compositor/tests/test_protocol_show-desktop/main.cpp `、` compositor/tests/test_protocol_window-management/CMakeLists.txt `、` compositor/tests/test_protocol_window-management/main.cpp `、` protocols/compositor/CMakeLists.txt `、` protocols/compositor/xml/treeland-show-desktop-unstable-v1.xml `、` protocols/compositor/xml/treeland-window-management-v1.xml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 1f37c019972da79aa624947a1cdcc3c97f625559 ` → ` 1f37c019972da79aa624947a1cdcc3c97f625559 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/parent-evidence.json`；以来源 ` 5023ac25718db141361d66018746e66bd8e56bc6 ` 和原目标 ` 1663c425c3c639f8a3f98bf3808670f9c4ef40d8 ` 查询。
- 原审核说明：` 按来源差异进行三方合并，保留相邻本地树的构建名、受控协议目录及已有条件；新增/移动文件使用规范映射路径。协议额外路径仅按 PRD §5.3.1 精确迁移。show-desktop 测试替代 window-management 后，继续保留本地 compositor/src 私有 include 路径；不改变 libdeckcompositor 公共 include 合同。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/1663c425c3c639f8a3f98bf3808670f9c4ef40d8.md)。

<a id="entry-42"></a>
### 42. N8b / ` feat(foreign-toplevel): adapt to treeland-foreign-toplevel-manager v2 `

- 本仓内容路径：` compositor/src/core/qml/DockPreview.qml `、` compositor/src/core/shellhandler.cpp `、` compositor/src/core/shellhandler.h `、` compositor/src/modules/foreign-toplevel/CMakeLists.txt `、` compositor/src/modules/foreign-toplevel/dockpreviewcontextv1.h `、` compositor/src/modules/foreign-toplevel/dockpreviewcontextv2.h `、` compositor/src/modules/foreign-toplevel/foreigntoplevelhandlev1.h `、` compositor/src/modules/foreign-toplevel/foreigntoplevelhandlev2.h `、` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv1.cpp `、` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv2.cpp `、` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv1.h `、` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv2.h `、` compositor/src/seat/helper.h `、` compositor/tests/protocols/CMakeLists.txt `、` compositor/tests/protocols/INDEX.md `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/README.md `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v2/README.md `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/setup.cpp `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v2/setup.cpp `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/treeland-foreign-toplevel-manager-v1.c `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v2/treeland-foreign-toplevel-manager-v2.c `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/treeland-foreign-toplevel-manager-v1.h `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v2/treeland-foreign-toplevel-manager-v2.h `。
- 实际改变：` compositor/src/core/qml/DockPreview.qml `、` compositor/src/core/shellhandler.cpp `、` compositor/src/core/shellhandler.h `、` compositor/src/modules/foreign-toplevel/CMakeLists.txt `、` compositor/src/modules/foreign-toplevel/dockpreviewcontextv1.h `、` compositor/src/modules/foreign-toplevel/dockpreviewcontextv2.h `、` compositor/src/modules/foreign-toplevel/foreigntoplevelhandlev1.h `、` compositor/src/modules/foreign-toplevel/foreigntoplevelhandlev2.h `、` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv1.cpp `、` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv1.h `、` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv2.cpp `、` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv2.h `、` compositor/src/seat/helper.h `、` compositor/tests/protocols/CMakeLists.txt `、` compositor/tests/protocols/INDEX.md `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/README.md `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/setup.cpp `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/treeland-foreign-toplevel-manager-v1.c `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/treeland-foreign-toplevel-manager-v1.h `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v2/README.md `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v2/setup.cpp `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v2/treeland-foreign-toplevel-manager-v2.c `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v2/treeland-foreign-toplevel-manager-v2.h `、` compositor/tests/test_protocol_foreign-toplevel/CMakeLists.txt `、` compositor/tests/test_protocol_foreign-toplevel/main.cpp `、` protocols/compositor/CMakeLists.txt `、` protocols/compositor/xml/treeland-foreign-toplevel-manager-unstable-v2.xml `、` protocols/compositor/xml/treeland-foreign-toplevel-manager-v1.xml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 1f37c019972da79aa624947a1cdcc3c97f625559 ` → ` 1f37c019972da79aa624947a1cdcc3c97f625559 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/parent-evidence.json`；以来源 ` 2f5bb78f3e8b5fc73b7cf1f4a8ea09c38a946339 ` 和原目标 ` ee6b6472609d03d754d76f699006209260ec6aaf ` 查询。
- 原审核说明：` 按来源差异进行三方合并，保留相邻本地树的构建名、受控协议目录及已有条件；新增/移动文件使用规范映射路径。协议额外路径仅按 PRD §5.3.1 精确迁移。2026-09-27 用户精确批准 XML 07d336875741f08d73001fa2409b2c2ed621dc26；保留拒绝重复 dock context 的行为，公告版本按 XML 为 1，增加真实客户端重复请求的 error=1 及 destroy 后重建回归；激活用例先清除并确认停用和失焦前提，再由真实协议请求验证状态转移，保留 wire activated=2、产品激活与焦点断言，不要求幂等请求重复发事件。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/ee6b6472609d03d754d76f699006209260ec6aaf.md)。

<a id="entry-43"></a>
### 43. N8b / ` fix: preserve output identity in frame callbacks `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/qtquick/woutputrenderwindow.cpp `、` waylib/tests/unit_tests/CMakeLists.txt `、` waylib/tests/unit_tests/test_output_frame/CMakeLists.txt `、` waylib/tests/unit_tests/test_output_frame/main.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 1f37c019972da79aa624947a1cdcc3c97f625559 ` → ` c8d083592f3c149bc81dd63476a47deae9a10168 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/parent-evidence.json`；以来源 ` b9759c0c68ac278ed1f7c6444e59f14e7743abb4 ` 和原目标 ` 0060010150ceb7dbe6331f52156b446bc82862eb ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` c8d083592f3c149bc81dd63476a47deae9a10168 `；跨仓定位 ` docs/treeland-sync/20260922_treeland_0_9_1_to_0_10_0_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-44"></a>
### 44. N8b / ` chore: bump version to 0.10.0 `

- 本仓内容路径：` compositor/CMakeLists.txt `、` compositor/debian/changelog `、` compositor/debian/control `。
- 实际改变：` compositor/CMakeLists.txt `、` compositor/debian/changelog `、` compositor/debian/control `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` c8d083592f3c149bc81dd63476a47deae9a10168 ` → ` c8d083592f3c149bc81dd63476a47deae9a10168 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/parent-evidence.json`；以来源 ` 3a100f265970cb6acf9addf07e5c297aab9e9839 ` 和原目标 ` 375e1bb98daef4d3b50b0a4a40d8127bd761a73a ` 查询。
- 原审核说明：` 按来源差异进行三方合并，保留相邻本地树的构建名、受控协议目录及已有条件；新增/移动文件使用规范映射路径。协议额外路径仅按 PRD §5.3.1 精确迁移。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/375e1bb98daef4d3b50b0a4a40d8127bd761a73a.md)。

<a id="entry-45"></a>
### 45. N8b / chore(protocol): 同步 remote-subsurface 配套快照

- 独立类型：protocol-companion；不计为普通来源回放。
- [逐路径增量及原依据](adaptations/bee3531566e9d325e8d89db1ad124759033d7bc2.md)。

## 节点验证与历史边界

### N8a / 原节点验收

- 原报告状态：**pass**。
- 来源验收终点：` a5656ab80ae11a0068d507659f35bb999b6d815d `；普通中间提交不作构建承诺。
- 原候选 P / DeckShell：` cb9c6bf6bbc4a53bc50212204f34ad0cd5308ffb `。
- 原候选 C / waylib-shared：` a2b1c5752afca1581a95a8bd8ac6d3dbe115b8e4 `。
- 原候选 R / wlroots：` 005b8c571c002d266ffdd560b7eb4e3bd46c4e3a `。
- 原报告：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/sync-report-authorized.json`。
- 原报告状态：BLOCKED；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/sync-report.json`；原字节保留。
- 原接受收口：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/closeout-journal.json`
- 限定授权：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/drm-skip-authorization.json`
- 授权仅属 ` 20260922_treeland_0_9_1_to_0_10_0_local_sync ` / ` N8a `：` {'source_head': 'a5656ab80ae11a0068d507659f35bb999b6d815d', 'upstream_test_commit': '8bfa446c589f06d4f427a39b93a585a2406f5cdb', 'validation_id': 'deckshell-compositor-ctest', 'validation_attempt': 2, 'allowed_skips': ['test_drm']} `。
- 原验证 FAIL/SKIP 保持原样；按该节点原授权接受唯一限定跳过，不证明 DRM/GPU 行为通过，不外推到其它节点或未来批次。
- deckshell_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/deckshell-verify.json`。
- waylib_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/waylib-verify.json`。
- wlroots_verify：pass / verified；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/wlroots-verify.json`。
- gitlink_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/gitlink-verify.json`。
- nested_gitlink_verify：pass / verified；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/nested-gitlink-verify.json`。
- protocol_tracking：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/protocol-candidates.json`。
- contract_audit：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/waylib-contract-audit.json`。
- child_materialization：pass / created；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/child-materialization.json`。
- protocol_pairing：pass / paired；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/protocol-pairing.json`。

| 原验证项 | 结果 | 退出码 | 原测试计数 | 原始日志 |
|---|---|---|---|---|
| ` waylib-base-build ` / attempt 2 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/waylib-base-build-attempt-2.log` |
| ` waylib-candidate-build ` / attempt 2 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/waylib-candidate-build-attempt-2.log` |
| ` waylib-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/waylib-base-configure-attempt-1.log` |
| ` waylib-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/waylib-base-install-attempt-1.log` |
| ` waylib-base-ctest ` / attempt 1 | PASS | 0 | ` {'total': 11, 'passed': 11, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/waylib-base-ctest-attempt-1.log` |
| ` waylib-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/waylib-candidate-configure-attempt-1.log` |
| ` waylib-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/waylib-candidate-install-attempt-1.log` |
| ` waylib-ctest ` / attempt 1 | PASS | 0 | ` {'total': 11, 'passed': 11, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/waylib-ctest-attempt-1.log` |
| ` wlroots-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/wlroots-base-configure-attempt-1.log` |
| ` wlroots-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/wlroots-base-build-attempt-1.log` |
| ` wlroots-base-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/wlroots-base-test-attempt-1.log` |
| ` wlroots-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/wlroots-candidate-configure-attempt-1.log` |
| ` wlroots-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/wlroots-candidate-build-attempt-1.log` |
| ` wlroots-candidate-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/wlroots-candidate-test-attempt-1.log` |
| ` waylib-package-consumer-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/waylib-package-consumer-configure-attempt-1.log` |
| ` waylib-package-consumer-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/waylib-package-consumer-build-attempt-1.log` |
| ` waylib-package-consumer ` / attempt 1 | PASS | 0 | ` {'total': 9, 'passed': 9, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/waylib-package-consumer-attempt-1.log` |
| ` deckshell-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/deckshell-configure-attempt-1.log` |
| ` deckshell-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/deckshell-build-attempt-1.log` |
| ` deckshell-compositor-ctest ` / attempt 2 | FAIL | 0 | ` {'total': 66, 'passed': 65, 'failed': 0, 'skipped': 1} ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8a-attempt-8/logs/deckshell-compositor-ctest-attempt-2.log` |

以上状态属于原候选；未替换成整理后 SHA，也未因本次生成而重新通过。

### N8b / 原节点验收

- 原报告状态：**pass**。
- 来源验收终点：` 3a100f265970cb6acf9addf07e5c297aab9e9839 `；普通中间提交不作构建承诺。
- 原候选 P / DeckShell：` bee3531566e9d325e8d89db1ad124759033d7bc2 `。
- 原候选 C / waylib-shared：` d0344634c057b8c29ac2e138a935e5c80a89b768 `。
- 原候选 R / wlroots：` 005b8c571c002d266ffdd560b7eb4e3bd46c4e3a `。
- 原报告：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/sync-report.json`。
- 原接受收口：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/closeout-journal.json`
- 其他报告版本：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/sync-report-final.json`；未被该次 closeout 绑定，不替代原接受报告，也不表示重新收口。
- 限定授权：外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/drm-skip-authorization.json`
- 授权仅属 ` 20260922_treeland_0_9_1_to_0_10_0_local_sync ` / ` N8b `：` {'source_head': '3a100f265970cb6acf9addf07e5c297aab9e9839', 'upstream_test_commit': '8bfa446c589f06d4f427a39b93a585a2406f5cdb', 'validation_id': 'deckshell-compositor-ctest', 'validation_attempt': 1, 'allowed_skips': ['test_drm']} `。
- 原验证 FAIL/SKIP 保持原样；按该节点原授权接受唯一限定跳过，不证明 DRM/GPU 行为通过，不外推到其它节点或未来批次。
- deckshell_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/deckshell-verify.json`。
- waylib_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/waylib-verify.json`。
- wlroots_verify：pass / verified；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/wlroots-verify.json`。
- gitlink_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/gitlink-verify.json`。
- nested_gitlink_verify：pass / verified；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/nested-gitlink-verify.json`。
- protocol_tracking：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/protocol-candidates.json`。
- contract_audit：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/waylib-contract-audit.json`。
- child_materialization：pass / created；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/child-materialization.json`。
- protocol_pairing：pass / paired；外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/protocol-pairing.json`。

| 原验证项 | 结果 | 退出码 | 原测试计数 | 原始日志 |
|---|---|---|---|---|
| ` waylib-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/waylib-candidate-configure-attempt-1.log` |
| ` waylib-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/waylib-candidate-build-attempt-1.log` |
| ` waylib-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/waylib-candidate-install-attempt-1.log` |
| ` waylib-ctest ` / attempt 1 | PASS | 0 | ` {'total': 12, 'passed': 12, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/waylib-ctest-attempt-1.log` |
| ` waylib-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/waylib-base-configure-attempt-1.log` |
| ` waylib-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/waylib-base-build-attempt-1.log` |
| ` waylib-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/waylib-base-install-attempt-1.log` |
| ` waylib-base-ctest ` / attempt 1 | PASS | 0 | ` {'total': 11, 'passed': 11, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/waylib-base-ctest-attempt-1.log` |
| ` waylib-package-consumer-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/waylib-package-consumer-configure-attempt-1.log` |
| ` waylib-package-consumer-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/waylib-package-consumer-build-attempt-1.log` |
| ` waylib-package-consumer ` / attempt 1 | PASS | 0 | ` {'total': 9, 'passed': 9, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/waylib-package-consumer-attempt-1.log` |
| ` wlroots-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/wlroots-base-configure-attempt-1.log` |
| ` wlroots-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/wlroots-base-build-attempt-1.log` |
| ` wlroots-base-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/wlroots-base-test-attempt-1.log` |
| ` wlroots-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/wlroots-candidate-configure-attempt-1.log` |
| ` wlroots-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/wlroots-candidate-build-attempt-1.log` |
| ` wlroots-candidate-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/wlroots-candidate-test-attempt-1.log` |
| ` deckshell-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/deckshell-configure-attempt-1.log` |
| ` deckshell-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/deckshell-build-attempt-1.log` |
| ` deckshell-compositor-ctest ` / attempt 1 | FAIL | 0 | ` {'total': 66, 'passed': 65, 'failed': 0, 'skipped': 1} ` | 外层历史资料：`.helloagents/plans/20260922_treeland_0_9_1_to_0_10_0_local_sync/evidence/N8b-attempt-8/logs/deckshell-compositor-ctest-attempt-1.log` |

以上状态属于原候选；未替换成整理后 SHA，也未因本次生成而重新通过。
