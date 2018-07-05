from functools import lru_cache

from django.conf import settings


DEFAULTS = {
    'ENDPOINT': 'https://api.pwnedpasswords.com/range/',
    'TIMEOUT': 2, # The default is conservative but will cut off some requests; average is 280ms
    'PREFIX_LENGTH': 5,
    'OCCURRENCE_THRESHOLD': 1, # How many occurrences is too many
    'USER_AGENT': 'github.com/craigloftus/django-pwned-validator',
    'LOG_ONLY': False, # Don't raise a validation error, just log the failure
}


@lru_cache()
def get_config():
    SETTINGS = DEFAULTS.copy()
    # Override with any user settings
    SETTINGS.update(getattr(settings, 'PWNED', {}))
    return SETTINGS
