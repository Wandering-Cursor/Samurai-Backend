from django.contrib import admin

from accounts.models import Overseer

from .base_user import BaseUserAdmin


@admin.register(Overseer)
class OverseerAdmin(BaseUserAdmin):
	class Meta:
		model = Overseer
