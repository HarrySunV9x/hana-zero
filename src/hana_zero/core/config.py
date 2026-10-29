"""应用配置。

配置来源优先级：环境变量 > .env 文件 > 字段默认值。
所有环境变量统一使用 ``HANA_`` 前缀，例如 ``HANA_ENV=prod``。
"""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """hana-zero 服务的运行时配置。"""

    model_config = SettingsConfigDict(
        env_prefix="HANA_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "hana-zero"
    env: str = "dev"
    api_v1_prefix: str = "/api/v1"

    @field_validator("api_v1_prefix")
    @classmethod
    def _normalize_prefix(cls, value: str) -> str:
        """规整路由前缀：补上开头的 ``/``、去掉结尾的 ``/``。

        少了开头的斜杠会生成非法路径（``api/v1/health``），多了结尾的斜杠
        会拼出双斜杠（``/api/v1//health``），两者都在这里一次性纠正。
        """
        normalized = value.strip().rstrip("/") or "/"
        return normalized if normalized.startswith("/") else f"/{normalized}"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """返回进程内唯一的 Settings 实例。

    测试不要改这个单例，直接构造 ``Settings(_env_file=None, ...)`` 传给
    ``create_app()``——否则本地 ``.env`` 会把断言污染掉。
    """
    return Settings()
