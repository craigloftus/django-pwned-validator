from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from .client import PwnedClient
from .settings import get_config


@deconstructible
class PwnedValidator:
    error = _('This password is in common use, please choose another')
    help_text = _("Your password can't be in common use")
    code = 'invalid'
    client = PwnedClient

    def validate(self, password, user=None):
        pwned_client = self.client()
        count = pwned_client.count_occurrences(password)
        if count >= get_config()['OCCURRENCE_THRESHOLD']:
            raise ValidationError(self.error, code=self.code)

    def get_help_text(self):
        return self.help_text
