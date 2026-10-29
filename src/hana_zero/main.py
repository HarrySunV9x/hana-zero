"""FastAPI 应用入口。

本模块只负责**定义**应用，不负责启动。启动交给命令行：

- 开发：``uv run fastapi dev``（入口见 ``pyproject.toml`` 的 ``[tool.fastapi]``）
- 生产：``uvicorn hana_zero.main:app --host 0.0.0.0 --port 8000 --workers 4``

不在代码里写 ``uvicorn.run(...)`` 的原因：监听地址、端口、worker 数、日志格式
都随部署环境变化。写死在代码里，改一个端口就要改代码、重新打包发版。
"""

from fastapi import FastAPI

from hana_zero import __version__
from hana_zero.api.router import api_router
from hana_zero.core.config import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """构建 FastAPI 应用（工厂函数，便于测试注入不同配置）。"""
    settings = settings or get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="hana-zero — 赛博女儿零号机",
    )
    # 挂到 state 上，路由内才能读到当前实例的配置（工厂注入才真正生效）
    app.state.settings = settings
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
