Django Pwned Passwords Validator
================================

This package provides a password validator for Django that checks submitted
passwords against the `Pwned Passwords API <https://haveibeenpwned.com/API/v2>`.

To protect the security of the password being checked a range search is used. Specifically,
only the first 5 characters of a SHA-1 password hash are sent to the API. The
validator then locally looks for the full hash in the range returned.
