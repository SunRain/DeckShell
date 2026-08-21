# `treeland-ddm-v1` 测试规范

## 范围

- 测试源码：`compositor/tests/protocols/treeland-ddm-v1/`
- Fixture：协议 fixture。
- 覆盖等级：**I**。

## 构建配置合同

DeckShell 默认 `DISABLE_DDM=ON`，不构建或注册 `DDMInterfaceV1`。此配置下，测试仍建立真实 Wayland 连接、读取 registry 并执行 roundtrip，断言不宣告 `treeland_ddm_v1`；连接失败或意外宣告该接口均失败，不跳过测试。

`DISABLE_DDM=OFF` 时保留下面的全部 DDM 绑定、连接生命周期及事件断言。默认配置的缺席检查不代表已验证启用 DDM 的运行模式。

同一默认配置下，`treeland-dde-shell-lockscreen-desktop-v1` 仍发送真实锁屏请求，并验证在没有 DDM locker、也没有 ext-session-lock 客户端时不改变 Normal 模式；外部锁屏客户端的正向生命周期由现有 `test_session_lock_lifecycle` 覆盖。

## 必须观察到的结果

| 场景 | 客户端动作 | 必须观察到的结果 |
| --- | --- | --- |
| 全局兼容性 | 以 v1 绑定、请求 v2 | global 宣告 v1，绑定版本被限制为 v1 |
| 连接生命周期 | 绑定、连接第二客户端、断开主客户端 | 生产 `DDMInterfaceV1::isConnected()` 跟随主客户端生命周期 |
| 初始流量 | 绑定 global | 没有未请求的事件 |

## 生产结果

验证的是生产接口的连接状态，而非仅仅能够绑定 global。

## 已知边界 / 下一项结果

目前该测试没有额外 DDM 业务请求；协议未来增加请求时，应断言其业务消费者的结果。
