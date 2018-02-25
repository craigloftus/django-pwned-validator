from django.conf import settings


DEFAULTS = {
    'ENDPOINT': 'https://api.pwnedpasswords.com/range/',
    'TIMEOUT': 1, # The default is conservative, it should be <20ms typically, 500ms if uncached
    'PREFIX_LENGTH': 5,
    'OCCURRENCE_THRESHOLD': 1, # How many occurrences is too many
    'USER-AGENT': 'github.com/craigloftus/django-pwned-validator',
}


PWNED = getattr(settings, 'PWNED', DEFAULTS)
