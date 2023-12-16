from django.contrib import admin

from accounts.models import BaseUser


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
	list_display = [
		"id",
		"email",
		"first_name",
		"last_name",
		"is_active",
		"is_staff",
		"is_superuser",
		"registration_code",
	]
	exclude = [
		"password",
	]

	search_fields = [
		"id",
		"email",
		"first_name",
		"last_name",
		"registration_code",
	]

	class Meta:
		model = BaseUser
