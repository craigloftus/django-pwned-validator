import pytest

from django.core.exceptions import ValidationError

from pwned.validators import PwnedValidator


@pytest.mark.vcr
def test_validator_found():
    validator = PwnedValidator()
    with pytest.raises(ValidationError):
        validator('password')


@pytest.mark.vcr
def test_validator_not_found():
    validator = PwnedValidator()
    validator('8CEF1E00B20F463C1E48B589B03660D4E3B9EF7A')
