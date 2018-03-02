import pytest

from django.core.exceptions import ValidationError
from requests.exceptions import Timeout

from pwned.validators import PwnedValidator


@pytest.mark.vcr
def test_validator_found():
    validator = PwnedValidator()
    with pytest.raises(ValidationError):
        validator.validate('password')


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
