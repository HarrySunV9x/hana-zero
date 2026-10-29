"""骨架冒烟测试：确认应用可构建、健康检查行为正确。"""

from fastapi.testclient import TestClient

from hana_zero.core.config import Settings
from hana_zero.main import create_app


def make_client(**overrides: object) -> TestClient:
    """用指定配置构建测试客户端。

    ``_env_file=None`` 关掉本地 ``.env`` 读取：否则开发者按 README 复制出 ``.env`` 后，
    测试断言会被真实环境变量污染。
    """
    return TestClient(create_app(Settings(_env_file=None, **overrides)))


def test_health_returns_ok() -> None:
    response = make_client().get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["version"]


def test_health_reflects_injected_settings() -> None:
    """工厂注入的配置必须能真正传到路由里，而不是被全局单例覆盖。"""
    body = make_client(app_name="hana-test", env="test").get("/api/v1/health").json()

    assert body["app"] == "hana-test"
    assert body["env"] == "test"
