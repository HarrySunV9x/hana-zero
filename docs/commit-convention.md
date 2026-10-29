# hana-zero 提交规范

基于 [Conventional Commits 1.0.0](https://www.conventionalcommits.org/zh-hans/v1.0.0/) ，结合 hana-zero 的模块边界做了 scope 约束。

## 1. 格式

```text
<type>(<scope>): <subject>

[body]

[footer]
```

- **subject**：一行，不超过 72 字符；结尾不加句号；使用祈使句（"add" 而非 "added"）。
- **body**：可选。说明**为什么**这么做，而不是改了哪几行；每行不超过 100 字符。
- **footer**：可选。用于 `BREAKING CHANGE:`、关闭 issue（`Closes #12`）、评审人等。
- 一个提交只表达一个意图。混了重构和新功能就拆成两个提交。

## 2. type

| type | 用途 |
|---|---|
| `feat` | 新能力（用户或调用方可感知） |
| `fix` | 缺陷修复 |
| `docs` | 文档、注释、ADR |
| `refactor` | 重构，不改变外部行为 |
| `perf` | 性能优化 |
| `test` | 测试新增或调整 |
| `build` | 构建系统、依赖、打包 |
| `ci` | CI / 流水线配置 |
| `chore` | 其他不触及源码的杂项 |
| `revert` | 回滚某个提交 |

## 3. scope（按架构模块划分）

| scope | 对应位置 |
|---|---|
| `api` | `src/hana_zero/api` |
| `runtime` | Agent Runtime / Executor / Journal |
| `context` | Context Manager |
| `memory` | 记忆与检索 |
| `policy` | Policy Engine、审批与权限 |
| `events` | Event Ingress、Outbox、Trigger |
| `models` | Model Gateway / 路由 / 计费 |
| `capabilities` | Capability Registry |
| `mcp` | MCP Client / Server 适配器 |
| `skills` | Skill Loader 与执行 |
| `devices` | Device Node 与设备命令 |
| `workflows` | Temporal 定义与 Activity |
| `protocol` | 跨端协议与 DTO |
| `observability` | OTel Trace / Metrics / Logs |
| `web` / `desktop` / `mobile` / `cli` | 各端应用 |
| `deploy` | systemd unit / Windows 服务 / 启动脚本 |
| `deps` | 依赖版本变更 |
| `docs` | 架构与设计文档 |

scope 省略是允许的（跨模块改动），但**不要自造上表之外的 scope**，需要时先补表。

## 4. 示例

```text
feat(api): add SSE streaming endpoint for agent runs

客户端需要逐步渲染 Agent 输出，原先只能等整段结果返回。
新增 /api/v1/runs/{id}/stream，复用现有 session 鉴权。

Closes #23
```

```text
fix(policy): reject approval whose deadline already elapsed

批准记录在等待期间可能过期，此前仍会被执行。
```

```text
feat(protocol)!: rename device command field `cmd` to `capability`

BREAKING CHANGE: Device Node 需同步升级到 0.2.0 以上版本。
```

## 5. 破坏性变更

- 在 `type(scope)` 后加 `!`，并在 footer 写 `BREAKING CHANGE: <影响与迁移方式>`。
- 破坏性变更必须同步更新 README 或 `docs/` 下的相关文档。

## 6. 本地配置

仓库提供提交模板，执行后 `git commit` 会自动带出格式提示：

```bash
git config commit.template .gitmessage
```

对本仓库单独生效（不污染全局配置），Windows / macOS / Linux 通用。
