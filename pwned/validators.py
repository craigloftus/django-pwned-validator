import logging

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from .client import PwnedClient
from .settings import get_config


logger = logging.getLogger(__name__)


@deconstructible
class PwnedValidator:
    message = _('This password is known to be weak')
    code = 'invalid'
    client = PwnedClient

    def validate(self, password, user=None):
        pwned_client = self.client()
        count = pwned_client.count_occurrences(password)

        if count >= get_config()['OCCURRENCE_THRESHOLD']:
            if get_config()['LOG_ONLY']:
                logger.warn('Password used with %d occurrences in Pwned Password', count, extra={'user': user})
            else:
                logger.info('Password blocked with %d occurrences in Pwned Password', count, extra={'user': user})
                raise ValidationError(self.message, code=self.code)
