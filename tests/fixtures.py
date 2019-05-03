import pytest

from django.contrib.auth.models import User


@pytest.fixture
def bypass_config_cache():
    from pwned.settings import get_config
    get_config.cache_clear()
    yield
    get_config.cache_clear()


@pytest.fixture
def make_user():
    def _make_user(username, email, password):
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
    return _make_user
