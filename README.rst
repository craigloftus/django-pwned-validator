Django Pwned Passwords Validator
================================

This package provides a password validator for Django that checks submitted
passwords against the `Pwned Passwords API <https://haveibeenpwned.com/API/v2>`_
to help your users protect themselves against credential stuffing attacks.

To protect the security of the password being checked a range search is used. Specifically,
only the first 5 characters of a SHA-1 password hash are sent to the API. The
validator then locally looks for the full hash in the range returned.

The package also provides a custom authentication backend that wraps the
standard model backend so passwords of existing users can be checked when
they login.


Installation
~~~~~~~~~~~~

.. code-block:: sh

    pip install django-pwned-validator

Modify your `settings.py` to install the app, then add the validator and
the custom authentication backend:

.. code-block:: python

    INSTALLED_APPS = [
        'pwned.apps.PwnedConfig',
        ...
    ]

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'pwned.validators.PwnedValidator',
        },
        ...
    ]

    AUTHENTICATION_BACKENDS = [
        'pwned.backends.PwnedModelBackend',
    ]

We would also suggest removing the `CommonPasswordValidator` as it fills a
very similar role and this validator uses the same help text.


Settings
~~~~~~~~

.. code-block:: python

    PWNED = {
        'ENDPOINT': 'https://api.pwnedpasswords.com/range/',
        'OCCURRENCE_NOTIFY_THRESHOLD': 1, # How many occurrences cause a validation error
        'PREFIX_LENGTH': 5,
        'RECORD_HITS': True,
        'TIMEOUT': 2, # The default is conservative but will cut off some requests; typical is 200ms
        'USER_AGENT': 'github.com/craigloftus/django-pwned-validator',
    }


Compatibility
~~~~~~~~~~~~~
Supports Django 1.11, 2.0, 2.1 and 2.2 on Python 3.5 and 3.6.
