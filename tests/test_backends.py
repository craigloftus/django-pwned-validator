import pytest

from pwned.backends import PwnedModelBackend
from pwned.models import PwnedRecord

from .fixtures import bypass_config_cache, make_user


@pytest.mark.vcr
@pytest.mark.django_db
def test_login_hit(rf, make_user):
    request = rf.get('/login/')
    backend = PwnedModelBackend()
    user = make_user('test', 'test@test.com', 'password')
    backend.authenticate(request, 'test', 'password')
    record = PwnedRecord.objects.first()
    assert PwnedRecord.objects.count() == 1
    assert record.email == 'test@test.com'


@pytest.mark.vcr
@pytest.mark.django_db
def test_login_hit_recording_disabled(rf, make_user, settings, bypass_config_cache):
    settings.PWNED = {
        'RECORD_HITS': False,
    }
    request = rf.get('/login/')
    backend = PwnedModelBackend()
    user = make_user('test', 'test@test.com', 'password')
    backend.authenticate(request, 'test', 'password')
    assert PwnedRecord.objects.count() == 0


@pytest.mark.vcr
@pytest.mark.django_db
def test_login_failed_hit(rf, make_user):
    request = rf.get('/login/')
    backend = PwnedModelBackend()
    backend.authenticate(request, 'test', 'password')
    assert PwnedRecord.objects.count() == 0
