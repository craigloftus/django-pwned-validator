import pytest

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from requests.exceptions import Timeout

from pwned.validators import PwnedValidator
from pwned.models import PwnedRecord

from .fixtures import bypass_config_cache


@pytest.mark.vcr
@pytest.mark.django_db
def test_validator_hit():
    validator = PwnedValidator()
    with pytest.raises(ValidationError):
        validator.validate('password')


@pytest.mark.vcr
@pytest.mark.django_db
def test_validator_hit_but_under_threshold(settings, bypass_config_cache):
    settings.PWNED = {
        'OCCURRENCE_NOTIFY_THRESHOLD': 4000000,
    }
    validator = PwnedValidator()
    validator.validate('password')


@pytest.mark.vcr
@pytest.mark.django_db
def test_validator_hit_no_user_not_recorded():
    validator = PwnedValidator()
    with pytest.raises(ValidationError):
        validator.validate('password')
    assert PwnedRecord.objects.count() == 0


@pytest.mark.vcr
@pytest.mark.django_db
def test_validator_hit_recording_disabled(settings, bypass_config_cache):
    settings.PWNED = {
        'RECORD_HITS': False,
    }
    validator = PwnedValidator()
    with pytest.raises(ValidationError):
        validator.validate('password')
    assert PwnedRecord.objects.count() == 0


@pytest.mark.vcr
@pytest.mark.django_db
def test_validator_hit_recorded_with_user():
    validator = PwnedValidator()
    user = User(email='test@test.com')

    with pytest.raises(ValidationError):
        validator.validate('password', user=user)

    record = PwnedRecord.objects.first()

    assert PwnedRecord.objects.count() == 1
    assert record.email == 'test@test.com'


@pytest.mark.vcr
@pytest.mark.django_db
def test_validator_not_found():
    validator = PwnedValidator()
    validator.validate('8CEF1E00B20F463C1E48B589B03660D4E3B9EF7A')
    assert PwnedRecord.objects.count() == 0


def test_validator_api_unreachable(caplog, monkeypatch):
    def raiser(*args, **kwargs):
        raise Timeout()
    monkeypatch.setattr('requests.sessions.Session.get', raiser)
    validator = PwnedValidator()
    # Shouldn't throw a ValidationError
    validator.validate('password')
    for record in caplog.records:
        assert record.levelname == 'ERROR'
