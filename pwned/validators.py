from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from .client import PwnedClient
from .models import PwnedRecord
from .settings import get_config


@deconstructible
class PwnedValidator:
    message = _("This is a commonly used password")
    code = "invalid"
    client = PwnedClient

    def validate(self, password, user=None):
        pwned_client = self.client()
        count = pwned_client.count_occurrences(password)

        if count and user and get_config()['RECORD_HITS']:
            PwnedRecord.objects.create(
                email = user.email,
                count = count,
            )

        if count >= get_config()['OCCURRENCE_NOTIFY_THRESHOLD']:
            raise ValidationError(self.message, code=self.code)

    def get_help_text(self):
        return _("Your password can't be a commonly used password.")
