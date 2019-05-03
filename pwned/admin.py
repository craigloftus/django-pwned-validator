from django.contrib import admin

from .models import PwnedRecord


@admin.register(PwnedRecord)
class PwnedRecordAdmin(admin.ModelAdmin):
    list_display = ('email', 'created', 'count', 'notified',)

