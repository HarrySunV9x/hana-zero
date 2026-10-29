# hana-zero

> 人工智能女儿零号机 · hana-zero

hana-zero 的目标是搭建一个功能完整的 Agent 系统，构造赛博女儿零号机~

设计层面的想法另行记录在
[`docs/architecture-design-v1.md`](docs/architecture-design-v1.md)。该文档目前由 AI 生成，尚未人工检阅，后续会逐步修正。

---

## 一、修改历史

- 2026-10-30：初始化仓库，完成 FastAPI 骨架搭建

---

## 二、目录结构

```text
hana-zero/
├── src/hana_zero/
│   ├── main.py              # create_app() 工厂，只定义不启动
│   ├── __init__.py          # __version__
│   ├── api/
│   │   ├── router.py        # 聚合路由，新模块在此挂载
│   │   └── health.py        # 健康检查 /health
│   └── core/
│       └── config.py        # Settings（HANA_ 前缀）+ 前缀规整
├── tests/
│   ├── test_health.py       # 健康检查测试
│   └── test_config.py       # 配置加载测试
├── docs/
│   ├── architecture-design-v1.md        # 设计草案（未实现）
│   └── commit-convention.md             # 提交规范
├── .env.example             # 环境变量样例（复制为 .env 使用）
├── requirements.txt         # 运行期锁定清单（uv export 生成）
├── uv.lock                  # 全量依赖锁（含 dev）
└── pyproject.toml           # 项目元数据 + [tool.fastapi] 入口 + ruff/mypy/pytest 配置
```

---

## 三、快速开始

前置要求：Python **>= 3.12**（开发验证环境 3.13.14）。

### 开发

首先[安装 `uv`](https://docs.astral.sh/uv/getting-started/installation/)，然后同步依赖：

```bash
uv sync --extra dev   # 建 .venv、装运行期依赖 + dev extra、可编辑方式安装本项目
uv run fastapi dev    # 热重载：保存文件即自动重启
```

开发期依赖（pytest / ruff / mypy / fastapi-cli）放在 `[project.optional-dependencies].dev`
里，**属于 extra 而不是 uv 的默认 dev group**，所以必须带 `--extra dev`；只写 `uv sync`
只会装运行期那 21 个包。

不用 uv 的等价写法：

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
uvicorn hana_zero.main:app --reload
```

### 部署

```bash
# 1) 按锁文件安装运行期依赖（不含 pytest / ruff / mypy）
pip install -r requirements.txt

# 2) 安装本项目本身
pip install --no-deps .

# 3) 起服务。host / port / workers 全在命令行，不进代码
uvicorn hana_zero.main:app --host 0.0.0.0 --port 8000 --workers 4
```

用 uv 的等价写法：

```bash
uv sync --no-dev --frozen
uv run uvicorn hana_zero.main:app --host 0.0.0.0 --port 8000 --workers 4
```

启动后可访问：

- 交互式文档：<http://127.0.0.1:8000/docs>
- 健康检查：<http://127.0.0.1:8000/api/v1/health>

---

## 四、质量门禁

```bash
pytest          # 测试
ruff check .    # lint（E, F, I, UP, B；line-length 100）
mypy src        # 类型检查
```

---

## 五、提交规范

采用 Conventional Commits：

```text
<type>(<scope>): <subject>
```

type：`feat` `fix` `docs` `refactor` `perf` `test` `build` `ci` `chore` `revert`

scope 为可选，用于约束改动归属的模块。完整说明与示例见
[`docs/commit-convention.md`](docs/commit-convention.md)。启用提交模板：

```bash
git config commit.template .gitmessage
```

---

## 许可

[MIT](LICENSE)
