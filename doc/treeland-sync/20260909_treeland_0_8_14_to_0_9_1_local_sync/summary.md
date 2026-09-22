# P / DeckShell 同步记录：20260909_treeland_0_8_14_to_0_9_1_local_sync

这是按仓归属生成的同步事实记录，不是新的产品验收报告。
原节点结果只绑定下文列出的原候选与原环境；本次生成未执行同步、构建、测试、收口或远端发布。

- 来源范围（左开右闭）：` 7da2254d386935f753ed907f8d6e76c1639d01a9 ` → ` fd573cf44fb06ee1eebcdd8c39716d1c797b64d4 `。
- 本仓内容基线：` 4e5d37c144edee006a7ff2598c243f0f9715b979 `。
- 本仓内容终点：` d76ef0a531100d18bfb966c33531e28e03b838fe `；不含后继文档、URL/gitlink 或工具维护提交。
- 本仓普通目标：**501**；独立初始化：**1**；合计 **502**。
- 普通 action：{'applied': 90, 'empty': 2, 'adapted': 52, 'gitlink-only': 357}。
- 原同步内容基线/终点：` 4e5d37c144edee006a7ff2598c243f0f9715b979 ` → ` bf1092f11da49ffe4cdaacf148dab7f60d02198d `。
- 三类身份严格区分：Treeland 来源不变；原目标由旧证据验收；整理后目标由旧新映射及 Git 对象对应。
- 生成时已逐目标核对来源、映射顺序、普通文件不变及派生 gitlink；这不是产品重新验收。
- 原需求与实施记录：[PRD](prd.md)、[plan](plan.md)。
- 外层历史资料仅用标识和相对定位列出，不是本仓链接；记录不包含完整日志、构建树或安装树。
- R 的短 Refs 是 P/C 共同方案标识，不承诺 R 仓内存在方案副本。

## 有序提交映射

| 序号 / 节点 | Treeland 来源 | 原目标 | 本仓目标 | action（C 另列 content_action） | 归属 |
|---|---|---|---|---|---|
| 1 / N1 | ` 2eabcfb98d49d520b96c9f2cd2ea517a6fa91719 ` | ` 3eceaef344dedab8431ca88a6d1cf5e89cd9eb98 ` | ` 0d60ea0549fa07d233c57cc8047a0e5191ee57bc ` [条目](#entry-1) | applied | deckshell-only |
| 2 / N1 | ` aa362eedfd17db30e9737a008f8386ba87098a71 ` | ` a85c4c48029b950f28713fbae8a1e1b573f3dcd2 ` | ` 36c42602c3b6a533a86eb43d45dbe3b9a807509f ` [条目](#entry-2) | applied | deckshell-only |
| 3 / N1 | ` 506ece05ff4a8cdfd17732dfcc8432a7a1e90091 ` | ` a9e6e19818d9f05ee1c86f06c0e095a04065f2d7 ` | ` 2f99a098ae2ed459a754b76dfacae08e1f43db51 ` [条目](#entry-3) | applied | deckshell-only |
| 4 / N1 | ` 467f0dfd7d0fc94689c282d72f554b86c9781f28 ` | ` b6cf8fbddd147660a6a52cee1157801ec5fab719 ` | ` ca4c8bd2538cd1a3882dd8d8937ab377aaf2a858 ` [条目](#entry-4) | applied | deckshell-only |
| 5 / N1 | ` 1f025a9ba3784f4ac36a5d9d6402b4031585dde4 ` | ` 145028fdc2538f0cc53f5d6ba3b3916f1ad2f06f ` | ` 1b8771b7cdf3118a589940642cfb918f87f310bf ` [条目](#entry-5) | applied | deckshell-only |
| 6 / N1 | ` 0050d87e38b4be8fa4addac6c4c94debf05a6594 ` | ` b8758ce1b1a00fddf9faf141afc212b60d1e6899 ` | ` 4dbd0c5fa6ccf8248bc50967680a59a4ac09e98e ` [条目](#entry-6) | applied | deckshell-only |
| 7 / N1 | ` ed9ae1a22c69d70fe3e09e048678f5a587d52418 ` | ` efde569b6e72f291f0c9ff0b5daa6df80f8bc76b ` | ` 05c0b85e16c3839149fb72e9a1e1d8936486b802 ` [条目](#entry-7) | applied | deckshell-only |
| 8 / N1 | ` 5398e81caf1cefc335a713b4be1085a5fadbe98e ` | ` b0eba486798c847685b7e72130d9cc8bb3bb7f3f ` | ` 9ed2cfb00c6064a3be7253ce1b65c5e72d9a75b7 ` [条目](#entry-8) | empty | deckshell-only |
| 9 / N1 | ` dc245f5fa59e490ec79ce629e0fccf6662fc26a9 ` | ` a1af95b4f80b98205c466f2fc2462afde8d7cd40 ` | ` 1b5dc5f31fdf23aa8627972c73d23fe4c7c0f03c ` [适配详情](adaptations/1b5dc5f31fdf23aa8627972c73d23fe4c7c0f03c.md) | adapted | deckshell-only |
| 10 / N1 | ` bf058f1d9f59471cf8c4500a519048842a0dcace ` | ` dee1db68a6a7b3094f17f14ac5bd08140bc133f8 ` | ` 6e0e14dc5cd97e82406f89311700043fd768295f ` [适配详情](adaptations/6e0e14dc5cd97e82406f89311700043fd768295f.md) | adapted | deckshell-only |
| 11 / N1 | ` 09a8d72c9bda873b2696139c55132eb7c5ab41d2 ` | ` 3cb6be9084ee2e4fea5f67a1f443360f654708c5 ` | ` 77372236f8ae3b1481463ffeac6fff6f1e37a961 ` [条目](#entry-11) | applied | deckshell-only |
| 12 / N1 | ` a00bd19c76b4c8cee2f9491883a3d845d002d6b1 ` | ` b771382ed8bd8364edbe6a430fe6f9eef2aa14b2 ` | ` ccc53299352eae97b11c0a06d5bb5ce29ec534ad ` [适配详情](adaptations/ccc53299352eae97b11c0a06d5bb5ce29ec534ad.md) | adapted | deckshell-only |
| 13 / N1 | ` c8c69c9f679cac1e22ed2e32e74c9f3df5b60d56 ` | ` 0166846131eebabc3519383cd1b27c3753040411 ` | ` c9f77774cb3ba9d5b770fbe400b1e25e20300317 ` [条目](#entry-13) | applied | deckshell-only |
| 14 / N1 | ` c223a631ade7662aae09c132f575be23d63460b9 ` | ` 21794db17b8a1e59215998fe9357600193181a7c ` | ` 8fab44dd3bf585d15ceb1b23fc1408b471fe11c3 ` [适配详情](adaptations/8fab44dd3bf585d15ceb1b23fc1408b471fe11c3.md) | adapted | deckshell-only |
| 15 / N1 | ` 919986c388ba5b5f1e4e7d6a761f028e6a3fb5be ` | ` 0f4195972ec7f1aff138508e5102244759a9c66f ` | ` 998f20402ffbee0e799503c52fc4b51a863d8ff6 ` [适配详情](adaptations/998f20402ffbee0e799503c52fc4b51a863d8ff6.md) | adapted | deckshell-only |
| 16 / N1 | ` 55fb88aa91f152fa4837ee469a8299179bee5ecc ` | ` 8527f55266135710a6b6c8a9a7d5d489efd4bace ` | ` 70c7aa6094de87123e114d5b8f660e79ca3ebdca ` [条目](#entry-16) | applied | deckshell-only |
| 17 / N1 | ` 868a0fcee2919031c5b50d06d7258c19d2ca1103 ` | ` cdeeb1d76d8bd1840a3e3bee39ec7acc25f68147 ` | ` a1fa19f6c430573f58374019b184d7d6ce91779c ` [条目](#entry-17) | applied | deckshell-only |
| 18 / N1 | ` 3eeb8956884cb9eb759ff81107a60cfa7841e756 ` | ` 5c14d1083fc804f45c400a372d5cf5a40315ec73 ` | ` c56fa0d842eb03204827a7e6369bb97392207fc5 ` [条目](#entry-18) | gitlink-only | waylib-only |
| 19 / N1 | ` 0e2a8e1dd2c31d87fd67fc86ca5a7e6596d5f157 ` | ` 86b8fd0b23b3e70d8ed08aa168453165971731c1 ` | ` 57002bfe37a17ab11e9279253343324419a5f7c1 ` [适配详情](adaptations/57002bfe37a17ab11e9279253343324419a5f7c1.md) | adapted | deckshell-only |
| 20 / N1 | ` d2de8c2fc730637ae37aca693235c63168ddbf58 ` | ` 3c69a74019ec9257c95df68ccbf2329284f383d1 ` | ` 91f99b31b1e29cec4ed8fdb3958ed0359577faa7 ` [条目](#entry-20) | applied | deckshell-only |
| 21 / N1 | ` 53637fd5388bdb5e71f4644303afe84cdbe6483b ` | ` 4af8a96329f2782514962dbe2f8a2b179adb671f ` | ` d589dd41c7b7245776186e6050b2817654290ac3 ` [条目](#entry-21) | applied | deckshell-only |
| 22 / N1 | ` 8f387a5b4d94fc1590548f51979a7ac718689c73 ` | ` dc1e7c311ff660c04e500e4e70171f78c8d342ff ` | ` 9d735bc5fd17019cc1d53af9eba0d919c5789922 ` [条目](#entry-22) | applied | deckshell-only |
| 23 / N1 | ` 4410a4d8201987eed9d6e1fd3791f19ee0ac6c89 ` | ` 888fd1a0a97e288283833c343fd81d8281eefc6e ` | ` 4f13127f5af15bbeb3ac06b7162681c0e568931b ` [适配详情](adaptations/4f13127f5af15bbeb3ac06b7162681c0e568931b.md) | adapted | deckshell-only |
| 24 / N1 | ` 997937396a22fc6b3729b124343271e4202df044 ` | ` 5d42e8135aebf98859cebf013c0bd8be5e2d27b4 ` | ` d531aa1a39482412f90b35feb101e281ccdd8518 ` [条目](#entry-24) | applied | deckshell-only |
| 25 / N1 | ` 250a4889fd74676bb23b74c245b0ef77c0467778 ` | ` 263b90392e5b14bc21487c664290d9bc9dc0f64f ` | ` 1526611c44afad3d729f7fb90ce030e08455b6e4 ` [条目](#entry-25) | applied | deckshell-only |
| 26 / N1 | ` 1f8416145ca848d9affdccae3a9aa35c23f0c883 ` | ` 04983aa6b262472459cb0ab00f654d87a11bf84f ` | ` fbfe8bb9407007cbccdbb7fb5452633661c94a3c ` [适配详情](adaptations/fbfe8bb9407007cbccdbb7fb5452633661c94a3c.md) | adapted | deckshell-only |
| 27 / N1 | ` ea290441942f04bada1ba8fda7897b12cf26b158 ` | ` 4f8af2f049888b30f991d26cbbe18ff89bdfc604 ` | ` 1bebf60167bb49dab050e960e2ad091974450cfc ` [条目](#entry-27) | applied | deckshell-only |
| 28 / N1 | ` 2df4c21c0499b46229f1ef0080cc265994b4fd60 ` | ` 055be261d35138ec678b3a7aaf1521bfc2d9a05e ` | ` aab728dd63010fd3004aa04ddf283ddb704d302a ` [适配详情](adaptations/aab728dd63010fd3004aa04ddf283ddb704d302a.md) | adapted | deckshell-only |
| 29 / N2 | ` 1ffe0010193a8c696ef6436a4c436f57bbb1e8ec ` | ` 4071efb9caf5adc60d236f41c9ca1bbfb49f8c10 ` | ` e1b74b4a9bc49a373edf883ee24ab55023d3412d ` [条目](#entry-29) | initialization | 独立初始化 |
| 30 / N3 | ` 896a8953e3695577e05e9e93d10530920dc7d6d9 ` | ` 1fb372d2deb909815b26a58ffcc0311b50b7481c ` | ` 26804e427f757e0185dc95e699d57f880045ec65 ` [适配详情](adaptations/26804e427f757e0185dc95e699d57f880045ec65.md) | adapted | dual |
| 31 / N3 | ` 719523d3c31281c47991cf5e73c93d839aa44398 ` | ` 1c2b1392fad8091d2454eddb1c2986614d0db510 ` | ` ab808b066e50c74b02d162c7ba3546e8dbe16809 ` [条目](#entry-31) | applied | deckshell-only |
| 32 / N3 | ` a4beeb367b4451fa36fc52accee720d807341364 ` | ` 22e870cff432c0d4c0278f412308ac6ee59aba39 ` | ` ef863a85b3046941b067ecec6f829222c67d6adf ` [适配详情](adaptations/ef863a85b3046941b067ecec6f829222c67d6adf.md) | adapted | deckshell-only |
| 33 / N3 | ` 4dbcf637cfccb6d2814b05e5e777e37031623f71 ` | ` fef857ebd2377692d1f1b50210b1c54976008486 ` | ` 10d67d92ef3b0b1eb8ac26fba0aeff03fd641435 ` [条目](#entry-33) | applied | deckshell-only |
| 34 / N3 | ` ca8a95ff333080d56bbc3b9895966160f1c96071 ` | ` d79286b5db3e20964340db4edcafbd8d3bd71e3d ` | ` 49bd45a4ec0901f65d0eedd9cb9246d8dbc3aa3b ` [条目](#entry-34) | applied | deckshell-only |
| 35 / N3 | ` aac67eea93c777558d41903c7a37f360ec0fbe81 ` | ` 2429fe320875bf811580322582e2c0b638651929 ` | ` be239e909ce177626ad613ed819ca08115755f4a ` [条目](#entry-35) | gitlink-only | waylib-only |
| 36 / N3 | ` 8a3e65490a7380fdd168fdac4d92634445816014 ` | ` aeeab25755ec7b82367559759bca2bc63931a052 ` | ` 7883a832d29950c3b13caf48d9cac5702ae31038 ` [条目](#entry-36) | applied | deckshell-only |
| 37 / N3 | ` ff0aa9861d0d71b723da86483d0571b4aa1beab3 ` | ` 9bc70b772c698a8d9c215b8543dc3960ab269f9a ` | ` 5f95519c1c6372d4352f564fe42b3ff0715c3a2f ` [条目](#entry-37) | applied | dual |
| 38 / N3 | ` 0d008c38411bb097ab66cc78a1593ea985dd6a06 ` | ` 60300fc3271ad5af489370a96b1bd4c5d52777c2 ` | ` 42c438e244443ef53fe11b1fc29669f411a4a4f6 ` [条目](#entry-38) | gitlink-only | waylib-only |
| 39 / N3 | ` 25258137413e911c9ef21b76dab49c1a43b192a8 ` | ` 8adafa80d63494fe533aeff2010f84dc706274e0 ` | ` 564dfe1d9f7362ffc3f83c376b51339923a84bcd ` [条目](#entry-39) | applied | deckshell-only |
| 40 / N3 | ` d3d186b30d2d0dc41f4b53ce106bdc4d5f007513 ` | ` f98f940f915b2526c5f5d210be501d04d64eda21 ` | ` 9da1b51d0207b4f57bd4dd45d9e8af37c97bc066 ` [条目](#entry-40) | applied | deckshell-only |
| 41 / N3 | ` 5a90432efb33646a8d1e92ce2c5901e0dcb7fc04 ` | ` 08922d0411ff55d471df1374475f5978cd26a5f5 ` | ` e40c04aa9f3db51e408c37421901341169860186 ` [适配详情](adaptations/e40c04aa9f3db51e408c37421901341169860186.md) | adapted | dual |
| 42 / N3 | ` 4e21f708be59d24f4aac55bcdc3964a800feb74c ` | ` a93a699c0c49f7c50ae9bac088792de6152574a9 ` | ` 8200c899f854b92e643dae7134771be7e563ae5e ` [适配详情](adaptations/8200c899f854b92e643dae7134771be7e563ae5e.md) | adapted | dual |
| 43 / N3 | ` 268ca973be0d5eeb33d6be03b5e51e4ce62f4997 ` | ` 939f7acabeaca39c0dfccf8b2568f8c79b57758f ` | ` 5f58534233351c8ce506c055726e46fe7e59b4c7 ` [适配详情](adaptations/5f58534233351c8ce506c055726e46fe7e59b4c7.md) | adapted | dual |
| 44 / N3 | ` 34049a416fb66f7c6c8ab73dbda3e42e9c59f309 ` | ` 0c438ce5dd97d84f35deaa62584edbcd501f0ffd ` | ` bcb590e170012289b985f5334316a6bdd1c4d773 ` [适配详情](adaptations/bcb590e170012289b985f5334316a6bdd1c4d773.md) | adapted | dual |
| 45 / N3 | ` 7228321461027bb935a08593d8d1363a14ddcbdb ` | ` f44b2435b906db13175c43a86dfbbbca7a0905bf ` | ` f57ec828baeb24c364f8dc3ffca26a3799a4a619 ` [条目](#entry-45) | applied | deckshell-only |
| 46 / N3 | ` 649d00ca053b4085520fdda3d4271973d258bf22 ` | ` 4acc3fd146d0a36fd5094eb2f95f288150dcf8ae ` | ` 02d194ecf5fb8fab5e781224d083ac30e661d498 ` [条目](#entry-46) | applied | deckshell-only |
| 47 / N3 | ` 93777bf5546bba1a4d106fe1da44a6a0d4811845 ` | ` c6f031ff080fca9e0762776231472ce3f2fb6eda ` | ` 147e42766ba5673907872192e53c0e11de48d5ae ` [条目](#entry-47) | applied | deckshell-only |
| 48 / N3 | ` ae0648cf38e2a9ce6cf62dd8f281b75ff91dd553 ` | ` dd0e75c9b6e1009de549ae25bd48ac5f5274630d ` | ` 6e3899c7be4ae832a6310e7b597c97595a47ff16 ` [条目](#entry-48) | applied | deckshell-only |
| 49 / N3 | ` 25cb8dd422d381b64f18f535a51066c85d80818b ` | ` 53e4aeacddc45f1923bba37fc1fe7f3c53d52919 ` | ` b2e5001951b1c9456a74d3447154a374ac3d270d ` [条目](#entry-49) | gitlink-only | waylib-only |
| 50 / N3 | ` 4db6917f873990966f58578abe7dca8b8b371d36 ` | ` dc4f7d20294b8b6fa9decc39a783bf504246f34e ` | ` 322a731543791a78d4e7ac485468c22409f309bf ` [适配详情](adaptations/322a731543791a78d4e7ac485468c22409f309bf.md) | adapted | deckshell-only |
| 51 / N4 | ` 57aeaea3b99ef70cd6a1f3edba13e245ce58cd5d ` | ` bb89b79e2524df37bb508cbf2f243c0d0fb1db25 ` | ` b25300e8fa60bc16731ebb1c5c2bf8a16ee8a259 ` [条目](#entry-51) | applied | deckshell-only |
| 52 / N4 | ` d4e547c9f0094626689b5db8e95db0da49164b50 ` | ` 67b5d6b215a588213e196760f862af0a166c4c69 ` | ` f44914538e7facf862af0d35c21b6f41889a0f98 ` [条目](#entry-52) | gitlink-only | waylib-only |
| 53 / N4 | ` 48da5274244c1a78f3130b321f1d70f9a53e10e2 ` | ` b411ecb5c43efd4b359e4352d0725a2464518f48 ` | ` c36b18d37e00d5a91726c91118c398f4995ec84d ` [条目](#entry-53) | applied | deckshell-only |
| 54 / N4 | ` 97bfdf2a44975ba53f5f417b661f596fa76a30bd ` | ` d64dab08dab9c84dbfea4998fce212cfc5b519cb ` | ` d90847a29bea9d030b9bc6eae825b01ea0fc0e4a ` [条目](#entry-54) | applied | deckshell-only |
| 55 / N4 | ` 1f5d35eadc6ce02d708a7edadba97a56bf2a7883 ` | ` 6ce8fe0c1a91c4617d88818256ec5191c6e6581f ` | ` 957cefa6b47620adce0985efa6c689a680685779 ` [条目](#entry-55) | gitlink-only | waylib-only |
| 56 / N4 | ` 57fe3c71cafcefca1b2e419e3a008f1ebc0be38c ` | ` 775e7c8661f23f1d9e84a1e585147444ed9eda74 ` | ` b76493b280334371cb8485b8369309b017609b38 ` [条目](#entry-56) | gitlink-only | waylib-only |
| 57 / N4 | ` 00f6f3a6994a086a4b919f30558b14019fbb5c55 ` | ` 646dfdda45fcfe3fe821fe91641b6daa1a67074b ` | ` e60fbe02d29796a9aae3e18cdb52c7c06e902316 ` [条目](#entry-57) | applied | deckshell-only |
| 58 / N4 | ` 746076b98e77bd783de261822000505ca5a344ef ` | ` c826d6129ea09a1f0bedbadfc91ac801659e7b19 ` | ` 6f3c33a6143be3c6caa88e8accd5c1f43680194d ` [条目](#entry-58) | applied | deckshell-only |
| 59 / N4 | ` 3554ce7eceb09e0d14ee2253714b9257db728f42 ` | ` fba4f624dc524109f7c4fc19933b27870970ac6a ` | ` 4f420f9dc56e790647a3ca98abcaf9dabe898275 ` [条目](#entry-59) | applied | deckshell-only |
| 60 / N4 | ` 9f9dfa6b6a2134e1882431c5ef1db4f7e71c1814 ` | ` 5f807c898cfb9bd8a48a5888edf89f4280df7405 ` | ` 0a797fe88049d738a5729241a366d304152c98f1 ` [条目](#entry-60) | applied | deckshell-only |
| 61 / N4 | ` cd0879de06bd33744993e99cc395615bd986de9e ` | ` d001bd70c4d9050f9a8e153fc607859b9550e9d8 ` | ` 3a59c6f5d06d218e85a6b9820c40daf6b642a77f ` [适配详情](adaptations/3a59c6f5d06d218e85a6b9820c40daf6b642a77f.md) | adapted | deckshell-only |
| 62 / N4 | ` 4953e6dddf34acee1371b8b651e24c496a26253f ` | ` 889316df02f80582008562ff3512ef4559ca37c7 ` | ` c8d13ed580222f12704822d9d7b28fb4b05ffb51 ` [条目](#entry-62) | applied | deckshell-only |
| 63 / N4 | ` 7743aa7a094671430b9f3c594fd71f2630429327 ` | ` a94fc93bd3b072490e1fb5dcd01250b3abc5118c ` | ` d162f63288b9932a19938c5614501329cf305295 ` [条目](#entry-63) | applied | deckshell-only |
| 64 / N4 | ` 65a2822daa752e16ca5d62e2916b2032f8b4f650 ` | ` 53b6a6e117afed7176d5156f0dc5ec9920f54258 ` | ` 9d4fcaa42bc7dd3c5cd0b02856711dec67cf5eb4 ` [条目](#entry-64) | applied | deckshell-only |
| 65 / N4 | ` 63116956e9f77e691250b3326ac15a9dd4c6a47d ` | ` 894741dd529dfca9c39fc0bdf532620beb2ec4b6 ` | ` a6425769eafee3e9cd253560cf5998876fb910d3 ` [条目](#entry-65) | gitlink-only | waylib-only |
| 66 / N4 | ` 3d1a458a7ee298ba190fd0b73b0418dd331d27bf ` | ` f9d10829f29720ba2d0694c3d9188648fb28bd77 ` | ` e5ca7b09b7fa94a3791d7bb0dfab8f265e08c6b3 ` [条目](#entry-66) | applied | dual |
| 67 / N4 | ` f46ee9929e3b22fe009e1c19f8c66ea9ad941371 ` | ` d5c176303535b27f1b5c2cb91577d9514d264832 ` | ` 16dc3761174c163a24772523f201b41975c23883 ` [条目](#entry-67) | applied | deckshell-only |
| 68 / N4 | ` 371d32244323c914a6816fc7c14fec57c04fa333 ` | ` 19d1aa51a50bb15177022ff33e7bf72cca04631f ` | ` bb402df018ae3ac8e437b7212ae853cc575fe73a ` [条目](#entry-68) | gitlink-only | waylib-only |
| 69 / N4 | ` 07a7b175b71e5fb78a57e962db7b30d227e3936a ` | ` 1aad388c0b107b6e16f19154fbf0e74bb9e3c0ad ` | ` 9f66cdf64764ef8ee2323f536d42a15a62ff559e ` [条目](#entry-69) | gitlink-only | waylib-only |
| 70 / N4 | ` 24c1a0b547fc8a1c6617bdff147efcbad03c2f98 ` | ` d1be07121ea0f20bf87a128208a703a0dbbf3b68 ` | ` c1525adbc980b2265dd95c480d955fb76de00011 ` [适配详情](adaptations/c1525adbc980b2265dd95c480d955fb76de00011.md) | adapted | deckshell-only |
| 71 / N5 | ` ad91d436f0c7b8afd79153c766d6cccebc767370 ` | ` 64f6f0811be796564b5ebe0cc22028aa8dfebacd ` | ` 51ee64ab8faf3baf667c17a054c3f2704c825ef0 ` [条目](#entry-71) | applied | dual |
| 72 / N5 | ` bad95a0501c65177093d29bfb6512e4f4a56b580 ` | ` 5dea3074513768bff63f904acbc8de49d536e073 ` | ` a56066e5b6e1e4bad22ed4a3a7fd71ba9c5789a7 ` [条目](#entry-72) | applied | deckshell-only |
| 73 / N5 | ` 53918c4459982e245f7cff74d6a5038b9367f5f3 ` | ` 2c274bc916def0d7e2218820c4615d851b9511c1 ` | ` 5703ddc2ef3e60cf786765cd43f6ed692350862a ` [条目](#entry-73) | applied | deckshell-only |
| 74 / N5 | ` 275daf1769fc81d129c30e5625c8309c2a415f4c ` | ` 665b9f827c5b566ede2dd776d0c65f4147b60ac3 ` | ` d31eccdf1de36bc0440a4a53aa71b16ef993c4c5 ` [条目](#entry-74) | applied | deckshell-only |
| 75 / N5 | ` 4e221941db9abb6244b274ec0341347282610677 ` | ` 689c60464a1c6fbcde253be2fd2f2057c411f247 ` | ` de76c63a59c208f36bc56a0bd2e6168aa8c86302 ` [条目](#entry-75) | applied | deckshell-only |
| 76 / N5 | ` 944f8cdb0c3f11190fb5f21110b74715f1e35092 ` | ` b8260da472d0d94e774774680e9e8668a5c7eb39 ` | ` 2f585b01bbbdc1b384e8fccc5bad0c00f666e226 ` [条目](#entry-76) | applied | deckshell-only |
| 77 / N5 | ` 97ed8df0b546f925c17388b71fdd78181b2cb861 ` | ` d491c00e9282336836b82b61094ba8b703b062b5 ` | ` 267e44a4c9109d47fc4e0332c13345035eb55791 ` [适配详情](adaptations/267e44a4c9109d47fc4e0332c13345035eb55791.md) | adapted | dual |
| 78 / N5 | ` afbc3f99f27341540a7a01b4ea403bc8317dca67 ` | ` 486114a11eb75ee1aff0b6f05092c77ec3d098fa ` | ` 8c78649d46c0aa66ae5646b7f0de56bea578effd ` [条目](#entry-78) | applied | deckshell-only |
| 79 / N5 | ` ac2b0abcca695f82b6ade4313f49c121f3e338ba ` | ` ab60d002637d884c01480c9cfb0c3f0854090d24 ` | ` 3c6be81fa6aba76fffa1547e8df4f9e3eaa64c0a ` [条目](#entry-79) | applied | deckshell-only |
| 80 / N5 | ` 90a0790f9bed00ec0c52e35ffa0b421237b7e04e ` | ` 6f670f557b4541368f506c10cdb81d54bf6b9592 ` | ` 83bd0f817a4cef3d6057b578a164518399e246ad ` [条目](#entry-80) | applied | deckshell-only |
| 81 / N5 | ` 9f54c436e86ee07836b2dc486a154f17563e67cb ` | ` b717fefbf1e85c2bfb6a51e3e3abfc702ae8e3eb ` | ` 2bcf96cb95790abd39ab742f85c32dfa4c2026e2 ` [条目](#entry-81) | applied | deckshell-only |
| 82 / N5 | ` 0750fdaacee9ff641d1fed38096e5d4793391788 ` | ` f664763c24959a9b062386cc1ce8441c72cb7dd4 ` | ` 9392cc156e2797e1632257f7294680d8b5b8f478 ` [适配详情](adaptations/9392cc156e2797e1632257f7294680d8b5b8f478.md) | adapted | deckshell-only |
| 83 / N5 | ` 4325c6a384d7612265880f005acef8f04bc28e76 ` | ` 28e4c97b76eac3f398f1d7f17df5ee4f53c2d178 ` | ` 8dce58dc8defb49812c72f9fb3fd4f35d65c42ac ` [条目](#entry-83) | applied | deckshell-only |
| 84 / N5 | ` 9573a52366dc29e77213053b9902ee6237675344 ` | ` dafd320441740c956f39073798adf1670f62175f ` | ` 8f3999adea0edf132d7ff5c64a66dc030dbf8487 ` [条目](#entry-84) | applied | deckshell-only |
| 85 / N5 | ` a9df8d3d87256c84a593838057e587a6beee4ec4 ` | ` 7bfb0fbcdf84f9a35f350b6e62a04ef7ac15ad32 ` | ` 3a92b7a76b0048b9bc1cbeba1763d4fca11a2303 ` [条目](#entry-85) | gitlink-only | waylib-only |
| 86 / N5 | ` d63ad285b642d4a7489a9914441fde559e3b1839 ` | ` 1338e1a23f0e9ef0e67b1ec735839eae6e9fb2e3 ` | ` 8262fa7501b2f4862eacecaa46201522ad69ecba ` [条目](#entry-86) | applied | deckshell-only |
| 87 / N5 | ` a96f30f68645c48ebef7b8cac8299acbba2f4cba ` | ` 63eaead33c02e6b00ba8b12da3bd698a76632eb7 ` | ` c5947c0466d536533e0fa5dead5d1c57cdd80b31 ` [条目](#entry-87) | applied | deckshell-only |
| 88 / N5 | ` 526308f00028711152378a181e29045342f78790 ` | ` 86c68f5a971bcad870f68c495a36766c15df689d ` | ` 3b45db76bb11df355c90f29327c1253be74b2a51 ` [条目](#entry-88) | gitlink-only | waylib-only |
| 89 / N5 | ` b4d7bff91684db691da410dc4c49a3a4936044fa ` | ` a6c94355d4dca81057d35e1d3455b6bea6553413 ` | ` d0101a2b7346652365a535b2c7ab1ae841216bb9 ` [条目](#entry-89) | gitlink-only | waylib-only |
| 90 / N5 | ` 6ea349ac28b93b61ca3f9223ec021344141d6fce ` | ` 7d2daba2014eabef671253fb361c372cedcfb4f0 ` | ` 5b04ac8e277ac6d7887bf2ffb0be358f554d4bcc ` [适配详情](adaptations/5b04ac8e277ac6d7887bf2ffb0be358f554d4bcc.md) | adapted | dual |
| 91 / N5 | ` 252d0df3366671533b1914b55053a5ac4cbe6a3a ` | ` 0b78f4b4bc17080372dd230c180abd9b5643ddec ` | ` bde8fd486752be3c8dc0d6d7ffd5a0f8e3aceaf8 ` [适配详情](adaptations/bde8fd486752be3c8dc0d6d7ffd5a0f8e3aceaf8.md) | adapted | deckshell-only |
| 92 / N5 | ` 7d56f56671dc411e631b95b4b5546bbdee0f0d1f ` | ` 4e1b025de4bccbcc102dae76767d99b58af6890e ` | ` 7034642af76e4db8f8f6dcdb45e031c2ccc13005 ` [适配详情](adaptations/7034642af76e4db8f8f6dcdb45e031c2ccc13005.md) | adapted | deckshell-only |
| 93 / N5 | ` a7679c9a4645f10555ed76d30845efa80ae3fbeb ` | ` a4fde1a3fa68245d70814a2e61d519840b20087c ` | ` 373870104071ce3120dc7829d70ce8f70d720a59 ` [条目](#entry-93) | applied | deckshell-only |
| 94 / N5 | ` b8f04600d0106636501e569f7785f80d0568565f ` | ` 4145ac43114354607bf4bdf09d65d508156eadee ` | ` 38761145d78fb4ad44609a310bbf8c7fbc4ad92f ` [适配详情](adaptations/38761145d78fb4ad44609a310bbf8c7fbc4ad92f.md) | adapted | deckshell-only |
| 95 / N5 | ` 9886fca6d0eef13612b4046935b9bbe6f7df9fb1 ` | ` f87bf9134910b33ded5b315dc0c59931cb35684e ` | ` 3d592cb35f0f71f4d07dca88133deb5576be639f ` [适配详情](adaptations/3d592cb35f0f71f4d07dca88133deb5576be639f.md) | adapted | deckshell-only |
| 96 / N5 | ` 36cb2c941da52b65bd2d5f879197657d73b39bad ` | ` 7b50a09e1f1a84ffd8b5e8911a34b5253909f5d2 ` | ` 9177b1b00b85cd2bb766c12ceb347537230db115 ` [适配详情](adaptations/9177b1b00b85cd2bb766c12ceb347537230db115.md) | adapted | deckshell-only |
| 97 / N5 | ` da6c88f5239831ac5641c3f2bd1a84f5eab05c32 ` | ` e2ca4614c1f41d828e7dd6500bcf42ba9d8245ff ` | ` 1a547cd2022a0139314c437897a3a4d7561068b1 ` [条目](#entry-97) | applied | deckshell-only |
| 98 / N5 | ` 6e980c1bf5e451b4ccc62d68256cc41247156b02 ` | ` 711d5d88ba050e198125dfced7f2e765e02137d1 ` | ` 3213b8b8d4cc6a68e05a9ded9e569e9965fcb7b8 ` [条目](#entry-98) | applied | deckshell-only |
| 99 / N5 | ` 4d4736f4dfa73b04192245446ac1bde05eb83563 ` | ` 16db9a1f75c16d8ecbf9e2a9d5c0b25f1ee83b93 ` | ` 52f727ca188d6837bac23164983001f622fde376 ` [条目](#entry-99) | applied | dual |
| 100 / N5 | ` 0333a31456c7f90708c7f482939e23d939283b45 ` | ` 66f83af19a18b1d78d9860e5c6d675fb11e5c110 ` | ` a35e2d49279ba82d0892b73a9017feac71f64826 ` [适配详情](adaptations/a35e2d49279ba82d0892b73a9017feac71f64826.md) | adapted | dual |
| 101 / N5 | ` 9582881ddc2e71c73f01eb1f8f5efd0b87a8b107 ` | ` c65523a80d93d7fb885ac16b4338169eaab99c7c ` | ` d3726e904dac69ac8d2e5f319c2d7f076b645e23 ` [适配详情](adaptations/d3726e904dac69ac8d2e5f319c2d7f076b645e23.md) | adapted | dual |
| 102 / N5 | ` c696665b368bcb54ef6c8e5510f383672ea10329 ` | ` 6a44102ce5d9f86ce168a90e42ef128af773944c ` | ` cc65b1cffce4a1dacee6b0bba83c8c2fb702310a ` [条目](#entry-102) | applied | deckshell-only |
| 103 / N5 | ` 1addea0a87111d2121d42977ab5b65f8a16544c3 ` | ` c172fd981d2764a0fd96084b84c5f4df482a6af5 ` | ` 96f72e95820c980b62c1711497d32658cd8db2e1 ` [条目](#entry-103) | applied | deckshell-only |
| 104 / N5 | ` c5466c27e69c09833cfc69444d19b10484a28d0c ` | ` 98104edfd8ffad3dabfc1fb787b8a6086beed977 ` | ` c25b785d08ebbf102f93e79793034a53c7deeec5 ` [条目](#entry-104) | applied | deckshell-only |
| 105 / N5 | ` 78de1d09212c1491d1107a76a0e6ebc4f13c06d3 ` | ` 1182ac54012841668b8687378c6d94c5615ac573 ` | ` d191ca9270590e0912f0d119f1a20bf3c0a6be1b ` [条目](#entry-105) | applied | deckshell-only |
| 106 / N5 | ` 1708d699270363c01d636bce8f444628ba6b95d1 ` | ` 818c71467e13e56da48d63e241b55db2452fc01e ` | ` 2e938af1ae80f934aa36823d7fd0e34e3f147589 ` [条目](#entry-106) | gitlink-only | waylib-only |
| 107 / N5 | ` 293dbe5ef45d3e3bf597126ba990a77003502210 ` | ` d5f2b63e0625545925c98068367f7f70e241528f ` | ` 6a4067b259530f22d6accd973cc7460f668d321c ` [适配详情](adaptations/6a4067b259530f22d6accd973cc7460f668d321c.md) | adapted | dual |
| 108 / N5 | ` 78773de1f242c1438b78f716c7d11522b58022a5 ` | ` 8922d52eccc5d1b6a2a7cc91ba8251010dc902fd ` | ` 8dac6a4963f2cf229258e8a2c40fb317c365883f ` [条目](#entry-108) | gitlink-only | waylib-only |
| 109 / N5 | ` b037ac5c5dcd33032424d546a312d0ad702c4bf0 ` | ` ee6dbab417444731ce4947f5cc0fa5d9a6d9e917 ` | ` 9b069501667a3171600b360d65b6224ee4291fbd ` [条目](#entry-109) | gitlink-only | waylib-only |
| 110 / N5 | ` 2c203454926f687ee5de51bba5f1f0478249c88c ` | ` 8b13bc88dfeda8f013972dd2cdfe12028c931ded ` | ` 282ef67dd3dd1e0238f3298b15227ee9c039797f ` [适配详情](adaptations/282ef67dd3dd1e0238f3298b15227ee9c039797f.md) | adapted | deckshell-only |
| 111 / N5 | ` b6dfb35207860d75b07cabf216484b7ba166038f ` | ` 8e3d0d0096837a3e4237779319e10bf58a9becdd ` | ` 7fed084667655e3ba8f49ecc721915ca2411b75f ` [适配详情](adaptations/7fed084667655e3ba8f49ecc721915ca2411b75f.md) | adapted | deckshell-only |
| 112 / N5 | ` fdd73671fe9a16b061bad76e2d73babc65856581 ` | ` decd03f1654c315938d43ea1451d1ba14ae421c7 ` | ` 20498f81eed9d58b88b08665f432699442585b31 ` [条目](#entry-112) | applied | deckshell-only |
| 113 / N5 | ` 7134887c66e5215182e1a1f648bdc8971f17e864 ` | ` d24d389a597f9be2e619586bcc76b3c0518ceef3 ` | ` 9df94d7acf275a73289f2b31315e4dc42dc22207 ` [适配详情](adaptations/9df94d7acf275a73289f2b31315e4dc42dc22207.md) | adapted | deckshell-only |
| 114 / N6 | ` b248e3682368a351ee2d4622c06fbe5e9c2d3b16 ` | ` 4954329816561c4d82b69f691c4627a3aa24c58b ` | ` 829a3932472f2ba3021c52541660e52a0b5629a2 ` [条目](#entry-114) | gitlink-only | waylib-only |
| 115 / N6 | ` f2773149b47ddca53b9fc234172830073964334b ` | ` 3c7f3d83d1ec7b341a5b81137c792bf4ffb7751f ` | ` 7c717fbbc24f0c7d7b7dc6e6bc767a770bb0258f ` [条目](#entry-115) | gitlink-only | waylib-only |
| 116 / N6 | ` ecb32e8a1fab02512038324e5a5e7a6cdf8ffa74 ` | ` 2b85480211e6fb1ba43814440cc835f2a70859bc ` | ` cc3a40184cd538ce280aa46d9365cabb50c668e1 ` [条目](#entry-116) | gitlink-only | waylib-only |
| 117 / N6 | ` ee787154f3035363bd1c3a95741fd5283b1796f3 ` | ` 9851d44e6dc6e9ef8c658396f2b0a4477c5a2866 ` | ` 96d32e9f367b37fe04f77d2b9e5a6e486b44a2aa ` [条目](#entry-117) | gitlink-only | waylib-only |
| 118 / N6 | ` 48f9b57f346766710f86592cb4d2929cf6b3ed08 ` | ` c9b3fe937f7f2aeed5fbe0629530e13d370c745a ` | ` 096bf10c0ad671a7494ca10742b6c468f7ac55e5 ` [条目](#entry-118) | applied | deckshell-only |
| 119 / N6 | ` 7df69e62d117508e633ac4d740cde9cbd31dc338 ` | ` f810abe625e56051a2167498c1a03fe05a27f48c ` | ` 5ad9f4c5f7e270c149b64b59eaf24de1f67d664c ` [条目](#entry-119) | applied | deckshell-only |
| 120 / N6 | ` 447c3da6712695822738ee399ca08eb9c82eef4e ` | ` a95ea37df1b89841931749bba252c2acf794091d ` | ` b303382581aaf549d9375a1f3dcaf2e9bf824da0 ` [条目](#entry-120) | gitlink-only | waylib-only |
| 121 / N6 | ` 2e27ca38141087e551e22330165c86d886bd8cdf ` | ` a0fd3d5f69f8ec3ddd8d1cffe9a1d6fb69b469e6 ` | ` 607d7c87fda0da5a019b40e7b339ea48c35c00fb ` [适配详情](adaptations/607d7c87fda0da5a019b40e7b339ea48c35c00fb.md) | adapted | dual |
| 122 / N6 | ` 8e41511b7dbc1ad148a23f5817b36527def9ddce ` | ` aea999673fe2f249fc975be237a1d9d1189e8c75 ` | ` 99ee1b5737ab41417d42ac4ea2ca452b6b9f1b19 ` [适配详情](adaptations/99ee1b5737ab41417d42ac4ea2ca452b6b9f1b19.md) | adapted | dual |
| 123 / N6 | ` 53dffe1867ea3a13167eecff0d08343b3cc2a368 ` | ` e3486b1bab6bcd9270dfcff0b34d161b9adfe00f ` | ` ee48507b1f2e9b092d95c4a2b6f5e1588cffce7d ` [条目](#entry-123) | gitlink-only | waylib-only |
| 124 / N6 | ` 0060a0d0dcdc189b263fffc51b4ad6e021de9854 ` | ` 929909b325d11ee2801036ef7ca6c721160255e2 ` | ` 3f6a45c376e219dba41bb78e7cc47db97e977e90 ` [适配详情](adaptations/3f6a45c376e219dba41bb78e7cc47db97e977e90.md) | adapted | deckshell-only |
| 125 / N6 | ` 9ba10c8ef0650cb2743d0666132c667046c6c51b ` | ` a4ae48a523a4ebc090d55192f1c81dd6f64ff8a7 ` | ` 5f554a489d848513b2d9ed0639de47a10a420847 ` [条目](#entry-125) | applied | deckshell-only |
| 126 / N6 | ` 30447d0582ccb582acf38cef4db4b729704dc6b6 ` | ` 24dbc1727571c5137eff819c468058d236081000 ` | ` 4256636980913e8d4f3f7e5d4991fb74dae43141 ` [条目](#entry-126) | applied | dual |
| 127 / N6 | ` a50a1ff5dd11bd4a769a5c2176ff718411dea9fe ` | ` a801b9bd05f2c51c57445da3751adc6f63d8bded ` | ` 04b021c1ab55c06abe39bdec0914831ba1b1c0a6 ` [条目](#entry-127) | applied | deckshell-only |
| 128 / N6 | ` 80137e42c2dfa4b1ff7edb0c81ab75da9c9f171f ` | ` 965c520ea5dce8c4ee5ae66d65a77039fea7bb1e ` | ` a4c3cc1f3934206dede125474835a9196c615d4e ` [条目](#entry-128) | applied | dual |
| 129 / N6 | ` 0c6e43e72c74a95ec603c6f7e517507dfbf0311e ` | ` a7496a016c4bb70eca6cf7182c8e310595ffaf06 ` | ` 156814d3a8d67946f8e5c60d96a7491d00b17559 ` [条目](#entry-129) | applied | deckshell-only |
| 130 / N6 | ` b1c772c6cbf1061bce476dff32878f0894901ab4 ` | ` 27de46cad543e6c3d830456b7ab4b80a6f57db42 ` | ` 9c1ffcb5c40dc48dcf91f8a6d65ffd65bf3e72f3 ` [条目](#entry-130) | applied | deckshell-only |
| 131 / N6 | ` 22609c6cb07f3493b948aeee2d018093478eca83 ` | ` b6a0f8fb50d77417654f844cafc825d142fe8f8e ` | ` a7dc05dff36251c8395757fe172b2cd699408ca8 ` [条目](#entry-131) | gitlink-only | waylib-only |
| 132 / N6 | ` e7bd2c16c3b7c1dff1b39236b9724b4a15e2fab2 ` | ` 6a5fce35493da5471a6daaa22c0ab83ebd036e35 ` | ` a4e9d9757c34f44b0ec94a9673c303fe38b88609 ` [条目](#entry-132) | applied | deckshell-only |
| 133 / N6 | ` 07421a378dfb63d2e84ab0af2cdc2224b87802c8 ` | ` 426d11f2bec4acc24cb493feec6cfb018feec68a ` | ` 9d1413eafc5d5cf6dd3b3fc64d06cbba3821fadc ` [条目](#entry-133) | applied | deckshell-only |
| 134 / N6 | ` a050947305cd232a992d4e70b4668b20bcaaff25 ` | ` a62e09b2a18442c47c4140caba074d6e84471632 ` | ` cf5c5ac84e68c1c1af7349d985df26885e673002 ` [适配详情](adaptations/cf5c5ac84e68c1c1af7349d985df26885e673002.md) | adapted | deckshell-only |
| 135 / N6 | ` 1921954d28e618fc3496d88d32b4063fbb56563e ` | ` b9e028bc01eddf54a1cf0a4d7dbf63121695aafa ` | ` 519189e1861788d17714f6c5b1bea7b63ff2ec1c ` [条目](#entry-135) | gitlink-only | waylib-only |
| 136 / N6 | ` 8b6d1783cf48bc865d762701f97e376ce2449e50 ` | ` 7298e94929212100f5354fd6ef7203a1e19d52b7 ` | ` 8f44e0d4fe9aa629736cbce7fd8145e5e7cbd0ab ` [条目](#entry-136) | gitlink-only | waylib-only |
| 137 / N6 | ` 2d47e5ed21e1b2c9cfa5ba80f4ca8ba1200e9f5c ` | ` 651782d1aaf41de179160be9b89aa52118ec5b04 ` | ` cc7a35132f760e484b324e474636c657ceba36b1 ` [条目](#entry-137) | gitlink-only | waylib-only |
| 138 / N6 | ` b6b92729856e1cfb59a5f4abccfa73fea008852d ` | ` f6d10af3e4e1d93905fe6082e8ed7954a30c1e84 ` | ` daa1bdf9d47c490ff3adf74e5f94eb0c61fdf8c5 ` [条目](#entry-138) | gitlink-only | waylib-only |
| 139 / N6 | ` 92cf9d3d54f20cbf7bc509a2413678e89f8a0f25 ` | ` 0bce1099c8cb3086a37b75de3a012fa564324fd5 ` | ` 166a0f2bca42cacb506862cda5227d36c75c27b0 ` [条目](#entry-139) | gitlink-only | waylib-only |
| 140 / N6 | ` eec5773b46a1e5286ba8f6f85a4da40eba85580f ` | ` 11415e1f8f22020b7abc4cf7443e169c0ff9cdd1 ` | ` bd8a819e957b5b94e9edd37494fd7946db0ca59e ` [条目](#entry-140) | gitlink-only | waylib-only |
| 141 / N6 | ` f1cbaab98b5d4568ebe244229931d5ae4665ea9d ` | ` f5ed4f40d542de2cf9eef79ab339caaad5c449d8 ` | ` 502927a9a42a15937b00e7a2abd6db95dfb36da3 ` [条目](#entry-141) | gitlink-only | waylib-only |
| 142 / N6 | ` 3b7e3f20e120dc85e9f08d0989075f17818334ef ` | ` 1914c653363161faaef2c7c894dcc8a82ae0b904 ` | ` 27381571b68b314cc2c8584536e946158f778c47 ` [条目](#entry-142) | gitlink-only | waylib-only |
| 143 / N6 | ` 6ad1e1212a78210e7c6f8bec0476d40193852fde ` | ` 58e10daba700b60b28f86d43d4ffbea73314b06b ` | ` 943d72afa97b954c9c461eaac6ea704c699a38d0 ` [条目](#entry-143) | gitlink-only | waylib-only |
| 144 / N6 | ` 22b4fe8e7a5d0eb9688d407442ec941c715b1546 ` | ` 9f99b02fdf346be97d0665a3fe0732ae12e07cfd ` | ` f973c44994ff4f21d3c4dc1628d77aa80be41437 ` [条目](#entry-144) | gitlink-only | waylib-only |
| 145 / N6 | ` 8d1df35e6373636631bd0a46a1c89bd59763374e ` | ` 11246d02e00b551f6eac1fe0cb58bf7b3dc6f580 ` | ` bc4c18532be0b002fc840d6dab49710c9c5494bc ` [条目](#entry-145) | gitlink-only | waylib-only |
| 146 / N6 | ` 1419b581afd87ad0ae5df76757add34cb9a98bde ` | ` b3c14b459a64d80335605c3cb6029579b8214a75 ` | ` cc2a056b7bb43df856357c4d1072dbd96ef967e0 ` [条目](#entry-146) | gitlink-only | waylib-only |
| 147 / N6 | ` 8c6229f9c4eacae14accc02f0a941b0a03ca622b ` | ` 16f7b31e4d8e3d597d7123f4771cce5f9e788436 ` | ` ad05c755b4981e6758bbc1f45700fd21183d765c ` [条目](#entry-147) | gitlink-only | waylib-only |
| 148 / N6 | ` e6793bd93ffc041083e31d408c3e3aced255d8bf ` | ` 11d56309fffc4309dcb735a8414d637e86b9e825 ` | ` 2c4e376dacc5461807f3af0c0a3fd5af0a5fe49a ` [条目](#entry-148) | gitlink-only | waylib-only |
| 149 / N6 | ` 54187ff9b725b409e4f6533415a32dd3c11c442e ` | ` 889979d4216a8a91c3c9336ed396567f21ccf653 ` | ` 4b9690cfdc181a5e675495f68586a1dcf7230dc8 ` [条目](#entry-149) | gitlink-only | waylib-only |
| 150 / N6 | ` b3c71df01083877ecf3200323ea551c192d8a898 ` | ` fc690665b76b0c08be2396b0df94f7d5a92b3ec1 ` | ` b7fcd9f1a7f28f35fc4d2c54ff4fd185104d1195 ` [条目](#entry-150) | gitlink-only | waylib-only |
| 151 / N6 | ` 3697e0f99a06e24895ac96cf0ee3c7a54bf1608b ` | ` d653b99d978c5c78d96104a9b6ebaeab283c17a2 ` | ` 750fc9c7ce6208577bcb5afc23f7acee3b838d9a ` [条目](#entry-151) | gitlink-only | waylib-only |
| 152 / N6 | ` 30f621f3623fcdf8d3256886584286f4aaf08f3a ` | ` 5fa870246b3670640638f9ffbde04206f5a3f8af ` | ` d9260e8190dcb26ba7d46abfa6e7c2cc31508cce ` [条目](#entry-152) | gitlink-only | waylib-only |
| 153 / N6 | ` a7e0d3626ecafd17cbfc9c19f5807cced5b7dbf3 ` | ` ac4d55eb69fa0a57a9b524de822c374464ec53b9 ` | ` 4416ebd65ca782b694010cd8c38a5bc3f4f3871b ` [条目](#entry-153) | gitlink-only | waylib-only |
| 154 / N6 | ` 5912dc0f34fcecfdd5476656e3c34a26e74db765 ` | ` 3211263a79a966b813ce08160f1bdf0fc1c53c7e ` | ` c017ab00d35e7282a45115fcf3d921e72e6980ff ` [条目](#entry-154) | gitlink-only | waylib-only |
| 155 / N6 | ` 622b27271a424a1dc392ad665f0ddfca06263231 ` | ` 545a0b7cdcb965a6e1bc871233becb1667399764 ` | ` cca3a30d223eace840bb22dc9cdfbc0ccb30b8b0 ` [条目](#entry-155) | gitlink-only | waylib-only |
| 156 / N6 | ` 96bccf46d3653a46327e838e90d52d5ec96554f5 ` | ` badd8e20986b256d6b07d891067e9f1a7489b69b ` | ` b27ec29f0395734053d864f8a7818f95e3f6c272 ` [条目](#entry-156) | gitlink-only | waylib-only |
| 157 / N6 | ` 5515da6732aefbe2a23826617dd834bf9a2a7134 ` | ` 83cc1b00e1a78831462a5c3a442c286482cd97ce ` | ` 764543acdbdcc02dd6210386b53c35c95f41819d ` [条目](#entry-157) | gitlink-only | waylib-only |
| 158 / N6 | ` ea887de23d872cf160647f8320633fc361d9f067 ` | ` 34a79a3b518dfe3c8c77667d817cf69832554639 ` | ` 33569503d0550352b10f397c8582e34c6b5351fb ` [条目](#entry-158) | gitlink-only | waylib-only |
| 159 / N6 | ` c96938ef3a78fc7d454eea5109cbde66d795ed6c ` | ` 80f066e2fd824fcd561bf974a767f906822352e2 ` | ` 9f030f1b40e015a5f6a2ae5f838da66e50b66a76 ` [条目](#entry-159) | gitlink-only | waylib-only |
| 160 / N6 | ` 573e7aa6533edcbf765751bb3e2355eed15ba689 ` | ` 8840e115e3c987c4c88b5645276c22ba3425fd57 ` | ` ac005fa43d6c40e16d7eb0112c364031629214ce ` [条目](#entry-160) | gitlink-only | waylib-only |
| 161 / N6 | ` a3ad65170cb0d59adde8d743d3c0efcb90f101ae ` | ` 6658466f91b60a6656d8354855cab2a2bc12f311 ` | ` 2b1c6e6ccd9c4debae8619f85135a66ddf8cf409 ` [条目](#entry-161) | gitlink-only | waylib-only |
| 162 / N6 | ` 28b8cd207acf042de0cde21a419944f3a5e98c0a ` | ` 94710e566549d37c32d12c84b084e74e7508ef69 ` | ` 8495a9d37621566d722d5cce964baa7ece08e304 ` [条目](#entry-162) | gitlink-only | waylib-only |
| 163 / N6 | ` fa6a35279263b8f45ed98922e408b371641ce6f4 ` | ` a071c375fd77ee1515aa1f7c04f48f62b56567eb ` | ` b6988fea36f8a4c5cd7b055a85bca7c66d5e6974 ` [条目](#entry-163) | gitlink-only | waylib-only |
| 164 / N6 | ` 3fa894cc040d4028e425492841f86d5556d46937 ` | ` 33de57f30e6a2babed922d03ed949f75b1751ccd ` | ` 510071ba7c26c022ad3e6efce6cba5d83b34b93e ` [条目](#entry-164) | gitlink-only | waylib-only |
| 165 / N6 | ` d40797ab9cfd328185f3a3ba8290fc083c292758 ` | ` 1508b3afb0e4a86964e18f07d59e0bd6eafc3cfc ` | ` 37484f29a09561dd6dab1ae31717aeba155bfe8d ` [条目](#entry-165) | gitlink-only | waylib-only |
| 166 / N6 | ` 7b15516aa256d738c76e32fdd62e8ca11069b42d ` | ` d76b74cc45400c2081b05640da25a044a9e3f7ff ` | ` dfb53a755f865b8c1500d6bfb516bf55454612a7 ` [条目](#entry-166) | gitlink-only | waylib-only |
| 167 / N6 | ` 334c2b21f20cf142d6fada8c47b074c73b9976c2 ` | ` 9f40dd4d3f82f9cbcbbe7be03a6cc8f94316021e ` | ` 42997d773cedb420f5cbe29feafa12f8c94a9993 ` [条目](#entry-167) | gitlink-only | waylib-only |
| 168 / N6 | ` bf5238919abe86a4fe0dd6909fc3f0bc76aa7369 ` | ` 4a3c9f286f7f295e384a576e74c5683453071b66 ` | ` 1225f4c75ff081903b19a17b97373ee08f55eb5f ` [条目](#entry-168) | gitlink-only | waylib-only |
| 169 / N6 | ` edd2ff863d2799591b41bfc6a633d205f240e7d4 ` | ` 4f0d38314a2a4ba953b8ee9fed57b779b0e55749 ` | ` d9f8f0d1b9fb875ae812abf28a5009a2befef08e ` [条目](#entry-169) | gitlink-only | waylib-only |
| 170 / N6 | ` 85be1f0a54bb42dcf542ab6aeb12bf3360eb9b5a ` | ` 7a1ae9fd6de7dd8fa2bcb6b4c98581a98ae1d30b ` | ` 82329d6e0ab47a7f9349f42a34dcf2fb08417810 ` [条目](#entry-170) | gitlink-only | waylib-only |
| 171 / N6 | ` b02653d741e06f43e39329492ba348fea9081722 ` | ` ac11ce200417bf4f8c6e86bee8866a9d5ff54fba ` | ` abfe1114159e3db29551286a3599e5dd5b634bad ` [条目](#entry-171) | gitlink-only | waylib-only |
| 172 / N6 | ` ef9eb4e7391ebcb5e0ed8de36ee2d16e7a35ccf5 ` | ` cb8627bdd8bb3ae759a80e3095eff2bdc45a4ef1 ` | ` 0ab0b4c63231fafa94a7921f5d985b09f243d05d ` [条目](#entry-172) | gitlink-only | waylib-only |
| 173 / N6 | ` 9604e4859299596f83425af79e7dfdea0d180b99 ` | ` 2049967d82e98145be89c9eb7f7ac55634b16f1a ` | ` 606a90e69a10c5d72197e134d1fbd599f79d5494 ` [条目](#entry-173) | gitlink-only | waylib-only |
| 174 / N6 | ` 8f52ccea285f0f3c8a52142d597f5382c9b64197 ` | ` 64ef4361008b38ab40c22d47b668bf473ea5bcfd ` | ` a102cd592527a8d8bb347856de6cba45f9496e1f ` [条目](#entry-174) | gitlink-only | waylib-only |
| 175 / N6 | ` a730f12008999409a4b07957833e1c0a494d43af ` | ` 7d880ef834c54c36286696d7373aba5a4a6cd72a ` | ` b1eacbeba95bcedf2f92e5dcc2093efffe9ef22e ` [条目](#entry-175) | gitlink-only | waylib-only |
| 176 / N6 | ` 8808fbce11b8159413957d64adfb844dd068d5bc ` | ` 3a92883d4adab1d9e95f427b94ab718b5ef91fc2 ` | ` e7bd185ab81aff1cfe77b5d75c5a9c9153dd744b ` [条目](#entry-176) | gitlink-only | waylib-only |
| 177 / N6 | ` f686dfea1e1d783715acf91889f317ca1a94a151 ` | ` 76e874583635e8994af46985dd115177489c851c ` | ` 6a4deb7098882fc321aef03fccf64aa5072f0ec7 ` [条目](#entry-177) | gitlink-only | waylib-only |
| 178 / N6 | ` 34f1e53916440ad471d025e5c118cf7769ec0af3 ` | ` d424c8010ccc126dd4feb1fc9d3bfc863ee56a75 ` | ` ea500e0cc5d58440e8c5c08ceb0f29ed370aa2b3 ` [条目](#entry-178) | gitlink-only | waylib-only |
| 179 / N6 | ` 4ec0a9e4bf7ef12a6a6830b3ef15cd260bbb2de0 ` | ` 2db22e2e4b72835aca460a02c8115610fa849b3f ` | ` ebf05518ccdc5cf8693fd34e6f89e38280b70820 ` [条目](#entry-179) | gitlink-only | waylib-only |
| 180 / N6 | ` 7a009f2f18007c6afc7c11fa72948af9fabf990c ` | ` 2263349be1a78821d2bf6bd576eb4d74036bba59 ` | ` 67fab95475a74479a16caae0466653b92300ba16 ` [条目](#entry-180) | gitlink-only | waylib-only |
| 181 / N6 | ` e2e62b6ea6965c65f499de1b40a08330f371c9c8 ` | ` c3574d750cc67a4a67a464d5fe5cc74a6c642dbf ` | ` 301e294f429d71e8fd11a1e96bbae85b81e25c69 ` [条目](#entry-181) | gitlink-only | waylib-only |
| 182 / N6 | ` 1fcd0c9da6a25d58a23b9450acdcd0d5609e9bbe ` | ` 55883d772fc853d72fb22927889ca03b76f3d3ff ` | ` d0ae74d8e134c65035a6e8689dff77b132bcb4d5 ` [条目](#entry-182) | gitlink-only | waylib-only |
| 183 / N6 | ` 04f282f3f12debe935a41ec6e709d40575ee8c8e ` | ` 94a8020c923c5b71a554335fbd3508265d8f440e ` | ` b76a76271c82c0249782008321ccb0634915528b ` [条目](#entry-183) | gitlink-only | waylib-only |
| 184 / N6 | ` 116c2281e863d65584756b8ff2eb3f8b34490bc5 ` | ` a59c54b6e8a14815d16ce1b591a41960a371192f ` | ` 30e536d48a72dc5e2fd7d8a46187a69619800b39 ` [条目](#entry-184) | gitlink-only | waylib-only |
| 185 / N6 | ` ca49086f7f6582a8efa246fa1e1c93624b825a74 ` | ` f7a6d6324a68402bd7a8889efa82372c263f337a ` | ` 81ede01ad391c1ce72eb532bfaff00d1300b80ea ` [条目](#entry-185) | gitlink-only | waylib-only |
| 186 / N6 | ` d04c4477b8dff7b358d8950acc974dfe353f9602 ` | ` 42036ad32c8a2706d1102377455fe46f2e2e25b8 ` | ` 303f99c25aa097ae4179389a95f75be1e8f0604f ` [条目](#entry-186) | gitlink-only | waylib-only |
| 187 / N6 | ` 31c96911257d84b52b6e85590d2c7a0ae1fbbde3 ` | ` adbeb09971f5fdd91635a95df20495ed0ffff5c9 ` | ` b1e6e2901d5699271b6df0b83a07f73605931c47 ` [条目](#entry-187) | gitlink-only | waylib-only |
| 188 / N6 | ` dfdbade3b1fba232c2d723922e1c95f3a7e0fbf4 ` | ` 413b1f75b7e72034fd2748296916ec716ac0856c ` | ` ce637ce16b90c42e462120dad494550c297c4fef ` [条目](#entry-188) | gitlink-only | waylib-only |
| 189 / N6 | ` 385d8feaab802bcd0f29086eb7397fc0d45f5525 ` | ` 5aecde5383ad9219c6014621de90bc6f254a8b8c ` | ` 8bc79e55826a496a81abf8b085ea7ec050fbdfd1 ` [条目](#entry-189) | gitlink-only | waylib-only |
| 190 / N6 | ` cc8a61bcb5cffc94a98020891c6839002714738c ` | ` 46b8d043f5c50d5c3c82b360af9815722a572796 ` | ` ce71660226663f13e2d35e84e9726e421c9e5b2b ` [条目](#entry-190) | gitlink-only | waylib-only |
| 191 / N6 | ` 19383eccf888693daab4cc2fca8dc60a44906c37 ` | ` 1d0ca8a3d91bad5ea7e04dba01750a2bed0b09f9 ` | ` 66f1d53d8c746b0d68fcd33f9b834ea7901332bd ` [条目](#entry-191) | gitlink-only | waylib-only |
| 192 / N6 | ` d14e882d30f6edf50ed2cdc90526e46b671f9897 ` | ` 93c3c55c6671bdb7990e5cf1ab545abc9c219df2 ` | ` 93a849b415cc7eab5b11185e97bf6c1b31bdca34 ` [条目](#entry-192) | gitlink-only | waylib-only |
| 193 / N6 | ` 09e79cdfc902341d74cbe20bf8c31c14dac8db71 ` | ` 0e3d1f90716d82726338151af1a639430d63433a ` | ` 524712e93c9c057986aef88a5f2c15be7315a54d ` [条目](#entry-193) | gitlink-only | waylib-only |
| 194 / N6 | ` ab42b16e5dcd895822b003517d7927906a1f41d1 ` | ` a02b66429a213921c8d75a695758c80a0286d4df ` | ` c022902959434260a6aca54d93b72643ee95993c ` [条目](#entry-194) | gitlink-only | waylib-only |
| 195 / N6 | ` f4af38c3cba717b2fcc9f6bd264a3c00abcf5f7c ` | ` ff7000275f7cbc486b1e2122c5a1ac7a685d0e41 ` | ` 8d9eccee4181919b77a95290753066cfc6d66e14 ` [条目](#entry-195) | gitlink-only | waylib-only |
| 196 / N6 | ` f570342baf591db7616dc5befeb70b6f235d1713 ` | ` abbe5b06d26617d58f14f90cdab677eea5c9bd2b ` | ` 7cbab831d359ffaa40bd3e9821cea61f1586b3a8 ` [条目](#entry-196) | gitlink-only | waylib-only |
| 197 / N6 | ` d67047baf7fc29be4808d31dcfc0174be85a2f40 ` | ` 83247e7f7c2c920669c5cc8bbf4034bf82fb648b ` | ` d77ad8d73b97175a52b8b568c8de9d186edebe57 ` [条目](#entry-197) | gitlink-only | waylib-only |
| 198 / N6 | ` 06511afe2c784af2714aee5588bfbffa91c87f0a ` | ` b52a2f88851517dd2f78a94b12d8141580cb952c ` | ` 9b83068369b8842b1618ce4e2eb3efe5854e91c0 ` [条目](#entry-198) | gitlink-only | waylib-only |
| 199 / N6 | ` 880b5241663166d65ba65243ffaeff01a6ce5073 ` | ` ad6fcdbfa71d7705d8f420f8aa3478dbb7bb2cf1 ` | ` ae0d40c9a03f64d16b7a126d5b547df923874f94 ` [条目](#entry-199) | gitlink-only | waylib-only |
| 200 / N6 | ` 5b55eddc4888fbe9a49197d49fe58b98c0bf03af ` | ` d53520a011086e1b33c06afcf89ec69c6c239560 ` | ` 365b2ef28bda509b073fb335734289660cc351a7 ` [条目](#entry-200) | gitlink-only | waylib-only |
| 201 / N6 | ` ff043fe802074ca7ee9dd46d17ecb9d482016948 ` | ` 6dc2ecf54b19baa5d204933b28eae15458e5635f ` | ` 9f451838680c5c95f939570660982b1a3dae6c50 ` [条目](#entry-201) | gitlink-only | waylib-only |
| 202 / N6 | ` 019c13f41d3538924467c7ef1a3a34695a7ff255 ` | ` 5291a2172bfdaa7b5bc6b5c047fffe9e4024e7d4 ` | ` 2b4664d03374dcbb4691de5b774a0a4249b61079 ` [条目](#entry-202) | gitlink-only | waylib-only |
| 203 / N6 | ` 29ea403f65a802989dda25824ff9476dc7b77c12 ` | ` bb27abcdcebbe2115f3edee0e236e3746b9aab18 ` | ` c5b06653de74824ee84344413a24eacb119165a8 ` [条目](#entry-203) | gitlink-only | waylib-only |
| 204 / N6 | ` bd81e21bc6c1cab671d0594f0b41d28f38d1d1a6 ` | ` a15fad0f35176ffea938ba75ee86383be93428a6 ` | ` d3474ecba9c0b307bc37ea6344cfce593ce828ac ` [条目](#entry-204) | gitlink-only | waylib-only |
| 205 / N6 | ` e17a03422776f63782cc9ddeb94bdb879651adf8 ` | ` 58745850aece14ce2d65ef262a9eeb5ba43c5781 ` | ` 32f5b112ea9a4d0e16e3592bf4664297072bdff0 ` [条目](#entry-205) | gitlink-only | waylib-only |
| 206 / N6 | ` 08fb9384626292da9eefe05bbebdc57ba5f26517 ` | ` 80845a1ccca777374343ddcc5e33d266d2c9d6f7 ` | ` 7957f97443449fd940d188a2319a34caf852e479 ` [条目](#entry-206) | gitlink-only | waylib-only |
| 207 / N6 | ` 700447dfa49073a8cea8fdba86c929171a97bb2b ` | ` b2689caca7876286ebe71d816c863d49fffcbcc8 ` | ` 924616655e4ed541cfe5f157d703f81eb42181be ` [条目](#entry-207) | gitlink-only | waylib-only |
| 208 / N6 | ` fa6c1816fc2d18e430fca57a5da9760e48c70a06 ` | ` 8d7a225fbd14fafb3e3e293ea7d50cd726ee5f47 ` | ` 56a6ff604a16df11d4787e788bd74e6a6bebab30 ` [条目](#entry-208) | gitlink-only | waylib-only |
| 209 / N6 | ` b99faa4272d5b51540fa0ce6bcac13fb16dad171 ` | ` ca3509624c0a02cf26139e8ce85969ec6f6e22ed ` | ` b7c756cef12fc05774a41b32c7ffc9f567de9a56 ` [条目](#entry-209) | gitlink-only | waylib-only |
| 210 / N6 | ` 8e41c92ee120806a59baf7347e9f13487e23bdd6 ` | ` 650c164c1563142280439e6f49d9cce427fbd757 ` | ` 30a2acc5f19c7803e691a356f54b85d994427817 ` [条目](#entry-210) | gitlink-only | waylib-only |
| 211 / N6 | ` 8b3fa373749ffd6da4b8500fca8883f43f171d1e ` | ` 1028e37dafb2cc7afb9a24797ebe22554827c7c2 ` | ` 70d315b206485d8d31dad6898204aa08e013c0ed ` [条目](#entry-211) | gitlink-only | waylib-only |
| 212 / N6 | ` 0202d8213967db6169f13fe42637fe9d35ab4d1f ` | ` 5b24b13ab1e3cb60b65f38f8079c532b6b117b32 ` | ` 0e9685826f6b4c70665e87b25a06b56992de385c ` [条目](#entry-212) | gitlink-only | waylib-only |
| 213 / N6 | ` b7e086318c74d3e39442fa3e30aa07ef1e0c7243 ` | ` 0b3636dae88736821457528853b9c72228bbcf79 ` | ` 76bf00442bb979eabbfa66d0ff14418b084de2e7 ` [条目](#entry-213) | gitlink-only | waylib-only |
| 214 / N6 | ` 18b4d8410b7d8897e0d723a85a60a1782adeb8ca ` | ` d1bf99b49991482a4343f3143161d7edfccd6302 ` | ` de42bc7a90ba3a1a502d6251a81400ff0e59870b ` [条目](#entry-214) | gitlink-only | waylib-only |
| 215 / N6 | ` 6dfa30759182985cad9215e1a56df24098706961 ` | ` 03c9faa0df437983742dd9e3588cb8e9ce1b29a5 ` | ` 6013a73bb7e443d223044c05e7be580969754303 ` [条目](#entry-215) | gitlink-only | waylib-only |
| 216 / N6 | ` c0ffefdd17ff771496458051a89686879768a182 ` | ` 26fb1cbddc0d5bc6837a6ca8874d8b9d274542dd ` | ` 78177b68153ccbbc65cb68a97224c48aa1368a54 ` [条目](#entry-216) | gitlink-only | waylib-only |
| 217 / N6 | ` 159aa593b87db474536c89b6cd75586fd0f88170 ` | ` 2e82fceddb17a4734fd71e9dee701f2de81235df ` | ` d74498ea452790cecfc97ba7249c94f0c1d29b06 ` [条目](#entry-217) | gitlink-only | waylib-only |
| 218 / N6 | ` d4e343cd04c5cbda3fe649b593cad22b41adff3c ` | ` 133bacf82d265162b070e6145ca0f84949f423ff ` | ` 21d157c501883ec3ab4d1c82cc567aad966c2e45 ` [条目](#entry-218) | gitlink-only | waylib-only |
| 219 / N6 | ` fcd0b60f3dbaef8e45ad1e2609811dfcd11c63b1 ` | ` 5099363808eb469eccbbb6de9989292f6ccfec51 ` | ` 58a2d6d3d46e1b4013f0ba0ef3bd42add944319c ` [条目](#entry-219) | gitlink-only | waylib-only |
| 220 / N6 | ` 094f8fa20e188f0da667df121b0eb9bb6f202ca2 ` | ` 198224fa5373fbf69287b2cf9474a5da9cf62f1b ` | ` 9ac4f1da1e18b29c08361007954770487b2e033b ` [条目](#entry-220) | gitlink-only | waylib-only |
| 221 / N6 | ` df2d519225b3fefb5c63cf6c9386b4f62c2defa2 ` | ` b51774765e343765913d44cf08744e83118da7ab ` | ` 167e28ab77de171f995819d670b0e3436ac0f287 ` [条目](#entry-221) | gitlink-only | waylib-only |
| 222 / N6 | ` 8ed92bbc78a136c4adb16182b38121ca5b44ed46 ` | ` 1e72bdf6a9b6a268f07d877d0feb51bf2036c025 ` | ` 1b0da6aac0d2f7c9bb43817e176174e7110c6b8f ` [条目](#entry-222) | gitlink-only | waylib-only |
| 223 / N6 | ` 5d2ed41d2be0afe22cd28ee05db3cd47305ca11a ` | ` 09a4aaee3cb0e7ae702c50aa354c8a4f33d35bad ` | ` 157ad0ec24094e58beeacb38efcdf792da28235e ` [条目](#entry-223) | gitlink-only | waylib-only |
| 224 / N6 | ` fa71f552d76b9565cc79f3a48768342f9186bd06 ` | ` 86356b17add9571b013f11432f85b26131ad0498 ` | ` b543ef933f7e785f047ad6adccb0fa115d4dac22 ` [条目](#entry-224) | gitlink-only | waylib-only |
| 225 / N6 | ` 33471be4c733a280bc804957c0bd307c07943e19 ` | ` dac95d2b10afb94aeb04b6fb4d55e543b00248ca ` | ` 48746f475a14ff83dc64b4b4ca409c685de1ac49 ` [条目](#entry-225) | gitlink-only | waylib-only |
| 226 / N6 | ` 682273cf854842c378362d2e167785898b256806 ` | ` 560b8f3544a7fd40fbd0ecbcc0d841259254e841 ` | ` 52e681cb4bbd348ffe4af6642d010ab9edc53746 ` [条目](#entry-226) | gitlink-only | waylib-only |
| 227 / N6 | ` 74da40725dca4808b943e17d5bce82b9ce87f6b3 ` | ` cefde07377a32b323fd2a6d71e52fbdc6de13d29 ` | ` 1528e2c65fac189eb81857ebb17c8bdb00a0af7f ` [条目](#entry-227) | gitlink-only | waylib-only |
| 228 / N6 | ` e9490f064a03e6c201149528e6c0c4c72f10ab86 ` | ` c14a456fb58697ad201bce67aeace869b3f881a0 ` | ` 29304f4502495c7c1b9d5c07414cb7b81c747d3d ` [条目](#entry-228) | gitlink-only | waylib-only |
| 229 / N6 | ` 5c5b0af13756a49fd922031a621465f01b73d7e6 ` | ` f7a1cc685d2a3782fd954580e50506773f316227 ` | ` caa0f11234979fff36ac20566357339c1d0a34b9 ` [条目](#entry-229) | gitlink-only | waylib-only |
| 230 / N6 | ` d42414caafb7b6627440a0665d371210c0d47e7a ` | ` 6364d3ad0fab19fa96ab0a9134cd40e10ca9356d ` | ` dbf154b328cf94a45e35e39e68abc1ee9e3e6270 ` [条目](#entry-230) | gitlink-only | waylib-only |
| 231 / N6 | ` 859718dc888c11841a8a460349ad5748c121e3e8 ` | ` 706564050ea892b967666d7a96a60532b5adc230 ` | ` c8f8384d8deebddbf3d7908743bb6efe15ffbdd4 ` [条目](#entry-231) | gitlink-only | waylib-only |
| 232 / N6 | ` 87d58d55d9bbd55f89c667abb8641b707fc593d5 ` | ` efb318004042fd6921f1fb46d9c315c8a698c261 ` | ` 3e397c34ddf92281062b10d3d155c606c3f113d5 ` [条目](#entry-232) | gitlink-only | waylib-only |
| 233 / N6 | ` ee0d9a7de7b275592767c8c3429b4fe472f79e20 ` | ` 4668a87a562c6b31e40d91bb0ad84fa959fb1893 ` | ` 232247f88d886bc4720d8aa92d9c6d778ff5f0f3 ` [条目](#entry-233) | gitlink-only | waylib-only |
| 234 / N6 | ` 73caa1c03a8b26eec23a253152f3ae893ff6d85f ` | ` 0e0d387031a7b095dd478276381ceed97f4b9e22 ` | ` 34eefa983f26491bcf3d27baece2a25af7c398ee ` [条目](#entry-234) | gitlink-only | waylib-only |
| 235 / N6 | ` 033a7c7b4278b88eec561d97307b111a7bbc0c06 ` | ` b11be642ce1573c35db03b3f7465da3aa7ee53d3 ` | ` b4e6513699f35015dcd96db7b73fc4eb8b9352e0 ` [条目](#entry-235) | gitlink-only | waylib-only |
| 236 / N6 | ` aa980f02c6e0e119ab271141fa42adecfae48707 ` | ` df946859c39247dca0e495451f344677ff3f2a9c ` | ` bbcf1d4997f7c2dd5ff121ae8ee364161e07263c ` [条目](#entry-236) | gitlink-only | waylib-only |
| 237 / N6 | ` d4dfa7caab388a3c682d86be0aad378851f7363d ` | ` 548d7fab8e70439d3fd8bcae8b2634d03e7ae8f8 ` | ` d988b1cdf1cc12f11740e5feee7fbe8bc8a869c9 ` [条目](#entry-237) | gitlink-only | waylib-only |
| 238 / N6 | ` fe8906bcfbf6eb65d0c68669ffd177efe282f178 ` | ` 017abc234dc80b17296492fd3ce5f80aa236064b ` | ` 5e71e56056ce957273ed7ab42a64ef682044fe6d ` [条目](#entry-238) | gitlink-only | waylib-only |
| 239 / N6 | ` 5ffc9a8b7bf68b5da60ef9f6cdd52bca9e8e1a6c ` | ` 8bc3019747ecb4af5ec2c8bf67ed2432a90f2ef3 ` | ` 0038748c15e5a84f3a2bf569eff60170f373f4c7 ` [条目](#entry-239) | gitlink-only | waylib-only |
| 240 / N6 | ` 9cad8d729fd3550040a7ece3fe2d4cfafd67e5b6 ` | ` d356a4d5f73f39e676d12259f1f4fd1c57d48c08 ` | ` 9d06f307721223ab84c0610e042c23a56cf53b9a ` [条目](#entry-240) | gitlink-only | waylib-only |
| 241 / N6 | ` c7439c3833d0cd35720a5d229617602e5ba5fcb1 ` | ` 2b66404a35c673e4e0b72a6a7280a261d01bf89c ` | ` 6d3bc12b97ed97368057174d7fc61b1340d5c088 ` [条目](#entry-241) | gitlink-only | waylib-only |
| 242 / N6 | ` 45194c916e691c9228f30d87085da35052b75a72 ` | ` 6015296a9f0dd854516a0a6f9625eca98aa4d000 ` | ` 412f33e565e11158057be57ef6046f72602ea72e ` [条目](#entry-242) | gitlink-only | waylib-only |
| 243 / N6 | ` 908ba59932df7cbe837af6280a6de083abcb69c6 ` | ` 23d9af69508fed3a13d659c7b1c0b584999fb4a7 ` | ` b4fcca336237a0cfdb0a62b4df2aef3553bb96e1 ` [条目](#entry-243) | gitlink-only | waylib-only |
| 244 / N6 | ` 564a3ca2e2e219480b75df745aa61aa706ec6e19 ` | ` 19c3c8cb3a8b957feb1b4524ffdac78c8ffa10d2 ` | ` ea4b8aa9513646f49ab84b1809923ff86a325bd8 ` [条目](#entry-244) | gitlink-only | waylib-only |
| 245 / N6 | ` 2b85c5d40accb13fc3acb33fdca64bc795e7c74b ` | ` 35b27a483a490f8fd15d81e377ee7626f8990367 ` | ` 29ccd138f6572251952424add96ca97f9fbc41a1 ` [条目](#entry-245) | gitlink-only | waylib-only |
| 246 / N6 | ` 276ea2949d7d0b42e6d9a28f186c378293cae922 ` | ` cd7ee22d3e370ccb18a393155c6d607cfced71c8 ` | ` b865bb07d2bf5a943b841cbac02f68325c40d082 ` [条目](#entry-246) | gitlink-only | waylib-only |
| 247 / N6 | ` c4c3d95a38040104339e8ed8984b847290df294d ` | ` faab1a2428f418efd050ce63b6c8829ac503a0a1 ` | ` 1a7ab86e77c711381d7d08d55802bcf48a981f39 ` [条目](#entry-247) | gitlink-only | waylib-only |
| 248 / N6 | ` f827a249077f26ad91928b581d3fc5a96af3ec01 ` | ` f515abf21a171f14f7ff552c6f4e09b2696696d0 ` | ` 46bf3361d5a3986291ca177fd618a7a01764de56 ` [条目](#entry-248) | gitlink-only | waylib-only |
| 249 / N6 | ` f23cb2387656aab8d243c8814a53da6c0a70db48 ` | ` 04955a3751b48cc1349f0f3dbea7b12a2ea96439 ` | ` be8f9274a06014d5c9c45691ce88aecbf196dec5 ` [条目](#entry-249) | gitlink-only | waylib-only |
| 250 / N6 | ` 5b8b45b08e13328031c464d9913eef55e39c91d0 ` | ` c1f7a7e99fa20e3680df36ede7e390e99869cfce ` | ` 43c5ca5643823f5b9ca57622617ab0e3df2a9e65 ` [条目](#entry-250) | gitlink-only | waylib-only |
| 251 / N6 | ` 529950cb158ad7a02c6ac3a446fac29d87028ab3 ` | ` 4537a4e3367eb34a4863346f6d2b3958a695e65c ` | ` a059b5edb7a293dc89cb0b2a6aceb4a42717cb2c ` [条目](#entry-251) | gitlink-only | waylib-only |
| 252 / N6 | ` 93864b26690744c7b9f9eba8d128acde6e98b379 ` | ` 06192bc5e3e9a8319080330d5fb38c21b5003691 ` | ` 63641c7162099432a4bb33011db099ad5dc49776 ` [条目](#entry-252) | gitlink-only | waylib-only |
| 253 / N6 | ` 6e63017817a6ce37cc822f527ba57ac222e9d2c7 ` | ` dbb8677b6d41c38f2dd55c115a0844b104d3cc42 ` | ` c939af0b217281c9232dde230aa7144b347a4be1 ` [条目](#entry-253) | gitlink-only | waylib-only |
| 254 / N6 | ` 8b61f805d33f81a7afe2a18c336867fc32b8620a ` | ` 12d443c072c1aeb2301b324fe6668133cf744e7f ` | ` 5c9e26f4ff5d0850eb5d961c09d694022721490e ` [条目](#entry-254) | gitlink-only | waylib-only |
| 255 / N6 | ` b7b7012f449273e29486ebdc9a4eddd5e76ec7af ` | ` 271b43b49b3cd62e2d8d977609b5866c1967f353 ` | ` fefd0297618a3c9327411e6355eebde2c6ade15e ` [条目](#entry-255) | gitlink-only | waylib-only |
| 256 / N6 | ` 86dbbae0f5f21fe7220137c59ba76d385399dc58 ` | ` fde7240b44c69dd2211e13e0f97dd58803ea4dba ` | ` bf841edb69b6b206cadea5c7bd448b2991d17643 ` [条目](#entry-256) | gitlink-only | waylib-only |
| 257 / N6 | ` 6dc50b9db882b034646f79db6fc49914f5fb40d1 ` | ` f383ab3899733ead50241f4bc3df8e17c66f08dc ` | ` 91ac826f226da9f5a671d93f3d5829558399e560 ` [条目](#entry-257) | gitlink-only | waylib-only |
| 258 / N6 | ` f02da149ffd4c801ab386b93f01061eec6eea06b ` | ` a12c8468fbf4317289d2ed44e4c54ee767cc9b2c ` | ` b52d37e523acff6b8e3273592b0767772705b4be ` [条目](#entry-258) | gitlink-only | waylib-only |
| 259 / N6 | ` 34dc93862257c1c9f69958379fd8d1e8b75e5461 ` | ` de1fe1cad703f37235073f94b8fbedee54b2ed1e ` | ` cc0ccaaf1655b2f022867cfbeb747313285cef8c ` [条目](#entry-259) | gitlink-only | waylib-only |
| 260 / N6 | ` 950bbb8fe1b23fa77e0953d40d76cfaf46f0d92f ` | ` 0a291d0073380a993493c8d8b93cb1c11661ecbb ` | ` 86086a7a051d4696c7d0d3b1a2581c1f55325ca8 ` [条目](#entry-260) | gitlink-only | waylib-only |
| 261 / N6 | ` 75c10a1391360aa29920a801f59ff7461912d6aa ` | ` 4aa4e2d0d036427fedd039834e4a4fc5e6c1b571 ` | ` 50d9b9cdfd92f9202ab567d4e178ff3e52944cda ` [条目](#entry-261) | gitlink-only | waylib-only |
| 262 / N6 | ` 635bf146b865db63416f82bd6092442de594f507 ` | ` bb292724b9b9ee07ae376c4dc1b889c0c56ce1bc ` | ` a3bbfe7c2ac3bb5d5647721b33657d9ff0508afc ` [条目](#entry-262) | gitlink-only | waylib-only |
| 263 / N6 | ` 8e64fba9494a4dc8c2c9845a2c2724c7632b81a4 ` | ` 363db0dbc2fb20224ea7a2e5ad3230bc1dabd5ec ` | ` 6d8842aaf556568dfaa2a7a15495b3f386002ac8 ` [条目](#entry-263) | gitlink-only | waylib-only |
| 264 / N6 | ` a378e058a4bd3bc87edf943504258c76f668ed9b ` | ` ca431b96f84283bd1ce7fb9767c745e3e557c9c5 ` | ` ac14a5b3ba48f0afeca76304af54d4b16148de68 ` [条目](#entry-264) | gitlink-only | waylib-only |
| 265 / N6 | ` 263e98177d78628e1aeb6d90dd9e0598db87454b ` | ` 7af02bfd16484d40303240387041c62747fc8fdd ` | ` 2e8ee72a7a6dd147984a3a88d95f883e5c7b31cf ` [条目](#entry-265) | gitlink-only | waylib-only |
| 266 / N6 | ` 437174b43a3832b1d812eb88af1f716d748197b1 ` | ` 953d859137c5e8d98723f7f5c187e693ff92bc31 ` | ` 331893bfdd7c48771358a8db6f02f9effb1e5338 ` [条目](#entry-266) | gitlink-only | waylib-only |
| 267 / N6 | ` 505329bf071892244a4e8b80e8595429f68230c8 ` | ` 358693ffe243d50b6a849f2c830a2f3ef83c8076 ` | ` 5a25b40c3a0c4615aa1cdcf66ba45669707807e1 ` [条目](#entry-267) | gitlink-only | waylib-only |
| 268 / N6 | ` 91921354b90f4eeadd031b2baaeeba95e9996644 ` | ` 69e81d1c6a1a275f956fbe617afc34133f17176e ` | ` 48bb13c8ee6c7b59a80a99b6d0479051f23e4c2a ` [条目](#entry-268) | gitlink-only | waylib-only |
| 269 / N6 | ` b66698bab2ac579ad52fb40e3438a45110f104c4 ` | ` fb6f8c5eb6cf0485b308f28514dc8625a1c92e4d ` | ` a8b4c51fb6ee320da65df0b18efb904edd8ba275 ` [条目](#entry-269) | gitlink-only | waylib-only |
| 270 / N6 | ` 52382ecfe26abb0987212c5d019770cfd29a38cf ` | ` 45993b851fe4f299636492faa00b4d52566d982c ` | ` 0ef4890bb77d07a4962c1a2005bcc05a154302af ` [条目](#entry-270) | gitlink-only | waylib-only |
| 271 / N6 | ` 4353caeb24222b3e9a9862997814d794ae00b94d ` | ` 1c859bdc13f2316ebd952deab4a47a3ea19d8f3d ` | ` 72e369f6d3b56d9fd5a9f8050cd27d04bf9932c7 ` [条目](#entry-271) | gitlink-only | waylib-only |
| 272 / N6 | ` 7b7c401f960cb323ac70ba3b3523f3f0df15970a ` | ` d8bdfbfbe64aa43bfe5049be719d30d1c8686abe ` | ` 2851ae97f00835f7e0854bc0069f3510dc385e3d ` [条目](#entry-272) | gitlink-only | waylib-only |
| 273 / N6 | ` ab94ac3465ed64e79b82c0c33bebc84c650d9d4c ` | ` 2d74f0462ad2a194b214c69092a1ba1dbfae4068 ` | ` 789350b65690a09a0eb4165fe200d500aed7ae94 ` [条目](#entry-273) | gitlink-only | waylib-only |
| 274 / N6 | ` 8cb8af048a6aab2dfe8e972ebbac757d18952ebf ` | ` 5af00710987f3bbf1a87899178684f0dc4f67c3d ` | ` 832f8b37f4577efbb92d0b03d7152fce60a46572 ` [条目](#entry-274) | gitlink-only | waylib-only |
| 275 / N6 | ` de8a45ad87af71675c2d1e8bdff0b84578e4afe2 ` | ` e464c31b6b7c85653173a02f6472cc4264de585f ` | ` 494e361c18cdf43534a07b6aafdc19ac09d2e8a0 ` [条目](#entry-275) | gitlink-only | waylib-only |
| 276 / N6 | ` 14bc196ab3bd402cfbf024ad7161ea740d9438d5 ` | ` 17a6d9c13d3d98039d652119bd9f9cfe39492b88 ` | ` 95338802c3174b0f3dfa215166e553743f260b9c ` [条目](#entry-276) | gitlink-only | waylib-only |
| 277 / N6 | ` 1b12bc8f66b4b00a3106978d5dbfdc32f79477f1 ` | ` 03ef3aab2fc02d636f50b5098252551df1dc7794 ` | ` 5547b4a50a480cdc14adcc81ff8145dbcfdc1420 ` [条目](#entry-277) | gitlink-only | waylib-only |
| 278 / N6 | ` 281b27d95f3c8a0530023f2f33e514c894a2a4eb ` | ` 1ddf3648ecadc85ffc7c00e4c9bc0ff9abab2d02 ` | ` 3c4e1ee8d72fd6372929ade67a39d399bcfbd3ab ` [条目](#entry-278) | gitlink-only | waylib-only |
| 279 / N6 | ` d9a79f78d0d3e7dca79fd1ec3c42bbb93b4d9119 ` | ` 34cf6e709d029400c3bebac048710a360c6b2f00 ` | ` aac09e833eb365c85d7717b2a5c623024ef43bfd ` [条目](#entry-279) | gitlink-only | waylib-only |
| 280 / N6 | ` 176a8cc2e8a5aee7d7f658a0e48aae7273bd0164 ` | ` f7b649c1774915f54e216503778feb21b39b97cf ` | ` 93888d169a47c665f177091460f2bc857c12c078 ` [条目](#entry-280) | gitlink-only | waylib-only |
| 281 / N6 | ` d1aad42faaf0e715d3ef79f329827ab6bdad8709 ` | ` ca18de3547d9d100cb60718fd2f1ee6ef0a17e7d ` | ` c5d1408b1cfb31e0406233c9ea991092ec2690eb ` [条目](#entry-281) | gitlink-only | waylib-only |
| 282 / N6 | ` 067a405aee6453f2be435febaeac6bb00fea3b5a ` | ` e2fcfff47df33d37aa07355140d049eb8a838e8c ` | ` 9b68323a5565c00c26f1c60ea7bbe1885d481373 ` [条目](#entry-282) | gitlink-only | waylib-only |
| 283 / N6 | ` 376af70c54377ce8266a194c98b8f6b89a07abb8 ` | ` beaae2c113dfab24091f76fd650507da0c6dd2e6 ` | ` cee008a6094cb958ee5b35189606cd496dfa43a0 ` [条目](#entry-283) | gitlink-only | waylib-only |
| 284 / N6 | ` f6962a9d32fe455341ece7d6c90b4dfb976f9755 ` | ` 2af6f2771ce543eb9ccef18c1135fe60b3a18622 ` | ` 58949a4a89491ad2d62c7f828a4ea8d040211d10 ` [条目](#entry-284) | gitlink-only | waylib-only |
| 285 / N6 | ` a193b80ad2a620584e4ef3ef276f0df67a9abb1a ` | ` 23ef71df172761333c0c1ba0d38f1488f8e45a32 ` | ` 180194f1dcfd4e4d52b1b3501ab9594870957636 ` [条目](#entry-285) | gitlink-only | waylib-only |
| 286 / N6 | ` 157c8e5c6d66ac8f8bf878bf9314cc18f796d576 ` | ` c0541f2bfd7c289962e0978e7077b1a579589f6a ` | ` 61426fa0b91a8ea79ccfeb00784772010b784b5c ` [条目](#entry-286) | gitlink-only | waylib-only |
| 287 / N6 | ` 8a1c9cb02c96da1e87b6648f729154c30d57dc61 ` | ` 68c0d26e0977c9f5318f2a1fe8f8b21801308b0b ` | ` 4b5cc8f4a41cc64ab9a58320cb05ed3b7d064d9b ` [条目](#entry-287) | gitlink-only | waylib-only |
| 288 / N6 | ` 6af85fa8f6fbec935f4395475f7af72e798ee51c ` | ` e9bba9f73624ee2009b73e630d98ae2187dc7e61 ` | ` aa407fc97c89c512b044054c947b500069faa7aa ` [条目](#entry-288) | gitlink-only | waylib-only |
| 289 / N6 | ` a8ad377c4b0933fda640a95ead1786e39a479152 ` | ` f7417f36b50f9c335b11544872d5961e47a63272 ` | ` 00b092c18591f708685043e9cb5c187021f24909 ` [条目](#entry-289) | gitlink-only | waylib-only |
| 290 / N6 | ` ee51b8c2d6ab1f641b3923d85cf3f3d400806a6b ` | ` c2190191e8e8d1d90211ee826e9da92d0c006fa4 ` | ` d07041af35fdb7e381996279e720cf2fd7c709a9 ` [条目](#entry-290) | gitlink-only | waylib-only |
| 291 / N6 | ` 0ad625e31c0e3db7cc06ed5fcb78bdc264bd8963 ` | ` 2ebb8b950e10cc12f3e4cfcedb2b77f0740d3779 ` | ` c80e529bfff58ea003287bc5fe5a02b5f7040d14 ` [条目](#entry-291) | gitlink-only | waylib-only |
| 292 / N6 | ` cd468f22a2d22b122ae7f90a106b2e17be4425ed ` | ` 8c0383f08296843f0ca018de7d9c015cfbc89ccb ` | ` dcca27213df1e1744cc76e01ef5c5282fb2a8b84 ` [条目](#entry-292) | gitlink-only | waylib-only |
| 293 / N6 | ` ec2cc0d8f046917b349beec7427acebe1e9fb92a ` | ` b0df667bd1f83791dbbfbffd321e57bb65fd6478 ` | ` 7f3de74732416e8454a798cc0e01aa936edc4c1b ` [条目](#entry-293) | gitlink-only | waylib-only |
| 294 / N6 | ` 74ddba3ad69645de9c9d0574ad1b51f31f6acc15 ` | ` 95de8d294ac88a432580842290894f67f6e84383 ` | ` be5f3cff6cd846e2c3578dd9e7c65b71381251ad ` [条目](#entry-294) | gitlink-only | waylib-only |
| 295 / N6 | ` 98311478a1842967c73b02182288a3d8f6794605 ` | ` 7f816077dc42d96038d31274024e68a24708093c ` | ` 99eb280a48054145e29d034573f8715b4ab54adc ` [条目](#entry-295) | gitlink-only | waylib-only |
| 296 / N6 | ` 7975208b038626a0df83fc285aaba339c52d8115 ` | ` 6a1328b6b6e24cfc0cbd406b9af390a3654dbc1e ` | ` b7d8183b5ab7cee1c9fa8125b6e14f740413cf8b ` [条目](#entry-296) | gitlink-only | waylib-only |
| 297 / N6 | ` a6acfaa2493ccfb4848ad4455df0e048d0f250a0 ` | ` e4c0c57a1872b1117958ea2ca07d2124c6b45e6d ` | ` 34c5ccfeab948c1bc147500bc91fbd483c1fb735 ` [条目](#entry-297) | gitlink-only | waylib-only |
| 298 / N6 | ` 062478639d1a54ce37b217b56ab0da36cdd567cd ` | ` 87ceab53f54d91a85d2aa4e9f19f98e4132fc8ab ` | ` ad97f50fc149aad7250542ce0136157260071e35 ` [条目](#entry-298) | gitlink-only | waylib-only |
| 299 / N6 | ` 6c857fd08e4b9f38cf859052a51e0f70b0bc0534 ` | ` abbc6a72b7c0fdd04abe1da267f67b4e245d549c ` | ` c9b8092c287ff3c87064efb1713a5b1801a5d1ed ` [条目](#entry-299) | gitlink-only | waylib-only |
| 300 / N6 | ` 5706871fba99a052671e17f8f9ecab92fb5927a3 ` | ` b8e44bca4cc41a3cce7077ddc874ad9c67f7ee59 ` | ` 50a35a22550f814a31c911b654515ce704f66969 ` [条目](#entry-300) | gitlink-only | waylib-only |
| 301 / N6 | ` d8a3e90459942b4af5d0869901d8f1be12fbc40a ` | ` 68bf6d9b22696934eb5978955e75fcfefe38fbff ` | ` 1c583946cbb9fa982b8e26e15cdc6a2278f69799 ` [条目](#entry-301) | gitlink-only | waylib-only |
| 302 / N6 | ` 7a6e9e84bb9a20d6d8d4c170b40689b05044176d ` | ` f5505dd3787c586526bebae29e2e74aab194513b ` | ` 2ce3ca69bd7f46c986ba868ca98e99486fe2f601 ` [条目](#entry-302) | gitlink-only | waylib-only |
| 303 / N6 | ` 185dbab6bd716e5de74581d12a903e3eba742f83 ` | ` 8b97bba533ac7e237e198a211fd8b09f6ab4f528 ` | ` c6036f5ba8c1190c8419d92f4e8c5421a261e5c1 ` [条目](#entry-303) | gitlink-only | waylib-only |
| 304 / N6 | ` b134d3316de3017b1b520e4dd0077e703b50438c ` | ` aa0d0878bc23fb07ece7e58780fcc3000462f4e6 ` | ` a67ca2959eb32efec463438d33f869b8dc345795 ` [条目](#entry-304) | gitlink-only | waylib-only |
| 305 / N6 | ` 57c36469b466184c578da62d73bed578e4783258 ` | ` f510a2ccde9a9b60c2af261b303c8b5f257c3bfe ` | ` b07341aba6873e2000c905617c6daa6f2c49fb67 ` [条目](#entry-305) | gitlink-only | waylib-only |
| 306 / N6 | ` 2bcefab7736eec802cee9293c3e1ef45b94c5391 ` | ` c1e9acebb008815accbc4beb68efd1fef5b3411a ` | ` 76ba22e9daf87be7edc4a9fca6012eb5a0162d04 ` [条目](#entry-306) | gitlink-only | waylib-only |
| 307 / N6 | ` d6a6ecfb0ba65b1e0142740edc046ed95a45c733 ` | ` eade18a067fef4f80ae0b67dbd46a77fe63b2331 ` | ` 657f379f9287ec44cb160ce60516376aaa237702 ` [条目](#entry-307) | gitlink-only | waylib-only |
| 308 / N6 | ` b22ff363877fff122484669b129585f21fb1789a ` | ` 1e2c4719fb29690f46e2fc5923b96a2b12ad0116 ` | ` 88c92df65dbb870732588af1cc31fd4346bd1369 ` [条目](#entry-308) | gitlink-only | waylib-only |
| 309 / N6 | ` 5b312c3ecee51220bdd55cf7ac94482d45039f22 ` | ` 372e6f18e684003f7ec3926d470786ce022431c0 ` | ` 651a758800b465952c1d8f27675a52c4f18a92f0 ` [条目](#entry-309) | gitlink-only | waylib-only |
| 310 / N6 | ` 2db1217d9547190f1a0636321ac9d92018a18511 ` | ` 720b8dbf3bf7654e8747b94708e62825b98b1a1e ` | ` 30283e60da9f64f8ff548b8ebd0a46828d8a51f5 ` [条目](#entry-310) | gitlink-only | waylib-only |
| 311 / N6 | ` 2016ffa81ceff6c6bbc6e95f53cae5bb8a101d66 ` | ` c8af1be28fbcaca68737a30d9e2a32af40340556 ` | ` ac07f3647e4c353ed7bbf0c34908abb692316b78 ` [条目](#entry-311) | gitlink-only | waylib-only |
| 312 / N6 | ` 2b150ee90c8091c9f9a798521e566b7fe3dce935 ` | ` 31b234852aeb053bda30d8511e3b0d481a0f0f11 ` | ` 3a961d238c82737c11b23fcd14897df92b29065a ` [条目](#entry-312) | gitlink-only | waylib-only |
| 313 / N6 | ` 5937df5c87b4785cba5b8a81886f4850d5dd61fb ` | ` 70cc85201ceb79706c3294f21eeb8c425ceddc1b ` | ` 39496aa77247e776b50b5441bafddba9143f2bab ` [条目](#entry-313) | gitlink-only | waylib-only |
| 314 / N6 | ` d842378e12e4a35671be9d5c21d37cd08d13c459 ` | ` c90b7d05635841c6226a5ebab62501a1b3c75584 ` | ` 7aebbd9d87e206f547e1350af75950737edd439a ` [条目](#entry-314) | gitlink-only | waylib-only |
| 315 / N6 | ` 90691cdea7530c371e3805e28b479c06b8c04aa0 ` | ` 6e4ef5c068055fb1f723f5c45683babb951e9944 ` | ` a4e8ac77be3a1e2fc29d4af7a9b7cea437f380e3 ` [条目](#entry-315) | gitlink-only | waylib-only |
| 316 / N6 | ` da21f4e5915a14fea778d9fa038fb434f893d4e7 ` | ` 14a6891d06a03c93f87af4477c8d4d5b1eb6ec0a ` | ` e5dcab202049de7bee386c71c5957f1cc8e8e306 ` [条目](#entry-316) | gitlink-only | waylib-only |
| 317 / N6 | ` f7face1e13784f9b4de186ccffc70891c0fe63d4 ` | ` b50a34f54fb1579d40ecd2cc6a50789212ed8a04 ` | ` 2de8d4fb7be37e4809b326bd2884a2ee2a7e4997 ` [条目](#entry-317) | gitlink-only | waylib-only |
| 318 / N6 | ` 81aba2cb86984a3be3b18bdd56b7d7fd14e6f7dd ` | ` 8ff3e75c15a72bb63db67ef922971d16fc201e30 ` | ` 447834bedca70f05578b2c3728e5ce415c89dac6 ` [条目](#entry-318) | gitlink-only | waylib-only |
| 319 / N6 | ` e967582c197f412fc46eab0890e8181de7455e8b ` | ` f836ee5dc29637559537c508e2484c8f6de6b89f ` | ` 42b50405a9da9ad7a3d2207aa5e848f59a568d76 ` [条目](#entry-319) | gitlink-only | waylib-only |
| 320 / N6 | ` ba5abbbf116d925c10ce8f9f3113849df5d87aa8 ` | ` 41ebc23410491decc554c026d9cef0ae28431552 ` | ` 9c6b3c922bce2a308daac0c3f0f0f35e74ed17bb ` [条目](#entry-320) | gitlink-only | waylib-only |
| 321 / N6 | ` 4ea7c83c74b513e9f2113805e58ffd761593373e ` | ` 952dec77f3cca1e72b7fb130164a751c79928e5e ` | ` 9b28550b923a8bfb7bbb7084a491a512b0972743 ` [条目](#entry-321) | gitlink-only | waylib-only |
| 322 / N6 | ` 71c789fbe3542417423e61363791d565240c9da0 ` | ` a09c4bfa727f2f3e6f39879af1d499420af4141a ` | ` ccaffc93fc93a1dc215ca1f75b13bed77fb17693 ` [条目](#entry-322) | gitlink-only | waylib-only |
| 323 / N6 | ` 4b83bf88e9e763439c03a01e733e0946e0b52cdc ` | ` e8ef439595713e1a3ad13d3bc4f588477efa579d ` | ` 8394128a0a3596ffbde00aaa07cd0cb835670741 ` [条目](#entry-323) | gitlink-only | waylib-only |
| 324 / N6 | ` 4f0ce89fb2c884c5109838d66a6e5f24d2383e5d ` | ` 8eed4a788d3f8f7a6cf631a66ded408f6bae9a85 ` | ` 344eb8798615835499798f53400f9f639d9d50c8 ` [条目](#entry-324) | gitlink-only | waylib-only |
| 325 / N6 | ` 4c0f2e48eb8c07c157d541770862f10887d05201 ` | ` 1f1ebda328e32a23a0924e292d23b85d9f077ae3 ` | ` 8606a1b93364a43cc07bd33afbbf80963c0f074e ` [条目](#entry-325) | gitlink-only | waylib-only |
| 326 / N6 | ` 067b0ade78281960f9e31aa4820de0bc86883cf8 ` | ` e6d7323d7f8aecc93e05b9570b5fce523558c938 ` | ` c2296ad4d7fbc7592eb4d0dbd8b49d34ddb8195d ` [条目](#entry-326) | gitlink-only | waylib-only |
| 327 / N6 | ` 75d29da9934335df1a7717be0d795765e46af7c7 ` | ` 9284c6a73e9f3ca3df1425671b3a541360870004 ` | ` 114a2fa26ceadcbc90a235a3b2c4e510b0f52646 ` [条目](#entry-327) | gitlink-only | waylib-only |
| 328 / N6 | ` ad86e8232cf0a4304b39f03826a85c8d99daa4da ` | ` a1561b50d7b5557afd3974e31f22335ba99f99ce ` | ` 084bee35f3dcaf2bf8d512d515203bbff5ad70a3 ` [条目](#entry-328) | gitlink-only | waylib-only |
| 329 / N6 | ` 76e9d812c4171953af224eb9c2261ad4d406fc07 ` | ` 5345c59e37c5d2f0e6cc09659d2092807111efb1 ` | ` f1fcb4bad6074463539fcac77aeaf91aa251467c ` [条目](#entry-329) | gitlink-only | waylib-only |
| 330 / N6 | ` 0c10122d1ebb57b0643585fc2c7528d5d7cdf36a ` | ` d8faed4649f1137d37032e735787fa0112cc0cfa ` | ` e51c6487cdffad26bd619c413d37ffd09c452039 ` [条目](#entry-330) | gitlink-only | waylib-only |
| 331 / N6 | ` e9c267ff80ded1d3d9aad35557242b393ffba4e6 ` | ` 7920017a659a56bde3faaff7f9cfa9da9db52f4a ` | ` c025ec667ee9dfbf4b56bc130269e5130115b523 ` [条目](#entry-331) | gitlink-only | waylib-only |
| 332 / N6 | ` b00c4f4321a6811340eb21790513eaef257daad7 ` | ` 78cb69150805df9257fc15af60540b4baa219824 ` | ` ed546f1542dcb04ca0f0748c43ca1725681f177b ` [条目](#entry-332) | gitlink-only | waylib-only |
| 333 / N6 | ` 26876224f2460506f1eb0a6ca43ed7910c3e9a4c ` | ` d23cadd91c45960de324fa0d6df985420f738062 ` | ` 936631b80d5805cd7587fb9a76bac61ff2ff812f ` [条目](#entry-333) | gitlink-only | waylib-only |
| 334 / N6 | ` 39f129f848fd5a310087dfdca21f65912b755eed ` | ` 4de4f559ffb987d25a0403714208aa18fe9ad3d9 ` | ` 9e01af0b314903de42242b1f8f033deeec84a603 ` [条目](#entry-334) | gitlink-only | waylib-only |
| 335 / N6 | ` 43c1fe1ed8f964937cd59101f3a0dae71c2aaac7 ` | ` 5ddf0140934254b5d6881841ab788f3f25027d9c ` | ` e44c6a4d03c798256cbdbc3158f441e652417998 ` [条目](#entry-335) | gitlink-only | waylib-only |
| 336 / N6 | ` a8ebb8932f8f28fa247f54e394db0133f1363051 ` | ` 64d1e755fb3771294b97a6cd471f5d50276dba34 ` | ` 29373194fca092344904817f2c20c5e113df8317 ` [条目](#entry-336) | gitlink-only | waylib-only |
| 337 / N6 | ` 36d6251519cb258e33455dcbeee700b29c818a80 ` | ` 8d127871bf4209311714f62c81f222c8612733f3 ` | ` a888f6aa6a79afd2e1784090d2b56aa47c2d957c ` [条目](#entry-337) | gitlink-only | waylib-only |
| 338 / N6 | ` b5bfbe09427cf35324917c2cbc2606490bbb0a57 ` | ` 4deb7dbb518a4ee874469d61b5f3662a8c11ec79 ` | ` d5c2a8ea0941c5951f36417876f0a38db9259ce6 ` [条目](#entry-338) | gitlink-only | waylib-only |
| 339 / N6 | ` bc8eee2feea24b094f952da1c8c5dd31ffd2c703 ` | ` 6b9b3c84baf449602350e56f486783a3524a8994 ` | ` f50be821ee6d923e78751f09fd3a078f6ddde67f ` [条目](#entry-339) | gitlink-only | waylib-only |
| 340 / N6 | ` 5d82753f7c09aaec904c85b54225b64301afe61c ` | ` 8ec56b0823972a3d40d89e3f7286593b9caabf29 ` | ` 30ee81905f8a0f14c009dfbb695fdbede77ed31e ` [条目](#entry-340) | gitlink-only | waylib-only |
| 341 / N6 | ` b174ad188ccd15d8a3121b97a9cc36c6a2f67fbf ` | ` c48a8b7e02159e3c3f67572a85774ab9af677406 ` | ` 9ec56b0a0e1a5ffd0cdf28e5d0b7ff1d6a4ee925 ` [条目](#entry-341) | gitlink-only | waylib-only |
| 342 / N6 | ` 58f9eed9aba894fe667600c3e00a7310da425099 ` | ` 5a4bc8a7dafa02cec7c2f9e218c3fbb901215665 ` | ` 13cc75567aaa4c9bddf9e1b4c6c650c491b474e9 ` [条目](#entry-342) | gitlink-only | waylib-only |
| 343 / N6 | ` 47b86e3a72846d16bc15de91d9e25307e74a6f9d ` | ` e9eba16a5370e52993b79b8c1345e4136396e385 ` | ` 9c86ef3e8325d97635497a2bb858e9792676b0cc ` [条目](#entry-343) | gitlink-only | waylib-only |
| 344 / N6 | ` 6cc4e12f5165d20d987ba17874e9082c96b31092 ` | ` 63a6597dcfe276f1259929de71da6099061ec460 ` | ` 90f2abdc72afe54382604a0e049869a74e37e9f1 ` [条目](#entry-344) | gitlink-only | waylib-only |
| 345 / N6 | ` f1a83816508406225f8e5658e32d7e5a52066daf ` | ` fa298baff4874800cef63babe839b89728f37dac ` | ` bcc82dd5c00fd9ff770254f10a0f026cd25ba234 ` [条目](#entry-345) | gitlink-only | waylib-only |
| 346 / N6 | ` e2f55b8c3b12ee79a38c3140c31c3d7d22656a3c ` | ` b0b7c3bb45af5eec9f65a484967f8317d7fc9f92 ` | ` 2fb00f544e96d31aea0d93297f27af5b3d582adc ` [条目](#entry-346) | gitlink-only | waylib-only |
| 347 / N6 | ` 389983c28b815abf4a3c963de2dce0ddaffc0986 ` | ` b700b81231c4a4caeffe3da31600eeebac2d1034 ` | ` 9a88afde1f46e50e0eada648c55c680d264f4041 ` [条目](#entry-347) | gitlink-only | waylib-only |
| 348 / N6 | ` 4b62fd3265ddbc26db3c6c7d062bf102fb6c7d9a ` | ` a470d1b526d1e863573e0175c05837e0b6b4399f ` | ` 7ab27c9c7f6648899f18c669ea8db8d66f912fc7 ` [条目](#entry-348) | gitlink-only | waylib-only |
| 349 / N6 | ` 8b3d05ae4538d8d4cd72d5d63ee3109d6e76e32b ` | ` 57818d5dfc310240ce91f9e0750d2fe765d7a778 ` | ` aa37c75b7ca2e75de2fb0db0f7afef55ccbbd165 ` [条目](#entry-349) | gitlink-only | waylib-only |
| 350 / N6 | ` f5243d5d08f98aa662592fb94c9032ba21bcb343 ` | ` ca902c55fe610907c74ec30ce9a13ca4003f6a47 ` | ` ccbe31412220d9a03e0d6d08afb2127e14db8dc5 ` [条目](#entry-350) | gitlink-only | waylib-only |
| 351 / N6 | ` 48264e43b25daf9f396478ed753be4a47533cbc6 ` | ` c986835fb9e70b385fdfb65346f26a46adc3f3de ` | ` ba84a23d38e2c41aff16abfe143a135b15179393 ` [条目](#entry-351) | gitlink-only | waylib-only |
| 352 / N6 | ` 82fc3c6fd467be4b146db30daeae46e7c17857f3 ` | ` 484b993fd585087db10c2c0c084fc49a94a24ad2 ` | ` 331558aa00a3b53b88ddd97a8bfd10a84b4fe5ee ` [条目](#entry-352) | gitlink-only | waylib-only |
| 353 / N6 | ` 6ba97a939ab4869d29102b4539ad9a4f1a9e8cae ` | ` dbce0505ed3d5706e0ee58ea8a5d5b93f5f22c1c ` | ` 57a45a1b87e3c5158c4db4feda67b36791661923 ` [条目](#entry-353) | gitlink-only | waylib-only |
| 354 / N6 | ` 83fe6dd04a62bdb7f28406b90f61a0cc921e36dc ` | ` b2e395225c7728236f44e4043457a69a4e0b6c2a ` | ` 76945575c1902a7a7c38498d97011a41c012bdfe ` [条目](#entry-354) | gitlink-only | waylib-only |
| 355 / N6 | ` 59871dc496250d6b03de9749a4422098e8f18906 ` | ` ba50226694a0103ad8dd4e34115ccbaee980e8bd ` | ` 42dbc70aa923d69231d2682293989ec27344384c ` [条目](#entry-355) | gitlink-only | waylib-only |
| 356 / N6 | ` 7774ea8fda1917293324caae6922529bc1a7a846 ` | ` ea32e25fd4a5f627715525d6c742ae61ab3def13 ` | ` f3291c84055ff827ec9eed3352336ade7ba4ff68 ` [条目](#entry-356) | gitlink-only | waylib-only |
| 357 / N6 | ` 021cc6c2cf8255c98c74b4a18b7945de424ac65c ` | ` 01fe53ba9f00f8343b59f7a29b9737f547103ed2 ` | ` 6393f9c16b071ffc19b097af76e4df73a7ab502a ` [条目](#entry-357) | gitlink-only | waylib-only |
| 358 / N6 | ` c852ee8d9ce7dc8072f1be44b1349f17eda236de ` | ` 12ee5f35bf753d2f48f32e09b5f571e8f1fa9cd4 ` | ` d8d844979b762d79f2e9cf55aeccc7506cfb36fa ` [条目](#entry-358) | gitlink-only | waylib-only |
| 359 / N6 | ` ddc9c388e4567b395043144773ebf06251178895 ` | ` d2e62cb63c789e62ae5f46d30c9211cca7263dba ` | ` c77c5549d77dcd0965eac8523887df3ef02c7e64 ` [条目](#entry-359) | gitlink-only | waylib-only |
| 360 / N6 | ` c93555dc03169fdbf42ab4aaf8e7bb1a74904084 ` | ` 8119bdf83523dc31b012c7d8918d0cf63f8440bc ` | ` 68ca12a70353f32975bbac30b8b3dc8abbc4368a ` [条目](#entry-360) | gitlink-only | waylib-only |
| 361 / N6 | ` fadf5214d54853c1852e5be59e9b569e4068adf6 ` | ` 5bd260029e1c91783b693438d6b0f5f2e65f63c3 ` | ` 58be65f5a8b25e0936653ac084469905a49ca1a1 ` [条目](#entry-361) | gitlink-only | waylib-only |
| 362 / N6 | ` ab75ae1c5270a293dc63a07819982896abbc58f5 ` | ` fd1deba5881202104233163a521d821fdd462bd7 ` | ` b45304ff64778f67b12754854f9e676f8a81bb90 ` [条目](#entry-362) | gitlink-only | waylib-only |
| 363 / N6 | ` fd27ca253c30c4f08e7f31af1631c69824741b13 ` | ` 3f8458739e81f8814d5d7521b578bbc4ff776225 ` | ` 9ffe3104a356ed5419d4d466ee75fb024ba33172 ` [条目](#entry-363) | gitlink-only | waylib-only |
| 364 / N6 | ` a3bbf452fc9968d58d8c6e8c5eea7152d9ab867c ` | ` 2f5e66ba1856fd248d0abf01f97f8ea71768d556 ` | ` 7891c981be27e7514f43ad8a8a17b1f221baaa89 ` [条目](#entry-364) | gitlink-only | waylib-only |
| 365 / N6 | ` 26af21548c5d80dc1142f5c44557833632c4ff5d ` | ` d0a442c3e7550d068a2341ce38c0fbc26cb80e91 ` | ` 5cbbcff6541bc809072f2d86bd441dcb02fb1b3a ` [条目](#entry-365) | gitlink-only | waylib-only |
| 366 / N6 | ` bd6b287ac9d76591a55f554c0bdde1b3832a2309 ` | ` 10c32d86b4acb99379c13898f16ad6bb6dbb0884 ` | ` 3ec4283130ed887ebf651ac4b5ec2dfd7f494c98 ` [条目](#entry-366) | gitlink-only | waylib-only |
| 367 / N6 | ` 5d3fb87c4b682ee30b0633166127e2dac28f114c ` | ` 079ee9a9c4f915f86253f229098686525cf1bc0f ` | ` e82fbe80a5840a6908cdec24c4dde63dffffc04c ` [条目](#entry-367) | gitlink-only | waylib-only |
| 368 / N6 | ` c2390909a26d9a9fc3c246c551ad80a69a7b66ef ` | ` 83f80cb193ba3a5f4148b303e5e5e111084fd352 ` | ` 8b0d7a188fbde3aa81fe48307e9d9b0fe2c7a3d4 ` [条目](#entry-368) | gitlink-only | waylib-only |
| 369 / N6 | ` 71270845bf373f80251e45756a8c286318294cc3 ` | ` a5bb7e1e1a06b7655a568089f417f700151223fb ` | ` ba8dccaed3a138b9a204e572b1f28c4df6ddb6c5 ` [条目](#entry-369) | gitlink-only | waylib-only |
| 370 / N6 | ` eb77b4b14501c40f1b1de2b99fb8bac620ee4071 ` | ` b7b52eaba2e947d868bbc033bd440841a3d90341 ` | ` e122a8822f7ce5ddbce9103375af573a102c044c ` [条目](#entry-370) | gitlink-only | waylib-only |
| 371 / N6 | ` 7a8f3e20c4cd9a4d66cb804af2a00f2d385a7c5f ` | ` dbfcfa3850f1ca564455a3b2f901d230052bfc85 ` | ` 20286a49a5f1dab357ec5a638a3de8debdfd7cb0 ` [条目](#entry-371) | gitlink-only | waylib-only |
| 372 / N6 | ` 6dd43c98dde630107bae193867bc4f6d69cdf092 ` | ` 62feb013defaa5f87d40f01171012a9208670c77 ` | ` b2596cc7a17095820237975c9ac79f64e06a6f1a ` [条目](#entry-372) | gitlink-only | waylib-only |
| 373 / N6 | ` 3e2c4ba46b2a4048b8e7beb961080920c7ef0ea7 ` | ` 0062950c4e2bea153593af8ae2d87b94a3f9bf0c ` | ` 5ef1edae59fc3d4e5e2a853117c19fd1776e833f ` [条目](#entry-373) | gitlink-only | waylib-only |
| 374 / N6 | ` 99fccac3fbc2267c2750508111f70639ffb0ea75 ` | ` af76f350af6446d7520b2c3156f040bd7cf99665 ` | ` eb45e900c0e93c61251379cbae57ecfa8ab6ae7c ` [条目](#entry-374) | gitlink-only | waylib-only |
| 375 / N6 | ` a69221cdcccb767a6167b5854239ddc519f27788 ` | ` 1f5bb2bb35ca720a1856b1abd97770acb69437c3 ` | ` d7f82ea567cfb2ceed502a59d3151ea44c0b7c7e ` [条目](#entry-375) | gitlink-only | waylib-only |
| 376 / N6 | ` 1f07ad74867449605c595af816f92dd3e73bcce5 ` | ` db94577f79456aafe80c629406bbd3470161a85d ` | ` f072ded8d436dd90f6daa2c2725ee1fa34bd2bfe ` [条目](#entry-376) | gitlink-only | waylib-only |
| 377 / N6 | ` ed9c8498336eeff3fd9502740ec48191b2c6d984 ` | ` bb29268e26fe908c3393d35cbbda2db626bb66d0 ` | ` 9657647d5ae4382cfbd802d0cb8bccf5adfdb516 ` [条目](#entry-377) | gitlink-only | waylib-only |
| 378 / N6 | ` 092a194ac64c581e62bd64ca05c904d01b143296 ` | ` 29b943872a50d3c5124dea56e409f8e6d592535a ` | ` 90ec2bc1e8202ca49ea6ef07691e17aff896fc44 ` [条目](#entry-378) | gitlink-only | waylib-only |
| 379 / N6 | ` 50f1a3b7acc17d93ac453b95b31db4b0f14eb00d ` | ` 292ad7396dce15c735fe338d9dd384a82ca487de ` | ` c94acc2109f0dc97141e4ed2590ef5c19699be6e ` [条目](#entry-379) | gitlink-only | waylib-only |
| 380 / N6 | ` a05e29aa1f38147a6795a90b3572e9ae00b1d523 ` | ` 79726897b933ef00e1058308510435addb1e31a6 ` | ` 7d93d454d4340fe1acb1ef05c37267ea47a19e3f ` [条目](#entry-380) | gitlink-only | waylib-only |
| 381 / N6 | ` 6ca4dfa6fc6fdfe86af2adbb5d9c8c907b6d6c15 ` | ` 6e69d9d9265038ca481d05c4f34537cdc64b7047 ` | ` ff9b126fc7ea93235089ae3532364e3e0d7d1cf0 ` [条目](#entry-381) | gitlink-only | waylib-only |
| 382 / N6 | ` f2b078c4f9d952d9115904183c11a187ffdebf1a ` | ` 67b5f3a0c7558d11076535acc8a2a753521ff695 ` | ` 8a23737046c95d6efd280b41390e12c6df6bc83d ` [条目](#entry-382) | gitlink-only | waylib-only |
| 383 / N6 | ` d8728e7e6240203c615eff349735f3daed8429c5 ` | ` 7ee6dffe38169afccf1d518da0a9cc89ad63328c ` | ` e37de2693fd4153bb8fd9736a605be25215509ec ` [条目](#entry-383) | gitlink-only | waylib-only |
| 384 / N6 | ` c2e66806de72b0a4a12220a752e4c69386a946fc ` | ` 5ec1b80437c801bae0a6c09ad90cada385e8e7cc ` | ` b3b23a7770a5855226896d3acc7394b62b836ef6 ` [条目](#entry-384) | gitlink-only | waylib-only |
| 385 / N6 | ` 59d835a1f7b3211dfc09070ea0aa7a509c125e45 ` | ` dd81b8aaaac13c9e7bf2a3cca5216364fa351b89 ` | ` 0f9dc6d7a10ae711afe208cdb6fde64e0fb0b113 ` [条目](#entry-385) | gitlink-only | waylib-only |
| 386 / N6 | ` 2870ec3689bda747464e5127b0d87ccb13d5e292 ` | ` 3ada81126f17ed1192c0f4101bd4c822fc19dafd ` | ` 0a57af26c65950601b06a01d8537ce4c01f263f2 ` [条目](#entry-386) | gitlink-only | waylib-only |
| 387 / N6 | ` 28d97085e61eaa1c7fdfca9158d741508d74acaa ` | ` bbfacb02940d4455d47c88a880ab3e0b4fe512d1 ` | ` cf66f597b27c9ea8c4c8007d6303a26c4defa2e4 ` [条目](#entry-387) | gitlink-only | waylib-only |
| 388 / N6 | ` 6f77ec93958ceaf024988b7e3d074fae0690b69b ` | ` 35a16141290d52bdc05f3bb2710717fb8687f9c5 ` | ` 02a604d4d31a87739ea49a6672ab03dbbd1f957c ` [条目](#entry-388) | gitlink-only | waylib-only |
| 389 / N6 | ` 4864dabb6453b3eb7041c8e3b6703a183ecd565d ` | ` d6c153b7d26792bb696252178eaaa6ad79e5f0a8 ` | ` 94935594ef29f3d7746a62169d3adefe5cfe1dcb ` [条目](#entry-389) | gitlink-only | waylib-only |
| 390 / N6 | ` 4d23ec22fda34f1ca2670bde9ab4ede3184863bb ` | ` e0e48767434dafbe93df6f21c3f56d8ae5eda6aa ` | ` d411d61b5f41555f3e2c3c8a07f69e0e856fdd96 ` [条目](#entry-390) | gitlink-only | waylib-only |
| 391 / N6 | ` c36184c982fa24b4a4d234d361b01982ed7bb984 ` | ` f33ba2538f1eb994183cb07d5b23cb3595afc3c6 ` | ` f0bd11a7a917a4b9573ac4c106e9994e1a4e0511 ` [条目](#entry-391) | gitlink-only | waylib-only |
| 392 / N6 | ` 9d02d0388ca2cd519deb342fbbdd290b67a9f6cd ` | ` 1cdaff2807a44ab7dfbbe16bb7a3d3677946d32d ` | ` ca4dbc1b1c460a044f7c6afd49a53c3f61a4159d ` [条目](#entry-392) | gitlink-only | waylib-only |
| 393 / N6 | ` 7b5eddb314e66f4fe69418fc3ae1ffede42d7969 ` | ` 6080219d9e6526fdc74283bf5a7c9cbd0991ae9c ` | ` 7da32fe003ed1cb41816afd5c1210a9656508f7e ` [条目](#entry-393) | gitlink-only | waylib-only |
| 394 / N6 | ` 6dc4affecbb95c861c13b134c04c55030270fc69 ` | ` be16d8319886d710a4914a354c12f361254ded89 ` | ` c979989888e47ffaaac0676197c2657a496c947c ` [条目](#entry-394) | gitlink-only | waylib-only |
| 395 / N6 | ` e567d0eb4f588c0bff923695dda75da1ef184a6d ` | ` b82ea03c515165226ea0ad0dab87ce74ec71031f ` | ` a37e470d946d22cf45885880135b3988295d02d5 ` [条目](#entry-395) | gitlink-only | waylib-only |
| 396 / N6 | ` fcb7f7e59ffaf681611e8cc382e3bdda2158e2ed ` | ` 56e08fd636126682eabe759edaeeae7e689f3c92 ` | ` cd7a9c1717e8cf3dcbd0f66bab69bea2d999952c ` [条目](#entry-396) | gitlink-only | waylib-only |
| 397 / N6 | ` b13cce374175a427ad3f8d0e050c89f9b99c0e87 ` | ` 8b0062b6a2248f443082e8eb0221a6c7f6d238fc ` | ` b0f357149187ca1d065b45da2bed883ffaf307b6 ` [条目](#entry-397) | gitlink-only | waylib-only |
| 398 / N6 | ` 58eb62c4764ed0a1d1e40db3ee56f1d4c9767b4c ` | ` 3c20b5d759f1f535e93ba0036d6537991af23241 ` | ` 6ba34f48d17996cf2ceed1bbbedea1ec71184f7b ` [条目](#entry-398) | gitlink-only | waylib-only |
| 399 / N6 | ` be50944f57d106eff1ca25b152998092a100eaad ` | ` 2de7af1260aaeac677e2483ea56667df9c0b0248 ` | ` 21fad14ea4c3b7073e6b709d4e870753de3e1281 ` [条目](#entry-399) | gitlink-only | waylib-only |
| 400 / N6 | ` 71a5ae7444c554dda9a5c661aea316df073ae019 ` | ` 686d1eeb2510e06c239bbec9ccbfc465ae3ff4f5 ` | ` 14a9a564531a697f2e51c3a5c212bc12e2dd076a ` [条目](#entry-400) | gitlink-only | waylib-only |
| 401 / N6 | ` e8c9c2245a2eaf584b2f2de3d009ca906b437da9 ` | ` f02e3d42923ff649c48d09bac936efdb68996ea0 ` | ` 925deae538b5891fa558b5be5220888b14903a7b ` [条目](#entry-401) | gitlink-only | waylib-only |
| 402 / N6 | ` e034d859f2f76e51771de6558652ca570c0778f0 ` | ` a3c5600b1ef00a24675deb590d188ed89d3d6a85 ` | ` b1c7f5158de5376c2c034a8a9340caf8044fb78c ` [条目](#entry-402) | gitlink-only | waylib-only |
| 403 / N6 | ` e06bfb9853fc7bb854d7e9cad4d8728574384d52 ` | ` ec559da748351da00f8aaec553edc202c978164f ` | ` 21f7e8e8cd398ee20b9301efedbe74e8e33dd761 ` [条目](#entry-403) | gitlink-only | waylib-only |
| 404 / N6 | ` 4fa410097e83f574ba669117f79d6d20e42f5f43 ` | ` 730d2b54ab610f6ae813973c159b6bee48ec1bd0 ` | ` 6b5768ed8e64bf07592942ed041f0bb3b0d87cee ` [条目](#entry-404) | gitlink-only | waylib-only |
| 405 / N6 | ` f73f0f111c1ccd89fb7adc63f0fd1b0e70a5e98a ` | ` a6bc6ac8c76b57aaf40449a4b725f551100f00f2 ` | ` c7ec648d25b462a8c9396dcd9422fd50318e21f9 ` [条目](#entry-405) | gitlink-only | waylib-only |
| 406 / N6 | ` c1458dcbc931cf644ca59b30012cb877905b4bb4 ` | ` fc1520c1f57927debc74c75b682b7612dd6f1d7e ` | ` edbe96b2f8381bf807b28972bb67f9770edc835d ` [条目](#entry-406) | gitlink-only | waylib-only |
| 407 / N6 | ` fbb806fdafe8c84afae72234394ae5856859456f ` | ` 60d5b63b71cb2197b29e95a4d3753947f8bd3503 ` | ` d97642f30ee1addb53ecd5d0ac1e846c278b7adc ` [条目](#entry-407) | gitlink-only | waylib-only |
| 408 / N6 | ` 085c0c51de465e449d6ac15aae047f42b44c2b25 ` | ` c4e674a790a9f9c619a7bf8681b8d90cfceb54c8 ` | ` 463779e862d89983faffcee644a5df1518897e8a ` [条目](#entry-408) | gitlink-only | waylib-only |
| 409 / N6 | ` 944566dec88e50356d2bea6ced447771a84af8ff ` | ` 84fefc34c8eaa8d4b6e46312446af074804d7c4d ` | ` b928859be3fdcc5154e9be88962d6e1fb9c518f2 ` [条目](#entry-409) | gitlink-only | waylib-only |
| 410 / N6 | ` 2455271ec8bfd1f0b41d0f3b8fbb2a516572e15d ` | ` b68ee3a668800b79966f2dada487a2189288f9a1 ` | ` 581d7a627a68a855df30352b01d8c1e2dfda54f8 ` [条目](#entry-410) | gitlink-only | waylib-only |
| 411 / N6 | ` 7d8d255dd2f75ed9588c2b77d31ce3e5ae23a799 ` | ` 08214f9dea9ba8300e548a0dd4bd380552e6b79d ` | ` b2d7bda88ea77bf2b26d08795a3fcb31c1d19fa4 ` [条目](#entry-411) | gitlink-only | waylib-only |
| 412 / N6 | ` 03dea01bc170d9a4a5208cb6f0312994a882d957 ` | ` 35c7564da9baf0590ceefcfe7baf6aae88f550f4 ` | ` 128d4a6b4dcc72678e939df8948debdc0e0f90ee ` [条目](#entry-412) | gitlink-only | waylib-only |
| 413 / N6 | ` bd247488a513aa70965ffd13d3c3b313b33e8523 ` | ` d7f86675ca9471772f09a126e0b2a41166530b4f ` | ` 3f0192bbefd7410f7aa93f09adabb25ada89d115 ` [条目](#entry-413) | gitlink-only | waylib-only |
| 414 / N6 | ` abb07e9a8cab1e2c855e881ec4a216b7a4d8943f ` | ` 7d600d624665262f79f93ec4c786dac784656f28 ` | ` c8702b4a6c1dec7fa343b762c512e6eefc3b879d ` [条目](#entry-414) | gitlink-only | waylib-only |
| 415 / N6 | ` f42de4aad659d7cbc7d3cafe1ea574c3fed1898b ` | ` 5385277aea0d12a1279726f84255d47e8ad60861 ` | ` e5a4f448db16f677d19d5e0aa965d75b73ecfa82 ` [条目](#entry-415) | gitlink-only | waylib-only |
| 416 / N6 | ` e8a3639bab3b83ff21a238ff49e7d92f1ff0acbb ` | ` 7e00b74d0656551b424e50fb37035e1a136293f1 ` | ` 36d0c496fdb1fd886acec6f12bfc4c3ca3f81eb8 ` [条目](#entry-416) | gitlink-only | waylib-only |
| 417 / N6 | ` 0b88a499773b71f6be1d3eae9b3a56fe59b1070d ` | ` c1df83045815aa35ea14b27bb63a91941e5eeacc ` | ` be561d7e449482b7aaf768be4c448118bb717dfe ` [条目](#entry-417) | gitlink-only | waylib-only |
| 418 / N6 | ` 327493f4f869e1dc4a9dbb90df8d698d8e4d45cd ` | ` 15e8139968d68a14ec47147e270c17a77174378f ` | ` 2af8b3f873ccfaa7b2e0c4eb34bdf4aa4d0de7e9 ` [条目](#entry-418) | gitlink-only | waylib-only |
| 419 / N6 | ` 4a57045bea78cb348fcf06add4ca8c33bc962014 ` | ` 7d4614279767a0ccd62534bc756bb9eb145ceda8 ` | ` 22e6f3e74e30f24be2c8d513f30b9f7c8851304b ` [条目](#entry-419) | gitlink-only | waylib-only |
| 420 / N6 | ` 07b20196d39dfeea14c19ad20980bcefbeccf298 ` | ` e62895ea40628aa4f3bd35a1e66b995b942027f0 ` | ` 081460343395858ef7dc29f040baad614395d106 ` [条目](#entry-420) | gitlink-only | waylib-only |
| 421 / N6 | ` ea645b18740f3435025b713223590b9ffb58d7ec ` | ` 09334d837749f4b1347ba46aa2052710bf4b6d64 ` | ` 4f0d8d19f22df10267d0b0d3e54b1a74eb34852a ` [条目](#entry-421) | gitlink-only | waylib-only |
| 422 / N6 | ` 29005752b1cb2fd500f319609110aa881adcaa64 ` | ` b7f0a618e6eda44578d9dadd6d1ec97776e6a4a6 ` | ` 9520fe32165432c2eca9efa350da9a1aa9f4e499 ` [条目](#entry-422) | gitlink-only | waylib-only |
| 423 / N6 | ` 5b85ed5b09fbda6407a68416c2b214be489907ed ` | ` 21d623c51ac2f63e57c2596e94c9d2d9dd61982c ` | ` 4b203dba65044dda9cd0fec4a7aac5e283f575d5 ` [条目](#entry-423) | gitlink-only | waylib-only |
| 424 / N6 | ` 04e824869922bcedc67865f904f8ff4b6c4cb076 ` | ` 39d445f6d846bbf10072b4d9de63ab8445bb0a7b ` | ` 390ed18e8e46dec35013c90b634460e4759b74b1 ` [条目](#entry-424) | gitlink-only | waylib-only |
| 425 / N6 | ` 2fad5dcfdcaf8394e118088173fc8be8ace13045 ` | ` 80dde7bb92d302c8e764394f48446d001cc7d562 ` | ` ad6b1de9410a5ac14e310219acbbaf141904499b ` [条目](#entry-425) | gitlink-only | waylib-only |
| 426 / N6 | ` e03e943d4766a6c670ee77b1b315b3c30c33c9fd ` | ` a7b199f58e15271c177e44a592647585d324ec6e ` | ` c513d428f17f2702f9e25163bfb635b687317865 ` [条目](#entry-426) | gitlink-only | waylib-only |
| 427 / N6 | ` 208e2d7f0c50b85095631b20db3ba8b451ae41a6 ` | ` d2a5bf9897229a629cc17fe8b0371e5833086265 ` | ` 3832d44d69c3b348909a4450a4c81ee05cb6bff2 ` [条目](#entry-427) | gitlink-only | waylib-only |
| 428 / N6 | ` 11e27740fefae88af7cbb6349a388775882c7ec2 ` | ` ffe8d89bfcb5af678da550c2b22030affda68421 ` | ` eb83e9d4e376587acd646073e1485c74cc7a848e ` [条目](#entry-428) | gitlink-only | waylib-only |
| 429 / N6 | ` 4963e7bc7daa0e2d29b546f10267bcf07569ef5c ` | ` ff82c099c3e86b89982e0fdf952a935df2256868 ` | ` 55918546eddcff1e553af37d623f77a646f70095 ` [条目](#entry-429) | gitlink-only | waylib-only |
| 430 / N6 | ` 5d445e265ea404db6e00eb30b1d9d8eb84572a16 ` | ` 4a31dda7e981c006ed3cf93871a38a45b49b34de ` | ` c928b5dc0376302784200c8ab917c43ac33d5a78 ` [条目](#entry-430) | gitlink-only | waylib-only |
| 431 / N6 | ` 252e508d682bfb3eaedd6aecab26a2ca8544d8f7 ` | ` 16babc2c58bf89a1f2f7c570ed6d66b268b24a14 ` | ` f884174bfeb69d696c28cbfabc6e355d5f4b7a12 ` [条目](#entry-431) | gitlink-only | waylib-only |
| 432 / N6 | ` b5d62efc17b9809001ac767199218fd70f8f4224 ` | ` d8e6ba152db4dd49d2708061103d011df80e37d0 ` | ` bff0e7984a8e9233e0d2440e7c3bd9709cd4fdca ` [条目](#entry-432) | gitlink-only | waylib-only |
| 433 / N6 | ` acb1a07ca29a1c96353095fc9400a636a8a586e8 ` | ` 227ef5ae64503301cdccf0e6854a66335d770368 ` | ` 862606ecd4a027215c334d7415238fd6f7042baf ` [条目](#entry-433) | gitlink-only | waylib-only |
| 434 / N6 | ` 1c5061d5dc556ab87e855e27891c85a53c132703 ` | ` 796b30fac21594b039599e4e6c1c3d208ec8bd70 ` | ` 95898859748492d1f8393723d7adb42f84ede90d ` [条目](#entry-434) | gitlink-only | waylib-only |
| 435 / N6 | ` 777ed58419d07e51038195608bcbec544748985d ` | ` 9b82130b8e017dcea7af067cf0443877eda12466 ` | ` f3588f2dde8bebdc643172bb3b9f11762b2c2298 ` [条目](#entry-435) | gitlink-only | waylib-only |
| 436 / N6 | ` d2570147440a6707d9667d1ff7377f55dd91f8ab ` | ` d76fa2257b552962f7b4153b97c7219947487c1a ` | ` a492b1376f0ce3fcf67a5e91302dcee3ac83960f ` [条目](#entry-436) | gitlink-only | waylib-only |
| 437 / N6 | ` 80eb79813fa825180bd2681247a272350b7b8d25 ` | ` ee2482472ed3de57464ca4df949c7c253e980e53 ` | ` 43ccae7d6e288441eb3c3f3d5ceaa08c9051db1f ` [条目](#entry-437) | gitlink-only | waylib-only |
| 438 / N6 | ` 41aec9d71f90c68323d4de15c2ddf6f16bdc1a37 ` | ` f3793493efd419439ecd11d447cc046a89083f4b ` | ` 76443e553a6e1d487662d9348d3905c0e0b859ae ` [条目](#entry-438) | gitlink-only | waylib-only |
| 439 / N6 | ` 1afe33b15978c2682fd3a7d88e1191d4c8a01f60 ` | ` bb107736385c281a5c8f0908624ee95ec3192cab ` | ` daee6b5e7dd504cfdfc864998625b56e02c19649 ` [条目](#entry-439) | gitlink-only | waylib-only |
| 440 / N6 | ` 7be5f6c58c2481e5289c114ca2cbfb61086eb7e8 ` | ` 0b18e133721394a794947ad1dd91c13467c69242 ` | ` 0c793fc518a4f0b8cb1a170ddd3767a0defc23ca ` [条目](#entry-440) | gitlink-only | waylib-only |
| 441 / N6 | ` ef86cc7863d65c84955e6e27d20cf65ac2ce3675 ` | ` b2907742b1a468f9fc148b25ab2d2b2f8ed07403 ` | ` 379a60d6205624b6831ede0039f47b2306bae0a1 ` [条目](#entry-441) | gitlink-only | waylib-only |
| 442 / N6 | ` 99dfd9b78f387745f72c3c2ef964b258561d2fd9 ` | ` d7d8065062d85b5c7399a1ac44220ce2f2565177 ` | ` 70560f1219926b5535555527938778b1f9583d89 ` [条目](#entry-442) | gitlink-only | waylib-only |
| 443 / N6 | ` efcf521d9e167344a0eaa88411323e0a682b4352 ` | ` d36822a006491fa6250035d9a0afe3d7f8cb5b91 ` | ` a8045448f768721e53c272a466253dc533c53933 ` [条目](#entry-443) | gitlink-only | waylib-only |
| 444 / N6 | ` c72ebde4606fda987130454c43e3619dab48c9e0 ` | ` 0f8d30e6c291687420724c6aa6b6cceb3356bafe ` | ` 1cc1168ddc1471a1fa2558cad3dd452e5403ce13 ` [条目](#entry-444) | gitlink-only | waylib-only |
| 445 / N6 | ` d1834b51b4e9dcfb18351dece8769fe81bb2d1bb ` | ` 2b57bf34583100590a4d0025ff4605ca3bd061fe ` | ` 44f81d82d96c1511cd92f350e7ced7192699b365 ` [条目](#entry-445) | gitlink-only | waylib-only |
| 446 / N6 | ` 8a3d1b8a4424bacf3f5beabde5ec66983ce8dca0 ` | ` f66adc9553727f68cba1d5dd89d1df47679906ca ` | ` 21634c9529237ed8972236cccc157ab74575a827 ` [条目](#entry-446) | gitlink-only | waylib-only |
| 447 / N6 | ` 4dad66cf6f99303e211dabc0e72c9f00e0c4c93d ` | ` 2017cb12903cfa0dcdc30c23f02d6f14e95b2517 ` | ` 447747c2ba68afcd483d6119dd8efe2dc33deb0b ` [条目](#entry-447) | gitlink-only | waylib-only |
| 448 / N6 | ` aec82dd30308ad1f6aea17b4bccc363cd6b9c73c ` | ` 1358414a1b59ce5c89b85254a966abd231cf8c8d ` | ` 8ee7ac9eacdcc190c1b14e011ae1e81eb43f57b8 ` [条目](#entry-448) | gitlink-only | waylib-only |
| 449 / N6 | ` 63790e1d8cd454f69947f141dbfc403844cc420e ` | ` 99739f3297ad1795edae807f5a5bfcc90dda8114 ` | ` 5a0975cee991f6194aaeba00374c3f48c9b25700 ` [条目](#entry-449) | gitlink-only | waylib-only |
| 450 / N6 | ` 1715ce5d5e91628b9323c096429781245c08b582 ` | ` 26ffbacee0d75dd35ff5e73976fc3b34578d9309 ` | ` 9076299f2beb0cbe43edd47ebd14e06cec67ba64 ` [条目](#entry-450) | gitlink-only | waylib-only |
| 451 / N6 | ` 9f4afb87e591bb33912e3d7278cf49d6edf6b287 ` | ` 16ec894425bd02aec658d9ea9e5bd0ea227f53d6 ` | ` a344edbb80d08367cb6eaad383d1f99aa36e86cb ` [条目](#entry-451) | gitlink-only | waylib-only |
| 452 / N6 | ` 39e7a61b472519868038242f95335616ba8f5b8e ` | ` 346d04c02b7decf5bcda494718f3fd9b4742db3b ` | ` 75e7124d01cd56be02c99348e1c3a26243c448d0 ` [条目](#entry-452) | gitlink-only | waylib-only |
| 453 / N6 | ` d003741eaa4e1832e2554710175415628784c94b ` | ` b2e2390027eba52b24a145fafa77b2497e0eed35 ` | ` 0faca04c0fd9421d3415c6f37eeffd8ef1df7a1f ` [条目](#entry-453) | gitlink-only | waylib-only |
| 454 / N6 | ` 15bc8d04b8df33c82d0208c582e234e60aba60a0 ` | ` 5ba1e67d993ccb39384f0d6dc7860cc17a4c8135 ` | ` 79ca1642d3d94a2e7527b49183a135c8abff8ab3 ` [条目](#entry-454) | gitlink-only | waylib-only |
| 455 / N6 | ` d37140d74ab9d0f8cb32f222ffbfd83937c0e891 ` | ` 7ef7fd0722a31f08b18e9c591999a85939858e46 ` | ` bfa552f64ea6835a64048468d618d74c5ca62e2e ` [条目](#entry-455) | gitlink-only | waylib-only |
| 456 / N6 | ` d8829e42caefa988029a62148a9ababfe467640f ` | ` d6a1e82a620a540f1d722070627f1b59f12548f1 ` | ` 2180ecd076075bc5ccb21d791b42a80f416f2132 ` [条目](#entry-456) | gitlink-only | waylib-only |
| 457 / N6 | ` 5c661fd02bed08c4b2e6a633688d6d5c944842c5 ` | ` 53b278677c0875a69d56bad11ab8342516bf69c1 ` | ` f97d448b4d88d98915e364a28c08c14dc0f57742 ` [条目](#entry-457) | gitlink-only | waylib-only |
| 458 / N6 | ` d85ecab59bfe36b18a00a728810df435e6f1543e ` | ` 81affb7dd81c3ea0d9ccee3c535510ba6d047393 ` | ` 473e4539caf9e28a9a29262d5f17f17e8292c32b ` [条目](#entry-458) | gitlink-only | waylib-only |
| 459 / N6 | ` 324909af3e2b1fda50896fe9863747fb6011ec9a ` | ` 678c56baba4e20a4313980125ed37e131b6d6daa ` | ` d16389b69a645d4cfc6bf358147b8a2e8629b4db ` [条目](#entry-459) | gitlink-only | waylib-only |
| 460 / N6 | ` e4079612adb3e567c7f661dcb404663484817f39 ` | ` b7824a49ddace87952f0aecf7ce6fd8443475ac9 ` | ` 45cdb04acc57153006dc234bab392d94dea913a4 ` [条目](#entry-460) | gitlink-only | waylib-only |
| 461 / N6 | ` 981ef4b18cbe7e908804e17bf7fd2ae4d65e6fca ` | ` 750fdb3a14f7bb66237e336c15ade4baa1d266c0 ` | ` b4bb1dccdafa6e8d551eabf37b3c3153ab590380 ` [条目](#entry-461) | gitlink-only | waylib-only |
| 462 / N6 | ` 475f3cb6f5f21d0ecc059c6998e590a38f291560 ` | ` 7bc4ddc002d64c60bf0f51e226913c87cae808f7 ` | ` b9a05b795109edd2c383d557ba09b264d73ff4ec ` [条目](#entry-462) | gitlink-only | waylib-only |
| 463 / N6 | ` 06ab77c1664548ef90e1f953ff00e2d5dacea166 ` | ` 6c588fd2b7299511a56b3ccc15055be531023b76 ` | ` 73f73be5d4dd72a348375e730e794f60066415b0 ` [条目](#entry-463) | gitlink-only | waylib-only |
| 464 / N6 | ` ca160e1eb74ecb4f43102ac3f6463ab0e1a25137 ` | ` 152281e9ebef1be22310b29b85741a12488955cc ` | ` 543dce9a1873bd78b5654ce8587a889e10d20848 ` [适配详情](adaptations/543dce9a1873bd78b5654ce8587a889e10d20848.md) | adapted | dual |
| 465 / N6 | ` eb6dfbebd9050ed78947d4e85ac28873d1e9b4c1 ` | ` 2e9bb0e2e5ac181c8d834c0e6ff41d096df5c0fb ` | ` 89cd75e58ef84f4350761fa484fae58eb69e8efc ` [条目](#entry-465) | applied | deckshell-only |
| 466 / N6 | ` 726a9e57b3f9f56df4a5d81fc099e2e4f954b8c6 ` | ` 5d74ce228c5389efbbd94bfc610122b4030538e5 ` | ` b85d61bd28103128802a282d9adcb6c91dd47d67 ` [条目](#entry-466) | applied | deckshell-only |
| 467 / N6 | ` f40f2fe7ba7daf686b3dbf352d592e56f9e182bc ` | ` 1fd5f769397d97a65fceeddc7bd9b7597062d481 ` | ` 139051af09f25abf4fbc2b2d3737a6f282268a2c ` [适配详情](adaptations/139051af09f25abf4fbc2b2d3737a6f282268a2c.md) | adapted | dual |
| 468 / N6 | ` 6d4772876759e122571b6ff409c476fe92865c5e ` | ` 8c6c1b2aa89e2e5668403edf37503dfe382b4ab7 ` | ` a137c78dfc3d046a3d5e262dd5a04f4682befda6 ` [条目](#entry-468) | applied | deckshell-only |
| 469 / N6 | ` 4cd2c672c10ec0e3004c88bbd48a18ded22872bd ` | ` bca2766cb19205e84846b44f5ece15c6c478bbb2 ` | ` b7d2ffd21cccc75e75d0d58d992232294c57804c ` [适配详情](adaptations/b7d2ffd21cccc75e75d0d58d992232294c57804c.md) | adapted | dual |
| 470 / N6 | ` ce57dab0259c33eb183589928249ef9e2be149af ` | ` 77d487cedd0b1f1eabf1ec38ee744af3fe4a0930 ` | ` a6cea1c57039b25b2c1d5504b01300af5a221477 ` [适配详情](adaptations/a6cea1c57039b25b2c1d5504b01300af5a221477.md) | adapted | deckshell-only |
| 471 / N7 | ` a0329cd13c3071d658cf6043c4884b0cbf8844ec ` | ` 09bd655c5d38804169777a9d0aa52b2ff5322e4d ` | ` 8452d15c1bbc974f17d55e49f52b91bac57e47f4 ` [条目](#entry-471) | gitlink-only | waylib-only |
| 472 / N7 | ` b9f6069fa3e1354091af377c9c9472fda290e2d8 ` | ` f8f38e5af5ad8799bac9bf3bfe3331b63e91baa5 ` | ` b4afb2b36ae594780ee51343ada5a33828a796b8 ` [条目](#entry-472) | applied | dual |
| 473 / N7 | ` cf2dc0a911759ef9cc94fd9d8d81c76f4ccb4769 ` | ` 1c9eaeb6c0362f9b00d4af5fd92c90974507eac7 ` | ` 38bf63ee2a56c08d0b852f54337c63131f8c6064 ` [适配详情](adaptations/38bf63ee2a56c08d0b852f54337c63131f8c6064.md) | adapted | dual |
| 474 / N7 | ` debeeb67804d44dfa1140058d592f617e37951f8 ` | ` 082095f3f36d644441926c706c16e41f41e2092f ` | ` 7a880ac6713bb5334982a7326df13f03eae601a8 ` [适配详情](adaptations/7a880ac6713bb5334982a7326df13f03eae601a8.md) | adapted | deckshell-only |
| 475 / N7 | ` 98c1a0c9347f4f3af593692261bbd8150ec85f2f ` | ` 9115cc151e5d967b6d58d4b2f162e6467137910e ` | ` 7365a7e8d9670ba620c6c32ca90222086ae28048 ` [条目](#entry-475) | gitlink-only | waylib-only |
| 476 / N7 | ` 12d4cff2dc6a81c6b891812d55b1a98378720d43 ` | ` 610a02c74915ba0f9d86d61a0c818da1d61a7efb ` | ` 569e4c863f8996b68b7f0209638b60e113ff12e8 ` [条目](#entry-476) | applied | dual |
| 477 / N7 | ` f2ebdf403cef739166a5aacc7324a24d3662176b ` | ` 83e918c139389abfea9846909a52e5a199258d6e ` | ` 0cf9ae3c48e4c18be22f895ba4fb44e12f67c5a6 ` [适配详情](adaptations/0cf9ae3c48e4c18be22f895ba4fb44e12f67c5a6.md) | adapted | dual |
| 478 / N7 | ` 9a36a9924ef6b74d944accd17e149ec015ef862d ` | ` 5cb809142145817c9fbb556472da51d5621ba2e1 ` | ` 454bc766e594dbbce4d6fb297645ec3b3558b8d9 ` [条目](#entry-478) | gitlink-only | waylib-only |
| 479 / N7 | ` 9ac30111d8170b207ec5c821a3131804ce4447c7 ` | ` 024f7e35db68da4bb33177f7f7cabcd270cff76c ` | ` a718224c9297e7471194021604c1a68910c132ee ` [条目](#entry-479) | applied | deckshell-only |
| 480 / N7 | ` 27dc6ce6022dbcd77ebdf3323d3672d47f78a9e7 ` | ` a8ab40323105f670c1785131ed0c0f83d25086e7 ` | ` 16f668bc2b3baf0f13cfd97735803a6a3bd280bc ` [适配详情](adaptations/16f668bc2b3baf0f13cfd97735803a6a3bd280bc.md) | adapted | deckshell-only |
| 481 / N7 | ` 00f0a3572f081baab08ab21db8b018c4f0feec49 ` | ` d021fb8a021717ddc95c3bdaa32e7ffa32d920c0 ` | ` 927a692d2ed71014e924f320a075cc0f323d37e7 ` [条目](#entry-481) | applied | dual |
| 482 / N7 | ` 8d3212c1e7927fc0b9060ae9302a4329cce1e23f ` | ` f21267bb9c65c07090492dff84f4fd50afdf364a ` | ` feb01c4236e1ca54ff50d25232e30b50d9cc05b8 ` [适配详情](adaptations/feb01c4236e1ca54ff50d25232e30b50d9cc05b8.md) | adapted | deckshell-only |
| 483 / N7 | ` 5a69d2fe71dedb6f2a13ad9cf3d3dd593613623b ` | ` 307b63828736ec99c3ab93009f5242fe6773c0e3 ` | ` d7c37307ae4ffee0b3d3654b8fe82304430c6b16 ` [条目](#entry-483) | gitlink-only | waylib-only |
| 484 / N7 | ` 07b7bec96c3ecc690931578663f0baf66a9b6a68 ` | ` 42c929d26aed3ef207a73c80a4610300fcebe927 ` | ` 0bee1076cb2eb918d7e8f6898e02f7510e949aa7 ` [条目](#entry-484) | applied | deckshell-only |
| 485 / N7 | ` 2031e780f5c770a11843bc81b3cef5271e477dd0 ` | ` 3a9f920ba1c86133c7c2d5881cd1694a76020d62 ` | ` 6470237c3b55e2f9e723f822cbacd2de5401f780 ` [条目](#entry-485) | empty | deckshell-only |
| 486 / N7 | ` d823b8c907699dc86f0fe554cb46b2db8991d408 ` | ` ac86a80eab3a36b9c88a633ac6859523ae3c1e16 ` | ` f011b1d4b805b2b4f9fb3db88bec41137708a24a ` [条目](#entry-486) | applied | deckshell-only |
| 487 / N7 | ` 90f6045bf432515698e9f5324b7e5fcf8a375331 ` | ` 17ce7c157b44491ef669397fe766485017eda91c ` | ` 54575de7c248bd8052673002d8bcac70d69bc26c ` [条目](#entry-487) | gitlink-only | waylib-only |
| 488 / N7 | ` 3a11cdf2ad5a20b7122ce4faf94401b39b90d870 ` | ` 020aaed6a88da685bdfdf97ec2ed495c811bf206 ` | ` 164ed07bf4a03ca0ffe8a2911d5cab539d81e4d6 ` [条目](#entry-488) | applied | deckshell-only |
| 489 / N7 | ` 593c48420d29f84f8cb320ea34dbf5ea67cb1abf ` | ` 79cbdc7509986440ee77a47a36475cc4d01e439f ` | ` 8a2ed96d1c61331af681ee2fb8540c2ab49d099d ` [适配详情](adaptations/8a2ed96d1c61331af681ee2fb8540c2ab49d099d.md) | adapted | dual |
| 490 / N7 | ` bf156fcbf01417acfad112849851b458452f3a60 ` | ` 4197ce38292120028b51d59058a201891ebe25eb ` | ` a7c71089f48162fcd8c7d4dc2a411de512615d69 ` [适配详情](adaptations/a7c71089f48162fcd8c7d4dc2a411de512615d69.md) | adapted | deckshell-only |
| 491 / N7 | ` dde64ada3f04449e1b4d58e298926955c2fee2dc ` | ` 47dbb0e91f1bbb589547ce2e7d640ae8a75e6536 ` | ` 439f3b4636523d0042ec958892c961cdcaa2bd95 ` [条目](#entry-491) | applied | deckshell-only |
| 492 / N7 | ` a610119f49b547467a8871c6853ed1c04932d198 ` | ` c4f8494662684cfad8c29ba343c23919d40dbf0d ` | ` 8deb95382d4e45d5e7f2132ea3a223498ce7df6f ` [条目](#entry-492) | applied | dual |
| 493 / N7 | ` 660b4f0f3cccb43371c63931aa96429f1b8621c7 ` | ` 2453dd21c33137e4e8186b44852c805d25a78f5d ` | ` d8bbabc055577e9da132aa71e999d07d0609bf60 ` [适配详情](adaptations/d8bbabc055577e9da132aa71e999d07d0609bf60.md) | adapted | deckshell-only |
| 494 / N7 | ` f26fd6ec0d0afe0b44d03877c30d7618f5fd3b79 ` | ` 24475024dabeb7b09ee6d6ff0df35a1a42594f80 ` | ` 2bc72cc83afea646c5f96a29ded615c72f1328f6 ` [条目](#entry-494) | applied | deckshell-only |
| 495 / N7 | ` 3d74c4c805a7ce5768a8ce8fc1af638a8fadff60 ` | ` 081276dfc30da0d22889d442410e74a51eb71fe6 ` | ` e8e57b4274d81bc7e928d4638cb6ad1be0d257d1 ` [条目](#entry-495) | applied | deckshell-only |
| 496 / N7 | ` 66eb7b7058b3dc9200ab056c4fa796527a9ca144 ` | ` a625f69e1043af631043c43b24c71542db8da3eb ` | ` 271c5bbf25ca971c0cd80824df40e074f8ba5945 ` [适配详情](adaptations/271c5bbf25ca971c0cd80824df40e074f8ba5945.md) | adapted | deckshell-only |
| 497 / N7 | ` 6587755e422a878b681a5cdfd9bb12b999c02c33 ` | ` a12a9cca017f2bb17565459e29dc0c4c1a87c4ac ` | ` d8ce6ae0db5497a0e674dd579dd9b9d796eca9a1 ` [适配详情](adaptations/d8ce6ae0db5497a0e674dd579dd9b9d796eca9a1.md) | adapted | deckshell-only |
| 498 / N7 | ` 02970b2654e734ed2f4ba076e79cd92d8f7d0c0f ` | ` 6e12ca78126e4ed42def12d63fb6b970e217eb8d ` | ` bd6ee08b2af086bcc326cd9a9286f9f371212b11 ` [条目](#entry-498) | applied | deckshell-only |
| 499 / N7 | ` a1ef0412ee9992b052c833d3eda797a549cd628a ` | ` afeece1396afd5182d201782be026afdba321061 ` | ` 5fafaf0eae462ac257ac69d3e4e27fd7968c1767 ` [条目](#entry-499) | applied | deckshell-only |
| 500 / N7 | ` fc7e6582ee247ec1e8e1059c53aa6e131c413586 ` | ` 8be1df924b752263a8a4481c84e503d7b1ff88ae ` | ` ae4974963937d12a722d2a8ae73a2cd1600138e4 ` [适配详情](adaptations/ae4974963937d12a722d2a8ae73a2cd1600138e4.md) | adapted | deckshell-only |
| 501 / N7 | ` 19919612da6be2ec7f38f6f124a3532a9447bcad ` | ` 673da7a0d47b338749fe03ba2e19918fd8dc9daa ` | ` 072ee1f2121e5fd99cc51232e51fa0c52e5b3d55 ` [条目](#entry-501) | applied | deckshell-only |
| 502 / N7 | ` fd573cf44fb06ee1eebcdd8c39716d1c797b64d4 ` | ` bf1092f11da49ffe4cdaacf148dab7f60d02198d ` | ` d76ef0a531100d18bfb966c33531e28e03b838fe ` [适配详情](adaptations/d76ef0a531100d18bfb966c33531e28e03b838fe.md) | adapted | deckshell-only |

## 逐项归属、路径与依赖

<a id="entry-1"></a>
### 1. N1 / ` fix(effects): smooth glass edges and optimize liquidglass shader `

- 本仓内容路径：` compositor/misc/shaders/liquidglass.frag `。
- 实际改变：` compositor/misc/shaders/liquidglass.frag `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 2eabcfb98d49d520b96c9f2cd2ea517a6fa91719 ` 和原目标 ` 3eceaef344dedab8431ca88a6d1cf5e89cd9eb98 ` 查询。

<a id="entry-2"></a>
### 2. N1 / ` fix(effects): tune liquid glass defaults and disable dispersion `

- 本仓内容路径：` compositor/examples/test_glass/Main.qml `、` compositor/examples/test_glass/helper.h `、` compositor/misc/dconfig/org.deepin.dde.treeland.user.json `、` compositor/src/core/qml/Effects/GlassEffect.qml `。
- 实际改变：` compositor/examples/test_glass/Main.qml `、` compositor/examples/test_glass/helper.h `、` compositor/misc/dconfig/org.deepin.dde.treeland.user.json `、` compositor/src/core/qml/Effects/GlassEffect.qml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` aa362eedfd17db30e9737a008f8386ba87098a71 ` 和原目标 ` a85c4c48029b950f28713fbae8a1e1b573f3dcd2 ` 查询。

<a id="entry-3"></a>
### 3. N1 / ` fix(wallpaper): restore wallpapers after output reconnect `

- 本仓内容路径：` compositor/src/wallpaper/wallpaperconfig.cpp `、` compositor/src/wallpaper/wallpaperconfig.h `、` compositor/src/wallpaper/wallpapermanager.cpp `、` compositor/src/wallpaper/wallpapermanager.h `。
- 实际改变：` compositor/src/wallpaper/wallpaperconfig.cpp `、` compositor/src/wallpaper/wallpaperconfig.h `、` compositor/src/wallpaper/wallpapermanager.cpp `、` compositor/src/wallpaper/wallpapermanager.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 506ece05ff4a8cdfd17732dfcc8432a7a1e90091 ` 和原目标 ` a9e6e19818d9f05ee1c86f06c0e095a04065f2d7 ` 查询。

<a id="entry-4"></a>
### 4. N1 / ` fix: auto-wake DPMS-off outputs on input events `

- 本仓内容路径：` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `。
- 实际改变：` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 467f0dfd7d0fc94689c282d72f554b86c9781f28 ` 和原目标 ` b6cf8fbddd147660a6a52cee1157801ec5fab719 ` 查询。

<a id="entry-5"></a>
### 5. N1 / ` fix: emit startedChanged signal on session start `

- 本仓内容路径：` compositor/examples/test_capture/capture.cpp `。
- 实际改变：` compositor/examples/test_capture/capture.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 1f025a9ba3784f4ac36a5d9d6402b4031585dde4 ` 和原目标 ` 145028fdc2538f0cc53f5d6ba3b3916f1ad2f06f ` 查询。

<a id="entry-6"></a>
### 6. N1 / ` refactor: consolidate surface capability init `

- 本仓内容路径：` compositor/src/surface/surfacewrapper.cpp `。
- 实际改变：` compositor/src/surface/surfacewrapper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 0050d87e38b4be8fa4addac6c4c94debf05a6594 ` 和原目标 ` b8758ce1b1a00fddf9faf141afc212b60d1e6899 ` 查询。

<a id="entry-7"></a>
### 7. N1 / ` fix(wallpaper): resend all wallpapers after output reconnect `

- 本仓内容路径：` compositor/src/wallpaper/wallpapermanager.cpp `、` compositor/src/wallpaper/wallpapermanager.h `、` compositor/wallpaper-factory/treelandwallpapernotifierclient.cpp `。
- 实际改变：` compositor/src/wallpaper/wallpapermanager.cpp `、` compositor/src/wallpaper/wallpapermanager.h `、` compositor/wallpaper-factory/treelandwallpapernotifierclient.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` ed9ae1a22c69d70fe3e09e048678f5a587d52418 ` 和原目标 ` efde569b6e72f291f0c9ff0b5daa6df80f8bc76b ` 查询。

<a id="entry-8"></a>
### 8. N1 / ` fix: allow Video Bus brightness shortcuts `

- 本仓内容路径：` compositor/src/seat/seatsmanager.cpp `。
- 实际改变：无。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 5398e81caf1cefc335a713b4be1085a5fadbe98e ` 和原目标 ` b0eba486798c847685b7e72130d9cc8bb3bb7f3f ` 查询。
- 原审核说明：` 规范路径 SeatsManager::assignDevice 已保留 Video Bus 亮度键，使用相同过滤条件的等价证明保留本地设备生命周期修复。 `。
- empty 的原等价证明（不把未改文件说成新适配）：

```json
{
  "kind": "canonical-path-equivalence-review",
  "review_state": "approved",
  "source_commit": "5398e81caf1cefc335a713b4be1085a5fadbe98e",
  "target_parent": "03036027a7bbc137c57fa8f200b1948386887d54",
  "target_path": "compositor/src/seat/seatsmanager.cpp",
  "source_before_predicate": "if (deviceType == WInputDevice::Type::Keyboard &&\n        (deviceName.contains(\"Power Button\") || deviceName.contains(\"Sleep Button\") ||\n         deviceName.contains(\"Lid Switch\") || deviceName.contains(\"Video Bus\"))) {\n        return;\n    }",
  "source_after_predicate": "if (deviceType == WInputDevice::Type::Keyboard &&\n        (deviceName.contains(\"Power Button\") || deviceName.contains(\"Sleep Button\") ||\n         deviceName.contains(\"Lid Switch\"))) {\n        return;\n    }",
  "target_predicate": "if (deviceType == WInputDevice::Type::Keyboard\n        && (deviceName.contains(\"Power Button\") || deviceName.contains(\"Sleep Button\")\n            || deviceName.contains(\"Lid Switch\"))) {\n        return;\n    }",
  "normalized_after_equals_target": true,
  "normalized_before_differs_from_target": true,
  "reason": "目标规范路径中的 assignDevice 已通过本地设备生命周期修复移除 Video Bus 过滤，继续保留 Power Button、Sleep Button 和 Lid Switch 过滤；来源唯一语义差异已满足。不存在兄弟文件代替实现。"
}
```


<a id="entry-9"></a>
### 9. N1 / ` fix: correct shadow rendering during layer shell window animations `

- 本仓内容路径：` compositor/src/core/qml/Animations/LayerShellAnimation.qml `。
- 实际改变：` compositor/src/core/qml/Animations/LayerShellAnimation.qml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` dc245f5fa59e490ec79ce629e0fccf6662fc26a9 ` 和原目标 ` a1af95b4f80b98205c466f2fc2462afde8d7cd40 ` 查询。
- 原审核说明：` 保留目标现有 WaylibShared.QuickSharedServer QML 导入；其余内容严格取来源后的同一规范文件，包含 boundingRect 阴影范围、Blur 路径和 ShaderEffectSource 裁切修复。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/1b5dc5f31fdf23aa8627972c73d23fe4c7c0f03c.md)。

<a id="entry-10"></a>
### 10. N1 / ` refactor: delegate activation to SeatSurfaceManager `

- 本仓内容路径：` compositor/src/core/rootsurfacecontainer.cpp `、` compositor/src/modules/shortcut/shortcutrunner.cpp `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `。
- 实际改变：` compositor/src/core/rootsurfacecontainer.cpp `、` compositor/src/modules/shortcut/shortcutrunner.cpp `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` bf058f1d9f59471cf8c4500a519048842a0dcace ` 和原目标 ` dee1db68a6a7b3094f17f14ac5bd08140bc133f8 ` 查询。
- 原审核说明：` 采用来源的每座席激活归属及焦点回调迁移；三方合并保留目标既有路径和局部格式，锁屏解锁回调改用 activatedSurface()，保留目标已有的空 impl 卸载及提前返回，不能重新引入对已删除成员的访问。 同时迁移 init() 与 onExtSessionLock() 中两处外部锁屏解锁回调；空激活窗口仍不恢复焦点。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/6e0e14dc5cd97e82406f89311700043fd768295f.md)。

<a id="entry-11"></a>
### 11. N1 / ` refactor: extract surface inactivation logic `

- 本仓内容路径：` compositor/src/core/shellhandler.cpp `、` compositor/src/core/shellhandler.h `、` compositor/src/seat/helper.cpp `。
- 实际改变：` compositor/src/core/shellhandler.cpp `、` compositor/src/core/shellhandler.h `、` compositor/src/seat/helper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 09a8d72c9bda873b2696139c55132eb7c5ab41d2 ` 和原目标 ` 3cb6be9084ee2e4fea5f67a1f443360f654708c5 ` 查询。

<a id="entry-12"></a>
### 12. N1 / ` refactor(keyboard-focus): unify focus management path `

- 本仓内容路径：` compositor/src/core/popupfocusmanager.cpp `、` compositor/src/core/popupfocusmanager.h `、` compositor/src/core/shellhandler.cpp `、` compositor/src/seat/helper.cpp `、` compositor/src/surface/seatsurfacemanager.cpp `。
- 实际改变：` compositor/src/core/popupfocusmanager.cpp `、` compositor/src/core/popupfocusmanager.h `、` compositor/src/core/shellhandler.cpp `、` compositor/src/seat/helper.cpp `、` compositor/src/surface/seatsurfacemanager.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` a00bd19c76b4c8cee2f9491883a3d845d002d6b1 ` 和原目标 ` b771382ed8bd8364edbe6a430fe6f9eef2aa14b2 ` 查询。
- 原审核说明：` 在规范路径完整吸收 popup wrapper 和每座席焦点仲裁迁移；三方合并仅适应 Helper 既有 include 布局，保留本地 include 布局与锁屏生命周期接入，不重新引入目标已不使用的 wxdgtopleveltagmanager 头。 外部锁屏解锁回调同样通过 hasFocusCapability() 与 requestKeyboardFocus() 恢复焦点，避免绕过本次迁移后的 SeatSurfaceManager 仲裁。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/ccc53299352eae97b11c0a06d5bb5ce29ec534ad.md)。

<a id="entry-13"></a>
### 13. N1 / ` fix: avoid writes when querying personalization state `

- 本仓内容路径：` compositor/src/modules/personalization/personalizationmanagerinterfacev1.cpp `。
- 实际改变：` compositor/src/modules/personalization/personalizationmanagerinterfacev1.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` c8c69c9f679cac1e22ed2e32e74c9f3df5b60d56 ` 和原目标 ` 0166846131eebabc3519383cd1b27c3753040411 ` 查询。

<a id="entry-14"></a>
### 14. N1 / ` fix(activation): pass seat through activation pipeline for multi-seat `

- 本仓内容路径：` compositor/src/modules/activation/activationmanagerinterfacev1.cpp `、` compositor/src/modules/activation/activationmanagerinterfacev1.h `、` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv1.cpp `、` compositor/src/seat/helper.cpp `。
- 实际改变：` compositor/src/modules/activation/activationmanagerinterfacev1.cpp `、` compositor/src/modules/activation/activationmanagerinterfacev1.h `、` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv1.cpp `、` compositor/src/seat/helper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` c223a631ade7662aae09c132f575be23d63460b9 ` 和原目标 ` 21794db17b8a1e59215998fe9357600193181a7c ` 查询。
- 原审核说明：` 在原有 TokenInfo/activate 规范实现中保存 QPointer<WSeat>，消费 token 前读取 seat 并同步 signal、Helper 和 foreign-toplevel 调用方；保留过期和一次性消费检查，不改协议 XML 或资源销毁约定。三方冲突只涉及日志格式；保留 lcTlActivation 分类与 disposition 信息，但不把 token 前缀搬入新的日志行。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/8fab44dd3bf585d15ceb1b23fc1408b471fe11c3.md)。

<a id="entry-15"></a>
### 15. N1 / ` fix(seat): add keyboardFocusPriority check in setKeyboardFocusSurface `

- 本仓内容路径：` compositor/src/seat/helper.cpp `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `。
- 实际改变：` compositor/src/seat/helper.cpp `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 919986c388ba5b5f1e4e7d6a761f028e6a3fb5be ` 和原目标 ` 0f4195972ec7f1aff138508e5102244759a9c66f ` 查询。
- 原审核说明：` 完整同步焦点优先级、Qt::FocusReason 和清空焦点始终允许的语义；锁屏恢复通过 hasFocusCapability 与 requestKeyboardFocus 进入相同仲裁路径，保留目标既有空 impl 卸载/提前返回结构，不重复或后移生命周期检查。 三处锁屏解锁回调在前序焦点迁移适配中已统一到 requestKeyboardFocus()；本提交保留其等价最终行为，并完整应用 SeatSurfaceManager 集中焦点仲裁改动。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/998f20402ffbee0e799503c52fc4b51a863d8ff6.md)。

<a id="entry-16"></a>
### 16. N1 / ` fix(workspace): reload workspace config after DConfig initialized `

- 本仓内容路径：` compositor/src/seat/helper.cpp `、` compositor/src/workspace/workspace.cpp `、` compositor/src/workspace/workspace.h `。
- 实际改变：` compositor/src/seat/helper.cpp `、` compositor/src/workspace/workspace.cpp `、` compositor/src/workspace/workspace.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 55fb88aa91f152fa4837ee469a8299179bee5ecc ` 和原目标 ` 8527f55266135710a6b6c8a9a7d5d489efd4bace ` 查询。

<a id="entry-17"></a>
### 17. N1 / ` fix: improve shortcut event dispatch and Alt+Tab task switch reliability `

- 本仓内容路径：` compositor/src/core/shellhandler.cpp `、` compositor/src/modules/shortcut/shortcutcontroller.cpp `、` compositor/src/modules/shortcut/shortcutmanager.cpp `、` compositor/src/modules/shortcut/shortcutmanager.h `、` compositor/src/seat/helper.cpp `。
- 实际改变：` compositor/src/core/shellhandler.cpp `、` compositor/src/modules/shortcut/shortcutcontroller.cpp `、` compositor/src/modules/shortcut/shortcutmanager.cpp `、` compositor/src/modules/shortcut/shortcutmanager.h `、` compositor/src/seat/helper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 26f52806c0432c70438a027b7e7659e1cb481b2b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 868a0fcee2919031c5b50d06d7258c19d2ca1103 ` 和原目标 ` cdeeb1d76d8bd1840a3e3bee39ec7acc25f68147 ` 查询。

<a id="entry-18"></a>
### 18. N1 / ` fix(waylib): use notify_* API for keyboard focus operations `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/kernel/wseat.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 3eb629c01b8d26c920ab0baededf76d35675602f `。
  原证据引用：` 26f52806c0432c70438a027b7e7659e1cb481b2b ` → ` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 3eeb8956884cb9eb759ff81107a60cfa7841e756 ` 和原目标 ` 5c14d1083fc804f45c400a372d5cf5a40315ec73 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 3eb629c01b8d26c920ab0baededf76d35675602f `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-19"></a>
### 19. N1 / ` refactor: remove built-in shortcut daemon (treeland-shortcut) `

- 本仓内容路径：` compositor/CMakeLists.txt `、` compositor/misc/systemd/CMakeLists.txt `、` compositor/misc/systemd/dde-session-pre.target.wants/treeland-shortcut.service.in `、` compositor/src/CMakeLists.txt `、` compositor/src/treeland-shortcut/CMakeLists.txt `、` compositor/src/treeland-shortcut/shortcut.cpp `、` compositor/src/treeland-shortcut/shortcut.h `、` compositor/src/treeland-shortcut/shortcuts/_dde-clipboard.ini `、` compositor/src/treeland-shortcut/shortcuts/_dde-file-manager.ini `、` compositor/src/treeland-shortcut/shortcuts/_dde-launchpad.ini `、` compositor/src/treeland-shortcut/shortcuts/_dde-notification.ini `、` compositor/src/treeland-shortcut/shortcuts/_deepin-screen-recorder.ini `、` compositor/src/treeland-shortcut/shortcuts/_deepin-screenshot.ini `、` compositor/src/treeland-shortcut/shortcuts/_deepin-system-monitor.ini `、` compositor/src/treeland-shortcut/shortcuts/_deepin-terminal.ini `、` compositor/src/treeland-shortcut/shortcuts/_global-search.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-cancel-maximize-window.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-close-multitaskview.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-close-window.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-lockscreen.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-maximize-window.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-move-window.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-next-ws.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-open-multitaskview.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-open-shutdown-menu.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-prev-ws.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-quit.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-show-desktop.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-show-window-menu.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-taskswitch-next.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-taskswitch-prev.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-taskswitch-sameapp-next.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-taskswitch-sameapp-prev.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-toggle-fpsdisplay.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-toggle-multitaskview.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-ws-1.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-ws-2.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-ws-3.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-ws-4.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-ws-5.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-ws-6.ini `、` compositor/src/treeland-shortcut/shortcuts/_uos-ai-iat.ini `、` compositor/src/treeland-shortcut/shortcuts/_uos-ai-talk.ini `、` compositor/src/treeland-shortcut/shortcuts/_uos-ai-tts.ini `、` compositor/src/treeland-shortcut/shortcuts/_uos-ai-wordwizard.ini `、` compositor/src/treeland-shortcut/shortcuts/_uos-ai.ini `。
- 实际改变：` compositor/CMakeLists.txt `、` compositor/misc/systemd/CMakeLists.txt `、` compositor/misc/systemd/dde-session-pre.target.wants/treeland-shortcut.service.in `、` compositor/src/CMakeLists.txt `、` compositor/src/treeland-shortcut/CMakeLists.txt `、` compositor/src/treeland-shortcut/shortcut.cpp `、` compositor/src/treeland-shortcut/shortcut.h `、` compositor/src/treeland-shortcut/shortcuts/_dde-clipboard.ini `、` compositor/src/treeland-shortcut/shortcuts/_dde-file-manager.ini `、` compositor/src/treeland-shortcut/shortcuts/_dde-launchpad.ini `、` compositor/src/treeland-shortcut/shortcuts/_dde-notification.ini `、` compositor/src/treeland-shortcut/shortcuts/_deepin-screen-recorder.ini `、` compositor/src/treeland-shortcut/shortcuts/_deepin-screenshot.ini `、` compositor/src/treeland-shortcut/shortcuts/_deepin-system-monitor.ini `、` compositor/src/treeland-shortcut/shortcuts/_deepin-terminal.ini `、` compositor/src/treeland-shortcut/shortcuts/_global-search.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-cancel-maximize-window.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-close-multitaskview.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-close-window.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-lockscreen.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-maximize-window.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-move-window.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-next-ws.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-open-multitaskview.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-open-shutdown-menu.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-prev-ws.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-quit.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-show-desktop.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-show-window-menu.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-taskswitch-next.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-taskswitch-prev.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-taskswitch-sameapp-next.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-taskswitch-sameapp-prev.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-toggle-fpsdisplay.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-toggle-multitaskview.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-ws-1.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-ws-2.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-ws-3.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-ws-4.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-ws-5.ini `、` compositor/src/treeland-shortcut/shortcuts/_treeland-ws-6.ini `、` compositor/src/treeland-shortcut/shortcuts/_uos-ai-iat.ini `、` compositor/src/treeland-shortcut/shortcuts/_uos-ai-talk.ini `、` compositor/src/treeland-shortcut/shortcuts/_uos-ai-tts.ini `、` compositor/src/treeland-shortcut/shortcuts/_uos-ai-wordwizard.ini `、` compositor/src/treeland-shortcut/shortcuts/_uos-ai.ini `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 3eb629c01b8d26c920ab0baededf76d35675602f ` → ` 3eb629c01b8d26c920ab0baededf76d35675602f `。
  原证据引用：` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 ` → ` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 0e2a8e1dd2c31d87fd67fc86ca5a7e6596d5f157 ` 和原目标 ` 86b8fd0b23b3e70d8ed08aa168453165971731c1 ` 查询。
- 原审核说明：` 完整删除来源清单中的内置 treeland-shortcut 客户端、默认快捷键和 systemd 接入，保留 src/modules/shortcut 协议服务。目标客户端 CMake 仅因已有 DeckCompositor 协议路径适配而与来源不同，仍整体删除；compositor/CMakeLists.txt 只去掉废弃选项，保留相邻本地 ASan 配置；src/CMakeLists.txt 保留 libdeckcompositor 和现有链接结构。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/57002bfe37a17ab11e9279253343324419a5f7c1.md)。

<a id="entry-20"></a>
### 20. N1 / ` refactor: use Q_ENUM reflection for ShortcutAction name logging `

- 本仓内容路径：` compositor/src/modules/shortcut/shortcutcontroller.cpp `、` compositor/src/modules/shortcut/shortcutcontroller.h `、` compositor/src/modules/shortcut/shortcutmanager.h `。
- 实际改变：` compositor/src/modules/shortcut/shortcutcontroller.cpp `、` compositor/src/modules/shortcut/shortcutcontroller.h `、` compositor/src/modules/shortcut/shortcutmanager.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 3eb629c01b8d26c920ab0baededf76d35675602f ` → ` 3eb629c01b8d26c920ab0baededf76d35675602f `。
  原证据引用：` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 ` → ` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` d2de8c2fc730637ae37aca693235c63168ddbf58 ` 和原目标 ` 3c69a74019ec9257c95df68ccbf2329284f383d1 ` 查询。

<a id="entry-21"></a>
### 21. N1 / ` fix(tools): integrate WindowTree client build `

- 本仓内容路径：` compositor/tools/CMakeLists.txt `、` compositor/tools/treeland-windowtree/CMakeLists.txt `、` compositor/tools/treeland-windowtree/README.md `、` compositor/tools/treeland-windowtree/pyproject.toml `、` compositor/tools/treeland-windowtree/setup.py `、` compositor/tools/treeland-windowtree/treeland-windowtree.in `。
- 实际改变：` compositor/tools/CMakeLists.txt `、` compositor/tools/treeland-windowtree/CMakeLists.txt `、` compositor/tools/treeland-windowtree/README.md `、` compositor/tools/treeland-windowtree/pyproject.toml `、` compositor/tools/treeland-windowtree/setup.py `、` compositor/tools/treeland-windowtree/treeland-windowtree.in `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 3eb629c01b8d26c920ab0baededf76d35675602f ` → ` 3eb629c01b8d26c920ab0baededf76d35675602f `。
  原证据引用：` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 ` → ` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 53637fd5388bdb5e71f4644303afe84cdbe6483b ` 和原目标 ` 4af8a96329f2782514962dbe2f8a2b179adb671f ` 查询。

<a id="entry-22"></a>
### 22. N1 / ` fix(tools): replace Python WindowTree client replace `

- 本仓内容路径：` compositor/debian/treeland.install `、` compositor/tools/CMakeLists.txt `、` compositor/tools/treeland-debug/CMakeLists.txt `、` compositor/tools/treeland-debug/README.md `、` compositor/tools/treeland-debug/main.cpp `、` compositor/tools/treeland-windowtree/CMakeLists.txt `、` compositor/tools/treeland-windowtree/README.md `、` compositor/tools/treeland-windowtree/pyproject.toml `、` compositor/tools/treeland-windowtree/setup.py `、` compositor/tools/treeland-windowtree/src/treeland_windowtree/_core.cpp `、` compositor/tools/treeland-windowtree/treeland-windowtree.in `、` compositor/tools/treeland-windowtree/treeland_windowtree/__init__.py `、` compositor/tools/treeland-windowtree/treeland_windowtree/cli.py `。
- 实际改变：` compositor/debian/treeland.install `、` compositor/tools/CMakeLists.txt `、` compositor/tools/treeland-debug/CMakeLists.txt `、` compositor/tools/treeland-debug/README.md `、` compositor/tools/treeland-debug/main.cpp `、` compositor/tools/treeland-windowtree/CMakeLists.txt `、` compositor/tools/treeland-windowtree/README.md `、` compositor/tools/treeland-windowtree/pyproject.toml `、` compositor/tools/treeland-windowtree/setup.py `、` compositor/tools/treeland-windowtree/src/treeland_windowtree/_core.cpp `、` compositor/tools/treeland-windowtree/treeland-windowtree.in `、` compositor/tools/treeland-windowtree/treeland_windowtree/__init__.py `、` compositor/tools/treeland-windowtree/treeland_windowtree/cli.py `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 3eb629c01b8d26c920ab0baededf76d35675602f ` → ` 3eb629c01b8d26c920ab0baededf76d35675602f `。
  原证据引用：` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 ` → ` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 8f387a5b4d94fc1590548f51979a7ac718689c73 ` 和原目标 ` dc1e7c311ff660c04e500e4e70171f78c8d342ff ` 查询。

<a id="entry-23"></a>
### 23. N1 / ` refactor(surface): merge PopupFocusManager into SeatSurfaceManager `

- 本仓内容路径：` compositor/src/CMakeLists.txt `、` compositor/src/core/popupfocusmanager.cpp `、` compositor/src/core/popupfocusmanager.h `、` compositor/src/core/rootsurfacecontainer.cpp `、` compositor/src/core/rootsurfacecontainer.h `、` compositor/src/core/shellhandler.cpp `、` compositor/src/core/shellhandler.h `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `、` compositor/src/workspace/workspace.cpp `。
- 实际改变：` compositor/src/CMakeLists.txt `、` compositor/src/core/popupfocusmanager.cpp `、` compositor/src/core/popupfocusmanager.h `、` compositor/src/core/rootsurfacecontainer.cpp `、` compositor/src/core/rootsurfacecontainer.h `、` compositor/src/core/shellhandler.cpp `、` compositor/src/core/shellhandler.h `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `、` compositor/src/workspace/workspace.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 3eb629c01b8d26c920ab0baededf76d35675602f ` → ` 3eb629c01b8d26c920ab0baededf76d35675602f `。
  原证据引用：` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 ` → ` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 4410a4d8201987eed9d6e1fd3791f19ee0ac6c89 ` 和原目标 ` 888fd1a0a97e288283833c343fd81d8281eefc6e ` 查询。
- 原审核说明：` 在原有规范文件中完整合并 PopupFocusManager 到 SeatSurfaceManager，删除原类及全部构建/调用入口，并通过 RootSurfaceContainer 逐座席路由 popup grab；源头文件改动包含已在目标规范化的空行，三方合并保留该格式。实际目标树中已无 PopupFocusManager 或 popupFocusManager() 残留调用，没有在兄弟文件保留平行实现。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/4f13127f5af15bbeb3ac06b7162681c0e568931b.md)。

<a id="entry-24"></a>
### 24. N1 / ` fix(greeter): reconnect to DDM on service changes `

- 本仓内容路径：` compositor/src/greeter/greeterproxy.cpp `。
- 实际改变：` compositor/src/greeter/greeterproxy.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 3eb629c01b8d26c920ab0baededf76d35675602f ` → ` 3eb629c01b8d26c920ab0baededf76d35675602f `。
  原证据引用：` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 ` → ` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 997937396a22fc6b3729b124343271e4202df044 ` 和原目标 ` 5d42e8135aebf98859cebf013c0bd8be5e2d27b4 ` 查询。

<a id="entry-25"></a>
### 25. N1 / ` fix(seat): clear keyboard focus for all seats on internal QML focus `

- 本仓内容路径：` compositor/src/seat/helper.cpp `。
- 实际改变：` compositor/src/seat/helper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 3eb629c01b8d26c920ab0baededf76d35675602f ` → ` 3eb629c01b8d26c920ab0baededf76d35675602f `。
  原证据引用：` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 ` → ` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 250a4889fd74676bb23b74c245b0ef77c0467778 ` 和原目标 ` 263b90392e5b14bc21487c664290d9bc9dc0f64f ` 查询。

<a id="entry-26"></a>
### 26. N1 / ` docs: update agent skills with accuracy fixes and review corrections `

- 本仓内容路径：` compositor/.agents/skills/logging-guidelines/SKILL.md `、` compositor/.agents/skills/treeland-private-wayland-protocol/SKILL.md `、` compositor/AGENTS.md `、` compositor/src/modules/activation/activationmanagerinterfacev1.cpp `、` compositor/src/modules/prelaunch-splash/prelaunchsplash.cpp `。
- 实际改变：` compositor/.agents/skills/logging-guidelines/SKILL.md `、` compositor/.agents/skills/treeland-private-wayland-protocol/SKILL.md `、` compositor/AGENTS.md `、` compositor/src/modules/activation/activationmanagerinterfacev1.cpp `、` compositor/src/modules/prelaunch-splash/prelaunchsplash.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 3eb629c01b8d26c920ab0baededf76d35675602f ` → ` 3eb629c01b8d26c920ab0baededf76d35675602f `。
  原证据引用：` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 ` → ` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 1f8416145ca848d9affdccae3a9aa35c23f0c883 ` 和原目标 ` 04983aa6b262472459cb0ab00f654d87a11bf84f ` 查询。
- 原审核说明：` 保留来源的技能准确性、资源接口和 Helper 入口说明；新增协议来源说明改为目标已验证的 protocols/compositor、DeckCompositorProtocols 0.5.9 与 DECKCOMPOSITOR_PROTOCOLS_DATA_DIR，同时区分系统 xdg-activation 标准 XML。不保留同段已删除 treeland-shortcut 的日志示例；其余源码改动按来源同步，未改变 XML。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/fbfe8bb9407007cbccdbb7fb5452633661c94a3c.md)。

<a id="entry-27"></a>
### 27. N1 / ` fix(lockscreen): accept numpad Enter key for password submission `

- 本仓内容路径：` compositor/src/plugins/lockscreen/qml/UserInput.qml `。
- 实际改变：` compositor/src/plugins/lockscreen/qml/UserInput.qml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 3eb629c01b8d26c920ab0baededf76d35675602f ` → ` 3eb629c01b8d26c920ab0baededf76d35675602f `。
  原证据引用：` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 ` → ` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` ea290441942f04bada1ba8fda7897b12cf26b158 ` 和原目标 ` 4f8af2f049888b30f991d26cbbe18ff89bdfc604 ` 查询。

<a id="entry-28"></a>
### 28. N1 / ` chore: bump version to 0.8.15 `

- 本仓内容路径：` compositor/CMakeLists.txt `、` compositor/debian/changelog `。
- 实际改变：` compositor/CMakeLists.txt `、` compositor/debian/changelog `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 3eb629c01b8d26c920ab0baededf76d35675602f ` → ` 3eb629c01b8d26c920ab0baededf76d35675602f `。
  原证据引用：` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 ` → ` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/parent-evidence.json`；以来源 ` 2df4c21c0499b46229f1ef0080cc265994b4fd60 ` 和原目标 ` 055be261d35138ec678b3a7aaf1521bfc2d9a05e ` 查询。
- 原审核说明：` 来源仅更新 0.8.15 版本与 changelog；目标在 compositor/CMakeLists.txt 的同一 project() 中更新 VERSION，保留 DeckCompositor 名称、描述、根项目集成和本地构建选项，changelog 按来源补丁同步。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/aab728dd63010fd3004aa04ddf283ddb704d302a.md)。

<a id="entry-29"></a>
### 29. N2 / ` 首次 wlroots 独立初始化 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 3eb629c01b8d26c920ab0baededf76d35675602f ` → ` 827ea426576b8990e393500a4f976a8c7b2ae57f `。
  原证据引用：` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 ` → ` 05e24276e3d5878b653adf692cd33391038dd398 `。
- **独立初始化，不属于普通 replay/action 计数。**
- 来源第一父提交：` 2df4c21c0499b46229f1ef0080cc265994b4fd60 `；导入原始 R：` 88a869855742281c98c22cab9641b317b8d065ef `。
- 接入方式：` native-meson-via-local-pkg-config-imported-target `；原始历史对象不重写。
- 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/initialization-report.json`；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/structure-proof.json`。
- 原审核说明：` 独立初始化，只传播已审核的 C 依赖；没有 P 源码适配。 `。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 827ea426576b8990e393500a4f976a8c7b2ae57f `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-30"></a>
### 30. N3 / ` build: add waylib-wlroots CMake module and switch consumers `

- 本仓内容路径：` .github/workflows/qwlroots-archlinux-build.yml `、` .github/workflows/qwlroots-debian-build.yml `、` .github/workflows/qwlroots-deepin-build.yml `、` .github/workflows/treeland-archlinux-build.yml `、` .github/workflows/waylib-archlinux-build.yml `、` .github/workflows/waylib-debian-build.yml `、` .github/workflows/waylib-deepin-build.yml `、` compositor/CMakeLists.txt `、` compositor/REUSE.toml `、` compositor/debian/control `、` compositor/src/modules/capture/CMakeLists.txt `、` compositor/src/modules/shortcut/CMakeLists.txt `、` compositor/src/modules/virtual-output/CMakeLists.txt `、` compositor/src/modules/wallpaper-color/CMakeLists.txt `、` compositor/src/modules/window-management/CMakeLists.txt `。
- 实际改变：` .github/workflows/qwlroots-archlinux-build.yml `、` .github/workflows/qwlroots-debian-build.yml `、` .github/workflows/qwlroots-deepin-build.yml `、` .github/workflows/treeland-archlinux-build.yml `、` .github/workflows/waylib-archlinux-build.yml `、` .github/workflows/waylib-debian-build.yml `、` .github/workflows/waylib-deepin-build.yml `、` 3rdparty/waylib-shared `、` compositor/CMakeLists.txt `、` compositor/REUSE.toml `、` compositor/debian/control `、` compositor/src/modules/capture/CMakeLists.txt `、` compositor/src/modules/shortcut/CMakeLists.txt `、` compositor/src/modules/virtual-output/CMakeLists.txt `、` compositor/src/modules/wallpaper-color/CMakeLists.txt `、` compositor/src/modules/window-management/CMakeLists.txt `。
- 排除的来源路径：` 3rdparty/wlroots/types/seat/wlr_seat_pointer.c `、` 3rdparty/wlroots/types/xdg_shell/wlr_xdg_popup.c `、` 3rdparty/wlroots/xwayland/xwm.c `、` qwlroots/CMakeLists.txt `、` qwlroots/debian/control `、` qwlroots/src/CMakeLists.txt `、` qwlroots/src/cmake/CMakeConfig.cmake.in `、` waylib/debian/control `、` waylib/src/server/CMakeLists.txt `、` wlroots/CMakeLists.txt `、` wlroots/UPSTREAM `、` wlroots/cmake/WlrootsProtocols.cmake `、` wlroots/cmake/WlrootsShaders.cmake `、` wlroots/cmake/WlrootsSources.cmake `、` wlroots/update-from-upstream.sh `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 827ea426576b8990e393500a4f976a8c7b2ae57f ` → ` 56a2765a569517f8f19b732e5bc1a75a65c476b5 `。
  原证据引用：` 05e24276e3d5878b653adf692cd33391038dd398 ` → ` 2e9e9ce9ff975fb39b7a506d96562d94b216e831 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` 896a8953e3695577e05e9e93d10530920dc7d6d9 ` 和原目标 ` 1fb372d2deb909815b26a58ffcc0311b50b7481c ` 查询。
- 原审核说明：` 在规范 compositor 路径保留 DeckShell 项目与 WaylibShared 名称，将模块依赖切换到当前子仓的 Wlroots::wlroots；根部只验证已由 C 提供的 target。CI 路径映射至固定子模块并保留独立子项目公开开发依赖，远端 R URL 不属于本次本地交付。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/26804e427f757e0185dc95e699d57f880045ec65.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 56a2765a569517f8f19b732e5bc1a75a65c476b5 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-31"></a>
### 31. N3 / ` feat(wm): implement show-desktop via taskbar click `

- 本仓内容路径：` compositor/src/modules/window-management/windowmanagementinterfacev1.cpp `、` compositor/src/modules/window-management/windowmanagementinterfacev1.h `。
- 实际改变：` compositor/src/modules/window-management/windowmanagementinterfacev1.cpp `、` compositor/src/modules/window-management/windowmanagementinterfacev1.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 56a2765a569517f8f19b732e5bc1a75a65c476b5 ` → ` 56a2765a569517f8f19b732e5bc1a75a65c476b5 `。
  原证据引用：` 2e9e9ce9ff975fb39b7a506d96562d94b216e831 ` → ` 2e9e9ce9ff975fb39b7a506d96562d94b216e831 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` 719523d3c31281c47991cf5e73c93d839aa44398 ` 和原目标 ` 1c2b1392fad8091d2454eddb1c2986614d0db510 ` 查询。

<a id="entry-32"></a>
### 32. N3 / ` fix(lockscreen): reposition caps indicator and center password input `

- 本仓内容路径：` compositor/src/plugins/lockscreen/qml/UserInput.qml `。
- 实际改变：` compositor/src/plugins/lockscreen/qml/UserInput.qml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 56a2765a569517f8f19b732e5bc1a75a65c476b5 ` → ` 56a2765a569517f8f19b732e5bc1a75a65c476b5 `。
  原证据引用：` 2e9e9ce9ff975fb39b7a506d96562d94b216e831 ` → ` 2e9e9ce9ff975fb39b7a506d96562d94b216e831 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` a4beeb367b4451fa36fc52accee720d807341364 ` 和原目标 ` 22e870cff432c0d4c0278f412308ac6ee59aba39 ` 查询。
- 原审核说明：` 保留来源密码输入居中与 Caps 指示器重排的全部行为，仅去除该来源新增空行的行尾空格。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/ef863a85b3046941b067ecec6f829222c67d6adf.md)。

<a id="entry-33"></a>
### 33. N3 / ` fix(output): detach proxy hardware layers before output teardown `

- 本仓内容路径：` compositor/src/output/output.cpp `。
- 实际改变：` compositor/src/output/output.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 56a2765a569517f8f19b732e5bc1a75a65c476b5 ` → ` 56a2765a569517f8f19b732e5bc1a75a65c476b5 `。
  原证据引用：` 2e9e9ce9ff975fb39b7a506d96562d94b216e831 ` → ` 2e9e9ce9ff975fb39b7a506d96562d94b216e831 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` 4dbcf637cfccb6d2814b05e5e777e37031623f71 ` 和原目标 ` fef857ebd2377692d1f1b50210b1c54976008486 ` 查询。

<a id="entry-34"></a>
### 34. N3 / ` fix(taskswitch): reset currentMode when dismissed by mouse click `

- 本仓内容路径：` compositor/src/seat/helper.cpp `。
- 实际改变：` compositor/src/seat/helper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 56a2765a569517f8f19b732e5bc1a75a65c476b5 ` → ` 56a2765a569517f8f19b732e5bc1a75a65c476b5 `。
  原证据引用：` 2e9e9ce9ff975fb39b7a506d96562d94b216e831 ` → ` 2e9e9ce9ff975fb39b7a506d96562d94b216e831 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` ca8a95ff333080d56bbc3b9895966160f1c96071 ` 和原目标 ` d79286b5db3e20964340db4edcafbd8d3bd71e3d ` 查询。

<a id="entry-35"></a>
### 35. N3 / ` fix(surface): track subsurface teardown independently `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/kernel/wsurface.cpp `、` waylib/src/server/qtquick/private/wsurfaceitem_p.h `、` waylib/src/server/qtquick/wsurfaceitem.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 56a2765a569517f8f19b732e5bc1a75a65c476b5 ` → ` 23ab4323280d7ccbcfc0b7309f0679af56fe9f6e `。
  原证据引用：` 2e9e9ce9ff975fb39b7a506d96562d94b216e831 ` → ` f477380331437ea960565a87b8162f3a6aa65321 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` aac67eea93c777558d41903c7a37f360ec0fbe81 ` 和原目标 ` 2429fe320875bf811580322582e2c0b638651929 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 23ab4323280d7ccbcfc0b7309f0679af56fe9f6e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-36"></a>
### 36. N3 / ` fix: resolve -Wsfinae-incomplete moc warnings `

- 本仓内容路径：` compositor/src/core/shellhandler.h `、` compositor/src/modules/foreign-toplevel/dockpreviewcontextv1.h `。
- 实际改变：` compositor/src/core/shellhandler.h `、` compositor/src/modules/foreign-toplevel/dockpreviewcontextv1.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 23ab4323280d7ccbcfc0b7309f0679af56fe9f6e ` → ` 23ab4323280d7ccbcfc0b7309f0679af56fe9f6e `。
  原证据引用：` f477380331437ea960565a87b8162f3a6aa65321 ` → ` f477380331437ea960565a87b8162f3a6aa65321 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` 8a3e65490a7380fdd168fdac4d92634445816014 ` 和原目标 ` aeeab25755ec7b82367559759bca2bc63931a052 ` 查询。

<a id="entry-37"></a>
### 37. N3 / ` fix(surface): distinguish popup/IME/drag keyboard grabs `

- 本仓内容路径：` compositor/src/core/shellhandler.h `、` compositor/src/surface/seatsurfacemanager.cpp `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/core/shellhandler.h `、` compositor/src/surface/seatsurfacemanager.cpp `。
- 排除的来源路径：` waylib/src/server/protocols/winputmethodhelper.cpp `、` waylib/src/server/protocols/winputmethodhelper.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 23ab4323280d7ccbcfc0b7309f0679af56fe9f6e ` → ` f7a593d1112a9c34d2d5900820fd137205e86fe7 `。
  原证据引用：` f477380331437ea960565a87b8162f3a6aa65321 ` → ` 30f6a61d4392ad4cc15dbfdd40a16155adfabe44 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` ff0aa9861d0d71b723da86483d0571b4aa1beab3 ` 和原目标 ` 9bc70b772c698a8d9c215b8543dc3960ab269f9a ` 查询。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 同一 Treeland 来源的 C / waylib-shared 目标：` f7a593d1112a9c34d2d5900820fd137205e86fe7 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-38"></a>
### 38. N3 / ` fix(surface): remove cached subsurface state `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/kernel/private/wsurface_p.h `、` waylib/src/server/kernel/wsurface.cpp `、` waylib/src/server/kernel/wsurface.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` f7a593d1112a9c34d2d5900820fd137205e86fe7 ` → ` 1054d79edbc86132c09c6fd0d94b09ae16ffdf66 `。
  原证据引用：` 30f6a61d4392ad4cc15dbfdd40a16155adfabe44 ` → ` 7bba19b60c4203f530c9b3ca79f521d9ed2d4bb2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` 0d008c38411bb097ab66cc78a1593ea985dd6a06 ` 和原目标 ` 60300fc3271ad5af489370a96b1bd4c5d52777c2 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 1054d79edbc86132c09c6fd0d94b09ae16ffdf66 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-39"></a>
### 39. N3 / ` fix(CI): update cppcheck.yml `

- 本仓内容路径：` .github/workflows/cppcheck.yml `。
- 实际改变：` .github/workflows/cppcheck.yml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 1054d79edbc86132c09c6fd0d94b09ae16ffdf66 ` → ` 1054d79edbc86132c09c6fd0d94b09ae16ffdf66 `。
  原证据引用：` 7bba19b60c4203f530c9b3ca79f521d9ed2d4bb2 ` → ` 7bba19b60c4203f530c9b3ca79f521d9ed2d4bb2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` 25258137413e911c9ef21b76dab49c1a43b192a8 ` 和原目标 ` 8adafa80d63494fe533aeff2010f84dc706274e0 ` 查询。

<a id="entry-40"></a>
### 40. N3 / ` fix(task-switcher): preserve surface positions during exit `

- 本仓内容路径：` compositor/src/core/qml/TaskSwitcher.qml `、` compositor/src/surface/surfacefilterproxymodel.cpp `、` compositor/src/surface/surfacefilterproxymodel.h `。
- 实际改变：` compositor/src/core/qml/TaskSwitcher.qml `、` compositor/src/surface/surfacefilterproxymodel.cpp `、` compositor/src/surface/surfacefilterproxymodel.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 1054d79edbc86132c09c6fd0d94b09ae16ffdf66 ` → ` 1054d79edbc86132c09c6fd0d94b09ae16ffdf66 `。
  原证据引用：` 7bba19b60c4203f530c9b3ca79f521d9ed2d4bb2 ` → ` 7bba19b60c4203f530c9b3ca79f521d9ed2d4bb2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` d3d186b30d2d0dc41f4b53ce106bdc4d5f007513 ` 和原目标 ` f98f940f915b2526c5f5d210be501d04d64eda21 ` 查询。

<a id="entry-41"></a>
### 41. N3 / ` fix: resolve sfinae and qml type registration warnings `

- 本仓内容路径：` compositor/src/CMakeLists.txt `、` compositor/src/core/shellhandler.h `、` compositor/src/modules/capture/CMakeLists.txt `、` compositor/src/modules/foreign-toplevel/foreigntoplevelhandlev1.h `、` compositor/src/seat/helper.h `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/CMakeLists.txt `、` compositor/src/core/shellhandler.h `、` compositor/src/modules/capture/CMakeLists.txt `、` compositor/src/modules/foreign-toplevel/foreigntoplevelhandlev1.h `、` compositor/src/seat/helper.h `。
- 排除的来源路径：` waylib/examples/tinywl/CMakeLists.txt `、` waylib/src/server/kernel/wbackend.h `、` waylib/src/server/kernel/woutputlayout.h `、` waylib/src/server/kernel/wseat.h `、` waylib/src/server/kernel/wsurface.h `、` waylib/src/server/protocols/wlayershell.h `、` waylib/src/server/protocols/wxdgdialogmanagerv1.h `、` waylib/src/server/protocols/wxdgshell.h `、` waylib/src/server/protocols/wxwayland.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 1054d79edbc86132c09c6fd0d94b09ae16ffdf66 ` → ` 5e859f63bebca57be2237e75174a20f265611349 `。
  原证据引用：` 7bba19b60c4203f530c9b3ca79f521d9ed2d4bb2 ` → ` 4a419790f030e9b5e92e2a9d3503b9e1ea56d944 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` 5a90432efb33646a8d1e92ce2c5901e0dcb7fc04 ` 和原目标 ` 08922d0411ff55d471df1374475f5978cd26a5f5 ` 查询。
- 原审核说明：` 在规范路径三方合并本次来源，保留已审核的 DeckShell/WaylibShared 名称及本地集成差异；所有新增行为仍来自该来源，不扩展兄弟文件。；QML IMPORTS 映射到本项目实际 URI WaylibShared.QuickSharedServer/DeckShell.Compositor，版本限定使用 Qt 的 URI/version 语法，并随后按来源移除限定。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/e40c04aa9f3db51e408c37421901341169860186.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 5e859f63bebca57be2237e75174a20f265611349 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-42"></a>
### 42. N3 / ` fix: fix XWayland cursor truncation on fractional-scaled multi-monitor `

- 本仓内容路径：` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `。
- 排除的来源路径：` waylib/src/server/protocols/wxdgoutput.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 5e859f63bebca57be2237e75174a20f265611349 ` → ` 6f46e9498ff1b4caec6cb1f035ef05a5b43b4873 `。
  原证据引用：` 4a419790f030e9b5e92e2a9d3503b9e1ea56d944 ` → ` c7f3abfdc806fc9b8dff1aada32d131e52c9aa2e `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` 4e21f708be59d24f4aac55bcdc3964a800feb74c ` 和原目标 ` a93a699c0c49f7c50ae9bac088792de6152574a9 ` 查询。
- 原审核说明：` 在规范路径三方合并本次来源，保留已审核的 DeckShell/WaylibShared 名称及本地集成差异；所有新增行为仍来自该来源，不扩展兄弟文件。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/8200c899f854b92e643dae7134771be7e563ae5e.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 6f46e9498ff1b4caec6cb1f035ef05a5b43b4873 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-43"></a>
### 43. N3 / ` fix(output): restore configured topology after output reconnect `

- 本仓内容路径：` compositor/misc/dconfig/org.deepin.dde.treeland.json `、` compositor/misc/dconfig/org.deepin.dde.treeland.output.json `、` compositor/src/CMakeLists.txt `、` compositor/src/modules/virtual-output/virtualoutputmanagerinterfacev1.cpp `、` compositor/src/modules/virtual-output/virtualoutputmanagerinterfacev1.h `、` compositor/src/output/output.cpp `、` compositor/src/output/outputconfigstate.cpp `、` compositor/src/output/outputconfigstate.h `、` compositor/src/output/outputlifecyclemanager.cpp `、` compositor/src/output/outputlifecyclemanager.h `、` compositor/src/output/outputmanager.cpp `、` compositor/src/output/outputmanager.h `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/misc/dconfig/org.deepin.dde.treeland.json `、` compositor/misc/dconfig/org.deepin.dde.treeland.output.json `、` compositor/src/CMakeLists.txt `、` compositor/src/modules/virtual-output/virtualoutputmanagerinterfacev1.cpp `、` compositor/src/modules/virtual-output/virtualoutputmanagerinterfacev1.h `、` compositor/src/output/output.cpp `、` compositor/src/output/outputconfigstate.cpp `、` compositor/src/output/outputconfigstate.h `、` compositor/src/output/outputlifecyclemanager.cpp `、` compositor/src/output/outputlifecyclemanager.h `、` compositor/src/output/outputmanager.cpp `、` compositor/src/output/outputmanager.h `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `。
- 排除的来源路径：` waylib/src/server/qtquick/woutputviewport.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 6f46e9498ff1b4caec6cb1f035ef05a5b43b4873 ` → ` 557ccb9c28071777197ab456546207c8dd3f85f6 `。
  原证据引用：` c7f3abfdc806fc9b8dff1aada32d131e52c9aa2e ` → ` ab88bfa08af0973888b967304b25c274a656c2ac `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` 268ca973be0d5eeb33d6be03b5e51e4ce62f4997 ` 和原目标 ` 939f7acabeaca39c0dfccf8b2568f8c79b57758f ` 查询。
- 原审核说明：` 合入输出拓扑持久化、重连恢复及虚拟输出组接口；保留本地协议 destroy 生命周期和 pendingConfig 回调命名，省略来源新增但未使用的 outputName/enabled 捕获；4 个旧实现与来源前像一致，已移入回收站。；QML IMPORTS 映射到本项目实际 URI WaylibShared.QuickSharedServer/DeckShell.Compositor，版本限定使用 Qt 的 URI/version 语法，并随后按来源移除限定。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/5f58534233351c8ce506c055726e46fe7e59b4c7.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 557ccb9c28071777197ab456546207c8dd3f85f6 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-44"></a>
### 44. N3 / ` fix: remove version pinning from QML module IMPORTS `

- 本仓内容路径：` compositor/src/CMakeLists.txt `、` compositor/src/modules/capture/CMakeLists.txt `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/CMakeLists.txt `、` compositor/src/modules/capture/CMakeLists.txt `。
- 排除的来源路径：` waylib/examples/tinywl/CMakeLists.txt `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 557ccb9c28071777197ab456546207c8dd3f85f6 ` → ` c5ec822f8301881b46570c7e39148712f82b1809 `。
  原证据引用：` ab88bfa08af0973888b967304b25c274a656c2ac ` → ` 37609f7ef1d1cf24cc5490d5ed3198fb240a097b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` 34049a416fb66f7c6c8ab73dbda3e42e9c59f309 ` 和原目标 ` 0c438ce5dd97d84f35deaa62584edbcd501f0ffd ` 查询。
- 原审核说明：` 在规范路径三方合并本次来源，保留已审核的 DeckShell/WaylibShared 名称及本地集成差异；所有新增行为仍来自该来源，不扩展兄弟文件。；QML IMPORTS 映射到本项目实际 URI WaylibShared.QuickSharedServer/DeckShell.Compositor，版本限定使用 Qt 的 URI/version 语法，并随后按来源移除限定。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/bcb590e170012289b985f5334316a6bdd1c4d773.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` c5ec822f8301881b46570c7e39148712f82b1809 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-45"></a>
### 45. N3 / ` fix(input): filter hold gestures by finger count at start `

- 本仓内容路径：` compositor/src/input/gestures.cpp `、` compositor/src/input/gestures.h `、` compositor/src/input/inputdevice.cpp `。
- 实际改变：` compositor/src/input/gestures.cpp `、` compositor/src/input/gestures.h `、` compositor/src/input/inputdevice.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` c5ec822f8301881b46570c7e39148712f82b1809 ` → ` c5ec822f8301881b46570c7e39148712f82b1809 `。
  原证据引用：` 37609f7ef1d1cf24cc5490d5ed3198fb240a097b ` → ` 37609f7ef1d1cf24cc5490d5ed3198fb240a097b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` 7228321461027bb935a08593d8d1363a14ddcbdb ` 和原目标 ` f44b2435b906db13175c43a86dfbbbca7a0905bf ` 查询。

<a id="entry-46"></a>
### 46. N3 / ` fix(input): trigger hold gesture immediately with configurable timeout `

- 本仓内容路径：` compositor/misc/dconfig/org.deepin.dde.treeland.user.seat.json `、` compositor/src/input/gestures.cpp `、` compositor/src/input/gestures.h `、` compositor/src/input/inputdevice.cpp `、` compositor/src/input/inputdevice.h `、` compositor/src/input/inputmanager.cpp `。
- 实际改变：` compositor/misc/dconfig/org.deepin.dde.treeland.user.seat.json `、` compositor/src/input/gestures.cpp `、` compositor/src/input/gestures.h `、` compositor/src/input/inputdevice.cpp `、` compositor/src/input/inputdevice.h `、` compositor/src/input/inputmanager.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` c5ec822f8301881b46570c7e39148712f82b1809 ` → ` c5ec822f8301881b46570c7e39148712f82b1809 `。
  原证据引用：` 37609f7ef1d1cf24cc5490d5ed3198fb240a097b ` → ` 37609f7ef1d1cf24cc5490d5ed3198fb240a097b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` 649d00ca053b4085520fdda3d4271973d258bf22 ` 和原目标 ` 4acc3fd146d0a36fd5094eb2f95f288150dcf8ae ` 查询。

<a id="entry-47"></a>
### 47. N3 / ` feat: set fcitx input method environment in session service `

- 本仓内容路径：` compositor/misc/systemd/dde-session-pre.target.wants/treeland-sd.service.in `。
- 实际改变：` compositor/misc/systemd/dde-session-pre.target.wants/treeland-sd.service.in `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` c5ec822f8301881b46570c7e39148712f82b1809 ` → ` c5ec822f8301881b46570c7e39148712f82b1809 `。
  原证据引用：` 37609f7ef1d1cf24cc5490d5ed3198fb240a097b ` → ` 37609f7ef1d1cf24cc5490d5ed3198fb240a097b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` 93777bf5546bba1a4d106fe1da44a6a0d4811845 ` 和原目标 ` c6f031ff080fca9e0762776231472ce3f2fb6eda ` 查询。

<a id="entry-48"></a>
### 48. N3 / ` fix(workspace): activate focus on touchpad gesture workspace switch `

- 本仓内容路径：` compositor/src/modules/shortcut/shortcutrunner.cpp `、` compositor/src/workspace/workspace.cpp `、` compositor/src/workspace/workspace.h `。
- 实际改变：` compositor/src/modules/shortcut/shortcutrunner.cpp `、` compositor/src/workspace/workspace.cpp `、` compositor/src/workspace/workspace.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` c5ec822f8301881b46570c7e39148712f82b1809 ` → ` c5ec822f8301881b46570c7e39148712f82b1809 `。
  原证据引用：` 37609f7ef1d1cf24cc5490d5ed3198fb240a097b ` → ` 37609f7ef1d1cf24cc5490d5ed3198fb240a097b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` ae0648cf38e2a9ce6cf62dd8f281b75ff91dd553 ` 和原目标 ` dd0e75c9b6e1009de549ae25bd48ac5f5274630d ` 查询。

<a id="entry-49"></a>
### 49. N3 / ` fix(waylib/xwayland): deny Activate for surfaces without Focus capability `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/protocols/wxwaylandsurface.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` c5ec822f8301881b46570c7e39148712f82b1809 ` → ` 6e4916aa969d77c67a4a96c05554ccc1f8c12b68 `。
  原证据引用：` 37609f7ef1d1cf24cc5490d5ed3198fb240a097b ` → ` 1db059be68d697b7c47c7003f7433e0d1836139a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` 25cb8dd422d381b64f18f535a51066c85d80818b ` 和原目标 ` 53e4aeacddc45f1923bba37fc1fe7f3c53d52919 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 6e4916aa969d77c67a4a96c05554ccc1f8c12b68 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-50"></a>
### 50. N3 / ` chore: bump version to 0.8.16 `

- 本仓内容路径：` compositor/CMakeLists.txt `、` compositor/debian/changelog `。
- 实际改变：` compositor/CMakeLists.txt `、` compositor/debian/changelog `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 6e4916aa969d77c67a4a96c05554ccc1f8c12b68 ` → ` 6e4916aa969d77c67a4a96c05554ccc1f8c12b68 `。
  原证据引用：` 1db059be68d697b7c47c7003f7433e0d1836139a ` → ` 1db059be68d697b7c47c7003f7433e0d1836139a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/parent-evidence.json`；以来源 ` 4db6917f873990966f58578abe7dca8b8b371d36 ` 和原目标 ` dc4f7d20294b8b6fa9decc39a783bf504246f34e ` 查询。
- 原审核说明：` 按来源升级到 0.8.16 并完整保留 Debian changelog；仅保留目标 DeckCompositor 的项目名称、结构与构建选项。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/322a731543791a78d4e7ac485468c22409f309bf.md)。

<a id="entry-51"></a>
### 51. N4 / ` fix(surface): add m_wrapperAboutToRemove guard to updateBoundingRect `

- 本仓内容路径：` compositor/src/surface/surfacewrapper.cpp `。
- 实际改变：` compositor/src/surface/surfacewrapper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 6e4916aa969d77c67a4a96c05554ccc1f8c12b68 ` → ` 6e4916aa969d77c67a4a96c05554ccc1f8c12b68 `。
  原证据引用：` 1db059be68d697b7c47c7003f7433e0d1836139a ` → ` 1db059be68d697b7c47c7003f7433e0d1836139a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` 57aeaea3b99ef70cd6a1f3edba13e245ce58cd5d ` 和原目标 ` bb89b79e2524df37bb508cbf2f243c0d0fb1db25 ` 查询。

<a id="entry-52"></a>
### 52. N4 / ` feat(waylib): add _NET_WM_WINDOW_TYPE_DIALOG support for XWayland `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/protocols/wxwayland.h `、` waylib/src/server/protocols/wxwaylandsurface.cpp `、` waylib/src/server/protocols/wxwaylandsurface.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 6e4916aa969d77c67a4a96c05554ccc1f8c12b68 ` → ` d64bb4cc5e2670a46f2e0ef5c06f45b90b6291d7 `。
  原证据引用：` 1db059be68d697b7c47c7003f7433e0d1836139a ` → ` d0b854c0fb58851c2da86e5e7a8d90f8fa354c48 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` d4e547c9f0094626689b5db8e95db0da49164b50 ` 和原目标 ` 67b5d6b215a588213e196760f862af0a166c4c69 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` d64bb4cc5e2670a46f2e0ef5c06f45b90b6291d7 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-53"></a>
### 53. N4 / ` fix(surface): fix skipSwitcher/skipMultitaskView for X11 surfaces `

- 本仓内容路径：` compositor/src/plugins/multitaskview/multitaskview.cpp `、` compositor/src/surface/surfacefilterproxymodel.cpp `、` compositor/src/surface/surfacewrapper.cpp `。
- 实际改变：` compositor/src/plugins/multitaskview/multitaskview.cpp `、` compositor/src/surface/surfacefilterproxymodel.cpp `、` compositor/src/surface/surfacewrapper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` d64bb4cc5e2670a46f2e0ef5c06f45b90b6291d7 ` → ` d64bb4cc5e2670a46f2e0ef5c06f45b90b6291d7 `。
  原证据引用：` d0b854c0fb58851c2da86e5e7a8d90f8fa354c48 ` → ` d0b854c0fb58851c2da86e5e7a8d90f8fa354c48 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` 48da5274244c1a78f3130b321f1d70f9a53e10e2 ` 和原目标 ` b411ecb5c43efd4b359e4352d0725a2464518f48 ` 查询。

<a id="entry-54"></a>
### 54. N4 / ` fix(task-switcher): restore surface state after interrupted exit `

- 本仓内容路径：` compositor/src/core/qml/TaskSwitcher.qml `。
- 实际改变：` compositor/src/core/qml/TaskSwitcher.qml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` d64bb4cc5e2670a46f2e0ef5c06f45b90b6291d7 ` → ` d64bb4cc5e2670a46f2e0ef5c06f45b90b6291d7 `。
  原证据引用：` d0b854c0fb58851c2da86e5e7a8d90f8fa354c48 ` → ` d0b854c0fb58851c2da86e5e7a8d90f8fa354c48 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` 97bfdf2a44975ba53f5f417b661f596fa76a30bd ` 和原目标 ` d64dab08dab9c84dbfea4998fce212cfc5b519cb ` 查询。

<a id="entry-55"></a>
### 55. N4 / ` fix(input): handle drags without an icon `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/kernel/wseat.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` d64bb4cc5e2670a46f2e0ef5c06f45b90b6291d7 ` → ` 4df2dfc789813ae121f738166ddf9d0df3897c39 `。
  原证据引用：` d0b854c0fb58851c2da86e5e7a8d90f8fa354c48 ` → ` 55c904bbbe0e3520a86eca9792b748a530e171ac `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` 1f5d35eadc6ce02d708a7edadba97a56bf2a7883 ` 和原目标 ` 6ce8fe0c1a91c4617d88818256ec5191c6e6581f ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 4df2dfc789813ae121f738166ddf9d0df3897c39 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-56"></a>
### 56. N4 / ` fix(input): allow drag source to update cursor `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/kernel/wseat.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 4df2dfc789813ae121f738166ddf9d0df3897c39 ` → ` 5f878b97d3420b99c988e546bdadd3098bd51d89 `。
  原证据引用：` 55c904bbbe0e3520a86eca9792b748a530e171ac ` → ` 6e8369a56b958114ecac6b6424604a5b459771a2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` 57fe3c71cafcefca1b2e419e3a008f1ebc0be38c ` 和原目标 ` 775e7c8661f23f1d9e84a1e585147444ed9eda74 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 5f878b97d3420b99c988e546bdadd3098bd51d89 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-57"></a>
### 57. N4 / ` fix(surface): child may remain below parent after XdgToplevel set_parent `

- 本仓内容路径：` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 实际改变：` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 5f878b97d3420b99c988e546bdadd3098bd51d89 ` → ` 5f878b97d3420b99c988e546bdadd3098bd51d89 `。
  原证据引用：` 6e8369a56b958114ecac6b6424604a5b459771a2 ` → ` 6e8369a56b958114ecac6b6424604a5b459771a2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` 00f6f3a6994a086a4b919f30558b14019fbb5c55 ` 和原目标 ` 646dfdda45fcfe3fe821fe91641b6daa1a67074b ` 查询。

<a id="entry-58"></a>
### 58. N4 / ` fix(output): prevent repeated repositioning of child windows across outputs `

- 本仓内容路径：` compositor/src/output/output.cpp `、` compositor/src/output/output.h `。
- 实际改变：` compositor/src/output/output.cpp `、` compositor/src/output/output.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 5f878b97d3420b99c988e546bdadd3098bd51d89 ` → ` 5f878b97d3420b99c988e546bdadd3098bd51d89 `。
  原证据引用：` 6e8369a56b958114ecac6b6424604a5b459771a2 ` → ` 6e8369a56b958114ecac6b6424604a5b459771a2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` 746076b98e77bd783de261822000505ca5a344ef ` 和原目标 ` c826d6129ea09a1f0bedbadfc91ac801659e7b19 ` 查询。

<a id="entry-59"></a>
### 59. N4 / ` fix(multitaskview): resolve transition, gesture and workspace switching issues `

- 本仓内容路径：` compositor/src/input/gestures.cpp `、` compositor/src/interfaces/multitaskviewinterface.h `、` compositor/src/modules/shortcut/shortcutrunner.cpp `、` compositor/src/plugins/multitaskview/multitaskview.cpp `、` compositor/src/plugins/multitaskview/multitaskview.h `、` compositor/src/plugins/multitaskview/multitaskviewplugin.cpp `、` compositor/src/plugins/multitaskview/multitaskviewplugin.h `、` compositor/src/plugins/multitaskview/qml/MultitaskviewProxy.qml `、` compositor/src/plugins/multitaskview/qml/WindowSelectionGrid.qml `。
- 实际改变：` compositor/src/input/gestures.cpp `、` compositor/src/interfaces/multitaskviewinterface.h `、` compositor/src/modules/shortcut/shortcutrunner.cpp `、` compositor/src/plugins/multitaskview/multitaskview.cpp `、` compositor/src/plugins/multitaskview/multitaskview.h `、` compositor/src/plugins/multitaskview/multitaskviewplugin.cpp `、` compositor/src/plugins/multitaskview/multitaskviewplugin.h `、` compositor/src/plugins/multitaskview/qml/MultitaskviewProxy.qml `、` compositor/src/plugins/multitaskview/qml/WindowSelectionGrid.qml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 5f878b97d3420b99c988e546bdadd3098bd51d89 ` → ` 5f878b97d3420b99c988e546bdadd3098bd51d89 `。
  原证据引用：` 6e8369a56b958114ecac6b6424604a5b459771a2 ` → ` 6e8369a56b958114ecac6b6424604a5b459771a2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` 3554ce7eceb09e0d14ee2253714b9257db728f42 ` 和原目标 ` fba4f624dc524109f7c4fc19933b27870970ac6a ` 查询。

<a id="entry-60"></a>
### 60. N4 / ` feat(glass): implement Liquid Glass effect with smooth corner deformation `

- 本仓内容路径：` compositor/docs/liquid-glass-dispersion.md `、` compositor/examples/test_glass/Main.qml `、` compositor/examples/test_glass/helper.h `、` compositor/examples/test_glass/main.cpp `、` compositor/misc/dconfig/org.deepin.dde.treeland.user.json `、` compositor/misc/shaders/liquidglass.frag `、` compositor/src/core/qml/Effects/Blur.qml `、` compositor/src/core/qml/Effects/GlassEffect.qml `、` compositor/src/plugins/lockscreen/qml/RoundBlur.qml `、` compositor/tests/test_effect_glass/GlassEffectScene.qml `、` compositor/tests/test_effect_glass/main.cpp `。
- 实际改变：` compositor/docs/liquid-glass-dispersion.md `、` compositor/examples/test_glass/Main.qml `、` compositor/examples/test_glass/helper.h `、` compositor/examples/test_glass/main.cpp `、` compositor/misc/dconfig/org.deepin.dde.treeland.user.json `、` compositor/misc/shaders/liquidglass.frag `、` compositor/src/core/qml/Effects/Blur.qml `、` compositor/src/core/qml/Effects/GlassEffect.qml `、` compositor/src/plugins/lockscreen/qml/RoundBlur.qml `、` compositor/tests/test_effect_glass/GlassEffectScene.qml `、` compositor/tests/test_effect_glass/main.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 5f878b97d3420b99c988e546bdadd3098bd51d89 ` → ` 5f878b97d3420b99c988e546bdadd3098bd51d89 `。
  原证据引用：` 6e8369a56b958114ecac6b6424604a5b459771a2 ` → ` 6e8369a56b958114ecac6b6424604a5b459771a2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` 9f9dfa6b6a2134e1882431c5ef1db4f7e71c1814 ` 和原目标 ` 5f807c898cfb9bd8a48a5888edf89f4280df7405 ` 查询。

<a id="entry-61"></a>
### 61. N4 / ` perf(glass): cut center-fill cost and tighten bezel path `

- 本仓内容路径：` compositor/examples/test_glass/CMakeLists.txt `、` compositor/misc/shaders/liquidglass.frag `、` compositor/src/CMakeLists.txt `、` compositor/tests/test_effect_glass/CMakeLists.txt `。
- 实际改变：` compositor/examples/test_glass/CMakeLists.txt `、` compositor/misc/shaders/liquidglass.frag `、` compositor/src/CMakeLists.txt `、` compositor/tests/test_effect_glass/CMakeLists.txt `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 5f878b97d3420b99c988e546bdadd3098bd51d89 ` → ` 5f878b97d3420b99c988e546bdadd3098bd51d89 `。
  原证据引用：` 6e8369a56b958114ecac6b6424604a5b459771a2 ` → ` 6e8369a56b958114ecac6b6424604a5b459771a2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` cd0879de06bd33744993e99cc395615bd986de9e ` 和原目标 ` d001bd70c4d9050f9a8e153fc607859b9550e9d8 ` 查询。
- 原审核说明：` 合入来源的 shader 优化并保留本地 target/QML 路径；将测试 SOURCE_DIR 精确映射到 compositor 根以读取真实 DConfig 描述，不改默认值断言、不复制配置、不新增兄弟路径。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/3a59c6f5d06d218e85a6b9820c40daf6b642a77f.md)。

<a id="entry-62"></a>
### 62. N4 / ` fix(animation): smooth minimize transitions `

- 本仓内容路径：` compositor/src/core/qml/Animations/MinimizeAnimation.qml `、` compositor/src/surface/surfacewrapper.cpp `。
- 实际改变：` compositor/src/core/qml/Animations/MinimizeAnimation.qml `、` compositor/src/surface/surfacewrapper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 5f878b97d3420b99c988e546bdadd3098bd51d89 ` → ` 5f878b97d3420b99c988e546bdadd3098bd51d89 `。
  原证据引用：` 6e8369a56b958114ecac6b6424604a5b459771a2 ` → ` 6e8369a56b958114ecac6b6424604a5b459771a2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` 4953e6dddf34acee1371b8b651e24c496a26253f ` 和原目标 ` 889316df02f80582008562ff3512ef4559ca37c7 ` 查询。

<a id="entry-63"></a>
### 63. N4 / ` fix(glass): pull refraction to lip and retune glass defaults `

- 本仓内容路径：` compositor/examples/test_glass/Main.qml `、` compositor/examples/test_glass/helper.h `、` compositor/misc/dconfig/org.deepin.dde.treeland.user.json `、` compositor/misc/shaders/liquidglass.frag `、` compositor/src/core/qml/Effects/Blur.qml `、` compositor/src/core/qml/Effects/GlassEffect.qml `、` compositor/tests/test_effect_glass/main.cpp `。
- 实际改变：` compositor/examples/test_glass/Main.qml `、` compositor/examples/test_glass/helper.h `、` compositor/misc/dconfig/org.deepin.dde.treeland.user.json `、` compositor/misc/shaders/liquidglass.frag `、` compositor/src/core/qml/Effects/Blur.qml `、` compositor/src/core/qml/Effects/GlassEffect.qml `、` compositor/tests/test_effect_glass/main.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 5f878b97d3420b99c988e546bdadd3098bd51d89 ` → ` 5f878b97d3420b99c988e546bdadd3098bd51d89 `。
  原证据引用：` 6e8369a56b958114ecac6b6424604a5b459771a2 ` → ` 6e8369a56b958114ecac6b6424604a5b459771a2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` 7743aa7a094671430b9f3c594fd71f2630429327 ` 和原目标 ` a94fc93bd3b072490e1fb5dcd01250b3abc5118c ` 查询。

<a id="entry-64"></a>
### 64. N4 / ` fix(output): avoid enabling output before restoring topology `

- 本仓内容路径：` compositor/src/seat/helper.cpp `。
- 实际改变：` compositor/src/seat/helper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 5f878b97d3420b99c988e546bdadd3098bd51d89 ` → ` 5f878b97d3420b99c988e546bdadd3098bd51d89 `。
  原证据引用：` 6e8369a56b958114ecac6b6424604a5b459771a2 ` → ` 6e8369a56b958114ecac6b6424604a5b459771a2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` 65a2822daa752e16ca5d62e2916b2032f8b4f650 ` 和原目标 ` 53b6a6e117afed7176d5156f0dc5ec9920f54258 ` 查询。

<a id="entry-65"></a>
### 65. N4 / ` Revert "fix(input): allow drag source to update cursor" `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/kernel/wseat.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 5f878b97d3420b99c988e546bdadd3098bd51d89 ` → ` fbef982ae1546244cf86fbbbae05963b601bff18 `。
  原证据引用：` 6e8369a56b958114ecac6b6424604a5b459771a2 ` → ` f366cc17407f02f1249d002088da4aea0cdfc06e `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` 63116956e9f77e691250b3326ac15a9dd4c6a47d ` 和原目标 ` 894741dd529dfca9c39fc0bdf532620beb2ec4b6 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` fbef982ae1546244cf86fbbbae05963b601bff18 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-66"></a>
### 66. N4 / ` fix(input): update cursor from DnD action `

- 本仓内容路径：` compositor/src/seat/helper.cpp `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/seat/helper.cpp `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_data_device.h `、` 3rdparty/wlroots/types/data_device/wlr_data_source.c `、` qwlroots/src/types/qwdatadevice.h `、` waylib/src/server/kernel/private/wcursor_p.h `、` waylib/src/server/kernel/wcursor.cpp `、` waylib/src/server/kernel/wcursor.h `、` waylib/src/server/kernel/wseat.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` fbef982ae1546244cf86fbbbae05963b601bff18 ` → ` 41bdc82765653b610ae06c25549d419124faf509 `。
  原证据引用：` f366cc17407f02f1249d002088da4aea0cdfc06e ` → ` 5b2456ea15df37dac357dc4eb8f12a14f109bad8 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` 3d1a458a7ee298ba190fd0b73b0418dd331d27bf ` 和原目标 ` f9d10829f29720ba2d0694c3d9188648fb28bd77 ` 查询。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 41bdc82765653b610ae06c25549d419124faf509 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-67"></a>
### 67. N4 / ` fix(gesture): fix workspace gesture issues and add lock screen guards `

- 本仓内容路径：` compositor/src/input/gestures.cpp `、` compositor/src/modules/shortcut/shortcutrunner.cpp `、` compositor/src/modules/shortcut/shortcutrunner.h `、` compositor/src/seat/helper.cpp `、` compositor/src/workspace/workspaceanimationcontroller.cpp `、` compositor/src/workspace/workspaceanimationcontroller.h `。
- 实际改变：` compositor/src/input/gestures.cpp `、` compositor/src/modules/shortcut/shortcutrunner.cpp `、` compositor/src/modules/shortcut/shortcutrunner.h `、` compositor/src/seat/helper.cpp `、` compositor/src/workspace/workspaceanimationcontroller.cpp `、` compositor/src/workspace/workspaceanimationcontroller.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 41bdc82765653b610ae06c25549d419124faf509 ` → ` 41bdc82765653b610ae06c25549d419124faf509 `。
  原证据引用：` 5b2456ea15df37dac357dc4eb8f12a14f109bad8 ` → ` 5b2456ea15df37dac357dc4eb8f12a14f109bad8 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` f46ee9929e3b22fe009e1c19f8c66ea9ad941371 ` 和原目标 ` d5c176303535b27f1b5c2cb91577d9514d264832 ` 查询。

<a id="entry-68"></a>
### 68. N4 / ` fix(seat): correct keyboard attach/detach and modifier forwarding `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/kernel/wseat.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 41bdc82765653b610ae06c25549d419124faf509 ` → ` 495e18db5c4dd3b96d9d2fadbd529073cc1d6329 `。
  原证据引用：` 5b2456ea15df37dac357dc4eb8f12a14f109bad8 ` → ` 154a53703f463f4882b39bc98bb8b5c574a861af `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` 371d32244323c914a6816fc7c14fec57c04fa333 ` 和原目标 ` 19d1aa51a50bb15177022ff33e7bf72cca04631f ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 495e18db5c4dd3b96d9d2fadbd529073cc1d6329 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-69"></a>
### 69. N4 / ` fix(seat): restore group keyboard when virtual keyboard is destroyed `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/kernel/wseat.cpp `、` waylib/src/server/protocols/winputmethodhelper.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 495e18db5c4dd3b96d9d2fadbd529073cc1d6329 ` → ` 7c8a47d9f4624e970504fd44780c36198785a5ca `。
  原证据引用：` 154a53703f463f4882b39bc98bb8b5c574a861af ` → ` 0d8c99c886084818a1caee37995390bb69603184 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` 07a7b175b71e5fb78a57e962db7b30d227e3936a ` 和原目标 ` 1aad388c0b107b6e16f19154fbf0e74bb9e3c0ad ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 7c8a47d9f4624e970504fd44780c36198785a5ca `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-70"></a>
### 70. N4 / ` chore: bump version to 0.8.17 `

- 本仓内容路径：` compositor/CMakeLists.txt `、` compositor/debian/changelog `。
- 实际改变：` compositor/CMakeLists.txt `、` compositor/debian/changelog `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 7c8a47d9f4624e970504fd44780c36198785a5ca ` → ` 7c8a47d9f4624e970504fd44780c36198785a5ca `。
  原证据引用：` 0d8c99c886084818a1caee37995390bb69603184 ` → ` 0d8c99c886084818a1caee37995390bb69603184 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/parent-evidence.json`；以来源 ` 24c1a0b547fc8a1c6617bdff147efcbad03c2f98 ` 和原目标 ` d1be07121ea0f20bf87a128208a703a0dbbf3b68 ` 查询。
- 原审核说明：` 按来源升级到 0.8.17 并完整保留 changelog，保留 DeckCompositor 标识和现有构建布局。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/c1525adbc980b2265dd95c480d955fb76de00011.md)。

<a id="entry-71"></a>
### 71. N5 / ` fix(output): restore configured topology after output reconnect `

- 本仓内容路径：` compositor/src/core/rootsurfacecontainer.cpp `、` compositor/src/seat/helper.cpp `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/core/rootsurfacecontainer.cpp `、` compositor/src/seat/helper.cpp `。
- 排除的来源路径：` waylib/src/server/protocols/woutputmanagerv1.cpp `、` waylib/src/server/protocols/woutputmanagerv1.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 7c8a47d9f4624e970504fd44780c36198785a5ca ` → ` c68ed41d8224c355a2335463a487017c55156d55 `。
  原证据引用：` 0d8c99c886084818a1caee37995390bb69603184 ` → ` 4f43ed9c7fe9b818f0565a7c44f4b49c2b871b75 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` ad91d436f0c7b8afd79153c766d6cccebc767370 ` 和原目标 ` 64f6f0811be796564b5ebe0cc22028aa8dfebacd ` 查询。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 同一 Treeland 来源的 C / waylib-shared 目标：` c68ed41d8224c355a2335463a487017c55156d55 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-72"></a>
### 72. N5 / `  fix(lockscreen): ignore geometry changes from removed outputs `

- 本仓内容路径：` compositor/src/core/lockscreen.cpp `。
- 实际改变：` compositor/src/core/lockscreen.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` c68ed41d8224c355a2335463a487017c55156d55 ` → ` c68ed41d8224c355a2335463a487017c55156d55 `。
  原证据引用：` 4f43ed9c7fe9b818f0565a7c44f4b49c2b871b75 ` → ` 4f43ed9c7fe9b818f0565a7c44f4b49c2b871b75 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` bad95a0501c65177093d29bfb6512e4f4a56b580 ` 和原目标 ` 5dea3074513768bff63f904acbc8de49d536e073 ` 查询。

<a id="entry-73"></a>
### 73. N5 / ` fix(lockscreen): add missing password error translation `

- 本仓内容路径：` compositor/src/plugins/lockscreen/translations/lockscreen.ca.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.en_US.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.es.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.fi.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.fr.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.gl_ES.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.ja.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.pl.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.pt_BR.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.ru.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.sq.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.tr.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.uk.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.zh_CN.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.zh_HK.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.zh_TW.ts `。
- 实际改变：` compositor/src/plugins/lockscreen/translations/lockscreen.ca.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.en_US.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.es.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.fi.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.fr.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.gl_ES.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.ja.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.pl.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.pt_BR.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.ru.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.sq.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.tr.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.uk.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.zh_CN.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.zh_HK.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.zh_TW.ts `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` c68ed41d8224c355a2335463a487017c55156d55 ` → ` c68ed41d8224c355a2335463a487017c55156d55 `。
  原证据引用：` 4f43ed9c7fe9b818f0565a7c44f4b49c2b871b75 ` → ` 4f43ed9c7fe9b818f0565a7c44f4b49c2b871b75 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 53918c4459982e245f7cff74d6a5038b9367f5f3 ` 和原目标 ` 2c274bc916def0d7e2218820c4615d851b9511c1 ` 查询。

<a id="entry-74"></a>
### 74. N5 / ` fix: correct vendored wlroots license annotations `

- 本仓内容路径：` compositor/LICENSES/LGPL-2.1-or-later.txt `、` compositor/REUSE.toml `。
- 实际改变：` compositor/LICENSES/LGPL-2.1-or-later.txt `、` compositor/REUSE.toml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` c68ed41d8224c355a2335463a487017c55156d55 ` → ` c68ed41d8224c355a2335463a487017c55156d55 `。
  原证据引用：` 4f43ed9c7fe9b818f0565a7c44f4b49c2b871b75 ` → ` 4f43ed9c7fe9b818f0565a7c44f4b49c2b871b75 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 275daf1769fc81d129c30e5625c8309c2a415f4c ` 和原目标 ` 665b9f827c5b566ede2dd776d0c65f4147b60ac3 ` 查询。

<a id="entry-75"></a>
### 75. N5 / ` fix(lockscreen): update leftPadding imperatively to fix binding loop `

- 本仓内容路径：` compositor/src/plugins/lockscreen/qml/UserInput.qml `。
- 实际改变：` compositor/src/plugins/lockscreen/qml/UserInput.qml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` c68ed41d8224c355a2335463a487017c55156d55 ` → ` c68ed41d8224c355a2335463a487017c55156d55 `。
  原证据引用：` 4f43ed9c7fe9b818f0565a7c44f4b49c2b871b75 ` → ` 4f43ed9c7fe9b818f0565a7c44f4b49c2b871b75 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 4e221941db9abb6244b274ec0341347282610677 ` 和原目标 ` 689c60464a1c6fbcde253be2fd2f2057c411f247 ` 查询。

<a id="entry-76"></a>
### 76. N5 / ` Updates for project TreeLand (#1233) `

- 本仓内容路径：` compositor/src/plugins/lockscreen/translations/lockscreen.ca.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.es.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.fi.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.fr.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.gl_ES.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.ja.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.pl.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.pt_BR.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.ru.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.sq.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.uk.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.zh_CN.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.zh_HK.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.zh_TW.ts `。
- 实际改变：` compositor/src/plugins/lockscreen/translations/lockscreen.ca.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.es.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.fi.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.fr.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.gl_ES.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.ja.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.pl.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.pt_BR.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.ru.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.sq.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.uk.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.zh_CN.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.zh_HK.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.zh_TW.ts `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` c68ed41d8224c355a2335463a487017c55156d55 ` → ` c68ed41d8224c355a2335463a487017c55156d55 `。
  原证据引用：` 4f43ed9c7fe9b818f0565a7c44f4b49c2b871b75 ` → ` 4f43ed9c7fe9b818f0565a7c44f4b49c2b871b75 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 944f8cdb0c3f11190fb5f21110b74715f1e35092 ` 和原目标 ` b8260da472d0d94e774774680e9e8668a5c7eb39 ` 查询。

<a id="entry-77"></a>
### 77. N5 / ` fix(output): remove disabled outputs from single-output layout `

- 本仓内容路径：` compositor/src/output/output.cpp `、` compositor/src/output/outputmanager.cpp `、` compositor/src/seat/helper.cpp `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/output/output.cpp `、` compositor/src/output/outputmanager.cpp `、` compositor/src/seat/helper.cpp `。
- 排除的来源路径：` waylib/src/server/protocols/woutputmanagerv1.cpp `、` waylib/src/server/protocols/woutputmanagerv1.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` c68ed41d8224c355a2335463a487017c55156d55 ` → ` 9874b79331a380ad66883575eaba4b25e20add14 `。
  原证据引用：` 4f43ed9c7fe9b818f0565a7c44f4b49c2b871b75 ` → ` 58f0bb706ed29f0cf6c16aeb89be1365d3846511 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 97ed8df0b546f925c17388b71fdd78181b2cb861 ` 和原目标 ` d491c00e9282336836b82b61094ba8b703b062b5 ` 查询。
- 原审核说明：` 按来源在成功提交启用/禁用后更新输出 layout，并保留 QPointer 输出生命周期保护；合并本地 pendingConfig 捕获命名及意外状态/协议销毁处理，成功与失败回调仍绑定同一个配置对象。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/267e44a4c9109d47fc4e0332c13345035eb55791.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 9874b79331a380ad66883575eaba4b25e20add14 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-78"></a>
### 78. N5 / ` fix(output): persist output settings while preserving saved position `

- 本仓内容路径：` compositor/src/output/output.h `、` compositor/src/seat/helper.cpp `。
- 实际改变：` compositor/src/output/output.h `、` compositor/src/seat/helper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 9874b79331a380ad66883575eaba4b25e20add14 ` → ` 9874b79331a380ad66883575eaba4b25e20add14 `。
  原证据引用：` 58f0bb706ed29f0cf6c16aeb89be1365d3846511 ` → ` 58f0bb706ed29f0cf6c16aeb89be1365d3846511 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` afbc3f99f27341540a7a01b4ea403bc8317dca67 ` 和原目标 ` 486114a11eb75ee1aff0b6f05092c77ec3d098fa ` 查询。

<a id="entry-79"></a>
### 79. N5 / ` fix(xsettings): store cursor size and DPI as integers `

- 本仓内容路径：` compositor/src/xsettings/settingmanager.cpp `。
- 实际改变：` compositor/src/xsettings/settingmanager.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 9874b79331a380ad66883575eaba4b25e20add14 ` → ` 9874b79331a380ad66883575eaba4b25e20add14 `。
  原证据引用：` 58f0bb706ed29f0cf6c16aeb89be1365d3846511 ` → ` 58f0bb706ed29f0cf6c16aeb89be1365d3846511 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` ac2b0abcca695f82b6ade4313f49c121f3e338ba ` 和原目标 ` ab60d002637d884c01480c9cfb0c3f0854090d24 ` 查询。

<a id="entry-80"></a>
### 80. N5 / ` refactor(surface): extract state-change helpers and add setSurfaceStateDirectly `

- 本仓内容路径：` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 实际改变：` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 9874b79331a380ad66883575eaba4b25e20add14 ` → ` 9874b79331a380ad66883575eaba4b25e20add14 `。
  原证据引用：` 58f0bb706ed29f0cf6c16aeb89be1365d3846511 ` → ` 58f0bb706ed29f0cf6c16aeb89be1365d3846511 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 90a0790f9bed00ec0c52e35ffa0b421237b7e04e ` 和原目标 ` 6f670f557b4541368f506c10cdb81d54bf6b9592 ` 查询。

<a id="entry-81"></a>
### 81. N5 / ` feat(tile): add QuickTile helpers and de-tile on move begin `

- 本仓内容路径：` compositor/src/CMakeLists.txt `、` compositor/src/surface/quicktile.cpp `、` compositor/src/surface/quicktile.h `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `。
- 实际改变：` compositor/src/CMakeLists.txt `、` compositor/src/surface/quicktile.cpp `、` compositor/src/surface/quicktile.h `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 9874b79331a380ad66883575eaba4b25e20add14 ` → ` 9874b79331a380ad66883575eaba4b25e20add14 `。
  原证据引用：` 58f0bb706ed29f0cf6c16aeb89be1365d3846511 ` → ` 58f0bb706ed29f0cf6c16aeb89be1365d3846511 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 9f54c436e86ee07836b2dc486a154f17563e67cb ` 和原目标 ` b717fefbf1e85c2bfb6a51e3e3abfc702ae8e3eb ` 查询。

<a id="entry-82"></a>
### 82. N5 / ` feat(tile): detect edge-tiling during move with preview overlay `

- 本仓内容路径：` compositor/misc/dconfig/org.deepin.dde.treeland.user.json `、` compositor/src/CMakeLists.txt `、` compositor/src/core/qml/EdgeTilePreview.qml `、` compositor/src/core/qmlengine.cpp `、` compositor/src/core/qmlengine.h `、` compositor/src/core/rootsurfacecontainer.cpp `、` compositor/src/core/rootsurfacecontainer.h `、` compositor/src/seat/helper.cpp `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `。
- 实际改变：` compositor/misc/dconfig/org.deepin.dde.treeland.user.json `、` compositor/src/CMakeLists.txt `、` compositor/src/core/qml/EdgeTilePreview.qml `、` compositor/src/core/qmlengine.cpp `、` compositor/src/core/qmlengine.h `、` compositor/src/core/rootsurfacecontainer.cpp `、` compositor/src/core/rootsurfacecontainer.h `、` compositor/src/seat/helper.cpp `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 9874b79331a380ad66883575eaba4b25e20add14 ` → ` 9874b79331a380ad66883575eaba4b25e20add14 `。
  原证据引用：` 58f0bb706ed29f0cf6c16aeb89be1365d3846511 ` → ` 58f0bb706ed29f0cf6c16aeb89be1365d3846511 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 0750fdaacee9ff641d1fed38096e5d4793391788 ` 和原目标 ` f664763c24959a9b062386cc1ce8441c72cb7dd4 ` 查询。
- 原审核说明：` 完整合入边缘平铺预览与配置行为；组件构造按既有 DeckShell.Compositor URI 映射，保留本地模块/target 与先前输出配置生命周期适配，不扩展规范路径。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/9392cc156e2797e1632257f7294680d8b5b8f478.md)。

<a id="entry-83"></a>
### 83. N5 / ` fix(tile): reposition window under cursor when de-tiling on move begin `

- 本仓内容路径：` compositor/src/core/rootsurfacecontainer.cpp `。
- 实际改变：` compositor/src/core/rootsurfacecontainer.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 9874b79331a380ad66883575eaba4b25e20add14 ` → ` 9874b79331a380ad66883575eaba4b25e20add14 `。
  原证据引用：` 58f0bb706ed29f0cf6c16aeb89be1365d3846511 ` → ` 58f0bb706ed29f0cf6c16aeb89be1365d3846511 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 4325c6a384d7612265880f005acef8f04bc28e76 ` 和原目标 ` 28e4c97b76eac3f398f1d7f17df5ee4f53c2d178 ` 查询。

<a id="entry-84"></a>
### 84. N5 / ` feat(shortcut): add TileLeft/TileRight shortcuts `

- 本仓内容路径：` compositor/src/modules/shortcut/shortcutcontroller.h `、` compositor/src/modules/shortcut/shortcutrunner.cpp `。
- 实际改变：` compositor/src/modules/shortcut/shortcutcontroller.h `、` compositor/src/modules/shortcut/shortcutrunner.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 9874b79331a380ad66883575eaba4b25e20add14 ` → ` 9874b79331a380ad66883575eaba4b25e20add14 `。
  原证据引用：` 58f0bb706ed29f0cf6c16aeb89be1365d3846511 ` → ` 58f0bb706ed29f0cf6c16aeb89be1365d3846511 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 9573a52366dc29e77213053b9902ee6237675344 ` 和原目标 ` dafd320441740c956f39073798adf1670f62175f ` 查询。

<a id="entry-85"></a>
### 85. N5 / ` feat: add containerOf utility for struct member offset calculation `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/CMakeLists.txt `、` waylib/src/server/utils/WContainerOf `、` waylib/src/server/utils/wcontainerof.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 9874b79331a380ad66883575eaba4b25e20add14 ` → ` 13fb708ed222f89b4a4776b3513fb3f4264b4aee `。
  原证据引用：` 58f0bb706ed29f0cf6c16aeb89be1365d3846511 ` → ` 85bf4347afe2aaf028e8053f3429205ac7a15a2a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` a9df8d3d87256c84a593838057e587a6beee4ec4 ` 和原目标 ` 7bfb0fbcdf84f9a35f350b6e62a04ef7ac15ad32 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 13fb708ed222f89b4a4776b3513fb3f4264b4aee `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-86"></a>
### 86. N5 / ` [skip CI] Translate lockscreen.en_US.ts in pl `

- 本仓内容路径：` compositor/src/plugins/lockscreen/translations/lockscreen.pl.ts `。
- 实际改变：` compositor/src/plugins/lockscreen/translations/lockscreen.pl.ts `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 13fb708ed222f89b4a4776b3513fb3f4264b4aee ` → ` 13fb708ed222f89b4a4776b3513fb3f4264b4aee `。
  原证据引用：` 85bf4347afe2aaf028e8053f3429205ac7a15a2a ` → ` 85bf4347afe2aaf028e8053f3429205ac7a15a2a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` d63ad285b642d4a7489a9914441fde559e3b1839 ` 和原目标 ` 1338e1a23f0e9ef0e67b1ec735839eae6e9fb2e3 ` 查询。

<a id="entry-87"></a>
### 87. N5 / ` fix(greeter): fall back to NSS when logged-in user missing from UserModel `

- 本仓内容路径：` compositor/src/greeter/greeterproxy.cpp `。
- 实际改变：` compositor/src/greeter/greeterproxy.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 13fb708ed222f89b4a4776b3513fb3f4264b4aee ` → ` 13fb708ed222f89b4a4776b3513fb3f4264b4aee `。
  原证据引用：` 85bf4347afe2aaf028e8053f3429205ac7a15a2a ` → ` 85bf4347afe2aaf028e8053f3429205ac7a15a2a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` a96f30f68645c48ebef7b8cac8299acbba2f4cba ` 和原目标 ` 63eaead33c02e6b00ba8b12da3bd698a76632eb7 ` 查询。

<a id="entry-88"></a>
### 88. N5 / ` fix(output): correct WOutputManagerV1::interfaceName return value `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/protocols/woutputmanagerv1.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 13fb708ed222f89b4a4776b3513fb3f4264b4aee ` → ` da7f26ec3960947fe4fc7d348b4f7cbba5fdb56b `。
  原证据引用：` 85bf4347afe2aaf028e8053f3429205ac7a15a2a ` → ` e31be11aedefe191b29d1106947f9d8f1ff96477 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 526308f00028711152378a181e29045342f78790 ` 和原目标 ` 86c68f5a971bcad870f68c495a36766c15df689d ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` da7f26ec3960947fe4fc7d348b4f7cbba5fdb56b `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-89"></a>
### 89. N5 / ` fix(waylib): fix Vulkan scanout RT via wlroots render_buffer `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/renderer.c `、` 3rdparty/wlroots/wlroots.syms `、` waylib/src/server/kernel/wglobal.h `、` waylib/src/server/qtquick/private/wbufferrenderer.cpp `、` waylib/src/server/qtquick/private/wbufferrenderer_p.h `、` waylib/src/server/qtquick/private/woutputviewport_p.h `、` waylib/src/server/qtquick/woutputhelper.cpp `、` waylib/src/server/qtquick/woutputhelper.h `、` waylib/src/server/qtquick/woutputlayer.cpp `、` waylib/src/server/qtquick/woutputlayer.h `、` waylib/src/server/qtquick/woutputrenderwindow.cpp `、` waylib/src/server/qtquick/woutputviewport.cpp `、` waylib/src/server/qtquick/woutputviewport.h `、` waylib/src/server/qtquick/wrenderhelper.cpp `、` waylib/src/server/qtquick/wrenderhelper.h `、` waylib/src/server/qtquick/wsgtextureprovider.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` da7f26ec3960947fe4fc7d348b4f7cbba5fdb56b ` → ` 8d64ef27ffd82c64501e79ca0ce5058594582ceb `。
  原证据引用：` e31be11aedefe191b29d1106947f9d8f1ff96477 ` → ` be08de9af5176fb71ee1a05c5b1ca140b26078fd `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` b4d7bff91684db691da410dc4c49a3a4936044fa ` 和原目标 ` a6c94355d4dca81057d35e1d3455b6bea6553413 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 8d64ef27ffd82c64501e79ca0ce5058594582ceb `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-90"></a>
### 90. N5 / ` fix(lockscreen): add Vulkan-specific Blur placeholder `

- 本仓内容路径：` compositor/src/CMakeLists.txt `、` compositor/src/core/qml/Effects/+vulkan/Blur.qml `、` compositor/src/core/qml/Effects/Blur.qml `、` compositor/src/core/qml/overridable/InWindowBlur.qml `、` compositor/src/core/qmlengine.cpp `、` compositor/src/core/qmlengine.h `、` compositor/src/main.cpp `、` compositor/src/plugins/lockscreen/qml/SessionList.qml `、` compositor/src/plugins/lockscreen/qml/UserList.qml `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/CMakeLists.txt `、` compositor/src/core/qml/Effects/+vulkan/Blur.qml `、` compositor/src/core/qml/Effects/Blur.qml `、` compositor/src/core/qml/overridable/InWindowBlur.qml `、` compositor/src/core/qmlengine.cpp `、` compositor/src/core/qmlengine.h `、` compositor/src/main.cpp `、` compositor/src/plugins/lockscreen/qml/SessionList.qml `、` compositor/src/plugins/lockscreen/qml/UserList.qml `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/renderer.c `、` waylib/src/server/qtquick/woutputrenderwindow.cpp `、` waylib/src/server/qtquick/wrenderhelper.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 8d64ef27ffd82c64501e79ca0ce5058594582ceb ` → ` 5d193f6dccab6ad38890d453710c38dc69f53c0b `。
  原证据引用：` be08de9af5176fb71ee1a05c5b1ca140b26078fd ` → ` ed4f019301c0d3dd8434d842152f343a69e988d5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 6ea349ac28b93b61ca3f9223ec021344141d6fce ` 和原目标 ` 7d2daba2014eabef671253fb361c372cedcfb4f0 ` 查询。
- 原审核说明：` 合入 Vulkan Blur 与 Dtk file selector；新 QML 使用既有 DeckShell.Compositor URI，资源归属 libdeckcompositor，保持 +treeland 资源别名与 treeland selector 配对，不改外部选择协议。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/5b04ac8e277ac6d7887bf2ffb0be358f554d4bcc.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 5d193f6dccab6ad38890d453710c38dc69f53c0b `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-91"></a>
### 91. N5 / ` fix(wallpaper): use build factory in Debug `

- 本仓内容路径：` compositor/CMakeLists.txt `、` compositor/src/wallpaper/wallpaperlauncher.cpp `、` compositor/src/wallpaper/wallpaperlauncher.h `。
- 实际改变：` compositor/CMakeLists.txt `、` compositor/src/wallpaper/wallpaperlauncher.cpp `、` compositor/src/wallpaper/wallpaperlauncher.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 5d193f6dccab6ad38890d453710c38dc69f53c0b ` → ` 5d193f6dccab6ad38890d453710c38dc69f53c0b `。
  原证据引用：` ed4f019301c0d3dd8434d842152f343a69e988d5 ` → ` ed4f019301c0d3dd8434d842152f343a69e988d5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 252d0df3366671533b1914b55053a5ac4cbe6a3a ` 和原目标 ` 0b78f4b4bc17080372dd230c180abd9b5643ddec ` 查询。
- 原审核说明：` 保留来源 Debug 构建树壁纸工厂选择与 Release 已安装程序选择；构建输出按嵌套 compositor 的 PROJECT_BINARY_DIR 映射，保持现有 treeland-wallpaper-factory 可执行名称。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/bde8fd486752be3c8dc0d6d7ffd5a0f8e3aceaf8.md)。

<a id="entry-92"></a>
### 92. N5 / ` chore: Sync by https://github.com/linuxdeepin/.github/commit/cba9eafcc7c0d9b6b0d393d6e84ce38d4d541e1b `

- 本仓内容路径：` .github/workflows/cppcheck.yml `。
- 实际改变：` .github/workflows/cppcheck.yml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 5d193f6dccab6ad38890d453710c38dc69f53c0b ` → ` 5d193f6dccab6ad38890d453710c38dc69f53c0b `。
  原证据引用：` ed4f019301c0d3dd8434d842152f343a69e988d5 ` → ` ed4f019301c0d3dd8434d842152f343a69e988d5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 7d56f56671dc411e631b95b4b5546bbdee0f0d1f ` 和原目标 ` 4e1b025de4bccbcc102dae76767d99b58af6890e ` 查询。
- 原审核说明：` 仅加入来源的 fork repository 定位，继续 checkout 固定 PR head SHA 并关闭凭据持久化；拒绝可漂移 head.ref 分支定位，事件/action/权限及既有 checkout 标志不扩大，本次不执行 CI。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/7034642af76e4db8f8f6dcdb45e031c2ccc13005.md)。

<a id="entry-93"></a>
### 93. N5 / ` fix(multitaskview): skip hover-driven focus during animation and exit `

- 本仓内容路径：` compositor/src/plugins/multitaskview/qml/WindowSelectionGrid.qml `。
- 实际改变：` compositor/src/plugins/multitaskview/qml/WindowSelectionGrid.qml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 5d193f6dccab6ad38890d453710c38dc69f53c0b ` → ` 5d193f6dccab6ad38890d453710c38dc69f53c0b `。
  原证据引用：` ed4f019301c0d3dd8434d842152f343a69e988d5 ` → ` ed4f019301c0d3dd8434d842152f343a69e988d5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` a7679c9a4645f10555ed76d30845efa80ae3fbeb ` 和原目标 ` a4fde1a3fa68245d70814a2e61d519840b20087c ` 查询。

<a id="entry-94"></a>
### 94. N5 / ` fix(qml): drop redundant D. prefix for dtk-provided Qt controls `

- 本仓内容路径：` compositor/src/core/qml/WindowMenu.qml `、` compositor/src/plugins/lockscreen/qml/ControlAction.qml `、` compositor/src/plugins/lockscreen/qml/HintLabel.qml `、` compositor/src/plugins/lockscreen/qml/ShutdownButton.qml `、` compositor/src/plugins/lockscreen/qml/UserInput.qml `、` compositor/src/plugins/lockscreen/qml/UserList.qml `、` compositor/src/plugins/multitaskview/qml/WindowSelectionGrid.qml `、` compositor/src/plugins/multitaskview/qml/WorkspaceSelectionList.qml `。
- 实际改变：` compositor/src/core/qml/WindowMenu.qml `、` compositor/src/plugins/lockscreen/qml/ControlAction.qml `、` compositor/src/plugins/lockscreen/qml/HintLabel.qml `、` compositor/src/plugins/lockscreen/qml/ShutdownButton.qml `、` compositor/src/plugins/lockscreen/qml/UserInput.qml `、` compositor/src/plugins/lockscreen/qml/UserList.qml `、` compositor/src/plugins/multitaskview/qml/WindowSelectionGrid.qml `、` compositor/src/plugins/multitaskview/qml/WorkspaceSelectionList.qml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 5d193f6dccab6ad38890d453710c38dc69f53c0b ` → ` 5d193f6dccab6ad38890d453710c38dc69f53c0b `。
  原证据引用：` ed4f019301c0d3dd8434d842152f343a69e988d5 ` → ` ed4f019301c0d3dd8434d842152f343a69e988d5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` b8f04600d0106636501e569f7785f80d0568565f ` 和原目标 ` 4145ac43114354607bf4bdf09d65d508156eadee ` 查询。
- 原审核说明：` 采用来源的 QtQuick.Controls 类型及 Chameleon 样式解析，移除冗余 D. 控件前缀；WindowMenu 的两个项目模块继续使用既有 DeckShell.Compositor 和 WaylibShared.QuickSharedServer URI，保留本地 surface 可操作性保护。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/38761145d78fb4ad44609a310bbf8c7fbc4ad92f.md)。

<a id="entry-95"></a>
### 95. N5 / ` refactor(output): centralize output ID generation `

- 本仓内容路径：` compositor/src/core/rootsurfacecontainer.cpp `、` compositor/src/output/output.cpp `、` compositor/src/output/output.h `、` compositor/src/output/outputmanager.cpp `、` compositor/src/output/outputmanager.h `、` compositor/src/seat/helper.cpp `、` compositor/src/wallpaper/wallpapermanager.cpp `、` compositor/src/wallpaper/wallpapermanager.h `。
- 实际改变：` compositor/src/core/rootsurfacecontainer.cpp `、` compositor/src/output/output.cpp `、` compositor/src/output/output.h `、` compositor/src/output/outputmanager.cpp `、` compositor/src/output/outputmanager.h `、` compositor/src/seat/helper.cpp `、` compositor/src/wallpaper/wallpapermanager.cpp `、` compositor/src/wallpaper/wallpapermanager.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 5d193f6dccab6ad38890d453710c38dc69f53c0b ` → ` 5d193f6dccab6ad38890d453710c38dc69f53c0b `。
  原证据引用：` ed4f019301c0d3dd8434d842152f343a69e988d5 ` → ` ed4f019301c0d3dd8434d842152f343a69e988d5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 9886fca6d0eef13612b4046935b9bbe6f7df9fb1 ` 和原目标 ` f87bf9134910b33ded5b315dc0c59931cb35684e ` 查询。
- 原审核说明：` 在规范路径三方合并本次来源，保留已审核的 DeckShell/WaylibShared 名称及本地集成差异；所有新增行为仍来自该来源，不扩展兄弟文件。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/3d592cb35f0f71f4d07dca88133deb5576be639f.md)。

<a id="entry-96"></a>
### 96. N5 / ` feat: add build-tree wallpaper factory option `

- 本仓内容路径：` compositor/CMakeLists.txt `、` compositor/src/CMakeLists.txt `、` compositor/src/wallpaper/wallpaperlauncher.cpp `。
- 实际改变：` compositor/CMakeLists.txt `、` compositor/src/CMakeLists.txt `、` compositor/src/wallpaper/wallpaperlauncher.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 5d193f6dccab6ad38890d453710c38dc69f53c0b ` → ` 5d193f6dccab6ad38890d453710c38dc69f53c0b `。
  原证据引用：` ed4f019301c0d3dd8434d842152f343a69e988d5 ` → ` ed4f019301c0d3dd8434d842152f343a69e988d5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 36cb2c941da52b65bd2d5f879197657d73b39bad ` 和原目标 ` 7b50a09e1f1a84ffd8b5e8911a34b5253909f5d2 ` 查询。
- 原审核说明：` 完整采用默认关闭的构建树壁纸工厂选项，移除全局定义并作用于既有 libdeckcompositor；路径保持 compositor PROJECT_BINARY_DIR，保留本地 DDM 默认值、ext-session-lock 与插件/调试选项，不引入第二套路径。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/9177b1b00b85cd2bb766c12ceb347537230db115.md)。

<a id="entry-97"></a>
### 97. N5 / ` fix(xsettings): format XResources with tab separators `

- 本仓内容路径：` compositor/src/xsettings/xresource.cpp `。
- 实际改变：` compositor/src/xsettings/xresource.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 5d193f6dccab6ad38890d453710c38dc69f53c0b ` → ` 5d193f6dccab6ad38890d453710c38dc69f53c0b `。
  原证据引用：` ed4f019301c0d3dd8434d842152f343a69e988d5 ` → ` ed4f019301c0d3dd8434d842152f343a69e988d5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` da6c88f5239831ac5641c3f2bd1a84f5eab05c32 ` 和原目标 ` e2ca4614c1f41d828e7dd6500bcf42ba9d8245ff ` 查询。

<a id="entry-98"></a>
### 98. N5 / ` Updates for project TreeLand (#1260) `

- 本仓内容路径：` compositor/src/plugins/lockscreen/translations/lockscreen.fi.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.pt.ts `、` compositor/src/plugins/multitaskview/translations/multitaskview.pt.ts `、` compositor/translations/treeland.pt.ts `。
- 实际改变：` compositor/src/plugins/lockscreen/translations/lockscreen.fi.ts `、` compositor/src/plugins/lockscreen/translations/lockscreen.pt.ts `、` compositor/src/plugins/multitaskview/translations/multitaskview.pt.ts `、` compositor/translations/treeland.pt.ts `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 5d193f6dccab6ad38890d453710c38dc69f53c0b ` → ` 5d193f6dccab6ad38890d453710c38dc69f53c0b `。
  原证据引用：` ed4f019301c0d3dd8434d842152f343a69e988d5 ` → ` ed4f019301c0d3dd8434d842152f343a69e988d5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 6e980c1bf5e451b4ccc62d68256cc41247156b02 ` 和原目标 ` 711d5d88ba050e198125dfced7f2e765e02137d1 ` 查询。

<a id="entry-99"></a>
### 99. N5 / ` fix: avoid UB casting HoverMove to QMouseEvent `

- 本仓内容路径：` compositor/examples/test_pinch_handler/eventitem.cpp `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/examples/test_pinch_handler/eventitem.cpp `。
- 排除的来源路径：` waylib/src/server/kernel/wseat.cpp `、` waylib/src/server/qtquick/wsurfaceitem.cpp `、` waylib/tests/manual/pinchhandler/eventitem.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 5d193f6dccab6ad38890d453710c38dc69f53c0b ` → ` dcb885cf3b9823bffa91ff9535601041263bb252 `。
  原证据引用：` ed4f019301c0d3dd8434d842152f343a69e988d5 ` → ` e69ca1635752605a109dda3d05c61b93c9e05026 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 4d4736f4dfa73b04192245446ac1bde05eb83563 ` 和原目标 ` 16db9a1f75c16d8ecbf9e2a9d5c0b25f1ee83b93 ` 查询。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 同一 Treeland 来源的 C / waylib-shared 目标：` dcb885cf3b9823bffa91ff9535601041263bb252 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-100"></a>
### 100. N5 / ` fix: remove WBackend::activateSession/deactivateSession hack `

- 本仓内容路径：` compositor/src/modules/ddm/ddminterfacev1.cpp `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/modules/ddm/ddminterfacev1.cpp `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `。
- 排除的来源路径：` waylib/src/server/kernel/wbackend.cpp `、` waylib/src/server/kernel/wbackend.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` dcb885cf3b9823bffa91ff9535601041263bb252 ` → ` 93e9eef541115c83126b256489ab618d465c057f `。
  原证据引用：` e69ca1635752605a109dda3d05c61b93c9e05026 ` → ` 54a49ec203485a02f6531b58020cabce631b0e14 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 0333a31456c7f90708c7f482939e23d939283b45 ` 和原目标 ` 66f83af19a18b1d78d9860e5c6d675fb11e5c110 ` 查询。
- 原审核说明：` 在规范路径三方合并本次来源，保留已审核的 DeckShell/WaylibShared 名称及本地集成差异；所有新增行为仍来自该来源，不扩展兄弟文件。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/a35e2d49279ba82d0892b73a9017feac71f64826.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 93e9eef541115c83126b256489ab618d465c057f `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-101"></a>
### 101. N5 / ` feat: remove qwlroots dependency, use wlroots C API directly `

- 本仓内容路径：` .github/workflows/qwlroots-archlinux-build.yml `、` .github/workflows/qwlroots-debian-build.yml `、` .github/workflows/qwlroots-deepin-build.yml `、` .github/workflows/treeland-archlinux-build.yml `、` .github/workflows/waylib-archlinux-build.yml `、` .github/workflows/waylib-debian-build.yml `、` .github/workflows/waylib-deepin-build.yml `、` .gitignore `、` compositor/CMakeLists.txt `、` compositor/README.md `、` compositor/README.zh_CN.md `、` compositor/debian/control `、` compositor/debian/treeland-dev.install `、` compositor/default.nix `、` compositor/examples/test_glass/CMakeLists.txt `、` compositor/examples/test_glass/helper.cpp `、` compositor/examples/test_glass/helper.h `、` compositor/examples/test_glass/main.cpp `、` compositor/examples/test_window_bg/main.cpp `、` compositor/flake.nix `、` compositor/nix/default.nix `、` compositor/src/core/imcandidatepanelmanager.cpp `、` compositor/src/core/lockscreen.cpp `、` compositor/src/core/qmlengine.cpp `、` compositor/src/core/qmlengine.h `、` compositor/src/core/rootsurfacecontainer.cpp `、` compositor/src/core/rootsurfacecontainer.h `、` compositor/src/core/shellhandler.cpp `、` compositor/src/core/shellhandler.h `、` compositor/src/input/inputdevice.cpp `、` compositor/src/input/inputmanager.cpp `、` compositor/src/input/inputmanager.h `、` compositor/src/main.cpp `、` compositor/src/modules/CMakeLists.txt `、` compositor/src/modules/activation/activationmanagerinterfacev1.cpp `、` compositor/src/modules/app-id-resolver/appidresolver.cpp `、` compositor/src/modules/capture/capture.cpp `、` compositor/src/modules/capture/capture.h `、` compositor/src/modules/capture/impl/capturev1impl.cpp `、` compositor/src/modules/capture/impl/capturev1impl.h `、` compositor/src/modules/dde-shell/ddeshellmanagerinterfacev1.cpp `、` compositor/src/modules/dde-shell/ddeshellmanagerinterfacev1.h `、` compositor/src/modules/ddm/ddminterfacev1.cpp `、` compositor/src/modules/ddm/ddminterfacev1.h `、` compositor/src/modules/foreign-toplevel/dockpreviewcontextv1.h `、` compositor/src/modules/foreign-toplevel/foreigntoplevelhandlev1.h `、` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv1.cpp `、` compositor/src/modules/input-manager/inputmanagerinterfacev1.cpp `、` compositor/src/modules/input-manager/inputmanagerinterfacev1.h `、` compositor/src/modules/keyboard-state-notify/keyboardstatenotifymanagerinterfacev1.cpp `、` compositor/src/modules/output-manager/outputmanagement.cpp `、` compositor/src/modules/output-manager/outputmanagement.h `、` compositor/src/modules/personalization/personalizationmanagerinterfacev1.cpp `、` compositor/src/modules/personalization/personalizationmanagerinterfacev1.h `、` compositor/src/modules/prelaunch-splash/prelaunchsplash.cpp `、` compositor/src/modules/prelaunch-splash/prelaunchsplash.h `、` compositor/src/modules/screensaver/screensaverinterfacev1.cpp `、` compositor/src/modules/shortcut/shortcutmanager.cpp `、` compositor/src/modules/virtual-output/virtualoutputmanagerinterfacev1.cpp `、` compositor/src/modules/virtual-output/virtualoutputmanagerinterfacev1.h `、` compositor/src/modules/wallpaper-color/wallpapercolorinterfacev1.cpp `、` compositor/src/modules/wallpaper/wallpapermanagerinterfacev1.cpp `、` compositor/src/modules/wallpaper/wallpapermanagerinterfacev1.h `、` compositor/src/modules/wallpaper/wallpapernotifierinterfacev1.cpp `、` compositor/src/modules/wallpaper/wallpapernotifierinterfacev1.h `、` compositor/src/modules/wallpaper/wallpapershellinterfacev1.cpp `、` compositor/src/modules/wallpaper/wallpapershellinterfacev1.h `、` compositor/src/modules/window-management/windowmanagementinterfacev1.cpp `、` compositor/src/modules/wine-window-management/winewindowmanagement.cpp `、` compositor/src/modules/wine-window-state/winewindowstate.cpp `、` compositor/src/output/backlight.cpp `、` compositor/src/output/output.cpp `、` compositor/src/output/outputmanager.cpp `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/src/seat/seatsmanager.cpp `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `、` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `、` compositor/src/utils/fpsdisplaymanager.cpp `、` compositor/src/utils/fpsdisplaymanager.h `、` compositor/src/wallpaper/wallpaperitem.cpp `、` compositor/src/wallpaper/wallpapermanager.cpp `、` compositor/src/wallpaper/wallpapersurface.cpp `、` compositor/src/wallpaper/wallpapersurface.h `、` compositor/src/wallpaper/wallpaperswitcheritem.cpp `、` compositor/tests/test_effect_glass/CMakeLists.txt `、` compositor/tests/test_effect_glass/TestHelper.cpp `、` compositor/tests/test_effect_glass/TestHelper.h `、` compositor/tests/test_effect_glass/main.cpp `。
- 实际改变：` .github/workflows/qwlroots-archlinux-build.yml `、` .github/workflows/qwlroots-debian-build.yml `、` .github/workflows/qwlroots-deepin-build.yml `、` .github/workflows/treeland-archlinux-build.yml `、` .github/workflows/waylib-archlinux-build.yml `、` .github/workflows/waylib-debian-build.yml `、` .github/workflows/waylib-deepin-build.yml `、` .gitignore `、` 3rdparty/waylib-shared `、` compositor/CMakeLists.txt `、` compositor/README.md `、` compositor/README.zh_CN.md `、` compositor/debian/control `、` compositor/debian/treeland-dev.install `、` compositor/default.nix `、` compositor/examples/test_glass/helper.cpp `、` compositor/examples/test_glass/helper.h `、` compositor/examples/test_glass/main.cpp `、` compositor/examples/test_window_bg/main.cpp `、` compositor/flake.nix `、` compositor/nix/default.nix `、` compositor/src/CMakeLists.txt `、` compositor/src/core/imcandidatepanelmanager.cpp `、` compositor/src/core/lockscreen.cpp `、` compositor/src/core/qmlengine.cpp `、` compositor/src/core/qmlengine.h `、` compositor/src/core/rootsurfacecontainer.cpp `、` compositor/src/core/rootsurfacecontainer.h `、` compositor/src/core/shellhandler.cpp `、` compositor/src/core/shellhandler.h `、` compositor/src/input/inputdevice.cpp `、` compositor/src/input/inputmanager.cpp `、` compositor/src/input/inputmanager.h `、` compositor/src/main.cpp `、` compositor/src/modules/CMakeLists.txt `、` compositor/src/modules/activation/activationmanagerinterfacev1.cpp `、` compositor/src/modules/app-id-resolver/appidresolver.cpp `、` compositor/src/modules/capture/capture.cpp `、` compositor/src/modules/capture/capture.h `、` compositor/src/modules/capture/impl/capturev1impl.cpp `、` compositor/src/modules/capture/impl/capturev1impl.h `、` compositor/src/modules/dde-shell/ddeshellmanagerinterfacev1.cpp `、` compositor/src/modules/dde-shell/ddeshellmanagerinterfacev1.h `、` compositor/src/modules/ddm/ddminterfacev1.cpp `、` compositor/src/modules/ddm/ddminterfacev1.h `、` compositor/src/modules/foreign-toplevel/dockpreviewcontextv1.h `、` compositor/src/modules/foreign-toplevel/foreigntoplevelhandlev1.h `、` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv1.cpp `、` compositor/src/modules/input-manager/inputmanagerinterfacev1.cpp `、` compositor/src/modules/input-manager/inputmanagerinterfacev1.h `、` compositor/src/modules/keyboard-state-notify/keyboardstatenotifymanagerinterfacev1.cpp `、` compositor/src/modules/output-manager/outputmanagement.cpp `、` compositor/src/modules/output-manager/outputmanagement.h `、` compositor/src/modules/personalization/personalizationmanagerinterfacev1.cpp `、` compositor/src/modules/personalization/personalizationmanagerinterfacev1.h `、` compositor/src/modules/prelaunch-splash/prelaunchsplash.cpp `、` compositor/src/modules/prelaunch-splash/prelaunchsplash.h `、` compositor/src/modules/screensaver/screensaverinterfacev1.cpp `、` compositor/src/modules/shortcut/shortcutmanager.cpp `、` compositor/src/modules/virtual-output/virtualoutputmanagerinterfacev1.cpp `、` compositor/src/modules/virtual-output/virtualoutputmanagerinterfacev1.h `、` compositor/src/modules/wallpaper-color/wallpapercolorinterfacev1.cpp `、` compositor/src/modules/wallpaper/wallpapermanagerinterfacev1.cpp `、` compositor/src/modules/wallpaper/wallpapermanagerinterfacev1.h `、` compositor/src/modules/wallpaper/wallpapernotifierinterfacev1.cpp `、` compositor/src/modules/wallpaper/wallpapernotifierinterfacev1.h `、` compositor/src/modules/wallpaper/wallpapershellinterfacev1.cpp `、` compositor/src/modules/wallpaper/wallpapershellinterfacev1.h `、` compositor/src/modules/window-management/windowmanagementinterfacev1.cpp `、` compositor/src/modules/wine-window-management/winewindowmanagement.cpp `、` compositor/src/modules/wine-window-state/winewindowstate.cpp `、` compositor/src/output/backlight.cpp `、` compositor/src/output/output.cpp `、` compositor/src/output/outputmanager.cpp `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/src/seat/seatsmanager.cpp `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `、` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `、` compositor/src/utils/fpsdisplaymanager.cpp `、` compositor/src/utils/fpsdisplaymanager.h `、` compositor/src/wallpaper/wallpaperitem.cpp `、` compositor/src/wallpaper/wallpapermanager.cpp `、` compositor/src/wallpaper/wallpapersurface.cpp `、` compositor/src/wallpaper/wallpapersurface.h `、` compositor/src/wallpaper/wallpaperswitcheritem.cpp `、` compositor/tests/test_effect_glass/TestHelper.cpp `、` compositor/tests/test_effect_glass/TestHelper.h `、` compositor/tests/test_effect_glass/main.cpp `、` compositor/tests/test_late_dde_listener/main.cpp `、` compositor/tests/test_manager_resource_lifecycle/main.cpp `、` compositor/tests/test_multi_seat/CMakeLists.txt `、` compositor/tests/test_multi_seat/main.cpp `、` compositor/tests/test_multi_seat/surfaceclient.cpp `、` compositor/tests/test_multi_seat/surfaceclient.h `、` compositor/tests/test_protocol_foreign-toplevel/main.cpp `、` compositor/tests/test_scroll_factor/CMakeLists.txt `、` compositor/tests/test_scroll_factor/main.cpp `。
- 排除的来源路径：` 3rdparty/wlroots/types/buffer/buffer.c `、` qwlroots/.clang-format `、` qwlroots/.cursorindexingignore `、` qwlroots/.envrc `、` qwlroots/.github/workflows/archlinux-build.yaml `、` qwlroots/.github/workflows/reuse-check.yml `、` qwlroots/.gitignore `、` qwlroots/.gitmodules `、` qwlroots/.obs/deepin_workflows.yml `、` qwlroots/.obs/workflows.yml `、` qwlroots/.reuse/dep5 `、` qwlroots/CMakeLists.txt `、` qwlroots/CMakePresets.json `、` qwlroots/LICENSES/Apache-2.0.txt `、` qwlroots/LICENSES/CC-BY-4.0.txt `、` qwlroots/LICENSES/CC0-1.0.txt `、` qwlroots/LICENSES/GPL-2.0-only.txt `、` qwlroots/LICENSES/GPL-3.0-only.txt `、` qwlroots/LICENSES/LGPL-3.0-only.txt `、` qwlroots/README.md `、` qwlroots/README.zh_CN.md `、` qwlroots/analyze_coverage.py `、` qwlroots/cmake/Helpers.cmake `、` qwlroots/cmake/PackageVersionHelper.cmake `、` qwlroots/debian/changelog `、` qwlroots/debian/control `、` qwlroots/debian/copyright `、` qwlroots/debian/rules `、` qwlroots/debian/source/format `、` qwlroots/debian/watch `、` qwlroots/default.nix `、` qwlroots/doc/ai/qwcolormanagementv1-usage-guide.md `、` qwlroots/doc/ai/qwlroots-wrapping-patterns-best-practices-en.md `、` qwlroots/doc/ai/qwlroots-wrapping-patterns-best-practices.md `、` qwlroots/examples/CMakeLists.txt `、` qwlroots/examples/tinywl/CMakeLists.txt `、` qwlroots/examples/tinywl/main.cpp `、` qwlroots/flake.lock `、` qwlroots/flake.nix `、` qwlroots/garnix.yaml `、` qwlroots/nix/default.nix `、` qwlroots/src/CMakeLists.txt `、` qwlroots/src/cmake/CMakeConfig.cmake.in `、` qwlroots/src/cmake/pkgconfig.pc.in `、` qwlroots/src/interfaces/qwbackendinterface.h `、` qwlroots/src/interfaces/qwbufferinterface.h `、` qwlroots/src/interfaces/qwextimagecapturesourcev1interface.h `、` qwlroots/src/interfaces/qwinterface.h `、` qwlroots/src/interfaces/qwkeyboardinterface.h `、` qwlroots/src/interfaces/qwoutputinterface.h `、` qwlroots/src/interfaces/qwpointerinterface.h `、` qwlroots/src/interfaces/qwrendererinterface.h `、` qwlroots/src/interfaces/qwswitchinterface.h `、` qwlroots/src/interfaces/qwtabletpadinterface.h `、` qwlroots/src/qwbackend.cpp `、` qwlroots/src/qwbackend.h `、` qwlroots/src/qwdisplay.h `、` qwlroots/src/qwglobal.h `、` qwlroots/src/qwobject.cpp `、` qwlroots/src/qwobject.h `、` qwlroots/src/qwsession.h `、` qwlroots/src/render/qwallocator.h `、` qwlroots/src/render/qwcolor.h `、` qwlroots/src/render/qwdmabuf.h `、` qwlroots/src/render/qwdrmformatset.h `、` qwlroots/src/render/qwdrmsyncobj.h `、` qwlroots/src/render/qwegl.h `、` qwlroots/src/render/qwrenderer.h `、` qwlroots/src/render/qwswapchain.h `、` qwlroots/src/render/qwtexture.h `、` qwlroots/src/types/qwalphamodifierv1.h `、` qwlroots/src/types/qwbuffer.h `、` qwlroots/src/types/qwcolormanagerv1.h `、` qwlroots/src/types/qwcompositor.h `、` qwlroots/src/types/qwcontenttypev1.h `、` qwlroots/src/types/qwcursor.h `、` qwlroots/src/types/qwcursorshapev1.h `、` qwlroots/src/types/qwdamagering.h `、` qwlroots/src/types/qwdatacontrolv1.h `、` qwlroots/src/types/qwdatadevice.h `、` qwlroots/src/types/qwdrm.h `、` qwlroots/src/types/qwdrmleasev1.h `、` qwlroots/src/types/qwexportdmabufv1.h `、` qwlroots/src/types/qwextdatacontrolv1.h `、` qwlroots/src/types/qwextforeigntoplevellistv1.h `、` qwlroots/src/types/qwextimagecapturesourcev1.h `、` qwlroots/src/types/qwextimagecopycapturev1.h `、` qwlroots/src/types/qwforeigntoplevelhandlev1.h `、` qwlroots/src/types/qwfractionalscalemanagerv1.h `、` qwlroots/src/types/qwfullscreenshellv1.h `、` qwlroots/src/types/qwgammacontorlv1.h `、` qwlroots/src/types/qwidleinhibitv1.h `、` qwlroots/src/types/qwidlenotifyv1.h `、` qwlroots/src/types/qwinputdevice.cpp `、` qwlroots/src/types/qwinputdevice.h `、` qwlroots/src/types/qwinputmethodv2.h `、` qwlroots/src/types/qwkeyboard.h `、` qwlroots/src/types/qwkeyboardgroup.h `、` qwlroots/src/types/qwkeyboardshortcutsinhibitv1.h `、` qwlroots/src/types/qwlayershellv1.h `、` qwlroots/src/types/qwlinuxdmabufv1.h `、` qwlroots/src/types/qwlinuxdrmsyncobjv1.h `、` qwlroots/src/types/qwoutput.h `、` qwlroots/src/types/qwoutputlayer.h `、` qwlroots/src/types/qwoutputlayout.h `、` qwlroots/src/types/qwoutputmanagementv1.h `、` qwlroots/src/types/qwoutputpowermanagementv1.h `、` qwlroots/src/types/qwpointer.h `、` qwlroots/src/types/qwpointerconstraintsv1.h `、` qwlroots/src/types/qwpointergesturesv1.h `、` qwlroots/src/types/qwpresentation.h `、` qwlroots/src/types/qwprimaryselection.h `、` qwlroots/src/types/qwprimaryselectionv1.h `、` qwlroots/src/types/qwrelativepointerv1.h `、` qwlroots/src/types/qwscene.h `、` qwlroots/src/types/qwscreencopyv1.h `、` qwlroots/src/types/qwseat.h `、` qwlroots/src/types/qwsecuritycontextmanagerv1.h `、` qwlroots/src/types/qwsessionlockv1.h `、` qwlroots/src/types/qwshm.h `、` qwlroots/src/types/qwsinglepixelbufferv1.h `、` qwlroots/src/types/qwsubcompositor.h `、` qwlroots/src/types/qwswitch.h `、` qwlroots/src/types/qwtablet.h `、` qwlroots/src/types/qwtabletpad.h `、` qwlroots/src/types/qwtabletv2.h `、` qwlroots/src/types/qwtearingcontrolv1.h `、` qwlroots/src/types/qwtextinputv3.h `、` qwlroots/src/types/qwtouch.h `、` qwlroots/src/types/qwtransientseatv1.h `、` qwlroots/src/types/qwviewporter.h `、` qwlroots/src/types/qwvirtualkeyboardv1.h `、` qwlroots/src/types/qwvirtualpointerv1.h `、` qwlroots/src/types/qwxcursormanager.h `、` qwlroots/src/types/qwxdgactivationv1.h `、` qwlroots/src/types/qwxdgdecorationmanagerv1.h `、` qwlroots/src/types/qwxdgdialogv1.h `、` qwlroots/src/types/qwxdgforeignregistry.h `、` qwlroots/src/types/qwxdgforeignv1.h `、` qwlroots/src/types/qwxdgforeignv2.h `、` qwlroots/src/types/qwxdgoutputv1.h `、` qwlroots/src/types/qwxdgshell.h `、` qwlroots/src/types/qwxwayland.h `、` qwlroots/src/types/qwxwaylandserver.h `、` qwlroots/src/types/qwxwaylandshellv1.h `、` qwlroots/src/types/qwxwaylandsurface.h `、` qwlroots/src/util/qwbox.h `、` qwlroots/src/util/qwlogging.h `、` qwlroots/src/util/qwsignalconnector.h `、` qwlroots/tests/CMakeLists.txt `、` qwlroots/tests/qwobject_test/CMakeLists.txt `、` qwlroots/tests/qwobject_test/qwabc.h `、` qwlroots/tests/qwobject_test/test_qwobject.cpp `、` qwlroots/tests/qwobject_test/wlr_abc.cpp `、` qwlroots/tests/qwobject_test/wlr_abc.h `、` qwlroots/tests/test_qwobject.cpp `、` waylib/.github/workflows/archlinux-build-wlroots-19.yaml `、` waylib/.gitmodules `、` waylib/.reuse/dep5 `、` waylib/CMakeLists.txt `、` waylib/README.md `、` waylib/README.zh_CN.md `、` qwlroots/cmake/WaylandScannerHelpers.cmake `、` waylib/cmake/WaylandScannerHelpers.cmake `、` waylib/debian/control `、` waylib/debian/rules `、` waylib/examples/blur/helper.h `、` waylib/examples/blur/main.cpp `、` waylib/examples/outputcopy/helper.h `、` waylib/examples/outputcopy/main.cpp `、` waylib/examples/outputviewport/helper.h `、` waylib/examples/outputviewport/main.cpp `、` waylib/examples/surface-delegate/main.cpp `、` waylib/examples/tinywl/helper.cpp `、` waylib/examples/tinywl/helper.h `、` waylib/examples/tinywl/main.cpp `、` waylib/examples/tinywl/output.cpp `、` waylib/examples/tinywl/rootsurfacecontainer.cpp `、` waylib/examples/tinywl/rootsurfacecontainer.h `、` waylib/examples/tinywl/surfacewrapper.cpp `、` waylib/flake.lock `、` waylib/flake.nix `、` waylib/nix/default.nix `、` waylib/src/cmake/WaylibServerConfig.cmake.in `、` waylib/src/server/CMakeLists.txt `、` qwlroots/src/cmake/qwconfig.h.in `、` waylib/src/server/cmake/wconfig.h.in `、` waylib/src/server/kernel/private/wcursor_p.h `、` waylib/src/server/kernel/private/wglobal_p.h `、` waylib/src/server/kernel/private/woutputlayout_p.h `、` waylib/src/server/kernel/private/wserver_p.h `、` waylib/src/server/kernel/private/wsurface_p.h `、` waylib/src/server/kernel/private/wtoplevelsurface_p.h `、` waylib/src/server/kernel/wbackend.cpp `、` waylib/src/server/kernel/wbackend.h `、` waylib/src/server/kernel/wcursor.cpp `、` waylib/src/server/kernel/wcursor.h `、` waylib/src/server/kernel/wglobal.cpp `、` waylib/src/server/kernel/wglobal.h `、` waylib/src/server/kernel/winputdevice.cpp `、` waylib/src/server/kernel/winputdevice.h `、` waylib/src/server/kernel/wlr_all.h `、` waylib/src/server/kernel/wlr_fwd.h `、` waylib/src/server/kernel/woutput.cpp `、` waylib/src/server/kernel/woutput.h `、` waylib/src/server/kernel/woutputlayout.cpp `、` waylib/src/server/kernel/woutputlayout.h `、` waylib/src/server/kernel/wpointer.h `、` waylib/src/server/kernel/wseat.cpp `、` waylib/src/server/kernel/wseat.h `、` waylib/src/server/kernel/wserver.cpp `、` waylib/src/server/kernel/wserver.h `、` waylib/src/server/kernel/wsocket.cpp `、` waylib/src/server/kernel/wsurface.cpp `、` waylib/src/server/kernel/wsurface.h `、` waylib/src/server/kernel/wtoplevelsurface.cpp `、` waylib/src/server/kernel/wtoplevelsurface.h `、` waylib/src/server/kernel/wxcursorimage.cpp `、` waylib/src/server/kernel/wxcursorimage.h `、` waylib/src/server/pch/pch.hxx `、` waylib/src/server/platformplugin/qwlrootscreen.cpp `、` waylib/src/server/platformplugin/qwlrootscreen.h `、` waylib/src/server/platformplugin/qwlrootscursor.h `、` waylib/src/server/platformplugin/qwlrootsintegration.cpp `、` waylib/src/server/platformplugin/qwlrootsintegration.h `、` waylib/src/server/platformplugin/qwlrootswindow.cpp `、` waylib/src/server/platformplugin/qwlrootswindow.h `、` waylib/src/server/protocols/ext_foreign_toplevel_image_capture_source_manager_v1.h `、` waylib/src/server/protocols/private/winputmethodv2.cpp `、` waylib/src/server/protocols/private/winputmethodv2_p.h `、` waylib/src/server/protocols/private/wtextinputv1.cpp `、` waylib/src/server/protocols/private/wtextinputv1_p.h `、` waylib/src/server/protocols/private/wtextinputv2.cpp `、` waylib/src/server/protocols/private/wtextinputv2_p.h `、` waylib/src/server/protocols/private/wtextinputv3.cpp `、` waylib/src/server/protocols/private/wtextinputv3_p.h `、` waylib/src/server/protocols/private/wvirtualkeyboardv1.cpp `、` waylib/src/server/protocols/private/wvirtualkeyboardv1_p.h `、` waylib/src/server/protocols/private/wxwaylandsurface_p.h `、` waylib/src/server/protocols/qwextforeigntoplevelimagecapturesourcemanagerv1.h `、` waylib/src/server/protocols/wcursorshapemanagerv1.cpp `、` waylib/src/server/protocols/wcursorshapemanagerv1.h `、` waylib/src/server/protocols/wextforeigntoplevellistv1.cpp `、` waylib/src/server/protocols/wextforeigntoplevellistv1.h `、` waylib/src/server/protocols/wforeigntoplevelv1.cpp `、` waylib/src/server/protocols/wforeigntoplevelv1.h `、` waylib/src/server/protocols/winputmethodhelper.cpp `、` waylib/src/server/protocols/winputmethodhelper.h `、` waylib/src/server/protocols/winputpopupsurface.cpp `、` waylib/src/server/protocols/winputpopupsurface.h `、` waylib/src/server/protocols/wlayershell.cpp `、` waylib/src/server/protocols/wlayershell.h `、` waylib/src/server/protocols/wlayersurface.cpp `、` waylib/src/server/protocols/wlayersurface.h `、` waylib/src/server/protocols/woutputmanagerv1.cpp `、` waylib/src/server/protocols/woutputmanagerv1.h `、` waylib/src/server/protocols/wsecuritycontextmanager.cpp `、` waylib/src/server/protocols/wsecuritycontextmanager.h `、` waylib/src/server/protocols/wsessionlock.cpp `、` waylib/src/server/protocols/wsessionlock.h `、` waylib/src/server/protocols/wsessionlockmanager.cpp `、` waylib/src/server/protocols/wsessionlockmanager.h `、` waylib/src/server/protocols/wsessionlocksurface.cpp `、` waylib/src/server/protocols/wsessionlocksurface.h `、` waylib/src/server/protocols/wxdgdecorationmanager.cpp `、` waylib/src/server/protocols/wxdgdecorationmanager.h `、` waylib/src/server/protocols/wxdgdialogmanagerv1.cpp `、` waylib/src/server/protocols/wxdgdialogmanagerv1.h `、` waylib/src/server/protocols/wxdgoutput.cpp `、` waylib/src/server/protocols/wxdgpopupsurface.cpp `、` waylib/src/server/protocols/wxdgpopupsurface.h `、` waylib/src/server/protocols/wxdgshell.cpp `、` waylib/src/server/protocols/wxdgshell.h `、` waylib/src/server/protocols/wxdgsurface.cpp `、` waylib/src/server/protocols/wxdgsurface.h `、` waylib/src/server/protocols/wxdgtoplevelsurface.cpp `、` waylib/src/server/protocols/wxdgtoplevelsurface.h `、` waylib/src/server/protocols/wxdgtopleveltagmanager.cpp `、` waylib/src/server/protocols/wxwayland.cpp `、` waylib/src/server/protocols/wxwayland.h `、` waylib/src/server/protocols/wxwaylandsurface.cpp `、` waylib/src/server/protocols/wxwaylandsurface.h `、` waylib/src/server/qtquick/private/wbufferrenderer.cpp `、` waylib/src/server/qtquick/private/wbufferrenderer_p.h `、` waylib/src/server/qtquick/private/woutputitem_p.h `、` waylib/src/server/qtquick/private/woutputviewport_p.h `、` waylib/src/server/qtquick/private/wrenderbuffernode.cpp `、` waylib/src/server/qtquick/private/wsurfaceitem_p.h `、` waylib/src/server/qtquick/wbufferitem.cpp `、` waylib/src/server/qtquick/wbufferitem.h `、` waylib/src/server/qtquick/wlayersurfaceitem.cpp `、` waylib/src/server/qtquick/woutputhelper.cpp `、` waylib/src/server/qtquick/woutputhelper.h `、` waylib/src/server/qtquick/woutputitem.cpp `、` waylib/src/server/qtquick/woutputlayer.cpp `、` waylib/src/server/qtquick/woutputlayer.h `、` waylib/src/server/qtquick/woutputlayoutitem.cpp `、` waylib/src/server/qtquick/woutputlayoutitem.h `、` waylib/src/server/qtquick/woutputrenderwindow.cpp `、` waylib/src/server/qtquick/woutputrenderwindow.h `、` waylib/src/server/qtquick/woutputviewport.cpp `、` waylib/src/server/qtquick/woutputviewport.h `、` waylib/src/server/qtquick/wquickcursor.cpp `、` waylib/src/server/qtquick/wquickoutputlayout.cpp `、` waylib/src/server/qtquick/wrenderhelper.cpp `、` waylib/src/server/qtquick/wrenderhelper.h `、` waylib/src/server/qtquick/wsgtextureprovider.cpp `、` waylib/src/server/qtquick/wsgtextureprovider.h `、` waylib/src/server/qtquick/wsurfaceitem.cpp `、` waylib/src/server/qtquick/wxdgpopupsurfaceitem.cpp `、` waylib/src/server/qtquick/wxdgtoplevelsurfaceitem.cpp `、` waylib/src/server/qtquick/wxwaylandsurfaceitem.cpp `、` waylib/src/server/utils/wbufferdumper.cpp `、` waylib/src/server/utils/wbufferdumper.h `、` waylib/src/server/utils/wcontainerof.h `、` waylib/src/server/utils/wcursorimage.cpp `、` waylib/src/server/utils/wextimagecapturesourcev1impl.cpp `、` waylib/src/server/utils/wextimagecapturesourcev1impl.h `、` waylib/src/server/utils/wimagebuffer.cpp `、` waylib/src/server/utils/wimagebuffer.h `、` waylib/src/server/utils/wlogging.h `、` waylib/src/server/utils/wscopedvalue.h `、` waylib/src/server/utils/wscoplistener.cpp `、` waylib/src/server/utils/wscoplistener.h `、` waylib/src/server/utils/wtools.cpp `、` waylib/src/server/utils/wwrappointer.h `、` waylib/src/server/wayliblogging.cpp `、` waylib/src/server/wayliblogging.h `、` waylib/tests/manual/live/helper.h `、` waylib/tests/manual/live/main.cpp `、` waylib/tests/unit_tests/CMakeLists.txt `、` waylib/tests/unit_tests/test_containerof/CMakeLists.txt `、` waylib/tests/unit_tests/test_containerof/main.cpp `、` waylib/tests/unit_tests/test_containerof/negative_compile.cpp `、` waylib/tests/unit_tests/test_native_handles/CMakeLists.txt `、` waylib/tests/unit_tests/test_native_handles/main.cpp `、` waylib/tests/unit_tests/test_native_lifecycle/CMakeLists.txt `、` waylib/tests/unit_tests/test_native_lifecycle/main.cpp `、` waylib/tests/unit_tests/test_wlog/CMakeLists.txt `、` waylib/tests/unit_tests/test_wlog/main.cpp `、` waylib/tests/unit_tests/test_wobject_listeners/CMakeLists.txt `、` waylib/tests/unit_tests/test_wobject_listeners/main.cpp `、` waylib/tests/unit_tests/test_wpointer/CMakeLists.txt `、` waylib/tests/unit_tests/test_wpointer/main.cpp `、` waylib/tests/unit_tests/test_wscoplistener/CMakeLists.txt `、` waylib/tests/unit_tests/test_wscoplistener/main.cpp `、` waylib/tests/unit_tests/test_wwrappointer/CMakeLists.txt `、` waylib/tests/unit_tests/test_wwrappointer/main.cpp `、` waylib/tests/unit_tests/test_wwrappointer/wrapobject.h `、` wlroots/CMakeLists.txt `、` wlroots/cmake/waylib-wlroots.pc.in `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 93e9eef541115c83126b256489ab618d465c057f ` → ` 9e58c1f7a8e4af110340e8ada6d24398d2f90c1a `。
  原证据引用：` 54a49ec203485a02f6531b58020cabce631b0e14 ` → ` 93d893187e4bf4491a089d567e31a7a7da532c00 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 9582881ddc2e71c73f01eb1f8f5efd0b87a8b107 ` 和原目标 ` c65523a80d93d7fb885ac16b4338169eaab99c7c ` 查询。
- 原审核说明：` 完成原生 API 和测试调用方迁移，保留本地多座席、生命周期和 QML URI；在精确批准的既有运行时安装入口安装真实原生共享库，不借用系统或构建树库，也不增加兼容别名。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/d3726e904dac69ac8d2e5f319c2d7f076b645e23.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 9e58c1f7a8e4af110340e8ada6d24398d2f90c1a `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-102"></a>
### 102. N5 / ` refactor(wallpaper): simplify native output conversion `

- 本仓内容路径：` compositor/src/modules/wallpaper/wallpapermanagerinterfacev1.cpp `。
- 实际改变：` compositor/src/modules/wallpaper/wallpapermanagerinterfacev1.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 9e58c1f7a8e4af110340e8ada6d24398d2f90c1a ` → ` 9e58c1f7a8e4af110340e8ada6d24398d2f90c1a `。
  原证据引用：` 93d893187e4bf4491a089d567e31a7a7da532c00 ` → ` 93d893187e4bf4491a089d567e31a7a7da532c00 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` c696665b368bcb54ef6c8e5510f383672ea10329 ` 和原目标 ` 6a44102ce5d9f86ce168a90e42ef128af773944c ` 查询。

<a id="entry-103"></a>
### 103. N5 / ` fix(wallpaper): handle missing reference configuration `

- 本仓内容路径：` compositor/src/wallpaper/wallpapermanager.cpp `。
- 实际改变：` compositor/src/wallpaper/wallpapermanager.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 9e58c1f7a8e4af110340e8ada6d24398d2f90c1a ` → ` 9e58c1f7a8e4af110340e8ada6d24398d2f90c1a `。
  原证据引用：` 93d893187e4bf4491a089d567e31a7a7da532c00 ` → ` 93d893187e4bf4491a089d567e31a7a7da532c00 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 1addea0a87111d2121d42977ab5b65f8a16544c3 ` 和原目标 ` c172fd981d2764a0fd96084b84c5f4df482a6af5 ` 查询。

<a id="entry-104"></a>
### 104. N5 / ` Updates for project TreeLand (#1265) `

- 本仓内容路径：` compositor/src/plugins/lockscreen/translations/lockscreen.ru.ts `、` compositor/src/plugins/multitaskview/translations/multitaskview.ru.ts `、` compositor/translations/treeland.ru.ts `。
- 实际改变：` compositor/src/plugins/lockscreen/translations/lockscreen.ru.ts `、` compositor/src/plugins/multitaskview/translations/multitaskview.ru.ts `、` compositor/translations/treeland.ru.ts `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 9e58c1f7a8e4af110340e8ada6d24398d2f90c1a ` → ` 9e58c1f7a8e4af110340e8ada6d24398d2f90c1a `。
  原证据引用：` 93d893187e4bf4491a089d567e31a7a7da532c00 ` → ` 93d893187e4bf4491a089d567e31a7a7da532c00 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` c5466c27e69c09833cfc69444d19b10484a28d0c ` 和原目标 ` 98104edfd8ffad3dabfc1fb787b8a6086beed977 ` 查询。

<a id="entry-105"></a>
### 105. N5 / ` fix(xwayland): displayed incorrectly when maximized during initialization `

- 本仓内容路径：` compositor/src/core/shellhandler.cpp `、` compositor/src/surface/surfacewrapper.cpp `。
- 实际改变：` compositor/src/core/shellhandler.cpp `、` compositor/src/surface/surfacewrapper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 9e58c1f7a8e4af110340e8ada6d24398d2f90c1a ` → ` 9e58c1f7a8e4af110340e8ada6d24398d2f90c1a `。
  原证据引用：` 93d893187e4bf4491a089d567e31a7a7da532c00 ` → ` 93d893187e4bf4491a089d567e31a7a7da532c00 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 78de1d09212c1491d1107a76a0e6ebc4f13c06d3 ` 和原目标 ` 1182ac54012841668b8687378c6d94c5615ac573 ` 查询。

<a id="entry-106"></a>
### 106. N5 / ` fix: restore declarativeData cleanup in WObject::teardown `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/kernel/wglobal.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 9e58c1f7a8e4af110340e8ada6d24398d2f90c1a ` → ` 8dff87ca8ecbcc2d37fdaeb6ff0769bb0b2733b2 `。
  原证据引用：` 93d893187e4bf4491a089d567e31a7a7da532c00 ` → ` 098ac7e1d82f7f8c0ac099eb34bbd5ec16ebaf4b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 1708d699270363c01d636bce8f444628ba6b95d1 ` 和原目标 ` 818c71467e13e56da48d63e241b55db2452fc01e ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 8dff87ca8ecbcc2d37fdaeb6ff0769bb0b2733b2 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-107"></a>
### 107. N5 / ` fix(xwayland): synchronize EWMH desktop properties `

- 本仓内容路径：` compositor/src/core/shellhandler.cpp `、` compositor/src/core/shellhandler.h `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/core/shellhandler.cpp `、` compositor/src/core/shellhandler.h `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `。
- 排除的来源路径：` waylib/src/server/protocols/wxdgoutput.cpp `、` waylib/src/server/protocols/wxdgoutput.h `、` waylib/src/server/protocols/wxwayland.cpp `、` waylib/src/server/protocols/wxwayland.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 8dff87ca8ecbcc2d37fdaeb6ff0769bb0b2733b2 ` → ` de74680ea8a70564993b5aee0cbee7405848eada `。
  原证据引用：` 098ac7e1d82f7f8c0ac099eb34bbd5ec16ebaf4b ` → ` c64f150a29bd79a6cacf14b4a7878de7f76d0978 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 293dbe5ef45d3e3bf597126ba990a77003502210 ` 和原目标 ` d5f2b63e0625545925c98068367f7f70e241528f ` 查询。
- 原审核说明：` 三方合入 EWMH 桌面属性同步，保留目标 Helper 与多座席既有实现，只在来源规定的四个规范文件增加桌面通知、输出和工作区监听。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/6a4067b259530f22d6accd973cc7460f668d321c.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` de74680ea8a70564993b5aee0cbee7405848eada `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-108"></a>
### 108. N5 / ` refactor: extract WWaylandResource from WObject `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/CMakeLists.txt `、` waylib/src/server/kernel/private/wglobal_p.h `、` waylib/src/server/kernel/private/wsurface_p.h `、` waylib/src/server/kernel/private/wtoplevelsurface_p.h `、` waylib/src/server/kernel/private/wwaylandresource_p.h `、` waylib/src/server/kernel/wglobal.cpp `、` waylib/src/server/kernel/wglobal.h `、` waylib/src/server/kernel/wsurface.cpp `、` waylib/src/server/kernel/wsurface.h `、` waylib/src/server/kernel/wtoplevelsurface.cpp `、` waylib/src/server/kernel/wtoplevelsurface.h `、` waylib/src/server/kernel/wwaylandresource.cpp `、` waylib/src/server/kernel/wwaylandresource.h `、` waylib/src/server/protocols/private/wtextinput_p.h `、` waylib/src/server/protocols/wxwayland.cpp `、` waylib/src/server/protocols/wxwayland.h `、` waylib/src/server/qtquick/private/wquicksocketattached.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` de74680ea8a70564993b5aee0cbee7405848eada ` → ` b57b8ff6ca4f7d109a9fb60d5eba6793e4c1003e `。
  原证据引用：` c64f150a29bd79a6cacf14b4a7878de7f76d0978 ` → ` 0a38730db85e772c6b80050210344fde60dddc61 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 78773de1f242c1438b78f716c7d11522b58022a5 ` 和原目标 ` 8922d52eccc5d1b6a2a7cc91ba8251010dc902fd ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` b57b8ff6ca4f7d109a9fb60d5eba6793e4c1003e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-109"></a>
### 109. N5 / ` fix(waylib): adapt native handles after qwlroots removal `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/protocols/wxdgoutput.cpp `、` waylib/src/server/protocols/wxwayland.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` b57b8ff6ca4f7d109a9fb60d5eba6793e4c1003e ` → ` f448e31e43bffb462f083707bf2f95d8f010e8f2 `。
  原证据引用：` 0a38730db85e772c6b80050210344fde60dddc61 ` → ` 11e096a97e13d4b8740cea0d735f758e66b6534c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` b037ac5c5dcd33032424d546a312d0ad702c4bf0 ` 和原目标 ` ee6dbab417444731ce4947f5cc0fa5d9a6d9e917 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` f448e31e43bffb462f083707bf2f95d8f010e8f2 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-110"></a>
### 110. N5 / ` chore(examples): use hyphens in example binary names `

- 本仓内容路径：` compositor/examples/test_data_control_manager/CMakeLists.txt `、` compositor/examples/test_glass/CMakeLists.txt `、` compositor/examples/test_idle_inhibit_v1/CMakeLists.txt `、` compositor/examples/test_input_manager/CMakeLists.txt `、` compositor/examples/test_monitor_active_event/CMakeLists.txt `、` compositor/examples/test_set_wallpaper/CMakeLists.txt `。
- 实际改变：` compositor/examples/test_data_control_manager/CMakeLists.txt `、` compositor/examples/test_glass/CMakeLists.txt `、` compositor/examples/test_idle_inhibit_v1/CMakeLists.txt `、` compositor/examples/test_input_manager/CMakeLists.txt `、` compositor/examples/test_monitor_active_event/CMakeLists.txt `、` compositor/examples/test_set_wallpaper/CMakeLists.txt `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` f448e31e43bffb462f083707bf2f95d8f010e8f2 ` → ` f448e31e43bffb462f083707bf2f95d8f010e8f2 `。
  原证据引用：` 11e096a97e13d4b8740cea0d735f758e66b6534c ` → ` 11e096a97e13d4b8740cea0d735f758e66b6534c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 2c203454926f687ee5de51bba5f1f0478249c88c ` 和原目标 ` 8b13bc88dfeda8f013972dd2cdfe12028c931ded ` 查询。
- 原审核说明：` 将来源示例可执行文件及其 CMake 引用一致改为连字符名称；保留目标的 WaylibShared 链接、协议源和 compositor 构建布局。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/282ef67dd3dd1e0238f3298b15227ee9c039797f.md)。

<a id="entry-111"></a>
### 111. N5 / ` fix(output): skip configuration callbacks on initialization failure `

- 本仓内容路径：` compositor/src/seat/helper.cpp `。
- 实际改变：` compositor/src/seat/helper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` f448e31e43bffb462f083707bf2f95d8f010e8f2 ` → ` f448e31e43bffb462f083707bf2f95d8f010e8f2 `。
  原证据引用：` 11e096a97e13d4b8740cea0d735f758e66b6534c ` → ` 11e096a97e13d4b8740cea0d735f758e66b6534c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` b6dfb35207860d75b07cabf216484b7ba166038f ` 和原目标 ` 8e3d0d0096837a3e4237779319e10bf58a9becdd ` 查询。
- 原审核说明：` 保留配置失败不执行恢复回调的来源语义；独立处理同步和异步初始化失败，仅发布存活输出的当前状态并告警，共享单次标记防止两个失败信号重复添加协议头。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/7fed084667655e3ba8f49ecc721915ca2411b75f.md)。

<a id="entry-112"></a>
### 112. N5 / ` feat(systemd): set GTK_IM_MODULE=fcitx in treeland-sd service `

- 本仓内容路径：` compositor/misc/systemd/dde-session-pre.target.wants/treeland-sd.service.in `。
- 实际改变：` compositor/misc/systemd/dde-session-pre.target.wants/treeland-sd.service.in `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` f448e31e43bffb462f083707bf2f95d8f010e8f2 ` → ` f448e31e43bffb462f083707bf2f95d8f010e8f2 `。
  原证据引用：` 11e096a97e13d4b8740cea0d735f758e66b6534c ` → ` 11e096a97e13d4b8740cea0d735f758e66b6534c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` fdd73671fe9a16b061bad76e2d73babc65856581 ` 和原目标 ` decd03f1654c315938d43ea1451d1ba14ae421c7 ` 查询。

<a id="entry-113"></a>
### 113. N5 / ` chore: bump version to 0.8.18 `

- 本仓内容路径：` compositor/CMakeLists.txt `、` compositor/debian/changelog `。
- 实际改变：` compositor/CMakeLists.txt `、` compositor/debian/changelog `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` f448e31e43bffb462f083707bf2f95d8f010e8f2 ` → ` f448e31e43bffb462f083707bf2f95d8f010e8f2 `。
  原证据引用：` 11e096a97e13d4b8740cea0d735f758e66b6534c ` → ` 11e096a97e13d4b8740cea0d735f758e66b6534c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/parent-evidence.json`；以来源 ` 7134887c66e5215182e1a1f648bdc8971f17e864 ` 和原目标 ` d24d389a597f9be2e619586bcc76b3c0518ceef3 ` 查询。
- 原审核说明：` 仅将产品版本推进到来源 0.8.18 并保留来源 changelog，维持 DeckCompositor 项目名、AUTOMOC/AUTORCC/AUTOUIC 与本地顶层集成。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/9df94d7acf275a73289f2b31315e4dc42dc22207.md)。

<a id="entry-114"></a>
### 114. N6 / ` fix(waylib): drop invalid rect count assertion in toPixmanRegion `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/utils/wtools.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` f448e31e43bffb462f083707bf2f95d8f010e8f2 ` → ` 1df4bc80fb5aeeb3cf89eac354668102cdde1e61 `。
  原证据引用：` 11e096a97e13d4b8740cea0d735f758e66b6534c ` → ` a4ffa524241607aaeb72724845956ad5f26216da `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` b248e3682368a351ee2d4622c06fbe5e9c2d3b16 ` 和原目标 ` 4954329816561c4d82b69f691c4627a3aa24c58b ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 1df4bc80fb5aeeb3cf89eac354668102cdde1e61 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-115"></a>
### 115. N6 / ` fix: support restart after WServer::stop `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/kernel/wseat.cpp `、` waylib/src/server/kernel/wserver.cpp `、` waylib/src/server/kernel/wserver.h `、` waylib/src/server/kernel/wsocket.cpp `、` waylib/src/server/kernel/wsocket.h `、` waylib/src/server/protocols/private/winputmethodv2.cpp `、` waylib/src/server/protocols/private/winputmethodv2_p.h `、` waylib/src/server/protocols/private/wtextinputv3.cpp `、` waylib/src/server/protocols/private/wvirtualkeyboardv1.cpp `、` waylib/src/server/protocols/private/wvirtualkeyboardv1_p.h `、` waylib/src/server/protocols/wcursorshapemanagerv1.cpp `、` waylib/src/server/protocols/wcursorshapemanagerv1.h `、` waylib/src/server/protocols/wextforeigntoplevellistv1.cpp `、` waylib/src/server/protocols/wforeigntoplevelv1.cpp `、` waylib/src/server/protocols/wlayershell.cpp `、` waylib/src/server/protocols/wsecuritycontextmanager.cpp `、` waylib/src/server/protocols/wsecuritycontextmanager.h `、` waylib/src/server/protocols/wsessionlockmanager.cpp `、` waylib/src/server/protocols/wxdgdecorationmanager.cpp `、` waylib/src/server/protocols/wxdgdialogmanagerv1.cpp `、` waylib/src/server/protocols/wxdgshell.cpp `、` waylib/src/server/protocols/wxwayland.cpp `、` waylib/tests/unit_tests/test_native_handles/main.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 1df4bc80fb5aeeb3cf89eac354668102cdde1e61 ` → ` c2fee2e4fd0aed29f0c8ee9537076b8a9d403c1c `。
  原证据引用：` a4ffa524241607aaeb72724845956ad5f26216da ` → ` 09e92a03ef380917965047fb18010131303e4b98 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` f2773149b47ddca53b9fc234172830073964334b ` 和原目标 ` 3c7f3d83d1ec7b341a5b81137c792bf4ffb7751f ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` c2fee2e4fd0aed29f0c8ee9537076b8a9d403c1c `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-116"></a>
### 116. N6 / ` fix(waylib): guard removeListeners against null owner in detach `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/qtquick/woutputrenderwindow.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` c2fee2e4fd0aed29f0c8ee9537076b8a9d403c1c ` → ` edc0e10e06169968888fd781fff799da0bdf2acd `。
  原证据引用：` 09e92a03ef380917965047fb18010131303e4b98 ` → ` 41c86dc64620e0c8e71a709b070ba43fb6605cd9 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ecb32e8a1fab02512038324e5a5e7a6cdf8ffa74 ` 和原目标 ` 2b85480211e6fb1ba43814440cc835f2a70859bc ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` edc0e10e06169968888fd781fff799da0bdf2acd `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-117"></a>
### 117. N6 / ` fix(waylib): skip removeListeners in detach during window destruction `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/qtquick/woutputrenderwindow.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` edc0e10e06169968888fd781fff799da0bdf2acd ` → ` 896c23dfb3484bd65551c2246352a7743276e616 `。
  原证据引用：` 41c86dc64620e0c8e71a709b070ba43fb6605cd9 ` → ` f6c78a55d25f172bc9d682ac50ee3d3f09c8b231 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ee787154f3035363bd1c3a95741fd5283b1796f3 ` 和原目标 ` 9851d44e6dc6e9ef8c658396f2b0a4477c5a2866 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 896c23dfb3484bd65551c2246352a7743276e616 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-118"></a>
### 118. N6 / ` fix: show desktop — move keyboard focus to the desktop layer `

- 本仓内容路径：` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `。
- 实际改变：` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 896c23dfb3484bd65551c2246352a7743276e616 ` → ` 896c23dfb3484bd65551c2246352a7743276e616 `。
  原证据引用：` f6c78a55d25f172bc9d682ac50ee3d3f09c8b231 ` → ` f6c78a55d25f172bc9d682ac50ee3d3f09c8b231 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 48f9b57f346766710f86592cb4d2929cf6b3ed08 ` 和原目标 ` c9b3fe937f7f2aeed5fbe0629530e13d370c745a ` 查询。

<a id="entry-119"></a>
### 119. N6 / ` fix(popup): dismiss popup grab on outside click; drop UB drag cast `

- 本仓内容路径：` compositor/src/seat/helper.cpp `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `。
- 实际改变：` compositor/src/seat/helper.cpp `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 896c23dfb3484bd65551c2246352a7743276e616 ` → ` 896c23dfb3484bd65551c2246352a7743276e616 `。
  原证据引用：` f6c78a55d25f172bc9d682ac50ee3d3f09c8b231 ` → ` f6c78a55d25f172bc9d682ac50ee3d3f09c8b231 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 7df69e62d117508e633ac4d740cde9cbd31dc338 ` 和原目标 ` f810abe625e56051a2167498c1a03fe05a27f48c ` 查询。

<a id="entry-120"></a>
### 120. N6 / ` fix(waylib): commit a buffer for capture on static screens `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/qtquick/woutputrenderwindow.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 896c23dfb3484bd65551c2246352a7743276e616 ` → ` 281088c63a118b2cf9cf47ec67023009f7e37676 `。
  原证据引用：` f6c78a55d25f172bc9d682ac50ee3d3f09c8b231 ` → ` ed0bd1a229adff58a1acffa0d2aeec5d28e1be5d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 447c3da6712695822738ee399ca08eb9c82eef4e ` 和原目标 ` a95ea37df1b89841931749bba252c2acf794091d ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 281088c63a118b2cf9cf47ec67023009f7e37676 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-121"></a>
### 121. N6 / ` refactor: move qtwaylandscanner from src/modules/tools to waylib/tools `

- 本仓内容路径：` compositor/.agents/skills/treeland-private-wayland-protocol/SKILL.md `、` compositor/src/modules/CMakeLists.txt `、` compositor/src/modules/activation/CMakeLists.txt `、` compositor/src/modules/app-id-resolver/CMakeLists.txt `、` compositor/src/modules/dde-shell/CMakeLists.txt `、` compositor/src/modules/ddm/CMakeLists.txt `、` compositor/src/modules/foreign-toplevel/CMakeLists.txt `、` compositor/src/modules/input-manager/CMakeLists.txt `、` compositor/src/modules/keyboard-state-notify/CMakeLists.txt `、` compositor/src/modules/output-manager/CMakeLists.txt `、` compositor/src/modules/personalization/CMakeLists.txt `、` compositor/src/modules/prelaunch-splash/CMakeLists.txt `、` compositor/src/modules/screensaver/CMakeLists.txt `、` compositor/src/modules/shortcut/CMakeLists.txt `、` compositor/src/modules/virtual-output/CMakeLists.txt `、` compositor/src/modules/wallpaper-color/CMakeLists.txt `、` compositor/src/modules/wallpaper/CMakeLists.txt `、` compositor/src/modules/window-management/CMakeLists.txt `、` compositor/src/modules/wine-window-management/CMakeLists.txt `、` compositor/src/modules/wine-window-state/CMakeLists.txt `、` compositor/src/modules/tools/CMakeLists.txt `、` compositor/src/modules/tools/qtwaylandscanner.cpp `。
- 实际改变：` 3rdparty/waylib-shared `、` CMakeLists.txt `、` compositor/.agents/skills/treeland-private-wayland-protocol/SKILL.md `、` compositor/src/modules/CMakeLists.txt `、` compositor/src/modules/activation/CMakeLists.txt `、` compositor/src/modules/app-id-resolver/CMakeLists.txt `、` compositor/src/modules/dde-shell/CMakeLists.txt `、` compositor/src/modules/ddm/CMakeLists.txt `、` compositor/src/modules/foreign-toplevel/CMakeLists.txt `、` compositor/src/modules/input-manager/CMakeLists.txt `、` compositor/src/modules/keyboard-state-notify/CMakeLists.txt `、` compositor/src/modules/output-manager/CMakeLists.txt `、` compositor/src/modules/personalization/CMakeLists.txt `、` compositor/src/modules/prelaunch-splash/CMakeLists.txt `、` compositor/src/modules/screensaver/CMakeLists.txt `、` compositor/src/modules/shortcut/CMakeLists.txt `、` compositor/src/modules/tools/CMakeLists.txt `、` compositor/src/modules/tools/qtwaylandscanner.cpp `、` compositor/src/modules/virtual-output/CMakeLists.txt `、` compositor/src/modules/wallpaper-color/CMakeLists.txt `、` compositor/src/modules/wallpaper/CMakeLists.txt `、` compositor/src/modules/window-management/CMakeLists.txt `、` compositor/src/modules/wine-window-management/CMakeLists.txt `、` compositor/src/modules/wine-window-state/CMakeLists.txt `、` qtwaylandscanner/CMakeLists.txt `、` qtwaylandscanner/qtwaylandscanner.cpp `。
- 排除的来源路径：` waylib/CMakeLists.txt `、` waylib/tools/CMakeLists.txt `、` waylib/tools/qtwaylandscanner.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 281088c63a118b2cf9cf47ec67023009f7e37676 ` → ` eb6e6905b6231c6be2292c7bbc57c9a1928c7b27 `。
  原证据引用：` ed0bd1a229adff58a1acffa0d2aeec5d28e1be5d ` → ` 350e7b8af815d0ee111663f9686daae88f93df63 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 2e27ca38141087e551e22330165c86d886bd8cdf ` 和原目标 ` a0fd3d5f69f8ec3ddd8d1cffe9a1d6fb69b469e6 ` 查询。
- 原审核说明：` 使用 C 的统一 scanner 与生成函数，保留 DeckShell target、仓库内协议目录和当前模块输出路径；移除重复生成 C 源登记及旧 scanner，原件已移入回收站。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/607d7c87fda0da5a019b40e7b339ea48c35c00fb.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` eb6e6905b6231c6be2292c7bbc57c9a1928c7b27 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-122"></a>
### 122. N6 / ` feat(wayland): implement cross-process subsurface protocol and rendering integration `

- 本仓内容路径：` .github/workflows/waylib-archlinux-build.yml `、` .github/workflows/waylib-debian-build.yml `、` .github/workflows/waylib-deepin-build.yml `、` compositor/REUSE.toml `、` compositor/src/modules/capture/capture.cpp `、` compositor/src/seat/helper.cpp `。
- 实际改变：` .github/workflows/waylib-archlinux-build.yml `、` .github/workflows/waylib-debian-build.yml `、` .github/workflows/waylib-deepin-build.yml `、` 3rdparty/waylib-shared `、` CMakeLists.txt `、` compositor/REUSE.toml `、` compositor/src/modules/capture/capture.cpp `、` compositor/src/seat/helper.cpp `、` compositor/tests/test_protocol_source_policy/package_policy.cmake `、` protocols/compositor/CMakeLists.txt `、` protocols/compositor/xml/treeland-remote-subsurface-unstable-v1.xml `。
- 排除的来源路径：` waylib/debian/control `、` waylib/src/server/CMakeLists.txt `、` waylib/src/server/kernel/WSubsurface `、` waylib/src/server/kernel/private/wsubsurface_p.h `、` waylib/src/server/kernel/private/wsurface_p.h `、` waylib/src/server/kernel/wsubsurface.cpp `、` waylib/src/server/kernel/wsubsurface.h `、` waylib/src/server/kernel/wsurface.cpp `、` waylib/src/server/kernel/wsurface.h `、` waylib/src/server/protocols/wremotesubsurfacemanagerv1.cpp `、` waylib/src/server/protocols/wremotesubsurfacemanagerv1.h `、` waylib/src/server/qtquick/private/wsurfaceitem_p.h `、` waylib/src/server/qtquick/wsurfaceitem.cpp `、` waylib/src/server/wayliblogging.cpp `、` waylib/src/server/wayliblogging.h `、` waylib/tools/CMakeLists.txt `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` eb6e6905b6231c6be2292c7bbc57c9a1928c7b27 ` → ` 773b23071dcd4ed01a82eb1c1218e00284403345 `。
  原证据引用：` 350e7b8af815d0ee111663f9686daae88f93df63 ` → ` 97a507e3b0bfff1a60d92c556ad890628bf87420 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 8e41511b7dbc1ad148a23f5817b36527def9ddce ` 和原目标 ` aea999673fe2f249fc975be237a1d9d1189e8c75 ` 查询。
- 原审核说明：` 跨进程子表面协议已按冻结 Git 输入加入包中，现有来源与安装包测试均固定检查 22 个 XML，保留缺失文件和未安装文件的拒绝行为。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/99ee1b5737ab41417d42ac4ea2ca452b6b9f1b19.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 773b23071dcd4ed01a82eb1c1218e00284403345 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-123"></a>
### 123. N6 / ` refactor(waylib): rename OutputHelper output/qwoutput to outputViewport/output `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/qtquick/woutputrenderwindow.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 773b23071dcd4ed01a82eb1c1218e00284403345 ` → ` 711c38995fa56c82ce1c78f40a00702b4b533eca `。
  原证据引用：` 97a507e3b0bfff1a60d92c556ad890628bf87420 ` → ` 055e192714a6f1fddb6619edaa694fc5a0ddfc35 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 53dffe1867ea3a13167eecff0d08343b3cc2a368 ` 和原目标 ` e3486b1bab6bcd9270dfcff0b34d161b9adfe00f ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 711c38995fa56c82ce1c78f40a00702b4b533eca `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-124"></a>
### 124. N6 / ` feat: add privileged overlay surface support `

- 本仓内容路径：` compositor/src/CMakeLists.txt `、` compositor/src/common/treelandlogging.cpp `、` compositor/src/common/treelandlogging.h `、` compositor/src/core/imcandidatepanelmanager.cpp `、` compositor/src/core/imcandidatepanelmanager.h `、` compositor/src/core/rootsurfacecontainer.h `、` compositor/src/core/shellhandler.cpp `、` compositor/src/core/shellhandler.h `、` compositor/src/plugins/lockscreen/qml/ControlAction.qml `、` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 实际改变：` compositor/src/CMakeLists.txt `、` compositor/src/common/treelandlogging.cpp `、` compositor/src/common/treelandlogging.h `、` compositor/src/core/imcandidatepanelmanager.cpp `、` compositor/src/core/imcandidatepanelmanager.h `、` compositor/src/core/rootsurfacecontainer.h `、` compositor/src/core/shellhandler.cpp `、` compositor/src/core/shellhandler.h `、` compositor/src/plugins/lockscreen/qml/ControlAction.qml `、` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 711c38995fa56c82ce1c78f40a00702b4b533eca ` → ` 711c38995fa56c82ce1c78f40a00702b4b533eca `。
  原证据引用：` 055e192714a6f1fddb6619edaa694fc5a0ddfc35 ` → ` 055e192714a6f1fddb6619edaa694fc5a0ddfc35 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 0060a0d0dcdc189b263fffc51b4ad6e021de9854 ` 和原目标 ` 929909b325d11ee2801036ef7ca6c721160255e2 ` 查询。
- 原审核说明：` 逐路径三方合入来源变化，保留已确认的目标布局、依赖接入、命名空间与非冲突本地修复；源前后对象及目标前后对象逐项绑定。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/3f6a45c376e219dba41bb78e7cc47db97e977e90.md)。

<a id="entry-125"></a>
### 125. N6 / ` feat(examples): add tag selection combobox to test-toplevel-tag `

- 本仓内容路径：` compositor/examples/test_toplevel_tag/main.cpp `。
- 实际改变：` compositor/examples/test_toplevel_tag/main.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 711c38995fa56c82ce1c78f40a00702b4b533eca ` → ` 711c38995fa56c82ce1c78f40a00702b4b533eca `。
  原证据引用：` 055e192714a6f1fddb6619edaa694fc5a0ddfc35 ` → ` 055e192714a6f1fddb6619edaa694fc5a0ddfc35 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 9ba10c8ef0650cb2743d0666132c667046c6c51b ` 和原目标 ` a4ae48a523a4ebc090d55192f1c81dd6f64ff8a7 ` 查询。

<a id="entry-126"></a>
### 126. N6 / ` docs: drop qwlroots references from agent docs and fix build instructions `

- 本仓内容路径：` compositor/.agents/skills/logging-guidelines/SKILL.md `、` compositor/.agents/skills/treeland-private-wayland-protocol/SKILL.md `、` compositor/.agents/skills/upstream-wayland-protocol-wrapper/SKILL.md `、` compositor/AGENTS.md `、` compositor/REUSE.toml `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/.agents/skills/logging-guidelines/SKILL.md `、` compositor/.agents/skills/treeland-private-wayland-protocol/SKILL.md `、` compositor/.agents/skills/upstream-wayland-protocol-wrapper/SKILL.md `、` compositor/AGENTS.md `、` compositor/REUSE.toml `。
- 排除的来源路径：` waylib/README.md `、` waylib/README.zh_CN.md `、` waylib/src/server/CMakeLists.txt `、` waylib/src/server/kernel/wpointer.h `、` waylib/src/server/utils/wlogging.h `、` wlroots/CMakeLists.txt `、` wlroots/cmake/WlrootsProtocols.cmake `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 711c38995fa56c82ce1c78f40a00702b4b533eca ` → ` 95805e685187082bf4d98c48b3ad9b62aa3cb083 `。
  原证据引用：` 055e192714a6f1fddb6619edaa694fc5a0ddfc35 ` → ` 9e5db571fabf467e04cb9cee8c140fe25f8cede7 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 30447d0582ccb582acf38cef4db4b729704dc6b6 ` 和原目标 ` 24dbc1727571c5137eff819c468058d236081000 ` 查询。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 95805e685187082bf4d98c48b3ad9b62aa3cb083 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-127"></a>
### 127. N6 / ` fix(lockscreen): improve keyboard navigation in lock screen power controls `

- 本仓内容路径：` compositor/src/plugins/lockscreen/qml/ControlAction.qml `、` compositor/src/plugins/lockscreen/qml/PowerList.qml `、` compositor/src/plugins/lockscreen/qml/ShutdownButton.qml `、` compositor/src/plugins/lockscreen/qml/ShutdownView.qml `。
- 实际改变：` compositor/src/plugins/lockscreen/qml/ControlAction.qml `、` compositor/src/plugins/lockscreen/qml/PowerList.qml `、` compositor/src/plugins/lockscreen/qml/ShutdownButton.qml `、` compositor/src/plugins/lockscreen/qml/ShutdownView.qml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 95805e685187082bf4d98c48b3ad9b62aa3cb083 ` → ` 95805e685187082bf4d98c48b3ad9b62aa3cb083 `。
  原证据引用：` 9e5db571fabf467e04cb9cee8c140fe25f8cede7 ` → ` 9e5db571fabf467e04cb9cee8c140fe25f8cede7 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` a50a1ff5dd11bd4a769a5c2176ff718411dea9fe ` 和原目标 ` a801b9bd05f2c51c57445da3751adc6f63d8bded ` 查询。

<a id="entry-128"></a>
### 128. N6 / ` feat: support relative pointer motion `

- 本仓内容路径：` compositor/REUSE.toml `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/REUSE.toml `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `。
- 排除的来源路径：` waylib/src/server/CMakeLists.txt `、` waylib/src/server/kernel/wcursor.cpp `、` waylib/src/server/kernel/wlr_all.h `、` waylib/src/server/kernel/wlr_fwd.h `、` waylib/src/server/kernel/wseat.h `、` waylib/src/server/protocols/WRelativePointerManagerV1 `、` waylib/src/server/protocols/wrelativepointermanagerv1.cpp `、` waylib/src/server/protocols/wrelativepointermanagerv1.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 95805e685187082bf4d98c48b3ad9b62aa3cb083 ` → ` bac6df1fc667642884ff0cf696e10c88c1f1e0ab `。
  原证据引用：` 9e5db571fabf467e04cb9cee8c140fe25f8cede7 ` → ` 2eb3bb27299d7875cf3fc6b231f13a72b255cfab `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 80137e42c2dfa4b1ff7edb0c81ab75da9c9f171f ` 和原目标 ` 965c520ea5dce8c4ee5ae66d65a77039fea7bb1e ` 查询。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 同一 Treeland 来源的 C / waylib-shared 目标：` bac6df1fc667642884ff0cf696e10c88c1f1e0ab `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-129"></a>
### 129. N6 / ` fix: minimize abandoned show-desktop windows in cancelShowDesktop `

- 本仓内容路径：` compositor/src/plugins/multitaskview/multitaskview.cpp `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `。
- 实际改变：` compositor/src/plugins/multitaskview/multitaskview.cpp `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` bac6df1fc667642884ff0cf696e10c88c1f1e0ab ` → ` bac6df1fc667642884ff0cf696e10c88c1f1e0ab `。
  原证据引用：` 2eb3bb27299d7875cf3fc6b231f13a72b255cfab ` → ` 2eb3bb27299d7875cf3fc6b231f13a72b255cfab `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 0c6e43e72c74a95ec603c6f7e517507dfbf0311e ` 和原目标 ` a7496a016c4bb70eca6cf7182c8e310595ffaf06 ` 查询。

<a id="entry-130"></a>
### 130. N6 / ` fix: show desktop — fade decoration shadow with the restore animation `

- 本仓内容路径：` compositor/src/core/qml/Animations/ShowDesktopAnimation.qml `。
- 实际改变：` compositor/src/core/qml/Animations/ShowDesktopAnimation.qml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` bac6df1fc667642884ff0cf696e10c88c1f1e0ab ` → ` bac6df1fc667642884ff0cf696e10c88c1f1e0ab `。
  原证据引用：` 2eb3bb27299d7875cf3fc6b231f13a72b255cfab ` → ` 2eb3bb27299d7875cf3fc6b231f13a72b255cfab `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` b1c772c6cbf1061bce476dff32878f0894901ab4 ` 和原目标 ` 27de46cad543e6c3d830456b7ab4b80a6f57db42 ` 查询。

<a id="entry-131"></a>
### 131. N6 / ` fix: use WPointer for cursorClient and skip redundant cursor updates `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/kernel/wseat.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` bac6df1fc667642884ff0cf696e10c88c1f1e0ab ` → ` caec417b89bcc3fad81f8a8d84600ed68b7e9f7a `。
  原证据引用：` 2eb3bb27299d7875cf3fc6b231f13a72b255cfab ` → ` 2417ba7c1c5a418da1bfa917ff2ad26da20f333c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 22609c6cb07f3493b948aeee2d018093478eca83 ` 和原目标 ` b6a0f8fb50d77417654f844cafc825d142fe8f8e ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` caec417b89bcc3fad81f8a8d84600ed68b7e9f7a `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-132"></a>
### 132. N6 / ` fix(lockscreen): use loginGroup.width for leftPadding binding to fix binding loop `

- 本仓内容路径：` compositor/src/plugins/lockscreen/qml/UserInput.qml `。
- 实际改变：` compositor/src/plugins/lockscreen/qml/UserInput.qml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` caec417b89bcc3fad81f8a8d84600ed68b7e9f7a ` → ` caec417b89bcc3fad81f8a8d84600ed68b7e9f7a `。
  原证据引用：` 2417ba7c1c5a418da1bfa917ff2ad26da20f333c ` → ` 2417ba7c1c5a418da1bfa917ff2ad26da20f333c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` e7bd2c16c3b7c1dff1b39236b9724b4a15e2fab2 ` 和原目标 ` 6a5fce35493da5471a6daaa22c0ab83ebd036e35 ` 查询。

<a id="entry-133"></a>
### 133. N6 / ` docs: recommend the ci build preset for daily development in AGENTS.md `

- 本仓内容路径：` compositor/AGENTS.md `。
- 实际改变：` compositor/AGENTS.md `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` caec417b89bcc3fad81f8a8d84600ed68b7e9f7a ` → ` caec417b89bcc3fad81f8a8d84600ed68b7e9f7a `。
  原证据引用：` 2417ba7c1c5a418da1bfa917ff2ad26da20f333c ` → ` 2417ba7c1c5a418da1bfa917ff2ad26da20f333c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 07421a378dfb63d2e84ab0af2cdc2224b87802c8 ` 和原目标 ` 426d11f2bec4acc24cb493feec6cfb018feec68a ` 查询。

<a id="entry-134"></a>
### 134. N6 / ` feat: add prestart script runner for launching apps before lock screen `

- 本仓内容路径：` compositor/src/CMakeLists.txt `、` compositor/src/common/treelandlogging.cpp `、` compositor/src/common/treelandlogging.h `、` compositor/src/core/treeland.cpp `、` compositor/src/utils/scriptrunner.cpp `、` compositor/src/utils/scriptrunner.h `。
- 实际改变：` compositor/src/CMakeLists.txt `、` compositor/src/common/treelandlogging.cpp `、` compositor/src/common/treelandlogging.h `、` compositor/src/core/treeland.cpp `、` compositor/src/utils/scriptrunner.cpp `、` compositor/src/utils/scriptrunner.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` caec417b89bcc3fad81f8a8d84600ed68b7e9f7a ` → ` caec417b89bcc3fad81f8a8d84600ed68b7e9f7a `。
  原证据引用：` 2417ba7c1c5a418da1bfa917ff2ad26da20f333c ` → ` 2417ba7c1c5a418da1bfa917ff2ad26da20f333c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` a050947305cd232a992d4e70b4668b20bcaaff25 ` 和原目标 ` a62e09b2a18442c47c4140caba074d6e84471632 ` 查询。
- 原审核说明：` 合入锁屏前应用脚本启动器，保留本地产品链接和目录；仅移除上游日志文件末尾多余空行。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/cf5c5ac84e68c1c1af7349d985df26885e673002.md)。

<a id="entry-135"></a>
### 135. N6 / ` build: bump version to 0.20.0-dev `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/.builds/archlinux.yml `、` 3rdparty/wlroots/.gitlab-ci.yml `、` 3rdparty/wlroots/backend/backend.c `、` 3rdparty/wlroots/backend/drm/drm.c `、` 3rdparty/wlroots/backend/libinput/events.c `、` 3rdparty/wlroots/backend/libinput/keyboard.c `、` 3rdparty/wlroots/backend/libinput/meson.build `、` 3rdparty/wlroots/backend/libinput/pointer.c `、` 3rdparty/wlroots/backend/libinput/switch.c `、` 3rdparty/wlroots/backend/libinput/tablet_pad.c `、` 3rdparty/wlroots/backend/libinput/tablet_tool.c `、` 3rdparty/wlroots/backend/session/session.c `、` 3rdparty/wlroots/include/backend/libinput.h `、` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/include/types/wlr_output.h `、` 3rdparty/wlroots/include/wlr/render/vulkan.h `、` 3rdparty/wlroots/include/wlr/types/wlr_data_device.h `、` 3rdparty/wlroots/include/wlr/types/wlr_drm_lease_v1.h `、` 3rdparty/wlroots/include/wlr/types/wlr_switch.h `、` 3rdparty/wlroots/include/xwayland/xwm.h `、` 3rdparty/wlroots/meson.build `、` 3rdparty/wlroots/render/allocator/shm.c `、` 3rdparty/wlroots/render/allocator/udmabuf.c `、` 3rdparty/wlroots/render/egl.c `、` 3rdparty/wlroots/render/pass.c `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/renderer.c `、` 3rdparty/wlroots/tinywl/Makefile `、` 3rdparty/wlroots/types/buffer/buffer.c `、` 3rdparty/wlroots/types/data_device/wlr_data_source.c `、` 3rdparty/wlroots/types/ext_image_capture_source_v1/output.c `、` 3rdparty/wlroots/types/output/cursor.c `、` 3rdparty/wlroots/types/output/output.c `、` 3rdparty/wlroots/types/scene/surface.c `、` 3rdparty/wlroots/types/seat/wlr_seat_pointer.c `、` 3rdparty/wlroots/types/wlr_cursor.c `、` 3rdparty/wlroots/types/wlr_drm_lease_v1.c `、` 3rdparty/wlroots/types/wlr_linux_drm_syncobj_v1.c `、` 3rdparty/wlroots/types/wlr_transient_seat_v1.c `、` 3rdparty/wlroots/types/wlr_virtual_pointer_v1.c `、` 3rdparty/wlroots/types/xdg_shell/wlr_xdg_popup.c `、` 3rdparty/wlroots/util/box.c `、` 3rdparty/wlroots/wlroots.syms `、` 3rdparty/wlroots/xcursor/xcursor.c `、` 3rdparty/wlroots/xwayland/selection/outgoing.c `、` 3rdparty/wlroots/xwayland/xwayland.c `、` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` caec417b89bcc3fad81f8a8d84600ed68b7e9f7a ` → ` bda29d68784ae59019163cebca299ebcbf32d8bf `。
  原证据引用：` 2417ba7c1c5a418da1bfa917ff2ad26da20f333c ` → ` bfea5a19eb419cf1e849237feed13ce320eb52b0 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 1921954d28e618fc3496d88d32b4063fbb56563e ` 和原目标 ` b9e028bc01eddf54a1cf0a4d7dbf63121695aafa ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` bda29d68784ae59019163cebca299ebcbf32d8bf `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-136"></a>
### 136. N6 / ` Change all timespec pointers in events to owned `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_output.h `、` 3rdparty/wlroots/types/ext_image_capture_source_v1/output.c `、` 3rdparty/wlroots/types/output/output.c `、` 3rdparty/wlroots/types/wlr_cursor.c `、` 3rdparty/wlroots/types/wlr_export_dmabuf_v1.c `、` 3rdparty/wlroots/types/wlr_screencopy_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` bda29d68784ae59019163cebca299ebcbf32d8bf ` → ` 1465965ff43efd8ec6ecddbf7dbf50a996b8ad3e `。
  原证据引用：` bfea5a19eb419cf1e849237feed13ce320eb52b0 ` → ` 30317341c929cb749a3e7b948bec04da40f07021 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 8b6d1783cf48bc865d762701f97e376ce2449e50 ` 和原目标 ` 7298e94929212100f5354fd6ef7203a1e19d52b7 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 1465965ff43efd8ec6ecddbf7dbf50a996b8ad3e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-137"></a>
### 137. N6 / ` output: don't send make/model `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/output/output.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 1465965ff43efd8ec6ecddbf7dbf50a996b8ad3e ` → ` 4d19d6bae4130df6bbcbc2908da78d12a4c347a8 `。
  原证据引用：` 30317341c929cb749a3e7b948bec04da40f07021 ` → ` 4c93c2ac341cc2c6092f8d8a338995075757c8a4 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 2d47e5ed21e1b2c9cfa5ba80f4ca8ba1200e9f5c ` 和原目标 ` 651782d1aaf41de179160be9b89aa52118ec5b04 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 4d19d6bae4130df6bbcbc2908da78d12a4c347a8 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-138"></a>
### 138. N6 / ` Add support for XKB_LED_NAME_COMPOSE and XKB_LED_NAME_KANA USB HID LEDs Requires xkbcommon 1.8.0 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_keyboard.h `、` 3rdparty/wlroots/meson.build `、` 3rdparty/wlroots/types/wlr_keyboard.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 4d19d6bae4130df6bbcbc2908da78d12a4c347a8 ` → ` 01c2fc4420bdd6576060def42c58250e7958d1c3 `。
  原证据引用：` 4c93c2ac341cc2c6092f8d8a338995075757c8a4 ` → ` 5b098ba0991facda3bd5a476dd08b256d3e9f928 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` b6b92729856e1cfb59a5f4abccfa73fea008852d ` 和原目标 ` f6d10af3e4e1d93905fe6082e8ed7954a30c1e84 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 01c2fc4420bdd6576060def42c58250e7958d1c3 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-139"></a>
### 139. N6 / ` text-input-v3: Name new text input event correctly `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_text_input_v3.h `、` 3rdparty/wlroots/types/wlr_text_input_v3.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 01c2fc4420bdd6576060def42c58250e7958d1c3 ` → ` c95af3799d6189906ba41999a16c8fd0920020e1 `。
  原证据引用：` 5b098ba0991facda3bd5a476dd08b256d3e9f928 ` → ` 768c1a40227b489e92b427a1437c534bc4123a81 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 92cf9d3d54f20cbf7bc509a2413678e89f8a0f25 ` 和原目标 ` 0bce1099c8cb3086a37b75de3a012fa564324fd5 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` c95af3799d6189906ba41999a16c8fd0920020e1 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-140"></a>
### 140. N6 / `` text-input-v3: Use `NULL` when emitting signals ``

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_text_input_v3.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` c95af3799d6189906ba41999a16c8fd0920020e1 ` → ` c6c8b99d2e4b350c9c05a4a3d40af339750b26cc `。
  原证据引用：` 768c1a40227b489e92b427a1437c534bc4123a81 ` → ` ee8a08b5d74c1bf52c28d847d779c09d7771093a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` eec5773b46a1e5286ba8f6f85a4da40eba85580f ` 和原目标 ` 11415e1f8f22020b7abc4cf7443e169c0ff9cdd1 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` c6c8b99d2e4b350c9c05a4a3d40af339750b26cc `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-141"></a>
### 141. N6 / ` backend/libinput: don't leak udev_device `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/libinput/tablet_pad.c `、` 3rdparty/wlroots/backend/libinput/tablet_tool.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` c6c8b99d2e4b350c9c05a4a3d40af339750b26cc ` → ` d6ba89bf3e9b4d7e18e96d563a5e6f71f4719df1 `。
  原证据引用：` ee8a08b5d74c1bf52c28d847d779c09d7771093a ` → ` 943ac702b52165264a468b7209ba9b3902de6d30 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` f1cbaab98b5d4568ebe244229931d5ae4665ea9d ` 和原目标 ` f5ed4f40d542de2cf9eef79ab339caaad5c449d8 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` d6ba89bf3e9b4d7e18e96d563a5e6f71f4719df1 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-142"></a>
### 142. N6 / ` xwayland: Remove has_utf8_title field `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/xwayland/xwayland.h `、` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` d6ba89bf3e9b4d7e18e96d563a5e6f71f4719df1 ` → ` 110e9183432076f513cfec931934b6bb5cf8540b `。
  原证据引用：` 943ac702b52165264a468b7209ba9b3902de6d30 ` → ` bc3da7afa4792fdb4610943273491af1e0316b2c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 3b7e3f20e120dc85e9f08d0989075f17818334ef ` 和原目标 ` 1914c653363161faaef2c7c894dcc8a82ae0b904 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 110e9183432076f513cfec931934b6bb5cf8540b `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-143"></a>
### 143. N6 / ` cursor-shape-v1: use generated enum validator `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_cursor_shape_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 110e9183432076f513cfec931934b6bb5cf8540b ` → ` ca7c10c62e923bd66fa707950b104e3ba20f5c52 `。
  原证据引用：` bc3da7afa4792fdb4610943273491af1e0316b2c ` → ` b74e13d52832ad7899e9bbb86558445b6c090e7d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 6ad1e1212a78210e7c6f8bec0476d40193852fde ` 和原目标 ` 58e10daba700b60b28f86d43d4ffbea73314b06b ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` ca7c10c62e923bd66fa707950b104e3ba20f5c52 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-144"></a>
### 144. N6 / ` cursor-shape-v1: bump to version 2 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/protocol/meson.build `、` 3rdparty/wlroots/types/wlr_cursor_shape_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` ca7c10c62e923bd66fa707950b104e3ba20f5c52 ` → ` 561d3f245a9e27c4af84aca5d68cf3ad7ed38736 `。
  原证据引用：` b74e13d52832ad7899e9bbb86558445b6c090e7d ` → ` c0147dc4251f608e544615b1648de51915c502dc `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 22b4fe8e7a5d0eb9688d407442ec941c715b1546 ` 和原目标 ` 9f99b02fdf346be97d0665a3fe0732ae12e07cfd ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 561d3f245a9e27c4af84aca5d68cf3ad7ed38736 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-145"></a>
### 145. N6 / ` render/pass: Ensure the precision is consistent during comparison `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 561d3f245a9e27c4af84aca5d68cf3ad7ed38736 ` → ` 00f46e97b30b893ff466517f2f2c8447da7b9b76 `。
  原证据引用：` c0147dc4251f608e544615b1648de51915c502dc ` → ` 406365476c29a57cd8429d619aabed63633981b9 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 8d1df35e6373636631bd0a46a1c89bd59763374e ` 和原目标 ` 11246d02e00b551f6eac1fe0cb58bf7b3dc6f580 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 00f46e97b30b893ff466517f2f2c8447da7b9b76 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-146"></a>
### 146. N6 / ` xdg-shell: add support for v7 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_xdg_shell.h `、` 3rdparty/wlroots/types/xdg_shell/wlr_xdg_shell.c `、` 3rdparty/wlroots/types/xdg_shell/wlr_xdg_toplevel.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 00f46e97b30b893ff466517f2f2c8447da7b9b76 ` → ` 2c7225a42cc4b03ad948bfd19b147d6fe6a5e8a0 `。
  原证据引用：` 406365476c29a57cd8429d619aabed63633981b9 ` → ` dca599a64b5009bea6b7a053bad4804c1271fc42 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 1419b581afd87ad0ae5df76757add34cb9a98bde ` 和原目标 ` b3c14b459a64d80335605c3cb6029579b8214a75 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 2c7225a42cc4b03ad948bfd19b147d6fe6a5e8a0 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-147"></a>
### 147. N6 / ` xwayland: Create a dummy no_focus_window to use for non-X window focus `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/xwayland/xwm.h `、` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 2c7225a42cc4b03ad948bfd19b147d6fe6a5e8a0 ` → ` ff665e2661e43887d500cd36a7b2d55a9de0156c `。
  原证据引用：` dca599a64b5009bea6b7a053bad4804c1271fc42 ` → ` 0293857a069034c7dbee77c02586a4e363490db3 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 8c6229f9c4eacae14accc02f0a941b0a03ca622b ` 和原目标 ` 16f7b31e4d8e3d597d7123f4771cce5f9e788436 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` ff665e2661e43887d500cd36a7b2d55a9de0156c `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-148"></a>
### 148. N6 / ` xwayland: Activate no_focus_window when a Wayland window is activated `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` ff665e2661e43887d500cd36a7b2d55a9de0156c ` → ` d2bf4483461d3c4d703d831dd3c7ad6046ef70cc `。
  原证据引用：` 0293857a069034c7dbee77c02586a4e363490db3 ` → ` e19151928ab4e645c8b18ee4745fa362d972126d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` e6793bd93ffc041083e31d408c3e3aced255d8bf ` 和原目标 ` 11d56309fffc4309dcb735a8414d637e86b9e825 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` d2bf4483461d3c4d703d831dd3c7ad6046ef70cc `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-149"></a>
### 149. N6 / ` idle_notify_v1: drop trailing spaces `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_idle_notify_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` d2bf4483461d3c4d703d831dd3c7ad6046ef70cc ` → ` a29179450adea072d9a8cc8c5fe66f953fa64588 `。
  原证据引用：` e19151928ab4e645c8b18ee4745fa362d972126d ` → ` 075b25aaacf1bf0119c80c15f60d96dad6455ff3 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 54187ff9b725b409e4f6533415a32dd3c11c442e ` 和原目标 ` 889979d4216a8a91c3c9336ed396567f21ccf653 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` a29179450adea072d9a8cc8c5fe66f953fa64588 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-150"></a>
### 150. N6 / ` xwayland: require xcb-xfixes 1.15 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/meson.build `、` 3rdparty/wlroots/xwayland/xwayland.c `、` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` a29179450adea072d9a8cc8c5fe66f953fa64588 ` → ` d5e4250c5a73576a3ae05a72096b9b479cc052be `。
  原证据引用：` 075b25aaacf1bf0119c80c15f60d96dad6455ff3 ` → ` 8badc5ae8201eab5827b7adee05a17b4bc5b60bd `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` b3c71df01083877ecf3200323ea551c192d8a898 ` 和原目标 ` fc690665b76b0c08be2396b0df94f7d5a92b3ec1 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` d5e4250c5a73576a3ae05a72096b9b479cc052be `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-151"></a>
### 151. N6 / ` render/allocator/gbm: require GBM 21.1 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/allocator/gbm.c `、` 3rdparty/wlroots/render/allocator/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` d5e4250c5a73576a3ae05a72096b9b479cc052be ` → ` 004fe8fffdfe15e81b7ffb36ed3dbb3005678361 `。
  原证据引用：` 8badc5ae8201eab5827b7adee05a17b4bc5b60bd ` → ` 4d713766203aa69f8093a8318401047d37787fde `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 3697e0f99a06e24895ac96cf0ee3c7a54bf1608b ` 和原目标 ` d653b99d978c5c78d96104a9b6ebaeab283c17a2 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 004fe8fffdfe15e81b7ffb36ed3dbb3005678361 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-152"></a>
### 152. N6 / ` swapchain: assert that size is not empty at creation time `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/swapchain.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 004fe8fffdfe15e81b7ffb36ed3dbb3005678361 ` → ` 693ff3574911b388917423f7a467acd3c48f1424 `。
  原证据引用：` 4d713766203aa69f8093a8318401047d37787fde ` → ` 2248d37a4527f86556c06daeffdd295e8b7d4648 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 30f621f3623fcdf8d3256886584286f4aaf08f3a ` 和原目标 ` 5fa870246b3670640638f9ffbde04206f5a3f8af ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 693ff3574911b388917423f7a467acd3c48f1424 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-153"></a>
### 153. N6 / ` ext_image_capture_source_v1: add support for foreign toplevels `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_ext_image_capture_source_v1.h `、` 3rdparty/wlroots/types/ext_image_capture_source_v1/foreign_toplevel.c `、` 3rdparty/wlroots/types/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 693ff3574911b388917423f7a467acd3c48f1424 ` → ` 09513062f8da9891fd7e88f76c54e7669645d2b4 `。
  原证据引用：` 2248d37a4527f86556c06daeffdd295e8b7d4648 ` → ` 0a62c6e4ef95240bcc8929f47e1103bdfde54233 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` a7e0d3626ecafd17cbfc9c19f5807cced5b7dbf3 ` 和原目标 ` ac4d55eb69fa0a57a9b524de822c374464ec53b9 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 09513062f8da9891fd7e88f76c54e7669645d2b4 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-154"></a>
### 154. N6 / ` ext_image_capture_source_v1: add helper to capture scene nodes `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/types/wlr_scene.h `、` 3rdparty/wlroots/include/wlr/types/wlr_ext_image_capture_source_v1.h `、` 3rdparty/wlroots/types/ext_image_capture_source_v1/scene.c `、` 3rdparty/wlroots/types/meson.build `、` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 09513062f8da9891fd7e88f76c54e7669645d2b4 ` → ` 1353228b9af02f52385c7f40f449107da90a239e `。
  原证据引用：` 0a62c6e4ef95240bcc8929f47e1103bdfde54233 ` → ` ff44ffca1bf151d73f19560696ad23a80fdc5a08 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 5912dc0f34fcecfdd5476656e3c34a26e74db765 ` 和原目标 ` 3211263a79a966b813ce08160f1bdf0fc1c53c7e ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 1353228b9af02f52385c7f40f449107da90a239e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-155"></a>
### 155. N6 / ` scene: ignore outputs with too small intersection with nodes `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 1353228b9af02f52385c7f40f449107da90a239e ` → ` cf0b326a402c77045cea41af7d9ee6e06c5f762d `。
  原证据引用：` ff44ffca1bf151d73f19560696ad23a80fdc5a08 ` → ` 322f1c6c247bffd43727cee45d36f5d560644d51 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 622b27271a424a1dc392ad665f0ddfca06263231 ` 和原目标 ` 545a0b7cdcb965a6e1bc871233becb1667399764 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` cf0b326a402c77045cea41af7d9ee6e06c5f762d `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-156"></a>
### 156. N6 / ` scene: configure clients with the highest output scale `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/surface.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` cf0b326a402c77045cea41af7d9ee6e06c5f762d ` → ` 3773ca6d34e1c1674e0b8b470cdd94dd053940bb `。
  原证据引用：` 322f1c6c247bffd43727cee45d36f5d560644d51 ` → ` bf997e2f1535710dc1025ee170b468a166ae0341 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 96bccf46d3653a46327e838e90d52d5ec96554f5 ` 和原目标 ` badd8e20986b256d6b07d891067e9f1a7489b69b ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 3773ca6d34e1c1674e0b8b470cdd94dd053940bb `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-157"></a>
### 157. N6 / ` scene: filter frame_done primary output in surface handler `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_scene.h `、` 3rdparty/wlroots/types/scene/surface.c `、` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 3773ca6d34e1c1674e0b8b470cdd94dd053940bb ` → ` 084bce3a18f534d251123ca94e3646899fb1c3a7 `。
  原证据引用：` bf997e2f1535710dc1025ee170b468a166ae0341 ` → ` 4e3dc5ca8900acbeb5fdbfd0766cd3d77ed287d3 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 5515da6732aefbe2a23826617dd834bf9a2a7134 ` 和原目标 ` 83cc1b00e1a78831462a5c3a442c286482cd97ce ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 084bce3a18f534d251123ca94e3646899fb1c3a7 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-158"></a>
### 158. N6 / ` scene: use output with highest refresh rate for frame pacing `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_scene.h `、` 3rdparty/wlroots/types/scene/surface.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 084bce3a18f534d251123ca94e3646899fb1c3a7 ` → ` 9dc4d94f40d5894c5753daa82ecfba08d196785e `。
  原证据引用：` 4e3dc5ca8900acbeb5fdbfd0766cd3d77ed287d3 ` → ` 7dc80eefa105c1a313e5c6b9a125aa5cdccbe0ff `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ea887de23d872cf160647f8320633fc361d9f067 ` 和原目标 ` 34a79a3b518dfe3c8c77667d817cf69832554639 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 9dc4d94f40d5894c5753daa82ecfba08d196785e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-159"></a>
### 159. N6 / ` scene: send surface preferred transform alongside DMA-BUF feedback `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/surface.c `、` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 9dc4d94f40d5894c5753daa82ecfba08d196785e ` → ` 302fcac63a7fb33cee62a4956f25793d51e760d2 `。
  原证据引用：` 7dc80eefa105c1a313e5c6b9a125aa5cdccbe0ff ` → ` 0614224aef588dfe07aa028c0add9ad5b1b114f1 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` c96938ef3a78fc7d454eea5109cbde66d795ed6c ` 和原目标 ` 80f066e2fd824fcd561bf974a767f906822352e2 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 302fcac63a7fb33cee62a4956f25793d51e760d2 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-160"></a>
### 160. N6 / ` render/color: add wlr_color_transform_init() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/color.h `、` 3rdparty/wlroots/render/color.c `、` 3rdparty/wlroots/render/color_lcms2.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 302fcac63a7fb33cee62a4956f25793d51e760d2 ` → ` 039e19ef481c1261ce0829939fe7b33484c7840f `。
  原证据引用：` 0614224aef588dfe07aa028c0add9ad5b1b114f1 ` → ` 029e32cc33f4268ee2c814bca7a1aec25976664a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 573e7aa6533edcbf765751bb3e2355eed15ba689 ` 和原目标 ` 8840e115e3c987c4c88b5645276c22ba3425fd57 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 039e19ef481c1261ce0829939fe7b33484c7840f `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-161"></a>
### 161. N6 / ` render/color: use variable instead of type in sizeof() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/color.c `、` 3rdparty/wlroots/render/color_lcms2.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 039e19ef481c1261ce0829939fe7b33484c7840f ` → ` ae0b851047440eca17d4fa8130242b4d293ea9eb `。
  原证据引用：` 029e32cc33f4268ee2c814bca7a1aec25976664a ` → ` 9a328e1c03d2fbca5f12d506162a971843d9e08f `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` a3ad65170cb0d59adde8d743d3c0efcb90f101ae ` 和原目标 ` 6658466f91b60a6656d8354855cab2a2bc12f311 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` ae0b851047440eca17d4fa8130242b4d293ea9eb `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-162"></a>
### 162. N6 / ` render/color: replace COLOR_TRANSFORM_LUT_3D with COLOR_TRANSFORM_LCMS2 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/color.h `、` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/color.c `、` 3rdparty/wlroots/render/color_fallback.c `、` 3rdparty/wlroots/render/color_lcms2.c `、` 3rdparty/wlroots/render/vulkan/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` ae0b851047440eca17d4fa8130242b4d293ea9eb ` → ` 4663a72aa26a20b086c03e6073116da43fb7c493 `。
  原证据引用：` 9a328e1c03d2fbca5f12d506162a971843d9e08f ` → ` df635874401991d02b5949f8c45496d834249afb `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 28b8cd207acf042de0cde21a419944f3a5e98c0a ` 和原目标 ` 94710e566549d37c32d12c84b084e74e7508ef69 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 4663a72aa26a20b086c03e6073116da43fb7c493 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-163"></a>
### 163. N6 / ` render/color: introduce COLOR_TRANSFORM_LUT_3X1D `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/color.h `、` 3rdparty/wlroots/include/wlr/render/color.h `、` 3rdparty/wlroots/render/color.c `、` 3rdparty/wlroots/render/vulkan/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 4663a72aa26a20b086c03e6073116da43fb7c493 ` → ` fd6f0c8792143a6b7724581c5a0d058fcd2c3d74 `。
  原证据引用：` df635874401991d02b5949f8c45496d834249afb ` → ` 0587cc661376ffbfb7261cf4988c765d723f10ec `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` fa6a35279263b8f45ed98922e408b371641ce6f4 ` 和原目标 ` a071c375fd77ee1515aa1f7c04f48f62b56567eb ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` fd6f0c8792143a6b7724581c5a0d058fcd2c3d74 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-164"></a>
### 164. N6 / ` output: add color transform to state `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_output.h `、` 3rdparty/wlroots/types/output/output.c `、` 3rdparty/wlroots/types/output/state.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` fd6f0c8792143a6b7724581c5a0d058fcd2c3d74 ` → ` f6ed45b83dcc2359938099c6a4a3c9d931ebe06e `。
  原证据引用：` 0587cc661376ffbfb7261cf4988c765d723f10ec ` → ` d517ac9cfbec29c1cb5f7385a08128712dec2b35 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 3fa894cc040d4028e425492841f86d5556d46937 ` 和原目标 ` 33de57f30e6a2babed922d03ed949f75b1751ccd ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` f6ed45b83dcc2359938099c6a4a3c9d931ebe06e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-165"></a>
### 165. N6 / ` backend/drm: add support for color transforms `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/drm/atomic.c `、` 3rdparty/wlroots/backend/drm/drm.c `、` 3rdparty/wlroots/backend/drm/legacy.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` f6ed45b83dcc2359938099c6a4a3c9d931ebe06e ` → ` 3acf21fff4532368826a5c9f6a11473c9f02678d `。
  原证据引用：` d517ac9cfbec29c1cb5f7385a08128712dec2b35 ` → ` 801c81c2c42e489afd6775a1bb1077617e05d76e `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d40797ab9cfd328185f3a3ba8290fc083c292758 ` 和原目标 ` 1508b3afb0e4a86964e18f07d59e0bd6eafc3cfc ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 3acf21fff4532368826a5c9f6a11473c9f02678d `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-166"></a>
### 166. N6 / ` wlr_gamma_control_v1: use color transforms `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_gamma_control_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 3acf21fff4532368826a5c9f6a11473c9f02678d ` → ` 4d4495f0c203f7f74c174b52e57f11183e3e3129 `。
  原证据引用：` 801c81c2c42e489afd6775a1bb1077617e05d76e ` → ` 25bbb0582ecf710232588d9a28912f1629570a21 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 7b15516aa256d738c76e32fdd62e8ca11069b42d ` 和原目标 ` d76b74cc45400c2081b05640da25a044a9e3f7ff ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 4d4495f0c203f7f74c174b52e57f11183e3e3129 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-167"></a>
### 167. N6 / ` output: drop gamma LUT from state `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_output.h `、` 3rdparty/wlroots/types/output/output.c `、` 3rdparty/wlroots/types/output/state.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 4d4495f0c203f7f74c174b52e57f11183e3e3129 ` → ` 4e5cd5584f2967c0ee21d43ee85909b41386b56e `。
  原证据引用：` 25bbb0582ecf710232588d9a28912f1629570a21 ` → ` cadeafa7b05c1bf9774e40481fcaf85494b8ba96 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 334c2b21f20cf142d6fada8c47b074c73b9976c2 ` 和原目标 ` 9f40dd4d3f82f9cbcbbe7be03a6cc8f94316021e ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 4e5cd5584f2967c0ee21d43ee85909b41386b56e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-168"></a>
### 168. N6 / ` render/vulkan: add color transformation matrix `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/shaders/output.frag `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 4e5cd5584f2967c0ee21d43ee85909b41386b56e ` → ` 0b8d21bb32b9313d862498ec9753dfcb2f7bac4b `。
  原证据引用：` cadeafa7b05c1bf9774e40481fcaf85494b8ba96 ` → ` ab789d57e7f02fc0cecbab772567c58fefd33f31 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` bf5238919abe86a4fe0dd6909fc3f0bc76aa7369 ` 和原目标 ` 4a3c9f286f7f295e384a576e74c5683453071b66 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 0b8d21bb32b9313d862498ec9753dfcb2f7bac4b `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-169"></a>
### 169. N6 / ` render/vulkan: use output_pipe_srgb for non-NULL sRGB color transform `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 0b8d21bb32b9313d862498ec9753dfcb2f7bac4b ` → ` 2a86812fe2a4d7ce54fe10d388e8a6af245f807a `。
  原证据引用：` ab789d57e7f02fc0cecbab772567c58fefd33f31 ` → ` 57427cc4073c32f9b11f41822d3cfa6ca5c246f2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` edd2ff863d2799591b41bfc6a633d205f240e7d4 ` 和原目标 ` 4f0d38314a2a4ba953b8ee9fed57b779b0e55749 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 2a86812fe2a4d7ce54fe10d388e8a6af245f807a `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-170"></a>
### 170. N6 / ` render/vulkan: rename mat3_to_mat4() to encode_proj_matrix() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 2a86812fe2a4d7ce54fe10d388e8a6af245f807a ` → ` e53e15bede67f47503ac739f62f4bf9a644198d4 `。
  原证据引用：` 57427cc4073c32f9b11f41822d3cfa6ca5c246f2 ` → ` 877151afff019ab6d8432cdfb3abcd5ab68abb88 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 85be1f0a54bb42dcf542ab6aeb12bf3360eb9b5a ` 和原目标 ` 7a1ae9fd6de7dd8fa2bcb6b4c98581a98ae1d30b ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` e53e15bede67f47503ac739f62f4bf9a644198d4 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-171"></a>
### 171. N6 / ` render/vulkan: use array declaration in encode_proj_matrix() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` e53e15bede67f47503ac739f62f4bf9a644198d4 ` → ` 0d071b5f47e29acb9729a32dbd1d27f38e296989 `。
  原证据引用：` 877151afff019ab6d8432cdfb3abcd5ab68abb88 ` → ` 07457c22502ae0b982bf97d216db1b84404556ce `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` b02653d741e06f43e39329492ba348fea9081722 ` 和原目标 ` ac11ce200417bf4f8c6e86bee8866a9d5ff54fba ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 0d071b5f47e29acb9729a32dbd1d27f38e296989 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-172"></a>
### 172. N6 / ` render, render/vulkan: add primaries to wlr_buffer_pass_options `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/include/wlr/render/pass.h `、` 3rdparty/wlroots/render/vulkan/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 0d071b5f47e29acb9729a32dbd1d27f38e296989 ` → ` 4f2bb0ba57c8edf4787c33b6cf494ecbe24bcdcb `。
  原证据引用：` 07457c22502ae0b982bf97d216db1b84404556ce ` → ` 458aed70573092e3957a567244761d1b840d1e7c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ef9eb4e7391ebcb5e0ed8de36ee2d16e7a35ccf5 ` 和原目标 ` cb8627bdd8bb3ae759a80e3095eff2bdc45a4ef1 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 4f2bb0ba57c8edf4787c33b6cf494ecbe24bcdcb `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-173"></a>
### 173. N6 / ` output: add color primaries to output state `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_output.h `、` 3rdparty/wlroots/types/output/output.c `、` 3rdparty/wlroots/types/output/state.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 4f2bb0ba57c8edf4787c33b6cf494ecbe24bcdcb ` → ` ed25b7d3ff21bbcf968d2a002e593a27cfe1e075 `。
  原证据引用：` 458aed70573092e3957a567244761d1b840d1e7c ` → ` 436d2769bf185affcecc83b9c8154ef287026920 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 9604e4859299596f83425af79e7dfdea0d180b99 ` 和原目标 ` 2049967d82e98145be89c9eb7f7ac55634b16f1a ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` ed25b7d3ff21bbcf968d2a002e593a27cfe1e075 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-174"></a>
### 174. N6 / ` backend/drm: add support for color primaries `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/drm/atomic.c `、` 3rdparty/wlroots/backend/drm/drm.c `、` 3rdparty/wlroots/backend/drm/meson.build `、` 3rdparty/wlroots/backend/drm/properties.c `、` 3rdparty/wlroots/backend/drm/util.c `、` 3rdparty/wlroots/include/backend/drm/drm.h `、` 3rdparty/wlroots/include/backend/drm/properties.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` ed25b7d3ff21bbcf968d2a002e593a27cfe1e075 ` → ` 1d6c9ae270a1fe1c081a00cea0190783215db831 `。
  原证据引用：` 436d2769bf185affcecc83b9c8154ef287026920 ` → ` eb071219e32d9b8f9cc0ead3fa982b90762bf1f3 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 8f52ccea285f0f3c8a52142d597f5382c9b64197 ` 和原目标 ` 64ef4361008b38ab40c22d47b668bf473ea5bcfd ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 1d6c9ae270a1fe1c081a00cea0190783215db831 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-175"></a>
### 175. N6 / ` render/vulkan: add PQ inverse EOTF to output shader `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/renderer.c `、` 3rdparty/wlroots/render/vulkan/shaders/output.frag `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 1d6c9ae270a1fe1c081a00cea0190783215db831 ` → ` 95de6e66e1bd29930c154cca7d0128399e9a229f `。
  原证据引用：` eb071219e32d9b8f9cc0ead3fa982b90762bf1f3 ` → ` cc164c99997248a38bf8cd2de937f9f72793d3ba `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` a730f12008999409a4b07957833e1c0a494d43af ` 和原目标 ` 7d880ef834c54c36286696d7373aba5a4a6cd72a ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 95de6e66e1bd29930c154cca7d0128399e9a229f `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-176"></a>
### 176. N6 / ` render/color, render/vulkan: add support for PQ transfer function `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/color.h `、` 3rdparty/wlroots/include/wlr/render/color.h `、` 3rdparty/wlroots/render/color.c `、` 3rdparty/wlroots/render/vulkan/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 95de6e66e1bd29930c154cca7d0128399e9a229f ` → ` 77b098b6e45992f1d8790e4941d6ad4a23e0ed0d `。
  原证据引用：` cc164c99997248a38bf8cd2de937f9f72793d3ba ` → ` cc2ecd2f5dbeb469b830623d2f406d27476335fa `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 8808fbce11b8159413957d64adfb844dd068d5bc ` 和原目标 ` 3a92883d4adab1d9e95f427b94ab718b5ef91fc2 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 77b098b6e45992f1d8790e4941d6ad4a23e0ed0d `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-177"></a>
### 177. N6 / ` output: add transfer function to image description `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_output.h `、` 3rdparty/wlroots/types/output/output.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 77b098b6e45992f1d8790e4941d6ad4a23e0ed0d ` → ` 5cd0e8b0090fdb21d13418711464d434ea824e6b `。
  原证据引用：` cc2ecd2f5dbeb469b830623d2f406d27476335fa ` → ` e005ddb13a02652f853aed332557253e8c4029af `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` f686dfea1e1d783715acf91889f317ca1a94a151 ` 和原目标 ` 76e874583635e8994af46985dd115177489c851c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 5cd0e8b0090fdb21d13418711464d434ea824e6b `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-178"></a>
### 178. N6 / ` backend/drm: add support for image description transfer function `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/drm/atomic.c `、` 3rdparty/wlroots/backend/drm/properties.c `、` 3rdparty/wlroots/backend/drm/util.c `、` 3rdparty/wlroots/include/backend/drm/drm.h `、` 3rdparty/wlroots/include/backend/drm/properties.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 5cd0e8b0090fdb21d13418711464d434ea824e6b ` → ` 01d042f59dc0b3ca0f6f882ed19be3aa6364b476 `。
  原证据引用：` e005ddb13a02652f853aed332557253e8c4029af ` → ` 84b1a3b4edee7c1ca46b3ad21e5415a8a7e76200 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 34f1e53916440ad471d025e5c118cf7769ec0af3 ` 和原目标 ` d424c8010ccc126dd4feb1fc9d3bfc863ee56a75 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 01d042f59dc0b3ca0f6f882ed19be3aa6364b476 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-179"></a>
### 179. N6 / ` render/vulkan: add luminance multipler for output shader `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/shaders/output.frag `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 01d042f59dc0b3ca0f6f882ed19be3aa6364b476 ` → ` d47d456cb3e3afb482f57f03048755382c5cdee7 `。
  原证据引用：` 84b1a3b4edee7c1ca46b3ad21e5415a8a7e76200 ` → ` 3281c4f0f154d1ba8faf6280e27ff26c1ab98ec9 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 4ec0a9e4bf7ef12a6a6830b3ef15cd260bbb2de0 ` 和原目标 ` 2db22e2e4b72835aca460a02c8115610fa849b3f ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` d47d456cb3e3afb482f57f03048755382c5cdee7 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-180"></a>
### 180. N6 / ` render/vulkan: fix multiplication order for output color matrix `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` d47d456cb3e3afb482f57f03048755382c5cdee7 ` → ` 86061fd770a796108c9ad23fb8d5f5b292aa5b25 `。
  原证据引用：` 3281c4f0f154d1ba8faf6280e27ff26c1ab98ec9 ` → ` 0c42501119b972e76fd2fd60197656eb33edb14d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 7a009f2f18007c6afc7c11fa72948af9fabf990c ` 和原目标 ` 2263349be1a78821d2bf6bd576eb4d74036bba59 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 86061fd770a796108c9ad23fb8d5f5b292aa5b25 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-181"></a>
### 181. N6 / ` render/color, render/vulkan: add EXT_LINEAR to enum wlr_color_transfer_function `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/drm/atomic.c `、` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/include/wlr/render/color.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/renderer.c `、` 3rdparty/wlroots/render/vulkan/shaders/output.frag `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 86061fd770a796108c9ad23fb8d5f5b292aa5b25 ` → ` 2e88d8b62ccb66aabd4249625c84963ffee2db42 `。
  原证据引用：` 0c42501119b972e76fd2fd60197656eb33edb14d ` → ` 606e8363df106909de8e2b4dd904f514560c8ef9 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` e2e62b6ea6965c65f499de1b40a08330f371c9c8 ` 和原目标 ` c3574d750cc67a4a67a464d5fe5cc74a6c642dbf ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 2e88d8b62ccb66aabd4249625c84963ffee2db42 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-182"></a>
### 182. N6 / ` color-management-v1: add EXT_LINEAR `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 2e88d8b62ccb66aabd4249625c84963ffee2db42 ` → ` b93009d326ac2412bb57111784b35bbd76439594 `。
  原证据引用：` 606e8363df106909de8e2b4dd904f514560c8ef9 ` → ` 6086d6be5d6c3d1abdd5900402586c30c961a354 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 1fcd0c9da6a25d58a23b9450acdcd0d5609e9bbe ` 和原目标 ` 55883d772fc853d72fb22927889ca03b76f3d3ff ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` b93009d326ac2412bb57111784b35bbd76439594 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-183"></a>
### 183. N6 / ` render/pass: add wlr_render_texture_options.transfer_function `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/render/pass.h `、` 3rdparty/wlroots/include/wlr/render/wlr_renderer.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` b93009d326ac2412bb57111784b35bbd76439594 ` → ` 7b1c119ab285e69133b73a24c5e92fa40647a36a `。
  原证据引用：` 6086d6be5d6c3d1abdd5900402586c30c961a354 ` → ` 9dcd00d1b7aa3804d008ed25a7d5d472ff357035 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 04f282f3f12debe935a41ec6e709d40575ee8c8e ` 和原目标 ` 94a8020c923c5b71a554335fbd3508265d8f440e ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 7b1c119ab285e69133b73a24c5e92fa40647a36a `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-184"></a>
### 184. N6 / ` render/vulkan: fix typo in wlr_vk_texture.views comment `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 7b1c119ab285e69133b73a24c5e92fa40647a36a ` → ` a40e7694b04d0d385faa4a50e6a193f2e672dc50 `。
  原证据引用：` 9dcd00d1b7aa3804d008ed25a7d5d472ff357035 ` → ` 140ba9d203f2191d92d42e6a9514cc4b715e62ad `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 116c2281e863d65584756b8ff2eb3f8b34490bc5 ` 和原目标 ` a59c54b6e8a14815d16ce1b591a41960a371192f ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` a40e7694b04d0d385faa4a50e6a193f2e672dc50 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-185"></a>
### 185. N6 / ` render/vulkan: add support for texture transfer functions `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/renderer.c `、` 3rdparty/wlroots/render/vulkan/texture.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` a40e7694b04d0d385faa4a50e6a193f2e672dc50 ` → ` 3b5b9ed8886e94ce06d386da8207011c91141764 `。
  原证据引用：` 140ba9d203f2191d92d42e6a9514cc4b715e62ad ` → ` 8fb1466ff9a864cfa5be1a4ef7bc03b7e9aedf4b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ca49086f7f6582a8efa246fa1e1c93624b825a74 ` 和原目标 ` f7a6d6324a68402bd7a8889efa82372c263f337a ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 3b5b9ed8886e94ce06d386da8207011c91141764 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-186"></a>
### 186. N6 / ` scene: add transfer function support for wlr_scene_buffer `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_scene.h `、` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 3b5b9ed8886e94ce06d386da8207011c91141764 ` → ` 630b9c8d17917dc14c5200f8b787d63713a31a6f `。
  原证据引用：` 8fb1466ff9a864cfa5be1a4ef7bc03b7e9aedf4b ` → ` b180b97f41e105abcc0b03e68d478c039c6da4d5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d04c4477b8dff7b358d8950acc974dfe353f9602 ` 和原目标 ` 42036ad32c8a2706d1102377455fe46f2e2e25b8 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 630b9c8d17917dc14c5200f8b787d63713a31a6f `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-187"></a>
### 187. N6 / ` scene: add support for color-management-v1 transfer functions `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/surface.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 630b9c8d17917dc14c5200f8b787d63713a31a6f ` → ` f5eaf92ee414ce80e7ea48c1ec6ed090f2451ae4 `。
  原证据引用：` b180b97f41e105abcc0b03e68d478c039c6da4d5 ` → ` 63043d254c76bcd774aea910d736b40cf26e03df `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 31c96911257d84b52b6e85590d2c7a0ae1fbbde3 ` 和原目标 ` adbeb09971f5fdd91635a95df20495ed0ffff5c9 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` f5eaf92ee414ce80e7ea48c1ec6ed090f2451ae4 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-188"></a>
### 188. N6 / ` render/vulkan: prepare texture shader for new transforms `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/shaders/texture.frag `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` f5eaf92ee414ce80e7ea48c1ec6ed090f2451ae4 ` → ` 63fe5e1ad8e72fc8241b9677eecac26745e0d2a3 `。
  原证据引用：` 63043d254c76bcd774aea910d736b40cf26e03df ` → ` ce5de5ae0cf2ce282be13a9d91b1e48c4fcac7b5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` dfdbade3b1fba232c2d723922e1c95f3a7e0fbf4 ` 和原目标 ` 413b1f75b7e72034fd2748296916ec716ac0856c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 63fe5e1ad8e72fc8241b9677eecac26745e0d2a3 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-189"></a>
### 189. N6 / ` render/vulkan: introduce wlr_vk_frag_texture_pcr_data `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/shaders/texture.frag `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 63fe5e1ad8e72fc8241b9677eecac26745e0d2a3 ` → ` d470ca91cc9856df897999c43e28165b615a0589 `。
  原证据引用：` ce5de5ae0cf2ce282be13a9d91b1e48c4fcac7b5 ` → ` bf2b0e440a767dd23271904be70f32cf408c5114 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 385d8feaab802bcd0f29086eb7397fc0d45f5525 ` 和原目标 ` 5aecde5383ad9219c6014621de90bc6f254a8b8c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` d470ca91cc9856df897999c43e28165b615a0589 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-190"></a>
### 190. N6 / ` render/vulkan: add texture color transformation matrix `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/shaders/texture.frag `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` d470ca91cc9856df897999c43e28165b615a0589 ` → ` d653aac5ddc88c6aae8a6983e32def982b5aa4cb `。
  原证据引用：` bf2b0e440a767dd23271904be70f32cf408c5114 ` → ` ae3aa1344fc4a4d39be90807338717ce0ec7bf77 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` cc8a61bcb5cffc94a98020891c6839002714738c ` 和原目标 ` 46b8d043f5c50d5c3c82b360af9815722a572796 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` d653aac5ddc88c6aae8a6983e32def982b5aa4cb `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-191"></a>
### 191. N6 / ` render/vulkan: add support for PQ for textures `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/shaders/texture.frag `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` d653aac5ddc88c6aae8a6983e32def982b5aa4cb ` → ` 57aafc5c76d52d4805d2d65ad3819cae05982fd4 `。
  原证据引用：` ae3aa1344fc4a4d39be90807338717ce0ec7bf77 ` → ` 0fbc7fa696eaaebb144808a400c5b3d89145efeb `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 19383eccf888693daab4cc2fca8dc60a44906c37 ` 和原目标 ` 1d0ca8a3d91bad5ea7e04dba01750a2bed0b09f9 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 57aafc5c76d52d4805d2d65ad3819cae05982fd4 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-192"></a>
### 192. N6 / ` render, render/vulkan: add primaries to wlr_render_texture_options `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/render/pass.h `、` 3rdparty/wlroots/render/vulkan/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 57aafc5c76d52d4805d2d65ad3819cae05982fd4 ` → ` 8dd8caffcb28802bf6c2ebd2b499d6fcbf322590 `。
  原证据引用：` 0fbc7fa696eaaebb144808a400c5b3d89145efeb ` → ` 7f368248d231c14d597586aafe1abd6e7a52ced1 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d14e882d30f6edf50ed2cdc90526e46b671f9897 ` 和原目标 ` 93c3c55c6671bdb7990e5cf1ab545abc9c219df2 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 8dd8caffcb28802bf6c2ebd2b499d6fcbf322590 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-193"></a>
### 193. N6 / ` render/vulkan: add luminance multiplier for texture shader `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/shaders/texture.frag `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 8dd8caffcb28802bf6c2ebd2b499d6fcbf322590 ` → ` 8050aec358db12a1a6872151080dc8ec06af1d67 `。
  原证据引用：` 7f368248d231c14d597586aafe1abd6e7a52ced1 ` → ` 3d200c3472fb185035f7c15d8cf386250f4f8df6 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 09e79cdfc902341d74cbe20bf8c31c14dac8db71 ` 和原目标 ` 0e3d1f90716d82726338151af1a639430d63433a ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 8050aec358db12a1a6872151080dc8ec06af1d67 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-194"></a>
### 194. N6 / ` scene: add primaries support to wlr_scene_buffer `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_scene.h `、` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 8050aec358db12a1a6872151080dc8ec06af1d67 ` → ` a77744fb4a74508296b8046e4cf39dc99cb5bc74 `。
  原证据引用：` 3d200c3472fb185035f7c15d8cf386250f4f8df6 ` → ` 5763401d4ef38c47ba8a9fd0cb5874a31b5a2a5d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ab42b16e5dcd895822b003517d7927906a1f41d1 ` 和原目标 ` a02b66429a213921c8d75a695758c80a0286d4df ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` a77744fb4a74508296b8046e4cf39dc99cb5bc74 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-195"></a>
### 195. N6 / ` scene: add support for color-management-v1 primaries `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/surface.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` a77744fb4a74508296b8046e4cf39dc99cb5bc74 ` → ` 4355e35766b98dac6119f91b2780f9f85badcce1 `。
  原证据引用：` 5763401d4ef38c47ba8a9fd0cb5874a31b5a2a5d ` → ` 2287d97c348369714c3b9ea158025d760d4ce41b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` f4af38c3cba717b2fcc9f6bd264a3c00abcf5f7c ` 和原目标 ` ff7000275f7cbc486b1e2122c5a1ac7a685d0e41 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 4355e35766b98dac6119f91b2780f9f85badcce1 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-196"></a>
### 196. N6 / ` output: shorten output enabled checks `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/output/output.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 4355e35766b98dac6119f91b2780f9f85badcce1 ` → ` 8f722f1bd418bcea2542707d8b86481d7dc636d0 `。
  原证据引用：` 2287d97c348369714c3b9ea158025d760d4ce41b ` → ` 94fbfd48d2a619b1d6bb5502704c341c0500137b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` f570342baf591db7616dc5befeb70b6f235d1713 ` 和原目标 ` abbe5b06d26617d58f14f90cdab677eea5c9bd2b ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 8f722f1bd418bcea2542707d8b86481d7dc636d0 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-197"></a>
### 197. N6 / ` util/box: set dest to empty if boxes don't intersect `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/util/box.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 8f722f1bd418bcea2542707d8b86481d7dc636d0 ` → ` fbfc9159402f58e2b52628e8990bac8edf450774 `。
  原证据引用：` 94fbfd48d2a619b1d6bb5502704c341c0500137b ` → ` 626e6ce5f1172f825d794f2eb94112051669982a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d67047baf7fc29be4808d31dcfc0174be85a2f40 ` 和原目标 ` 83247e7f7c2c920669c5cc8bbf4034bf82fb648b ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` fbfc9159402f58e2b52628e8990bac8edf450774 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-198"></a>
### 198. N6 / ` xwm: add support for _NET_WM_ICON `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/xwayland/xwayland.h `、` 3rdparty/wlroots/include/xwayland/xwm.h `、` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` fbfc9159402f58e2b52628e8990bac8edf450774 ` → ` 0858040e1d5bd1b04d89a2780435edfab09dd08f `。
  原证据引用：` 626e6ce5f1172f825d794f2eb94112051669982a ` → ` 4e4c8fac93fc4a370d70172fd9e946e7e27d18a8 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 06511afe2c784af2714aee5588bfbffa91c87f0a ` 和原目标 ` b52a2f88851517dd2f78a94b12d8141580cb952c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 0858040e1d5bd1b04d89a2780435edfab09dd08f `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-199"></a>
### 199. N6 / ` output: add wlr_output.image_description `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_output.h `、` 3rdparty/wlroots/types/output/output.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 0858040e1d5bd1b04d89a2780435edfab09dd08f ` → ` df8609cacb092ef9a49fda7df413c1c23c16066b `。
  原证据引用：` 4e4c8fac93fc4a370d70172fd9e946e7e27d18a8 ` → ` 5c9618d70af274ac5d49f8ada1d3a60d405b9fcb `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 880b5241663166d65ba65243ffaeff01a6ce5073 ` 和原目标 ` ad6fcdbfa71d7705d8f420f8aa3478dbb7bb2cf1 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` df8609cacb092ef9a49fda7df413c1c23c16066b `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-200"></a>
### 200. N6 / ` output: add output_pending_image_description() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/types/wlr_output.h `、` 3rdparty/wlroots/types/output/output.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` df8609cacb092ef9a49fda7df413c1c23c16066b ` → ` 26699c9211d52c0ea5f5092fc8a8e8e6771376a1 `。
  原证据引用：` 5c9618d70af274ac5d49f8ada1d3a60d405b9fcb ` → ` b6281114ff1d73227b0b11a672e4559bf4d3c668 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 5b55eddc4888fbe9a49197d49fe58b98c0bf03af ` 和原目标 ` d53520a011086e1b33c06afcf89ec69c6c239560 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 26699c9211d52c0ea5f5092fc8a8e8e6771376a1 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-201"></a>
### 201. N6 / ` scene: grab image description from output state `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_scene.h `、` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 26699c9211d52c0ea5f5092fc8a8e8e6771376a1 ` → ` c80ad01a750072c5b40747fe9352cf846d5b6000 `。
  原证据引用：` b6281114ff1d73227b0b11a672e4559bf4d3c668 ` → ` 1db9e9e4cd41eb95fb4217ec823cb29b7af10a44 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ff043fe802074ca7ee9dd46d17ecb9d482016948 ` 和原目标 ` 6dc2ecf54b19baa5d204933b28eae15458e5635f ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` c80ad01a750072c5b40747fe9352cf846d5b6000 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-202"></a>
### 202. N6 / ` output: add full HDR metadata to wlr_output_image_description `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_output.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` c80ad01a750072c5b40747fe9352cf846d5b6000 ` → ` e186207d74d6f5b7dfecb8b11179d816ef963f40 `。
  原证据引用：` 1db9e9e4cd41eb95fb4217ec823cb29b7af10a44 ` → ` c442691f263c156509e71a6fac0eac912061a175 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 019c13f41d3538924467c7ef1a3a34695a7ff255 ` 和原目标 ` 5291a2172bfdaa7b5bc6b5c047fffe9e4024e7d4 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` e186207d74d6f5b7dfecb8b11179d816ef963f40 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-203"></a>
### 203. N6 / ` backend/drm: relay full HDR metadata `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/drm/atomic.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` e186207d74d6f5b7dfecb8b11179d816ef963f40 ` → ` b0c600caaa63a74cb35ec9aa18139b3cd5ca3238 `。
  原证据引用：` c442691f263c156509e71a6fac0eac912061a175 ` → ` d20d87bcf1b7da6976bb58edbed41ee328582ac0 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 29ea403f65a802989dda25824ff9476dc7b77c12 ` 和原目标 ` bb27abcdcebbe2115f3edee0e236e3746b9aab18 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` b0c600caaa63a74cb35ec9aa18139b3cd5ca3238 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-204"></a>
### 204. N6 / ` render/egl: fix software rendering check `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/egl.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` b0c600caaa63a74cb35ec9aa18139b3cd5ca3238 ` → ` 0df9783ce06cf26251a2cd0fdafed53e94cd027b `。
  原证据引用：` d20d87bcf1b7da6976bb58edbed41ee328582ac0 ` → ` 3c5223d48bee39855ef774ce822d1ceef9b146f8 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` bd81e21bc6c1cab671d0594f0b41d28f38d1d1a6 ` 和原目标 ` a15fad0f35176ffea938ba75ee86383be93428a6 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 0df9783ce06cf26251a2cd0fdafed53e94cd027b `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-205"></a>
### 205. N6 / ` scene: Block damage on single-pixel buffer textures `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/surface.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 0df9783ce06cf26251a2cd0fdafed53e94cd027b ` → ` 7a9f068eb46fdae0e05b76987e463adc2f81432e `。
  原证据引用：` 3c5223d48bee39855ef774ce822d1ceef9b146f8 ` → ` 295067471966906cd88f3cb9fa2b71c6f550b738 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` e17a03422776f63782cc9ddeb94bdb879651adf8 ` 和原目标 ` 58745850aece14ce2d65ef262a9eeb5ba43c5781 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 7a9f068eb46fdae0e05b76987e463adc2f81432e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-206"></a>
### 206. N6 / ` scene: fix output transfer functions `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 7a9f068eb46fdae0e05b76987e463adc2f81432e ` → ` 6d04cea723d9b6c0a55114473f6c53c6d7a8eaa2 `。
  原证据引用：` 295067471966906cd88f3cb9fa2b71c6f550b738 ` → ` 630eb48af7c3277f5f35d1467d066859bd56ab22 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 08fb9384626292da9eefe05bbebdc57ba5f26517 ` 和原目标 ` 80845a1ccca777374343ddcc5e33d266d2c9d6f7 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 6d04cea723d9b6c0a55114473f6c53c6d7a8eaa2 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-207"></a>
### 207. N6 / ` wlr_text_input_v3: remove event arguments from header `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_text_input_v3.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 6d04cea723d9b6c0a55114473f6c53c6d7a8eaa2 ` → ` f2553656a8e7deaa66828da1f18c7c018dae29a3 `。
  原证据引用：` 630eb48af7c3277f5f35d1467d066859bd56ab22 ` → ` 505f341937f6d8d31457ba60069dcf050afb27fd `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 700447dfa49073a8cea8fdba86c929171a97bb2b ` 和原目标 ` b2689caca7876286ebe71d816c863d49fffcbcc8 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` f2553656a8e7deaa66828da1f18c7c018dae29a3 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-208"></a>
### 208. N6 / ` xdg-toplevel-tag-v1: new protocol `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_xdg_toplevel_tag_v1.h `、` 3rdparty/wlroots/protocol/meson.build `、` 3rdparty/wlroots/types/meson.build `、` 3rdparty/wlroots/types/wlr_xdg_toplevel_tag_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` f2553656a8e7deaa66828da1f18c7c018dae29a3 ` → ` 5f0a8190dd8f867773a3cc12c92da6c86078b8e5 `。
  原证据引用：` 505f341937f6d8d31457ba60069dcf050afb27fd ` → ` d4cb66d72bdf14ec87a3bc787acdfec5ef8b2d92 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` fa6c1816fc2d18e430fca57a5da9760e48c70a06 ` 和原目标 ` 8d7a225fbd14fafb3e3e293ea7d50cd726ee5f47 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 5f0a8190dd8f867773a3cc12c92da6c86078b8e5 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-209"></a>
### 209. N6 / ` transient_seat: initialize seat destroy listener `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_transient_seat_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 5f0a8190dd8f867773a3cc12c92da6c86078b8e5 ` → ` 97d914d7e8986469581a518c5da965ae3107c173 `。
  原证据引用：` d4cb66d72bdf14ec87a3bc787acdfec5ef8b2d92 ` → ` 84443cb2c2653bd27d98a11bc80e3b2cd1736fc6 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` b99faa4272d5b51540fa0ce6bcac13fb16dad171 ` 和原目标 ` ca3509624c0a02cf26139e8ce85969ec6f6e22ed ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 97d914d7e8986469581a518c5da965ae3107c173 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-210"></a>
### 210. N6 / ` render/vulkan: destroy vulkan instance when drm phdev mismatch `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/renderer.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 97d914d7e8986469581a518c5da965ae3107c173 ` → ` 81ca3fb1f7a4954d8afc1532c414c57b5517f446 `。
  原证据引用：` 84443cb2c2653bd27d98a11bc80e3b2cd1736fc6 ` → ` 40eba48d8f4c546fb7b2b68086b110f05d8a4bbb `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 8e41c92ee120806a59baf7347e9f13487e23bdd6 ` 和原目标 ` 650c164c1563142280439e6f49d9cce427fbd757 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 81ca3fb1f7a4954d8afc1532c414c57b5517f446 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-211"></a>
### 211. N6 / ` util/mem: Move memdup to new util/mem.c file `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/util/mem.h `、` 3rdparty/wlroots/types/wlr_color_management_v1.c `、` 3rdparty/wlroots/util/mem.c `、` 3rdparty/wlroots/util/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 81ca3fb1f7a4954d8afc1532c414c57b5517f446 ` → ` 84a155261cdb93a3321229fa6e8bd26fdaee844c `。
  原证据引用：` 40eba48d8f4c546fb7b2b68086b110f05d8a4bbb ` → ` 255e11dc2d2dea8a258c67f21e976a181e34c534 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 8b3fa373749ffd6da4b8500fca8883f43f171d1e ` 和原目标 ` 1028e37dafb2cc7afb9a24797ebe22554827c7c2 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 84a155261cdb93a3321229fa6e8bd26fdaee844c `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-212"></a>
### 212. N6 / ` color-representation-v1: new protocol `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_color_representation_v1.h `、` 3rdparty/wlroots/protocol/meson.build `、` 3rdparty/wlroots/types/meson.build `、` 3rdparty/wlroots/types/wlr_color_representation_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 84a155261cdb93a3321229fa6e8bd26fdaee844c ` → ` 9282b4493d988a85f3677ecc8724617916d652a9 `。
  原证据引用：` 255e11dc2d2dea8a258c67f21e976a181e34c534 ` → ` fea7929bfe8c43639be45fa900e13922ff4c2245 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 0202d8213967db6169f13fe42637fe9d35ab4d1f ` 和原目标 ` 5b24b13ab1e3cb60b65f38f8079c532b6b117b32 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 9282b4493d988a85f3677ecc8724617916d652a9 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-213"></a>
### 213. N6 / ` color-representation-v1: Add wlr enums + converters `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/render/color.h `、` 3rdparty/wlroots/include/wlr/types/wlr_color_representation_v1.h `、` 3rdparty/wlroots/types/wlr_color_representation_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 9282b4493d988a85f3677ecc8724617916d652a9 ` → ` ae8ea6321b69ae47b6496e6caee54c37aef378da `。
  原证据引用：` fea7929bfe8c43639be45fa900e13922ff4c2245 ` → ` df38a8207221f136710996014f96de6506b16025 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` b7e086318c74d3e39442fa3e30aa07ef1e0c7243 ` 和原目标 ` 0b3636dae88736821457528853b9c72228bbcf79 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` ae8ea6321b69ae47b6496e6caee54c37aef378da `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-214"></a>
### 214. N6 / ` types/color_representation: correctly cleanup in manager create `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_color_representation_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` ae8ea6321b69ae47b6496e6caee54c37aef378da ` → ` d25f38e861f611ac9510ac2f91bc9f7c9f72de4e `。
  原证据引用：` df38a8207221f136710996014f96de6506b16025 ` → ` 3303770f4fc3ca6d2d1cc6b2161939a1e0df326f `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 18b4d8410b7d8897e0d723a85a60a1782adeb8ca ` 和原目标 ` d1bf99b49991482a4343f3143161d7edfccd6302 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` d25f38e861f611ac9510ac2f91bc9f7c9f72de4e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-215"></a>
### 215. N6 / ` types/color_management: check on invalid image description `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` d25f38e861f611ac9510ac2f91bc9f7c9f72de4e ` → ` b0da0d1bd33e9bcfe9a9a2af6450c813a122a5ea `。
  原证据引用：` 3303770f4fc3ca6d2d1cc6b2161939a1e0df326f ` → ` 4d4257417a71ccf0713dbdf15284764dfeede308 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 6dfa30759182985cad9215e1a56df24098706961 ` 和原目标 ` 03c9faa0df437983742dd9e3588cb8e9ce1b29a5 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` b0da0d1bd33e9bcfe9a9a2af6450c813a122a5ea `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-216"></a>
### 216. N6 / ` ext-image-capture-source: output: Apply transform to cursor `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/ext_image_capture_source_v1/output.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` b0da0d1bd33e9bcfe9a9a2af6450c813a122a5ea ` → ` 7003e22532873bae6abc5503a44a3effbc07ad4c `。
  原证据引用：` 4d4257417a71ccf0713dbdf15284764dfeede308 ` → ` ec987bed0fb5b6ac72822355ac704aa94b1bbe94 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` c0ffefdd17ff771496458051a89686879768a182 ` 和原目标 ` 26fb1cbddc0d5bc6837a6ca8874d8b9d274542dd ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 7003e22532873bae6abc5503a44a3effbc07ad4c `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-217"></a>
### 217. N6 / ` cursor: update output cursor even if output is disabled `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_cursor.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 7003e22532873bae6abc5503a44a3effbc07ad4c ` → ` aec1dba58540647bd6f9c464f972980e2dae7a1b `。
  原证据引用：` ec987bed0fb5b6ac72822355ac704aa94b1bbe94 ` → ` 512813df914c640ffee3bdae69d10940c331c601 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 159aa593b87db474536c89b6cd75586fd0f88170 ` 和原目标 ` 2e82fceddb17a4734fd71e9dee701f2de81235df ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` aec1dba58540647bd6f9c464f972980e2dae7a1b `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-218"></a>
### 218. N6 / ` ext_image_capture_source_v1: remove unused struct definition `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/ext_image_capture_source_v1/foreign_toplevel.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` aec1dba58540647bd6f9c464f972980e2dae7a1b ` → ` c8d38f43582fc9e4d80f3706e8fdc10f9b0cb412 `。
  原证据引用：` 512813df914c640ffee3bdae69d10940c331c601 ` → ` 83a423d59ef7761c3f2a9b4cc4582b4288320e34 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d4e343cd04c5cbda3fe649b593cad22b41adff3c ` 和原目标 ` 133bacf82d265162b070e6145ca0f84949f423ff ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` c8d38f43582fc9e4d80f3706e8fdc10f9b0cb412 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-219"></a>
### 219. N6 / ` meson: bump minimum wayland-protocols version `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/protocol/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` c8d38f43582fc9e4d80f3706e8fdc10f9b0cb412 ` → ` fa511b48774bf85881c9e56ccc5794790a2fed80 `。
  原证据引用：` 83a423d59ef7761c3f2a9b4cc4582b4288320e34 ` → ` 37335dc2ea50b83b6380405b20bca832faf94dda `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` fcd0b60f3dbaef8e45ad1e2609811dfcd11c63b1 ` 和原目标 ` 5099363808eb469eccbbb6de9989292f6ccfec51 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` fa511b48774bf85881c9e56ccc5794790a2fed80 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-220"></a>
### 220. N6 / ` color_management_v1: add helpers to convert TF/primaries enums `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_color_management_v1.h `、` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` fa511b48774bf85881c9e56ccc5794790a2fed80 ` → ` 08f55f99d7604c9b38d3765534bbd508606e8104 `。
  原证据引用：` 37335dc2ea50b83b6380405b20bca832faf94dda ` → ` 83cbb6602a8647cb7eb6aef7f607c27bad19d9ad `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 094f8fa20e188f0da667df121b0eb9bb6f202ca2 ` 和原目标 ` 198224fa5373fbf69287b2cf9474a5da9cf62f1b ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 08f55f99d7604c9b38d3765534bbd508606e8104 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-221"></a>
### 221. N6 / ` scene: use helpers to convert TF/primaries enums `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/surface.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 08f55f99d7604c9b38d3765534bbd508606e8104 ` → ` 4e82e98bd185e695fbc76346d9423e4b722b61ba `。
  原证据引用：` 83cbb6602a8647cb7eb6aef7f607c27bad19d9ad ` → ` 5152415872d63670e09aa25f4389fccb6eb6f192 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` df2d519225b3fefb5c63cf6c9386b4f62c2defa2 ` 和原目标 ` b51774765e343765913d44cf08744e83118da7ab ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 4e82e98bd185e695fbc76346d9423e4b722b61ba `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-222"></a>
### 222. N6 / ` tinywl: fix cursor disappears when focused window is closed `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/tinywl/tinywl.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 4e82e98bd185e695fbc76346d9423e4b722b61ba ` → ` 6d801440ba08000a6c5ce20fdfa8cbf7947165d0 `。
  原证据引用：` 5152415872d63670e09aa25f4389fccb6eb6f192 ` → ` cf54921b2cfcece3a288ae931fa9400fab0577da `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 8ed92bbc78a136c4adb16182b38121ca5b44ed46 ` 和原目标 ` 1e72bdf6a9b6a268f07d877d0feb51bf2036c025 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 6d801440ba08000a6c5ce20fdfa8cbf7947165d0 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-223"></a>
### 223. N6 / ` color_management_v1: set output color properties `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 6d801440ba08000a6c5ce20fdfa8cbf7947165d0 ` → ` cbd5b931aa7bfa52ef032ef4b0b0886e459f0e7f `。
  原证据引用：` cf54921b2cfcece3a288ae931fa9400fab0577da ` → ` ad97f2a7e76791819024ac24e4dcd819f90253cf `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 5d2ed41d2be0afe22cd28ee05db3cd47305ca11a ` 和原目标 ` 09a4aaee3cb0e7ae702c50aa354c8a4f33d35bad ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` cbd5b931aa7bfa52ef032ef4b0b0886e459f0e7f `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-224"></a>
### 224. N6 / ` wlr_ext_data_control_v1: Make all listeners private `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_ext_data_control_v1.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` cbd5b931aa7bfa52ef032ef4b0b0886e459f0e7f ` → ` 355ff36497187bfec1f3a559ac580a209b515402 `。
  原证据引用：` ad97f2a7e76791819024ac24e4dcd819f90253cf ` → ` 6122a0d44b5df1d5dd5b5ea545640a5cc92f0f33 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` fa71f552d76b9565cc79f3a48768342f9186bd06 ` 和原目标 ` 86356b17add9571b013f11432f85b26131ad0498 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 355ff36497187bfec1f3a559ac580a209b515402 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-225"></a>
### 225. N6 / ` color-representation-v1: Fix missing destroy signal init `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_color_representation_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 355ff36497187bfec1f3a559ac580a209b515402 ` → ` 75464a16b00ef2c969fecff690387666ad5f2c29 `。
  原证据引用：` 6122a0d44b5df1d5dd5b5ea545640a5cc92f0f33 ` → ` c54870a6a4a2105f831a263d643a47b9b3d4fea9 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 33471be4c733a280bc804957c0bd307c07943e19 ` 和原目标 ` dac95d2b10afb94aeb04b6fb4d55e543b00248ca ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 75464a16b00ef2c969fecff690387666ad5f2c29 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-226"></a>
### 226. N6 / ` ext_image_capture_source_v1: advertise fallback {A,X}RGB8888 formats `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/ext_image_capture_source_v1/base.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 75464a16b00ef2c969fecff690387666ad5f2c29 ` → ` d53987b3cc12cda460076d77e38f65566925faf7 `。
  原证据引用：` c54870a6a4a2105f831a263d643a47b9b3d4fea9 ` → ` 27ea05296e44507a0fd9d1f64322e8bba4c94f7a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 682273cf854842c378362d2e167785898b256806 ` 和原目标 ` 560b8f3544a7fd40fbd0ecbcc0d841259254e841 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` d53987b3cc12cda460076d77e38f65566925faf7 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-227"></a>
### 227. N6 / ` output/cursor: Fix double cursor bug `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/output/cursor.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` d53987b3cc12cda460076d77e38f65566925faf7 ` → ` 207de72a7ac63ed3d6679285f55efddf7265e27a `。
  原证据引用：` 27ea05296e44507a0fd9d1f64322e8bba4c94f7a ` → ` c5379333c311c9630453391ec0e9869a5bbfa22f `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 74da40725dca4808b943e17d5bce82b9ce87f6b3 ` 和原目标 ` cefde07377a32b323fd2a6d71e52fbdc6de13d29 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 207de72a7ac63ed3d6679285f55efddf7265e27a `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-228"></a>
### 228. N6 / ` backend, output: send commit events after applying all in wlr_backend_commit() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/backend.c `、` 3rdparty/wlroots/include/types/wlr_output.h `、` 3rdparty/wlroots/types/output/output.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 207de72a7ac63ed3d6679285f55efddf7265e27a ` → ` 5a6abec15362153665bd67862f21afd0d67f9689 `。
  原证据引用：` c5379333c311c9630453391ec0e9869a5bbfa22f ` → ` 0ad3139584c534aeaddb4a1bf255d1f17e7ae018 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` e9490f064a03e6c201149528e6c0c4c72f10ab86 ` 和原目标 ` c14a456fb58697ad201bce67aeace869b3f881a0 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 5a6abec15362153665bd67862f21afd0d67f9689 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-229"></a>
### 229. N6 / ` fixes: add implementation `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_fixes.h `、` 3rdparty/wlroots/meson.build `、` 3rdparty/wlroots/types/meson.build `、` 3rdparty/wlroots/types/wlr_fixes.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 5a6abec15362153665bd67862f21afd0d67f9689 ` → ` 43b5a31e199601a405466a71dbe6f0cc8c7275b0 `。
  原证据引用：` 0ad3139584c534aeaddb4a1bf255d1f17e7ae018 ` → ` 255d487493af28800c16f54e732431af3aa26bdf `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 5c5b0af13756a49fd922031a621465f01b73d7e6 ` 和原目标 ` f7a1cc685d2a3782fd954580e50506773f316227 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 43b5a31e199601a405466a71dbe6f0cc8c7275b0 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-230"></a>
### 230. N6 / ` Avoid including generated headers publicly where possible `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_color_management_v1.h `、` 3rdparty/wlroots/include/wlr/types/wlr_color_representation_v1.h `、` 3rdparty/wlroots/include/wlr/types/wlr_content_type_v1.h `、` 3rdparty/wlroots/include/wlr/types/wlr_cursor_shape_v1.h `、` 3rdparty/wlroots/include/wlr/types/wlr_ext_image_copy_capture_v1.h `、` 3rdparty/wlroots/include/wlr/types/wlr_pointer_constraints_v1.h `、` 3rdparty/wlroots/include/wlr/types/wlr_tablet_v2.h `、` 3rdparty/wlroots/include/wlr/types/wlr_tearing_control_v1.h `、` 3rdparty/wlroots/include/wlr/types/wlr_xdg_shell.h `、` 3rdparty/wlroots/types/wlr_color_management_v1.c `、` 3rdparty/wlroots/types/wlr_content_type_v1.c `、` 3rdparty/wlroots/types/wlr_cursor_shape_v1.c `、` 3rdparty/wlroots/types/wlr_ext_image_copy_capture_v1.c `、` 3rdparty/wlroots/types/wlr_pointer_constraints_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 43b5a31e199601a405466a71dbe6f0cc8c7275b0 ` → ` 52077be289830311108a826c56ada2f6e940bbef `。
  原证据引用：` 255d487493af28800c16f54e732431af3aa26bdf ` → ` d1c54c851b469ed0dd1cc8d0a0bb70c31edfcf14 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d42414caafb7b6627440a0665d371210c0d47e7a ` 和原目标 ` 6364d3ad0fab19fa96ab0a9134cd40e10ca9356d ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 52077be289830311108a826c56ada2f6e940bbef `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-231"></a>
### 231. N6 / ` compositor: use wl_resource_post_error_vargs() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_compositor.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 52077be289830311108a826c56ada2f6e940bbef ` → ` 6f1ce42117835db68569446a31295d8e70e20503 `。
  原证据引用：` d1c54c851b469ed0dd1cc8d0a0bb70c31edfcf14 ` → ` 735774f7062d42b8886c63dd144674c12f4b249b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 859718dc888c11841a8a460349ad5748c121e3e8 ` 和原目标 ` 706564050ea892b967666d7a96a60532b5adc230 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 6f1ce42117835db68569446a31295d8e70e20503 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-232"></a>
### 232. N6 / ` color-management-v1: handle inert outputs in get_output `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 6f1ce42117835db68569446a31295d8e70e20503 ` → ` 270ac33c71f018031c51070a6ecc55feacc80fa7 `。
  原证据引用：` 735774f7062d42b8886c63dd144674c12f4b249b ` → ` db39a0807bfe4b8269c0de2298bb1e97783e9bed `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 87d58d55d9bbd55f89c667abb8641b707fc593d5 ` 和原目标 ` efb318004042fd6921f1fb46d9c315c8a698c261 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 270ac33c71f018031c51070a6ecc55feacc80fa7 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-233"></a>
### 233. N6 / ` render/allocator/gbm: insert buffer after export gbm bo `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/allocator/gbm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 270ac33c71f018031c51070a6ecc55feacc80fa7 ` → ` f0fda0d94cd9e3cb5a628d634040db2dc8d2afe8 `。
  原证据引用：` db39a0807bfe4b8269c0de2298bb1e97783e9bed ` → ` 94d605647f80a638793accdc03f27c371bacca5f `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ee0d9a7de7b275592767c8c3429b4fe472f79e20 ` 和原目标 ` 4668a87a562c6b31e40d91bb0ad84fa959fb1893 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` f0fda0d94cd9e3cb5a628d634040db2dc8d2afe8 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-234"></a>
### 234. N6 / ` wlr_xdg_toplevel_icon_v1: check the correct resource `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_xdg_toplevel_icon_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` f0fda0d94cd9e3cb5a628d634040db2dc8d2afe8 ` → ` c28297bb0f778d1da5579c04ee89e5650931a7c8 `。
  原证据引用：` 94d605647f80a638793accdc03f27c371bacca5f ` → ` c983e6f2c19bcb48eeb36cc9bfaf93bc4e7bfce9 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 73caa1c03a8b26eec23a253152f3ae893ff6d85f ` 和原目标 ` 0e0d387031a7b095dd478276381ceed97f4b9e22 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` c28297bb0f778d1da5579c04ee89e5650931a7c8 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-235"></a>
### 235. N6 / ` tinywl: stop generating xdg-shell header `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/tinywl/Makefile `、` 3rdparty/wlroots/tinywl/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` c28297bb0f778d1da5579c04ee89e5650931a7c8 ` → ` 213c86cfb38ed8cca146b53c99abf9aa376a49dc `。
  原证据引用：` c983e6f2c19bcb48eeb36cc9bfaf93bc4e7bfce9 ` → ` 3bfeaa6f61185af3216ca3fbd07e6e3bc277857d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 033a7c7b4278b88eec561d97307b111a7bbc0c06 ` 和原目标 ` b11be642ce1573c35db03b3f7465da3aa7ee53d3 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 213c86cfb38ed8cca146b53c99abf9aa376a49dc `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-236"></a>
### 236. N6 / ` render/vulkan: fix VkPushConstantRange for wlr_vk_frag_texture_pcr_data `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/renderer.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 213c86cfb38ed8cca146b53c99abf9aa376a49dc ` → ` 84f2c44e3950187ce7ae08497a4e47edff613c6e `。
  原证据引用：` 3bfeaa6f61185af3216ca3fbd07e6e3bc277857d ` → ` 38313286cb2f0cdbb686b5b9d1e0f82562066381 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` aa980f02c6e0e119ab271141fa42adecfae48707 ` 和原目标 ` df946859c39247dca0e495451f344677ff3f2a9c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 84f2c44e3950187ce7ae08497a4e47edff613c6e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-237"></a>
### 237. N6 / ` render/vulkan: remove hardcoded counts `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/renderer.c `、` 3rdparty/wlroots/render/vulkan/texture.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 84f2c44e3950187ce7ae08497a4e47edff613c6e ` → ` f6ec46993c371cb47f3934c62da700500b4138a6 `。
  原证据引用：` 38313286cb2f0cdbb686b5b9d1e0f82562066381 ` → ` 8f27778fb594600be4cf98e218df5d56fadae940 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d4dfa7caab388a3c682d86be0aad378851f7363d ` 和原目标 ` 548d7fab8e70439d3fd8bcae8b2634d03e7ae8f8 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` f6ec46993c371cb47f3934c62da700500b4138a6 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-238"></a>
### 238. N6 / ` docs: deprecate legacy wlr_data_control_v1 interface `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_data_control_v1.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` f6ec46993c371cb47f3934c62da700500b4138a6 ` → ` f7c51f3da40e01bd91fcbc17b99917d2d326f4b6 `。
  原证据引用：` 8f27778fb594600be4cf98e218df5d56fadae940 ` → ` ac80308713fa8b514efb32197a4b9ad56c74dd68 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` fe8906bcfbf6eb65d0c68669ffd177efe282f178 ` 和原目标 ` 017abc234dc80b17296492fd3ce5f80aa236064b ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` f7c51f3da40e01bd91fcbc17b99917d2d326f4b6 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-239"></a>
### 239. N6 / ` build: add wayland-protocols to dependencies array `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/protocol/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` f7c51f3da40e01bd91fcbc17b99917d2d326f4b6 ` → ` 992e0e3037cb52c3a26fe2f70abb7024cba4d3bc `。
  原证据引用：` ac80308713fa8b514efb32197a4b9ad56c74dd68 ` → ` 4c94a790857b65e9cbb5ead713ec591c4e2d35ec `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 5ffc9a8b7bf68b5da60ef9f6cdd52bca9e8e1a6c ` 和原目标 ` 8bc3019747ecb4af5ec2c8bf67ed2432a90f2ef3 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 992e0e3037cb52c3a26fe2f70abb7024cba4d3bc `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-240"></a>
### 240. N6 / ` types: deprecate wlr-screencopy-unstable-v1 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_screencopy_v1.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 992e0e3037cb52c3a26fe2f70abb7024cba4d3bc ` → ` 131816ddbf3d916392724072867f23b09eaeb53c `。
  原证据引用：` 4c94a790857b65e9cbb5ead713ec591c4e2d35ec ` → ` 6d67edafbc0dd0e5fbaf3fdcf702e94da9a33684 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 9cad8d729fd3550040a7ece3fe2d4cfafd67e5b6 ` 和原目标 ` d356a4d5f73f39e676d12259f1f4fd1c57d48c08 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 131816ddbf3d916392724072867f23b09eaeb53c `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-241"></a>
### 241. N6 / ` drm-lease-v1: remove connector active_lease & lease connectors `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_drm_lease_v1.h `、` 3rdparty/wlroots/types/wlr_drm_lease_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 131816ddbf3d916392724072867f23b09eaeb53c ` → ` f4d2de93826105c418c3f63a1495159205f6288d `。
  原证据引用：` 6d67edafbc0dd0e5fbaf3fdcf702e94da9a33684 ` → ` 0beec9fd2bfd2778054a29dd0a1aacbee949d80c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` c7439c3833d0cd35720a5d229617602e5ba5fcb1 ` 和原目标 ` 2b66404a35c673e4e0b72a6a7280a261d01bf89c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` f4d2de93826105c418c3f63a1495159205f6288d `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-242"></a>
### 242. N6 / ` input-method: rename input_method event to new_input_method `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_input_method_v2.h `、` 3rdparty/wlroots/types/wlr_input_method_v2.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` f4d2de93826105c418c3f63a1495159205f6288d ` → ` 22bf9654c48451a2119a6cb90f1b92d54eb04cf4 `。
  原证据引用：` 0beec9fd2bfd2778054a29dd0a1aacbee949d80c ` → ` 3c44f2c16a20e94419b7714f4a728cd5e525988c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 45194c916e691c9228f30d87085da35052b75a72 ` 和原目标 ` 6015296a9f0dd854516a0a6f9625eca98aa4d000 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 22bf9654c48451a2119a6cb90f1b92d54eb04cf4 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-243"></a>
### 243. N6 / `` input-method: use `NULL` when emitting signals ``

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_input_method_v2.h `、` 3rdparty/wlroots/types/wlr_input_method_v2.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 22bf9654c48451a2119a6cb90f1b92d54eb04cf4 ` → ` 93dc16bd5d14c31e139ea54a30f067890d24dce3 `。
  原证据引用：` 3c44f2c16a20e94419b7714f4a728cd5e525988c ` → ` a3fd28122b984e932256090d5cb6cd39f8a886f1 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 908ba59932df7cbe837af6280a6de083abcb69c6 ` 和原目标 ` 23d9af69508fed3a13d659c7b1c0b584999fb4a7 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 93dc16bd5d14c31e139ea54a30f067890d24dce3 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-244"></a>
### 244. N6 / ` color-representation-v1: Actually set supported_*_len `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_color_representation_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 93dc16bd5d14c31e139ea54a30f067890d24dce3 ` → ` e5d2f2ceff3bbdb497c1ffa1f045887d9f09f859 `。
  原证据引用：` a3fd28122b984e932256090d5cb6cd39f8a886f1 ` → ` 0b8ddc517c64cd19d2d73409343d80f89186ae5d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 564a3ca2e2e219480b75df745aa61aa706ec6e19 ` 和原目标 ` 19c3c8cb3a8b957feb1b4524ffdac78c8ffa10d2 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` e5d2f2ceff3bbdb497c1ffa1f045887d9f09f859 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-245"></a>
### 245. N6 / ` protocols: sync with wlr-protocols, apply non-breaking updates and doc improvements `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/protocol/wlr-export-dmabuf-unstable-v1.xml `、` 3rdparty/wlroots/protocol/wlr-foreign-toplevel-management-unstable-v1.xml `、` 3rdparty/wlroots/protocol/wlr-gamma-control-unstable-v1.xml `、` 3rdparty/wlroots/protocol/wlr-output-management-unstable-v1.xml `、` 3rdparty/wlroots/protocol/wlr-output-power-management-unstable-v1.xml `、` 3rdparty/wlroots/protocol/wlr-screencopy-unstable-v1.xml `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` e5d2f2ceff3bbdb497c1ffa1f045887d9f09f859 ` → ` 79859f208cc35ae14f77154299648d241a4d434e `。
  原证据引用：` 0b8ddc517c64cd19d2d73409343d80f89186ae5d ` → ` 54cc1ebfc617551c0df45d0670381ea657aad4fd `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 2b85c5d40accb13fc3acb33fdca64bc795e7c74b ` 和原目标 ` 35b27a483a490f8fd15d81e377ee7626f8990367 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 79859f208cc35ae14f77154299648d241a4d434e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-246"></a>
### 246. N6 / ` drm_lease_v1: initialize device resource link during abnormal exit `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_drm_lease_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 79859f208cc35ae14f77154299648d241a4d434e ` → ` 5ea44aa3760578c8b8005c7d286ef8cafecf140a `。
  原证据引用：` 54cc1ebfc617551c0df45d0670381ea657aad4fd ` → ` a72f14ead3d638724c1243d4f484340674fb26f2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 276ea2949d7d0b42e6d9a28f186c378293cae922 ` 和原目标 ` cd7ee22d3e370ccb18a393155c6d607cfced71c8 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 5ea44aa3760578c8b8005c7d286ef8cafecf140a `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-247"></a>
### 247. N6 / ` output/cursor: fix missing second cursor `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/output/cursor.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 5ea44aa3760578c8b8005c7d286ef8cafecf140a ` → ` 38dc201b0aa73c51916a3f977fb0176febed9565 `。
  原证据引用：` a72f14ead3d638724c1243d4f484340674fb26f2 ` → ` 86f7f4a88490878eeca920043298b23f6f6e89a3 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` c4c3d95a38040104339e8ed8984b847290df294d ` 和原目标 ` faab1a2428f418efd050ce63b6c8829ac503a0a1 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 38dc201b0aa73c51916a3f977fb0176febed9565 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-248"></a>
### 248. N6 / ` scene/surface: simplify single-pixel-buffer check in surface_reconfigure() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/surface.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 38dc201b0aa73c51916a3f977fb0176febed9565 ` → ` bf286154e1ac36dc0fd87dbfe1f0433cdde97460 `。
  原证据引用：` 86f7f4a88490878eeca920043298b23f6f6e89a3 ` → ` 245c3d0c2131b1b6d138f6ccbace8448d4aae1e9 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` f827a249077f26ad91928b581d3fc5a96af3ec01 ` 和原目标 ` f515abf21a171f14f7ff552c6f4e09b2696696d0 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` bf286154e1ac36dc0fd87dbfe1f0433cdde97460 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-249"></a>
### 249. N6 / ` scene/surface: fix NULL deref when source buffer is destroyed `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/surface.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` bf286154e1ac36dc0fd87dbfe1f0433cdde97460 ` → ` 8825cedba02e42433fcea115c16394ddd1f8e279 `。
  原证据引用：` 245c3d0c2131b1b6d138f6ccbace8448d4aae1e9 ` → ` 3fbdf7d9068eb0d49cf9c552879b94d2d9faaa8e `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` f23cb2387656aab8d243c8814a53da6c0a70db48 ` 和原目标 ` 04955a3751b48cc1349f0f3dbea7b12a2ea96439 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 8825cedba02e42433fcea115c16394ddd1f8e279 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-250"></a>
### 250. N6 / ` cursor: use source buffer to signal release timeline point `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_cursor.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 8825cedba02e42433fcea115c16394ddd1f8e279 ` → ` 0885a43c202cb47c66e2bb6d0507c8a9e0deb9bb `。
  原证据引用：` 3fbdf7d9068eb0d49cf9c552879b94d2d9faaa8e ` → ` 7b7f276e65ed9176774ae57e5bcd65dfc44e1091 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 5b8b45b08e13328031c464d9913eef55e39c91d0 ` 和原目标 ` c1f7a7e99fa20e3680df36ede7e390e99869cfce ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 0885a43c202cb47c66e2bb6d0507c8a9e0deb9bb `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-251"></a>
### 251. N6 / ` xwayland: fix assertion failure in wlr_xwayland_shell_v1 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/xwayland.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 0885a43c202cb47c66e2bb6d0507c8a9e0deb9bb ` → ` 0d6a6dc13d229a903cd9fa7efbf6941d64e6e76a `。
  原证据引用：` 7b7f276e65ed9176774ae57e5bcd65dfc44e1091 ` → ` a3ba725bfe8f6776293e7ac51297e9ecba2c47ae `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 529950cb158ad7a02c6ac3a446fac29d87028ab3 ` 和原目标 ` 4537a4e3367eb34a4863346f6d2b3958a695e65c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 0d6a6dc13d229a903cd9fa7efbf6941d64e6e76a `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-252"></a>
### 252. N6 / ` render/vulkan: Handle multi-descriptor sets `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/renderer.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 0d6a6dc13d229a903cd9fa7efbf6941d64e6e76a ` → ` 0416c53f21b0260f1190c9ac939522197b15f05a `。
  原证据引用：` a3ba725bfe8f6776293e7ac51297e9ecba2c47ae ` → ` c4594d98268350bdd3a264687eaf2ec477e8088c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 93864b26690744c7b9f9eba8d128acde6e98b379 ` 和原目标 ` 06192bc5e3e9a8319080330d5fb38c21b5003691 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 0416c53f21b0260f1190c9ac939522197b15f05a `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-253"></a>
### 253. N6 / ` render/vulkan: rename plain to two_pass `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/renderer.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 0416c53f21b0260f1190c9ac939522197b15f05a ` → ` 18355498eb03ccf45b041a600345096bd7980724 `。
  原证据引用：` c4594d98268350bdd3a264687eaf2ec477e8088c ` → ` ff1547c2a7cd3f8a3ce19fd6c5215a2eea852470 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 6e63017817a6ce37cc822f527ba57ac222e9d2c7 ` 和原目标 ` dbb8677b6d41c38f2dd55c115a0844b104d3cc42 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 18355498eb03ccf45b041a600345096bd7980724 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-254"></a>
### 254. N6 / ` render/vulkan: use sRGB image view when color transform is set `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 18355498eb03ccf45b041a600345096bd7980724 ` → ` 297e4347f2132dafcbc29923a5028fd4d88ef638 `。
  原证据引用：` ff1547c2a7cd3f8a3ce19fd6c5215a2eea852470 ` → ` ce5d2e79b5eaeebcef0e694cd9afa325382f7328 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 8b61f805d33f81a7afe2a18c336867fc32b8620a ` 和原目标 ` 12d443c072c1aeb2301b324fe6668133cf744e7f ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 297e4347f2132dafcbc29923a5028fd4d88ef638 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-255"></a>
### 255. N6 / ` render/vulkan: rename vulkan_setup_srgb_framebuffer() for linear `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/renderer.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 297e4347f2132dafcbc29923a5028fd4d88ef638 ` → ` ed6fda898a58eba5e183eb0d8df87d2f73295b4a `。
  原证据引用：` ce5d2e79b5eaeebcef0e694cd9afa325382f7328 ` → ` a59c3078306c25bf394eb00674cca481ea33da53 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` b7b7012f449273e29486ebdc9a4eddd5e76ec7af ` 和原目标 ` 271b43b49b3cd62e2d8d977609b5866c1967f353 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` ed6fda898a58eba5e183eb0d8df87d2f73295b4a `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-256"></a>
### 256. N6 / ` render/vulkan: introduce wlr_vk_render_buffer_out `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/renderer.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` ed6fda898a58eba5e183eb0d8df87d2f73295b4a ` → ` 3a51987fb30ee8322729f534a9b9d409dd69f433 `。
  原证据引用：` a59c3078306c25bf394eb00674cca481ea33da53 ` → ` 4d34886e98057e8efade91bbb6e66da6007fe8be `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 86dbbae0f5f21fe7220137c59ba76d385399dc58 ` 和原目标 ` fde7240b44c69dd2211e13e0f97dd58803ea4dba ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 3a51987fb30ee8322729f534a9b9d409dd69f433 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-257"></a>
### 257. N6 / ` render/vulkan: add wlr_vk_render_pass.render_setup `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 3a51987fb30ee8322729f534a9b9d409dd69f433 ` → ` e357f578069b444576d025ab338d9f0d5a7c6c17 `。
  原证据引用：` 4d34886e98057e8efade91bbb6e66da6007fe8be ` → ` f7c73e944853dfcb00631c04d726975a0ac1f532 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 6dc50b9db882b034646f79db6fc49914f5fb40d1 ` 和原目标 ` f383ab3899733ead50241f4bc3df8e17c66f08dc ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` e357f578069b444576d025ab338d9f0d5a7c6c17 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-258"></a>
### 258. N6 / ` render/vulkan: add wlr_vk_render_pass.render_buffer_out `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` e357f578069b444576d025ab338d9f0d5a7c6c17 ` → ` 6a813b463cb523693c617f2e8dc159e4b36374fa `。
  原证据引用：` f7c73e944853dfcb00631c04d726975a0ac1f532 ` → ` 58872f39769740cc784e37d80aeb7e745eca86d0 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` f02da149ffd4c801ab386b93f01061eec6eea06b ` 和原目标 ` a12c8468fbf4317289d2ed44e4c54ee767cc9b2c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 6a813b463cb523693c617f2e8dc159e4b36374fa `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-259"></a>
### 259. N6 / ` render/vulkan: replace wlr_vk_render_pass.srgb_pathway with two_pass `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 6a813b463cb523693c617f2e8dc159e4b36374fa ` → ` 6245192f7b22a26d401356c96cf02f1cdcc979ee `。
  原证据引用：` 58872f39769740cc784e37d80aeb7e745eca86d0 ` → ` 638b0db58146d07990785d434cdfb2ea70a307e8 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 34dc93862257c1c9f69958379fd8d1e8b75e5461 ` 和原目标 ` de1fe1cad703f37235073f94b8fbedee54b2ed1e ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 6245192f7b22a26d401356c96cf02f1cdcc979ee `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-260"></a>
### 260. N6 / ` render/vulkan: add linear single-subpass `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/renderer.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 6245192f7b22a26d401356c96cf02f1cdcc979ee ` → ` 5bd77933cbc88578fecbf45dd7ec470261472209 `。
  原证据引用：` 638b0db58146d07990785d434cdfb2ea70a307e8 ` → ` 1e043e87e6ec146503757cefe8869be88ea99cd0 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 950bbb8fe1b23fa77e0953d40d76cfaf46f0d92f ` 和原目标 ` 0a291d0073380a993493c8d8b93cb1c11661ecbb ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 5bd77933cbc88578fecbf45dd7ec470261472209 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-261"></a>
### 261. N6 / ` wlr_drag: drag motion signal also needs to be sent `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/data_device/wlr_drag.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 5bd77933cbc88578fecbf45dd7ec470261472209 ` → ` d559a98555de64f0a6d4c8f2c75864355b78f775 `。
  原证据引用：` 1e043e87e6ec146503757cefe8869be88ea99cd0 ` → ` bce6ec5113af1d3f61f9bec9d1716dd8b73b39ab `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 75c10a1391360aa29920a801f59ff7461912d6aa ` 和原目标 ` 4aa4e2d0d036427fedd039834e4a4fc5e6c1b571 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` d559a98555de64f0a6d4c8f2c75864355b78f775 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-262"></a>
### 262. N6 / ` Add release script `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/release.sh `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` d559a98555de64f0a6d4c8f2c75864355b78f775 ` → ` 7156339346e4fcf4d4b94e54df4f8539d869d52f `。
  原证据引用：` bce6ec5113af1d3f61f9bec9d1716dd8b73b39ab ` → ` 29706cdf213c8aaa699bf0ded75ad8066fb0b796 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 635bf146b865db63416f82bd6092442de594f507 ` 和原目标 ` bb292724b9b9ee07ae376c4dc1b889c0c56ce1bc ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 7156339346e4fcf4d4b94e54df4f8539d869d52f `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-263"></a>
### 263. N6 / ` color_management_v1: drop duplicated enum converters `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 7156339346e4fcf4d4b94e54df4f8539d869d52f ` → ` dd74beaaf72de68d11e5f300866dfceae80c984b `。
  原证据引用：` 29706cdf213c8aaa699bf0ded75ad8066fb0b796 ` → ` 9475851a2a60521eef5043019f5ae2d0b871a7a5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 8e64fba9494a4dc8c2c9845a2c2724c7632b81a4 ` 和原目标 ` 363db0dbc2fb20224ea7a2e5ad3230bc1dabd5ec ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` dd74beaaf72de68d11e5f300866dfceae80c984b `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-264"></a>
### 264. N6 / ` color_management_v1: make from_wlr enum converters public `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_color_management_v1.h `、` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` dd74beaaf72de68d11e5f300866dfceae80c984b ` → ` 96629037052b4153632ccd854c0971a6556eae7f `。
  原证据引用：` 9475851a2a60521eef5043019f5ae2d0b871a7a5 ` → ` ab3ff3155d3f88be9f00515a562ace463c4193a7 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` a378e058a4bd3bc87edf943504258c76f668ed9b ` 和原目标 ` ca431b96f84283bd1ce7fb9767c745e3e557c9c5 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 96629037052b4153632ccd854c0971a6556eae7f `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-265"></a>
### 265. N6 / ` color_management_v1: add destroy event to manager `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_color_management_v1.h `、` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 96629037052b4153632ccd854c0971a6556eae7f ` → ` 3a2014ff56481ec91bc47b76f152b1bd9612bb6f `。
  原证据引用：` ab3ff3155d3f88be9f00515a562ace463c4193a7 ` → ` aebe5b083205c86a52532454f52c0aaf56ddf902 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 263e98177d78628e1aeb6d90dd9e0598db87454b ` 和原目标 ` 7af02bfd16484d40303240387041c62747fc8fdd ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 3a2014ff56481ec91bc47b76f152b1bd9612bb6f `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-266"></a>
### 266. N6 / ` scene: send color_management_v1 surface feedback `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_scene.h `、` 3rdparty/wlroots/types/scene/surface.c `、` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 3a2014ff56481ec91bc47b76f152b1bd9612bb6f ` → ` 4e6ea4f8ce63556b27246df5bf22cc7c13a36769 `。
  原证据引用：` aebe5b083205c86a52532454f52c0aaf56ddf902 ` → ` 7f9b603040163279eaae6f2d9e9e6aa30a299ffb `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 437174b43a3832b1d812eb88af1f716d748197b1 ` 和原目标 ` 953d859137c5e8d98723f7f5c187e693ff92bc31 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 4e6ea4f8ce63556b27246df5bf22cc7c13a36769 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-267"></a>
### 267. N6 / ` render/color: fix bounds check in lut_1d_get() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/color.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 4e6ea4f8ce63556b27246df5bf22cc7c13a36769 ` → ` 166e06180f2967780b2819f302e1a7eb82afcea6 `。
  原证据引用：` 7f9b603040163279eaae6f2d9e9e6aa30a299ffb ` → ` d34d8520a8ac9192ae882afd90432e99ca8e7427 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 505329bf071892244a4e8b80e8595429f68230c8 ` 和原目标 ` 358693ffe243d50b6a849f2c830a2f3ef83c8076 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 166e06180f2967780b2819f302e1a7eb82afcea6 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-268"></a>
### 268. N6 / ` backend/wayland: log when getting disconnected from remote display `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/wayland/backend.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 166e06180f2967780b2819f302e1a7eb82afcea6 ` → ` e83df8a497421a736d787db7bc0bc5eed0f64843 `。
  原证据引用：` d34d8520a8ac9192ae882afd90432e99ca8e7427 ` → ` 4a7c08161fed07b7cf4f583b4774d5434a067098 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 91921354b90f4eeadd031b2baaeeba95e9996644 ` 和原目标 ` 69e81d1c6a1a275f956fbe617afc34133f17176e ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` e83df8a497421a736d787db7bc0bc5eed0f64843 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-269"></a>
### 269. N6 / ` backend/wayland: continue reading on hangup `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/wayland/backend.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` e83df8a497421a736d787db7bc0bc5eed0f64843 ` → ` ee0cd79c9ae51e6a75c60dc2e71c693ea82877b9 `。
  原证据引用：` 4a7c08161fed07b7cf4f583b4774d5434a067098 ` → ` ec0c5a6454025e942d1dab727090ced8e485262d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` b66698bab2ac579ad52fb40e3438a45110f104c4 ` 和原目标 ` fb6f8c5eb6cf0485b308f28514dc8625a1c92e4d ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` ee0cd79c9ae51e6a75c60dc2e71c693ea82877b9 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-270"></a>
### 270. N6 / ` backend/drm: avoid error message when EDID is missing `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/drm/drm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` ee0cd79c9ae51e6a75c60dc2e71c693ea82877b9 ` → ` a63c6b131122f91f85792cdbf9fe462d0d842ae5 `。
  原证据引用：` ec0c5a6454025e942d1dab727090ced8e485262d ` → ` 5616e031674c4328473e3bcbd499152cf676deac `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 52382ecfe26abb0987212c5d019770cfd29a38cf ` 和原目标 ` 45993b851fe4f299636492faa00b4d52566d982c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` a63c6b131122f91f85792cdbf9fe462d0d842ae5 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-271"></a>
### 271. N6 / ` backend/session: fix crash on udev device remove event `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/session/session.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` a63c6b131122f91f85792cdbf9fe462d0d842ae5 ` → ` 9a32885b7ad23c656e7ac06cde6301869f1d4c91 `。
  原证据引用：` 5616e031674c4328473e3bcbd499152cf676deac ` → ` 35be5103a38fc87995ab0978592ed0d29f1918f7 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 4353caeb24222b3e9a9862997814d794ae00b94d ` 和原目标 ` 1c859bdc13f2316ebd952deab4a47a3ea19d8f3d ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 9a32885b7ad23c656e7ac06cde6301869f1d4c91 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-272"></a>
### 272. N6 / ` wlr_scene: fix tf/prim comparison for scanout attempt `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 9a32885b7ad23c656e7ac06cde6301869f1d4c91 ` → ` c864484bcc89dfaa353a1d2cc41cb4baec75f8f2 `。
  原证据引用：` 35be5103a38fc87995ab0978592ed0d29f1918f7 ` → ` c6a5860a50f7a539b247732ecc194b204400ca5f `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 7b7c401f960cb323ac70ba3b3523f3f0df15970a ` 和原目标 ` d8bdfbfbe64aa43bfe5049be719d30d1c8686abe ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` c864484bcc89dfaa353a1d2cc41cb4baec75f8f2 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-273"></a>
### 273. N6 / ` wlr_scene: return scene_direct_scanout_result instead of bool `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` c864484bcc89dfaa353a1d2cc41cb4baec75f8f2 ` → ` 3ff70cf762ec20ef48183210b85aaf1143d4829f `。
  原证据引用：` c6a5860a50f7a539b247732ecc194b204400ca5f ` → ` a2a5005855607fed13c9012e7d0d4f06733b0e51 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ab94ac3465ed64e79b82c0c33bebc84c650d9d4c ` 和原目标 ` 2d74f0462ad2a194b214c69092a1ba1dbfae4068 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 3ff70cf762ec20ef48183210b85aaf1143d4829f `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-274"></a>
### 274. N6 / ` Revert "wlr_scene: fix tf/prim comparison for scanout attempt" `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 3ff70cf762ec20ef48183210b85aaf1143d4829f ` → ` b75ab00a0c5166e22bc32d4714628da29b1a1c01 `。
  原证据引用：` a2a5005855607fed13c9012e7d0d4f06733b0e51 ` → ` 333ceace41e49e0ff23dd859cc290657c2717793 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 8cb8af048a6aab2dfe8e972ebbac757d18952ebf ` 和原目标 ` 5af00710987f3bbf1a87899178684f0dc4f67c3d ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` b75ab00a0c5166e22bc32d4714628da29b1a1c01 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-275"></a>
### 275. N6 / ` render: introduce Gamma 2.2 color transform `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/drm/atomic.c `、` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/include/wlr/render/color.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/renderer.c `、` 3rdparty/wlroots/render/vulkan/shaders/output.frag `、` 3rdparty/wlroots/render/vulkan/shaders/texture.frag `、` 3rdparty/wlroots/types/scene/surface.c `、` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` b75ab00a0c5166e22bc32d4714628da29b1a1c01 ` → ` 329020b96a1c580f64cdb16b615eb02b015baddf `。
  原证据引用：` 333ceace41e49e0ff23dd859cc290657c2717793 ` → ` 39ee5addc607aa03dbe9ee9852f7bfc87e4ad5db `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` de8a45ad87af71675c2d1e8bdff0b84578e4afe2 ` 和原目标 ` e464c31b6b7c85653173a02f6472cc4264de585f ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 329020b96a1c580f64cdb16b615eb02b015baddf `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-276"></a>
### 276. N6 / ` scene, render: use Gamma 2.2 TF as default `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/render/pass.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/types/scene/surface.c `、` 3rdparty/wlroots/types/scene/wlr_scene.c `、` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 329020b96a1c580f64cdb16b615eb02b015baddf ` → ` 838003573cb2dd04b93bb2be6d3465d2465c7ab5 `。
  原证据引用：` 39ee5addc607aa03dbe9ee9852f7bfc87e4ad5db ` → ` 2dfd5d13a5cf247a7f2fe95e3065bc83f4c28e1b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 14bc196ab3bd402cfbf024ad7161ea740d9438d5 ` 和原目标 ` 17a6d9c13d3d98039d652119bd9f9cfe39492b88 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 838003573cb2dd04b93bb2be6d3465d2465c7ab5 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-277"></a>
### 277. N6 / ` render: introduce bt.1886 transfer function `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/drm/atomic.c `、` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/include/wlr/render/color.h `、` 3rdparty/wlroots/render/color.c `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/renderer.c `、` 3rdparty/wlroots/render/vulkan/shaders/output.frag `、` 3rdparty/wlroots/render/vulkan/shaders/texture.frag `、` 3rdparty/wlroots/types/scene/surface.c `、` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 838003573cb2dd04b93bb2be6d3465d2465c7ab5 ` → ` eec1fa673c2bdc9e3f50993f5e2d63e5798d83e0 `。
  原证据引用：` 2dfd5d13a5cf247a7f2fe95e3065bc83f4c28e1b ` → ` bac499735f6e48518ed5ceb261681a43108b615f `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 1b12bc8f66b4b00a3106978d5dbfdc32f79477f1 ` 和原目标 ` 03ef3aab2fc02d636f50b5098252551df1dc7794 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` eec1fa673c2bdc9e3f50993f5e2d63e5798d83e0 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-278"></a>
### 278. N6 / ` wlr_scene: fix direct scanout for gamma2.2 buffers `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` eec1fa673c2bdc9e3f50993f5e2d63e5798d83e0 ` → ` 3170541414acca10529893792294605ff16ac713 `。
  原证据引用：` bac499735f6e48518ed5ceb261681a43108b615f ` → ` 5d86cfdcbe12e04ac1dea1a9f2e3bdf263bd8d07 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 281b27d95f3c8a0530023f2f33e514c894a2a4eb ` 和原目标 ` 1ddf3648ecadc85ffc7c00e4c9bc0ff9abab2d02 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 3170541414acca10529893792294605ff16ac713 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-279"></a>
### 279. N6 / ` ci: fix VKMS lookup after faux bus migration `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/.builds/archlinux.yml `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 3170541414acca10529893792294605ff16ac713 ` → ` 5f97e5c124af8e0da70cea949b430bd0ab5ad809 `。
  原证据引用：` 5d86cfdcbe12e04ac1dea1a9f2e3bdf263bd8d07 ` → ` 9948c3378df5182c86cc868d721a58627872aacb `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d9a79f78d0d3e7dca79fd1ec3c42bbb93b4d9119 ` 和原目标 ` 34cf6e709d029400c3bebac048710a360c6b2f00 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 5f97e5c124af8e0da70cea949b430bd0ab5ad809 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-280"></a>
### 280. N6 / ` input-method-v2: Destroy keyboard grab before input method `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_input_method_v2.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 5f97e5c124af8e0da70cea949b430bd0ab5ad809 ` → ` a5c42867cd39118f54c3c4295cb9b87a97fc235f `。
  原证据引用：` 9948c3378df5182c86cc868d721a58627872aacb ` → ` 469767a5d16acaebfe27b6510c9a5bacb8bde0c3 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 176a8cc2e8a5aee7d7f658a0e48aae7273bd0164 ` 和原目标 ` f7b649c1774915f54e216503778feb21b39b97cf ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` a5c42867cd39118f54c3c4295cb9b87a97fc235f `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-281"></a>
### 281. N6 / ` util/box.c: use 1/256 instead of 1/65536 in wlr_box_closest_point() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/util/box.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` a5c42867cd39118f54c3c4295cb9b87a97fc235f ` → ` fef499d04dd353f718addc084a2e88aaa9a7df3a `。
  原证据引用：` 469767a5d16acaebfe27b6510c9a5bacb8bde0c3 ` → ` a6a7ab0654d73cb08b5558e08312ad61390582f1 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d1aad42faaf0e715d3ef79f329827ab6bdad8709 ` 和原目标 ` ca18de3547d9d100cb60718fd2f1ee6ef0a17e7d ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` fef499d04dd353f718addc084a2e88aaa9a7df3a `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-282"></a>
### 282. N6 / ` linux_drm_syncobj_v1: fix use-after-free in surface_commit_destroy() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_linux_drm_syncobj_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` fef499d04dd353f718addc084a2e88aaa9a7df3a ` → ` 08102cad998f241d4e762b5604ffc1f1792d31f4 `。
  原证据引用：` a6a7ab0654d73cb08b5558e08312ad61390582f1 ` → ` 47a22ef4f5384c4905607b57104c83a66d8b7642 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 067a405aee6453f2be435febaeac6bb00fea3b5a ` 和原目标 ` e2fcfff47df33d37aa07355140d049eb8a838e8c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 08102cad998f241d4e762b5604ffc1f1792d31f4 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-283"></a>
### 283. N6 / `` backend/session: use device `boot_display` ``

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/session/session.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 08102cad998f241d4e762b5604ffc1f1792d31f4 ` → ` f4754aa1f93cab8a0e76ee75a5cf6100f5800ee5 `。
  原证据引用：` 47a22ef4f5384c4905607b57104c83a66d8b7642 ` → ` e7d50f2d68812ef676b37bb82fc1c73736584a60 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 376af70c54377ce8266a194c98b8f6b89a07abb8 ` 和原目标 ` beaae2c113dfab24091f76fd650507da0c6dd2e6 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` f4754aa1f93cab8a0e76ee75a5cf6100f5800ee5 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-284"></a>
### 284. N6 / ` render/color: add wlr_color_transform_eval() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/color.h `、` 3rdparty/wlroots/include/wlr/render/color.h `、` 3rdparty/wlroots/render/color.c `、` 3rdparty/wlroots/render/vulkan/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` f4754aa1f93cab8a0e76ee75a5cf6100f5800ee5 ` → ` 4720d5b0a45b449ba3d5dcec49ab267eb5624ac4 `。
  原证据引用：` e7d50f2d68812ef676b37bb82fc1c73736584a60 ` → ` 435b53c728b394feff1b9fe83e1b09c9cac9b2b5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` f6962a9d32fe455341ece7d6c90b4dfb976f9755 ` 和原目标 ` 2af6f2771ce543eb9ccef18c1135fe60b3a18622 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 4720d5b0a45b449ba3d5dcec49ab267eb5624ac4 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-285"></a>
### 285. N6 / ` render/color: add wlr_color_transform_pipeline `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/color.h `、` 3rdparty/wlroots/include/wlr/render/color.h `、` 3rdparty/wlroots/render/color.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 4720d5b0a45b449ba3d5dcec49ab267eb5624ac4 ` → ` 632f52c194ef4c4ed28390672620298ed48e4f66 `。
  原证据引用：` 435b53c728b394feff1b9fe83e1b09c9cac9b2b5 ` → ` 3890e8c825b20c2562d597c07519f4fd771e25fa `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` a193b80ad2a620584e4ef3ef276f0df67a9abb1a ` 和原目标 ` 23ef71df172761333c0c1ba0d38f1488f8e45a32 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 632f52c194ef4c4ed28390672620298ed48e4f66 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-286"></a>
### 286. N6 / ` output: check for color transform no-op changes `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_output.h `、` 3rdparty/wlroots/types/output/output.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 632f52c194ef4c4ed28390672620298ed48e4f66 ` → ` 838f8a9f333d3bb234687326ffd197f58a6b77d3 `。
  原证据引用：` 3890e8c825b20c2562d597c07519f4fd771e25fa ` → ` 6340677ee09372979b7f03342bf5827e7e005a7d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 157c8e5c6d66ac8f8bf878bf9314cc18f796d576 ` 和原目标 ` c0541f2bfd7c289962e0978e7077b1a579589f6a ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 838f8a9f333d3bb234687326ffd197f58a6b77d3 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-287"></a>
### 287. N6 / ` gamma_control_v1: add wlr_gamma_control_v1_get_color_transform() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_gamma_control_v1.h `、` 3rdparty/wlroots/types/wlr_gamma_control_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 838f8a9f333d3bb234687326ffd197f58a6b77d3 ` → ` 165a20d1143d9378c2df70fcfb749df0a01f56ec `。
  原证据引用：` 6340677ee09372979b7f03342bf5827e7e005a7d ` → ` 31f8b57dad90c9765bbe0f7e5ea7ad7277470413 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 8a1c9cb02c96da1e87b6648f729154c30d57dc61 ` 和原目标 ` 68c0d26e0977c9f5318f2a1fe8f8b21801308b0b ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 165a20d1143d9378c2df70fcfb749df0a01f56ec `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-288"></a>
### 288. N6 / ` gamma_control_v1: introduce fallback_gamma_size `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_gamma_control_v1.h `、` 3rdparty/wlroots/types/wlr_gamma_control_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 165a20d1143d9378c2df70fcfb749df0a01f56ec ` → ` 5feb7f4b77b4e4bf7674dd84d140d087798baae0 `。
  原证据引用：` 31f8b57dad90c9765bbe0f7e5ea7ad7277470413 ` → ` e13321f0b6514f884522c6666d3053706246a920 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 6af85fa8f6fbec935f4395475f7af72e798ee51c ` 和原目标 ` e9bba9f73624ee2009b73e630d98ae2187dc7e61 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 5feb7f4b77b4e4bf7674dd84d140d087798baae0 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-289"></a>
### 289. N6 / ` scene: add software fallback for gamma LUT `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_scene.h `、` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 5feb7f4b77b4e4bf7674dd84d140d087798baae0 ` → ` d847a0c3d6d5d76a13d84c70ab12ad5aa659b2e1 `。
  原证据引用：` e13321f0b6514f884522c6666d3053706246a920 ` → ` a9e6ef3bd25e5152b77ddd3fe247f2453910f924 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` a8ad377c4b0933fda640a95ead1786e39a479152 ` 和原目标 ` f7417f36b50f9c335b11544872d5961e47a63272 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` d847a0c3d6d5d76a13d84c70ab12ad5aa659b2e1 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-290"></a>
### 290. N6 / ` xwm: Fix double-close `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/xwayland/xwm.h `、` 3rdparty/wlroots/xwayland/xwayland.c `、` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` d847a0c3d6d5d76a13d84c70ab12ad5aa659b2e1 ` → ` 0313dbbbce692507905d6888e9742a9546057a18 `。
  原证据引用：` a9e6ef3bd25e5152b77ddd3fe247f2453910f924 ` → ` c62697e15c37d50319ae115a8cbc125352578b45 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ee51b8c2d6ab1f641b3923d85cf3f3d400806a6b ` 和原目标 ` c2190191e8e8d1d90211ee826e9da92d0c006fa4 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 0313dbbbce692507905d6888e9742a9546057a18 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-291"></a>
### 291. N6 / ` render/vulkan: clip negative values before applying transfer function `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/shaders/output.frag `、` 3rdparty/wlroots/render/vulkan/shaders/texture.frag `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 0313dbbbce692507905d6888e9742a9546057a18 ` → ` fa321f6a65fbddee5e1705939b520182e6096231 `。
  原证据引用：` c62697e15c37d50319ae115a8cbc125352578b45 ` → ` 03e713f506cf6bd6a6c658823bbc8110bc3dcae8 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 0ad625e31c0e3db7cc06ed5fcb78bdc264bd8963 ` 和原目标 ` 2ebb8b950e10cc12f3e4cfcedb2b77f0740d3779 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` fa321f6a65fbddee5e1705939b520182e6096231 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-292"></a>
### 292. N6 / ` types/wlr_input_device: name maybe NULL `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_input_device.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` fa321f6a65fbddee5e1705939b520182e6096231 ` → ` a42a448c34430a2f160af30b6fc62dd539b40100 `。
  原证据引用：` 03e713f506cf6bd6a6c658823bbc8110bc3dcae8 ` → ` 0ad0aec09c0f996024d853100a1505df1d8c5f57 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` cd468f22a2d22b122ae7f90a106b2e17be4425ed ` 和原目标 ` 8c0383f08296843f0ca018de7d9c015cfbc89ccb ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` a42a448c34430a2f160af30b6fc62dd539b40100 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-293"></a>
### 293. N6 / ` drm: save edid color characteristics in wlr_output `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/drm/util.c `、` 3rdparty/wlroots/include/wlr/types/wlr_output.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` a42a448c34430a2f160af30b6fc62dd539b40100 ` → ` 5362486aa8b01a51169e468acc82c2ceea33da00 `。
  原证据引用：` 0ad0aec09c0f996024d853100a1505df1d8c5f57 ` → ` abf173ac9c35d54c2c8342daab35f34996937b61 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ec2cc0d8f046917b349beec7427acebe1e9fb92a ` 和原目标 ` b0df667bd1f83791dbbfbffd321e57bb65fd6478 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 5362486aa8b01a51169e468acc82c2ceea33da00 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-294"></a>
### 294. N6 / ` wlr_virtual_pointer: Set axis source on all axis `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_virtual_pointer_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 5362486aa8b01a51169e468acc82c2ceea33da00 ` → ` 29d1a0910001fb661222bc6c2834214d6e000b41 `。
  原证据引用：` abf173ac9c35d54c2c8342daab35f34996937b61 ` → ` 1c4ab8ff2a6f1589fb4faa26d7c87b48113769cf `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 74ddba3ad69645de9c9d0574ad1b51f31f6acc15 ` 和原目标 ` 95de8d294ac88a432580842290894f67f6e84383 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 29d1a0910001fb661222bc6c2834214d6e000b41 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-295"></a>
### 295. N6 / ` cursor: apply output image description when preparing texture `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/output/cursor.c `、` 3rdparty/wlroots/types/wlr_cursor.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 29d1a0910001fb661222bc6c2834214d6e000b41 ` → ` aa9327ad36cf4b15b97f9adf71335d449476dcb6 `。
  原证据引用：` 1c4ab8ff2a6f1589fb4faa26d7c87b48113769cf ` → ` bf752bda90e5c1488f0c8ff1231a3591d5a99ac7 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 98311478a1842967c73b02182288a3d8f6794605 ` 和原目标 ` 7f816077dc42d96038d31274024e68a24708093c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` aa9327ad36cf4b15b97f9adf71335d449476dcb6 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-296"></a>
### 296. N6 / ` render/color: turn enum wlr_color_encoding into a bitfield `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/render/color.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` aa9327ad36cf4b15b97f9adf71335d449476dcb6 ` → ` af7dd4e41ba112c0d4a6e703f74054965c6bd292 `。
  原证据引用：` bf752bda90e5c1488f0c8ff1231a3591d5a99ac7 ` → ` f44c24bbad12e4bcfc9eefc2fc0e0a63a57abd49 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 7975208b038626a0df83fc285aaba339c52d8115 ` 和原目标 ` 6a1328b6b6e24cfc0cbd406b9af390a3654dbc1e ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` af7dd4e41ba112c0d4a6e703f74054965c6bd292 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-297"></a>
### 297. N6 / ` render: add color encoding and range to wlr_render_texture_options `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/render/pass.h `、` 3rdparty/wlroots/include/wlr/render/wlr_renderer.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` af7dd4e41ba112c0d4a6e703f74054965c6bd292 ` → ` f42ba3e3c182094628987c5651a77e7b2ef6113f `。
  原证据引用：` f44c24bbad12e4bcfc9eefc2fc0e0a63a57abd49 ` → ` e97e9564a6cd81d22649d6bb16f8fa0fd5e75721 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` a6acfaa2493ccfb4848ad4455df0e048d0f250a0 ` 和原目标 ` e4c0c57a1872b1117958ea2ca07d2124c6b45e6d ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` f42ba3e3c182094628987c5651a77e7b2ef6113f `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-298"></a>
### 298. N6 / ` render/vulkan: add suport for color encoding and range `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/renderer.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` f42ba3e3c182094628987c5651a77e7b2ef6113f ` → ` 1dfd40ec41b18653bc7aadc81c00af9fefab9f1f `。
  原证据引用：` e97e9564a6cd81d22649d6bb16f8fa0fd5e75721 ` → ` 5d88280805504f8af8c3a209cbb0b920df613fec `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 062478639d1a54ce37b217b56ab0da36cdd567cd ` 和原目标 ` 87ceab53f54d91a85d2aa4e9f19f98e4132fc8ab ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 1dfd40ec41b18653bc7aadc81c00af9fefab9f1f `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-299"></a>
### 299. N6 / ` color_representation_v1: make supported_alpha_modes const `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_color_representation_v1.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 1dfd40ec41b18653bc7aadc81c00af9fefab9f1f ` → ` 8650d2e38e67f923f057b8aa2d77b7603cf1d0bf `。
  原证据引用：` 5d88280805504f8af8c3a209cbb0b920df613fec ` → ` 1d733bf5d94155dd172744add15ff667c7946e60 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 6c857fd08e4b9f38cf859052a51e0f70b0bc0534 ` 和原目标 ` abbc6a72b7c0fdd04abe1da267f67b4e245d549c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 8650d2e38e67f923f057b8aa2d77b7603cf1d0bf `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-300"></a>
### 300. N6 / ` scene: add support for color encoding and range `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_scene.h `、` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 8650d2e38e67f923f057b8aa2d77b7603cf1d0bf ` → ` ec14f93b9acad59f8b55c98d180c6c2e356cbe80 `。
  原证据引用：` 1d733bf5d94155dd172744add15ff667c7946e60 ` → ` a48f9c3a39697e0560d8ce4c27cc95f9d32650ee `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 5706871fba99a052671e17f8f9ecab92fb5927a3 ` 和原目标 ` b8e44bca4cc41a3cce7077ddc874ad9c67f7ee59 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` ec14f93b9acad59f8b55c98d180c6c2e356cbe80 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-301"></a>
### 301. N6 / ` scene: add support for color-representation-v1 coeffs and range `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/surface.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` ec14f93b9acad59f8b55c98d180c6c2e356cbe80 ` → ` bab4e673ff08164322f7742d459e95432fc01479 `。
  原证据引用：` a48f9c3a39697e0560d8ce4c27cc95f9d32650ee ` → ` d61d3c34cf3751a5e910b29bc1a99ad88786f9cd `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d8a3e90459942b4af5d0869901d8f1be12fbc40a ` 和原目标 ` 68bf6d9b22696934eb5978955e75fcfefe38fbff ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` bab4e673ff08164322f7742d459e95432fc01479 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-302"></a>
### 302. N6 / ` color_representation_v1: add helper to create global from renderer `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_color_representation_v1.h `、` 3rdparty/wlroots/types/wlr_color_representation_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` bab4e673ff08164322f7742d459e95432fc01479 ` → ` ee64e991d877ce01935a70ec0cb4b1b7e5a535e1 `。
  原证据引用：` d61d3c34cf3751a5e910b29bc1a99ad88786f9cd ` → ` ffea25ff5d2cf70c46bb162637bad57e31b97d6a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 7a6e9e84bb9a20d6d8d4c170b40689b05044176d ` 和原目标 ` f5505dd3787c586526bebae29e2e74aab194513b ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` ee64e991d877ce01935a70ec0cb4b1b7e5a535e1 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-303"></a>
### 303. N6 / ` output/state: add missing unref for color_transform `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/output/state.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` ee64e991d877ce01935a70ec0cb4b1b7e5a535e1 ` → ` 101008c3e83b875773627f701189ac9d7b755df2 `。
  原证据引用：` ffea25ff5d2cf70c46bb162637bad57e31b97d6a ` → ` 4ee3e69b97d6a9b4f2d2659d05bed11a136e4b53 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 185dbab6bd716e5de74581d12a903e3eba742f83 ` 和原目标 ` 8b97bba533ac7e237e198a211fd8b09f6ab4f528 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 101008c3e83b875773627f701189ac9d7b755df2 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-304"></a>
### 304. N6 / ` render/vulkan: fix single-pass linear path `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/renderer.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 101008c3e83b875773627f701189ac9d7b755df2 ` → ` 78eb463ea2c735d8798886f964f431e57f917bb9 `。
  原证据引用：` 4ee3e69b97d6a9b4f2d2659d05bed11a136e4b53 ` → ` 8b6e6292269b6a2f77fd734324670cbb5edd94e2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` b134d3316de3017b1b520e4dd0077e703b50438c ` 和原目标 ` aa0d0878bc23fb07ece7e58780fcc3000462f4e6 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 78eb463ea2c735d8798886f964f431e57f917bb9 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-305"></a>
### 305. N6 / ` input-method-unstable-v2: There are no enable / disable events `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/protocol/input-method-unstable-v2.xml `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 78eb463ea2c735d8798886f964f431e57f917bb9 ` → ` 57535a4dbaac6a89579d2b75c0ce2b8f6d2014ce `。
  原证据引用：` 8b6e6292269b6a2f77fd734324670cbb5edd94e2 ` → ` a5a5156e043dbae5a4fea949de69bfe2808f3000 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 57c36469b466184c578da62d73bed578e4783258 ` 和原目标 ` f510a2ccde9a9b60c2af261b303c8b5f257c3bfe ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 57535a4dbaac6a89579d2b75c0ce2b8f6d2014ce `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-306"></a>
### 306. N6 / ` input-method-unstable-v2: surrounding text sends surrounding text `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/protocol/input-method-unstable-v2.xml `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 57535a4dbaac6a89579d2b75c0ce2b8f6d2014ce ` → ` 0731daa24b274a9a6ed21cdb1d33395d7895a82a `。
  原证据引用：` a5a5156e043dbae5a4fea949de69bfe2808f3000 ` → ` c21e778590050003da863eaa6981bae3b18261f1 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 2bcefab7736eec802cee9293c3e1ef45b94c5391 ` 和原目标 ` c1e9acebb008815accbc4beb68efd1fef5b3411a ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 0731daa24b274a9a6ed21cdb1d33395d7895a82a `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-307"></a>
### 307. N6 / ` render/color: add wlr_color_primaries_transform_absolute_colorimetric `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/render/color.h `、` 3rdparty/wlroots/render/color.c `、` 3rdparty/wlroots/render/vulkan/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 0731daa24b274a9a6ed21cdb1d33395d7895a82a ` → ` 8c4e4cad9ba890f68447a997ae3dcd30aedcee44 `。
  原证据引用：` c21e778590050003da863eaa6981bae3b18261f1 ` → ` 2e94fd024418d2178396a6c1b4f5985047eb3f6f `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d6a6ecfb0ba65b1e0142740edc046ed95a45c733 ` 和原目标 ` eade18a067fef4f80ae0b67dbd46a77fe63b2331 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 8c4e4cad9ba890f68447a997ae3dcd30aedcee44 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-308"></a>
### 308. N6 / ` render/color: introduce wlr_color_transform_matrix `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/color.h `、` 3rdparty/wlroots/include/wlr/render/color.h `、` 3rdparty/wlroots/render/color.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 8c4e4cad9ba890f68447a997ae3dcd30aedcee44 ` → ` cdffda4bb04ee0273cdaa1de52f0c518fb06564e `。
  原证据引用：` 2e94fd024418d2178396a6c1b4f5985047eb3f6f ` → ` b6e14aabfe22cfb77c62e9fed4f06cffd986bc03 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` b22ff363877fff122484669b129585f21fb1789a ` 和原目标 ` 1e2c4719fb29690f46e2fc5923b96a2b12ad0116 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` cdffda4bb04ee0273cdaa1de52f0c518fb06564e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-309"></a>
### 309. N6 / ` render/vulkan: apply "matrix" color transforms in shader `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` cdffda4bb04ee0273cdaa1de52f0c518fb06564e ` → ` f8dfba21317b9bc8d6ed07dfea72ef3f4f0d874a `。
  原证据引用：` b6e14aabfe22cfb77c62e9fed4f06cffd986bc03 ` → ` cd84c9be93be4ccd1d86e52c42388bdd84e88160 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 5b312c3ecee51220bdd55cf7ac94482d45039f22 ` 和原目标 ` 372e6f18e684003f7ec3926d470786ce022431c0 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` f8dfba21317b9bc8d6ed07dfea72ef3f4f0d874a `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-310"></a>
### 310. N6 / ` scene: always apply user gamma after scene color transform `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` f8dfba21317b9bc8d6ed07dfea72ef3f4f0d874a ` → ` 12018d0dd52536d9a2b0328324b210d67c089db5 `。
  原证据引用：` cd84c9be93be4ccd1d86e52c42388bdd84e88160 ` → ` 6e174b3638e16de7620b8e401f9e72c077963d2a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 2db1217d9547190f1a0636321ac9d92018a18511 ` 和原目标 ` 720b8dbf3bf7654e8747b94708e62825b98b1a1e ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 12018d0dd52536d9a2b0328324b210d67c089db5 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-311"></a>
### 311. N6 / ` render: remove buffer primaries from pass options `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/include/wlr/render/pass.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/types/output/cursor.c `、` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 12018d0dd52536d9a2b0328324b210d67c089db5 ` → ` 95a2af04f152ec052a8ac34bd1541adf0ed6c0d9 `。
  原证据引用：` 6e174b3638e16de7620b8e401f9e72c077963d2a ` → ` 6ecf0de43938531d04334cbc5e19ce8cb4d2eaa6 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 2016ffa81ceff6c6bbc6e95f53cae5bb8a101d66 ` 和原目标 ` c8af1be28fbcaca68737a30d9e2a32af40340556 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 95a2af04f152ec052a8ac34bd1541adf0ed6c0d9 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-312"></a>
### 312. N6 / ` scene: don't rebuild color transforms each frame `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_scene.h `、` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 95a2af04f152ec052a8ac34bd1541adf0ed6c0d9 ` → ` 3b0b20bbbb32a2df362b4beff3dfa3fe3821e275 `。
  原证据引用：` 6ecf0de43938531d04334cbc5e19ce8cb4d2eaa6 ` → ` 0ece1b83e012398758abdae5bf3e5417792e80d2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 2b150ee90c8091c9f9a798521e566b7fe3dce935 ` 和原目标 ` 31b234852aeb053bda30d8511e3b0d481a0f0f11 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 3b0b20bbbb32a2df362b4beff3dfa3fe3821e275 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-313"></a>
### 313. N6 / ` output: don't rebuild cursor color transform for each update `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/types/wlr_output.h `、` 3rdparty/wlroots/include/wlr/types/wlr_output.h `、` 3rdparty/wlroots/types/output/cursor.c `、` 3rdparty/wlroots/types/output/output.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 3b0b20bbbb32a2df362b4beff3dfa3fe3821e275 ` → ` 383a489da26ef398b82d0b13ddae613b7be66ff5 `。
  原证据引用：` 0ece1b83e012398758abdae5bf3e5417792e80d2 ` → ` cfc190c2232ccda4c95fe9be062a1a16b16c076a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 5937df5c87b4785cba5b8a81886f4850d5dd61fb ` 和原目标 ` 70cc85201ceb79706c3294f21eeb8c425ceddc1b ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 383a489da26ef398b82d0b13ddae613b7be66ff5 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-314"></a>
### 314. N6 / ` wlr-foreign-toplevel: avoid wl_resource_find_for_client() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_foreign_toplevel_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 383a489da26ef398b82d0b13ddae613b7be66ff5 ` → ` 4858cabcc163c192e3690e9eb9383d02a9de1e89 `。
  原证据引用：` cfc190c2232ccda4c95fe9be062a1a16b16c076a ` → ` bf4d2cd0f91bbca6d9ea9ff2f07edb6a3b8d0056 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d842378e12e4a35671be9d5c21d37cd08d13c459 ` 和原目标 ` c90b7d05635841c6226a5ebab62501a1b3c75584 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 4858cabcc163c192e3690e9eb9383d02a9de1e89 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-315"></a>
### 315. N6 / ` Add "const" to eliminate "error: initialization discards ‘const’ qualifier from pointer target type" `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xcursor/xcursor.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 4858cabcc163c192e3690e9eb9383d02a9de1e89 ` → ` 3dbc2d769b1bf9f0700736a6657c648fe7b2b1a1 `。
  原证据引用：` bf4d2cd0f91bbca6d9ea9ff2f07edb6a3b8d0056 ` → ` 0a70b71d3a2be3b90851cd33d0ea2493fe47ec5f `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 90691cdea7530c371e3805e28b479c06b8c04aa0 ` 和原目标 ` 6e4ef5c068055fb1f723f5c45683babb951e9944 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 3dbc2d769b1bf9f0700736a6657c648fe7b2b1a1 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-316"></a>
### 316. N6 / ` color_representation_v1: don't leak supported_* on display destroy `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_color_representation_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 3dbc2d769b1bf9f0700736a6657c648fe7b2b1a1 ` → ` 46072e58789574589ea3f989176b6c069a81a5a8 `。
  原证据引用：` 0a70b71d3a2be3b90851cd33d0ea2493fe47ec5f ` → ` 72b4c95e7f58c13133c7db0f5dc30099a3544e5c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` da21f4e5915a14fea778d9fa038fb434f893d4e7 ` 和原目标 ` 14a6891d06a03c93f87af4477c8d4d5b1eb6ec0a ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 46072e58789574589ea3f989176b6c069a81a5a8 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-317"></a>
### 317. N6 / ` render/color: make wlr_color_primaries_from_named public `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/color.h `、` 3rdparty/wlroots/include/wlr/render/color.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 46072e58789574589ea3f989176b6c069a81a5a8 ` → ` 5a3a57693d4f0955c54b8f4beb988757c91aa067 `。
  原证据引用：` 72b4c95e7f58c13133c7db0f5dc30099a3544e5c ` → ` df41a402fe84df688ca472f9a31dc6ca6f02047e `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` f7face1e13784f9b4de186ccffc70891c0fe63d4 ` 和原目标 ` b50a34f54fb1579d40ecd2cc6a50789212ed8a04 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 5a3a57693d4f0955c54b8f4beb988757c91aa067 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-318"></a>
### 318. N6 / ` render/vulkan: normalize luminance range in bt.1886 formula `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/shaders/output.frag `、` 3rdparty/wlroots/render/vulkan/shaders/texture.frag `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 5a3a57693d4f0955c54b8f4beb988757c91aa067 ` → ` daaa763fb0b5f0518217057091c6c2887497cce3 `。
  原证据引用：` df41a402fe84df688ca472f9a31dc6ca6f02047e ` → ` 1f9a1d93771f928eaee3a4b8edf662f34e12c92b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 81aba2cb86984a3be3b18bdd56b7d7fd14e6f7dd ` 和原目标 ` 8ff3e75c15a72bb63db67ef922971d16fc201e30 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` daaa763fb0b5f0518217057091c6c2887497cce3 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-319"></a>
### 319. N6 / ` drag: destroy data source on touch_up `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/data_device/wlr_drag.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` daaa763fb0b5f0518217057091c6c2887497cce3 ` → ` 9071b37212e1c3a04bc727ccc45fc0b583597f2e `。
  原证据引用：` 1f9a1d93771f928eaee3a4b8edf662f34e12c92b ` → ` b16a4f233df6d23a5afaf7b7ca8651f0e8676dfb `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` e967582c197f412fc46eab0890e8181de7455e8b ` 和原目标 ` f836ee5dc29637559537c508e2484c8f6de6b89f ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 9071b37212e1c3a04bc727ccc45fc0b583597f2e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-320"></a>
### 320. N6 / ` seat: add wlr_seat_touch_notify_clear_focus `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_seat.h `、` 3rdparty/wlroots/types/data_device/wlr_drag.c `、` 3rdparty/wlroots/types/seat/wlr_seat_touch.c `、` 3rdparty/wlroots/types/xdg_shell/wlr_xdg_popup.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 9071b37212e1c3a04bc727ccc45fc0b583597f2e ` → ` 9dcf5ac2e4271f8d0c7aeecb134e4d7e95fcdfe2 `。
  原证据引用：` b16a4f233df6d23a5afaf7b7ca8651f0e8676dfb ` → ` 4730a9fdffc23f8a8cdf5e531fd3342ff4041c50 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ba5abbbf116d925c10ce8f9f3113849df5d87aa8 ` 和原目标 ` 41ebc23410491decc554c026d9cef0ae28431552 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 9dcf5ac2e4271f8d0c7aeecb134e4d7e95fcdfe2 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-321"></a>
### 321. N6 / ` Add wlr_version_get_{major,minor,micro}() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/version.h.in `、` 3rdparty/wlroots/util/meson.build `、` 3rdparty/wlroots/util/version.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 9dcf5ac2e4271f8d0c7aeecb134e4d7e95fcdfe2 ` → ` 051c9a8fc50ea6caa829abf9d5dfdc7b369a4aeb `。
  原证据引用：` 4730a9fdffc23f8a8cdf5e531fd3342ff4041c50 ` → ` 5ea5c48a077577ae2932768b2e0163a6f06b963c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 4ea7c83c74b513e9f2113805e58ffd761593373e ` 和原目标 ` 952dec77f3cca1e72b7fb130164a751c79928e5e ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 051c9a8fc50ea6caa829abf9d5dfdc7b369a4aeb `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-322"></a>
### 322. N6 / ` color_management_v1: add helpers to get supported TFs/primaries `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_color_management_v1.h `、` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 051c9a8fc50ea6caa829abf9d5dfdc7b369a4aeb ` → ` 90549545dca6316d39429ea7512cade051889f57 `。
  原证据引用：` 5ea5c48a077577ae2932768b2e0163a6f06b963c ` → ` 594a84cc08e1b328214a70a673590b89db1a0331 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 71c789fbe3542417423e61363791d565240c9da0 ` 和原目标 ` a09c4bfa727f2f3e6f39879af1d499420af4141a ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 90549545dca6316d39429ea7512cade051889f57 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-323"></a>
### 323. N6 / ` tinywl: fix duplicate object files passed to linker `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/tinywl/Makefile `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 90549545dca6316d39429ea7512cade051889f57 ` → ` 2ef506d3c868cfb2e5159f56001e695b17edf10d `。
  原证据引用：` 594a84cc08e1b328214a70a673590b89db1a0331 ` → ` 7859f18b11f7f04d4b1cb1ca80f05866879140d5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 4b83bf88e9e763439c03a01e733e0946e0b52cdc ` 和原目标 ` e8ef439595713e1a3ad13d3bc4f588477efa579d ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 2ef506d3c868cfb2e5159f56001e695b17edf10d `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-324"></a>
### 324. N6 / ` render/pixman: add support for ABGR16161616 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/pixman/meson.build `、` 3rdparty/wlroots/render/pixman/pixel_format.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 2ef506d3c868cfb2e5159f56001e695b17edf10d ` → ` fc67c471a9564d919e586e2f8087803fe9d1ebd0 `。
  原证据引用：` 7859f18b11f7f04d4b1cb1ca80f05866879140d5 ` → ` e5643820dbbd5e8087277b4ccb4511bdf29ba949 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 4f0ce89fb2c884c5109838d66a6e5f24d2383e5d ` 和原目标 ` 8eed4a788d3f8f7a6cf631a66ded408f6bae9a85 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` fc67c471a9564d919e586e2f8087803fe9d1ebd0 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-325"></a>
### 325. N6 / ` color_management_v1: add BT.1886 to TF-from-renderer helper `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` fc67c471a9564d919e586e2f8087803fe9d1ebd0 ` → ` f15254642b1a40f5db7f9b7cc6a2a0a6ac99a30c `。
  原证据引用：` e5643820dbbd5e8087277b4ccb4511bdf29ba949 ` → ` 87fbf7b932a9512c270550e45f6f6a3a43ca380f `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 4c0f2e48eb8c07c157d541770862f10887d05201 ` 和原目标 ` 1f1ebda328e32a23a0924e292d23b85d9f077ae3 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` f15254642b1a40f5db7f9b7cc6a2a0a6ac99a30c `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-326"></a>
### 326. N6 / ` render/color: introduce color_transform_compose `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/color.h `、` 3rdparty/wlroots/render/color.c `、` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` f15254642b1a40f5db7f9b7cc6a2a0a6ac99a30c ` → ` 6ebaf88c4337fc4834de59b12417fbfe39be7503 `。
  原证据引用：` 87fbf7b932a9512c270550e45f6f6a3a43ca380f ` → ` 06468d74a91e408c964f7fa7e15b9b3d76a5c261 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 067b0ade78281960f9e31aa4820de0bc86883cf8 ` 和原目标 ` e6d7323d7f8aecc93e05b9570b5fce523558c938 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 6ebaf88c4337fc4834de59b12417fbfe39be7503 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-327"></a>
### 327. N6 / ` render/color: assert that wlr_color_transform_pipeline contains no NULLs `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/color.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 6ebaf88c4337fc4834de59b12417fbfe39be7503 ` → ` c583c9575d4faaba65f141cad6567aae3b9403c7 `。
  原证据引用：` 06468d74a91e408c964f7fa7e15b9b3d76a5c261 ` → ` 8e5cb1a3e427a457cf794d2430ca60691dff1afb `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 75d29da9934335df1a7717be0d795765e46af7c7 ` 和原目标 ` 9284c6a73e9f3ca3df1425671b3a541360870004 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` c583c9575d4faaba65f141cad6567aae3b9403c7 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-328"></a>
### 328. N6 / ` backend/session: respond to event hangup or error `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/session/session.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` c583c9575d4faaba65f141cad6567aae3b9403c7 ` → ` 4aed4b677206e9f6ddf9bd6e81fa184a70a6550c `。
  原证据引用：` 8e5cb1a3e427a457cf794d2430ca60691dff1afb ` → ` 7aef90609f1bd9581344130b58b76b5fec1be2f3 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ad86e8232cf0a4304b39f03826a85c8d99daa4da ` 和原目标 ` a1561b50d7b5557afd3974e31f22335ba99f99ce ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 4aed4b677206e9f6ddf9bd6e81fa184a70a6550c `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-329"></a>
### 329. N6 / ` render/allocator: add missing wlr_buffer_finish() in destroy impls `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/allocator/shm.c `、` 3rdparty/wlroots/render/allocator/udmabuf.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 4aed4b677206e9f6ddf9bd6e81fa184a70a6550c ` → ` 706cb329d4e88345d68c5fa7f59421c4adf4c405 `。
  原证据引用：` 7aef90609f1bd9581344130b58b76b5fec1be2f3 ` → ` e19937cd0b75f67b8a84d6b99e643c1176e17199 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 76e9d812c4171953af224eb9c2261ad4d406fc07 ` 和原目标 ` 5345c59e37c5d2f0e6cc09659d2092807111efb1 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 706cb329d4e88345d68c5fa7f59421c4adf4c405 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-330"></a>
### 330. N6 / ` session: simplify libudev unref handling `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/session/session.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 706cb329d4e88345d68c5fa7f59421c4adf4c405 ` → ` 53bc3e4ebe780a236d58f967e3c1a0fa970ede81 `。
  原证据引用：` e19937cd0b75f67b8a84d6b99e643c1176e17199 ` → ` 131eec8d8ad3dab03425e42e1a3ab760e8033f95 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 0c10122d1ebb57b0643585fc2c7528d5d7cdf36a ` 和原目标 ` d8faed4649f1137d37032e735787fa0112cc0cfa ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 53bc3e4ebe780a236d58f967e3c1a0fa970ede81 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-331"></a>
### 331. N6 / ` scene: don't assign outputs to invisible nodes `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 53bc3e4ebe780a236d58f967e3c1a0fa970ede81 ` → ` 7a6c64ccdb040fd99b4220172ce5c73832f939b2 `。
  原证据引用：` 131eec8d8ad3dab03425e42e1a3ab760e8033f95 ` → ` c9328ea6bf5e5b565f56f9622ea59c2d10ee83dd `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` e9c267ff80ded1d3d9aad35557242b393ffba4e6 ` 和原目标 ` 7920017a659a56bde3faaff7f9cfa9da9db52f4a ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 7a6c64ccdb040fd99b4220172ce5c73832f939b2 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-332"></a>
### 332. N6 / ` scene: constify pixman_region32_t `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 7a6c64ccdb040fd99b4220172ce5c73832f939b2 ` → ` cb540ea79f69e2646c54018dabb480bca29b04c9 `。
  原证据引用：` c9328ea6bf5e5b565f56f9622ea59c2d10ee83dd ` → ` 661a80244c200cdd937c1428ce6d0c359b5d9785 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` b00c4f4321a6811340eb21790513eaef257daad7 ` 和原目标 ` 78cb69150805df9257fc15af60540b4baa219824 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` cb540ea79f69e2646c54018dabb480bca29b04c9 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-333"></a>
### 333. N6 / ` render: add new 16- and 32-bits-per-component pixel formats `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/meson.build `、` 3rdparty/wlroots/render/pixel_format.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` cb540ea79f69e2646c54018dabb480bca29b04c9 ` → ` 469db003f143d566b7f6d311419b696a910fbc37 `。
  原证据引用：` 661a80244c200cdd937c1428ce6d0c359b5d9785 ` → ` abd30eed4cebbc09f4acaf3962257357edffa8c1 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 26876224f2460506f1eb0a6ca43ed7910c3e9a4c ` 和原目标 ` d23cadd91c45960de324fa0d6df985420f738062 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 469db003f143d566b7f6d311419b696a910fbc37 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-334"></a>
### 334. N6 / ` render/gles2: add BGR161616F and BGR161616 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/gles2/pixel_format.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 469db003f143d566b7f6d311419b696a910fbc37 ` → ` 5b176e8632e13736af2b92042a8dbfdc9eade66e `。
  原证据引用：` abd30eed4cebbc09f4acaf3962257357edffa8c1 ` → ` ff628ba2a014f7be0451bc36a55f63b265648e7c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 39f129f848fd5a310087dfdca21f65912b755eed ` 和原目标 ` 4de4f559ffb987d25a0403714208aa18fe9ad3d9 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 5b176e8632e13736af2b92042a8dbfdc9eade66e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-335"></a>
### 335. N6 / ` render/vulkan: add new 16- and 32-bits-per-component pixel formats `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/pixel_format.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 5b176e8632e13736af2b92042a8dbfdc9eade66e ` → ` 8b4d4a6d99a7ab140d1a62e2832d7078cc9f5a93 `。
  原证据引用：` ff628ba2a014f7be0451bc36a55f63b265648e7c ` → ` dd0baf6974db81b84410bc10c3023659f7c04e18 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 43c1fe1ed8f964937cd59101f3a0dae71c2aaac7 ` 和原目标 ` 5ddf0140934254b5d6881841ab788f3f25027d9c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 8b4d4a6d99a7ab140d1a62e2832d7078cc9f5a93 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-336"></a>
### 336. N6 / ` scene: keep last preferred configuration when leaving last output `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/surface.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 8b4d4a6d99a7ab140d1a62e2832d7078cc9f5a93 ` → ` a4bdd584addfbe57bee1b9f4b68215fe984fcc95 `。
  原证据引用：` dd0baf6974db81b84410bc10c3023659f7c04e18 ` → ` 57fc34692f54351354b7634be6dbe67247d60c85 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` a8ebb8932f8f28fa247f54e394db0133f1363051 ` 和原目标 ` 64d1e755fb3771294b97a6cd471f5d50276dba34 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` a4bdd584addfbe57bee1b9f4b68215fe984fcc95 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-337"></a>
### 337. N6 / ` render: drop <linux/dma-buf.h> compat defines `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/dmabuf_linux.c `、` 3rdparty/wlroots/render/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` a4bdd584addfbe57bee1b9f4b68215fe984fcc95 ` → ` 61a896900479706672b40e21cbfa0cbea9186dc5 `。
  原证据引用：` 57fc34692f54351354b7634be6dbe67247d60c85 ` → ` 142ed073a76f3d7a468effd3a634ce8cb7021c26 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 36d6251519cb258e33455dcbeee700b29c818a80 ` 和原目标 ` 8d127871bf4209311714f62c81f222c8612733f3 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 61a896900479706672b40e21cbfa0cbea9186dc5 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-338"></a>
### 338. N6 / ` ext_image_capture_source_v1/scene: fix stop for parallel captures `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/ext_image_capture_source_v1/scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 61a896900479706672b40e21cbfa0cbea9186dc5 ` → ` dc05cc4095fc54511a90abe6c18c06254a5ecd77 `。
  原证据引用：` 142ed073a76f3d7a468effd3a634ce8cb7021c26 ` → ` 17ffe4fb6db56248185e9aefe1c9c62bbace3a4e `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` b5bfbe09427cf35324917c2cbc2606490bbb0a57 ` 和原目标 ` 4deb7dbb518a4ee874469d61b5f3662a8c11ec79 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` dc05cc4095fc54511a90abe6c18c06254a5ecd77 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-339"></a>
### 339. N6 / ` scene/surface: don't cache frame pacing output `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_scene.h `、` 3rdparty/wlroots/types/scene/surface.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` dc05cc4095fc54511a90abe6c18c06254a5ecd77 ` → ` 62168e68ed06cfce2daf103ec5e102a08ceebaf8 `。
  原证据引用：` 17ffe4fb6db56248185e9aefe1c9c62bbace3a4e ` → ` cb3f9854c36378a1aad3be81671a650ab4cf6da0 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` bc8eee2feea24b094f952da1c8c5dd31ffd2c703 ` 和原目标 ` 6b9b3c84baf449602350e56f486783a3524a8994 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 62168e68ed06cfce2daf103ec5e102a08ceebaf8 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-340"></a>
### 340. N6 / ` scene: add knob to turn off Xwayland surface restacking `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_scene.h `、` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 62168e68ed06cfce2daf103ec5e102a08ceebaf8 ` → ` 419fac393c1b8206424f6efc8051e9f795437b0a `。
  原证据引用：` cb3f9854c36378a1aad3be81671a650ab4cf6da0 ` → ` 9e69a2e75f18e8bd0887731b1512b545ab343d37 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 5d82753f7c09aaec904c85b54225b64301afe61c ` 和原目标 ` 8ec56b0823972a3d40d89e3f7286593b9caabf29 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 419fac393c1b8206424f6efc8051e9f795437b0a `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-341"></a>
### 341. N6 / ` render/gles2: skip glslang check when shaders are unchanged `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/gles2/shaders/check.sh `、` 3rdparty/wlroots/render/gles2/shaders/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 419fac393c1b8206424f6efc8051e9f795437b0a ` → ` 383d7b930a5586bb389e643c2dc4a8b790ad11eb `。
  原证据引用：` 9e69a2e75f18e8bd0887731b1512b545ab343d37 ` → ` c6d486144ac796d0044055734353de9110f9647c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` b174ad188ccd15d8a3121b97a9cc36c6a2f67fbf ` 和原目标 ` c48a8b7e02159e3c3f67572a85774ab9af677406 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 383d7b930a5586bb389e643c2dc4a8b790ad11eb `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-342"></a>
### 342. N6 / ` xcursor: add shared helper to create a wlr_xcursor_image `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xcursor/wlr_xcursor.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 383d7b930a5586bb389e643c2dc4a8b790ad11eb ` → ` 4406185ea4271eb17564efd03fb8f6859bd0bf83 `。
  原证据引用：` c6d486144ac796d0044055734353de9110f9647c ` → ` 4716a4077513ad9979581320e74df1aec3a253df `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 58f9eed9aba894fe667600c3e00a7310da425099 ` 和原目标 ` 5a4bc8a7dafa02cec7c2f9e218c3fbb901215665 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 4406185ea4271eb17564efd03fb8f6859bd0bf83 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-343"></a>
### 343. N6 / ` xcursor: introduce wlr_xcursor_image_get_buffer() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/xcursor.h `、` 3rdparty/wlroots/xcursor/wlr_xcursor.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 4406185ea4271eb17564efd03fb8f6859bd0bf83 ` → ` d901075c54491652ff4485985bca3cf67b4c1a08 `。
  原证据引用：` 4716a4077513ad9979581320e74df1aec3a253df ` → ` e300d7e68a6303be0042dd104d61ba2710d02c07 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 47b86e3a72846d16bc15de91d9e25307e74a6f9d ` 和原目标 ` e9eba16a5370e52993b79b8c1345e4136396e385 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` d901075c54491652ff4485985bca3cf67b4c1a08 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-344"></a>
### 344. N6 / ` cursor: use wlr_xcursor_image_get_buffer() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_cursor.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` d901075c54491652ff4485985bca3cf67b4c1a08 ` → ` 162bda79cf5293f9d60ddeac5f4203d0116068ea `。
  原证据引用：` e300d7e68a6303be0042dd104d61ba2710d02c07 ` → ` efb71eb145a20694f5e3d3341233e6bfca923fa0 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 6cc4e12f5165d20d987ba17874e9082c96b31092 ` 和原目标 ` 63a6597dcfe276f1259929de71da6099061ec460 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 162bda79cf5293f9d60ddeac5f4203d0116068ea `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-345"></a>
### 345. N6 / ` xwayland: take wlr_buffer in wlr_xwayland_set_cursor() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/xwayland/xwayland.h `、` 3rdparty/wlroots/include/xwayland/xwm.h `、` 3rdparty/wlroots/xwayland/xwayland.c `、` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 162bda79cf5293f9d60ddeac5f4203d0116068ea ` → ` dc87d9ad6f018d9d0aaa5aa0413c7fb62d38fcef `。
  原证据引用：` efb71eb145a20694f5e3d3341233e6bfca923fa0 ` → ` b46dfbd14945f492f41b692605506ce131e42a59 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` f1a83816508406225f8e5658e32d7e5a52066daf ` 和原目标 ` fa298baff4874800cef63babe839b89728f37dac ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` dc87d9ad6f018d9d0aaa5aa0413c7fb62d38fcef `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-346"></a>
### 346. N6 / ` xwayland: lock new buffer instead of the old one `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/xwayland.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` dc87d9ad6f018d9d0aaa5aa0413c7fb62d38fcef ` → ` d9e8aba0bbe8bebc2bb9ccbe569486375300d6d0 `。
  原证据引用：` b46dfbd14945f492f41b692605506ce131e42a59 ` → ` d0280f5eb56d40117d2a64b3cb58bfbcb1b8e392 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` e2f55b8c3b12ee79a38c3140c31c3d7d22656a3c ` 和原目标 ` b0b7c3bb45af5eec9f65a484967f8317d7fc9f92 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` d9e8aba0bbe8bebc2bb9ccbe569486375300d6d0 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-347"></a>
### 347. N6 / ` ext_image_copy_capture_v1: replace schedule_frame with request_frame `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/interfaces/wlr_ext_image_capture_source_v1.h `、` 3rdparty/wlroots/types/ext_image_capture_source_v1/output.c `、` 3rdparty/wlroots/types/ext_image_capture_source_v1/scene.c `、` 3rdparty/wlroots/types/wlr_ext_image_copy_capture_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` d9e8aba0bbe8bebc2bb9ccbe569486375300d6d0 ` → ` bc9be88277fc3b41b73819758e3e191d3bbf8df1 `。
  原证据引用：` d0280f5eb56d40117d2a64b3cb58bfbcb1b8e392 ` → ` 40dc6023c9f84c67fd648d3964b4e65349ab840c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 389983c28b815abf4a3c963de2dce0ddaffc0986 ` 和原目标 ` b700b81231c4a4caeffe3da31600eeebac2d1034 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` bc9be88277fc3b41b73819758e3e191d3bbf8df1 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-348"></a>
### 348. N6 / ` ext_image_capture_source_v1: wait for capture client before sending frame event `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/ext_image_capture_source_v1/scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` bc9be88277fc3b41b73819758e3e191d3bbf8df1 ` → ` b6a7c78b53a7d7f6bc9057ae8b1b4de40832b60d `。
  原证据引用：` 40dc6023c9f84c67fd648d3964b4e65349ab840c ` → ` d2abaa46859f87f1b917ccc6849b906ea85a28cb `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 4b62fd3265ddbc26db3c6c7d062bf102fb6c7d9a ` 和原目标 ` a470d1b526d1e863573e0175c05837e0b6b4399f ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` b6a7c78b53a7d7f6bc9057ae8b1b4de40832b60d `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-349"></a>
### 349. N6 / ` wlr_ext_image_copy_capture_v1: new_session event `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_ext_image_copy_capture_v1.h `、` 3rdparty/wlroots/types/wlr_ext_image_copy_capture_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` b6a7c78b53a7d7f6bc9057ae8b1b4de40832b60d ` → ` 1124cdc75eb7a1a4ae95f902553edd3c0d203011 `。
  原证据引用：` d2abaa46859f87f1b917ccc6849b906ea85a28cb ` → ` cb437cb0d6940129fa29e2d17f96ca10af2164f7 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 8b3d05ae4538d8d4cd72d5d63ee3109d6e76e32b ` 和原目标 ` 57818d5dfc310240ce91f9e0750d2fe765d7a778 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 1124cdc75eb7a1a4ae95f902553edd3c0d203011 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-350"></a>
### 350. N6 / ` image_capture_source: wlr_output_try_from_ext_image_capture_source_v1() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_ext_image_capture_source_v1.h `、` 3rdparty/wlroots/types/ext_image_capture_source_v1/output.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 1124cdc75eb7a1a4ae95f902553edd3c0d203011 ` → ` 1fa1144408b5ee89ba2905bcef8af5f9118ba45d `。
  原证据引用：` cb437cb0d6940129fa29e2d17f96ca10af2164f7 ` → ` c8dc5bbb1b5d741ce2835f14f5839e5706933056 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` f5243d5d08f98aa662592fb94c9032ba21bcb343 ` 和原目标 ` ca902c55fe610907c74ec30ce9a13ca4003f6a47 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 1fa1144408b5ee89ba2905bcef8af5f9118ba45d `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-351"></a>
### 351. N6 / ` wlr_scene: Make restack_xwayland_surface_below generic `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 1fa1144408b5ee89ba2905bcef8af5f9118ba45d ` → ` 5c28de1cfeba8164115360e0daa4b3a6b784981d `。
  原证据引用：` c8dc5bbb1b5d741ce2835f14f5839e5706933056 ` → ` 79e488ab49492895ca73dc633673d08f885608f7 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 48264e43b25daf9f396478ed753be4a47533cbc6 ` 和原目标 ` c986835fb9e70b385fdfb65346f26a46adc3f3de ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 5c28de1cfeba8164115360e0daa4b3a6b784981d `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-352"></a>
### 352. N6 / ` wlr_scene: Don't recurse when disabling scene node if a child is already disabled `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 5c28de1cfeba8164115360e0daa4b3a6b784981d ` → ` 20e77dbb9dcf6c792bd5cdd03aa7b1656c040b83 `。
  原证据引用：` 79e488ab49492895ca73dc633673d08f885608f7 ` → ` 91dfad4a074021d9e5437873ba3a06da6d64d378 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 82fc3c6fd467be4b146db30daeae46e7c17857f3 ` 和原目标 ` 484b993fd585087db10c2c0c084fc49a94a24ad2 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 20e77dbb9dcf6c792bd5cdd03aa7b1656c040b83 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-353"></a>
### 353. N6 / ` wlr_scene: Update outputs when node is disabled `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 20e77dbb9dcf6c792bd5cdd03aa7b1656c040b83 ` → ` d48c5646ce7f46f1ae4dfa506284a1e70ebcfeca `。
  原证据引用：` 91dfad4a074021d9e5437873ba3a06da6d64d378 ` → ` 2f3a868607636cc98430a4a1dd3487a0bcf96334 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 6ba97a939ab4869d29102b4539ad9a4f1a9e8cae ` 和原目标 ` dbce0505ed3d5706e0ee58ea8a5d5b93f5f22c1c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` d48c5646ce7f46f1ae4dfa506284a1e70ebcfeca `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-354"></a>
### 354. N6 / ` wlr_scene: Only do disable cleanup when explicit damage is given `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` d48c5646ce7f46f1ae4dfa506284a1e70ebcfeca ` → ` dc71f3e5c545e4f403134e9ad96221b862f6fb7e `。
  原证据引用：` 2f3a868607636cc98430a4a1dd3487a0bcf96334 ` → ` 97aa3e409a80d4404dd81edc14852af2b603952e `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 83fe6dd04a62bdb7f28406b90f61a0cc921e36dc ` 和原目标 ` b2e395225c7728236f44e4043457a69a4e0b6c2a ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` dc71f3e5c545e4f403134e9ad96221b862f6fb7e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-355"></a>
### 355. N6 / ` wlr_scene: Add documentation to scene_node_update() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` dc71f3e5c545e4f403134e9ad96221b862f6fb7e ` → ` 53dcb940f2dc5e4d0d8fbf0485ba89efb8fab4dc `。
  原证据引用：` 97aa3e409a80d4404dd81edc14852af2b603952e ` → ` 36c4eb0e809781eea7036d9c727f0a11b4704ebc `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 59871dc496250d6b03de9749a4422098e8f18906 ` 和原目标 ` ba50226694a0103ad8dd4e34115ccbaee980e8bd ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 53dcb940f2dc5e4d0d8fbf0485ba89efb8fab4dc `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-356"></a>
### 356. N6 / ` wlr_ext_image_copy_capture_v1: Fix segmentation fault when using cursor session `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_ext_image_copy_capture_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 53dcb940f2dc5e4d0d8fbf0485ba89efb8fab4dc ` → ` 1d42aff732b644f4c747b554a7c893a86bf7f099 `。
  原证据引用：` 36c4eb0e809781eea7036d9c727f0a11b4704ebc ` → ` 0684c2b09c3bf69f763d0bb65532a0f3972dfcc2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 7774ea8fda1917293324caae6922529bc1a7a846 ` 和原目标 ` ea32e25fd4a5f627715525d6c742ae61ab3def13 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 1d42aff732b644f4c747b554a7c893a86bf7f099 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-357"></a>
### 357. N6 / ` xwayland: add set_size_hints signal `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/xwayland/xwayland.h `、` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 1d42aff732b644f4c747b554a7c893a86bf7f099 ` → ` 081151a6a798c0cc5a592e560b51a686e99f8972 `。
  原证据引用：` 0684c2b09c3bf69f763d0bb65532a0f3972dfcc2 ` → ` 8c386affe272d2979ea5cea748f04fcfdbdb1927 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 021cc6c2cf8255c98c74b4a18b7945de424ac65c ` 和原目标 ` 01fe53ba9f00f8343b59f7a29b9737f547103ed2 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 081151a6a798c0cc5a592e560b51a686e99f8972 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-358"></a>
### 358. N6 / ` xwm: don't leak msg in case of realloc failure `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 081151a6a798c0cc5a592e560b51a686e99f8972 ` → ` a980e42993c6d513bd4268fd21f54227356cd58b `。
  原证据引用：` 8c386affe272d2979ea5cea748f04fcfdbdb1927 ` → ` bf83ba94c4b4bb9fa51f60e84d1dcec6f150806e `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` c852ee8d9ce7dc8072f1be44b1349f17eda236de ` 和原目标 ` 12ee5f35bf753d2f48f32e09b5f571e8f1fa9cd4 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` a980e42993c6d513bd4268fd21f54227356cd58b `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-359"></a>
### 359. N6 / ` backend/libinput: expose libinput_tablet_tool `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/libinput/tablet_tool.c `、` 3rdparty/wlroots/include/wlr/backend/libinput.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` a980e42993c6d513bd4268fd21f54227356cd58b ` → ` 30e1045264442a3db9610cd17a0a7833e3a4c696 `。
  原证据引用：` bf83ba94c4b4bb9fa51f60e84d1dcec6f150806e ` → ` 1182e5b8fa26d92b0b96aca9edc5c3bf93e0d1cc `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ddc9c388e4567b395043144773ebf06251178895 ` 和原目标 ` d2e62cb63c789e62ae5f46d30c9211cca7263dba ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 30e1045264442a3db9610cd17a0a7833e3a4c696 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-360"></a>
### 360. N6 / ` xwayland/selection/dnd: fix parameter type `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/selection/dnd.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 30e1045264442a3db9610cd17a0a7833e3a4c696 ` → ` 2c8dda23b705ff54330aa21cf70e47de01c9991e `。
  原证据引用：` 1182e5b8fa26d92b0b96aca9edc5c3bf93e0d1cc ` → ` b4da6ca707c91d27814326227734f1efa1c1be87 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` c93555dc03169fdbf42ab4aaf8e7bb1a74904084 ` 和原目标 ` 8119bdf83523dc31b012c7d8918d0cf63f8440bc ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 2c8dda23b705ff54330aa21cf70e47de01c9991e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-361"></a>
### 361. N6 / ` output-swapchain-manager: Reject zero resolution `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_output_swapchain_manager.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 2c8dda23b705ff54330aa21cf70e47de01c9991e ` → ` 5e51728ec3ea4fc9d4e05a2b5afd9b5764b78f10 `。
  原证据引用：` b4da6ca707c91d27814326227734f1efa1c1be87 ` → ` d31017c5c4016856b4783024026bf4e74de9bb0d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` fadf5214d54853c1852e5be59e9b569e4068adf6 ` 和原目标 ` 5bd260029e1c91783b693438d6b0f5f2e65f63c3 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 5e51728ec3ea4fc9d4e05a2b5afd9b5764b78f10 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-362"></a>
### 362. N6 / ` meson: bump minimum wayland-protocols version `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/protocol/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 5e51728ec3ea4fc9d4e05a2b5afd9b5764b78f10 ` → ` 2e15d8a516f52b88ac94ca60f3761059e8b3f038 `。
  原证据引用：` d31017c5c4016856b4783024026bf4e74de9bb0d ` → ` e0d8238f92b74e0fde50e55ea45d9e28ffdb07d3 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ab75ae1c5270a293dc63a07819982896abbc58f5 ` 和原目标 ` fd1deba5881202104233163a521d821fdd462bd7 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 2e15d8a516f52b88ac94ca60f3761059e8b3f038 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-363"></a>
### 363. N6 / ` color_management_v1: relax restrictions on maxCLL and maxFALL `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 2e15d8a516f52b88ac94ca60f3761059e8b3f038 ` → ` bbaae63db3740656df7b1db5fb4e39d1ffc60cf0 `。
  原证据引用：` e0d8238f92b74e0fde50e55ea45d9e28ffdb07d3 ` → ` 5d7616bc433e0daeb93160b5934ebcb72459d60e `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` fd27ca253c30c4f08e7f31af1631c69824741b13 ` 和原目标 ` 3f8458739e81f8814d5d7521b578bbc4ff776225 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` bbaae63db3740656df7b1db5fb4e39d1ffc60cf0 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-364"></a>
### 364. N6 / ` color_management_v1: use 64bit image description identities `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_color_management_v1.h `、` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` bbaae63db3740656df7b1db5fb4e39d1ffc60cf0 ` → ` 3a552f9275454ca97cf55a5a5d7556bad843bf9a `。
  原证据引用：` 5d7616bc433e0daeb93160b5934ebcb72459d60e ` → ` 5c37c1d548a92abcb99da0e73bef0bd507a8df1b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` a3bbf452fc9968d58d8c6e8c5eea7152d9ab867c ` 和原目标 ` 2f5e66ba1856fd248d0abf01f97f8ea71768d556 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 3a552f9275454ca97cf55a5a5d7556bad843bf9a `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-365"></a>
### 365. N6 / ` color_management_v1: new enum value for 'srgb' transfer function `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 3a552f9275454ca97cf55a5a5d7556bad843bf9a ` → ` 89e5524a293695f40f5f22000a7377c9518f3694 `。
  原证据引用：` 5c37c1d548a92abcb99da0e73bef0bd507a8df1b ` → ` 5b07b395e78acfbd5e1edae43db6baba168bcb91 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 26af21548c5d80dc1142f5c44557833632c4ff5d ` 和原目标 ` d0a442c3e7550d068a2341ce38c0fbc26cb80e91 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 89e5524a293695f40f5f22000a7377c9518f3694 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-366"></a>
### 366. N6 / ` render: don't infer luminance multipliers from color TF `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/include/wlr/render/pass.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/shaders/output.frag `、` 3rdparty/wlroots/types/output/cursor.c `、` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 89e5524a293695f40f5f22000a7377c9518f3694 ` → ` d0a37bb4c4ed572e94b95eaee74b2f91b43d03ad `。
  原证据引用：` 5b07b395e78acfbd5e1edae43db6baba168bcb91 ` → ` 75226b52af65afd1a8582f9386e16b979efc12ac `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` bd6b287ac9d76591a55f554c0bdde1b3832a2309 ` 和原目标 ` 10c32d86b4acb99379c13898f16ad6bb6dbb0884 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` d0a37bb4c4ed572e94b95eaee74b2f91b43d03ad `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-367"></a>
### 367. N6 / ` ext_image_copy_capture_v1: Only render scene source on damage `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/ext_image_capture_source_v1/scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` d0a37bb4c4ed572e94b95eaee74b2f91b43d03ad ` → ` 391a8bece190796c0d89421bfa33f7a7e4f56d59 `。
  原证据引用：` 75226b52af65afd1a8582f9386e16b979efc12ac ` → ` 7bf7f33aef63e6f2516ccabd2a0d2718e17c3e0a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 5d3fb87c4b682ee30b0633166127e2dac28f114c ` 和原目标 ` 079ee9a9c4f915f86253f229098686525cf1bc0f ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 391a8bece190796c0d89421bfa33f7a7e4f56d59 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-368"></a>
### 368. N6 / ` ext-workspace-v1: add implementation `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_ext_workspace_v1.h `、` 3rdparty/wlroots/protocol/meson.build `、` 3rdparty/wlroots/types/meson.build `、` 3rdparty/wlroots/types/wlr_ext_workspace_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 391a8bece190796c0d89421bfa33f7a7e4f56d59 ` → ` 2d8605c9ced89f0ecfb322de152672bf38527391 `。
  原证据引用：` 7bf7f33aef63e6f2516ccabd2a0d2718e17c3e0a ` → ` 20d1f3af2c0985dd51836052ba87d37ebdc9504c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` c2390909a26d9a9fc3c246c551ad80a69a7b66ef ` 和原目标 ` 83f80cb193ba3a5f4148b303e5e5e111084fd352 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 2d8605c9ced89f0ecfb322de152672bf38527391 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-369"></a>
### 369. N6 / ` color_representation_v1: send chroma_location protocol error `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_color_representation_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 2d8605c9ced89f0ecfb322de152672bf38527391 ` → ` 4d7b91652d6e6a790207558e066eafade8e92d73 `。
  原证据引用：` 20d1f3af2c0985dd51836052ba87d37ebdc9504c ` → ` 867364fe32fdd665cfe4ef171c0411264b10d0f5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 71270845bf373f80251e45756a8c286318294cc3 ` 和原目标 ` a5bb7e1e1a06b7655a568089f417f700151223fb ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 4d7b91652d6e6a790207558e066eafade8e92d73 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-370"></a>
### 370. N6 / ` build: bump version to 0.20.0-rc1 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 4d7b91652d6e6a790207558e066eafade8e92d73 ` → ` 1b5d2c6fa52fb31057fe50e88cc86133822ea966 `。
  原证据引用：` 867364fe32fdd665cfe4ef171c0411264b10d0f5 ` → ` 840a465bb3af3688794989094adcc008936da4b3 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` eb77b4b14501c40f1b1de2b99fb8bac620ee4071 ` 和原目标 ` b7b52eaba2e947d868bbc033bd440841a3d90341 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 1b5d2c6fa52fb31057fe50e88cc86133822ea966 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-371"></a>
### 371. N6 / ` render/drm_syncobj: drop unnecessary drmSyncobjTimelineWait() arg `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/drm_syncobj.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 1b5d2c6fa52fb31057fe50e88cc86133822ea966 ` → ` 005967b7e1b376a7c2fd98f03f8fdf0791fabec6 `。
  原证据引用：` 840a465bb3af3688794989094adcc008936da4b3 ` → ` 6e6b0712fb7c892ba6fb04705b34ce4cc818b036 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 7a8f3e20c4cd9a4d66cb804af2a00f2d385a7c5f ` 和原目标 ` dbfcfa3850f1ca564455a3b2f901d230052bfc85 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 005967b7e1b376a7c2fd98f03f8fdf0791fabec6 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-372"></a>
### 372. N6 / ` render/drm_syncobj: fix function name in drmSyncobjTimelineWait() error log `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/drm_syncobj.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 005967b7e1b376a7c2fd98f03f8fdf0791fabec6 ` → ` c5690bacde41a1415a5e1e1cb9ce6faf4f54477c `。
  原证据引用：` 6e6b0712fb7c892ba6fb04705b34ce4cc818b036 ` → ` afa7c04b65e5c3fbd3c87c086e1f18cb76dca883 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 6dd43c98dde630107bae193867bc4f6d69cdf092 ` 和原目标 ` 62feb013defaa5f87d40f01171012a9208670c77 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` c5690bacde41a1415a5e1e1cb9ce6faf4f54477c `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-373"></a>
### 373. N6 / ` types: Simplify wlr_keyboard_group_destroy `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_keyboard_group.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` c5690bacde41a1415a5e1e1cb9ce6faf4f54477c ` → ` 4f0bf5096a3d2bf7d431acd3c5176a037ad8be50 `。
  原证据引用：` afa7c04b65e5c3fbd3c87c086e1f18cb76dca883 ` → ` 052416800f62a795d758813791d2d70b42704de9 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 3e2c4ba46b2a4048b8e7beb961080920c7ef0ea7 ` 和原目标 ` 0062950c4e2bea153593af8ae2d87b94a3f9bf0c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 4f0bf5096a3d2bf7d431acd3c5176a037ad8be50 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-374"></a>
### 374. N6 / ` wlr_cursor: add comments for signal parameters `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_cursor.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 4f0bf5096a3d2bf7d431acd3c5176a037ad8be50 ` → ` 060197bf8e43323661a6c8b3321256a4637e33f9 `。
  原证据引用：` 052416800f62a795d758813791d2d70b42704de9 ` → ` 4d9a16dee1aef5619897347c7967d0696f9a676c `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 99fccac3fbc2267c2750508111f70639ffb0ea75 ` 和原目标 ` af76f350af6446d7520b2c3156f040bd7cf99665 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 060197bf8e43323661a6c8b3321256a4637e33f9 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-375"></a>
### 375. N6 / ` wlr_cursor: fix event type in handle_tablet_tool_button `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_cursor.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 060197bf8e43323661a6c8b3321256a4637e33f9 ` → ` 38fc70179beb4ed3e9d494d84b9681e021741686 `。
  原证据引用：` 4d9a16dee1aef5619897347c7967d0696f9a676c ` → ` c5aba193fe95ea8882ed8a6c958cb597c5b52b94 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` a69221cdcccb767a6167b5854239ddc519f27788 ` 和原目标 ` 1f5bb2bb35ca720a1856b1abd97770acb69437c3 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 38fc70179beb4ed3e9d494d84b9681e021741686 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-376"></a>
### 376. N6 / ` xwayland: try flushing immediately in xwm_schedule_flush() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 38fc70179beb4ed3e9d494d84b9681e021741686 ` → ` 385044f92cc53110807d76835adf24b2bf2a39d2 `。
  原证据引用：` c5aba193fe95ea8882ed8a6c958cb597c5b52b94 ` → ` 45e74431f528559eb6d96ea58a0e412a32a75e04 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 1f07ad74867449605c595af816f92dd3e73bcce5 ` 和原目标 ` db94577f79456aafe80c629406bbd3470161a85d ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 385044f92cc53110807d76835adf24b2bf2a39d2 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-377"></a>
### 377. N6 / ` xwayland: fix wl_array rollback when adding selection targets `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/selection/incoming.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 385044f92cc53110807d76835adf24b2bf2a39d2 ` → ` 2db43f4f2700ca6d410de9192c556e68fdf3f450 `。
  原证据引用：` 45e74431f528559eb6d96ea58a0e412a32a75e04 ` → ` ffbf14786afd89d6560f9455c65de1c6aee274e9 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ed9c8498336eeff3fd9502740ec48191b2c6d984 ` 和原目标 ` bb29268e26fe908c3393d35cbbda2db626bb66d0 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 2db43f4f2700ca6d410de9192c556e68fdf3f450 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-378"></a>
### 378. N6 / ` ext_image_capture_source_v1: remove unused variable `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/ext_image_capture_source_v1/scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 2db43f4f2700ca6d410de9192c556e68fdf3f450 ` → ` 2a70b280b857edac6a10e207213c4f4d67f3549b `。
  原证据引用：` ffbf14786afd89d6560f9455c65de1c6aee274e9 ` → ` 0eda0092ea7dc54f87a0672cb50dcecde0a0332a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 092a194ac64c581e62bd64ca05c904d01b143296 ` 和原目标 ` 29b943872a50d3c5124dea56e409f8e6d592535a ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 2a70b280b857edac6a10e207213c4f4d67f3549b `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-379"></a>
### 379. N6 / ` output/cursor: fix missing newline at end of file `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/output/cursor.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 2a70b280b857edac6a10e207213c4f4d67f3549b ` → ` 623b7bd23822f5b76b31517143256512cae2b8b4 `。
  原证据引用：` 0eda0092ea7dc54f87a0672cb50dcecde0a0332a ` → ` 64cfebe0c736503bffd90aac6d76f42e1b03fd9a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 50f1a3b7acc17d93ac453b95b31db4b0f14eb00d ` 和原目标 ` 292ad7396dce15c735fe338d9dd384a82ca487de ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 623b7bd23822f5b76b31517143256512cae2b8b4 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-380"></a>
### 380. N6 / ` render/pixel-format: add function to determine YCbCr from drm fourcc `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/pixel_format.h `、` 3rdparty/wlroots/render/pixel_format.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 623b7bd23822f5b76b31517143256512cae2b8b4 ` → ` 88e5cf5bfec7323c8af28f9ffbc69fc31d2b6f51 `。
  原证据引用：` 64cfebe0c736503bffd90aac6d76f42e1b03fd9a ` → ` b685fc886d3d5fe6b7f7710bb0caa987041ad859 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` a05e29aa1f38147a6795a90b3572e9ae00b1d523 ` 和原目标 ` 79726897b933ef00e1058308510435addb1e31a6 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 88e5cf5bfec7323c8af28f9ffbc69fc31d2b6f51 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-381"></a>
### 381. N6 / ` vulkan: make use of new pixel_format_is_ycbcr function `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/pixel_format.c `、` 3rdparty/wlroots/render/vulkan/renderer.c `、` 3rdparty/wlroots/render/vulkan/texture.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 88e5cf5bfec7323c8af28f9ffbc69fc31d2b6f51 ` → ` a8b2172221d85449fb8ecbcad7a28129d184990c `。
  原证据引用：` b685fc886d3d5fe6b7f7710bb0caa987041ad859 ` → ` a0bb80d1741fbe721b572b09221ed292e4b6aec2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 6ca4dfa6fc6fdfe86af2adbb5d9c8c907b6d6c15 ` 和原目标 ` 6e69d9d9265038ca481d05c4f34537cdc64b7047 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` a8b2172221d85449fb8ecbcad7a28129d184990c `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-382"></a>
### 382. N6 / ` color_representation: ensure encoding/range/drm formats compatibility `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_color_representation_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` a8b2172221d85449fb8ecbcad7a28129d184990c ` → ` a5076d94d0d0b0f321c5dc100cec9463d7097d9e `。
  原证据引用：` a0bb80d1741fbe721b572b09221ed292e4b6aec2 ` → ` 4e5409f3fdc005141806de6450add455c313a650 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` f2b078c4f9d952d9115904183c11a187ffdebf1a ` 和原目标 ` 67b5f3a0c7558d11076535acc8a2a753521ff695 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` a5076d94d0d0b0f321c5dc100cec9463d7097d9e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-383"></a>
### 383. N6 / ` color-representation: add support for identity+full `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/renderer.c `、` 3rdparty/wlroots/types/scene/wlr_scene.c `、` 3rdparty/wlroots/types/wlr_color_representation_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` a5076d94d0d0b0f321c5dc100cec9463d7097d9e ` → ` dbcb5c7a756854cb075d8a7c5119a3b12ef5ae51 `。
  原证据引用：` 4e5409f3fdc005141806de6450add455c313a650 ` → ` 3ca9d77948007b470ef56db93c58fcdf7f691065 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d8728e7e6240203c615eff349735f3daed8429c5 ` 和原目标 ` 7ee6dffe38169afccf1d518da0a9cc89ad63328c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` dbcb5c7a756854cb075d8a7c5119a3b12ef5ae51 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-384"></a>
### 384. N6 / ` types/wlr_buffer: add buffer_get_drm_format helper function `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/x11/output.c `、` 3rdparty/wlroots/include/types/wlr_buffer.h `、` 3rdparty/wlroots/types/buffer/buffer.c `、` 3rdparty/wlroots/types/wlr_color_representation_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` dbcb5c7a756854cb075d8a7c5119a3b12ef5ae51 ` → ` 68c84e6ff15dc524e3e6a854028d9d29e1f0a71c `。
  原证据引用：` 3ca9d77948007b470ef56db93c58fcdf7f691065 ` → ` 08c017dea15a32cb2d0d985a20667a5551032837 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` c2e66806de72b0a4a12220a752e4c69386a946fc ` 和原目标 ` 5ec1b80437c801bae0a6c09ad90cada385e8e7cc ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 68c84e6ff15dc524e3e6a854028d9d29e1f0a71c `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-385"></a>
### 385. N6 / ` color-representation-v1: fix condition in surface commit `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_color_representation_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 68c84e6ff15dc524e3e6a854028d9d29e1f0a71c ` → ` 1883c3a9273c8924d12c35ccf1add17700ec5b68 `。
  原证据引用：` 08c017dea15a32cb2d0d985a20667a5551032837 ` → ` 8eb74114ccf23e2bd126f6b28b024808f92187e2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 59d835a1f7b3211dfc09070ea0aa7a509c125e45 ` 和原目标 ` dd81b8aaaac13c9e7bf2a3cca5216364fa351b89 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 1883c3a9273c8924d12c35ccf1add17700ec5b68 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-386"></a>
### 386. N6 / ` backend/libinput: fix build with libinput 1.31 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/libinput/meson.build `、` 3rdparty/wlroots/backend/libinput/switch.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 1883c3a9273c8924d12c35ccf1add17700ec5b68 ` → ` 9677965cf2a54fc3c2f54e649da60a5655e13ca4 `。
  原证据引用：` 8eb74114ccf23e2bd126f6b28b024808f92187e2 ` → ` 3755d3e0e9b75d3cb7eba58e56422888e41197dd `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 2870ec3689bda747464e5127b0d87ccb13d5e292 ` 和原目标 ` 3ada81126f17ed1192c0f4101bd4c822fc19dafd ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 9677965cf2a54fc3c2f54e649da60a5655e13ca4 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-387"></a>
### 387. N6 / ` backend/libinput: add support for LIBINPUT_SWITCH_KEYPAD_SLIDE `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/libinput/switch.c `、` 3rdparty/wlroots/include/wlr/types/wlr_switch.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 9677965cf2a54fc3c2f54e649da60a5655e13ca4 ` → ` abbf117e0632468d838cb92e5edd1c4c48236035 `。
  原证据引用：` 3755d3e0e9b75d3cb7eba58e56422888e41197dd ` → ` 1f2f4098c0b018fb6a46a128594ab0af29f9f9ba `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 28d97085e61eaa1c7fdfca9158d741508d74acaa ` 和原目标 ` bbfacb02940d4455d47c88a880ab3e0b4fe512d1 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` abbf117e0632468d838cb92e5edd1c4c48236035 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-388"></a>
### 388. N6 / ` build: bump version to 0.20.0-rc2 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` abbf117e0632468d838cb92e5edd1c4c48236035 ` → ` 0121a86a62762703b65b6307f9d35135e44fb66e `。
  原证据引用：` 1f2f4098c0b018fb6a46a128594ab0af29f9f9ba ` → ` 4ea51d099dd3f60bc56d4f3860da92a69b64fbe9 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 6f77ec93958ceaf024988b7e3d074fae0690b69b ` 和原目标 ` 35a16141290d52bdc05f3bb2710717fb8687f9c5 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 0121a86a62762703b65b6307f9d35135e44fb66e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-389"></a>
### 389. N6 / ` backend/x11: reject shm buffers with non-min strides `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/x11/output.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 0121a86a62762703b65b6307f9d35135e44fb66e ` → ` 643dcb55fd497b5572a27c966b6954730c9b61e9 `。
  原证据引用：` 4ea51d099dd3f60bc56d4f3860da92a69b64fbe9 ` → ` 3b7215542ec9247bdd3b34c3d73eff502c564eaa `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 4864dabb6453b3eb7041c8e3b6703a183ecd565d ` 和原目标 ` d6c153b7d26792bb696252178eaaa6ad79e5f0a8 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 643dcb55fd497b5572a27c966b6954730c9b61e9 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-390"></a>
### 390. N6 / ` backend/libinput: guard against new enum entries `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/libinput/events.c `、` 3rdparty/wlroots/backend/libinput/keyboard.c `、` 3rdparty/wlroots/backend/libinput/pointer.c `、` 3rdparty/wlroots/backend/libinput/switch.c `、` 3rdparty/wlroots/backend/libinput/tablet_pad.c `、` 3rdparty/wlroots/backend/libinput/tablet_tool.c `、` 3rdparty/wlroots/include/backend/libinput.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 643dcb55fd497b5572a27c966b6954730c9b61e9 ` → ` 64fc8a22a082ef6cdd3c8d7da77d6dd4b2a125de `。
  原证据引用：` 3b7215542ec9247bdd3b34c3d73eff502c564eaa ` → ` 67def39b94a52fc9f969342248cab3e4fb3882d9 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 4d23ec22fda34f1ca2670bde9ab4ede3184863bb ` 和原目标 ` e0e48767434dafbe93df6f21c3f56d8ae5eda6aa ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 64fc8a22a082ef6cdd3c8d7da77d6dd4b2a125de `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-391"></a>
### 391. N6 / ` backend/drm: Close non-master drm fd on failure `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/drm/drm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 64fc8a22a082ef6cdd3c8d7da77d6dd4b2a125de ` → ` 524997c10e272535954425b0b847a53efa49e738 `。
  原证据引用：` 67def39b94a52fc9f969342248cab3e4fb3882d9 ` → ` bf5019a26b6bc321fab136c60b106c346036a83a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` c36184c982fa24b4a4d234d361b01982ed7bb984 ` 和原目标 ` f33ba2538f1eb994183cb07d5b23cb3595afc3c6 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 524997c10e272535954425b0b847a53efa49e738 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-392"></a>
### 392. N6 / ` CONTRIBUTING.md: update git host `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/CONTRIBUTING.md `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 524997c10e272535954425b0b847a53efa49e738 ` → ` 4b9d59bf3f87caf3db9cfee055f052c9c988ac20 `。
  原证据引用：` bf5019a26b6bc321fab136c60b106c346036a83a ` → ` 71ec973a0160c349cec14dcdf834357bcea44ea8 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 9d02d0388ca2cd519deb342fbbdd290b67a9f6cd ` 和原目标 ` 1cdaff2807a44ab7dfbbe16bb7a3d3677946d32d ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 4b9d59bf3f87caf3db9cfee055f052c9c988ac20 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-393"></a>
### 393. N6 / ` build: bump version to 0.20.0-rc3 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 4b9d59bf3f87caf3db9cfee055f052c9c988ac20 ` → ` 7cedd4a07a90ab245e401db0828187550436f4b1 `。
  原证据引用：` 71ec973a0160c349cec14dcdf834357bcea44ea8 ` → ` 132f4a300ee763ded8d39f59ef57db32e8ef80f0 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 7b5eddb314e66f4fe69418fc3ae1ffede42d7969 ` 和原目标 ` 6080219d9e6526fdc74283bf5a7c9cbd0991ae9c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 7cedd4a07a90ab245e401db0828187550436f4b1 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-394"></a>
### 394. N6 / ` render/vulkan: introduce buffer_import_sync_file() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/renderer.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 7cedd4a07a90ab245e401db0828187550436f4b1 ` → ` 9e63f64733930596fb0f1045dd01c4519d22809a `。
  原证据引用：` 132f4a300ee763ded8d39f59ef57db32e8ef80f0 ` → ` 061f2ae64cb5f12815b8f435d3aefa368bbc1fac `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 6dc4affecbb95c861c13b134c04c55030270fc69 ` 和原目标 ` be16d8319886d710a4914a354c12f361254ded89 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 9e63f64733930596fb0f1045dd01c4519d22809a `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-395"></a>
### 395. N6 / ` render/vulkan: take render pass in vulkan_sync_render_buffer() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/renderer.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 9e63f64733930596fb0f1045dd01c4519d22809a ` → ` 8576c5392fba0fa7a4e4e732620db3461a5f1381 `。
  原证据引用：` 061f2ae64cb5f12815b8f435d3aefa368bbc1fac ` → ` 62be5c466232439260118f9cb58e389a96cde7f1 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` e567d0eb4f588c0bff923695dda75da1ef184a6d ` 和原目标 ` b82ea03c515165226ea0ad0dab87ce74ec71031f ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 8576c5392fba0fa7a4e4e732620db3461a5f1381 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-396"></a>
### 396. N6 / ` render/vulkan: fix missing DMA-BUF implicit read fence for textures `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/renderer.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 8576c5392fba0fa7a4e4e732620db3461a5f1381 ` → ` 95aeffdc7a1813465336dfb4c76db46db1a485e7 `。
  原证据引用：` 62be5c466232439260118f9cb58e389a96cde7f1 ` → ` 4d0eae6f8fc7b67ed0229d61511909c2d6621a9d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` fcb7f7e59ffaf681611e8cc382e3bdda2158e2ed ` 和原目标 ` 56e08fd636126682eabe759edaeeae7e689f3c92 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 95aeffdc7a1813465336dfb4c76db46db1a485e7 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-397"></a>
### 397. N6 / ` render/vulkan: introduce buffer_export_sync_file() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/renderer.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 95aeffdc7a1813465336dfb4c76db46db1a485e7 ` → ` 265af3e9d95d4d4774d9e5089fa69fd63c35b15d `。
  原证据引用：` 4d0eae6f8fc7b67ed0229d61511909c2d6621a9d ` → ` c7e62356929d5e11346e4a5824dfb0daa401da88 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` b13cce374175a427ad3f8d0e050c89f9b99c0e87 ` 和原目标 ` 8b0062b6a2248f443082e8eb0221a6c7f6d238fc ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 265af3e9d95d4d4774d9e5089fa69fd63c35b15d `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-398"></a>
### 398. N6 / ` render/vulkan: add "acquire" to vulkan_sync_foreign_texture() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/renderer.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 265af3e9d95d4d4774d9e5089fa69fd63c35b15d ` → ` 7f5bde4a8c62fa986d487ba35f85d7daf5b7c8cf `。
  原证据引用：` c7e62356929d5e11346e4a5824dfb0daa401da88 ` → ` b5290cf0547594113da1a1587eeb15187e58cdd2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 58eb62c4764ed0a1d1e40db3ee56f1d4c9767b4c ` 和原目标 ` 3c20b5d759f1f535e93ba0036d6537991af23241 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 7f5bde4a8c62fa986d487ba35f85d7daf5b7c8cf `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-399"></a>
### 399. N6 / ` render/vulkan: fix missing DMA-BUF implicit write fence for render buffer `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/render/vulkan/pass.c `、` 3rdparty/wlroots/render/vulkan/renderer.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 7f5bde4a8c62fa986d487ba35f85d7daf5b7c8cf ` → ` 871c4fb99a1ea849e53aa59bbc35e081043ec4d8 `。
  原证据引用：` b5290cf0547594113da1a1587eeb15187e58cdd2 ` → ` 8d4679e0fb4bb2bb2f16475ec2d36dd81a4e060d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` be50944f57d106eff1ca25b152998092a100eaad ` 和原目标 ` 2de7af1260aaeac677e2483ea56667df9c0b0248 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 871c4fb99a1ea849e53aa59bbc35e081043ec4d8 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-400"></a>
### 400. N6 / ` scene/layer_shell_v1: Add support for exclusive_edge `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/layer_shell_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 871c4fb99a1ea849e53aa59bbc35e081043ec4d8 ` → ` 5e75ffecb8ad30ad876fb450e821237078423da9 `。
  原证据引用：` 8d4679e0fb4bb2bb2f16475ec2d36dd81a4e060d ` → ` 68551a9aa81d21179886dc1105ba1c45cc36ba20 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 71a5ae7444c554dda9a5c661aea316df073ae019 ` 和原目标 ` 686d1eeb2510e06c239bbec9ccbfc465ae3ff4f5 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 5e75ffecb8ad30ad876fb450e821237078423da9 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-401"></a>
### 401. N6 / ` treewide: fix typos `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/drm/drm.c `、` 3rdparty/wlroots/backend/wayland/seat.c `、` 3rdparty/wlroots/include/render/color.h `、` 3rdparty/wlroots/include/render/vulkan.h `、` 3rdparty/wlroots/include/wlr/xcursor.h `、` 3rdparty/wlroots/render/egl.c `、` 3rdparty/wlroots/render/pixman/pass.c `、` 3rdparty/wlroots/render/vulkan/shaders/common.vert `、` 3rdparty/wlroots/render/vulkan/texture.c `、` 3rdparty/wlroots/render/vulkan/vulkan.c `、` 3rdparty/wlroots/tinywl/tinywl.c `、` 3rdparty/wlroots/types/scene/wlr_scene.c `、` 3rdparty/wlroots/util/array.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 5e75ffecb8ad30ad876fb450e821237078423da9 ` → ` 8db8ef9e197d0dbca7e8066409d9b86538dcca5a `。
  原证据引用：` 68551a9aa81d21179886dc1105ba1c45cc36ba20 ` → ` aa7882005cc00a688a5ac6783f0406291a2cb74e `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` e8c9c2245a2eaf584b2f2de3d009ca906b437da9 ` 和原目标 ` f02e3d42923ff649c48d09bac936efdb68996ea0 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 8db8ef9e197d0dbca7e8066409d9b86538dcca5a `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-402"></a>
### 402. N6 / ` xwayland: fix memory leak on pipe() failure `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/selection/outgoing.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 8db8ef9e197d0dbca7e8066409d9b86538dcca5a ` → ` 0bc5807427508aa883748b18bb50d8f8f0e09977 `。
  原证据引用：` aa7882005cc00a688a5ac6783f0406291a2cb74e ` → ` 88d04ea9774e6a5fd44082f538b3ba5a342b355a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` e034d859f2f76e51771de6558652ca570c0778f0 ` 和原目标 ` a3c5600b1ef00a24675deb590d188ed89d3d6a85 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 0bc5807427508aa883748b18bb50d8f8f0e09977 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-403"></a>
### 403. N6 / ` render/gles: use optimized clears for unblended rects `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/gles2/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 0bc5807427508aa883748b18bb50d8f8f0e09977 ` → ` f560e21d0017973b83a18d901323e0e3d7ba0dab `。
  原证据引用：` 88d04ea9774e6a5fd44082f538b3ba5a342b355a ` → ` 1cac48ccc44691f35bc0b6db04b869f3aa94b77a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` e06bfb9853fc7bb854d7e9cad4d8728574384d52 ` 和原目标 ` ec559da748351da00f8aaec553edc202c978164f ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` f560e21d0017973b83a18d901323e0e3d7ba0dab `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-404"></a>
### 404. N6 / ` screencopy: simplify capture error handling `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_screencopy_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` f560e21d0017973b83a18d901323e0e3d7ba0dab ` → ` 920cc024980d0416ba1378022bf3cc98b4b920ef `。
  原证据引用：` 1cac48ccc44691f35bc0b6db04b869f3aa94b77a ` → ` 99c09ccaecf99b89495ea5ee159c6f5d7e53389f `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 4fa410097e83f574ba669117f79d6d20e42f5f43 ` 和原目标 ` 730d2b54ab610f6ae813973c159b6bee48ec1bd0 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 920cc024980d0416ba1378022bf3cc98b4b920ef `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-405"></a>
### 405. N6 / ` build: bump version to 0.20.0-rc4 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 920cc024980d0416ba1378022bf3cc98b4b920ef ` → ` 83a84e8d88b01f6943e14850e01691868697cf0f `。
  原证据引用：` 99c09ccaecf99b89495ea5ee159c6f5d7e53389f ` → ` 6b093b0788885252fd5582b2639d10ec1ec1597e `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` f73f0f111c1ccd89fb7adc63f0fd1b0e70a5e98a ` 和原目标 ` a6bc6ac8c76b57aaf40449a4b725f551100f00f2 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 83a84e8d88b01f6943e14850e01691868697cf0f `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-406"></a>
### 406. N6 / ` image_capture_source/output: Update constraints on enable `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/ext_image_capture_source_v1/output.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 83a84e8d88b01f6943e14850e01691868697cf0f ` → ` b67f37056da7b6a19acff7700a5801d9e4fd504c `。
  原证据引用：` 6b093b0788885252fd5582b2639d10ec1ec1597e ` → ` 5a5e7f179b8ccfb795fd6a3b80d1357d4bc6dde8 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` c1458dcbc931cf644ca59b30012cb877905b4bb4 ` 和原目标 ` fc1520c1f57927debc74c75b682b7612dd6f1d7e ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` b67f37056da7b6a19acff7700a5801d9e4fd504c `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-407"></a>
### 407. N6 / ` ci: update dalligi upstream repo `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/.gitlab-ci.yml `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` b67f37056da7b6a19acff7700a5801d9e4fd504c ` → ` 8cdcff973d7c8e49b6f8d104ce674306601f4d1b `。
  原证据引用：` 5a5e7f179b8ccfb795fd6a3b80d1357d4bc6dde8 ` → ` 887a735dd50eca595d09d42b86e8c7c855620403 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` fbb806fdafe8c84afae72234394ae5856859456f ` 和原目标 ` 60d5b63b71cb2197b29e95a4d3753947f8bd3503 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 8cdcff973d7c8e49b6f8d104ce674306601f4d1b `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-408"></a>
### 408. N6 / ` scene: fix color format compare `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/surface.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 8cdcff973d7c8e49b6f8d104ce674306601f4d1b ` → ` d1b8a1997bd4d5f877cd87c52beb590574000100 `。
  原证据引用：` 887a735dd50eca595d09d42b86e8c7c855620403 ` → ` 3860cd1a6c8014cb745045bf3e2ddf002cd9c77a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 085c0c51de465e449d6ac15aae047f42b44c2b25 ` 和原目标 ` c4e674a790a9f9c619a7bf8681b8d90cfceb54c8 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` d1b8a1997bd4d5f877cd87c52beb590574000100 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-409"></a>
### 409. N6 / ` util/box: Use integer min/max for intersection `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/util/box.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` d1b8a1997bd4d5f877cd87c52beb590574000100 ` → ` a20ab762a766ef08afc1bd7eb23265f46cc96baa `。
  原证据引用：` 3860cd1a6c8014cb745045bf3e2ddf002cd9c77a ` → ` e1db4e5abd80ad16c82f182ca9e584bfcf496922 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 944566dec88e50356d2bea6ced447771a84af8ff ` 和原目标 ` 84fefc34c8eaa8d4b6e46312446af074804d7c4d ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` a20ab762a766ef08afc1bd7eb23265f46cc96baa `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-410"></a>
### 410. N6 / ` backend/x11: ignore DestroyNotify events `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/x11/backend.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` a20ab762a766ef08afc1bd7eb23265f46cc96baa ` → ` 0edf9f948fe7ba91d9e6f0a604b9416bbd954982 `。
  原证据引用：` e1db4e5abd80ad16c82f182ca9e584bfcf496922 ` → ` 6327c5da8baddfc2c1205595f2d5df9a6f902fd5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 2455271ec8bfd1f0b41d0f3b8fbb2a516572e15d ` 和原目标 ` b68ee3a668800b79966f2dada487a2189288f9a1 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 0edf9f948fe7ba91d9e6f0a604b9416bbd954982 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-411"></a>
### 411. N6 / ` wlr-export-dmabuf-unstable-v1: fix typo `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/protocol/wlr-export-dmabuf-unstable-v1.xml `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 0edf9f948fe7ba91d9e6f0a604b9416bbd954982 ` → ` 04c0f206359fa1ae4b917cfad84728cf142e80c4 `。
  原证据引用：` 6327c5da8baddfc2c1205595f2d5df9a6f902fd5 ` → ` 4ebc94fe3527fe73fa2c08a123316525950a0954 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 7d8d255dd2f75ed9588c2b77d31ce3e5ae23a799 ` 和原目标 ` 08214f9dea9ba8300e548a0dd4bd380552e6b79d ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 04c0f206359fa1ae4b917cfad84728cf142e80c4 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-412"></a>
### 412. N6 / ` scene: avoid redundant wl_surface.enter/leave events `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_scene.h `、` 3rdparty/wlroots/types/scene/surface.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 04c0f206359fa1ae4b917cfad84728cf142e80c4 ` → ` ae39e2780a8f13cf911243603bc5ce57a8a0ea49 `。
  原证据引用：` 4ebc94fe3527fe73fa2c08a123316525950a0954 ` → ` b89ec9a6609741387c9c54cc55202075a91e0449 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 03dea01bc170d9a4a5208cb6f0312994a882d957 ` 和原目标 ` 35c7564da9baf0590ceefcfe7baf6aae88f550f4 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` ae39e2780a8f13cf911243603bc5ce57a8a0ea49 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-413"></a>
### 413. N6 / ` scene: use wl_list_for_each_safe to iterate outputs `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/surface.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` ae39e2780a8f13cf911243603bc5ce57a8a0ea49 ` → ` 57f43265cd80a4a93c1acfb5a5a06433a6c9340d `。
  原证据引用：` b89ec9a6609741387c9c54cc55202075a91e0449 ` → ` 456beb1534566e28cb0e18349cb6b694e254d8c2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` bd247488a513aa70965ffd13d3c3b313b33e8523 ` 和原目标 ` d7f86675ca9471772f09a126e0b2a41166530b4f ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 57f43265cd80a4a93c1acfb5a5a06433a6c9340d `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-414"></a>
### 414. N6 / ` wlr_ext_image_copy_capture_v1: Fix crash when client creates a cursor session not implemented server side `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_ext_image_copy_capture_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 57f43265cd80a4a93c1acfb5a5a06433a6c9340d ` → ` 71a104b03b0b4cbef52df077e2213499b658aca9 `。
  原证据引用：` 456beb1534566e28cb0e18349cb6b694e254d8c2 ` → ` 1863be0193a231c22f195e002a6742d6eb9b6e59 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` abb07e9a8cab1e2c855e881ec4a216b7a4d8943f ` 和原目标 ` 7d600d624665262f79f93ec4c786dac784656f28 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 71a104b03b0b4cbef52df077e2213499b658aca9 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-415"></a>
### 415. N6 / ` virtual-keyboard: add wlr_virtual_keyboard_v1_from_resource() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_virtual_keyboard_v1.h `、` 3rdparty/wlroots/types/wlr_virtual_keyboard_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 71a104b03b0b4cbef52df077e2213499b658aca9 ` → ` 74ff1c28be06ca3d8d4ae3c680d0a9d03d2d20dc `。
  原证据引用：` 1863be0193a231c22f195e002a6742d6eb9b6e59 ` → ` 39535b3b1935fb8934cfb1bcc7aa276d0d010f39 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` f42de4aad659d7cbc7d3cafe1ea574c3fed1898b ` 和原目标 ` 5385277aea0d12a1279726f84255d47e8ad60861 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 74ff1c28be06ca3d8d4ae3c680d0a9d03d2d20dc `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-416"></a>
### 416. N6 / ` virtual-keyboard: handle seat destroy `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_virtual_keyboard_v1.h `、` 3rdparty/wlroots/types/wlr_virtual_keyboard_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 74ff1c28be06ca3d8d4ae3c680d0a9d03d2d20dc ` → ` 2edb7a0c08413a03a3cd58cdc9e1ba7c20602bde `。
  原证据引用：` 39535b3b1935fb8934cfb1bcc7aa276d0d010f39 ` → ` d55bace60be798b20d5f866f69f9932b27880867 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` e8a3639bab3b83ff21a238ff49e7d92f1ff0acbb ` 和原目标 ` 7e00b74d0656551b424e50fb37035e1a136293f1 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 2edb7a0c08413a03a3cd58cdc9e1ba7c20602bde `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-417"></a>
### 417. N6 / ` render/drm_syncobj: add wlr_drm_syncobj_timeline_signal() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/render/drm_syncobj.h `、` 3rdparty/wlroots/render/drm_syncobj.c `、` 3rdparty/wlroots/types/wlr_linux_drm_syncobj_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 2edb7a0c08413a03a3cd58cdc9e1ba7c20602bde ` → ` c67cefc9d06c5fabfde6c68ca23f6c830b412cd8 `。
  原证据引用：` d55bace60be798b20d5f866f69f9932b27880867 ` → ` 722de85483002c44e2e037e10e325d7766dac1bb `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 0b88a499773b71f6be1d3eae9b3a56fe59b1070d ` 和原目标 ` c1df83045815aa35ea14b27bb63a91941e5eeacc ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` c67cefc9d06c5fabfde6c68ca23f6c830b412cd8 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-418"></a>
### 418. N6 / ` scene: add buffer release point to 'sample' event `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_scene.h `、` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` c67cefc9d06c5fabfde6c68ca23f6c830b412cd8 ` → ` 751200abe04f882d16899eaebadba3c2e2f18276 `。
  原证据引用：` 722de85483002c44e2e037e10e325d7766dac1bb ` → ` b9393bed06b25a190c7483f38d6c653faacf774e `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 327493f4f869e1dc4a9dbb90df8d698d8e4d45cd ` 和原目标 ` 15e8139968d68a14ec47147e270c17a77174378f ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 751200abe04f882d16899eaebadba3c2e2f18276 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-419"></a>
### 419. N6 / ` drm/syncobj: add timeline point merger utility `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/render/drm_syncobj_merger.h `、` 3rdparty/wlroots/render/drm_syncobj_merger.c `、` 3rdparty/wlroots/render/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 751200abe04f882d16899eaebadba3c2e2f18276 ` → ` 221afc1ec9145f235b5e952d604479c8a41adea3 `。
  原证据引用：` b9393bed06b25a190c7483f38d6c653faacf774e ` → ` 1700418df8a8d0f0e6b8c8e70716e5eda892fe7f `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 4a57045bea78cb348fcf06add4ca8c33bc962014 ` 和原目标 ` 7d4614279767a0ccd62534bc756bb9eb145ceda8 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 221afc1ec9145f235b5e952d604479c8a41adea3 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-420"></a>
### 420. N6 / ` linux_drm_syncobj_v1: add release point accumulation `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_linux_drm_syncobj_v1.h `、` 3rdparty/wlroots/types/wlr_linux_drm_syncobj_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 221afc1ec9145f235b5e952d604479c8a41adea3 ` → ` def7870af55525af2332c6202404140212f591b7 `。
  原证据引用：` 1700418df8a8d0f0e6b8c8e70716e5eda892fe7f ` → ` 997dcee51e7aa6924b6cb3fbef7049f33e1a8d20 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 07b20196d39dfeea14c19ad20980bcefbeccf298 ` 和原目标 ` e62895ea40628aa4f3bd35a1e66b995b942027f0 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` def7870af55525af2332c6202404140212f591b7 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-421"></a>
### 421. N6 / ` scene: transfer sample syncobj to client timeline `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/surface.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` def7870af55525af2332c6202404140212f591b7 ` → ` ac9d0debfcfe2105c4e9141f22c8283be71a59ac `。
  原证据引用：` 997dcee51e7aa6924b6cb3fbef7049f33e1a8d20 ` → ` 6ac1a87c3d842e9492dff84be3ba2793e0237067 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ea645b18740f3435025b713223590b9ffb58d7ec ` 和原目标 ` 09334d837749f4b1347ba46aa2052710bf4b6d64 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` ac9d0debfcfe2105c4e9141f22c8283be71a59ac `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-422"></a>
### 422. N6 / ` backend/drm: properly delay syncobj signalling `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/drm/atomic.c `、` 3rdparty/wlroots/backend/drm/drm.c `、` 3rdparty/wlroots/include/backend/drm/drm.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` ac9d0debfcfe2105c4e9141f22c8283be71a59ac ` → ` 18f0ee6aaf8ed52f8222ae1a79e064af7b36287c `。
  原证据引用：` 6ac1a87c3d842e9492dff84be3ba2793e0237067 ` → ` 2e243c0eaee56c069be1b2dc69228f76ff9d4221 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 29005752b1cb2fd500f319609110aa881adcaa64 ` 和原目标 ` b7f0a618e6eda44578d9dadd6d1ec97776e6a4a6 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 18f0ee6aaf8ed52f8222ae1a79e064af7b36287c `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-423"></a>
### 423. N6 / ` output/drm: don't use OUT_FENCE_PTR `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/backend/drm/atomic.c `、` 3rdparty/wlroots/backend/drm/drm.c `、` 3rdparty/wlroots/backend/drm/libliftoff.c `、` 3rdparty/wlroots/include/backend/drm/drm.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 18f0ee6aaf8ed52f8222ae1a79e064af7b36287c ` → ` adb440b017e6478e60fdad0d71000a832da0f038 `。
  原证据引用：` 2e243c0eaee56c069be1b2dc69228f76ff9d4221 ` → ` 92b126978d965c78aeb0d33595b8a001f14144f1 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 5b85ed5b09fbda6407a68416c2b214be489907ed ` 和原目标 ` 21d623c51ac2f63e57c2596e94c9d2d9dd61982c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` adb440b017e6478e60fdad0d71000a832da0f038 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-424"></a>
### 424. N6 / ` build: bump version to 0.20.0-rc5 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` adb440b017e6478e60fdad0d71000a832da0f038 ` → ` ddb94bc3d2a730bae34e15eecde1f6cc200de95a `。
  原证据引用：` 92b126978d965c78aeb0d33595b8a001f14144f1 ` → ` d200db269847d16c4076d7edb18cf25df2841f85 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 04e824869922bcedc67865f904f8ff4b6c4cb076 ` 和原目标 ` 39d445f6d846bbf10072b4d9de63ab8445bb0a7b ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` ddb94bc3d2a730bae34e15eecde1f6cc200de95a `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-425"></a>
### 425. N6 / ` color_management_v1: use early continue in surface loop `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` ddb94bc3d2a730bae34e15eecde1f6cc200de95a ` → ` 801b4a53c8ab63c650d3570f02547b966a19ab5c `。
  原证据引用：` d200db269847d16c4076d7edb18cf25df2841f85 ` → ` ab88b3297d1f405ae2f5af5f619ad4f138e192cd `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 2fad5dcfdcaf8394e118088173fc8be8ace13045 ` 和原目标 ` 80dde7bb92d302c8e764394f48446d001cc7d562 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 801b4a53c8ab63c650d3570f02547b966a19ab5c `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-426"></a>
### 426. N6 / ` color_management_v1: ignore surface update if no-op `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_color_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 801b4a53c8ab63c650d3570f02547b966a19ab5c ` → ` 73041cf13aa75e46881034b659ea107c0f07ed23 `。
  原证据引用：` ab88b3297d1f405ae2f5af5f619ad4f138e192cd ` → ` 35380a50bdd15b08b4af2a4ed4f10584dd90ad4b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` e03e943d4766a6c670ee77b1b315b3c30c33c9fd ` 和原目标 ` a7b199f58e15271c177e44a592647585d324ec6e ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 73041cf13aa75e46881034b659ea107c0f07ed23 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-427"></a>
### 427. N6 / ` linux_drm_syncobj_v1: fix handling of empty first commit `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_linux_drm_syncobj_v1.h `、` 3rdparty/wlroots/types/wlr_linux_drm_syncobj_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 73041cf13aa75e46881034b659ea107c0f07ed23 ` → ` 285827451be680a2aec040f35ff7bb7f69d56a85 `。
  原证据引用：` 35380a50bdd15b08b4af2a4ed4f10584dd90ad4b ` → ` 72986ba53dd9424ce04943d0d610617e406de66a `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 208e2d7f0c50b85095631b20db3ba8b451ae41a6 ` 和原目标 ` d2a5bf9897229a629cc17fe8b0371e5833086265 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 285827451be680a2aec040f35ff7bb7f69d56a85 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-428"></a>
### 428. N6 / ` render/vulkan: compile against vulkan 1.2 header `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/util.c `、` 3rdparty/wlroots/render/vulkan/vulkan.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 285827451be680a2aec040f35ff7bb7f69d56a85 ` → ` f2bc617902605dc61f4d0f974ef0cab55a9df869 `。
  原证据引用：` 72986ba53dd9424ce04943d0d610617e406de66a ` → ` 27be31e5c2a16be5a67be8fa50212e8bb0a6f653 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 11e27740fefae88af7cbb6349a388775882c7ec2 ` 和原目标 ` ffe8d89bfcb5af678da550c2b22030affda68421 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` f2bc617902605dc61f4d0f974ef0cab55a9df869 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-429"></a>
### 429. N6 / ` build: bump version to 0.20.0 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` f2bc617902605dc61f4d0f974ef0cab55a9df869 ` → ` 49d45b5e663f9c01aafa9744ce5baa902e9b41f7 `。
  原证据引用：` 27be31e5c2a16be5a67be8fa50212e8bb0a6f653 ` → ` 99331ac0b0a77576dc045311ce50067c01ed2bc5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 4963e7bc7daa0e2d29b546f10267bcf07569ef5c ` 和原目标 ` ff82c099c3e86b89982e0fdf952a935df2256868 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 49d45b5e663f9c01aafa9744ce5baa902e9b41f7 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-430"></a>
### 430. N6 / ` ext_image_capture_source_v1/scene: fix extents `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/ext_image_capture_source_v1/scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 49d45b5e663f9c01aafa9744ce5baa902e9b41f7 ` → ` 6f701cf92a9fc588e21ca9a6399ca7854cac5ab8 `。
  原证据引用：` 99331ac0b0a77576dc045311ce50067c01ed2bc5 ` → ` fcfeedea2cd87a7f181151fb3f98c515fd297ee7 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 5d445e265ea404db6e00eb30b1d9d8eb84572a16 ` 和原目标 ` 4a31dda7e981c006ed3cf93871a38a45b49b34de ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 6f701cf92a9fc588e21ca9a6399ca7854cac5ab8 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-431"></a>
### 431. N6 / ` toplevel_capture: allocate new_request argument on the stack `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/ext_image_capture_source_v1/foreign_toplevel.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 6f701cf92a9fc588e21ca9a6399ca7854cac5ab8 ` → ` 2d5d34f8df973c16d3f38f62de1a067cb7495693 `。
  原证据引用：` fcfeedea2cd87a7f181151fb3f98c515fd297ee7 ` → ` a3c46d22b234aff223e3ca26b8b4ebaaad5a32fa `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 252e508d682bfb3eaedd6aecab26a2ca8544d8f7 ` 和原目标 ` 16babc2c58bf89a1f2f7c570ed6d66b268b24a14 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 2d5d34f8df973c16d3f38f62de1a067cb7495693 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-432"></a>
### 432. N6 / ` wlr-foreign-toplevel-management: add new toplevels to end of list `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_foreign_toplevel_management_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 2d5d34f8df973c16d3f38f62de1a067cb7495693 ` → ` a636f27f7862039675c223bf9ebfb50c3cc2d0c7 `。
  原证据引用：` a3c46d22b234aff223e3ca26b8b4ebaaad5a32fa ` → ` ba722750335ddc4fb50d5a7fbad90ceaabac91d9 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` b5d62efc17b9809001ac767199218fd70f8f4224 ` 和原目标 ` d8e6ba152db4dd49d2708061103d011df80e37d0 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` a636f27f7862039675c223bf9ebfb50c3cc2d0c7 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-433"></a>
### 433. N6 / ` ext-foreign-toplevel-list: add new toplevels to end of list `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_ext_foreign_toplevel_list_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` a636f27f7862039675c223bf9ebfb50c3cc2d0c7 ` → ` c257768894ec34f39d8cefad646b002e37ac56c0 `。
  原证据引用：` ba722750335ddc4fb50d5a7fbad90ceaabac91d9 ` → ` a1496802c9811c10165ad7e2f2786c98dc5195d4 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` acb1a07ca29a1c96353095fc9400a636a8a586e8 ` 和原目标 ` 227ef5ae64503301cdccf0e6854a66335d770368 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` c257768894ec34f39d8cefad646b002e37ac56c0 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-434"></a>
### 434. N6 / ` wlr_ext_workspace_v1.c: add new workspaces to end of list `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_ext_workspace_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` c257768894ec34f39d8cefad646b002e37ac56c0 ` → ` feb1cef26c4453fa97f0a275b0000c6fdb2afb55 `。
  原证据引用：` a1496802c9811c10165ad7e2f2786c98dc5195d4 ` → ` 85b8be26bec1b0b8dde58a6639d2d92fc28e418e `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 1c5061d5dc556ab87e855e27891c85a53c132703 ` 和原目标 ` 796b30fac21594b039599e4e6c1c3d208ec8bd70 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` feb1cef26c4453fa97f0a275b0000c6fdb2afb55 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-435"></a>
### 435. N6 / ` wlr_virtual_keyboard_v1: specify size when creating keymap `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_virtual_keyboard_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` feb1cef26c4453fa97f0a275b0000c6fdb2afb55 ` → ` 22659b04f9f660e958a88ddab25e3b61dc5e9335 `。
  原证据引用：` 85b8be26bec1b0b8dde58a6639d2d92fc28e418e ` → ` e0fcd28156fb4716868480f8022945368d3f0815 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 777ed58419d07e51038195608bcbec544748985d ` 和原目标 ` 9b82130b8e017dcea7af067cf0443877eda12466 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 22659b04f9f660e958a88ddab25e3b61dc5e9335 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-436"></a>
### 436. N6 / ` render/pixman: fix bilinear filtering to match gles2 renderer `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/render/pixman/pass.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 22659b04f9f660e958a88ddab25e3b61dc5e9335 ` → ` 89ca6f8ed09564cf22b4b69a16636ec31f53fccf `。
  原证据引用：` e0fcd28156fb4716868480f8022945368d3f0815 ` → ` 23cd5be8bd531ba3466baf7b6acdd0fcb0eead8d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d2570147440a6707d9667d1ff7377f55dd91f8ab ` 和原目标 ` d76fa2257b552962f7b4153b97c7219947487c1a ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 89ca6f8ed09564cf22b4b69a16636ec31f53fccf `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-437"></a>
### 437. N6 / ` keyboard: fix modifiers event when no keymap set `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_keyboard.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 89ca6f8ed09564cf22b4b69a16636ec31f53fccf ` → ` 60598870cc5a4aedd0933a116f4422d4e80ab79b `。
  原证据引用：` 23cd5be8bd531ba3466baf7b6acdd0fcb0eead8d ` → ` ee94d0e5814fbbb28a696144e8f1092f6e5ee318 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 80eb79813fa825180bd2681247a272350b7b8d25 ` 和原目标 ` ee2482472ed3de57464ca4df949c7c253e980e53 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 60598870cc5a4aedd0933a116f4422d4e80ab79b `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-438"></a>
### 438. N6 / ` scene/surface: schedule on frame pacing output `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/surface.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 60598870cc5a4aedd0933a116f4422d4e80ab79b ` → ` 0ffb5f08fe99a00e97803d12d022459d7f265ac1 `。
  原证据引用：` ee94d0e5814fbbb28a696144e8f1092f6e5ee318 ` → ` 1ac830c42aad7fd68b0a91bf9f9253c7cabf4a89 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 41aec9d71f90c68323d4de15c2ddf6f16bdc1a37 ` 和原目标 ` f3793493efd419439ecd11d447cc046a89083f4b ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 0ffb5f08fe99a00e97803d12d022459d7f265ac1 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-439"></a>
### 439. N6 / ` wlr_compositor: Apply state before updating surface_damage `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_compositor.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 0ffb5f08fe99a00e97803d12d022459d7f265ac1 ` → ` 42e32ba3bd19b45bf2fcce549a386b423c5a2d34 `。
  原证据引用：` 1ac830c42aad7fd68b0a91bf9f9253c7cabf4a89 ` → ` b1f864d47863f92b8438e098fb86958043c75887 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 1afe33b15978c2682fd3a7d88e1191d4c8a01f60 ` 和原目标 ` bb107736385c281a5c8f0908624ee95ec3192cab ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 42e32ba3bd19b45bf2fcce549a386b423c5a2d34 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-440"></a>
### 440. N6 / ` linux_drm_syncobj_v1: fix memory leak `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/wlr_linux_drm_syncobj_v1.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 42e32ba3bd19b45bf2fcce549a386b423c5a2d34 ` → ` 709120f658cd1714526102b92d56fbba1658f6ec `。
  原证据引用：` b1f864d47863f92b8438e098fb86958043c75887 ` → ` 6b6cd3b7812b977724b64654fc611cfd89083b9b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 7be5f6c58c2481e5289c114ca2cbfb61086eb7e8 ` 和原目标 ` 0b18e133721394a794947ad1dd91c13467c69242 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 709120f658cd1714526102b92d56fbba1658f6ec `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-441"></a>
### 441. N6 / ` scene: only send leave events to outputs with matching scene root `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/types/wlr_compositor.h `、` 3rdparty/wlroots/types/scene/surface.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 709120f658cd1714526102b92d56fbba1658f6ec ` → ` eeb918bc10d1fac474cf135e796a02d1e4477378 `。
  原证据引用：` 6b6cd3b7812b977724b64654fc611cfd89083b9b ` → ` 1fc920ed9fb5a4c05f8bc8926370061e80c6bb53 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ef86cc7863d65c84955e6e27d20cf65ac2ce3675 ` 和原目标 ` b2907742b1a468f9fc148b25ab2d2b2f8ed07403 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` eeb918bc10d1fac474cf135e796a02d1e4477378 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-442"></a>
### 442. N6 / ` build: bump version to 0.20.1 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` eeb918bc10d1fac474cf135e796a02d1e4477378 ` → ` e940bae765bd33bb6a21ca7b6bf8f0e72fe11b77 `。
  原证据引用：` 1fc920ed9fb5a4c05f8bc8926370061e80c6bb53 ` → ` 8b78ec9269832cdbf4443329482b7c3ed47416ec `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 99dfd9b78f387745f72c3c2ef964b258561d2fd9 ` 和原目标 ` d7d8065062d85b5c7399a1ac44220ce2f2565177 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` e940bae765bd33bb6a21ca7b6bf8f0e72fe11b77 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-443"></a>
### 443. N6 / ` xwayland/selection: stop using VLAs for MIME type atom lists `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/selection/dnd.c `、` 3rdparty/wlroots/xwayland/selection/outgoing.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` e940bae765bd33bb6a21ca7b6bf8f0e72fe11b77 ` → ` e23fbc92e357e141b51ae7b6c772ad5672c97da4 `。
  原证据引用：` 8b78ec9269832cdbf4443329482b7c3ed47416ec ` → ` b204d53215683ba45201a5f00bf49a007707268d `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` efcf521d9e167344a0eaa88411323e0a682b4352 ` 和原目标 ` d36822a006491fa6250035d9a0afe3d7f8cb5b91 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` e23fbc92e357e141b51ae7b6c772ad5672c97da4 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-444"></a>
### 444. N6 / ` xwayland: use const pointers for xcb_get_property_value() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/selection/incoming.c `、` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` e23fbc92e357e141b51ae7b6c772ad5672c97da4 ` → ` a3787782e27d50f6b54c87f74ffeb59ad43bdb6f `。
  原证据引用：` b204d53215683ba45201a5f00bf49a007707268d ` → ` cec0549b6d67a28d7d16595d59f357cb00920739 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` c72ebde4606fda987130454c43e3619dab48c9e0 ` 和原目标 ` 0f8d30e6c291687420724c6aa6b6cceb3356bafe ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` a3787782e27d50f6b54c87f74ffeb59ad43bdb6f `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-445"></a>
### 445. N6 / ` xwayland/xwm: fix out-of-bounds strndup() in read_surface_class() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` a3787782e27d50f6b54c87f74ffeb59ad43bdb6f ` → ` 598061603960e0fc9cb0f29d2b7644c90d65eeeb `。
  原证据引用：` cec0549b6d67a28d7d16595d59f357cb00920739 ` → ` 71c40bdb266ce3423486aa3dab16d48557a47469 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d1834b51b4e9dcfb18351dece8769fe81bb2d1bb ` 和原目标 ` 2b57bf34583100590a4d0025ff4605ca3bd061fe ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 598061603960e0fc9cb0f29d2b7644c90d65eeeb `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-446"></a>
### 446. N6 / ` xwayland/xwm: pluralize array variable in read_surface_net_wm_state() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 598061603960e0fc9cb0f29d2b7644c90d65eeeb ` → ` ea61afcf19fae29d5368ea378e967adae15a4f60 `。
  原证据引用：` 71c40bdb266ce3423486aa3dab16d48557a47469 ` → ` 08cb77a53d89b49d1216ce4c34c0028d6de3bb93 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 8a3d1b8a4424bacf3f5beabde5ec66983ce8dca0 ` 和原目标 ` f66adc9553727f68cba1d5dd89d1df47679906ca ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` ea61afcf19fae29d5368ea378e967adae15a4f60 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-447"></a>
### 447. N6 / ` xwayland: stop using xcb_get_property_reply_t.value_len `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/selection/incoming.c `、` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` ea61afcf19fae29d5368ea378e967adae15a4f60 ` → ` 5e3135a80a99e2c0bc90059db62fbbd3789b51c2 `。
  原证据引用：` 08cb77a53d89b49d1216ce4c34c0028d6de3bb93 ` → ` a1cc7cd3654f222622fbfad7d04460a450a8b8e1 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 4dad66cf6f99303e211dabc0e72c9f00e0c4c93d ` 和原目标 ` 2017cb12903cfa0dcdc30c23f02d6f14e95b2517 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 5e3135a80a99e2c0bc90059db62fbbd3789b51c2 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-448"></a>
### 448. N6 / ` xwayland/xwm: align WL_SURFACE_ID error message with WL_SURFACE_SERIAL `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 5e3135a80a99e2c0bc90059db62fbbd3789b51c2 ` → ` 34335213c24f776e5aeaf43984c3f85546b36f05 `。
  原证据引用：` a1cc7cd3654f222622fbfad7d04460a450a8b8e1 ` → ` 5443bb9539e70d9f9255f4e0695339b5b3405cb4 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` aec82dd30308ad1f6aea17b4bccc363cd6b9c73c ` 和原目标 ` 1358414a1b59ce5c89b85254a966abd231cf8c8d ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 34335213c24f776e5aeaf43984c3f85546b36f05 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-449"></a>
### 449. N6 / ` xwayland/xwm: expand comment about WL_SURFACE_ID event ordering `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 34335213c24f776e5aeaf43984c3f85546b36f05 ` → ` aa99c2ca8163855cb96c26eb38d88bc30e692a1e `。
  原证据引用：` 5443bb9539e70d9f9255f4e0695339b5b3405cb4 ` → ` 4b649ae37a673c0e6f2c21a327e8e1b48c5eb2bb `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 63790e1d8cd454f69947f141dbfc403844cc420e ` 和原目标 ` 99739f3297ad1795edae807f5a5bfcc90dda8114 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` aa99c2ca8163855cb96c26eb38d88bc30e692a1e `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-450"></a>
### 450. N6 / ` xwayland/xwm: check whether surface is already associated for WL_SURFACE_ID `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` aa99c2ca8163855cb96c26eb38d88bc30e692a1e ` → ` e2111058e5f8e167bc1a6fdf4606cf21ee33649c `。
  原证据引用：` 4b649ae37a673c0e6f2c21a327e8e1b48c5eb2bb ` → ` 1ae941b1604de38c26eefce0eb9eb04bb39f6931 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 1715ce5d5e91628b9323c096429781245c08b582 ` 和原目标 ` 26ffbacee0d75dd35ff5e73976fc3b34578d9309 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` e2111058e5f8e167bc1a6fdf4606cf21ee33649c `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-451"></a>
### 451. N6 / ` xwayland/xwm: check object type in xwm_handle_surface_id_message() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` e2111058e5f8e167bc1a6fdf4606cf21ee33649c ` → ` 9aab36caa3b74f44cc82405dffc65fd33278f4cb `。
  原证据引用：` 1ae941b1604de38c26eefce0eb9eb04bb39f6931 ` → ` 9b58dc87f5bd250515f8981ca2875539aa57447e `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 9f4afb87e591bb33912e3d7278cf49d6edf6b287 ` 和原目标 ` 16ec894425bd02aec658d9ea9e5bd0ea227f53d6 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 9aab36caa3b74f44cc82405dffc65fd33278f4cb `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-452"></a>
### 452. N6 / ` xwayland/xwm: check WM_TRANSIENT_FOR length `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 9aab36caa3b74f44cc82405dffc65fd33278f4cb ` → ` 8f595393af06f839801a7465076ac542b3f285c5 `。
  原证据引用：` 9b58dc87f5bd250515f8981ca2875539aa57447e ` → ` 39bf76ba2561244986f81dbc416b78eb15b65a79 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 39e7a61b472519868038242f95335616ba8f5b8e ` 和原目标 ` 346d04c02b7decf5bcda494718f3fd9b4742db3b ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 8f595393af06f839801a7465076ac542b3f285c5 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-453"></a>
### 453. N6 / ` xwayland: emit set_parent signal when parent is destroyed `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/xwm.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 8f595393af06f839801a7465076ac542b3f285c5 ` → ` 21064eaf19346bedd9b08b59a8c8b246bff79225 `。
  原证据引用：` 39bf76ba2561244986f81dbc416b78eb15b65a79 ` → ` 3785c332db0dafc2f31689005de3fcf013415aa9 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d003741eaa4e1832e2554710175415628784c94b ` 和原目标 ` b2e2390027eba52b24a145fafa77b2497e0eed35 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 21064eaf19346bedd9b08b59a8c8b246bff79225 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-454"></a>
### 454. N6 / ` scene: don't send new dmabuf feedback after node disable `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 21064eaf19346bedd9b08b59a8c8b246bff79225 ` → ` 744b97d6ed80b2a8ccdb909d33274424d254dce8 `。
  原证据引用：` 3785c332db0dafc2f31689005de3fcf013415aa9 ` → ` 478d84aa08ee09ceafbd2ad96c71d6fbcbf95343 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 15bc8d04b8df33c82d0208c582e234e60aba60a0 ` 和原目标 ` 5ba1e67d993ccb39384f0d6dc7860cc17a4c8135 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 744b97d6ed80b2a8ccdb909d33274424d254dce8 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-455"></a>
### 455. N6 / ` drag: check dnd action and accepted on touch up `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/data_device/wlr_drag.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 744b97d6ed80b2a8ccdb909d33274424d254dce8 ` → ` 4e29cb94d91e391b442cc25324ebfab80ec88f37 `。
  原证据引用：` 478d84aa08ee09ceafbd2ad96c71d6fbcbf95343 ` → ` bc817082dde4c0cb31f50b140b89d8c97af24aa5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d37140d74ab9d0f8cb32f222ffbfd83937c0e891 ` 和原目标 ` 7ef7fd0722a31f08b18e9c591999a85939858e46 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 4e29cb94d91e391b442cc25324ebfab80ec88f37 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-456"></a>
### 456. N6 / ` xwayland:use size of the pointed type instead of pointer `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/xwayland/selection/incoming.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 4e29cb94d91e391b442cc25324ebfab80ec88f37 ` → ` cd806fbbf93285e3c6d1a4ea97dccb68d7bc4457 `。
  原证据引用：` bc817082dde4c0cb31f50b140b89d8c97af24aa5 ` → ` 7cacf98abe023616b2d29649a19f845cff796c0f `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d8829e42caefa988029a62148a9ababfe467640f ` 和原目标 ` d6a1e82a620a540f1d722070627f1b59f12548f1 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` cd806fbbf93285e3c6d1a4ea97dccb68d7bc4457 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-457"></a>
### 457. N6 / ` scene: intersect visible area with output layout in update_node_update_outputs() `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/types/scene/wlr_scene.c `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` cd806fbbf93285e3c6d1a4ea97dccb68d7bc4457 ` → ` 38147b44eafff95d519dd7d5023d277d7921ab0c `。
  原证据引用：` 7cacf98abe023616b2d29649a19f845cff796c0f ` → ` b7525e569deb150bb03718d220a8c5b2f6644990 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 5c661fd02bed08c4b2e6a633688d6d5c944842c5 ` 和原目标 ` 53b278677c0875a69d56bad11ab8342516bf69c1 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 38147b44eafff95d519dd7d5023d277d7921ab0c `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-458"></a>
### 458. N6 / ` security_context_v1: set CLOEXEC for client FDs `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/util/fd.h `、` 3rdparty/wlroots/types/wlr_security_context_v1.c `、` 3rdparty/wlroots/util/fd.c `、` 3rdparty/wlroots/util/meson.build `、` 3rdparty/wlroots/xwayland/server.c `、` 3rdparty/wlroots/xwayland/sockets.c `、` 3rdparty/wlroots/xwayland/sockets.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 38147b44eafff95d519dd7d5023d277d7921ab0c ` → ` 964e55ef572bac0b2187e711c93e3191b08b0d21 `。
  原证据引用：` b7525e569deb150bb03718d220a8c5b2f6644990 ` → ` 66f46e21d9388959996d78c8677885a2398a179b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` d85ecab59bfe36b18a00a728810df435e6f1543e ` 和原目标 ` 81affb7dd81c3ea0d9ccee3c535510ba6d047393 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 964e55ef572bac0b2187e711c93e3191b08b0d21 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-459"></a>
### 459. N6 / ` build: bump version to 0.20.2 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/meson.build `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 964e55ef572bac0b2187e711c93e3191b08b0d21 ` → ` 8f4ec1b09ba5f19cd70948f625fcedcfda774889 `。
  原证据引用：` 66f46e21d9388959996d78c8677885a2398a179b ` → ` e8aab674762dadfeb91495af8d7fcb80f8d38986 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 324909af3e2b1fda50896fe9863747fb6011ec9a ` 和原目标 ` 678c56baba4e20a4313980125ed37e131b6d6daa ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 8f4ec1b09ba5f19cd70948f625fcedcfda774889 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-460"></a>
### 460. N6 / ` Update '3rdparty/wlroots/' from upstream commit '88a869855742281c98c22cab9641b317b8d065ef' to 'd783533489e1f75d6886c2ab5c5960090ef268f8' `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` 3rdparty/wlroots/include/wlr/render/vulkan.h `、` 3rdparty/wlroots/include/wlr/types/wlr_data_device.h `、` 3rdparty/wlroots/render/vulkan/renderer.c `、` 3rdparty/wlroots/types/buffer/buffer.c `、` 3rdparty/wlroots/types/data_device/wlr_data_source.c `、` 3rdparty/wlroots/types/seat/wlr_seat_pointer.c `、` 3rdparty/wlroots/types/xdg_shell/wlr_xdg_popup.c `、` 3rdparty/wlroots/wlroots.syms `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 8f4ec1b09ba5f19cd70948f625fcedcfda774889 ` → ` 10beea71f6d2c09d6cec15d8b49425d3f6f8dfc4 `。
  原证据引用：` e8aab674762dadfeb91495af8d7fcb80f8d38986 ` → ` a8e5cac236bc01f7ce0d9aa782b588de857cc00b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` e4079612adb3e567c7f661dcb404663484817f39 ` 和原目标 ` b7824a49ddace87952f0aecf7ce6fd8443475ac9 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 10beea71f6d2c09d6cec15d8b49425d3f6f8dfc4 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-461"></a>
### 461. N6 / ` fix(wlroots): define HAVE_LINUX_SYNC_FILE for CMake builds `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` wlroots/CMakeLists.txt `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 10beea71f6d2c09d6cec15d8b49425d3f6f8dfc4 ` → ` 7d30760134a5ff722319b83d7d244b12fee87ea0 `。
  原证据引用：` a8e5cac236bc01f7ce0d9aa782b588de857cc00b ` → ` adb3af1b9100b411d9bcd95cb53b6dafd5312641 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 981ef4b18cbe7e908804e17bf7fd2ae4d65e6fca ` 和原目标 ` 750fdb3a14f7bb66237e336c15ade4baa1d266c0 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 7d30760134a5ff722319b83d7d244b12fee87ea0 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-462"></a>
### 462. N6 / ` fix: guard wlroots C99 array parameters in C++ headers `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/kernel/wlr_all.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 7d30760134a5ff722319b83d7d244b12fee87ea0 ` → ` 404c5a67a0aef52038b9729265843ff8b83410f9 `。
  原证据引用：` adb3af1b9100b411d9bcd95cb53b6dafd5312641 ` → ` 7fbd74467a473b0e8e93d700f32d539e6512a5d4 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 475f3cb6f5f21d0ecc059c6998e590a38f291560 ` 和原目标 ` 7bc4ddc002d64c60bf0f51e226913c87cae808f7 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 404c5a67a0aef52038b9729265843ff8b83410f9 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-463"></a>
### 463. N6 / ` feat(wlroots): upgrade vendored wlroots to 0.20.2 `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` wlroots/CMakeLists.txt `、` wlroots/UPSTREAM `、` wlroots/cmake/WlrootsProtocols.cmake `、` wlroots/cmake/WlrootsSources.cmake `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 404c5a67a0aef52038b9729265843ff8b83410f9 ` → ` cfbde75aa06eba39919406cb30bb2017be4e9c49 `。
  原证据引用：` 7fbd74467a473b0e8e93d700f32d539e6512a5d4 ` → ` 6abb97a1033a928c276bc96a943447564c90f5c1 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 06ab77c1664548ef90e1f953ff00e2d5dacea166 ` 和原目标 ` 6c588fd2b7299511a56b3ccc15055be531023b76 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` cfbde75aa06eba39919406cb30bb2017be4e9c49 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-464"></a>
### 464. N6 / ` feat(wlroots): adapt to wlroots 0.20.2 API changes `

- 本仓内容路径：` compositor/src/output/output.cpp `、` compositor/src/seat/helper.cpp `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/output/output.cpp `、` compositor/src/seat/helper.cpp `、` compositor/tests/test_manager_resource_lifecycle/main.cpp `、` compositor/tests/test_multi_seat/devicepathfixture.cpp `。
- 排除的来源路径：` 3rdparty/wlroots/render/vulkan/renderer.c `、` waylib/examples/tinywl/helper.cpp `、` waylib/src/server/CMakeLists.txt `、` waylib/src/server/protocols/ext_foreign_toplevel_image_capture_source.c `、` waylib/src/server/protocols/ext_foreign_toplevel_image_capture_source_manager_v1.h `、` waylib/src/server/protocols/private/winputmethodv2.cpp `、` waylib/src/server/protocols/private/wtextinputv3.cpp `、` waylib/src/server/qtquick/woutputhelper.cpp `、` waylib/src/server/utils/wextimagecapturesourcev1impl.cpp `、` waylib/src/server/utils/wextimagecapturesourcev1impl.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` cfbde75aa06eba39919406cb30bb2017be4e9c49 ` → ` db0ff5dca7fde5c57b7029842c6f42cba91235e8 `。
  原证据引用：` 6abb97a1033a928c276bc96a943447564c90f5c1 ` → ` 983dd5707d2e6cb2a59434062ed2b45036f99452 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ca160e1eb74ecb4f43102ac3f6463ab0e1a25137 ` 和原目标 ` 152281e9ebef1be22310b29b85741a12488955cc ` 查询。
- 原审核说明：` N6 原生 API 的本地测试调用方完整适配：WServer::stop 已销毁 display，保留三条资源各销毁一次的断言并显式检查 stop 后的空句柄，不再调度已销毁的事件循环；同时保留已审查的 wlr_all.h 头入口修正。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/543dce9a1873bd78b5654ce8587a889e10d20848.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` db0ff5dca7fde5c57b7029842c6f42cba91235e8 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-465"></a>
### 465. N6 / ` feat(ci): add deepin-community testing repo for wlroots 0.20.2 `

- 本仓内容路径：` .github/workflows/treeland-deepin-build.yml `、` .github/workflows/waylib-deepin-build.yml `。
- 实际改变：` .github/workflows/treeland-deepin-build.yml `、` .github/workflows/waylib-deepin-build.yml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` db0ff5dca7fde5c57b7029842c6f42cba91235e8 ` → ` db0ff5dca7fde5c57b7029842c6f42cba91235e8 `。
  原证据引用：` 983dd5707d2e6cb2a59434062ed2b45036f99452 ` → ` 983dd5707d2e6cb2a59434062ed2b45036f99452 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` eb6dfbebd9050ed78947d4e85ac28873d1e9b4c1 ` 和原目标 ` 2e9bb0e2e5ac181c8d834c0e6ff41d096df5c0fb ` 查询。

<a id="entry-466"></a>
### 466. N6 / ` fix(session): guard null active session in xwayland primary output sync `

- 本仓内容路径：` compositor/src/session/session.cpp `。
- 实际改变：` compositor/src/session/session.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` db0ff5dca7fde5c57b7029842c6f42cba91235e8 ` → ` db0ff5dca7fde5c57b7029842c6f42cba91235e8 `。
  原证据引用：` 983dd5707d2e6cb2a59434062ed2b45036f99452 ` → ` 983dd5707d2e6cb2a59434062ed2b45036f99452 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 726a9e57b3f9f56df4a5d81fc099e2e4f954b8c6 ` 和原目标 ` 5d74ce228c5389efbbd94bfc610122b4030538e5 ` 查询。

<a id="entry-467"></a>
### 467. N6 / ` feat: gate dev file installation behind TREELAND_INSTALL_DEV option (default OFF) `

- 本仓内容路径：` compositor/CMakeLists.txt `、` compositor/debian/control `、` compositor/debian/rules `、` compositor/debian/treeland-dev.install `、` compositor/misc/cmake/CMakeLists.txt `、` compositor/src/CMakeLists.txt `、` compositor/src/modules/capture/CMakeLists.txt `、` compositor/src/modules/personalization/CMakeLists.txt `。
- 实际改变：` 3rdparty/waylib-shared `、` CMakeLists.txt `、` compositor/CMakeLists.txt `、` compositor/debian/control `、` compositor/debian/rules `、` compositor/debian/treeland-dev.install `、` compositor/src/CMakeLists.txt `、` compositor/src/modules/capture/CMakeLists.txt `、` compositor/src/modules/personalization/CMakeLists.txt `。
- 排除的来源路径：` waylib/CMakeLists.txt `、` waylib/src/CMakeLists.txt `、` waylib/src/server/CMakeLists.txt `、` wlroots/CMakeLists.txt `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` db0ff5dca7fde5c57b7029842c6f42cba91235e8 ` → ` f5fd08be82b50f706813c6248e56142095fcd97c `。
  原证据引用：` 983dd5707d2e6cb2a59434062ed2b45036f99452 ` → ` 9f5ef46c65c4b5f4765468db73cf6368617841ba `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` f40f2fe7ba7daf686b3dbf352d592e56f9e182bc ` 和原目标 ` 1fd5f769397d97a65fceeddc7bd9b7597062d481 ` 查询。
- 原审核说明：` 在 P 根提前设置开发安装默认关闭，保留运行时真实库；保留已退役的 Treeland 兼容包删除状态，并对其缺失安装路径记录等价无操作。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/139051af09f25abf4fbc2b2d3737a6f282268a2c.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` f5fd08be82b50f706813c6248e56142095fcd97c `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-468"></a>
### 468. N6 / ` fix: remove redundant connectSeat loop (seatAdded signal already covers all seats) `

- 本仓内容路径：` compositor/src/seat/helper.cpp `。
- 实际改变：` compositor/src/seat/helper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` f5fd08be82b50f706813c6248e56142095fcd97c ` → ` f5fd08be82b50f706813c6248e56142095fcd97c `。
  原证据引用：` 9f5ef46c65c4b5f4765468db73cf6368617841ba ` → ` 9f5ef46c65c4b5f4765468db73cf6368617841ba `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 6d4772876759e122571b6ff409c476fe92865c5e ` 和原目标 ` 8c6c1b2aa89e2e5668403edf37503dfe382b4ab7 ` 查询。

<a id="entry-469"></a>
### 469. N6 / ` feat: support pointer-constraints protocol `

- 本仓内容路径：` compositor/REUSE.toml `、` compositor/src/CMakeLists.txt `、` compositor/src/core/rootsurfacecontainer.cpp `、` compositor/src/core/rootsurfacecontainer.h `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/src/seat/pointerconstraintsmanager.cpp `、` compositor/src/seat/pointerconstraintsmanager.h `、` compositor/tests/CMakeLists.txt `、` compositor/tests/test_protocol_pointerconstraints/CMakeLists.txt `、` compositor/tests/test_protocol_pointerconstraints/main.cpp `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/REUSE.toml `、` compositor/src/CMakeLists.txt `、` compositor/src/core/rootsurfacecontainer.cpp `、` compositor/src/core/rootsurfacecontainer.h `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/src/seat/pointerconstraintsmanager.cpp `、` compositor/src/seat/pointerconstraintsmanager.h `、` compositor/tests/CMakeLists.txt `、` compositor/tests/test_protocol_pointerconstraints/CMakeLists.txt `、` compositor/tests/test_protocol_pointerconstraints/main.cpp `。
- 排除的来源路径：` waylib/src/server/CMakeLists.txt `、` waylib/src/server/kernel/private/wcursor_p.h `、` waylib/src/server/kernel/wcursor.cpp `、` waylib/src/server/kernel/wcursor.h `、` waylib/src/server/kernel/wlr_all.h `、` waylib/src/server/kernel/wlr_fwd.h `、` waylib/src/server/protocols/WPointerConstraintsV1 `、` waylib/src/server/protocols/wpointerconstraintsv1.cpp `、` waylib/src/server/protocols/wpointerconstraintsv1.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` f5fd08be82b50f706813c6248e56142095fcd97c ` → ` 219f4dee7780fb7c2b056e62186266b606d075bd `。
  原证据引用：` 9f5ef46c65c4b5f4765468db73cf6368617841ba ` → ` 83365fc20abbfdb29b710446d5e3cc5fabc86efe `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` 4cd2c672c10ec0e3004c88bbd48a18ded22872bd ` 和原目标 ` bca2766cb19205e84846b44f5ece15c6c478bbb2 ` 查询。
- 原审核说明：` 接入指针约束策略和原始测试，测试链接实际 libdeckcompositor 目标，保留本地完整测试集合并增加当前来源的许可证条目；不更名 C++ 命名空间、不新增兼容库。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/b7d2ffd21cccc75e75d0d58d992232294c57804c.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 219f4dee7780fb7c2b056e62186266b606d075bd `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-470"></a>
### 470. N6 / ` chore: bump version to 0.9.0 `

- 本仓内容路径：` compositor/CMakeLists.txt `、` compositor/debian/changelog `。
- 实际改变：` compositor/CMakeLists.txt `、` compositor/debian/changelog `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 219f4dee7780fb7c2b056e62186266b606d075bd ` → ` 219f4dee7780fb7c2b056e62186266b606d075bd `。
  原证据引用：` 83365fc20abbfdb29b710446d5e3cc5fabc86efe ` → ` 83365fc20abbfdb29b710446d5e3cc5fabc86efe `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/parent-evidence.json`；以来源 ` ce57dab0259c33eb183589928249ef9e2be149af ` 和原目标 ` 77d487cedd0b1f1eabf1ec38ee744af3fe4a0930 ` 查询。
- 原审核说明：` 将 DeckCompositor 版本同步为 0.9.0，保留本地 project 名称、自动代码生成开关及项目说明，保留来源 changelog 完整内容。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/a6cea1c57039b25b2c1d5504b01300af5a221477.md)。

<a id="entry-471"></a>
### 471. N7 / ` fix: use wlr_xdg_toplevel_tag_v1 API instead of custom C implementation `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/CMakeLists.txt `、` waylib/src/server/kernel/wlr_all.h `、` waylib/src/server/protocols/wxdgtopleveltagmanager.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 219f4dee7780fb7c2b056e62186266b606d075bd ` → ` 65e42e24b4dfa9d2637862e589c43024853bdc95 `。
  原证据引用：` 83365fc20abbfdb29b710446d5e3cc5fabc86efe ` → ` 767ee8170341d0d20e1352afaaf95a9090a7ffe9 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` a0329cd13c3071d658cf6043c4884b0cbf8844ec ` 和原目标 ` 09bd655c5d38804169777a9d0aa52b2ff5322e4d ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 65e42e24b4dfa9d2637862e589c43024853bdc95 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-472"></a>
### 472. N7 / ` chore: clean up Qt < 6.8 compatibility code `

- 本仓内容路径：` compositor/examples/test_pinch_handler/main.cpp `、` compositor/src/effects/tsgradiusimagenode.cpp `、` compositor/src/modules/item-selector/itemselector.cpp `、` compositor/src/seat/helper.cpp `、` compositor/src/xsettings/xsettings.cpp `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/examples/test_pinch_handler/main.cpp `、` compositor/src/effects/tsgradiusimagenode.cpp `、` compositor/src/modules/item-selector/itemselector.cpp `、` compositor/src/seat/helper.cpp `、` compositor/src/xsettings/xsettings.cpp `。
- 排除的来源路径：` waylib/examples/tinywl/helper.cpp `、` waylib/examples/tinywl/surfacewrapper.cpp `、` waylib/src/server/platformplugin/qwlrootsintegration.cpp `、` waylib/src/server/platformplugin/qwlrootsintegration.h `、` waylib/src/server/platformplugin/qwlrootswindow.cpp `、` waylib/src/server/qtquick/private/wrenderbuffernode.cpp `、` waylib/src/server/qtquick/woutputrenderwindow.cpp `、` waylib/src/server/qtquick/wqmlcreator.cpp `、` waylib/src/server/qtquick/wquickobserver.cpp `、` waylib/src/server/qtquick/wquickobserver.h `、` waylib/src/server/qtquick/wrenderhelper.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 65e42e24b4dfa9d2637862e589c43024853bdc95 ` → ` b17f567f1f6ef94ce3a2cf2c5a87f77f1a58df59 `。
  原证据引用：` 767ee8170341d0d20e1352afaaf95a9090a7ffe9 ` → ` 6aea08e0bb8f4623b6c3ea294b4baa119e0922da `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` b9f6069fa3e1354091af377c9c9472fda290e2d8 ` 和原目标 ` f8f38e5af5ad8799bac9bf3bfe3331b63e91baa5 ` 查询。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 同一 Treeland 来源的 C / waylib-shared 目标：` b17f567f1f6ef94ce3a2cf2c5a87f77f1a58df59 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-473"></a>
### 473. N7 / ` feat(protocol-tests): add production Wayland protocol integration suite `

- 本仓内容路径：` compositor/.agents/skills/wayland-protocol-test/SKILL.md `、` .github/workflows/treeland-deepin-build.yml `、` compositor/src/CMakeLists.txt `、` compositor/src/core/treeland.cpp `、` compositor/src/core/treelandinit.cpp `、` compositor/src/core/treelandinit.h `、` compositor/src/core/windowpicker.cpp `、` compositor/src/core/windowpicker.h `、` compositor/src/main.cpp `、` compositor/src/modules/capture/capture.cpp `、` compositor/src/modules/capture/capture.h `、` compositor/src/modules/wallpaper/wallpapershellinterfacev1.cpp `、` compositor/src/plugins/lockscreen/qml/ShutdownButton.qml `、` compositor/src/plugins/multitaskview/qml/WindowSelectionGrid.qml `、` compositor/src/plugins/multitaskview/qml/WorkspaceSelectionList.qml `、` compositor/src/seat/helper.cpp `、` compositor/tests/CMakeLists.txt `、` compositor/tests/protocols/CMakeLists.txt `、` compositor/tests/protocols/INDEX.md `、` compositor/tests/protocols/README.md `、` compositor/tests/protocols/framework/ProtocolTest.cmake `、` compositor/tests/protocols/framework/README.md `、` compositor/tests/protocols/framework/client-connection.c `、` compositor/tests/protocols/framework/client-connection.h `、` compositor/tests/protocols/framework/protocol-test-entry.cpp `、` compositor/tests/protocols/framework/server-bridge-api.h `、` compositor/tests/protocols/framework/server-bridge.cpp `、` compositor/tests/protocols/framework/server-bridge.h `、` compositor/tests/protocols/framework/test-accounts-service.cpp `、` compositor/tests/protocols/framework/test-accounts-service.h `、` compositor/tests/protocols/framework/test-dconfig-service.cpp `、` compositor/tests/protocols/framework/test-dconfig-service.h `、` compositor/tests/protocols/framework/xdg-toplevel-client.c `、` compositor/tests/protocols/framework/xdg-toplevel-client.h `、` compositor/tests/protocols/protocol-specification-template.md `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v1/treeland-app-id-resolver-desktop-v1.c `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v1/treeland-app-id-resolver-desktop-v1.h `、` compositor/tests/protocols/treeland-app-id-resolver-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-app-id-resolver-v1/README.md `、` compositor/tests/protocols/treeland-app-id-resolver-v1/setup.cpp `、` compositor/tests/protocols/treeland-app-id-resolver-v1/treeland-app-id-resolver-v1.c `、` compositor/tests/protocols/treeland-app-id-resolver-v1/treeland-app-id-resolver-v1.h `、` compositor/tests/protocols/treeland-capture-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-capture-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-capture-desktop-v1/treeland-capture-desktop-v1.c `、` compositor/tests/protocols/treeland-capture-desktop-v1/treeland-capture-desktop-v1.h `、` compositor/tests/protocols/treeland-capture-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-capture-unstable-v1/README.md `、` compositor/tests/protocols/treeland-capture-unstable-v1/setup.cpp `、` compositor/tests/protocols/treeland-capture-unstable-v1/treeland-capture-unstable-v1.c `、` compositor/tests/protocols/treeland-capture-unstable-v1/treeland-capture-unstable-v1.h `、` compositor/tests/protocols/treeland-dde-shell-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-dde-shell-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-dde-shell-desktop-v1/treeland-dde-shell-desktop-v1.c `、` compositor/tests/protocols/treeland-dde-shell-desktop-v1/treeland-dde-shell-desktop-v1.h `、` compositor/tests/protocols/treeland-dde-shell-lockscreen-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-dde-shell-lockscreen-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-dde-shell-lockscreen-desktop-v1/treeland-dde-shell-lockscreen-desktop-v1.c `、` compositor/tests/protocols/treeland-dde-shell-lockscreen-desktop-v1/treeland-dde-shell-lockscreen-desktop-v1.h `、` compositor/tests/protocols/treeland-dde-shell-multitask-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-dde-shell-multitask-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-dde-shell-multitask-desktop-v1/treeland-dde-shell-multitask-desktop-v1.c `、` compositor/tests/protocols/treeland-dde-shell-multitask-desktop-v1/treeland-dde-shell-multitask-desktop-v1.h `、` compositor/tests/protocols/treeland-dde-shell-picker-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-dde-shell-picker-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-dde-shell-picker-desktop-v1/treeland-dde-shell-picker-desktop-v1.c `、` compositor/tests/protocols/treeland-dde-shell-picker-desktop-v1/treeland-dde-shell-picker-desktop-v1.h `、` compositor/tests/protocols/treeland-dde-shell-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-dde-shell-v1/README.md `、` compositor/tests/protocols/treeland-dde-shell-v1/setup.cpp `、` compositor/tests/protocols/treeland-dde-shell-v1/treeland-dde-shell-v1.c `、` compositor/tests/protocols/treeland-dde-shell-v1/treeland-dde-shell-v1.h `、` compositor/tests/protocols/treeland-ddm-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-ddm-v1/README.md `、` compositor/tests/protocols/treeland-ddm-v1/setup.cpp `、` compositor/tests/protocols/treeland-ddm-v1/treeland-ddm-v1.c `、` compositor/tests/protocols/treeland-ddm-v1/treeland-ddm-v1.h `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/README.md `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/setup.cpp `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/treeland-foreign-toplevel-manager-v1.c `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/treeland-foreign-toplevel-manager-v1.h `、` compositor/tests/protocols/treeland-input-manager-uinput-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-input-manager-uinput-v1/setup.cpp `、` compositor/tests/protocols/treeland-input-manager-uinput-v1/treeland-input-manager-uinput-v1.c `、` compositor/tests/protocols/treeland-input-manager-uinput-v1/treeland-input-manager-uinput-v1.h `、` compositor/tests/protocols/treeland-input-manager-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-input-manager-unstable-v1/README.md `、` compositor/tests/protocols/treeland-input-manager-unstable-v1/setup.cpp `、` compositor/tests/protocols/treeland-input-manager-unstable-v1/treeland-input-manager-unstable-v1.c `、` compositor/tests/protocols/treeland-input-manager-unstable-v1/treeland-input-manager-unstable-v1.h `、` compositor/tests/protocols/treeland-keyboard-state-notify-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-keyboard-state-notify-unstable-v1/README.md `、` compositor/tests/protocols/treeland-keyboard-state-notify-unstable-v1/setup.cpp `、` compositor/tests/protocols/treeland-keyboard-state-notify-unstable-v1/treeland-keyboard-state-notify-unstable-v1.c `、` compositor/tests/protocols/treeland-keyboard-state-notify-unstable-v1/treeland-keyboard-state-notify-unstable-v1.h `、` compositor/tests/protocols/treeland-output-manager-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-output-manager-v1/README.md `、` compositor/tests/protocols/treeland-output-manager-v1/setup.cpp `、` compositor/tests/protocols/treeland-output-manager-v1/treeland-output-manager-v1.c `、` compositor/tests/protocols/treeland-output-manager-v1/treeland-output-manager-v1.h `、` compositor/tests/protocols/treeland-personalization-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-personalization-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-personalization-desktop-v1/treeland-personalization-desktop-v1.c `、` compositor/tests/protocols/treeland-personalization-desktop-v1/treeland-personalization-desktop-v1.h `、` compositor/tests/protocols/treeland-personalization-manager-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-personalization-manager-v1/README.md `、` compositor/tests/protocols/treeland-personalization-manager-v1/setup.cpp `、` compositor/tests/protocols/treeland-personalization-manager-v1/treeland-personalization-manager-v1.c `、` compositor/tests/protocols/treeland-personalization-manager-v1/treeland-personalization-manager-v1.h `、` compositor/tests/protocols/treeland-prelaunch-splash-desktop-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-prelaunch-splash-desktop-v2/setup.cpp `、` compositor/tests/protocols/treeland-prelaunch-splash-desktop-v2/treeland-prelaunch-splash-desktop-v2.c `、` compositor/tests/protocols/treeland-prelaunch-splash-desktop-v2/treeland-prelaunch-splash-desktop-v2.h `、` compositor/tests/protocols/treeland-prelaunch-splash-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-prelaunch-splash-v2/README.md `、` compositor/tests/protocols/treeland-prelaunch-splash-v2/setup.cpp `、` compositor/tests/protocols/treeland-prelaunch-splash-v2/treeland-prelaunch-splash-v2.c `、` compositor/tests/protocols/treeland-prelaunch-splash-v2/treeland-prelaunch-splash-v2.h `、` compositor/tests/protocols/treeland-screensaver-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-screensaver-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-screensaver-desktop-v1/treeland-screensaver-desktop-v1.c `、` compositor/tests/protocols/treeland-screensaver-desktop-v1/treeland-screensaver-desktop-v1.h `、` compositor/tests/protocols/treeland-screensaver-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-screensaver-v1/README.md `、` compositor/tests/protocols/treeland-screensaver-v1/setup.cpp `、` compositor/tests/protocols/treeland-screensaver-v1/treeland-screensaver-v1.c `、` compositor/tests/protocols/treeland-screensaver-v1/treeland-screensaver-v1.h `、` compositor/tests/protocols/treeland-shortcut-manager-desktop-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-shortcut-manager-desktop-v2/setup.cpp `、` compositor/tests/protocols/treeland-shortcut-manager-desktop-v2/treeland-shortcut-manager-desktop-v2.c `、` compositor/tests/protocols/treeland-shortcut-manager-desktop-v2/treeland-shortcut-manager-desktop-v2.h `、` compositor/tests/protocols/treeland-shortcut-manager-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-shortcut-manager-v2/README.md `、` compositor/tests/protocols/treeland-shortcut-manager-v2/setup.cpp `、` compositor/tests/protocols/treeland-shortcut-manager-v2/treeland-shortcut-manager-v2.c `、` compositor/tests/protocols/treeland-shortcut-manager-v2/treeland-shortcut-manager-v2.h `、` compositor/tests/protocols/treeland-virtual-output-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-virtual-output-desktop-v1/README.md `、` compositor/tests/protocols/treeland-virtual-output-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-virtual-output-desktop-v1/treeland-virtual-output-desktop-v1.c `、` compositor/tests/protocols/treeland-virtual-output-desktop-v1/treeland-virtual-output-desktop-v1.h `、` compositor/tests/protocols/treeland-virtual-output-manager-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-virtual-output-manager-v1/README.md `、` compositor/tests/protocols/treeland-virtual-output-manager-v1/setup.cpp `、` compositor/tests/protocols/treeland-virtual-output-manager-v1/treeland-virtual-output-manager-v1.c `、` compositor/tests/protocols/treeland-virtual-output-manager-v1/treeland-virtual-output-manager-v1.h `、` compositor/tests/protocols/treeland-wallpaper-color-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-wallpaper-color-v1/README.md `、` compositor/tests/protocols/treeland-wallpaper-color-v1/setup.cpp `、` compositor/tests/protocols/treeland-wallpaper-color-v1/treeland-wallpaper-color-v1.c `、` compositor/tests/protocols/treeland-wallpaper-color-v1/treeland-wallpaper-color-v1.h `、` compositor/tests/protocols/treeland-wallpaper-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-wallpaper-desktop-v1/README.md `、` compositor/tests/protocols/treeland-wallpaper-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-wallpaper-desktop-v1/treeland-wallpaper-desktop-v1.c `、` compositor/tests/protocols/treeland-wallpaper-desktop-v1/treeland-wallpaper-desktop-v1.h `、` compositor/tests/protocols/treeland-wallpaper-manager-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-wallpaper-manager-unstable-v1/README.md `、` compositor/tests/protocols/treeland-wallpaper-manager-unstable-v1/setup.cpp `、` compositor/tests/protocols/treeland-wallpaper-manager-unstable-v1/treeland-wallpaper-manager-unstable-v1.c `、` compositor/tests/protocols/treeland-wallpaper-manager-unstable-v1/treeland-wallpaper-manager-unstable-v1.h `、` compositor/tests/protocols/treeland-wallpaper-shell-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-wallpaper-shell-unstable-v1/README.md `、` compositor/tests/protocols/treeland-wallpaper-shell-unstable-v1/setup.cpp `、` compositor/tests/protocols/treeland-wallpaper-shell-unstable-v1/treeland-wallpaper-shell-unstable-v1.c `、` compositor/tests/protocols/treeland-wallpaper-shell-unstable-v1/treeland-wallpaper-shell-unstable-v1.h `、` compositor/tests/protocols/treeland-window-management-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-window-management-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-window-management-desktop-v1/treeland-window-management-desktop-v1.c `、` compositor/tests/protocols/treeland-window-management-desktop-v1/treeland-window-management-desktop-v1.h `、` compositor/tests/protocols/treeland-window-management-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-window-management-v1/README.md `、` compositor/tests/protocols/treeland-window-management-v1/setup.cpp `、` compositor/tests/protocols/treeland-window-management-v1/treeland-window-management-v1.c `、` compositor/tests/protocols/treeland-window-management-v1/treeland-window-management-v1.h `、` compositor/tests/protocols/treeland-wine-window-management-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-wine-window-management-unstable-v1/README.md `、` compositor/tests/protocols/treeland-wine-window-management-unstable-v1/setup.cpp `、` compositor/tests/protocols/treeland-wine-window-management-unstable-v1/treeland-wine-window-management-unstable-v1.c `、` compositor/tests/protocols/treeland-wine-window-management-unstable-v1/treeland-wine-window-management-unstable-v1.h `、` compositor/tests/protocols/treeland-wine-window-state-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-wine-window-state-unstable-v1/README.md `、` compositor/tests/protocols/treeland-wine-window-state-unstable-v1/setup.cpp `、` compositor/tests/protocols/treeland-wine-window-state-unstable-v1/treeland-wine-window-state-unstable-v1.c `、` compositor/tests/protocols/treeland-wine-window-state-unstable-v1/treeland-wine-window-state-unstable-v1.h `。
- 实际改变：` .github/workflows/treeland-deepin-build.yml `、` 3rdparty/waylib-shared `、` compositor/.agents/skills/wayland-protocol-test/SKILL.md `、` compositor/src/CMakeLists.txt `、` compositor/src/core/qml/PrelaunchSplash.qml `、` compositor/src/core/treelandinit.cpp `、` compositor/src/core/treelandinit.h `、` compositor/src/core/windowpicker.cpp `、` compositor/src/core/windowpicker.h `、` compositor/src/main.cpp `、` compositor/src/modules/capture/capture.cpp `、` compositor/src/modules/capture/capture.h `、` compositor/src/modules/wallpaper/wallpapershellinterfacev1.cpp `、` compositor/src/plugins/lockscreen/qml/ShutdownButton.qml `、` compositor/src/plugins/multitaskview/qml/WindowSelectionGrid.qml `、` compositor/src/plugins/multitaskview/qml/WorkspaceSelectionList.qml `、` compositor/src/seat/helper.cpp `、` compositor/tests/CMakeLists.txt `、` compositor/tests/protocols/CMakeLists.txt `、` compositor/tests/protocols/INDEX.md `、` compositor/tests/protocols/README.md `、` compositor/tests/protocols/framework/ProtocolTest.cmake `、` compositor/tests/protocols/framework/README.md `、` compositor/tests/protocols/framework/client-connection.c `、` compositor/tests/protocols/framework/client-connection.h `、` compositor/tests/protocols/framework/protocol-test-entry.cpp `、` compositor/tests/protocols/framework/server-bridge-api.h `、` compositor/tests/protocols/framework/server-bridge.cpp `、` compositor/tests/protocols/framework/server-bridge.h `、` compositor/tests/protocols/framework/test-accounts-service.cpp `、` compositor/tests/protocols/framework/test-accounts-service.h `、` compositor/tests/protocols/framework/test-dconfig-service.cpp `、` compositor/tests/protocols/framework/test-dconfig-service.h `、` compositor/tests/protocols/framework/xdg-toplevel-client.c `、` compositor/tests/protocols/framework/xdg-toplevel-client.h `、` compositor/tests/protocols/protocol-specification-template.md `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v1/treeland-app-id-resolver-desktop-v1.c `、` compositor/tests/protocols/treeland-app-id-resolver-desktop-v1/treeland-app-id-resolver-desktop-v1.h `、` compositor/tests/protocols/treeland-app-id-resolver-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-app-id-resolver-v1/README.md `、` compositor/tests/protocols/treeland-app-id-resolver-v1/setup.cpp `、` compositor/tests/protocols/treeland-app-id-resolver-v1/treeland-app-id-resolver-v1.c `、` compositor/tests/protocols/treeland-app-id-resolver-v1/treeland-app-id-resolver-v1.h `、` compositor/tests/protocols/treeland-capture-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-capture-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-capture-desktop-v1/treeland-capture-desktop-v1.c `、` compositor/tests/protocols/treeland-capture-desktop-v1/treeland-capture-desktop-v1.h `、` compositor/tests/protocols/treeland-capture-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-capture-unstable-v1/README.md `、` compositor/tests/protocols/treeland-capture-unstable-v1/setup.cpp `、` compositor/tests/protocols/treeland-capture-unstable-v1/treeland-capture-unstable-v1.c `、` compositor/tests/protocols/treeland-capture-unstable-v1/treeland-capture-unstable-v1.h `、` compositor/tests/protocols/treeland-dde-shell-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-dde-shell-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-dde-shell-desktop-v1/treeland-dde-shell-desktop-v1.c `、` compositor/tests/protocols/treeland-dde-shell-desktop-v1/treeland-dde-shell-desktop-v1.h `、` compositor/tests/protocols/treeland-dde-shell-lockscreen-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-dde-shell-lockscreen-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-dde-shell-lockscreen-desktop-v1/treeland-dde-shell-lockscreen-desktop-v1.c `、` compositor/tests/protocols/treeland-dde-shell-lockscreen-desktop-v1/treeland-dde-shell-lockscreen-desktop-v1.h `、` compositor/tests/protocols/treeland-dde-shell-multitask-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-dde-shell-multitask-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-dde-shell-multitask-desktop-v1/treeland-dde-shell-multitask-desktop-v1.c `、` compositor/tests/protocols/treeland-dde-shell-multitask-desktop-v1/treeland-dde-shell-multitask-desktop-v1.h `、` compositor/tests/protocols/treeland-dde-shell-picker-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-dde-shell-picker-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-dde-shell-picker-desktop-v1/treeland-dde-shell-picker-desktop-v1.c `、` compositor/tests/protocols/treeland-dde-shell-picker-desktop-v1/treeland-dde-shell-picker-desktop-v1.h `、` compositor/tests/protocols/treeland-dde-shell-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-dde-shell-v1/README.md `、` compositor/tests/protocols/treeland-dde-shell-v1/setup.cpp `、` compositor/tests/protocols/treeland-dde-shell-v1/treeland-dde-shell-v1.c `、` compositor/tests/protocols/treeland-dde-shell-v1/treeland-dde-shell-v1.h `、` compositor/tests/protocols/treeland-ddm-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-ddm-v1/README.md `、` compositor/tests/protocols/treeland-ddm-v1/setup.cpp `、` compositor/tests/protocols/treeland-ddm-v1/treeland-ddm-v1.c `、` compositor/tests/protocols/treeland-ddm-v1/treeland-ddm-v1.h `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/README.md `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/setup.cpp `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/treeland-foreign-toplevel-manager-v1.c `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/treeland-foreign-toplevel-manager-v1.h `、` compositor/tests/protocols/treeland-input-manager-uinput-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-input-manager-uinput-v1/setup.cpp `、` compositor/tests/protocols/treeland-input-manager-uinput-v1/treeland-input-manager-uinput-v1.c `、` compositor/tests/protocols/treeland-input-manager-uinput-v1/treeland-input-manager-uinput-v1.h `、` compositor/tests/protocols/treeland-input-manager-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-input-manager-unstable-v1/README.md `、` compositor/tests/protocols/treeland-input-manager-unstable-v1/setup.cpp `、` compositor/tests/protocols/treeland-input-manager-unstable-v1/treeland-input-manager-unstable-v1.c `、` compositor/tests/protocols/treeland-input-manager-unstable-v1/treeland-input-manager-unstable-v1.h `、` compositor/tests/protocols/treeland-keyboard-state-notify-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-keyboard-state-notify-unstable-v1/README.md `、` compositor/tests/protocols/treeland-keyboard-state-notify-unstable-v1/setup.cpp `、` compositor/tests/protocols/treeland-keyboard-state-notify-unstable-v1/treeland-keyboard-state-notify-unstable-v1.c `、` compositor/tests/protocols/treeland-keyboard-state-notify-unstable-v1/treeland-keyboard-state-notify-unstable-v1.h `、` compositor/tests/protocols/treeland-output-manager-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-output-manager-v1/README.md `、` compositor/tests/protocols/treeland-output-manager-v1/setup.cpp `、` compositor/tests/protocols/treeland-output-manager-v1/treeland-output-manager-v1.c `、` compositor/tests/protocols/treeland-output-manager-v1/treeland-output-manager-v1.h `、` compositor/tests/protocols/treeland-personalization-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-personalization-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-personalization-desktop-v1/treeland-personalization-desktop-v1.c `、` compositor/tests/protocols/treeland-personalization-desktop-v1/treeland-personalization-desktop-v1.h `、` compositor/tests/protocols/treeland-personalization-manager-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-personalization-manager-v1/README.md `、` compositor/tests/protocols/treeland-personalization-manager-v1/setup.cpp `、` compositor/tests/protocols/treeland-personalization-manager-v1/treeland-personalization-manager-v1.c `、` compositor/tests/protocols/treeland-personalization-manager-v1/treeland-personalization-manager-v1.h `、` compositor/tests/protocols/treeland-prelaunch-splash-desktop-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-prelaunch-splash-desktop-v2/setup.cpp `、` compositor/tests/protocols/treeland-prelaunch-splash-desktop-v2/treeland-prelaunch-splash-desktop-v2.c `、` compositor/tests/protocols/treeland-prelaunch-splash-desktop-v2/treeland-prelaunch-splash-desktop-v2.h `、` compositor/tests/protocols/treeland-prelaunch-splash-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-prelaunch-splash-v2/README.md `、` compositor/tests/protocols/treeland-prelaunch-splash-v2/setup.cpp `、` compositor/tests/protocols/treeland-prelaunch-splash-v2/treeland-prelaunch-splash-v2.c `、` compositor/tests/protocols/treeland-prelaunch-splash-v2/treeland-prelaunch-splash-v2.h `、` compositor/tests/protocols/treeland-screensaver-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-screensaver-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-screensaver-desktop-v1/treeland-screensaver-desktop-v1.c `、` compositor/tests/protocols/treeland-screensaver-desktop-v1/treeland-screensaver-desktop-v1.h `、` compositor/tests/protocols/treeland-screensaver-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-screensaver-v1/README.md `、` compositor/tests/protocols/treeland-screensaver-v1/setup.cpp `、` compositor/tests/protocols/treeland-screensaver-v1/treeland-screensaver-v1.c `、` compositor/tests/protocols/treeland-screensaver-v1/treeland-screensaver-v1.h `、` compositor/tests/protocols/treeland-shortcut-manager-desktop-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-shortcut-manager-desktop-v2/setup.cpp `、` compositor/tests/protocols/treeland-shortcut-manager-desktop-v2/treeland-shortcut-manager-desktop-v2.c `、` compositor/tests/protocols/treeland-shortcut-manager-desktop-v2/treeland-shortcut-manager-desktop-v2.h `、` compositor/tests/protocols/treeland-shortcut-manager-v2/CMakeLists.txt `、` compositor/tests/protocols/treeland-shortcut-manager-v2/README.md `、` compositor/tests/protocols/treeland-shortcut-manager-v2/setup.cpp `、` compositor/tests/protocols/treeland-shortcut-manager-v2/treeland-shortcut-manager-v2.c `、` compositor/tests/protocols/treeland-shortcut-manager-v2/treeland-shortcut-manager-v2.h `、` compositor/tests/protocols/treeland-virtual-output-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-virtual-output-desktop-v1/README.md `、` compositor/tests/protocols/treeland-virtual-output-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-virtual-output-desktop-v1/treeland-virtual-output-desktop-v1.c `、` compositor/tests/protocols/treeland-virtual-output-desktop-v1/treeland-virtual-output-desktop-v1.h `、` compositor/tests/protocols/treeland-virtual-output-manager-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-virtual-output-manager-v1/README.md `、` compositor/tests/protocols/treeland-virtual-output-manager-v1/setup.cpp `、` compositor/tests/protocols/treeland-virtual-output-manager-v1/treeland-virtual-output-manager-v1.c `、` compositor/tests/protocols/treeland-virtual-output-manager-v1/treeland-virtual-output-manager-v1.h `、` compositor/tests/protocols/treeland-wallpaper-color-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-wallpaper-color-v1/README.md `、` compositor/tests/protocols/treeland-wallpaper-color-v1/setup.cpp `、` compositor/tests/protocols/treeland-wallpaper-color-v1/treeland-wallpaper-color-v1.c `、` compositor/tests/protocols/treeland-wallpaper-color-v1/treeland-wallpaper-color-v1.h `、` compositor/tests/protocols/treeland-wallpaper-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-wallpaper-desktop-v1/README.md `、` compositor/tests/protocols/treeland-wallpaper-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-wallpaper-desktop-v1/treeland-wallpaper-desktop-v1.c `、` compositor/tests/protocols/treeland-wallpaper-desktop-v1/treeland-wallpaper-desktop-v1.h `、` compositor/tests/protocols/treeland-wallpaper-manager-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-wallpaper-manager-unstable-v1/README.md `、` compositor/tests/protocols/treeland-wallpaper-manager-unstable-v1/setup.cpp `、` compositor/tests/protocols/treeland-wallpaper-manager-unstable-v1/treeland-wallpaper-manager-unstable-v1.c `、` compositor/tests/protocols/treeland-wallpaper-manager-unstable-v1/treeland-wallpaper-manager-unstable-v1.h `、` compositor/tests/protocols/treeland-wallpaper-shell-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-wallpaper-shell-unstable-v1/README.md `、` compositor/tests/protocols/treeland-wallpaper-shell-unstable-v1/setup.cpp `、` compositor/tests/protocols/treeland-wallpaper-shell-unstable-v1/treeland-wallpaper-shell-unstable-v1.c `、` compositor/tests/protocols/treeland-wallpaper-shell-unstable-v1/treeland-wallpaper-shell-unstable-v1.h `、` compositor/tests/protocols/treeland-window-management-desktop-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-window-management-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-window-management-desktop-v1/treeland-window-management-desktop-v1.c `、` compositor/tests/protocols/treeland-window-management-desktop-v1/treeland-window-management-desktop-v1.h `、` compositor/tests/protocols/treeland-window-management-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-window-management-v1/README.md `、` compositor/tests/protocols/treeland-window-management-v1/setup.cpp `、` compositor/tests/protocols/treeland-window-management-v1/treeland-window-management-v1.c `、` compositor/tests/protocols/treeland-window-management-v1/treeland-window-management-v1.h `、` compositor/tests/protocols/treeland-wine-window-management-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-wine-window-management-unstable-v1/README.md `、` compositor/tests/protocols/treeland-wine-window-management-unstable-v1/setup.cpp `、` compositor/tests/protocols/treeland-wine-window-management-unstable-v1/treeland-wine-window-management-unstable-v1.c `、` compositor/tests/protocols/treeland-wine-window-management-unstable-v1/treeland-wine-window-management-unstable-v1.h `、` compositor/tests/protocols/treeland-wine-window-state-unstable-v1/CMakeLists.txt `、` compositor/tests/protocols/treeland-wine-window-state-unstable-v1/README.md `、` compositor/tests/protocols/treeland-wine-window-state-unstable-v1/setup.cpp `、` compositor/tests/protocols/treeland-wine-window-state-unstable-v1/treeland-wine-window-state-unstable-v1.c `、` compositor/tests/protocols/treeland-wine-window-state-unstable-v1/treeland-wine-window-state-unstable-v1.h `。
- 排除的来源路径：` waylib/src/server/qtquick/wtextureproviderprovider.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` b17f567f1f6ef94ce3a2cf2c5a87f77f1a58df59 ` → ` 24127943ee472d37b728fb113f8c1f180c9bdd22 `。
  原证据引用：` 6aea08e0bb8f4623b6c3ea294b4baa119e0922da ` → ` 7809ec68cab35eed59341b5a0d8286589cde22ef `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` cf2dc0a911759ef9cc94fd9d8d81c76f4ccb4769 ` 和原目标 ` 1c9eaeb6c0362f9b00d4af5fd92c90974507eac7 ` 查询。
- 原审核说明：` 引入来源的生产协议测试及独立初始化入口；测试只消费本地 DeckCompositorProtocols，按现有 compositor/ 和 3rdparty/waylib-shared/ 布局链接 libdeckcompositor。main 保留既有日志开关；core/treeland.cpp 已以默认开启的独立插件路径开关实现 Release 搜索，保留该可关闭合同，不再受 QT_DEBUG 限制。 合入本来源的真实协议集成诊断修复；保持正常产品配置、真实协议请求和完整断言，不禁用测试或引入兼容层。 2026-09-14 用户明确批准唯一 PrelaunchSplash.qml 集成文件，将上游 QML 导入修正为既有 WaylibShared.QuickSharedServer 1.0；不引入兼容模块或扩大普通来源路径。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/38bf63ee2a56c08d0b852f54337c63131f8c6064.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 24127943ee472d37b728fb113f8c1f180c9bdd22 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-474"></a>
### 474. N7 / ` fix: avoid QGuiApplication static destruction crash `

- 本仓内容路径：` compositor/src/core/treelandinit.cpp `、` compositor/src/core/treelandinit.h `、` compositor/src/main.cpp `、` compositor/tests/protocols/framework/protocol-test-entry.cpp `。
- 实际改变：` compositor/src/core/treelandinit.cpp `、` compositor/src/core/treelandinit.h `、` compositor/src/main.cpp `、` compositor/tests/protocols/framework/protocol-test-entry.cpp `、` compositor/tests/test_qpa_lifecycle/run.cmake `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 24127943ee472d37b728fb113f8c1f180c9bdd22 ` → ` 24127943ee472d37b728fb113f8c1f180c9bdd22 `。
  原证据引用：` 7809ec68cab35eed59341b5a0d8286589cde22ef ` → ` 7809ec68cab35eed59341b5a0d8286589cde22ef `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` debeeb67804d44dfa1140058d592f617e37951f8 ` 和原目标 ` 082095f3f36d644441926c706c16e41f41e2092f ` 查询。
- 原审核说明：` 逐路径三方合入来源变化，保留已确认的目标布局、依赖接入、命名空间与非冲突本地修复；源前后对象及目标前后对象逐项绑定。 合入本来源的真实协议集成诊断修复；保持正常产品配置、真实协议请求和完整断言，不禁用测试或引入兼容层。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/7a880ac6713bb5334982a7326df13f03eae601a8.md)。

<a id="entry-475"></a>
### 475. N7 / ` fix: extract protocol interface versions into static constexpr InterfaceVersion `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/protocols/private/wtextinputv1.cpp `、` waylib/src/server/protocols/private/wtextinputv1_p.h `、` waylib/src/server/protocols/private/wtextinputv2.cpp `、` waylib/src/server/protocols/private/wtextinputv2_p.h `、` waylib/src/server/protocols/wcursorshapemanagerv1.cpp `、` waylib/src/server/protocols/wcursorshapemanagerv1.h `、` waylib/src/server/protocols/wextforeigntoplevellistv1.cpp `、` waylib/src/server/protocols/wextforeigntoplevellistv1.h `、` waylib/src/server/protocols/wlayershell.cpp `、` waylib/src/server/protocols/wlayershell.h `、` waylib/src/server/protocols/wxdgdialogmanagerv1.cpp `、` waylib/src/server/protocols/wxdgdialogmanagerv1.h `、` waylib/src/server/protocols/wxdgtopleveltagmanager.cpp `、` waylib/src/server/protocols/wxdgtopleveltagmanager.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 24127943ee472d37b728fb113f8c1f180c9bdd22 ` → ` 60b110eb8f75bb76b1c21cb1e8ad12bb3a8b4df5 `。
  原证据引用：` 7809ec68cab35eed59341b5a0d8286589cde22ef ` → ` 7bb39c5721565690b7d77745a42b91f1723dc54b `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 98c1a0c9347f4f3af593692261bbd8150ec85f2f ` 和原目标 ` 9115cc151e5d967b6d58d4b2f162e6467137910e ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 60b110eb8f75bb76b1c21cb1e8ad12bb3a8b4df5 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-476"></a>
### 476. N7 / ` feat(multi-output): forward client fullscreen output to surface handler `

- 本仓内容路径：` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv1.cpp `、` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/modules/foreign-toplevel/foreigntoplevelmanagerv1.cpp `、` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 排除的来源路径：` waylib/src/server/kernel/wtoplevelsurface.h `、` waylib/src/server/protocols/wxdgtoplevelsurface.cpp `、` waylib/src/server/protocols/wxwaylandsurface.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 60b110eb8f75bb76b1c21cb1e8ad12bb3a8b4df5 ` → ` bb3491c7cfb6f4261fed9604be3d1bd30e79cf01 `。
  原证据引用：` 7bb39c5721565690b7d77745a42b91f1723dc54b ` → ` 312ab98c1f9c28c6046e6c3c56466fffb41f47f2 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 12d4cff2dc6a81c6b891812d55b1a98378720d43 ` 和原目标 ` 610a02c74915ba0f9d86d61a0c818da1d61a7efb ` 查询。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 同一 Treeland 来源的 C / waylib-shared 目标：` bb3491c7cfb6f4261fed9604be3d1bd30e79cf01 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-477"></a>
### 477. N7 / ` fix(surface): set maximized on initial surface commit `

- 本仓内容路径：` compositor/src/core/shellhandler.cpp `、` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/core/shellhandler.cpp `、` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 排除的来源路径：` waylib/src/server/qtquick/wxdgtoplevelsurfaceitem.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` bb3491c7cfb6f4261fed9604be3d1bd30e79cf01 ` → ` ec253a9bc0de3d5f32aa6a6fdbbfcaae649f19e2 `。
  原证据引用：` 312ab98c1f9c28c6046e6c3c56466fffb41f47f2 ` → ` 566a4727ecd7590d054bdde46ddb71acc55cdc96 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` f2ebdf403cef739166a5aacc7324a24d3662176b ` 和原目标 ` 83e918c139389abfea9846909a52e5a199258d6e ` 查询。
- 原审核说明：` 保留来源变更及已验收的本地布局和非冲突适配。 合入本来源的真实协议集成诊断修复；保持正常产品配置、真实协议请求和完整断言，不禁用测试或引入兼容层。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/0cf9ae3c48e4c18be22f895ba4fb44e12f67c5a6.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` ec253a9bc0de3d5f32aa6a6fdbbfcaae649f19e2 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-478"></a>
### 478. N7 / ` fix: avoid invalid pointer constraint warp `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/kernel/wcursor.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` ec253a9bc0de3d5f32aa6a6fdbbfcaae649f19e2 ` → ` af00c1b0f1c1ebbb7d34a2435900192512188ee4 `。
  原证据引用：` 566a4727ecd7590d054bdde46ddb71acc55cdc96 ` → ` a523bd2505b84fa5238b2b041320c6157ba265d8 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 9a36a9924ef6b74d944accd17e149ec015ef862d ` 和原目标 ` 5cb809142145817c9fbb556472da51d5621ba2e1 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` af00c1b0f1c1ebbb7d34a2435900192512188ee4 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-479"></a>
### 479. N7 / ` style(tests): remove consecutive blank lines in tests directory `

- 本仓内容路径：` compositor/tests/protocols/framework/README.md `、` compositor/tests/protocols/treeland-app-id-resolver-v1/setup.cpp `、` compositor/tests/protocols/treeland-app-id-resolver-v1/treeland-app-id-resolver-v1.c `、` compositor/tests/protocols/treeland-app-id-resolver-v1/treeland-app-id-resolver-v1.h `、` compositor/tests/protocols/treeland-capture-unstable-v1/treeland-capture-unstable-v1.h `、` compositor/tests/protocols/treeland-dde-shell-v1/treeland-dde-shell-v1.h `、` compositor/tests/protocols/treeland-ddm-v1/treeland-ddm-v1.c `、` compositor/tests/protocols/treeland-ddm-v1/treeland-ddm-v1.h `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/treeland-foreign-toplevel-manager-v1.h `、` compositor/tests/protocols/treeland-keyboard-state-notify-unstable-v1/treeland-keyboard-state-notify-unstable-v1.c `、` compositor/tests/protocols/treeland-output-manager-v1/treeland-output-manager-v1.c `、` compositor/tests/protocols/treeland-output-manager-v1/treeland-output-manager-v1.h `、` compositor/tests/protocols/treeland-personalization-manager-v1/treeland-personalization-manager-v1.c `、` compositor/tests/protocols/treeland-personalization-manager-v1/treeland-personalization-manager-v1.h `、` compositor/tests/protocols/treeland-prelaunch-splash-v2/treeland-prelaunch-splash-v2.h `、` compositor/tests/protocols/treeland-screensaver-v1/setup.cpp `、` compositor/tests/protocols/treeland-screensaver-v1/treeland-screensaver-v1.c `、` compositor/tests/protocols/treeland-screensaver-v1/treeland-screensaver-v1.h `、` compositor/tests/protocols/treeland-shortcut-manager-v2/treeland-shortcut-manager-v2.h `、` compositor/tests/protocols/treeland-virtual-output-manager-v1/setup.cpp `、` compositor/tests/protocols/treeland-virtual-output-manager-v1/treeland-virtual-output-manager-v1.c `、` compositor/tests/protocols/treeland-virtual-output-manager-v1/treeland-virtual-output-manager-v1.h `、` compositor/tests/protocols/treeland-wallpaper-color-v1/setup.cpp `、` compositor/tests/protocols/treeland-wallpaper-color-v1/treeland-wallpaper-color-v1.h `、` compositor/tests/protocols/treeland-wallpaper-manager-unstable-v1/treeland-wallpaper-manager-unstable-v1.c `、` compositor/tests/protocols/treeland-wallpaper-manager-unstable-v1/treeland-wallpaper-manager-unstable-v1.h `、` compositor/tests/protocols/treeland-wallpaper-shell-unstable-v1/setup.cpp `、` compositor/tests/protocols/treeland-wallpaper-shell-unstable-v1/treeland-wallpaper-shell-unstable-v1.h `、` compositor/tests/protocols/treeland-window-management-v1/setup.cpp `、` compositor/tests/protocols/treeland-window-management-v1/treeland-window-management-v1.c `、` compositor/tests/protocols/treeland-window-management-v1/treeland-window-management-v1.h `、` compositor/tests/protocols/treeland-wine-window-management-unstable-v1/treeland-wine-window-management-unstable-v1.c `、` compositor/tests/protocols/treeland-wine-window-management-unstable-v1/treeland-wine-window-management-unstable-v1.h `、` compositor/tests/protocols/treeland-wine-window-state-unstable-v1/treeland-wine-window-state-unstable-v1.c `、` compositor/tests/test_effect_glass/main.cpp `、` compositor/tests/test_protocol_window-management/main.cpp `。
- 实际改变：` compositor/tests/protocols/framework/README.md `、` compositor/tests/protocols/treeland-app-id-resolver-v1/setup.cpp `、` compositor/tests/protocols/treeland-app-id-resolver-v1/treeland-app-id-resolver-v1.c `、` compositor/tests/protocols/treeland-app-id-resolver-v1/treeland-app-id-resolver-v1.h `、` compositor/tests/protocols/treeland-capture-unstable-v1/treeland-capture-unstable-v1.h `、` compositor/tests/protocols/treeland-dde-shell-v1/treeland-dde-shell-v1.h `、` compositor/tests/protocols/treeland-ddm-v1/treeland-ddm-v1.c `、` compositor/tests/protocols/treeland-ddm-v1/treeland-ddm-v1.h `、` compositor/tests/protocols/treeland-foreign-toplevel-manager-v1/treeland-foreign-toplevel-manager-v1.h `、` compositor/tests/protocols/treeland-keyboard-state-notify-unstable-v1/treeland-keyboard-state-notify-unstable-v1.c `、` compositor/tests/protocols/treeland-output-manager-v1/treeland-output-manager-v1.c `、` compositor/tests/protocols/treeland-output-manager-v1/treeland-output-manager-v1.h `、` compositor/tests/protocols/treeland-personalization-manager-v1/treeland-personalization-manager-v1.c `、` compositor/tests/protocols/treeland-personalization-manager-v1/treeland-personalization-manager-v1.h `、` compositor/tests/protocols/treeland-prelaunch-splash-v2/treeland-prelaunch-splash-v2.h `、` compositor/tests/protocols/treeland-screensaver-v1/setup.cpp `、` compositor/tests/protocols/treeland-screensaver-v1/treeland-screensaver-v1.c `、` compositor/tests/protocols/treeland-screensaver-v1/treeland-screensaver-v1.h `、` compositor/tests/protocols/treeland-shortcut-manager-v2/treeland-shortcut-manager-v2.h `、` compositor/tests/protocols/treeland-virtual-output-manager-v1/setup.cpp `、` compositor/tests/protocols/treeland-virtual-output-manager-v1/treeland-virtual-output-manager-v1.c `、` compositor/tests/protocols/treeland-virtual-output-manager-v1/treeland-virtual-output-manager-v1.h `、` compositor/tests/protocols/treeland-wallpaper-color-v1/setup.cpp `、` compositor/tests/protocols/treeland-wallpaper-color-v1/treeland-wallpaper-color-v1.h `、` compositor/tests/protocols/treeland-wallpaper-manager-unstable-v1/treeland-wallpaper-manager-unstable-v1.c `、` compositor/tests/protocols/treeland-wallpaper-manager-unstable-v1/treeland-wallpaper-manager-unstable-v1.h `、` compositor/tests/protocols/treeland-wallpaper-shell-unstable-v1/setup.cpp `、` compositor/tests/protocols/treeland-wallpaper-shell-unstable-v1/treeland-wallpaper-shell-unstable-v1.h `、` compositor/tests/protocols/treeland-window-management-v1/setup.cpp `、` compositor/tests/protocols/treeland-window-management-v1/treeland-window-management-v1.c `、` compositor/tests/protocols/treeland-window-management-v1/treeland-window-management-v1.h `、` compositor/tests/protocols/treeland-wine-window-management-unstable-v1/treeland-wine-window-management-unstable-v1.c `、` compositor/tests/protocols/treeland-wine-window-management-unstable-v1/treeland-wine-window-management-unstable-v1.h `、` compositor/tests/protocols/treeland-wine-window-state-unstable-v1/treeland-wine-window-state-unstable-v1.c `、` compositor/tests/test_effect_glass/main.cpp `、` compositor/tests/test_protocol_window-management/main.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` af00c1b0f1c1ebbb7d34a2435900192512188ee4 ` → ` af00c1b0f1c1ebbb7d34a2435900192512188ee4 `。
  原证据引用：` a523bd2505b84fa5238b2b041320c6157ba265d8 ` → ` a523bd2505b84fa5238b2b041320c6157ba265d8 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 9ac30111d8170b207ec5c821a3131804ce4447c7 ` 和原目标 ` 024f7e35db68da4bb33177f7f7cabcd270cff76c ` 查询。

<a id="entry-480"></a>
### 480. N7 / ` test(protocols): share protocol test framework build `

- 本仓内容路径：` .github/workflows/treeland-deepin-build.yml `、` compositor/tests/protocols/framework/ProtocolTest.cmake `。
- 实际改变：` .github/workflows/treeland-deepin-build.yml `、` compositor/tests/protocols/framework/ProtocolTest.cmake `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` af00c1b0f1c1ebbb7d34a2435900192512188ee4 ` → ` af00c1b0f1c1ebbb7d34a2435900192512188ee4 `。
  原证据引用：` a523bd2505b84fa5238b2b041320c6157ba265d8 ` → ` a523bd2505b84fa5238b2b041320c6157ba265d8 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 27dc6ce6022dbcd77ebdf3323d3672d47f78a9e7 ` 和原目标 ` a8ab40323105f670c1785131ed0c0f83d25086e7 ` 查询。
- 原审核说明：` 协议共享测试框架沿用 compositor 插件的同一 DISABLE_DDM 条件：multitaskview 始终依赖，启用 DDM 时依赖真实 lockscreen 目标；不创建占位 target，不修改产品默认开关，不跳过任何已注册测试，并保留本地源码路径和库名。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/16f668bc2b3baf0f13cfd97735803a6a3bd280bc.md)。

<a id="entry-481"></a>
### 481. N7 / ` feat: support wp_single_pixel_buffer_manager_v1 protocol `

- 本仓内容路径：` compositor/src/seat/helper.cpp `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/seat/helper.cpp `。
- 排除的来源路径：` waylib/src/server/kernel/wlr_all.h `、` waylib/src/server/kernel/wlr_fwd.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` af00c1b0f1c1ebbb7d34a2435900192512188ee4 ` → ` 6ddaa982f7fb1339111f05973356f455d1626640 `。
  原证据引用：` a523bd2505b84fa5238b2b041320c6157ba265d8 ` → ` 70aa2211dc13db005e115359e918810e548541f7 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 00f0a3572f081baab08ab21db8b018c4f0feec49 ` 和原目标 ` d021fb8a021717ddc95c3bdaa32e7ffa32d920c0 ` 查询。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 同一 Treeland 来源的 C / waylib-shared 目标：` 6ddaa982f7fb1339111f05973356f455d1626640 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-482"></a>
### 482. N7 / ` refactor(multi-output): rename primary/copy outputs to source/mirror `

- 本仓内容路径：` compositor/src/CMakeLists.txt `、` compositor/src/core/qml/CopyOutput.qml `、` compositor/src/core/qml/MirrorOutput.qml `、` compositor/src/core/qml/OutputMenuBar.qml `、` compositor/src/core/qml/PrimaryOutput.qml `、` compositor/src/core/qml/SourceOutput.qml `、` compositor/src/output/output.cpp `、` compositor/src/output/output.h `、` compositor/src/seat/helper.cpp `、` compositor/src/surface/surfacewrapper.cpp `、` compositor/tests/protocols/treeland-virtual-output-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-virtual-output-desktop-v1/treeland-virtual-output-desktop-v1.c `、` compositor/tests/protocols/treeland-virtual-output-desktop-v1/treeland-virtual-output-desktop-v1.h `。
- 实际改变：` compositor/src/CMakeLists.txt `、` compositor/src/core/qml/CopyOutput.qml `、` compositor/src/core/qml/MirrorOutput.qml `、` compositor/src/core/qml/OutputMenuBar.qml `、` compositor/src/core/qml/PrimaryOutput.qml `、` compositor/src/core/qml/SourceOutput.qml `、` compositor/src/output/output.cpp `、` compositor/src/output/output.h `、` compositor/src/seat/helper.cpp `、` compositor/src/surface/surfacewrapper.cpp `、` compositor/tests/protocols/treeland-virtual-output-desktop-v1/setup.cpp `、` compositor/tests/protocols/treeland-virtual-output-desktop-v1/treeland-virtual-output-desktop-v1.c `、` compositor/tests/protocols/treeland-virtual-output-desktop-v1/treeland-virtual-output-desktop-v1.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 6ddaa982f7fb1339111f05973356f455d1626640 ` → ` 6ddaa982f7fb1339111f05973356f455d1626640 `。
  原证据引用：` 70aa2211dc13db005e115359e918810e548541f7 ` → ` 70aa2211dc13db005e115359e918810e548541f7 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 8d3212c1e7927fc0b9060ae9302a4329cce1e23f ` 和原目标 ` f21267bb9c65c07090492dff84f4fd50afdf364a ` 查询。
- 原审核说明：` 完整同步 Source/Mirror 输出重命名；QML 重命名按旧目标、本次来源前后内容做三方合并，保留本地可见标签和既有 WaylibShared/DeckShell QML URI。旧文件逐项移入回收站，输出工厂与测试调用方使用新的真实类型，不保留旧名兼容壳。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/feb01c4236e1ca54ff50d25232e30b50d9cc05b8.md)。

<a id="entry-483"></a>
### 483. N7 / ` fix(xwayland): acknowledge client configure requests `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/qtquick/wxwaylandsurfaceitem.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 6ddaa982f7fb1339111f05973356f455d1626640 ` → ` 1f6f594824b48569b157ac78f1b7dd84dcb393d8 `。
  原证据引用：` 70aa2211dc13db005e115359e918810e548541f7 ` → ` abd05da0bed28aec18c77a784a854f79a66d0ff7 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 5a69d2fe71dedb6f2a13ad9cf3d3dd593613623b ` 和原目标 ` 307b63828736ec99c3ab93009f5242fe6773c0e3 ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` 1f6f594824b48569b157ac78f1b7dd84dcb393d8 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-484"></a>
### 484. N7 / ` feat(ci): remove deb-src repositories `

- 本仓内容路径：` .github/workflows/treeland-deepin-build.yml `。
- 实际改变：` .github/workflows/treeland-deepin-build.yml `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 1f6f594824b48569b157ac78f1b7dd84dcb393d8 ` → ` 1f6f594824b48569b157ac78f1b7dd84dcb393d8 `。
  原证据引用：` abd05da0bed28aec18c77a784a854f79a66d0ff7 ` → ` abd05da0bed28aec18c77a784a854f79a66d0ff7 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 07b7bec96c3ecc690931578663f0baf66a9b6a68 ` 和原目标 ` 42c929d26aed3ef207a73c80a4610300fcebe927 ` 查询。

<a id="entry-485"></a>
### 485. N7 / ` fix(protocol): correct output manager protocol path `

- 本仓内容路径：` compositor/examples/test_color_control/CMakeLists.txt `、` compositor/examples/test_primary_output/CMakeLists.txt `。
- 实际改变：无。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 1f6f594824b48569b157ac78f1b7dd84dcb393d8 ` → ` 1f6f594824b48569b157ac78f1b7dd84dcb393d8 `。
  原证据引用：` abd05da0bed28aec18c77a784a854f79a66d0ff7 ` → ` abd05da0bed28aec18c77a784a854f79a66d0ff7 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 2031e780f5c770a11843bc81b3cef5271e477dd0 ` 和原目标 ` 3a9f920ba1c86133c7c2d5881cd1694a76020d62 ` 查询。
- 原审核说明：` 两个目标示例均已使用 ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-output-manager-v1.xml，已包含本来源修正的目录分隔符，且消费仓库内协议；保留独立可追溯空提交，不重复改动。 `。
- empty 的原等价证明（不把未改文件说成新适配）：

```json
{
  "source_commit": "2031e780f5c770a11843bc81b3cef5271e477dd0",
  "review_state": "approved",
  "reason": "两个目标示例均已使用 ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-output-manager-v1.xml，已包含本来源修正的目录分隔符，且消费仓库内协议；保留独立可追溯空提交，不重复改动。",
  "paths": [
    {
      "path": "compositor/examples/test_color_control/CMakeLists.txt",
      "source_before": {
        "mode": "100644",
        "type": "blob",
        "sha": "a768f2743f9c7eb88cdfac240c3f6baf93acd957",
        "path": "examples/test_color_control/CMakeLists.txt"
      },
      "source_after": {
        "mode": "100644",
        "type": "blob",
        "sha": "4aa526fab24bbdd5c906e4ef668ef2bf0304e979",
        "path": "examples/test_color_control/CMakeLists.txt"
      },
      "target": {
        "mode": "100644",
        "type": "blob",
        "sha": "6c12e33282b5d3a75931fad3f1c3b80a26db9646",
        "path": "compositor/examples/test_color_control/CMakeLists.txt"
      },
      "reason": "两个目标示例均已使用 ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-output-manager-v1.xml，已包含本来源修正的目录分隔符，且消费仓库内协议；保留独立可追溯空提交，不重复改动。"
    },
    {
      "path": "compositor/examples/test_primary_output/CMakeLists.txt",
      "source_before": {
        "mode": "100644",
        "type": "blob",
        "sha": "57779c84fb709fd266c17277bf6909811265f04a",
        "path": "examples/test_primary_output/CMakeLists.txt"
      },
      "source_after": {
        "mode": "100644",
        "type": "blob",
        "sha": "ac58f77f0d71c8fad26716a8b5c8638a91ce59fc",
        "path": "examples/test_primary_output/CMakeLists.txt"
      },
      "target": {
        "mode": "100644",
        "type": "blob",
        "sha": "a0a77cfe9306104867534d173691e454bbcb1c6a",
        "path": "compositor/examples/test_primary_output/CMakeLists.txt"
      },
      "reason": "两个目标示例均已使用 ${DECKCOMPOSITOR_PROTOCOLS_DATA_DIR}/treeland-output-manager-v1.xml，已包含本来源修正的目录分隔符，且消费仓库内协议；保留独立可追溯空提交，不重复改动。"
    }
  ]
}
```


<a id="entry-486"></a>
### 486. N7 / ` fix(tests): remove unused protocols subdirectory build `

- 本仓内容路径：` compositor/tests/CMakeLists.txt `。
- 实际改变：` compositor/tests/CMakeLists.txt `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` 1f6f594824b48569b157ac78f1b7dd84dcb393d8 ` → ` 1f6f594824b48569b157ac78f1b7dd84dcb393d8 `。
  原证据引用：` abd05da0bed28aec18c77a784a854f79a66d0ff7 ` → ` abd05da0bed28aec18c77a784a854f79a66d0ff7 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` d823b8c907699dc86f0fe554cb46b2db8991d408 ` 和原目标 ` ac86a80eab3a36b9c88a633ac6859523ae3c1e16 ` 查询。

<a id="entry-487"></a>
### 487. N7 / ` fix(xwayland): handle size hint updates `

- 本仓内容路径：无。
- 实际改变：` 3rdparty/waylib-shared `。
- 排除的来源路径：` waylib/src/server/protocols/wxwaylandsurface.cpp `、` waylib/tests/unit_tests/test_native_handles/main.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` 1f6f594824b48569b157ac78f1b7dd84dcb393d8 ` → ` bb28166b0b41f2c947ee6cebabbf4465ee69e0ce `。
  原证据引用：` abd05da0bed28aec18c77a784a854f79a66d0ff7 ` → ` ea079e2c68ef826f9c41c24d04f87f1f93d3a634 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 90f6045bf432515698e9f5324b7e5fcf8a375331 ` 和原目标 ` 17ce7c157b44491ef669397fe766485017eda91c ` 查询。
- 原审核说明：` DeckShell contains only the gitlink update. `。
- 原审核说明：` 这是一个单纯的 gitlink 变更。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- **仅依赖引用传播，不是本仓源码适配。**
- 同一 Treeland 来源的 C / waylib-shared 目标：` bb28166b0b41f2c947ee6cebabbf4465ee69e0ce `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-488"></a>
### 488. N7 / ` refactor(surface): move quick tile logic into SurfaceWrapper `

- 本仓内容路径：` compositor/src/CMakeLists.txt `、` compositor/src/core/rootsurfacecontainer.cpp `、` compositor/src/core/rootsurfacecontainer.h `、` compositor/src/modules/shortcut/shortcutrunner.cpp `、` compositor/src/output/output.cpp `、` compositor/src/output/output.h `、` compositor/src/surface/quicktile.cpp `、` compositor/src/surface/quicktile.h `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `、` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 实际改变：` compositor/src/CMakeLists.txt `、` compositor/src/core/rootsurfacecontainer.cpp `、` compositor/src/core/rootsurfacecontainer.h `、` compositor/src/modules/shortcut/shortcutrunner.cpp `、` compositor/src/output/output.cpp `、` compositor/src/output/output.h `、` compositor/src/surface/quicktile.cpp `、` compositor/src/surface/quicktile.h `、` compositor/src/surface/seatsurfacemanager.cpp `、` compositor/src/surface/seatsurfacemanager.h `、` compositor/src/surface/surfacewrapper.cpp `、` compositor/src/surface/surfacewrapper.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` bb28166b0b41f2c947ee6cebabbf4465ee69e0ce ` → ` bb28166b0b41f2c947ee6cebabbf4465ee69e0ce `。
  原证据引用：` ea079e2c68ef826f9c41c24d04f87f1f93d3a634 ` → ` ea079e2c68ef826f9c41c24d04f87f1f93d3a634 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 3a11cdf2ad5a20b7122ce4faf94401b39b90d870 ` 和原目标 ` 020aaed6a88da685bdfdf97ec2ed495c811bf206 ` 查询。

<a id="entry-489"></a>
### 489. N7 / ` feat(keyboard-shortcuts-inhibit): implement zwp_keyboard_shortcuts_inhibit_v1 server `

- 本仓内容路径：` compositor/src/common/treelandlogging.cpp `、` compositor/src/common/treelandlogging.h `、` compositor/src/modules/CMakeLists.txt `、` compositor/src/modules/keyboard-shortcuts-inhibit/CMakeLists.txt `、` compositor/src/modules/keyboard-shortcuts-inhibit/keyboardshortcutsinhibitmanager.cpp `、` compositor/src/modules/keyboard-shortcuts-inhibit/keyboardshortcutsinhibitmanager.h `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/common/treelandlogging.cpp `、` compositor/src/common/treelandlogging.h `、` compositor/src/modules/CMakeLists.txt `、` compositor/src/modules/keyboard-shortcuts-inhibit/CMakeLists.txt `、` compositor/src/modules/keyboard-shortcuts-inhibit/keyboardshortcutsinhibitmanager.cpp `、` compositor/src/modules/keyboard-shortcuts-inhibit/keyboardshortcutsinhibitmanager.h `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `。
- 排除的来源路径：` waylib/src/server/kernel/wlr_all.h `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` bb28166b0b41f2c947ee6cebabbf4465ee69e0ce ` → ` a687f61b1150c228fc259eea679bf2ebbf0b59c5 `。
  原证据引用：` ea079e2c68ef826f9c41c24d04f87f1f93d3a634 ` → ` 123c60108ef98f8f6a240cdbdbec5513538a3011 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 593c48420d29f84f8cb320ea34dbf5ea67cb1abf ` 和原目标 ` 79cbdc7509986440ee77a47a36475cc4d01e439f ` 查询。
- 原审核说明：` 按来源接入键盘快捷键抑制协议，使用现有 impl_deckcompositor 模块入口，不恢复已移除的 impl_treeland 兼容函数；其他协议语义及来源调用链保持不变。 `。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/8a2ed96d1c61331af681ee2fb8540c2ab49d099d.md)。
- 同一 Treeland 来源的 C / waylib-shared 目标：` a687f61b1150c228fc259eea679bf2ebbf0b59c5 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-490"></a>
### 490. N7 / ` refactor(surface): drop redundant fullscreen re-arrangement `

- 本仓内容路径：` compositor/src/surface/surfacewrapper.cpp `。
- 实际改变：` compositor/src/surface/surfacewrapper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` a687f61b1150c228fc259eea679bf2ebbf0b59c5 ` → ` a687f61b1150c228fc259eea679bf2ebbf0b59c5 `。
  原证据引用：` 123c60108ef98f8f6a240cdbdbec5513538a3011 ` → ` 123c60108ef98f8f6a240cdbdbec5513538a3011 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` bf156fcbf01417acfad112849851b458452f3a60 ` 和原目标 ` 4197ce38292120028b51d59058a201891ebe25eb ` 查询。
- 原审核说明：` 保留来源删除冗余全屏重排的实际行为，仅修正该来源新增条件行的尾随空格，不改变判断和输出归属。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/a7c71089f48162fcd8c7d4dc2a411de512615d69.md)。

<a id="entry-491"></a>
### 491. N7 / ` refactor: extract set_region lambda to member function `

- 本仓内容路径：` compositor/AGENTS.md `、` compositor/src/seat/pointerconstraintsmanager.cpp `、` compositor/src/seat/pointerconstraintsmanager.h `。
- 实际改变：` compositor/AGENTS.md `、` compositor/src/seat/pointerconstraintsmanager.cpp `、` compositor/src/seat/pointerconstraintsmanager.h `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` a687f61b1150c228fc259eea679bf2ebbf0b59c5 ` → ` a687f61b1150c228fc259eea679bf2ebbf0b59c5 `。
  原证据引用：` 123c60108ef98f8f6a240cdbdbec5513538a3011 ` → ` 123c60108ef98f8f6a240cdbdbec5513538a3011 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` dde64ada3f04449e1b4d58e298926955c2fee2dc ` 和原目标 ` 47dbb0e91f1bbb589547ce2e7d640ae8a75e6536 ` 查询。

<a id="entry-492"></a>
### 492. N7 / ` fix(xwayland): honor client resize configure requests `

- 本仓内容路径：` compositor/src/surface/surfacewrapper.cpp `。
- 实际改变：` 3rdparty/waylib-shared `、` compositor/src/surface/surfacewrapper.cpp `。
- 排除的来源路径：` waylib/src/server/qtquick/wxwaylandsurfaceitem.cpp `。
- 依赖 ` 3rdparty/waylib-shared `：updated；` a687f61b1150c228fc259eea679bf2ebbf0b59c5 ` → ` be76893d3d5b20494567b8b7041420db299d3507 `。
  原证据引用：` 123c60108ef98f8f6a240cdbdbec5513538a3011 ` → ` eadc4da0c975dbb65489bd990b48524b23489cc5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` a610119f49b547467a8871c6853ed1c04932d198 ` 和原目标 ` c4f8494662684cfad8c29ba343c23919d40dbf0d ` 查询。
- 原审核说明：` 此次包含了 DeckShell/3rdparty/waylib-shared/ 的更新。 `。
- 同一 Treeland 来源的 C / waylib-shared 目标：` be76893d3d5b20494567b8b7041420db299d3507 `；跨仓定位 ` docs/treeland-sync/20260909_treeland_0_8_14_to_0_9_1_local_sync/summary.md `，不是本仓相对链接。

<a id="entry-493"></a>
### 493. N7 / ` refactor: replace hardcoded etc path with CMake variable `

- 本仓内容路径：` compositor/CMakeLists.txt `、` compositor/src/CMakeLists.txt `、` compositor/src/seat/helper.cpp `。
- 实际改变：` compositor/CMakeLists.txt `、` compositor/src/CMakeLists.txt `、` compositor/src/seat/helper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` be76893d3d5b20494567b8b7041420db299d3507 ` → ` be76893d3d5b20494567b8b7041420db299d3507 `。
  原证据引用：` eadc4da0c975dbb65489bd990b48524b23489cc5 ` → ` eadc4da0c975dbb65489bd990b48524b23489cc5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 660b4f0f3cccb43371c63931aa96429f1b8621c7 ` 和原目标 ` 2453dd21c33137e4e8186b44852c805d25a78f5d ` 查询。
- 原审核说明：` 接入来源的可配置 TREELAND_SYSCONFDIR 并供 seat 配置加载使用，同时保留本地 GNUInstallDirs 路径计算和 DeckShell QML 编译目录定义；两组定义用途独立，不互相覆盖。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/d8bbabc055577e9da132aa71e999d07d0609bf60.md)。

<a id="entry-494"></a>
### 494. N7 / ` ci: skip Debian test target builds `

- 本仓内容路径：` .github/workflows/treeland-archlinux-build.yml `、` .github/workflows/treeland-deepin-build.yml `、` compositor/CMakeLists.txt `、` compositor/debian/rules `、` compositor/tests/CMakeLists.txt `。
- 实际改变：` .github/workflows/treeland-archlinux-build.yml `、` .github/workflows/treeland-deepin-build.yml `、` compositor/CMakeLists.txt `、` compositor/debian/rules `、` compositor/tests/CMakeLists.txt `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` be76893d3d5b20494567b8b7041420db299d3507 ` → ` be76893d3d5b20494567b8b7041420db299d3507 `。
  原证据引用：` eadc4da0c975dbb65489bd990b48524b23489cc5 ` → ` eadc4da0c975dbb65489bd990b48524b23489cc5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` f26fd6ec0d0afe0b44d03877c30d7618f5fd3b79 ` 和原目标 ` 24475024dabeb7b09ee6d6ff0df35a1a42594f80 ` 查询。

<a id="entry-495"></a>
### 495. N7 / ` test(protocols): forcibly reap test service helpers `

- 本仓内容路径：` compositor/tests/protocols/framework/test-dconfig-service.cpp `。
- 实际改变：` compositor/tests/protocols/framework/test-dconfig-service.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` be76893d3d5b20494567b8b7041420db299d3507 ` → ` be76893d3d5b20494567b8b7041420db299d3507 `。
  原证据引用：` eadc4da0c975dbb65489bd990b48524b23489cc5 ` → ` eadc4da0c975dbb65489bd990b48524b23489cc5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 3d74c4c805a7ce5768a8ce8fc1af638a8fadff60 ` 和原目标 ` 081276dfc30da0d22889d442410e74a51eb71fe6 ` 查询。

<a id="entry-496"></a>
### 496. N7 / ` feat(treeland-debug): adb-style debugger with scene tree, capture fallback and live-monitor interrupt `

- 本仓内容路径：` .github/workflows/treeland-archlinux-build.yml `、` compositor/CMakeLists.txt `、` compositor/README.md `、` compositor/README.zh_CN.md `、` compositor/debian/control `、` compositor/src/modules/resource/treelandremotesource.cpp `、` compositor/src/modules/resource/treelandremotesource.h `、` compositor/src/modules/resource/treelandwindowtree.rep `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/tests/CMakeLists.txt `、` compositor/tests/test_treeland_debug/CMakeLists.txt `、` compositor/tests/test_treeland_debug/main.cpp `、` compositor/tools/treeland-debug/CMakeLists.txt `、` compositor/tools/treeland-debug/README.md `、` compositor/tools/treeland-debug/debughelpers.cpp `、` compositor/tools/treeland-debug/debughelpers.h `、` compositor/tools/treeland-debug/debugserver.cpp `、` compositor/tools/treeland-debug/debugserver.h `、` compositor/tools/treeland-debug/debugsession.cpp `、` compositor/tools/treeland-debug/debugsession.h `、` compositor/tools/treeland-debug/main.cpp `。
- 实际改变：` .github/workflows/treeland-archlinux-build.yml `、` compositor/CMakeLists.txt `、` compositor/README.md `、` compositor/README.zh_CN.md `、` compositor/debian/control `、` compositor/src/modules/resource/treelandremotesource.cpp `、` compositor/src/modules/resource/treelandremotesource.h `、` compositor/src/modules/resource/treelandwindowtree.rep `、` compositor/src/seat/helper.cpp `、` compositor/src/seat/helper.h `、` compositor/tests/CMakeLists.txt `、` compositor/tests/test_treeland_debug/CMakeLists.txt `、` compositor/tests/test_treeland_debug/main.cpp `、` compositor/tools/treeland-debug/CMakeLists.txt `、` compositor/tools/treeland-debug/README.md `、` compositor/tools/treeland-debug/debughelpers.cpp `、` compositor/tools/treeland-debug/debughelpers.h `、` compositor/tools/treeland-debug/debugserver.cpp `、` compositor/tools/treeland-debug/debugserver.h `、` compositor/tools/treeland-debug/debugsession.cpp `、` compositor/tools/treeland-debug/debugsession.h `、` compositor/tools/treeland-debug/main.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` be76893d3d5b20494567b8b7041420db299d3507 ` → ` be76893d3d5b20494567b8b7041420db299d3507 `。
  原证据引用：` eadc4da0c975dbb65489bd990b48524b23489cc5 ` → ` eadc4da0c975dbb65489bd990b48524b23489cc5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 66eb7b7058b3dc9200ab056c4fa796527a9ca144 ` 和原目标 ` a625f69e1043af631043c43b24c71542db8da3eb ` 查询。
- 原审核说明：` 接入来源的 treeland-debug 工具及测试，新增调试源编译定义，同时完整保留既有 sanitizer 配置、本地回归和条件 DDM 测试入口；不重复添加 sanitizer flags，不以新测试替换旧测试。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/271c5bbf25ca971c0cd80824df40e074f8ba5945.md)。

<a id="entry-497"></a>
### 497. N7 / ` fix(treeland-debug): async capture, QMetaEnum keys, default-on source `

- 本仓内容路径：` compositor/CMakeLists.txt `、` compositor/src/modules/resource/treelandremotesource.cpp `、` compositor/src/modules/resource/treelandremotesource.h `、` compositor/src/modules/resource/treelandwindowtree.rep `、` compositor/tests/test_treeland_debug/main.cpp `、` compositor/tools/treeland-debug/debughelpers.cpp `、` compositor/tools/treeland-debug/debughelpers.h `、` compositor/tools/treeland-debug/debugserver.cpp `、` compositor/tools/treeland-debug/debugserver.h `、` compositor/tools/treeland-debug/debugsession.cpp `、` compositor/tools/treeland-debug/debugsession.h `、` compositor/tools/treeland-debug/main.cpp `。
- 实际改变：` compositor/CMakeLists.txt `、` compositor/src/modules/resource/treelandremotesource.cpp `、` compositor/src/modules/resource/treelandremotesource.h `、` compositor/src/modules/resource/treelandwindowtree.rep `、` compositor/tests/test_treeland_debug/main.cpp `、` compositor/tools/treeland-debug/debughelpers.cpp `、` compositor/tools/treeland-debug/debughelpers.h `、` compositor/tools/treeland-debug/debugserver.cpp `、` compositor/tools/treeland-debug/debugserver.h `、` compositor/tools/treeland-debug/debugsession.cpp `、` compositor/tools/treeland-debug/debugsession.h `、` compositor/tools/treeland-debug/main.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` be76893d3d5b20494567b8b7041420db299d3507 ` → ` be76893d3d5b20494567b8b7041420db299d3507 `。
  原证据引用：` eadc4da0c975dbb65489bd990b48524b23489cc5 ` → ` eadc4da0c975dbb65489bd990b48524b23489cc5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 6587755e422a878b681a5cdfd9bb12b999c02c33 ` 和原目标 ` a12a9cca017f2bb17565459e29dc0c4c1a87c4ac ` 查询。
- 原审核说明：` 按来源改为默认编译调试源且仍由 debugSource 配置控制运行时启用；保留既有 ASan 定义且不重复注入，接续原生异步捕获与枚举键名修订，仅去除三个新头文件新增的空白 EOF 行。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/d8ce6ae0db5497a0e674dd579dd9b9d796eca9a1.md)。

<a id="entry-498"></a>
### 498. N7 / ` fix(treeland-debug): use QXkbCommon for Qt::Key to evdev conversion `

- 本仓内容路径：` compositor/src/modules/resource/treelandremotesource.cpp `。
- 实际改变：` compositor/src/modules/resource/treelandremotesource.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` be76893d3d5b20494567b8b7041420db299d3507 ` → ` be76893d3d5b20494567b8b7041420db299d3507 `。
  原证据引用：` eadc4da0c975dbb65489bd990b48524b23489cc5 ` → ` eadc4da0c975dbb65489bd990b48524b23489cc5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 02970b2654e734ed2f4ba076e79cd92d8f7d0c0f ` 和原目标 ` 6e12ca78126e4ed42def12d63fb6b970e217eb8d ` 查询。

<a id="entry-499"></a>
### 499. N7 / ` i18n: Updates for project TreeLand (#1346) `

- 本仓内容路径：` compositor/src/plugins/lockscreen/translations/lockscreen.ar.ts `、` compositor/src/plugins/multitaskview/translations/multitaskview.ar.ts `、` compositor/translations/treeland.ar.ts `。
- 实际改变：` compositor/src/plugins/lockscreen/translations/lockscreen.ar.ts `、` compositor/src/plugins/multitaskview/translations/multitaskview.ar.ts `、` compositor/translations/treeland.ar.ts `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` be76893d3d5b20494567b8b7041420db299d3507 ` → ` be76893d3d5b20494567b8b7041420db299d3507 `。
  原证据引用：` eadc4da0c975dbb65489bd990b48524b23489cc5 ` → ` eadc4da0c975dbb65489bd990b48524b23489cc5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` a1ef0412ee9992b052c833d3eda797a549cd628a ` 和原目标 ` afeece1396afd5182d201782be026afdba321061 ` 查询。

<a id="entry-500"></a>
### 500. N7 / ` feat(greeter): support undecided state waiting for DDM decision `

- 本仓内容路径：` compositor/src/core/lockscreen.cpp `、` compositor/src/greeter/greeterproxy.cpp `、` compositor/src/greeter/greeterproxy.h `、` compositor/src/greeter/usermodel.cpp `、` compositor/src/plugins/lockscreen/qml/Greeter.qml `、` compositor/src/plugins/lockscreen/qml/UserInput.qml `、` compositor/src/seat/helper.cpp `。
- 实际改变：` compositor/src/core/lockscreen.cpp `、` compositor/src/greeter/greeterproxy.cpp `、` compositor/src/greeter/greeterproxy.h `、` compositor/src/greeter/usermodel.cpp `、` compositor/src/plugins/lockscreen/qml/Greeter.qml `、` compositor/src/plugins/lockscreen/qml/UserInput.qml `、` compositor/src/seat/helper.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` be76893d3d5b20494567b8b7041420db299d3507 ` → ` be76893d3d5b20494567b8b7041420db299d3507 `。
  原证据引用：` eadc4da0c975dbb65489bd990b48524b23489cc5 ` → ` eadc4da0c975dbb65489bd990b48524b23489cc5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` fc7e6582ee247ec1e8e1059c53aa6e131c413586 ` 和原目标 ` 8be1df924b752263a8a4481c84e503d7b1ff88ae ` 查询。
- 原审核说明：` 接入 DDM undecided 等待状态及无密码账户登录分支；保留原密码显示切换按钮，新无密码登录按钮独立调用 userLogin，并保持 DeckShell QML 模块导入，不混淆两个按钮的动作。 合入本来源的真实协议集成诊断修复；保持正常产品配置、真实协议请求和完整断言，不禁用测试或引入兼容层。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/ae4974963937d12a722d2a8ae73a2cd1600138e4.md)。

<a id="entry-501"></a>
### 501. N7 / ` fix(greeter): guard ShowGreeter for DDM < 0.3.8 `

- 本仓内容路径：` compositor/src/CMakeLists.txt `、` compositor/src/greeter/greeterproxy.cpp `。
- 实际改变：` compositor/src/CMakeLists.txt `、` compositor/src/greeter/greeterproxy.cpp `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` be76893d3d5b20494567b8b7041420db299d3507 ` → ` be76893d3d5b20494567b8b7041420db299d3507 `。
  原证据引用：` eadc4da0c975dbb65489bd990b48524b23489cc5 ` → ` eadc4da0c975dbb65489bd990b48524b23489cc5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` 19919612da6be2ec7f38f6f124a3532a9447bcad ` 和原目标 ` 673da7a0d47b338749fe03ba2e19918fd8dc9daa ` 查询。

<a id="entry-502"></a>
### 502. N7 / ` chore: bump version to 0.9.1 `

- 本仓内容路径：` compositor/CMakeLists.txt `、` compositor/debian/changelog `。
- 实际改变：` compositor/CMakeLists.txt `、` compositor/debian/changelog `。
- 排除的来源路径：无。
- 依赖 ` 3rdparty/waylib-shared `：unchanged；` be76893d3d5b20494567b8b7041420db299d3507 ` → ` be76893d3d5b20494567b8b7041420db299d3507 `。
  原证据引用：` eadc4da0c975dbb65489bd990b48524b23489cc5 ` → ` eadc4da0c975dbb65489bd990b48524b23489cc5 `。
- lane 依据：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/parent-evidence.json`；以来源 ` fd573cf44fb06ee1eebcdd8c39716d1c797b64d4 ` 和原目标 ` bf1092f11da49ffe4cdaacf148dab7f60d02198d ` 查询。
- 原审核说明：` 同步来源的 0.9.1 版本和 changelog，保留 DeckCompositor 项目名称、多行 project 定义及所有本地构建选项。 `。
- 逐路径理由与增量对照：[本仓适配详情](adaptations/d76ef0a531100d18bfb966c33531e28e03b838fe.md)。

## 节点验证与历史边界

### N1 / 原节点验收

- 原报告状态：**pass**。
- 来源验收终点：` 2df4c21c0499b46229f1ef0080cc265994b4fd60 `；普通中间提交不作构建承诺。
- 原候选 P / DeckShell：` 055be261d35138ec678b3a7aaf1521bfc2d9a05e `。
- 原候选 C / waylib-shared：` 5832583291b2ad14c4e723e26f5c5b851e6dbe03 `。
- 原候选 R / wlroots：` None `。
- 原报告：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/sync-report.json`。
- deckshell_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/deckshell-verify.json`。
- waylib_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/waylib-verify.json`。
- wlroots_verify：pass / not-applicable；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/wlroots-verify.json`。
- gitlink_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/gitlink-verify.json`。
- nested_gitlink_verify：pass / not-applicable；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/nested-gitlink-verify.json`。
- protocol_tracking：pass / not-triggered；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/protocol-candidates.json`。
- contract_audit：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/waylib-contract-audit.json`。
- child_materialization：pass / created；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/child-materialization.json`。

| 原验证项 | 结果 | 退出码 | 原测试计数 | 原始日志 |
|---|---|---|---|---|
| ` waylib-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/logs/waylib-base-configure-attempt-1.log` |
| ` waylib-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/logs/waylib-candidate-configure-attempt-1.log` |
| ` deckshell-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/logs/deckshell-configure-attempt-1.log` |
| ` deckshell-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/logs/deckshell-build-attempt-1.log` |
| ` waylib-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/logs/waylib-base-build-attempt-1.log` |
| ` waylib-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/logs/waylib-base-install-attempt-1.log` |
| ` waylib-base-ctest ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/logs/waylib-base-ctest-attempt-1.log` |
| ` waylib-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/logs/waylib-candidate-build-attempt-1.log` |
| ` waylib-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/logs/waylib-candidate-install-attempt-1.log` |
| ` waylib-ctest ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/logs/waylib-ctest-attempt-1.log` |
| ` waylib-package-consumer-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/logs/waylib-package-consumer-configure-attempt-1.log` |
| ` waylib-package-consumer-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/logs/waylib-package-consumer-build-attempt-1.log` |
| ` waylib-package-consumer ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/logs/waylib-package-consumer-attempt-1.log` |
| ` deckshell-compositor-ctest ` / attempt 1 | PASS | 0 | ` {'total': 21, 'passed': 21, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/logs/deckshell-compositor-ctest-attempt-1.log` |
| ` deckshell-top-level-ctest ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N1-attempt-4/logs/deckshell-top-level-ctest-attempt-1.log` |

以上状态属于原候选；未替换成整理后 SHA，也未因本次生成而重新通过。

### N2 / 原节点验收

- 原报告状态：**pass**。
- 来源验收终点：` 1ffe0010193a8c696ef6436a4c436f57bbb1e8ec `；普通中间提交不作构建承诺。
- 原候选 P / DeckShell：` 4071efb9caf5adc60d236f41c9ca1bbfb49f8c10 `。
- 原候选 C / waylib-shared：` 05e24276e3d5878b653adf692cd33391038dd398 `。
- 原候选 R / wlroots：` 88a869855742281c98c22cab9641b317b8d065ef `。
- 原报告：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/initialization-report.json`。

| 原验证项 | 结果 | 退出码 | 原测试计数 | 原始日志 |
|---|---|---|---|---|
| ` wlroots-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/wlroots-base-configure-attempt-1.log` |
| ` wlroots-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/wlroots-base-build-attempt-1.log` |
| ` wlroots-base-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/wlroots-base-test-attempt-1.log` |
| ` wlroots-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/wlroots-base-install-attempt-1.log` |
| ` wlroots-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/wlroots-candidate-configure-attempt-1.log` |
| ` wlroots-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/wlroots-candidate-build-attempt-1.log` |
| ` wlroots-candidate-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/wlroots-candidate-test-attempt-1.log` |
| ` wlroots-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/wlroots-candidate-install-attempt-1.log` |
| ` waylib-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/waylib-candidate-configure-attempt-1.log` |
| ` waylib-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/waylib-candidate-build-attempt-1.log` |
| ` waylib-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/waylib-candidate-install-attempt-1.log` |
| ` waylib-ctest ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/waylib-ctest-attempt-1.log` |
| ` waylib-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/waylib-base-configure-attempt-1.log` |
| ` waylib-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/waylib-base-build-attempt-1.log` |
| ` waylib-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/waylib-base-install-attempt-1.log` |
| ` waylib-base-ctest ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/waylib-base-ctest-attempt-1.log` |
| ` waylib-package-consumer-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/waylib-package-consumer-configure-attempt-1.log` |
| ` waylib-package-consumer-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/waylib-package-consumer-build-attempt-1.log` |
| ` waylib-package-consumer ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/waylib-package-consumer-attempt-1.log` |
| ` deckshell-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/deckshell-configure-attempt-1.log` |
| ` deckshell-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/deckshell-build-attempt-1.log` |
| ` deckshell-compositor-ctest ` / attempt 1 | PASS | 0 | ` {'total': 21, 'passed': 21, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/deckshell-compositor-ctest-attempt-1.log` |
| ` deckshell-top-level-ctest ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N2-attempt-4/initialization/logs/deckshell-top-level-ctest-attempt-1.log` |

以上状态属于原候选；未替换成整理后 SHA，也未因本次生成而重新通过。

### N3 / 原节点验收

- 原报告状态：**pass**。
- 来源验收终点：` 4db6917f873990966f58578abe7dca8b8b371d36 `；普通中间提交不作构建承诺。
- 原候选 P / DeckShell：` dc4f7d20294b8b6fa9decc39a783bf504246f34e `。
- 原候选 C / waylib-shared：` 1db059be68d697b7c47c7003f7433e0d1836139a `。
- 原候选 R / wlroots：` 4bc1705abf5b1250ea5888b6387b66d54718e331 `。
- 原报告：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/sync-report.json`。
- deckshell_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/deckshell-verify.json`。
- waylib_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/waylib-verify.json`。
- wlroots_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/wlroots-verify.json`。
- gitlink_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/gitlink-verify.json`。
- nested_gitlink_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/nested-gitlink-verify.json`。
- protocol_tracking：pass / not-triggered；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/protocol-candidates.json`。
- contract_audit：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/waylib-contract-audit.json`。
- child_materialization：pass / created；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/child-materialization.json`。

| 原验证项 | 结果 | 退出码 | 原测试计数 | 原始日志 |
|---|---|---|---|---|
| ` wlroots-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/wlroots-base-configure-attempt-1.log` |
| ` wlroots-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/wlroots-base-build-attempt-1.log` |
| ` wlroots-base-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/wlroots-base-test-attempt-1.log` |
| ` wlroots-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/wlroots-base-install-attempt-1.log` |
| ` wlroots-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/wlroots-candidate-configure-attempt-1.log` |
| ` wlroots-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/wlroots-candidate-build-attempt-1.log` |
| ` wlroots-candidate-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/wlroots-candidate-test-attempt-1.log` |
| ` wlroots-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/wlroots-candidate-install-attempt-1.log` |
| ` waylib-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/waylib-candidate-configure-attempt-1.log` |
| ` waylib-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/waylib-candidate-build-attempt-1.log` |
| ` waylib-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/waylib-candidate-install-attempt-1.log` |
| ` waylib-ctest ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/waylib-ctest-attempt-1.log` |
| ` waylib-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/waylib-base-configure-attempt-1.log` |
| ` waylib-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/waylib-base-build-attempt-1.log` |
| ` waylib-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/waylib-base-install-attempt-1.log` |
| ` waylib-base-ctest ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/waylib-base-ctest-attempt-1.log` |
| ` waylib-package-consumer-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/waylib-package-consumer-configure-attempt-1.log` |
| ` waylib-package-consumer-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/waylib-package-consumer-build-attempt-1.log` |
| ` waylib-package-consumer ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/waylib-package-consumer-attempt-1.log` |
| ` deckshell-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/deckshell-configure-attempt-1.log` |
| ` deckshell-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/deckshell-build-attempt-1.log` |
| ` deckshell-compositor-ctest ` / attempt 1 | PASS | 0 | ` {'total': 21, 'passed': 21, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/deckshell-compositor-ctest-attempt-1.log` |
| ` deckshell-top-level-ctest ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-3/logs/deckshell-top-level-ctest-attempt-1.log` |

以上状态属于原候选；未替换成整理后 SHA，也未因本次生成而重新通过。

### N3-attempt-2 / 历史失败/先前尝试

- 原报告状态：**blocked**。
- 来源验收终点：` 4db6917f873990966f58578abe7dca8b8b371d36 `；普通中间提交不作构建承诺。
- 原候选 P / DeckShell：` cc92b79ee541e5ec7b0371385f21259206a3c6a9 `。
- 原候选 C / waylib-shared：` b240153223af7d11a816801bbb3e695368cde110 `。
- 原候选 R / wlroots：` 50291db598e076b9e44bc50e5c36e8c151a53c9a `。
- 原报告：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/sync-report.json`。
- deckshell_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/deckshell-verify.json`。
- waylib_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/waylib-verify.json`。
- wlroots_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/wlroots-verify.json`。
- gitlink_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/gitlink-verify.json`。
- nested_gitlink_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/nested-gitlink-verify.json`。
- protocol_tracking：pass / not-triggered；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/protocol-candidates.json`。
- contract_audit：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/waylib-contract-audit.json`。
- child_materialization：pass / created；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/child-materialization.json`。

| 原验证项 | 结果 | 退出码 | 原测试计数 | 原始日志 |
|---|---|---|---|---|
| ` wlroots-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/wlroots-base-configure-attempt-1.log` |
| ` wlroots-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/wlroots-base-build-attempt-1.log` |
| ` wlroots-base-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/wlroots-base-test-attempt-1.log` |
| ` wlroots-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/wlroots-base-install-attempt-1.log` |
| ` wlroots-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/wlroots-candidate-configure-attempt-1.log` |
| ` wlroots-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/wlroots-candidate-build-attempt-1.log` |
| ` wlroots-candidate-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/wlroots-candidate-test-attempt-1.log` |
| ` wlroots-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/wlroots-candidate-install-attempt-1.log` |
| ` waylib-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/waylib-candidate-configure-attempt-1.log` |
| ` waylib-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/waylib-candidate-build-attempt-1.log` |
| ` waylib-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/waylib-candidate-install-attempt-1.log` |
| ` waylib-ctest ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/waylib-ctest-attempt-1.log` |
| ` waylib-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/waylib-base-configure-attempt-1.log` |
| ` waylib-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/waylib-base-build-attempt-1.log` |
| ` waylib-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/waylib-base-install-attempt-1.log` |
| ` waylib-base-ctest ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/waylib-base-ctest-attempt-1.log` |
| ` waylib-package-consumer-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/waylib-package-consumer-configure-attempt-1.log` |
| ` waylib-package-consumer-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/waylib-package-consumer-build-attempt-1.log` |
| ` waylib-package-consumer ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/waylib-package-consumer-attempt-1.log` |
| ` deckshell-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/deckshell-configure-attempt-1.log` |
| ` deckshell-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/deckshell-build-attempt-1.log` |
| ` deckshell-compositor-ctest ` / attempt 1 | FAIL | 8 | ` {'total': 21, 'passed': 18, 'failed': 3, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N3-attempt-2/logs/deckshell-compositor-ctest-attempt-1.log` |

以上状态属于原候选；未替换成整理后 SHA，也未因本次生成而重新通过。

### N4 / 原节点验收

- 原报告状态：**pass**。
- 来源验收终点：` 24c1a0b547fc8a1c6617bdff147efcbad03c2f98 `；普通中间提交不作构建承诺。
- 原候选 P / DeckShell：` d1be07121ea0f20bf87a128208a703a0dbbf3b68 `。
- 原候选 C / waylib-shared：` 0d8c99c886084818a1caee37995390bb69603184 `。
- 原候选 R / wlroots：` 4507a6f414191bcfc150a966ba251c89f864663f `。
- 原报告：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/sync-report.json`。
- deckshell_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/deckshell-verify.json`。
- waylib_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/waylib-verify.json`。
- wlroots_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/wlroots-verify.json`。
- gitlink_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/gitlink-verify.json`。
- nested_gitlink_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/nested-gitlink-verify.json`。
- protocol_tracking：pass / not-triggered；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/protocol-candidates.json`。
- contract_audit：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/waylib-contract-audit.json`。
- child_materialization：pass / created；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/child-materialization.json`。

| 原验证项 | 结果 | 退出码 | 原测试计数 | 原始日志 |
|---|---|---|---|---|
| ` wlroots-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/wlroots-base-configure-attempt-1.log` |
| ` wlroots-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/wlroots-base-build-attempt-1.log` |
| ` wlroots-base-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/wlroots-base-test-attempt-1.log` |
| ` wlroots-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/wlroots-base-install-attempt-1.log` |
| ` wlroots-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/wlroots-candidate-configure-attempt-1.log` |
| ` wlroots-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/wlroots-candidate-build-attempt-1.log` |
| ` wlroots-candidate-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/wlroots-candidate-test-attempt-1.log` |
| ` wlroots-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/wlroots-candidate-install-attempt-1.log` |
| ` waylib-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/waylib-candidate-configure-attempt-1.log` |
| ` waylib-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/waylib-candidate-build-attempt-1.log` |
| ` waylib-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/waylib-candidate-install-attempt-1.log` |
| ` waylib-ctest ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/waylib-ctest-attempt-1.log` |
| ` waylib-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/waylib-base-configure-attempt-1.log` |
| ` waylib-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/waylib-base-build-attempt-1.log` |
| ` waylib-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/waylib-base-install-attempt-1.log` |
| ` waylib-base-ctest ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/waylib-base-ctest-attempt-1.log` |
| ` waylib-package-consumer-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/waylib-package-consumer-configure-attempt-1.log` |
| ` waylib-package-consumer-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/waylib-package-consumer-build-attempt-1.log` |
| ` waylib-package-consumer ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/waylib-package-consumer-attempt-1.log` |
| ` deckshell-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/deckshell-configure-attempt-1.log` |
| ` deckshell-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/deckshell-build-attempt-1.log` |
| ` deckshell-compositor-ctest ` / attempt 1 | PASS | 0 | ` {'total': 21, 'passed': 21, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/deckshell-compositor-ctest-attempt-1.log` |
| ` deckshell-top-level-ctest ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-3/logs/deckshell-top-level-ctest-attempt-1.log` |

以上状态属于原候选；未替换成整理后 SHA，也未因本次生成而重新通过。

### N4-attempt-2 / 历史失败/先前尝试

- 原报告状态：**blocked**。
- 来源验收终点：` 24c1a0b547fc8a1c6617bdff147efcbad03c2f98 `；普通中间提交不作构建承诺。
- 原候选 P / DeckShell：` 6ba6fd6346fb89d4bb502d0caf612abd06b74c68 `。
- 原候选 C / waylib-shared：` 3b47a60c3380293fcc418b55260256bf71c074d1 `。
- 原候选 R / wlroots：` 5c8b9bdfd6f4a610cef869bcb8988ad6f77026b7 `。
- 原报告：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/sync-report.json`。
- deckshell_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/deckshell-verify.json`。
- waylib_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/waylib-verify.json`。
- wlroots_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/wlroots-verify.json`。
- gitlink_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/gitlink-verify.json`。
- nested_gitlink_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/nested-gitlink-verify.json`。
- protocol_tracking：pass / not-triggered；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/protocol-candidates.json`。
- contract_audit：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/waylib-contract-audit.json`。
- child_materialization：pass / created；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/child-materialization.json`。

| 原验证项 | 结果 | 退出码 | 原测试计数 | 原始日志 |
|---|---|---|---|---|
| ` wlroots-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/wlroots-base-configure-attempt-1.log` |
| ` wlroots-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/wlroots-base-build-attempt-1.log` |
| ` wlroots-base-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/wlroots-base-test-attempt-1.log` |
| ` wlroots-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/wlroots-base-install-attempt-1.log` |
| ` wlroots-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/wlroots-candidate-configure-attempt-1.log` |
| ` wlroots-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/wlroots-candidate-build-attempt-1.log` |
| ` wlroots-candidate-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/wlroots-candidate-test-attempt-1.log` |
| ` wlroots-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/wlroots-candidate-install-attempt-1.log` |
| ` waylib-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/waylib-candidate-configure-attempt-1.log` |
| ` waylib-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/waylib-candidate-build-attempt-1.log` |
| ` waylib-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/waylib-candidate-install-attempt-1.log` |
| ` waylib-ctest ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/waylib-ctest-attempt-1.log` |
| ` waylib-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/waylib-base-configure-attempt-1.log` |
| ` waylib-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/waylib-base-build-attempt-1.log` |
| ` waylib-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/waylib-base-install-attempt-1.log` |
| ` waylib-base-ctest ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/waylib-base-ctest-attempt-1.log` |
| ` waylib-package-consumer-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/waylib-package-consumer-configure-attempt-1.log` |
| ` waylib-package-consumer-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/waylib-package-consumer-build-attempt-1.log` |
| ` waylib-package-consumer ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/waylib-package-consumer-attempt-1.log` |
| ` deckshell-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/deckshell-configure-attempt-1.log` |
| ` deckshell-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/deckshell-build-attempt-1.log` |
| ` deckshell-compositor-ctest ` / attempt 1 | FAIL | 8 | ` {'total': 21, 'passed': 20, 'failed': 1, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N4-attempt-2/logs/deckshell-compositor-ctest-attempt-1.log` |

以上状态属于原候选；未替换成整理后 SHA，也未因本次生成而重新通过。

### N5 / 原节点验收

- 原报告状态：**pass**。
- 来源验收终点：` 7134887c66e5215182e1a1f648bdc8971f17e864 `；普通中间提交不作构建承诺。
- 原候选 P / DeckShell：` d24d389a597f9be2e619586bcc76b3c0518ceef3 `。
- 原候选 C / waylib-shared：` 11e096a97e13d4b8740cea0d735f758e66b6534c `。
- 原候选 R / wlroots：` c254362a1f79c88d21c773e22373ebe538194169 `。
- 原报告：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/sync-report.json`。
- deckshell_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/deckshell-verify.json`。
- waylib_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/waylib-verify.json`。
- wlroots_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/wlroots-verify.json`。
- gitlink_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/gitlink-verify.json`。
- nested_gitlink_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/nested-gitlink-verify.json`。
- protocol_tracking：pass / not-triggered；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/protocol-candidates.json`。
- contract_audit：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/waylib-contract-audit.json`。
- child_materialization：pass / created；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/child-materialization.json`。

| 原验证项 | 结果 | 退出码 | 原测试计数 | 原始日志 |
|---|---|---|---|---|
| ` deckshell-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/deckshell-configure-attempt-1.log` |
| ` deckshell-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/deckshell-build-attempt-1.log` |
| ` deckshell-compositor-ctest ` / attempt 1 | PASS | 0 | ` {'total': 21, 'passed': 21, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/deckshell-compositor-ctest-attempt-1.log` |
| ` deckshell-top-level-ctest ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/deckshell-top-level-ctest-attempt-1.log` |
| ` waylib-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/waylib-candidate-configure-attempt-1.log` |
| ` waylib-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/waylib-candidate-build-attempt-1.log` |
| ` waylib-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/waylib-candidate-install-attempt-1.log` |
| ` waylib-ctest ` / attempt 1 | PASS | 0 | ` {'total': 8, 'passed': 8, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/waylib-ctest-attempt-1.log` |
| ` waylib-package-consumer-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/waylib-package-consumer-configure-attempt-1.log` |
| ` waylib-package-consumer-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/waylib-package-consumer-build-attempt-1.log` |
| ` waylib-package-consumer ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/waylib-package-consumer-attempt-1.log` |
| ` waylib-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/waylib-base-configure-attempt-1.log` |
| ` waylib-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/waylib-base-build-attempt-1.log` |
| ` waylib-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/waylib-base-install-attempt-1.log` |
| ` waylib-base-ctest ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/waylib-base-ctest-attempt-1.log` |
| ` wlroots-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/wlroots-base-configure-attempt-1.log` |
| ` wlroots-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/wlroots-base-build-attempt-1.log` |
| ` wlroots-base-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/wlroots-base-test-attempt-1.log` |
| ` wlroots-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/wlroots-base-install-attempt-1.log` |
| ` wlroots-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/wlroots-candidate-configure-attempt-1.log` |
| ` wlroots-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/wlroots-candidate-build-attempt-1.log` |
| ` wlroots-candidate-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/wlroots-candidate-test-attempt-1.log` |
| ` wlroots-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N5-attempt-7/logs/wlroots-candidate-install-attempt-1.log` |

以上状态属于原候选；未替换成整理后 SHA，也未因本次生成而重新通过。

### N6 / 原节点验收

- 原报告状态：**pass**。
- 来源验收终点：` ce57dab0259c33eb183589928249ef9e2be149af `；普通中间提交不作构建承诺。
- 原候选 P / DeckShell：` 77d487cedd0b1f1eabf1ec38ee744af3fe4a0930 `。
- 原候选 C / waylib-shared：` 83365fc20abbfdb29b710446d5e3cc5fabc86efe `。
- 原候选 R / wlroots：` eace3155cdc96d6bea3b708255e27f3b28499078 `。
- 原报告：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/sync-report.json`。
- deckshell_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/deckshell-verify.json`。
- waylib_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/waylib-verify.json`。
- wlroots_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/wlroots-verify.json`。
- gitlink_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/gitlink-verify.json`。
- nested_gitlink_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/nested-gitlink-verify.json`。
- protocol_tracking：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/protocol-candidates.json`。
- contract_audit：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/waylib-contract-audit.json`。
- child_materialization：pass / created；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/child-materialization.json`。

| 原验证项 | 结果 | 退出码 | 原测试计数 | 原始日志 |
|---|---|---|---|---|
| ` wlroots-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/wlroots-base-configure-attempt-1.log` |
| ` wlroots-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/wlroots-base-build-attempt-1.log` |
| ` wlroots-base-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/wlroots-base-test-attempt-1.log` |
| ` wlroots-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/wlroots-base-install-attempt-1.log` |
| ` wlroots-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/wlroots-candidate-configure-attempt-1.log` |
| ` wlroots-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/wlroots-candidate-build-attempt-1.log` |
| ` wlroots-candidate-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/wlroots-candidate-test-attempt-1.log` |
| ` wlroots-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/wlroots-candidate-install-attempt-1.log` |
| ` waylib-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/waylib-candidate-configure-attempt-1.log` |
| ` waylib-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/waylib-candidate-build-attempt-1.log` |
| ` waylib-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/waylib-candidate-install-attempt-1.log` |
| ` waylib-ctest ` / attempt 1 | PASS | 0 | ` {'total': 8, 'passed': 8, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/waylib-ctest-attempt-1.log` |
| ` waylib-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/waylib-base-configure-attempt-1.log` |
| ` waylib-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/waylib-base-build-attempt-1.log` |
| ` waylib-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/waylib-base-install-attempt-1.log` |
| ` waylib-base-ctest ` / attempt 1 | PASS | 0 | ` {'total': 8, 'passed': 8, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/waylib-base-ctest-attempt-1.log` |
| ` waylib-package-consumer-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/waylib-package-consumer-configure-attempt-1.log` |
| ` waylib-package-consumer-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/waylib-package-consumer-build-attempt-1.log` |
| ` waylib-package-consumer ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/waylib-package-consumer-attempt-1.log` |
| ` deckshell-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/deckshell-configure-attempt-1.log` |
| ` deckshell-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/deckshell-build-attempt-1.log` |
| ` deckshell-compositor-ctest ` / attempt 1 | PASS | 0 | ` {'total': 22, 'passed': 22, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/deckshell-compositor-ctest-attempt-1.log` |
| ` deckshell-top-level-ctest ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-4/logs/deckshell-top-level-ctest-attempt-1.log` |

以上状态属于原候选；未替换成整理后 SHA，也未因本次生成而重新通过。

### N6-attempt-3 / 历史失败/先前尝试

- 原报告状态：**blocked**。
- 来源验收终点：` ce57dab0259c33eb183589928249ef9e2be149af `；普通中间提交不作构建承诺。
- 原候选 P / DeckShell：` cab31e5953bd0fe725648b99db2eef8bf48e27a5 `。
- 原候选 C / waylib-shared：` 62c4680bde8380fa6f5bd046f950147e6528d845 `。
- 原候选 R / wlroots：` 501746bae90f0690451ea20c8bf8bae98682e11d `。
- 原报告：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/sync-report.json`。
- deckshell_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/deckshell-verify.json`。
- waylib_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/waylib-verify.json`。
- wlroots_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/wlroots-verify.json`。
- gitlink_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/gitlink-verify.json`。
- nested_gitlink_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/nested-gitlink-verify.json`。
- protocol_tracking：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/protocol-candidates.json`。
- contract_audit：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/waylib-contract-audit.json`。
- child_materialization：pass / created；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/child-materialization.json`。

| 原验证项 | 结果 | 退出码 | 原测试计数 | 原始日志 |
|---|---|---|---|---|
| ` wlroots-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/wlroots-base-configure-attempt-1.log` |
| ` wlroots-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/wlroots-base-build-attempt-1.log` |
| ` wlroots-base-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/wlroots-base-test-attempt-1.log` |
| ` wlroots-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/wlroots-base-install-attempt-1.log` |
| ` wlroots-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/wlroots-candidate-configure-attempt-1.log` |
| ` wlroots-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/wlroots-candidate-build-attempt-1.log` |
| ` wlroots-candidate-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/wlroots-candidate-test-attempt-1.log` |
| ` wlroots-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/wlroots-candidate-install-attempt-1.log` |
| ` waylib-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/waylib-candidate-configure-attempt-1.log` |
| ` waylib-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/waylib-candidate-build-attempt-1.log` |
| ` waylib-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/waylib-candidate-install-attempt-1.log` |
| ` waylib-ctest ` / attempt 1 | PASS | 0 | ` {'total': 8, 'passed': 8, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/waylib-ctest-attempt-1.log` |
| ` waylib-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/waylib-base-configure-attempt-1.log` |
| ` waylib-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/waylib-base-build-attempt-1.log` |
| ` waylib-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/waylib-base-install-attempt-1.log` |
| ` waylib-base-ctest ` / attempt 1 | PASS | 0 | ` {'total': 8, 'passed': 8, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/waylib-base-ctest-attempt-1.log` |
| ` waylib-package-consumer-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/waylib-package-consumer-configure-attempt-1.log` |
| ` waylib-package-consumer-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/waylib-package-consumer-build-attempt-1.log` |
| ` waylib-package-consumer ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/waylib-package-consumer-attempt-1.log` |
| ` deckshell-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/deckshell-configure-attempt-1.log` |
| ` deckshell-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/deckshell-build-attempt-1.log` |
| ` deckshell-compositor-ctest ` / attempt 1 | FAIL | 8 | ` {'total': 22, 'passed': 20, 'failed': 2, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N6-attempt-3/logs/deckshell-compositor-ctest-attempt-1.log` |

以上状态属于原候选；未替换成整理后 SHA，也未因本次生成而重新通过。

### N7 / 原节点验收

- 原报告状态：**pass**。
- 来源验收终点：` fd573cf44fb06ee1eebcdd8c39716d1c797b64d4 `；普通中间提交不作构建承诺。
- 原候选 P / DeckShell：` bf1092f11da49ffe4cdaacf148dab7f60d02198d `。
- 原候选 C / waylib-shared：` eadc4da0c975dbb65489bd990b48524b23489cc5 `。
- 原候选 R / wlroots：` eace3155cdc96d6bea3b708255e27f3b28499078 `。
- 原报告：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/sync-report.json`。
- deckshell_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/deckshell-verify.json`。
- waylib_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/waylib-verify.json`。
- wlroots_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/wlroots-verify.json`。
- gitlink_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/gitlink-verify.json`。
- nested_gitlink_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/nested-gitlink-verify.json`。
- protocol_tracking：pass / not-triggered；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/protocol-candidates.json`。
- contract_audit：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/waylib-contract-audit.json`。
- child_materialization：pass / created；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/child-materialization.json`。

| 原验证项 | 结果 | 退出码 | 原测试计数 | 原始日志 |
|---|---|---|---|---|
| ` wlroots-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/wlroots-base-configure-attempt-1.log` |
| ` wlroots-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/wlroots-base-build-attempt-1.log` |
| ` wlroots-base-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/wlroots-base-test-attempt-1.log` |
| ` wlroots-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/wlroots-base-install-attempt-1.log` |
| ` wlroots-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/wlroots-candidate-configure-attempt-1.log` |
| ` wlroots-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/wlroots-candidate-build-attempt-1.log` |
| ` wlroots-candidate-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/wlroots-candidate-test-attempt-1.log` |
| ` wlroots-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/wlroots-candidate-install-attempt-1.log` |
| ` waylib-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/waylib-base-configure-attempt-1.log` |
| ` waylib-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/waylib-base-build-attempt-1.log` |
| ` waylib-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/waylib-base-install-attempt-1.log` |
| ` waylib-base-ctest ` / attempt 1 | PASS | 0 | ` {'total': 8, 'passed': 8, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/waylib-base-ctest-attempt-1.log` |
| ` waylib-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/waylib-candidate-configure-attempt-1.log` |
| ` waylib-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/waylib-candidate-build-attempt-1.log` |
| ` waylib-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/waylib-candidate-install-attempt-1.log` |
| ` waylib-ctest ` / attempt 1 | PASS | 0 | ` {'total': 8, 'passed': 8, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/waylib-ctest-attempt-1.log` |
| ` waylib-package-consumer-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/waylib-package-consumer-configure-attempt-1.log` |
| ` waylib-package-consumer-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/waylib-package-consumer-build-attempt-1.log` |
| ` waylib-package-consumer ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/waylib-package-consumer-attempt-1.log` |
| ` deckshell-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/deckshell-configure-attempt-1.log` |
| ` deckshell-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/deckshell-build-attempt-1.log` |
| ` deckshell-compositor-ctest ` / attempt 1 | PASS | 0 | ` {'total': 55, 'passed': 55, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/deckshell-compositor-ctest-attempt-1.log` |
| ` deckshell-top-level-ctest ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-3/logs/deckshell-top-level-ctest-attempt-1.log` |

以上状态属于原候选；未替换成整理后 SHA，也未因本次生成而重新通过。

### N7-attempt-2 / 历史失败/先前尝试

- 原报告状态：**blocked**。
- 来源验收终点：` fd573cf44fb06ee1eebcdd8c39716d1c797b64d4 `；普通中间提交不作构建承诺。
- 原候选 P / DeckShell：` c9d3dd09c46651a8b3114bb61108564af5f9beed `。
- 原候选 C / waylib-shared：` 9eb721dffdbc592a50b4006cd780f5a190cb55a1 `。
- 原候选 R / wlroots：` eace3155cdc96d6bea3b708255e27f3b28499078 `。
- 原报告：外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/sync-report.json`。
- deckshell_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/deckshell-verify.json`。
- waylib_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/waylib-verify.json`。
- wlroots_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/wlroots-verify.json`。
- gitlink_verify：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/gitlink-verify.json`。
- nested_gitlink_verify：pass / verified；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/nested-gitlink-verify.json`。
- protocol_tracking：pass / not-triggered；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/protocol-candidates.json`。
- contract_audit：pass / 未另设状态；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/waylib-contract-audit.json`。
- child_materialization：pass / created；外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/child-materialization.json`。

| 原验证项 | 结果 | 退出码 | 原测试计数 | 原始日志 |
|---|---|---|---|---|
| ` wlroots-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/wlroots-base-configure-attempt-1.log` |
| ` wlroots-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/wlroots-base-build-attempt-1.log` |
| ` wlroots-base-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/wlroots-base-test-attempt-1.log` |
| ` wlroots-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/wlroots-base-install-attempt-1.log` |
| ` wlroots-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/wlroots-candidate-configure-attempt-1.log` |
| ` wlroots-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/wlroots-candidate-build-attempt-1.log` |
| ` wlroots-candidate-test ` / attempt 1 | NO_TESTS | 0 | ` {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/wlroots-candidate-test-attempt-1.log` |
| ` wlroots-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/wlroots-candidate-install-attempt-1.log` |
| ` waylib-candidate-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/waylib-candidate-configure-attempt-1.log` |
| ` waylib-candidate-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/waylib-candidate-build-attempt-1.log` |
| ` waylib-candidate-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/waylib-candidate-install-attempt-1.log` |
| ` waylib-ctest ` / attempt 1 | PASS | 0 | ` {'total': 8, 'passed': 8, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/waylib-ctest-attempt-1.log` |
| ` waylib-base-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/waylib-base-configure-attempt-1.log` |
| ` waylib-base-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/waylib-base-build-attempt-1.log` |
| ` waylib-base-install ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/waylib-base-install-attempt-1.log` |
| ` waylib-base-ctest ` / attempt 1 | PASS | 0 | ` {'total': 8, 'passed': 8, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/waylib-base-ctest-attempt-1.log` |
| ` waylib-package-consumer-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/waylib-package-consumer-configure-attempt-1.log` |
| ` waylib-package-consumer-build ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/waylib-package-consumer-build-attempt-1.log` |
| ` waylib-package-consumer ` / attempt 1 | PASS | 0 | ` {'total': 3, 'passed': 3, 'failed': 0, 'skipped': 0} ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/waylib-package-consumer-attempt-1.log` |
| ` deckshell-configure ` / attempt 1 | PASS | 0 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/deckshell-configure-attempt-1.log` |
| ` deckshell-build ` / attempt 1 | FAIL | 1 | ` None ` | 外层历史资料：`.helloagents/plans/20260909_treeland_0_8_14_to_0_9_1_local_sync/evidence/N7-attempt-2/logs/deckshell-build-attempt-1.log` |

以上状态属于原候选；未替换成整理后 SHA，也未因本次生成而重新通过。
