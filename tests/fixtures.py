import pytest


@pytest.fixture
def bypass_config_cache():
    from pwned.settings import get_config
    get_config.cache_clear()
    yield
    get_config.cache_clear()
