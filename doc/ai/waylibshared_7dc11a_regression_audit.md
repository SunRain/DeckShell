# WaylibShared 7dc11a v2 历史回归审核

## 审核目的

本文只使用第 303 项封口的 `treeland-target-prefix.v2.json`，记录
commit-aligned-history-rewrite-v2 的 Treeland 来源与目标映射。产品构建、运行测试和
完整 330 项 mapping 由后续独立门禁验证，不作为本文输入。

## 冻结投影

- Treeland remote: `treeland`
- Treeland branch: `master`
- Treeland tracking ref: `refs/remotes/treeland/master`
- first source: `aa5d668cd6f386fa5bd19ee0bcde6d9e2e524598`
- last source: `7da2254d386935f753ed907f8d6e76c1639d01a9`
- sync head target: `4d38d039aa226273fb0316daa9832396381cdf95`
- target prefix canonical SHA-256: `5524932f1f01bd9287e57bc5cda7e02c04d485803fbf016711396a44edf6ddfe`

## 数量门禁

| 项目 | 数量 |
| --- | ---: |
| Treeland targets | 298 |
| other | 233 |
| mixed | 29 |
| dependency-only | 36 |
| duplicate source | 0 |
| duplicate target | 0 |

## 结构性结论

1. 298 个来源均有唯一 v2 target，且来源身份固定为 `treeland/master`。
2. 29 个 mixed 与 36 个 dependency-only 条目均保留 WaylibShared gitlink 承载语义。
3. `fd7baaa323c4c23cf021c29704cf1bb3c89dc244` 保持 `adapted/omitted`，没有降级为 `empty`。
4. 本文不引用 legacy target、v1 target、完整 output mapping 或第 330 项自身 SHA。
