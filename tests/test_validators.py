import logging

from django.core.exceptions import ValidationError
import pytest
from requests.exceptions import Timeout

from pwned.validators import PwnedValidator

from .fixtures import bypass_config_cache


@pytest.mark.vcr
def test_validator_found(caplog):
    caplog.set_level(logging.INFO)
    validator = PwnedValidator()
    with pytest.raises(ValidationError):
        validator.validate('password')
    assert 'Password blocked' in caplog.text


@pytest.mark.vcr
def test_validator_found_logonly(caplog, settings, bypass_config_cache):
    settings.PWNED = {
        'LOG_ONLY': True,
    }
    validator = PwnedValidator()
    validator.validate('password')
    assert 'Password used' in caplog.text


@pytest.mark.vcr
def test_validator_not_found():
    validator = PwnedValidator()
    validator.validate('8CEF1E00B20F463C1E48B589B03660D4E3B9EF7A')


def test_validator_api_unreachable(caplog, monkeypatch):
    def raiser(*args, **kwargs):
        raise Timeout()
    monkeypatch.setattr('requests.sessions.Session.get', raiser)
    validator = PwnedValidator()
    # Shouldn't throw a ValidationError
    validator.validate('password')
    for record in caplog.records:
        assert record.levelname == 'ERROR'
