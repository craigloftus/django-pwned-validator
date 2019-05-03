from django.contrib.auth.backends import ModelBackend

from .client import PwnedClient
from .models import PwnedRecord
from .settings import get_config


class PwnedBackendMixin:

    client = PwnedClient

    def authenticate(self, request, username=None, password=None):
        user = super().authenticate(request, username=username, password=password)
        # If authenticated, check supplied password against API
        if user and password:
            pwned_client = self.client()
            count = pwned_client.count_occurrences(password)
            if count and get_config()['RECORD_HITS']:
                PwnedRecord.objects.create(
                    email = user.email,
                    count = count,
                )
        return user


class PwnedModelBackend(PwnedBackendMixin, ModelBackend):
    pass
