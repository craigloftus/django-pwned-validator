from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from .client import PwnedClient
from .settings import get_config


@deconstructible
class PwnedValidator:
    message = _('This password is in common use, please choose another')
    code = 'invalid'
    client = PwnedClient

    def validate(self, password, user=None):
        pwned_client = self.client()
        count = pwned_client.count_occurrences(password)
        if count >= get_config()['OCCURRENCE_THRESHOLD']:
            raise ValidationError(self.message, code=self.code)
