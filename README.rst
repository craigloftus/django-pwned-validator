Django Pwned Passwords Validator
================================

This package provides a password validator for Django that checks submitted
passwords against the `Pwned Passwords API <https://haveibeenpwned.com/API/v2>`_.

To protect the security of the password being checked a range search is used. Specifically,
only the first 5 characters of a SHA-1 password hash are sent to the API. The
validator then locally looks for the full hash in the range returned.

Installation
~~~~~~~~~~~~

.. code-block:: sh

    pip install django-pwned-validator

Modify your `settings.py` to install the app and enable the validator:

.. code-block:: python

    INSTALLED_APPS = [
        'pwned',
        ...
    ]

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'pwned.validators.PwnedValidator',
        },
        ...
    ]


Compatibility
~~~~~~~~~~~~
Supports Django 1.11.x and 2.0 on Python 3.5 and 3.6.
