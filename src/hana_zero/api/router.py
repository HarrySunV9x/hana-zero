"""API 聚合路由。新增模块时在此注册即可。"""

from fastapi import APIRouter

from hana_zero.api import health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
