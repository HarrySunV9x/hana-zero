"""健康检查接口。

`/health` 是 liveness 探针，只证明进程还活着，刻意不检查数据库、缓存等外部依赖——
一旦在这里做依赖检查，依赖抖动就会让编排系统把所有实例全部重启，形成雪崩。

将来真正接入外部依赖、并且部署层需要「摘流量但不重启」这种语义时，再补一个
readiness 探针（`/ready`，依赖不可用时返回 503）。在那之前不加，避免出现一个
空有其表、实际什么都没检查的接口。
"""

from typing import Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel

from hana_zero import __version__
from hana_zero.core.config import Settings

router = APIRouter()


class HealthResponse(BaseModel):
    """健康检查响应体。"""

    status: Literal["ok"] = "ok"
    app: str
    version: str
    env: str


@router.get("/health", response_model=HealthResponse, summary="健康检查")
async def health(request: Request) -> HealthResponse:
    """返回服务存活状态，供 systemd、监控拨测与部署检查使用。"""
    settings: Settings = request.app.state.settings
    return HealthResponse(
        app=settings.app_name,
        version=__version__,
        env=settings.env,
    )
