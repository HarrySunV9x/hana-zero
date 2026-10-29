"""配置加载与规整的单元测试。"""

from hana_zero.core.config import Settings


def load(**overrides: object) -> Settings:
    """构造隔离的 Settings：``_env_file=None`` 使本地 ``.env`` 不参与，断言才稳定。"""
    return Settings(_env_file=None, **overrides)


def test_prefix_is_normalized() -> None:
    assert load(api_v1_prefix="api/v1").api_v1_prefix == "/api/v1"
    assert load(api_v1_prefix="/api/v1/").api_v1_prefix == "/api/v1"
    assert load(api_v1_prefix="/").api_v1_prefix == "/"


def test_defaults() -> None:
    settings = load()
    assert settings.api_v1_prefix == "/api/v1"
    assert settings.env == "dev"
