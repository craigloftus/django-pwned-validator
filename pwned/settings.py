from functools import lru_cache

from django.conf import settings


DEFAULTS = {
    'ENDPOINT': 'https://api.pwnedpasswords.com/range/',
    'OCCURRENCE_NOTIFY_THRESHOLD': 1, # How many occurrences cause a email or validation error
    'PREFIX_LENGTH': 5,
    'RECORD_HITS': True,
    'TIMEOUT': 2, # The default is conservative but will cut off some requests; typical is 200ms
    'USER_AGENT': 'github.com/craigloftus/django-pwned-validator',
}


@lru_cache()
def get_config():
    SETTINGS = DEFAULTS.copy()
    # Override with any user settings
    SETTINGS.update(getattr(settings, 'PWNED', {}))
    return SETTINGS
