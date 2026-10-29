"""pytest 全局钩子：把外部环境变量挡在测试之外。

``Settings(_env_file=None)`` 只关掉了 ``.env`` 文件，pydantic-settings 仍然会读
``os.environ``。只要跑测试的 shell 里 export 过 ``HANA_ENV`` 之类的变量，
``test_config::test_defaults`` 这类断言就会莫名其妙地红——CI 里设了环境变量、
本地手动验证时 export 过一次，都会踩到。

这里在每条用例前把 ``HANA_`` 开头的变量清掉，测试的输入就只剩用例自己传的参数。
"""

import os

import pytest

HANA_ENV_PREFIX = "HANA_"


@pytest.fixture(autouse=True)
def _clear_hana_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """清除外部注入的 ``HANA_*`` 变量（用例结束后由 monkeypatch 自动还原）。"""
    for name in list(os.environ):
        if name.startswith(HANA_ENV_PREFIX):
            monkeypatch.delenv(name, raising=False)
