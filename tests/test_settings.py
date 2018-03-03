from pwned.settings import get_config

from .fixtures import bypass_config_cache


def test_override_individual_settings(settings, bypass_config_cache):
    settings.PWNED = {
        'TIMEOUT': 10,
    }
    assert get_config()['TIMEOUT'] == 10
