from django.contrib import admin

from accounts.models import BaseUser


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    exclude = ["password"]

    class Meta:
        model = BaseUser
