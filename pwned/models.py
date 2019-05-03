from django.contrib.auth import get_user_model
from django.db import models


UserModel = get_user_model()


class PwnedRecord(models.Model):
    email = models.EmailField(blank=True)
    count = models.PositiveIntegerField(db_index=True)
    notified = models.BooleanField(db_index=True, default=False)
    created = models.DateTimeField(auto_now_add=True)
