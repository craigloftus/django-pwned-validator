from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from .client import PwnedClient
from . import app_settings


@deconstructible
class PwnedValidator:
    message = _('This password is known to be weak')
    code = 'invalid'
    client = PwnedClient

    def __call__(self, password):
        pwned_client = self.client()
        count = pwned_client.count_occurrences(password)
        if count >= app_settings.PWNED['OCCURRENCE_THRESHOLD']:
            raise ValidationError(self.message, code=self.code)
